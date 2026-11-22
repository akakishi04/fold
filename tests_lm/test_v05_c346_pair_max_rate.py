"""C346 software checks: canonical streams/real scorers and explicitly synthetic fits."""
from __future__ import annotations
from collections import Counter
import contextlib
import copy
import inspect
import io
import itertools
import json
import math
from pathlib import Path
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c346_pair_max_rate as s
from tests_lm import test_v05_c340_length5_training as old_tests

ROOT = Path(__file__).resolve().parents[1]
fixtures = old_tests.fixtures
TokenToy = old_tests.TokenToy
tree_copy = old_tests.tree_copy


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def scalar_contrast(split, answer=0, pair=0):
    """Arithmetic-only gate fixture; it does not claim a measured model result."""
    n = 576 if split == 'TRAIN' else 288; m = n//2
    return dict(answers=n,query_pairs=m,control_correct=n-4,candidate_correct=n-4+answer,
        control_both_correct=m-4,candidate_both_correct=m-4+pair,
        rescued=max(answer,0),regressed=max(-answer,0),pair_rescued=max(pair,0),pair_regressed=max(-pair,0),
        answer_gain=answer,query_pair_gain=pair)


def scalar_pairs():
    return [dict(seed=seed,control_arm=control,candidate_arm=s.CANDIDATE,candidate_full_pass=True,
        normal_by_domain={domain:{split:scalar_contrast(split,int(domain == 'interior4'),int(domain == 'interior4'))
            for split in s.SPLITS} for domain in s.DOMAINS}) for seed,control in itertools.product(s.SEEDS,s.CONTROLS)]


class C346ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.p = s.previous(); cls.cx = cls.p.source().base().context(); cls.x = cls.cx[-1]
        cls.data = cls.x.c.p267.dataset(); cls.old = cls.x.parent.prompt_dataset(cls.data,cls.x.p313)
        cls.new = cls.cx[2].new_prompts(cls.data); cls.tables,cls.y = s.prepared(cls.data,cls.old,cls.new,cls.cx)
        cls.events,cls.family = s.schedule(s.SEEDS[0],cls.data['TRAIN'],cls.x)
        cls.selected = s.length_mask(cls.events,cls.family)
        cls.toy = fixtures.toy_environment(); cls.toy.p.state_hash = cls.p.state_hash
        cls.toy.p.source = lambda:NS(curriculum=lambda:cls.p.source().curriculum(),base=lambda:NS(check_dependencies=lambda *a:None))
        cls.toy.x.parent = NS(plan_for_order=lambda *a:cls.events)
        cls.toy.x.c.p267.dataset = lambda:cls.data
        def groups(model,policy):
            assert policy == 'core_slow'
            core = list(model.backbone.core.parameters()); ids = {id(p) for p in core}
            return [dict(params=[p for p in model.parameters() if id(p) not in ids],lr=.005),dict(params=core,lr=.0005)]
        cls.toy.x.policy.parameter_groups = groups
        cls.positive_summary = None
        cls.traces,cls.states,cls.models = {},{},{}
        # Fixed, always-created software fixtures; these small models are not native
        # benchmark results and are never selected according to test outcomes.
        with patch.object(s,'previous',return_value=cls.toy.p),contextlib.redirect_stdout(io.StringIO()):
            for arm in s.ARMS:
                model = TokenToy(); cls.models[arm] = model
                cls.traces[arm],cls.states[arm] = s.train_one(s.SEEDS[0],arm,model,cls.tables,cls.y,
                    cls.data['TRAIN'],(cls.toy.x,),ROOT,{})
                s.check_trace(cls.traces[arm],cls.data['TRAIN'],cls.toy.x,cls.tables,cls.y)
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
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads)
    def quiet(self):
        return contextlib.redirect_stdout(io.StringIO())
    def trace(self,arm=s.CANDIDATE):
        return copy.deepcopy(self.traces[arm])
    def check_trace(self,value,tables=None):
        with patch.object(s,'previous',return_value=self.toy.p):
            s.check_trace(value,self.data['TRAIN'],self.toy.x,self.tables if tables is None else tables,self.y)
    def write_data(self,folder):
        for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):
            (folder/name).write_bytes(s.blob(value))
    def science_fixture(self):
        """Invented saved logits/states; all real saved scorers and terminal arithmetic remain active."""
        traces,records,states = [],[],[]
        for seed,arm in s.identities():
            state = {'synthetic_state':torch.tensor([float(seed),float(s.ARMS.index(arm))],dtype=torch.float64)}; states.append(state)
            trace = {key:'paired' for key in ('initial_sha256','core_initial_sha256','logical_training_sha256','schedule_sha256',
                'mask_sha256','family_exposure_per_cycle','actual_exposure_per_cycle','event_indices',
                'training_input_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256')}
            trace.update(seed=seed,arm=arm,nonpadding_token_presentations=3168000,final_sha256=self.p.state_hash(state),
                loss_history=[dict(mean_ce=1.,pair_max=1.5,selected=1. if arm == 'mean_ce' else 1.5)],
                optimizer_group_lrs=[list(s.RATES[arm])]*s.STEPS,steps=2400,optimizer_steps=2400,optimizer_creations=1,
                policy_receipt=dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400),
                measured_training_work=dict(calls=2400,rows=115200,core_calls=9600)); traces.append(trace)
            raw = tree_copy(self.raw)
            if arm in s.CONTROLS:
                for split in s.SPLITS:
                    views = raw['interior'][split]['balanced']; views['normal'] = views['normal'].clone()
                    row = self.data[split][0]; views['normal'][0].fill_(-4.)
                    views['normal'][0,48+row['values'][1-row['entities'].index(row['query'])]] = 4.
            records.append(dict(seed=seed,arm=arm,state_sha256=self.p.state_hash(state),evaluation_policy='native_before',
                raw={mode:tree_copy(raw) for mode in ('evaluation','replay')},
                receipts={mode:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for mode in ('evaluation','replay')}))
        return traces,records,states
    def analyze_fixture(self,items):
        return s.analyze(*items,self.data,self.cx,self.tables,self.y)
    def synthetic_summary(self):
        if type(self).positive_summary is None:
            with patch.object(s,'check_trace'),self.x.guarded.no_neural():
                type(self).positive_summary = self.analyze_fixture(self.science_fixture())[1]
        return copy.deepcopy(type(self).positive_summary)
    def saved_fixture(self,root):
        data_out,out = root/'data',root/'science'; data_out.mkdir(); out.mkdir(); self.write_data(data_out)
        items = self.science_fixture(); metrics,value = self.analyze_fixture(items)
        torch.save(dict(schema='fold-c346-trained-models-v1',identities=[list(z) for z in s.identities()],states=items[2]),out/'trained-models.pt')
        torch.save(dict(schema='fold-c346-evaluations-v1',records=items[1]),out/'evaluations.pt')
        for name,item in (('experiment-plan.json',s.manifest()),('training-traces.json',items[0]),('measurements.json',metrics),('validation-summary.json',value)):
            (out/name).write_bytes(s.blob(item))
        return data_out,out,value
    def mixed_errors(self):
        raw = tree_copy(self.raw); views = raw['interior']['TRAIN']['balanced']; views['normal'] = views['normal'].clone()
        z = views['normal']; pairs = self.p.source().base().query_pairs(self.data['TRAIN'])
        for number in range(1,6):
            a,b = pairs[number]; ta,tb = [self.data['TRAIN'][i]['target'] for i in (a,b)]
            absent = min(set(range(48,52))-{ta,tb})
            predictions = {1:(ta,ta),2:(tb,ta),3:(absent,absent),4:(7,7),5:(ta,7)}[number]
            for i,pred in zip((a,b),predictions,strict=True): z[i].fill_(-4.); z[i,pred] = 4.
        return raw

    def test_01_manifest_seal_cohort_budget_and_fixed_estimand(self):
        s.validate_seal(); self.assertEqual(s.SEEDS,tuple(range(346001,346006))); self.assertEqual(s.ORDERS,tuple(range(346101,346106)))
        self.assertEqual(s.ARMS,('mean_ce','pair_max','pair_max_half_rate')); self.assertEqual(len(s.identities()),15)
        self.assertEqual((s.STEPS,s.WORK['train_steps'],s.WORK['model_forward_calls']),(2400,36000,41130))
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.OWN_TESTS,s.FULL_TESTS,s.MODULES),(944,9177,74,6652,243))
        self.assertEqual(s.manifest()['contrasts'],120); self.assertEqual(len(s.manifest()['strict_endpoints']),4)
        self.assertEqual(s.manifest()['acceptance_base'],'f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2')
        self.assertEqual(s.manifest()['rates'],{'mean_ce':[.005,.0005],'pair_max':[.005,.0005],'pair_max_half_rate':[.0025,.00025]})
    def test_02_canonical_nonbinary_train_split_and_immutable_banks(self):
        self.assertEqual(self.data,fixtures.data_fixture()); self.assertEqual(set(self.y.tolist()),{48,49,50,51})
        self.assertEqual((len(self.data['TRAIN']),len(self.data['HOLDOUT'])),(192,96))
        banks,y = s.reference().prepared(self.data,self.old,self.new,self.cx)
        self.assertTrue(torch.equal(y,self.y))
        self.assertEqual(s.training_fingerprint(banks,y,self.events,self.family,self.selected),
                         s.training_fingerprint(self.tables,self.y,self.events,self.family,self.selected))
        self.assertFalse({r['id'] for r in self.data['TRAIN']}&{r['id'] for r in self.data['HOLDOUT']})
    def test_03_native_triple_has_equal_independent_fresh_weights(self):
        models = s.make_models(s.SEEDS[0],self.x); a,b,c = models.values()
        self.assertEqual(len({self.p.state_hash(m.state_dict()) for m in models.values()}),1)
        for left,right in itertools.combinations(models.values(),2):
            self.assertFalse({v.data_ptr() for v in left.parameters()}&{v.data_ptr() for v in right.parameters()})
        self.assertEqual(sum(v.numel() for v in a.parameters()),14256)
        self.assertTrue(all(v.requires_grad and v.dtype == torch.float64 for v in a.parameters()))
        with torch.no_grad(): next(a.parameters()).add_(.1)
        self.assertNotEqual(self.p.state_hash(a.state_dict()),self.p.state_hash(b.state_dict()))
        self.assertEqual(self.p.state_hash(b.state_dict()),self.p.state_hash(c.state_dict()))
    def test_04_all_five_schedules_preserve_events_family_and_pair_identity(self):
        for seed,order in zip(s.SEEDS,s.ORDERS,strict=True):
            events,family = s.schedule(seed,self.data['TRAIN'],self.x)
            expected = self.x.parent.plan_for_order(order,'two_to_four',self.data['TRAIN'],self.x.p312,self.x.pairs)
            self.assertTrue(torch.equal(events,expected)); self.assertTrue(torch.equal(family,self.p.source().curriculum().family_mask(events,'batch4')))
            s.validate_training_pairs(self.data['TRAIN'],self.y,events,self.x)
        with self.assertRaises(ValueError): s.schedule(342001,self.data['TRAIN'],self.x)
    def test_05_all_allocations_have_fixed_per_cycle_exposure_and_complement(self):
        for seed in s.SEEDS:
            events,family = s.schedule(seed,self.data['TRAIN'],self.x); selected = s.length_mask(events,family)
            self.assertTrue(torch.equal(selected[:1200]+selected[1200:],((events[:,:,0] == 4)&(family == 0)).long()))
            for cycle in s.actual_exposure(events,family,selected):
                for domain,n in s.manifest()['per_cycle_exposure'].items(): self.assertEqual(cycle[domain],[n]*192)
    def test_06_actual_selector_matches_immutable_mixed45_in_every_update(self):
        before = s.training_fingerprint(self.tables,self.y,self.events,self.family,self.selected)
        for step in range(2400):
            args = (self.tables,self.events[step%1200],self.family[step%1200],self.selected[step])
            z,ids = s.select_tokens(*args); expected,rows = s.reference().select_tokens(*args)
            self.assertTrue(torch.equal(z,expected)); self.assertTrue(torch.equal(ids,rows))
            self.assertTrue(torch.equal(ids,self.events[step%1200,:,2:].reshape(-1)))
        self.assertEqual(s.training_fingerprint(self.tables,self.y,self.events,self.family,self.selected),before)
    def test_07_paired_streams_are_identical_and_label_order_is_bound(self):
        count,stream = s.input_accounting(self.tables,self.y,self.events,self.family,self.selected)
        self.assertEqual(count,3168000)
        for arm in s.ARMS:
            self.assertEqual(self.traces[arm]['actual_training_stream_sha256'],stream)
            self.assertEqual(self.traces[arm]['nonpadding_token_presentations'],count)
        labels = self.y.clone(); labels[0] = 48+(int(labels[0])-47)%4
        altered = s.input_accounting(self.tables,labels,self.events,self.family,self.selected)
        self.assertEqual(altered[0],count); self.assertNotEqual(altered[1],stream)
    def test_08_corrupted_metadata_prevents_optimizer_creation(self):
        for kind in ('rows','targets','event'):
            rows = copy.deepcopy(self.data['TRAIN']); y = self.y.clone(); events = self.events.clone()
            if kind == 'rows': rows[0]['values'].reverse()
            elif kind == 'targets': y[0] = 7
            else: events[0,0,3] = events[0,0,2]
            with patch.object(s,'previous',return_value=self.toy.p),patch.object(s,'optimizer_for') as opt,self.assertRaises(ValueError):
                s.optimize(TokenToy(),'pair_max',self.tables,y,events,self.family,self.selected,rows,self.toy.x)
            opt.assert_not_called()
    def test_09_actual_selected_pair_order_is_checked_before_forward(self):
        model = TokenToy(); selector = s.select_tokens
        def changed(*args):
            z,ids = selector(*args); ids = ids.clone(); ids[:2] = ids[:2].flip(0); return z,ids
        with patch.object(s,'previous',return_value=self.toy.p),patch.object(s,'select_tokens',side_effect=changed),\
             patch.object(model,'forward',wraps=model.forward) as forward,self.assertRaisesRegex(ValueError,'actual paired'):
            s.optimize(model,'pair_max',self.tables,self.y,self.events,self.family,self.selected,self.data['TRAIN'],self.toy.x)
        forward.assert_not_called()
    def independent_first_updates(self,arm):
        expected = TokenToy(); actual = TokenToy(); core = list(expected.backbone.core.parameters()); ids = {id(p) for p in core}
        rates = (.0025,.00025) if arm == 'pair_max_half_rate' else (.005,.0005)
        refopt = torch.optim.AdamW([dict(params=[p for p in expected.parameters() if id(p) not in ids],lr=rates[0]),
            dict(params=core,lr=rates[1])],lr=rates[0],betas=(.9,.999),eps=1e-8,weight_decay=0.)
        hashes = []
        for step in range(4):
            tokens,ids = s.select_tokens(self.tables,self.events[step],self.family[step],self.selected[step]); refopt.zero_grad(set_to_none=True)
            logits = expected(tokens,torch.zeros(48,dtype=torch.int64))
            if arm == 'mean_ce': loss = F.cross_entropy(logits,self.y[ids])
            else:
                losses = F.cross_entropy(logits,self.y[ids],reduction='none').reshape(24,2)
                loss = torch.maximum(losses[:,0],losses[:,1]).mean()
            loss.backward(); torch.nn.utils.clip_grad_norm_(list(expected.parameters()),1.,error_if_nonfinite=True); refopt.step()
            hashes.append(self.p.state_hash(expected.state_dict()))
        class ProbeComplete(Exception): pass
        checked = []; optimizer = s.optimizer_for
        def monitored(model,chosen,x):
            self.assertEqual(chosen,arm); opt = optimizer(model,chosen,x); step = opt.step
            def advance(*args,**kwargs):
                value = step(*args,**kwargs); self.assertEqual(self.p.state_hash(model.state_dict()),hashes[len(checked)])
                checked.append(True)
                if len(checked) == 4: raise ProbeComplete()
                return value
            opt.step = advance; return opt
        with patch.object(s,'previous',return_value=self.toy.p),patch.object(s,'optimizer_for',side_effect=monitored),self.assertRaises(ProbeComplete):
            s.optimize(actual,arm,self.tables,self.y,self.events,self.family,self.selected,self.data['TRAIN'],self.toy.x)
        self.assertEqual(len(checked),4)
    def test_10_control_updates_match_independent_ordinary_ce_reference(self):
        self.independent_first_updates('mean_ce')
    def test_11_default_pairmax_updates_match_independent_pair_max_reference(self):
        self.independent_first_updates('pair_max')
    def test_12_three_full_toy_fits_use_registered_losses_and_identical_inputs(self):
        for arm in s.ARMS:
            t = self.traces[arm]; self.assertEqual(len(t['loss_history']),2400)
            self.assertTrue(all(row['selected'] == row['mean_ce' if arm == 'mean_ce' else 'pair_max'] for row in t['loss_history']))
            self.assertEqual(t['checked_training_pairs'],57600)
            self.assertEqual(t['policy_receipt'],dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400))
        a = self.traces[s.ARMS[0]]
        for arm in s.ARMS[1:]:
            b = self.traces[arm]
            for key in ('initial_sha256','training_input_sha256','logical_training_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256'):
                self.assertEqual(a[key],b[key])
            for key in ('mean_ce','pair_max'): self.assertEqual(a['loss_history'][0][key],b['loss_history'][0][key])
        self.assertEqual(len({t['final_sha256'] for t in self.traces.values()}),3)
    def test_13_continuous_optimizer_and_deep_snapshots_survive_both_cycles(self):
        for arm in s.ARMS:
            trace,state,model = self.traces[arm],self.states[arm],self.models[arm]
            self.assertEqual(trace['boundary'],trace['continuation']); self.assertEqual(trace['optimizer_creations'],1)
            self.assertEqual(trace['event_indices'],list(range(1200))*2); self.assertEqual(trace['intermediate_evaluations'],0)
            self.assertEqual(trace['optimizer_group_lrs'],[list(s.RATES[arm])]*2400)
            self.assertTrue(all(v.data_ptr() != model.state_dict()[k].data_ptr() for k,v in state.items()))
            copied = copy.deepcopy(model); before = self.p.state_hash(state)
            with torch.no_grad(): next(copied.parameters()).add_(1.)
            self.assertEqual(self.p.state_hash(state),before)
    def test_14_trace_rejects_wrong_objective_and_nonfinite_loss_or_gradient_norm(self):
        for kind in ('selected','bound','nan','negative','norm','length'):
            value = self.trace(); row = value['loss_history'][0]
            if kind == 'selected': row['selected'] = row['mean_ce']-.1
            elif kind == 'bound': row['pair_max'] = row['selected'] = 3*row['mean_ce']
            elif kind == 'nan': row['mean_ce'] = float('nan')
            elif kind == 'negative': row['mean_ce'] = -.1
            elif kind == 'norm': value['preclip_norm_history'][0] = float('inf')
            else: value['loss_history'].pop()
            with self.assertRaises(ValueError): self.check_trace(value)
    def test_15_trace_rejects_recipe_pair_stream_and_exposure_tampering(self):
        for key,value in (('pair_metadata_sha256','a'*64),('checked_training_pairs',57599),('actual_training_stream_sha256','b'*64),
                          ('training_input_sha256','c'*64),('nonpadding_token_presentations',3225600),('length_mask_sha256','d'*64)):
            trace = self.trace(); trace[key] = value
            with self.assertRaises(ValueError): self.check_trace(trace)
        trace = self.trace(); trace['actual_exposure_per_cycle'][0]['original4'][0] = 24
        with self.assertRaises(ValueError): self.check_trace(trace)
    def test_16_trace_rejects_reset_selection_rate_change_and_readout_change(self):
        for key,value in (('optimizer_creations',2),('intermediate_evaluations',1),('length_policy','original5'),('readout_mode','first_mean')):
            trace = self.trace(); trace[key] = value
            with self.assertRaises(ValueError): self.check_trace(trace)
        for key in ('continuation','optimizer_group_lrs'):
            trace = self.trace()
            if key == 'continuation': trace[key]['optimizer'] = 'a'*64
            else: trace[key][1200][0] = .01
            with self.assertRaises(ValueError): self.check_trace(trace)
    def test_17_input_source_and_canonical_bank_tampering_are_rejected(self):
        bad = copy.deepcopy(self.old); bad['5']['TRAIN']['repeat'][0]['target'] += 1
        with self.assertRaises(ValueError): s.prepared(self.data,bad,self.new,self.cx)
        banks = tree_copy(self.tables); key = (4,'repeat')
        banks['original4']['original'][key] = banks['original4']['original'][key].clone(); banks['original4']['original'][key][0,1] += 1
        with self.assertRaises(ValueError): self.check_trace(self.trace(),banks)
        # C340's table validator checks schema and substitution boundaries; the
        # canonical length4 token change above is instead bound by the trace.
        banks = tree_copy(self.tables); key = (3,'repeat')
        banks['original4']['original'][key] = banks['original4']['original'][key].clone(); banks['original4']['original'][key][0,1] += 1
        with self.assertRaises(ValueError): s.reference().reference().validate_tables(banks,self.y)
    def test_18_nonfinite_actual_training_logits_abort_without_update(self):
        model = TokenToy(); before = self.p.state_hash(model.state_dict())
        with patch.object(s,'previous',return_value=self.toy.p),\
             patch.object(model,'forward',return_value=torch.full((48,256),float('nan'),dtype=torch.float64)),self.assertRaisesRegex(ValueError,'toy logits'):
            s.optimize(model,'pair_max',self.tables,self.y,self.events,self.family,self.selected,self.data['TRAIN'],self.toy.x)
        self.assertEqual(self.p.state_hash(model.state_dict()),before)
    def test_19_native_preflight_checks_actual_pairs_three_rates_and_backward(self):
        count = [0,0,0]; maker = s.make_model; optimizer = s.optimizer_for
        def create(*args):
            model = maker(*args)
            def forward(m,inputs,output): count[0] += 1; count[1] += len(inputs[0])
            def backward(grad): count[2] += 1
            model.register_forward_hook(forward); model.read.query.weight.register_hook(backward); return model
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp); self.write_data(folder)
            with patch.object(self.p.source().base(),'check_dependencies'),patch.object(s,'make_model',side_effect=create),                 patch.object(s,'optimizer_for',wraps=optimizer) as optimizers,patch.object(torch.optim.AdamW,'step') as step,self.quiet():
                self.assertEqual(s.native_preflight(folder,self.cx,ROOT,{},read),s.identities())
            self.assertEqual([call.args[1] for call in optimizers.call_args_list],list(s.ARMS)); step.assert_not_called()
            self.assertEqual(count,[24,96,12])
    def test_20_schedule_failure_prevents_native_preflight_model_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp); self.write_data(folder)
            with patch.object(s,'length_mask',side_effect=ValueError('allocator failure')),patch.object(s,'make_model') as model,\
                 self.assertRaisesRegex(ValueError,'allocator failure'):
                s.native_preflight(folder,self.cx,ROOT,{},read)
            model.assert_not_called()
    def test_21_real_saved_scorers_produce_complete_positive_two_control_gate(self):
        value = self.synthetic_summary(); s.check_summary(value)
        self.assertTrue(value['candidate_gate']); self.assertEqual(value['eligible_seed_count'],5)
        self.assertEqual(value['strict_interior_gains'],{sp:dict(answer_gain=5,query_pair_gain=5) for sp in s.SPLITS})
        self.assertEqual(sum(len(v) for row in value['paired_comparisons'] for v in row['normal_by_domain'].values()),120)
        components = value['gate_components']
        self.assertTrue(all(components[k] for k in ('all_candidates_full_pass','nonnegative_vs_pair_max','nonnegative_vs_mean_ce','strict_interior_vs_pair_max')))
        self.assertEqual(components['nonnegative_counts'],{control:dict(passed=120,total=120) for control in s.CONTROLS})
        self.assertFalse(value['strict_interior_ceiling'])
    def test_22_each_seed_control_domain_split_endpoint_must_be_nonnegative(self):
        for index,control,domain,split,criterion in itertools.product(range(5),s.CONTROLS,s.DOMAINS,s.SPLITS,('answer_gain','query_pair_gain')):
            pairs = scalar_pairs(); row = next(r for r in pairs if (r['seed'],r['control_arm']) == (s.SEEDS[index],control))
            row['normal_by_domain'][domain][split] = scalar_contrast(split,-1 if criterion == 'answer_gain' else 0,-1 if criterion == 'query_pair_gain' else 0)
            gate,eligible,_,components,_ = s.fixed_gate(pairs)
            self.assertFalse(gate); self.assertFalse(eligible[index]); self.assertEqual(sum(eligible),4)
            self.assertFalse(components['nonnegative_vs_'+control]); self.assertEqual(components['nonnegative_counts'][control]['passed'],119)
    def test_23_each_of_four_primary_strict_endpoints_rejects_ties(self):
        for split,criterion in itertools.product(s.SPLITS,('answer_gain','query_pair_gain')):
            pairs = scalar_pairs()
            for row in pairs:
                if row['control_arm'] == 'pair_max':
                    row['normal_by_domain']['interior4'][split] = scalar_contrast(split,0 if criterion == 'answer_gain' else 1,0 if criterion == 'query_pair_gain' else 1)
            gate,eligible,strict,components,_ = s.fixed_gate(pairs)
            self.assertFalse(gate); self.assertEqual(eligible,[True]*5); self.assertEqual(strict[split][criterion],0)
            self.assertFalse(components['strict_interior_vs_pair_max']); self.assertTrue(components['nonnegative_vs_mean_ce'])
    def test_24_gate_requires_all_five_full_candidates_and_exact_cohort(self):
        for seed in s.SEEDS:
            pairs = scalar_pairs()
            for row in pairs:
                if row['seed'] == seed: row['candidate_full_pass'] = False
            gate,eligible,_,components,_ = s.fixed_gate(pairs)
            self.assertFalse(gate); self.assertEqual(sum(eligible),4); self.assertEqual(components['candidate_full_pass_count'],4)
        for kind in ('missing','reverse','bool','split','candidate','control','inconsistent'):
            pairs = scalar_pairs()
            if kind == 'missing': pairs.pop()
            elif kind == 'reverse': pairs.reverse()
            elif kind == 'bool': pairs[0]['candidate_full_pass'] = 1
            elif kind == 'split': del pairs[0]['normal_by_domain']['original6']['TRAIN']
            elif kind == 'candidate': pairs[0]['candidate_arm'] = 'pair_max'
            elif kind == 'control': pairs[0]['control_arm'] = 'mean_ce'
            else: pairs[0]['candidate_full_pass'] = False
            with self.assertRaises(ValueError): s.fixed_gate(pairs)
    def test_25_normal_report_separates_support_pair_errors_and_collapse(self):
        value = s.normal_report(self.mixed_errors(),self.data)['interior4']['TRAIN']
        expected = dict(answers=576,query_pairs=288,correct=568,wrong_observed=3,absent_digit=2,outside_catalog=3,
            both_query_correct=283,one_correct_pairs=2,zero_correct_pairs=3,collapsed_pairs=3)
        self.assertEqual({k:value[k] for k in expected},expected); s.check_normal_report(value,'interior4','TRAIN')
    def test_26_paired_rescue_regression_direction_is_asymmetric_and_complete(self):
        control = self.mixed_errors(); candidate = tree_copy(self.raw)
        views = candidate['interior']['TRAIN']['balanced']; views['normal'] = views['normal'].clone()
        a,b = self.p.source().base().query_pairs(self.data['TRAIN'])[6]
        for i,j in ((a,b),(b,a)):
            views['normal'][i].fill_(-4.); views['normal'][i,self.data['TRAIN'][j]['target']] = 4.
        forward = s.compare_normal(control,candidate,self.data); reverse = s.compare_normal(candidate,control,self.data)
        z = forward['interior4']['TRAIN']
        self.assertEqual([z[k] for k in ('rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')],[8,2,5,1,6,4])
        r = reverse['interior4']['TRAIN']; self.assertEqual([r[k] for k in ('rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')],[2,8,1,5,-6,-4])
        for domain,split in itertools.product(s.DOMAINS,s.SPLITS):
            s.contrast_check(forward[domain][split],split)
            if (domain,split) != ('interior4','TRAIN'): self.assertEqual(forward[domain][split]['answer_gain'],0)
    def test_27_reported_exposure_distinguishes_known_values_from_fitted_prompts(self):
        report = s.normal_report(self.raw,self.data)
        for domain,split in itertools.product(s.DOMAINS,s.SPLITS):
            z = report[domain][split]; s.check_normal_report(z,domain,split)
            expected = s.manifest()['actual_per_row_exposure'][domain] if split == 'TRAIN' else 0
            self.assertEqual(z['domain_presentations_per_logical_row'],expected)
            self.assertIs(z['normal_prompt_seen_in_training'],expected > 0)
        self.assertFalse(report['original6']['TRAIN']['normal_prompt_seen_in_training'])
    def test_28_summary_binds_all_normal_counts_support_flags_and_endpoints(self):
        original = self.synthetic_summary()
        for kind in ('work','support','normal','exposure','endpoint','full','tokens','strict','extra'):
            value = copy.deepcopy(original); state = value['seed_results'][0]
            if kind == 'work': value['train_steps'] = True
            elif kind == 'support': state['support']['interior4']['correct'] -= 1
            elif kind == 'normal': state['normal_by_domain']['original2']['TRAIN']['collapsed_pairs'] = 1
            elif kind == 'exposure': state['normal_by_domain']['original6']['TRAIN']['normal_prompt_seen_in_training'] = True
            elif kind == 'endpoint': value['paired_comparisons'][0]['interior_train_answer_gain'] += 1
            elif kind == 'full': value['paired_comparisons'][0]['candidate_full_pass'] = False
            elif kind == 'tokens': state['training_nonpadding_tokens'] = 3225600
            elif kind == 'strict': value['strict_interior_gains']['TRAIN']['answer_gain'] = 6
            else: value['selected_best_seed'] = s.SEEDS[0]
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_29_contrast_conservation_feasibility_and_exact_integer_schema(self):
        for split in s.SPLITS:
            row = scalar_contrast(split,1,1); s.contrast_check(row,split)
            for kind in ('bool','count','gain','feasibility','extra'):
                bad = copy.deepcopy(row)
                if kind == 'bool': bad['answer_gain'] = True
                elif kind == 'count': bad['answers'] += 1
                elif kind == 'gain': bad['rescued'] += 1
                elif kind == 'feasibility':
                    bad['rescued'] = 5; bad['regressed'] = 4
                else: bad['unregistered'] = 0
                with self.assertRaises(ValueError): s.contrast_check(bad,split)
    def test_30_raw_replay_requires_exact_argmax_even_below_numeric_tolerance(self):
        items = self.science_fixture(); record = items[1][0]
        for mode,amount in (('evaluation',-2e-10),('replay',2e-10)):
            views = record['raw'][mode]['interior']['HOLDOUT']['balanced']; views['normal'] = views['normal'].clone()
            views['normal'][1,7] = 4.+amount
        with patch.object(s,'check_trace'),self.assertRaises(ValueError): self.analyze_fixture(items)
    def test_31_state_and_all_paired_condition_fingerprints_are_bound(self):
        for key in ('state','initial_sha256','logical_training_sha256','training_input_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256'):
            items = self.science_fixture()
            if key == 'state': items[1][0]['state_sha256'] = '0'*64
            else: items[0][1][key] = 'changed'
            with patch.object(s,'check_trace'),self.assertRaises(ValueError): self.analyze_fixture(items)
    def test_32_saved_raw_inventory_type_finiteness_and_detachment_are_checked(self):
        for kind in ('nan','dtype','grad','view','receipt'):
            items = self.science_fixture(); record = items[1][0]; views = record['raw']['evaluation']['interior']['TRAIN']['balanced']
            if kind == 'nan': views['normal'] = views['normal'].clone(); views['normal'][0,7] = float('nan')
            elif kind == 'dtype': views['normal'] = views['normal'].float()
            elif kind == 'grad': views['normal'] = views['normal'].clone().requires_grad_(True)
            elif kind == 'view': del views['query_blind']
            else: record['receipts']['evaluation']['calls'] = 170
            with patch.object(s,'check_trace'),self.assertRaises(ValueError): self.analyze_fixture(items)
    def test_33_archive_identity_order_and_full_cohort_are_required(self):
        for kind in ('missing','reverse','arm'):
            items = self.science_fixture()
            if kind == 'missing': items[1].pop()
            elif kind == 'reverse': items[1].reverse()
            else: items[1][0]['arm'] = 'mixed45'
            with patch.object(s,'check_trace'),self.assertRaises(ValueError): self.analyze_fixture(items)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'models.pt'; value = dict(schema='fold-c346-trained-models-v1',identities=[list(z) for z in s.identities()],states=[{}]*15)
            torch.save(value,path); self.assertEqual(len(s.load_states(path)),15)
            for kind in ('order','schema','count'):
                bad = copy.deepcopy(value)
                if kind == 'order': bad['identities'].reverse()
                elif kind == 'schema': bad['schema'] = 'fold-c342-trained-models-v1'
                else: bad['states'].pop()
                torch.save(bad,path)
                with self.assertRaises(ValueError): s.load_states(path)
    def test_34_production_run_finishes_all_fifteen_fits_before_thirty_evaluations(self):
        calls = []; loads = []; proxy = NS(**{k:getattr(self.p,k) for k in ('state_hash','source')})
        proxy.load_data = lambda *a:(self.data,self.old,self.new)
        class CountedToy(TokenToy):
            def load_state_dict(model,*args,**kwargs):
                loads.append(True); return super().load_state_dict(*args,**kwargs)
        def measure(model,mode,*args):
            self.assertEqual(mode,'native_before'); self.assertFalse(model.training)
            self.assertTrue(all(not v.requires_grad for v in model.parameters())); calls.append('eval'); return {},{}
        proxy.readouts = lambda:NS(measure=measure)
        def train(seed,arm,model,tables,y,*args):
            calls.append('train'); self.assertIs(tables,self.tables); self.assertTrue(torch.equal(y,self.y))
            return dict(seed=seed,arm=arm),{k:v.detach().clone() for k,v in model.state_dict().items()}
        value = self.synthetic_summary(); bundle_load = s.load_states; save = torch.save
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'previous',return_value=proxy),patch.object(s,'prepared',return_value=(self.tables,self.y)),             patch.object(s,'make_models',side_effect=lambda *a:{k:CountedToy() for k in s.ARMS}),patch.object(s,'make_model',side_effect=lambda *a:CountedToy()),             patch.object(s,'train_one',side_effect=train),patch.object(s,'analyze',return_value=({},value)),             patch.object(s,'load_states',wraps=bundle_load) as load,patch.object(torch,'save',wraps=save) as writer,             patch.object(self.p.source().base(),'check_dependencies'),self.quiet():
            actual = s.run_training(Path(tmp),Path(tmp),self.cx,ROOT,{},read)
            self.assertEqual(calls,['train']*15+['eval']*30); self.assertEqual(len(loads),30)
            self.assertEqual(load.call_count,1); self.assertEqual([call.args[0]['schema'] for call in writer.call_args_list],['fold-c346-trained-models-v1','fold-c346-evaluations-v1'])
            self.assertEqual(set(p.name for p in Path(tmp).iterdir()),set(s.OUTPUTS)); self.assertEqual(actual,value)
    def test_35_saved_semantic_reconstruction_uses_real_scorers_without_neural_calls(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'check_trace'):
            data_out,out,value = self.saved_fixture(Path(tmp))
            with self.x.guarded.no_neural(): self.assertEqual(s.blob(s.semantic_recheck(out,data_out,self.cx,read)),s.blob(value))
    def test_36_reconstruction_rejects_resealed_measurements_summary_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'check_trace'):
            data_out,out,_ = self.saved_fixture(Path(tmp))
            for name in ('measurements.json','validation-summary.json','experiment-plan.json'):
                path = out/name; saved = path.read_bytes(); path.write_bytes(s.blob({'changed':True}))
                with self.assertRaises(ValueError): s.semantic_recheck(out,data_out,self.cx,read)
                path.write_bytes(saved)
    def test_37_saved_recheck_dispatch_checks_archive_schema_and_canonical_source(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'check_trace'):
            data_out,out,_ = self.saved_fixture(Path(tmp)); path = out/'evaluations.pt'
            saved = torch.load(path,map_location='cpu',weights_only=True); bad = dict(saved); bad['schema'] = 'fold-c342-evaluations-v1'; torch.save(bad,path)
            with self.assertRaises(ValueError): s.semantic_recheck(out,data_out,self.cx,read)
            torch.save(saved,path); source = data_out/'dataset.json'; value = read(source); value['TRAIN'][0]['target'] = 7; source.write_bytes(s.blob(value))
            with self.assertRaises(ValueError): s.semantic_recheck(out,data_out,self.cx,read)
    def test_38_console_reports_all_states_both_controls_and_terminal_objectives(self):
        value = self.synthetic_summary(); lines = []
        with self.x.guarded.no_neural(): s.report_results(value,lambda name,row:lines.append((name,row)))
        self.assertEqual(Counter(name for name,_ in lines),{'C346 seed result':15,'C346 normal result':180,
            'C346 paired comparison':10,'C346 normal contrast':120,'C346 terminal objective':180,'C346 terminal contrast':120,
            'C346 strict interior gains':1,'C346 gate components':1,'C346 primary headroom':1,'C346 measured work':1})
        self.assertEqual({(z['seed'],z['arm'],z['domain'],z['split']) for name,z in lines if name == 'C346 normal result'},
            set(itertools.product(s.SEEDS,s.ARMS,s.DOMAINS,s.SPLITS)))
        self.assertEqual({(z['seed'],z['control_arm'],z['domain'],z['split']) for name,z in lines if name == 'C346 normal contrast'},
            set(itertools.product(s.SEEDS,s.CONTROLS,s.DOMAINS,s.SPLITS)))
    def test_39_helper_abis_and_immutable_source_seals_remain_registered(self):
        self.assertEqual(s.parent().__name__,'fold_lm.v05_benchmarks.model_c345_saved_objective_audit')
        self.assertEqual(s.prior().__name__,'fold_lm.v05_benchmarks.model_c344_pair_max_training')
        self.assertEqual(s.previous().__name__,'fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')
        self.assertEqual(s.reference().__name__,'fold_lm.v05_benchmarks.model_c342_mixed_length45_training')
        for helper in (s.parent(),s.prior(),s.previous(),s.reference(),s.reference().reference(),s.previous().source().curriculum()): helper.validate_seal()
        self.assertEqual(s.prior().SEEDS,tuple(range(344001,344006))); self.assertEqual(s.prior().ARMS,('mean_ce','pair_max'))
        self.assertEqual(s.prior().RATES,(.005,.0005))
        for name,n in (('native_preflight',5),('run_training',6),('semantic_recheck',4),('report_results',2)):
            self.assertEqual(len(inspect.signature(getattr(s,name)).parameters),n)
        self.assertEqual(set(inspect.signature(s.optimize).parameters),{'model','arm','tables','y','events','family','selected','rows','x'})
    def test_40_perfect_control_saturation_is_valid_negative_without_selection(self):
        items = self.science_fixture()
        for record in items[1]: record['raw'] = {mode:tree_copy(self.raw) for mode in ('evaluation','replay')}
        with patch.object(s,'check_trace'),self.x.guarded.no_neural(): _,value = self.analyze_fixture(items)
        s.check_summary(value); self.assertFalse(value['candidate_gate']); self.assertEqual(value['eligible_seed_count'],5)
        self.assertEqual(value['strict_interior_gains'],{sp:dict(answer_gain=0,query_pair_gain=0) for sp in s.SPLITS})
        self.assertEqual(value['strict_interior_headroom'],{sp:dict(answer_headroom=0,query_pair_headroom=0) for sp in s.SPLITS})
        self.assertTrue(value['strict_interior_ceiling']); self.assertFalse(value['gate_components']['strict_interior_vs_pair_max'])
        self.assertTrue(value['gate_components']['nonnegative_vs_pair_max']); self.assertTrue(value['gate_components']['nonnegative_vs_mean_ce'])

    def test_41_half_rate_updates_match_independent_pairmax_adamw_reference(self):
        self.independent_first_updates(s.CANDIDATE)

    def test_42_first_step_halves_both_group_updates_without_changing_gradients_or_moments(self):
        models = [TokenToy(),TokenToy()]; states = []; gradients = []; optimizers = []
        tokens,ids = s.select_tokens(self.tables,self.events[0],self.family[0],self.selected[0])
        initial = {name:p.detach().clone() for name,p in models[0].named_parameters()}
        for model,arm in zip(models,('pair_max',s.CANDIDATE),strict=True):
            opt = s.optimizer_for(model,arm,self.toy.x); optimizers.append(opt)
            logits = model(tokens,torch.zeros(48,dtype=torch.int64)); loss,_,_ = s.objective(logits,self.y[ids],arm)
            loss.backward(); torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True)
            gradients.append({name:p.grad.clone() for name,p in model.named_parameters()})
            opt.step(); states.append(dict(model.named_parameters()))
        for name in initial:
            self.assertTrue(torch.equal(gradients[0][name],gradients[1][name]))
            default_delta = initial[name]-states[0][name].detach(); half_delta = initial[name]-states[1][name].detach()
            self.assertGreater(float(default_delta.abs().max()),0.)
            self.assertTrue(torch.allclose(half_delta,.5*default_delta,atol=1e-16,rtol=1e-12),name)
        for a,b in zip(optimizers[0].state.values(),optimizers[1].state.values(),strict=True):
            self.assertEqual(set(a),{'step','exp_avg','exp_avg_sq'})
            for key in a: self.assertTrue(torch.equal(a[key],b[key]),key)

    def test_43_actual_native_optimizer_preserves_boundaries_and_rejects_policy_drift(self):
        model = s.make_model(s.SEEDS[0],self.x)
        core_ids = {id(p) for p in model.backbone.core.parameters()}
        for arm in s.ARMS:
            opt = s.optimizer_for(model,arm,self.x); s.verify_optimizer(opt,model,arm,self.x)
            self.assertEqual([g['lr'] for g in opt.param_groups],list(s.RATES[arm]))
            self.assertEqual({id(p) for p in opt.param_groups[1]['params']},core_ids)
            self.assertEqual(sum(p.numel() for p in opt.param_groups[0]['params']),10928)
            for key,changed in (('lr',.01),('betas',(.8,.999)),('eps',1e-7),('weight_decay',.1),('amsgrad',True),
                                ('maximize',True),('capturable',True),('differentiable',True),('foreach',True),('fused',True)):
                for group in opt.param_groups:
                    saved = group[key]; group[key] = changed
                    with self.assertRaises(ValueError): s.verify_optimizer(opt,model,arm,self.x)
                    group[key] = saved
            opt.param_groups[0]['params'],opt.param_groups[1]['params'] = opt.param_groups[1]['params'],opt.param_groups[0]['params']
            with self.assertRaises(ValueError): s.verify_optimizer(opt,model,arm,self.x)
        with self.assertRaises(ValueError): s.optimizer_for(model,'unknown',self.x)

    def test_44_work_uses_actual_full_toy_training_path_receipts_and_complete_production_cohort(self):
        # Each source trace comes from all 2400 actual production optimize/train_one
        # updates in setUpClass; cohort replication tests arithmetic, not native efficacy.
        traces = [copy.deepcopy(self.traces[arm]) for _,arm in s.identities()]
        records = self.science_fixture()[1]; states = [self.states[arm] for _,arm in s.identities()]
        for trace,(seed,arm) in zip(traces,s.identities(),strict=True): trace.update(seed=seed,arm=arm)
        for arm in s.ARMS:
            trace = self.traces[arm]
            self.assertEqual(trace['measured_training_work'],dict(calls=2400,rows=115200,core_calls=9600))
            self.assertEqual(trace['optimizer_steps'],2400); self.assertEqual(trace['optimizer_creations'],1)
        self.assertEqual(s.observed_work(traces,records,states),s.WORK)
        traces[0]['measured_training_work']['core_calls'] -= 1
        with self.assertRaises(ValueError): s.observed_work(traces,records,states)
        traces[0]['measured_training_work']['core_calls'] += 1; traces[0]['optimizer_steps'] -= 1
        self.assertNotEqual(s.observed_work(traces,records,states),s.WORK)
        bad = self.trace(); bad['optimizer_steps'] = 2399
        with self.assertRaises(ValueError): self.check_trace(bad)

    def test_45_terminal_values_use_full256_canonical_pairs_and_correct_domain_weights(self):
        raw = self.mixed_errors(); normal = s.normal_report(raw,self.data)
        with self.x.guarded.no_neural(): rows = s.terminal_report(raw,self.data,normal,s.SEEDS[0],s.CANDIDATE)
        self.assertEqual([(r['domain'],r['split']) for r in rows],list(itertools.product(s.DOMAINS,s.SPLITS)))
        for row in rows:
            split,domain = row['split'],row['domain']; tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
            targets = torch.tensor([r['target'] for r in self.data[split]],dtype=torch.int64)
            pair_indices = self.p.source().base().query_pairs(self.data[split]); ce=[]; maxima=[]
            for profile in s.parent().profiles(domain):
                z = tree[split][profile]['normal']; losses = (torch.logsumexp(z,1)-z[torch.arange(len(z)),targets]).tolist()
                ce.extend(losses); maxima.extend(max(losses[a],losses[b]) for a,b in pair_indices)
            self.assertAlmostEqual(row['mean_ce']['mean'],math.fsum(ce)/len(ce),places=13)
            self.assertAlmostEqual(row['pair_max']['mean'],math.fsum(maxima)/len(maxima),places=13)
            self.assertEqual(row['pair_max']['count'],row['mean_ce']['count']); self.assertEqual(row['mean_ce']['count'],len(ce)//2)
        six = next(r for r in rows if (r['domain'],r['split']) == ('original6','TRAIN'))
        self.assertGreater(six['mean_ce']['mean'],0.); self.assertFalse(six['normal']['normal_prompt_seen_in_training'])

    def test_46_summary_rejects_terminal_inventory_deltas_counts_and_subgate_tampering(self):
        original = self.synthetic_summary()
        for kind in ('missing','coordinate','loss','nan','count','normal','delta','contrast','headroom','ceiling','subgate'):
            value = copy.deepcopy(original)
            if kind == 'missing': value['terminal'].pop()
            elif kind == 'coordinate': value['terminal'][0]['arm'] = s.CANDIDATE
            elif kind == 'loss': value['terminal'][0]['pair_max']['mean'] = 3*value['terminal'][0]['mean_ce']['mean']
            elif kind == 'nan': value['terminal'][0]['mean_ce']['minimum'] = float('nan')
            elif kind == 'count': value['terminal'][0]['mean_ce']['count'] -= 1
            elif kind == 'normal': value['terminal'][0]['normal'] = dict(value['terminal'][0]['normal'],correct=0)
            elif kind == 'delta': value['terminal_contrasts'][0]['pair_max_delta'] += .1
            elif kind == 'contrast': value['terminal_contrasts'][0]['control_arm'] = 'mean_ce'
            elif kind == 'headroom': value['strict_interior_headroom']['TRAIN']['answer_headroom'] += 1
            elif kind == 'ceiling': value['strict_interior_ceiling'] = True
            else: value['gate_components']['nonnegative_counts']['mean_ce']['passed'] = 119
            with self.assertRaises(ValueError): s.check_summary(value)

    def test_47_both_pairmax_arms_use_identical_unscaled_objective_and_gradient(self):
        targets = torch.tensor([48,49,50,51],dtype=torch.int64)
        initial = torch.linspace(-2.,2.,4*256,dtype=torch.float64).reshape(4,256)
        losses=[]; gradients=[]
        for arm in s.ARMS:
            logits = initial.clone().requires_grad_(True); loss,ce,maximum = s.objective(logits,targets,arm)
            loss.backward(); losses.append((float(loss.detach()),float(ce.detach()),float(maximum.detach()))); gradients.append(logits.grad)
            selected = ce if arm == 'mean_ce' else maximum; self.assertIs(loss,selected)
        self.assertEqual(losses[1],losses[2]); self.assertTrue(torch.equal(gradients[1],gradients[2]))
        ordinary = initial.clone().requires_grad_(True); F.cross_entropy(ordinary,targets).backward()
        self.assertTrue(torch.equal(gradients[0],ordinary.grad))
        self.assertGreater(float(gradients[1].abs().sum()),0.)
        with self.assertRaises(ValueError): s.objective(initial,targets,'half_mean_ce')

    def test_48_larger_terminal_loss_is_descriptive_and_does_not_override_binding_gate(self):
        items = self.science_fixture()
        for record in items[1]:
            if record['arm'] != s.CANDIDATE: continue
            for mode in ('evaluation','replay'):
                raw = record['raw'][mode]
                for domain in [*raw['original'].values(),raw['interior']]:
                    for split,profiles in domain.items():
                        for views in profiles.values():
                            z = views['normal'].clone(); z.fill_(0.)
                            for i,row in enumerate(self.data[split]): z[i,row['target']] = .1
                            views['normal'] = z
        with patch.object(s,'check_trace'),self.x.guarded.no_neural(): _,value = self.analyze_fixture(items)
        self.assertTrue(value['candidate_gate']); self.assertEqual(value['eligible_seed_count'],5)
        self.assertEqual(len(value['terminal']),180); self.assertEqual(len(value['terminal_contrasts']),120)
        self.assertTrue(all(row['mean_ce_delta'] > 0 and row['pair_max_delta'] > 0 for row in value['terminal_contrasts']))
        s.check_summary(value)


if __name__ == '__main__':
    unittest.main()
