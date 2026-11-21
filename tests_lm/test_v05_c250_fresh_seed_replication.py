"""C250 authoring checks; synthetic networks do not supply scientific results."""
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
from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as base
from fold_lm.v05_benchmarks import model_c250_fresh_seed_replication as b


def fixture():
    blocks={k:[] for k in ("old","added","held")};names={"en":("box","book"),"ja":("箱","本")}
    for x,y in itertools.permutations(range(4),2):
        block="old" if (x,y) in ((0,1),(1,0),(2,3),(3,2)) else "added" if (x,y) in ((0,2),(2,0),(1,3),(3,1)) else "held"
        group=f"0-1-{x}-{y}"
        for lang in names:
            for order,q in itertools.product((0,1),repeat=2):
                facts=[(0,x),(1,y)]
                if order: facts.reverse()
                r=dict(id=f"{lang}-{group}-{order}-{q}",group=group,objects=[0,1],values=[x,y],language=lang,order=order,query=q,
                    split="EVAL" if tuple(sorted((x,y))) in ((0,3),(1,2)) else "TRAIN",target=48+(x if q==0 else y))
                r["prompt"]=";".join(names[lang][k]+"="+str(v) for k,v in facts)+";"+names[lang][q]+"="
                blocks[block].append(r)
    return dict(TRAIN=blocks["old"]+blocks["added"],HOLDOUT=blocks["held"])


class Toy(nn.Module):
    def __init__(self,family="full"):
        super().__init__();self.linear=nn.Linear(4,256,dtype=torch.float64)
        self.padding=nn.Parameter(torch.zeros(b.BASE_PARAMS[family]-1280,dtype=torch.float64))
    def forward(self,tokens,tasks): return self.linear(tokens)


class ToyWrapper(nn.Module):
    """Lightweight protocol double; not the actual token encoder or FOLD core."""
    def __init__(self,backbone,family,arm,seed):
        super().__init__();self.backbone=backbone;self.read=reader.ResidualHead(arm,seed)
    def forward(self,tokens,tasks):
        pooled=tokens.repeat(1,4)
        states=torch.stack((pooled,pooled.flip(-1),pooled*.5),dim=1)
        valid=torch.ones(len(tokens),3,dtype=torch.bool)
        residual=self.read(pooled,states,valid)-pooled
        return self.backbone(tokens,tasks)+F.pad(residual,(48,192))


class Factory:
    @staticmethod
    def new_model(seed): torch.manual_seed(seed);return Toy().eval()
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for k,v in sorted(model.state_dict().items()):h.update(k.encode());h.update(v.detach().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    @staticmethod
    def parent_module(): return Binding
    @staticmethod
    def new_baseline(full):
        model=Toy("gru_only");model.linear.load_state_dict(copy.deepcopy(full.linear.state_dict()));return model.eval()
    @staticmethod
    def tensors(rows,view):
        x=torch.tensor([[*r["values"],r["query"],r["order"]] for r in rows],dtype=torch.float64)
        if view=="evidence_blind":x[:,:2]=0
        if view=="query_blind":x[:,2]=.5
        return x,torch.tensor([r["target"] for r in rows])


class Fitting:
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
                m[kind+"_pair_accuracy"]=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
            out[lang]=m
        return out
    @staticmethod
    def prediction_record(logits,n):
        b.require(len(logits)==3 and all(x.shape==(n,256) for x in logits),"test logits")
        return {v:x.argmax(-1).tolist() for v,x in zip(b.VIEWS,logits,strict=True)}
    @staticmethod
    def evaluate(model,rows,binding,fingerprint):
        before=fingerprint(model);mode=model.training;model.eval()
        try:
            with torch.no_grad():
                views=[binding.tensors(rows,v) for v in b.VIEWS]
                logits=[model(x,torch.zeros(len(rows),dtype=torch.int64)).detach() for x,_ in views]
        finally: model.train(mode)
        metrics=Fitting.discrete_metrics(rows,Fitting.prediction_record(logits,len(rows)))
        for lang,m in metrics.items():
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            m["answer_nll"]=float(F.cross_entropy(logits[0][ids],views[0][1][ids]))
        b.require(fingerprint(model)==before,"test evaluation mutation")
        return metrics,logits
    @staticmethod
    def validate_metrics(metrics,n):
        b.require(set(metrics)=={"en","ja"} and all(m["rows"]==n//2 and all(type(v) in (int,float) for v in m.values()) for m in metrics.values()),"test metric schema")
    @staticmethod
    def cell_pass(m):
        return m["accuracy"]>=.90 and all(m[k+"_pair_accuracy"]>=.80 for k in ("fact","query","order")) and m["evidence_drop"]>=.35 and m["query_drop"]>=.35


def metric(n):
    return {l:dict(rows=n//2,accuracy=1.,answer_nll=.01,fact_pair_accuracy=1.,query_pair_accuracy=1.,order_pair_accuracy=1.,
        evidence_blind_accuracy=.25,query_blind_accuracy=.5,evidence_drop=.75,query_drop=.5) for l in ("en","ja")}


def records_and_refs():
    refs=[dict(seed=s,family=f,initial_sha256=hashlib.sha256(f"{s}-{f}".encode()).hexdigest(),initial_train=metric(64),
        reference_forward_calls=3,reference_row_presentations=192) for s,f in b.reference_identities()]
    refmap={(r["seed"],r["family"]):r for r in refs}
    recs=[dict(seed=s,family=f,arm=a,backbone_initial_sha256=refmap[s,f]["initial_sha256"],
        parameters=b.BASE_PARAMS[f]+768,block_updates=[200,200],fit=dict(steps=400,answer_presentations=12800),
        forward_calls=415,row_presentations=13568,checkpoint_roundtrip=True,prediction_replayed=True,weights_changed=True,
        head_weights_changed=True,initial_metric_error=0.,reload_max_error=0.,final={k:metric(n) for k,n in b.ROWS.items()}) for s,f,a in b.identities()]
    return recs,refs


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(340)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,source_blobs=pins,
        input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(550)},artifacts=[dict(file=p) for p in b.OUTPUTS],
        validation_summary=summary,status="PASS" if summary["gates"]["token_read"]["full"] else "FAIL",production_adoption=False,gate_f_candidate=False,network_calls=0)


class Audit:
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
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
        if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


class C250Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):torch.set_num_threads(2);cls.parts=fixture()

    def test_01_manifest_fixed_partition_and_new_seeds(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA);self.assertEqual(b.digest(self.parts),b.SPLIT_SHA)
        self.assertTrue(set(b.SEEDS).isdisjoint(reader.SEEDS));self.assertEqual(len(b.identities()),20)

    def test_02_actual_initial_reference_counts(self):
        model=Factory.new_model(b.SEEDS[0]);r=b.initial_reference(model,self.parts,b.SEEDS[0],"full",fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["reference_forward_calls"],r["reference_row_presentations"]),(3,192))
        self.assertEqual(r["initial_sha256"],Factory.fingerprint(model))

    def test_03_unregistered_reference_stops(self):
        with self.assertRaises(ValueError):b.initial_reference(Factory.new_model(1),self.parts,234001,"full",fitting=Fitting,binding=Binding,factory=Factory)

    def test_04_reference_mutation_detected(self):
        class Mutating(Fitting):
            @staticmethod
            def evaluate(model,*args):
                result=Fitting.evaluate(model,*args)
                with torch.no_grad():model.linear.bias.add_(1.)
                return result
        with self.assertRaises(ValueError):b.initial_reference(Factory.new_model(b.SEEDS[0]),self.parts,b.SEEDS[0],"full",fitting=Mutating,binding=Binding,factory=Factory)

    def test_05_reference_never_renders_holdout(self):
        class Checked(Binding):
            @staticmethod
            def tensors(rows,view):
                if len(rows)!=64:raise AssertionError("holdout in reference")
                return Binding.tensors(rows,view)
        b.initial_reference(Factory.new_model(b.SEEDS[0]),self.parts,b.SEEDS[0],"full",fitting=Fitting,binding=Checked,factory=Factory)

    def test_06_old_record_or_reference_order_rejected(self):
        r,refs=records_and_refs()
        with self.assertRaises(ValueError):b.summarize(r,list(reversed(refs)),Fitting)
        r[0]["seed"]=234001
        with self.assertRaises(ValueError):b.summarize(r,refs,Fitting)

    def test_07_all_seeds_gate_and_full_workload(self):
        r,refs=records_and_refs();s=b.summarize(r,refs,Fitting);b.validate_result(payload(s))
        self.assertEqual((s["model_forward_calls"],s["row_presentations"]),(8330,273280))
        self.assertEqual(s["seed_pass_counts"]["token_read"]["full"],5)

    def test_08_single_full_seed_failure_not_dropped(self):
        r,refs=records_and_refs();r[0]["final"]["HOLDOUT"]["en"].update(accuracy=.5,evidence_drop=.25,query_drop=0.)
        s=b.summarize(r,refs,Fitting);self.assertFalse(s["gates"]["token_read"]["full"])
        self.assertEqual(s["seed_pass_counts"]["token_read"]["full"],4);b.validate_result(payload(s))

    def test_09_gru_and_control_gates_independent(self):
        r,refs=records_and_refs()
        for row in r:
            if row["family"]=="gru_only" or row["arm"]=="eos_adapter":row["final"]["HOLDOUT"]["ja"]["query_pair_accuracy"]=0.
        s=b.summarize(r,refs,Fitting);self.assertTrue(s["gates"]["token_read"]["full"]);self.assertFalse(s["gates"]["token_read"]["gru_only"])

    def test_10_seed_counts_not_language_counts(self):
        r,refs=records_and_refs();s=b.summarize(r,refs,Fitting)
        self.assertEqual(len(s["seed_results"]),20);self.assertEqual(s["cell_outcomes"]["token_read"],{"BOTH_PASS":20})
        self.assertEqual(s["seed_pass_counts"]["token_read"]["full"],5)

    def test_11_mask_criterion_not_only_accuracy(self):
        r,refs=records_and_refs();r[0]["final"]["TRAIN"]["en"].update(evidence_blind_accuracy=1.,evidence_drop=0.)
        self.assertFalse(b.summarize(r,refs,Fitting)["gates"]["token_read"]["full"])

    def test_12_pair_backbones_must_match_reference(self):
        r,refs=records_and_refs();r[1]["backbone_initial_sha256"]="0"*64
        with self.assertRaises(ValueError):b.summarize(r,refs,Fitting)

    def test_13_reference_cost_cannot_be_omitted(self):
        r,refs=records_and_refs();refs[0]["reference_forward_calls"]=0
        with self.assertRaises(ValueError):b.summarize(r,refs,Fitting)

    def test_14_replay_and_model_counts_rejected(self):
        for key,value in (("forward_calls",414),("reload_max_error",float("nan")),("head_weights_changed",False)):
            r,refs=records_and_refs();r[0][key]=value
            with self.assertRaises(ValueError):b.summarize(r,refs,Fitting)

    def test_15_reference_error_removes_hook(self):
        model=Factory.new_model(b.SEEDS[0]);broken=SimpleNamespace(evaluate=lambda *args:(_ for _ in ()).throw(ValueError("fixture")))
        with self.assertRaises(ValueError):b.initial_reference(model,self.parts,b.SEEDS[0],"full",fitting=broken,binding=Binding,factory=Factory)
        self.assertFalse(model._forward_hooks)

    def test_16_progress_only_changes_tag(self):
        out=io.StringIO();stream=b.Progress(out);stream.write("[C248] step=100/400\nunchanged");stream.flush()
        self.assertEqual(out.getvalue(),"[C250] step=100/400\nunchanged")

    def test_17_head_rule_zero_output_and_rng_unchanged(self):
        for arm in b.ARMS:
            torch.manual_seed(9010);before=torch.get_rng_state().clone();head=reader.ResidualHead(arm,b.SEEDS[0])
            self.assertTrue(torch.equal(before,torch.get_rng_state()));self.assertEqual(sum(p.numel() for p in head.parameters()),768)
            self.assertEqual(int(torch.count_nonzero(head.output.weight)),0)
            clone=reader.ResidualHead(arm,b.SEEDS[0]);self.assertEqual(Factory.fingerprint(head),Factory.fingerprint(clone))

    def test_18_inherited_training_and_reload_actually_run(self):
        seed=b.SEEDS[0];backbone=Factory.new_model(seed)
        ref=b.initial_reference(backbone,self.parts,seed,"full",fitting=Fitting,binding=Binding,factory=Factory)
        model=ToyWrapper(copy.deepcopy(backbone),"full","token_read",seed)
        with contextlib.redirect_stdout(io.StringIO()):r,state,raw=reader.train_one(model,self.parts,ref,"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        base.replay_one(ToyWrapper(Factory.new_model(seed),"full","token_read",seed),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,13568));self.assertTrue(r["head_weights_changed"])

    def test_19_wrong_initial_rejected_before_inherited_fit(self):
        model=ToyWrapper(Factory.new_model(b.SEEDS[0]),"full","token_read",b.SEEDS[0])
        with patch.object(reader,"fit") as fitted,self.assertRaises(ValueError):
            reader.train_one(model,self.parts,{"initial_sha256":"wrong"},"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        fitted.assert_not_called()

    def test_20_bundle_has_new_twenty_state_schema(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bundle.pt";v=dict(schema="fold-c250-fresh-seeds-v1",identities=[list(x) for x in b.identities()],states=[{}]*20)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),20)
            v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_21_actual_input_loader_uses_c248_not_c249_schema(self):
        parent=SimpleNamespace(load_inputs=lambda path:(self.parts,[]));seen=[]
        adapter=SimpleNamespace(validate_result=lambda p:seen.append(p))
        audit=SimpleNamespace(sha=lambda p:b.C248_SHA,read_json=lambda p:{"fixture":"C248"})
        with patch.object(b,"context",return_value=(parent,adapter,None,None,None,None,audit)):
            self.assertEqual(b.load_inputs(Path("C248-summary.json")),self.parts)
        self.assertEqual(seen,[{"fixture":"C248"}])

    def test_22_actual_twenty_model_run_and_postcheck(self):
        r,refs=records_and_refs();p=payload(b.summarize(r,refs,Fitting))
        base_adapter=SimpleNamespace(replay_one=base.replay_one,parent_module=lambda:SimpleNamespace(discrete_metrics=Fitting.discrete_metrics))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,reader,base_adapter,Fitting,Binding,Factory,Audit)),\
             patch.object(b,"precheck",return_value=(p["source_blobs"],p["input_sha256"])) as pre,\
             patch.object(b,"load_inputs",return_value=self.parts) as loader,patch.object(reader,"ReadoutPilot",ToyWrapper):
            out=Path(d)/"out";c249=Path(d)/"c249.json";c248=Path(d)/"c248.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c249_summary=c249,c248_summary=c248,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,c248,"synthetic-head")[0],result)
            self.assertEqual(result["validation_summary"]["reference_forwards"],30)
            with self.assertRaises(ValueError):b.verify_artifacts(out,c248,"wrong")
            (out/"initial-references.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,c248,"synthetic-head")

    def test_23_runner_cli_guards_and_parent_paths(self):
        root=Path(__file__).resolve().parents[1];run=(root/"tools/run_c250.ps1").read_text(encoding="utf-8");launch=(root/"tools/invoke_c250.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(s):
            return {n.slice.value for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1,2});self.assertEqual(argv(blocks[2]),{1,2,3,4})
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c249-v5b-frozen-read-ablation-9da92553f325421d8acd94d8cccc3b98",launch)
        self.assertIn("c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22",launch)

    def test_24_semantic_counts_and_real_call_order(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}),24)
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        count=b.manifest()["loaded_tests"];source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(count-1)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        line=lambda name:min(i for i,k in calls if k==name)
        for a,c in (("load_inputs","train_one"),("new_baseline","initial_reference"),("initial_reference","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):
            self.assertLess(line(a),line(c))


if __name__=="__main__":unittest.main(verbosity=2)
