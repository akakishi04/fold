"""Self-contained C186 wrapper/scoring tests; not a frozen-checkpoint integration run."""
from copy import deepcopy
from dataclasses import dataclass
import unittest
import numpy as np
from fold_lm.v05_benchmarks import gate_e_c186_nonadmission_reclassification as b


@dataclass(frozen=True)
class ToyDelivery:
    value: int = 0
    source_document: str = 'unchanged witness'
    fact_id: str = 'external:D'


class ToyFailure(ValueError):
    pass


class ToyFetch:
    def __init__(self, value=0):
        self.delivery = ToyDelivery(value)
        self.calls = []
    def __call__(self, request):
        self.calls.append(request)
        return self.delivery


def trace(scenario='FOUND_ZERO', initial_prediction=1, post_prediction=None):
    spec=b.scenario_spec(scenario)
    features=[7,4,1,1]+[0]*42+[1,2,1,1, 1,2,1,0, 1,2,1,0, 1,1,0,0]+[12,4,1,0,0,1,0,0,0,7]
    binding=dict(request_id='test|query',scope_id='test',fact_ids=['A','B','C','D'],
                 reference_ids=[['a'],['b'],['c'],[]])
    packet=dict(schema='fold-structured-task-input-v1',features=features,binding=binding)
    record=dict(initial=deepcopy(packet),phases=[],acquisition=None,receipts=[],pending=None,runtime_terminal=None)
    first=deepcopy(packet);first['features'][62]=11;first['features'][71]=8
    record['phases'].append(dict(phase=0,packet=first,prediction=initial_prediction))
    if initial_prediction==0:
        record.update(final=deepcopy(first),decision_charges=1,status='SUFFICIENT_CLASSIFICATION')
        return record
    last=deepcopy(first);last['features'][62:]=[7,3,1,0,0,1,0,0,spec['outcome'],12]
    receipt=None
    if spec['admitted']:
        last['features'][58:62]=[1,2,1,spec['bit']]
        last['binding']['reference_ids'][3]=['new-ref']
        receipt=dict(fact_id='D',request_id='test|query',scope_id='test',action='RETRIEVE',
                     value=spec['bit'],reference_id='new-ref')
        record['receipts']=[receipt]
    if post_prediction is None:post_prediction=int(not spec['admitted'])
    record['phases'].append(dict(phase=1,packet=deepcopy(last),prediction=post_prediction))
    record['acquisition']=dict(input_index=3,canonical_index=3,fact_id='D',
        action=dict(status='PENDING',internal_charged=1,acquisition_reserved=1),
        dispatch=dict(status=spec['status'],reason=spec['reason'],provider_calls=1,
            fact_publications=int(spec['admitted']),internal_charged=2,evidence=receipt))
    record.update(final=last,decision_charges=2,status='SUFFICIENT_CLASSIFICATION' if post_prediction==0 else 'UNRESOLVED')
    return record


def passing_records():
    rows=[]
    for s,a,l,c in b.expected_order():
        admitted=b.scenario_spec(c)['admitted'];r={k:0 for k in b.COUNTERS}
        r.update(seed=s,arm=a,layout=l,scenario=c,episodes=3712,labels={'needs':768,'sufficient':2944})
        if a==b.RULES[1]:
            r.update(initial_error=768,missed_attempt=768,failed=768,decision_charges=3712,internal_charged=3712)
        else:
            calls=3712 if a==b.RULES[0] else 768
            r.update(action_attempts=calls,provider_calls=calls,publications=calls*int(admitted),
                non_admitted_attempts=calls*int(not admitted),reservations=calls,
                decision_charges=3712+calls,internal_charged=3712+4*calls)
            if a==b.RULES[0]:r.update(initial_error=2944,unnecessary_attempt=2944,failed=2944,post_error=2944*int(not admitted))
        rows.append(r)
    return rows


class C186Tests(unittest.TestCase):
    def test_01_registered_specs(self):
        self.assertEqual(len(b.SCENARIOS),5)
        self.assertEqual([b.scenario_spec(s)['outcome'] for s in b.SCENARIOS],[0,0,4,6,0])
    def test_02_unknown_scenario_rejected(self):
        with self.assertRaises(ValueError):b.scenario_spec('drop-hard-cases')
    def test_03_found_preserves_delivery(self):
        f=ToyFetch(1);w=b.OutcomeProvider(f,'FOUND_ONE',ToyFailure)
        self.assertIs(w('r'),f.delivery);self.assertEqual(f.calls,['r'])
    def test_04_no_delivery_after_fetch(self):
        f=ToyFetch();w=b.OutcomeProvider(f,'NO_DELIVERY',ToyFailure)
        self.assertIsNone(w('r'));self.assertEqual(f.calls,['r']);self.assertEqual(w.calls,1)
    def test_05_zero_flipped(self):
        self.assertEqual(b.OutcomeProvider(ToyFetch(0),'WRONG_VALUE',ToyFailure)('r').value,1)
    def test_06_one_flipped(self):
        self.assertEqual(b.OutcomeProvider(ToyFetch(1),'WRONG_VALUE',ToyFailure)('r').value,0)
    def test_07_corrupt_only_value_not_witness(self):
        f=ToyFetch();d=b.OutcomeProvider(f,'WRONG_VALUE',ToyFailure)('r')
        self.assertEqual(d.source_document,f.delivery.source_document);self.assertEqual(d.fact_id,f.delivery.fact_id)
    def test_08_provider_failure_after_fetch(self):
        f=ToyFetch();w=b.OutcomeProvider(f,'PROVIDER_FAILURE',ToyFailure)
        with self.assertRaises(ToyFailure):w('r')
        self.assertEqual(f.calls,['r']);self.assertEqual(w.calls,1)
    def test_09_original_delivery_not_mutated(self):
        f=ToyFetch();b.OutcomeProvider(f,'WRONG_VALUE',ToyFailure)('r');self.assertEqual(f.delivery.value,0)
    def test_10_unexpected_fetch_error_propagates(self):
        def broken(_):raise OSError('synthetic read error')
        with self.assertRaises(OSError):b.OutcomeProvider(broken,'FOUND_ZERO',ToyFailure)('r')
    def test_11_invalid_pre_corruption_bit(self):
        with self.assertRaises(ValueError):b.OutcomeProvider(ToyFetch(True),'WRONG_VALUE',ToyFailure)('r')
    def test_12_zero_is_admitted(self):
        r=b.score_episode(trace(),1,'FOUND_ZERO');self.assertEqual(r['failed'],0);self.assertEqual(r['publications'],1)
    def test_13_one_is_admitted(self):
        self.assertEqual(b.score_episode(trace('FOUND_ONE'),1,'FOUND_ONE')['failed'],0)
    def test_14_no_delivery_still_needed(self):
        r=b.score_episode(trace('NO_DELIVERY'),1,'NO_DELIVERY');self.assertEqual(r['failed'],0);self.assertEqual(r['publications'],0)
    def test_15_corrupt_value_still_needed(self):
        self.assertEqual(b.score_episode(trace('WRONG_VALUE'),1,'WRONG_VALUE')['failed'],0)
    def test_16_failure_still_needed(self):
        self.assertEqual(b.score_episode(trace('PROVIDER_FAILURE'),1,'PROVIDER_FAILURE')['failed'],0)
    def test_17_false_sufficiency_retained(self):
        r=b.score_episode(trace('NO_DELIVERY',1,0),1,'NO_DELIVERY')
        self.assertEqual(r['failed'],1);self.assertEqual(r['false_sufficient_after_nonadmission'],1);self.assertEqual(r['contract_error'],0)
    def test_18_unnecessary_attempt_not_redeemed(self):
        r=b.score_episode(trace(),0,'FOUND_ZERO');self.assertEqual(r['failed'],1);self.assertEqual(r['unnecessary_attempt'],1)
    def test_19_never_query_misses(self):
        r=b.score_episode(trace(initial_prediction=0),1,'FOUND_ZERO');self.assertEqual(r['failed'],1);self.assertEqual(r['missed_attempt'],1)
    def test_20_no_query_preserves_unknown(self):
        r=trace(initial_prediction=0);before=deepcopy(r)
        self.assertEqual(b.score_episode(r,0,'FOUND_ZERO')['failed'],0);self.assertEqual(r,before)
    def test_21_fault_cannot_publish_zero(self):
        r=trace('NO_DELIVERY');r['final']['features'][58:62]=[1,2,1,0]
        self.assertEqual(b.score_episode(r,1,'NO_DELIVERY')['contract_error'],1)
    def test_22_live_budget_reset_rejected(self):
        r=trace();r['phases'][1]['packet']['features'][62:]=[12,4,1,0,0,1,0,0,0,7]
        self.assertEqual(b.score_episode(r,1,'FOUND_ZERO')['contract_error'],1)
    def test_23_pending_work_rejected(self):
        r=trace();r['pending']={'intent':'unconsumed'}
        self.assertEqual(b.score_episode(r,1,'FOUND_ZERO')['contract_error'],1)
    def test_24_classification_not_answer(self):
        r=trace();r['runtime_terminal']='ANSWERED';self.assertEqual(b.score_episode(r,1,'FOUND_ZERO')['contract_error'],1)
    def test_25_wrong_external_target_rejected(self):
        r=trace();r['acquisition']['fact_id']='different';self.assertEqual(b.score_episode(r,1,'FOUND_ZERO')['contract_error'],1)
    def test_26_fault_outcome_not_reset(self):
        r=trace('WRONG_VALUE');r['final']['features'][70]=0
        self.assertEqual(b.score_episode(r,1,'WRONG_VALUE')['contract_error'],1)
    def test_27_perfect_candidates_allow_control_errors(self):
        self.assertTrue(b.gate(passing_records()))
    def test_28_one_candidate_error_fails(self):
        r=passing_records();r[10]['failed']=1;self.assertFalse(b.gate(r))
    def test_29_order_and_coverage_strict(self):
        r=passing_records();self.assertFalse(b.gate(r[:-1]));r[0],r[1]=r[1],r[0];self.assertFalse(b.gate(r))
    def test_30_broken_control_fails(self):
        r=passing_records();r[-1]['provider_calls']=1;self.assertFalse(b.gate(r))
        r=passing_records();r[-11]['post_error']=0;self.assertFalse(b.gate(r))
    def test_31_replay_is_unmodified_and_finite(self):
        d=dict(predictions=np.zeros((2,2),np.int8),logit_present=np.ones((2,2),bool),
               policy_inputs=np.zeros((2,2,72),np.int32),logits=np.zeros((2,2,2),np.float32))
        self.assertEqual(b.replay_arrays(d,deepcopy(d)),0)
        e=deepcopy(d);e['logits'][0,0,0]=5e-7;self.assertLess(b.replay_arrays(e,d),b.ATOL)
        e['logits'][0,0,0]=1e-3
        with self.assertRaises(ValueError):b.replay_arrays(e,d)
        e['logits'][0,0,0]=np.nan
        with self.assertRaises(ValueError):b.replay_arrays(e,d)
        e=deepcopy(d);e['predictions'][0,0]=1
        with self.assertRaises(ValueError):b.replay_arrays(e,d)
    def test_32_frozen_manifest(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(len(b.expected_order()),80);self.assertEqual(8*2*5*3712,296960)
        self.assertEqual(len(b.OUTPUTS),13);self.assertEqual(len(b.PARENTS),11)
        self.assertEqual(len(b.SOURCES),8)


if __name__=='__main__':unittest.main()
