"""C272 authoring tests; toy models are implementation fixtures, not learned-capability evidence."""
import ast,copy,hashlib,inspect,itertools,re,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as p267
from fold_lm.v05_benchmarks import model_c269_query_span_pooling as c269
from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as c270
from fold_lm.v05_benchmarks import model_c272_query_boundaries as b
from tests_lm.test_v05_c251_precore_read import Factory as ToyFactory

class Factory:
    LM_SOURCES=()
    @staticmethod
    def new_model(seed): return ToyFactory.new_model(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.req(len(raw)<=46,"prefix")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)

class Base:
    fingerprint=staticmethod(ToyFactory.fingerprint)

class CoreCounter:
    @staticmethod
    def core_counter(model):
        calls=[0]
        def h(m,a,k,o): calls[0]+=1
        return calls,model.backbone.core.register_forward_hook(h,with_kwargs=True)

def perfect(data,profiles):
    raw={}
    for split,rows in data.items():
        raw[split]={}
        for profile in profiles:
            raw[split][profile]={}
            for view in ("normal","evidence_blind","query_blind"):
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows): x[i,r["target"] if view=="normal" else 255]=10.
                raw[split][profile][view]=x
    return raw

def records(data):
    two=perfect(data,p267.PROFILES);tri=perfect(data,c270.PROFILES);out=[]
    for seed in b.SEEDS:
        plan=b.schedule(seed,data["TRAIN"])[2]
        for arm in b.ARMS:
            out.append(dict(seed=seed,arm=arm,parameters=14256,initial_sha256=str(seed),final_sha256="f"*64,
                weights_changed=True,forward_calls=854,row_presentations=43584,core_forward_calls=3416,
                replay_forward_calls=54,replay_row_presentations=5184,replay_core_forward_calls=216,
                checkpoint_roundtrip=True,reload_max_error=0.,
                fit=dict(steps=800,training_rows=38400,last_ce=.001,**plan),
                raw_two=copy.deepcopy(two),raw_triple=copy.deepcopy(tri)))
    return out

def protection():
    pins={f"old-{i}":"fixture" for i in range(472)}
    pins.update({x:"fixture" for x in b.OWN})
    return pins,{f"input-{i}":"0"*64 for i in range(826)}

class C272Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data=p267.dataset();p267.validate_data(cls.data)
        cls.prompts=c270.prompt_dataset(cls.data,p267);c270.validate_dataset(cls.prompts,cls.data,p267)
        cls.tokens,cls.targets=p267.training_tables(cls.data,Factory)
        cls.raws=[b"aaa=0;baa=1;baa=","甲甲甲=0;乙甲甲=1;乙甲甲=".encode()]
        cls.examples=torch.stack([Factory.prefix_tensor(x) for x in cls.raws])
        cls.tasks=torch.zeros(2,dtype=torch.int64)

    def test_01_manifest_is_final_and_matches_digest(self):
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL")
        self.assertRegex(b.MANIFEST_SHA,r"^[0-9a-f]{64}$")
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_mean_and_boundary_initial_states_match(self):
        m=b.make_arm(b.SEEDS[0],"mean_span",c269,Base,reader,Factory)
        q=b.make_arm(b.SEEDS[0],"boundary_pair",c269,Base,reader,Factory)
        self.assertEqual(Base.fingerprint(m),Base.fingerprint(q))
        self.assertEqual(list(m.state_dict()),list(q.state_dict()))
        self.assertEqual(sum(p.numel() for p in q.parameters()),14256)
        self.assertTrue(all(a.data_ptr()!=z.data_ptr() for a,z in zip(m.parameters(),q.parameters(),strict=True)))

    def test_03_boundary_query_is_first_last_state_mean(self):
        m=b.BoundaryPairReadout(ToyFactory.new_model(9010),9010,reader,c269.query_span_mask);cap={}
        h=m.backbone.local_encoder.register_forward_hook(lambda mod,a,o:cap.update(local=o[0]))
        orig=m.read.query.forward
        with patch.object(m.read.query,"forward",side_effect=lambda x:(cap.update(query=x.detach().clone()) or orig(x))):
            m(self.examples,self.tasks)
        h.remove()
        span=c269.query_span_mask(self.examples);pos=torch.arange(48).expand(2,-1)
        first=torch.where(span,pos,torch.full_like(pos,48)).min(1).values
        last=torch.where(span,pos,torch.full_like(pos,-1)).max(1).values
        local=cap["local"]*(self.examples!=256).unsqueeze(-1)
        expected=(local[torch.arange(2),first]+local[torch.arange(2),last])*.5
        self.assertTrue(torch.equal(cap["query"],expected))

    def test_04_ascii_and_utf8_boundaries_use_visible_bytes(self):
        span=c269.query_span_mask(self.examples);pos=torch.arange(48).expand(2,-1)
        first=torch.where(span,pos,torch.full_like(pos,48)).min(1).values
        last=torch.where(span,pos,torch.full_like(pos,-1)).max(1).values
        self.assertEqual(bytes(self.examples[0][span[0]].tolist()),b"baa")
        self.assertEqual(bytes(self.examples[1][span[1]].tolist()),"乙甲甲".encode())
        self.assertEqual((self.examples[0,first[0]].item(),self.examples[0,last[0]].item()),(ord("b"),ord("a")))
        j="乙甲甲".encode()
        self.assertEqual((self.examples[1,first[1]].item(),self.examples[1,last[1]].item()),(j[0],j[-1]))

    def test_05_one_byte_query_blind_does_not_double_change_state(self):
        x=Factory.prefix_tensor(b"aaa=0;baa=1;?=").unsqueeze(0)
        span=c269.query_span_mask(x);pos=torch.arange(48).expand(1,-1)
        first=torch.where(span,pos,torch.full_like(pos,48)).min(1).values
        last=torch.where(span,pos,torch.full_like(pos,-1)).max(1).values
        self.assertEqual(first.item(),last.item())
        self.assertEqual(bytes(x[0][span[0]].tolist()),b"?")

    def test_06_boundary_and_full_mean_query_sources_are_distinct(self):
        mean=c269.SpanQueryReadout(ToyFactory.new_model(9010),9010,reader)
        boundary=b.BoundaryPairReadout(ToyFactory.new_model(9010),9010,reader,c269.query_span_mask)
        values=[]
        for model in (mean,boundary):
            cap={};orig=model.read.query.forward
            with patch.object(model.read.query,"forward",side_effect=lambda x,cap=cap,orig=orig:(cap.update(q=x.detach().clone()) or orig(x))):
                model(self.examples,self.tasks)
            values.append(cap["q"])
        self.assertFalse(torch.equal(values[0],values[1]))

    def test_07_gradient_flow_reaches_query_key_encoder_and_core(self):
        m=b.BoundaryPairReadout(ToyFactory.new_model(9010),9010,reader,c269.query_span_mask)
        with torch.no_grad():m.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        nn.functional.cross_entropy(m(self.examples,self.tasks),torch.tensor([49,49])).backward()
        ps=[m.read.query.weight,m.read.key.weight,m.backbone.local_encoder.linear.weight,m.backbone.core.layers[0].weight]
        self.assertTrue(all(p.grad is not None and float(p.grad.abs().sum())>0 for p in ps))

    def test_08_schedule_complete_equal_exposure(self):
        for seed in b.SEEDS:
            ids,profiles,plan=b.schedule(seed,self.data["TRAIN"])
            self.assertEqual(tuple(ids.shape),(800,48))
            self.assertEqual(plan["row_exposures"],[200]*192)
            self.assertEqual(plan["profile_updates"],[268,268,264])
            self.assertEqual(len(profiles),800)

    def test_09_schedule_is_fresh_and_deterministic(self):
        a=b.schedule(b.SEEDS[0],self.data["TRAIN"]);z=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        self.assertTrue(torch.equal(a[0],z[0]));self.assertEqual(a[2],z[2])
        with self.assertRaises(ValueError):b.schedule(271001,self.data["TRAIN"])

    def test_10_fit_is_ce_only_and_forward_gets_no_supervision_metadata(self):
        tree=ast.parse(inspect.getsource(b.fit))
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="model"]
        self.assertEqual(len(calls),1)
        call=ast.unparse(calls[0]);self.assertNotIn("targets",call);self.assertNotIn("arm",call)
        self.assertEqual(sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="cross_entropy" for n in ast.walk(tree)),1)

    def test_11_both_original_and_triple_tasks_decide(self):
        m,s=b.analyze(records(self.data),self.data,self.prompts,p267,c270)
        self.assertTrue(s["candidate_gate"]);self.assertEqual(s["seed_pass_counts"],{"mean_span":5,"boundary_pair":5})
        self.assertEqual(len(s["contrasts"]),90);self.assertEqual(len(m[0]["two_char"]["cells"]),72);self.assertEqual(len(m[0]["triple"]["cells"]),72)

    def test_12_control_failure_does_not_fail_candidate(self):
        rr=records(self.data);rr[0]["raw_triple"]["HOLDOUT"]["shared_prefix2"]["normal"][0]=0
        self.assertTrue(b.analyze(rr,self.data,self.prompts,p267,c270)[1]["candidate_gate"])

    def test_13_candidate_two_char_failure_fails_gate(self):
        rr=records(self.data);rr[1]["raw_two"]["HOLDOUT"]["shared_prefix"]["normal"][0]=0
        self.assertFalse(b.analyze(rr,self.data,self.prompts,p267,c270)[1]["candidate_gate"])

    def test_14_candidate_triple_failure_fails_gate(self):
        rr=records(self.data);rr[1]["raw_triple"]["HOLDOUT"]["shared_suffix2"]["normal"][0]=0
        self.assertFalse(b.analyze(rr,self.data,self.prompts,p267,c270)[1]["candidate_gate"])

    def test_15_record_integrity_guards(self):
        for k,v in (("checkpoint_roundtrip",False),("reload_max_error",2e-9),("core_forward_calls",0)):
            rr=records(self.data);rr[1][k]=v
            with self.assertRaises(ValueError):b.analyze(rr,self.data,self.prompts,p267,c270)
        rr=records(self.data);rr[1]["fit"]["profile_updates"]=[800,0,0]
        with self.assertRaises(ValueError):b.analyze(rr,self.data,self.prompts,p267,c270)

    def test_16_parent_loader_requires_exact_c271_negative(self):
        payload=dict(status="FAIL",commit_sha=b.PARENT_EXECUTION,
            validation_summary={"seed_pass_counts":{"endpoint_span":0,"mean_span":0},
                                "two_char_pass_counts":{"endpoint_span":4,"mean_span":4},
                                "triple_pass_counts":{"endpoint_span":0,"mean_span":0},
                                "candidate_gate":False},
            artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        fake=SimpleNamespace(verify_artifacts=Mock(return_value=(payload,[{}]*10)),validate_result=Mock())
        audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA)
        with patch.object(b,"context",return_value=(fake,None,None,None,None,None,None,None,None,audit)):
            self.assertEqual(b.load_parent(Path("parent.json")),payload)
            fake.verify_artifacts.assert_called_once()
            payload["status"]="PASS"
            with self.assertRaises(ValueError):b.load_parent(Path("parent.json"))

    def test_17_result_validation_and_scope(self):
        _,s=b.analyze(records(self.data),self.data,self.prompts,p267,c270);pins,inputs=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",
            source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
            gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,
            arbitrary_name_claim=False,causal_parser_claim=False)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,causal_parser_claim=True))

    def test_18_bundle_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.pt";v=dict(schema="fold-c272-query-boundaries-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),10)
            v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_19_boundary_forward_has_no_supervision_metadata_or_parameters(self):
        src=inspect.getsource(b.BoundaryPairReadout.forward)
        self.assertNotIn("target",src);self.assertNotIn("entity",src);self.assertNotIn("profile",src)
        self.assertIn("_span_mask(tokens)",src);self.assertIn("[rows,first]",src);self.assertIn("[rows,last]",src)

    def test_20_semantic_suite_count_and_exact_filter(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),24)
        class D(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def id(self):return self.n
        suite=unittest.TestSuite([D(b.EXCLUDED)]+[D(f"x{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3693)

    def test_21_dependency_and_resource_contract(self):
        tree=ast.parse(inspect.getsource(b.precheck))
        pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,272)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names));self.assertEqual(5+len(names)+1,48)
        self.assertEqual(812+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),826)
        self.assertEqual((b.manifest()["source_pins"],b.manifest()["protected_inputs"]),(478,826))
        self.assertNotIn("(478,820)",inspect.getsource(b.validate_result))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.validate_result))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.precheck))
        self.assertEqual(10*(854+54),b.manifest()["model_forward_calls"])

    def test_22_runner_validate_execute_and_cli_contract(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c272.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c272.ps1").read_text(encoding="utf-8")
        self.assertIn('[ValidateSet("Validate","Execute")]',runner)
        self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("$failure = $null"))
        self.assertGreater(launcher.index("-Mode Execute"),launcher.index("$failure = $null"))
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        sets=[]
        for x in blocks:
            compile(x,"embedded","exec");sets.append({int(m.group(1)) for m in re.finditer(r"sys\.argv\[(\d+)\]",x)})
        self.assertEqual(sets,[{1},set(),{1,2,3}])

    def test_23_scientific_run_phase_order_uses_unique_markers(self):
        src=inspect.getsource(b.run)
        phases=("pins,protected=precheck(c271_summary,root)","data=p267.dataset()","out=Path(output_dir)",
                "train_one(models[arm]","loaded=load_bundle(out/\"trained-models.pt\")",
                "metrics,summary=analyze(records,data,prompts,p267,c270)")
        pos=[]
        for p in phases:self.assertEqual(src.count(p),1,p);pos.append(src.index(p))
        self.assertEqual(pos,sorted(pos));self.assertEqual(len({src[:p].count("\n") for p in pos}),len(pos))

    def test_24_manifest_seal_and_dispatcher_pins(self):
        root=Path(__file__).resolve().parents[1]
        prereg=(root/"docs/experiment-ledger-addendum-c272-preregistration.md").read_text(encoding="utf-8")
        handoff=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL")
        self.assertIn(b.MANIFEST_SHA,prereg);self.assertIn(b.MANIFEST_SHA,handoff)
        legacy=(root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode()
        active=(root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),"86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(active.encode()).hexdigest(),"68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")
        self.assertIn("RESULT_ALREADY_PUBLISHED",active);self.assertNotRegex(active,r"\$ExpectedHead\s*=\s*\$currentHead")

if __name__=="__main__":unittest.main(verbosity=2)
