"""C239 authoring checks; synthetic tests do not establish model capability."""
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
from fold_lm.v05_benchmarks import model_c239_order_holdout as b


def fixture():
    rows=[]; names={"en":("box","book"),"ja":("箱","本")}
    for x,y in ((0,1),(1,0)):
        group=f"0-1-{x}-{y}"
        for lang in names:
            for order,query in itertools.product((0,1),(0,1)):
                facts=[(0,x),(1,y)]
                if order: facts.reverse()
                text=";".join(names[lang][k]+"="+str(v) for k,v in facts)+";"+names[lang][query]+"="
                rows.append(dict(id=f"{lang}-{group}-{order}-{query}",group=group,objects=[0,1],values=[x,y],
                    language=lang,order=order,query=query,split="TRAIN",target=ord(str(x if query==0 else y)),prompt=text))
    return rows


def metrics(good=True):
    return {l:dict(rows=4,accuracy=1.0 if good else .5,answer_nll=.1 if good else .7,
        evidence_blind_accuracy=.5,query_blind_accuracy=.5,evidence_drop=.5 if good else 0,
        query_drop=.5 if good else 0,fact_pair_accuracy=1.0 if good else 0,
        query_pair_accuracy=1.0 if good else 0) for l in ("en","ja")}


def records():
    return [dict(seed=s,family=f,initial_sha256="a"*64,final_sha256="b"*64,final={k:metrics() for k in b.SPLITS},
        fit=dict(steps=400,answer_presentations=12800),forward_calls=415,row_presentations=12920,
        checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.0,weights_changed=True)
        for s,f in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(274)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        status="PASS" if summary["full_order_gate"] else "FAIL",source_blobs=pins,
        input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(418)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,network_calls=0)


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
    @staticmethod
    def evaluate(model,rows,views):
        before=model.training;model.eval()
        try:
            with torch.no_grad(): outputs=[model(x,torch.zeros(len(x),dtype=torch.int64)).detach() for x,_ in views]
        finally: model.train(before)
        pred=[x.argmax(-1).tolist() for x in outputs];out={}
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            acc=[sum(p[i]==rows[i]["target"] for i in ids)/len(ids) for p in pred]
            pairs={k:defaultdict(list) for k in ("facts","query")}
            for i in ids:
                r=rows[i];pairs["facts"][(r["order"],r["query"])].append(i);pairs["query"][(r["group"],r["order"])].append(i)
            values={k:sum(all(pred[0][i]==rows[i]["target"] for i in p) for p in groups.values())/len(groups) for k,groups in pairs.items()}
            out[lang]=dict(rows=len(ids),accuracy=acc[0],answer_nll=float(F.cross_entropy(outputs[0][ids],views[0][1][ids])),
                evidence_blind_accuracy=acc[1],query_blind_accuracy=acc[2],evidence_drop=acc[0]-acc[1],query_drop=acc[0]-acc[2],
                fact_pair_accuracy=values["facts"],query_pair_accuracy=values["query"])
        return out,outputs


class C239Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.pool=fixture();cls.parts=b.split_pool(cls.pool)

    def exercise(self):
        model=Factory.new_model(9010);ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model))
        with contextlib.redirect_stdout(io.StringIO()):
            return b.train_one(model,self.parts,ref,binding=Binding,factory=Factory)

    def test_01_manifest_and_pool_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.pool),b.PARENT_ARTIFACTS["probe-dataset.json"])
        self.assertEqual(b.digest(self.parts),b.SPLIT_SHA)

    def test_02_split_disjoint_and_balanced(self):
        for key,order in zip(b.SPLITS,(0,1),strict=True):
            part=self.parts[key];self.assertEqual(len(part),8);self.assertEqual({r["order"] for r in part},{order})
            self.assertEqual(Counter((r["language"],r["target"]) for r in part),{(l,t):2 for l in ("en","ja") for t in (48,49)})
        for key in ("id","prompt"):
            self.assertFalse({r[key] for r in self.parts["TRAIN"]}&{r[key] for r in self.parts["HOLDOUT"]})

    def test_03_shared_fact_groups_are_intentional(self):
        self.assertEqual({r["group"] for r in self.parts["TRAIN"]},{r["group"] for r in self.parts["HOLDOUT"]})
        self.assertTrue(all(r["split"]=="TRAIN" for r in self.pool))

    def test_04_split_tamper_rejected(self):
        for key,value in (("order",1),("target",255),("split","EVAL")):
            p=copy.deepcopy(self.pool);p[0][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError):b.split_pool(p)

    def test_05_batch_contains_train8_four_times(self):
        ids=b.balanced_indices(8);self.assertEqual(ids.tolist(),list(range(8))*4)
        self.assertEqual(Counter(ids.tolist()),{i:4 for i in range(8)})

    def test_06_bad_sampler_count_rejected(self):
        for n in (0,16,True,8.0):
            with self.assertRaises(ValueError):b.balanced_indices(n)

    def test_07_real_parent_fit_ast_contract(self):
        parent=b.parent_module();b.audit_fit_contract(parent)
        with patch.object(parent,"LR",.1):
            with self.assertRaises(ValueError):b.audit_fit_contract(parent)

    def test_08_metric_schema_not_parent_count(self):
        b.validate_metrics(metrics());bad=metrics();bad["en"]["rows"]=8
        with self.assertRaises(ValueError):b.validate_metrics(bad)

    def test_09_nonfinite_and_drop_semantics(self):
        for key,value in (("answer_nll",float("nan")),("query_drop",0),("accuracy",2)):
            m=metrics();m["en"][key]=value
            with self.assertRaises(ValueError):b.validate_metrics(m)

    def test_10_primary_and_gru_gate_are_separate(self):
        r=records();r[0]["final"]["HOLDOUT"]=metrics(False)
        s=b.summarize(r);self.assertFalse(s["full_order_gate"]);self.assertTrue(s["gru_order_gate"])
        p=payload(s);b.validate_result(p);self.assertEqual(p["status"],"FAIL")

    def test_11_train_failure_separate_from_order_miss(self):
        r=records();r[0]["final"]["TRAIN"]=metrics(False);r[1]["final"]["HOLDOUT"]=metrics(False)
        s=b.summarize(r);self.assertEqual(s["cell_outcomes"],{"TRAIN_FIT_MISS":2,"ORDER_HOLDOUT_MISS":2,"BOTH_PASS":8})

    def test_12_all_pass_workload_and_scope(self):
        s=b.summarize(records());b.validate_result(payload(s))
        self.assertEqual((s["model_forward_calls"],s["total_row_presentations"]),(2490,77520))
        self.assertFalse(s["general_language_claim"])

    def test_13_replay_and_protection_faults_invalid(self):
        r=records();r[0]["reload_max_error"]=.1
        with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r)))
        p=payload(b.summarize(records()));p["source_blobs"].pop(b.OWN[0])
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_14_actual_fit_observed_batch_membership(self):
        x,y=Binding.tensors(self.parts["TRAIN"],"normal");model=Factory.new_model(9011);seen=[]
        handle=model.register_forward_pre_hook(lambda module,args:seen.append(args[0].clone()))
        b.fit(model,x,y,9012,steps=2);handle.remove()
        self.assertEqual(len(seen),2);self.assertTrue(all(torch.equal(batch,x.repeat(4,1)) for batch in seen))
        self.assertTrue(all(bool((batch[:,2]==0).all()) for batch in seen))

    def test_15_holdout_rendered_only_after_fit(self):
        model=Factory.new_model(9010);ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model))
        completed=[False];native=b.fit
        def fitted(*args,**kwargs):
            value=native(*args,**kwargs);completed[0]=True;return value
        class Checked(Binding):
            @staticmethod
            def tensors(rows,mode):
                if any(r["order"]==1 for r in rows):
                    if not completed[0]:raise AssertionError("holdout reached evaluator before training endpoint")
                return Binding.tensors(rows,mode)
        with patch.object(b,"fit",side_effect=fitted),contextlib.redirect_stdout(io.StringIO()):
            r,_,_=b.train_one(model,self.parts,ref,binding=Checked,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(409,12872))

    def test_16_initial_mismatch_stops_before_training(self):
        with patch.object(b,"fit") as fitted:
            with self.assertRaises(ValueError):b.train_one(Factory.new_model(9010),self.parts,dict(initial_sha256="wrong"),binding=Binding,factory=Factory)
            fitted.assert_not_called()

    def test_17_actual_checkpoint_replay_counts(self):
        r,state,raw=self.exercise();b.replay_one(Factory.new_model(9010),state,r,raw,self.parts,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,12920));self.assertTrue(r["checkpoint_roundtrip"])

    def test_18_changed_logits_rejected(self):
        r,state,raw=self.exercise();raw["HOLDOUT"][0]=raw["HOLDOUT"][0]+.1
        with self.assertRaises(ValueError):b.replay_one(Factory.new_model(9010),state,r,raw,self.parts,binding=Binding,factory=Factory)

    def test_19_checkpoint_schema_and_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"model.pt";value=dict(schema="fold-c239-order-holdout-v1",identities=[list(x) for x in b.identities()],states=[{}]*6)
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),6)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    def test_20_actual_loader_uses_initial_not_final(self):
        refs=[dict(seed=s,family=f,initial_sha256="a"*64,final_sha256="b"*64,initial_probe={},final_probe={}) for s,f in b.identities()]
        class Audit:
            @staticmethod
            def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
        parent=SimpleNamespace(summarize=lambda r,**kw:{"models":len(r)})
        fitting=SimpleNamespace(validate_metrics=lambda m:None)
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(parent,fitting,None,None,Audit)):
            root=Path(tmp)
            for name,value in (("probe-dataset.json",self.pool),("measurements.json",refs),("summary.json",dict(validation_summary={"models":6}))):
                (root/name).write_bytes(b.blob(value))
            parts,saved=b.load_inputs(root/"summary.json");self.assertEqual(parts,self.parts);self.assertEqual(saved,refs)
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
                p=(Path(root)/name).resolve()
                if p.parent!=Path(root).resolve():raise ValueError("unsafe child")
                return p
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(None,None,Binding,Factory,Audit)), \
            patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
            patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader:
            out=Path(tmp)/"out";parent=Path(tmp)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c238_summary=parent,output_dir=out,expected_head="synthetic-head")
            self.assertEqual(pre.call_count,2);loader.assert_called_once()
            p,r=b.verify_artifacts(out,parent,"synthetic-head");self.assertEqual(p,result);self.assertEqual(len(r),6)
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,"wrong")
            (out/"split-dataset.json").write_text("{}",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,"synthetic-head")

    def test_22_run_loader_and_common_copy_order(self):
        tree=ast.parse(inspect.getsource(b.run))
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
            for n in ast.walk(tree) if isinstance(n,ast.Call)]
        line=lambda name:min(i for i,k in calls if k==name)
        for first,second in (("load_inputs","train_one"),("new_baseline","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):
            self.assertLess(line(first),line(second))
        self.assertEqual(set(inspect.signature(b.fit).parameters),{"model","train_tokens","train_targets","seed","steps"})

    def test_23_runner_cli_and_parser(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c239.ps1").read_text(encoding="utf-8");launch=(root/"tools/invoke_c239.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c238-v5b-complete-cohort-sampler-df6538e306784434bdcbb2848e4c278d",launch)

    def test_24_semantic_test_count_and_unrestricted_output(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"]);self.assertEqual(len(ids),len(set(ids)))
        x=torch.zeros(8,256,dtype=torch.float64);x[:,255]=1
        self.assertEqual(b.predictions([x,x,x])["normal"],[255]*8)
        self.assertEqual(b.manifest()["loaded_tests"]-b.manifest()["focused_tests"],1)


if __name__=="__main__":unittest.main(verbosity=2)
