"""C187 contract tests with synthetic packets; not official checkpoint evaluation."""
from copy import deepcopy
from dataclasses import dataclass, replace
import unittest
import numpy as np
from fold_lm.v05_benchmarks import gate_e_c187_restricted_acquisition as b


@dataclass(frozen=True)
class ToyResources:
    internal_remaining: int = 12
    acquisitions_remaining: int = 4
    available: tuple = (True,False,False)
    permitted: tuple = (True,False,False)
    last_outcome: str = 'NONE'
    internal_step: int = 7


@dataclass(frozen=True)
class ToyView:
    resources: ToyResources = ToyResources()
    facts: tuple = ('known1','known0','known0','unknown')
    nodes: tuple = ('opaque expression',)
    request_id: str = 'test|q'
    scope_id: str = 'test'
    evidence_time: int = 1
    revision: int = 1


def trace(scenario='ALLOWED_ZERO', p0=1, p1=None, missing_index=3):
    spec=b.scenario_spec(scenario)
    facts=[1,2,1,1, 1,2,1,0, 1,2,1,0, 1,2,1,0]
    facts[4*missing_index:4*missing_index+4]=[1,1,0,0]
    refs=[['r0'],['r1'],['r2'],['r3']];refs[missing_index]=[]
    packet=dict(schema='fold-structured-task-input-v1',features=[7,4,1,1]+[0]*42+facts+b.resource_fields(scenario,'initial'),
                binding=dict(request_id='test|q',scope_id='test',fact_ids=['A','B','C','D'],reference_ids=refs))
    record=dict(initial=deepcopy(packet),phases=[],acquisition=None,receipts=[],pending=None,runtime_terminal=None)
    first=deepcopy(packet);first['features'][62:]=b.resource_fields(scenario,'first')
    record['phases'].append(dict(phase=0,packet=first,prediction=p0))
    if p0==0:
        record.update(final=deepcopy(first),decision_charges=1,status='SUFFICIENT_CLASSIFICATION')
        return record
    final=deepcopy(first);final['features'][62:]=b.resource_fields(scenario,'post')
    fid=packet['binding']['fact_ids'][missing_index]
    delivery=None
    if spec['allowed']:
        start=46+4*missing_index;final['features'][start:start+4]=[1,2,1,spec['bit']]
        final['binding']['reference_ids'][missing_index]=['new-ref']
        receipt=dict(fact_id=fid,request_id='test|q',scope_id='test',action='RETRIEVE',value=spec['bit'],reference_id='new-ref')
        record['receipts']=[receipt]
        delivery=dict(status='PUBLISHED',reason='OBSERVATION_ADMITTED',provider_calls=1,
                      fact_publications=1,internal_charged=2,evidence=receipt)
    if p1 is None:p1=int(not spec['allowed'])
    record['phases'].append(dict(phase=1,packet=deepcopy(final),prediction=p1))
    record['acquisition']=dict(fact_id=fid,input_index=missing_index,canonical_index=missing_index,
        action=dict(status='PENDING' if spec['allowed'] else 'DENIED',reason=spec['reason'],
                    internal_charged=1,acquisition_reserved=int(spec['allowed'])),dispatch=delivery)
    record.update(final=final,decision_charges=2,status='SUFFICIENT_CLASSIFICATION' if p1==0 else 'UNRESOLVED')
    return record


def passing_records():
    records=[]
    for s,a,l,c in b.expected_order():
        allowed=b.scenario_spec(c)['allowed'];calls=0 if a==b.RULES[1] else 3712 if a==b.RULES[0] else 768
        r={k:0 for k in b.COUNTERS}
        r.update(seed=s,arm=a,layout=l,scenario=c,episodes=3712,labels={'needs':768,'sufficient':2944},
            action_attempts=calls,denied_attempts=calls*int(not allowed),provider_calls=calls*int(allowed),
            publications=calls*int(allowed),reservations=calls*int(allowed),decision_charges=3712+calls,
            internal_charged=3712+calls*(4 if allowed else 2))
        if a==b.RULES[0]:r.update(initial_error=2944,unnecessary_proposal=2944,failed=2944,post_error=2944*int(not allowed))
        if a==b.RULES[1]:r.update(initial_error=768,missed_proposal=768,failed=768)
        records.append(r)
    return records


class C187Tests(unittest.TestCase):
    def test_01_fixed_scenarios(self):
        self.assertEqual([b.scenario_spec(s)['field'] for s in b.SCENARIOS],[None,None,67,64,63])
        self.assertEqual([b.scenario_spec(s)['outcome'] for s in b.SCENARIOS],[0,0,2,0,3])
    def test_02_unknown_scenario_rejected(self):
        with self.assertRaises(ValueError):b.scenario_spec('change-unregistered-field')
    def test_03_allowed_view_unchanged(self):
        v=ToyView();self.assertEqual(b.restrict_views([v],'ALLOWED_ZERO'),[v]);self.assertEqual(b.restrict_views([v],'ALLOWED_ONE'),[v])
    def test_04_permission_only(self):
        v=ToyView();w=b.restrict_views([v],'PERMISSION_DENIED')[0]
        self.assertEqual(w,replace(v,resources=replace(v.resources,permitted=(False,False,False))))
    def test_05_availability_only(self):
        v=ToyView();w=b.restrict_views([v],'PROVIDER_UNAVAILABLE')[0]
        self.assertEqual(w,replace(v,resources=replace(v.resources,available=(False,False,False))))
    def test_06_budget_only(self):
        v=ToyView();self.assertEqual(b.restrict_views([v],'ACQUISITION_BUDGET_ZERO')[0],replace(v,resources=replace(v.resources,acquisitions_remaining=0)))
    def test_07_no_context_reset_or_input_mutation(self):
        v=ToyView(resources=ToyResources(8,2,(True,True,False),(True,False,True),'AUTHORIZED',20))
        before=deepcopy(v)
        for c in b.SCENARIOS:
            w=b.restrict_views([v],c)[0]
            self.assertEqual((w.facts,w.nodes,w.request_id,w.scope_id,w.evidence_time,w.revision),(v.facts,v.nodes,v.request_id,v.scope_id,v.evidence_time,v.revision))
            self.assertEqual((w.resources.internal_remaining,w.resources.internal_step,w.resources.last_outcome),(8,20,'AUTHORIZED'))
            self.assertEqual(w.resources.available[1:],v.resources.available[1:]);self.assertEqual(w.resources.permitted[1:],v.resources.permitted[1:])
        self.assertEqual(v,before)
    def test_08_exact_live_resources(self):
        self.assertEqual(b.resource_fields('PERMISSION_DENIED','post'),[9,4,1,0,0,0,0,0,2,10])
        self.assertEqual(b.resource_fields('PROVIDER_UNAVAILABLE','post'),[9,4,0,0,0,1,0,0,0,10])
        self.assertEqual(b.resource_fields('ACQUISITION_BUDGET_ZERO','post'),[9,0,1,0,0,1,0,0,3,10])
        self.assertEqual(b.resource_fields('ALLOWED_ZERO','post'),[7,3,1,0,0,1,0,0,0,12])
    def test_09_allowed_zero_admitted_not_missing(self):
        s=b.score_episode(trace(),1,'ALLOWED_ZERO');self.assertEqual(s['failed'],0);self.assertEqual(s['publications'],1)
    def test_10_allowed_one_admitted(self):
        self.assertEqual(b.score_episode(trace('ALLOWED_ONE'),1,'ALLOWED_ONE')['failed'],0)
    def test_11_permission_denial_preserves_needs(self):
        s=b.score_episode(trace('PERMISSION_DENIED'),1,'PERMISSION_DENIED');self.assertEqual((s['failed'],s['provider_calls'],s['denied_attempts']),(0,0,1))
    def test_12_unavailable_preserves_needs(self):
        self.assertEqual(b.score_episode(trace('PROVIDER_UNAVAILABLE'),1,'PROVIDER_UNAVAILABLE')['failed'],0)
    def test_13_zero_budget_preserves_needs(self):
        self.assertEqual(b.score_episode(trace('ACQUISITION_BUDGET_ZERO'),1,'ACQUISITION_BUDGET_ZERO')['failed'],0)
    def test_14_finite_false_sufficiency_not_repaired(self):
        for c in b.SCENARIOS[2:]:
            r=trace(c,p1=0);before=deepcopy(r);s=b.score_episode(r,1,c)
            self.assertEqual((s['failed'],s['post_error'],s['false_sufficient_after_denial'],s['contract_error']),(1,1,1,0));self.assertEqual(r,before)
    def test_15_initial_sufficiency_on_needs_recorded(self):
        for c in b.SCENARIOS:
            s=b.score_episode(trace(c,p0=0),1,c);self.assertEqual((s['failed'],s['missed_proposal'],s['provider_calls']),(1,1,0))
    def test_16_no_proposal_when_sufficient(self):
        for c in b.SCENARIOS:self.assertEqual(b.score_episode(trace(c,p0=0),0,c)['failed'],0)
    def test_17_unnecessary_proposal_not_redeemed(self):
        s=b.score_episode(trace(),0,'ALLOWED_ZERO');self.assertEqual((s['failed'],s['unnecessary_proposal'],s['post_error']),(1,1,0))
    def test_18_blind_rule_denial_is_not_semantic_needs(self):
        for c in b.SCENARIOS[2:]:
            s=b.score_episode(trace(c),0,c);self.assertEqual((s['failed'],s['post_error'],s['unnecessary_proposal'],s['contract_error']),(1,1,1,0))
    def test_19_denial_cannot_publish_a_fake_zero(self):
        r=trace('PERMISSION_DENIED');r['final']['features'][58:62]=[1,2,1,0]
        self.assertEqual(b.score_episode(r,1,'PERMISSION_DENIED')['contract_error'],1)
    def test_20_denial_cannot_dispatch(self):
        r=trace('PERMISSION_DENIED');r['acquisition']['dispatch']=dict(provider_calls=1,fact_publications=0,internal_charged=2)
        self.assertEqual(b.score_episode(r,1,'PERMISSION_DENIED')['contract_error'],1)
    def test_21_denial_has_no_acquisition_reservation(self):
        r=trace('ACQUISITION_BUDGET_ZERO');r['acquisition']['action']['acquisition_reserved']=1
        self.assertEqual(b.score_episode(r,1,'ACQUISITION_BUDGET_ZERO')['contract_error'],1)
    def test_22_all_external_slots_and_source_identity(self):
        for mi in range(4):
            for c in b.SCENARIOS:self.assertEqual(b.score_episode(trace(c,missing_index=mi),1,c)['contract_error'],0)
        r=trace();r['acquisition']['fact_id']='wrong';self.assertEqual(b.score_episode(r,1,'ALLOWED_ZERO')['contract_error'],1)
    def test_23_live_budget_and_outcome_cannot_reset(self):
        for field in (62,63,67,70,71):
            r=trace('PERMISSION_DENIED');r['final']['features'][field]+=1
            self.assertEqual(b.score_episode(r,1,'PERMISSION_DENIED')['contract_error'],1)
    def test_24_other_facts_bindings_clocks_preserved(self):
        for field in (2,3,49):
            r=trace();r['final']['features'][field]+=1
            self.assertEqual(b.score_episode(r,1,'ALLOWED_ZERO')['contract_error'],1)
        r=trace();r['final']['binding']['scope_id']='other'
        self.assertEqual(b.score_episode(r,1,'ALLOWED_ZERO')['contract_error'],1)
    def test_25_no_pending_retry_or_verified_answer(self):
        for field,value in [('pending',{'intent':'retry'}),('runtime_terminal','ANSWERED')]:
            r=trace('PROVIDER_UNAVAILABLE');r[field]=value
            self.assertEqual(b.score_episode(r,1,'PROVIDER_UNAVAILABLE')['contract_error'],1)
    def test_26_successful_candidates_and_deliberate_controls(self):
        self.assertTrue(b.gate(passing_records()))
    def test_27_single_candidate_error_fails(self):
        r=passing_records();r[10]['failed']=1;self.assertFalse(b.gate(r))
    def test_28_strict_order_and_count(self):
        r=passing_records();self.assertFalse(b.gate(r[:-1]));r[0],r[1]=r[1],r[0];self.assertFalse(b.gate(r))
    def test_29_contract_errors_any_policy_fail(self):
        r=passing_records();r[0]['contract_error']=1;self.assertFalse(b.gate(r))
        r=passing_records();r[-1]['contract_error']=1;self.assertFalse(b.gate(r))
    def test_30_rule_patterns_cannot_change(self):
        r=passing_records();r[-11]['post_error']=0;self.assertFalse(b.gate(r))
        r=passing_records();r[-1]['action_attempts']=1;self.assertFalse(b.gate(r))
    def test_31_counters_are_nonnegative_integers(self):
        for value in (-1,False,0.0,None):
            r=passing_records();r[0]['contract_error']=value;self.assertFalse(b.gate(r))
    def test_32_input_coordinate_change_is_exact(self):
        p=np.zeros((3,72),np.int32);p[:,62:]=b.resource_fields('ALLOWED_ZERO','first');before=p.copy()
        for c in b.SCENARIOS:
            a=p.copy();field=b.scenario_spec(c)['field']
            if field is not None:a[:,field]=0
            b.check_initial_packet_change(a,p,c)
        np.testing.assert_array_equal(p,before)
    def test_33_other_input_change_rejected(self):
        p=np.zeros((3,72),np.int32);a=p.copy();a[0,49]=1
        with self.assertRaises(ValueError):b.check_initial_packet_change(a,p,'PERMISSION_DENIED')
        with self.assertRaises(ValueError):b.check_initial_packet_change(p.astype(np.float32),p,'ALLOWED_ZERO')
    def test_34_concrete_workload(self):
        self.assertEqual(len(b.expected_order()),80);self.assertEqual(8*2*5*3712,296960)
        self.assertEqual(3*2*5*3712,111360);self.assertEqual(len(b.OUTPUTS),13)
        self.assertEqual(len(b.PARENTS),12);self.assertEqual(len(b.OWN),4)
    def test_35_fixed_scientific_manifest(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.manifest()['training'],0);self.assertEqual(b.manifest()['fresh_seeds'],0)
        self.assertEqual(b.manifest()['source_files'],b.SOURCES)
    def test_36_fixed_parent_and_replay_budget(self):
        self.assertEqual(b.BASE,'6e59bcbcdf84a37c4bece228b8163042cc6ac06a')
        self.assertEqual(b.ATOL,1e-6);self.assertEqual(b.manifest()['total_neural_rows_max'],56376+2*222720)
        r=passing_records();r[12]['provider_calls']=1;self.assertFalse(b.gate(r))


if __name__=='__main__':
    unittest.main()
