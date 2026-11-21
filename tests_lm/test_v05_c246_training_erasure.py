"""C246 authoring checks: toy models are not scientific FOLD results."""
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
from fold_lm.v05_benchmarks import model_c246_training_erasure as b


class Factory:
    @staticmethod
    def prefix_tensor(raw):
        if len(raw)>46:raise ValueError("prefix too long")
        return torch.tensor([257,*raw,258]+[256]*(46-len(raw)),dtype=torch.int64)
    @staticmethod
    def new_model(seed):torch.manual_seed(seed);return Toy(13488)
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for k,v in sorted(model.state_dict().items()):h.update(k.encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Toy(torch.nn.Module):
    def __init__(self,count):
        super().__init__();self.layer=torch.nn.Linear(3,256).double()
        self.padding=torch.nn.Parameter(torch.zeros(count-1024,dtype=torch.float64))
    def forward(self,tokens,tasks):
        x=tokens.double()/300
        return self.layer(torch.stack((x.mean(1),x[:,5],x[:,15]),dim=1))


class Binding:
    names={"en":("box","book"),"ja":("箱","本")}
    @staticmethod
    def render(r,mode="normal"):
        facts=list(zip(r["objects"],r["values"],strict=True))
        if r["order"]:facts.reverse()
        names=Binding.names[r["language"]]
        return ";".join(names[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)+";"+("?" if mode=="query_blind" else names[r["query"]])+"="
    @staticmethod
    def tensors(rows,mode):
        return torch.stack([Factory.prefix_tensor(Binding.render(r,mode).encode()) for r in rows]),torch.tensor([r["target"] for r in rows])
    @staticmethod
    def new_baseline(full):
        model=Toy(10160);model.layer.load_state_dict(copy.deepcopy(full.layer.state_dict()));return model
    @staticmethod
    def parent_module():return Binding


class Fitting:
    @staticmethod
    def prediction_record(logits,n):
        b.require(len(logits)==3 and all(x.shape==(n,256) and bool(torch.isfinite(x).all()) for x in logits),"test logits")
        return {v:x.argmax(-1).tolist() for v,x in zip(b.VIEWS,logits,strict=True)}
    @staticmethod
    def discrete_metrics(rows,pred):
        out={}
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            acc={v:sum(pred[v][i]==rows[i]["target"] for i in ids)/len(ids) for v in b.VIEWS}
            m=dict(rows=len(ids),accuracy=acc["normal"],evidence_blind_accuracy=acc["evidence_blind"],query_blind_accuracy=acc["query_blind"],
                   evidence_drop=acc["normal"]-acc["evidence_blind"],query_drop=acc["normal"]-acc["query_blind"])
            for kind in ("fact","query","order"):
                groups=defaultdict(list)
                for i in ids:
                    r=rows[i]
                    key=(tuple(sorted(r["values"])),r["order"],r["query"]) if kind=="fact" else (r["group"],r["order"] if kind=="query" else r["query"])
                    groups[key].append(i)
                b.require(all(len(g)==2 for g in groups.values()),"test pairs")
                m[kind+"_pair_accuracy"]=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
            out[lang]=m
        return out
    @staticmethod
    def validate_metrics(metrics,n):
        b.require(set(metrics)=={"en","ja"} and all(m["rows"]==n//2 for m in metrics.values()),"test metric count")
        for m in metrics.values():b.require(all(isinstance(v,(int,float)) and v==v for v in m.values()),"test metric finite")
    @staticmethod
    def cell_pass(m):
        return m["accuracy"]>=.90 and all(m[k+"_pair_accuracy"]>=.80 for k in ("fact","query","order")) and m["evidence_drop"]>=.35 and m["query_drop"]>=.35
    @staticmethod
    def evaluate(model,rows,binding,fingerprint):
        before=fingerprint(model);training=model.training;model.eval()
        views=[binding.tensors(rows,v) for v in b.VIEWS]
        try:
            with torch.no_grad():logits=[model(x,torch.zeros(len(x),dtype=torch.int64)).detach() for x,_ in views]
        finally:model.train(training)
        metrics=Fitting.discrete_metrics(rows,Fitting.prediction_record(logits,len(rows)))
        loss=F.cross_entropy(logits[0],views[0][1],reduction="none")
        for lang in metrics:metrics[lang]["answer_nll"]=float(loss[[i for i,r in enumerate(rows) if r["language"]==lang]].mean())
        b.require(fingerprint(model)==before,"test evaluation mutation")
        return metrics,logits


class Audit:
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"):return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def safe_child(root,name):
        p=(Path(root)/name).resolve()
        if p.parent!=Path(root).resolve():raise ValueError("unsafe child")
        return p
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
        if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def fixture():
    blocks={"old":[],"added":[],"held":[]}
    for x,y in itertools.permutations(range(4),2):
        block="old" if (x,y) in ((0,1),(1,0),(2,3),(3,2)) else "added" if (x,y) in ((0,2),(2,0),(1,3),(3,1)) else "held"
        group=f"0-1-{x}-{y}"
        for lang in Binding.names:
            for order,q in itertools.product((0,1),repeat=2):
                r=dict(id=f"{lang}-{group}-{order}-{q}",group=group,objects=[0,1],values=[x,y],language=lang,
                    order=order,query=q,split="EVAL" if tuple(sorted((x,y))) in ((0,3),(1,2)) else "TRAIN",target=48+(x if q==0 else y))
                r["prompt"]=Binding.render(r);blocks[block].append(r)
    return dict(TRAIN=blocks["old"]+blocks["added"],HOLDOUT=blocks["held"])


def good_metrics(n,good=True):
    return {l:dict(rows=n//2,accuracy=1. if good else .25,answer_nll=.1,evidence_blind_accuracy=.25,query_blind_accuracy=.5,
        evidence_drop=.75 if good else 0.,query_drop=.5 if good else -.25,
        fact_pair_accuracy=1. if good else 0.,query_pair_accuracy=1. if good else 0.,order_pair_accuracy=1. if good else 0.) for l in ("en","ja")}


def records():
    return [dict(seed=s,family=f,final={k:good_metrics(n) for k,n in b.ROWS.items()},fit=dict(steps=400,answer_presentations=12800),
        block_updates=[200,200],block_view_updates=[[100,100],[100,100]],forward_calls=415,row_presentations=13568,
        checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.,weights_changed=True) for s,f in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(316)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS" if summary["full_augmentation_gate"] else "FAIL",
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(502)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,network_calls=0)


class C246Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=fixture();cls.parent=b.parent_module();cls.base=cls.parent.context()[0]
    def exercise(self):
        model=Factory.new_model(9010)
        ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model),final={s:good_metrics(n) for s,n in b.ROWS.items()})
        with contextlib.redirect_stdout(io.StringIO()):
            return b.train_one(model,self.parts,ref,parent=self.parent,base=self.base,fitting=Fitting,binding=Binding,factory=Factory)
    def test_01_manifest_and_source_split(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA);self.assertEqual(b.digest(self.parts),b.SPLIT_SHA)
    def test_02_training_masks_actual_tokens(self):
        tokens,targets=b.training_tokens(self.parts,self.parent,Binding,Factory)
        self.assertEqual(tokens.shape,(64,2,48));self.assertEqual(targets.tolist(),[r["target"] for r in self.parts["TRAIN"]])
        changes=tokens[:,0]!=tokens[:,1];self.assertTrue(bool((changes.sum(1)==1).all()));self.assertTrue(bool((tokens[:,1][changes]==63).all()))
    def test_03_erasure_uses_visible_query_not_target(self):
        r=copy.deepcopy(self.parts["TRAIN"][0]);text=self.parent.masked_prompt(r,"other_value_blind",Binding);r.pop("target")
        self.assertEqual(self.parent.masked_prompt(r,"other_value_blind",Binding),text)
    def test_04_normal_holdout_remains_disjoint(self):
        train={r["prompt"] for r in self.parts["TRAIN"]}|{self.parent.masked_prompt(r,"other_value_blind",Binding) for r in self.parts["TRAIN"]}
        self.assertFalse(train & {r["prompt"] for r in self.parts["HOLDOUT"]})
        # Selectively masked HOLDOUT would collide and therefore is NOT a capability endpoint.
        self.assertEqual({self.parent.masked_prompt(r,"other_value_blind",Binding) for r in self.parts["TRAIN"]},
                         {self.parent.masked_prompt(r,"other_value_blind",Binding) for r in self.parts["HOLDOUT"]})
    def test_05_tampered_partition_rejected(self):
        parts=copy.deepcopy(self.parts);parts["TRAIN"][0]["target"]=255
        with self.assertRaises(ValueError):b.training_tokens(parts,self.parent,Binding,Factory)
    def test_06_complete_schedule_and_final_normal(self):
        exposure=Counter();tokens=torch.stack((torch.zeros(64,48),torch.ones(64,48)),dim=1)
        for step in range(400):
            ids=b.balanced_indices(64,step);view=int(b.select_view(tokens[ids],step)[0,0])
            exposure.update((i,view) for i in ids.tolist())
            self.assertTrue(torch.equal(ids,self.base.balanced_indices(64,step)))
        self.assertEqual(exposure,{(i,v):100 for i in range(64) for v in (0,1)})
        self.assertEqual(int(b.select_view(tokens[:32],399)[0,0]),0)
    def test_07_exact_parent_optimizer_ast(self):
        b.audit_fit_contract(self.base)
        with patch.object(self.base,"LR",.1):
            with self.assertRaises(ValueError):b.audit_fit_contract(self.base)
    def test_08_invalid_schedule_inputs(self):
        for n,s in ((32,0),(64,-1),(64,True)):
            with self.assertRaises(ValueError):b.balanced_indices(n,s)
        with self.assertRaises(ValueError):b.select_view(torch.zeros(32,48),0)
    def test_09_actual_optimizer_batch_cycle(self):
        tokens,targets=b.training_tokens(self.parts,self.parent,Binding,Factory);model=Factory.new_model(9011);seen=[]
        handle=model.register_forward_pre_hook(lambda m,args:seen.append(args[0].clone()))
        b.fit(model,tokens,targets,9012,steps=4);handle.remove()
        for step,batch in enumerate(seen):self.assertTrue(torch.equal(batch,tokens[self.base.balanced_indices(64,step),1-(step//2),:]))
        self.assertEqual(len(seen),4)
    def test_10_holdout_evaluation_only_after_fit(self):
        done=[False];native=b.fit
        def fitted(*args,**kwargs):value=native(*args,**kwargs);done[0]=True;return value
        class Checked(Fitting):
            @staticmethod
            def evaluate(model,rows,binding,fingerprint):
                if len(rows)==32 and not done[0]:raise AssertionError("holdout before endpoint")
                return Fitting.evaluate(model,rows,binding,fingerprint)
        model=Factory.new_model(9010);ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model),final={})
        with patch.object(b,"fit",side_effect=fitted),contextlib.redirect_stdout(io.StringIO()):
            b.train_one(model,self.parts,ref,parent=self.parent,base=self.base,fitting=Checked,binding=Binding,factory=Factory)
        self.assertTrue(done[0])
    def test_11_wrong_initial_stops_before_fit(self):
        with patch.object(b,"fit") as fit:
            with self.assertRaises(ValueError):b.train_one(Factory.new_model(1),self.parts,{"initial_sha256":"bad"},parent=self.parent,base=self.base,fitting=Fitting,binding=Binding,factory=Factory)
            fit.assert_not_called()
    def test_12_actual_forward_and_replay_accounting(self):
        r,state,raw=self.exercise();self.assertEqual((r["forward_calls"],r["row_presentations"]),(409,13280))
        self.assertEqual(r["block_view_updates"],[[100,100],[100,100]])
        self.base.replay_one(Factory.new_model(9010),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,13568))
    def test_13_modified_logits_replay_rejected(self):
        r,state,raw=self.exercise();raw["HOLDOUT"][0]=raw["HOLDOUT"][0]+.1
        with self.assertRaises(ValueError):self.base.replay_one(Factory.new_model(9010),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
    def test_14_missing_view_exposures_rejected(self):
        r=records();r[0]["block_view_updates"]=[[99,101],[100,100]]
        with self.assertRaises(ValueError):b.summarize(r,self.base,Fitting)
    def test_15_primary_and_baseline_independent(self):
        r=records();r[0]["final"]["HOLDOUT"]=good_metrics(32,False);s=b.summarize(r,self.base,Fitting)
        self.assertFalse(s["full_augmentation_gate"]);self.assertTrue(s["gru_augmentation_gate"]);b.validate_result(payload(s))
    def test_16_integrity_distinct_from_science(self):
        s=b.summarize(records(),self.base,Fitting);b.validate_result(payload(s))
        self.assertEqual(s["normal_presentations"]+s["masked_presentations"],76800)
        for key,value in (("all_replays",False),("row_presentations",1)):
            bad=copy.deepcopy(s);bad[key]=value
            with self.assertRaises(ValueError):b.validate_result(payload(bad))
    def test_17_actual_loader_initial_and_comparator_fields(self):
        refs=[dict(seed=s,family=f,initial_sha256="a"*64,final_sha256="b"*64,final={}) for s,f in b.identities()]
        with patch.object(b,"context",return_value=(self.parent,self.base,Fitting,Binding,Factory,Audit)),patch.object(self.parent,"load_inputs",return_value=(self.parts,refs)) as loader:
            self.assertEqual(b.load_inputs(Path("parent.json")),(self.parts,refs));loader.assert_called_once()
            refs[0]["initial_sha256"]=refs[0]["final_sha256"]
            with self.assertRaises(ValueError):b.load_inputs(Path("parent.json"))
    def test_18_six_model_run_and_real_replay_helper(self):
        refs=[]
        for seed,family in b.identities():
            model=Factory.new_model(seed)
            if family=="gru_only":model=Binding.new_baseline(model)
            refs.append(dict(seed=seed,family=family,initial_sha256=Factory.fingerprint(model),final={s:good_metrics(n) for s,n in b.ROWS.items()}))
        data=payload(b.summarize(records(),self.base,Fitting))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(self.parent,self.base,Fitting,Binding,Factory,Audit)), \
             patch.object(b,"precheck",return_value=(data["source_blobs"],data["input_sha256"])) as pre, \
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader, \
             patch.object(self.base,"parent_module",return_value=SimpleNamespace(discrete_metrics=Fitting.discrete_metrics)):
            out=Path(d)/"out";p245=Path(d)/"245.json";p244=Path(d)/"244.json"
            with contextlib.redirect_stdout(io.StringIO()):p=b.run(c245_summary=p245,c244_summary=p244,output_dir=out,expected_head="synthetic-head")
            self.assertEqual(pre.call_count,2);loader.assert_called_once()
            self.assertEqual(b.verify_artifacts(out,p244,"synthetic-head")[0],p)
            with self.assertRaises(ValueError):b.verify_artifacts(out,p244,"bad-head")
            (out/"measurements.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,p244,"synthetic-head")
    def test_19_failed_training_removes_hook(self):
        model=Factory.new_model(9010);ref=dict(initial_sha256=Factory.fingerprint(model),seed=9010)
        with patch.object(b,"fit",side_effect=ValueError("test")),self.assertRaises(ValueError):
            b.train_one(model,self.parts,ref,parent=self.parent,base=self.base,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertFalse(model._forward_hooks)
    def test_20_checkpoint_identity_order(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"models.pt";value=dict(schema="fold-c246-training-erasure-v1",identities=[list(x) for x in b.identities()],states=[{}]*6)
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),6)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)
    def test_21_actual_schedule_guard_rejects_wrong_view(self):
        native=b.select_view
        def wrong(batch,step):return native(batch,step+2)
        with patch.object(b,"select_view",side_effect=wrong),self.assertRaisesRegex(ValueError,"actual scheduled input"):
            self.exercise()
    def test_22_semantic_test_counts_and_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        self.assertEqual(len({x.id() for x in b.flatten(suite)}),24)
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(3073)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])
    def test_23_runner_cli_parser_paths(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c246.ps1").read_text(encoding="utf-8");launch=(root/"tools/invoke_c246.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for text in blocks:compile(text,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1,2});self.assertEqual(argv(blocks[2]),{1,2,3,4})
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c245-v5b-selective-evidence-484b9afa921e4fe4a3430a1d7a88e4d4",launch)
        self.assertIn("c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639",launch)
    def test_24_source_order_and_no_selective_eval(self):
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        line=lambda k:min(i for i,name in calls if name==k)
        for first,second in (("load_inputs","train_one"),("new_baseline","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):
            self.assertLess(line(first),line(second))
        self.assertEqual(b.VIEWS,("normal","evidence_blind","query_blind"))


if __name__=="__main__":unittest.main(verbosity=2)
