"""C240 authoring tests; synthetic answer arrays are not scientific evidence."""
import ast
from collections import Counter
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
from fold_lm.v05_benchmarks import model_c240_saved_position_audit as b


def fixture():
    pool=[]; names={"en":("box","book"),"ja":("箱","本")}
    for x,y in ((0,1),(1,0)):
        group=f"0-1-{x}-{y}"
        for lang in names:
            for order,query in itertools.product((0,1),(0,1)):
                facts=[(0,x),(1,y)]
                if order: facts.reverse()
                text=";".join(names[lang][k]+"="+str(v) for k,v in facts)+";"+names[lang][query]+"="
                pool.append(dict(id=f"{lang}-{group}-{order}-{query}",group=group,objects=[0,1],values=[x,y],
                    language=lang,order=order,query=query,split="TRAIN",target=48+(x if query==0 else y),prompt=text))
    return {key:[r for r in pool if r["order"]==order] for key,order in zip(b.SPLITS,(0,1),strict=True)}


def record(parts,rule="query_fixed_position"):
    predictions={key:{mode:[b.rule_answers(r)[rule] if mode=="normal" else 48 for r in rows]
                    for mode in b.VIEWS} for key,rows in parts.items()}
    final={k:{l:dict(m,answer_nll=.7) for l,m in b.discrete_metrics(parts[k],predictions[k]).items()} for k in b.SPLITS}
    return dict(seed=234001,family="full",predictions=predictions,final=final,checkpoint_roundtrip=True,
                prediction_replayed=True,weights_changed=True,reload_max_error=0.0)


def records(parts,rule="query_fixed_position"):
    return [dict(copy.deepcopy(record(parts,rule)),seed=s,family=f) for s,f in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(280)};pins.update({p:"fixture" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(430)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,network_calls=0)


class Audit:
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def safe_child(root,name):
        p=(Path(root)/name).resolve()
        if p.parent!=Path(root).resolve(): raise ValueError("unsafe child")
        return p
    @staticmethod
    def git(root,*args):
        if args[:2]==("rev-parse","HEAD"): return b"synthetic-head"
        if args[:2]==("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


class C240Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.parts=fixture()

    def test_01_manifest_hash_and_zero_model_work(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        for key in ("model_forward_calls","new_training_steps","checkpoint_loads","checkpoint_writes"):
            self.assertEqual(b.manifest()[key],0)
        self.assertFalse(b.manifest()["nll_recomputed"])

    def test_02_exact_parent_partition_semantics(self):
        self.assertEqual(b.validate_parts(self.parts),self.parts)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["split-dataset.json"])
        self.assertEqual(Counter(r["language"] for r in self.parts["TRAIN"]),{"en":4,"ja":4})

    def test_03_parent_partition_tampering_rejected(self):
        for key,value in (("order",1),("target",255),("split","HOLDOUT")):
            p=copy.deepcopy(self.parts);p["TRAIN"][0][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError): b.validate_parts(p)

    def test_04_rules_do_not_read_target(self):
        r=copy.deepcopy(self.parts["TRAIN"][0]);a=b.rule_answers(r);r.pop("target")
        self.assertEqual(b.rule_answers(r),a)

    def test_05_training_rule_degeneracy_is_explicit(self):
        for row in self.parts["TRAIN"]:
            r=b.rule_answers(row);self.assertEqual(r["entity"],r["query_fixed_position"])

    def test_06_holdout_fixed_position_equals_other_not_correct(self):
        for row in self.parts["HOLDOUT"]:
            r=b.rule_answers(row)
            self.assertEqual(r["query_fixed_position"],48+row["values"][1-row["query"]])
            self.assertNotEqual(r["query_fixed_position"],r["entity"])

    def test_07_first_last_use_rendered_order(self):
        for split,rows in self.parts.items():
            for row in rows:
                r=b.rule_answers(row);values=row["values"] if split=="TRAIN" else row["values"][::-1]
                self.assertEqual((r["first"],r["last"]),(48+values[0],48+values[1]))

    def test_08_unrestricted_byte_validation(self):
        pred={m:[255]*8 for m in b.VIEWS};b.validate_predictions(pred)
        for value in (-1,256,True,48.0):
            bad=copy.deepcopy(pred);bad["normal"][0]=value
            with self.subTest(value=value):
                with self.assertRaises(ValueError): b.validate_predictions(bad)

    def test_09_prediction_views_and_lengths(self):
        p={m:[48]*8 for m in b.VIEWS};p["normal"].pop()
        with self.assertRaises(ValueError): b.validate_predictions(p)
        p={"normal":[48]*8}
        with self.assertRaises(ValueError): b.validate_predictions(p)

    def test_10_discrete_metrics_exact_binding(self):
        r=record(self.parts,"entity")
        for split in b.SPLITS:
            for m in b.discrete_metrics(self.parts[split],r["predictions"][split]).values():
                self.assertEqual((m["accuracy"],m["fact_pair_accuracy"],m["query_pair_accuracy"]),(1,1,1))
                self.assertEqual((m["evidence_drop"],m["query_drop"]),(.5,.5))

    def test_11_discrete_metrics_fixed_position_reverse_failure(self):
        r=record(self.parts)
        for m in b.discrete_metrics(self.parts["HOLDOUT"],r["predictions"]["HOLDOUT"]).values():
            self.assertEqual((m["accuracy"],m["fact_pair_accuracy"],m["query_pair_accuracy"]),(0,0,0))
            self.assertEqual(m["query_drop"],-.5)

    def test_12_saved_discrete_metric_mismatch_rejected(self):
        r=record(self.parts);r["final"]["HOLDOUT"]["en"]["accuracy"]=.5
        with self.assertRaises(ValueError): b.validate_record(self.parts,r)

    def test_13_nll_retained_not_reconstructed(self):
        r=record(self.parts);r["final"]["HOLDOUT"]["en"]["answer_nll"]=100.0
        b.validate_record(self.parts,r)
        for value in (float("nan"),float("inf"),-1):
            r["final"]["HOLDOUT"]["en"]["answer_nll"]=value
            with self.assertRaises(ValueError): b.validate_record(self.parts,r)

    def test_14_parent_flag_and_schema_rejected(self):
        r=record(self.parts);r["prediction_replayed"]=False
        with self.assertRaises(ValueError): b.validate_record(self.parts,r)
        r=record(self.parts);r["final_probe"]=r.pop("final")
        with self.assertRaises(KeyError): b.validate_record(self.parts,r)

    def test_15_wrong_other_entity_not_outside_value(self):
        report,detail,pairs=b.audit_record(self.parts,record(self.parts))
        for c in report["cells"]:
            self.assertEqual(c["categories"]["other_entity"],4 if c["split"]=="HOLDOUT" else 0)
            self.assertEqual(c["categories"]["outside_supplied"],0)
        self.assertEqual(sum(p["same_answer"] for p in pairs),0)
        self.assertEqual(sum(p["both_fixed_position"] for p in pairs),8)

    def test_16_outside_value_kept_not_forced_to_other(self):
        r=record(self.parts)
        for split in b.SPLITS:
            r["predictions"][split]["normal"]=[255]*8
            r["final"][split]={l:dict(m,answer_nll=5) for l,m in b.discrete_metrics(self.parts[split],r["predictions"][split]).items()}
        report,_,_=b.audit_record(self.parts,r)
        for c in report["cells"]:
            self.assertEqual(c["categories"],{"correct":0,"other_entity":0,"outside_supplied":4})
            self.assertEqual(sum(c["rule_matches"].values()),0)

    def test_17_matched_order_identity_and_counts(self):
        _,_,pairs=b.audit_record(self.parts,record(self.parts,"entity"))
        self.assertEqual(len(pairs),8);self.assertTrue(all(p["same_answer"] and p["both_correct"] for p in pairs))
        self.assertTrue(all(p["train_id"]!=p["holdout_id"] for p in pairs))

    def test_18_integrity_pass_does_not_depend_on_rule(self):
        for rule in b.RULES:
            reports,rows,pairs,s=b.analyze(self.parts,records(self.parts,rule))
            b.validate_result(payload(s))
            self.assertEqual((len(rows),len(pairs),s["saved_predictions"],s["rule_comparisons"]),(96,48,288,576))
            self.assertFalse(s["causal_claim"])

    def test_19_identity_or_count_fault_is_invalid(self):
        reports,_,_,_=b.analyze(self.parts,records(self.parts))
        with self.assertRaises(ValueError): b.summarize(list(reversed(reports)))
        reports[0]["saved_predictions"]=47
        with self.assertRaises(ValueError): b.summarize(reports)

    def test_20_actual_loader_with_parent_adapter(self):
        refs=records(self.parts);parent=SimpleNamespace(summarize=lambda records:{"models":len(records)})
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(parent,None,Audit)):
            root=Path(tmp)
            for name,value in (("split-dataset.json",self.parts),("measurements.json",refs),("summary.json",dict(validation_summary={"models":6}))):
                (root/name).write_bytes(b.blob(value))
            self.assertEqual(b.load_inputs(root/"summary.json"),(self.parts,refs))
            refs[0]["predictions"]["HOLDOUT"]["normal"][0]=255
            (root/"measurements.json").write_bytes(b.blob(refs))
            # This particular byte was already wrong: mutate a correct TRAIN byte too.
            refs[0]["predictions"]["TRAIN"]["normal"][0]=255
            (root/"measurements.json").write_bytes(b.blob(refs))
            with self.assertRaises(ValueError): b.load_inputs(root/"summary.json")

    def test_21_full_saved_data_run_and_postcheck(self):
        refs=records(self.parts);summary=b.analyze(self.parts,refs)[3];base=payload(summary)
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(None,None,Audit)), \
             patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
             patch.object(b,"load_inputs",return_value=(self.parts,refs)) as loader:
            out=Path(tmp)/"out";parent=Path(tmp)/"parent.json"
            with contextlib.redirect_stdout(io.StringIO()): p=b.run(c239_summary=parent,output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            self.assertEqual(b.verify_artifacts(out,parent,"synthetic-head")[0],p)
            with self.assertRaises(ValueError): b.verify_artifacts(out,parent,"wrong")
            (out/"row-audit.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError): b.verify_artifacts(out,parent,"synthetic-head")
            self.assertEqual({p.name for p in out.iterdir()},b.OUTPUTS|{"summary.json"})

    def test_22_no_model_work_and_actual_loader_dispatch(self):
        tree=ast.parse(inspect.getsource(b))
        forbidden={"fit","backward","step","zero_grad","new_model","load_state_dict","load_bundle","evaluate","tensors"}
        for n in ast.walk(tree):
            if isinstance(n,ast.Call):
                name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ""
                self.assertNotIn(name,forbidden)
        calls={n.func.id for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertTrue({"load_inputs","analyze","precheck"}<=calls)

    def test_23_runner_python_cli_parser_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c240.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c240.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks: compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5",launch)

    def test_24_semantic_own_count_and_protection(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"]);self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(b.manifest()["loaded_tests"]-b.manifest()["focused_tests"],1)
        p=payload(b.analyze(self.parts,records(self.parts))[3]);p["source_blobs"].pop(b.OWN[0])
        with self.assertRaises(ValueError): b.validate_result(p)


if __name__=="__main__": unittest.main(verbosity=2)
