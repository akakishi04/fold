import ast
import hashlib
import inspect
from pathlib import Path
import tempfile
import unittest

import numpy as np

from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as b


class C177Tests(unittest.TestCase):
    def test_01_perfect_order(self):
        r = b.rank_pairs([0, 0, 1, 1], [0., 1., 2., 3.])
        self.assertEqual((r['auc'], r['wins'], r['ties'], r['pairs']), (1, 4, 0, 4))

    def test_02_reverse_order(self):
        r = b.rank_pairs([0, 0, 1, 1], [3., 2., 1., 0.])
        self.assertEqual((r['auc'], r['losses']), (0, 4))

    def test_03_ties_half_credit(self):
        r = b.rank_pairs([0, 0, 1], [1., 1., 1.])
        self.assertEqual((r['auc'], r['ties'], r['pairs']), (.5, 2, 2))

    def test_04_brute_force_agreement(self):
        rng = np.random.default_rng(7)
        for _ in range(30):
            y = np.tile([0, 1], 8); s = rng.integers(-3, 4, len(y))
            expected = sum(float(a > c) + .5 * float(a == c) for a in s[y == 1] for c in s[y == 0]) / 64
            self.assertEqual(b.rank_pairs(y, s)['auc'], expected)

    def test_05_permutation_invariance(self):
        y = np.array([0, 1, 0, 1]); s = np.array([1., 1., 2., 3.]); ids = [2, 3, 1, 0]
        self.assertEqual(b.rank_pairs(y, s), b.rank_pairs(y[ids], s[ids]))

    def test_06_pure_class_auc_is_null(self):
        for v in (0, 1):
            r = b.rank_pairs([v, v], [1., 2.]); self.assertIsNone(r['auc']); self.assertEqual(r['pairs'], 0)

    def test_07_empty_auc_is_null(self):
        r = b.rank_pairs(np.array([], dtype=int), np.array([], dtype=float))
        self.assertEqual(r['n'], 0); self.assertIsNone(r['auc'])

    def test_08_bad_labels(self):
        for y in ([0, 2], [False, True], [0., 1.], [[0, 1]]):
            with self.assertRaises(b.InvalidExecution): b.rank_pairs(y, [0., 1.])

    def test_09_bad_scores(self):
        for s in ([np.nan, 1], [0, np.inf], [1.], [[0, 1]], [False, True]):
            with self.assertRaises(b.InvalidExecution): b.rank_pairs([0, 1], s)

    def test_10_raw_argmax_and_no_mutation(self):
        z = np.array([[1., 1.], [0., 2.], [2., 0.]], dtype=np.float32); old = z.copy()
        np.testing.assert_array_equal(b.raw_margins(z, [0, 1, 0]), [0., 2., -2.])
        np.testing.assert_array_equal(z, old)
        with self.assertRaises(b.InvalidExecution): b.raw_margins(z, [1, 1, 0])

    def test_11_stratum_constant_shift_preserves_order(self):
        y = [0, 0, 1, 1]; s = np.array([1., 3., 2., 3.])
        self.assertEqual(b.rank_pairs(y, s), b.rank_pairs(y, s + 100))

    def test_12_score_sign_has_declared_positive_class(self):
        y = [0, 0, 1, 1]; s = np.array([0., 3., 2., 3.])
        self.assertAlmostEqual(b.rank_pairs(y, s)['auc'] + b.rank_pairs(y, -s)['auc'], 1.)

    def test_13_grouped_pairs_do_not_cross_keys(self):
        r = b.grouped_rank_pairs(['a', 'a', 'b', 'b'], [0, 1, 0, 1], [100., 101., 0., -1.])
        self.assertEqual((r['pairs'], r['wins'], r['losses'], r['auc']), (2, 1, 1, .5))

    def test_14_no_mixed_key_has_no_pairs(self):
        r = b.grouped_rank_pairs(['a', 'b'], [0, 1], [1., 2.])
        self.assertEqual(r['mixed_keys'], 0); self.assertIsNone(r['auc'])

    def test_15_grouped_ties_exact(self):
        r = b.grouped_rank_pairs([('a',)] * 4, [0, 1, 0, 1], [1., 1., 1., 1.])
        self.assertEqual((r['ties'], r['pairs'], r['auc']), (4, 4, .5))

    def test_16_error_exchange_identities(self):
        r = b.transitions([0, 0, 1, 1], [0, 1, 0, 1], [0, 0, 0, 0])
        self.assertEqual([r[k] for k in ('both_correct', 'both_wrong', 'rescued', 'regressed')], [1, 1, 1, 1])
        self.assertEqual(r['to_sufficient'], 2)

    def test_17_error_exchange_additivity(self):
        y = np.array([0, 1, 0, 1, 0, 1]); u = np.array([0, 0, 1, 1, 0, 1]); c = 1 - u
        a = b.transitions(y, u, c); l = b.transitions(y[:3], u[:3], c[:3]); r = b.transitions(y[3:], u[3:], c[3:])
        self.assertEqual(a, {k: l[k] + r[k] for k in a})
        with self.assertRaises(b.InvalidExecution): b.transitions(y, u, c[:-1])

    def test_18_primary_equal_stratum_not_pair_weighted(self):
        a = b.rank_pairs([0, 1], [0., 1.]); z = b.rank_pairs([0, 0, 1, 1], [2., 3., 0., 1.])
        r = b.primary({'1': a, '2': a, '3': z})
        self.assertEqual((r['numerator'], r['denominator']), (2, 3))

    def test_19_primary_cannot_drop_pure_stratum(self):
        a = b.rank_pairs([0, 1], [0., 1.]); z = b.rank_pairs([0], [0.])
        with self.assertRaises(b.InvalidExecution): b.primary({'1': a, '2': a, '3': z})

    def test_20_gate_strict_each_seed(self):
        rows = [dict(seed=s, uniform=dict(primary=dict(numerator=1, denominator=2)),
                     conditional=dict(primary=dict(numerator=3, denominator=5))) for s in b.SEEDS]
        self.assertTrue(b.gate(rows)); rows[1]['conditional']['primary'] = dict(numerator=1, denominator=2)
        self.assertFalse(b.gate(rows)); self.assertFalse(b.gate(rows[:2])); self.assertFalse(b.gate(list(reversed(rows))))

    def test_21_missing_count_uses_presence_not_value(self):
        x = np.zeros((2, 72), dtype=np.int32); x[:, 48:62:4] = 1; x[1, 48] = 0
        np.testing.assert_array_equal(b.missing_counts(x), [0, 1])
        x[0, 48] = 2
        with self.assertRaises(b.InvalidExecution): b.missing_counts(x)

    def test_22_ordering_uses_all_declared_strata_and_groups(self):
        y = np.tile([0, 1], 3); s = np.tile([0., 1.], 3); m = np.repeat([1, 2, 3], 2); g = np.zeros(6, dtype=int)
        r = b.ordering(y, s, g, m, ['a'] * 6)
        self.assertEqual(r['primary']['auc'], 1.); self.assertEqual(set(r['by_missing_count']), {'0', '1', '2', '3', '4'})
        self.assertEqual(r['overall']['pairs'], 9)

    def test_23_manifest_and_no_learning_import(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(), b.MANIFEST_SHA)
        self.assertEqual(b.manifest()['threshold_searches'], 0)
        for node in ast.walk(ast.parse(inspect.getsource(b))):
            if isinstance(node, ast.Import): self.assertFalse(any(n.name.startswith('torch') for n in node.names))
            if isinstance(node, ast.ImportFrom): self.assertFalse((node.module or '').startswith('torch'))
        with self.assertRaises(ValueError): b.blob({'x': float('nan')})

    def test_24_regression_list_appends_one_current_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'tools').mkdir()
            (root/'tools/run_c167.ps1').write_text('\n'.join(f'"tests_lm.test_old{i}"' for i in range(51)), encoding='utf-8')
            names = b.regression_modules(root)
            self.assertEqual(len(names), 61); self.assertEqual(len(set(names)), 61)
            self.assertEqual(names[-1], 'tests_lm.test_v05_c177_frozen_score_order')


if __name__ == '__main__':
    unittest.main()
