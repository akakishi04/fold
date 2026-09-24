"""C247 authoring tests; inherited synthetic helpers are not capability evidence."""
import ast
from collections import Counter
import contextlib
import copy
import inspect
import io
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from fold_lm.v05_benchmarks import model_c247_normal_exposure_control as b
from tests_lm.test_v05_c246_training_erasure import Factory, Binding, Fitting, Audit, fixture, good_metrics


def records():
    return [dict(seed=s,family=f,final={k:good_metrics(n) for k,n in b.ROWS.items()},
        c246_comparator={k:good_metrics(n,False) for k,n in b.ROWS.items()},
        c244_comparator={k:good_metrics(n) for k,n in b.ROWS.items()},
        block_updates=[100,100],fit=dict(steps=200,answer_presentations=6400),
        forward_calls=215,row_presentations=7168,checkpoint_roundtrip=True,prediction_replayed=True,
        reload_max_error=0.,weights_changed=True) for s,f in b.identities()]


def payload(s):
    pins={f"parent-{i}":"fixture" for i in range(322)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        status="PASS" if s["full_train_control_gate"] else "FAIL",source_blobs=pins,
        input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(514)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,network_calls=0)


class C247Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=fixture();cls.parent=b.parent_module();cls.base=cls.parent.context()[1]

    def exercise(self):
        model=Factory.new_model(9010)
        ref=dict(seed=9010,family="full",initial_sha256=Factory.fingerprint(model),
            final={s:good_metrics(n,False) for s,n in b.ROWS.items()},
            c244_comparator={s:good_metrics(n) for s,n in b.ROWS.items()})
        with contextlib.redirect_stdout(io.StringIO()):
            return b.train_one(model,self.parts,ref,base=self.base,fitting=Fitting,binding=Binding,factory=Factory)

    def test_01_manifest_and_partition_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.SPLIT_SHA)
        self.assertEqual(b.manifest()["masked_updates"],0)

    def test_02_exact_parent_normal_subsequence(self):
        selected=[s for s in range(400) if s%4>=2]
        self.assertEqual([b.parent_normal_step(s) for s in range(200)],selected)
        for s,p in enumerate(selected):
            self.assertTrue(torch.equal(b.balanced_indices(64,s),self.parent.balanced_indices(64,p)))

    def test_03_per_row_normal_exposure_is100(self):
        counts=Counter()
        for s in range(200):counts.update(b.balanced_indices(64,s).tolist())
        self.assertEqual(counts,{i:100 for i in range(64)})
        self.assertEqual(sum(counts.values()),6400)

    def test_04_invalid_steps_or_batch_count_rejected(self):
        for s in (-1,200,True):
            with self.assertRaises(ValueError):b.parent_normal_step(s)
        for n,s in ((32,0),(64,-1),(64,True)):
            with self.assertRaises(ValueError):b.balanced_indices(n,s)

    def test_05_actual_parent_optimizer_ast_and_schedule(self):
        b.audit_recipe(self.base,self.parent)
        with patch.object(self.base,"LR",.1):
            with self.assertRaises(ValueError):b.audit_recipe(self.base,self.parent)

    def test_06_actual_fit_has_only_normal_batches(self):
        x,y=Binding.tensors(self.parts["TRAIN"],"normal");model=Factory.new_model(9011);seen=[]
        h=model.register_forward_pre_hook(lambda m,args:seen.append(args[0].clone()))
        b.fit(model,x,y,9012,steps=4);h.remove()
        self.assertEqual(len(seen),4)
        for step,batch in enumerate(seen):self.assertTrue(torch.equal(batch,x[self.base.balanced_indices(64,step)]))

    def test_07_holdout_first_scored_after_training(self):
        done=[False];native=b.fit
        def fitted(*args,**kwargs):out=native(*args,**kwargs);done[0]=True;return out
        class Checked(Fitting):
            @staticmethod
            def evaluate(model,rows,binding,fingerprint):
                if len(rows)==32 and not done[0]:raise AssertionError("early holdout")
                return Fitting.evaluate(model,rows,binding,fingerprint)
        ref=dict(initial_sha256=Factory.fingerprint(Factory.new_model(9010)),seed=9010,family="full",final={},c244_comparator={})
        with patch.object(b,"fit",side_effect=fitted),contextlib.redirect_stdout(io.StringIO()):
            b.train_one(Factory.new_model(9010),self.parts,ref,base=self.base,fitting=Checked,binding=Binding,factory=Factory)
        self.assertTrue(done[0])

    def test_08_wrong_initial_identity_stops_before_fit(self):
        with patch.object(b,"fit") as fitted:
            with self.assertRaises(ValueError):b.train_one(Factory.new_model(1),self.parts,{"initial_sha256":"bad"},base=self.base,fitting=Fitting,binding=Binding,factory=Factory)
            fitted.assert_not_called()

    def test_09_actual200_updates_and_forward_counts(self):
        r,_,_=self.exercise()
        self.assertEqual((r["fit"]["steps"],r["fit"]["answer_presentations"]),(200,6400))
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(209,6880))
        self.assertEqual(r["block_updates"],[100,100])

    def test_10_parent_replay_helper_accepts_shorter_training(self):
        r,state,raw=self.exercise()
        self.base.replay_one(Factory.new_model(9010),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(215,7168))

    def test_11_changed_logits_fail_replay(self):
        r,state,raw=self.exercise();raw["HOLDOUT"][0]=raw["HOLDOUT"][0]+.1
        with self.assertRaises(ValueError):self.base.replay_one(Factory.new_model(9010),state,r,raw,self.parts,fitting=Fitting,binding=Binding,factory=Factory)

    def test_12_primary_train_not_holdout(self):
        r=records()
        for row in r:row["final"]["HOLDOUT"]=good_metrics(32,False)
        s=b.summarize(r,Fitting);self.assertTrue(s["full_train_control_gate"])
        self.assertFalse(s["secondary_full_joint_gate"]);p=payload(s);b.validate_result(p);self.assertEqual(p["status"],"PASS")

    def test_13_full_and_gru_gates_are_separate(self):
        r=records();r[0]["final"]["TRAIN"]=good_metrics(64,False)
        s=b.summarize(r,Fitting);self.assertFalse(s["full_train_control_gate"]);self.assertTrue(s["gru_train_control_gate"])
        p=payload(s);b.validate_result(p);self.assertEqual(p["status"],"FAIL")

    def test_14_mask_criterion_matters_at100percent_accuracy(self):
        r=records()
        r[0]["final"]["TRAIN"]["en"].update(evidence_blind_accuracy=1.,evidence_drop=0.)
        s=b.summarize(r,Fitting);self.assertFalse(s["full_train_control_gate"])
        self.assertEqual(r[0]["final"]["TRAIN"]["en"]["accuracy"],1.)

    def test_15_comparison_labels_are_exhaustive(self):
        r=records();r[0]["c246_comparator"]["TRAIN"]=good_metrics(64)
        r[1]["final"]["TRAIN"]=good_metrics(64,False);r[1]["c246_comparator"]["TRAIN"]=good_metrics(64)
        r[2]["final"]["TRAIN"]=good_metrics(64,False)
        s=b.summarize(r,Fitting)
        self.assertEqual(s["comparison_counts"],{"BOTH_TRAIN_PASS":2,"C246_TRAIN_PASS_ONLY":2,"NEITHER_TRAIN_PASS":2,"CONTROL_TRAIN_PASS_ONLY":6})

    def test_16_invalid_counts_replay_or_weight_change(self):
        for k,v in (("forward_calls",214),("reload_max_error",1.),("weights_changed",False)):
            r=records();r[0][k]=v
            with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r,Fitting)))
        r=records();r[0]["block_updates"]=[200,200]
        with self.assertRaises(ValueError):b.summarize(r,Fitting)

    def test_17_failed_fit_removes_hooks(self):
        model=Factory.new_model(9010);ref=dict(initial_sha256=Factory.fingerprint(model),seed=9010)
        with patch.object(b,"fit",side_effect=ValueError("fixture")),self.assertRaises(ValueError):
            b.train_one(model,self.parts,ref,base=self.base,fitting=Fitting,binding=Binding,factory=Factory)
        self.assertFalse(model._forward_hooks)

    def test_18_actual_schedule_guard_detects_wrong_block(self):
        native=b.balanced_indices
        with patch.object(b,"balanced_indices",side_effect=lambda n,s:native(n,s+1)),self.assertRaisesRegex(ValueError,"actual normal optimizer batch"):
            self.exercise()

    def test_19_loader_replays_actual_parent_record_schema(self):
        refs=[]
        for seed,family in b.identities():
            predictions={s:{v:([r["target"] for r in rows] if v=="normal" else [48]*len(rows)) for v in b.VIEWS} for s,rows in self.parts.items()}
            final={s:{l:dict(m,answer_nll=.1) for l,m in Fitting.discrete_metrics(rows,predictions[s]).items()} for s,rows in self.parts.items()}
            refs.append(dict(seed=seed,family=family,initial_sha256="a"*64,final_sha256="b"*64,final=final,predictions=predictions,
                c244_comparator=copy.deepcopy(final),fit=dict(steps=400,answer_presentations=12800),block_updates=[200,200],block_view_updates=[[100,100],[100,100]],
                forward_calls=415,row_presentations=13568,checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.,weights_changed=True))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(self.parent,self.base,Fitting,Binding,Factory,Audit)), \
             patch.object(self.base,"parent_module",return_value=SimpleNamespace(discrete_metrics=Fitting.discrete_metrics)):
            root=Path(d);summary=self.parent.summarize(refs,self.base,Fitting)
            for name,value in (("split-dataset.json",self.parts),("measurements.json",refs),("summary.json",dict(validation_summary=summary))):(root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"),(self.parts,refs))
            refs[0]["initial_sha256"]=refs[0]["final_sha256"];(root/"measurements.json").write_bytes(b.blob(refs))
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_20_actual_six_model_run_and_postcheck(self):
        refs=[]
        for seed,family in b.identities():
            model=Factory.new_model(seed)
            if family=="gru_only":model=Binding.new_baseline(model)
            refs.append(dict(seed=seed,family=family,initial_sha256=Factory.fingerprint(model),final={s:good_metrics(n,False) for s,n in b.ROWS.items()},c244_comparator={s:good_metrics(n) for s,n in b.ROWS.items()}))
        p=payload(b.summarize(records(),Fitting))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(self.parent,self.base,Fitting,Binding,Factory,Audit)), \
             patch.object(b,"precheck",return_value=(p["source_blobs"],p["input_sha256"])) as pre, \
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader, \
             patch.object(self.base,"parent_module",return_value=SimpleNamespace(discrete_metrics=Fitting.discrete_metrics)):
            out=Path(d)/"out";parent=Path(d)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c246_summary=parent,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,parent,"synthetic-head")[0],result)
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,"wrong")
            (out/"measurements.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,parent,"synthetic-head")

    def test_21_bundle_identity_order(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"model.pt";value=dict(schema="fold-c247-normal-exposure-v1",identities=[list(x) for x in b.identities()],states=[{}]*6)
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),6)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    def test_22_own_count_and_constructed_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}),24)
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Case(b.EXCLUDED)]+[Case(f"fixture{i}") for i in range(3097)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_23_runner_cli_parent_path_and_parser(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c247.ps1").read_text(encoding="utf-8");launch=(root/"tools/invoke_c247.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c246-v5b-training-erasure-471de735eb204a129692672d2849c270",launch)

    def test_24_loader_copy_save_replay_order(self):
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        line=lambda name:min(i for i,k in calls if k==name)
        for first,second in (("load_inputs","train_one"),("new_baseline","train_one"),("train_one","save"),("save","load_bundle"),("load_bundle","replay_one")):
            self.assertLess(line(first),line(second))
        self.assertEqual(b.VIEWS,("normal","evidence_blind","query_blind"))


if __name__=="__main__":unittest.main(verbosity=2)
