"""C267 authoring fixtures are synthetic; they do not establish learned FOLD capability."""
import ast
from collections import Counter
import contextlib
import copy
import hashlib
import inspect
import io
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as b


class Tiny(nn.Module):
    """Four surrogate core calls and14256 parameters, not the production architecture."""
    def __init__(self, seed):
        super().__init__(); torch.manual_seed(seed)
        self.backbone = nn.Module()
        self.backbone.embedding = nn.Embedding(259,16)
        self.backbone.linear = nn.Linear(16,16)
        self.backbone.core = nn.Linear(16,16,bias=False)
        self.read = nn.Linear(16,256)
        self.padding = nn.Parameter(torch.zeros(5232))
        self.double().eval()
    def forward(self,tokens,tasks):
        x = torch.tanh(self.backbone.linear(self.backbone.embedding(tokens).mean(1)))
        for _ in range(4): x = x + .1*torch.tanh(self.backbone.core(x))
        return self.read(x)


class Factory:
    @staticmethod
    def new_model(seed): return Tiny(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw) <= 46,"length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def make_model(model,arm,seed,aligned,reader):
        b.require(arm == "aligned_precore_read","architecture"); return model
    @staticmethod
    def fingerprint(model):
        h = hashlib.sha256()
        for name,t in sorted(model.state_dict().items()):
            h.update(name.encode()); h.update(t.detach().cpu().numpy().tobytes())
        return h.hexdigest()


class Core:
    @staticmethod
    def core_counter(model):
        counts = [0]
        def hook(module,args,output): counts[0] += 1
        return counts,model.backbone.core.register_forward_hook(hook)


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("fixture-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        p = (Path(root)/name).resolve(); b.require(p.parent == Path(root).resolve(),"unsafe child"); return p
    @staticmethod
    def git(root,*args):
        if args == ("rev-parse","HEAD"): return b"fixture-head"
        if args == ("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


def protection():
    return ({**{f"old-{i}":"fixture" for i in range(442)},**{n:"fixture" for n in b.OWN}},
            {f"fixture-input-{i}":"0"*64 for i in range(761)})


def fixture_records(data):
    raw = {}
    for split,rows in data.items():
        raw[split] = {}
        for profile in b.PROFILES:
            raw[split][profile] = {}
            for view in b.VIEWS:
                x = torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):
                    target = r["target"] if view == "normal" else 48 if view == "evidence_blind" else 48+r["values"][0]
                    x[i,target] = 10.
                raw[split][profile][view] = x
    return [dict(seed=s,arm=a,parameters=14256,initial_sha256=str(s),final_sha256="fixture",weights_changed=True,
        forward_calls=827,row_presentations=40992,core_forward_calls=3308,
        replay_forward_calls=27,replay_row_presentations=2592,replay_core_forward_calls=108,
        checkpoint_roundtrip=True,reload_max_error=0.,
        fit=dict(steps=800,training_rows=38400,last_loss=0.,**b.schedule(s,a)[2]),raw=copy.deepcopy(raw)) for s,a in b.identities()]


class C267Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data = b.dataset(); cls.tokens,cls.targets = b.training_tables(cls.data,Factory)
        cls.records = fixture_records(cls.data)

    def test_01_manifest_and_data_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.data),b.DATA_SHA)
        self.assertTrue(all(len(v) == 64 for v in b.PARENT_ARTIFACTS.values()))
        b.validate_data(self.data)

    def test_02_disjoint_balanced_value_split(self):
        for split,count in (("TRAIN",8),("HOLDOUT",4)):
            pairs = {tuple(r["values"]) for r in self.data[split]}
            self.assertEqual(len(pairs),count)
            for i in (0,1): self.assertEqual(Counter(p[i] for p in pairs),{v:count//4 for v in range(4)})
        self.assertFalse({tuple(r["values"]) for r in self.data["TRAIN"]} & set(b.HOLDOUT_VALUES))
        self.assertEqual(sum(len(v) for v in self.data.values()),288)

    def test_03_name_maps_targets_lengths_and_bytes(self):
        known = set("abc甲乙丙0123=;?".encode())
        for rows in self.data.values():
            for r in rows:
                lengths = []
                for p in b.PROFILES:
                    text = b.render(r,p); fields = text.split(";"); facts = dict(x.split("=") for x in fields[:-1])
                    self.assertEqual(ord(facts[fields[-1][:-1]]),r["target"])
                    lengths.append(len(text.encode())); self.assertTrue(set(text.encode()) <= known)
                self.assertEqual(len(set(lengths)),1)

    def test_04_no_holdout_tokenization_for_training(self):
        data = dict(self.data,HOLDOUT=[])
        x,y = b.training_tables(data,Factory)
        self.assertTrue(torch.equal(x,self.tokens) and torch.equal(y,self.targets))
        self.assertEqual(x.shape,(3,192,48))
        bad = copy.deepcopy(self.data); bad["TRAIN"][0]["target"] = 200
        with self.assertRaises(ValueError): b.training_tables(bad,Factory)

    def test_05_all_seeds_matched_800_step_schedules(self):
        for seed in b.SEEDS:
            a,ap,am = b.schedule(seed,b.ARMS[0]); c,cp,cm = b.schedule(seed,b.ARMS[1])
            self.assertTrue(torch.equal(a,c)); self.assertEqual(am["logical_batch_sha256"],cm["logical_batch_sha256"])
            self.assertEqual(am["row_exposures"],[200]*192)
            self.assertEqual(cm["profile_updates"],[268,268,264]); self.assertEqual(am["profile_updates"],[800,0,0])
            for epoch in range(200): self.assertEqual(sorted(a[epoch*4:epoch*4+4].flatten().tolist()),list(range(192)))

    def test_06_profile_changes_only_visible_names(self):
        for r in self.data["TRAIN"]:
            for p in b.PROFILES:
                fields = b.render(r,p).split(";")
                self.assertEqual([x.split("=")[1] for x in fields[:-1]], [str(r["values"][r["entities"].index(i)]) for i in r["permutation"]])
        with self.assertRaises(ValueError): b.schedule(263001,b.ARMS[0])
        with self.assertRaises(ValueError): b.schedule(b.SEEDS[0],"other")

    def test_07_initial_clones_are_equal_not_aliased(self):
        m = Tiny(b.SEEDS[0]); a,c = copy.deepcopy(m),copy.deepcopy(m)
        self.assertEqual(sum(p.numel() for p in m.parameters()),14256)
        self.assertEqual(Base.fingerprint(a),Base.fingerprint(c))
        with torch.no_grad(): a.read.weight.add_(1)
        self.assertEqual(Base.fingerprint(m),Base.fingerprint(c)); self.assertNotEqual(Base.fingerprint(a),Base.fingerprint(c))

    def test_08_actual_short_optimizer_dispatch(self):
        original = torch.optim.AdamW; m = Tiny(b.SEEDS[0])
        before = Base.fingerprint(m)
        with patch.object(b,"STEPS",4),patch.object(torch.optim,"AdamW",wraps=original) as optimizer:
            out = b.fit(m,self.tokens,self.targets,b.SEEDS[0],b.ARMS[1])
        self.assertEqual(optimizer.call_args.kwargs["lr"],.005)
        self.assertEqual(out["training_rows"],192); self.assertNotEqual(before,Base.fingerprint(m))

    def test_09_actual_800_update_loop_and_strict_replay(self):
        model = Tiny(b.SEEDS[0])
        with contextlib.redirect_stdout(io.StringIO()):
            r,state = b.train_one(model,b.SEEDS[0],b.ARMS[1],self.data,self.tokens,self.targets,Core,Base,Factory)
        b.replay_one(Tiny(b.SEEDS[0]),state,r,self.data,Core,Base,Factory)
        self.assertEqual((r["forward_calls"],r["core_forward_calls"],r["replay_forward_calls"]),(827,3308,27))
        self.assertEqual(r["reload_max_error"],0.)

    def test_10_exception_cleans_count_hooks(self):
        m = Tiny(b.SEEDS[0])
        with patch.object(b,"fit",side_effect=RuntimeError("fixture")),self.assertRaises(RuntimeError):
            b.train_one(m,b.SEEDS[0],b.ARMS[0],self.data,self.tokens,self.targets,Core,Base,Factory)
        self.assertFalse(m._forward_hooks); self.assertFalse(m.backbone.core._forward_hooks)

    def test_11_perfect_metrics_and_fixed_denominators(self):
        metrics,s = b.analyze(self.records,self.data)
        self.assertTrue(s["candidate_gate"]); self.assertEqual(s["seed_pass_counts"],{a:5 for a in b.ARMS})
        self.assertEqual((len(metrics[0]["cells"]),len(metrics[0]["two_order"]),len(s["contrasts"])),(72,36,30))
        self.assertTrue(all(c["rows"] == (16 if c["split"] == "TRAIN" else 8) for c in metrics[0]["cells"]))
        self.assertTrue(all(c["correct_delta"] == c["collapse_delta"] == 0 for c in s["contrasts"]))
        reordered = json.loads(b.blob(self.data))
        self.assertEqual(b.score(self.data,self.records[0]["raw"]),b.score(reordered,self.records[0]["raw"]))

    def test_12_candidate_requires_all_profiles_and_seeds(self):
        for p in b.PROFILES:
            rr = copy.deepcopy(self.records); rr[1]["raw"]["HOLDOUT"][p]["normal"][0] = 0
            _,s = b.analyze(rr,self.data)
            self.assertFalse(s["candidate_gate"]); self.assertEqual(s["seed_pass_counts"]["mixed_names"],4)

    def test_13_control_cannot_rescue_or_fail_candidate(self):
        rr = copy.deepcopy(self.records); rr[0]["raw"]["TRAIN"][b.PROFILES[0]]["normal"][:] = 0
        _,s = b.analyze(rr,self.data); self.assertTrue(s["candidate_gate"]); self.assertEqual(s["seed_pass_counts"]["doubled_only"],4)

    def test_14_identical_wrong_answers_are_not_capability(self):
        rr = copy.deepcopy(self.records)
        for r in rr:
            if r["arm"] == "mixed_names":
                for split in r["raw"].values():
                    for views in split.values(): views["normal"][:] = 0
        metrics,s = b.analyze(rr,self.data); self.assertFalse(s["candidate_gate"])
        self.assertTrue(all(c["collapsed_pairs"] == c["pairs"] for c in metrics[1]["cells"]))

    def test_15_mask_gates_are_not_replaced_by_accuracy(self):
        for view in ("query_blind","evidence_blind"):
            raw = copy.deepcopy(self.records[0]["raw"])
            raw["HOLDOUT"]["shared_suffix"][view] = raw["HOLDOUT"]["shared_suffix"]["normal"].clone()
            self.assertFalse(b.score(self.data,raw)["passed"])

    def test_16_query_and_order_groups_count_both_versions(self):
        raw = copy.deepcopy(self.records[0]["raw"])
        raw["TRAIN"]["doubled"]["normal"][0] = 0
        m = b.score(self.data,raw)
        first = m["cells"][0]; order = m["two_order"][0]
        self.assertEqual(first["query_pair_accuracy"],7/8); self.assertEqual(order["both_correct"],15)
        self.assertEqual(first["correct"],15)

    def test_17_wrong_record_counts_seed_and_pairing(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data)
        for key,value in (("initial_sha256","mismatch"),("core_forward_calls",0),("reload_max_error",2e-9)):
            rr = copy.deepcopy(self.records); rr[1][key] = value
            with self.assertRaises(ValueError): b.analyze(rr,self.data)
        rr = copy.deepcopy(self.records); rr[1]["fit"]["profile_updates"] = [800,0,0]
        with self.assertRaises(ValueError): b.analyze(rr,self.data)

    def test_18_nonfinite_outputs_and_data_corruption(self):
        rr = copy.deepcopy(self.records); rr[0]["raw"]["TRAIN"]["doubled"]["normal"][0,0] = float("nan")
        with self.assertRaises(ValueError): b.analyze(rr,self.data)
        data = copy.deepcopy(self.data); data["HOLDOUT"][0]["target"] = 200
        with self.assertRaises(ValueError): b.analyze(self.records,data)

    def test_19_actual_diagnostic_parent_loader(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); summary = {"normal_answers":17280}; plan = {"synthetic":True}
            for name in b.PARENT_ARTIFACTS:
                (root/name).write_bytes(b.blob(summary if name == "validation-summary.json" else plan))
            artifacts = [dict(file=n,sha256=Audit.sha(root/n),serialized_bytes=(root/n).stat().st_size) for n in b.PARENT_ARTIFACTS]
            payload = dict(commit_sha=b.PARENT_EXECUTION,status="PASS",capability_pass_claim=False,validation_summary=summary,artifacts=artifacts)
            (root/"summary.json").write_bytes(b.blob(payload))
            parent = SimpleNamespace(validate_result=Mock(),manifest=lambda:plan)
            with patch.object(b,"context",return_value=(parent,Core,Base,None,None,Factory,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(root/"summary.json")),patch.object(b,"PARENT_ARTIFACTS",{x["file"]:x["sha256"] for x in artifacts}),patch.object(torch,"load",side_effect=AssertionError("no parent learned weights")):
                self.assertEqual(b.load_parent(root/"summary.json"),payload); parent.validate_result.assert_called_once()
                (root/"cells.json").write_bytes(b"bad")
                with self.assertRaises(ValueError): b.load_parent(root/"summary.json")

    def test_20_actual_ten_model_run_and_saved_postcheck(self):
        def train(model,seed,arm,data,tokens,targets,core,base,factory):
            r = copy.deepcopy(self.records[b.identities().index((seed,arm))]); r["initial_sha256"] = base.fingerprint(model)
            with torch.no_grad(): model.read.weight.add_(.01)
            r.update(final_sha256=base.fingerprint(model),raw=b.evaluate(model,data,factory))
            return r,copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,Core,Base,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"train_one",side_effect=train) as training:
            out = Path(d)/"out"
            with contextlib.redirect_stdout(io.StringIO()): p = b.run(c266_summary=Path(d)/"parent.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(training.call_count,10); self.assertEqual(pre.call_count,2)
            with patch.object(Factory,"new_model",side_effect=AssertionError("no postcheck model")),patch.object(b,"load_bundle",side_effect=AssertionError("no postcheck weight load")):
                self.assertEqual(b.verify_artifacts(out,"fixture-head")[0],p)
            with self.assertRaisesRegex(ValueError,"saved HEAD"): b.verify_artifacts(out,"wrong")
            (out/"measurements.json").write_bytes(b"[]")
            with self.assertRaises(ValueError): b.verify_artifacts(out,"fixture-head")

    def test_21_bundle_scope_and_summary_accounting(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"states.pt"; v = dict(schema="fold-c267-coverage-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(v,path); self.assertEqual(len(b.load_bundle(path)),10)
            v["identities"].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        _,s = b.analyze(self.records,self.data); pins,protected = protection()
        p = dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
            gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False,naming_benefit_claim=False)
        b.validate_result(p)
        with self.assertRaises(ValueError): b.validate_result(dict(p,unseen_name_transfer_claim=True))
        s["seed_pass_counts"]["mixed_names"] = 4
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_22_semantic_test_count_and_exact_exclusion(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name): super().__init__(); self.name = name
            def id(self): return self.name
        suite = unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_23_cli_parser_and_scientific_call_order(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root/"tools/run_c267.ps1").read_text(encoding="utf-8"); launcher = (root/"tools/invoke_c267.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3); indices = []
        for text in blocks:
            compile(text,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id == "sys" and n.value.attr == "argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure = re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher); self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start()); self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        calls = [(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first = lambda name:min(line for line,n in calls if n == name)
        for left,right in (("precheck","training_tables"),("train_one","load_bundle"),("replay_one","analyze")): self.assertLess(first(left),first(right))
        self.assertIn("load_parent",inspect.getsource(b.precheck))

    def test_24_dependency_count_and_resource_arithmetic(self):
        tree = ast.parse(inspect.getsource(b.precheck))
        pattern = next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id == "pattern" for t in n.targets))
        names = ["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,267)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names)); self.assertEqual(5+len(names)+1,43)
        self.assertEqual(748+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),761)
        self.assertEqual(10*(800+27+27),b.manifest()["model_forward_calls"])
        self.assertEqual(10*(800*48+2592*2),b.manifest()["row_presentations"])
        self.assertEqual(10*2592*256*8,b.manifest()["logit_payload_bytes"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
