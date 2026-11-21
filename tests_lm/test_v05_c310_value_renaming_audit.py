"""C310 software-control fixtures; saved-data consistency is not model capability."""
import ast
from collections import Counter, defaultdict
import contextlib
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c310_value_renaming_audit as b

SCORER_SOURCE = "fold_lm/v05_benchmarks/model_c270_frozen_triple_identifiers.py"


def dataset():
    data = {s: [] for s in b.SPLITS}
    for entities, values, lang in itertools.product(((0, 1), (0, 2), (1, 2)), itertools.permutations(range(4), 2), ("en", "ja")):
        split = "HOLDOUT" if (values[1]-values[0]) % 4 == 2 else "TRAIN"
        for perm, query in itertools.product((entities, entities[::-1]), entities):
            data[split].append(dict(id=f"{lang}:{entities}:{values}:{perm}:{query}", entities=list(entities), values=list(values),
                                   language=lang, permutation=list(perm), query=query, target=48+values[entities.index(query)]))
    return data


def ref_totals(rows, predicted, language):
    ids = [i for i, row in enumerate(rows) if row["language"] == language]
    buckets = defaultdict(list)
    for i in ids:
        row = rows[i]
        buckets[(tuple(row["entities"]), tuple(row["values"]), tuple(row["permutation"]))].append(predicted[i])
    return dict(rows=len(ids), correct=sum(predicted[i] == rows[i]["target"] for i in ids), pairs=len(buckets),
                collapsed_pairs=sum(len(set(values)) == 1 for values in buckets.values()))


def fixtures(kind="correct"):
    data = dataset(); raw = {}; totals = []
    for split in b.SPLITS:
        rows = data[split]; raw[split] = {}
        for profile, old_profile in zip(b.PROFILES, b.OLD_PROFILES, strict=True):
            z = torch.zeros((len(rows), 256), dtype=torch.float64)
            for i, row in enumerate(rows):
                pred = row["target"]
                if kind == "other": pred = 48+row["values"][1-row["entities"].index(row["query"])]
                elif kind == "nonvalue": pred = 70
                elif kind == "constant": pred = 48
                elif kind == "split_failure" and split == "HOLDOUT": pred = 48+row["values"][1-row["entities"].index(row["query"])]
                z[i, pred] = 4.
            if kind == "ties": z.zero_(); z[:, 48:50] = 4.
            raw[split][profile] = dict(normal=z, evidence_blind=torch.zeros_like(z), query_blind=torch.zeros_like(z))
            pred = z.argmax(1).tolist()
            for language in ("en", "ja"):
                totals.append(dict(split=split, profile=old_profile, language=language, **ref_totals(rows, pred, language)))
    records, metrics = [], []
    for seed, arm in b.identities():
        # Share immutable fixture tensors,not model weights. Mutating tests take their own copies.
        records.append(dict(seed=seed, arm=arm, raw={str(n): copy.deepcopy(raw) for n in b.LENGTHS}))
        metrics.append(dict(seed=seed, arm=arm, length_scores={str(n): dict(totals=copy.deepcopy(totals)) for n in b.LENGTHS}))
    return records, data, metrics


def reference_counts(pred, rows, mask):
    index = {(r["language"], tuple(r["entities"]), tuple(r["values"]), tuple(r["permutation"]), r["query"]): i for i, r in enumerate(rows)}
    result = dict.fromkeys(b.COUNT_KEYS, 0)
    for k, perm in enumerate(itertools.permutations(range(4))):
        for i, row in enumerate(rows):
            if not bool(mask[k, i]): continue
            values = tuple(perm[x] for x in row["values"])
            j = index[(row["language"], tuple(row["entities"]), values, tuple(row["permutation"]), row["query"])]
            left, right = int(pred[i]), int(pred[j]); want = 48+perm[left-48] if 48 <= left < 52 else left
            eq = right == want; lc = left == row["target"]; rc = right == rows[j]["target"]
            flags = dict(comparisons=True, equivariant=eq, violations=not eq, both_correct=lc and rc, both_wrong=not lc and not rc,
                correct_to_wrong=lc and not rc, wrong_to_correct=not lc and rc, equivariant_wrong=eq and not lc and not rc,
                left_correct=lc, right_correct=rc, same_prediction=left == right)
            for name, flag in flags.items(): result[name] += int(flag)
    return result


def parent_payload():
    return dict(experiment_id="C309-v5b-core-lr-replication", commit_sha=b.PARENT_EXECUTION, status="FAIL",
        source_blobs={b.PARENT_SOURCE: b.PARENT_BLOB, b.WIDE_SOURCE: b.WIDE_BLOB},
        artifacts=[dict(file=n, sha256="a"*64) for n in ("architecture-plan.json", "dataset.json", "length-datasets.json",
            "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")],
        validation_summary=dict(seed_results=b.expected_parent_flags(), candidate_gate=False, all_replays=True, all_groups_matched=True))


def protection():
    pins = {name: "b"*40 for name in b.OWN}; pins[b.PARENT_SOURCE] = b.PARENT_BLOB; pins[b.WIDE_SOURCE] = b.WIDE_BLOB
    while len(pins) < 706: pins["fixture/"+str(len(pins))] = "b"*40
    return pins, {"fixture/input/"+str(i): "a"*64 for i in range(1323)}


class Audit:
    @staticmethod
    def sha(path):
        path = Path(path); return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, name):
        path = (Path(root)/name).resolve()
        b.require(path.is_relative_to(Path(root).resolve()), "unsafe artifact path")
        return path
    @staticmethod
    def git(root, *args):
        if args[0] == "rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0] == "branch": return b"feat/sft-target-loss\n"
        return b""


def payload(summary):
    pins, inputs = protection()
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, commit_sha="f"*40, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=inputs, artifacts=[dict(file=n) for n in b.OUTPUTS], validation_summary=summary,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False)


class C310Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.records, cls.data, cls.metrics = fixtures()
        cls.rows, cls.mapping, cls.labels = b.align_values(cls.data)
        cls.targets = torch.tensor([r["target"] for r in cls.rows], dtype=torch.int64)
        cls.changed = cls.mapping != torch.arange(288)
        cls.report, cls.summary = b.analyze(cls.records, cls.data, cls.metrics)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)

    def test_01_manifest_seal(self):
        b.validate_seal(); self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)

    def test_02_invalid_seals(self):
        for value in ("PENDING", "0"*64, "A"*64):
            with patch.object(b, "MANIFEST_SHA", value), self.assertRaises(ValueError): b.validate_seal()

    def test_03_exact_data_and_preserved_context(self):
        self.assertEqual(b.digest(self.data), b.DATA_SHA)
        for k, perm in enumerate(b.PERMUTATIONS):
            for i, j in enumerate(self.mapping[k].tolist()):
                row, other = self.rows[i], self.rows[j]
                for name in ("entities", "permutation", "query", "language"): self.assertEqual(row[name], other[name])
                self.assertEqual(other["values"], [perm[v] for v in row["values"]])
                self.assertEqual(other["target"], int(self.labels[k, row["target"]]))

    def test_04_independent_scalar_oracle(self):
        pred = torch.tensor([r["target"] if i % 3 == 0 else (i*17) % 256 for i, r in enumerate(self.rows)])
        for mask in (self.changed, ~self.changed, self.changed & (torch.arange(288) < 192)[None, :]):
            got = b.count_comparisons(pred, self.targets, self.mapping, self.labels, mask)
            self.assertEqual(got, reference_counts(pred, self.rows, mask))

    def test_05_bijection_inverse_and_stabilizers(self):
        for k, perm in enumerate(b.PERMUTATIONS):
            self.assertEqual(sorted(self.mapping[k].tolist()), list(range(288)))
            inverse = tuple(perm.index(i) for i in range(4)); inv = b.PERMUTATIONS.index(inverse)
            self.assertTrue(torch.equal(self.mapping[inv][self.mapping[k]], torch.arange(288)))
            self.assertTrue(torch.equal(self.labels[k, :48], torch.arange(48)))
            self.assertTrue(torch.equal(self.labels[k, 52:], torch.arange(52, 256)))
        self.assertTrue(bool((self.changed.sum(0) == 22).all()))
        for i in range(288): self.assertEqual(set(Counter(self.mapping[:, i].tolist()).values()), {2})

    def test_06_bad_rows_rejected(self):
        mutations = (lambda d: d["TRAIN"].pop(), lambda d: d["TRAIN"][1].update(id=d["TRAIN"][0]["id"]),
            lambda d: d["TRAIN"][0].update(target=99), lambda d: d["TRAIN"][0].update(values=[0, 0]),
            lambda d: d["TRAIN"][0].update(query=9), lambda d: d["TRAIN"][0].update(permutation=[0, True]),
            lambda d: d["TRAIN"][0].update(language="xx"))
        for fn in mutations:
            data = copy.deepcopy(self.data); fn(data)
            with self.assertRaises(ValueError): b.align_values(data)
        data = copy.deepcopy(self.data)
        data["TRAIN"][0], data["HOLDOUT"][0] = data["HOLDOUT"][0], data["TRAIN"][0]
        with self.assertRaisesRegex(ValueError, "original split"): b.align_values(data)

    def test_07_correct_outputs_equivariant(self):
        self.assertTrue(all(r["violations"] == 0 and r["both_correct"] == r["comparisons"] for r in self.summary["changed_input"]))
        self.assertEqual(self.summary["changed_input_comparisons"], 1140480)

    def test_08_other_fact_can_be_consistent_and_wrong(self):
        pred = torch.tensor([48+r["values"][1-r["entities"].index(r["query"])] for r in self.rows])
        r = b.count_comparisons(pred, self.targets, self.mapping, self.labels, self.changed)
        self.assertEqual(r["equivariant_wrong"], r["comparisons"]); self.assertEqual(r["both_correct"], 0)

    def test_09_constant_nonvalue_trivial_consistency(self):
        r = b.count_comparisons(torch.full((288,), 70), self.targets, self.mapping, self.labels, self.changed)
        self.assertEqual(r["equivariant_wrong"], r["comparisons"]); self.assertEqual(r["same_prediction"], r["comparisons"])

    def test_10_absent_value_swap_is_not_changed_input(self):
        pred = torch.full((288,), 48)
        absent = ~self.changed & (torch.arange(24)[:, None] != 0)
        r = b.count_comparisons(pred, self.targets, self.mapping, self.labels, absent)
        self.assertEqual(r["comparisons"], 288); self.assertEqual(r["same_prediction"], 288)
        self.assertEqual(r["violations"], sum(0 not in row["values"] for row in self.rows))
        self.assertGreater(r["violations"], 0)

    def test_11_split_denominators(self):
        expected = {(a, z): count for (a, z), count in zip(itertools.product(b.SPLITS, repeat=2), (8064, 4608, 4608, 1728), strict=True)}
        for r in self.summary["changed_input"]: self.assertEqual(r["comparisons"], expected[r["source_split"], r["destination_split"]])
        for r in self.summary["absent_swap"]: self.assertEqual(r["comparisons"], 576 if r["source_split"] == "TRAIN" else 288)
        self.assertTrue(all(r["comparisons"] == 864 for r in self.summary["identity_controls"]))

    def test_12_inventory_original_totals(self):
        self.assertEqual((len(self.report["predictions"]), len(self.report["original_totals"])), (60, 720))
        self.assertEqual(len(set(self.report["row_ids"])), 288)
        self.assertEqual(self.summary["tied_max_rows"], 0)
        self.assertEqual(sum(len(v) for block in self.report["predictions"] for v in block["predictions"].values()), 51840)
        b.validate_result(payload(self.summary))

    def test_13_tied_argmax_uses_original_class_order(self):
        records, data, metrics = fixtures("ties")
        report, summary = b.analyze(records, data, metrics)
        self.assertEqual(summary["tied_max_rows"], 51840)
        self.assertTrue(all(set(v) == {48} for block in report["predictions"] for v in block["predictions"].values()))
        b.validate_result(payload(summary))

    def test_14_logit_contract(self):
        for fn in (lambda z: z.float(), lambda z: z[:, :255], lambda z: z.clone().requires_grad_(), lambda z: z+float("nan")):
            record = copy.deepcopy(self.records[0]); views = record["raw"]["2"]["TRAIN"]["repeat"]
            views["normal"] = fn(views["normal"])
            with self.assertRaisesRegex(ValueError, "saved logits"): b.analyze([record]+self.records[1:], self.data, self.metrics)
        record = copy.deepcopy(self.records[0]); record["raw"]["2"]["TRAIN"]["repeat"].pop("query_blind")
        with self.assertRaises(ValueError): b.analyze([record]+self.records[1:], self.data, self.metrics)

    def test_15_parent_counts_must_match(self):
        for name in ("rows", "correct", "pairs", "collapsed_pairs"):
            metrics = copy.deepcopy(self.metrics); metrics[0]["length_scores"]["2"]["totals"][0][name] += 1
            with self.assertRaisesRegex(ValueError, "original normal totals"): b.analyze(self.records, self.data, metrics)

    def test_16_complete_cohort(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1], self.data, self.metrics)
        with self.assertRaises(ValueError): b.analyze(self.records, self.data, self.metrics[::-1])
        record = copy.deepcopy(self.records[0]); record["raw"].pop("5")
        with self.assertRaises(ValueError): b.analyze([record]+self.records[1:], self.data, self.metrics)

    def test_17_no_neural_guard_restores(self):
        functions = (lambda: torch.nn.Identity()(torch.ones(1)), lambda: torch.nn.Identity().load_state_dict({}),
                     lambda: torch.save({}, io.BytesIO()))
        for fn in functions:
            with b.no_neural(), self.assertRaisesRegex(RuntimeError, "C310 forbids"): fn()
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]), 1.)
        with b.no_neural(): self.assertFalse(torch.is_grad_enabled())

    @contextlib.contextmanager
    def loader_fixture(self):
        paths = [(Path(tempfile.gettempdir())/"c310-parent-fixture"/str(i)/"summary.json").resolve() for i in range(36)]
        hashes = (b.PARENT_SHA, *[str(i % 10)*64 for i in range(35)])
        mapping = dict(zip(map(str, paths), hashes, strict=True)); p = parent_payload()
        parent = NS(context=lambda: (None,), parent_hashes=lambda _: hashes[1:], OUTPUTS=tuple(a["file"] for a in p["artifacts"]),
                    verify_artifacts=Mock(return_value=(p, self.metrics)), validate_result=Mock())
        c = NS(audit=NS(sha=lambda path: mapping[str(path)], read_json=lambda path: self.data), p267=NS(validate_data=Mock()))
        archive = dict(schema="fold-c309-core-lr-replication-eval-v1", records=self.records)
        with patch.object(b, "context", return_value=(parent, None, c)), patch.object(torch, "load", return_value=archive):
            yield paths, mapping, parent, p, archive

    def test_18_all36_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths, mapping, parent, p, _):
            self.assertEqual(b.load_parent(paths)[0], p)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent, paths[1:], b.PARENT_EXECUTION)
            for path in paths:
                old = mapping[str(path)]; mapping[str(path)] = "f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)] = old

    def test_19_parent_metadata_and_archive(self):
        for fn in (lambda p, a: p.update(status="PASS"), lambda p, a: p["artifacts"].pop(),
                   lambda p, a: p["source_blobs"].pop(b.WIDE_SOURCE), lambda p, a: a.update(schema="wrong"),
                   lambda p, a: p["validation_summary"]["seed_results"].pop()):
            with self.loader_fixture() as (paths, _, _, p, archive):
                fn(p, archive)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_20_source_and_input_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); pins = {b.PARENT_SOURCE: b.PARENT_BLOB, b.WIDE_SOURCE: b.WIDE_BLOB}
            while len(pins) < 700: pins["accepted/"+str(len(pins))] = "b"*40
            for name in list(pins)+list(b.OWN):
                path = root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(name, encoding="utf-8")
            inputs = {str((root/name).resolve()): Audit.sha(root/name) for name in pins}
            for i in range(1309-len(inputs)):
                path = root/f"input{i}"; path.write_text("data", encoding="utf-8"); inputs[str(path.resolve())] = Audit.sha(path)
            folder = root/"parent"; folder.mkdir(); sp = folder/"summary.json"; sp.write_text("summary", encoding="utf-8")
            mapping = {str(sp.resolve()): b.PARENT_SHA}; artifacts = []
            for descriptor in parent_payload()["artifacts"]:
                path = folder/descriptor["file"]; path.write_text("parent", encoding="utf-8")
                mapping[str(path.resolve())] = descriptor["sha256"]; artifacts.append(descriptor)
            def sha(path): return mapping.get(str(Path(path).resolve()), Audit.sha(path))
            parent = types.ModuleType("parent"); parent.__file__ = str(root/b.PARENT_SOURCE); parent.context = lambda: ()
            wide = NS(PINNED={b.PARENT_SOURCE: b.PARENT_BLOB, b.WIDE_SOURCE: b.WIDE_BLOB}, context=lambda: ())
            c = NS(factory=NS(language_module=lambda: None), audit=NS(sha=sha, safe_child=Audit.safe_child,
                git=lambda root, *args: (pins.get(args[1][5:], "c"*40)+"\n").encode(),
                protect_tree_files=lambda root, ps: {str((root/name).resolve()): sha(root/name) for name in ps}))
            p = dict(source_blobs=pins, input_sha256=inputs, artifacts=artifacts)
            with patch.object(b, "context", return_value=(parent, wide, c)), patch.object(b, "load_parent", return_value=(p, None, None, None)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len, b.precheck([sp]*36, root))), (706, 1323))
                c.missing = types.ModuleType("missing"); c.missing.__file__ = str(root/"missing.py")
                with self.assertRaisesRegex(ValueError, "unprotected helper"): b.precheck([sp]*36, root)
                del c.missing
                (root/"input0").write_text("changed", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "changed input"): b.precheck([sp]*36, root)

    def test_21_result_schema_and_conservation(self):
        for fn in (lambda p: p.update(capability_gate_applicable=True), lambda p: p["validation_summary"].update(train_steps=False),
                   lambda p: p["validation_summary"]["changed_input"][0].update(equivariant_wrong=1),
                   lambda p: p["validation_summary"]["changed_input"][0].update(seed=1),
                   lambda p: p["validation_summary"].update(changed_input_comparisons=10)):
            p = payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)

    @contextlib.contextmanager
    def run_fixture(self):
        events = []
        def precheck(*args): events.append("precheck"); return protection()
        def load(*args): events.append("load"); return parent_payload(), self.records, self.data, self.metrics
        with patch.object(b, "context", return_value=(None, None, NS(audit=Audit()))), patch.object(b, "precheck", side_effect=precheck), patch.object(b, "load_parent", side_effect=load):
            yield events

    def test_22_run_order_roundtrip(self):
        with self.run_fixture() as events, tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp)/"run"; p = b.run(summaries=["x"]*36, output_dir=out, expected_head="f"*40)
            self.assertEqual(events, ["precheck", "load", "precheck"])
            q, report = b.verify_artifacts(out, ["x"]*36, "f"*40)
            self.assertEqual(p, q); self.assertEqual(report, self.report)
            self.assertEqual(set(path.name for path in out.iterdir()), set(b.OUTPUTS)|{"summary.json"})

    def test_23_output_bytes_and_semantics(self):
        with self.run_fixture(), tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp)/"run"; p = b.run(summaries=["x"]*36, output_dir=out, expected_head="f"*40)
            path = out/"value-renaming-report.json"; path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "output bytes"): b.verify_artifacts(out, ["x"]*36, "f"*40)
            a = next(a for a in p["artifacts"] if a["file"] == path.name)
            a.update(sha256=Audit.sha(path), serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError, "persisted"): b.verify_artifacts(out, ["x"]*36, "f"*40)

    def test_24_no_overwrite_or_wrong_head(self):
        with self.run_fixture(), tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*36, output_dir=tmp, expected_head="f"*40)
            with self.assertRaisesRegex(ValueError, "repository guard"): b.run(summaries=["x"]*36, output_dir=Path(tmp)/"other", expected_head="e"*40)

    def test_25_cli_context_and_modules(self):
        argv = ["prog", "--summaries"]+[str(i) for i in range(36)]+["--output-dir", "out", "--expected-head", "f"*40]
        with patch.object(sys, "argv", argv), patch.object(b, "run") as run:
            b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]), 36)
        parent = NS(context=lambda: tuple(range(9)), regression_modules=lambda _: [f"m{i}" for i in range(194)])
        package = types.ModuleType("fold_lm.v05_benchmarks"); package.model_c309_core_lr_replication = parent
        with patch.dict(sys.modules, {"fold_lm.v05_benchmarks": package}):
            self.assertEqual(b.context(), (parent, 4, 8)); self.assertEqual(len(b.regression_modules(Path.cwd())), 195)

    def test_26_semantic_regression_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def runTest(self): pass
            def id(self): return self.name
        ids = [f"fixture.{i}" for i in range(4941)]+[b.EXCLUDED]
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite = b.regression_suite(Path.cwd()); self.assertEqual(suite.countTestCases(), 4941)
            self.assertEqual({t.id() for t in b.flatten(suite)}, set(ids)-{b.EXCLUDED})
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite([Dummy("x"), Dummy("x")])), self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_27_utf8_documents_and_source(self):
        root = Path(__file__).resolve().parents[1]
        with patch.object(io, "text_encoding", side_effect=lambda encoding, stacklevel=2: "cp932" if encoding is None else encoding):
            for name in b.OWN: self.assertTrue((root/name).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA, (root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__), Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "read_text":
                    self.assertTrue(any(k.arg == "encoding" and isinstance(k.value, ast.Constant) and k.value.value == "utf-8" for k in node.keywords))

    def test_28_runner_and_launcher(self):
        root = Path(__file__).resolve().parents[1]
        runner, launcher = [(root/name).read_text(encoding="utf-8") for name in b.OWN[2:4]]
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S); self.assertEqual(len(blocks), 3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:38]", blocks[2]); self.assertIn("head = sys.argv[38]", blocks[2])
        self.assertEqual(len(re.findall(r"runs\\c\d{3}-.*?\\summary.json", launcher)), 36)
        self.assertLess(launcher.index("-Mode Validate"), launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"), launcher.index("publish_experiment_log.ps1"))

    def test_29_actual_runtime_preflight(self):
        with self.run_fixture() as events, contextlib.redirect_stdout(io.StringIO()) as output:
            b.runtime_preflight(["x"]*36, Path.cwd())
        self.assertEqual(events, ["precheck", "load"]); self.assertIn("real_saved_value_alignment_and_totals = PASS", output.getvalue())

    def test_30_split_failure_is_not_hidden_by_consistency(self):
        records, data, metrics = fixtures("split_failure")
        _, s = b.analyze(records, data, metrics); b.validate_result(payload(s))
        for row in s["changed_input"]:
            if row["source_split"] == row["destination_split"]:
                self.assertEqual(row["violations"], 0)
            else:
                self.assertEqual(row["violations"], row["comparisons"])
        self.assertTrue(s["diagnostic_complete"])

    def test_31_actual_accepted_scorer_totals(self):
        path = Path(__file__).resolve().parents[1]/SCORER_SOURCE
        tree = ast.parse(path.read_text(encoding="utf-8"))
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "score")
        scope = dict(torch=torch, F=F, itertools=itertools, defaultdict=defaultdict, require=b.require,
                     SPLITS=b.SPLITS, PROFILES=b.OLD_PROFILES, VIEWS=("normal", "evidence_blind", "query_blind"))
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), "exec"), scope)
        backend = NS(SUBSETS=((0, 1), (0, 2), (1, 2)), validate_data=lambda d: self.assertEqual(b.digest(d), b.DATA_SHA),
                     check_logits=lambda z, n: self.assertEqual((z.shape, z.dtype), ((n, 256), torch.float64)))
        raw = self.records[0]["raw"]["2"]
        adapted = {s: {old: raw[s][new] for new, old in zip(b.PROFILES, b.OLD_PROFILES, strict=True)} for s in b.SPLITS}
        scored = scope["score"](self.data, adapted, backend)
        self.assertTrue(scored["passed"])
        self.assertEqual(scored["totals"], self.metrics[0]["length_scores"]["2"]["totals"])

    def test_32_parent_flags_imports_and_test_count(self):
        flags = b.expected_parent_flags()
        self.assertEqual(len(flags), 15)
        self.assertEqual([sum(r["quint_pass"] for r in flags if r["arm"] == arm) for arm in b.ARMS], [3, 4, 4])
        imports = [n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8")))
                   if isinstance(n, ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports, ["model_c309_core_lr_replication"])
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))), b.manifest()["own_tests"])


if __name__ == "__main__":
    unittest.main()
