"""C305 behavioral controls; synthetic fixtures are not FOLD capability evidence."""
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
from fold_lm.v05_benchmarks import model_c305_saved_length_overlap as b


def fixture():
    data = {s: [] for s in b.SPLITS}
    for entities, values, language in itertools.product(((0, 1), (0, 2), (1, 2)), itertools.permutations(range(4), 2), ("en", "ja")):
        split = "HOLDOUT" if (values[1] - values[0]) % 4 == 2 else "TRAIN"
        for order, query in itertools.product((entities, entities[::-1]), entities):
            data[split].append(dict(id=str((entities, values, language, order, query)), entities=list(entities),
                values=list(values), language=language, permutation=list(order), query=query, target=48 + values[entities.index(query)]))
    prompts = {str(n): {s: {p: [dict(source_id=r["id"], target=r["target"]) for r in rows] for p in b.PROFILES}
                       for s, rows in data.items()} for n in b.LENGTHS}
    records, metrics, partitions = [], [], []
    for index, (seed, arm) in enumerate(b.identities()):
        raw, scores = {}, {}
        for n in b.LENGTHS:
            raw[str(n)], totals = {}, []
            for split, rows in data.items():
                raw[str(n)][split] = {}
                total_correct = 0
                for profile, old in zip(b.PROFILES, b.SCORE_PROFILES, strict=True):
                    pred = [r["target"] if (i + n + index) % 7 else 70 for i, r in enumerate(rows)]
                    z = torch.zeros((len(rows), 256), dtype=torch.float64)
                    z[torch.arange(len(rows)), torch.tensor(pred)] = 4.
                    raw[str(n)][split][profile] = dict(normal=z, evidence_blind=z, query_blind=z)
                    total_correct += sum(v == r["target"] for r, v in zip(rows, pred, strict=True))
                    for lang in ("en", "ja"):
                        ids = [i for i, r in enumerate(rows) if r["language"] == lang]
                        groups = defaultdict(list)
                        for i in ids:
                            r = rows[i]
                            groups[(tuple(r["entities"]), tuple(r["values"]), tuple(r["permutation"]))].append(pred[i])
                        totals.append(dict(split=split, profile=old, language=lang, rows=len(ids),
                            correct=sum(pred[i] == rows[i]["target"] for i in ids), pairs=len(ids) // 2,
                            collapsed_pairs=sum(v[0] == v[1] for v in groups.values())))
                partitions.append(dict(seed=seed, arm=arm, identifier_length=n, split=split, rows=3 * len(rows), correct=total_correct))
            scores[str(n)] = dict(totals=totals)
        records.append(dict(seed=seed, arm=arm, raw=raw))
        metrics.append(dict(seed=seed, arm=arm, length_scores=scores))
    return records, data, prompts, metrics, partitions


def protection():
    pins = {n: "b" * 40 for n in b.OWN}
    pins[b.PARENT_SOURCE] = b.PARENT_BLOB
    while len(pins) < 676:
        pins["fixture/" + str(len(pins))] = "b" * 40
    return pins, {"fixture/input/" + str(i): "a" * 64 for i in range(1257)}


class Audit:
    @staticmethod
    def sha(path):
        p = Path(path)
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a" * 64
    @staticmethod
    def read_json(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, n):
        return Path(root) / n
    @staticmethod
    def git(root, *args):
        if args[0] == "rev-parse":
            return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0] == "branch":
            return b"feat/sft-target-loss\n"
        return b""


def payload(summary):
    pins, protected = protection()
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, commit_sha="f" * 40, status="PASS",
        diagnostic_execution_valid=True, capability_gate_applicable=False, gate_f_candidate=False,
        production_adoption=False, source_blobs=pins, input_sha256=protected,
        artifacts=[dict(file=n) for n in b.OUTPUTS], validation_summary=summary)


def row(predictions, target=48):
    return dict(predictions=predictions, target=target)


class C305Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads()
        torch.set_num_threads(2)
        cls.args = fixture()
        cls.aligned, cls.summary = b.analyze(*cls.args)
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads)

    def test_01_seal(self):
        b.validate_seal()
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)
    def test_02_bad_seal(self):
        with patch.object(b, "MANIFEST_SHA", "0" * 64), self.assertRaises(ValueError):
            b.validate_seal()
    def test_03_four_transitions(self):
        rows = [row([48, 48, a, c]) for a, c in ((48, 48), (48, 49), (49, 48), (49, 49))]
        r = b.transition(rows, 4)
        self.assertEqual([r[k] for k in ("both_correct", "reference_only", "five_only", "both_wrong")], [1] * 4)
        self.assertEqual((r["argmax_flips"], r["persistent_fraction_of_five_errors"]), (2, .5))
    def test_04_wrong_answer_change(self):
        r = b.transition([row([48, 48, 49, 70])], 4)
        self.assertEqual((r["both_wrong"], r["both_wrong_changed_answer"], r["argmax_flips"]), (1, 1, 1))
    def test_05_zero_denominators(self):
        r = b.transition([row([48] * 4)], 4)
        self.assertIsNone(r["persistent_fraction_of_five_errors"])
        r = b.transition([row([70] * 4)], 4)
        self.assertIsNone(r["five_error_rate_given_reference_correct"])
    def test_06_bad_bytes_and_reference(self):
        for pred in ([-1] * 4, [256] * 4, [True] * 4, [48.] * 4, [48]):
            with self.assertRaises(ValueError):
                b.transition([row(pred)], 4)
        with self.assertRaises(ValueError):
            b.transition([], 4)
        with self.assertRaises(ValueError):
            b.transition([row([48] * 4)], 5)
    def test_07_reference_selection(self):
        r = row([48, 70, 48, 70])
        self.assertEqual(b.transition([r], 2)["reference_only"], 1)
        self.assertEqual(b.transition([r], 3)["both_wrong"], 1)
    def test_08_independent_exhaustive_conservation(self):
        rows = [row(list(v)) for v in itertools.product((48, 49, 70), repeat=4)]
        for n in (2, 3, 4):
            r = b.transition(rows, n)
            self.assertEqual(r["reference_correct"], sum(v["predictions"][n - 2] == 48 for v in rows))
            self.assertEqual(r["five_errors"], sum(v["predictions"][3] != 48 for v in rows))
    def test_09_pair_coverage(self):
        rows = self.args[1]["TRAIN"][:2]
        self.assertEqual(b.collapse(rows, [48, 48]), 1)
        with self.assertRaises(ValueError):
            b.collapse(rows[:1], [48])
    def test_10_complete_inventory(self):
        self.assertEqual(len(self.aligned), 12960)
        self.assertEqual(tuple(len(self.summary[k]) for k in ("transition_groups", "detail_groups", "signature_groups")), (90, 540, 30))
        self.assertEqual(self.summary["reconciled_totals"], 720)
        self.assertEqual(self.summary["saved_predictions"], 51840)
    def test_11_independent_signature_counts(self):
        for group in self.summary["signature_groups"]:
            rows = [r for r in self.aligned if all(r[k] == group[k] for k in ("seed", "arm", "split"))]
            counts = Counter("".join(str(int(p == r["target"])) for p in r["predictions"]) for r in rows)
            self.assertEqual(group["counts"], {f"{i:04b}": counts[f"{i:04b}"] for i in range(16)})
    def test_12_stratified_counts_sum(self):
        for g in self.summary["transition_groups"]:
            ds = [d for d in self.summary["detail_groups"] if all(d[k] == g[k] for k in ("seed", "arm", "split", "reference_length"))]
            for k in ("rows", "both_correct", "both_wrong", "reference_only", "five_only", "argmax_flips"):
                self.assertEqual(sum(d[k] for d in ds), g[k])
    def test_13_missing_model(self):
        args = list(self.args)
        args[0] = args[0][:-1]
        with self.assertRaises(ValueError):
            b.analyze(*args)
    def test_14_wrong_prompt_identity(self):
        args = list(self.args)
        args[2] = copy.deepcopy(args[2])
        args[2]["5"]["TRAIN"]["repeat"][0]["source_id"] = "wrong"
        with self.assertRaisesRegex(ValueError, "prompt identity"):
            b.analyze(*args)
    def test_15_parent_totals_mismatch(self):
        args = list(self.args)
        args[3] = copy.deepcopy(args[3])
        args[3][0]["length_scores"]["2"]["totals"][0]["correct"] -= 1
        with self.assertRaisesRegex(ValueError, "normal totals"):
            b.analyze(*args)
    def test_16_partition_mismatch(self):
        args = list(self.args)
        args[4] = copy.deepcopy(args[4])
        args[4][0]["correct"] -= 1
        with self.assertRaisesRegex(ValueError, "partition totals"):
            b.analyze(*args)
    def test_17_logits_contract(self):
        for transform in (lambda x: x.float(), lambda x: x[:, :255], lambda x: x + float("nan"), lambda x: x.clone().requires_grad_()):
            args = list(self.args)
            records = list(args[0]); records[0] = copy.deepcopy(records[0]); args[0] = records
            views = records[0]["raw"]["2"]["TRAIN"]["repeat"]
            views["normal"] = transform(views["normal"])
            with self.assertRaisesRegex(ValueError, "saved logits"):
                b.analyze(*args)
    def test_18_duplicate_logical_rows(self):
        args = list(self.args)
        args[1] = copy.deepcopy(args[1])
        args[1]["TRAIN"][1]["id"] = args[1]["TRAIN"][0]["id"]
        with self.assertRaises(ValueError):
            b.analyze(*args)
    def test_19_forbidden_neural_operations(self):
        for fn in (lambda: torch.nn.Identity()(torch.ones(1)), lambda: torch.nn.Linear(1, 1).load_state_dict({}), lambda: torch.save({}, "never.pt")):
            with b.no_neural(), self.assertRaises(RuntimeError):
                fn()
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]), 1.)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths = [(Path("/c305-fixture") / str(i) / "summary.json").resolve() for i in range(31)]
        artifacts = [dict(file=n) for n in ("architecture-plan.json", "dataset.json", "length-datasets.json", "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")]
        p = dict(experiment_id="C304-v5b-length-breadth-to-five", commit_sha=b.PARENT_EXECUTION, status="FAIL", source_blobs={b.PARENT_SOURCE: b.PARENT_BLOB}, artifacts=artifacts,
            validation_summary=dict(seed_results=b.expected_flags(), candidate_gate=False, all_groups_matched=True, all_replays=True, final_partitions=self.args[4]))
        parent = NS(context=lambda: (None,), parent_hashes=lambda _: tuple(str(i % 10) * 64 for i in range(30)),
            OUTPUTS=tuple(a["file"] for a in artifacts), verify_artifacts=Mock(return_value=(p, self.args[3])), validate_result=Mock())
        mapping = dict(zip(map(str, paths), (b.PARENT_SHA, *parent.parent_hashes(None)), strict=True))
        c = NS(audit=NS(sha=lambda path: mapping[str(path)], read_json=lambda path: self.args[1] if path.name == "dataset.json" else self.args[2]))
        archive = dict(schema="fold-c304-length-eval-v1", records=self.args[0])
        with patch.object(b, "context", return_value=(parent, c)), patch.object(torch, "load", return_value=archive):
            yield paths, mapping, parent, p, archive

    def test_20_all_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths, mapping, parent, p, _):
            self.assertEqual(b.load_parent(paths)[0], p)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent, paths[1:], b.PARENT_EXECUTION)
            for path in paths:
                old = mapping[str(path)]; mapping[str(path)] = "f" * 64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):
                    b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)] = old
    def test_21_parent_contract_failures(self):
        for mutate in (lambda p, a: p.update(status="PASS"), lambda p, a: p["validation_summary"]["seed_results"].pop(), lambda p, a: a.update(schema="wrong")):
            with self.loader_fixture() as (paths, _, _, p, archive):
                mutate(p, archive)
                with self.assertRaises(ValueError):
                    b.load_parent(paths)
    def test_22_real_reconstruct_dispatch(self):
        with self.loader_fixture() as (paths, _, _, _, _):
            rows, s = b.reconstruct(paths)
            self.assertEqual(rows, self.aligned)
            self.assertEqual(s, self.summary)
    def test_23_protection_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); pins = {b.PARENT_SOURCE: b.PARENT_BLOB}
            while len(pins) < 670:
                pins["accepted/" + str(len(pins))] = "b" * 40
            for name in list(pins) + list(b.OWN):
                p = root / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(name, encoding="utf-8")
            protected = {str((root / n).resolve()): Audit.sha(root / n) for n in pins}
            for i in range(1243 - len(protected)):
                p = root / f"input{i}"; p.write_text("input", encoding="utf-8"); protected[str(p.resolve())] = Audit.sha(p)
            folder = root / "parent"; folder.mkdir(); sp = folder / "summary.json"; sp.write_text("summary", encoding="utf-8")
            mapping = {str(sp.resolve()): b.PARENT_SHA}; artifacts = []
            for i in range(7):
                p = folder / str(i); p.write_text("artifact", encoding="utf-8"); mapping[str(p.resolve())] = "a" * 64; artifacts.append(dict(file=str(i), sha256="a" * 64))
            def sha(p):
                return mapping.get(str(Path(p).resolve()), Audit.sha(p))
            parent = types.ModuleType("parent"); parent.__file__ = str(root / b.PARENT_SOURCE); parent.context = lambda: ()
            c = NS(audit=NS(sha=sha, git=lambda root, *a: (pins.get(a[1][5:], "c" * 40) + "\n").encode(), safe_child=Audit.safe_child,
                           protect_tree_files=lambda root, ps: {str((root / n).resolve()): sha(root / n) for n in ps}))
            p = dict(source_blobs=pins, input_sha256=protected, artifacts=artifacts)
            with patch.object(b, "context", return_value=(parent, c)), patch.object(b, "load_parent", return_value=(p,)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len, b.precheck([sp] * 31, root))), (676, 1257))
                c.missing = types.ModuleType("missing"); c.missing.__file__ = str(root / "missing.py")
                with self.assertRaisesRegex(ValueError, "unprotected"):
                    b.precheck([sp] * 31, root)
    def test_24_result_scope(self):
        b.validate_result(payload(self.summary))
        for mutate in (lambda p: p.update(gate_f_candidate=True), lambda p: p["validation_summary"].update(train_steps=False), lambda p: p["validation_summary"]["detail_groups"].pop()):
            p = payload(copy.deepcopy(self.summary)); mutate(p)
            with self.assertRaises(ValueError):
                b.validate_result(p)

    @contextlib.contextmanager
    def run_fixture(self):
        events = []
        def precheck(*args):
            events.append("precheck"); return protection()
        def reconstruct(*args):
            events.append("reconstruct"); return self.aligned, self.summary
        with patch.object(b, "context", return_value=(None, NS(audit=Audit()))), patch.object(b, "precheck", side_effect=precheck), patch.object(b, "reconstruct", side_effect=reconstruct):
            yield events
    def test_25_production_run_roundtrip_order(self):
        with self.run_fixture() as events, tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp) / "run"
            p = b.run(summaries=["x"] * 31, output_dir=out, expected_head="f" * 40)
            self.assertEqual(events, ["precheck", "reconstruct", "precheck"])
            self.assertEqual(b.verify_artifacts(out, ["x"] * 31, "f" * 40), p)
            with self.assertRaises(FileExistsError):
                b.run(summaries=["x"] * 31, output_dir=out, expected_head="f" * 40)
    def test_26_byte_and_semantic_tamper(self):
        with self.run_fixture(), tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp) / "run"; p = b.run(summaries=["x"] * 31, output_dir=out, expected_head="f" * 40)
            path = out / "aligned-answers.json"; path.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "output bytes"):
                b.verify_artifacts(out, ["x"] * 31, "f" * 40)
            item = next(a for a in p["artifacts"] if a["file"] == path.name)
            item.update(sha256=Audit.sha(path), serialized_bytes=path.stat().st_size)
            (out / "summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError, "persisted"):
                b.verify_artifacts(out, ["x"] * 31, "f" * 40)
    def test_27_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self, name):
                super().__init__(); self.name = name
            def runTest(self):
                pass
            def id(self):
                return self.name
        ids = [f"fixture.{i}" for i in range(4781)] + [b.EXCLUDED]
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite = b.regression_suite(Path.cwd())
            self.assertEqual(suite.countTestCases(), 4781)
            self.assertEqual({t.id() for t in b.flatten(suite)}, set(ids) - {b.EXCLUDED})
    def test_28_cli_and_context(self):
        args = ["prog", "--summaries"] + [str(i) for i in range(31)] + ["--output-dir", "out", "--expected-head", "f" * 40]
        with patch.object(sys, "argv", args), patch.object(b, "run") as run:
            b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]), 31)
        parent = NS(context=lambda: (1, 2), regression_modules=lambda root: [f"f{i}" for i in range(189)])
        package = types.ModuleType("fold_lm.v05_benchmarks"); package.model_c304_length_breadth = parent
        with patch.dict(sys.modules, {"fold_lm.v05_benchmarks": package}):
            self.assertEqual(b.context(), (parent, 2)); self.assertEqual(len(b.regression_modules(Path.cwd())), 190)
    def test_29_guard(self):
        b.guard(Path.cwd(), "f" * 40, NS(audit=Audit()))
        with self.assertRaises(ValueError):
            b.guard(Path.cwd(), "e" * 40, NS(audit=Audit()))
    def test_30_utf8_inventory(self):
        root = Path(__file__).resolve().parents[1]
        with patch.object(io, "text_encoding", side_effect=lambda encoding, stacklevel=2: "cp932" if encoding is None else encoding):
            for n in b.OWN:
                self.assertTrue((root / n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA, (root / b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__), Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "read_text":
                    self.assertTrue(any(k.arg == "encoding" and isinstance(k.value, ast.Constant) and k.value.value == "utf-8" for k in node.keywords))
    def test_31_runner_blocks(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root / b.OWN[2]).read_text(encoding="utf-8"); launcher = (root / b.OWN[3]).read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S)
        self.assertEqual(len(blocks), 3)
        for code in blocks:
            ast.parse(code)
        self.assertIn("sys.argv[2:33]", blocks[2]); self.assertIn("head = sys.argv[33]", blocks[2])
        self.assertEqual(len(re.findall(r"runs\\c\d{3}-.*?\\summary.json", launcher)), 31)
        self.assertLess(launcher.index("-Mode Validate"), launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"), launcher.index("publish_experiment_log.ps1"))
    def test_32_import_and_test_count(self):
        imports = [n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8")))
                   if isinstance(n, ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports, ["model_c304_length_breadth"])
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))), b.manifest()["own_tests"])


if __name__ == "__main__":
    unittest.main()
