"""C254 exact authoring tests; all models/activations here are synthetic."""
import ast
from collections import Counter
import contextlib
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from torch import nn
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c254_paired_residual_swap as b


def fixture():
    data = []
    for x, y in itertools.permutations(range(4), 2):
        for lang in ("en", "ja"):
            for order, query in itertools.product((0, 1), (0, 1)):
                group = f"0-1-{x}-{y}"; names = ("box", "book") if lang == "en" else ("箱", "本")
                r = dict(id=f"{lang}-{group}-{order}-{query}", group=group, objects=[0, 1], values=[x, y],
                    language=lang, order=order, query=query, target=48+(x if query == 0 else y),
                    split="EVAL" if tuple(sorted((x, y))) in ((0, 3), (1, 2)) else "TRAIN")
                facts = [(0, x), (1, y)]
                if order: facts.reverse()
                r["prompt"] = ";".join(names[k]+"="+str(v) for k, v in facts)+";"+names[query]+"="
                data.append(r)
    old = {(0, 1), (1, 0), (2, 3), (3, 2)}; added = {(0, 2), (2, 0), (1, 3), (3, 1)}
    return {"TRAIN": [r for r in data if tuple(r["values"]) in old]+[r for r in data if tuple(r["values"]) in added],
            "HOLDOUT": [r for r in data if tuple(r["values"]) not in old | added]}


class Model(nn.Module):
    def __init__(self, seed):
        super().__init__()
        with torch.random.fork_rng():
            torch.manual_seed(seed)
            self.backbone = nn.Module()
            self.backbone.readout_norm = nn.LayerNorm(16).double()
            self.backbone.decoder = nn.Linear(16, 256).double()
            self.backbone.local_encoder = nn.Identity()
            self.backbone.core = nn.Identity()
            self.read = nn.Identity()
        self.eval().requires_grad_(False)


def fingerprint(model):
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode()); h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def parent_entry(model, seed, parts):
    generator = torch.Generator().manual_seed(seed+101)
    signals, outputs = {}, {}
    for split, rows in parts.items():
        n = len(rows); signals[split], outputs[split] = {}, {}
        for view in b.VIEWS:
            post = torch.randn(n, 16, generator=generator, dtype=torch.float64)
            read = torch.randn(n, 16, generator=generator, dtype=torch.float64)
            if view == "query_blind":
                donors = b.donor_indices(rows, "query_swap")
                for i, j in enumerate(donors):
                    if i < j: post[j] = post[i]; read[j] = read[i]
            signals[split][view] = dict(post=post, read=read)
            with torch.no_grad(): outputs[split][view] = model.backbone.decoder(model.backbone.readout_norm(post+read))
    return dict(seed=seed, final_sha256=fingerprint(model), components={"intact": signals}, outputs={"intact": outputs})


def metric_oracle(rows, outputs):
    """Exhaustive unordered pair enumeration, independent of parent grouping code."""
    predictions = {v: t.argmax(-1).tolist() for v, t in outputs.items()}; result = {}
    losses = F.cross_entropy(outputs["normal"], torch.tensor([r["target"] for r in rows]), reduction="none")
    for lang in ("en", "ja"):
        ids = [i for i, r in enumerate(rows) if r["language"] == lang]
        acc = {v: sum(p[i] == rows[i]["target"] for i in ids)/len(ids) for v, p in predictions.items()}
        item = dict(rows=len(ids), accuracy=acc["normal"], answer_nll=float(losses[ids].mean()),
            evidence_blind_accuracy=acc["evidence_blind"], query_blind_accuracy=acc["query_blind"],
            evidence_drop=acc["normal"]-acc["evidence_blind"], query_drop=acc["normal"]-acc["query_blind"])
        for kind in ("fact", "query", "order"):
            pairs = []
            for i, j in itertools.combinations(ids, 2):
                a, c = rows[i], rows[j]
                match = (a["values"] == c["values"][::-1] and a["order"] == c["order"] and a["query"] == c["query"]) if kind == "fact" else (
                    a["group"] == c["group"] and (a["order"] == c["order"] if kind == "query" else a["query"] == c["query"]))
                if match: pairs.append((i, j))
            assert len(pairs) == len(rows)//4
            item[kind+"_pair_accuracy"] = sum(all(predictions["normal"][k] == rows[k]["target"] for k in pair) for pair in pairs)/len(pairs)
        result[lang] = item
    return result, predictions


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, name):
        p = (Path(root)/name).resolve()
        if p.parent != Path(root).resolve(): raise ValueError("unsafe child")
        return p
    @staticmethod
    def git(root, *args):
        if args == ("rev-parse", "HEAD"): return b"synthetic-head"
        if args == ("branch", "--show-current"): return b"feat/sft-target-loss"
        return b""


def payload(summary):
    pins = {f"old-{i}": "fixture" for i in range(364)}; pins.update({n: "fixture" for n in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256={f"synthetic-input-{i}": "0"*64 for i in range(599)},
        artifacts=[dict(file=n) for n in b.OUTPUTS], validation_summary=summary, production_adoption=False, gate_f_candidate=False, network_calls=0)


class C254Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.parts = fixture(); cls.models = []; cls.original = []; cls.records = []
        for seed in b.SEEDS:
            model = Model(seed); entry = parent_entry(model, seed, cls.parts)
            cls.records.append(b.score_one(model, cls.parts, entry, fingerprint))
            cls.models.append(model); cls.original.append(entry)

    def test_01_manifest_partition_and_modes(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA); self.assertEqual(b.digest(self.parts), b.SPLIT_SHA)
        self.assertEqual(b.MODES, ("self", "order_swap", "query_swap", "restored"))

    def test_02_self_and_restored_donors(self):
        for rows in self.parts.values():
            for mode in ("self", "restored"): self.assertEqual(b.donor_indices(rows, mode), list(range(len(rows))))

    def test_03_changed_donors_are_involutions(self):
        for rows in self.parts.values():
            for mode in ("order_swap", "query_swap"):
                d = b.donor_indices(rows, mode)
                self.assertEqual(sorted(d), list(range(len(rows)))); self.assertTrue(all(i != d[i] and d[d[i]] == i for i in range(len(rows))))

    def test_04_donor_semantics(self):
        for rows in self.parts.values():
            for mode in ("order_swap", "query_swap"):
                for i, j in enumerate(b.donor_indices(rows, mode)):
                    a, c = rows[i], rows[j]
                    self.assertEqual((a["language"], a["group"], a["values"]), (c["language"], c["group"], c["values"]))
                    self.assertEqual(a["query"] == c["query"], mode == "order_swap")
                    self.assertEqual(a["order"] == c["order"], mode == "query_swap")

    def test_05_target_values_do_not_select_donors(self):
        rows = copy.deepcopy(self.parts["TRAIN"]); original = b.donor_indices(rows, "query_swap")
        for r in rows: r["target"] += 20
        self.assertEqual(b.donor_indices(rows, "query_swap"), original)

    def test_06_bad_donor_identity_or_pair_rejected(self):
        rows = copy.deepcopy(self.parts["TRAIN"]); rows[0] = copy.deepcopy(rows[1])
        with self.assertRaises(ValueError): b.donor_indices(rows, "query_swap")
        rows = copy.deepcopy(self.parts["TRAIN"]); rows[0]["values"] = [3, 2]
        with self.assertRaises(ValueError): b.donor_indices(rows, "order_swap")
        with self.assertRaises(ValueError): b.donor_indices(self.parts["TRAIN"], "best")

    def test_07_all_modes_match_explicit_head_equation(self):
        model, entry, record = self.models[0], self.original[0], self.records[0]
        for mode in b.MODES:
            for split, rows in self.parts.items():
                d = b.donor_indices(rows, mode)
                for view in b.VIEWS:
                    c = entry["components"]["intact"][split][view]
                    with torch.no_grad(): expected = model.backbone.decoder(model.backbone.readout_norm(c["post"][d]+c["read"]))
                    self.assertTrue(torch.equal(record["outputs"][mode][split][view], expected))

    def test_08_self_replay_and_restoration(self):
        for record, entry in zip(self.records, self.original, strict=True):
            for s in b.SPLITS:
                for v in b.VIEWS:
                    self.assertTrue(torch.equal(record["outputs"]["self"][s][v], entry["outputs"]["intact"][s][v]))
                    self.assertTrue(torch.equal(record["outputs"]["self"][s][v], record["outputs"]["restored"][s][v]))

    def test_09_query_blind_is_exact_negative_control(self):
        for r in self.records:
            for s in b.SPLITS: self.assertTrue(torch.equal(r["outputs"]["self"][s]["query_blind"], r["outputs"]["query_swap"][s]["query_blind"]))
        entry = copy.deepcopy(self.original[0]); entry["components"]["intact"]["TRAIN"]["query_blind"]["post"][0, 0] += .1
        c = entry["components"]["intact"]["TRAIN"]["query_blind"]; m = self.models[0]
        entry["outputs"]["intact"]["TRAIN"]["query_blind"] = m.backbone.decoder(m.backbone.readout_norm(c["post"]+c["read"]))
        with self.assertRaisesRegex(ValueError, "query-blind paired"): b.score_one(m, self.parts, entry, fingerprint)

    def test_10_intact_mismatch_stops_before_swaps(self):
        entry = copy.deepcopy(self.original[0]); entry["outputs"]["intact"]["TRAIN"]["normal"] += .1
        with patch.object(b, "donor_indices", wraps=b.donor_indices) as d, self.assertRaisesRegex(ValueError, "raw-logit"):
            b.score_one(self.models[0], self.parts, entry, fingerprint)
        self.assertTrue(all(call.args[1] == "self" for call in d.call_args_list))

    def test_11_no_full_encoder_core_reader_forward(self):
        model = copy.deepcopy(self.models[0])
        with patch.object(model.backbone.core, "forward", side_effect=AssertionError("core called")), patch.object(model.read, "forward", side_effect=AssertionError("reader called")):
            r = b.score_one(model, self.parts, self.original[0], fingerprint)
        self.assertEqual((r["head_forward_calls"], r["head_row_presentations"]), (24, 1152))

    def test_12_attempted_core_call_is_blocked(self):
        model = copy.deepcopy(self.models[0]); native = model.backbone.readout_norm.forward
        def bad(x): model.backbone.core(x); return native(x)
        with patch.object(model.backbone.readout_norm, "forward", side_effect=bad), self.assertRaisesRegex(ValueError, "forward forbidden"):
            b.score_one(model, self.parts, self.original[0], fingerprint)

    def test_13_freeze_identity_norm_guards(self):
        model = copy.deepcopy(self.models[0]).train()
        with self.assertRaises(ValueError): b.score_one(model, self.parts, self.original[0], fingerprint)
        model.eval().requires_grad_(True)
        with self.assertRaises(ValueError): b.score_one(model, self.parts, self.original[0], fingerprint)
        with self.assertRaises(ValueError): b.score_one(self.models[0], self.parts, dict(self.original[0], final_sha256="wrong"), fingerprint)

    def test_14_source_vectors_and_weights_unchanged(self):
        entry = copy.deepcopy(self.original[0]); before = copy.deepcopy(entry)
        b.score_one(self.models[0], self.parts, entry, fingerprint)
        for s in b.SPLITS:
            for v in b.VIEWS:
                for k in ("post", "read"): self.assertTrue(torch.equal(entry["components"]["intact"][s][v][k], before["components"]["intact"][s][v][k]))
        self.assertEqual(fingerprint(self.models[0]), entry["final_sha256"])

    def test_15_mutation_and_hook_cleanup(self):
        model = copy.deepcopy(self.models[0]); norm = model.backbone.readout_norm
        def mutate(module, args, output):
            with torch.no_grad(): model.backbone.decoder.bias.add_(.01)
        h = norm.register_forward_hook(mutate)
        try:
            with self.assertRaises(ValueError): b.score_one(model, self.parts, self.original[0], fingerprint)
        finally: h.remove()
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))

    def test_16_all_five_metrics_and_contrasts(self):
        d, c, s = b.analyze(self.parts, self.records, self.original, metric_oracle)
        self.assertEqual((len(d), len(c), s["head_forward_calls"], s["head_row_presentations"]), (5, 40, 120, 5760))
        self.assertEqual(s["full_model_forward_calls"], 0); b.validate_result(payload(s))
        for x in c: self.assertEqual(x["changed_correct"]-x["original_correct"], x["wrong_to_correct"]-x["correct_to_wrong"])

    def test_17_record_mode_identity_count_faults(self):
        for key, val in (("head_forward_calls", 23), ("weights_preserved", False), ("replay_max_error", float("nan"))):
            r = copy.deepcopy(self.records); r[0][key] = val
            with self.assertRaises(ValueError): b.analyze(self.parts, r, self.original, metric_oracle)
        with self.assertRaises(ValueError): b.analyze(self.parts, list(reversed(self.records)), self.original, metric_oracle)

    def test_18_persisted_replay_guards(self):
        r = copy.deepcopy(self.records); r[0]["outputs"]["restored"]["TRAIN"]["normal"] += .1
        with self.assertRaises(ValueError): b.analyze(self.parts, r, self.original, metric_oracle)
        r = copy.deepcopy(self.records); r[0]["outputs"]["query_swap"]["TRAIN"]["query_blind"] += .1
        with self.assertRaises(ValueError): b.analyze(self.parts, r, self.original, metric_oracle)

    def test_19_output_schema_and_claim_guards(self):
        s = b.analyze(self.parts, self.records, self.original, metric_oracle)[2]
        for key, val in (("head_forward_calls", 119), ("new_training_steps", 1), ("capability_pass_claim", True)):
            with self.assertRaises(ValueError): b.validate_result(payload(dict(s, **{key: val})))
        x = torch.zeros(32, 256, dtype=torch.float64); x[0, 0] = float("nan")
        with self.assertRaises(ValueError): b.max_error(x, x)

    def test_20_actual_loader_replays_parent_archive(self):
        refs = [{"seed": s} for s in b.SEEDS]
        parent = SimpleNamespace(validate_result=lambda p: None, load_inputs=lambda path: (self.parts, refs),
            analyze=lambda parts, entries, refs: ([{"d": 1}], [{"c": 1}], {"fixture": 5}), manifest=lambda: {"plan": 1})
        audit = SimpleNamespace(sha=lambda path: b.C252_SHA if Path(path).name == "c252.json" else b.PARENT_SHA, read_json=Audit.read_json)
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(parent, None, None, audit)):
            root = Path(d)
            for n, v in (("summary.json", {"validation_summary": {"fixture": 5}}), ("residual-plan.json", {"plan": 1}),
                         ("diagnostics.json", [{"d": 1}]), ("contrasts.json", [{"c": 1}]), ("validation-summary.json", {"fixture": 5})):
                (root/n).write_bytes(b.blob(v))
            torch.save(dict(schema="fold-c253-frozen-outputs-v1", entries=self.original), root/"outputs.pt")
            p, r, e = b.load_inputs(root/"summary.json", root/"c252.json")
            self.assertEqual(p, self.parts); self.assertEqual(r, refs); self.assertEqual([x["seed"] for x in e], list(b.SEEDS))
            (root/"contrasts.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError): b.load_inputs(root/"summary.json", root/"c252.json")

    def test_21_actual_run_archive_postcheck(self):
        refs = [{"seed": s} for s in b.SEEDS]; models = dict(zip(b.SEEDS, self.models, strict=True))
        parent = SimpleNamespace(frozen_model=lambda ref, state, c252, factory: copy.deepcopy(models[ref["seed"]]), metrics=metric_oracle)
        checkpoint = SimpleNamespace(load_bundle=lambda path: [{}]*5); factory = SimpleNamespace(fingerprint=fingerprint)
        p = payload(b.analyze(self.parts, self.records, self.original, metric_oracle)[2])
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(parent, checkpoint, factory, Audit)), \
             patch.object(b, "precheck", return_value=(p["source_blobs"], p["input_sha256"])) as pre, \
             patch.object(b, "load_inputs", return_value=(self.parts, refs, self.original)) as loader:
            root = Path(d); out = root/"out"
            with contextlib.redirect_stdout(io.StringIO()): result = b.run(c253_summary=root/"c253.json", c252_summary=root/"c252.json", output_dir=out, expected_head="synthetic-head")
            self.assertEqual(pre.call_count, 2); loader.assert_called_once()
            with patch.object(b, "score_one", side_effect=AssertionError("no scoring in postcheck")):
                self.assertEqual(b.verify_artifacts(out, root/"c253.json", root/"c252.json", "synthetic-head")[0], result)
            with self.assertRaises(ValueError): b.verify_artifacts(out, root/"c253.json", root/"c252.json", "wrong")
            (out/"diagnostics.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError): b.verify_artifacts(out, root/"c253.json", root/"c252.json", "synthetic-head")

    def test_22_historical_suite_and_unique_own_ids(self):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(type(self)); self.assertEqual(suite.countTestCases(), b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}), b.manifest()["own_tests"])
        class Case(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def id(self): return self.name
        source = unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(), b.manifest()["focused_tests"])

    def test_23_runner_cli_paths_and_no_training(self):
        root = Path(__file__).resolve().parents[1]; runner = (root/"tools/run_c254.ps1").read_text(encoding="utf-8")
        launcher = (root/"tools/invoke_c254.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S); self.assertEqual(len(blocks), 3)
        for block in blocks: compile(block, "embedded", "exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant)
                and isinstance(n.value, ast.Attribute) and isinstance(n.value.value, ast.Name) and n.value.value.id == "sys" and n.value.attr == "argv"}
        self.assertEqual(argv(blocks[0]), {1, 2}); self.assertEqual(argv(blocks[2]), {1, 2, 3, 4})
        self.assertLess(launcher.index("::ParseFile"), launcher.index("$failure = $null"))
        self.assertIn("c253-v5b-frozen-residual-97fc39ef6e8b42cba8c2d1933ddfcbf6", launcher)
        for node in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                self.assertNotIn(name, {"fit", "backward", "step", "AdamW", "train_one", "probe_forward"})

    def test_24_residual_multiset_preserved_in_all_modes(self):
        entry = self.original[0]
        for s, rows in self.parts.items():
            for v in b.VIEWS:
                post = entry["components"]["intact"][s][v]["post"]
                for mode in b.MODES:
                    d = b.donor_indices(rows, mode)
                    self.assertTrue(torch.equal(post[d][d], post))


if __name__ == "__main__": unittest.main(verbosity=2)
