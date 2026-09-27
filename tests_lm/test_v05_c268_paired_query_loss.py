"""C268 authoring tests. Synthetic model fixtures are not capability evidence."""
import ast
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
from unittest.mock import Mock,patch
import torch
from torch import nn
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as parent
from fold_lm.v05_benchmarks import model_c268_paired_query_loss as b


class Tiny(nn.Module):
    """A surrogate encoder/core, not FOLD's real state-update architecture."""
    def __init__(self,seed):
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
        for _ in range(4):
            x = x+.1*torch.tanh(self.backbone.core(x))
        return self.read(x)


class Factory:
    @staticmethod
    def new_model(seed): return Tiny(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,"prefix length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def make_model(model,arm,seed,aligned,reader):
        b.require(arm=="aligned_precore_read","architecture"); return model
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
        def hook(module,args,out): counts[0]+=1
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
        p = (Path(root)/name).resolve(); b.require(p.parent==Path(root).resolve(),"unsafe child"); return p
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"): return b"fixture-head"
        if args==("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


def protection():
    return {**{f"old-{i}":"fixture" for i in range(448)},**{n:"fixture" for n in b.OWN}}, {f"fixture-input-{i}":"0"*64 for i in range(774)}


def records(data):
    raw = {}
    for split,rows in data.items():
        raw[split] = {}
        for profile in b.PROFILES:
            raw[split][profile] = {}
            for view in b.VIEWS:
                x = torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):
                    target = r["target"] if view=="normal" else 48 if view=="evidence_blind" else 48+r["values"][0]
                    x[i,target] = 10.
                raw[split][profile][view] = x
    return [dict(seed=s,arm=a,parameters=14256,initial_sha256=str(s),final_sha256="fixture",weights_changed=True,
        forward_calls=827,row_presentations=40992,core_forward_calls=3308,replay_forward_calls=27,
        replay_row_presentations=2592,replay_core_forward_calls=108,checkpoint_roundtrip=True,reload_max_error=0.,
        fit=dict(steps=800,training_rows=38400,last_ce=0.,last_penalty=0.,last_total=0.,**b.schedule(s,data["TRAIN"])[2]),raw=copy.deepcopy(raw)) for s,a in b.identities()]


class C268Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data = parent.dataset(); cls.tokens,cls.targets = parent.training_tables(cls.data,Factory)
        cls.records = records(cls.data)

    def test_01_manifest_and_unchanged_dataset(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.data),b.manifest()["dataset_sha256"])
        parent.validate_data(self.data)
        self.assertTrue(all(len(v)==64 for v in b.PARENT_ARTIFACTS.values()))

    def test_02_pair_partition_uses_same_facts_different_queries(self):
        pairs = b.query_pairs(self.data["TRAIN"])
        self.assertEqual(pairs.shape,(96,2))
        for a,c in pairs.tolist():
            ra,rc = self.data["TRAIN"][a],self.data["TRAIN"][c]
            for key in ("language","entities","values","permutation"):
                self.assertEqual(ra[key],rc[key])
            self.assertNotEqual(ra["query"],rc["query"]); self.assertNotEqual(ra["target"],rc["target"])
        self.assertEqual(sorted(pairs.flatten().tolist()),list(range(192)))

    def test_03_all_seeds_same_schedule_and_exposure(self):
        for seed in b.SEEDS:
            ids,profiles,plan = b.schedule(seed,self.data["TRAIN"])
            other = b.schedule(seed,self.data["TRAIN"])
            self.assertTrue(torch.equal(ids,other[0])); self.assertEqual(plan,other[2])
            self.assertEqual(plan["row_exposures"],[200]*192); self.assertEqual(plan["profile_updates"],[268,268,264])
            for epoch in range(200):
                self.assertEqual(sorted(ids[epoch*4:epoch*4+4].flatten().tolist()),list(range(192)))
            self.assertEqual(len(profiles),800)

    def test_04_no_holdout_in_training_pairs_or_tables(self):
        x,y = parent.training_tables(dict(self.data,HOLDOUT=[]),Factory)
        self.assertTrue(torch.equal(x,self.tokens)); self.assertTrue(torch.equal(y,self.targets))
        with self.assertRaises(ValueError): b.query_pairs(self.data["HOLDOUT"])
        with self.assertRaises(ValueError): b.schedule(267005,self.data["TRAIN"])

    def test_05_ce_control_is_exact_ce(self):
        z = torch.randn(48,256,dtype=torch.float64,requires_grad=True)
        y = torch.tensor([48,49]*24)
        loss,ce,penalty = b.objective(z,y,"ce_only")
        expected = F.cross_entropy(z,y)
        self.assertTrue(torch.equal(loss,expected)); self.assertTrue(torch.equal(ce,expected))
        self.assertTrue(torch.equal(torch.autograd.grad(loss,z,retain_graph=True)[0],torch.autograd.grad(expected,z)[0]))
        self.assertGreaterEqual(float(penalty.detach()),0.)

    def test_06_collapsed_logits_receive_margin_penalty(self):
        z = torch.zeros(48,256,dtype=torch.float64,requires_grad=True); y = torch.tensor([48,49]*24)
        loss,ce,p = b.objective(z,y,"ce_pair_margin")
        self.assertEqual(float(p.detach()),2.); self.assertAlmostEqual(float((loss-ce).detach()),.2)
        grad = torch.autograd.grad(p,z)[0]
        self.assertLess(grad[0,48],0); self.assertGreater(grad[0,49],0)
        self.assertGreater(grad[1,48],0); self.assertLess(grad[1,49],0)

    def test_07_correct_and_swapped_margin_orientation(self):
        z = torch.zeros(48,256,dtype=torch.float64); y = torch.tensor([48,49]*24)
        z[0::2,48]=1.; z[1::2,49]=1.
        self.assertEqual(float(b.objective(z,y,"ce_pair_margin")[2]),0.)
        swapped = z.reshape(24,2,256).flip(1).reshape(48,256)
        self.assertEqual(float(b.objective(swapped,y,"ce_pair_margin")[2]),4.)

    def test_08_margin_alone_is_not_correctness(self):
        z = torch.zeros(48,256,dtype=torch.float64); y = torch.tensor([48,49]*24)
        z[:,48]=10.; z[0::2,48]=12.
        loss,ce,penalty = b.objective(z,y,"ce_pair_margin")
        self.assertEqual(float(penalty),0.); self.assertGreater(float(ce),4.)
        self.assertTrue((z.argmax(-1)==48).all()); self.assertTrue(torch.equal(loss,ce))

    def test_09_loss_rejects_nonfinite_or_equal_targets(self):
        z = torch.zeros(48,256,dtype=torch.float64); y = torch.tensor([48,49]*24)
        for bad in (torch.full_like(y,48),torch.full_like(y,256)):
            with self.assertRaises(ValueError): b.objective(z,bad,b.ARMS[1])
        z[0,0]=float("nan")
        with self.assertRaises(ValueError): b.objective(z,y,b.ARMS[1])

    def test_10_pair_loss_matches_scalar_calculation(self):
        z = torch.randn(48,256,dtype=torch.float64); y = torch.tensor([48,49]*24)
        expected = sum(max(0.,2.-float((z[i,48]-z[i,49])-(z[i+1,48]-z[i+1,49]))) for i in range(0,48,2))/24
        self.assertAlmostEqual(float(b.objective(z,y,b.ARMS[1])[2]),expected,places=12)
        reordered = z.reshape(24,2,256).flip(1).reshape(48,256)
        yr = y.reshape(24,2).flip(1).reshape(48)
        self.assertAlmostEqual(float(b.objective(z,y,b.ARMS[1])[2]),float(b.objective(reordered,yr,b.ARMS[1])[2]),places=12)

    def test_11_actual_short_optimizer_flow(self):
        m = Tiny(b.SEEDS[0]); before = Base.fingerprint(m)
        with patch.object(b,"STEPS",4),patch.object(torch.optim,"AdamW",wraps=torch.optim.AdamW) as optimizer:
            r = b.fit(m,self.data,self.tokens,self.targets,b.SEEDS[0],b.ARMS[1])
        self.assertEqual(r["training_rows"],192); self.assertNotEqual(before,Base.fingerprint(m))
        self.assertEqual(optimizer.call_args.kwargs["lr"],.005)
        self.assertIsNotNone(m.read.weight.grad)

    def test_12_full800_train_loop_and_parent_checkpoint_replay(self):
        m = Tiny(b.SEEDS[0])
        with contextlib.redirect_stdout(io.StringIO()):
            r,state = b.train_one(m,b.SEEDS[0],b.ARMS[1],self.data,self.tokens,self.targets,parent,Core,Base,Factory)
        parent.replay_one(Tiny(b.SEEDS[0]),state,r,self.data,Core,Base,Factory)
        self.assertEqual((r["forward_calls"],r["core_forward_calls"],r["replay_forward_calls"]),(827,3308,27))
        self.assertEqual(r["reload_max_error"],0.)
        self.assertAlmostEqual(r["fit"]["last_total"],r["fit"]["last_ce"]+.1*r["fit"]["last_penalty"])

    def test_13_actual_failure_cleans_hooks(self):
        m = Tiny(b.SEEDS[0])
        with patch.object(b,"fit",side_effect=RuntimeError("fixture")),self.assertRaises(RuntimeError):
            b.train_one(m,b.SEEDS[0],b.ARMS[0],self.data,self.tokens,self.targets,parent,Core,Base,Factory)
        self.assertFalse(m._forward_hooks); self.assertFalse(m.backbone.core._forward_hooks)

    def test_14_existing_scoring_and_candidate_control_separation(self):
        metrics,s = b.analyze(self.records,self.data,parent)
        self.assertTrue(s["candidate_gate"]); self.assertEqual(len(metrics[0]["cells"]),72)
        self.assertEqual(len(metrics[0]["two_order"]),36); self.assertEqual(len(s["contrasts"]),30)
        for index,want in ((0,True),(1,False)):
            rr = copy.deepcopy(self.records); rr[index]["raw"]["HOLDOUT"]["shared_suffix"]["normal"][0]=0
            self.assertEqual(b.analyze(rr,self.data,parent)[1]["candidate_gate"],want)

    def test_15_all_profiles_and_masks_remain_required(self):
        for profile in b.PROFILES:
            for view in ("query_blind","evidence_blind"):
                rr = copy.deepcopy(self.records)
                rr[1]["raw"]["HOLDOUT"][profile][view] = rr[1]["raw"]["HOLDOUT"][profile]["normal"].clone()
                self.assertFalse(b.analyze(rr,self.data,parent)[1]["candidate_gate"])

    def test_16_record_schedule_identity_and_loss_arithmetic(self):
        for key,value in (("initial_sha256","bad"),("reload_max_error",2e-9),("core_forward_calls",0)):
            rr = copy.deepcopy(self.records); rr[1][key]=value
            with self.assertRaises(ValueError): b.analyze(rr,self.data,parent)
        rr = copy.deepcopy(self.records); rr[1]["fit"]["last_total"]=2.
        with self.assertRaises(ValueError): b.analyze(rr,self.data,parent)
        rr = copy.deepcopy(self.records); rr[1]["fit"]["profile_updates"]=[800,0,0]
        with self.assertRaises(ValueError): b.analyze(rr,self.data,parent)

    def test_17_parent_valid_negative_two_argument_loader(self):
        p = dict(status="FAIL",commit_sha=b.PARENT_EXECUTION,validation_summary={"seed_pass_counts":{"doubled_only":0,"mixed_names":1}},artifacts=[dict(file=n,sha256=v) for n,v in b.PARENT_ARTIFACTS.items()])
        fake = SimpleNamespace(verify_artifacts=Mock(return_value=(p,[{}]*10)),validate_result=Mock())
        audit = SimpleNamespace(sha=lambda path:b.PARENT_SHA)
        path = Path(tempfile.gettempdir())/"c268-parent"/"summary.json"
        with patch.object(b,"context",return_value=(fake,Core,Base,None,None,Factory,audit)):
            self.assertEqual(b.load_parent(path),p)
            fake.verify_artifacts.assert_called_once_with(path.resolve().parent,b.PARENT_EXECUTION)
            p["status"]="PASS"
            with self.assertRaises(ValueError): b.load_parent(path)

    def test_18_actual_ten_model_orchestration_and_persistence(self):
        def trained(model,seed,arm,data,tokens,targets,p,core,base,factory):
            r = copy.deepcopy(self.records[b.identities().index((seed,arm))]); r["initial_sha256"]=base.fingerprint(model)
            with torch.no_grad(): model.read.weight.add_(.01)
            r.update(final_sha256=base.fingerprint(model),raw=p.evaluate(model,data,factory))
            return r,copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,Core,Base,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"train_one",side_effect=trained) as train:
            out = Path(d)/"out"
            with contextlib.redirect_stdout(io.StringIO()): payload = b.run(c267_summary=Path(d)/"p.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(train.call_count,10); self.assertEqual(pre.call_count,2)
            with patch.object(Factory,"new_model",side_effect=AssertionError("no postcheck model")),patch.object(b,"load_bundle",side_effect=AssertionError("no postcheck weights")):
                self.assertEqual(b.verify_artifacts(out,"fixture-head")[0],payload)
            with self.assertRaisesRegex(ValueError,"saved HEAD"): b.verify_artifacts(out,"bad")
            (out/"measurements.json").write_bytes(b"[]")
            with self.assertRaises(ValueError): b.verify_artifacts(out,"fixture-head")

    def test_19_bundle_identity_and_scope_guards(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"states.pt"; v = dict(schema="fold-c268-query-loss-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(v,path); self.assertEqual(len(b.load_bundle(path)),10)
            v["identities"].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        _,s = b.analyze(self.records,self.data,parent); pins,protected = protection()
        p = dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False)
        b.validate_result(p)
        with self.assertRaises(ValueError): b.validate_result(dict(p,unseen_name_transfer_claim=True))
        s["seed_pass_counts"][b.ARMS[1]]=4
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_20_semantic_suite_count_and_exact_filter(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name): super().__init__(); self.name=name
            def id(self): return self.name
        suite = unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_21_training_model_receives_no_supervision_metadata(self):
        tree = ast.parse(inspect.getsource(b.fit))
        calls = [n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="model"]
        self.assertEqual(len(calls),1); self.assertEqual(len(calls[0].args),2)
        source = ast.unparse(calls[0])
        self.assertNotIn("targets",source); self.assertIn("tokens[",source)
        self.assertIn("torch.zeros(48",source)

    def test_22_cli_parser_and_actual_call_order(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root/"tools/run_c268.ps1").read_text(encoding="utf-8")
        launcher = (root/"tools/invoke_c268.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3); indices=[]
        for text in blocks:
            compile(text,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure = re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher); self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start())
        self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        calls = [(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first = lambda name:min(line for line,n in calls if n==name)
        for a,c in (("precheck","training_tables"),("train_one","load_bundle"),("replay_one","analyze")):
            self.assertLess(first(a),first(c))

    def test_23_dependency_and_resource_contract(self):
        tree = ast.parse(inspect.getsource(b.precheck))
        pattern = next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names = ["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,268)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names)); self.assertEqual(5+len(names)+1,44)
        self.assertEqual(761+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),774)
        self.assertEqual(10*(800+27+27),b.manifest()["model_forward_calls"])
        self.assertEqual(10*(800*48+2*2592),b.manifest()["row_presentations"])

    def test_24_dispatcher_source_contract_retains_safety(self):
        # Source-contract test only; not a substitute for Windows execution/ParseFile.
        root = Path(__file__).resolve().parents[1]
        legacy = (root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode()
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),
                         "86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(legacy.replace(b"\n",b"\r\n")).hexdigest(),
                         "57a0f1ffa3a9370b5261ec5bf1e9eb3d778dc84f19f35c51e21174f61735a95b")
        source = (root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha256(source.encode()).hexdigest(),
                         "68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")
        self.assertLess(source.index("POWERSHELL_7_3_REQUIRED"),source.index("$actualBranch ="))
        self.assertIn('$PSNativeCommandArgumentPassing = "Standard"',source)
        self.assertIn('LEGACY_DISPATCHER_BLOB_MISMATCH',source)
        self.assertIn('LEGACY_DISPATCHER_BYTES_MISMATCH',source)
        launcher = (root/"tools/invoke_c268.ps1").read_text(encoding="utf-8")
        self.assertLess(launcher.index('POWERSHELL_7_3_REQUIRED'),launcher.index('$failure = $null'))
        self.assertIn('$PSNativeCommandArgumentPassing = "Standard"',launcher)
        call = source.index("& $launcher -ExpectedHead")
        for text in ("WRONG_BRANCH","DIRTY_TRACKED_TREE","ACTIVE_EXPERIMENT_UNRESOLVED","STALE_EXPECTED_HEAD","[System.Management.Automation.Language.Parser]::ParseFile"):
            self.assertLess(source.index(text),call)
        self.assertIn("$publishedMetadata.experiment_id -eq $activeExperiment",source)
        self.assertIn("$publishedMetadata.execution_head -eq $ExpectedHead",source)
        start = source.index("if ($currentHead -ne $ExpectedHead)")
        end = source.index('$launcher = Join-Path',start)
        block = source[start:end]
        self.assertIn("Report-PublishedResult",block)
        self.assertLess(block.index("Report-PublishedResult"),block.index('Skip-Invocation -Reason "STALE_EXPECTED_HEAD"'))
        self.assertIn('return',block); self.assertNotIn('publish_experiment_log.ps1',source)
        self.assertNotRegex(source,r'\$ExpectedHead\s*=\s*\$currentHead')


if __name__=="__main__":
    unittest.main(verbosity=2)
