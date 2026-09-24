"""Exact C255 authoring tests with self-contained synthetic heads and saved activations."""
import ast
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
from fold_lm.v05_benchmarks import model_c255_value_residual_swap as b


def fixture():
    rows = []
    for x, y in itertools.permutations(range(4), 2):
        for lang in ("en", "ja"):
            for order, query in itertools.product((0, 1), (0, 1)):
                names = ("box", "book") if lang == "en" else ("箱", "本")
                group = f"0-1-{x}-{y}"; facts = [(0, x), (1, y)]
                if order: facts.reverse()
                rows.append(dict(id=f"{lang}-{group}-{order}-{query}", group=group, objects=[0, 1], values=[x, y],
                    language=lang, order=order, query=query, target=48+(x if query == 0 else y),
                    split="EVAL" if tuple(sorted((x, y))) in ((0, 3), (1, 2)) else "TRAIN",
                    prompt=";".join(names[k]+"="+str(v) for k, v in facts)+";"+names[query]+"="))
    old = {(0, 1), (1, 0), (2, 3), (3, 2)}; added = {(0, 2), (2, 0), (1, 3), (3, 1)}
    return {"TRAIN": [r for r in rows if tuple(r["values"]) in old]+[r for r in rows if tuple(r["values"]) in added],
            "HOLDOUT": [r for r in rows if tuple(r["values"]) not in old | added]}


class Model(nn.Module):
    def __init__(self, seed):
        super().__init__()
        with torch.random.fork_rng():
            torch.manual_seed(seed); self.backbone = nn.Module()
            self.backbone.readout_norm = nn.LayerNorm(16).double()
            self.backbone.decoder = nn.Linear(16, 256).double()
            self.backbone.local_encoder = nn.Identity(); self.backbone.core = nn.Identity(); self.read = nn.Identity()
        self.eval().requires_grad_(False)


def fingerprint(model):
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode()); h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def metric_oracle(rows, outputs):
    pred = {v: t.argmax(-1).tolist() for v, t in outputs.items()}; result = {}
    losses = F.cross_entropy(outputs["normal"], torch.tensor([r["target"] for r in rows]), reduction="none")
    for lang in ("en", "ja"):
        ids = [i for i, r in enumerate(rows) if r["language"] == lang]
        acc = {v: sum(p[i] == rows[i]["target"] for i in ids)/len(ids) for v, p in pred.items()}
        m = dict(rows=len(ids), accuracy=acc["normal"], answer_nll=float(losses[ids].mean()),
            evidence_blind_accuracy=acc["evidence_blind"], query_blind_accuracy=acc["query_blind"],
            evidence_drop=acc["normal"]-acc["evidence_blind"], query_drop=acc["normal"]-acc["query_blind"])
        for kind in ("fact", "query", "order"):
            pairs = []
            for i, j in itertools.combinations(ids, 2):
                a, c = rows[i], rows[j]
                ok = (a["values"] == c["values"][::-1] and a["order"] == c["order"] and a["query"] == c["query"]) if kind == "fact" else (
                    a["group"] == c["group"] and (a["order"] == c["order"] if kind == "query" else a["query"] == c["query"]))
                if ok: pairs.append((i, j))
            assert len(pairs) == len(rows)//4
            m[kind+"_pair_accuracy"] = sum(all(pred["normal"][k] == rows[k]["target"] for k in p) for p in pairs)/len(pairs)
        result[lang] = m
    return result, pred


def saved(model, seed, parts):
    g = torch.Generator().manual_seed(seed+101); components, outputs = {}, {}
    for split, rows in parts.items():
        components[split], outputs[split] = {}, {}; d = b.donors(rows)
        for view in b.VIEWS:
            post = torch.randn(len(rows), 16, generator=g, dtype=torch.float64)
            read = torch.randn(len(rows), 16, generator=g, dtype=torch.float64)
            if view == "evidence_blind":
                for i, j in enumerate(d):
                    if i < j: post[j] = post[i]; read[j] = read[i]
            components[split][view] = dict(post=post, read=read)
            outputs[split][view] = model.backbone.decoder(model.backbone.readout_norm(post+read))
    entry = dict(seed=seed, final_sha256=fingerprint(model), components={"intact": components}, outputs={"intact": outputs})
    prior = dict(seed=seed, final_sha256=fingerprint(model), outputs={"self": outputs})
    for mode in ("order_swap", "query_swap"):
        prior["outputs"][mode] = {}
        for split, rows in parts.items():
            keys = {(r["language"], r["group"], r["order"], r["query"]): i for i, r in enumerate(rows)}
            d = [keys[(r["language"], r["group"], 1-r["order"] if mode == "order_swap" else r["order"],
                       1-r["query"] if mode == "query_swap" else r["query"])] for r in rows]
            prior["outputs"][mode][split] = {v: model.backbone.decoder(model.backbone.readout_norm(components[split][v]["post"][d]+components[split][v]["read"])) for v in b.VIEWS}
    return entry, prior


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
    pins = {f"old-{i}": "fixture" for i in range(370)}; pins.update({n: "fixture" for n in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256={f"synthetic-input-{i}": "0"*64 for i in range(611)},
        artifacts=[dict(file=n) for n in b.OUTPUTS], validation_summary=summary, production_adoption=False, gate_f_candidate=False, network_calls=0)


class C255Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.parts = fixture(); cls.models = []; cls.original = []; cls.prior = []; cls.records = []
        for seed in b.SEEDS:
            model = Model(seed); entry, prior = saved(model, seed, cls.parts)
            cls.models.append(model); cls.original.append(entry); cls.prior.append(prior)
            cls.records.append(b.score_one(model, cls.parts, entry, fingerprint))

    def test_01_manifest_and_exact_partition(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA); self.assertEqual(b.digest(self.parts), b.SPLIT_SHA)

    def test_02_donor_involution_and_no_self(self):
        for rows in self.parts.values():
            d = b.donors(rows); self.assertEqual(sorted(d), list(range(len(rows))))
            self.assertTrue(all(i != j and d[j] == i for i, j in enumerate(d)))

    def test_03_query_order_language_fixed_values_reverse(self):
        for rows in self.parts.values():
            for i, j in enumerate(b.donors(rows)):
                for k in ("language", "order", "query", "objects"): self.assertEqual(rows[i][k], rows[j][k])
                self.assertEqual(rows[i]["values"], rows[j]["values"][::-1]); self.assertNotEqual(rows[i]["target"], rows[j]["target"])

    def test_04_targets_do_not_select_donor(self):
        rows = copy.deepcopy(self.parts["TRAIN"]); wanted = b.donors(rows)
        for r in rows: r["target"] += 20
        self.assertEqual(b.donors(rows), wanted)

    def test_05_missing_duplicate_and_wrong_pair_rejected(self):
        rows = copy.deepcopy(self.parts["TRAIN"]); rows[0] = copy.deepcopy(rows[1])
        with self.assertRaises(ValueError): b.donors(rows)
        rows = copy.deepcopy(self.parts["TRAIN"]); rows[0]["values"] = [8, 9]
        with self.assertRaises(ValueError): b.donors(rows)
        with self.assertRaises(ValueError): b.donors([])

    def test_06_all_forward_equations(self):
        m, e, r = self.models[0], self.original[0], self.records[0]
        for mode in b.MODES:
            for s, rows in self.parts.items():
                d = b.donors(rows)
                for v in b.VIEWS:
                    c = e["components"]["intact"][s][v]
                    p = c["post"][d] if mode in ("value_swap", "coherent_swap") else c["post"]
                    read = c["read"][d] if mode == "coherent_swap" else c["read"]
                    self.assertTrue(torch.equal(r["outputs"][mode][s][v], m.backbone.decoder(m.backbone.readout_norm(p+read))))

    def test_07_coherent_control_matches_donor_not_recipient(self):
        for r, e in zip(self.records, self.original, strict=True):
            for s, rows in self.parts.items():
                d = b.donors(rows)
                for v in b.VIEWS: self.assertLessEqual(b.replay(r["outputs"]["coherent_swap"][s][v], e["outputs"]["intact"][s][v][d]), b.TOL)
        self.assertNotIn("coherent_swap", b.SCORED_MODES)

    def test_08_evidence_blind_negative_control(self):
        for r in self.records:
            for s in b.SPLITS: self.assertTrue(torch.equal(r["outputs"]["self"][s]["evidence_blind"], r["outputs"]["value_swap"][s]["evidence_blind"]))
        e = copy.deepcopy(self.original[0]); e["components"]["intact"]["TRAIN"]["evidence_blind"]["post"][0, 0] += .1
        with self.assertRaisesRegex(ValueError, "masked fact-pair"): b.score_one(self.models[0], self.parts, e, fingerprint)

    def test_09_self_mismatch_stops_before_swaps(self):
        e = copy.deepcopy(self.original[0]); e["outputs"]["intact"]["TRAIN"]["normal"] += .1
        calls = []; h = self.models[0].backbone.decoder.register_forward_hook(lambda m, a, o: calls.append(1))
        try:
            with self.assertRaisesRegex(ValueError, "replay"): b.score_one(self.models[0], self.parts, e, fingerprint)
        finally: h.remove()
        self.assertEqual(len(calls), 1)

    def test_10_restore_exactly(self):
        for r in self.records:
            for s in b.SPLITS:
                for v in b.VIEWS: self.assertTrue(torch.equal(r["outputs"]["self"][s][v], r["outputs"]["restored"][s][v]))

    def test_11_no_full_core_reader_calls(self):
        m = copy.deepcopy(self.models[0])
        with patch.object(m.backbone.core, "forward", side_effect=AssertionError("core")), patch.object(m.read, "forward", side_effect=AssertionError("reader")):
            self.assertEqual(b.score_one(m, self.parts, self.original[0], fingerprint)["head_forward_calls"], 24)

    def test_12_nested_core_call_blocked(self):
        m = copy.deepcopy(self.models[0]); native = m.backbone.readout_norm.forward
        def bad(x): m.backbone.core(x); return native(x)
        with patch.object(m.backbone.readout_norm, "forward", side_effect=bad), self.assertRaisesRegex(ValueError, "forward forbidden"):
            b.score_one(m, self.parts, self.original[0], fingerprint)
        self.assertTrue(all(not x._forward_hooks and not x._forward_pre_hooks for x in m.modules()))

    def test_13_frozen_state_and_identity(self):
        m = copy.deepcopy(self.models[0]).train()
        with self.assertRaises(ValueError): b.score_one(m, self.parts, self.original[0], fingerprint)
        m.eval().requires_grad_(True)
        with self.assertRaises(ValueError): b.score_one(m, self.parts, self.original[0], fingerprint)
        with self.assertRaises(ValueError): b.score_one(self.models[0], self.parts, dict(self.original[0], final_sha256="wrong"), fingerprint)

    def test_14_source_activation_and_weight_preservation(self):
        e = copy.deepcopy(self.original[0]); before = copy.deepcopy(e)
        b.score_one(self.models[0], self.parts, e, fingerprint)
        for s in b.SPLITS:
            for v in b.VIEWS:
                for k in ("post", "read"): self.assertTrue(torch.equal(e["components"]["intact"][s][v][k], before["components"]["intact"][s][v][k]))
        self.assertEqual(fingerprint(self.models[0]), e["final_sha256"])

    def test_15_mutation_and_cleanup(self):
        m = copy.deepcopy(self.models[0])
        def mutate(mod, args, output): m.backbone.decoder.bias.add_(.01)
        h = m.backbone.readout_norm.register_forward_hook(mutate)
        try:
            with self.assertRaises(ValueError): b.score_one(m, self.parts, self.original[0], fingerprint)
        finally: h.remove()
        self.assertTrue(all(not x._forward_hooks and not x._forward_pre_hooks for x in m.modules()))

    def test_16_all_five_counts_comparators_and_transitions(self):
        d, c, s = b.analyze(self.parts, self.records, self.original, self.prior, metric_oracle)
        self.assertEqual((len(d), len(c), s["head_forward_calls"], s["head_row_presentations"]), (5, 20, 120, 5760))
        b.validate_result(payload(s)); self.assertEqual(s["full_model_forward_calls"], 0)
        for x in c:
            self.assertEqual(x["changed_correct"]-x["original_correct"], x["wrong_to_correct"]-x["correct_to_wrong"])
            self.assertIn("accuracy", x["c254_query_metrics"])

    def test_17_bad_record_counts_and_order(self):
        for k, v in (("head_forward_calls", 23), ("replay_max_error", float("nan")), ("weights_preserved", False)):
            r = copy.deepcopy(self.records); r[0][k] = v
            with self.assertRaises(ValueError): b.analyze(self.parts, r, self.original, self.prior, metric_oracle)
        with self.assertRaises(ValueError): b.analyze(self.parts, list(reversed(self.records)), self.original, self.prior, metric_oracle)

    def test_18_persisted_coherent_and_restore_corruption(self):
        for mode in ("coherent_swap", "restored"):
            r = copy.deepcopy(self.records); r[0]["outputs"][mode]["TRAIN"]["normal"] += .1
            with self.assertRaises(ValueError): b.analyze(self.parts, r, self.original, self.prior, metric_oracle)

    def test_19_nonfinite_and_claim_guard(self):
        x = torch.zeros(32, 256, dtype=torch.float64); x[0, 0] = float("nan")
        with self.assertRaises(ValueError): b.replay(x, x)
        s = b.analyze(self.parts, self.records, self.original, self.prior, metric_oracle)[2]
        for k, v in (("new_training_steps", 1), ("capability_pass_claim", True), ("head_forward_calls", 119)):
            with self.assertRaises(ValueError): b.validate_result(payload(dict(s, **{k: v})))

    def test_20_actual_loader_parent_archive_and_signatures(self):
        refs = [{"seed": s} for s in b.SEEDS]; marker = object()
        parent = SimpleNamespace(validate_result=lambda p: None, load_inputs=lambda x, y: (self.parts, refs, self.original),
            analyze=lambda p, r, o, metric: ([1], [2], {"fixture": 5}) if metric is marker else None, manifest=lambda: {"plan": 1})
        hashes = {"c254.json": b.PARENT_SHA, "c253.json": b.C253_SHA, "c252.json": b.C252_SHA}
        a = SimpleNamespace(sha=lambda path: hashes[Path(path).name], read_json=Audit.read_json)
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(parent, SimpleNamespace(metrics=marker), None, None, a)):
            root = Path(d)
            for name, v in (("c254.json", {"validation_summary": {"fixture": 5}}), ("swap-plan.json", {"plan": 1}), ("diagnostics.json", [1]), ("contrasts.json", [2]), ("validation-summary.json", {"fixture": 5})):
                (root/name).write_bytes(b.blob(v))
            torch.save(dict(schema="fold-c254-head-outputs-v1", records=self.prior), root/"head-outputs.pt")
            parts, got, original, prior = b.load_inputs(root/"c254.json", root/"c253.json", root/"c252.json")
            self.assertEqual(parts, self.parts); self.assertEqual(got, refs); self.assertEqual(len(prior), 5)
            (root/"contrasts.json").write_text("[]")
            with self.assertRaises(ValueError): b.load_inputs(root/"c254.json", root/"c253.json", root/"c252.json")

    def test_21_actual_five_model_run_archive_postcheck(self):
        refs = [{"seed": s} for s in b.SEEDS]; models = dict(zip(b.SEEDS, self.models, strict=True))
        diagnostic = SimpleNamespace(metrics=metric_oracle, frozen_model=lambda ref, state, c252, f: copy.deepcopy(models[ref["seed"]]))
        c252 = SimpleNamespace(load_bundle=lambda path: [{}]*5); f = SimpleNamespace(fingerprint=fingerprint)
        p = payload(b.analyze(self.parts, self.records, self.original, self.prior, metric_oracle)[2])
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(None, diagnostic, c252, f, Audit)), \
             patch.object(b, "precheck", return_value=(p["source_blobs"], p["input_sha256"])) as pre, \
             patch.object(b, "load_inputs", return_value=(self.parts, refs, self.original, self.prior)) as loader:
            root = Path(d); out = root/"out"; parents = [root/n for n in ("c254.json", "c253.json", "c252.json")]
            with contextlib.redirect_stdout(io.StringIO()): result = b.run(c254_summary=parents[0], c253_summary=parents[1], c252_summary=parents[2], output_dir=out, expected_head="synthetic-head")
            loader.assert_called_once(); self.assertEqual(pre.call_count, 2)
            with patch.object(b, "score_one", side_effect=AssertionError("postcheck must not score")):
                self.assertEqual(b.verify_artifacts(out, *parents, "synthetic-head")[0], result)
            with self.assertRaises(ValueError): b.verify_artifacts(out, *parents, "wrong")
            (out/"diagnostics.json").write_text("[]")
            with self.assertRaises(ValueError): b.verify_artifacts(out, *parents, "synthetic-head")

    def test_22_actual_own_ids_and_constructed_historical_filter(self):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(type(self)); self.assertEqual(suite.countTestCases(), b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}), 24)
        class Case(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def id(self): return self.name
        source = unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(), b.manifest()["focused_tests"])

    def test_23_runner_cli_and_no_training(self):
        root = Path(__file__).resolve().parents[1]; runner = (root/"tools/run_c255.ps1").read_text(encoding="utf-8")
        launcher = (root/"tools/invoke_c255.ps1").read_text(encoding="utf-8"); blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S)
        self.assertEqual(len(blocks), 3)
        for block in blocks: compile(block, "embedded", "exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant)
                and isinstance(n.value, ast.Attribute) and isinstance(n.value.value, ast.Name) and n.value.value.id == "sys" and n.value.attr == "argv"}
        self.assertEqual(argv(blocks[0]), {1, 2, 3}); self.assertEqual(argv(blocks[2]), {1, 2, 3, 4, 5})
        self.assertLess(launcher.index("::ParseFile"), launcher.index("$failure = $null"))
        self.assertIn("c254-v5b-paired-residual-e324dc81a0364f92820cf8da7f3a0172", launcher)
        for node in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                self.assertNotIn(name, {"fit", "backward", "step", "AdamW", "train_one", "probe_forward"})

    def test_24_compare_parent_self_and_exclude_coherent_accuracy(self):
        prior = copy.deepcopy(self.prior); prior[0]["outputs"]["self"]["TRAIN"]["normal"] += .1
        with self.assertRaises(ValueError): b.analyze(self.parts, self.records, self.original, prior, metric_oracle)
        d = b.analyze(self.parts, self.records, self.original, self.prior, metric_oracle)[0]
        self.assertTrue(all(set(x["metrics"]) == set(b.SCORED_MODES) and x["coherent_donor_replay"] for x in d))


if __name__ == "__main__": unittest.main(verbosity=2)
