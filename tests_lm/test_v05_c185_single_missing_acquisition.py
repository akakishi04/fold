"""C185 helper tests: real typed runtime/files, synthetic policy outputs, no learned scores."""
from dataclasses import asdict, replace
import hashlib
import inspect
import itertools
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import torch
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as b
from fold_lm.v05 import structured_task_input as t
from fold_lm.v05 import structured_action_runtime as a
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_derived_result as proof


def view(values=(1,None,0,1), resources=None):
    nodes=(t.Node('FACT',0),t.Node('FACT',1),t.Node('AND',left=0,right=1),
           t.Node('FACT',2),t.Node('FACT',3,negate=True),t.Node('AND',left=3,right=4),
           t.Node('OR',left=2,right=5))
    facts=tuple(t.Fact(b.FACT_IDS[i]) if v is None else
                t.Fact(b.FACT_IDS[i],'OBSERVED',v,(f'ref:{i}',)) for i,v in enumerate(values))
    return t.TaskView('scope|q','scope',nodes,facts,resources or t.Resources(12,4))


def rename(v,p):
    facts=[None]*4
    for i,j in enumerate(p): facts[j]=v.facts[i]
    return replace(v,nodes=tuple(replace(n,fact=p[n.fact]) if n.kind=='FACT' else n for n in v.nodes),facts=tuple(facts))


class SyntheticPolicy:
    def __init__(self, sequence=(1,0)):
        self.sequence=sequence;self.calls=[]
    def __call__(self,raw):
        label=self.sequence[min(len(self.calls),len(self.sequence)-1)]
        self.calls.append(raw.clone())
        z=np.zeros((len(raw),2),dtype=np.float32);z[:,label]=1
        return z.argmax(1),z,dict(rows=len(raw),forward_calls=1,cell_calls=7)


def ideal_records():
    rows=[]
    for s,arm in [(s,a) for s in b.SEEDS for a in b.ARMS]+[(0,r) for r in b.RULES]:
        for li in range(2):
            for bit in (0,1):
                r=dict(seed=s,arm=arm,layout=li,completion=bit,episodes=3712,
                    labels=dict(sufficient=2944,needs=768),contract_error=0,failed=0,
                    initial_error=0,missed_acquisition=0,unnecessary_acquisition=0,post_error=0,provider_calls=768)
                if arm==b.RULES[0]:r.update(provider_calls=3712,unnecessary_acquisition=2944)
                if arm==b.RULES[1]:r.update(provider_calls=0,missed_acquisition=768)
                rows.append(r)
    return rows


class C185Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.providers=[];self.endpoints={}
        for i,fid in enumerate(b.FACT_IDS):
            raw=b.fixture_bytes(i,0);path=Path(self.tmp.name)/str(i);path.write_bytes(raw)
            sb=life.SourceBinding(f'C185-fixture-{i}-0',hashlib.sha256(raw).hexdigest())
            provider=life.FileSnapshotProvider(path,sb);self.providers.append(provider)
            self.endpoints[fid]=life.Endpoint(sb,provider)

    def test_01_binding_all_permutations(self):
        v=view()
        for p in itertools.permutations(range(4)):
            changed=rename(v,p);raw,bindings=b.bind_views([changed])
            self.assertEqual(t.decode(bindings[0].packet),v)
            self.assertEqual(bindings[0].canonical_to_input,p)
            self.assertEqual(raw[0].tolist(),list(t.encode(v).features))

    def test_02_binding_preserves_ids_and_references(self):
        v=rename(view(),(3,2,1,0));_,bs=b.bind_views([v]);nv=t.decode(bs[0].packet)
        self.assertEqual(set(f.fact_id for f in nv.facts),set(f.fact_id for f in v.facts))
        self.assertEqual({f.fact_id:f.reference_ids for f in nv.facts},{f.fact_id:f.reference_ids for f in v.facts})

    def test_03_binding_keeps_resources(self):
        v=view(resources=t.Resources(7,3,(False,True,False),(False,True,False),'PERMISSION_DENIED',12))
        raw,_=b.bind_views([v]);self.assertEqual(raw[0,62:].tolist(),list(t.encode(v).features[62:]))

    def test_04_known_zero_is_not_unknown(self):
        raw,_=b.bind_views([view()]);self.assertEqual(raw[0,50:58].tolist(),[1,1,0,0,1,2,1,0])

    def test_05_source_view_is_immutable(self):
        v=view();before=asdict(v);b.bind_views([v]);self.assertEqual(before,asdict(v))

    def test_06_repeated_fact_is_rejected(self):
        v=view();v=replace(v,nodes=(replace(v.nodes[0],fact=1),)+v.nodes[1:])
        with self.assertRaises(ValueError):b.bind_views([v])

    def test_07_unusable_status_is_rejected(self):
        v=view();facts=list(v.facts);facts[1]=t.Fact(facts[1].fact_id,'STALE')
        with self.assertRaises(ValueError):b.bind_views([replace(v,facts=tuple(facts))])

    def test_08_target_maps_to_external_identity(self):
        v=rename(view(),(3,2,1,0));_,bs=b.bind_views([v])
        self.assertEqual(b.unique_target(v,bs[0]),(1,2,b.FACT_IDS[1]))

    def test_09_stale_binding_rejected(self):
        v=view();_,bs=b.bind_views([v]);v=replace(v,resources=replace(v.resources,internal_step=8))
        with self.assertRaises(ValueError):b.unique_target(v,bs[0])

    def test_10_forged_mapping_rejected(self):
        v=view();_,bs=b.bind_views([v]);bad=replace(bs[0],canonical_to_input=(1,0,2,3))
        with self.assertRaises(ValueError):b.unique_target(v,bad)

    def test_11_multiple_unknown_targets_rejected(self):
        v=view((None,None,0,1));_,bs=b.bind_views([v])
        with self.assertRaises(ValueError):b.unique_target(v,bs[0])

    def test_12_zero_budget_does_not_call_policy(self):
        policy=SyntheticPolicy();rs,ar,_=b.run_block([view(resources=t.Resources(0,4))],self.endpoints,policy)
        self.assertFalse(policy.calls);self.assertEqual(ar['predictions'].tolist(),[[-1,-1]])
        self.assertEqual(rs[0]['decision_charges'],0)

    def test_13_charge_only_changes_accounting(self):
        v=view();owner=life.AcquisitionOwner(a.RuntimeState(v),{})
        self.assertTrue(b.charge_decision(owner));after=owner.state.view
        self.assertEqual(after.facts,v.facts);self.assertEqual(after.resources.internal_remaining,11)
        self.assertEqual(after.resources.internal_step,8);self.assertEqual(after.resources.acquisitions_remaining,4)

    def test_14_sufficient_never_calls_provider(self):
        policy=SyntheticPolicy((0,));rs,ar,m=b.run_block([view()],self.endpoints,policy)
        self.assertEqual(sum(p.reads for p in self.providers),0)
        self.assertEqual(rs[0]['status'],'SUFFICIENT_CLASSIFICATION');self.assertIsNone(rs[0]['acquisition'])
        self.assertEqual(ar['predictions'].tolist(),[[0,-1]]);self.assertEqual(m['rows'],1)

    def test_15_acquisition_zero_is_observed(self):
        rs,ar,_=b.run_block([view()],self.endpoints,SyntheticPolicy())
        self.assertEqual(rs[0]['final']['features'][50:54],(1,2,1,0))
        self.assertEqual(ar['predictions'].tolist(),[[1,0]])
        self.assertEqual(self.providers[1].reads,1)

    def test_16_acquisition_one_is_observed(self):
        raw=b.fixture_bytes(1,1);p=Path(self.tmp.name)/'one';p.write_bytes(raw)
        sb=life.SourceBinding('C185-fixture-1-1',hashlib.sha256(raw).hexdigest());provider=life.FileSnapshotProvider(p,sb)
        self.endpoints[b.FACT_IDS[1]]=life.Endpoint(sb,provider)
        rs,_,_=b.run_block([view()],self.endpoints,SyntheticPolicy())
        self.assertEqual(rs[0]['final']['features'][50:54],(1,2,1,1));self.assertEqual(provider.reads,1)
        self.assertEqual(b.assess(rs[0],1,1)['failed'],0)

    def test_17_real_renamed_target_and_receipt(self):
        rs,_,_=b.run_block([rename(view(),(3,2,1,0))],self.endpoints,SyntheticPolicy())
        r=rs[0];self.assertEqual(r['acquisition']['input_index'],2)
        self.assertEqual(r['receipts'][0]['fact_id'],b.FACT_IDS[1]);self.assertEqual(b.assess(r,1,0)['failed'],0)

    def test_18_first_and_post_inputs_use_live_counters(self):
        policy=SyntheticPolicy();rs,ar,_=b.run_block([view()],self.endpoints,policy)
        self.assertEqual(policy.calls[0][0,[62,63,71]].tolist(),[11,4,8])
        self.assertEqual(policy.calls[1][0,[62,63,71]].tolist(),[7,3,12])
        self.assertEqual(rs[0]['final']['features'][62],7)

    def test_19_permission_denial_remains_model_need(self):
        r=t.Resources(12,4,permitted=(False,False,False));policy=SyntheticPolicy((1,1))
        rs,ar,_=b.run_block([view(resources=r)],self.endpoints,policy)
        self.assertEqual(rs[0]['acquisition']['action']['reason'],'PERMISSION_DENIED')
        self.assertEqual(sum(p.reads for p in self.providers),0);self.assertEqual(ar['predictions'].tolist(),[[1,1]])

    def test_20_provider_unavailable_no_io(self):
        rs,_,_=b.run_block([view(resources=t.Resources(12,4,available=(False,False,False)))],self.endpoints,SyntheticPolicy((1,1)))
        self.assertEqual(rs[0]['acquisition']['action']['reason'],'PROVIDER_UNAVAILABLE')
        self.assertEqual(sum(p.reads for p in self.providers),0)

    def test_21_acquisition_budget_zero_no_io(self):
        rs,_,_=b.run_block([view(resources=t.Resources(12,0))],self.endpoints,SyntheticPolicy((1,1)))
        self.assertEqual(rs[0]['acquisition']['action']['reason'],'BUDGET_EXHAUSTED')
        self.assertEqual(sum(p.reads for p in self.providers),0)

    def test_22_wrong_delivery_identity_not_published(self):
        e=self.endpoints[b.FACT_IDS[1]]
        self.endpoints[b.FACT_IDS[1]]=life.Endpoint(e.source,lambda req:replace(e.fetch(req),fact_id='wrong'))
        rs,_,_=b.run_block([view()],self.endpoints,SyntheticPolicy((1,1)))
        self.assertFalse(rs[0]['receipts']);self.assertEqual(rs[0]['final']['features'][50:54],(1,1,0,0))
        self.assertEqual(self.providers[1].reads,1)

    def test_23_provider_failure_no_retry(self):
        self.providers[1].path.write_bytes(b'corrupt')
        policy=SyntheticPolicy((1,1));rs,_,_=b.run_block([view()],self.endpoints,policy)
        self.assertEqual(self.providers[1].reads,1);self.assertEqual(len(policy.calls),2)
        self.assertEqual(rs[0]['status'],'UNRESOLVED');self.assertFalse(rs[0]['receipts'])

    def test_24_remaining_need_never_requests_twice(self):
        rs,ar,_=b.run_block([view()],self.endpoints,SyntheticPolicy((1,1)))
        self.assertEqual(self.providers[1].reads,1);self.assertEqual(rs[0]['status'],'UNRESOLVED')
        self.assertEqual(b.assess(rs[0],1,0)['post_error'],1)

    def test_25_no_proof_answer_or_auxiliary_rescue(self):
        with patch.object(proof,'verify',side_effect=AssertionError('forbidden proof')):
            rs,_,_=b.run_block([view()],self.endpoints,SyntheticPolicy())
        self.assertIsNone(rs[0]['runtime_terminal']);self.assertIsNone(rs[0]['acquisition']['action']['derived'])

    def test_26_hidden_completion_not_in_initial_policy_input(self):
        policy=SyntheticPolicy();b.run_block([view()],self.endpoints,policy)
        self.assertEqual(policy.calls[0][0,50:54].tolist(),[1,1,0,0])
        self.assertNotEqual(policy.calls[0][0,50:54].tolist(),policy.calls[1][0,50:54].tolist())

    def test_27_wrong_sufficient_is_scored_not_corrected(self):
        rs,ar,_=b.run_block([view()],self.endpoints,SyntheticPolicy((0,)))
        score=b.assess(rs[0],1,0);self.assertEqual(score['missed_acquisition'],1)
        self.assertEqual(score['initial_error'],1);self.assertEqual(ar['predictions'][0,0],0)

    def test_28_wrong_need_is_counted_as_unnecessary(self):
        rs,_,_=b.run_block([view()],self.endpoints,SyntheticPolicy())
        s=b.assess(rs[0],0,0);self.assertEqual(s['unnecessary_acquisition'],1);self.assertEqual(s['failed'],1)

    def test_29_nonfinite_logits_rejected(self):
        raw,_=b.bind_views([view()])
        class Bad:
            def __call__(self,x):return np.ones(len(x),dtype=int),np.full((len(x),2),np.nan,dtype=np.float32),{}
        with self.assertRaises(ValueError):b.checked_predictions(Bad(),raw)

    def test_30_repaired_prediction_rejected(self):
        raw,_=b.bind_views([view()])
        class Bad:
            def __call__(self,x):return np.ones(len(x),dtype=int),np.zeros((len(x),2),dtype=np.float32),{}
        with self.assertRaises(ValueError):b.checked_predictions(Bad(),raw)

    def test_31_batch_states_are_independent(self):
        vs=[view(),replace(view((None,1,0,1)),request_id='other|q',scope_id='other')]
        rs,_,_=b.run_block(vs,self.endpoints,SyntheticPolicy())
        self.assertEqual(len(rs),2);self.assertEqual(self.providers[0].reads,1);self.assertEqual(self.providers[1].reads,1)
        self.assertNotEqual(rs[0]['receipts'][0]['scope_id'],rs[1]['receipts'][0]['scope_id'])

    def test_32_fixed_gate_perfect_candidates_not_controls(self):
        records=ideal_records()
        for r in records:
            if r['arm']=='FINAL_ONLY':r.update(failed=100,initial_error=100)
        self.assertTrue(b.gate(records))

    def test_33_single_candidate_error_fails(self):
        rows=ideal_records();rows[4]['initial_error']=1
        self.assertFalse(b.gate(rows))

    def test_34_incomplete_or_broken_control_fails(self):
        rows=ideal_records();self.assertFalse(b.gate(rows[:-1]));rows[-1]['provider_calls']=1
        self.assertFalse(b.gate(rows))

    def test_35_manifest_and_label_free_interfaces(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        for fn in (b.bind_views,b.unique_target,b.run_block,b.acquire_once):
            self.assertFalse({'label','completion','expected','truth'} & set(inspect.signature(fn).parameters))
        self.assertEqual(len(b.OUTPUTS),13);self.assertEqual(b.manifest()['episodes'],3712*2*2*8)

    def test_36_rule_controls_and_cost(self):
        for name,reads in ((b.RULES[0],1),(b.RULES[1],0)):
            before=sum(p.reads for p in self.providers)
            rs,ar,m=b.run_block([view()],self.endpoints,b.RulePolicy(name))
            self.assertEqual(sum(p.reads for p in self.providers)-before,reads)
            self.assertFalse(ar['logit_present'].any());self.assertEqual(m['rows'],0)
            self.assertEqual(rs[0]['final']['features'][62],7 if reads else 11)


if __name__=='__main__':unittest.main()
