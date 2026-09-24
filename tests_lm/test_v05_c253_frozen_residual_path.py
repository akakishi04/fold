"""C253 authoring tests use synthetic parent-compatible models, not accepted checkpoints."""
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
from fold_lm.v05_benchmarks import model_c253_frozen_residual_path as b


class Core(nn.Module):
    def __init__(self):
        super().__init__(); self.linear = nn.Linear(16, 16); self.context = nn.Linear(16, 16)
    def forward(self, working, context, *, route_index):
        return torch.tanh(self.linear(working) + self.context(context) + route_index * .1)


class Backbone(nn.Module):
    def __init__(self):
        super().__init__()
        self.config = SimpleNamespace(width=16, max_tokens=48, next_route=0, instruction_route=1, internal_steps=2)
        self.byte_embedding = nn.Embedding(259, 16, padding_idx=256)
        self.local_encoder = nn.GRU(16, 16, batch_first=True)
        self.core = Core(); self.readout_norm = nn.LayerNorm(16); self.decoder = nn.Linear(16, 256)
        self.padding = nn.Parameter(torch.zeros(13488 - sum(p.numel() for p in self.parameters())))
        self.double()
    def forward(self, tokens, tasks):
        valid = tokens != 256; encoded, _ = self.local_encoder(self.byte_embedding(tokens))
        context = encoded * valid.unsqueeze(-1); working = torch.zeros_like(context)
        for _ in range(self.config.internal_steps):
            next_state = self.core(working, context, route_index=0)
            other = self.core(working, context, route_index=1)
            working = torch.where(tasks.bool()[:, None, None], other, next_state)
        post = working[torch.arange(len(tokens)), valid.sum(1)-1]
        return self.decoder(self.readout_norm(post))


class Head(nn.Module):
    def __init__(self):
        super().__init__()
        self.query = nn.Linear(16, 16, bias=False).double()
        self.key = nn.Linear(16, 16, bias=False).double()
        self.output = nn.Linear(16, 16, bias=False).double()


class ToyAligned(nn.Module):
    def __init__(self, backbone, seed):
        super().__init__(); self.backbone = backbone
        with torch.random.fork_rng():
            torch.manual_seed(seed+248000); self.read = Head()
        self.wrong_query = False
    def forward(self, tokens, tasks):
        captured = {}; valid = tokens != 256; eos = valid.sum(1)-1
        def local(module, args, output):
            captured["local"] = output[0] * valid.unsqueeze(-1)
        def inject(module, args):
            memory = captured["local"]; pre = memory[torch.arange(len(tokens)), eos]
            query = self.read.query(args[0] if self.wrong_query else pre)
            weights = ((self.read.key(memory)*query[:, None, :]).sum(-1)/4).masked_fill(~valid, float("-inf")).softmax(-1)
            return (args[0] + self.read.output((weights[:, :, None]*memory).sum(1)),)
        handles = [self.backbone.local_encoder.register_forward_hook(local),
                   self.backbone.readout_norm.register_forward_pre_hook(inject)]
        try:
            return self.backbone(tokens, tasks)
        finally:
            for handle in handles: handle.remove()


class Factory:
    @staticmethod
    def new_model(seed):
        with torch.random.fork_rng():
            torch.manual_seed(seed); return Backbone()
    @staticmethod
    def fingerprint(model):
        h = hashlib.sha256()
        for key, value in sorted(model.state_dict().items()):
            h.update(key.encode()); h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    @staticmethod
    def render(r, view="normal"):
        names = ("box", "book") if r["language"] == "en" else ("箱", "本")
        facts = list(zip(r["objects"], r["values"], strict=True))
        if r["order"]: facts.reverse()
        return ";".join(names[k]+"="+("?" if view == "evidence_blind" else str(v)) for k, v in facts) + ";" + ("?" if view == "query_blind" else names[r["query"]]) + "="
    @staticmethod
    def tensors(rows, view):
        def encode(row):
            ids = [257, *Binding.render(row, view).encode(), 258]
            return ids + [256]*(48-len(ids))
        return torch.tensor([encode(r) for r in rows], dtype=torch.int64), torch.tensor([r["target"] for r in rows], dtype=torch.int64)


def fixture():
    data = []
    for x, y in itertools.permutations(range(4), 2):
        for lang in ("en", "ja"):
            for order, query in itertools.product((0, 1), (0, 1)):
                group = f"0-1-{x}-{y}"
                r = dict(id=f"{lang}-{group}-{order}-{query}", group=group, objects=[0, 1], values=[x, y], language=lang,
                         order=order, query=query, target=48+(x if query == 0 else y),
                         split="EVAL" if tuple(sorted((x, y))) in ((0, 3), (1, 2)) else "TRAIN")
                r["prompt"] = Binding.render(r); data.append(r)
    old = {(0, 1), (1, 0), (2, 3), (3, 2)}
    added = {(0, 2), (2, 0), (1, 3), (3, 1)}
    return {"TRAIN": [r for r in data if tuple(r["values"]) in old] + [r for r in data if tuple(r["values"]) in added],
            "HOLDOUT": [r for r in data if tuple(r["values"]) not in old | added]}


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, name):
        result = (Path(root)/name).resolve()
        if result.parent != Path(root).resolve(): raise ValueError("unsafe child")
        return result
    @staticmethod
    def git(root, *args):
        if args == ("rev-parse", "HEAD"): return b"synthetic-head"
        if args == ("branch", "--show-current"): return b"feat/sft-target-loss"
        return b""


def baseline(seed, parts):
    model = ToyAligned(Factory.new_model(seed), seed).eval().requires_grad_(False)
    ref = dict(seed=seed, family="full", arm="aligned_precore_read", final_sha256=Factory.fingerprint(model), predictions={}, final={})
    for split, rows in parts.items():
        with torch.no_grad():
            outputs = {v: model(Binding.tensors(rows, v)[0], torch.zeros(len(rows), dtype=torch.int64)) for v in b.VIEWS}
        ref["final"][split], ref["predictions"][split] = b.metrics(rows, outputs)
    return model, ref


def payload(summary):
    pins = {f"old-{i}": "fixture" for i in range(358)}; pins.update({n: "fixture" for n in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256={f"synthetic-input-{i}": "0"*64 for i in range(587)},
        artifacts=[dict(file=n) for n in b.OUTPUTS], validation_summary=summary,
        gate_f_candidate=False, production_adoption=False, network_calls=0)


class C253Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.parts = fixture(); cls.entries = []; cls.refs = []; cls.states = []
        for seed in b.SEEDS:
            model, ref = baseline(seed, cls.parts)
            cls.entries.append(b.diagnose_one(model, cls.parts, ref, Binding, Factory.fingerprint))
            cls.refs.append(ref); cls.states.append(copy.deepcopy(model.state_dict()))
        cls.model, _ = baseline(9010, cls.parts)
        cls.tokens = Binding.tensors(cls.parts["TRAIN"][:4], "normal")[0]; cls.tasks = torch.zeros(4, dtype=torch.int64)

    def test_01_manifest_and_partition(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts), b.PARENT_ARTIFACTS["split-dataset.json"])

    def test_02_intact_equals_original(self):
        with torch.no_grad(): expected = self.model(self.tokens, self.tasks)
        actual, _ = b.probe_forward(self.model, self.tokens, self.tasks, "intact")
        self.assertTrue(torch.equal(actual, expected))

    def test_03_intervention_equations(self):
        for mode in b.MODES:
            out, c = b.probe_forward(self.model, self.tokens, self.tasks, mode)
            z = c["pre"]+c["read"] if mode == "pre_residual" else c["read"] if mode == "reader_only" else c["post"]+c["read"]
            with torch.no_grad(): expected = self.model.backbone.decoder(self.model.backbone.readout_norm(z))
            self.assertTrue(torch.equal(out, expected))

    def test_04_reader_and_core_components_do_not_change(self):
        signals = [b.probe_forward(self.model, self.tokens, self.tasks, mode)[1] for mode in b.MODES]
        self.assertTrue(all(torch.equal(c[k], signals[0][k]) for c in signals for k in c))

    def test_05_restore_exact_logits(self):
        outputs = [b.probe_forward(self.model, self.tokens, self.tasks, mode)[0] for mode in b.MODES]
        self.assertTrue(torch.equal(outputs[0], outputs[-1]))
        self.assertFalse(torch.equal(outputs[0], outputs[2]))

    def test_06_frozen_and_mode_guards(self):
        model = copy.deepcopy(self.model).train()
        with self.assertRaises(ValueError): b.probe_forward(model, self.tokens, self.tasks, "intact")
        model.eval().requires_grad_(True)
        with self.assertRaises(ValueError): b.probe_forward(model, self.tokens, self.tasks, "intact")
        with self.assertRaises(ValueError): b.probe_forward(self.model, self.tokens, self.tasks, "unknown")

    def test_07_exception_removes_both_hook_layers(self):
        model = copy.deepcopy(self.model)
        with patch.object(model.read.output, "forward", side_effect=ValueError("fixture")), self.assertRaises(ValueError):
            b.probe_forward(model, self.tokens, self.tasks, "pre_residual")
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))
        b.probe_forward(model, self.tokens, self.tasks, "intact")

    def test_08_wrong_query_provenance_rejected(self):
        model = copy.deepcopy(self.model); model.wrong_query = True
        with self.assertRaisesRegex(ValueError, "query invariant"):
            b.probe_forward(model, self.tokens, self.tasks, "intact")

    def test_09_invalid_task_and_eos(self):
        with self.assertRaises(ValueError): b.probe_forward(self.model, self.tokens, self.tasks+1, "intact")
        bad = self.tokens.clone(); bad[bad == 258] = 1
        with self.assertRaises(ValueError): b.probe_forward(self.model, bad, self.tasks, "intact")

    def test_10_unsupported_normalization_rejected(self):
        model = copy.deepcopy(self.model); model.backbone.readout_norm = nn.Identity().eval()
        with self.assertRaisesRegex(ValueError, "normalization"):
            b.probe_forward(model, self.tokens, self.tasks, "reader_only")

    def test_11_weight_mutation_is_invalid(self):
        model, ref = baseline(9012, self.parts)
        def mutate(module, args, output):
            with torch.no_grad(): module.backbone.decoder.bias.add_(.001)
        hook = model.register_forward_hook(mutate)
        try:
            with self.assertRaisesRegex(ValueError, "weight mutation"):
                b.diagnose_one(model, self.parts, ref, Binding, Factory.fingerprint)
        finally: hook.remove()

    def test_12_parent_mismatch_stops_before_intervention(self):
        model, ref = baseline(9013, self.parts); ref["predictions"]["TRAIN"]["normal"][0] = 255
        with patch.object(b, "probe_forward", wraps=b.probe_forward) as probe, self.assertRaisesRegex(ValueError, "parent prediction"):
            b.diagnose_one(model, self.parts, ref, Binding, Factory.fingerprint)
        self.assertEqual(probe.call_count, 6)
        self.assertTrue(all(c.args[3] == "intact" for c in probe.call_args_list))

    def test_13_checkpoint_load_is_strict(self):
        parent = SimpleNamespace(AlignedPrecoreReadout=ToyAligned)
        m = b.frozen_model(self.refs[0], self.states[0], parent, Factory)
        self.assertEqual(Factory.fingerprint(m), self.refs[0]["final_sha256"])
        self.assertFalse(any(p.requires_grad for p in m.parameters()))
        with self.assertRaises(ValueError): b.frozen_model(dict(self.refs[0], final_sha256="wrong"), self.states[0], parent, Factory)
        state = dict(self.states[0]); state.pop(next(iter(state)))
        with self.assertRaises(RuntimeError): b.frozen_model(self.refs[0], state, parent, Factory)

    def test_14_perfect_metrics_and_pairs(self):
        for rows in self.parts.values():
            logits = torch.zeros(len(rows), 256, dtype=torch.float64)
            logits[torch.arange(len(rows)), [r["target"] for r in rows]] = 10
            masked = torch.zeros_like(logits); masked[:, 48] = 10
            measured, _ = b.metrics(rows, dict(normal=logits, evidence_blind=masked, query_blind=masked))
            for m in measured.values():
                self.assertEqual((m["accuracy"], m["fact_pair_accuracy"], m["query_pair_accuracy"], m["order_pair_accuracy"]), (1, 1, 1, 1))
                self.assertEqual((m["evidence_drop"], m["query_drop"]), (.75, .75))

    def test_15_bad_output_schema_or_nonfinite_rejected(self):
        outputs = copy.deepcopy(self.entries[0]["outputs"]["intact"]["TRAIN"])
        outputs["normal"][0, 0] = float("nan")
        with self.assertRaises(ValueError): b.metrics(self.parts["TRAIN"], outputs)
        outputs["normal"] = torch.zeros(63, 256, dtype=torch.float64)
        with self.assertRaises(ValueError): b.metrics(self.parts["TRAIN"], outputs)
        with self.assertRaises(ValueError): b.metrics(self.parts["TRAIN"], {})

    def test_16_actual_all_five_diagnostics_counts(self):
        diagnostics, contrasts, summary = b.analyze(self.parts, self.entries, self.refs)
        self.assertEqual((len(diagnostics), len(contrasts), summary["model_forward_calls"], summary["row_presentations"]), (5, 40, 120, 5760))
        b.validate_result(payload(summary))
        self.assertFalse(summary["capability_pass_claim"])

    def test_17_bad_identity_and_workload_rejected(self):
        with self.assertRaises(ValueError): b.analyze(self.parts, list(reversed(self.entries)), self.refs)
        entries = copy.deepcopy(self.entries); entries[0]["forward_calls"] = 23
        with self.assertRaises(ValueError): b.analyze(self.parts, entries, self.refs)
        entries = copy.deepcopy(self.entries); entries[0]["outputs"].pop("reader_only")
        with self.assertRaises(ValueError): b.analyze(self.parts, entries, self.refs)

    def test_18_persisted_components_must_stay_identical(self):
        entries = copy.deepcopy(self.entries); entries[0]["components"]["pre_residual"]["TRAIN"]["normal"]["read"][0, 0] += .1
        with self.assertRaisesRegex(ValueError, "component invariance"):
            b.analyze(self.parts, entries, self.refs)

    def test_19_restored_raw_logits_checked(self):
        entries = copy.deepcopy(self.entries); entries[0]["outputs"]["restored"]["TRAIN"]["normal"] += .1
        with self.assertRaisesRegex(ValueError, "restored output"):
            b.analyze(self.parts, entries, self.refs)

    def test_20_real_run_archive_and_postcheck(self):
        parent = SimpleNamespace(AlignedPrecoreReadout=ToyAligned, load_bundle=lambda path: copy.deepcopy(self.states))
        summary = b.analyze(self.parts, self.entries, self.refs)[2]; p = payload(summary)
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(parent, None, None, Binding, Factory, Audit)), \
             patch.object(b, "precheck", return_value=(p["source_blobs"], p["input_sha256"])) as pre, \
             patch.object(b, "load_inputs", return_value=(self.parts, self.refs)) as loader:
            out = Path(d)/"out"; source = Path(d)/"summary.json"
            with contextlib.redirect_stdout(io.StringIO()): result = b.run(c252_summary=source, output_dir=out, expected_head="synthetic-head")
            self.assertEqual(pre.call_count, 2); loader.assert_called_once()
            with patch.object(b, "probe_forward", side_effect=AssertionError("postcheck must not infer")):
                self.assertEqual(b.verify_artifacts(out, source, "synthetic-head")[0], result)
            with self.assertRaises(ValueError): b.verify_artifacts(out, source, "wrong")
            (out/"contrasts.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError): b.verify_artifacts(out, source, "synthetic-head")
            self.assertEqual({f.name for f in out.iterdir()}, b.OUTPUTS | {"summary.json"})

    def test_21_actual_loader_parent_signature(self):
        fitting = object(); parent = SimpleNamespace(validate_result=lambda p: None, summarize=lambda refs, f: {"fixture": 5} if f is fitting else None)
        audit = SimpleNamespace(sha=lambda path: b.PARENT_SHA, read_json=Audit.read_json)
        with tempfile.TemporaryDirectory() as d, patch.object(b, "context", return_value=(parent, None, fitting, None, None, audit)):
            root = Path(d)
            for name, value in (("summary.json", dict(validation_summary={"fixture": 5})), ("split-dataset.json", self.parts), ("measurements.json", self.refs)):
                (root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"), (self.parts, self.refs))
            wrong = copy.deepcopy(self.refs); wrong[0]["arm"] = "precore_read"
            (root/"measurements.json").write_bytes(b.blob(wrong))
            with self.assertRaises(ValueError): b.load_inputs(root/"summary.json")

    def test_22_result_count_and_claim_guard(self):
        summary = b.analyze(self.parts, self.entries, self.refs)[2]
        for key, value in (("new_training_steps", 1), ("model_forward_calls", 119), ("capability_pass_claim", True)):
            p = payload(dict(summary, **{key: value}))
            with self.assertRaises(ValueError): b.validate_result(p)
        p = payload(summary); p["source_blobs"].pop(b.OWN[0])
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_23_own_and_historical_suite_identity(self):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(), b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}), 24)
        class Case(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def id(self): return self.name
        source = unittest.TestSuite([Case(b.EXCLUDED)] + [Case(f"fixture{i}") for i in range(3241)])
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(), b.manifest()["focused_tests"])

    def test_24_runner_cli_and_no_training_calls(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root/"tools/run_c253.ps1").read_text(encoding="utf-8"); launcher = (root/"tools/invoke_c253.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S); self.assertEqual(len(blocks), 3)
        for block in blocks: compile(block, "embedded", "exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant)
                    and isinstance(n.value, ast.Attribute) and isinstance(n.value.value, ast.Name) and n.value.value.id == "sys" and n.value.attr == "argv"}
        self.assertEqual(argv(blocks[0]), {1}); self.assertEqual(argv(blocks[2]), {1, 2, 3})
        self.assertLess(launcher.index("::ParseFile"), launcher.index("$failure = $null"))
        self.assertIn("c252-v5b-precore-query-ea8199d8ca794acba051ca5f65a391b3", launcher)
        source = (root/"fold_lm/v05_benchmarks/model_c253_frozen_residual_path.py").read_text()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                self.assertNotIn(name, {"backward", "step", "AdamW", "fit", "train_one"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
