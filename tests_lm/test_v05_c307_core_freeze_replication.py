"""C307 software controls; synthetic target-coded inputs are not capability evidence."""
import ast
from collections import Counter
import contextlib
import copy
from dataclasses import dataclass, replace
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
from fold_lm.v05_benchmarks import model_c307_core_freeze_replication as b


def definitions(path, names, space):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    selected = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    if {n.name for n in selected} != set(names):
        raise AssertionError("missing accepted definition")
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), "exec"), space)
    return space


def reference_parent():
    root = Path(__file__).resolve().parents[1]
    # Isolated test namespace only; do not modify the imported accepted parent module.
    ns = dict(torch=torch, F=F, copy=copy, require=b.require, ARMS=b.ARMS, STEPS=b.STEPS,
              SLOTS=b.SLOTS, FIT_RNG=b.FIT_RNG, SEEDS=b.SEEDS, ORDERS=b.ORDERS, manifest=b.manifest)
    definitions(root / b.PARENT_SOURCE, ("configure", "schedule", "first_batch_probe", "fit"), ns)
    return NS(**{name: ns[name] for name in ("configure", "schedule", "first_batch_probe", "fit")})


def reference_wide():
    root = Path(__file__).resolve().parents[1]
    ns = dict(torch=torch, nn=torch.nn, copy=copy, Counter=Counter, replace=replace,
              require=b.require, SLOTS=64, digest=b.digest)
    definitions(root / b.WIDE_SOURCE, ("span_mask", "LengthReadout", "schedule_stats"), ns)
    return NS(**{k: ns[k] for k in ("span_mask", "LengthReadout", "schedule_stats")})


def dataset():
    data = {"TRAIN": [], "HOLDOUT": []}
    for entities, values, language in itertools.product(((0, 1), (0, 2), (1, 2)), itertools.permutations(range(4), 2), ("en", "ja")):
        split = "HOLDOUT" if (values[1] - values[0]) % 4 == 2 else "TRAIN"
        for order, query in itertools.product((entities, entities[::-1]), entities):
            data[split].append(dict(id=str((entities, values, language, order, query)), entities=list(entities), values=list(values),
                permutation=list(order), query=query, language=language, target=48+values[entities.index(query)]))
    return data


def pairs_from_rows(rows):
    groups = {}
    for i, r in enumerate(rows):
        key = (r["language"], tuple(r["entities"]), tuple(r["values"]), tuple(r["permutation"]))
        groups.setdefault(key, []).append(i)
    return torch.tensor([sorted(groups[k], key=lambda i: rows[i]["query"]) for k in sorted(groups)], dtype=torch.int64)


def tables(data):
    targets = torch.tensor([r["target"] for r in data["TRAIN"]], dtype=torch.int64)
    tokens = torch.zeros((3, 3, 192, 64), dtype=torch.int64)
    tokens[:, :, :, 0] = targets - 48
    return tokens, targets


class ToyCore(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(4, 4, dtype=torch.float64)
        self.unused = torch.nn.Parameter(torch.zeros(3308, dtype=torch.float64))
    def forward(self, x):
        return torch.tanh(self.linear(x))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = torch.nn.Module()
        self.backbone.local_encoder = torch.nn.Embedding(4, 4, dtype=torch.float64)
        self.backbone.core = ToyCore()
        self.backbone.unused = torch.nn.Parameter(torch.zeros(9632, dtype=torch.float64))
        self.read = torch.nn.Linear(4, 256, dtype=torch.float64)
        self.calls = self.rows = 0
    def forward(self, tokens, tasks):
        assert tokens.shape == (len(tokens), 64) and tasks.shape == (len(tokens),) and not bool(tasks.any())
        self.calls += 1
        self.rows += len(tokens)
        return self.read(self.backbone.core(self.backbone.local_encoder(tokens[:, 0])))


def fingerprint(model):
    return b.digest({k: v.detach().tolist() for k, v in model.state_dict().items()})


@dataclass
class Config:
    width: int = 16
    max_tokens: int = 48
    slots: int = 48
    next_route: int = 0
    instruction_route: int = 1
    internal_steps: int = 2


class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = torch.nn.Embedding(259, 16, dtype=torch.float64)
    def forward(self, tokens):
        return (self.embed(tokens),)


class Core(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.linear = torch.nn.Linear(16, 16, dtype=torch.float64)
        self.unused = torch.nn.Parameter(torch.zeros(3328-272, dtype=torch.float64))
    def forward(self, state, local, route_index):
        return torch.tanh(self.linear(state) + .1*local)


class Backbone(torch.nn.Module):
    def __init__(self, seed):
        super().__init__()
        torch.manual_seed(seed)
        self.config = Config()
        self.local_encoder = Encoder()
        self.core = Core()
        self.readout_norm = torch.nn.LayerNorm(16, dtype=torch.float64)
        self.output = torch.nn.Linear(16, 256, dtype=torch.float64)
        self.unused = torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()), dtype=torch.float64))
    def forward(self, tokens, tasks):
        valid = tokens != 256
        local = self.local_encoder(tokens)[0] * valid[:, :, None]
        state = local
        for _ in range(2):
            next_state = self.core(state, local, route_index=0)
            self.core(state, local, route_index=1)
            state = next_state
        post = state[torch.arange(len(tokens)), valid.sum(1)-1]
        return self.output(self.readout_norm(post))


class Reference(torch.nn.Module):
    def __init__(self, backbone, seed, *unused):
        super().__init__()
        self.backbone = backbone
        self.read = torch.nn.Module()
        torch.manual_seed(seed+1)
        for n in ("query", "key", "output"):
            setattr(self.read, n, torch.nn.Linear(16, 16, bias=False, dtype=torch.float64))


def factory():
    return NS(c278=NS(MeanFinalDualReadout=Reference), factory=NS(new_model=Backbone), reader=None,
              c269=NS(query_span_mask=None), base=NS(fingerprint=fingerprint))


def policy_parent():
    return NS(manifest=b.manifest, STEPS=1200, SLOTS=64, FIT_RNG=612000,
              SEEDS=tuple(range(306001, 306006)), ORDERS=tuple(range(306101, 306106)))


def records_fixture(data, wide, pairs):
    records = []
    for seed, arm in b.identities():
        events = b.schedule(seed, data["TRAIN"], pairs)
        raw = {str(n): dict(passed=True, totals=[dict(split=s, rows=size, correct=size, direct_pass=True, full_pass=True, final_normal_nll=.1)
                for s, size in (("TRAIN", 576), ("HOLDOUT", 288))]) for n in b.LENGTHS}
        fit = dict(steps=1200, training_rows=57600, optimizer_creations=1, fit_rng=612000,
            trainable_parameters=b.manifest()["trainable_parameters"][arm], ce_history=[.1]*1200,
            gradient_union={"read.weight": 1280}, gradient_parameter_counts=[1280]*1200,
            schedule_events=events, **wide.schedule_stats(events))
        records.append(dict(seed=seed, arm=arm, parameters=14256, slots=64, initial_sha256="a"*64, final_sha256="b"*64,
            core_initial_sha256="c"*64, core_final_sha256=("c" if arm == b.ARMS[1] else "d")*64, fit=fit, raw=raw,
            forward_calls=1308, row_presentations=67968, core_forward_calls=5232,
            checkpoint_roundtrip=True, reload_max_error=0., replay_forward_calls=108, replay_row_presentations=10368, replay_core_forward_calls=432))
    return records


def diagnostic():
    return NS(normalize_task=lambda scored, *args: scored["totals"], partition=lambda rows: {k: v for k, v in rows[0].items() if k != "split"})


def protection():
    pins = {n: "b"*40 for n in b.OWN}
    pins[b.PARENT_SOURCE], pins[b.WIDE_SOURCE] = b.PARENT_BLOB, b.WIDE_BLOB
    while len(pins) < 688:
        pins["fixture/"+str(len(pins))] = "b"*40
    return pins, {"fixture/input/"+str(i): "a"*64 for i in range(1281)}


class Audit:
    @staticmethod
    def sha(path):
        p = Path(path)
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, name):
        return Path(root)/name
    @staticmethod
    def git(root, *args):
        if args[0] == "rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0] == "branch": return b"feat/sft-target-loss\n"
        return b""


def payload(summary):
    pins, inputs = protection()
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, commit_sha="f"*40,
        status="PASS" if summary["candidate_gate"] else "FAIL", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=inputs, artifacts=[dict(file=n) for n in b.OUTPUTS],
        validation_summary=summary, gate_f_candidate=False, production_adoption=False)


class C307Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads()
        cls.det = torch.are_deterministic_algorithms_enabled()
        torch.set_num_threads(2)
        cls.parent, cls.wide = reference_parent(), reference_wide()
        cls.pairs = NS(pairs_from_rows=pairs_from_rows)
        cls.wide.score_length = lambda data, raw, c: raw
        cls.data = dataset()
        cls.tokens, cls.targets = tables(cls.data)
        torch.manual_seed(71)
        cls.initial = Toy()
        cls.models, cls.fits = {}, {}
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:
                model = cls.parent.configure(copy.deepcopy(cls.initial), arm)
                cls.fits[arm] = b.fit(model, cls.data, cls.tokens, cls.targets, b.SEEDS[0], arm, cls.pairs, cls.wide)
                cls.models[arm] = model
        cls.records = records_fixture(cls.data, cls.wide, cls.pairs)
        cls.metrics, cls.summary = b.analyze(cls.records, cls.data, cls.pairs, cls.wide, diagnostic(), None)
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads)
        torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self):
        b.validate_seal()
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for value in ("UNSEALED", "0"*64, "A"*64):
            with patch.object(b, "MANIFEST_SHA", value), self.assertRaises(ValueError): b.validate_seal()

    def test_03_unchanged_policy_new_seeds(self):
        parent = policy_parent()
        b.verify_parent_policy(parent)
        parent.manifest = lambda: {**b.manifest(), "lr": .01}
        with self.assertRaisesRegex(ValueError, "policy drift"): b.verify_parent_policy(parent)
        parent = policy_parent(); parent.SEEDS = b.SEEDS
        with self.assertRaisesRegex(ValueError, "new cohort"): b.verify_parent_policy(parent)

    def test_04_all_schedules_match_accepted_algorithm(self):
        for seed in b.SEEDS:
            current = b.schedule(seed, self.data["TRAIN"], self.pairs)
            original = self.parent.schedule(seed, self.data["TRAIN"], self.pairs)
            self.assertTrue(torch.equal(current, original))
            stats = self.wide.schedule_stats(current)
            self.assertEqual(stats["per_length_row_exposures"], [[100]*192 for _ in range(3)])
            self.assertEqual([sum(r[i] for r in stats["length_profile_updates"]) for i in range(3)], [400]*3)
        self.assertFalse(torch.equal(b.schedule(b.SEEDS[0], self.data["TRAIN"], self.pairs), b.schedule(b.SEEDS[1], self.data["TRAIN"], self.pairs)))

    def test_05_pair_rejection_private_rng(self):
        bad = copy.deepcopy(self.data["TRAIN"]); bad[1]["query"] = bad[0]["query"]
        with self.assertRaises(ValueError): b.schedule(b.SEEDS[0], bad, self.pairs)
        torch.manual_seed(1); state = torch.random.get_rng_state().clone()
        b.schedule(b.SEEDS[0], self.data["TRAIN"], self.pairs)
        self.assertTrue(torch.equal(state, torch.random.get_rng_state()))
        with self.assertRaises(ValueError): b.schedule(306001, self.data["TRAIN"], self.pairs)

    def test_06_actual_wide_factory_storage(self):
        models = b.make_models(b.SEEDS[0], self.parent, self.wide, factory())
        self.assertEqual(fingerprint(models[b.ARMS[0]]), fingerprint(models[b.ARMS[1]]))
        ptrs = [p.data_ptr() for m in models.values() for p in m.parameters()]
        self.assertEqual(len(ptrs), len(set(ptrs)))
        self.assertEqual([sum(p.numel() for p in m.parameters() if p.requires_grad) for m in models.values()], [14256, 10928])
        self.assertTrue(all(m.backbone.config.max_tokens == 64 and m.backbone.core.config.slots == 64 for m in models.values()))

    def test_07_actual_lengthreadout_gradient_probe(self):
        models = b.make_models(b.SEEDS[0], self.parent, self.wide, factory())
        x = torch.full_like(self.tokens, 256)
        text = [257, *b"AA=0;BB=1;AA=", 258]
        x[:, :, :, :len(text)] = torch.tensor(text)
        report = self.parent.first_batch_probe(models, x, self.targets, b.schedule(b.SEEDS[0], self.data["TRAIN"], self.pairs))
        self.assertEqual(report["max_logit_error"], 0.)
        self.assertEqual(report["max_noncore_gradient_error"], 0.)
        self.assertEqual(report["frozen_core_gradient_tensors"], 0)
        self.assertTrue(report["encoder_receives_signal"])

    def test_08_fit_equals_accepted_parent_loop(self):
        for arm in b.ARMS:
            model = self.parent.configure(copy.deepcopy(self.initial), arm)
            with contextlib.redirect_stdout(io.StringIO()):
                original = self.parent.fit(model, self.data, self.tokens, self.targets, b.SEEDS[0], arm, self.pairs, self.wide)
            current = self.fits[arm]
            self.assertEqual(original["ce_history"], current["ce_history"])
            self.assertEqual(original["gradient_parameter_counts"], current["gradient_parameter_counts"])
            self.assertEqual(original["gradient_union"], current["gradient_union"])
            self.assertTrue(torch.equal(original["schedule_events"], current["schedule_events"]))
            self.assertEqual(fingerprint(model), fingerprint(self.models[arm]))

    def test_09_core_preservation_and_learning(self):
        initial = fingerprint(self.initial.backbone.core)
        self.assertEqual(initial, fingerprint(self.models[b.ARMS[1]].backbone.core))
        self.assertNotEqual(initial, fingerprint(self.models[b.ARMS[0]].backbone.core))
        for arm in b.ARMS:
            b.check_fit(self.fits[arm], b.SEEDS[0], arm, self.data, self.pairs, self.wide)
            self.assertLess(self.fits[arm]["ce_history"][-1], self.fits[arm]["ce_history"][0])
            self.assertEqual((self.models[arm].calls, self.models[arm].rows), (1200, 57600))

    def test_10_optimizer_excludes_core_and_determinism(self):
        real, made = torch.optim.AdamW, []
        def build(*args, **kwargs):
            optimizer = real(*args, **kwargs); made.append(optimizer); return optimizer
        model = self.parent.configure(copy.deepcopy(self.initial), b.ARMS[1])
        torch.manual_seed(999)
        with patch.object(torch.optim, "AdamW", side_effect=build), contextlib.redirect_stdout(io.StringIO()):
            fitted = b.fit(model, self.data, self.tokens, self.targets, b.SEEDS[0], b.ARMS[1], self.pairs, self.wide)
        self.assertEqual(len(made), 1)
        self.assertEqual({int(state["step"]) for state in made[0].state.values()}, {1200})
        ids = {id(p) for group in made[0].param_groups for p in group["params"]}
        self.assertFalse(ids & {id(p) for p in model.backbone.core.parameters()})
        self.assertEqual(fitted["ce_history"], self.fits[b.ARMS[1]]["ce_history"])

    def test_11_bad_training_inputs(self):
        y = self.targets.clone(); y[0] = 99
        with self.assertRaises(ValueError): b.fit(copy.deepcopy(self.initial), self.data, self.tokens, y, b.SEEDS[0], b.ARMS[0], self.pairs, self.wide)
        with self.assertRaises(ValueError): b.fit(copy.deepcopy(self.initial), self.data, self.tokens, self.targets, b.SEEDS[0], b.ARMS[1], self.pairs, self.wide)

    def test_12_fit_metadata_tamper(self):
        for mutate in (lambda f: f.update(fit_rng=1), lambda f: f["ce_history"].pop(), lambda f: f["gradient_union"].update({"backbone.core.x": 1})):
            f = copy.deepcopy(self.fits[b.ARMS[1]]); mutate(f)
            with self.assertRaises(ValueError): b.check_fit(f, b.SEEDS[0], b.ARMS[1], self.data, self.pairs, self.wide)

    def test_13_actual_train_one_calls(self):
        model = self.parent.configure(copy.deepcopy(self.initial), b.ARMS[1])
        @contextlib.contextmanager
        def counted(m, core):
            calls, cores = [0, 0], [0]
            yield calls, cores
            calls[:] = [m.calls, m.rows]; cores[0] = m.calls*4  # Accounting stand-in,not measured FOLD core internals.
        def evaluate(m, prompts, data, c):
            self.assertFalse(m.training); self.assertFalse(any(p.requires_grad for p in m.parameters()))
            with torch.no_grad():
                for _ in range(108): m(torch.zeros((96, 64), dtype=torch.int64), torch.zeros(96, dtype=torch.int64))
            return {}
        c = NS(base=NS(fingerprint=fingerprint), p267=NS(counted=counted), core=None)
        with contextlib.redirect_stdout(io.StringIO()):
            record, state = b.train_one(model, self.data, {}, self.tokens, self.targets, b.SEEDS[0], b.ARMS[1], self.pairs, NS(schedule_stats=self.wide.schedule_stats, evaluate=evaluate), c)
        self.assertEqual((record["forward_calls"], record["row_presentations"], record["core_forward_calls"]), (1308, 67968, 5232))
        self.assertEqual(list(state), list(model.state_dict()))

    def test_14_inventory(self):
        self.assertEqual((len(self.metrics), len(self.summary["final_partitions"]), len(self.summary["contrasts"])), (10, 80, 40))
        b.validate_result(payload(self.summary))

    def test_15_one_new_failure_keeps_negative(self):
        records = copy.deepcopy(self.records); records[1]["raw"]["5"]["passed"] = False
        _, summary = b.analyze(records, self.data, self.pairs, self.wide, diagnostic(), None)
        self.assertFalse(summary["candidate_gate"])
        self.assertEqual(summary["paired_five"], dict(both_pass=4, full_only=1, frozen_only=0, both_fail=0))
        p = payload(summary); self.assertEqual(p["status"], "FAIL"); b.validate_result(p)

    def test_16_paired_contingency(self):
        results = copy.deepcopy(self.summary["seed_results"])
        for i, (a, c) in enumerate(((True, True), (True, False), (False, True), (False, False), (False, True))):
            results[2*i]["quint_pass"], results[2*i+1]["quint_pass"] = a, c
        self.assertEqual(b.paired_outcomes(results), dict(both_pass=1, full_only=1, frozen_only=2, both_fail=1))
        with self.assertRaises(ValueError): b.paired_outcomes(results[:-1])

    def test_17_state_replay_and_pair_guards(self):
        for field, value in (("core_final_sha256", "z"*64), ("reload_max_error", .01), ("initial_sha256", "z"*64), ("replay_forward_calls", 107)):
            records = copy.deepcopy(self.records); records[1][field] = value
            with self.assertRaises(ValueError): b.analyze(records, self.data, self.pairs, self.wide, diagnostic(), None)

    def test_18_exact_parent_flags(self):
        flags = b.expected_parent_flags()
        self.assertEqual([sum(r["length_pass"][str(n)] for r in flags if r["arm"] == b.ARMS[0]) for n in b.LENGTHS], [4, 3, 3, 3])
        self.assertEqual([sum(r["length_pass"][str(n)] for r in flags if r["arm"] == b.ARMS[1]) for n in b.LENGTHS], [5, 5, 5, 4])
        self.assertEqual([r["seed"] for r in flags if r["arm"] == b.ARMS[1] and not r["quint_pass"]], [306003])

    @contextlib.contextmanager
    def loader_fixture(self):
        paths = [(Path("/c307-fixture")/str(i)/"summary.json").resolve() for i in range(33)]
        parent = policy_parent(); parent.PARENT_SHA = "b"*64
        audit = NS(PARENT_SHA="c"*64, no_neural=contextlib.nullcontext)
        prompts = {"fixture": "sealed prompts"}
        wide = NS(parent_hashes=lambda p: tuple(str(i % 10)*64 for i in range(30)), context=lambda: (None,),
                  prompt_dataset=lambda d: prompts, validate_prompts=Mock())
        p = dict(experiment_id="C306-v5b-broad-length-core-freeze", commit_sha=b.PARENT_EXECUTION, status="FAIL",
            source_blobs={b.PARENT_SOURCE: b.PARENT_BLOB}, artifacts=[dict(file=n) for n in b.OUTPUTS],
            validation_summary=dict(seed_results=b.expected_parent_flags(), candidate_gate=False, all_pairs_matched=True, all_replays=True))
        parent.verify_artifacts = Mock(return_value=(p, [])); parent.validate_result = Mock()
        mapping = dict(zip(map(str, paths), (b.PARENT_SHA, parent.PARENT_SHA, audit.PARENT_SHA, *wide.parent_hashes(None)), strict=True))
        c = NS(audit=NS(sha=lambda path: mapping[str(path)], read_json=lambda path: self.data if path.name == "dataset.json" else prompts))
        with patch.object(b, "context", return_value=(parent, audit, wide, None, None, None, c)), patch.object(b, "DATA_SHA", b.digest(self.data)), patch.object(b, "PROMPTS_SHA", b.digest(prompts)):
            yield paths, mapping, parent, p

    def test_19_33_hashes_before_actual_dispatch(self):
        with self.loader_fixture() as (paths, mapping, parent, p):
            self.assertEqual(b.load_parent(paths)[0], p)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent, paths[1:], b.PARENT_EXECUTION)
            for path in paths:
                old = mapping[str(path)]; mapping[str(path)] = "f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)] = old

    def test_20_parent_outcome_and_data_contract(self):
        for mutate in (lambda p: p.update(status="PASS"), lambda p: p["artifacts"].pop(), lambda p: p["validation_summary"]["seed_results"].pop()):
            with self.loader_fixture() as (paths, _, _, p):
                mutate(p)
                with self.assertRaises(ValueError): b.load_parent(paths)
        with self.loader_fixture() as (paths, _, _, _), patch.object(b, "DATA_SHA", "0"*64), self.assertRaisesRegex(ValueError, "data hashes"):
            b.load_parent(paths)

    def test_21_protection_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); pins = {b.PARENT_SOURCE: b.PARENT_BLOB, b.WIDE_SOURCE: b.WIDE_BLOB}
            while len(pins) < 682: pins["accepted/"+str(len(pins))] = "b"*40
            for name in list(pins)+list(b.OWN):
                p = root/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(name, encoding="utf-8")
            protected = {str((root/n).resolve()): Audit.sha(root/n) for n in pins}
            for i in range(1267-len(protected)):
                p = root/f"input{i}"; p.write_text("input", encoding="utf-8"); protected[str(p.resolve())] = Audit.sha(p)
            folder = root/"parent"; folder.mkdir(); sp = folder/"summary.json"; sp.write_text("summary", encoding="utf-8")
            mapping, artifacts = {str(sp.resolve()): b.PARENT_SHA}, []
            for n in b.OUTPUTS:
                path = folder/n; path.write_text("artifact", encoding="utf-8"); mapping[str(path.resolve())] = "a"*64; artifacts.append(dict(file=n, sha256="a"*64))
            def sha(path): return mapping.get(str(Path(path).resolve()), Audit.sha(path))
            parent = types.ModuleType("parent"); parent.__file__ = str(root/b.PARENT_SOURCE); parent.context = lambda: ()
            wide = NS(PINNED={b.WIDE_SOURCE: b.WIDE_BLOB}, context=lambda: ())
            c = NS(factory=NS(language_module=lambda: None), audit=NS(sha=sha, git=lambda root, *args: (pins.get(args[1][5:], "c"*40)+"\n").encode(),
                   safe_child=Audit.safe_child, protect_tree_files=lambda root, ps: {str((root/n).resolve()): sha(root/n) for n in ps}))
            p = dict(source_blobs=pins, input_sha256=protected, artifacts=artifacts)
            with patch.object(b, "context", return_value=(parent, None, wide, None, None, None, c)), patch.object(b, "load_parent", return_value=(p, None, None)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len, b.precheck([sp]*33, root))), (688, 1281))
                c.missing = types.ModuleType("missing"); c.missing.__file__ = str(root/"unprotected.py")
                with self.assertRaisesRegex(ValueError, "unprotected helper"): b.precheck([sp]*33, root)

    def test_22_actual_runtime_preflight(self):
        parent = policy_parent(); parent.configure = self.parent.configure; parent.first_batch_probe = self.parent.first_batch_probe
        wide = reference_wide(); c = factory()
        tokens = torch.full_like(self.tokens, 256); text = [257, *b"AA=0;BB=1;AA=", 258]
        tokens[:, :, :, :len(text)] = torch.tensor(text); wide.training_tables = lambda d: (tokens, self.targets)
        with patch.object(b, "context", return_value=(parent, None, wide, self.pairs, None, None, c)), patch.object(b, "precheck", return_value=protection()), patch.object(b, "load_parent", return_value=({}, self.data, {})), contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*33, Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        records = copy.deepcopy(self.records); events = []
        def train(*args):
            events.append("train"); key = (args[5], args[6]); return records[b.identities().index(key)], {}
        def replay(model, state, record, prompts, data, c):
            self.assertEqual(prompts, {"fixture": "prompts"}); self.assertEqual(data, self.data); events.append("replay")
        def precheck(*args): events.append("precheck"); return protection()
        wide = NS(training_tables=lambda data: (self.tokens, self.targets), replay_one=replay,
                  score_length=self.wide.score_length, schedule_stats=self.wide.schedule_stats)
        c = NS(audit=Audit())
        with patch.object(b, "context", return_value=(None, NS(no_neural=contextlib.nullcontext), wide, self.pairs, diagnostic(), None, c)), patch.object(b, "load_parent", return_value=({}, self.data, {"fixture": "prompts"})), patch.object(b, "precheck", side_effect=precheck), patch.object(b, "make_models", return_value=dict.fromkeys(b.ARMS)), patch.object(b, "train_one", side_effect=train):
            yield events

    def test_23_production_run_loader_order_roundtrip(self):
        real = b.load_bundle; reads = []
        def loader(path): reads.append(Path(path).name); return real(path)
        with self.run_fixture() as events, tempfile.TemporaryDirectory() as tmp, patch.object(b, "load_bundle", side_effect=loader), contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp)/"run"; p = b.run(summaries=["x"]*33, output_dir=out, expected_head="f"*40)
            self.assertEqual(events, ["precheck"]+["train"]*10+["replay"]*10+["precheck"])
            self.assertEqual(reads, ["trained-models.pt"])
            self.assertEqual(b.verify_artifacts(out, ["x"]*33, "f"*40)[0], p)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*33, output_dir=out, expected_head="f"*40)

    def test_24_byte_semantic_tamper(self):
        with self.run_fixture(), tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp)/"run"; p = b.run(summaries=["x"]*33, output_dir=out, expected_head="f"*40)
            path = out/"measurements.json"; path.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "output bytes"): b.verify_artifacts(out, ["x"]*33, "f"*40)
            item = next(a for a in p["artifacts"] if a["file"] == path.name)
            item.update(sha256=Audit.sha(path), serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError, "persisted"): b.verify_artifacts(out, ["x"]*33, "f"*40)

    def test_25_bundle_reorder(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"models.pt"; value = dict(schema="fold-c307-replication-models-v1", identities=[list(i) for i in b.identities()], states=[{}]*10)
            torch.save(value, path); self.assertEqual(len(b.load_bundle(path)), 10)
            value["identities"].reverse(); torch.save(value, path)
            with self.assertRaises(ValueError): b.load_bundle(path)

    def test_26_result_scope_and_derived_flags(self):
        for mutate in (lambda p: p.update(gate_f_candidate=True), lambda p: p["validation_summary"].update(train_steps=False), lambda p: p["validation_summary"]["seed_results"][0].update(quint_pass=False)):
            p = payload(copy.deepcopy(self.summary)); mutate(p)
            with self.assertRaises(ValueError): b.validate_result(p)

    def test_27_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def runTest(self): pass
            def id(self): return self.name
        ids = [f"fixture.{i}" for i in range(4845)]+[b.EXCLUDED]
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite = b.regression_suite(Path.cwd())
            self.assertEqual(suite.countTestCases(), 4845); self.assertEqual({t.id() for t in b.flatten(suite)}, set(ids)-{b.EXCLUDED})
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite([Dummy("same"), Dummy("same")])), self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_28_cli_context_guard(self):
        args = ["prog", "--summaries"]+[str(i) for i in range(33)]+["--output-dir", "out", "--expected-head", "f"*40]
        with patch.object(sys, "argv", args), patch.object(b, "run") as run:
            b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]), 33)
        parent = NS(context=lambda: tuple(range(6)), regression_modules=lambda root: [f"m{i}" for i in range(191)])
        package = types.ModuleType("fold_lm.v05_benchmarks"); package.model_c306_broad_length_core_freeze = parent
        with patch.dict(sys.modules, {"fold_lm.v05_benchmarks": package}):
            self.assertEqual(b.context(), (parent, *range(6))); self.assertEqual(len(b.regression_modules(Path.cwd())), 192)
        b.guard(Path.cwd(), "f"*40, NS(audit=Audit()))
        with self.assertRaises(ValueError): b.guard(Path.cwd(), "e"*40, NS(audit=Audit()))

    def test_29_utf8_inventory(self):
        root = Path(__file__).resolve().parents[1]
        with patch.object(io, "text_encoding", side_effect=lambda encoding, stacklevel=2: "cp932" if encoding is None else encoding):
            for name in b.OWN: self.assertTrue((root/name).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA, (root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__), Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "read_text":
                    self.assertTrue(any(k.arg == "encoding" and isinstance(k.value, ast.Constant) and k.value.value == "utf-8" for k in node.keywords))

    def test_30_runner_contract(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root/b.OWN[2]).read_text(encoding="utf-8"); launcher = (root/b.OWN[3]).read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S); self.assertEqual(len(blocks), 3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:35]", blocks[2]); self.assertIn("head = sys.argv[35]", blocks[2])
        self.assertEqual(len(re.findall(r"runs\\c\d{3}-.*?\\summary.json", launcher)), 33)
        self.assertLess(launcher.index("-Mode Validate"), launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"), launcher.index("publish_experiment_log.ps1"))

    def test_31_no_parent_module_mutation(self):
        tree = ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        self.assertNotEqual(target.value.id, "parent")
        self.assertEqual(b.FIT_RNG, 612000); self.assertEqual(b.SHUFFLE_OFFSET, 306000)

    def test_32_imports_and_count(self):
        imports = [n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8")))
                   if isinstance(n, ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports, ["model_c306_broad_length_core_freeze"])
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))), 32)


if __name__ == "__main__":
    unittest.main()
