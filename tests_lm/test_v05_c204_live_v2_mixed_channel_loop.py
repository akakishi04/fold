import inspect
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as c202
from fold_lm.v05_benchmarks import gate_e_c204_live_v2_mixed_channel_loop as c204


def base_view():
    resources=v1.Resources(
        internal_remaining=13,acquisitions_remaining=4,
        available=(True,False,False),permitted=(True,False,False),
        last_outcome="NONE",internal_step=7)
    nodes=(
        v1.Node("FACT",0),v1.Node("FACT",1),v1.Node("AND",left=0,right=1),
        v1.Node("FACT",2),v1.Node("FACT",3),v1.Node("OR",left=3,right=4),
        v1.Node("OR",left=2,right=5),
    )
    facts=tuple(v1.Fact(c204.c185.FACT_IDS[i]) for i in range(4))
    return v1.TaskView("C204|test|query","C204|test",nodes,facts,resources,1,1)


def reference_one():
    n=np.full((1,4),-1,dtype=np.int8)
    nz=np.zeros((1,4,2),dtype=np.float32)
    t=np.full((1,3),-1,dtype=np.int8)
    tz=np.full((1,3,4),-np.inf,dtype=np.float32)
    n[0,0]=1;n[0,1]=0
    nz[0,0]=[0.0,1.0];nz[0,1]=[1.0,0.0]
    # C199 semantics: terminal SUFFICIENT phase can still carry target-head output.
    t[0,0]=0;t[0,1]=1
    tz[0,0]=[1.0,0.0,0.0,0.0]
    tz[0,1]=[-np.inf,1.0,0.0,0.0]
    return dict(
        necessity_predictions=n,necessity_logits=nz,
        target_predictions=t,target_logits=tz,
    )


def expected_one():
    return dict(
        episodes=1,decisions=2,acquisitions=1,final_sufficient=1,
        channel_counts={"RETRIEVE":1,"OBSERVE":0,"ASK_USER":0},
        channel_switches=0,
    )


def combined_side_effect(*args,**kwargs):
    raw=args[2]
    # First call sees four unknown facts; second sees fact0 observed.
    fact0_present=int(raw[0,48].item())
    if fact0_present==0:
        return (
            np.array([1],dtype=np.int8),
            np.array([0],dtype=np.int8),
            np.array([[0.0,1.0]],dtype=np.float32),
            np.array([[1.0,0.0,0.0,0.0]],dtype=np.float32),
            dict(rows=1,forward_calls=1,cell_calls=7,wall_clock_seconds=0.0),
        )
    return (
        np.array([0],dtype=np.int8),
        np.array([1],dtype=np.int8),
        np.array([[1.0,0.0]],dtype=np.float32),
        np.array([[-np.inf,1.0,0.0,0.0]],dtype=np.float32),
        dict(rows=1,forward_calls=1,cell_calls=7,wall_clock_seconds=0.0),
    )


def good_records():
    rows=[]
    for b in c204.BASE_SEEDS:
        for h in c204.HEAD_SEEDS:
            rows.append(dict(
                base_seed=b,head_seed=h,episodes=9536,decisions=1,acquisitions=1,
                final_sufficient=1,
                channel_counts={"RETRIEVE":1,"OBSERVE":0,"ASK_USER":0},
                channel_switches=0,v2_packets=1,inference_rows=1,
                inference_forward_calls=1,inference_cell_calls=7,
                necessity_max_abs_logit_difference=0.0,
                target_max_abs_logit_difference=0.0,
                failed=0,projection_error=0,v2_prefix_error=0,
                necessity_prediction_error=0,target_prediction_error=0,
            ))
    return rows


class C204Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c204.digest(c204.manifest()),c204.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c204.manifest()
        self.assertEqual((m["blocks"],m["episodes_per_block"]),(9,9536))
        self.assertEqual(m["channel_layout"],c204.c203.CHANNEL_LAYOUT)

    def test_03_manifest_has_zero_training(self):
        m=c204.manifest()
        self.assertEqual((m["training_steps"],m["fresh_seeds"],m["network_calls"]),(0,0,0))

    def test_04_model_summary_hashes_fixed(self):
        self.assertEqual(c204.C181_SUMMARY_SHA,"bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98")
        self.assertEqual(c204.C188_SUMMARY_SHA,"2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153")

    def test_05_encode_live_v2_prefix_exact(self):
        owner=life.AcquisitionOwner(action.RuntimeState(base_view()),{},max_dispatches=3)
        raw,packets,errors=c204.encode_live_v2([owner],[0])
        self.assertEqual((tuple(raw[0].tolist()),errors),(v1.encode(owner.state.view).features,0))
        self.assertEqual(len(packets[0].features),84)

    def test_06_encode_live_v2_tail_has_fixed_layout(self):
        owner=life.AcquisitionOwner(action.RuntimeState(base_view()),{},max_dispatches=3)
        _,packets,_=c204.encode_live_v2([owner],[0])
        view=v2.decode(packets[0])
        self.assertEqual(tuple(v2.declared_channels(view,i) for i in range(4)),
                         (("RETRIEVE",),("OBSERVE",),("ASK_USER",),("RETRIEVE",)))

    def test_07_replay_metrics_accept_exact(self):
        r=reference_one()
        q=c204.replay_metrics(r,r)
        self.assertEqual(q["necessity_prediction_errors"],0)
        self.assertEqual(q["target_prediction_errors"],0)
        self.assertEqual(q["necessity_max_abs_logit_difference"],0.0)
        self.assertEqual(q["target_max_abs_logit_difference"],0.0)

    def test_08_replay_metrics_reject_target_finite_mask_drift(self):
        r=reference_one(); live={k:v.copy() for k,v in r.items()}
        live["target_logits"][0,2,0]=0.0
        with self.assertRaises(ValueError):
            c204.replay_metrics(live,r)

    def test_09_replay_metrics_counts_prediction_error(self):
        r=reference_one(); live={k:v.copy() for k,v in r.items()}
        live["necessity_predictions"][0,0]=0
        q=c204.replay_metrics(live,r)
        self.assertEqual(q["necessity_prediction_errors"],1)

    def _integration(self):
        pm,em=c202.providers()
        ref=reference_one()
        with mock.patch.object(c189,"combined_predict",side_effect=combined_side_effect), \
             mock.patch.object(c189,"necessity_predict",side_effect=AssertionError("unexpected necessity-only call")):
            rec,replay=c204.run_live_block(
                [base_view()],np.array([3],dtype=np.int8),object(),object(),
                ref,pm,em,expected_one())
        return pm,rec,replay

    def test_10_live_integration_passes(self):
        _,rec,replay=self._integration()
        self.assertEqual((rec["failed"],rec["projection_error"]),(0,0))
        self.assertEqual(replay["necessity_prediction_errors"],0)
        self.assertEqual(replay["target_prediction_errors"],0)

    def test_11_live_integration_two_v2_packets(self):
        _,rec,_=self._integration()
        self.assertEqual((rec["v2_packets"],rec["decisions"]),(2,2))

    def test_12_live_integration_one_acquisition(self):
        _,rec,_=self._integration()
        self.assertEqual((rec["acquisitions"],rec["final_sufficient"]),(1,1))

    def test_13_live_integration_retrieve_only_for_fact0(self):
        pm,_,_=self._integration()
        self.assertEqual(tuple(pm[3][c].calls for c in v2.CHANNELS),(1,0,0))

    def test_14_live_integration_no_prefix_error(self):
        _,rec,_=self._integration()
        self.assertEqual(rec["v2_prefix_error"],0)

    def test_15_live_integration_exact_logit_replay(self):
        _,rec,_=self._integration()
        self.assertEqual(rec["necessity_max_abs_logit_difference"],0.0)
        self.assertEqual(rec["target_max_abs_logit_difference"],0.0)

    def test_16_live_integration_inference_meter(self):
        _,rec,_=self._integration()
        self.assertEqual((rec["inference_rows"],rec["inference_forward_calls"],rec["inference_cell_calls"]),(2,2,14))

    def test_17_gate_accepts_exact_global_profile(self):
        rows=good_records()
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
            channel_switches=32564,v2_packets=214948,inference_rows=214948,
            inference_forward_calls=100,inference_cell_calls=700,failures=0,
            projection_errors=0,v2_prefix_errors=0,necessity_prediction_errors=0,
            target_prediction_errors=0,max_necessity_logit_delta=0.0,max_target_logit_delta=0.0)
        self.assertTrue(c204.gate(rows,totals))

    def test_18_gate_rejects_prefix_error(self):
        rows=good_records(); rows[0]["v2_prefix_error"]=1
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
            channel_switches=32564,v2_packets=214948,inference_rows=214948,
            inference_forward_calls=100,inference_cell_calls=700,failures=0,
            projection_errors=0,v2_prefix_errors=1,necessity_prediction_errors=0,
            target_prediction_errors=0,max_necessity_logit_delta=0.0,max_target_logit_delta=0.0)
        self.assertFalse(c204.gate(rows,totals))

    def test_19_gate_rejects_necessity_flip(self):
        rows=good_records(); rows[0]["necessity_prediction_error"]=1
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
            channel_switches=32564,v2_packets=214948,inference_rows=214948,
            inference_forward_calls=100,inference_cell_calls=700,failures=1,
            projection_errors=0,v2_prefix_errors=0,necessity_prediction_errors=1,
            target_prediction_errors=0,max_necessity_logit_delta=0.0,max_target_logit_delta=0.0)
        self.assertFalse(c204.gate(rows,totals))

    def test_20_gate_rejects_target_flip(self):
        rows=good_records(); rows[0]["target_prediction_error"]=1
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
            channel_switches=32564,v2_packets=214948,inference_rows=214948,
            inference_forward_calls=100,inference_cell_calls=700,failures=1,
            projection_errors=0,v2_prefix_errors=0,necessity_prediction_errors=0,
            target_prediction_errors=1,max_necessity_logit_delta=0.0,max_target_logit_delta=0.0)
        self.assertFalse(c204.gate(rows,totals))

    def test_21_gate_rejects_logit_delta(self):
        rows=good_records(); rows[0]["necessity_max_abs_logit_difference"]=1e-3
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
            channel_switches=32564,v2_packets=214948,inference_rows=214948,
            inference_forward_calls=100,inference_cell_calls=700,failures=0,
            projection_errors=0,v2_prefix_errors=0,necessity_prediction_errors=0,
            target_prediction_errors=0,max_necessity_logit_delta=1e-3,max_target_logit_delta=0.0)
        self.assertFalse(c204.gate(rows,totals))

    def test_22_gate_rejects_channel_drift(self):
        rows=good_records()
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":88919,"OBSERVE":21251,"ASK_USER":18954},
            channel_switches=32564,v2_packets=214948,inference_rows=214948,
            inference_forward_calls=100,inference_cell_calls=700,failures=0,
            projection_errors=0,v2_prefix_errors=0,necessity_prediction_errors=0,
            target_prediction_errors=0,max_necessity_logit_delta=0.0,max_target_logit_delta=0.0)
        self.assertFalse(c204.gate(rows,totals))

    def test_23_source_builds_v2_before_live_predict(self):
        source=inspect.getsource(c204.run_live_block)
        self.assertLess(source.index("encode_live_v2"),source.index("c189.combined_predict"))

    def test_24_source_feeds_prefix_not_v2_tail(self):
        source=inspect.getsource(c204.encode_live_v2)
        self.assertIn("packet.features[:v1.FEATURE_WIDTH]",source)
        self.assertNotIn("features[72:]",source)

    def test_25_source_does_not_substitute_saved_decision(self):
        source=inspect.getsource(c204.run_live_block)
        self.assertIn("p,t,z,tz,m = c189.combined_predict",source)
        self.assertIn('reference["necessity_predictions"]',source)
        self.assertNotIn("p = reference",source)
        self.assertNotIn("t = reference",source)

    def test_26_source_restores_authority_after_dispatch(self):
        source=inspect.getsource(c204.run_live_block)
        self.assertLess(source.index("owner.dispatch"),source.index("c203.set_authority(owner,all_channels=False)"))

    def test_27_model_loader_uses_accepted_fingerprints(self):
        source=inspect.getsource(c204.restore_models)
        self.assertIn('fits[b]["final_sha256"]',source)
        self.assertIn("selector_sha[b,h]",source)

    def test_28_precheck_ties_models_to_c199(self):
        source=inspect.getsource(c204.precheck)
        self.assertIn("accepted_values",source)
        self.assertIn("Model checkpoint not tied to accepted C199",source)

    def test_29_regression_adds_one_module(self):
        source=inspect.getsource(c204.regression_modules)
        self.assertIn("== 88",source)
        self.assertIn("test_v05_c204_live_v2_mixed_channel_loop",source)

    def test_30_scope_no_training(self):
        source=inspect.getsource(c204.manifest)
        self.assertIn("training_steps=0",source)
        self.assertIn("production_runtime_modified=False",source)


    def test_31_active_dispatcher_guards_before_launcher(self):
        source=(Path(__file__).resolve().parents[1]/"tools"/"invoke_active.ps1").read_text(encoding="utf-8")
        self.assertIn("invocation_skipped = $Reason",source)
        self.assertIn("execution_log_publish_attempted = False",source)
        self.assertNotIn("publish_experiment_log.ps1",source)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",source)
        self.assertIn('ACTIVE_LAUNCHER_PARSE_ERROR',source)
        self.assertLess(source.index("if ($currentHead -ne $ExpectedHead)"),source.index("& $launcher -ExpectedHead"))
        self.assertLess(source.index("ACTIVE_EXPERIMENT_UNRESOLVED"),source.index("& $launcher -ExpectedHead"))
        self.assertLess(source.index("[System.Management.Automation.Language.Parser]::ParseFile"),source.index("& $launcher -ExpectedHead"))

    def test_32_c204_launcher_stale_guard_precedes_logging_and_publish(self):
        source=(Path(__file__).resolve().parents[1]/"tools"/"invoke_c204.ps1").read_text(encoding="utf-8")
        guard=source.index("if ($headNow -ne $ExpectedHead)")
        active=source.index("$activeMatch = [regex]::Match")
        logging=source.index("$failure = $null")
        publish=source.index("publish_experiment_log.ps1")
        self.assertLess(guard,logging)
        self.assertLess(active,logging)
        self.assertLess(logging,publish)
        self.assertIn("execution_log_publish_attempted = False",source)


    def test_33_active_dispatcher_resolves_current_formal_state(self):
        import re
        root=Path(__file__).resolve().parents[1]
        handoff=(root/"docs"/"experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        matches=re.findall(
            r"(?m)^\*\*[^*\r\n]*C(?P<id>\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)[^*\r\n]*\*\*$",
            handoff,
        )
        self.assertEqual(matches,["204"])
        source=(root/"tools"/"invoke_active.ps1").read_text(encoding="utf-8")
        self.assertIn("$activePattern = '(?m)^\\*\\*[^*\\r\\n]*C(?<id>\\d{3}) ACTIVE /",source)


if __name__=="__main__":
    unittest.main(verbosity=2)
