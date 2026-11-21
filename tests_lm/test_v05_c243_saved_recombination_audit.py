"""C243 synthetic tests; no accepted checkpoints or scientific answers are executed."""
import ast
import contextlib
import copy
import hashlib
import inspect
import io
import itertools
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from fold_lm.v05_benchmarks import model_c243_saved_recombination_audit as b


def fixture():
    parts = {s: [] for s in b.SPLITS}
    names = {"en": ("box", "book"), "ja": ("箱", "本")}
    for x, y in itertools.permutations(range(4), 2):
        group = f"0-1-{x}-{y}"
        split = "TRAIN" if b.PARTNER[x] == y else "HOLDOUT"
        provenance = "EVAL" if tuple(sorted((x, y))) in ((0, 3), (1, 2)) else "TRAIN"
        for lang in names:
            for order, q in itertools.product((0, 1), repeat=2):
                facts = [(0, x), (1, y)]
                if order:
                    facts.reverse()
                text = ";".join(names[lang][i] + "=" + str(v) for i, v in facts) + ";" + names[lang][q] + "="
                parts[split].append(dict(id=f"{lang}-{group}-{order}-{q}", group=group, objects=[0, 1],
                    values=[x, y], language=lang, order=order, query=q, split=provenance,
                    target=48 + (x if q == 0 else y), prompt=text))
    return parts


def records(parts, rule="entity"):
    result = []
    for seed, family in b.identities():
        pred, final = {}, {}
        for split, rows in parts.items():
            pred[split] = {v: [b.rule_answers(r)[rule] if v == "normal" else 48 for r in rows] for v in b.VIEWS}
            final[split] = {lang: dict(m, answer_nll=.7) for lang, m in b.discrete_metrics(rows, pred[split]).items()}
        result.append(dict(seed=seed, family=family, final=final, predictions=pred, checkpoint_roundtrip=True,
                           prediction_replayed=True, weights_changed=True, reload_max_error=0.0))
    return result


def payload(summary):
    pins = {f"parent-{i}": "fixture" for i in range(298)}
    pins.update({p: "fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256={f"synthetic-input-{i}": "0"*64 for i in range(466)},
        artifacts=[dict(file=p) for p in b.OUTPUTS], validation_summary=summary, gate_f_candidate=False, network_calls=0)


class Audit:
    @staticmethod
    def read_json(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"):
            return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def safe_child(root, name):
        p = (Path(root)/name).resolve()
        if p.parent != Path(root).resolve():
            raise ValueError("unsafe path")
        return p
    @staticmethod
    def git(root, *args):
        if args[:2] == ("rev-parse", "HEAD"):
            return b"synthetic-head"
        if args[:2] == ("branch", "--show-current"):
            return b"feat/sft-target-loss"
        return b""


class C243Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parts = fixture()

    def test_01_manifest_and_fixed_split(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)
        self.assertEqual(b.validate_parts(self.parts), self.parts)

    def test_02_parent_split_tamper_rejected(self):
        for key, value in (("target", 255), ("order", 1), ("values", [0, 2])):
            p = copy.deepcopy(self.parts)
            p["TRAIN"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                b.validate_parts(p)

    def test_03_rule_does_not_read_target(self):
        r = copy.deepcopy(self.parts["TRAIN"][0])
        wanted = b.rule_answers(r)
        r.pop("target")
        self.assertEqual(b.rule_answers(r), wanted)

    def test_04_train_partner_rule_degeneracy(self):
        for r in self.parts["TRAIN"]:
            rules = b.rule_answers(r)
            self.assertEqual(rules["entity"], rules["partner_of_other"])

    def test_05_holdout_four_digit_categories_distinct(self):
        for r in self.parts["HOLDOUT"]:
            cats = {b.category(r, d) for d in range(48, 52)}
            self.assertEqual(cats, set(b.CATEGORIES)-{"other_byte"})
            self.assertEqual(b.category(r, 255), "other_byte")

    def test_06_supplied_and_absent_are_not_conflated(self):
        r = self.parts["HOLDOUT"][0]
        a = b.rule_answers(r)
        self.assertEqual(b.category(r, a["other_entity"]), "other_supplied")
        self.assertEqual(b.category(r, a["partner_of_other"]), "absent_partner_of_other")
        self.assertNotIn(a["partner_of_other"], [48+x for x in r["values"]])

    def test_07_pair_sizes_and_relations(self):
        for split, rows in self.parts.items():
            for lang in ("en", "ja"):
                for kind in b.KINDS:
                    groups = b.pairs(rows, lang, kind)
                    self.assertEqual(len(groups), b.ROWS[split]//4)
                    for i, j in groups:
                        self.assertEqual(rows[i]["target"] == rows[j]["target"], kind == "order")

    def test_08_perfect_answer_metric_replay(self):
        r = records(self.parts)[0]
        b.validate_record(self.parts, r)
        for split in b.SPLITS:
            for m in r["final"][split].values():
                self.assertEqual(m["accuracy"], 1)
                self.assertEqual([m[k+"_pair_accuracy"] for k in b.KINDS], [1, 1, 1])

    def test_09_saved_metric_mismatch_rejected(self):
        r = records(self.parts)[0]
        r["final"]["TRAIN"]["en"]["accuracy"] = .5
        with self.assertRaises(ValueError):
            b.validate_record(self.parts, r)

    def test_10_byte_type_and_range_rejected(self):
        for val in (-1, 256, True, 48.0):
            r = records(self.parts)[0]
            r["predictions"]["TRAIN"]["normal"][0] = val
            with self.subTest(val=val), self.assertRaises(ValueError):
                b.validate_record(self.parts, r)

    def test_11_schema_and_view_lengths_rejected(self):
        r = records(self.parts)[0]
        r["predictions"]["HOLDOUT"]["normal"].pop()
        with self.assertRaises(ValueError):
            b.validate_record(self.parts, r)
        r = records(self.parts)[0]
        r["predictions"]["TRAIN"].pop("query_blind")
        with self.assertRaises(ValueError):
            b.validate_record(self.parts, r)

    def test_12_parent_replay_flag_rejected(self):
        r = records(self.parts)[0]
        r["prediction_replayed"] = False
        with self.assertRaises(ValueError):
            b.validate_record(self.parts, r)

    def test_13_nll_is_not_fabricated_from_argmax(self):
        r = records(self.parts)[0]
        r["final"]["TRAIN"]["en"]["answer_nll"] = 100
        b.validate_record(self.parts, r)
        for val in (float("nan"), float("inf"), -1):
            r["final"]["TRAIN"]["en"]["answer_nll"] = val
            with self.assertRaises(ValueError):
                b.validate_record(self.parts, r)

    def test_14_actual_workload_and_category_totals(self):
        out = b.analyze(self.parts, records(self.parts))
        b.validate_result(payload(out["validation-summary.json"]))
        self.assertEqual((len(out["row-errors.json"]), len(out["pair-audit.json"])), (576, 864))
        for c in out["diagnostics.json"]:
            self.assertEqual(sum(c["categories"].values()), c["rows"])

    def test_15_gate_independent_of_rule_agreement(self):
        for rule in b.RULES:
            out = b.analyze(self.parts, records(self.parts, rule))
            b.validate_result(payload(out["validation-summary.json"]))

    def test_16_partner_control_has_absent_holdout_predictions(self):
        out = b.analyze(self.parts, records(self.parts, "partner_of_other"))
        held = [c for c in out["diagnostics.json"] if c["split"] == "HOLDOUT"]
        self.assertEqual(sum(c["categories"]["absent_partner_of_other"] for c in held), 384)
        self.assertEqual(sum(c["categories"]["correct"] for c in held), 0)

    def test_17_order_and_query_pair_flags(self):
        out = b.analyze(self.parts, records(self.parts))
        for p in out["pair-audit.json"]:
            self.assertTrue(p["both_correct"])
            self.assertEqual(p["same_answer"], p["kind"] == "order")

    def test_18_identity_counts_and_protection_invalid(self):
        with self.assertRaises(ValueError):
            b.analyze(self.parts, list(reversed(records(self.parts))))
        p = payload(b.analyze(self.parts, records(self.parts))["validation-summary.json"])
        p["source_blobs"].pop(b.OWN[0])
        with self.assertRaises(ValueError):
            b.validate_result(p)

    def test_19_actual_loader_parent_adapter(self):
        r = records(self.parts)
        parent = SimpleNamespace(summarize=lambda x: {"models": len(x)})
        with tempfile.TemporaryDirectory() as tmp, patch.object(b, "context", return_value=(parent, None, Audit)):
            root = Path(tmp)
            for name, value in (("split-dataset.json", self.parts), ("measurements.json", r),
                                ("summary.json", dict(validation_summary={"models": 6}))):
                (root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"), (self.parts, r))
            r[0]["predictions"]["TRAIN"]["normal"][0] = 255
            (root/"measurements.json").write_bytes(b.blob(r))
            with self.assertRaises(ValueError):
                b.load_inputs(root/"summary.json")

    def test_20_actual_run_and_postcheck(self):
        r = records(self.parts)
        base = payload(b.analyze(self.parts, r)["validation-summary.json"])
        with tempfile.TemporaryDirectory() as tmp, patch.object(b, "context", return_value=(None, None, Audit)), \
             patch.object(b, "precheck", return_value=(base["source_blobs"], base["input_sha256"])) as pre, \
             patch.object(b, "load_inputs", return_value=(self.parts, r)) as loader:
            out, parent = Path(tmp)/"out", Path(tmp)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):
                result = b.run(c242_summary=parent, output_dir=out, expected_head="synthetic-head")
            loader.assert_called_once()
            self.assertEqual(pre.call_count, 2)
            self.assertEqual(b.verify_artifacts(out, parent, "synthetic-head")[0], result)
            with self.assertRaises(ValueError):
                b.verify_artifacts(out, parent, "wrong")
            (out/"row-errors.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                b.verify_artifacts(out, parent, "synthetic-head")

    def test_21_no_executable_model_operations(self):
        forbidden = {"fit", "backward", "step", "zero_grad", "new_model", "load_state_dict", "load_bundle", "evaluate", "tensors"}
        for n in ast.walk(ast.parse(inspect.getsource(b))):
            if isinstance(n, ast.Call):
                name = n.func.id if isinstance(n.func, ast.Name) else n.func.attr if isinstance(n.func, ast.Attribute) else ""
                self.assertNotIn(name, forbidden)
        names = {n.func.id for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        self.assertTrue({"load_inputs", "analyze", "precheck"} <= names)

    def test_22_runner_embedded_python_cli_and_parser(self):
        root = Path(__file__).resolve().parents[1]
        run = (root/"tools/run_c243.ps1").read_text(encoding="utf-8")
        launch = (root/"tools/invoke_c243.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", run, re.S)
        self.assertEqual(len(blocks), 3)
        for block in blocks:
            compile(block, "embedded", "exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant)
                    and isinstance(n.value, ast.Attribute) and isinstance(n.value.value, ast.Name)
                    and n.value.value.id == "sys" and n.value.attr == "argv"}
        self.assertEqual(argv(blocks[0]), {1})
        self.assertEqual(argv(blocks[2]), {1, 2, 3})
        self.assertLess(launch.index("::ParseFile"), launch.index("$failure = $null"))
        self.assertIn("c242-v5b-balanced-recombination-530e801ba23f496aa8e0a588e0d52982", launch)

    def test_23_semantic_own_suite_and_module_append(self):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(), b.manifest()["own_tests"])
        ids = [t.id() for t in b.flatten(suite)]
        self.assertEqual(len(ids), len(set(ids)))
        parent = SimpleNamespace(regression_modules=lambda root: [f"parent_{i}" for i in range(127)])
        with patch.object(b, "parent_module", return_value=parent):
            self.assertEqual(len(b.regression_modules(Path.cwd())), b.manifest()["modules"])

    def test_24_regression_filter_on_constructed_suite(self):
        class Case(unittest.TestCase):
            def __init__(self, name):
                super().__init__()
                self.name = name
            def id(self):
                return self.name
        suite = unittest.TestSuite([Case(b.EXCLUDED)] + [Case(f"fixture_{i}") for i in range(3001)])
        with patch.object(b, "regression_modules", return_value=[]), \
             patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=suite):
            result = b.regression_suite(Path.cwd())
            self.assertEqual(result.countTestCases(), b.manifest()["focused_tests"])
            self.assertNotIn(b.EXCLUDED, {t.id() for t in b.flatten(result)})


if __name__ == "__main__":
    unittest.main(verbosity=2)
