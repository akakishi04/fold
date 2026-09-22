import hashlib
import inspect
import itertools
from pathlib import Path
import re
import tempfile
import unittest

import torch

from fold_lm.v05_benchmarks import model_c235_frozen_binding_diagnostic as b


def parent_records():
    rows=[]
    metrics={lang:dict(rows=96,accuracy=.25,answer_nll=1.0,
        evidence_blind_accuracy=.25,query_blind_accuracy=.25,
        evidence_drop=0.0,query_drop=0.0,fact_pair_accuracy=0.0,
        query_pair_accuracy=0.0) for lang in ("en","ja")}
    for seed,family in b.identities():
        rows.append(dict(seed=seed,family=family,final_eval={k:dict(v) for k,v in metrics.items()},
            final_sha256="a"*64,checkpoint_roundtrip=True,prediction_replayed=True,
            weights_changed=True,reload_max_error=0.0,
            fit=dict(steps=400,answer_presentations=12800),
            predictions={mode:[48]*192 for mode in b.VIEWS}))
    return rows


def diagnostic_records():
    rows=[]
    for seed,family in b.identities():
        rows.append(dict(seed=seed,family=family,parent_replay_error=0.0,
            before_sha256="a"*64,after_sha256="a"*64,forward_calls=6,
            evaluated_rows=1728,
            diagnosis={"en":"TRAIN_ACCURACY_BELOW_90","ja":"TRAIN_ACCURACY_BELOW_90"}))
    return rows


def payload(summary):
    sources={f"parent-{i}":"fixture" for i in range(250)}
    sources.update({name:"fixture" for name in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=sources,input_sha256={f"input-{i}":"fixture" for i in range(370)},
        artifacts=[dict(file=name) for name in b.OUTPUTS],validation_summary=summary,
        status="PASS",gate_f_candidate=False,network_calls=0)


def exact_logits(rows, prediction=None):
    logits=torch.full((len(rows),256),-10.0,dtype=torch.float64)
    preds=[]
    for i,row in enumerate(rows):
        value=row["target"] if prediction is None else prediction
        logits[i,value]=10.0;preds.append(value)
    return preds,logits


class C235Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        p=b.parent_module();data=p.dataset()
        cls.train,cls.ev=p.validate_dataset(data)

    def test_01_manifest_hash_and_scope(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        m=b.manifest()
        self.assertEqual((m["new_training_steps"],m["checkpoint_writes"]),(0,0))
        self.assertFalse(m["general_language_claim"]);self.assertFalse(m["gate_f_candidate"])

    def test_02_fixed_identity_order_and_views(self):
        self.assertEqual(b.identities(),list(itertools.product(b.SEEDS,b.FAMILIES)))
        self.assertEqual(b.VIEWS,("normal","evidence_blind","query_blind"))

    def test_03_parent_dataset_split_is_reused(self):
        self.assertEqual((len(self.train),len(self.ev)),(384,192))
        self.assertTrue(all(r["split"]=="TRAIN" for r in self.train))
        self.assertTrue(all(r["split"]=="EVAL" for r in self.ev))

    def test_04_classify_train_failure(self):
        self.assertEqual(b.classify(.899,1.0),"TRAIN_ACCURACY_BELOW_90")

    def test_05_classify_generalization_gap(self):
        self.assertEqual(b.classify(.90,.899),"TRAIN_AT_LEAST_90_EVAL_BELOW_90")

    def test_06_classify_both_high(self):
        self.assertEqual(b.classify(.90,.90),"BOTH_ACCURACIES_AT_LEAST_90")

    def test_07_classify_rejects_invalid_rate(self):
        for values in ((-1.,.5),(.5,1.1),(float("nan"),.5)):
            with self.assertRaises(ValueError): b.classify(*values)

    def test_08_analyze_perfect_answers(self):
        pred,logits=exact_logits(self.ev);out=b.analyze(self.ev,pred,logits)
        for item in out.values():
            self.assertEqual((item["rows"],item["supplied_value_rate"]),(96,1.0))
            self.assertEqual((item["query_pairs"],item["query_same_answer_pairs"],
                              item["query_both_correct_pairs"]),(48,0,48))

    def test_09_analyze_constant_answer_exposes_query_invariance(self):
        pred,logits=exact_logits(self.ev,48);out=b.analyze(self.ev,pred,logits)
        for item in out.values():
            self.assertEqual(item["query_same_answer_pairs"],48)
            self.assertEqual(item["query_both_correct_pairs"],0)

    def test_10_analyze_non_supplied_byte(self):
        pred,logits=exact_logits(self.ev,255);out=b.analyze(self.ev,pred,logits)
        for item in out.values():
            self.assertEqual(item["supplied_value_answers"],0)
            self.assertEqual(item["query_same_answer_rate"],1.0)

    def test_11_analyze_rejects_prediction_logit_disagreement(self):
        pred,logits=exact_logits(self.ev)
        pred[0]=255
        with self.assertRaises(ValueError): b.analyze(self.ev,pred,logits)

    def test_12_parent_record_contract_accepts_complete_rows(self):
        self.assertEqual(len(b.validate_parent_records(parent_records())),6)

    def test_13_parent_record_contract_rejects_bad_replay(self):
        rows=parent_records();rows[0]["prediction_replayed"]=False
        with self.assertRaises(ValueError): b.validate_parent_records(rows)

    def test_14_eval_replay_exact_match(self):
        saved=parent_records()[0]
        self.assertEqual(b.replay_error(saved["final_eval"],saved["predictions"],saved),0.0)

    def test_15_eval_replay_rejects_prediction_change(self):
        saved=parent_records()[0];pred={k:list(v) for k,v in saved["predictions"].items()}
        pred["normal"][0]=49
        with self.assertRaises(ValueError): b.replay_error(saved["final_eval"],pred,saved)

    def test_16_eval_replay_rejects_metric_change(self):
        saved=parent_records()[0];metrics={k:dict(v) for k,v in saved["final_eval"].items()}
        metrics["en"]["accuracy"]+=.01
        with self.assertRaises(ValueError): b.replay_error(metrics,saved["predictions"],saved)

    def test_17_checkpoint_bundle_schema_and_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"models.pt"
            torch.save(dict(schema="fold-c234-binding-v1",
                identities=[list(x) for x in b.identities()],states=[{} for _ in range(6)]),path)
            self.assertEqual(len(b.load_bundle(path)),6)

    def test_18_integrity_gate_is_independent_of_bad_diagnosis(self):
        s=b.summarize(diagnostic_records())
        self.assertTrue(b.gate(s));self.assertFalse(s["capability_pass_claim"])
        self.assertEqual(s["diagnosis_cells"],12)

    def test_19_integrity_gate_rejects_mutation_or_missing_work(self):
        rows=diagnostic_records();rows[0]["after_sha256"]="b"*64
        self.assertFalse(b.gate(b.summarize(rows)))
        rows=diagnostic_records();rows[0]["forward_calls"]=5
        self.assertFalse(b.gate(b.summarize(rows)))

    def test_20_result_contract_is_diagnostic_pass_only(self):
        s=b.summarize(diagnostic_records());b.validate_result(payload(s))
        bad=payload(s);bad["status"]="FAIL"
        with self.assertRaises(ValueError): b.validate_result(bad)

    def test_21_parent_negative_contract_is_fixed(self):
        source=inspect.getsource(b.precheck)
        self.assertIn('p["status"]=="FAIL"',source)
        self.assertIn('s["full_binding_gate"] is False',source)
        self.assertIn('s["gru_binding_gate"] is False',source)
        self.assertIn('PARENT_ARTIFACTS',source)

    def test_22_run_is_frozen_no_training_or_checkpoint_write(self):
        source=inspect.getsource(b.run)
        self.assertNotIn(".fit(",source);self.assertNotIn("optimizer",source)
        self.assertNotIn("torch.save",source)
        self.assertIn("requires_grad_(False)",source)
        self.assertIn('replay_error(scores["EVAL"]',source)

    def test_23_runner_launcher_and_workload_contract(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c235.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c235.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2809",run)
        self.assertIn("own authoring tests first: 24",run)
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks: compile(block,"embedded","exec")
        self.assertIn("c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        m=b.manifest();self.assertEqual((m["model_forward_calls"],m["evaluated_rows_including_masks"]),(36,10368))

    def test_24_actual_historical_suite_counts(self):
        root=Path(__file__).resolve().parents[1];names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(120,2810))
        self.assertEqual(b.regression_suite(root).countTestCases(),2809)


if __name__=="__main__":
    unittest.main(verbosity=2)
