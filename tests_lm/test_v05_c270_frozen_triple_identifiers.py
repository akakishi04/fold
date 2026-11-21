"""C270 authoring tests. Toy backbones and synthetic logits are not learned-capability evidence."""
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

from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c252_precore_query_alignment as aligned
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as p267
from fold_lm.v05_benchmarks import model_c269_query_span_pooling as c269
from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as b
from tests_lm.test_v05_c251_precore_read import Factory as ToyFactory


class Factory:
    LM_SOURCES=()
    @staticmethod
    def new_model(seed): return ToyFactory.new_model(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,"prefix length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def make_model(model,arm,seed,aligned_module,reader_module):
        b.require(arm=="aligned_precore_read","architecture")
        return aligned_module.AlignedPrecoreReadout(model,seed)
    fingerprint=staticmethod(ToyFactory.fingerprint)


class CoreCounter:
    @staticmethod
    def core_counter(model):
        calls=[0]
        def hook(module,args,kwargs,output): calls[0]+=1
        return calls,model.backbone.core.register_forward_hook(hook,with_kwargs=True)


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):
        import json
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        child=(Path(root)/name).resolve();b.require(child.parent==Path(root).resolve(),"unsafe child");return child
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"):return b"fixture-head"
        if args==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def perfect_raw(data):
    raw={}
    for split,rows in data.items():
        raw[split]={}
        for profile in b.PROFILES:
            raw[split][profile]={}
            for view in b.VIEWS:
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):
                    x[i,r["target"] if view=="normal" else 255]=10.
                raw[split][profile][view]=x
    return raw


def protection():
    return {**{f"old-{i}":"fixture" for i in range(460)},**{n:"fixture" for n in b.OWN}},{f"input-{i}":"0"*64 for i in range(800)}


class C270Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data=p267.dataset();p267.validate_data(cls.data)
        cls.prompts=b.prompt_dataset(cls.data,p267);b.validate_dataset(cls.prompts,cls.data,p267)
        cls.models=[];cls.refs=[]
        for seed,arm in b.identities():
            m=c269.make_arm_model(seed,arm,Base,aligned,reader,Factory);m.eval().requires_grad_(False)
            raw=p267.evaluate(m,cls.data,Factory)
            cls.models.append(m);cls.refs.append(dict(seed=seed,arm=arm,final_sha256=Base.fingerprint(m),raw=raw))
        novel=perfect_raw(cls.data)
        cls.records=[dict(seed=r["seed"],arm=r["arm"],final_sha256=r["final_sha256"],weights_preserved=True,
            model_forward_calls=81,row_presentations=7776,core_forward_calls=324,anchor_error=0.,restore_error=0.,
            anchor=r["raw"],novel=copy.deepcopy(novel),restored=r["raw"]) for r in cls.refs]

    def test_01_manifest_and_dataset_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.prompts),b.DATA_SHA)
        self.assertEqual(b.identities(),list(__import__("itertools").product(b.SEEDS,b.ARMS)))

    def test_02_profile_maps_are_three_characters_and_distinct(self):
        for split,rows in self.data.items():
            for r in rows:
                for profile in b.PROFILES:
                    names=b.name_map(r,profile);self.assertEqual({len(x) for x in names.values()},{3})
                    self.assertEqual(len(set(names.values())),2)

    def test_03_three_character_names_are_unseen_in_c269_training_profiles(self):
        old=set();new=set()
        for r in self.data["TRAIN"]:
            for p in p267.PROFILES:
                chars=("a","b","c") if r["language"]=="en" else ("甲","乙","丙")
                i,j=r["entities"];u,v=chars[i],chars[j]
                old.update((u+u,v+v if p=="doubled" else u+v if p=="shared_prefix" else v+u))
            for p in b.PROFILES:new.update(b.name_map(r,p).values())
        self.assertTrue(old.isdisjoint(new))

    def test_04_prompt_dataset_complete_unique_and_within_limit(self):
        for split in b.SPLITS:
            for profile in b.PROFILES:
                items=self.prompts[split][profile]
                self.assertEqual(len(items),len(self.data[split]))
                self.assertEqual(len({x["views"]["normal"] for x in items}),len(items))
                self.assertLessEqual(max(len(x["views"]["normal"].encode()) for x in items),34)

    def test_05_ascii_and_utf8_examples(self):
        en=next(r for r in self.data["TRAIN"] if r["language"]=="en" and r["entities"]==[0,1] and r["permutation"]==[0,1] and r["query"]==1)
        ja=next(r for r in self.data["TRAIN"] if r["language"]=="ja" and r["entities"]==[0,1] and r["permutation"]==[0,1] and r["query"]==1)
        self.assertIn("aaa=",b.render(en,"shared_prefix2"))
        self.assertIn("aab=",b.render(en,"shared_prefix2"))
        self.assertIn("甲甲甲=",b.render(ja,"shared_suffix2"))
        self.assertIn("乙甲甲=",b.render(ja,"shared_suffix2"))

    def test_06_mask_rendering_keeps_name_semantics(self):
        r=self.data["TRAIN"][0]
        for p in b.PROFILES:
            self.assertEqual(b.render(r,p,"evidence_blind").count("?"),2)
            self.assertTrue(b.render(r,p,"query_blind").endswith(";?="))

    def test_07_corrupt_prompt_dataset_rejected(self):
        bad=copy.deepcopy(self.prompts);bad["TRAIN"]["tripled"][0]["target"]=200
        with self.assertRaises(ValueError):b.validate_dataset(bad,self.data,p267)

    def test_08_perfect_scoring_passes_all_cells(self):
        m=b.score(self.data,perfect_raw(self.data),p267)
        self.assertTrue(m["passed"]);self.assertEqual(len(m["cells"]),72);self.assertEqual(len(m["two_order"]),36)
        self.assertEqual(len(m["totals"]),12)
        self.assertTrue(all(x["collapsed_pairs"]==0 for x in m["totals"]))

    def test_09_weak_cell_cannot_be_pooled_away(self):
        raw=perfect_raw(self.data)
        ids=[i for i,r in enumerate(self.data["HOLDOUT"]) if r["language"]=="en" and r["entities"]==[0,1] and r["permutation"]==[0,1]][:1]
        raw["HOLDOUT"]["shared_suffix2"]["normal"][ids]=0
        self.assertFalse(b.score(self.data,raw,p267)["passed"])

    def test_10_mask_gates_remain_required(self):
        for view in ("evidence_blind","query_blind"):
            raw=perfect_raw(self.data);raw["HOLDOUT"]["tripled"][view]=raw["HOLDOUT"]["tripled"]["normal"].clone()
            self.assertFalse(b.score(self.data,raw,p267)["passed"])

    def test_11_replay_tolerance_and_argmax(self):
        ref=self.refs[0]["raw"];x=copy.deepcopy(ref);x["TRAIN"]["doubled"]["normal"]+=5e-10
        self.assertLessEqual(b.replay_old(x,ref,self.data,p267),b.TOL)
        x["TRAIN"]["doubled"]["normal"]+=2e-9
        with self.assertRaises(ValueError):b.replay_old(x,ref,self.data,p267)

    def test_12_actual_probe_preserves_frozen_state_and_counts(self):
        m=copy.deepcopy(self.models[1]);ref=self.refs[1]
        r=b.probe(m,ref,self.data,self.prompts,p267,CoreCounter,Base,Factory)
        self.assertEqual((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"]),(81,7776,324))
        self.assertEqual(r["final_sha256"],ref["final_sha256"]);self.assertEqual(r["restore_error"],0.)

    def test_13_probe_rejects_training_mode(self):
        m=copy.deepcopy(self.models[0]).train()
        with self.assertRaisesRegex(ValueError,"frozen"):b.probe(m,self.refs[0],self.data,self.prompts,p267,CoreCounter,Base,Factory)

    def test_14_analyze_requires_all_states_and_candidate_gate(self):
        metrics,s=b.analyze(self.records,self.refs,self.data,p267)
        self.assertEqual(len(metrics),10);self.assertTrue(s["candidate_gate"])
        self.assertEqual(s["seed_pass_counts"],{"eos_query":5,"span_query":5});self.assertEqual(len(s["contrasts"]),60)
        with self.assertRaises(ValueError):b.analyze(self.records[:-1],self.refs,self.data,p267)

    def test_15_control_failure_does_not_fail_candidate(self):
        rr=copy.deepcopy(self.records);rr[0]["novel"]["HOLDOUT"]["tripled"]["normal"][0]=0
        self.assertTrue(b.analyze(rr,self.refs,self.data,p267)[1]["candidate_gate"])
        rr=copy.deepcopy(self.records);rr[1]["novel"]["HOLDOUT"]["tripled"]["normal"][0]=0
        self.assertFalse(b.analyze(rr,self.refs,self.data,p267)[1]["candidate_gate"])

    def test_16_saved_identity_count_and_replay_guards(self):
        for k,v in (("weights_preserved",False),("core_forward_calls",0),("restore_error",float("nan"))):
            rr=copy.deepcopy(self.records);rr[0][k]=v
            with self.assertRaises(ValueError):b.analyze(rr,self.refs,self.data,p267)

    def test_17_parent_loader_requires_c269_pass_and_reduced_schema(self):
        payload=dict(commit_sha=b.PARENT_EXECUTION,status="PASS",
            validation_summary={"seed_pass_counts":{"eos_query":4,"span_query":5},"candidate_gate":True},
            artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        metrics=[dict(seed=r["seed"],arm=r["arm"],**p267.score(self.data,r["raw"])) for r in self.refs]
        parent=SimpleNamespace(validate_result=Mock(),verify_artifacts=Mock(return_value=(payload,metrics)),
            analyze=Mock(return_value=(metrics,payload["validation_summary"])))
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);summary=root/"summary.json";summary.write_bytes(b"x")
            (root/"dataset.json").write_bytes(b.blob(self.data))
            torch.save(dict(schema="fold-c269-query-span-eval-v1",records=self.refs),root/"evaluations.pt")
            audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA,read_json=Audit.read_json)
            with patch.object(b,"context",return_value=(parent,p267,None,None,None,None,None,audit)):
                got,refs=b.load_reference(summary);self.assertEqual(got,self.data);self.assertEqual(len(refs),10)
                parent.verify_artifacts.assert_called_once_with(root,b.PARENT_EXECUTION)
                payload["status"]="FAIL"
                with self.assertRaises(ValueError):b.load_reference(summary)

    def test_18_result_validation_scope_and_workload(self):
        _,s=b.analyze(self.records,self.refs,self.data,p267);pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",
            source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
            gate_f_candidate=False,production_adoption=False,arbitrary_name_claim=False,causal_parser_claim=False,general_language_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,arbitrary_name_claim=True))

    def test_19_no_training_or_optimizer_calls_in_scientific_run(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        names=[]
        for n in ast.walk(tree):
            if isinstance(n,ast.Call):
                names.append(n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
        for forbidden in ("AdamW","backward","train_one","fit","step"):self.assertNotIn(forbidden,names)

    def test_20_actual_run_orchestration_and_saved_postcheck(self):
        parent=SimpleNamespace(load_bundle=Mock(return_value=[m.state_dict() for m in self.models]),make_arm_model=c269.make_arm_model)
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,p267,CoreCounter,Base,aligned,reader,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"load_reference",return_value=(self.data,self.refs)) as load:
            out=Path(d)/"out"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c269_summary=Path(d)/"parent.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(pre.call_count,2);self.assertEqual(load.call_count,1);parent.load_bundle.assert_called_once()
            with patch.object(b,"probe",side_effect=AssertionError("no saved-postcheck inference")):
                self.assertEqual(b.verify_artifacts(out,Path(d)/"parent.json","fixture-head")[0],result)
            self.assertEqual(load.call_count,2);parent.load_bundle.assert_called_once()

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
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,270)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names));self.assertEqual(5+len(names)+1,46)
        self.assertEqual(787+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),800)
        self.assertEqual(10*81,b.manifest()["model_forward_calls"]);self.assertEqual(77760*256*8,b.manifest()["raw_logit_payload_bytes"])

    def test_23_runner_cli_and_call_order(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c270.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c270.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3);indices=[]
        for text in blocks:
            compile(text,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher);self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start());self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertLess(launcher.index("-Mode Validate"),failure.start())
        self.assertGreater(launcher.index("-Mode Execute"),failure.start())
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        runner_source=runner
        self.assertIn('[ValidateSet("Validate","Execute")]',runner_source)
        self.assertLess(runner_source.index('if ($Mode -eq "Validate")'),runner_source.index('=== C270 scientific execution ==='))
        source=inspect.getsource(b.run)
        phases=("pins,protected=precheck(c269_summary,root)","data,refs=load_reference(c269_summary)","states=parent.load_bundle(","probe(model,ref,data,prompts,p267,core,base,factory)","metrics,summary=analyze(records,refs,data,p267)")
        positions=[]
        for phase in phases:
            self.assertEqual(source.count(phase),1,phase)
            positions.append(source.index(phase))
        self.assertEqual(positions,sorted(positions))
        phase_lines=[source[:pos].count("\n")+1 for pos in positions]
        self.assertEqual(len(phase_lines),len(set(phase_lines)))

    def test_24_dispatcher_historical_pin_contract(self):
        root=Path(__file__).resolve().parents[1];legacy=(root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode()
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),"86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(legacy.replace(b"\n",b"\r\n")).hexdigest(),"57a0f1ffa3a9370b5261ec5bf1e9eb3d778dc84f19f35c51e21174f61735a95b")
        active=(root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha256(active.encode()).hexdigest(),"68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")
        self.assertIn("RESULT_ALREADY_PUBLISHED",active);self.assertNotRegex(active,r"\$ExpectedHead\s*=\s*\$currentHead")


if __name__=="__main__":
    unittest.main(verbosity=2)
