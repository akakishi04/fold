"""C249 authoring tests use synthetic backbones, not accepted model evidence."""
import ast
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
from fold_lm.v05_benchmarks import model_c249_frozen_read_ablation as b
from fold_lm.v05_benchmarks import model_c248_residual_token_read as parent


class Core(nn.Module):
    """Interface double, explicitly not the production FOLD core."""
    def __init__(self):
        super().__init__();self.weights=nn.Parameter(torch.randn(3328,dtype=torch.float64)*.01)
    def initial_working_state(self,n,*,device,dtype):return torch.zeros(n,48,16,device=device,dtype=dtype)
    def forward(self,working,context,*,route_index):return context+.5*working+self.weights[:16]*(route_index+1)


class Backbone(nn.Module):
    def __init__(self,family):
        super().__init__();self.family=family
        self.config=SimpleNamespace(width=16,max_tokens=48,next_route=0,instruction_route=1,internal_steps=2)
        self.byte_embedding=nn.Embedding(259,16,padding_idx=256,dtype=torch.float64)
        self.local_encoder=nn.GRU(16,16,batch_first=True,dtype=torch.float64)
        if family=="full":self.core=Core()
        self.readout_norm=nn.LayerNorm(16,dtype=torch.float64);self.decoder=nn.Linear(16,256,dtype=torch.float64)
    def forward(self,tokens,tasks):
        valid=tokens!=256;states,_=self.local_encoder(self.byte_embedding(tokens));states=states*valid.unsqueeze(-1)
        if self.family=="full":
            h=self.core.initial_working_state(len(tokens),device=tokens.device,dtype=states.dtype)
            for _ in range(2):
                n=self.core(h,states,route_index=0);i=self.core(h,states,route_index=1)
                h=torch.where(tasks.bool().view(-1,1,1),i,n)
        else:h=states
        return self.decoder(self.readout_norm(h[torch.arange(len(tokens)),valid.sum(1)-1]))


class Factory:
    @staticmethod
    def new_model(seed):torch.manual_seed(seed);return Backbone("full").eval()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for key,value in sorted(model.state_dict().items()):
            h.update(key.encode());h.update(value.detach().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    names={"en":("box","book"),"ja":("箱","本")}
    @staticmethod
    def parent_module():return Binding
    @staticmethod
    def new_baseline(full):
        model=Backbone("gru_only")
        for key in ("byte_embedding","local_encoder","readout_norm","decoder"):setattr(model,key,copy.deepcopy(getattr(full,key)))
        return model.eval()
    @staticmethod
    def render(row,mode="normal"):
        facts=list(zip(row["objects"],row["values"],strict=True))
        if row["order"]:facts.reverse()
        names=Binding.names[row["language"]]
        return ";".join(names[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)+";"+("?" if mode=="query_blind" else names[row["query"]])+"="
    @staticmethod
    def tensors(rows,mode):
        def encode(row):
            raw=Binding.render(row,mode).encode();return [257,*raw,258]+[256]*(46-len(raw))
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


def model_and_reference(parts,seed=9010,family="full",arm="token_read"):
    torch.manual_seed(seed);model=parent.ReadoutPilot(Backbone(family),family,arm,seed)
    with torch.no_grad():model.read.output.weight.normal_(0,.05)
    model.eval();model.requires_grad_(False);final={};pred={}
    for split,rows in parts.items():
        with torch.no_grad():outputs={v:model(Binding.tensors(rows,v)[0],torch.zeros(len(rows),dtype=torch.int64)) for v in b.VIEWS}
        final[split]=b.original_metrics(rows,outputs);pred[split]={v:x.argmax(-1).tolist() for v,x in outputs.items()}
    ref=dict(seed=seed,family=family,arm=arm,final_sha256=Factory.fingerprint(model),final=final,predictions=pred)
    return model,ref


def reports():
    return [dict(seed=s,family=f,arm=a,before_sha256="a"*64,after_sha256="a"*64,
        parent_metric_error=0.,restored_max_error=0.,parent_predictions_equal=True,restored_predictions_equal=True,
        forward_calls=16 if a=="token_read" else 14,row_presentations=768 if a=="token_read" else 672,
        intervention_calls={m:2 for m in b.modes(a)}) for s,f,a in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(334)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(538)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,network_calls=0)


class Audit:
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
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
        if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


class C249Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=fixture()

    def test_01_manifest_and_partition_identity(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["split-dataset.json"])

    def test_02_residual_off_returns_pooled_for_both_arms(self):
        p=torch.randn(2,16,dtype=torch.float64);h=torch.randn(2,48,16,dtype=torch.float64);v=torch.ones(2,48,dtype=torch.bool)
        for arm in b.ARMS:
            head=parent.ResidualHead(arm,1)
            with torch.no_grad():head.output.weight.fill_(.1)
            with b.intervention(head,"residual_off") as calls:self.assertTrue(torch.equal(head(p,h,v),p))
            self.assertEqual(calls[0],1);self.assertFalse(head._forward_hooks)

    def test_03_uniform_retains_trained_output_matrix(self):
        head=parent.ResidualHead("token_read",2);p=torch.randn(2,16,dtype=torch.float64);h=torch.randn(2,48,16,dtype=torch.float64)
        v=torch.arange(48)[None,:].expand(2,-1)<20
        with torch.no_grad():head.output.weight.copy_(torch.eye(16))
        with b.intervention(head,"uniform_read"):
            self.assertTrue(torch.allclose(head(p,h,v),p+h[:,:20].mean(1),atol=1e-12,rtol=0))

    def test_04_uniform_excludes_pad_states(self):
        head=parent.ResidualHead("token_read",2);p=torch.randn(2,16,dtype=torch.float64);h=torch.randn(2,48,16,dtype=torch.float64)
        v=torch.arange(48)[None,:].expand(2,-1)<20;changed=h.clone();changed[~v]=1000
        with torch.no_grad():head.output.weight.fill_(.01)
        with b.intervention(head,"uniform_read"):self.assertTrue(torch.equal(head(p,h,v),head(p,changed,v)))

    def test_05_uniform_not_supported_for_EOS_control(self):
        with self.assertRaises(ValueError):
            with b.intervention(parent.ResidualHead("eos_adapter",1),"uniform_read"):pass

    def test_06_no_persistent_forward_change(self):
        head=parent.ResidualHead("token_read",2);p=torch.randn(2,16,dtype=torch.float64);h=torch.randn(2,48,16,dtype=torch.float64);v=torch.ones(2,48,dtype=torch.bool)
        with torch.no_grad():head.output.weight.fill_(.1)
        before=head(p,h,v).detach().clone()
        with b.intervention(head,"residual_off"):self.assertTrue(torch.equal(head(p,h,v),p))
        self.assertTrue(torch.equal(head(p,h,v),before))

    def test_07_exception_removes_hook(self):
        head=parent.ResidualHead("token_read",1)
        with self.assertRaises(RuntimeError):
            with b.intervention(head,"residual_off"):raise RuntimeError("fixture")
        self.assertFalse(head._forward_hooks)

    def test_08_trainable_or_wrong_state_rejected(self):
        model,ref=model_and_reference(self.parts)
        with self.assertRaises(ValueError):b.check_frozen(model,Factory.fingerprint,"wrong")
        model.requires_grad_(True)
        with self.assertRaises(ValueError):b.check_frozen(model,Factory.fingerprint,ref["final_sha256"])

    def test_09_finite_logit_shape_dtype(self):
        for x in (torch.zeros(32,255,dtype=torch.float64),torch.zeros(32,256),torch.full((32,256),float("nan"),dtype=torch.float64)):
            with self.assertRaises(ValueError):b.finite_logits(x,32)

    def test_10_perfect_normal_pairs(self):
        rows=self.parts["TRAIN"];x=torch.zeros(len(rows),256,dtype=torch.float64)
        x[torch.arange(len(rows)),torch.tensor([r["target"] for r in rows])]=10
        for m in b.normal_metrics(rows,x).values():
            self.assertEqual((m["accuracy"],m["fact_pair_accuracy"],m["query_pair_accuracy"],m["order_pair_accuracy"]),(1,1,1,1))

    def test_11_pair_metric_agrees_with_independent_counterparts(self):
        rows=self.parts["HOLDOUT"]
        for seed in range(20):
            g=torch.Generator().manual_seed(seed);x=torch.randn(len(rows),256,generator=g,dtype=torch.float64);x[:,48:52]+=3
            pred=x.argmax(-1).tolist();m=b.normal_metrics(rows,x)
            for lang in m:
                indices=[i for i,r in enumerate(rows) if r["language"]==lang]
                for kind in ("fact","query","order"):
                    pairs=[]
                    for i in indices:
                        for j in indices:
                            a,c=rows[i],rows[j]
                            match=(a["values"]==c["values"][::-1] and a["order"]==c["order"] and a["query"]==c["query"]) if kind=="fact" else (a["values"]==c["values"] and ((a["order"]==c["order"] and a["query"]!=c["query"]) if kind=="query" else (a["order"]!=c["order"] and a["query"]==c["query"])))
                            if i<j and match:pairs.append((i,j))
                    expected=sum(pred[i]==rows[i]["target"] and pred[j]==rows[j]["target"] for i,j in pairs)/len(pairs)
                    self.assertEqual(m[lang][kind+"_pair_accuracy"],expected)

    def test_12_original_metric_mask_schema(self):
        rows=self.parts["TRAIN"];x=torch.zeros(len(rows),256,dtype=torch.float64);x[:,48]=1
        m=b.original_metrics(rows,{v:x for v in b.VIEWS})
        self.assertEqual(m["en"]["accuracy"],.25);self.assertEqual(m["en"]["evidence_drop"],0)
        self.assertEqual(m["ja"]["query_blind_accuracy"],.25)
        self.assertNotIn("evidence_drop",b.normal_metrics(rows,x)["en"])

    def test_13_metric_replay_schema_and_nonfinite(self):
        _,ref=model_and_reference(self.parts);m=ref["final"]["TRAIN"]
        self.assertEqual(b.metric_error(m,m),0)
        changed=copy.deepcopy(m);changed["en"]["answer_nll"]=float("nan")
        with self.assertRaises(ValueError):b.metric_error(m,changed)

    def test_14_transitions_distinguish_flips_and_logits(self):
        rows=self.parts["HOLDOUT"];x=torch.zeros(len(rows),256,dtype=torch.float64);x[:,48]=1
        for m in b.contrasts(rows,x,x+.1).values():
            self.assertEqual(m["answer_flips"],0);self.assertGreater(m["max_logit_change"],0)
        changed=x.clone();changed[:,48]=0;changed[:,49]=1
        for m in b.contrasts(rows,x,changed).values():
            self.assertEqual(m["answer_flips"],16);self.assertEqual(m["lost_correct"],4);self.assertEqual(m["gained_correct"],4)

    def test_15_actual_parent_wrapper_ablate_restore_counts(self):
        for family,arm in itertools.product(b.FAMILIES,b.ARMS):
            model,ref=model_and_reference(self.parts,family=family,arm=arm)
            record,raw,effects=b.audit_model(model,self.parts,ref,binding=Binding,factory=Factory)
            self.assertEqual((record["forward_calls"],record["row_presentations"]),(16,768) if arm=="token_read" else (14,672))
            self.assertEqual(record["restored_max_error"],0.);self.assertEqual(set(effects),set(b.modes(arm)))

    def test_16_bad_parent_predictions_stops_before_ablation(self):
        model,ref=model_and_reference(self.parts);ref["predictions"]["TRAIN"]["normal"][0]=255
        with patch.object(b,"intervention") as altered,self.assertRaisesRegex(ValueError,"parent prediction"):
            b.audit_model(model,self.parts,ref,binding=Binding,factory=Factory)
        altered.assert_not_called();self.assertFalse(model._forward_hooks)

    def test_17_diagnostic_gate_ignores_accuracy(self):
        summary=b.summarize(reports());b.validate_result(payload(summary))
        self.assertFalse(summary["capability_pass_claim"])
        for k,v in (("restored_max_error",1.),("forward_calls",15),("after_sha256","b"*64)):
            r=reports();r[0][k]=v
            with self.assertRaises(ValueError):b.summarize(r)

    def test_18_all_models_identity_and_mode_workload(self):
        r=reports()
        with self.assertRaises(ValueError):b.summarize(list(reversed(r)))
        r[0]["intervention_calls"]["uniform_read"]=1
        with self.assertRaises(ValueError):b.summarize(r)

    def test_19_actual_loader_adapts_final_not_initial(self):
        refs=[]
        for seed,family,arm in b.identities():
            _,r=model_and_reference(self.parts,seed,family,arm);refs.append(r)
        parent_adapter=SimpleNamespace(summarize=lambda r,f:{"fixture_models":len(r)})
        fitting=SimpleNamespace(validate_metrics=lambda m,n:None)
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent_adapter,None,fitting,Binding,Factory,Audit)):
            root=Path(d)
            for name,value in (("split-dataset.json",self.parts),("measurements.json",refs),("summary.json",dict(validation_summary={"fixture_models":12}))):(root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"),(self.parts,refs))
            refs[0]["final_sha256"]="not-a-fingerprint";(root/"measurements.json").write_bytes(b.blob(refs))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_20_constructs_frozen_original_wrapper_and_loads_strictly(self):
        model,ref=model_and_reference(self.parts,234001,"gru_only","token_read")
        copied=b.make_model(ref,model.state_dict(),parent,Binding,Factory)
        self.assertEqual(Factory.fingerprint(copied),ref["final_sha256"])
        bad=copy.deepcopy(model.state_dict());bad.pop(next(iter(bad)))
        with self.assertRaises(RuntimeError):b.make_model(ref,bad,parent,Binding,Factory)

    def test_21_full12_run_and_persisted_replay(self):
        refs=[];states=[]
        for seed,family,arm in b.identities():
            model,ref=model_and_reference(self.parts,seed,family,arm);refs.append(ref);states.append(copy.deepcopy(model.state_dict()))
        base=payload(b.summarize(reports()));parent_adapter=SimpleNamespace(ReadoutPilot=parent.ReadoutPilot,load_bundle=lambda path:states)
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent_adapter,None,None,Binding,Factory,Audit)),\
             patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre,\
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader:
            out=Path(d)/"out";parent_path=Path(d)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c248_summary=parent_path,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,parent_path,"synthetic-head")[0],result)
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent_path,"wrong")
            (out/"contrasts.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent_path,"synthetic-head")

    def test_22_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"]);self.assertEqual(len({t.id() for t in b.flatten(suite)}),24)
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(3145)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3145)

    def test_23_runner_cli_and_parser_order(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c249.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c249.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(s):
            return {n.slice.value for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(l.index("::ParseFile"),l.index("$failure = $null"))
        self.assertIn("c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22",l)

    def test_24_no_training_and_actual_loader_dispatch(self):
        for node in ast.walk(ast.parse(inspect.getsource(b))):
            if isinstance(node,ast.Call):
                name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else ""
                self.assertNotIn(name,{"fit","backward","step","zero_grad","save"})
        calls={n.func.id for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertTrue({"load_inputs","make_model","audit_model"}<=calls)


if __name__=="__main__":unittest.main(verbosity=2)
