"""C269 authoring tests. Toy backbones are implementation fixtures, not capability evidence."""
import ast
import contextlib
import copy
import hashlib
import inspect
import io
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
import torch
from torch import nn

from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c252_precore_query_alignment as aligned
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as p267
from fold_lm.v05_benchmarks import model_c269_query_span_pooling as b
from tests_lm.test_v05_c251_precore_read import Factory


class PrefixFactory:
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,"prefix length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def make_model(model,arm,seed,aligned_module,reader_module):
        b.require(arm=="aligned_precore_read","architecture")
        return aligned_module.AlignedPrecoreReadout(model,seed)
    fingerprint = staticmethod(Factory.fingerprint)


class LogitToy(nn.Module):
    def __init__(self,seed):
        super().__init__();torch.manual_seed(seed)
        self.emb=nn.Embedding(259,16,dtype=torch.float64)
        self.out=nn.Linear(16,256,dtype=torch.float64)
    def forward(self,tokens,tasks):
        return self.out(self.emb(tokens).mean(1))


def prefix(raw):
    return PrefixFactory.prefix_tensor(raw)


def perfect_raw(data):
    raw={}
    for split,rows in data.items():
        raw[split]={}
        for profile in b.PROFILES:
            raw[split][profile]={}
            for view in b.VIEWS:
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):
                    target=r["target"] if view=="normal" else 48
                    x[i,target]=10.
                raw[split][profile][view]=x
    return raw


def records(data):
    raw=perfect_raw(data);out=[]
    for seed in b.SEEDS:
        initial=str(seed)
        for arm in b.ARMS:
            plan=b.schedule(seed,data["TRAIN"])[2]
            out.append(dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,
                final_sha256="f"*64,weights_changed=True,forward_calls=827,row_presentations=40992,
                core_forward_calls=3308,replay_forward_calls=27,replay_row_presentations=2592,
                replay_core_forward_calls=108,checkpoint_roundtrip=True,reload_max_error=0.,
                fit=dict(steps=800,training_rows=38400,last_ce=.001,**plan),raw=copy.deepcopy(raw)))
    return out


class C269Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data=p267.dataset();p267.validate_data(cls.data)
        cls.tokens,cls.targets=p267.training_tables(cls.data,PrefixFactory)
        raws=[
            b"aa=0;ba=1;aa=",
            b"aa=0;ba=1;ba=",
            "甲甲=0;乙甲=1;甲甲=".encode(),
            "甲甲=0;乙甲=1;乙甲=".encode(),
        ]
        cls.span_tokens=torch.stack([prefix(x) for x in raws])
        cls.raws=raws;cls.tasks=torch.zeros(4,dtype=torch.int64)

    def test_01_manifest_identity_and_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.manifest()["acceptance_base"],b.BASE)
        self.assertEqual(b.SEEDS,(269001,269002,269003,269004,269005))
        self.assertEqual(b.ARMS,("eos_query","span_query"))

    def test_02_ascii_query_span_exact_bytes(self):
        mask=b.query_span_mask(self.span_tokens[:2])
        got=[bytes(self.span_tokens[i][mask[i]].tolist()) for i in range(2)]
        self.assertEqual(got,[b"aa",b"ba"])

    def test_03_utf8_query_span_uses_all_visible_bytes(self):
        mask=b.query_span_mask(self.span_tokens[2:])
        got=[bytes(self.span_tokens[i+2][mask[i]].tolist()) for i in range(2)]
        self.assertEqual(got,["甲甲".encode(),"乙甲".encode()])
        self.assertEqual([int(x.sum()) for x in mask],[6,6])

    def test_04_query_blind_span_is_visible_question_mark(self):
        x=prefix(b"aa=0;ba=1;?=").unsqueeze(0);mask=b.query_span_mask(x)
        self.assertEqual(bytes(x[0][mask[0]].tolist()),b"?")

    def test_05_invalid_query_boundaries_rejected(self):
        for raw in (b"aa=",b"aa=0;aa",b"aa=0;=",b"aa=0;a=b="):
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                b.query_span_mask(prefix(raw).unsqueeze(0))

    def test_06_candidate_and_control_have_exact_matched_state(self):
        control=b.make_arm_model(b.SEEDS[0],b.ARMS[0],Base,aligned,reader,Factory)
        candidate=b.make_arm_model(b.SEEDS[0],b.ARMS[1],Base,aligned,reader,Factory)
        self.assertEqual(Factory.fingerprint(control),Factory.fingerprint(candidate))
        self.assertEqual(list(control.state_dict()),list(candidate.state_dict()))
        self.assertEqual(sum(p.numel() for p in candidate.parameters()),14256)
        self.assertTrue(all(a.data_ptr()!=c.data_ptr() for a,c in zip(control.parameters(),candidate.parameters(),strict=True)))

    def test_07_candidate_query_input_is_span_mean(self):
        model=b.SpanQueryReadout(Factory.new_model(9010),9010,reader);cap={}
        h=model.backbone.local_encoder.register_forward_hook(lambda m,a,o:cap.update(local=o[0]))
        original=model.read.query.forward
        def q(x):
            cap["query"]=x.detach().clone();return original(x)
        with patch.object(model.read.query,"forward",side_effect=q):
            model(self.span_tokens,self.tasks)
        h.remove();valid=self.span_tokens!=256;local=cap["local"]*valid.unsqueeze(-1)
        mask=b.query_span_mask(self.span_tokens)
        expected=(local*mask.unsqueeze(-1)).sum(1)/mask.sum(1,keepdim=True)
        self.assertTrue(torch.equal(cap["query"],expected))
        eos=valid.sum(1)-1
        self.assertFalse(torch.equal(cap["query"],local[torch.arange(4),eos]))

    def test_08_memory_and_residual_routes_remain_actual(self):
        model=b.SpanQueryReadout(Factory.new_model(9010),9010,reader);cap={}
        h1=model.backbone.local_encoder.register_forward_hook(lambda m,a,o:cap.update(local=o[0]))
        def core(m,a,k,o):
            if k["route_index"]==0:cap["post"]=o
        h2=model.backbone.core.register_forward_hook(core,with_kwargs=True)
        h3=model.backbone.readout_norm.register_forward_pre_hook(lambda m,a:cap.update(norm=a[0]))
        model(self.span_tokens,self.tasks)
        for h in (h1,h2,h3):h.remove()
        eos=(self.span_tokens!=256).sum(1)-1
        post=cap["post"][torch.arange(4),eos]
        self.assertEqual(cap["norm"].shape,post.shape)
        self.assertFalse(torch.equal(cap["norm"],post))

    def test_09_forward_shape_finite_and_hooks_cleanup(self):
        model=b.SpanQueryReadout(Factory.new_model(9010),9010,reader)
        y=model(self.span_tokens,self.tasks)
        self.assertEqual(y.shape,(4,256));self.assertTrue(torch.isfinite(y).all())
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))
        with patch.object(model.read.output,"forward",side_effect=ValueError("fixture")),self.assertRaises(ValueError):
            model(self.span_tokens,self.tasks)
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))

    def test_10_query_key_encoder_and_core_gradients_survive(self):
        model=b.SpanQueryReadout(Factory.new_model(9010),9010,reader)
        with torch.no_grad():model.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        torch.nn.functional.cross_entropy(model(self.span_tokens,self.tasks),torch.tensor([48,49,48,49])).backward()
        params=[model.read.query.weight,model.read.key.weight,model.backbone.local_encoder.linear.weight,model.backbone.core.layers[0].weight]
        self.assertTrue(all(p.grad is not None and float(p.grad.abs().sum())>0 for p in params))

    def test_11_schedule_complete_and_equal_exposure(self):
        for seed in b.SEEDS:
            ids,profiles,plan=b.schedule(seed,self.data["TRAIN"])
            self.assertEqual(tuple(ids.shape),(800,48))
            self.assertEqual(plan["row_exposures"],[200]*192)
            self.assertEqual(plan["profile_updates"],[268,268,264])
            for epoch in range(200):
                self.assertEqual(sorted(ids[epoch*4:epoch*4+4].flatten().tolist()),list(range(192)))
            self.assertEqual(len(profiles),800)

    def test_12_schedule_rejects_old_seed_and_is_deterministic(self):
        with self.assertRaises(ValueError):b.schedule(268001,self.data["TRAIN"])
        a=b.schedule(b.SEEDS[0],self.data["TRAIN"]);c=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        self.assertTrue(torch.equal(a[0],c[0]));self.assertEqual(a[2],c[2])

    def test_13_fit_is_ce_only_and_forward_has_no_supervision_metadata(self):
        tree=ast.parse(inspect.getsource(b.fit))
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="model"]
        self.assertEqual(len(calls),1);src=ast.unparse(calls[0])
        self.assertNotIn("targets",src);self.assertNotIn("arm",src)
        self.assertEqual(sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="cross_entropy" for n in ast.walk(tree)),1)
        self.assertNotIn("pair_penalty",inspect.getsource(b.fit))

    def test_14_short_fit_changes_weights_with_same_ce_contract(self):
        model=LogitToy(7);before=copy.deepcopy(model.state_dict())
        with patch.object(b,"STEPS",4):
            result=b.fit(model,self.data,self.tokens,self.targets,b.SEEDS[0],b.ARMS[0])
        self.assertEqual(result["steps"],4);self.assertEqual(result["training_rows"],192)
        self.assertTrue(any(not torch.equal(before[k],model.state_dict()[k]) for k in before))

    def test_15_existing_gate_and_candidate_control_separation(self):
        rr=records(self.data);metrics,s=b.analyze(rr,self.data,p267)
        self.assertTrue(s["candidate_gate"]);self.assertEqual(s["seed_pass_counts"],{"eos_query":5,"span_query":5})
        self.assertEqual(len(metrics[0]["cells"]),72);self.assertEqual(len(s["contrasts"]),30)
        rr[1]["raw"]["HOLDOUT"]["shared_suffix"]["normal"][0]=0
        self.assertFalse(b.analyze(rr,self.data,p267)[1]["candidate_gate"])
        rr=records(self.data);rr[0]["raw"]["HOLDOUT"]["shared_suffix"]["normal"][0]=0
        self.assertTrue(b.analyze(rr,self.data,p267)[1]["candidate_gate"])

    def test_16_all_profiles_and_masks_still_decide(self):
        for profile in b.PROFILES:
            for view in ("query_blind","evidence_blind"):
                rr=records(self.data)
                rr[1]["raw"]["HOLDOUT"][profile][view]=rr[1]["raw"]["HOLDOUT"][profile]["normal"].clone()
                self.assertFalse(b.analyze(rr,self.data,p267)[1]["candidate_gate"])

    def test_17_record_workload_schedule_and_replay_guard(self):
        for key,value in (("reload_max_error",2e-9),("core_forward_calls",0),("checkpoint_roundtrip",False)):
            rr=records(self.data);rr[1][key]=value
            with self.assertRaises(ValueError):b.analyze(rr,self.data,p267)
        rr=records(self.data);rr[1]["fit"]["profile_updates"]=[800,0,0]
        with self.assertRaises(ValueError):b.analyze(rr,self.data,p267)

    def test_18_result_validation_protection_and_scope(self):
        _,s=b.analyze(records(self.data),self.data,p267)
        pins={f"old-{i}":"fixture" for i in range(454)};pins.update({x:"fixture" for x in b.OWN})
        protected={f"input-{i}":"0"*64 for i in range(787)}
        payload=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",
            source_blobs=pins,input_sha256=protected,artifacts=[dict(file=x) for x in b.OUTPUTS],
            validation_summary=s,gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False)
        b.validate_result(payload)
        with self.assertRaises(ValueError):b.validate_result(dict(payload,causal_parser_claim=True))

    def test_19_parent_loader_requires_exact_c268_valid_negative(self):
        p=dict(status="FAIL",commit_sha=b.PARENT_EXECUTION,
            validation_summary={"seed_pass_counts":{"ce_only":3,"ce_pair_margin":3},"candidate_gate":False},
            artifacts=[dict(file=n,sha256=v) for n,v in b.PARENT_ARTIFACTS.items()])
        fake=SimpleNamespace(verify_artifacts=Mock(return_value=(p,[{}]*10)),validate_result=Mock())
        audit=SimpleNamespace(sha=lambda path:b.PARENT_SHA)
        with patch.object(b,"context",return_value=(fake,None,None,None,None,None,None,audit)):
            self.assertEqual(b.load_parent(Path("parent.json")),p)
            fake.verify_artifacts.assert_called_once()
            p["validation_summary"]["candidate_gate"]=True
            with self.assertRaises(ValueError):b.load_parent(Path("parent.json"))

    def test_20_bundle_identity(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"states.pt";v=dict(schema="fold-c269-query-span-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(v,path);self.assertEqual(len(b.load_bundle(path)),10)
            v["identities"].reverse();torch.save(v,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    def test_21_semantic_suite_count_and_exact_filter(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),24)
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        suite=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_22_dependency_and_resource_contract(self):
        tree=ast.parse(inspect.getsource(b.precheck))
        pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,269)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names))
        self.assertEqual(5+len(names)+1,45)
        self.assertEqual(774+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),787)
        self.assertEqual(10*(800+27+27),b.manifest()["model_forward_calls"])

    def test_23_runner_cli_and_call_order_contract(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c269.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c269.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        indices=[]
        for text in blocks:
            compile(text,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher);self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start());self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(line for line,n in calls if n==name)
        for a,c in (("precheck","training_tables"),("make_arm_model","train_one"),("train_one","load_bundle"),("replay_one","analyze")):
            self.assertLess(first(a),first(c))

    def test_24_dispatcher_and_historical_pin_contract(self):
        root=Path(__file__).resolve().parents[1]
        legacy=(root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode()
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),"86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(legacy.replace(b"\n",b"\r\n")).hexdigest(),"57a0f1ffa3a9370b5261ec5bf1e9eb3d778dc84f19f35c51e21174f61735a95b")
        active=(root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha256(active.encode()).hexdigest(),"68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")
        launcher=(root/"tools/invoke_c269.ps1").read_text(encoding="utf-8")
        self.assertLess(launcher.index("POWERSHELL_7_3_REQUIRED"),launcher.index("$failure = $null"))
        self.assertIn('$PSNativeCommandArgumentPassing = "Standard"',launcher)
        self.assertNotIn("publish_experiment_log.ps1",active)
        self.assertNotRegex(active,r"\$ExpectedHead\s*=\s*\$currentHead")


if __name__=="__main__":
    unittest.main(verbosity=2)
