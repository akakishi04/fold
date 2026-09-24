"""C251 authoring checks. Toy encoders/cores are not scientific evidence."""
import ast
from collections import Counter
import contextlib
import copy
import hashlib
import inspect
import io
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as base
from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c251_precore_read as b
from tests_lm.test_v05_c250_fresh_seed_replication import fixture, Fitting, Audit, metric


class ToyEncoder(nn.Module):
    def __init__(self):
        super().__init__(); self.linear = nn.Linear(16,16,dtype=torch.float64)
    def forward(self,x):
        # Cheap causal prefix model for exercising the real wrapper's hooks.
        y = self.linear(x).cumsum(1)/torch.arange(1,x.shape[1]+1,dtype=x.dtype)[None,:,None]
        return y, y[:,-1].unsqueeze(0)


class ToyCore(nn.Module):
    def __init__(self):
        super().__init__(); self.layers = nn.ModuleList([nn.Linear(16,16,dtype=torch.float64) for _ in range(2)])
    def forward(self,working,context,*,route_index):
        return working + .3*torch.tanh(self.layers[route_index](context+working))


class Backbone(nn.Module):
    def __init__(self):
        super().__init__()
        self.config = SimpleNamespace(width=16,max_tokens=48,next_route=0,instruction_route=1,internal_steps=2)
        self.byte_embedding = nn.Embedding(259,16,padding_idx=256,dtype=torch.float64)
        self.local_encoder = ToyEncoder()
        self.core = ToyCore()
        self.readout_norm = nn.LayerNorm(16,dtype=torch.float64)
        self.decoder = nn.Linear(16,256,dtype=torch.float64)
        n = sum(p.numel() for p in self.parameters())
        self.unused_padding = nn.Parameter(torch.zeros(13488-n,dtype=torch.float64))
    def forward(self,tokens,tasks):
        valid = tokens != 256
        context = self.local_encoder(self.byte_embedding(tokens))[0]*valid.unsqueeze(-1)
        working = torch.zeros_like(context)
        for _ in range(self.config.internal_steps):
            nxt = self.core(working,context,route_index=0)
            other = self.core(working,context,route_index=1)
            working = torch.where(tasks.bool()[:,None,None],other,nxt)
        pooled = working[torch.arange(len(tokens)),valid.sum(1)-1]
        return self.decoder(self.readout_norm(pooled))


class Factory:
    @staticmethod
    def new_model(seed):
        torch.manual_seed(seed); return Backbone().eval()
    @staticmethod
    def fingerprint(model):
        h = hashlib.sha256()
        for k,v in sorted(model.state_dict().items()):
            h.update(k.encode()); h.update(v.detach().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    @staticmethod
    def tensors(rows,mode):
        names = {"en":("box","book"),"ja":("箱","本")}
        encoded = []
        for r in rows:
            pairs = list(enumerate(r["values"]))
            if r["order"]: pairs.reverse()
            n = names[r["language"]]
            text = ";".join(n[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in pairs)
            text += ";"+("?" if mode=="query_blind" else n[r["query"]])+"="
            ids = [257,*text.encode(),258]
            encoded.append(ids+[256]*(48-len(ids)))
        return torch.tensor(encoded),torch.tensor([r["target"] for r in rows])


def records():
    return [dict(seed=s,family="full",arm="precore_read",parameters=14256,block_updates=[200,200],
        fit=dict(steps=400,answer_presentations=12800),forward_calls=415,row_presentations=13568,
        weights_changed=True,head_weights_changed=True,checkpoint_roundtrip=True,prediction_replayed=True,
        initial_metric_error=0.,reload_max_error=0.,initial_sha256="a"*64,c250_initial_sha256="a"*64,
        final={k:metric(n) for k,n in b.ROWS.items()},c250_comparator={k:metric(n) for k,n in b.ROWS.items()}) for s in b.SEEDS]


def payload(s):
    pins={f"parent-{i}":"fixture" for i in range(346)}; pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(563)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=s,status="PASS" if s["candidate_gate"] else "FAIL",
        production_adoption=False,gate_f_candidate=False,network_calls=0)


class C251Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.parts=fixture()
        cls.tokens,cls.targets=Binding.tensors(cls.parts["TRAIN"][:4],"normal")
        cls.tasks=torch.zeros(4,dtype=torch.int64)

    def test_01_manifest_and_partition(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["split-dataset.json"])
        self.assertEqual(len(b.identities()),5)

    def test_02_zero_head_matches_original_and_complete_state(self):
        model=Factory.new_model(9010)
        old=reader.ReadoutPilot(copy.deepcopy(model),"full","token_read",9010)
        new=b.PrecoreReadout(copy.deepcopy(model),9010)
        self.assertEqual(Factory.fingerprint(old),Factory.fingerprint(new))
        self.assertEqual(sum(p.numel() for p in new.parameters()),14256)
        with torch.no_grad(): self.assertTrue(torch.equal(old(self.tokens,self.tasks),new(self.tokens,self.tasks)))

    def test_03_memory_is_encoder_query_is_postcore(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010)
        captures={}
        h1=model.backbone.local_encoder.register_forward_hook(lambda m,a,o:captures.update(encoder=o[0]))
        def core(m,a,k,o):
            if k["route_index"]==0: captures["postcore"]=o
        h2=model.backbone.core.register_forward_hook(core,with_kwargs=True)
        h3=model.read.register_forward_pre_hook(lambda m,a:captures.update(query=a[0],memory=a[1],valid=a[2]))
        model(self.tokens,self.tasks)
        for h in (h1,h2,h3):h.remove()
        valid=self.tokens!=256; eos=valid.sum(1)-1
        self.assertTrue(torch.equal(captures["memory"],captures["encoder"]*valid.unsqueeze(-1)))
        self.assertTrue(torch.equal(captures["query"],captures["postcore"][torch.arange(4),eos]))
        self.assertFalse(torch.equal(captures["memory"],captures["postcore"]))

    def test_04_nonzero_reader_manual_formula(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010); captured={}
        with torch.no_grad():model.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        h=model.read.register_forward_pre_hook(lambda m,a:captured.update(pool=a[0],states=a[1],valid=a[2]))
        out=model(self.tokens,self.tasks);h.remove()
        hidd=captured["states"]; pool=captured["pool"]
        q=model.read.query(pool)
        weights=((model.read.key(hidd)*q[:,None,:]).sum(-1)/4).masked_fill(~captured["valid"],float("-inf")).softmax(-1)
        wanted=model.backbone.decoder(model.backbone.readout_norm(pool+model.read.output((weights[:,:,None]*hidd).sum(1))))
        self.assertTrue(torch.equal(out,wanted))

    def test_05_backbone_core_and_encoder_gradients_survive(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010)
        with torch.no_grad():model.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        torch.nn.functional.cross_entropy(model(self.tokens,self.tasks),self.targets).backward()
        for p in (model.read.query.weight,model.read.key.weight,model.backbone.local_encoder.linear.weight,model.backbone.core.layers[0].weight):
            self.assertIsNotNone(p.grad); self.assertGreater(float(p.grad.abs().sum()),0)

    def test_06_pad_values_do_not_enter_read(self):
        head=reader.ResidualHead("token_read",9010)
        with torch.no_grad():head.output.weight.copy_(torch.eye(16,dtype=torch.float64))
        valid=self.tokens!=256;states=torch.randn(4,48,16,dtype=torch.float64);pool=states[:,0]
        changed=states.clone();changed[~valid]=12345
        self.assertTrue(torch.equal(head(pool,states,valid),head(pool,changed,valid)))

    def test_07_hook_cleanup_on_success_and_error(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010)
        model(self.tokens,self.tasks)
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))
        with patch.object(model.read,"forward",side_effect=ValueError("fixture")),self.assertRaises(ValueError):model(self.tokens,self.tasks)
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))

    def test_08_changed_core_context_detected(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010)
        h=model.backbone.core.register_forward_pre_hook(lambda m,a:(a[0],a[1]+1))
        with self.assertRaisesRegex(ValueError,"pre-core context"):model(self.tokens,self.tasks)
        h.remove()

    def test_09_invalid_task_and_eos_rejected(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010)
        with self.assertRaises(ValueError):model(self.tokens,torch.ones(4,dtype=torch.int64))
        bad=self.tokens.clone();bad[bad==258]=0
        with self.assertRaises(ValueError):model(bad,self.tasks)

    def test_10_pure_eval_does_not_change_state(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010).eval();before=Factory.fingerprint(model)
        with torch.no_grad():model(self.tokens,self.tasks)
        self.assertEqual(Factory.fingerprint(model),before)

    def test_11_whole_seed_gate_not_averaged(self):
        r=records();r[0]["final"]["HOLDOUT"]["en"].update(accuracy=.5,evidence_drop=.25,query_drop=0.)
        s=b.summarize(r,Fitting);self.assertFalse(s["candidate_gate"]);self.assertEqual(s["seed_pass_count"],4)
        b.validate_result(payload(s))

    def test_12_mask_gate_at_perfect_accuracy(self):
        r=records();r[1]["final"]["TRAIN"]["en"].update(evidence_blind_accuracy=1.,evidence_drop=0.)
        s=b.summarize(r,Fitting);self.assertEqual(s["cell_outcomes"]["TRAIN_CRITERIA_MISS"],1)
        self.assertFalse(s["candidate_gate"])

    def test_13_mismatched_initial_or_counts_rejected(self):
        for k,v in (("initial_sha256","b"*64),("forward_calls",414),("reload_max_error",float("nan"))):
            r=records();r[0][k]=v
            with self.assertRaises(ValueError):b.summarize(r,Fitting)

    def test_14_comparator_not_used_as_new_result(self):
        r=records()
        for row in r:
            for l in ("en","ja"):row["c250_comparator"]["HOLDOUT"][l].update(accuracy=.5,evidence_drop=.25,query_drop=0.)
        s=b.summarize(r,Fitting)
        self.assertTrue(s["candidate_gate"]);self.assertEqual(s["comparator_seed_pass_count"],0)
        self.assertTrue(all(c["delta"]==.5 for c in s["cells"]))

    def test_15_actual_loader_selects_all_five_from_twenty(self):
        refs=[];parent_records=[]
        for seed in b.SEEDS:
            for family in ("full","gru_only"):
                ref=dict(seed=seed,family=family,initial_sha256="a"*64,initial_train=metric(64));refs.append(ref)
                for arm in ("token_read","eos_adapter"):
                    pred={s:{v:([r["target"] for r in rows] if v=="normal" else [48]*len(rows)) for v in b.VIEWS} for s,rows in self.parts.items()}
                    final={s:{l:dict(m,answer_nll=.1) for l,m in Fitting.discrete_metrics(rows,pred[s]).items()} for s,rows in self.parts.items()}
                    parent_records.append(dict(seed=seed,family=family,arm=arm,backbone_initial_sha256="a"*64,initial_sha256="b"*64,initial_train=metric(64),predictions=pred,final=final))
        ba=SimpleNamespace(parent_module=lambda:SimpleNamespace(discrete_metrics=Fitting.discrete_metrics))
        audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA,read_json=Audit.read_json)
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(ba,Fitting,Binding,Factory,audit)),patch.object(b.parent,"validate_result"),patch.object(b.parent,"summarize",return_value={"fixture":20}):
            root=Path(d)
            for n,v in (("split-dataset.json",self.parts),("initial-references.json",refs),("measurements.json",parent_records),("summary.json",dict(validation_summary={"fixture":20}))):(root/n).write_bytes(b.blob(v))
            parts,rr,cc=b.load_inputs(root/"summary.json")
            self.assertEqual(parts,self.parts);self.assertEqual([r["seed"] for r in rr],list(b.SEEDS));self.assertEqual(len(cc),5)
            parent_records[0]["final"]["TRAIN"]["en"]["accuracy"]=.5
            (root/"measurements.json").write_bytes(b.blob(parent_records))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_16_wrong_initial_blocks_training(self):
        model=b.PrecoreReadout(Factory.new_model(9010),9010)
        with patch.object(reader,"fit") as fit,self.assertRaises(ValueError):
            reader.train_one(model,self.parts,{"initial_sha256":"wrong"},"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        fit.assert_not_called()

    def test_17_inherited_real_train_and_replay_on_new_wrapper(self):
        backbone=Factory.new_model(9010)
        initial,_=Fitting.evaluate(backbone,self.parts["TRAIN"],Binding,Factory.fingerprint)
        ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(backbone),initial_train=initial)
        model=b.PrecoreReadout(backbone,9010)
        with contextlib.redirect_stdout(io.StringIO()):r,state,raw=reader.train_one(model,self.parts,ref,"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        base.replay_one(b.PrecoreReadout(Factory.new_model(9010),9010),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,13568))

    def test_18_actual_five_model_run_and_postcheck(self):
        refs=[];comps=[]
        for seed in b.SEEDS:
            model=Factory.new_model(seed);initial,_=Fitting.evaluate(model,self.parts["TRAIN"],Binding,Factory.fingerprint)
            refs.append(dict(seed=seed,family="full",initial_sha256=Factory.fingerprint(model),initial_train=initial))
            comps.append(dict(seed=seed,family="full",arm="token_read",initial_sha256=Factory.fingerprint(reader.ReadoutPilot(copy.deepcopy(model),"full","token_read",seed)),final={s:metric(n) for s,n in b.ROWS.items()}))
        p=payload(b.summarize(records(),Fitting));ba=SimpleNamespace(replay_one=base.replay_one,parent_module=lambda:SimpleNamespace(discrete_metrics=Fitting.discrete_metrics))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(ba,Fitting,Binding,Factory,Audit)),patch.object(b,"precheck",return_value=(p["source_blobs"],p["input_sha256"])) as pre,patch.object(b,"load_inputs",return_value=(self.parts,refs,comps)) as load:
            out=Path(d)/"out";src=Path(d)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c250_summary=src,output_dir=out,expected_head="synthetic-head")
            load.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,src,"synthetic-head")[0],result)
            with self.assertRaises(ValueError):b.verify_artifacts(out,src,"wrong")
            (out/"measurements.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,src,"synthetic-head")

    def test_19_new_bundle_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"model.pt";v=dict(schema="fold-c251-precore-read-v1",identities=[list(x) for x in b.identities()],states=[{}]*5)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),5)
            v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_20_no_model_selection_or_detachment_path(self):
        calls={n.func.attr for n in ast.walk(ast.parse(inspect.getsource(b.PrecoreReadout))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)}
        self.assertNotIn("detach",calls);self.assertNotIn("load_state_dict",calls)
        self.assertEqual(b.SEEDS,(250001,250002,250003,250004,250005))

    def test_21_progress_changes_no_scientific_input(self):
        stream=io.StringIO();p=b.Progress(stream);p.write("[C248] step=100/400");p.flush()
        self.assertEqual(stream.getvalue(),"[C251] step=100/400")

    def test_22_runtime_call_order(self):
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,k in calls if k==name)
        for a,c in (("load_inputs","train_one"),("PrecoreReadout","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):self.assertLess(first(a),first(c))

    def test_23_runner_cli_paths_parser(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c251.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c251.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(s):
            return {n.slice.value for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launcher.index("::ParseFile"),launcher.index("$failure = $null"))
        self.assertIn("c250-v5b-fresh-seed-replication-9bf33a726c614e558f446871954550d7",launcher)

    def test_24_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),24)
        self.assertEqual(len({t.id() for t in b.flatten(suite)}),b.manifest()["own_tests"])
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])


if __name__=="__main__":unittest.main(verbosity=2)
