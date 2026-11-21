"""Explicit parser-oracle fixtures exercise C264 plumbing, not learned capability."""
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
from unittest.mock import Mock,patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c264_two_fact_deletion as b


def old_data():
    train={(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
    data={k:{s:[] for s in b.SPLITS} for k in ("original","extra")}
    for a in itertools.permutations(range(4),3):
        split="TRAIN" if a in train else "HOLDOUT"
        for language in ("en","ja"):
            for p in itertools.permutations(range(3)):
                for q in range(3):
                    stage="original" if p in b.KNOWN else "extra"
                    row=dict(id=f'{language}-{a}-{p}-{q}',assignment=list(a),language=language,
                             permutation=list(p),query=q,target=48+a[q])
                    if stage=="original":row["order"]=b.KNOWN.index(p)
                    data[stage][split].append(row)
    return data


class Oracle(nn.Module):
    """A deliberate string parser with placeholder weights; NOT an experimental model."""
    def __init__(self,seed):
        super().__init__();self.marker=nn.Parameter(torch.zeros(14256,dtype=torch.float64))
        with torch.no_grad():self.marker[0]=seed/1e6
        self.backbone=nn.Module();self.backbone.core=nn.Identity();self.eval().requires_grad_(False)
    def forward(self,tokens,tasks):
        logits=torch.full((len(tokens),256),-10.,dtype=torch.float64)
        for i,row in enumerate(tokens.tolist()):
            fields=bytes(x for x in row if x<256).decode().split(";")
            facts=dict(x.split("=") for x in fields[:-1]);q=fields[-1][:-1]
            value=facts.get(q,next(iter(facts.values())))
            if value=="?":value="0"
            logits[i,ord(value)]=10.
        for _ in range(4):logits=self.backbone.core(logits)
        return logits+self.marker[0]*0


class Factory:
    @staticmethod
    def new_model(seed):return Oracle(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,"prefix length");return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def make_model(model,arm,seed,aligned,reader):
        b.require(arm=="aligned_precore_read","factory arm");return model
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for name,x in sorted(model.state_dict().items()):h.update(name.encode());h.update(x.detach().cpu().numpy().tobytes())
        return h.hexdigest()


class Trainer:
    @staticmethod
    def evaluate(model,parts,extra,base,orders,factory):
        result={};model.eval()
        with torch.no_grad():
            for stage,data in (("original",parts),("extra",extra)):
                result[stage]={}
                for split,rows in data.items():
                    result[stage][split]={}
                    for view in b.VIEWS:
                        converted=[dict(entities=[0,1,2],values=r["assignment"],permutation=r["permutation"],query=r["query"],language=r["language"]) for r in rows]
                        x=torch.stack([factory.prefix_tensor(b.render(r,view).encode()) for r in converted])
                        result[stage][split][view]=model(x,torch.zeros(len(x),dtype=torch.int64))
        return result


class CoreCounter:
    @staticmethod
    def core_counter(model):
        count=[0]
        def hook(module,args,output):count[0]+=1
        return count,model.backbone.core.register_forward_hook(hook)


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("fixture-input-"):return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        child=(Path(root)/name).resolve();b.require(child.parent==Path(root).resolve(),"unsafe child");return child
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"):return b"fixture-head"
        if args==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def protection():
    return {**{f"old-{i}":"fixture" for i in range(424)},**{n:"fixture" for n in b.OWN}},{f"fixture-input-{i}":"0"*64 for i in range(723)}


def parent_payload():
    return dict(commit_sha=b.PARENT_EXECUTION,status="PASS",validation_summary=dict(seed_pass_counts={a:5 for a in b.ARMS},rate_joint_pass={"standard":True,"lower":True}),
                artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])


class C264Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.rows=b.dataset();cls.data=old_data();cls.models=[Oracle(s) for s,a in b.identities()]
        raw=Trainer.evaluate(cls.models[0],cls.data["original"],cls.data["extra"],Base,None,Factory)
        reduced=b.evaluate_new(cls.models[0],cls.rows,Factory)
        cls.refs=[dict(seed=s,arm=a,final_sha256=Base.fingerprint(m),raw=raw) for (s,a),m in zip(b.identities(),cls.models,strict=True)]
        cls.records=[dict(seed=r["seed"],arm=r["arm"],final_sha256=r["final_sha256"],weights_preserved=True,model_forward_calls=30,
                         row_presentations=6048,core_forward_calls=120,anchor_error=0.,restore_error=0.,anchor=raw,reduced=reduced,restored=raw) for r in cls.refs]

    def test_01_fixed_hashes_and_registration(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA);self.assertEqual(b.digest(self.rows),b.DATA_SHA)
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(430,723)
            with self.assertRaises(ValueError):b.validate_registration(429,723)
            with patch.object(b,"MANIFEST_SHA","bad"),self.assertRaises(ValueError):b.validate_registration(430,723)

    def test_02_unique_rows_and_subsets(self):
        b.validate_dataset(self.rows);self.assertEqual(Counter(tuple(r["entities"]) for r in self.rows),{s:96 for s in b.SUBSETS})
        self.assertTrue(all(r["query"] in r["entities"] and len(set(r["values"]))==2 for r in self.rows))
        self.assertEqual(len({r["prompt"] for r in self.rows}),288)

    def test_03_provenance_dedup_and_partition_crossing(self):
        p=b.provenance(self.data,self.rows);self.assertEqual(len(p),288);self.assertEqual(sum(len(x["parents"]) for x in p),1728)
        for row,item in zip(self.rows,p,strict=True):
            self.assertEqual(item["row_id"],row["id"]);self.assertEqual(len(item["parents"]),6)
            self.assertTrue(all(x["removed_entity"] not in row["entities"] for x in item["parents"]))
        self.assertTrue(any(len({x["source"].split("/")[1] for x in r["parents"]})==2 for r in p))
        self.assertFalse(any("split" in r for r in self.rows))

    def test_04_missing_source_or_changed_answer_rejected(self):
        d=copy.deepcopy(self.data);d["original"]["TRAIN"].pop()
        with self.assertRaises(ValueError):b.provenance(d,self.rows)
        d=copy.deepcopy(self.data);d["original"]["TRAIN"][0]["target"]=200
        with self.assertRaises(ValueError):b.provenance(d,self.rows)

    def test_05_visible_bytes_masks_and_targets(self):
        for r in self.rows:
            self.assertEqual(r["target"],48+r["values"][r["entities"].index(r["query"])])
            self.assertEqual(r["prompt"].count(";"),2);self.assertEqual(b.render(r,"evidence_blind").count("?"),2)
            self.assertTrue(b.render(r,"query_blind").endswith(";?="));self.assertEqual(Factory.prefix_tensor(r["prompt"].encode()).shape,(48,))

    def test_06_perfect_scores_and_group_denominators(self):
        m=b.score(self.rows,self.records[0]["reduced"]);self.assertTrue(m["passed"])
        self.assertEqual((m["correct"],len(m["cells"]),len(m["two_order"])),(288,12,6))
        for c in m["cells"]:self.assertEqual((c["rows"],c["query_pair_accuracy"],c["query_drop"]),(24,1.,.5))
        for c in m["two_order"]:self.assertEqual((c["groups"],c["both_correct"]),(24,24))

    def test_07_one_weak_cell_not_pooled_away(self):
        raw={k:v.clone() for k,v in self.records[0]["reduced"].items()}
        ids=[i for i,r in enumerate(self.rows) if r["language"]=="en" and r["entities"]==[0,1] and r["permutation"]==[0,1]][:3]
        raw["normal"][ids]=0;m=b.score(self.rows,raw)
        self.assertGreater(m["correct"]/288,.98);self.assertFalse(m["passed"])

    def test_08_query_pair_counts(self):
        raw={k:v.clone() for k,v in self.records[0]["reduced"].items()};raw["normal"][0]=0
        m=b.score(self.rows,raw);c=m["cells"][0]
        self.assertEqual(c["correct"],23);self.assertEqual(c["query_pair_accuracy"],11/12)

    def test_09_two_order_groups_follow_same_question(self):
        raw={k:v.clone() for k,v in self.records[0]["reduced"].items()}
        ids=[i for i,r in enumerate(self.rows) if r["language"]=="en" and r["entities"]==[0,1] and r["permutation"]==[0,1]][:5]
        raw["normal"][ids]=0;c=b.score(self.rows,raw)["two_order"][0]
        self.assertEqual(c["both_correct"],19);self.assertFalse(c["passed"])

    def test_10_evidence_dependence_gate(self):
        raw=dict(self.records[0]["reduced"]);raw["evidence_blind"]=raw["normal"]
        self.assertFalse(b.score(self.rows,raw)["passed"])

    def test_11_query_dependence_gate(self):
        raw=dict(self.records[0]["reduced"]);raw["query_blind"]=raw["normal"]
        self.assertFalse(b.score(self.rows,raw)["passed"])

    def test_12_nonfinite_dtype_and_dataset_identity(self):
        x=self.records[0]["reduced"]["normal"]
        for value in (x.float(),x[:-1],torch.full_like(x,float("nan"))):
            with self.assertRaises(ValueError):b.check_logits(value,288)
        r=copy.deepcopy(self.rows);r[0]["target"]=200
        with self.assertRaises(ValueError):b.validate_dataset(r)

    def test_13_replay_tolerance_and_argmax(self):
        raw=copy.deepcopy(self.refs[0]["raw"]);raw["original"]["TRAIN"]["normal"]+=5e-10
        self.assertLessEqual(b.replay_original(raw,self.refs[0]["raw"]),b.TOL)
        raw["original"]["TRAIN"]["normal"]+=2e-9
        with self.assertRaises(ValueError):b.replay_original(raw,self.refs[0]["raw"])
        a=copy.deepcopy(self.refs[0]["raw"]);a["original"]["TRAIN"]["normal"].zero_();c=copy.deepcopy(a);c["original"]["TRAIN"]["normal"][:,1]=5e-10
        with self.assertRaises(ValueError):b.replay_original(a,c)

    def test_14_anchor_failure_prevents_new_inputs(self):
        ref=copy.deepcopy(self.refs[0]);ref["raw"]["original"]["TRAIN"]["normal"]+=1
        with patch.object(b,"evaluate_new") as new,self.assertRaisesRegex(ValueError,"replay"):
            b.probe(self.models[0],ref,self.data,self.rows,CoreCounter,Trainer,Base,None,Factory)
        new.assert_not_called();self.assertFalse(self.models[0]._forward_hooks);self.assertFalse(self.models[0].backbone.core._forward_hooks)

    def test_15_freeze_and_mutation_guards(self):
        model=copy.deepcopy(self.models[0]).train()
        with self.assertRaisesRegex(ValueError,"frozen"):b.probe(model,self.refs[0],self.data,self.rows,CoreCounter,Trainer,Base,None,Factory)
        model.eval()
        def mutate(m,args,output):
            with torch.no_grad():m.marker[0]+=1
        h=model.register_forward_hook(mutate)
        try:
            with self.assertRaisesRegex(ValueError,"mutation"):b.probe(model,self.refs[0],self.data,self.rows,CoreCounter,Trainer,Base,None,Factory)
        finally:h.remove()

    def test_16_actual_probe_counts_and_no_new_weights(self):
        r=b.probe(self.models[0],self.refs[0],self.data,self.rows,CoreCounter,Trainer,Base,None,Factory)
        self.assertEqual((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"]),(30,6048,120))
        self.assertEqual(r["final_sha256"],self.refs[0]["final_sha256"]);self.assertEqual(r["restore_error"],0.)

    def test_17_saved_identity_and_count_guards(self):
        with self.assertRaises(ValueError):b.analyze(self.records[:-1],self.refs,self.rows)
        for key,value in (("weights_preserved",False),("core_forward_calls",0),("restore_error",float("nan"))):
            records=list(self.records);records[0]=dict(records[0],**{key:value})
            with self.assertRaises(ValueError):b.analyze(records,self.refs,self.rows)

    def test_18_all_four_arms_required(self):
        for index in range(4):
            records=list(self.records);r=dict(records[index]);r["reduced"]=dict(r["reduced"],normal=torch.zeros_like(r["reduced"]["normal"]));records[index]=r
            _,s=b.analyze(records,self.refs,self.rows);self.assertFalse(s["joint_gate"]);self.assertEqual(s["seed_pass_counts"][b.ARMS[index]],4)

    def test_19_actual_parent_loader_dispatch(self):
        p=parent_payload();parent=SimpleNamespace(validate_result=lambda p:None,verify_artifacts=Mock(return_value=(p,[{}]*20)))
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/"dataset.json").write_bytes(b.blob(self.data));torch.save(dict(schema="fold-c263-rate-eval-v1",records=self.refs),root/"evaluations.pt")
            audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA,read_json=Audit.read_json)
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,None,Factory,audit)),patch.object(torch,"load",wraps=torch.load) as load:
                data,refs=b.load_reference(root/"summary.json");self.assertEqual(data,self.data);self.assertEqual(len(refs),20)
                parent.verify_artifacts.assert_called_once_with(root,b.PARENT_EXECUTION);load.assert_called_once()
                p["status"]="FAIL"
                with self.assertRaises(ValueError):b.load_reference(root/"summary.json")

    def test_20_actual_twenty_model_run_and_saved_postcheck(self):
        parent=SimpleNamespace(load_bundle=Mock(return_value=[m.state_dict() for m in self.models]))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,CoreCounter,Trainer,Base,None,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"load_reference",return_value=(self.data,self.refs)) as load:
            root=Path(d);out=root/"out"
            with contextlib.redirect_stdout(io.StringIO()):p=b.run(c263_summary=root/"parent.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(pre.call_count,2);self.assertEqual(load.call_count,1);parent.load_bundle.assert_called_once()
            with patch.object(Factory,"new_model",side_effect=AssertionError("no postcheck model")),patch.object(b,"probe",side_effect=AssertionError("no postcheck inference")):
                self.assertEqual(b.verify_artifacts(out,root/"parent.json","fixture-head")[0],p)
            parent.load_bundle.assert_called_once();self.assertEqual(load.call_count,2)
            with self.assertRaisesRegex(ValueError,"saved HEAD"):b.verify_artifacts(out,root/"parent.json","wrong")
            (out/"provenance.json").write_bytes(b"[]")
            with self.assertRaises(ValueError):b.verify_artifacts(out,root/"parent.json","fixture-head")

    def test_21_no_training_and_real_call_order(self):
        import inspect
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if isinstance(n,ast.Call):
                name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ""
                self.assertNotIn(name,{"AdamW","backward","fit","train_one","step"})
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,n in calls if n==name)
        for a,c in (("load_reference","load_bundle"),("provenance","probe"),("load_bundle","probe"),("probe","analyze")):self.assertLess(first(a),first(c))
        model=nn.Linear(1,1)
        with b.no_model_calls(),self.assertRaises(RuntimeError):model(torch.zeros(1,1))
        self.assertEqual(model(torch.zeros(1,1)).shape,(1,1))

    def test_22_runner_cli_and_parser_order(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c264.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c264.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3);indices=[]
        for block in blocks:
            compile(block,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}]);failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher)
        self.assertIsNotNone(failure);self.assertLess(launcher.index("::ParseFile"),failure.start());self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("638f26dfee354c9cb3aa5fa174d3e9f6",launcher)

    def test_23_semantic_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        s=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=s):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3501)

    def test_24_resource_dependency_and_scope_contract(self):
        import inspect
        tree=ast.parse(inspect.getsource(b.precheck));pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,264)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names));self.assertEqual(5+len(names)+1,40)
        self.assertEqual(710+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),723);self.assertEqual(120960*256*8,b.manifest()["logit_payload_bytes"])
        _,s=b.analyze(self.records,self.refs,self.rows);pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,
               artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,production_adoption=False,gate_f_candidate=False,
               learning_rate_benefit_claim=False,general_language_claim=False,arbitrary_length_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,arbitrary_length_claim=True))
        s["seed_pass_counts"][b.ARMS[0]]=4
        with self.assertRaises(ValueError):b.validate_result(p)


if __name__=="__main__":
    unittest.main(verbosity=2)
