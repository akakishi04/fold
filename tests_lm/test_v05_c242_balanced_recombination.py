"""C242 authoring tests: synthetic data/models are not scientific result evidence."""
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
from fold_lm.v05_benchmarks import model_c242_balanced_recombination as b


class Binding:
    names={"en":("box","book","ball","umbrella"),"ja":("箱","本","玉","傘")}
    @staticmethod
    def render(r,mode="normal"):
        facts=list(zip(r["objects"],r["values"],strict=True))
        if r["order"]:facts.reverse()
        n=Binding.names[r["language"]]
        text=";".join(n[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)
        return text+";"+("?" if mode=="query_blind" else n[r["query"]])+"="
    @staticmethod
    def validate_dataset(data):
        b.require(b.digest(data)==b.DATA_SHA,"fixture source mismatch")
    @staticmethod
    def tensors(rows,mode):
        x=torch.tensor([[*r["values"],r["query"],r["order"]] for r in rows],dtype=torch.float64)
        if mode=="evidence_blind":x[:,:2]=0
        if mode=="query_blind":x[:,2]=.5
        return x,torch.tensor([r["target"] for r in rows])
    @staticmethod
    def evaluate(model,rows,views):
        old=model.training;model.eval()
        try:
            with torch.no_grad():logits=[model(x,torch.zeros(len(x),dtype=torch.int64)).detach() for x,_ in views]
        finally:model.train(old)
        pred=[x.argmax(-1).tolist() for x in logits];out={}
        for l in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==l]
            acc=[sum(p[i]==rows[i]["target"] for i in ids)/len(ids) for p in pred]
            pairs={k:defaultdict(list) for k in ("fact","query")}
            for i in ids:
                r=rows[i]
                pairs["fact"][(tuple(sorted(r["values"])),r["order"],r["query"])].append(i)
                pairs["query"][(r["group"],r["order"])].append(i)
            rates={k:sum(all(pred[0][i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups) for k,groups in pairs.items()}
            out[l]=dict(rows=len(ids),accuracy=acc[0],answer_nll=float(F.cross_entropy(logits[0][ids],views[0][1][ids])),
                evidence_blind_accuracy=acc[1],query_blind_accuracy=acc[2],evidence_drop=acc[0]-acc[1],query_drop=acc[0]-acc[2],
                fact_pair_accuracy=rates["fact"],query_pair_accuracy=rates["query"])
        return out,logits
    @staticmethod
    def parent_module():return Binding
    @staticmethod
    def new_baseline(full):
        model=Toy(10160);model.linear.load_state_dict(copy.deepcopy(full.linear.state_dict()));return model


def fixture():
    data=[]
    for a,c in itertools.combinations(range(4),2):
        for x,y in itertools.permutations(range(4),2):
            group=f"{a}-{c}-{x}-{y}"
            split="EVAL" if tuple(sorted((x,y))) in ((0,3),(1,2)) else "TRAIN"
            for l in Binding.names:
                for order,q in itertools.product((0,1),(a,c)):
                    r=dict(id=f"{l}-{group}-{order}-{q}",group=group,objects=[a,c],values=[x,y],language=l,
                        order=order,query=q,split=split,target=48+(x if q==a else y))
                    r["prompt"]=Binding.render(r);data.append(r)
    return data


class Toy(torch.nn.Module):
    def __init__(self,count=13488):
        super().__init__();self.linear=torch.nn.Linear(4,256).double()
        self.padding=torch.nn.Parameter(torch.zeros(count-1280,dtype=torch.float64))
    def forward(self,tokens,tasks):return self.linear(tokens)


class Factory:
    @staticmethod
    def new_model(seed):torch.manual_seed(seed);return Toy()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for k,v in sorted(model.state_dict().items()):h.update(k.encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Audit:
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"):return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def safe_child(root,name):
        path=(Path(root)/name).resolve()
        if path.parent!=Path(root).resolve():raise ValueError("unsafe child")
        return path
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
        if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def metric(n,good=True):
    return {l:dict(rows=n//2,accuracy=1.0 if good else .25,answer_nll=.1 if good else 2.0,
        evidence_blind_accuracy=.25,query_blind_accuracy=.5,evidence_drop=.75 if good else 0,
        query_drop=.5 if good else -.25,fact_pair_accuracy=1.0 if good else 0,
        query_pair_accuracy=1.0 if good else 0,order_pair_accuracy=1.0 if good else 0) for l in ("en","ja")}


def records():
    return [dict(seed=s,family=f,initial_sha256="a"*64,final_sha256="b"*64,
        final={k:metric(n) for k,n in b.ROWS.items()},fit=dict(steps=400,answer_presentations=12800),
        forward_calls=415,row_presentations=13472,checkpoint_roundtrip=True,prediction_replayed=True,
        reload_max_error=0.,weights_changed=True) for s,f in b.identities()]


def payload(s):
    pins={f"parent-{i}":"fixture" for i in range(292)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        status="PASS" if s["full_recombination_gate"] else "FAIL",source_blobs=pins,
        input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(454)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,network_calls=0)


class C242Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.data=fixture();cls.parts=b.split_data(cls.data,Binding)
    def exercise(self):
        model=Factory.new_model(9010);ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model))
        with contextlib.redirect_stdout(io.StringIO()):return b.train_one(model,self.parts,ref,binding=Binding,factory=Factory)

    def test_01_manifest_and_exact_data_hashes(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA);self.assertEqual(b.digest(self.parts),b.SPLIT_SHA)
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
    def test_02_coverage_and_disjoint_pairs(self):
        self.assertEqual({k:len(v) for k,v in self.parts.items()},b.ROWS)
        self.assertEqual({tuple(r["values"]) for r in self.parts["TRAIN"]},set(b.TRAIN_PAIRS))
        for k in ("id","prompt","group"):
            self.assertFalse({r[k] for r in self.parts["TRAIN"]}&{r[k] for r in self.parts["HOLDOUT"]})
    def test_03_masks_remove_necessary_information(self):
        for rows in self.parts.values():
            self.assertEqual(b.input_ceiling(rows,lambda r:Binding.render(r,"evidence_blind")),.25)
            self.assertEqual(b.input_ceiling(rows,lambda r:Binding.render(r,"query_blind")),.5)
    def test_04_each_entity_changes_values_and_positions(self):
        rows=self.parts["TRAIN"]
        self.assertEqual(Counter((r["language"],r["query"],r["order"],r["target"]) for r in rows),
            {k:1 for k in itertools.product(("en","ja"),(0,1),(0,1),range(48,52))})
    def test_05_tampered_source_is_rejected(self):
        data=copy.deepcopy(self.data);data[0]["target"]=255
        with self.assertRaises(ValueError):b.split_data(data,Binding)
    def test_06_batch_all32_once(self):
        self.assertEqual(b.balanced_indices(32).tolist(),list(range(32)))
        for n in (8,16,True,32.0):
            with self.assertRaises(ValueError):b.balanced_indices(n)
    def test_07_real_parent_fit_ast_contract(self):
        parent=b.parent_module();b.audit_fit_contract(parent)
        with patch.object(parent,"LR",.1):
            with self.assertRaises(ValueError):b.audit_fit_contract(parent)
    def test_08_metrics_validate_both_sizes(self):
        for n in (32,64):b.validate_metrics(metric(n),n)
        with self.assertRaises(ValueError):b.validate_metrics(metric(32),64)
    def test_09_schema_nonfinite_and_drop_faults(self):
        for k,v in (("answer_nll",float("nan")),("evidence_drop",0),("accuracy",2)):
            m=metric(32);m["en"][k]=v
            with self.assertRaises(ValueError):b.validate_metrics(m,32)
    def test_10_primary_and_baseline_independent(self):
        r=records();r[0]["final"]["HOLDOUT"]=metric(64,False);s=b.summarize(r)
        self.assertFalse(s["full_recombination_gate"]);self.assertTrue(s["gru_recombination_gate"]);b.validate_result(payload(s))
    def test_11_train_criterion_failure_not_accuracy_claim(self):
        r=records();m=r[0]["final"]["TRAIN"]
        for cell in m.values():cell.update(evidence_blind_accuracy=1.,evidence_drop=0.)
        s=b.summarize(r);self.assertEqual(s["cell_outcomes"]["TRAIN_CRITERIA_MISS"],2)
        self.assertEqual(m["en"]["accuracy"],1.)
    def test_12_fixed_total_workload(self):
        s=b.summarize(records());b.validate_result(payload(s))
        self.assertEqual((s["train_steps"],s["answer_presentations"],s["model_forward_calls"],s["row_presentations"]),(2400,76800,2490,80832))
    def test_13_replay_or_missing_work_invalid(self):
        for k,v in (("reload_max_error",.1),("forward_calls",414),("weights_changed",False)):
            r=records();r[0][k]=v
            with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r)))
    def test_14_actual_fit_batch_membership(self):
        model=Factory.new_model(9011);x,y=Binding.tensors(self.parts["TRAIN"],"normal");seen=[]
        h=model.register_forward_pre_hook(lambda m,args:seen.append(args[0].clone()))
        b.fit(model,x,y,9012,steps=2);h.remove()
        self.assertEqual(len(seen),2);self.assertTrue(all(torch.equal(a,x) for a in seen))
    def test_15_holdout_never_reaches_fit_or_early_eval(self):
        done=[False];native_fit=b.fit;native_eval=b.evaluate
        def fitted(model,x,y,seed):
            self.assertEqual(len(x),32);out=native_fit(model,x,y,seed);done[0]=True;return out
        def checked(model,rows,binding,fingerprint):
            if len(rows)==64:self.assertTrue(done[0])
            return native_eval(model,rows,binding,fingerprint)
        with patch.object(b,"fit",side_effect=fitted),patch.object(b,"evaluate",side_effect=checked):self.exercise()
    def test_16_wrong_initial_state_stops_before_fit(self):
        with patch.object(b,"fit") as f:
            with self.assertRaises(ValueError):b.train_one(Factory.new_model(1),self.parts,{"initial_sha256":"wrong"},binding=Binding,factory=Factory)
            f.assert_not_called()
    def test_17_actual_train_and_replay_counts(self):
        r,state,raw=self.exercise();self.assertEqual((r["forward_calls"],r["row_presentations"]),(409,13184))
        b.replay_one(Factory.new_model(9010),state,r,raw,self.parts,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,13472))
    def test_18_changed_logits_rejected(self):
        r,state,raw=self.exercise();raw["HOLDOUT"][0]=raw["HOLDOUT"][0]+.1
        with self.assertRaises(ValueError):b.replay_one(Factory.new_model(9010),state,r,raw,self.parts,binding=Binding,factory=Factory)
    def test_19_bundle_schema_order(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"states.pt";v=dict(schema="fold-c242-recombination-v1",identities=[list(x) for x in b.identities()],states=[{}]*6)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),6)
            v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)
    def test_20_actual_loader_uses_initial_parent_fields(self):
        refs=records();parent=SimpleNamespace(summarize=lambda r:{"models":len(r)})
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,Binding,None,Audit)):
            root=Path(d)
            for name,v in (("data.json",self.data),("measurements.json",refs),("summary.json",dict(validation_summary={"models":6}))):(root/name).write_bytes(b.blob(v))
            parts,saved=b.load_inputs(root/"summary.json",root/"data.json");self.assertEqual(parts,self.parts);self.assertEqual(saved,refs)
            refs[0]["initial_sha256"]=refs[0]["final_sha256"];(root/"measurements.json").write_bytes(b.blob(refs))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json",root/"data.json")
    def test_21_six_model_run_and_persisted_postcheck(self):
        refs=[]
        for s,f in b.identities():
            model=Factory.new_model(s)
            if f=="gru_only":model=Binding.new_baseline(model)
            refs.append(dict(seed=s,family=f,initial_sha256=Factory.fingerprint(model)))
        base=payload(b.summarize(records()))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,Binding,Factory,Audit)), \
             patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader:
            out=Path(d)/"out";parent=Path(d)/"parent.json";data=Path(d)/"data.json"
            with contextlib.redirect_stdout(io.StringIO()):p=b.run(c241_summary=parent,c234_dataset=data,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,parent,data,"synthetic-head")[0],p)
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,data,"wrong")
            (out/"split-dataset.json").write_text("{}",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,data,"synthetic-head")
    def test_22_dispatch_copy_save_replay_order(self):
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
            for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        line=lambda name:min(i for i,k in calls if k==name)
        for a,c in (("load_inputs","train_one"),("new_baseline","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):
            self.assertLess(line(a),line(c))
    def test_23_runner_embedded_cli_and_parser(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c242.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c242.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(s):
            return {n.slice.value for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1,2});self.assertEqual(argv(blocks[2]),{1,2,3,4})
        self.assertLess(l.index("::ParseFile"),l.index("$failure = $null"))
        self.assertIn("c241-v5b-assignment-holdout-445ca70720c948e7966236416922e580",l)
        self.assertIn("c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200",l)
    def test_24_own_loader_count_and_unrestricted_output(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"]);self.assertEqual(len(ids),len(set(ids)))
        x=torch.zeros(32,256,dtype=torch.float64);x[:,255]=1
        self.assertEqual(b.prediction_record([x,x,x],32)["normal"],[255]*32)


if __name__=="__main__":unittest.main(verbosity=2)
