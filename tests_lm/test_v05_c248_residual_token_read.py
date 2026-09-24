"""C248 authoring tests: synthetic backbones do not establish FOLD capability."""
import ast
from collections import defaultdict
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
from torch import nn
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c248_residual_token_read as b


class CheapGRU(nn.Module):
    """Fast differentiable interface double; not the production GRU algorithm."""
    def __init__(self):
        super().__init__();self.weights=nn.Parameter(torch.randn(1632,dtype=torch.float64)*.01)
    def forward(self,x):
        y=x.cumsum(1)/torch.arange(1,49,dtype=x.dtype).view(1,-1,1)
        return y+self.weights[:16],y[:,-1].unsqueeze(0)


class CheapCore(nn.Module):
    def __init__(self):
        super().__init__();self.weights=nn.Parameter(torch.randn(3328,dtype=torch.float64)*.01)
    def initial_working_state(self,n,*,device,dtype):return torch.zeros(n,48,16,device=device,dtype=dtype)
    def forward(self,working,context,*,route_index):return context+.5*working+self.weights[:16]*(route_index+1)


class Backbone(nn.Module):
    def __init__(self,family,real_gru=False):
        super().__init__();self.family=family
        self.config=SimpleNamespace(width=16,max_tokens=48,next_route=0,instruction_route=1,internal_steps=2)
        self.byte_embedding=nn.Embedding(259,16,padding_idx=256,dtype=torch.float64)
        self.local_encoder=nn.GRU(16,16,batch_first=True,dtype=torch.float64) if real_gru else CheapGRU()
        if family=="full":self.core=CheapCore()
        self.readout_norm=nn.LayerNorm(16,dtype=torch.float64)
        self.decoder=nn.Linear(16,256,dtype=torch.float64)
    def forward(self,tokens,tasks):
        valid=tokens!=256;context,_=self.local_encoder(self.byte_embedding(tokens));context=context*valid.unsqueeze(-1)
        if self.family=="full":
            working=self.core.initial_working_state(len(tokens),device=tokens.device,dtype=context.dtype)
            for _ in range(2):
                n=self.core(working,context,route_index=0);i=self.core(working,context,route_index=1)
                working=torch.where(tasks.bool().view(-1,1,1),i,n)
        else:working=context
        eos=valid.sum(1)-1
        return self.decoder(self.readout_norm(working[torch.arange(len(tokens)),eos]))


class Factory:
    @staticmethod
    def new_model(seed):torch.manual_seed(seed);return Backbone("full").eval()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for k,v in sorted(model.state_dict().items()):h.update(k.encode());h.update(v.detach().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    names={"en":("box","book"),"ja":("箱","本")}
    @staticmethod
    def parent_module():return Binding
    @staticmethod
    def new_baseline(full):
        result=Backbone("gru_only")
        for k in ("byte_embedding","local_encoder","readout_norm","decoder"):setattr(result,k,copy.deepcopy(getattr(full,k)))
        return result.eval()
    @staticmethod
    def render(r,mode="normal"):
        facts=list(zip(r["objects"],r["values"],strict=True))
        if r["order"]:facts.reverse()
        names=Binding.names[r["language"]]
        return ";".join(names[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)+";"+("?" if mode=="query_blind" else names[r["query"]])+"="
    @staticmethod
    def tensors(rows,mode):
        def encode(r):
            raw=Binding.render(r,mode).encode();return [257,*raw,258]+[256]*(46-len(raw))
        return torch.tensor([encode(r) for r in rows]),torch.tensor([r["target"] for r in rows])


def fixture():
    blocks={k:[] for k in ("old","added","held")}
    for x,y in itertools.permutations(range(4),2):
        block="old" if (x,y) in ((0,1),(1,0),(2,3),(3,2)) else "added" if (x,y) in ((0,2),(2,0),(1,3),(3,1)) else "held"
        group=f"0-1-{x}-{y}"
        for lang in Binding.names:
            for order,q in itertools.product((0,1),repeat=2):
                r=dict(id=f"{lang}-{group}-{order}-{q}",group=group,objects=[0,1],values=[x,y],language=lang,order=order,query=q,
                    split="EVAL" if tuple(sorted((x,y))) in ((0,3),(1,2)) else "TRAIN",target=48+(x if q==0 else y))
                r["prompt"]=Binding.render(r);blocks[block].append(r)
    return dict(TRAIN=blocks["old"]+blocks["added"],HOLDOUT=blocks["held"])


class Fitting:
    @staticmethod
    def prediction_record(logits,n):return {v:x.argmax(-1).tolist() for v,x in zip(b.VIEWS,logits,strict=True)}
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
                    r=rows[i];key=(tuple(sorted(r["values"])),r["order"],r["query"]) if kind=="fact" else (r["group"],r["order"] if kind=="query" else r["query"])
                    groups[key].append(i)
                m[kind+"_pair_accuracy"]=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
            out[lang]=m
        return out
    @staticmethod
    def evaluate(model,rows,binding,fingerprint):
        before=fingerprint(model);training=model.training;model.eval();views=[binding.tensors(rows,v) for v in b.VIEWS]
        try:
            with torch.no_grad():logits=[model(x,torch.zeros(len(x),dtype=torch.int64)).detach() for x,_ in views]
        finally:model.train(training)
        m=Fitting.discrete_metrics(rows,Fitting.prediction_record(logits,len(rows)))
        loss=F.cross_entropy(logits[0],views[0][1],reduction="none")
        for lang in m:m[lang]["answer_nll"]=float(loss[[i for i,r in enumerate(rows) if r["language"]==lang]].mean())
        if fingerprint(model)!=before:raise ValueError("evaluation mutation")
        return m,logits
    @staticmethod
    def validate_metrics(m,n):
        if set(m)!={"en","ja"} or any(x["rows"]!=n//2 for x in m.values()):raise ValueError("metric rows")
    @staticmethod
    def cell_pass(m):
        return m["accuracy"]>=.9 and all(m[k+"_pair_accuracy"]>=.8 for k in ("fact","query","order")) and m["evidence_drop"]>=.35 and m["query_drop"]>=.35


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
        if path.parent!=Path(root).resolve():raise ValueError("unsafe artifact")
        return path
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
        if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def good_metrics(n,good=True):
    return {l:dict(rows=n//2,accuracy=1. if good else .25,answer_nll=.1,evidence_blind_accuracy=.25,query_blind_accuracy=.5,
        evidence_drop=.75 if good else 0.,query_drop=.5 if good else -.25,
        fact_pair_accuracy=1. if good else 0.,query_pair_accuracy=1. if good else 0.,order_pair_accuracy=1. if good else 0.) for l in ("en","ja")}


def records():
    return [dict(seed=s,family=f,arm=a,backbone_initial_sha256="a"*64,initial_metric_error=0.,parameters=b.BASE_PARAMS[f]+768,
        final={k:good_metrics(n) for k,n in b.ROWS.items()},fit=dict(steps=400,answer_presentations=12800),block_updates=[200,200],
        forward_calls=415,row_presentations=13568,checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.,
        weights_changed=True,head_weights_changed=True) for s,f,a in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(328)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS" if summary["gates"]["token_read"]["full"] else "FAIL",
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(526)},artifacts=[dict(file=p) for p in b.OUTPUTS],
        validation_summary=summary,gate_f_candidate=False,production_adoption=False,network_calls=0)


class C248Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=fixture();cls.base=b.context()[1]
    def exercise(self):
        backbone=Factory.new_model(9010)
        initial,_=Fitting.evaluate(backbone,self.parts["TRAIN"],Binding,Factory.fingerprint)
        ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(backbone),initial_train=initial)
        model=b.ReadoutPilot(backbone,"full","token_read",9010)
        with contextlib.redirect_stdout(io.StringIO()):r,state,raw=b.train_one(model,self.parts,ref,"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        return r,state,raw
    def test_01_manifest_and_partition(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["split-dataset.json"])
    def test_02_zero_residual_equals_backbone_both_families(self):
        x,_=Binding.tensors(self.parts["TRAIN"],"normal");tasks=torch.zeros(len(x),dtype=torch.int64)
        for family,arm in itertools.product(b.FAMILIES,b.ARMS):
            with self.subTest(family=family,arm=arm):
                torch.manual_seed(9010);backbone=Backbone(family,real_gru=True).eval()
                model=b.ReadoutPilot(copy.deepcopy(backbone),family,arm,9010).eval()
                with torch.no_grad():self.assertTrue(torch.equal(backbone(x,tasks),model(x,tasks)))
                self.assertEqual(sum(p.numel() for p in model.parameters()),b.BASE_PARAMS[family]+768)
    def test_03_output_projection_receives_gradient(self):
        x,_=Binding.tensors(self.parts["TRAIN"],"normal")
        for arm in b.ARMS:
            model=b.ReadoutPilot(Factory.new_model(9011),"full",arm,9011)
            model(x,torch.zeros(len(x),dtype=torch.int64)).square().mean().backward()
            self.assertGreater(float(model.read.output.weight.grad.abs().sum()),0.)
    def test_04_reader_uses_nonEOS_states(self):
        h=b.ResidualHead("token_read",1)
        with torch.no_grad():h.output.weight.copy_(torch.eye(16))
        states=torch.zeros(2,48,16,dtype=torch.float64);valid=torch.ones(2,48,dtype=torch.bool);pooled=states[:,-1]
        other=states.clone();other[:,3]=1
        self.assertFalse(torch.equal(h(pooled,states,valid),h(pooled,other,valid)))
    def test_05_padding_cannot_contribute(self):
        h=b.ResidualHead("token_read",1)
        with torch.no_grad():h.output.weight.copy_(torch.eye(16))
        states=torch.randn(2,48,16,dtype=torch.float64);valid=torch.arange(48)[None,:].expand(2,-1)<20
        other=states.clone();other[~valid]+=100
        self.assertTrue(torch.equal(h(states[:,19],states,valid),h(states[:,19],other,valid)))
    def test_06_EOS_control_has_no_token_access(self):
        h=b.ResidualHead("eos_adapter",2)
        with torch.no_grad():h.output.weight.fill_(.2)
        pooled=torch.randn(2,16,dtype=torch.float64)
        self.assertTrue(torch.equal(h(pooled,None,None),h(pooled,torch.randn(2,48,16),None)))
    def test_07_both_initializations_preserve_rng(self):
        for arm in b.ARMS:
            torch.manual_seed(9013);state=torch.random.get_rng_state().clone();b.ResidualHead(arm,2)
            self.assertTrue(torch.equal(state,torch.random.get_rng_state()))
    def test_08_backbone_is_unchanged_after_zero_read(self):
        model=b.ReadoutPilot(Factory.new_model(1),"full","token_read",1);before=Factory.fingerprint(model.backbone)
        x,_=Binding.tensors(self.parts["TRAIN"],"normal");model(x,torch.zeros(len(x),dtype=torch.int64))
        self.assertEqual(before,Factory.fingerprint(model.backbone))
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.backbone.modules()))
    def test_09_failed_forward_removes_all_hooks(self):
        model=b.ReadoutPilot(Factory.new_model(1),"full","token_read",1);x,_=Binding.tensors(self.parts["TRAIN"],"normal")
        with patch.object(model.backbone.decoder,"forward",side_effect=ValueError("fixture")),self.assertRaises(ValueError):model(x,torch.zeros(len(x),dtype=torch.int64))
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.backbone.modules()))
    def test_10_EOS_and_task_contracts(self):
        model=b.ReadoutPilot(Factory.new_model(1),"full","token_read",1);x,_=Binding.tensors(self.parts["TRAIN"],"normal")
        with self.assertRaises(ValueError):model(x,torch.ones(len(x),dtype=torch.int64))
        x[x==258]=63
        with self.assertRaises(ValueError):model(x,torch.zeros(len(x),dtype=torch.int64))
    def test_11_actual400_training_and_parent_replay(self):
        r,state,raw=self.exercise();self.assertEqual((r["forward_calls"],r["row_presentations"]),(409,13280));self.assertTrue(r["head_weights_changed"])
        model=b.ReadoutPilot(Factory.new_model(9010),"full","token_read",9010)
        self.base.replay_one(model,state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,13568))
    def test_12_wrong_initial_stops_before_fit(self):
        model=b.ReadoutPilot(Factory.new_model(1),"full","token_read",1)
        with patch.object(b,"fit") as fit,self.assertRaises(ValueError):b.train_one(model,self.parts,{"initial_sha256":"bad"},"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        fit.assert_not_called()
    def test_13_actual_batch_inputs_no_erasure(self):
        model=b.ReadoutPilot(Factory.new_model(1),"full","token_read",1);x,y=Binding.tensors(self.parts["TRAIN"],"normal");seen=[]
        h=model.register_forward_pre_hook(lambda module,args:seen.append(args[0].clone()))
        b.fit(model,x,y,1,steps=2);h.remove()
        self.assertEqual(len(seen),2);self.assertTrue(torch.equal(seen[0],x[:32]));self.assertTrue(torch.equal(seen[1],x[32:]))
    def test_14_initial_metric_mismatch_stops_before_fit(self):
        model=b.ReadoutPilot(Factory.new_model(1),"full","token_read",1)
        ref=dict(initial_sha256=Factory.fingerprint(model.backbone),initial_train=good_metrics(64))
        with patch.object(b,"fit") as fit,self.assertRaisesRegex(ValueError,"initial metrics"):b.train_one(model,self.parts,ref,"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        fit.assert_not_called()
    def test_15_independent_family_arm_gates(self):
        r=records();r[0]["final"]["HOLDOUT"]=good_metrics(32,False);s=b.summarize(r,Fitting)
        self.assertFalse(s["gates"]["token_read"]["full"]);self.assertTrue(s["gates"]["eos_adapter"]["full"])
        self.assertTrue(s["gates"]["token_read"]["gru_only"]);b.validate_result(payload(s))
    def test_16_invalid_capacity_workload_and_replay(self):
        for k,v in (("parameters",1),("forward_calls",414),("reload_max_error",1.),("head_weights_changed",False)):
            r=records();r[0][k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r,Fitting)))
    def test_17_checkpoint_order_all12(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"models.pt";value=dict(schema="fold-c248-residual-read-v1",identities=[list(x) for x in b.identities()],states=[{}]*12)
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),12)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)
    def test_18_parent_optimizer_AST(self):b.audit_recipe(self.base)
    def test_19_matched_backbone_cannot_drift_between_arms(self):
        r=records();r[1]["backbone_initial_sha256"]="b"*64
        with self.assertRaises(ValueError):b.summarize(r,Fitting)
    def test_20_actual_parent_loader_schema(self):
        refs=[]
        for seed,family in itertools.product(b.SEEDS,b.FAMILIES):
            predictions={s:{v:([r["target"] for r in rows] if v=="normal" else [48]*len(rows)) for v in b.VIEWS} for s,rows in self.parts.items()}
            final={s:{l:dict(m,answer_nll=.1) for l,m in Fitting.discrete_metrics(rows,predictions[s]).items()} for s,rows in self.parts.items()}
            refs.append(dict(seed=seed,family=family,initial_sha256="a"*64,final_sha256="b"*64,initial_train=good_metrics(64),predictions=predictions,final=final))
        parent=SimpleNamespace(summarize=lambda r,f:{"models":len(r)})
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,self.base,Fitting,Binding,Factory,Audit)),patch.object(self.base,"parent_module",return_value=Fitting):
            root=Path(d)
            for name,value in (("split-dataset.json",self.parts),("measurements.json",refs),("summary.json",dict(validation_summary={"models":6}))):(root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"),(self.parts,refs))
    def test_21_actual12_model_run_and_postcheck(self):
        refs=[]
        for seed in b.SEEDS:
            full=Factory.new_model(seed);gru=Binding.new_baseline(full)
            for family,model in (("full",full),("gru_only",gru)):
                initial,_=Fitting.evaluate(model,self.parts["TRAIN"],Binding,Factory.fingerprint)
                refs.append(dict(seed=seed,family=family,initial_sha256=Factory.fingerprint(model),initial_train=initial))
        p=payload(b.summarize(records(),Fitting))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,self.base,Fitting,Binding,Factory,Audit)),\
            patch.object(b,"precheck",return_value=(p["source_blobs"],p["input_sha256"])) as pre,\
            patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader,patch.object(self.base,"parent_module",return_value=Fitting):
            out=Path(d)/"out";parent=Path(d)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c247_summary=parent,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,parent,"synthetic-head")[0],result)
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,"bad-head")
            (out/"measurements.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,"synthetic-head")
    def test_22_count_semantics_and_single_exclusion(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}),24)
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(3121)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3121)
    def test_23_runner_cli_and_parser(self):
        root=Path(__file__).resolve().parents[1];run=(root/"tools/run_c248.ps1").read_text(encoding="utf-8");launch=(root/"tools/invoke_c248.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c247-v5b-normal-exposure-a3cec4a219a14360bac90cf8d7303da5",launch)
    def test_24_run_calls_readout_and_no_fact_parser(self):
        tree=ast.parse(inspect.getsource(b.run));calls={n.func.id for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertTrue({"load_inputs","ReadoutPilot","train_one","load_bundle"}<=calls)
        self.assertEqual(set(inspect.signature(b.ReadoutPilot.forward).parameters),{"self","tokens","tasks"})
        self.assertEqual(set(b.ARMS),{"token_read","eos_adapter"})


if __name__=="__main__":unittest.main(verbosity=2)
