"""C281 behavioral contracts. Parent archives are fixtures in unit tests, real in runtime Validate."""
import ast
import contextlib
import copy
import hashlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import torch
from fold_lm.v05_benchmarks import model_c281_saved_support_transition_audit as b


def sync(metrics):
    for m in metrics:
        for task in b.PROFILES:
            tm = m[task]
            for c in tm["cells"]:
                c["passed"] = all(c[k] >= v for k, v in b.THRESHOLDS.items() if k != "two_order_accuracy")
            for c in tm["two_order"]:
                c["passed"] = c["accuracy"] >= b.THRESHOLDS["two_order_accuracy"]
            tm["passed"] = all(c["passed"] for c in tm["cells"] + tm["two_order"])
        m["passed"] = m["two_char"]["passed"] and m["triple"]["passed"]
    return metrics


def fail_answer(cell):
    n = cell["rows"]
    cell.update(correct=n - 2, accuracy=(n - 2) / n, query_pair_accuracy=(n - 2) / n)


def fixture(accepted=True):
    metrics = []
    for seed in b.SEEDS:
        for arm in b.ARMS:
            m = dict(seed=seed, arm=arm)
            for task in b.PROFILES:
                cells, orders = [], []
                for kind, _, split, profile, lang, entities, perm in sorted(b.expected_keys(task)):
                    n = 16 if split == "TRAIN" else 8
                    common = dict(split=split, profile=profile, language=lang, entities=list(entities), accuracy=1.)
                    if kind == "answer_cell":
                        cells.append(dict(**common, permutation=list(perm), rows=n, correct=n, pairs=n // 2,
                                          collapsed_pairs=0, query_pair_accuracy=1., evidence_drop=.5, query_drop=.5))
                    else:
                        orders.append(dict(**common, groups=n, both_correct=n))
                if accepted and (task == "triple" or seed == 280004):
                    fail_answer(next(c for c in cells if c["split"] == "TRAIN"))
                m[task] = dict(cells=cells, two_order=orders)
            metrics.append(m)
    return sync(metrics)


def target(metrics, arm=1, profile="shared_suffix2", split="TRAIN"):
    return next(c for c in metrics[arm]["triple"]["cells"] if c["profile"] == profile and c["split"] == split)


def parent_payload(metrics):
    _, s = b.analyze(metrics)
    rr = s["parent_results"]
    vs = dict(seed_results=rr, candidate_gate=False, all_replays=True, all_pairs_matched=True)
    for out, field in (("seed_pass_counts", "passed"), ("two_char_pass_counts", "two_char_pass"), ("triple_pass_counts", "triple_pass")):
        vs[out] = {a: sum(r[field] for r in rr if r["arm"] == a) for a in b.ARMS}
    return dict(commit_sha=b.PARENT_EXECUTION, status="FAIL", source_blobs={b.PARENT_SOURCE: b.PARENT_BLOB},
                validation_summary=vs, artifacts=[dict(file=n, sha256=v[0], serialized_bytes=v[1]) for n, v in b.PARENT_ARTIFACTS.items()])


def protection():
    pins = {n: "b" * 40 for n in b.OWN}
    pins[b.PARENT_SOURCE] = b.PARENT_BLOB
    while len(pins) < b.manifest()["source_pins"]:
        pins["fixture/source/" + str(len(pins))] = "b" * 40
    inputs = {"fixture/input/" + str(i): "a" * 64 for i in range(b.manifest()["protected_inputs"])}
    return pins, inputs


def result_fixture():
    _, s = b.analyze(fixture())
    pins, inputs = protection()
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, status="PASS", commit_sha="f" * 40,
                diagnostic_execution_valid=True, capability_gate_applicable=False, gate_f_candidate=False,
                production_adoption=False, source_blobs=pins, input_sha256=inputs,
                artifacts=[dict(file=n) for n in b.OUTPUTS], validation_summary=s)


class FakeAudit:
    @staticmethod
    def sha(path):
        p = Path(path)
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a" * 64

    @staticmethod
    def git(root, *args):
        if args[:1] == ("rev-parse",):
            return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[:1] == ("branch",):
            return b"feat/sft-target-loss\n"
        return b""

    @staticmethod
    def read_json(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))

    @staticmethod
    def safe_child(root, name):
        return Path(root) / name


class C281Tests(unittest.TestCase):
    def test_01_sealed_manifest_really_passes(self):
        b.validate_seal()
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)

    def test_02_bad_and_mismatched_seals_really_fail(self):
        for seal in ("UNSEALED", "0" * 64, "F" * 64):
            with self.subTest(seal=seal), patch.object(b, "MANIFEST_SHA", seal):
                with self.assertRaises(ValueError):
                    b.validate_seal()

    def test_03_complete_grid_and_denominators(self):
        report, s = b.analyze(fixture())
        self.assertEqual((len(report["records"]), s["paired_records"]), (2160, 1080))
        v = s["primary"]["triple_all"]
        self.assertEqual(v["criteria"]["accuracy"]["evaluable"], 360)
        self.assertEqual(v["criteria"]["two_order_accuracy"]["evaluable"], 180)
        self.assertEqual(v["totals"][b.ARMS[0]]["rows"], 4320)

    def test_04_duplicate_answer_rejected(self):
        m = fixture(); m[0]["triple"]["cells"].append(copy.deepcopy(m[0]["triple"]["cells"][0]))
        with self.assertRaises(ValueError): b.analyze(m)

    def test_05_missing_answer_rejected(self):
        m = fixture(); m[0]["triple"]["cells"].pop()
        with self.assertRaises(ValueError): b.analyze(m)

    def test_06_unknown_profile_rejected(self):
        m = fixture(); m[0]["triple"]["cells"][0]["profile"] = "unknown"
        with self.assertRaises(ValueError): b.analyze(m)

    def test_07_duplicate_order_rejected(self):
        m = fixture(); m[0]["triple"]["two_order"].append(copy.deepcopy(m[0]["triple"]["two_order"][0]))
        with self.assertRaises(ValueError): b.analyze(m)

    def test_08_cell_order_does_not_change_report(self):
        m = fixture(); expected = b.analyze(m)
        for r in m:
            for task in b.PROFILES:
                r[task]["cells"].reverse(); r[task]["two_order"].reverse()
        self.assertEqual(b.analyze(m), expected)

    def test_09_nonfinite_metric_rejected(self):
        for value in (float("nan"), float("inf")):
            m = fixture(); m[0]["triple"]["cells"][0]["accuracy"] = value
            with self.assertRaises(ValueError): b.analyze(m)

    def test_10_boolean_is_not_numeric_metric(self):
        m = fixture(); m[0]["triple"]["cells"][0]["accuracy"] = True
        with self.assertRaises(ValueError): b.analyze(m)

    def test_11_correct_count_mismatch_rejected(self):
        m = fixture(); m[0]["triple"]["cells"][0]["correct"] -= 1
        with self.assertRaises(ValueError): b.analyze(m)

    def test_12_impossible_or_fractional_blind_accuracy_rejected(self):
        for drop in (-.25, .31):
            m = fixture(False); target(m)["evidence_drop"] = drop; sync(m)
            with self.assertRaises(ValueError): b.analyze(m)

    def test_13_answer_pass_mismatch_rejected(self):
        m = fixture(); m[0]["triple"]["cells"][0]["passed"] = False
        with self.assertRaises(ValueError): b.analyze(m)

    def test_14_order_pass_mismatch_rejected(self):
        m = fixture(); m[0]["triple"]["two_order"][0]["passed"] = False
        with self.assertRaises(ValueError): b.analyze(m)

    def test_15_task_pass_mismatch_rejected(self):
        m = fixture(); m[0]["two_char"]["passed"] = False
        with self.assertRaises(ValueError): b.analyze(m)

    def test_16_whole_pass_mismatch_rejected(self):
        m = fixture(); m[0]["passed"] = True
        with self.assertRaises(ValueError): b.analyze(m)

    def test_17_model_identity_order_required(self):
        m = fixture(); m[0], m[1] = m[1], m[0]
        with self.assertRaises(ValueError): b.analyze(m)

    def test_18_integer_ratio_boundary(self):
        self.assertEqual(b.integer_ratio(.875, 8, "boundary"), 7)
        with self.assertRaises(ValueError): b.integer_ratio(.9, 8, "noninteger")

    def test_19_rescue_direction(self):
        m = fixture(False); target(m, 0)["evidence_drop"] = 0.; sync(m)
        _, s = b.analyze(m); c = s["primary"]["triple_all"]["criteria"]["evidence_drop"]
        self.assertEqual((c["rescued"], c["introduced"], c["candidate_minus_control"]), (1, 0, -1))

    def test_20_net_zero_does_not_hide_new_failure(self):
        m = fixture(False)
        target(m, 0, split="TRAIN")["evidence_drop"] = 0.
        target(m, 1, split="HOLDOUT")["evidence_drop"] = 0.
        _, s = b.analyze(sync(m)); c = s["primary"]["triple_all"]["criteria"]["evidence_drop"]
        self.assertEqual((c["rescued"], c["introduced"], c["candidate_minus_control"]), (1, 1, 0))

    def test_21_mask_only_and_answer_involving_separate(self):
        m = fixture(False); target(m)["evidence_drop"] = 0.
        fail_answer(target(m, split="HOLDOUT")); sync(m)
        _, s = b.analyze(m); totals = s["primary"]["triple_all"]["totals"][b.ARMS[1]]
        self.assertEqual((totals["mask_only_cells"], totals["answer_involving_cells"]), (1, 1))

    def test_22_discrete_blind_accuracy_reconstruction(self):
        m = fixture(False); target(m)["evidence_drop"] = .25; sync(m)
        p, _ = b.analyze(m)
        r = next(r for r in p["records"] if r["kind"] == "answer_cell" and r["evidence_drop"] == .25)
        self.assertEqual((r["evidence_blind_accuracy"], r["evidence_blind_correct"]), (.75, 12))

    def test_23_suffix_holdout_table_has_exact_scope(self):
        _, s = b.analyze(fixture())
        v = s["primary"]["shared_suffix2_holdout"]
        self.assertEqual(v["paired_records"], 90)
        self.assertEqual(v["totals"][b.ARMS[0]]["rows"], 480)

    def test_24_seed_partition_is_additive_not_exclusion(self):
        _, s = b.analyze(fixture()); p = s["primary"]
        for c in b.THRESHOLDS:
            for key in ("evaluable", "rescued", "introduced", "both_fail", "both_pass"):
                self.assertEqual(p["triple_all"]["criteria"][c][key],
                                 p["triple_seed280004"]["criteria"][c][key] + p["triple_other_seeds"]["criteria"][c][key])
        self.assertEqual(set(s["per_seed_triple"]), set(map(str, b.SEEDS)))

    def test_25_parent_loader_hashes_dispatch_and_neural_block(self):
        m = fixture(); payload = parent_payload(m)
        paths = [(Path("/c281-fixture") / str(i) / "summary.json").resolve() for i in range(7)]
        sha_map = dict(zip(map(str, paths), b.SUMMARY_SHAS, strict=True))
        audit = SimpleNamespace(sha=lambda p: sha_map[str(p)])
        parent = SimpleNamespace(verify_artifacts=Mock(return_value=(payload, m)), validate_result=Mock())
        with patch.object(b, "context", return_value=(parent, None, audit)):
            b.load_parent(paths)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent, *paths[1:], b.PARENT_EXECUTION)
            for p in paths:
                old = sha_map[str(p)]; sha_map[str(p)] = "0" * 64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); sha_map[str(p)] = old
            parent.verify_artifacts.side_effect = lambda *a: torch.nn.Identity()(torch.zeros(1))
            with self.assertRaisesRegex(RuntimeError, "forbids neural"): b.load_parent(paths)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]), 1.)

    def test_26_missing_direct_parent_pin_rejected(self):
        p = parent_payload(fixture()); b.validate_parent(p)
        del p["source_blobs"][b.PARENT_SOURCE]
        with self.assertRaisesRegex(ValueError, "source pin"): b.validate_parent(p)

    def test_27_zero_workload_and_scope_enforced(self):
        p = result_fixture(); b.validate_result(p)
        for k in b.ZERO_KEYS:
            for value in (1, False):
                q = copy.deepcopy(p); q["validation_summary"][k] = value
                with self.assertRaises(ValueError): b.validate_result(q)
        p["gate_f_candidate"] = True
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_28_real_run_dispatch_roundtrip_and_no_overwrite(self):
        m = fixture(); parent = parent_payload(m); events = []
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "audit"
            def pc(*args):
                events.append("precheck"); return protection()
            def lp(*args):
                events.append("parent"); return parent, m
            with patch.object(b, "context", return_value=(None, None, FakeAudit())), \
                 patch.object(b, "precheck", side_effect=pc), patch.object(b, "load_parent", side_effect=lp), \
                 contextlib.redirect_stdout(io.StringIO()):
                p = b.run(summaries=["x"] * 7, output_dir=out, expected_head="f" * 40)
                self.assertEqual(events, ["precheck", "parent", "precheck"])
                q, _ = b.verify_artifacts(out, ["x"] * 7, "f" * 40)
                self.assertEqual(q, p)
                self.assertEqual(set(x.name for x in out.iterdir()), set(b.OUTPUTS) | {"summary.json"})
                with self.assertRaises(FileExistsError): b.run(summaries=["x"] * 7, output_dir=out, expected_head="f" * 40)

    def test_29_output_hash_and_semantic_tampering_rejected(self):
        m = fixture(); parent = parent_payload(m)
        with tempfile.TemporaryDirectory() as tmp, patch.object(b, "context", return_value=(None, None, FakeAudit())), \
             patch.object(b, "precheck", return_value=protection()), patch.object(b, "load_parent", return_value=(parent, m)), \
             contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp) / "audit"
            p = b.run(summaries=["x"] * 7, output_dir=out, expected_head="f" * 40)
            f = out / "failure-profile.json"; report = json.loads(f.read_text())
            report["records"][0]["failure_class"] = "tampered"; f.write_bytes(b.blob(report))
            with self.assertRaisesRegex(ValueError, "output bytes"): b.verify_artifacts(out, ["x"] * 7, "f" * 40)
            a = next(a for a in p["artifacts"] if a["file"] == f.name)
            a.update(sha256=FakeAudit.sha(f), serialized_bytes=f.stat().st_size)
            (out / "summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError, "persisted reconstruction"): b.verify_artifacts(out, ["x"] * 7, "f" * 40)

    def test_30_suite_is_constructed_and_exact_id_filtered(self):
        class Dummy(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def runTest(self): pass
            def id(self): return self.name
        ids = ["fixture." + str(i) for i in range(b.manifest()["loaded_tests"] - 1)] + [b.EXCLUDED]
        suite = unittest.TestSuite(Dummy(i) for i in ids)
        with patch.object(b, "regression_modules", return_value=[]), \
             patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=suite):
            got = b.regression_suite(Path.cwd())
            self.assertEqual(got.countTestCases(), b.manifest()["focused_tests"])
            self.assertEqual({x.id() for x in b.flatten(got)}, set(ids) - {b.EXCLUDED})

    def test_31_runner_python_blocks_and_cli_order(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root / "tools/run_c281.ps1").read_text(encoding="utf-8")
        launcher = (root / "tools/invoke_c281.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S)
        self.assertEqual(len(blocks), 3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:9]", blocks[2]); self.assertIn("head = sys.argv[9]", blocks[2])
        self.assertIn("--summaries @Summaries", runner)
        self.assertIn("$Postcheck $Out @Summaries $ExpectedHead", runner)
        self.assertLess(launcher.index("-Mode Validate"), launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"), launcher.index("publish_experiment_log.ps1"))
        self.assertIn("Parser]::ParseFile", launcher)
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json', launcher)), 7)

    def test_32_lifecycle_seal_and_own_test_inventory(self):
        root = Path(__file__).resolve().parents[1]
        handoff = (root / "docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        prereg = (root / b.OWN[4]).read_text(encoding="utf-8")
        formal = re.search(r"(?ms)^## Formal state\s+(.*?)(?=^## |\Z)", handoff)
        self.assertIsNotNone(formal); self.assertIn(b.MANIFEST_SHA, prereg)
        if re.search(r"\bC281 ACTIVE /", formal.group(1)):
            self.assertIn(b.MANIFEST_SHA, handoff)
        else:
            acceptance = root / "docs/experiment-ledger-addendum-c281-c282.md"
            self.assertTrue(acceptance.is_file()); self.assertIn(b.MANIFEST_SHA, acceptance.read_text(encoding="utf-8"))
        names = unittest.defaultTestLoader.getTestCaseNames(type(self))
        self.assertEqual(len(names), b.manifest()["own_tests"])
        for name in b.OWN: self.assertTrue((root / name).is_file())


if __name__ == "__main__":
    unittest.main()
