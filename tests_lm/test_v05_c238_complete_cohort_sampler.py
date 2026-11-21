"""C238 authoring tests; synthetic toy work is not a scientific model result."""
import ast
from collections import Counter
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
from fold_lm.v05_benchmarks import model_c236_minimal_binding as old
from fold_lm.v05_benchmarks import model_c237_frozen_signal_audit as signal
from fold_lm.v05_benchmarks import model_c238_complete_cohort_sampler as b


def fixture():
    rows=[];names={"en":("box","book"),"ja":("箱","本")}
    for x,y in ((0,1),(1,0)):
        group=f"0-1-{x}-{y}"
        for lang in names:
            for order,query in itertools.product((0,1),(0,1)):
                facts=[(0,x),(1,y)]
                if order: facts.reverse()
                prompt=";".join(names[lang][k]+"="+str(v) for k,v in facts)+";"+names[lang][query]+"="
                rows.append(dict(id=f"{lang}-{group}-{order}-{query}",group=group,objects=[0,1],
                    values=[x,y],language=lang,order=order,query=query,split="TRAIN",
                    target=ord(str(x if query==0 else y)),prompt=prompt))
    return rows


def metrics(perfect=False):
    return {lang:dict(rows=8,accuracy=1.0 if perfect else .5,answer_nll=.1 if perfect else .7,
        evidence_blind_accuracy=.5,query_blind_accuracy=.5,evidence_drop=.5 if perfect else 0.0,
        query_drop=.5 if perfect else 0.0,fact_pair_accuracy=1.0 if perfect else 0.0,
        query_pair_accuracy=1.0 if perfect else 0.0) for lang in ("en","ja")}


def records():
    return [dict(seed=seed,family=family,initial_sha256="a"*64,final_sha256="b"*64,
        initial_probe=metrics(),final_probe=metrics(),initial_replay_error=0.0,
        checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.0,replay_metric_error=0.0,
        weights_changed=True,fit=dict(steps=400,answer_presentations=12800),forward_calls=409,
        row_presentations=12944,predictions={mode:[48]*16 for mode in b.VIEWS},comparator_final=metrics())
        for seed,family in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(268)};pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(406)},
        artifacts=[dict(file=name) for name in b.OUTPUTS],validation_summary=summary,
        status="PASS" if summary["full_probe_gate"] else "FAIL",gate_f_candidate=False,network_calls=0)


class Toy(torch.nn.Module):
    def __init__(self,total=13488):
        super().__init__();self.linear=torch.nn.Linear(4,256).double()
        self.padding=torch.nn.Parameter(torch.zeros(total-1280,dtype=torch.float64))
    def forward(self,tokens,tasks): return self.linear(tokens)


class Factory:
    @staticmethod
    def new_model(seed):
        torch.manual_seed(seed);return Toy()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for name,value in sorted(model.state_dict().items()):
            h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    @staticmethod
    def new_baseline(full):
        model=Toy(10160);model.linear.load_state_dict(copy.deepcopy(full.linear.state_dict()))
        return model
    @staticmethod
    def parent_module():return Binding
    @staticmethod
    def tensors(rows,mode):
        x=torch.tensor([[r["values"][0],r["query"],r["order"],int(r["language"]=="ja")]
            for r in rows],dtype=torch.float64)
        if mode=="evidence_blind":x[:,0]=0.5
        if mode=="query_blind":x[:,1]=0.5
        return x,torch.tensor([r["target"] for r in rows])
    @staticmethod
    def evaluate(model,rows,views):
        training=model.training;model.eval()
        try:
            with torch.no_grad():
                logits=[model(x,torch.zeros(len(x),dtype=torch.int64)).detach() for x,_ in views]
        finally:model.train(training)
        predictions=[x.argmax(-1).tolist() for x in logits];result={}
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            acc=[sum(pred[i]==rows[i]["target"] for i in ids)/len(ids) for pred in predictions]
            pairs={kind:{} for kind in ("facts","query")}
            for i in ids:
                r=rows[i]
                pairs["facts"].setdefault((r["order"],r["query"]),[]).append(i)
                pairs["query"].setdefault((r["group"],r["order"]),[]).append(i)
            paired={kind:sum(all(predictions[0][i]==rows[i]["target"] for i in pair)
                    for pair in groups.values())/len(groups) for kind,groups in pairs.items()}
            result[lang]=dict(rows=8,accuracy=acc[0],answer_nll=float(F.cross_entropy(logits[0][ids],views[0][1][ids])),
                evidence_blind_accuracy=acc[1],query_blind_accuracy=acc[2],evidence_drop=acc[0]-acc[1],
                query_drop=acc[0]-acc[2],fact_pair_accuracy=paired["facts"],query_pair_accuracy=paired["query"])
        return result,logits


class C238Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.rows=fixture();cls.views=[Binding.tensors(cls.rows,mode) for mode in b.VIEWS]

    def exercise(self):
        model=Factory.new_model(9010);initial,_=Binding.evaluate(model,self.rows,self.views)
        rec=records()[0];rec.update(seed=9010,initial_sha256=Factory.fingerprint(model),initial_probe=initial)
        with contextlib.redirect_stdout(io.StringIO()):
            record,state,reference=b.train_one(model,rows=self.rows,views=self.views,reference=rec,
                fitting=old,binding=Binding,factory=Factory)
        return record,state,reference

    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertFalse(b.manifest()["general_language_claim"])
        self.assertFalse(b.manifest()["held_out_generalization_claim"])

    def test_02_unchanged_cohort_hash(self):
        self.assertEqual(b.digest(self.rows),b.PROBE_SHA)
        self.assertEqual(Counter(r["language"] for r in self.rows),{"en":8,"ja":8})

    def test_03_complete_batch_exact_coverage(self):
        ids=b.balanced_indices(16)
        self.assertEqual(ids.tolist(),list(range(16))*2)
        self.assertTrue(torch.equal(torch.bincount(ids,minlength=16),torch.full((16,),2)))
        self.assertEqual(Counter(self.rows[i]["target"] for i in ids.tolist()),{48:16,49:16})

    def test_04_bad_cohort_count_rejected(self):
        for n in (0,8,17,True,16.0):
            with self.subTest(count=n):
                with self.assertRaises(ValueError):b.balanced_indices(n)

    def test_05_total_presentations_and_gate_unchanged(self):
        m=b.manifest();self.assertEqual(m["row_presentations_per_model"],[800]*16)
        self.assertEqual((m["total_training_steps"],m["total_answer_presentations"]),(2400,76800))
        self.assertTrue(old.probe_pass(metrics(True)));self.assertFalse(old.probe_pass(metrics()))

    def test_06_actual_parent_training_ast_delta(self):
        b.audit_fit_contract(old)
        with patch.object(old,"LR",old.LR*2):
            with self.assertRaises(ValueError):b.audit_fit_contract(old)

    def test_07_loss_change_is_rejected_by_ast_audit(self):
        source=inspect.getsource(old.fit).replace("loss.backward()","(loss*2).backward()")
        native=inspect.getsource
        with patch.object(b.inspect,"getsource",side_effect=lambda fn:source if fn is old.fit else native(fn)):
            with self.assertRaises(ValueError):b.audit_fit_contract(old)

    def test_08_parent_comparator_adapter(self):
        r=records();summary=old.summarize(r)
        self.assertEqual(len(b.validate_comparator(r,summary,parent=signal,fitting=old)),6)
        r[0]["final_probe"]["en"]=metrics(True)["en"]
        with self.assertRaises(ValueError):b.validate_comparator(r,old.summarize(r),parent=signal,fitting=old)

    def test_09_bad_initial_or_comparator_summary_rejected(self):
        r=records();r[0]["initial_sha256"]="not-a-hash"
        with self.assertRaises(ValueError):b.validate_comparator(r,old.summarize(r),parent=signal,fitting=old)
        r=records();summary=old.summarize(r);summary["models"]=5
        with self.assertRaises(ValueError):b.validate_comparator(r,summary,parent=signal,fitting=old)

    def test_10_metric_contract_nonfinite_and_keys(self):
        self.assertEqual(b.metric_error(metrics(),metrics()),0)
        for key,value in (("answer_nll",float("nan")),("unexpected",0)):
            m=metrics();m["en"][key]=value
            with self.assertRaises(ValueError):b.metric_error(m,metrics())

    def test_11_valid_negative_and_independent_baseline(self):
        r=records()
        for item in r:
            if item["family"]=="gru_only":item["final_probe"]=metrics(True)
        s=b.summarize(r,fitting=old)
        self.assertFalse(s["full_probe_gate"]);self.assertTrue(s["gru_probe_gate"])
        b.validate_result(payload(s));self.assertEqual(payload(s)["status"],"FAIL")

    def test_12_primary_pass_remains_bounded(self):
        r=records()
        for item in r:item["final_probe"]=metrics(True)
        p=payload(b.summarize(r,fitting=old));b.validate_result(p)
        self.assertEqual(p["status"],"PASS");self.assertFalse(p["gate_f_candidate"])

    def test_13_invalid_replay_not_valid_negative(self):
        for key,value in (("initial_replay_error",.1),("reload_max_error",.1),("forward_calls",408)):
            r=records();r[0][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r,fitting=old)))

    def test_14_missing_source_is_invalid(self):
        p=payload(b.summarize(records(),fitting=old));p["source_blobs"].pop(b.OWN[0])
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_15_actual_fit_uses_complete_batch_each_step(self):
        x=torch.arange(64,dtype=torch.float64).reshape(16,4)/64;y=torch.tensor([48,49]*8)
        model=Factory.new_model(9011);seen=[]
        handle=model.register_forward_pre_hook(lambda module,args:seen.append(args[0].clone()))
        b.fit(model,x,y,9012,steps=2);handle.remove()
        self.assertEqual(len(seen),2)
        self.assertTrue(all(torch.equal(batch,torch.cat((x,x))) for batch in seen))

    def test_16_deterministic_fit_and_nonfinite_rejection(self):
        a=Factory.new_model(9013);c=copy.deepcopy(a)
        b.fit(a,*self.views[0],9014,steps=2);b.fit(c,*self.views[0],9014,steps=2)
        self.assertEqual(Factory.fingerprint(a),Factory.fingerprint(c))
        x=self.views[0][0].clone();x[0,0]=float("nan")
        with self.assertRaises(ValueError):b.fit(Factory.new_model(9015),x,self.views[0][1],9016,steps=1)

    def test_17_actual_train_and_parent_replay_counts(self):
        rec,state,reference=self.exercise()
        self.assertEqual((rec["forward_calls"],rec["row_presentations"]),(406,12896))
        old.replay_one(Factory.new_model(9010),state,rec,reference,binding=Binding,factory=Factory,rows=self.rows,views=self.views)
        self.assertEqual((rec["forward_calls"],rec["row_presentations"]),(409,12944))
        self.assertEqual(rec["initial_replay_error"],0)

    def test_18_initial_mismatch_rejected_before_fit(self):
        model=Factory.new_model(9010);rec=records()[0]
        with self.assertRaises(ValueError),patch.object(b,"fit") as fitted:
            b.train_one(model,rows=self.rows,views=self.views,reference=rec,fitting=old,binding=Binding,factory=Factory)
        fitted.assert_not_called()

    def test_19_checkpoint_schema_and_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"models.pt"
            value=dict(schema="fold-c238-complete-cohort-v1",identities=[list(x) for x in b.identities()],states=[{} for _ in range(6)])
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),6)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    def test_20_actual_loader_uses_c236_initial_and_recorded_final(self):
        class Audit:
            @staticmethod
            def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
        r=records()
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(signal,old,None,None,Audit)):
            root=Path(tmp)
            (root/"probe-dataset.json").write_bytes(b.blob(self.rows))
            (root/"measurements.json").write_bytes(b.blob(r))
            (root/"summary.json").write_bytes(b.blob(dict(validation_summary=old.summarize(r))))
            rows,saved=b.load_inputs(root/"summary.json")
            self.assertEqual(rows,self.rows);self.assertEqual(saved,r)
            rows[0]["target"]=255;(root/"probe-dataset.json").write_bytes(b.blob(rows))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_21_synthetic_six_model_run_and_artifact_postcheck(self):
        comparators=records()
        for index,(seed,family) in enumerate(b.identities()):
            model=Factory.new_model(seed)
            if family=="gru_only":model=Binding.new_baseline(model)
            comparators[index]["initial_sha256"]=Factory.fingerprint(model)
            comparators[index]["initial_probe"]=Binding.evaluate(model,self.rows,self.views)[0]
        base=payload(b.summarize(records(),fitting=old))
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
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(signal,old,Binding,Factory,Audit)), \
            patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
            patch.object(b,"load_inputs",return_value=(self.rows,comparators)) as loader:
            out=Path(tmp)/"out"
            with contextlib.redirect_stdout(io.StringIO()):
                result=b.run(c237_summary=Path(tmp)/"c237.json",c236_summary=Path(tmp)/"c236.json",output_dir=out,expected_head="synthetic-head")
            self.assertEqual(pre.call_count,2);loader.assert_called_once()
            verified,recs=b.verify_artifacts(out,Path(tmp)/"c236.json","synthetic-head")
            self.assertEqual(verified,result);self.assertEqual(len(recs),6)
            self.assertEqual(result["validation_summary"]["model_forward_calls"],2454)
            with self.assertRaises(ValueError):b.verify_artifacts(out,Path(tmp)/"c236.json","wrong-head")
            (out/"probe-dataset.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,Path(tmp)/"c236.json","synthetic-head")

    def test_22_actual_run_common_copy_and_loader_order(self):
        tree=ast.parse(inspect.getsource(b.run))
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
            for n in ast.walk(tree) if isinstance(n,ast.Call)]
        line=lambda name:min(n for n,k in calls if k==name)
        self.assertLess(line("load_inputs"),line("train_one"))
        self.assertLess(line("new_baseline"),line("train_one"))
        self.assertLess(line("train_one"),line("save"))
        self.assertLess(line("save"),line("load_bundle"))
        self.assertLess(line("load_bundle"),line("replay_one"))
        called={n.func.id for n in ast.walk(ast.parse(inspect.getsource(b.precheck))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertIn("audit_fit_contract",called)

    def test_23_runner_embedded_python_and_parser(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c238.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c238.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name)
                and n.value.value.id=="sys" and n.value.attr=="argv" and isinstance(n.slice,ast.Constant)}
        self.assertEqual(argv(blocks[0]),{1,2});self.assertEqual(argv(blocks[2]),{1,2,3,4})
        self.assertLess(launcher.index("::ParseFile"),launcher.index("$failure = $null"))
        self.assertIn("c237-v5b-frozen-signal-audit-8dbdc04fdad84f49b41a78388ad0b7fb",launcher)
        self.assertIn("c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71",launcher)

    def test_24_semantic_own_count_and_fixed_identity(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(b.identities(),old.identities())
        self.assertEqual(b.manifest()["loaded_tests"]-b.manifest()["focused_tests"],1)
        self.assertEqual((len(b.OWN),len(b.OUTPUTS)),(6,5))


if __name__=="__main__":unittest.main(verbosity=2)
