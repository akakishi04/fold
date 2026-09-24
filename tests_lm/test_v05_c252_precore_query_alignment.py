"""C252 authoring checks. Toy encoders/cores are not scientific evidence."""
import ast
import contextlib
import copy
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

from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as base
from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
from fold_lm.v05_benchmarks import model_c251_precore_read as parent
from fold_lm.v05_benchmarks import model_c252_precore_query_alignment as b
from tests_lm.test_v05_c251_precore_read import Backbone, Factory, Binding, Fitting, Audit, fixture, metric


def records():
    return [dict(seed=s,family="full",arm="aligned_precore_read",parameters=14256,block_updates=[200,200],
        fit=dict(steps=400,answer_presentations=12800),forward_calls=415,row_presentations=13568,
        weights_changed=True,head_weights_changed=True,checkpoint_roundtrip=True,prediction_replayed=True,
        initial_metric_error=0.,reload_max_error=0.,initial_sha256="a"*64,c251_initial_sha256="a"*64,
        final={k:metric(n) for k,n in b.ROWS.items()},c251_comparator={k:metric(n) for k,n in b.ROWS.items()})
        for s in b.SEEDS]


def payload(s):
    pins={f"parent-{i}":"fixture" for i in range(352)};pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(575)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=s,
        status="PASS" if s["candidate_gate"] else "FAIL",production_adoption=False,gate_f_candidate=False,network_calls=0)


class C252Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=fixture()
        cls.tokens,cls.targets=Binding.tensors(cls.parts["TRAIN"][:4],"normal")
        cls.tasks=torch.zeros(4,dtype=torch.int64)

    def test_01_manifest_partition_and_identities(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["split-dataset.json"])
        self.assertEqual(b.identities(),[(s,"full","aligned_precore_read") for s in b.SEEDS])

    def test_02_initial_state_matches_c251_exactly(self):
        backbone=Factory.new_model(9010)
        old=parent.PrecoreReadout(copy.deepcopy(backbone),9010)
        new=b.AlignedPrecoreReadout(copy.deepcopy(backbone),9010)
        self.assertEqual(Factory.fingerprint(old),Factory.fingerprint(new))
        self.assertEqual(sum(p.numel() for p in new.parameters()),14256)
        with torch.no_grad():self.assertTrue(torch.equal(old(self.tokens,self.tasks),new(self.tokens,self.tasks)))

    def test_03_memory_and_query_are_precore_residual_is_postcore(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010);cap={}
        h1=model.backbone.local_encoder.register_forward_hook(lambda m,a,o:cap.update(local=o[0]))
        def core(m,a,k,o):
            if k["route_index"]==0:cap["post"]=o
        h2=model.backbone.core.register_forward_hook(core,with_kwargs=True)
        h3=model.backbone.readout_norm.register_forward_pre_hook(lambda m,a:cap.update(norm_in=a[0]))
        orig_q=model.read.query.forward
        def q(x):cap["query_input"]=x;return orig_q(x)
        with patch.object(model.read.query,"forward",side_effect=q):model(self.tokens,self.tasks)
        for h in (h1,h2,h3):h.remove()
        valid=self.tokens!=256;eos=valid.sum(1)-1
        self.assertTrue(torch.equal(cap["query_input"],cap["local"][torch.arange(4),eos]))
        self.assertTrue(torch.equal(cap["post"][torch.arange(4),eos]+
            (cap["norm_in"]-cap["post"][torch.arange(4),eos]),cap["norm_in"]))
        self.assertFalse(torch.equal(cap["query_input"],cap["post"][torch.arange(4),eos]))

    def test_04_manual_formula_matches_forward(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010);cap={}
        with torch.no_grad():model.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        h1=model.backbone.local_encoder.register_forward_hook(lambda m,a,o:cap.update(local=o[0]))
        def core(m,a,k,o):
            if k["route_index"]==0:cap["post"]=o
        h2=model.backbone.core.register_forward_hook(core,with_kwargs=True)
        out=model(self.tokens,self.tasks);h1.remove();h2.remove()
        valid=self.tokens!=256;eos=valid.sum(1)-1;local=cap["local"]*valid.unsqueeze(-1)
        post=cap["post"][torch.arange(4),eos];pre=local[torch.arange(4),eos]
        q=model.read.query(pre);score=(model.read.key(local)*q[:,None,:]).sum(-1)/4
        alpha=score.masked_fill(~valid,float("-inf")).softmax(-1)
        wanted=model.backbone.decoder(model.backbone.readout_norm(post+model.read.output((alpha[:,:,None]*local).sum(1))))
        self.assertTrue(torch.equal(out,wanted))

    def test_05_query_key_encoder_and_core_gradients_survive(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010)
        with torch.no_grad():model.read.output.weight.copy_(torch.eye(16,dtype=torch.float64)*.1)
        torch.nn.functional.cross_entropy(model(self.tokens,self.tasks),self.targets).backward()
        for p in (model.read.query.weight,model.read.key.weight,model.backbone.local_encoder.linear.weight,model.backbone.core.layers[0].weight):
            self.assertIsNotNone(p.grad);self.assertGreater(float(p.grad.abs().sum()),0)

    def test_06_pad_positions_cannot_change_reader_result(self):
        head=reader.ResidualHead("token_read",9010)
        with torch.no_grad():head.output.weight.copy_(torch.eye(16,dtype=torch.float64))
        valid=self.tokens!=256;states=torch.randn(4,48,16,dtype=torch.float64);query=states[:,0]
        changed=states.clone();changed[~valid]=12345
        q=head.query(query)
        def result(x):
            score=(head.key(x)*q[:,None,:]).sum(-1)/4
            alpha=score.masked_fill(~valid,float("-inf")).softmax(-1)
            return head.output((alpha[:,:,None]*x).sum(1))
        self.assertTrue(torch.equal(result(states),result(changed)))

    def test_07_hooks_cleanup_success_and_error(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010);model(self.tokens,self.tasks)
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))
        with patch.object(model.read.output,"forward",side_effect=ValueError("fixture")),self.assertRaises(ValueError):
            model(self.tokens,self.tasks)
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))

    def test_08_core_context_mismatch_rejected(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010)
        h=model.backbone.core.register_forward_pre_hook(lambda m,a:(a[0],a[1]+1))
        with self.assertRaisesRegex(ValueError,"pre-core context"):model(self.tokens,self.tasks)
        h.remove()

    def test_09_invalid_task_and_eos_rejected(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010)
        with self.assertRaises(ValueError):model(self.tokens,torch.ones(4,dtype=torch.int64))
        bad=self.tokens.clone();bad[bad==258]=0
        with self.assertRaises(ValueError):model(bad,self.tasks)

    def test_10_eval_does_not_change_state(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010).eval();before=Factory.fingerprint(model)
        with torch.no_grad():model(self.tokens,self.tasks)
        self.assertEqual(Factory.fingerprint(model),before)

    def test_11_whole_seed_gate_not_average(self):
        r=records();r[0]["final"]["HOLDOUT"]["en"].update(accuracy=.5,evidence_drop=.25,query_drop=0.)
        s=b.summarize(r,Fitting);self.assertFalse(s["candidate_gate"]);self.assertEqual(s["seed_pass_count"],4);b.validate_result(payload(s))

    def test_12_mask_gate_still_required(self):
        r=records();r[1]["final"]["TRAIN"]["en"].update(evidence_blind_accuracy=1.,evidence_drop=0.)
        s=b.summarize(r,Fitting);self.assertFalse(s["candidate_gate"]);self.assertEqual(s["cell_outcomes"]["TRAIN_CRITERIA_MISS"],1)

    def test_13_mismatched_initial_counts_or_nonfinite_rejected(self):
        for k,v in (("initial_sha256","b"*64),("forward_calls",414),("reload_max_error",float("nan"))):
            r=records();r[0][k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):b.summarize(r,Fitting)

    def test_14_comparator_does_not_decide_candidate_gate(self):
        r=records()
        for row in r:
            for lang in ("en","ja"):row["c251_comparator"]["HOLDOUT"][lang].update(accuracy=.5,evidence_drop=.25,query_drop=0.)
        s=b.summarize(r,Fitting);self.assertTrue(s["candidate_gate"]);self.assertEqual(s["comparator_seed_pass_count"],0)

    def test_15_loader_adapts_c251_final_and_initial_fields(self):
        comps=[];base_metrics={s:metric(n) for s,n in b.ROWS.items()}
        for seed in b.SEEDS:
            pred={s:{v:([r["target"] for r in rows] if v=="normal" else [48]*len(rows)) for v in b.VIEWS} for s,rows in self.parts.items()}
            final={s:{l:dict(m,answer_nll=.1) for l,m in Fitting.discrete_metrics(rows,pred[s]).items()} for s,rows in self.parts.items()}
            comps.append(dict(seed=seed,family="full",arm="precore_read",backbone_initial_sha256="a"*64,
                initial_sha256="b"*64,initial_train=metric(64),predictions=pred,final=final))
        parent_adapter=SimpleNamespace(validate_result=lambda p:None,summarize=lambda r,f:{"fixture":5})
        base_adapter=SimpleNamespace(parent_module=lambda:SimpleNamespace(discrete_metrics=Fitting.discrete_metrics))
        audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA,read_json=Audit.read_json)
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent_adapter,base_adapter,Fitting,Binding,Factory,audit)):
            root=Path(d)
            for n,v in (("split-dataset.json",self.parts),("measurements.json",comps),("summary.json",dict(validation_summary={"fixture":5}))):(root/n).write_bytes(b.blob(v))
            parts,refs,got=b.load_inputs(root/"summary.json");self.assertEqual(parts,self.parts);self.assertEqual(len(refs),len(got),5)
            comps[0]["final"]["TRAIN"]["en"]["accuracy"]=.5;(root/"measurements.json").write_bytes(b.blob(comps))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_16_wrong_initial_blocks_fit(self):
        model=b.AlignedPrecoreReadout(Factory.new_model(9010),9010)
        with patch.object(reader,"fit") as fit,self.assertRaises(ValueError):
            reader.train_one(model,self.parts,{"initial_sha256":"wrong"},"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        fit.assert_not_called()

    def test_17_inherited_train_and_replay_on_new_wrapper(self):
        backbone=Factory.new_model(9010);initial,_=Fitting.evaluate(backbone,self.parts["TRAIN"],Binding,Factory.fingerprint)
        ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(backbone),initial_train=initial)
        model=b.AlignedPrecoreReadout(backbone,9010)
        with contextlib.redirect_stdout(io.StringIO()):r,state,raw=reader.train_one(model,self.parts,ref,"token_read",fitting=Fitting,binding=Binding,factory=Factory)
        base.replay_one(b.AlignedPrecoreReadout(Factory.new_model(9010),9010),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(415,13568))

    def test_18_five_model_run_and_postcheck(self):
        refs=[];comps=[]
        for seed in b.SEEDS:
            backbone=Factory.new_model(seed);initial,_=Fitting.evaluate(backbone,self.parts["TRAIN"],Binding,Factory.fingerprint)
            refs.append(dict(seed=seed,family="full",initial_sha256=Factory.fingerprint(backbone),initial_train=initial))
            comps.append(dict(seed=seed,family="full",arm="precore_read",initial_sha256=Factory.fingerprint(parent.PrecoreReadout(copy.deepcopy(backbone),seed)),
                final={s:metric(n) for s,n in b.ROWS.items()}))
        p=payload(b.summarize(records(),Fitting));base_adapter=SimpleNamespace(replay_one=base.replay_one,parent_module=lambda:SimpleNamespace(discrete_metrics=Fitting.discrete_metrics))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,base_adapter,Fitting,Binding,Factory,Audit)),patch.object(b,"precheck",return_value=(p["source_blobs"],p["input_sha256"])) as pre,patch.object(b,"load_inputs",return_value=(self.parts,refs,comps)) as load:
            out=Path(d)/"out";src=Path(d)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c251_summary=src,output_dir=out,expected_head="synthetic-head")
            load.assert_called_once();self.assertEqual(pre.call_count,2);self.assertEqual(b.verify_artifacts(out,src,"synthetic-head")[0],result)
            with self.assertRaises(ValueError):b.verify_artifacts(out,src,"wrong")
            (out/"measurements.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,src,"synthetic-head")

    def test_19_bundle_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"m.pt";v=dict(schema="fold-c252-precore-query-v1",identities=[list(x) for x in b.identities()],states=[{}]*5)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),5);v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_20_no_detach_checkpoint_or_seed_selection(self):
        src=inspect.getsource(b.AlignedPrecoreReadout)
        self.assertNotIn(".detach(",src);self.assertNotIn("load_state_dict",src);self.assertEqual(b.SEEDS,(250001,250002,250003,250004,250005))

    def test_21_progress_is_console_only(self):
        s=io.StringIO();p=b.Progress(s);p.write("[C248] step=100/400");p.flush();self.assertEqual(s.getvalue(),"[C252] step=100/400")

    def test_22_runtime_call_order(self):
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,k in calls if k==name)
        for a,c in (("load_inputs","train_one"),("AlignedPrecoreReadout","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):self.assertLess(first(a),first(c))

    def test_23_runner_cli_paths_parser(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c252.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c252.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(s):
            return {n.slice.value for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launcher.index("::ParseFile"),launcher.index("$failure = $null"));self.assertIn("c251-v5b-precore-read-dcc6ca85fe504ea7a71db741ab1558b1",launcher)

    def test_24_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),24);self.assertEqual(len({t.id() for t in b.flatten(suite)}),24)
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])


if __name__=="__main__":unittest.main(verbosity=2)
