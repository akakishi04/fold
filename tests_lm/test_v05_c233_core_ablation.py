import hashlib
import inspect
import io
import json
import math
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c233_core_ablation as b


class SourceFixture(nn.Module):
    """Real GRU layers with a dummy extra parameter; synthetic parent interface only."""
    def __init__(self, seed=0):
        super().__init__()
        torch.manual_seed(seed)
        self.config = SimpleNamespace(width=16, max_tokens=48)
        self.byte_embedding = nn.Embedding(259, 16, padding_idx=256)
        self.local_encoder = nn.GRU(16, 16, batch_first=True)
        self.readout_norm = nn.LayerNorm(16)
        self.decoder = nn.Linear(16, 256)
        self.core = nn.Parameter(torch.zeros(3328))
        self.double().eval()


def fingerprint(model):
    h = hashlib.sha256()
    for name, value in sorted(model.state_dict().items()):
        h.update(name.encode()); h.update(value.detach().cpu().numpy().tobytes())
    return h.hexdigest()


def inputs():
    x = torch.tensor([[257, 65, 258] + [256]*45, [257, 66, 258] + [256]*45])
    return x, torch.tensor([65, 66])


def scores(bpb):
    return {name: dict(bytes=n, nll_sum=bpb*n*math.log(2), bits_per_byte=bpb)
            for name, n in (("all", 316), ("en", 164), ("ja", 152))}


def record(seed, full=1.0, baseline=2.0):
    return dict(seed=seed, weights_changed=True, checkpoint_roundtrip=True,
        generation_replayed=True, reload_max_error=0.0, full_replay_error=0.0,
        initial_train=scores(8.0), final_train=scores(2.0), initial_eval=scores(8.0),
        final_eval=scores(baseline), unigram_eval=scores(5.0), full_eval=scores(full),
        fit=dict(steps=400, byte_presentations=12800))


def payload(summary):
    pins = {name: "fixture" for name in b.OWN}
    pins.update({f"parent/{i}": "fixture" for i in range(238)})
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256={str(i): "fixture" for i in range(346)},
        artifacts=[dict(file=name) for name in b.OUTPUTS], validation_summary=summary,
        status="PASS" if b.gate(summary) else "FAIL", gate_f_candidate=False, network_calls=0)


class C233Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)

    def test_01_manifest_identity(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)

    def test_02_actual_backbone_parameter_count(self):
        model = b.new_baseline(SourceFixture())
        self.assertEqual(sum(p.numel() for p in model.parameters()), 10160)
        self.assertEqual(sum(p.numel() for p in SourceFixture().parameters()), 13488)

    def test_03_common_initial_weights_match_exactly(self):
        source = SourceFixture(32); model = b.new_baseline(source)
        self.assertEqual(set(model.state_dict()), set(b.common_state(source)))
        for name, value in model.state_dict().items():
            self.assertTrue(torch.equal(value, b.common_state(source)[name]))

    def test_04_copied_parameters_do_not_alias(self):
        source = SourceFixture(); model = b.new_baseline(source)
        before = fingerprint(source)
        with torch.no_grad(): model.decoder.bias.add_(1)
        self.assertEqual(fingerprint(source), before)
        self.assertNotEqual(model.decoder.bias.data_ptr(), source.decoder.bias.data_ptr())

    def test_05_no_core_parameters_remain(self):
        model = b.new_baseline(SourceFixture())
        self.assertFalse(hasattr(model, "core"))
        self.assertTrue(all(name.split('.')[0] in b.SHARED for name in model.state_dict()))

    def test_06_configuration_mismatch_rejected(self):
        source = SourceFixture(); source.config.width = 8
        with self.assertRaises(ValueError): b.new_baseline(source)

    def test_07_forward_matches_direct_gru_eos_readout(self):
        source = SourceFixture(); model = b.new_baseline(source); x, _ = inputs()
        with torch.no_grad():
            context, _ = source.local_encoder(source.byte_embedding(x))
            expected = source.decoder(source.readout_norm(context[:, 2]))
            actual = model(x, torch.zeros(2, dtype=torch.int64))
        torch.testing.assert_close(actual, expected, rtol=0, atol=0)

    def test_08_forward_rejects_shape_and_dtype(self):
        model = b.new_baseline(SourceFixture()); x, _ = inputs()
        for wrong in (x[:, :3], x.float()):
            with self.assertRaises(ValueError): model(wrong, torch.zeros(2, dtype=torch.int64))

    def test_09_only_next_task_allowed(self):
        model = b.new_baseline(SourceFixture()); x, _ = inputs()
        with self.assertRaises(ValueError): model(x, torch.ones(2, dtype=torch.int64))

    def test_10_invalid_token_ids_rejected(self):
        model = b.new_baseline(SourceFixture())
        for value in (-1, 259):
            x, _ = inputs(); x[0, 1] = value
            with self.assertRaises(ValueError): model(x, torch.zeros(2, dtype=torch.int64))

    def test_11_own_checkpoint_roundtrip(self):
        model = b.new_baseline(SourceFixture()); buffer = io.BytesIO()
        torch.save(model.state_dict(), buffer); buffer.seek(0)
        restored = b.new_baseline(SourceFixture(1))
        restored.load_state_dict(torch.load(buffer, weights_only=True), strict=True)
        self.assertEqual(fingerprint(model), fingerprint(restored))

    def test_12_initial_copy_precedes_trained_full_load(self):
        source = inspect.getsource(b.run)
        self.assertLess(source.index("model = new_baseline(initial)"), source.index("replay_full(initial"))
        self.assertNotIn("replay_full", inspect.getsource(b.new_baseline))

    def test_13_fit_inputs_are_train_only(self):
        self.assertEqual(tuple(inspect.signature(b.fit_baseline).parameters),
                         ("model", "train_tokens", "train_targets", "seed", "steps"))
        self.assertNotIn("final_eval", inspect.getsource(b.fit_baseline))

    def test_14_two_real_optimizer_steps_change_weights(self):
        model = b.new_baseline(SourceFixture()); before = fingerprint(model); x, y = inputs()
        fitted = b.fit_baseline(model, x, y, 232001, steps=2)
        self.assertNotEqual(fingerprint(model), before)
        self.assertEqual((fitted["steps"], fitted["byte_presentations"]), (2, 64))

    def test_15_short_training_is_reproducible(self):
        a = b.new_baseline(SourceFixture(3)); z = b.new_baseline(SourceFixture(3)); x, y = inputs()
        b.fit_baseline(a, x, y, 232001, steps=2); b.fit_baseline(z, x, y, 232001, steps=2)
        self.assertEqual(fingerprint(a), fingerprint(z))

    def test_16_sampler_uses_registered_order(self):
        x, y = inputs(); model = b.new_baseline(SourceFixture()); original = torch.randint; seen = []
        def capture(*args, **kwargs):
            result = original(*args, **kwargs); seen.append(result.clone()); return result
        with patch.object(torch, "randint", side_effect=capture):
            b.fit_baseline(model, x, y, 232001, steps=2)
        generator = torch.Generator().manual_seed(233001)
        for actual in seen:
            self.assertTrue(torch.equal(actual, original(2, (32,), generator=generator)))
        self.assertEqual(len(seen), 2)

    def test_17_score_adapter_reproduces_metric(self):
        self.assertEqual(b.score_error(scores(3.0), scores(3.0)), 0)

    def test_18_score_adapter_rejects_bad_count_and_units(self):
        expected = scores(3.0); expected["en"]["bytes"] = 1
        with self.assertRaises(ValueError): b.score_error(scores(3.0), expected)
        expected = scores(3.0); expected["ja"]["bits_per_byte"] += 1
        with self.assertRaises(ValueError): b.score_error(scores(3.0), expected)

    def test_19_score_adapter_rejects_nonfinite(self):
        expected = scores(3.0); expected["all"]["nll_sum"] = float("nan")
        with self.assertRaises(ValueError): b.score_error(scores(3.0), expected)

    def test_20_parent_checkpoint_schema_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"parent.pt"
            torch.save(dict(schema="fold-c232-trained-byte-models-v1", seeds=list(b.SEEDS), states=[{}, {}, {}]), path)
            self.assertEqual(len(b.load_parent_states(path)), 3)
            torch.save(dict(schema="wrong", seeds=list(b.SEEDS), states=[{}, {}, {}]), path)
            with self.assertRaises(ValueError): b.load_parent_states(path)

    def test_21_parent_record_adapter_checks_order(self):
        rows = [dict(parameters=13488, seed=s, fit=dict(steps=400, byte_presentations=12800),
                     initial_sha256="a"*64, final_sha256="b"*64, final_eval=scores(1.0)) for s in b.SEEDS]
        parent = SimpleNamespace(learning_pass=lambda row: True,
            audit_module=lambda: SimpleNamespace(read_json=lambda path: rows))
        with patch.object(b, "parent_module", return_value=parent):
            self.assertEqual(b.read_parent_measurements("unused"), rows)
            rows.reverse()
            with self.assertRaises(ValueError): b.read_parent_measurements("unused")

    def test_22_six_full_win_cells_pass(self):
        summary = b.summary_for([record(s) for s in b.SEEDS])
        self.assertEqual((summary["full_win_cells"], summary["baseline_win_cells"]), (6, 0))
        self.assertTrue(b.gate(summary))

    def test_23_competitive_smaller_baseline_is_valid_negative(self):
        summary = b.summary_for([record(s, full=2.0, baseline=1.0) for s in b.SEEDS])
        self.assertTrue(summary["baseline_qualified"]); self.assertFalse(b.gate(summary))
        self.assertEqual(summary["baseline_win_cells"], 6)
        b.validate_result(payload(summary))

    def test_24_tie_is_not_full_advantage(self):
        summary = b.summary_for([record(s, full=1.0, baseline=1.0) for s in b.SEEDS])
        self.assertEqual(summary["tied_cells"], 6); self.assertFalse(b.gate(summary))

    def test_25_unqualified_baseline_does_not_favor_full(self):
        summary = b.summary_for([record(s, full=1.0, baseline=6.0) for s in b.SEEDS])
        self.assertFalse(summary["baseline_qualified"]); self.assertFalse(b.gate(summary))
        b.validate_result(payload(summary))

    def test_26_failed_replay_is_invalid_not_scientific_negative(self):
        rows = [record(s) for s in b.SEEDS]; rows[0]["reload_max_error"] = 1.0
        with self.assertRaises(ValueError): b.validate_result(payload(b.summary_for(rows)))

    def test_27_runner_and_launcher_contracts(self):
        root = Path(__file__).resolve().parents[1]
        run = (root/"tools/run_c233.ps1").read_text(encoding="utf-8")
        launch = (root/"tools/invoke_c233.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2753", run)
        self.assertLess(run.index("authoring_selftest = PASS"), run.index("& $Python -u -c $Regression"))
        blocks = re.findall(r"@'\n(.*?)\n'@", run, re.S); self.assertEqual(len(blocks), 3)
        for block in blocks: compile(block, "runner-block", "exec")
        self.assertIn("c232-v5b-bilingual-learning-67b366b0db07449185a18bd0bbe7b996", launch)
        self.assertIn("RUNNER_PARSE_ERROR", launch)
        self.assertLess(launch.index("::ParseFile"), launch.index("$failure = $null"))

    def test_28_no_extra_hypothesis_or_training_budget(self):
        m = b.manifest()
        self.assertFalse(m["parameter_matched"]); self.assertFalse(m["general_language_claim"])
        self.assertEqual((m["steps_per_seed"], m["total_new_training_steps"], m["full_retraining_steps"]), (400, 1200, 0))
        self.assertIn("read_parent_measurements", inspect.getsource(b.run))
        self.assertIn("load_parent_states", inspect.getsource(b.run))

    def test_29_import_aliases_and_direct_source_guards(self):
        source = inspect.getsource(b)
        self.assertFalse(re.findall(r"\bc\d{3}\.", source))
        self.assertIn("deps <= set(pins)", inspect.getsource(b.precheck))
        self.assertIn("parent.parent_module().LM_SOURCES", inspect.getsource(b.precheck))

    def test_30_synthetic_full_run_uses_initial_copy_and_preserves_negative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); parent_dir = root/"parent"; parent_dir.mkdir()
            data = [dict(id="fixture", text="abcdefghij")]
            (parent_dir/"dataset.json").write_text(json.dumps(data), encoding="utf-8")
            rows = []; states = []
            for seed in b.SEEDS:
                model = SourceFixture(seed); before = fingerprint(model)
                with torch.no_grad(): model.decoder.bias.add_(0.02)
                states.append(model.state_dict())
                rows.append(dict(seed=seed, parameters=13488, initial_sha256=before,
                    final_sha256=fingerprint(model), fit=dict(steps=400, byte_presentations=12800),
                    final_eval=scores(4.0), unigram_eval=scores(5.0),
                    generation=[dict(id="fixture", generated_hex=b"test".hex())]))
            (parent_dir/"measurements.json").write_text(json.dumps(rows), encoding="utf-8")
            torch.save(dict(schema="fold-c232-trained-byte-models-v1", seeds=list(b.SEEDS), states=states), parent_dir/"trained-models.pt")
            audit = SimpleNamespace(read_json=lambda path: json.loads(Path(path).read_text(encoding="utf-8")),
                sha=lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                git=lambda root, *args: b"HEAD" if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b"")
            factory = SimpleNamespace(new_model=SourceFixture, fingerprint=fingerprint, generate=lambda *args: b"test")
            x, y = inputs()
            parent = SimpleNamespace(parent_module=lambda: factory, audit_module=lambda: audit,
                learning_pass=lambda row: True, validate_dataset=lambda value: (value, value),
                tensor_rows=lambda value: (x, y, None), unigram_tables=lambda value: None,
                reference_score=lambda *args: scores(5.0), evaluate=lambda *args: (scores(4.0), torch.zeros((2, 256))))
            paths = {}
            for i in range(346):
                path = root/f"input{i}"; path.write_bytes(b"x"); paths[str(path)] = audit.sha(path)
            pins = payload(b.summary_for([record(s) for s in b.SEEDS]))["source_blobs"]
            fitted = []
            def simulate_fit(model, tokens, targets, seed):
                self.assertEqual(fingerprint(model), fingerprint(b.new_baseline(SourceFixture(seed))))
                fitted.append(seed)
                with torch.no_grad(): model.decoder.bias.add_(0.1)
                return dict(steps=400, byte_presentations=12800, synthetic_training=True)
            with patch.object(b, "parent_module", return_value=parent), patch.object(b, "precheck", return_value=({}, pins, paths)), patch.object(b, "fit_baseline", side_effect=simulate_fit), patch("sys.stdout", new=io.StringIO()):
                result = b.run(c232_summary=parent_dir/"summary.json", output_dir=root/"out", expected_head="HEAD")
            self.assertEqual(fitted, list(b.SEEDS)); self.assertEqual(result["status"], "FAIL")
            self.assertTrue(result["validation_summary"]["all_replays"])
            self.assertEqual(len(result["artifacts"]), 5)

    def test_31_actual_parent_train_only_smoke(self):
        parent = b.parent_module(); factory = parent.parent_module()
        source = factory.new_model(b.SEEDS[0]); model = b.new_baseline(source)
        before = factory.fingerprint(model)
        train, _ = parent.validate_dataset(parent.dataset()); x, y, _ = parent.tensor_rows(train[:2])
        b.fit_baseline(model, x, y, b.SEEDS[0], steps=2)
        self.assertNotEqual(factory.fingerprint(model), before)
        self.assertEqual(sum(p.numel() for p in model.parameters()), 10160)
        self.assertTrue(all(bool(torch.isfinite(p).all()) for p in model.parameters()))

    def test_32_actual_historical_suite_counts(self):
        root = Path(__file__).resolve().parents[1]; names = b.regression_modules(root)
        loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names), loaded.countTestCases()), (118, 2754))
        self.assertEqual(b.regression_suite(root).countTestCases(), 2753)


if __name__ == "__main__":
    unittest.main(verbosity=2)
