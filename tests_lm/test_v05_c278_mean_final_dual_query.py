"""C278 authoring tests for mean-span plus final-boundary dual attention."""
import ast,copy,hashlib,inspect,re,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as p267
from fold_lm.v05_benchmarks import model_c269_query_span_pooling as c269
from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as c270
from fold_lm.v05_benchmarks import model_c278_mean_final_dual_query as b
from tests_lm.test_v05_c251_precore_read import Factory as ToyFactory

class Factory:
    LM_SOURCES=()
    @staticmethod
    def new_model(seed):return ToyFactory.new_model(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.req(len(raw)<=46,"prefix")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)

class Base:
    fingerprint=staticmethod(ToyFactory.fingerprint)

def perfect(data,profiles):
    raw={}
    for split,rows in data.items():
        raw[split]={}
        for profile in profiles:
            raw[split][profile]={}
            for view in ("normal","evidence_blind","query_blind"):
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):x[i,r["target"] if view=="normal" else 255]=10.
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
    pins={f"old-{i}":"fixture" for i in range(508)};pins.update({x:"fixture" for x in b.OWN})
    return pins,{f"input-{i}":"0"*64 for i in range(902)}

class C278Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data=p267.dataset();p267.validate_data(cls.data)
        cls.prompts=c270.prompt_dataset(cls.data,p267);c270.validate_dataset(cls.prompts,cls.data,p267)
        cls.examples=torch.stack([
            Factory.prefix_tensor(b"aa=0;ba=1;ba="),
            Factory.prefix_tensor("甲甲=0;乙甲=1;乙甲=".encode()),
        ])
        cls.tasks=torch.zeros(2,dtype=torch.int64)

    def test_01_manifest_is_final_and_matches_digest(self):
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL")
        self.assertRegex(b.MANIFEST_SHA,r"^[0-9a-f]{64}$")
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_arms_match_initial_state_and_capacity(self):
        a=b.make_arm(b.SEEDS[0],"mean_span",c269,Base,reader,Factory)
        z=b.make_arm(b.SEEDS[0],"mean_final_dual",c269,Base,reader,Factory)
        self.assertEqual(Base.fingerprint(a),Base.fingerprint(z));self.assertEqual(list(a.state_dict()),list(z.state_dict()))
        self.assertEqual(sum(p.numel() for p in a.parameters()),14256)
        self.assertTrue(all(x.data_ptr()!=y.data_ptr() for x,y in zip(a.parameters(),z.parameters(),strict=True)))

    def test_03_candidate_query_calls_are_mean_then_final(self):
        m=b.make_arm(b.SEEDS[0],"mean_final_dual",c269,Base,reader,Factory)
        calls=[];orig=m.read.query.forward
        with patch.object(m.read.query,"forward",side_effect=lambda x:(calls.append(x.detach().clone()) or orig(x))):
            m(self.examples,self.tasks)
        self.assertEqual(len(calls),2)
        self.assertEqual(tuple(calls[0].shape),(2,16));self.assertEqual(tuple(calls[1].shape),(2,16))
        self.assertFalse(torch.equal(calls[0],calls[1]))

    def test_04_one_byte_query_matches_mean_span_exactly(self):
        x=torch.stack([Factory.prefix_tensor(b"aa=0;ba=1;?="),Factory.prefix_tensor("甲甲=0;乙甲=1;?=".encode())])
        a=b.make_arm(b.SEEDS[0],"mean_span",c269,Base,reader,Factory)
        z=b.make_arm(b.SEEDS[0],"mean_final_dual",c269,Base,reader,Factory)
        self.assertTrue(torch.equal(a(x,self.tasks),z(x,self.tasks)))

    def test_05_candidate_has_two_softmaxes_and_one_output(self):
        src=inspect.getsource(b.MeanFinalDualReadout.forward)
        self.assertEqual(src.count(".softmax(-1)"),2)
        self.assertEqual(src.count("self.read.output(memory)"),1)
        self.assertIn("(memory_mean+memory_final)*.5",src)

    def test_06_forward_has_no_supervision_metadata(self):
        src=inspect.getsource(b.MeanFinalDualReadout.forward)
        for word in ("target","entity","profile","split","pair"):self.assertNotIn(word,src)
        self.assertIn("_span_mask(tokens)",src);self.assertIn("[rows,final]",src)

    def test_07_gradient_flow_reaches_query_key_encoder_and_core(self):
        m=b.make_arm(b.SEEDS[0],"mean_final_dual",c269,Base,reader,Factory)
        with torch.no_grad():m.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        nn.functional.cross_entropy(m(self.examples,self.tasks),torch.tensor([49,49])).backward()
        ps=[m.read.query.weight,m.read.key.weight,m.backbone.local_encoder.linear.weight,m.backbone.core.layers[0].weight]
        self.assertTrue(all(p.grad is not None and float(p.grad.abs().sum())>0 for p in ps))

    def test_08_schedule_complete_equal_exposure(self):
        for seed in b.SEEDS:
            ids,profiles,plan=b.schedule(seed,self.data["TRAIN"])
            self.assertEqual(tuple(ids.shape),(800,48));self.assertEqual(plan["row_exposures"],[200]*192)
            self.assertEqual(plan["profile_updates"],[268,268,264]);self.assertEqual(len(profiles),800)

    def test_09_schedule_is_fresh_and_deterministic(self):
        a=b.schedule(b.SEEDS[0],self.data["TRAIN"]);z=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        self.assertTrue(torch.equal(a[0],z[0]));self.assertEqual(a[2],z[2])
        with self.assertRaises(ValueError):b.schedule(276001,self.data["TRAIN"])

    def test_10_fit_is_ce_only_and_lr_fixed(self):
        src=inspect.getsource(b.fit);tree=ast.parse(src)
        self.assertIn("lr=.005",src);self.assertNotIn("scheduler",src.lower())
        self.assertEqual(sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="cross_entropy" for n in ast.walk(tree)),1)
        self.assertIn("for step in range(800)",src);self.assertNotIn("break",src)

    def test_11_both_tasks_decide_candidate(self):
        m,s=b.analyze(records(self.data),self.data,self.prompts,p267,c270)
        self.assertTrue(s["candidate_gate"]);self.assertEqual(s["seed_pass_counts"],{"mean_span":5,"mean_final_dual":5})
        self.assertEqual(s["two_char_pass_counts"],{"mean_span":5,"mean_final_dual":5})
        self.assertEqual(s["triple_pass_counts"],{"mean_span":5,"mean_final_dual":5})
        self.assertEqual(len(s["contrasts"]),90);self.assertEqual(len(m),10)

    def test_12_control_failure_does_not_fail_candidate(self):
        rr=records(self.data);rr[0]["raw_triple"]["HOLDOUT"]["shared_suffix2"]["normal"][0]=0
        self.assertTrue(b.analyze(rr,self.data,self.prompts,p267,c270)[1]["candidate_gate"])

    def test_13_candidate_failure_fails_gate(self):
        rr=records(self.data);rr[1]["raw_triple"]["HOLDOUT"]["shared_suffix2"]["normal"][0]=0
        self.assertFalse(b.analyze(rr,self.data,self.prompts,p267,c270)[1]["candidate_gate"])

    def test_14_record_integrity_guards(self):
        for k,v in (("checkpoint_roundtrip",False),("reload_max_error",2e-9),("core_forward_calls",0)):
            rr=records(self.data);rr[1][k]=v
            with self.assertRaises(ValueError):b.analyze(rr,self.data,self.prompts,p267,c270)

    def test_15_matched_initial_and_batch_pair_required(self):
        rr=records(self.data);rr[1]["initial_sha256"]="different"
        with self.assertRaises(ValueError):b.analyze(rr,self.data,self.prompts,p267,c270)
        rr=records(self.data);rr[1]["fit"]["batch_sha256"]="different"
        with self.assertRaises(ValueError):b.analyze(rr,self.data,self.prompts,p267,c270)

    def test_16_parent_loader_models_four_hashes_independently(self):
        payload=dict(status="PASS",commit_sha=b.PARENT_EXECUTION,
            validation_summary={"diagnostic_complete":True,"capability_gate_applicable":False,"model_forward_calls":0,
                "triple_criterion_delta":{"accuracy":-37,"evidence_drop":3,"query_drop":1,"query_pair_accuracy":-37,"two_order_accuracy":-18},
                "shared_suffix2_holdout_delta":{"accuracy":-7,"evidence_drop":4,"query_drop":5,"query_pair_accuracy":-7,"two_order_accuracy":-5}},
            artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        profile={"primary":{"recovery_seed276003":{"candidate_minus_control":{"accuracy":-72}},
                            "stable_seeds":{"candidate_minus_control":{"evidence_drop":12}}}}
        fake=SimpleNamespace(verify_artifacts=Mock(return_value=(payload,profile)),validate_result=Mock())
        sha=Mock(side_effect=lambda path:{"p":b.PARENT_SHA,"q":b.C276_SHA,"r":b.C275_SHA,"s":b.C274_SHA}.get(Path(path).name,"unexpected"))
        audit=SimpleNamespace(sha=sha)
        with patch.object(b,"context",return_value=(fake,None,None,None,None,None,None,None,None,audit)):
            got=b.load_parent(Path("p"),Path("q"),Path("r"),Path("s"));self.assertEqual(got,payload)
            self.assertEqual([Path(x.args[0]).name for x in sha.call_args_list[:4]],["p","q","r","s"])
            sha.reset_mock();sha.side_effect=lambda path:b.PARENT_SHA
            with self.assertRaisesRegex(ValueError,"parent hash"):b.load_parent(Path("p"),Path("q"),Path("r"),Path("s"))

    def test_17_result_validation_and_scope(self):
        _,s=b.analyze(records(self.data),self.data,self.prompts,p267,c270);pins,inputs=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",
            source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
            gate_f_candidate=False,production_adoption=False,arbitrary_name_claim=False,causal_parser_claim=False)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,gate_f_candidate=True))

    def test_18_bundle_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.pt";v=dict(schema="fold-c278-mean-final-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),10)
            v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_19_candidate_uses_shared_query_key_output_parameters(self):
        m=b.make_arm(b.SEEDS[0],"mean_final_dual",c269,Base,reader,Factory)
        names=list(m.state_dict())
        self.assertEqual(sum("read.query" in x for x in names),1)
        self.assertEqual(sum("read.key" in x for x in names),1)
        self.assertEqual(sum("read.output" in x for x in names),1)

    def test_20_semantic_suite_count_and_exact_filter(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),24)
        class D(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def id(self):return self.n
        suite=unittest.TestSuite([D(b.EXCLUDED)]+[D(f"x{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3837)

    def test_21_dependency_resource_and_registration(self):
        tree=ast.parse(inspect.getsource(b.precheck))
        pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,278)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names));self.assertEqual(5+len(names)+1,54)
        self.assertEqual(892+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),902)
        self.assertEqual((b.manifest()["source_pins"],b.manifest()["protected_inputs"]),(514,902))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.validate_result))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.precheck))

    def test_22_runner_validate_execute_and_cli_contract(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c278.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c278.ps1").read_text(encoding="utf-8")
        self.assertIn('[ValidateSet("Validate","Execute")]',runner);self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("$failure = $null"));self.assertGreater(launcher.index("-Mode Execute"),launcher.index("$failure = $null"))
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        sets=[]
        for x in blocks:compile(x,"embedded","exec");sets.append({int(m.group(1)) for m in re.finditer(r"sys\.argv\[(\d+)\]",x)})
        self.assertEqual(sets,[{1,2,3,4},set(),{1,2,3,4,5,6}])

    def test_23_run_phase_order_uses_unique_markers(self):
        src=inspect.getsource(b.run)
        phases=("pins,protected=precheck(c277_summary,c276_summary,c275_summary,c274_summary,root)",
                "data=p267.dataset()","out=Path(output_dir)","train_one(models[arm]",
                "loaded=load_bundle(out/\"trained-models.pt\")","metrics,summary=analyze(records,data,prompts,p267,c270)")
        pos=[]
        for p in phases:self.assertEqual(src.count(p),1,p);pos.append(src.index(p))
        self.assertEqual(pos,sorted(pos));self.assertEqual(len({src[:p].count("\n") for p in pos}),len(pos))

    def test_24_manifest_lifecycle_and_legacy_compatibility(self):
        root=Path(__file__).resolve().parents[1];prereg=(root/"docs/experiment-ledger-addendum-c278-preregistration.md").read_text(encoding="utf-8");handoff=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL");self.assertIn(b.MANIFEST_SHA,prereg)
        formal=re.search(r"(?ms)^## Formal state\s+(?P<body>.*?)(?=^## |\Z)",handoff);self.assertIsNotNone(formal)
        if re.search(r"\bC278 ACTIVE /",formal.group("body")):self.assertIn(b.MANIFEST_SHA,handoff)
        else:
            accepted=root/"docs/experiment-ledger-addendum-c278-c279.md";self.assertTrue(accepted.is_file());self.assertIn(b.MANIFEST_SHA,accepted.read_text(encoding="utf-8"))
        self.assertIn("89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604",handoff)
        legacy=(root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode();active=(root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),"86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(active.encode()).hexdigest(),"68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")

if __name__=="__main__":unittest.main(verbosity=2)
