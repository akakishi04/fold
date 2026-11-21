"""C340 authoring tests: real token/scorer paths; toy fits are software fixtures."""
from __future__ import annotations
import contextlib
import copy
import inspect
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c340_length5_training as s
from tests_lm import test_v05_c338_value_support_training as fixtures

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def tree_copy(value):
    """Separate containers while deliberately sharing immutable synthetic tensor leaves."""
    if isinstance(value,dict):return {k:tree_copy(v) for k,v in value.items()}
    if isinstance(value,list):return [tree_copy(v) for v in value]
    return value


class TokenToy(fixtures.Toy):
    def forward(self,tokens,tasks):
        valid=tokens != 256; z=tokens.to(torch.float64)*valid
        pos=torch.arange(1,tokens.shape[1]+1,dtype=torch.float64)
        x=torch.stack((z.sum(1)/1000.,(z*pos).sum(1)/40000.),1)
        for _ in range(4):x=torch.tanh(self.backbone.core(x))
        return self.read.output((self.read.query(x)+self.read.query(x))*.5)


def summary_fixture(gain=1):
    flags=[];pairs=[]
    for seed in s.SEEDS:
        for j,arm in enumerate(s.ARMS):
            partitions={d:dict(answers=288,correct=280+j*gain,wrong_observed=4,absent_digit=4-j*gain,outside_catalog=0) for d in s.DOMAINS}
            flags.append(dict(seed=seed,arm=arm,training_nonpadding_tokens=s.TRAIN_TOKENS[arm],original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True,support=partitions))
        old={str(n):fixtures.contrast(gain=gain) for n in range(2,7)};inside=fixtures.contrast(gain=gain)
        pairs.append(dict(seed=seed,control_full_pass=True,candidate_full_pass=True,original_by_length=old,interior=inside,
            six_answer_gain=gain,six_pair_gain=gain,short_answer_gain=4*gain,short_pair_gain=4*gain,
            interior_answer_gain=gain,interior_pair_gain=gain))
    return dict(candidate_gate=gain>0,eligible_seed_count=5,paired_conditions_valid=True,all_replays=True,
        evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**s.WORK)


class C340ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();torch.set_num_threads(2)
        cls.p=s.previous();cls.cx=cls.p.source().base().context();cls.x=cls.cx[-1]
        cls.data=cls.x.c.p267.dataset();cls.old=cls.x.parent.prompt_dataset(cls.data,cls.x.p313)
        cls.new=cls.cx[2].new_prompts(cls.data)
        cls.tables,cls.y=s.prepared(cls.data,cls.old,cls.new,cls.cx)
        cls.events,cls.mask=s.schedule(s.SEEDS[0],cls.data['TRAIN'],cls.x)
        cls.toy=fixtures.toy_environment()
        cls.toy.p.state_hash=cls.p.state_hash;cls.toy.p.training_fingerprint=cls.p.training_fingerprint
        cls.toy.p.source=lambda:NS(curriculum=lambda:cls.p.source().curriculum(),base=lambda:NS(check_dependencies=lambda *a:None))
        cls.toy.x.parent=NS(plan_for_order=lambda *a:cls.events)
        cls.raws={a:fixtures.raw_fixture(cls.data,'native' if a=='original4' else 'support_loss') for a in s.ARMS}
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)
    def quiet(self):return contextlib.redirect_stdout(io.StringIO())
    def test_01_manifest_and_registered_cohort(self):
        s.validate_seal();self.assertEqual(s.SEEDS,tuple(range(340001,340006)));self.assertEqual(len(s.identities()),10)
        self.assertEqual(s.STEPS,2400);self.assertEqual(s.SOURCE_COUNT,902);self.assertEqual(s.INPUT_COUNT,6243)
        self.assertEqual(s.manifest()['never_train'],'original6 and all HOLDOUT logical rows;masked prompts never enter training')
    def test_02_fixture_is_canonical_and_nonbinary(self):
        self.assertEqual(self.data,fixtures.data_fixture());self.assertEqual(s.digest(self.old),self.p.source().base().PROMPTS_SHA)
        self.assertEqual(set(self.y.tolist()),{48,49,50,51});self.assertEqual((len(self.data['TRAIN']),len(self.data['HOLDOUT'])),(192,96))
    def test_03_all_replacements_equal_canonical_length5_train(self):
        for pr in s.PROFILES:
            expected=torch.stack([self.x.wide.prefix_tensor(r['views']['normal']) for r in self.old['5']['TRAIN'][pr]])
            self.assertTrue(torch.equal(self.tables['original5']['original'][4,pr],expected))
        self.assertEqual(set(inspect.signature(s.optimize).parameters),{'model','arm','tables','y','events','mask','x'})
    def test_04_control_equals_accepted_train_preparation(self):
        baseline,y=self.p.prepared(self.data,self.old,self.new,self.cx)
        self.assertTrue(torch.equal(y,self.y))
        for family,table in baseline.items():
            for key,value in table.items():self.assertTrue(torch.equal(value,self.tables['original4'][family][key]))
    def test_05_invalid_source_metadata_rejected_before_tokens(self):
        bad=copy.deepcopy(self.old);bad['5']['TRAIN']['repeat'][0]['target']+=1
        with self.assertRaises(ValueError):s.prepared(self.data,bad,self.new,self.cx)
        bad=copy.deepcopy(self.old);bad['5']['TRAIN']['repeat'][0]['views']['normal']='leaked target'
        with self.assertRaises(ValueError):s.prepared(self.data,bad,self.new,self.cx)
    def test_06_interior_and_short_token_changes_rejected(self):
        for family,key in (('interior4',(4,'repeat')),('original',(3,'shared_prefix'))):
            bad=tree_copy(self.tables);bad['original5'][family][key]=bad['original5'][family][key].clone();bad['original5'][family][key][0,1]+=1
            with self.assertRaises(ValueError):s.validate_tables(bad,self.y)
    def test_07_missing_changed_profile_or_invalid_dtype_rejected(self):
        bad=tree_copy(self.tables);bad['original5']['original'][4,'shared_suffix']=bad['original4']['original'][4,'shared_suffix']
        with self.assertRaises(ValueError):s.validate_tables(bad,self.y)
        bad=tree_copy(self.tables);bad['original4']['original'][2,'repeat']=bad['original4']['original'][2,'repeat'].float()
        with self.assertRaises(ValueError):s.validate_tables(bad,self.y)
    def test_08_real_fresh_pair_equal_weights_independent_storage(self):
        pair=s.make_pair(s.SEEDS[0],self.x)
        self.assertEqual(self.p.state_hash(pair['original4'].state_dict()),self.p.state_hash(pair['original5'].state_dict()))
        a,b=pair.values();self.assertFalse({v.data_ptr() for v in a.parameters()}&{v.data_ptr() for v in b.parameters()})
        with torch.no_grad():next(a.parameters()).add_(.1)
        self.assertNotEqual(self.p.state_hash(a.state_dict()),self.p.state_hash(b.state_dict()))
    def test_09_all_actual_schedules_have_fixed_quotas(self):
        for seed in s.SEEDS:
            events,mask=s.schedule(seed,self.data['TRAIN'],self.x)
            for arm in s.ARMS:
                counts=s.actual_exposure(arm,events,mask)
                self.assertEqual(counts['original6'],[0]*192);self.assertEqual(counts['interior4'],[50]*192)
                self.assertEqual(counts['original'+str(s.length_for(arm))],[50]*192)
        with self.assertRaises(ValueError):s.schedule(338001,self.data['TRAIN'],self.x)
    def test_10_effective_token_count_records_unequal_byte_exposure(self):
        a,b=[s.token_presentations(self.tables[arm],self.events,self.mask) for arm in s.ARMS]
        self.assertEqual(2*(b-a),115200)
        self.assertEqual(sum(self.y.shape)*600,115200)
    def test_11_actual_batch_selector_changes_only_original4_slots(self):
        curr=self.p.source().curriculum();different=0
        for event,mask in zip(self.events,self.mask,strict=True):
            a,ids=curr.select_tokens(self.tables['original4'],event,mask)
            b,other=curr.select_tokens(self.tables['original5'],event,mask)
            expected=(mask==0).repeat_interleave(2)&(int(event[0,0])==4)
            self.assertTrue(torch.equal(ids,other));self.assertTrue(torch.equal((a!=b).any(1),expected));different+=int(expected.sum())
        self.assertEqual(different,9600)
    def test_12_one_seed_no_length6_or_holdout_training_rows(self):
        self.assertEqual(set(self.events[:,:,2:].flatten().tolist()),set(range(192)))
        self.assertEqual(set(self.events[:,:,0].flatten().tolist()),{2,3,4})
        self.assertFalse({r['id'] for r in self.data['TRAIN']}&{r['id'] for r in self.data['HOLDOUT']})
    def short_fit(self,arm):
        model=TokenToy();reference=copy.deepcopy(model);f=self.toy
        chosen=(self.events[:,0,0]==4).nonzero().flatten()[:2];events=self.events[chosen];mask=self.mask[chosen]
        with patch.object(s,'previous',return_value=f.p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),self.quiet():
            trace,state=s.optimize(model,arm,self.tables[arm],self.y,events,mask,f.x)
        opt=f.x.policy.optimizer_for(reference,'core_slow');losses=[]
        for i in (0,1,0,1):
            tokens,ids=self.p.source().curriculum().select_tokens(self.tables[arm],events[i],mask[i]);opt.zero_grad(set_to_none=True)
            loss=F.cross_entropy(reference(tokens,torch.zeros(48,dtype=torch.int64)),self.y[ids]);losses.append(float(loss.detach()))
            loss.backward();torch.nn.utils.clip_grad_norm_(list(reference.parameters()),1.,error_if_nonfinite=True);opt.step()
        self.assertEqual(trace['ce_history'],losses);self.assertEqual(self.p.state_hash(state),self.p.state_hash(reference.state_dict()))
        return trace,state
    def test_13_control_updates_equal_independent_ce_reference(self):self.short_fit('original4')
    def test_14_candidate_updates_equal_independent_ce_reference(self):self.short_fit('original5')
    def test_15_one_forward_and_native_query_pair_per_update(self):
        trace,_=self.short_fit('original5');self.assertEqual(trace['policy_receipt'],dict(calls=4,query_calls=8,rows=192,grad_calls=4))
        self.assertEqual(trace['boundary'],trace['continuation']);self.assertEqual(trace['optimizer_creations'],1)
    def full_trace(self):
        if not hasattr(type(self),'cached_trace'):
            f=self.toy;model=TokenToy()
            with patch.object(s,'previous',return_value=f.p),self.quiet():
                trace,state=s.train_one(s.SEEDS[0],'original4',model,self.tables['original4'],self.y,self.data['TRAIN'],(f.x,),ROOT,{})
                s.check_trace(trace,self.data['TRAIN'],f.x,self.tables['original4'],self.y)
            type(self).cached_trace=trace
        return copy.deepcopy(type(self).cached_trace)
    def test_16_full2400_toy_fit_continuous_optimizer_and_deep_state(self):
        trace=self.full_trace();self.assertEqual(len(trace['ce_history']),2400);self.assertEqual(trace['boundary'],trace['continuation'])
        self.assertEqual(trace['event_indices'],list(range(1200))*2);self.assertEqual(trace['policy_receipt']['calls'],2400)
    def test_17_saved_input_fingerprint_detects_token_tamper(self):
        trace=self.full_trace();bad=tree_copy(self.tables['original4']);bad['original'][4,'repeat']=bad['original'][4,'repeat'].clone();bad['original'][4,'repeat'][0,1]+=1
        with patch.object(s,'previous',return_value=self.toy.p),self.assertRaises(ValueError):s.check_trace(trace,self.data['TRAIN'],self.toy.x,bad,self.y)
    def test_18_saved_trace_rejects_reset_selection_and_wrong_exposure(self):
        for key,value in (('optimizer_creations',2),('intermediate_evaluations',1),('original_training_length',5),('nonpadding_token_presentations',1),('logical_training_sha256','b'*64)):
            trace=self.full_trace();trace[key]=value
            with patch.object(s,'previous',return_value=self.toy.p),self.assertRaises(ValueError):s.check_trace(trace,self.data['TRAIN'],self.toy.x,self.tables['original4'],self.y)
    def test_19_fixed_gate_requires_every_candidate_full_gate(self):
        value=summary_fixture();s.check_summary(value);self.assertTrue(value['candidate_gate'])
        pairs=value['paired_comparisons'];pairs[0]['candidate_full_pass']=False;self.assertFalse(s.fixed_gate(pairs)[0])
    def test_20_ties_and_one_sided_gains_are_valid_negative(self):
        value=summary_fixture(0);s.check_summary(value);self.assertFalse(value['candidate_gate'])
        for name in ('six_answer_gain','six_pair_gain'):
            pairs=summary_fixture()['paired_comparisons']
            for row in pairs:row[name]=0
            self.assertFalse(s.fixed_gate(pairs)[0])
    def test_21_per_seed_retention_harm_cannot_hide_in_totals(self):
        for name in ('six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain'):
            pairs=summary_fixture()['paired_comparisons'];pairs[0][name]=-1;self.assertFalse(s.fixed_gate(pairs)[0])
    def test_22_summary_count_binding_and_bool_work_rejected(self):
        for kind in ('work','support','gain'):
            value=summary_fixture()
            if kind=='work':value['train_steps']=True
            elif kind=='support':value['seed_results'][0]['support']['original5']['correct']+=1
            else:value['paired_comparisons'][0]['six_answer_gain']=0
            with self.assertRaises(ValueError):s.check_summary(value)
    def test_23_support_partitions_keep_unrestricted256_predictions(self):
        value=s.support().support_report(self.raws['original4'],self.data)
        for row in value.values():self.assertEqual((row['correct'],row['wrong_observed'],row['absent_digit'],row['outside_catalog']),(216,36,36,0))
        # Partitions describe the actual outputs; they add no gate or support objective.
        value=summary_fixture();value['seed_results'][1]['support']['original6']['wrong_observed']-=1;value['seed_results'][1]['support']['original6']['absent_digit']+=1
        s.check_summary(value)
    def science_fixture(self):
        traces=[];records=[];states=[]
        for seed,arm in s.identities():
            state={'w':torch.tensor([float(seed),float(arm=='original5')],dtype=torch.float64)};states.append(state)
            trace={k:'paired' for k in ('initial_sha256','core_initial_sha256','logical_training_sha256','schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')}
            trace.update(seed=seed,arm=arm,nonpadding_token_presentations=s.TRAIN_TOKENS[arm],training_input_sha256=arm,final_sha256=self.p.state_hash(state));traces.append(trace)
            records.append(dict(seed=seed,arm=arm,state_sha256=self.p.state_hash(state),evaluation_policy='native_before',
                raw={m:tree_copy(self.raws[arm]) for m in ('evaluation','replay')},receipts={m:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for m in ('evaluation','replay')}))
        return traces,records,states
    def analyze_fixture(self,items):return s.analyze(*items,self.data,self.cx,self.tables,self.y)
    def test_24_real_analyze_validators_scorers_and_pair_grouping(self):
        items=self.science_fixture()
        with patch.object(s,'check_trace'):
            metrics,value=self.analyze_fixture(items)
        self.assertEqual(len(metrics),10);self.assertFalse(value['candidate_gate'])
        self.assertEqual(value['paired_comparisons'][0]['six_answer_gain'],36)
    def test_25_saved_replay_drift_rejected(self):
        items=self.science_fixture();tree=items[1][0]['raw']['replay']['interior']['HOLDOUT']['balanced']
        tree['normal']=tree['normal'].clone();tree['normal'][0,0]+=1
        with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
    def test_26_state_pairing_and_absent_token_intervention_rejected(self):
        for kind in ('state','pair','tokens'):
            items=self.science_fixture()
            if kind=='state':items[1][0]['state_sha256']='0'*64
            elif kind=='pair':items[0][1]['logical_training_sha256']='mismatch'
            else:items[0][1]['training_input_sha256']=items[0][0]['training_input_sha256']
            with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
    def test_27_checkpoint_schema_cohort_and_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'weights.pt';value=dict(schema='fold-c340-trained-models-v1',identities=[list(z) for z in s.identities()],states=[{}]*10)
            torch.save(value,path);self.assertEqual(len(s.load_states(path)),10);value['identities'].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):s.load_states(path)
    def test_28_native_preflight_real_canonical_inputs_and_backprop(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):(folder/name).write_bytes(s.blob(value))
            with patch.object(self.p.source().base(),'check_dependencies'),self.quiet():s.native_preflight(folder,self.cx,ROOT,{},read)
    def test_29_run_orders_all_training_before_evaluation_and_uses_arm_tables(self):
        calls=[];original=self.p;proxy=NS(**{k:getattr(original,k) for k in ('state_hash','load_data','source')})
        proxy.load_data=lambda *a:(self.data,self.old,self.new)
        proxy.readouts=lambda:NS(measure=lambda *a:(calls.append('eval') or ({},{})))
        def train(seed,arm,model,tables,y,*args):
            calls.append('train');self.assertIs(tables,self.tables[arm]);self.assertTrue(torch.equal(y,self.y))
            return dict(seed=seed,arm=arm),model.state_dict()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'previous',return_value=proxy),patch.object(s,'prepared',return_value=(self.tables,self.y)),\
             patch.object(s,'make_pair',side_effect=lambda *a:{k:TokenToy() for k in s.ARMS}),patch.object(s,'make_model',side_effect=lambda *a:TokenToy()),\
             patch.object(s,'train_one',side_effect=train),patch.object(s,'analyze',return_value=({},summary_fixture())),patch.object(original.source().base(),'check_dependencies'),self.quiet():
            value=s.run_training(Path(tmp),Path(tmp),self.cx,ROOT,{},read)
            self.assertEqual(calls,['train']*10+['eval']*20);self.assertEqual(set(p.name for p in Path(tmp).iterdir()),set(s.OUTPUTS));self.assertTrue(value['candidate_gate'])
    def test_30_saved_semantic_recheck_recomputes_real_metrics_and_rejects_changes(self):
        items=self.science_fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'check_trace'):
            folder=Path(tmp);data_out=folder/'data';out=folder/'science';data_out.mkdir();out.mkdir()
            for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):(data_out/name).write_bytes(s.blob(value))
            metrics,result=self.analyze_fixture(items)
            torch.save(dict(schema='fold-c340-trained-models-v1',identities=[list(z) for z in s.identities()],states=items[2]),out/'trained-models.pt')
            torch.save(dict(schema='fold-c340-evaluations-v1',records=items[1]),out/'evaluations.pt')
            for name,value in (('experiment-plan.json',s.manifest()),('training-traces.json',items[0]),('measurements.json',metrics),('validation-summary.json',result)):(out/name).write_bytes(s.blob(value))
            got=s.semantic_recheck(out,data_out,self.cx,read);self.assertEqual(s.blob(got),s.blob(result))
            (out/'measurements.json').write_bytes(s.blob({'changed':True}))
            with self.assertRaises(ValueError):s.semantic_recheck(out,data_out,self.cx,read)
    def test_31_nonfinite_and_incomplete_cohort_rejected(self):
        items=self.science_fixture();tree=items[1][0]['raw']['evaluation']['interior']['TRAIN']['balanced'];tree['normal']=tree['normal'].clone();tree['normal'][0,0]=float('nan')
        with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
        items=self.science_fixture();items[1].pop()
        with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
    def test_32_actual_exposure_rejects_family_leak_and_cohort_gate_types(self):
        wrong=self.mask.clone();short=int((self.events[:,0,0]!=4).nonzero()[0]);wrong[short,0]=1
        with self.assertRaises(ValueError):s.actual_exposure('original5',self.events,wrong)
        pairs=summary_fixture()['paired_comparisons'];pairs[0]['six_answer_gain']=True
        with self.assertRaises(ValueError):s.fixed_gate(pairs)


if __name__ == '__main__':unittest.main()
