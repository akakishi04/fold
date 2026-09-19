import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from fold_lm.v05 import structured_task_input as task
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c192_post3_shadow_necessity as c192

def good_records():
    out=[]
    for b,h in c192.expected_order():
        out.append(dict(base_seed=b,head_seed=h,episodes=9536,
            parent_third_acquisitions=928,parent_actual_reads=14352,actual_reads=14352,
            parent_necessity_prediction_errors=0,parent_target_prediction_errors=0,
            parent_necessity_max_abs_logit_difference=0.0,
            parent_target_max_abs_logit_difference=0.0,
            failed=0,parent_replay_error=0,shadow_error=0,shadow_nonfinite=0,
            logical_teacher_error=0,runtime_mutation=0,shadow_rows=928,
            runtime_reads_after_shadow=0))
    return out

def final_record(eligible=True):
    x=[0]*72
    for j in range(4):
        x[48+4*j]=1
    x[62]=0;x[63]=1;x[71]=19
    return dict(status="BUDGET_EXHAUSTED_AFTER_THIRD" if eligible else "SUFFICIENT_CLASSIFICATION",
                final=dict(schema=task.SCHEMA,features=x,
                    binding=dict(request_id="S|q",scope_id="S",
                        fact_ids=["A","B","C","D"],reference_ids=[["a"],["b"],["c"],["d"]])))

class C192Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c192.digest(c192.manifest()),c192.MANIFEST_SHA)

    def test_02_manifest_workload(self):
        m=c192.manifest()
        self.assertEqual((m["episodes"],m["blocks"],m["shadow_rows"]),(85824,9,8352))

    def test_03_outputs_exact(self):
        self.assertEqual(len(c192.OUTPUTS),5)

    def test_04_expected_order(self):
        self.assertEqual(c192.expected_order(),
            [(b,h) for b in c192.BASE_SEEDS for h in c192.HEAD_SEEDS])

    def test_05_gate_accepts(self):
        self.assertTrue(c192.gate(good_records()))

    def test_06_gate_requires_nine(self):
        self.assertFalse(c192.gate(good_records()[:-1]))

    def test_07_gate_rejects_shadow_error(self):
        r=good_records();r[0]["shadow_error"]=r[0]["failed"]=1
        self.assertFalse(c192.gate(r))

    def test_08_gate_rejects_nonfinite(self):
        r=good_records();r[0]["shadow_nonfinite"]=r[0]["failed"]=1
        self.assertFalse(c192.gate(r))

    def test_09_gate_rejects_logical_error(self):
        r=good_records();r[0]["logical_teacher_error"]=r[0]["failed"]=1
        self.assertFalse(c192.gate(r))

    def test_10_gate_rejects_mutation(self):
        r=good_records();r[0]["runtime_mutation"]=r[0]["failed"]=1
        self.assertFalse(c192.gate(r))

    def test_11_gate_requires_928_shadow_rows(self):
        r=good_records();r[0]["shadow_rows"]=927
        self.assertFalse(c192.gate(r))

    def test_12_gate_rejects_extra_read(self):
        r=good_records();r[0]["actual_reads"]+=1
        self.assertFalse(c192.gate(r))

    def test_13_gate_rejects_parent_prediction_error(self):
        r=good_records();r[0]["parent_target_prediction_errors"]=1
        self.assertFalse(c192.gate(r))

    def test_14_gate_rejects_parent_logit_drift(self):
        r=good_records();r[0]["parent_necessity_max_abs_logit_difference"]=c192.ATOL*2
        self.assertFalse(c192.gate(r))

    def test_15_packet_from_dict(self):
        d=final_record()["final"]
        p=c192.packet_from_dict(d)
        self.assertEqual(p.schema,task.SCHEMA)
        self.assertEqual(p.binding.fact_ids,("A","B","C","D"))
        self.assertEqual(p.binding.reference_ids,(("a",),("b",),("c",),("d",)))

    def _write_parent(self,p):
        np.savez_compressed(p,
            necessity_predictions=np.zeros((9,9536,3),dtype=np.int8),
            necessity_logits=np.zeros((9,9536,3,2),dtype=np.float32),
            target_predictions=np.zeros((9,9536,3),dtype=np.int8),
            target_logits=np.zeros((9,9536,3,4),dtype=np.float32),
            row_indices=np.zeros(9536,dtype=np.int32),
            local_rows=np.zeros(9536,dtype=np.int32),
            world_codes=np.zeros(9536,dtype=np.int8))

    def test_16_parent_loader_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._write_parent(p)
            z=c192.load_parent_predictions(p)
            self.assertEqual(z["necessity_logits"].shape,(9,9536,3,2))

    def test_17_parent_loader_rejects_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";np.savez_compressed(p,x=np.zeros(1))
            with self.assertRaises(ValueError):c192.load_parent_predictions(p)
        import inspect
        source=inspect.getsource(c192.run)
        self.assertIn('saved=load_parent_predictions(',source)
        self.assertNotIn('saved=c191.load_parent_predictions(',source)

    def test_18_assess_shadow_pass(self):
        with mock.patch.object(c190,"logical_label",return_value=0):
            s=c192.assess_shadow(final_record(),0,np.asarray([2.,1.]),0,[])
        self.assertEqual(s["failed"],0);self.assertEqual(s["shadow_rows"],1)

    def test_19_assess_shadow_wrong_prediction(self):
        with mock.patch.object(c190,"logical_label",return_value=0):
            s=c192.assess_shadow(final_record(),1,np.asarray([1.,2.]),0,[])
        self.assertEqual((s["shadow_error"],s["failed"]),(1,1))

    def test_20_assess_shadow_nonfinite(self):
        with mock.patch.object(c190,"logical_label",return_value=0):
            s=c192.assess_shadow(final_record(),0,np.asarray([np.nan,1.]),0,[])
        self.assertEqual((s["shadow_nonfinite"],s["failed"]),(1,1))

    def test_21_assess_shadow_logical_teacher_error(self):
        with mock.patch.object(c190,"logical_label",return_value=1):
            s=c192.assess_shadow(final_record(),0,np.asarray([2.,1.]),0,[])
        self.assertEqual((s["logical_teacher_error"],s["failed"]),(1,1))

    def test_22_noneligible_not_scored(self):
        s=c192.assess_shadow(final_record(False),-1,np.asarray([0.,0.]),0,[])
        self.assertEqual((s["shadow_rows"],s["failed"]),(0,0))

    def test_23_shadow_is_declared_non_authoritative(self):
        self.assertIn("non-authoritative",c192.manifest()["limits"])

    def test_24_budget_is_not_changed(self):
        m=c192.manifest()
        self.assertIn("internal_remaining0",m["shadow_input"])
        self.assertIn("no charge_decision",m["shadow_policy"])

if __name__=="__main__":
    unittest.main(verbosity=2)
