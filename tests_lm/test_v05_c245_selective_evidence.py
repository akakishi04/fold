"""Synthetic C245 authoring tests; no accepted-model scientific results."""
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
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c245_selective_evidence as b


class Factory:
    @staticmethod
    def prefix_tensor(raw):
        if len(raw)>46:
            raise ValueError("prefix too long")
        return torch.tensor([257,*raw,258]+[256]*(46-len(raw)),dtype=torch.int64)
    @staticmethod
    def new_model(seed):
        torch.manual_seed(seed)
        return Toy()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for k,v in sorted(model.state_dict().items()):
            h.update(k.encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.layer=torch.nn.Linear(3,256).double()
    def forward(self,tokens,tasks):
        x=tokens.double()/300
        return self.layer(torch.stack((x.mean(1),x[:,5],x[:,15]),dim=1))


class Binding:
    names={"en":("box","book"),"ja":("箱","本")}
    @staticmethod
    def render(r,mode="normal"):
        names=Binding.names[r["language"]]
        facts=list(zip(r["objects"],r["values"],strict=True))
        if r["order"]:facts.reverse()
        return ";".join(names[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)+";"+("?" if mode=="query_blind" else names[r["query"]])+"="
    @staticmethod
    def tensors(rows,mode="normal"):
        return torch.stack([Factory.prefix_tensor(Binding.render(r,mode).encode()) for r in rows]),torch.tensor([r["target"] for r in rows])
    @staticmethod
    def metrics(rows,pred,evidence,query,logits,targets):
        loss=F.cross_entropy(logits,targets,reduction="none");out={}
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            accs=[sum(p[i]==rows[i]["target"] for i in ids)/len(ids) for p in (pred,evidence,query)]
            groups={kind:defaultdict(list) for kind in ("fact","query")}
            for i in ids:
                r=rows[i]
                groups["fact"][(tuple(sorted(r["values"])),r["order"],r["query"])].append(i)
                groups["query"][(r["group"],r["order"])].append(i)
            paired={k:sum(all(pred[i]==rows[i]["target"] for i in g) for g in gs.values())/len(gs) for k,gs in groups.items()}
            out[lang]=dict(rows=len(ids),accuracy=accs[0],answer_nll=float(loss[ids].mean()),
                evidence_blind_accuracy=accs[1],query_blind_accuracy=accs[2],evidence_drop=accs[0]-accs[1],query_drop=accs[0]-accs[2],
                fact_pair_accuracy=paired["fact"],query_pair_accuracy=paired["query"])
        return out
    @staticmethod
    def parent_module():return SimpleNamespace(new_baseline=copy.deepcopy)


def fixture():
    blocks={"old":[],"added":[],"held":[]}
    for x,y in itertools.permutations(range(4),2):
        key="old" if (x,y) in ((0,1),(1,0),(2,3),(3,2)) else "added" if (x,y) in ((0,2),(2,0),(1,3),(3,1)) else "held"
        group=f"0-1-{x}-{y}"
        for lang in Binding.names:
            for order,q in itertools.product((0,1),repeat=2):
                r=dict(id=f"{lang}-{group}-{order}-{q}",group=group,objects=[0,1],values=[x,y],language=lang,
                    order=order,query=q,split="EVAL" if tuple(sorted((x,y))) in ((0,3),(1,2)) else "TRAIN",target=48+(x if q==0 else y))
                r["prompt"]=Binding.render(r);blocks[key].append(r)
    return dict(TRAIN=blocks["old"]+blocks["added"],HOLDOUT=blocks["held"])


def reference(model,parts,seed=234001,family="full"):
    out={}
    with torch.no_grad():
        for split,rows in parts.items():
            out[split]={v:model(Binding.tensors(rows,v)[0],torch.zeros(len(rows),dtype=torch.int64)) for v in b.ORIGINAL}
    return dict(seed=seed,family=family,final_sha256=Factory.fingerprint(model),
        final={s:b.original_metrics(parts[s],out[s],Binding) for s in b.ROWS},
        predictions={s:{v:x.argmax(-1).tolist() for v,x in vs.items()} for s,vs in out.items()})


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(310)};pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(490)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,network_calls=0)


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
        if p.parent!=Path(root).resolve():raise ValueError("unsafe path")
        return p


class C245Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.parts=fixture();cls.inputs=b.input_records(cls.parts,Binding)
        cls.model=Factory.new_model(9010).eval().requires_grad_(False)
        cls.ref=reference(cls.model,cls.parts)
        cls.rec=b.score_model(cls.parts,cls.inputs,cls.model,cls.ref,Binding,Factory)
    def records(self):
        return [dict(copy.deepcopy(self.rec),seed=s,family=f) for s,f in b.identities()]

    def test_01_manifest_and_split_identity(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["split-dataset.json"])
    def test_02_mask_correct_entity_and_single_byte(self):
        for rows in self.parts.values():
            for r in rows:
                for mode in b.SELECTIVE:
                    text=b.masked_prompt(r,mode,Binding);name=Binding.names[r["language"]][r["query"] if mode==b.SELECTIVE[0] else 1-r["query"]]
                    self.assertIn(name+"=?",text.split(";")[0]+";"+text.split(";")[1])
                    self.assertEqual(text.split(";")[-1],r["prompt"].split(";")[-1])
                    self.assertEqual(sum(a!=c for a,c in zip(text.encode(),r["prompt"].encode())),1)
    def test_03_mask_does_not_read_target(self):
        r=copy.deepcopy(self.parts["TRAIN"][0]);wanted=b.masked_prompt(r,b.SELECTIVE[0],Binding);r.pop("target")
        self.assertEqual(b.masked_prompt(r,b.SELECTIVE[0],Binding),wanted)
    def test_04_ambiguity_boundary_is_explicit(self):
        m=b.manifest()["selective_input_ceilings"]
        self.assertEqual(m["TRAIN"]["queried_value_blind"],.5)
        self.assertEqual(m["HOLDOUT"]["queried_value_blind"],1.)
        self.assertEqual(b.input_records(self.parts,Binding),self.inputs)
    def test_05_tampered_partition_rejected(self):
        parts=copy.deepcopy(self.parts);parts["TRAIN"][0]["target"]=255
        with self.assertRaises(ValueError):b.input_records(parts,Binding)
    def test_06_actual_token_parity_and_mask_positions(self):
        for s,rows in self.parts.items():
            for mode in b.VIEWS:
                tokens,targets=b.tensors(rows,self.inputs[s][mode],mode,Binding,Factory)
                self.assertEqual(tokens.shape,(len(rows),48));self.assertEqual(targets.tolist(),[r["target"] for r in rows])
    def test_07_multi_byte_or_wrong_mask_rejected(self):
        texts=list(self.inputs["TRAIN"][b.SELECTIVE[0]]);texts[0]=texts[0].replace("box","xxx")
        with self.assertRaises(ValueError):b.tensors(self.parts["TRAIN"],texts,b.SELECTIVE[0],Binding,Factory)
    def test_08_nonfinite_shape_and_precision_rejected(self):
        for x in (torch.zeros(8,256),torch.zeros(64,255,dtype=torch.float64),torch.full((64,256),float("nan"),dtype=torch.float64)):
            with self.assertRaises(ValueError):b.checked_logits(x,64)
    def test_09_original_metric_replay_and_nll(self):
        self.assertEqual(b.compare_parent(self.parts,b.decode_outputs(self.rec),self.ref,Binding),0.)
        out=b.original_metrics(self.parts["TRAIN"],b.decode_outputs(self.rec)["TRAIN"],Binding)
        self.assertEqual(set(out["en"]),set(self.ref["final"]["TRAIN"]["en"]))
    def test_10_original_prediction_change_rejected(self):
        ref=copy.deepcopy(self.ref);ref["predictions"]["TRAIN"]["normal"][0]=(ref["predictions"]["TRAIN"]["normal"][0]+1)%256
        with self.assertRaises(ValueError):b.compare_parent(self.parts,b.decode_outputs(self.rec),ref,Binding)
    def test_11_original_metric_change_rejected(self):
        ref=copy.deepcopy(self.ref);ref["final"]["HOLDOUT"]["ja"]["answer_nll"]+=.1
        with self.assertRaises(ValueError):b.compare_parent(self.parts,b.decode_outputs(self.rec),ref,Binding)
    def test_12_actual_frozen_forward_counts(self):
        self.assertEqual((self.rec["forward_calls"],self.rec["row_presentations"]),(10,480))
        self.assertEqual(self.rec["before_sha256"],self.rec["after_sha256"])
        self.assertFalse(self.model._forward_hooks)
    def test_13_trainable_or_wrong_final_model_rejected(self):
        model=Factory.new_model(9010).eval()
        with self.assertRaises(ValueError):b.score_model(self.parts,self.inputs,model,self.ref,Binding,Factory)
        model.requires_grad_(False);ref=dict(self.ref,final_sha256="a"*64)
        with self.assertRaises(ValueError):b.score_model(self.parts,self.inputs,model,ref,Binding,Factory)
    def test_14_error_removes_instrumentation(self):
        model=Factory.new_model(9010).eval().requires_grad_(False)
        with patch.object(b,"tensors",side_effect=ValueError("fixture failure")),self.assertRaises(ValueError):
            b.score_model(self.parts,self.inputs,model,self.ref,Binding,Factory)
        self.assertFalse(model._forward_hooks)
    def test_15_diagnostic_baseline_identity_and_cell_counts(self):
        cells=b.diagnose(self.parts,self.records());self.assertEqual(len(cells),24)
        for c in cells:
            base=c["views"]["normal"]
            self.assertEqual((base["answer_flips"],base["nll_increase"],base["logit_linf"]),(0,0.,0.))
            self.assertEqual(set(c["views"]),set(b.VIEWS))
    def test_16_erasure_flip_and_broken_counts_independent(self):
        records=self.records()
        for rec in records:
            for s,rows in self.parts.items():
                normal=torch.zeros(len(rows),256,dtype=torch.float64)
                for i,r in enumerate(rows):normal[i,r["target"]]=10
                wrong=normal.clone();wrong[:,255]=20
                rec["logits"][s]["normal"]=normal.tolist();rec["logits"][s][b.SELECTIVE[0]]=wrong.tolist()
        for c in b.diagnose(self.parts,records):
            m=c["views"][b.SELECTIVE[0]];self.assertEqual((m["answer_flips"],m["correct_to_wrong"],m["wrong_to_correct"]),(c["rows"],c["rows"],0))
    def test_17_gate_not_controlled_by_mask_accuracy(self):
        records=self.records();p=payload(b.summarize(records));b.validate_result(p)
        self.assertFalse(p["validation_summary"]["capability_pass_claim"])
        self.assertEqual(p["validation_summary"]["model_forward_calls"],60)
    def test_18_bad_replay_mutation_and_count_rejected(self):
        for k,v in (("forward_calls",9),("row_presentations",479),("after_sha256","a"*64),("parent_metric_error",.1)):
            recs=self.records();recs[0][k]=v
            with self.assertRaises(ValueError):b.summarize(recs)
    def test_19_actual_loader_parent_contract(self):
        refs=[dict(copy.deepcopy(self.ref),seed=s,family=f) for s,f in b.identities()]
        parent=SimpleNamespace(summarize=lambda r,f:{"models":len(r)})
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,None,Binding,None,Audit)):
            root=Path(d)
            for name,value in (("split-dataset.json",self.parts),("measurements.json",refs),("summary.json",dict(validation_summary={"models":6}))):
                (root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"),(self.parts,refs))
            refs[0]["final_sha256"]="bad";(root/"measurements.json").write_bytes(b.blob(refs))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")
    def test_20_actual_six_model_run_saved_logit_postcheck(self):
        refs=[dict(copy.deepcopy(self.ref),seed=s,family=f) for s,f in b.identities()]
        states=[copy.deepcopy(self.model.state_dict()) for _ in refs]
        parent=SimpleNamespace(load_bundle=lambda p:states)
        base=payload(b.summarize(self.records()))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,None,Binding,Factory,Audit)), \
             patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader:
            out,source=Path(d)/"out",Path(d)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c244_summary=source,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,source,"synthetic-head")[0],result)
            with self.assertRaises(ValueError):b.verify_artifacts(out,source,"wrong")
            (out/"intervention-inputs.json").write_text("{}",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,source,"synthetic-head")
    def test_21_no_training_ast_and_load_before_frozen_scoring(self):
        for n in ast.walk(ast.parse(inspect.getsource(b))):
            if isinstance(n,ast.Call):
                name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ""
                self.assertNotIn(name,{"fit","backward","step","zero_grad"})
            if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name):
                self.assertFalse(n.value.id=="torch" and n.attr in {"optim","save"})
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        line=lambda k:min(i for i,name in calls if name==k)
        for first,second in (("load_inputs","load_bundle"),("load_bundle","load_state_dict"),("requires_grad_","score_model")):
            self.assertLess(line(first),line(second))
    def test_22_runner_cli_parser(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c245.ps1").read_text(encoding="utf-8");launch=(root/"tools/invoke_c245.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for x in blocks:compile(x,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639",launch)
    def test_23_semantic_own_count_and_module_append(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"]);self.assertEqual(len(ids),len(set(ids)))
        parent=SimpleNamespace(regression_modules=lambda root:[f"parent_{i}" for i in range(129)])
        with patch.object(b,"parent_module",return_value=parent):self.assertEqual(len(b.regression_modules(Path.cwd())),130)
    def test_24_constructed_historical_filter(self):
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        suite=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture_{i}") for i in range(3049)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            result=b.regression_suite(Path.cwd());self.assertEqual(result.countTestCases(),b.manifest()["focused_tests"])
            self.assertNotIn(b.EXCLUDED,{t.id() for t in b.flatten(result)})


if __name__=="__main__":unittest.main(verbosity=2)
