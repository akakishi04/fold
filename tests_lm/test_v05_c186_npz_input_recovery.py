"""C186 loader recovery; synthetic full-size NPZ, never official checkpoint scores."""
import ast
from contextlib import ExitStack
import hashlib
import inspect
import io
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import numpy as np
from fold_lm.v05_benchmarks import c186_c185_npz_input as loader
from fold_lm.v05_benchmarks import gate_e_c186_nonadmission_reclassification as c186


def npy_header(*, shape=(2,), dtype='|i1', fortran=False, extra=None, version=(1, 0)):
    obj = dict(descr=dtype, fortran_order=fortran, shape=shape)
    if extra:
        obj.update(extra)
    raw = (repr(obj) + '\n').encode('latin1')
    return b'\x93NUMPY' + bytes(version) + struct.pack('<H' if version == (1, 0) else '<I', len(raw)) + raw


class C186NpzInputRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.path = Path(cls.temp.name) / 'synthetic-c185.npz'
        cls.source = {name: np.zeros(shape, dtype=dtype) for name, shape, dtype in loader.ARRAY_SPECS}
        cls.source['predictions'][..., 1] = -1
        cls.source['logits'].flat[:4] = [-2, 3, 0, 0]
        cls.source['logit_present'].flat[:2] = [True, False]
        cls.source['policy_inputs'].flat[:4] = [7, 4, 1, 1]
        cls.source['row_indices'][:] = np.arange(3712, dtype='<i4')
        cls.source['policy_seeds'][:] = [181001, 181001, 181002, 181002, 181003, 181003, 0, 0]
        cls.source['policy_names'][:] = ['FINAL_ONLY', 'INTERNAL_SEMANTICS'] * 3 + ['MISSING_RULE', 'NEVER_QUERY']
        cls.source['layouts'][:] = [[0, 1, 2, 3], [3, 2, 1, 0]]
        np.savez_compressed(cls.path, **cls.source)
        cls.sha = hashlib.sha256(cls.path.read_bytes()).hexdigest()

    @classmethod
    def tearDownClass(cls):
        cls.source.clear()
        cls.temp.cleanup()

    def synthetic_identity(self):
        """Only tests patch identity; production exposes no hash/size override."""
        stack = ExitStack()
        stack.enter_context(patch.object(loader, 'SOURCE_SHA256', self.sha))
        stack.enter_context(patch.object(loader, 'SOURCE_SERIALIZED_BYTES', self.path.stat().st_size))
        return stack

    def header_ok(self, header, size=None):
        return loader._header(io.BytesIO(header), (2,), '|i1', len(header) + 2 if size is None else size)

    def test_01_registered_payload_and_bounds(self):
        self.assertEqual(loader.PAYLOAD_BYTES, 70810728)
        self.assertEqual(loader.MAX_EXPANDED_BYTES, 70843592)
        self.assertGreater(loader.PAYLOAD_BYTES, 32 * 1024 * 1024)
        self.assertEqual(loader.SOURCE_SERIALIZED_BYTES, 1716066)
        self.assertEqual(loader.SOURCE_SHA256, 'e597baf0dfa76b34a32dcb2a0445640aaeb21bb99a22af25c26c854ef3eabcf8')

    def test_02_full_registered_shapes_load_above_old_bound(self):
        with zipfile.ZipFile(self.path) as archive:
            self.assertGreater(sum(i.file_size for i in archive.infolist()), 32 * 1024 * 1024)
        with self.synthetic_identity():
            actual = loader.load_c185_predictions(self.path)
        self.assertEqual(set(actual), set(self.source))
        for name, shape, dtype in loader.ARRAY_SPECS:
            self.assertEqual(actual[name].shape, shape)
            self.assertEqual(actual[name].dtype.str, dtype)
            self.assertTrue(np.array_equal(actual[name], self.source[name]), name)
        self.assertEqual(sum(a.nbytes for a in actual.values()), loader.PAYLOAD_BYTES)
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), self.sha)

    def test_03_preflight_never_materializes(self):
        with self.synthetic_identity(), patch.object(np.lib.format, 'read_array', side_effect=AssertionError('allocated')):
            report = loader.inspect_c185_predictions(self.path)
        self.assertEqual(len(report['members']), 8)
        self.assertEqual(report['payload_bytes'], 70810728)

    def test_04_unaccepted_compressed_size_rejected(self):
        with patch.object(zipfile, 'ZipFile', side_effect=AssertionError('opened before identity')):
            with self.assertRaisesRegex(ValueError, 'compressed size'):
                loader.load_c185_predictions(self.path)

    def test_05_same_size_wrong_hash_rejected(self):
        with self.synthetic_identity(), patch.object(loader, 'SOURCE_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'hash'):
                loader.inspect_c185_predictions(self.path)

    def test_06_header_allows_v1_and_v2(self):
        for version in ((1, 0), (2, 0)):
            h = npy_header(version=version)
            self.assertEqual(self.header_ok(h), len(h))

    def test_07_bad_magic_rejected(self):
        h = npy_header()
        with self.assertRaisesRegex(ValueError, 'magic'):
            self.header_ok(b'notnpy!!' + h[8:])

    def test_08_unregistered_version_rejected(self):
        h = npy_header()
        with self.assertRaisesRegex(ValueError, 'version'):
            self.header_ok(h[:6] + b'\x03\x00' + h[8:])

    def test_09_header_length_bounded_before_read(self):
        h = b'\x93NUMPY\x02\x00' + struct.pack('<I', 2**31)
        with self.assertRaisesRegex(ValueError, 'header exceeds'):
            self.header_ok(h)

    def test_10_truncated_header_rejected(self):
        with self.assertRaisesRegex(ValueError, 'truncated'):
            self.header_ok(npy_header()[:-2])

    def test_11_object_dtype_rejected(self):
        with self.assertRaisesRegex(ValueError, 'dtype'):
            self.header_ok(npy_header(dtype='|O'))

    def test_12_wrong_numeric_dtype_rejected(self):
        with self.assertRaisesRegex(ValueError, 'dtype'):
            self.header_ok(npy_header(dtype='<i8'))

    def test_13_huge_shape_rejected_before_allocation(self):
        with self.assertRaisesRegex(ValueError, 'shape'):
            self.header_ok(npy_header(shape=(2**60,)))

    def test_14_boolean_dimension_rejected(self):
        with self.assertRaisesRegex(ValueError, 'shape'):
            self.header_ok(npy_header(shape=(True,)))

    def test_15_fortran_order_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Fortran'):
            self.header_ok(npy_header(fortran=True))

    def test_16_extra_header_field_rejected(self):
        with self.assertRaisesRegex(ValueError, 'header fields'):
            self.header_ok(npy_header(extra={'payload': 'unregistered'}))

    def test_17_payload_length_mismatch_rejected(self):
        h = npy_header()
        for delta in (-1, 1):
            with self.assertRaisesRegex(ValueError, 'payload size'):
                self.header_ok(h, len(h) + 2 + delta)

    def test_18_missing_or_extra_member_rejected(self):
        with zipfile.ZipFile(self.path) as archive:
            original = archive.infolist()
            for infos in (original[:-1], original + [zipfile.ZipInfo('extra.npy')]):
                with patch.object(archive, 'infolist', return_value=infos):
                    with self.assertRaisesRegex(ValueError, 'member'):
                        loader._inspect_archive(archive)

    def test_19_duplicate_member_rejected(self):
        with zipfile.ZipFile(self.path) as archive:
            infos = archive.infolist()
            with patch.object(archive, 'infolist', return_value=infos[:-1] + [infos[0]]):
                with self.assertRaisesRegex(ValueError, 'duplicate'):
                    loader._inspect_archive(archive)

    def test_20_total_expanded_bound_enforced(self):
        with zipfile.ZipFile(self.path) as archive:
            infos = archive.infolist()
            infos[0].file_size = loader.MAX_EXPANDED_BYTES + 1
            with patch.object(archive, 'infolist', return_value=infos):
                with self.assertRaisesRegex(ValueError, 'expanded archive'):
                    loader._inspect_archive(archive)

    def test_21_per_member_bound_enforced(self):
        with zipfile.ZipFile(self.path) as archive:
            infos = archive.infolist()
            infos[0].file_size += 8192
            with patch.object(archive, 'infolist', return_value=infos):
                with self.assertRaisesRegex(ValueError, 'expanded member'):
                    loader._inspect_archive(archive)

    def test_22_encrypted_member_rejected(self):
        with zipfile.ZipFile(self.path) as archive:
            infos = archive.infolist()
            infos[0].flag_bits |= 1
            with patch.object(archive, 'infolist', return_value=infos):
                with self.assertRaisesRegex(ValueError, 'encrypted'):
                    loader._inspect_archive(archive)

    def test_23_allow_pickle_false_and_no_override_interface(self):
        self.assertEqual(list(inspect.signature(loader.load_c185_predictions).parameters), ['path'])
        self.assertEqual(list(inspect.signature(loader.inspect_c185_predictions).parameters), ['path'])
        source = inspect.getsource(loader._consume)
        tree = ast.parse(source)
        read_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Attribute) and n.func.attr == 'read_array']
        self.assertEqual(len(read_calls), 1)
        self.assertTrue(any(k.arg == 'allow_pickle' and isinstance(k.value, ast.Constant)
                            and k.value.value is False for k in read_calls[0].keywords))

    def test_24_same_c186_manifest_and_explicit_loader_dispatch(self):
        self.assertEqual(c186.digest(c186.manifest()), '0cbe7212e5bafd9fc52f3f315d2d4732afaca6eb11940c6fa16ac58aeb336edc')
        self.assertIn('load_c185_predictions(', inspect.getsource(c186.run))
        self.assertNotIn('audit.load_npz(', inspect.getsource(c186.run))
        self.assertIn('inspect_c185_predictions(', inspect.getsource(c186.precheck))
        self.assertEqual(len(c186.OWN), 7)
        self.assertEqual(c186.ATOL, 1e-6)
        self.assertEqual(len(c186.expected_order()), 80)


if __name__ == '__main__':
    unittest.main()
