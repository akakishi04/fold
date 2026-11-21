"""C184 adapter tests use synthetic inputs only; no official checkpoint scores."""
import copy
import hashlib
import inspect
import itertools
import unittest

import torch
from fold_lm.v05_benchmarks import gate_e_c184_canonical_fact_indices as b

SHAPES = ((((0, 1), 2), 3), ((0, (1, 2)), 3), ((0, 1), (2, 3)),
          (0, ((1, 2), 3)), (0, (1, (2, 3))))


def fixture(shape=SHAPES[2], visible=(1, None, 0, 1), neg=(0, 1, 0, 1)):
    nodes = []
    def emit(s):
        if type(s) is int:
            nodes.append([1, 1, s+1, 0, 0, neg[s]])
        else:
            left, right = emit(s[0]), emit(s[1])
            nodes.append([1, 2+(len(nodes) % 2), 0, left, right, 0])
        return len(nodes)
    emit(shape)
    facts = [[1, 1 if v is None else 2, int(v is not None), 0 if v is None else v] for v in visible]
    return torch.tensor([[7, 4, 1, 0]+sum(nodes, [])+sum(facts, [])+[12, 4, 1, 1, 1, 1, 1, 1, 0, 7]], dtype=torch.int32)


def independent_rename(raw, p):
    rows = raw.tolist(); out = copy.deepcopy(rows)
    for old, new in zip(rows, out):
        for i in range(7):
            at = 4+6*i
            if old[at+1] == 1: new[at+2] = p[old[at+2]-1]+1
        for i, j in enumerate(p): new[46+4*j:50+4*j] = old[46+4*i:50+4*i]
    return torch.tensor(out, dtype=torch.int32)


def completion_results(row):
    """Independent full binary completion evaluation, TEST ONLY."""
    facts = [row[46+4*i:50+4*i] for i in range(4)]
    result = set()
    for assignment in itertools.product((0, 1), repeat=4):
        if any(f[2] and f[3] != assignment[i] for i, f in enumerate(facts)): continue
        values = []
        for i in range(7):
            _, kind, fact, left, right, neg = row[4+6*i:10+6*i]
            if kind == 1: v = assignment[fact-1] ^ neg
            elif kind == 2: v = values[left-1] & values[right-1]
            else: v = values[left-1] | values[right-1]
            values.append(v)
        result.add(values[-1])
    return result


def passing_gate():
    checks = [dict(permutation_index=j, rows=51840 if j == 0 else 9396,
        canonical_mismatches=0, roundtrip_mismatches=0, idempotence_mismatches=0, mutated_input_rows=0) for j in range(24)]
    rows = [dict(seed=s, arm=a, permutation_index=j, n=9396, errors=0,
                 decision_flips=0, max_abs_logit_difference=0.0)
            for j in range(1, 24) for s in b.SEEDS for a in b.ARMS]
    return rows, checks


class C184Tests(unittest.TestCase):
    def test_01_identity(self):
        x = fixture(); out, mapping = b.canonicalize(x)
        self.assertTrue(torch.equal(x, out)); self.assertEqual(mapping.tolist(), [[0, 1, 2, 3]])

    def test_02_first_occurrence_not_numeric_sort(self):
        x = fixture(); changed = independent_rename(x, (2, 3, 1, 0))
        out, mapping = b.canonicalize(changed)
        self.assertTrue(torch.equal(out, x)); self.assertEqual(mapping.tolist(), [[2, 3, 1, 0]])

    def test_03_roundtrip_all_permutations(self):
        for p in b.PERMUTATIONS:
            x = independent_rename(fixture(), p); out, mapping = b.canonicalize(x)
            self.assertTrue(torch.equal(b.restore_input(out, mapping), x))

    def test_04_idempotence(self):
        a, _ = b.canonicalize(independent_rename(fixture(), (3, 1, 0, 2)))
        c, m = b.canonicalize(a)
        self.assertTrue(torch.equal(c, a)); self.assertEqual(m.tolist(), [[0, 1, 2, 3]])

    def test_05_complete_numeric_records_move(self):
        x = fixture(visible=(None, 0, 1, 0)); out, mapping = b.canonicalize(independent_rename(x, (3, 2, 1, 0)))
        self.assertEqual(out[:, 46:62].tolist(), x[:, 46:62].tolist())

    def test_06_zero_and_unknown_remain_distinct(self):
        a, _ = b.canonicalize(fixture(visible=(0, None, 1, 1)))
        c, _ = b.canonicalize(fixture(visible=(None, 0, 1, 1)))
        self.assertFalse(torch.equal(a, c))

    def test_07_negation_is_not_evaluated(self):
        x = independent_rename(fixture(), (3, 2, 1, 0)); out, _ = b.canonicalize(x)
        self.assertTrue(torch.equal(x[:, 9:46:6], out[:, 9:46:6]))

    def test_08_operators_are_not_simplified(self):
        x = fixture(); out, _ = b.canonicalize(x)
        self.assertTrue(torch.equal(x[:, 5:46:6], out[:, 5:46:6]))

    def test_09_topology_retained(self):
        for shape in SHAPES:
            x = independent_rename(fixture(shape), (3, 1, 0, 2)); out, _ = b.canonicalize(x)
            self.assertTrue(torch.equal(x[:, 4:46].reshape(1, 7, 6)[:, :, 3:5], out[:, 4:46].reshape(1, 7, 6)[:, :, 3:5]))

    def test_10_context_transport(self):
        x = fixture(); x[:, 62:] = torch.arange(10); out, _ = b.canonicalize(x)
        self.assertTrue(torch.equal(x[:, 62:], out[:, 62:])); self.assertTrue(torch.equal(x[:, :4], out[:, :4]))

    def test_11_no_input_or_mapping_mutation(self):
        x = fixture(); before = x.clone(); out, m = b.canonicalize(x); mm = m.clone()
        b.restore_input(out, m); out[0, 62] = 0
        self.assertTrue(torch.equal(x, before)); self.assertTrue(torch.equal(m, mm))

    def test_12_no_label_or_checkpoint_interface(self):
        self.assertEqual(list(inspect.signature(b.canonicalize).parameters), ['raw'])
        self.assertEqual(list(inspect.signature(b.restore_input).parameters), ['canonical', 'to_input'])

    def test_13_width_dtype_and_cpu(self):
        for x in (fixture().float(), fixture().long(), fixture()[:, :71], fixture().flatten()):
            with self.assertRaises(ValueError): b.canonicalize(x)

    def test_14_empty(self):
        with self.assertRaises(ValueError): b.canonicalize(torch.empty(0, 72, dtype=torch.int32))

    def test_15_negative_field(self):
        x = fixture(); x[0, 62] = -1
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_16_integer_precision_range(self):
        x = fixture(); x[0, 62] = 2**24
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_17_unknown_reference(self):
        x = fixture(); x[0, 6] = 5
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_18_repeated_reference_out_of_scope(self):
        x = fixture(); x[0, 12] = 1
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_19_forward_child(self):
        x = fixture(); x[0, 19] = 7
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_20_disconnected_tree(self):
        x = fixture(); x[0, 44] = 3
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_21_hidden_payload_rejected(self):
        x = fixture(); x[0, 53] = 1
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_22_unsupported_fact_status_rejected(self):
        x = fixture(); x[0, 47] = 3
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_23_noncanonical_leaf_children(self):
        x = fixture(); x[0, 7] = 1
        with self.assertRaises(ValueError): b.canonicalize(x)

    def test_24_inverse_requires_bijection(self):
        for m in (torch.tensor([[0, 0, 2, 3]]), torch.tensor([[0, 1, 2, 4]]), torch.arange(4)[None].float()):
            with self.assertRaises(ValueError): b.restore_input(fixture(), m)

    def test_25_inverse_requires_canonical_order(self):
        x = independent_rename(fixture(), (3, 2, 1, 0))
        with self.assertRaises(ValueError): b.restore_input(x, torch.arange(4)[None])

    def test_26_batched_maps_keep_distinct_rows(self):
        p = ((2, 3, 1, 0), (3, 2, 0, 1))
        x = torch.cat([independent_rename(fixture(visible=(1, None, 0, i)), q) for i, q in enumerate(p)])
        out, m = b.canonicalize(x)
        self.assertEqual(m.tolist(), [list(q) for q in p]); self.assertTrue(torch.equal(b.restore_input(out, m), x))

    def test_27_finite_contract_mismatch_measured(self):
        x = fixture(); ref = x.clone(); ref[0, 71] = 6
        _, _, c = b.normalization_check(x, ref)
        self.assertEqual(c['canonical_mismatches'], 1); self.assertEqual(c['roundtrip_mismatches'], 0)
        r, checks = passing_gate(); checks[0]['canonical_mismatches'] = 1
        self.assertFalse(b.gate(r, checks))

    def test_28_single_candidate_error_fails(self):
        r, c = passing_gate(); self.assertTrue(b.gate(r, c)); r[1]['errors'] = 1
        self.assertFalse(b.gate(r, c))

    def test_29_control_errors_allowed_but_not_changed_decisions(self):
        r, c = passing_gate(); r[0]['errors'] = 3000; self.assertTrue(b.gate(r, c))
        r[0]['decision_flips'] = 1; self.assertFalse(b.gate(r, c))

    def test_30_coverage_nonfinite_and_tolerance(self):
        r, c = passing_gate(); self.assertFalse(b.gate(r[::-1], c)); self.assertFalse(b.gate(r, c[:-1]))
        for d in (float('nan'), float('inf'), -1., 1.01e-6):
            q = copy.deepcopy(r); q[1]['max_abs_logit_difference'] = d; self.assertFalse(b.gate(q, c))
        r[1]['max_abs_logit_difference'] = 1e-6; self.assertTrue(b.gate(r, c))

    def test_31_manifest_and_output_contract(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(), b.MANIFEST_SHA)
        self.assertEqual(len(b.OWN), 4); self.assertEqual(len(b.OUTPUTS), 5)
        self.assertEqual(b.manifest()['normalized_predictions'], 6*23*9396)
        self.assertEqual(b.manifest()['normalizer_row_calls_including_idempotence'], 2*(51840+23*9396))
        with self.assertRaises(ValueError): b.blob({'x': float('nan')})

    def test_32_independent_completions_for_all_9720_renamings(self):
        rows = torch.cat([fixture(shape, visible, neg=tuple((i+si)%2 for i in range(4)))
                          for si, shape in enumerate(SHAPES)
                          for visible in itertools.product((None, 0, 1), repeat=4)])
        expected = [completion_results(r) for r in rows.tolist()]
        count = 0
        for p in b.PERMUTATIONS:
            changed = independent_rename(rows, p); out, mapping = b.canonicalize(changed)
            self.assertTrue(torch.equal(out, rows)); self.assertTrue(torch.equal(b.restore_input(out, mapping), changed))
            self.assertEqual([completion_results(r) for r in changed.tolist()], expected)
            count += len(changed)
        self.assertEqual(count, 9720)


if __name__ == '__main__': unittest.main()
