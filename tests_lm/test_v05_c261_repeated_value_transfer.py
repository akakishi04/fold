"""Synthetic byte-parser oracle fixtures test C261 plumbing, not learned ability."""
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
from unittest.mock import Mock, patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c261_repeated_value_transfer as b


def original_data():
    train={(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
    data={"original":{s:[] for s in b.SPLITS},"extra":{s:[] for s in b.SPLITS}}
    for a in itertools.permutations(range(4),3):
        split="TRAIN" if a in train else "HOLDOUT"
        for language in ("en","ja"):
            for p in b.ORDERS:
                for query in range(3):
                    row=dict(assignment=list(a),language=language,permutation=list(p),query=query,target=48+a[query])
                    name="original" if p in ((0,1,2),(2,1,0)) else "extra"
                    data[name][split].append(row)
    return data


class Factory:
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,"length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Oracle(nn.Module):
    """Deliberate oracle. It must never be used as the experimental model."""
    def __init__(self,seed,arm):
        super().__init__();self.marker=nn.Parameter(torch.zeros(b.PARAMETERS[arm],dtype=torch.float64))
        with torch.no_grad():self.marker[0]=seed/1e6
        self.backbone=nn.Module();self.backbone.core=nn.Identity() if arm=="with_core" else None
        self.bad_original=(arm=="with_core" and seed==260005) or (arm=="without_core" and seed in (260002,260004))
        self.eval().requires_grad_(False)
    def forward(self,tokens,tasks):
        logits=torch.full((len(tokens),256),-10.,dtype=torch.float64)
        for i,token_row in enumerate(tokens.tolist()):
            text=bytes(v for v in token_row if v<256).decode();fields=text.split(";")
            facts=dict(f.split("=") for f in fields[:-1]);query=fields[-1][:-1]
            numeric=[v for v in facts.values() if v in ("0","1","2","3")]
            answer=facts.get(query,"?")
            if answer=="?":answer=Counter(numeric).most_common(1)[0][0] if numeric else "0"
            target=ord(answer)
            if self.bad_original and len(set(numeric))==3 and query in facts:
                target=200
            logits[i,target]=10.
        if self.backbone.core is not None:
            for _ in range(4):logits=self.backbone.core(logits)
        return logits+self.marker[0]*0


class Base:
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for key,value in sorted(model.state_dict().items()):
            h.update(key.encode());h.update(value.detach().cpu().numpy().tobytes())
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
                        tokens=torch.stack([factory.prefix_tensor(b.render(r,view).encode()) for r in rows])
                        result[stage][split][view]=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
        return result


class Parent:
    @staticmethod
    def core_counter(model):
        calls=[0]
        def counted(module,args,output):calls[0]+=1
        core=model.backbone.core
        return calls,None if core is None else core.register_forward_hook(counted)
    @staticmethod
    def make_pair(seed,base,aligned,reader,factory):
        return tuple(Oracle(seed,a) for a in b.ARMS)
    @staticmethod
    def validate_result(p):
        b.require(p["commit_sha"]==b.PARENT_EXECUTION,"parent execution")


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
    return {**{f"old-{i}":"fixture" for i in range(406)},**{n:"fixture" for n in b.OWN}},{f"fixture-input-{i}":"0"*64 for i in range(685)}


class C261Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.rows=b.dataset();cls.data=original_data();cls.models=[];cls.refs=[];cls.records=[]
        for seed,arm in b.identities():
            model=Oracle(seed,arm);raw=Trainer.evaluate(model,cls.data["original"],cls.data["extra"],Base,None,Factory)
            ref=dict(seed=seed,arm=arm,final_sha256=Base.fingerprint(model),raw=raw)
            cls.models.append(model);cls.refs.append(ref)
            cls.records.append(b.probe(model,ref,cls.data,cls.rows,Parent,Trainer,Base,None,Factory))

    def test_01_fixed_hashes_and_registration_rejection(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA);self.assertEqual(b.digest(self.rows),b.DATA_SHA)
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(412,685)
            with self.assertRaisesRegex(ValueError,"source/input counts"):b.validate_registration(411,685)
            with patch.object(b,"MANIFEST_SHA","bad"),self.assertRaisesRegex(ValueError,"manifest hash"):b.validate_registration(412,685)

    def test_02_complete_unseen_assignment_strata(self):
        assignments={tuple(r["assignment"]) for r in self.rows}
        self.assertEqual(len(assignments),40)
        self.assertTrue(assignments.isdisjoint(itertools.permutations(range(4),3)))
        self.assertEqual(Counter(r["kind"] for r in self.rows),{"pair_equal":1296,"all_equal":144})
        self.assertEqual(len({r["id"] for r in self.rows}),1440)

    def test_03_target_render_and_no_truncation(self):
        for r in self.rows:
            self.assertEqual(r["target"],48+r["assignment"][r["query"]]);self.assertEqual(r["prompt"],b.render(r))
            self.assertLessEqual(len(r["prompt"].encode()),46)
            self.assertEqual(Factory.prefix_tensor(r["prompt"].encode()).shape,(48,))

    def test_04_permutation_and_mask_semantics(self):
        for r in self.rows:
            self.assertEqual(b.render(r,"evidence_blind").count("?"),3)
            self.assertTrue(b.render(r,"query_blind").endswith(";?="))
            self.assertEqual(sorted(r["permutation"]),[0,1,2])
        with self.assertRaises(ValueError):b.render(self.rows[0],"bad")

    def test_05_frozen_oracle_scores_and_denominators(self):
        m=b.score(self.rows,self.records[0]["novel"])
        self.assertTrue(m["passed"]);self.assertEqual(m["correct"],1440);self.assertEqual(len(m["cells"]),24)
        self.assertEqual(len(m["six_order"]),4)
        for c in m["cells"]:
            self.assertEqual((c["rows"],c["singleton_rows"]),(108,36) if c["kind"]=="pair_equal" else (12,0))
        self.assertEqual(sorted(c["groups"] for c in m["six_order"]),[12,12,108,108])

    def test_06_query_blind_drop_is_not_old_gate(self):
        m=b.score(self.rows,self.records[0]["novel"])
        for c in m["cells"]:
            self.assertAlmostEqual(c["query_drop"],1/3 if c["kind"]=="pair_equal" else 0.)
            self.assertTrue(c["passed"])
            if c["kind"]=="all_equal":self.assertIsNone(c["singleton_accuracy"])

    def test_07_repeated_value_guess_cannot_pass(self):
        raw={k:v.clone() for k,v in self.records[0]["novel"].items()}
        raw["normal"]=raw["query_blind"].clone()
        m=b.score(self.rows,raw);self.assertFalse(m["passed"])
        for c in m["cells"]:
            if c["kind"]=="pair_equal":self.assertEqual(c["singleton_accuracy"],0.)

    def test_08_singleton_fail_not_hidden_by_total(self):
        raw={k:v.clone() for k,v in self.records[0]["novel"].items()}
        ids=[i for i,r in enumerate(self.rows) if r["singleton"] and r["language"]=="en" and tuple(r["permutation"])==b.ORDERS[0]][:4]
        raw["normal"][ids]=0
        c=next(c for c in b.score(self.rows,raw)["cells"] if c["kind"]=="pair_equal" and c["language"]=="en" and c["permutation"]==list(b.ORDERS[0]))
        self.assertGreater(c["accuracy"],.90);self.assertLess(c["singleton_accuracy"],.90);self.assertFalse(c["passed"])

    def test_09_all_equal_not_pooled_away(self):
        raw={k:v.clone() for k,v in self.records[0]["novel"].items()}
        ids=[i for i,r in enumerate(self.rows) if r["kind"]=="all_equal" and r["language"]=="ja" and tuple(r["permutation"])==b.ORDERS[0]][:2]
        raw["normal"][ids]=0
        m=b.score(self.rows,raw);self.assertGreater(m["correct"]/1440,.99);self.assertFalse(m["passed"])

    def test_10_six_order_consistency_required(self):
        raw={k:v.clone() for k,v in self.records[0]["novel"].items()}
        assignments=sorted({tuple(r["assignment"]) for r in self.rows if r["kind"]=="pair_equal"})
        for p,perm in enumerate(b.ORDERS):
            chosen=set(assignments[4*p:4*p+4])
            ids=[i for i,r in enumerate(self.rows) if r["language"]=="en" and tuple(r["permutation"])==perm and r["query"]==0 and tuple(r["assignment"]) in chosen]
            raw["normal"][ids]=0
        m=b.score(self.rows,raw);six=next(c for c in m["six_order"] if c["language"]=="en" and c["kind"]=="pair_equal")
        self.assertEqual(six["all_six_correct"],84);self.assertFalse(six["passed"])

    def test_11_no_evidence_use_fails(self):
        raw={k:v.clone() for k,v in self.records[0]["novel"].items()};raw["evidence_blind"]=raw["normal"].clone()
        self.assertFalse(b.score(self.rows,raw)["passed"])

    def test_12_bad_data_logits_dtype_and_finiteness(self):
        bad=copy.deepcopy(self.rows);bad[0]["target"]=200
        with self.assertRaises(ValueError):b.validate_dataset(bad)
        x=self.records[0]["novel"]["normal"]
        with self.assertRaises(ValueError):b.check_logits(x.float(),1440)
        y=x.clone();y[0,0]=float("nan")
        with self.assertRaises(ValueError):b.check_logits(y,1440)
        with self.assertRaises(ValueError):b.check_logits(x[:-1],1440)

    def test_13_replay_tolerance_and_exact_argmax(self):
        x=torch.zeros(2,256,dtype=torch.float64);x[:,0]=1
        self.assertLessEqual(b.replay(x,x+5e-10),b.TOL)
        with self.assertRaises(ValueError):b.replay(x,x+2e-9)
        x.zero_();y=x.clone();y[:,1]=5e-10
        with self.assertRaises(ValueError):b.replay(x,y)

    def test_14_anchor_barrier_before_new_questions(self):
        ref=dict(self.refs[0],raw=copy.deepcopy(self.refs[0]["raw"]))
        ref["raw"]["original"]["TRAIN"]["normal"]+=1.
        with patch.object(b,"evaluate_new") as new,self.assertRaisesRegex(ValueError,"replay"):
            b.probe(self.models[0],ref,self.data,self.rows,Parent,Trainer,Base,None,Factory)
        new.assert_not_called();self.assertFalse(self.models[0]._forward_hooks);self.assertFalse(self.models[0].backbone.core._forward_hooks)

    def test_15_actual_probe_counts_weights_and_freeze_guard(self):
        r=b.probe(self.models[1],self.refs[1],self.data,self.rows,Parent,Trainer,Base,None,Factory)
        self.assertEqual((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"]),(54,9504,0))
        self.assertEqual(r["restore_error"],0.)
        m=copy.deepcopy(self.models[0]).train()
        with self.assertRaisesRegex(ValueError,"frozen"):b.probe(m,self.refs[0],self.data,self.rows,Parent,Trainer,Base,None,Factory)

    def test_16_old_miss_does_not_fail_replay_or_new_gate(self):
        # Oracle deliberately has the same 4/5 and 3/5 distinct-task misses as the parent fixture.
        self.assertEqual(self.refs[8]["raw"]["original"]["TRAIN"]["normal"].argmax(-1)[0].item(),200)
        _,summary=b.analyze(self.records,self.refs,self.rows)
        self.assertTrue(summary["joint_gate"]);self.assertEqual(summary["seed_pass_counts"],{"with_core":5,"without_core":5})

    def test_17_each_arm_is_required_for_joint_gate(self):
        for index in (0,1):
            records=list(self.records);r=dict(records[index]);r["novel"]=dict(r["novel"],normal=torch.zeros_like(r["novel"]["normal"]));records[index]=r
            _,s=b.analyze(records,self.refs,self.rows)
            self.assertFalse(s["joint_gate"]);self.assertEqual(s["seed_pass_counts"][b.ARMS[index]],4)

    def test_18_saved_corruption_and_identity_rejected(self):
        for key,value in (("weights_preserved",False),("core_forward_calls",0),("restore_error",float("nan"))):
            records=list(self.records);records[0]=dict(records[0],**{key:value})
            with self.assertRaises(ValueError):b.analyze(records,self.refs,self.rows)
        with self.assertRaises(ValueError):b.analyze(list(reversed(self.records)),self.refs,self.rows)
        records=list(self.records);records[0]=dict(records[0],restored=copy.deepcopy(records[0]["restored"]))
        records[0]["restored"]["extra"]["TRAIN"]["normal"]+=.1
        with self.assertRaises(ValueError):b.analyze(records,self.refs,self.rows)

    def test_19_parent_loader_actual_dispatch_and_negative_status(self):
        payload=dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",validation_summary={"seed_pass_counts":{"with_core":4,"without_core":3}},
            artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        parent=SimpleNamespace(validate_result=Parent.validate_result,verify_artifacts=Mock(return_value=(payload,["metrics"])),analyze=Mock(return_value=(["metrics"],payload["validation_summary"])))
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/"dataset.json").write_bytes(b.blob(self.data))
            torch.save(dict(schema="fold-c260-core-eval-v1",records=self.refs),root/"evaluations.pt")
            audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA,read_json=Audit.read_json)
            with patch.object(b,"context",return_value=(parent,None,Base,None,None,None,Factory,audit)),patch.object(torch,"load",wraps=torch.load) as load:
                data,refs=b.load_reference(root/"summary.json")
                self.assertEqual(data,self.data);self.assertEqual(len(refs),10)
                parent.verify_artifacts.assert_called_once_with(root,b.PARENT_EXECUTION);load.assert_called_once()
                payload["status"]="PASS"
                with self.assertRaises(ValueError):b.load_reference(root/"summary.json")

    def test_20_actual_run_saved_postcheck_and_no_new_inference(self):
        parent=SimpleNamespace(make_pair=Parent.make_pair,core_counter=Parent.core_counter,load_bundle=Mock(return_value=[m.state_dict() for m in self.models]))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,Trainer,Base,None,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"load_reference",return_value=(self.data,self.refs)) as load:
            root=Path(d);out=root/"out"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c260_summary=root/"parent.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(pre.call_count,2);self.assertEqual(load.call_count,1);parent.load_bundle.assert_called_once()
            with patch.object(b,"probe",side_effect=AssertionError("no forward in persisted postcheck")):
                self.assertEqual(b.verify_artifacts(out,root/"parent.json","fixture-head")[0],result)
            self.assertEqual(load.call_count,2);parent.load_bundle.assert_called_once()
            with self.assertRaisesRegex(ValueError,"saved HEAD"):b.verify_artifacts(out,root/"parent.json","wrong")
            (out/"measurements.json").write_bytes(b"[]")
            with self.assertRaises(ValueError):b.verify_artifacts(out,root/"parent.json","fixture-head")

    def test_21_semantic_own_ids_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_22_runner_cli_parser_and_source_call_order(self):
        import inspect
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c261.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c261.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3);indices=[]
        for block in blocks:
            compile(block,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher);self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start());self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("697d8bdc3ca3411ba81f703b2f16fb96",launcher)
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,n in calls if n==name)
        for left,right in (("load_reference","load_bundle"),("load_bundle","probe"),("probe","analyze"),("analyze","save")):
            self.assertLess(first(left),first(right))

    def test_23_no_training_calls_and_state_mutation_guard(self):
        for node in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))):
            if isinstance(node,ast.Call):
                name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else ""
                self.assertNotIn(name,{"AdamW","backward","fit","train_one","step"})
        model=copy.deepcopy(self.models[0])
        def mutate(module,args,out):
            with torch.no_grad():module.marker[0]+=1
        h=model.register_forward_hook(mutate)
        try:
            with self.assertRaisesRegex(ValueError,"mutation"):b.probe(model,self.refs[0],self.data,self.rows,Parent,Trainer,Base,None,Factory)
        finally:h.remove()
        self.assertFalse(model._forward_hooks)

    def test_24_result_claim_and_gate_accounting_guards(self):
        _,s=b.analyze(self.records,self.refs,self.rows);pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False,core_superiority_claim=False,general_language_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,core_superiority_claim=True))
        p["validation_summary"]["seed_pass_counts"]["with_core"]=4
        with self.assertRaises(ValueError):b.validate_result(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
