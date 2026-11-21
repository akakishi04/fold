"""C309 software-control tests; synthetic target-coded fixtures are not capability evidence."""
import ast
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
from fold_lm.v05_benchmarks import model_c309_core_lr_replication as b


def selected(path, names, ns):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    if {n.name for n in nodes} != set(names): raise AssertionError("missing accepted definition")
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), ns)
    return NS(**{name: ns[name] for name in names})


def references():
    root = Path(__file__).resolve().parents[1]
    ns = {k: v for k, v in vars(b).items() if not k.startswith("__")}
    names = ("manifest", "configure", "parameter_groups", "optimizer_for", "verify_optimizer", "schedule", "fit", "first_batch_probe")
    ref = selected(root/b.PARENT_SOURCE, names, ns)
    # New-cohort inputs are bound only in this isolated reference namespace.
    # No imported accepted module or its globals are modified.
    ref.SEEDS = tuple(range(308001, 308006)); ref.ORDERS = tuple(range(308101, 308106))
    for key in ("ARMS", "BASE_LR", "CORE_LR", "FIT_RNG", "STEPS"): setattr(ref, key, getattr(b, key))
    p306 = selected(root/"fold_lm/v05_benchmarks/model_c306_broad_length_core_freeze.py", ("first_batch_probe",),
                    dict(torch=torch, F=F, copy=copy, require=b.require, ARMS=b.ARMS[:2]))
    wide = selected(root/b.WIDE_SOURCE, ("schedule_stats",), dict(torch=torch, digest=b.digest))
    return ref, p306, wide


def dataset():
    data = {"TRAIN": [], "HOLDOUT": []}
    for e, v, lang in itertools.product(((0, 1), (0, 2), (1, 2)), itertools.permutations(range(4), 2), ("en", "ja")):
        split = "HOLDOUT" if (v[1]-v[0]) % 4 == 2 else "TRAIN"
        for order, query in itertools.product((e, e[::-1]), e):
            data[split].append(dict(id=str((e, v, lang, order, query)), entities=list(e), values=list(v),
                permutation=list(order), query=query, language=lang, target=48+v[e.index(query)]))
    return data


def pairs_from_rows(rows):
    groups = {}
    for i, r in enumerate(rows):
        key = (r["language"], tuple(r["entities"]), tuple(r["values"]), tuple(r["permutation"]))
        groups.setdefault(key, []).append(i)
    return torch.tensor([sorted(groups[k], key=lambda i: rows[i]["query"]) for k in sorted(groups)], dtype=torch.int64)


def tables(data):
    y = torch.tensor([r["target"] for r in data["TRAIN"]], dtype=torch.int64)
    x = torch.zeros((3, 3, 192, 64), dtype=torch.int64); x[:, :, :, 0] = y-48
    return x, y


class ToyCore(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear = torch.nn.Linear(4, 4, dtype=torch.float64)
        self.unused = torch.nn.Parameter(torch.zeros(3308, dtype=torch.float64)); self.config = NS(slots=64)
    def forward(self, state): return torch.tanh(self.linear(state))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone = torch.nn.Module(); self.backbone.config = NS(max_tokens=64)
        self.backbone.local_encoder = torch.nn.Embedding(4, 4, dtype=torch.float64)
        self.backbone.core = ToyCore(); self.backbone.unused = torch.nn.Parameter(torch.zeros(9632, dtype=torch.float64))
        self.read = torch.nn.Linear(4, 256, dtype=torch.float64)
    def forward(self, tokens, tasks):
        assert tokens.shape == (len(tokens), 64) and tasks.shape == (len(tokens),) and not bool(tasks.any())
        local = self.backbone.local_encoder(tokens[:, 0]); state = local
        for _ in range(2):
            next_state = self.backbone.core(state); self.backbone.core(local); state = next_state
        return self.read(state)


def fingerprint(model): return b.digest({n: p.detach().tolist() for n, p in model.state_dict().items()})


class FakeLengthReadout(Toy):
    def __init__(self, ref):
        torch.nn.Module.__init__(self); self.backbone = copy.deepcopy(ref.backbone); self.read = copy.deepcopy(ref.read)


def factory():
    def model(seed): torch.manual_seed(seed); return Toy()
    c = NS(c278=NS(MeanFinalDualReadout=lambda m, *args: m), factory=NS(new_model=model),
           reader=None, c269=NS(query_span_mask=None), base=NS(fingerprint=fingerprint))
    return NS(LengthReadout=FakeLengthReadout), c


@contextlib.contextmanager
def counted(model, unused):
    calls, cores = [0, 0], [0]
    def count(m, args, output): calls[0] += 1; calls[1] += len(args[0])
    def core(m, args, output): cores[0] += 1
    h = model.register_forward_hook(count); g = model.backbone.core.register_forward_hook(core)
    try: yield calls, cores
    finally: h.remove(); g.remove()


def records_fixture(data, wide, pairs):
    records = []
    for seed, arm in b.identities():
        events = b.schedule(seed, data["TRAIN"], pairs)
        raw = {str(n): dict(passed=True, totals=[dict(split=s, rows=size, correct=size, direct_pass=True,
                 full_pass=True, final_normal_nll=.1) for s, size in (("TRAIN", 576), ("HOLDOUT", 288))]) for n in b.LENGTHS}
        rates = [b.BASE_LR, b.CORE_LR] if arm == "core_slow" else [b.BASE_LR]
        fit = dict(steps=1200, training_rows=57600, optimizer_creations=1, fit_rng=612000,
            trainable_parameters=b.manifest()["trainable_parameters"][arm], ce_history=[.1]*1200,
            optimizer_group_lrs=[rates.copy() for _ in range(1200)], gradient_union={"read.weight": 1280},
            gradient_parameter_counts=[1280]*1200, schedule_events=events, **wide.schedule_stats(events))
        records.append(dict(seed=seed, arm=arm, parameters=14256, slots=64, initial_sha256="a"*64, final_sha256="b"*64,
            core_initial_sha256="c"*64, core_final_sha256=("c" if arm == "core_frozen" else "d")*64,
            fit=fit, raw=raw, forward_calls=1308, row_presentations=67968, core_forward_calls=5232,
            checkpoint_roundtrip=True, reload_max_error=0., replay_forward_calls=108, replay_row_presentations=10368, replay_core_forward_calls=432))
    return records


def diagnostic():
    return NS(normalize_task=lambda scored, *args: scored["totals"], partition=lambda rows: {k: v for k, v in rows[0].items() if k != "split"})


def protection():
    pins = {n: "b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE] = b.PARENT_BLOB; pins[b.WIDE_SOURCE] = b.WIDE_BLOB
    while len(pins) < 700: pins["fixture/"+str(len(pins))] = "b"*40
    return pins, {"fixture/input/"+str(i): "a"*64 for i in range(1309)}


class Audit:
    @staticmethod
    def sha(path):
        p = Path(path); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root, n): return Path(root)/n
    @staticmethod
    def git(root, *args):
        if args[0] == "rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0] == "branch": return b"feat/sft-target-loss\n"
        return b""


def payload(summary):
    pins, inputs = protection()
    return dict(experiment_id=b.EXPERIMENT_ID, stage=b.STAGE, commit_sha="f"*40, status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True, source_blobs=pins, input_sha256=inputs, artifacts=[dict(file=n) for n in b.OUTPUTS],
        validation_summary=summary, gate_f_candidate=False, production_adoption=False)


class C309Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); cls.det = torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.ref, cls.p306, cls.wide = references(); cls.pairs = NS(pairs_from_rows=pairs_from_rows)
        cls.wide.score_length = lambda data, raw, c: raw; cls.data = dataset(); cls.x, cls.y = tables(cls.data)
        torch.manual_seed(72); cls.initial = Toy(); cls.models, cls.fits = {}, {}
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:
                m = cls.ref.configure(copy.deepcopy(cls.initial), arm)
                cls.fits[arm] = b.fit(m, cls.data, cls.x, cls.y, b.SEEDS[0], arm, cls.pairs, cls.wide, cls.ref); cls.models[arm] = m
        cls.records = records_fixture(cls.data, cls.wide, cls.pairs)
        cls.metrics, cls.summary = b.analyze(cls.records, cls.data, cls.pairs, cls.wide, diagnostic(), None)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest(self): b.validate_seal(); self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for value in ("UNSEALED", "0"*64, "A"*64):
            with patch.object(b, "MANIFEST_SHA", value), self.assertRaises(ValueError): b.validate_seal()

    def test_03_unchanged_policy_and_fresh_seeds(self):
        b.policy_contract(self.ref)
        old = self.ref.manifest(); old["core_lr"]["core_slow"] = .001
        with patch.object(self.ref, "manifest", return_value=old), self.assertRaisesRegex(ValueError, "policy drift"): b.policy_contract(self.ref)
        with patch.object(self.ref, "SEEDS", b.SEEDS), self.assertRaisesRegex(ValueError, "fresh seed"): b.policy_contract(self.ref)

    def test_04_factory_and_membership(self):
        wide, c = factory(); models = b.make_models(b.SEEDS[0], self.ref, wide, c)
        self.assertEqual(len({fingerprint(m) for m in models.values()}), 1)
        pointers = [p.data_ptr() for m in models.values() for p in m.parameters()]; self.assertEqual(len(pointers), len(set(pointers)))
        for arm, model in models.items():
            groups = self.ref.parameter_groups(model, arm); ids = [id(p) for g in groups for p in g["params"]]
            self.assertEqual(len(ids), len(set(ids))); self.assertEqual(set(ids), {id(p) for p in model.parameters() if p.requires_grad})
        with self.assertRaises(ValueError): b.make_models(308001, self.ref, wide, c)

    def test_05_all_schedules_match_accepted_algorithm(self):
        for seed in b.SEEDS:
            events = b.schedule(seed, self.data["TRAIN"], self.pairs)
            self.assertTrue(torch.equal(events, self.ref.schedule(seed, self.data["TRAIN"], self.pairs)))
            self.assertEqual(self.wide.schedule_stats(events)["per_length_row_exposures"], [[100]*192 for _ in range(3)])
        rng = torch.random.get_rng_state().clone(); b.schedule(b.SEEDS[0], self.data["TRAIN"], self.pairs)
        self.assertTrue(torch.equal(rng, torch.random.get_rng_state()))

    def test_06_probe_initial_models_unchanged(self):
        models = {a: self.ref.configure(copy.deepcopy(self.initial), a) for a in b.ARMS}; hashes = [fingerprint(m) for m in models.values()]
        probe = self.ref.first_batch_probe(models, self.x, self.y, b.schedule(b.SEEDS[0], self.data["TRAIN"], self.pairs), self.p306)
        self.assertTrue(probe["freeze_probe"]["encoder_receives_signal"]); self.assertTrue(probe["full_slow_preclip_gradients_equal"])
        self.assertLessEqual(probe["first_step_scaled_core_delta_max_error"], 1e-12); self.assertEqual(hashes, [fingerprint(m) for m in models.values()])

    def test_07_all_arms_equal_parent1200step_fit(self):
        for arm in b.ARMS:
            m = self.ref.configure(copy.deepcopy(self.initial), arm)
            with contextlib.redirect_stdout(io.StringIO()): f = self.ref.fit(m, self.data, self.x, self.y, b.SEEDS[0], arm, self.pairs, self.wide)
            for key in ("ce_history", "optimizer_group_lrs", "gradient_union", "gradient_parameter_counts", "event_sha256"):
                self.assertEqual(f[key], self.fits[arm][key])
            self.assertEqual(fingerprint(m), fingerprint(self.models[arm]))

    def test_08_optimizer_once_and_rng_reset(self):
        real, made = torch.optim.AdamW, []
        def create(*args, **kwargs): o = real(*args, **kwargs); made.append(o); return o
        m = copy.deepcopy(self.initial); torch.manual_seed(999)
        with patch.object(torch.optim, "AdamW", side_effect=create), contextlib.redirect_stdout(io.StringIO()):
            f = b.fit(m, self.data, self.x, self.y, b.SEEDS[0], "core_slow", self.pairs, self.wide, self.ref)
        self.assertEqual(len(made), 1); self.assertEqual({int(v["step"]) for v in made[0].state.values()}, {1200})
        self.assertEqual(f["ce_history"], self.fits["core_slow"]["ce_history"])

    def test_09_core_freeze_and_nonfinite(self):
        for arm in b.ARMS:
            self.assertEqual(fingerprint(self.initial.backbone.core) == fingerprint(self.models[arm].backbone.core), arm == "core_frozen")
            self.assertLess(self.fits[arm]["ce_history"][-1], self.fits[arm]["ce_history"][0])
        m = copy.deepcopy(self.initial)
        with torch.no_grad(): m.read.weight.fill_(float("nan"))
        with self.assertRaisesRegex(ValueError, "logits"): b.fit(m, self.data, self.x, self.y, b.SEEDS[0], "full_train", self.pairs, self.wide, self.ref)

    def test_10_bad_training_inputs(self):
        y = self.y.clone(); y[0] = 99
        with self.assertRaises(ValueError): b.fit(copy.deepcopy(self.initial), self.data, self.x, y, b.SEEDS[0], "full_train", self.pairs, self.wide, self.ref)
        rows = copy.deepcopy(self.data["TRAIN"]); rows[1]["query"] = rows[0]["query"]
        with self.assertRaises(ValueError): b.schedule(b.SEEDS[0], rows, self.pairs)
        with self.assertRaises(ValueError): b.schedule(308001, self.data["TRAIN"], self.pairs)

    def test_11_optimizer_policy_rejected(self):
        m = copy.deepcopy(self.initial); opt = self.ref.optimizer_for(m, "core_slow")
        opt.param_groups[1]["lr"] = .005
        with self.assertRaisesRegex(ValueError, "optimizer policy"): self.ref.verify_optimizer(opt, m, "core_slow")
        with patch.object(self.ref, "optimizer_for", return_value=opt), self.assertRaises(ValueError):
            b.fit(copy.deepcopy(self.initial), self.data, self.x, self.y, b.SEEDS[0], "core_slow", self.pairs, self.wide, self.ref)

    def test_12_fit_history_validation(self):
        for arm in b.ARMS: b.check_fit(self.fits[arm], b.SEEDS[0], arm, self.data, self.pairs, self.wide)
        for mutate in (lambda f: f["optimizer_group_lrs"][3].__setitem__(1, .005), lambda f: f.update(fit_rng=1), lambda f: f["ce_history"].pop()):
            f = copy.deepcopy(self.fits["core_slow"]); mutate(f)
            with self.assertRaises(ValueError): b.check_fit(f, b.SEEDS[0], "core_slow", self.data, self.pairs, self.wide)

    def test_13_actual_train_one_counted(self):
        def evaluate(model, prompts, data, c):
            self.assertFalse(model.training); self.assertFalse(any(p.requires_grad for p in model.parameters()))
            with torch.no_grad():
                for _ in range(108): model(torch.zeros((96, 64), dtype=torch.int64), torch.zeros(96, dtype=torch.int64))
            return {}
        m = copy.deepcopy(self.initial); c = NS(base=NS(fingerprint=fingerprint), p267=NS(counted=counted), core=None)
        with contextlib.redirect_stdout(io.StringIO()):
            r, state = b.train_one(m, self.data, {}, self.x, self.y, b.SEEDS[0], "core_slow", self.pairs,
                NS(schedule_stats=self.wide.schedule_stats, evaluate=evaluate), c, self.ref)
        self.assertEqual((r["forward_calls"], r["row_presentations"], r["core_forward_calls"]), (1308, 67968, 5232))
        self.assertEqual(list(state), list(m.state_dict()))

    def test_14_summary_inventory(self):
        self.assertEqual((len(self.metrics), len(self.summary["final_partitions"]), len(self.summary["contrasts"])), (15, 120, 80))
        b.validate_result(payload(self.summary))

    def test_15_new_cohort_primary_only(self):
        records = copy.deepcopy(self.records); records[2]["raw"]["5"]["passed"] = False
        _, s = b.analyze(records, self.data, self.pairs, self.wide, diagnostic(), None)
        self.assertFalse(s["candidate_gate"]); self.assertEqual(s["length_pass_counts"]["5"]["core_slow"], 4)
        b.validate_result(payload(s))

    def test_16_pairing_and_replay_rejections(self):
        for key, value in (("core_final_sha256", "z"*64), ("reload_max_error", .01), ("initial_sha256", "z"*64), ("replay_forward_calls", 107)):
            records = copy.deepcopy(self.records); records[1][key] = value
            with self.assertRaises(ValueError): b.analyze(records, self.data, self.pairs, self.wide, diagnostic(), None)
        with self.assertRaises(ValueError): b.analyze(self.records[:-1], self.data, self.pairs, self.wide, diagnostic(), None)

    def test_17_parent_flags_and_both_controls(self):
        flags = b.expected_parent_flags()
        self.assertEqual(len(flags), 15)
        for n in b.LENGTHS:
            self.assertEqual([sum(r["length_pass"][str(n)] for r in flags if r["arm"] == a) for a in b.ARMS], [4, 5, 5])
        self.assertTrue(all(r["fitted_train_direct_pass"] for r in flags))
        self.assertEqual(b.paired_outcomes(self.summary["seed_results"], "core_frozen")["both_pass"], 5)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths = [(Path("/c309-fixture")/str(i)/"summary.json").resolve() for i in range(35)]
        p = dict(experiment_id="C308-v5b-core-learning-rate", commit_sha=b.PARENT_EXECUTION, status="PASS",
            source_blobs={b.PARENT_SOURCE: b.PARENT_BLOB, b.WIDE_SOURCE: b.WIDE_BLOB}, artifacts=[dict(file=n) for n in b.OUTPUTS],
            validation_summary=dict(seed_results=b.expected_parent_flags(), candidate_gate=True, all_groups_matched=True,
                all_replays=True, paired_five={"full_train": dict(both_pass=4, control_only=0, candidate_only=1, both_fail=0),
                "core_frozen": dict(both_pass=5, control_only=0, candidate_only=0, both_fail=0)}))
        parent = NS(parent_hashes=lambda: tuple(str(i%10)*64 for i in range(34)), verify_artifacts=Mock(return_value=(p, [])), validate_result=Mock())
        prompts = {"fixture": "prompts"}; wide = NS(prompt_dataset=lambda _: prompts, validate_prompts=Mock())
        mapping = dict(zip(map(str, paths), b.parent_hashes(parent), strict=True))
        c = NS(audit=NS(sha=lambda path: mapping[str(path)], read_json=lambda path: self.data if path.name == "dataset.json" else prompts))
        with patch.object(b, "context", return_value=(parent, None, None, NS(no_neural=contextlib.nullcontext), wide, None, None, None, c)), patch.object(b, "DATA_SHA", b.digest(self.data)), patch.object(b, "PROMPTS_SHA", b.digest(prompts)):
            yield paths, mapping, parent, p

    def test_18_all35_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths, mapping, parent, p):
            self.assertEqual(b.load_parent(paths)[0], p); parent.verify_artifacts.assert_called_once_with(paths[0].parent, paths[1:], b.PARENT_EXECUTION)
            for path in paths:
                old = mapping[str(path)]; mapping[str(path)] = "f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)] = old

    def test_19_parent_schema_and_data_rejected(self):
        for mutate in (lambda p: p.update(status="FAIL"), lambda p: p["artifacts"].pop(), lambda p: p["validation_summary"]["seed_results"].pop()):
            with self.loader_fixture() as (paths, _, _, p):
                mutate(p)
                with self.assertRaises(ValueError): b.load_parent(paths)
        with self.loader_fixture() as (paths, _, _, _), patch.object(b, "DATA_SHA", "0"*64), self.assertRaises(ValueError): b.load_parent(paths)

    def test_20_protection_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); pins = {b.PARENT_SOURCE: b.PARENT_BLOB, b.WIDE_SOURCE: b.WIDE_BLOB}
            while len(pins) < 694: pins["accepted/"+str(len(pins))] = "b"*40
            for name in list(pins)+list(b.OWN):
                path = root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(name, encoding="utf-8")
            inputs = {str((root/n).resolve()): Audit.sha(root/n) for n in pins}
            for i in range(1295-len(inputs)):
                path = root/f"input{i}"; path.write_text("input", encoding="utf-8"); inputs[str(path.resolve())] = Audit.sha(path)
            folder = root/"parent"; folder.mkdir(); sp = folder/"summary.json"; sp.write_text("summary", encoding="utf-8")
            mapping, artifacts = {str(sp.resolve()): b.PARENT_SHA}, []
            for n in b.OUTPUTS:
                path = folder/n; path.write_text("output", encoding="utf-8"); mapping[str(path.resolve())] = "a"*64; artifacts.append(dict(file=n, sha256="a"*64))
            def sha(p): return mapping.get(str(Path(p).resolve()), Audit.sha(p))
            parent = types.ModuleType("parent"); parent.__file__ = str(root/b.PARENT_SOURCE); parent.context = lambda: ()
            for k, v in vars(self.ref).items(): setattr(parent, k, v)
            wide = NS(PINNED={b.WIDE_SOURCE: b.WIDE_BLOB}, context=lambda: ())
            c = NS(factory=NS(language_module=lambda: None), audit=NS(sha=sha, git=lambda root, *a: (pins.get(a[1][5:], "c"*40)+"\n").encode(),
                safe_child=Audit.safe_child, protect_tree_files=lambda root, ps: {str((root/n).resolve()): sha(root/n) for n in ps}))
            p = dict(source_blobs=pins, input_sha256=inputs, artifacts=artifacts)
            with patch.object(b, "context", return_value=(parent, None, None, None, wide, None, None, None, c)), patch.object(b, "load_parent", return_value=(p, None, None)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len, b.precheck([sp]*35, root))), (700, 1309))
                c.missing = types.ModuleType("missing"); c.missing.__file__ = str(root/"unprotected.py")
                with self.assertRaisesRegex(ValueError, "unprotected helper"): b.precheck([sp]*35, root)

    def test_21_actual_preflight_dispatch(self):
        wide, c = factory(); wide.training_tables = lambda data: (self.x, self.y); wide.schedule_stats = self.wide.schedule_stats
        with patch.object(b, "context", return_value=(self.ref, None, self.p306, None, wide, self.pairs, None, None, c)), patch.object(b, "precheck", return_value=protection()), patch.object(b, "load_parent", return_value=({}, self.data, {})), contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*35, Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        records = copy.deepcopy(self.records); events = []
        def train(*args): events.append("train"); return records[b.identities().index((args[5], args[6]))], {}
        def replay(model, state, record, prompts, data, c):
            self.assertEqual(prompts, {"fixture": "prompts"}); events.append("replay")
        def precheck(*args): events.append("precheck"); return protection()
        wide = NS(training_tables=lambda data: (self.x, self.y), replay_one=replay, score_length=self.wide.score_length, schedule_stats=self.wide.schedule_stats)
        with patch.object(b, "context", return_value=(self.ref, None, None, NS(no_neural=contextlib.nullcontext), wide, self.pairs, diagnostic(), None, NS(audit=Audit()))), patch.object(b, "load_parent", return_value=({}, self.data, {"fixture": "prompts"})), patch.object(b, "precheck", side_effect=precheck), patch.object(b, "make_models", return_value=dict.fromkeys(b.ARMS)), patch.object(b, "train_one", side_effect=train):
            yield events

    def test_22_actual_run_loader_replay_order(self):
        original, loads = b.load_bundle, []
        def load(path): loads.append(Path(path).name); return original(path)
        with self.run_fixture() as events, tempfile.TemporaryDirectory() as tmp, patch.object(b, "load_bundle", side_effect=load), contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp)/"run"; p = b.run(summaries=["x"]*35, output_dir=out, expected_head="f"*40)
            self.assertEqual(events, ["precheck"]+["train"]*15+["replay"]*15+["precheck"]); self.assertEqual(loads, ["trained-models.pt"])
            self.assertEqual(b.verify_artifacts(out, ["x"]*35, "f"*40)[0], p)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*35, output_dir=out, expected_head="f"*40)

    def test_23_byte_and_semantic_tamper(self):
        with self.run_fixture(), tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp)/"run"; p = b.run(summaries=["x"]*35, output_dir=out, expected_head="f"*40)
            path = out/"measurements.json"; path.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "output bytes"): b.verify_artifacts(out, ["x"]*35, "f"*40)
            a = next(a for a in p["artifacts"] if a["file"] == path.name); a.update(sha256=Audit.sha(path), serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError, "persisted"): b.verify_artifacts(out, ["x"]*35, "f"*40)

    def test_24_bundle_schema_reorder(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"m.pt"; value = dict(schema="fold-c309-core-lr-replication-models-v1", identities=[list(i) for i in b.identities()], states=[{}]*15)
            torch.save(value, path); self.assertEqual(len(b.load_bundle(path)), 15); value["identities"].reverse(); torch.save(value, path)
            with self.assertRaises(ValueError): b.load_bundle(path)

    def test_25_result_flags_scope(self):
        for mutate in (lambda p: p.update(gate_f_candidate=True), lambda p: p["validation_summary"].update(train_steps=False), lambda p: p["validation_summary"]["seed_results"][0].update(quint_pass=False)):
            p = payload(copy.deepcopy(self.summary)); mutate(p)
            with self.assertRaises(ValueError): b.validate_result(p)

    def test_26_semantic_regression_inventory(self):
        class Dummy(unittest.TestCase):
            def __init__(self, name): super().__init__(); self.name = name
            def runTest(self): pass
            def id(self): return self.name
        ids = [f"fixture.{i}" for i in range(4909)]+[b.EXCLUDED]
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite = b.regression_suite(Path.cwd()); self.assertEqual(suite.countTestCases(), 4909)
            self.assertEqual({t.id() for t in b.flatten(suite)}, set(ids)-{b.EXCLUDED})
        with patch.object(b, "regression_modules", return_value=[]), patch.object(unittest.defaultTestLoader, "loadTestsFromNames", return_value=unittest.TestSuite([Dummy("x"), Dummy("x")])), self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_27_cli_context_guard(self):
        argv = ["prog", "--summaries"]+[str(i) for i in range(35)]+["--output-dir", "out", "--expected-head", "f"*40]
        with patch.object(sys, "argv", argv), patch.object(b, "run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]), 35)
        parent = NS(context=lambda: tuple(range(8)), regression_modules=lambda root: [f"m{i}" for i in range(193)])
        package = types.ModuleType("fold_lm.v05_benchmarks"); package.model_c308_core_learning_rate = parent
        with patch.dict(sys.modules, {"fold_lm.v05_benchmarks": package}):
            self.assertEqual(b.context(), (parent, *range(8))); self.assertEqual(len(b.regression_modules(Path.cwd())), 194)
        b.guard(Path.cwd(), "f"*40, NS(audit=Audit()))
        with self.assertRaises(ValueError): b.guard(Path.cwd(), "e"*40, NS(audit=Audit()))

    def test_28_utf8_cp932(self):
        root = Path(__file__).resolve().parents[1]
        with patch.object(io, "text_encoding", side_effect=lambda encoding, stacklevel=2: "cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA, (root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__), Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "read_text":
                    self.assertTrue(any(k.arg == "encoding" and isinstance(k.value, ast.Constant) and k.value.value == "utf-8" for k in node.keywords))

    def test_29_runner_indices_paths(self):
        root = Path(__file__).resolve().parents[1]; runner = (root/b.OWN[2]).read_text(encoding="utf-8"); launcher = (root/b.OWN[3]).read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@", runner, re.S); self.assertEqual(len(blocks), 3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:37]", blocks[2]); self.assertIn("head = sys.argv[37]", blocks[2])
        self.assertEqual(len(re.findall(r"runs\\c\d{3}-.*?\\summary.json", launcher)), 35)
        self.assertLess(launcher.index("-Mode Validate"), launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"), launcher.index("publish_experiment_log.ps1"))

    def test_30_parent_not_mutated(self):
        before = {n: getattr(self.ref, n) for n in ("SEEDS", "ORDERS", "BASE_LR", "CORE_LR", "FIT_RNG")}
        b.policy_contract(self.ref); b.schedule(b.SEEDS[0], self.data["TRAIN"], self.pairs)
        self.assertEqual(before, {n: getattr(self.ref, n) for n in before})
        tree = ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store) and isinstance(node.value, ast.Name):
                self.assertNotIn(node.value.id, ("parent", "wide", "p306", "p307"))

    def test_31_clip_before_step_model_order(self):
        real_clip = torch.nn.utils.clip_grad_norm_; orders = []
        def clip(params, *args, **kwargs):
            params = list(params); orders.append([id(p) for p in params]); return real_clip(params, *args, **kwargs)
        m = copy.deepcopy(self.initial)
        with patch.object(torch.nn.utils, "clip_grad_norm_", side_effect=clip), contextlib.redirect_stdout(io.StringIO()):
            b.fit(m, self.data, self.x, self.y, b.SEEDS[0], "core_slow", self.pairs, self.wide, self.ref)
        self.assertEqual(orders, [[id(p) for p in m.parameters()]]*1200)

    def test_32_imports_and_count(self):
        tree = ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports = [n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports, ["model_c308_core_learning_rate"])
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))), 32)
        self.assertEqual(b.CORE_LR/b.BASE_LR, .1)


if __name__ == "__main__":
    unittest.main()
