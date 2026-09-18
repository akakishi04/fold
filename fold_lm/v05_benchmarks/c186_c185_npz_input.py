"""C186 execution repair: bounded loader for the already accepted C185 NPZ.

C175's generic 32 MiB ceiling is NOT changed. The fixed eight-array C185 schema
needs 70,810,728 payload bytes. Verify the accepted compressed file identity and
ALL bounded NPY headers before allocating any array. No policy/model/score change.
"""
from __future__ import annotations

import ast
import hashlib
import math
import os
from pathlib import Path
import struct
import zipfile

import numpy as np

SCHEMA = 'c186-c185-npz-input-v1'
SOURCE_SHA256 = 'e597baf0dfa76b34a32dcb2a0445640aaeb21bb99a22af25c26c854ef3eabcf8'
SOURCE_SERIALIZED_BYTES = 1716066
DIMS = (8, 2, 2, 3712, 2)
ARRAY_SPECS = (
    ('predictions', DIMS, '|i1'),
    ('logits', DIMS + (2,), '<f4'),
    ('logit_present', DIMS, '|b1'),
    ('policy_inputs', DIMS + (72,), '<i4'),
    ('row_indices', (3712,), '<i4'),
    ('policy_seeds', (8,), '<i4'),
    ('policy_names', (8,), '<U18'),
    ('layouts', (2, 4), '|i1'),
)
MAX_HEADER_BYTES = 4096
# NPY v1/v2 framing is at most 12 bytes; bounds are derived from the schema.
PAYLOAD_BYTES = sum(math.prod(shape) * np.dtype(dtype).itemsize
                    for _, shape, dtype in ARRAY_SPECS)
MAX_EXPANDED_BYTES = PAYLOAD_BYTES + len(ARRAY_SPECS) * (12 + MAX_HEADER_BYTES)


def _require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError('C185 NPZ: ' + message)


def _header(stream, shape: tuple[int, ...], dtype: str, member_size: int) -> int:
    """Bounded parsing only; no NumPy array allocation or pickle deserialization."""
    prefix = stream.read(8)
    _require(len(prefix) == 8 and prefix[:6] == b'\x93NUMPY', 'invalid NPY magic')
    version = tuple(prefix[6:])
    _require(version in ((1, 0), (2, 0)), 'unsupported NPY version')
    n = 2 if version == (1, 0) else 4
    length = stream.read(n)
    _require(len(length) == n, 'truncated NPY length')
    header_size = struct.unpack('<H' if n == 2 else '<I', length)[0]
    _require(0 < header_size <= MAX_HEADER_BYTES, 'NPY header exceeds bound')
    raw = stream.read(header_size)
    _require(len(raw) == header_size and raw.endswith(b'\n'), 'truncated/invalid NPY header')
    try:
        header = ast.literal_eval(raw.decode('latin1').strip())
    except (ValueError, SyntaxError, RecursionError) as exc:
        raise ValueError('C185 NPZ: invalid NPY header literal') from exc
    _require(type(header) is dict and set(header) == {'descr', 'fortran_order', 'shape'},
             'unexpected NPY header fields')
    # Checking the literal descriptor before constructing an array excludes object,
    # structured, endian-changing and unbounded string/void dtypes.
    _require(type(header['descr']) is str and header['descr'] == dtype, 'wrong dtype')
    actual_shape = header['shape']
    _require(type(actual_shape) is tuple and all(type(i) is int for i in actual_shape)
             and actual_shape == shape, 'wrong shape')
    _require(header['fortran_order'] is False, 'Fortran order not registered')
    offset = 8 + n + header_size
    _require(member_size == offset + math.prod(shape) * np.dtype(dtype).itemsize,
             'NPY header/payload size disagreement')
    return offset


def _inspect_archive(archive: zipfile.ZipFile) -> dict:
    """Validate the exact eight members and every header before materialization."""
    infos = archive.infolist()
    wanted = {name + '.npy' for name, _, _ in ARRAY_SPECS}
    names = [i.filename for i in infos]
    _require(len(names) == len(wanted) and len(set(names)) == len(names)
             and set(names) == wanted, 'missing/extra/duplicate NPZ member')
    expanded = sum(i.file_size for i in infos)
    _require(expanded <= MAX_EXPANDED_BYTES, 'expanded archive exceeds schema bound')
    entries = {i.filename: i for i in infos}
    members = []
    for name, shape, dtype in ARRAY_SPECS:
        info = entries[name + '.npy']
        size = math.prod(shape) * np.dtype(dtype).itemsize
        _require(not info.is_dir() and not (info.flag_bits & 1)
                 and info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                 'unsupported/encrypted member')
        _require(size + 10 <= info.file_size <= size + 12 + MAX_HEADER_BYTES,
                 'expanded member exceeds schema bound')
        with archive.open(info) as stream:
            offset = _header(stream, shape, dtype, info.file_size)
        members.append(dict(name=name, shape=list(shape), dtype=dtype,
                            payload_bytes=size, npy_header_bytes=offset))
    return dict(schema=SCHEMA, sha256=SOURCE_SHA256,
                serialized_bytes=SOURCE_SERIALIZED_BYTES, payload_bytes=PAYLOAD_BYTES,
                expanded_bytes=expanded, expanded_limit=MAX_EXPANDED_BYTES, members=members)


def _consume(path: Path, *, materialize: bool):
    """Hash and parse on one open descriptor; no size override or fallback path."""
    with Path(path).open('rb') as stream:
        _require(os.fstat(stream.fileno()).st_size == SOURCE_SERIALIZED_BYTES,
                 'compressed size does not match accepted artifact')
        _require(hashlib.file_digest(stream, 'sha256').hexdigest() == SOURCE_SHA256,
                 'hash does not match accepted artifact')
        stream.seek(0)
        with zipfile.ZipFile(stream) as archive:
            report = _inspect_archive(archive)
            result = {}
            if materialize:
                for name, shape, dtype in ARRAY_SPECS:
                    with archive.open(name + '.npy') as member:
                        array = np.lib.format.read_array(
                            member, allow_pickle=False, max_header_size=MAX_HEADER_BYTES)
                        _require(array.shape == shape and array.dtype.str == dtype
                                 and array.flags.c_contiguous, 'loaded array schema disagreement')
                        _require(member.read(1) == b'', 'trailing NPY data')
                    result[name] = array
                _require(sum(a.nbytes for a in result.values()) == PAYLOAD_BYTES,
                         'loaded payload accounting disagreement')
        stream.seek(0)
        _require(os.fstat(stream.fileno()).st_size == SOURCE_SERIALIZED_BYTES
                 and hashlib.file_digest(stream, 'sha256').hexdigest() == SOURCE_SHA256,
                 'artifact changed while reading')
    return result if materialize else report


def inspect_c185_predictions(path: Path) -> dict:
    """Pre-regression check: accepted bytes plus full schema, without array allocation."""
    return _consume(path, materialize=False)


def load_c185_predictions(path: Path) -> dict[str, np.ndarray]:
    """Materialize only the accepted C185 arrays, preserving every stored value."""
    return _consume(path, materialize=True)
