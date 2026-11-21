"""C241 authoring tests; synthetic toy work is not scientific evidence."""
import ast
from collections import Counter, defaultdict
import contextlib
import copy
import hashlib
import inspect
import io
import itertools
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c239_order_holdout as old
from fold_lm.v05_benchmarks import model_c240_saved_position_audit as audit
from fold_lm.v05_benchmarks import model_c241_assignment_holdout as b


def source_parts():
    pool=[]; names={"en":("box","book"),"ja":("箱","本")}
    for x,y in ((0,1),(1,0)):
        group=f"0-1-{x}-{y}"
        for lang in names:
            for order,query in itertools.product((0,1),(0,1)):
                facts=[(0,x),(1,y)]
                if order: facts.reverse()
                text=";".join(names[lang][k]+"="+str(v) for k,v in facts)+";"+names[lang][query]+"="
                pool.append(dict(id=f"{lang}-{group}-{order}-{query}",group=group,objects=[0,1],values=[x,y],
                    language=lang,order=order,query=query,split="TRAIN",target=48+(x if query==0 else y),prompt=text))
    return {key:[r for r in pool if r["order"]==order] for key,order in zip(b.SPLITS,(0,1),strict=True)}


def perfect_metrics(good=True):
    return {lang:dict(rows=4,accuracy=1.0 if good else .5,answer_nll=.1 if good else .7,
        evidence_blind_accuracy=.5,query_blind_accuracy=.5,evidence_drop=.5 if good else 0.0,
        query_drop=.5 if good else 0.0,query_pair_accuracy=1.0 if good else 0.0,
        order_pair_accuracy=1.0 if good else 0.0) for lang in ("en","ja")}


def records(good=True):
    return [dict(seed=seed,family=family,initial_sha256="a"*64,final_sha256="b"*64,
        initial_train=perfect_metrics(False),final={s:perfect_metrics(good) for s in b.SPLITS},
        fit=dict(steps=400,answer_presentations=12800),forward_calls=415,row_presentations=12920,
        checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.0,weights_changed=True)
        for seed,family in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(286)};pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(442)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=summary,
        status="PASS" if summary["full_assignment_gate"] else "FAIL",gate_f_candidate=False,network_calls=0)


class Toy(torch.nn.Module):
    def __init__(self,count=13488):
        super().__init__();self.linear=torch.nn.Linear(4,256).double()
        self.padding=torch.nn.Parameter(torch.zeros(count-1280,dtype=torch.float64))
    def forward(self,tokens,tasks): return self.linear(tokens)


class Factory:
    @staticmethod
    def new_model(seed):
        torch.manual_seed(seed);return Toy()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for key,value in sorted(model.state_dict().items()):
            h.update(key.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    @staticmethod
    def new_baseline(full):
        model=Toy(10160);model.linear.load_state_dict(copy.deepcopy(full.linear.state_dict()));return model
    @staticmethod
    def parent_module(): return Binding
    @staticmethod
    def tensors(rows,mode):
        x=torch.tensor([[r["values"][0],r["query"],r["order"],int(r["language"]=="ja")] for r in rows],dtype=torch.float64)
        if mode=="evidence_blind": x[:,0]=.5
        if mode=="query_blind": x[:,1]=.5
        return x,torch.tensor([r["target"] for r in rows])


class Audit:
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
        if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"):return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        path=(Path(root)/name).resolve()
        if path.parent!=Path(root).resolve():raise ValueError("unsafe child")
        return path


def c239_records(parts):
    result=[]
    for seed,family in b.identities():
        predictions={};final={}
        for split in b.SPLITS:
            rows=parts[split]
            pred={"normal":[r["target"] for r in rows],
                  "evidence_blind":[48]*8,"query_blind":[48]*8}
            predictions[split]=pred
            final[split]={lang:dict(m,answer_nll=.7) for lang,m in audit.discrete_metrics(rows,pred).items()}
        result.append(dict(seed=seed,family=family,initial_sha256="a"*64,final_sha256="b"*64,
            predictions=predictions,final=final,checkpoint_roundtrip=True,prediction_replayed=True,
            weights_changed=True,reload_max_error=0.0))
    return result


class C241Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.source=source_parts();cls.parts=b.split_assignments(cls.source)

    def exercise(self):
        model=Factory.new_model(9010);ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model))
        with contextlib.redirect_stdout(io.StringIO()):
            return b.train_one(model,self.parts,ref,binding=Binding,factory=Factory)

    def test_01_manifest_source_and_assignment_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.source),audit.PARENT_ARTIFACTS["split-dataset.json"])
        self.assertEqual(b.digest(self.parts),b.SPLIT_SHA)

    def test_02_split_balances_orders_queries_languages(self):
        for split,values in (("TRAIN",[0,1]),("HOLDOUT",[1,0])):
            rows=self.parts[split];self.assertEqual(len(rows),8)
            for lang in ("en","ja"):
                sub=[r for r in rows if r["language"]==lang]
                self.assertEqual(Counter(r["order"] for r in sub),{0:2,1:2})
                self.assertEqual(Counter(r["query"] for r in sub),{0:2,1:2})
                self.assertTrue(all(r["values"]==values for r in sub))

    def test_03_fixed_position_shortcut_cannot_fit_train(self):
        rows=self.parts["TRAIN"];pred=[]
        for r in rows:
            rendered=r["values"] if r["order"]==0 else r["values"][::-1]
            pred.append(48+rendered[r["query"]])
        self.assertEqual(sum(p==r["target"] for p,r in zip(pred,rows,strict=True))/8,.5)

    def test_04_fixed_entity_values_fit_train_fail_holdout(self):
        for split,wanted in (("TRAIN",1.0),("HOLDOUT",0.0)):
            rows=self.parts[split];pred=[48+r["query"] for r in rows]
            self.assertEqual(sum(p==r["target"] for p,r in zip(pred,rows,strict=True))/8,wanted)

    def test_05_partition_tamper_rejected(self):
        for key,value in (("values",[1,0]),("target",255),("split","EVAL")):
            source=copy.deepcopy(self.source);source["TRAIN"][0][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError):b.split_assignments(source)

    def test_06_complete_train8_batch_four_times(self):
        ids=b.balanced_indices(8)
        self.assertEqual(ids.tolist(),list(range(8))*4)
        self.assertEqual(Counter(ids.tolist()),{i:4 for i in range(8)})

    def test_07_parent_fit_ast_and_constants(self):
        b.audit_fit_contract(old)
        with patch.object(old,"LR",old.LR*2):
            with self.assertRaises(ValueError):b.audit_fit_contract(old)

    def test_08_perfect_custom_metrics_pass(self):
        m=perfect_metrics(True);b.validate_metrics(m)
        self.assertTrue(all(b.cell_pass(x) for x in m.values()))

    def test_09_query_and_order_pair_semantics(self):
        rows=[r for r in self.parts["TRAIN"] if r["language"]=="en"]
        pred=[r["target"] for r in rows]
        self.assertEqual(b.pair_accuracy(rows,pred,"query"),1)
        self.assertEqual(b.pair_accuracy(rows,pred,"order"),1)
        pred=[48]*4
        self.assertEqual(b.pair_accuracy(rows,pred,"query"),0)

    def test_10_metric_schema_nonfinite_and_drop_rejected(self):
        for key,value in (("rows",8),("answer_nll",float("nan")),("query_drop",0.25)):
            m=perfect_metrics();m["en"][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError):b.validate_metrics(m)

    def test_11_primary_and_baseline_are_independent(self):
        r=records()
        for item in r:
            if item["family"]=="full":item["final"]["HOLDOUT"]=perfect_metrics(False)
        s=b.summarize(r);self.assertFalse(s["full_assignment_gate"]);self.assertTrue(s["gru_assignment_gate"])
        p=payload(s);b.validate_result(p);self.assertEqual(p["status"],"FAIL")

    def test_12_outcome_localizes_train_vs_assignment_miss(self):
        r=records();r[0]["final"]["TRAIN"]=perfect_metrics(False);r[1]["final"]["HOLDOUT"]=perfect_metrics(False)
        s=b.summarize(r)
        self.assertEqual(s["cell_outcomes"],{"TRAIN_FIT_MISS":2,"ASSIGNMENT_HOLDOUT_MISS":2,"BOTH_PASS":8})

    def test_13_replay_or_workload_fault_is_invalid(self):
        for key,value in (("reload_max_error",.1),("forward_calls",414),("weights_changed",False)):
            r=records();r[0][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r)))

    def test_14_actual_fit_batch_contains_no_holdout_assignment(self):
        x,y=Binding.tensors(self.parts["TRAIN"],"normal");model=Factory.new_model(9011);seen=[]
        handle=model.register_forward_pre_hook(lambda module,args:seen.append(args[0].clone()))
        b.fit(model,x,y,9012,steps=2);handle.remove()
        self.assertEqual(len(seen),2);self.assertTrue(all(torch.equal(batch,x.repeat(4,1)) for batch in seen))

    def test_15_holdout_is_evaluated_only_after_fit(self):
        model=Factory.new_model(9010);ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model))
        complete=[False];native=b.fit;native_eval=b.evaluate
        def fitted(*args,**kwargs):
            result=native(*args,**kwargs);complete[0]=True;return result
        def checked(model,rows,binding,fingerprint):
            if rows and rows[0]["values"]==[1,0] and not complete[0]:raise AssertionError("holdout before fit")
            return native_eval(model,rows,binding,fingerprint)
        with patch.object(b,"fit",side_effect=fitted),patch.object(b,"evaluate",side_effect=checked),contextlib.redirect_stdout(io.StringIO()):
            r,_,_=b.train_one(model,self.parts,ref,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(409,12872))

    def test_16_initial_mismatch_stops_before_fit(self):
        with patch.object(b,"fit") as fitted:
            with self.assertRaises(ValueError):
                b.train_one(Factory.new_model(9010),self.parts,dict(initial_sha256="wrong"),binding=Binding,factory=Factory)
            fitted.assert_not_called()

    def test_17_actual_train_and_checkpoint_replay_counts(self):
        r,state,raw=self.exercise()
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(409,12872))
        b.replay_one(Factory.new_model(9010),state,r,raw,self.parts,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,12920))

    def test_18_changed_replay_logits_rejected(self):
        r,state,raw=self.exercise();raw["HOLDOUT"][0]=raw["HOLDOUT"][0]+.1
        with self.assertRaises(ValueError):
            b.replay_one(Factory.new_model(9010),state,r,raw,self.parts,binding=Binding,factory=Factory)

    def test_19_checkpoint_schema_and_identity_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"models.pt"
            value=dict(schema="fold-c241-assignment-holdout-v1",identities=[list(x) for x in b.identities()],states=[{}]*6)
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),6)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    def test_20_actual_loader_reads_c239_initial_identities(self):
        refs=c239_records(self.source)
        fitting=SimpleNamespace(summarize=lambda r:{"models":len(r)},validate_result=lambda p:None)
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(audit,fitting,None,None,Audit)):
            root=Path(tmp)
            for name,value in (("split-dataset.json",self.source),("measurements.json",refs),
                               ("summary.json",dict(validation_summary={"models":6}))):
                (root/name).write_bytes(b.blob(value))
            parts,saved=b.load_inputs(root/"summary.json")
            self.assertEqual(parts,self.parts);self.assertEqual(saved,refs)
            refs[0]["initial_sha256"]=refs[0]["final_sha256"]
            (root/"measurements.json").write_bytes(b.blob(refs))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_21_synthetic_six_model_run_and_postcheck(self):
        refs=[]
        for seed,family in b.identities():
            model=Factory.new_model(seed)
            if family=="gru_only":model=Binding.new_baseline(model)
            refs.append(dict(seed=seed,family=family,initial_sha256=Factory.fingerprint(model)))
        base=payload(b.summarize(records()))
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(None,None,Binding,Factory,Audit)), \
             patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader:
            out=Path(tmp)/"out";c240=Path(tmp)/"c240.json";c239=Path(tmp)/"c239.json"
            with contextlib.redirect_stdout(io.StringIO()):
                result=b.run(c240_summary=c240,c239_summary=c239,output_dir=out,expected_head="synthetic-head")
            self.assertEqual(pre.call_count,2);loader.assert_called_once()
            verified,recs=b.verify_artifacts(out,c239,"synthetic-head")
            self.assertEqual(verified,result);self.assertEqual(len(recs),6)
            with self.assertRaises(ValueError):b.verify_artifacts(out,c239,"wrong")
            (out/"split-dataset.json").write_text("{}",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,c239,"synthetic-head")

    def test_22_run_loader_common_copy_save_replay_order(self):
        tree=ast.parse(inspect.getsource(b.run))
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
               for n in ast.walk(tree) if isinstance(n,ast.Call)]
        line=lambda name:min(i for i,k in calls if k==name)
        for first,second in (("load_inputs","train_one"),("new_baseline","train_one"),("train_one","save"),
                             ("save","load_bundle"),("load_bundle","replay_one")):
            self.assertLess(line(first),line(second))

    def test_23_runner_cli_parser_and_parent_paths(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c241.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c241.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript)
                and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute)
                and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1,2});self.assertEqual(argv(blocks[2]),{1,2,3,4})
        self.assertLess(launcher.index("::ParseFile"),launcher.index("$failure = $null"))
        self.assertIn("c240-v5b-saved-position-audit-4b604be67f5b47f0b18cabdb2513d12d",launcher)
        self.assertIn("c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5",launcher)

    def test_24_semantic_own_count_and_unrestricted_output(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"]);self.assertEqual(len(ids),len(set(ids)))
        x=torch.zeros(8,256,dtype=torch.float64);x[:,255]=1
        self.assertEqual(b.predictions([x,x,x])["normal"],[255]*8)
        self.assertEqual(b.manifest()["loaded_tests"]-b.manifest()["focused_tests"],1)


if __name__=="__main__":
    unittest.main(verbosity=2)
