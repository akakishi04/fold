"""C244 authoring controls. Synthetic models are not scientific evidence."""
import ast
from collections import Counter, defaultdict
import contextlib
import copy
import hashlib
import inspect
import io
import itertools
import json
import math
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as b


def fixture():
    source = {s: [] for s in b.SPLITS}
    for x, y in itertools.permutations(range(4), 2):
        group = f"0-1-{x}-{y}"
        split = "TRAIN" if (x, y) in b.OLD_PAIRS else "HOLDOUT"
        provenance = "EVAL" if tuple(sorted((x, y))) in ((0, 3), (1, 2)) else "TRAIN"
        for lang in ("en", "ja"):
            for order, q in itertools.product((0, 1), repeat=2):
                r = dict(id=f"{lang}-{group}-{order}-{q}", group=group, objects=[0, 1], values=[x, y],
                         language=lang, order=order, query=q, split=provenance, target=48+(x if q == 0 else y))
                r["prompt"] = Binding.render(r)
                source[split].append(r)
    return source


class Binding:
    @staticmethod
    def render(r, mode="normal"):
        names = {"en": ("box", "book"), "ja": ("箱", "本")}[r["language"]]
        facts = list(zip(r["objects"], r["values"], strict=True))
        if r["order"]:
            facts.reverse()
        text = ";".join(names[k]+"="+("?" if mode == "evidence_blind" else str(v)) for k, v in facts)
        return text+";"+("?" if mode == "query_blind" else names[r["query"]])+"="
    @staticmethod
    def tensors(rows, mode):
        x = torch.tensor([[*r["values"], r["query"], r["order"]] for r in rows], dtype=torch.float64)
        if mode == "evidence_blind":
            x[:, :2] = .5
        if mode == "query_blind":
            x[:, 2] = .5
        return x, torch.tensor([r["target"] for r in rows])
    @staticmethod
    def parent_module():
        return Binding
    @staticmethod
    def new_baseline(full):
        result = Toy(10160)
        result.linear.load_state_dict(copy.deepcopy(full.linear.state_dict()))
        return result


class Parent:
    @staticmethod
    def validate_parts(source):
        b.require(b.digest(source) == b.SOURCE_SPLIT_SHA, "synthetic source hash")
        return source
    @staticmethod
    def discrete_metrics(rows, pred):
        out = {}
        for lang in ("en", "ja"):
            ids = [i for i, r in enumerate(rows) if r["language"] == lang]
            acc = {v: sum(pred[v][i] == rows[i]["target"] for i in ids)/len(ids) for v in b.VIEWS}
            m = dict(rows=len(ids), accuracy=acc["normal"], evidence_blind_accuracy=acc["evidence_blind"],
                     query_blind_accuracy=acc["query_blind"], evidence_drop=acc["normal"]-acc["evidence_blind"],
                     query_drop=acc["normal"]-acc["query_blind"])
            for kind in ("fact", "query", "order"):
                groups = defaultdict(list)
                for i in ids:
                    r = rows[i]
                    key = (tuple(sorted(r["values"])), r["order"], r["query"]) if kind == "fact" else (
                        r["group"], r["order"] if kind == "query" else r["query"])
                    groups[key].append(i)
                m[kind+"_pair_accuracy"] = sum(all(pred["normal"][i] == rows[i]["target"] for i in g)
                                                for g in groups.values())/len(groups)
            out[lang] = m
        return out
    @staticmethod
    def validate_record(source, record):
        for s in b.SPLITS:
            b.require(Parent.discrete_metrics(source[s], record["predictions"][s]) == record["discrete"][s], "synthetic parent replay")


class Fitting:
    @staticmethod
    def prediction_record(logits, n):
        b.require(len(logits) == 3 and all(t.shape == (n, 256) and bool(torch.isfinite(t).all()) for t in logits), "logits")
        return {v: t.argmax(-1).tolist() for v, t in zip(b.VIEWS, logits, strict=True)}
    @staticmethod
    def validate_metrics(value, n):
        b.require(set(value) == {"en", "ja"}, "languages")
        rates = ("accuracy", "evidence_blind_accuracy", "query_blind_accuracy", "fact_pair_accuracy", "query_pair_accuracy", "order_pair_accuracy")
        for m in value.values():
            b.require(m["rows"] == n//2 and set(m) == set(rates)|{"rows", "answer_nll", "evidence_drop", "query_drop"}, "schema")
            b.require(all(type(v) in (float, int) and math.isfinite(v) for v in m.values()), "finite")
            b.require(all(0 <= m[k] <= 1 for k in rates) and m["answer_nll"] >= 0, "range")
            for k in ("evidence", "query"):
                b.require(abs(m[k+"_drop"]-m["accuracy"]+m[k+"_blind_accuracy"]) <= b.TOL, "drop")
    @staticmethod
    def cell_pass(m):
        return m["accuracy"] >= .9 and all(m[k+"_pair_accuracy"] >= .8 for k in ("fact", "query", "order")) and m["evidence_drop"] >= .35 and m["query_drop"] >= .35
    @staticmethod
    def evaluate(model, rows, binding, fingerprint):
        before, training = fingerprint(model), model.training
        model.eval()
        views = [binding.tensors(rows, v) for v in b.VIEWS]
        try:
            with torch.no_grad():
                logits = [model(x, torch.zeros(len(x), dtype=torch.int64)).detach() for x, _ in views]
        finally:
            model.train(training)
        pred = Fitting.prediction_record(logits, len(rows))
        m = Parent.discrete_metrics(rows, pred)
        for l in m:
            ids = [i for i, r in enumerate(rows) if r["language"] == l]
            m[l]["answer_nll"] = float(F.cross_entropy(logits[0][ids], views[0][1][ids]))
        Fitting.validate_metrics(m, len(rows))
        b.require(fingerprint(model) == before, "mutation")
        return m, logits


class Toy(torch.nn.Module):
    def __init__(self, count=13488):
        super().__init__()
        self.linear = torch.nn.Linear(4, 256).double()
        self.padding = torch.nn.Parameter(torch.zeros(count-1280, dtype=torch.float64))
    def forward(self, tokens, tasks):
        return self.linear(tokens)


class Factory:
    @staticmethod
    def new_model(seed):
        torch.manual_seed(seed)
        return Toy()
    @staticmethod
    def fingerprint(model):
        h = hashlib.sha256()
        for k, v in sorted(model.state_dict().items()):
            h.update(k.encode())
            h.update(v.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Audit:
    @staticmethod
    def git(root, *args):
        if args[:2] == ("rev-parse", "HEAD"):
            return b"synthetic-head"
        if args[:2] == ("branch", "--show-current"):
            return b"feat/sft-target-loss"
        return b""
    @staticmethod
    def sha(path):
        return "0"*64 if str(path).startswith("synthetic-input-") else hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, name):
        p = (Path(root)/name).resolve()
        b.require(p.parent == Path(root).resolve(), "unsafe child")
        return p


def records():
    def metrics(n):
        return {l: dict(rows=n//2, accuracy=1., answer_nll=.1, evidence_blind_accuracy=.25,
            query_blind_accuracy=.5, evidence_drop=.75, query_drop=.5, fact_pair_accuracy=1.,
            query_pair_accuracy=1., order_pair_accuracy=1.) for l in ("en", "ja")}
    return [dict(seed=s, family=f, final={s: metrics(n) for s, n in b.ROWS.items()}, block_updates=[200, 200],
        fit=dict(steps=400, answer_presentations=12800), forward_calls=415, row_presentations=13568,
        checkpoint_roundtrip=True, prediction_replayed=True, reload_max_error=0., weights_changed=True) for s, f in b.identities()]


def refs_for(source):
    result = []
    for s, f in b.identities():
        model = Factory.new_model(s)
        if f == "gru_only":
            model = Binding.new_baseline(model)
        pred = {s: {v: [r["target"] if v == "normal" else 48 for r in rows] for v in b.VIEWS} for s, rows in source.items()}
        result.append(dict(seed=s, family=f, initial_sha256=Factory.fingerprint(model), final_sha256="b"*64,
            predictions=pred, discrete={s: Parent.discrete_metrics(source[s], pred[s]) for s in b.SPLITS}))
    return result


def payload(summary):
    pins = {f"parent-{i}": "fixture" for i in range(304)}
    pins.update({x: "fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, diagnostic_execution_valid=True,
        status="PASS" if summary["full_two_partner_gate"] else "FAIL", source_blobs=pins,
        input_sha256={f"synthetic-input-{i}": "0"*64 for i in range(478)},
        artifacts=[dict(file=x) for x in b.OUTPUTS], validation_summary=summary, network_calls=0, gate_f_candidate=False)


class C244Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.source = fixture()
        cls.parts = b.split_data(cls.source, Parent, Binding)
    def exercise(self):
        model = Factory.new_model(9010)
        ref = dict(seed=9010, family="full", initial_sha256=Factory.fingerprint(model))
        with contextlib.redirect_stdout(io.StringIO()):
            return b.train_one(model, self.parts, ref, fitting=Fitting, binding=Binding, factory=Factory)

    def test_01_manifest_source_split(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.source), b.SOURCE_SPLIT_SHA)
        self.assertEqual(b.digest(self.parts), b.SPLIT_SHA)
    def test_02_disjoint_groups_and_block_coverage(self):
        self.assertEqual([len(self.parts[s]) for s in b.SPLITS], [64, 32])
        self.assertEqual(self.parts["TRAIN"][:32], self.source["TRAIN"])
        self.assertEqual({tuple(r["values"]) for r in self.parts["TRAIN"][32:]}, set(b.ADDED_PAIRS))
        for k in ("id", "group", "prompt"):
            self.assertFalse({r[k] for r in self.parts["TRAIN"]}&{r[k] for r in self.parts["HOLDOUT"]})
    def test_03_other_value_is_not_sufficient_in_union_train(self):
        key = lambda r: (r["language"], r["query"], r["order"], r["values"][1-r["query"]])
        self.assertEqual(b.ceiling(self.source["TRAIN"], key), 1.)
        self.assertEqual(b.ceiling(self.parts["TRAIN"], key), .5)
    def test_04_masks_and_query_ceilings(self):
        for rows in self.parts.values():
            self.assertEqual(b.ceiling(rows, lambda r: Binding.render(r, "evidence_blind")), .25)
            self.assertEqual(b.ceiling(rows, lambda r: Binding.render(r, "query_blind")), .5)
    def test_05_tampered_source_rejected(self):
        source = copy.deepcopy(self.source)
        source["TRAIN"][0]["target"] = 255
        with self.assertRaises(ValueError):
            b.split_data(source, Parent, Binding)
    def test_06_schedule_complete_counts(self):
        counts = Counter(i for step in range(400) for i in b.balanced_indices(64, step).tolist())
        self.assertEqual(counts, {i: 200 for i in range(64)})
        self.assertEqual(b.balanced_indices(64, 0).tolist(), list(range(32)))
        self.assertEqual(b.balanced_indices(64, 1).tolist(), list(range(32, 64)))
    def test_07_actual_parent_fit_ast(self):
        fitting = b.parent_module().parent_module()
        b.audit_fit_contract(fitting)
        with patch.object(fitting, "LR", .1), self.assertRaises(ValueError):
            b.audit_fit_contract(fitting)
    def test_08_invalid_schedule_arguments(self):
        for n, step in ((32, 0), (64, -1), (64, True), (64., 0)):
            with self.assertRaises(ValueError):
                b.balanced_indices(n, step)
    def test_09_gate_and_workload(self):
        s = b.summarize(records(), Fitting)
        b.validate_result(payload(s))
        self.assertEqual((s["train_steps"], s["answer_presentations"], s["model_forward_calls"], s["row_presentations"]), (2400, 76800, 2490, 81408))
    def test_10_family_gates_independent(self):
        r = records()
        r[0]["final"]["HOLDOUT"]["en"]["query_pair_accuracy"] = 0.
        s = b.summarize(r, Fitting)
        self.assertFalse(s["full_two_partner_gate"])
        self.assertTrue(s["gru_two_partner_gate"])
        b.validate_result(payload(s))
    def test_11_schedule_and_replay_faults_rejected(self):
        r = records()
        r[0]["block_updates"] = [199, 201]
        with self.assertRaises(ValueError):
            b.summarize(r, Fitting)
        r = records()
        r[0]["reload_max_error"] = .1
        with self.assertRaises(ValueError):
            b.validate_result(payload(b.summarize(r, Fitting)))
    def test_12_actual_fit_batch_sequence(self):
        x, y = Binding.tensors(self.parts["TRAIN"], "normal")
        model, seen = Factory.new_model(9020), []
        h = model.register_forward_pre_hook(lambda m, args: seen.append(args[0].clone()))
        b.fit(model, x, y, 9021, steps=4)
        h.remove()
        self.assertTrue(all(torch.equal(a, x[b.balanced_indices(64, i)]) for i, a in enumerate(seen)))
        self.assertEqual(len(seen), 4)
    def test_13_holdout_after_fit_only(self):
        done = [False]
        native = b.fit
        def fitted(*args, **kwargs):
            value = native(*args, **kwargs)
            done[0] = True
            return value
        class Checked(Fitting):
            @staticmethod
            def evaluate(model, rows, binding, fingerprint):
                if tuple(rows[0]["values"]) in b.HELD_PAIRS:
                    self.assertTrue(done[0])
                return Fitting.evaluate(model, rows, binding, fingerprint)
        model = Factory.new_model(9010)
        ref = dict(seed=9010, family="full", initial_sha256=Factory.fingerprint(model))
        with patch.object(b, "fit", side_effect=fitted), contextlib.redirect_stdout(io.StringIO()):
            b.train_one(model, self.parts, ref, fitting=Checked, binding=Binding, factory=Factory)
    def test_14_wrong_initial_stops_before_fit(self):
        with patch.object(b, "fit") as fitted, self.assertRaises(ValueError):
            b.train_one(Factory.new_model(1), self.parts, {"initial_sha256": "wrong"}, fitting=Fitting, binding=Binding, factory=Factory)
        fitted.assert_not_called()
    def test_15_actual_training_replay_counts(self):
        r, state, raw = self.exercise()
        self.assertEqual((r["forward_calls"], r["row_presentations"]), (409, 13280))
        self.assertEqual(r["block_updates"], [200, 200])
        b.replay_one(Factory.new_model(9010), state, r, raw, self.parts, fitting=Fitting, binding=Binding, factory=Factory)
        self.assertEqual((r["forward_calls"], r["row_presentations"]), (415, 13568))
    def test_16_changed_logits_rejected(self):
        r, state, raw = self.exercise()
        raw["HOLDOUT"][0] += .1
        with self.assertRaises(ValueError):
            b.replay_one(Factory.new_model(9010), state, r, raw, self.parts, fitting=Fitting, binding=Binding, factory=Factory)
    def test_17_checkpoint_schema_order(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"models.pt"
            value = dict(schema="fold-c244-two-partner-v1", identities=[list(x) for x in b.identities()], states=[{}]*6)
            torch.save(value, path)
            self.assertEqual(len(b.load_bundle(path)), 6)
            value["identities"].reverse()
            torch.save(value, path)
            with self.assertRaises(ValueError):
                b.load_bundle(path)
    def test_18_comparator_only_identical_still_held_rows(self):
        refs = refs_for(self.source)
        for ref in refs:
            for i, r in enumerate(self.source["HOLDOUT"]):
                if tuple(r["values"]) in b.ADDED_PAIRS:
                    ref["predictions"]["HOLDOUT"]["normal"][i] = 255
            ref["discrete"]["HOLDOUT"] = Parent.discrete_metrics(self.source["HOLDOUT"], ref["predictions"]["HOLDOUT"])
        comp = b.common_comparator(self.source, refs, self.parts["HOLDOUT"], Parent)
        self.assertTrue(all(m[l]["accuracy"] == 1. and "answer_nll" not in m[l] for m in comp for l in ("en", "ja")))
    def test_19_actual_loader_initial_and_comparator(self):
        refs = refs_for(self.source)
        class Loaded(Parent):
            @staticmethod
            def load_inputs(path):
                return self.source, refs
        with patch.object(b, "context", return_value=(Loaded, None, Binding, None, None)):
            parts, result, comp = b.load_inputs("synthetic.json")
            self.assertEqual(parts, self.parts)
            self.assertEqual(result, refs)
            self.assertEqual(len(comp), 6)
            refs[0]["initial_sha256"] = refs[0]["final_sha256"]
            with self.assertRaises(ValueError):
                b.load_inputs("synthetic.json")
    def test_20_actual_six_model_run_and_postcheck(self):
        refs = refs_for(self.source)
        comp = b.common_comparator(self.source, refs, self.parts["HOLDOUT"], Parent)
        base = payload(b.summarize(records(), Fitting))
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(Parent, Fitting, Binding, Factory, Audit)), \
             patch.object(b, "precheck", return_value=(base["source_blobs"], base["input_sha256"])) as pre, \
             patch.object(b, "load_inputs", return_value=(self.parts, refs, comp)) as loader:
            out, parent, old = Path(d)/"out", Path(d)/"p.json", Path(d)/"old.json"
            with contextlib.redirect_stdout(io.StringIO()):
                p = b.run(c243_summary=parent, c242_summary=old, output_dir=out, expected_head="synthetic-head")
            loader.assert_called_once()
            self.assertEqual(pre.call_count, 2)
            self.assertEqual(b.verify_artifacts(out, old, "synthetic-head")[0], p)
            with self.assertRaises(ValueError):
                b.verify_artifacts(out, old, "wrong")
            (out/"split-dataset.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                b.verify_artifacts(out, old, "synthetic-head")
    def test_21_call_order_and_no_parent_weight_load(self):
        calls = [(n.lineno, n.func.id if isinstance(n.func, ast.Name) else n.func.attr if isinstance(n.func, ast.Attribute) else "")
                 for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n, ast.Call)]
        line = lambda name: min(i for i, k in calls if k == name)
        for a, c in (("load_inputs", "train_one"), ("new_baseline", "train_one"), ("train_one", "save"), ("save", "load_bundle"), ("load_bundle", "replay_one")):
            self.assertLess(line(a), line(c))
        self.assertNotIn("load_bundle", inspect.getsource(b.load_inputs))
    def test_22_runner_cli_parser_paths(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root/"tools/run_c244.ps1").read_text(encoding="utf-8")
        launcher = (root/"tools/invoke_c244.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S)
        self.assertEqual(len(blocks), 3)
        for block in blocks:
            compile(block, "embedded", "exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant)
                and isinstance(n.value, ast.Attribute) and isinstance(n.value.value, ast.Name) and n.value.value.id == "sys" and n.value.attr == "argv"}
        self.assertEqual(argv(blocks[0]), {1, 2})
        self.assertEqual(argv(blocks[2]), {1, 2, 3, 4})
        self.assertLess(launcher.index("::ParseFile"), launcher.index("$failure = $null"))
        self.assertIn("c243-v5b-saved-recombination-audit-9a4a52f99ee2402dbbc3cb303935217a", launcher)
        self.assertIn("c242-v5b-balanced-recombination-530e801ba23f496aa8e0a588e0d52982", launcher)
    def test_23_semantic_own_count_and_module_append(self):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(), b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}), suite.countTestCases())
        parent = SimpleNamespace(regression_modules=lambda root: [f"parent_{i}" for i in range(128)])
        with patch.object(b, "parent_module", return_value=parent):
            self.assertEqual(len(b.regression_modules(Path.cwd())), b.manifest()["modules"])
    def test_24_constructed_historical_suite_filter(self):
        class Case(unittest.TestCase):
            def __init__(self, name):
                super().__init__()
                self.name = name
            def id(self):
                return self.name
        source = unittest.TestSuite([Case(b.EXCLUDED)] + [Case(f"synthetic_{i}") for i in range(3025)])
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=source):
            suite = b.regression_suite(Path.cwd())
            self.assertEqual(suite.countTestCases(), b.manifest()["focused_tests"])
            self.assertNotIn(b.EXCLUDED, {t.id() for t in b.flatten(suite)})


if __name__ == "__main__":
    unittest.main(verbosity=2)
