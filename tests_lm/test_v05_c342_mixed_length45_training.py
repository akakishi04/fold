"""C342 author checks: canonical inputs/real scorers, explicit toy fits and logits."""
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
from fold_lm.v05_benchmarks import model_c342_mixed_length45_training as s
from tests_lm import test_v05_c340_length5_training as old_tests

ROOT = Path(__file__).resolve().parents[1]
fixtures = old_tests.fixtures
TokenToy = old_tests.TokenToy
tree_copy = old_tests.tree_copy


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def summary_fixture(gain=1):
    flags,pairs = [],[]
    for seed in s.SEEDS:
        for j,arm in enumerate(s.ARMS):
            wrong = gain if j == 0 else 0
            support = {d:dict(answers=288,correct=288-(wrong if d == 'original4' else 0),wrong_observed=0,
                absent_digit=wrong if d == 'original4' else 0,outside_catalog=0) for d in s.DOMAINS}
            original = {str(n):not (n == 4 and wrong) for n in range(2,7)}
            flags.append(dict(seed=seed,arm=arm,training_nonpadding_tokens=s.TRAIN_TOKENS[arm],
                original_pass=original,interior_pass=True,retention_pass=all(original.values()),support=support,
                failures={d:dict(local=wrong if d == 'original4' else 0,order=0) for d in s.DOMAINS}))
        old = {str(n):fixtures.contrast(correct=288-(gain if n == 4 else 0),gain=gain if n == 4 else 0,
            pairs=144-(gain if n == 4 else 0)) for n in range(2,7)}
        pairs.append(dict(seed=seed,control_full_pass=gain == 0,candidate_full_pass=True,original_by_length=old,
            interior=fixtures.contrast(correct=288,gain=0,pairs=144),four_answer_gain=gain,four_pair_gain=gain,
            six_answer_gain=0,six_pair_gain=0,short_answer_gain=0,short_pair_gain=0,interior_answer_gain=0,interior_pair_gain=0))
    return dict(candidate_gate=gain > 0,eligible_seed_count=5,paired_conditions_valid=True,all_replays=True,
        evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**s.WORK)


class C342ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.p = s.previous(); cls.cx = cls.p.source().base().context(); cls.x = cls.cx[-1]
        cls.data = cls.x.c.p267.dataset(); cls.old = cls.x.parent.prompt_dataset(cls.data,cls.x.p313)
        cls.new = cls.cx[2].new_prompts(cls.data); cls.tables,cls.y = s.prepared(cls.data,cls.old,cls.new,cls.cx)
        cls.events,cls.family = s.schedule(s.SEEDS[0],cls.data['TRAIN'],cls.x)
        cls.choices = {arm:s.length_mask(cls.events,cls.family,arm) for arm in s.ARMS}
        cls.toy = fixtures.toy_environment(); cls.toy.p.state_hash = cls.p.state_hash
        cls.toy.p.training_fingerprint = cls.p.training_fingerprint
        cls.toy.p.source = lambda:NS(curriculum=lambda:cls.p.source().curriculum(),base=lambda:NS(check_dependencies=lambda *a:None))
        cls.toy.x.parent = NS(plan_for_order=lambda *a:cls.events)
        with patch.object(s,'previous',return_value=cls.toy.p),contextlib.redirect_stdout(io.StringIO()):
            cls.fitted_trace,cls.fitted_state = s.train_one(s.SEEDS[0],'mixed45',TokenToy(),cls.tables,cls.y,
                cls.data['TRAIN'],(cls.toy.x,),ROOT,{})
            s.check_trace(cls.fitted_trace,cls.data['TRAIN'],cls.toy.x,cls.tables,cls.y)
        cls.raw = fixtures.raw_fixture(cls.data,'native')
        for domain in [*cls.raw['original'].values(),cls.raw['interior']]:
            for split,profiles in domain.items():
                for views in profiles.values():
                    for kind,z in views.items():
                        z.fill_(-4.)
                        if kind == 'normal':
                            for i,row in enumerate(cls.data[split]): z[i,row['target']] = 4.
                        else: z[:,48] = 4.
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)
    def quiet(self):return contextlib.redirect_stdout(io.StringIO())
    def trace(self):return copy.deepcopy(self.fitted_trace)
    def write_data(self,folder):
        for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):
            (folder/name).write_bytes(s.blob(value))
    def test_01_manifest_cohort_budget_and_new_estimand(self):
        s.validate_seal();self.assertEqual(s.SEEDS,tuple(range(342001,342006)));self.assertEqual(s.ORDERS,tuple(range(342101,342106)))
        self.assertEqual(s.ARMS,('original5','mixed45'));self.assertEqual(len(s.identities()),10)
        self.assertEqual((s.STEPS,s.WORK['train_steps'],s.WORK['model_forward_calls']),(2400,24000,27420))
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.MODULES),(916,7205,235))
        self.assertRegex(s.manifest()['acceptance_base'],'^[0-9a-f]{40}$')
        self.assertIn('original4 repair',s.manifest()['estimand']);self.assertEqual(s.FIRST_QUOTAS,(8,8,9))
    def test_02_banks_equal_immutable_c340_canonical_preparation(self):
        banks,y = s.reference().prepared(self.data,self.old,self.new,self.cx)
        self.assertTrue(torch.equal(y,self.y))
        self.assertEqual(s.training_fingerprint(banks,y,self.events,self.family,self.choices['mixed45']),
                         s.training_fingerprint(self.tables,self.y,self.events,self.family,self.choices['mixed45']))
        for pr in s.PROFILES:
            for n in (4,5):
                expected = torch.stack([self.x.wide.prefix_tensor(r['views']['normal']) for r in self.old[str(n)]['TRAIN'][pr]])
                self.assertTrue(torch.equal(self.tables['original'+str(n)]['original'][4,pr],expected))
    def test_03_training_sources_are_nonbinary_train_only(self):
        self.assertEqual(self.data,fixtures.data_fixture());self.assertEqual(set(self.y.tolist()),{48,49,50,51})
        self.assertEqual((len(self.data['TRAIN']),len(self.data['HOLDOUT'])),(192,96))
        self.assertEqual(set(self.events[:,:,2:].flatten().tolist()),set(range(192)))
        self.assertFalse({r['id'] for r in self.data['TRAIN']}&{r['id'] for r in self.data['HOLDOUT']})
        self.assertEqual(set(inspect.signature(s.select_tokens).parameters),{'tables','event','family','selected'})
    def test_04_fresh_native_pair_has_equal_independent_trainable_weights(self):
        models = s.make_pair(s.SEEDS[0],self.x);a,b = models.values()
        self.assertEqual(self.p.state_hash(a.state_dict()),self.p.state_hash(b.state_dict()))
        self.assertFalse({v.data_ptr() for v in a.parameters()}&{v.data_ptr() for v in b.parameters()})
        self.assertEqual(sum(v.numel() for v in a.parameters()),14256)
        with torch.no_grad():next(a.parameters()).add_(.1)
        self.assertNotEqual(self.p.state_hash(a.state_dict()),self.p.state_hash(b.state_dict()))
    def test_05_all_schedules_keep_canonical_events_and_family_masks(self):
        q = self.p.source().curriculum()
        for seed,order in zip(s.SEEDS,s.ORDERS,strict=True):
            events,family = s.schedule(seed,self.data['TRAIN'],self.x)
            expected = self.x.parent.plan_for_order(order,'two_to_four',self.data['TRAIN'],self.x.p312,self.x.pairs)
            self.assertTrue(torch.equal(events,expected));self.assertTrue(torch.equal(family,q.family_mask(events,'batch4')))
        with self.assertRaises(ValueError):s.schedule(340001,self.data['TRAIN'],self.x)
    def test_06_all_five_allocations_have_exact_per_cycle_row_exposure(self):
        for seed in s.SEEDS:
            events,family = s.schedule(seed,self.data['TRAIN'],self.x)
            for arm in s.ARMS:
                bits = s.length_mask(events,family,arm);exposure = s.actual_exposure(events,family,bits,arm)
                for cycle in exposure:
                    self.assertEqual(cycle['original2'],[100]*192);self.assertEqual(cycle['original3'],[100]*192)
                    self.assertEqual(cycle['interior4'],[50]*192);self.assertEqual(cycle['original6'],[0]*192)
                    self.assertEqual(cycle['original4'],[25 if arm == 'mixed45' else 0]*192)
                    self.assertEqual(cycle['original5'],[25 if arm == 'mixed45' else 50]*192)
    def test_07_allocation_determinism_and_no_input_mutation(self):
        before = self.p.state_hash((self.events,self.family))
        self.assertTrue(torch.equal(s.length_mask(self.events,self.family,'mixed45'),self.choices['mixed45']))
        self.assertEqual(self.p.state_hash((self.events,self.family)),before)
        self.assertFalse(bool(self.choices['original5'].any()))
    def test_08_exact_pair_profile_quotas_and_second_cycle_complement(self):
        selected = self.choices['mixed45'];eligible = ((self.events[:,:,0] == 4)&(self.family == 0)).long()
        self.assertTrue(torch.equal(selected[:1200]+selected[1200:],eligible))
        for phase,quotas in ((0,(8,8,9)),(1,(8,9,8))):
            counts = self.p.source().curriculum().exposure(self.events,selected[phase*1200:(phase+1)*1200])
            for key,value in counts.items():
                n,pr,_,_ = map(int,key.split(':'));self.assertEqual(value[1],quotas[pr] if n == 4 else 0)
    def test_09_allocator_uses_restricted_edges_and_has_no_fallback(self):
        q = self.p.source().curriculum();actual = q.balanced_allocation;calls = []
        def allocate(neighbors,quotas):
            calls.append((neighbors,quotas))
            return actual(neighbors,quotas)
        with patch.object(q,'balanced_allocation',side_effect=allocate):s.length_mask(self.events,self.family,'mixed45')
        # The accepted family-mask reconstruction first invokes the same helper
        # on all24 pairs. The child then invokes it on original-only edges.
        self.assertEqual(len(calls),6);self.assertTrue(all(len(r) == 24 for n,_ in calls[:3] for r in n))
        self.assertTrue(all(11 <= len(r) <= 13 for n,_ in calls[3:] for r in n))
        self.assertEqual([x[1] for x in calls[3:]],[[8]*96,[8]*96,[9]*96])
        def fail_child(neighbors,quotas):
            if all(len(r) == 24 for r in neighbors):return actual(neighbors,quotas)
            raise ValueError('infeasible')
        with patch.object(q,'balanced_allocation',side_effect=fail_child),self.assertRaisesRegex(ValueError,'infeasible'):
            s.length_mask(self.events,self.family,'mixed45')
    def test_10_actual_selector_changes_only_registered_query_pair_tokens(self):
        changed = 0;bits = self.choices['mixed45'];zero = torch.zeros(24,dtype=torch.int64)
        for step in range(2400):
            index = step%1200;event,family = self.events[index],self.family[index]
            control,ids = s.select_tokens(self.tables,event,family,zero)
            mixed,other = s.select_tokens(self.tables,event,family,bits[step])
            expected = bits[step].repeat_interleave(2).bool()
            self.assertTrue(torch.equal(ids,other));self.assertTrue(torch.equal((control != mixed).any(1),expected))
            self.assertTrue(torch.equal(expected[::2],expected[1::2]));changed += int(expected.sum())
            if bool(expected.any()):
                four = self.tables['original4']['original'][4,s.PROFILES[int(event[0,1])]][ids]
                self.assertTrue(torch.equal(mixed[expected],four[expected]))
        self.assertEqual(changed,9600)
    def test_11_control_equals_c340_all5_batches_in_both_cycles(self):
        q = self.p.source().curriculum()
        for event,family in zip(self.events,self.family,strict=True):
            expected,ids = q.select_tokens(self.tables['original5'],event,family)
            actual,got = s.select_tokens(self.tables,event,family,torch.zeros(24,dtype=torch.int64))
            self.assertTrue(torch.equal(actual,expected));self.assertTrue(torch.equal(got,ids))
    def test_12_nonpadding_stream_counts_actual_control_and_candidate(self):
        values = {a:s.input_accounting(self.tables,self.y,self.events,self.family,self.choices[a]) for a in s.ARMS}
        self.assertEqual({a:v[0] for a,v in values.items()},s.TRAIN_TOKENS)
        self.assertEqual(values['original5'][0]-values['mixed45'][0],57600)
        self.assertNotEqual(values['original5'][1],values['mixed45'][1])
        self.assertEqual(values['mixed45'][1],self.fitted_trace['actual_training_stream_sha256'])
    def test_13_masks_reject_leak_dtype_and_changed_family(self):
        bad = self.choices['mixed45'].clone();i = int((self.events[:,0,0] != 4).nonzero()[0]);bad[i,0] = 1
        with self.assertRaises(ValueError):s.check_length_mask(self.events,self.family,'mixed45',bad)
        with self.assertRaises(ValueError):s.check_length_mask(self.events,self.family,'mixed45',self.choices['mixed45'].bool())
        family = self.family.clone();family[i,0] = 1
        with self.assertRaises(ValueError):s.length_mask(self.events,family,'mixed45')
    def test_14_masks_reject_wrong_complement_and_pair_quota(self):
        i,k = self.choices['mixed45'][:1200].nonzero()[0].tolist()
        for complement in (False,True):
            bad = self.choices['mixed45'].clone();bad[i,k] = 0
            if complement:bad[1200+i,k] = 1
            with self.assertRaises(ValueError):s.check_length_mask(self.events,self.family,'mixed45',bad)
        with self.assertRaises(ValueError):s.check_length_mask(self.events,self.family,'original5',self.choices['mixed45'])
    def test_15_token_and_target_stream_binds_order_and_labels(self):
        value = s.input_accounting(self.tables,self.y,self.events,self.family,self.choices['mixed45'])
        labels = self.y.clone();labels[0] = 48+(int(labels[0])-48+1)%4
        changed = s.input_accounting(self.tables,labels,self.events,self.family,self.choices['mixed45'])
        self.assertEqual(value[0],changed[0]);self.assertNotEqual(value[1],changed[1])
        a = s.training_fingerprint(self.tables,self.y,self.events,self.family,self.choices['original5'])
        b = s.training_fingerprint(self.tables,self.y,self.events,self.family,self.choices['mixed45'])
        self.assertNotEqual(a,b)
    def short_fit(self,arm):
        model = TokenToy();reference = copy.deepcopy(model);f = self.toy
        indices = (self.events[:,0,0] == 4).nonzero().flatten()[:2]
        events,family = self.events[indices],self.family[indices]
        selected = torch.cat((self.choices[arm][indices],self.choices[arm][1200+indices]))
        with patch.object(s,'previous',return_value=f.p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),self.quiet():
            trace,state = s.optimize(model,arm,self.tables,self.y,events,family,selected,f.x)
        opt = f.x.policy.optimizer_for(reference,'core_slow');losses = []
        for step in range(4):
            tokens,ids = s.select_tokens(self.tables,events[step%2],family[step%2],selected[step]);opt.zero_grad(set_to_none=True)
            loss = F.cross_entropy(reference(tokens,torch.zeros(48,dtype=torch.int64)),self.y[ids]);losses.append(float(loss.detach()))
            loss.backward();torch.nn.utils.clip_grad_norm_(list(reference.parameters()),1.,error_if_nonfinite=True);opt.step()
        self.assertEqual(trace['ce_history'],losses);self.assertEqual(self.p.state_hash(state),self.p.state_hash(reference.state_dict()))
        return trace,state,model
    def test_16_all5_updates_equal_independent_ordinary_ce_reference(self):self.short_fit('original5')
    def test_17_mixed_updates_equal_independent_ordinary_ce_reference(self):self.short_fit('mixed45')
    def test_18_one_native_forward_per_update_and_deep_checkpoint(self):
        trace,state,model = self.short_fit('mixed45')
        self.assertEqual(trace['policy_receipt'],dict(calls=4,query_calls=8,rows=192,grad_calls=4))
        self.assertEqual(trace['boundary'],trace['continuation']);self.assertEqual(trace['optimizer_creations'],1)
        before = self.p.state_hash(state)
        with torch.no_grad():next(model.parameters()).add_(1.)
        self.assertEqual(self.p.state_hash(state),before)
    def test_19_full2400_toy_fit_preserves_optimizer_and_actual_inputs(self):
        trace = self.trace();self.assertEqual(len(trace['ce_history']),2400);self.assertEqual(trace['boundary'],trace['continuation'])
        self.assertEqual(trace['event_indices'],list(range(1200))*2);self.assertEqual(trace['policy_receipt']['calls'],2400)
        self.assertEqual(trace['nonpadding_token_presentations'],3168000)
        with patch.object(s,'previous',return_value=self.toy.p):s.check_trace(trace,self.data['TRAIN'],self.toy.x,self.tables,self.y)
    def test_20_trace_rejects_mask_stream_exposure_and_recipe_tampering(self):
        for key,value in (('length_mask_sha256','a'*64),('actual_training_stream_sha256','b'*64),
                          ('nonpadding_token_presentations',3225600),('logical_training_sha256','c'*64)):
            trace = self.trace();trace[key] = value
            with patch.object(s,'previous',return_value=self.toy.p),self.assertRaises(ValueError):s.check_trace(trace,self.data['TRAIN'],self.toy.x,self.tables,self.y)
        trace = self.trace();trace['actual_exposure_per_cycle'][0]['original4'][0] = 24
        with patch.object(s,'previous',return_value=self.toy.p),self.assertRaises(ValueError):s.check_trace(trace,self.data['TRAIN'],self.toy.x,self.tables,self.y)
    def test_21_trace_rejects_reset_selection_policy_and_nonfinite_history(self):
        for key,value in (('optimizer_creations',2),('intermediate_evaluations',1),('length_policy','original5'),('ce_history',[float('nan')]*2400)):
            trace = self.trace();trace[key] = value
            with patch.object(s,'previous',return_value=self.toy.p),self.assertRaises(ValueError):s.check_trace(trace,self.data['TRAIN'],self.toy.x,self.tables,self.y)
    def test_22_trace_rejects_changed_canonical_training_bank(self):
        banks = tree_copy(self.tables);key = (4,'repeat')
        banks['original4']['original'][key] = banks['original4']['original'][key].clone();banks['original4']['original'][key][0,1] += 1
        with patch.object(s,'previous',return_value=self.toy.p),self.assertRaises(ValueError):s.check_trace(self.trace(),self.data['TRAIN'],self.toy.x,banks,self.y)
    def test_23_fixed_gate_passes_repair_without_six_gain(self):
        value = summary_fixture();s.check_summary(value);self.assertTrue(value['candidate_gate'])
        self.assertTrue(all(r['six_answer_gain'] == r['six_pair_gain'] == 0 for r in value['paired_comparisons']))
    def test_24_fixed_gate_requires_all_seeds_and_full_candidate_gates(self):
        pairs = summary_fixture()['paired_comparisons'];pairs[0]['candidate_full_pass'] = False
        self.assertFalse(s.fixed_gate(pairs)[0])
        with self.assertRaises(ValueError):s.fixed_gate(pairs[:-1])
        pairs.reverse()
        with self.assertRaises(ValueError):s.fixed_gate(pairs)
    def test_25_no_domain_loss_can_hide_in_pooled_retention(self):
        for domain in s.DOMAINS:
            for criterion in ('answer_gain','query_pair_gain'):
                pairs = summary_fixture()['paired_comparisons']
                target = pairs[0]['interior'] if domain == 'interior4' else pairs[0]['original_by_length'][domain[-1]]
                target[criterion] = -1;self.assertFalse(s.fixed_gate(pairs)[0])
        pairs = summary_fixture()['paired_comparisons'];pairs[0]['original_by_length']['5']['answer_gain'] = True
        with self.assertRaises(ValueError):s.fixed_gate(pairs)
    def test_26_original4_endpoint_requires_both_strict_gains_and_ties_fail(self):
        value = summary_fixture(0);s.check_summary(value);self.assertFalse(value['candidate_gate'])
        for criterion in ('answer_gain','query_pair_gain'):
            pairs = summary_fixture()['paired_comparisons']
            for row in pairs:row['original_by_length']['4'][criterion] = 0
            self.assertFalse(s.fixed_gate(pairs)[0])
    def test_27_summary_reconciles_counts_gains_and_token_cost(self):
        for kind in ('work','support','endpoint','tokens','full'):
            value = summary_fixture()
            if kind == 'work':value['train_steps'] = True
            elif kind == 'support':value['seed_results'][0]['support']['original5']['correct'] -= 1
            elif kind == 'endpoint':value['paired_comparisons'][0]['four_answer_gain'] = 0
            elif kind == 'tokens':value['seed_results'][1]['training_nonpadding_tokens'] = 3225600
            else:value['paired_comparisons'][0]['candidate_full_pass'] = False
            with self.assertRaises(ValueError):s.check_summary(value)
    def test_28_support_partition_describes_unrestricted_predictions_only(self):
        raw = fixtures.raw_fixture(self.data,'native');report = s.support().support_report(raw,self.data)
        for row in report.values():self.assertEqual((row['correct'],row['wrong_observed'],row['absent_digit'],row['outside_catalog']),(216,36,36,0))
        value = summary_fixture();row = value['seed_results'][0]['support']['original4'];row['absent_digit'] -= 1;row['outside_catalog'] += 1
        s.check_summary(value)
    def science_fixture(self):
        traces,records,states = [],[],[]
        for seed,arm in s.identities():
            state = {'synthetic_state':torch.tensor([float(seed),float(arm == 'mixed45')],dtype=torch.float64)};states.append(state)
            trace = {key:'paired' for key in ('initial_sha256','core_initial_sha256','logical_training_sha256','schedule_sha256',
                'mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')}
            trace.update(seed=seed,arm=arm,nonpadding_token_presentations=s.TRAIN_TOKENS[arm],training_input_sha256=arm,
                actual_training_stream_sha256=arm,length_mask_sha256=arm,final_sha256=self.p.state_hash(state));traces.append(trace)
            raw = tree_copy(self.raw)
            if arm == 'original5':
                views = raw['original']['4']['HOLDOUT']['shared_suffix'];views['normal'] = views['normal'].clone()
                row = self.data['HOLDOUT'][0];views['normal'][0].fill_(-4.)
                views['normal'][0,48+row['values'][1-row['entities'].index(row['query'])]] = 4.
            records.append(dict(seed=seed,arm=arm,state_sha256=self.p.state_hash(state),evaluation_policy='native_before',
                raw={mode:tree_copy(raw) for mode in ('evaluation','replay')},
                receipts={mode:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for mode in ('evaluation','replay')}))
        return traces,records,states
    def analyze_fixture(self,items):return s.analyze(*items,self.data,self.cx,self.tables,self.y)
    def test_29_real_scorers_and_raw_comparisons_reproduce_positive_gate(self):
        with patch.object(s,'check_trace'),self.x.guarded.no_neural():metrics,value = self.analyze_fixture(self.science_fixture())
        self.assertEqual(len(metrics),10);self.assertTrue(value['candidate_gate']);self.assertEqual(value['eligible_seed_count'],5)
        for row in value['paired_comparisons']:
            self.assertEqual((row['four_answer_gain'],row['four_pair_gain']),(1,1));self.assertEqual(row['six_answer_gain'],0)
    def test_30_saved_replay_drift_rejected_before_gate(self):
        items = self.science_fixture();tree = items[1][0]['raw']['replay']['interior']['HOLDOUT']['balanced']
        tree['normal'] = tree['normal'].clone();tree['normal'][0,0] += 1.
        with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
    def test_31_state_pairing_and_actual_intervention_are_bound(self):
        for kind in ('state','pair','stream','mask','recipe'):
            items = self.science_fixture()
            if kind == 'state':items[1][0]['state_sha256'] = '0'*64
            elif kind == 'pair':items[0][1]['logical_training_sha256'] = 'changed'
            else:
                key = {'stream':'actual_training_stream_sha256','mask':'length_mask_sha256','recipe':'training_input_sha256'}[kind]
                items[0][1][key] = items[0][0][key]
            with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
    def test_32_nonfinite_incomplete_and_reordered_measurements_rejected(self):
        items = self.science_fixture();tree = items[1][0]['raw']['evaluation']['interior']['TRAIN']['balanced']
        tree['normal'] = tree['normal'].clone();tree['normal'][0,0] = float('nan')
        with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
        for reverse in (False,True):
            items = self.science_fixture()
            if reverse:items[1].reverse()
            else:items[1].pop()
            with patch.object(s,'check_trace'),self.assertRaises(ValueError):self.analyze_fixture(items)
    def test_33_checkpoint_schema_and_complete_ordered_cohort(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'models.pt';value = dict(schema='fold-c342-trained-models-v1',identities=[list(z) for z in s.identities()],states=[{}]*10)
            torch.save(value,path);self.assertEqual(len(s.load_states(path)),10);value['identities'].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):s.load_states(path)
            value['identities'].reverse();value['schema'] = 'fold-c340-trained-models-v1';torch.save(value,path)
            with self.assertRaises(ValueError):s.load_states(path)
    def test_34_production_run_finishes_all_fitting_before_any_evaluation(self):
        calls = [];proxy = NS(**{k:getattr(self.p,k) for k in ('state_hash','source')})
        proxy.load_data = lambda *a:(self.data,self.old,self.new)
        proxy.readouts = lambda:NS(measure=lambda *a:(calls.append('eval') or ({},{})))
        def train(seed,arm,model,tables,y,*args):
            calls.append('train');self.assertIs(tables,self.tables);self.assertTrue(torch.equal(y,self.y))
            return dict(seed=seed,arm=arm),model.state_dict()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'previous',return_value=proxy),patch.object(s,'prepared',return_value=(self.tables,self.y)),\
             patch.object(s,'make_pair',side_effect=lambda *a:{k:TokenToy() for k in s.ARMS}),patch.object(s,'make_model',side_effect=lambda *a:TokenToy()),\
             patch.object(s,'train_one',side_effect=train),patch.object(s,'analyze',return_value=({},summary_fixture())),\
             patch.object(self.p.source().base(),'check_dependencies'),self.quiet():
            value = s.run_training(Path(tmp),Path(tmp),self.cx,ROOT,{},read)
            self.assertEqual(calls,['train']*10+['eval']*20);self.assertEqual(set(p.name for p in Path(tmp).iterdir()),set(s.OUTPUTS))
            self.assertTrue(value['candidate_gate'])
    def saved_fixture(self,root):
        data_out,out = root/'data',root/'science';data_out.mkdir();out.mkdir();self.write_data(data_out)
        items = self.science_fixture();metrics,value = self.analyze_fixture(items)
        torch.save(dict(schema='fold-c342-trained-models-v1',identities=[list(z) for z in s.identities()],states=items[2]),out/'trained-models.pt')
        torch.save(dict(schema='fold-c342-evaluations-v1',records=items[1]),out/'evaluations.pt')
        for name,item in (('experiment-plan.json',s.manifest()),('training-traces.json',items[0]),('measurements.json',metrics),('validation-summary.json',value)):
            (out/name).write_bytes(s.blob(item))
        return data_out,out,value
    def test_35_saved_reconstruction_uses_real_scorers_without_neural_calls(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'check_trace'):
            data_out,out,value = self.saved_fixture(Path(tmp))
            with self.x.guarded.no_neural():
                self.assertEqual(s.blob(s.semantic_recheck(out,data_out,self.cx,read)),s.blob(value))
    def test_36_reconstruction_rejects_resealed_score_and_summary_changes(self):
        for name in ('measurements.json','validation-summary.json','experiment-plan.json'):
            with tempfile.TemporaryDirectory() as tmp,patch.object(s,'check_trace'):
                data_out,out,_ = self.saved_fixture(Path(tmp));(out/name).write_bytes(s.blob({'changed':True}))
                with self.assertRaises(ValueError):s.semantic_recheck(out,data_out,self.cx,read)
    def test_37_native_preflight_uses_actual_canonical_tokens_and_backprop(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp);self.write_data(folder)
            with patch.object(self.p.source().base(),'check_dependencies'),self.quiet():s.native_preflight(folder,self.cx,ROOT,{},read)
    def test_38_allocation_failure_prevents_preflight_model_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp);self.write_data(folder)
            with patch.object(s,'length_mask',side_effect=ValueError('allocator failure')),patch.object(s,'make_model') as model,\
                 self.assertRaisesRegex(ValueError,'allocator failure'):
                s.native_preflight(folder,self.cx,ROOT,{},read)
            model.assert_not_called()
    def test_39_canonical_source_tamper_and_both_bank_leak_rejected(self):
        bad = copy.deepcopy(self.old);bad['5']['TRAIN']['repeat'][0]['target'] += 1
        with self.assertRaises(ValueError):s.prepared(self.data,bad,self.new,self.cx)
        bad = tree_copy(self.tables);key = (3,'repeat');bad['original4']['original'][key] = bad['original4']['original'][key].clone()
        bad['original4']['original'][key][0,1] += 1
        with self.assertRaises(ValueError):s.reference().validate_tables(bad,self.y)
        s.reference().validate_seal();self.p.validate_seal();self.p.source().curriculum().validate_seal()
    def test_40_nonfinite_native_training_logits_abort_before_update(self):
        model = TokenToy();f = self.toy;event = self.events[:2];family = self.family[:2]
        selected = torch.zeros((4,24),dtype=torch.int64)
        before = self.p.state_hash(model.state_dict())
        with patch.object(s,'previous',return_value=f.p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),\
             patch.object(model,'forward',return_value=torch.full((48,256),float('nan'),dtype=torch.float64)),\
             self.assertRaisesRegex(ValueError,'toy logits'):
            s.optimize(model,'original5',self.tables,self.y,event,family,selected,f.x)
        self.assertEqual(self.p.state_hash(model.state_dict()),before)


if __name__ == '__main__':unittest.main()
