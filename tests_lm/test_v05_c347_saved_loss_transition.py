"""C347 checks use canonical data and explicitly invented saved logits; no fitting."""
from __future__ import annotations
import copy
import itertools
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import torch
from fold_lm.v05_benchmarks import model_c347_saved_loss_transition as s
from fold_lm.v05_benchmarks import model_c346_pair_max_rate as p
from tests_lm import test_v05_c340_length5_training as fixtures


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fixture():
    """Synthetic records, not a training run; only the historical trace verifier is stubbed."""
    previous = p.previous(); cx = previous.source().base().context(); x = cx[-1]
    data = x.c.p267.dataset(); old = x.parent.prompt_dataset(data,x.p313); new = cx[2].new_prompts(data)
    tables,targets = p.prepared(data,old,new,cx)
    base = fixtures.fixtures.raw_fixture(data,'native')
    for tree in [*base['original'].values(),base['interior']]:
        for views in (views for profiles in tree.values() for views in profiles.values()):
            for z in views.values(): z.fill_(-4.); z[:,48] = 4.
    arm_raw = {}
    for arm in s.ARMS:
        raw = fixtures.tree_copy(base)
        for domain,split in itertools.product(s.DOMAINS,s.SPLITS):
            tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
            for profile in s.diagnostic().profiles(domain):
                z = tree[split][profile]['normal'].clone(); z.fill_(-4.)
                for number,(a,b) in enumerate(s.diagnostic().canonical_pairs(data[split])):
                    ta,tb = [data[split][i]['target'] for i in (a,b)]
                    absent = min(set(range(48,52))-{ta,tb}); kind = number%8
                    candidate = [(ta,tb),(tb,ta),(ta,tb),(absent,absent),(ta,tb),(absent,absent),(tb,ta),(ta,ta)]
                    control = [(ta,tb),(ta,tb),(tb,ta),(ta,ta),(ta,ta),(tb,ta),(absent,absent),(ta,tb)]
                    if arm == 'mean_ce': control[3] = (tb,ta)
                    predictions = (ta,tb) if domain == 'original2' else (candidate if arm == s.CANDIDATE else control)[kind]
                    for i,prediction in zip((a,b),predictions,strict=True):
                        z[i,data[split][i]['target']] = 1.; z[i,prediction] = 4.+.25*s.ARMS.index(arm)
                tree[split][profile]['normal'] = z
        arm_raw[arm] = raw
    traces,records,states = [],[],[]
    for seed,arm in s.identities():
        state = {'synthetic_state':torch.tensor([float(seed),float(s.ARMS.index(arm))],dtype=torch.float64)}; states.append(state)
        trace = {key:'explicitly_synthetic_paired' for key in ('initial_sha256','core_initial_sha256','logical_training_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','actual_exposure_per_cycle','event_indices',
            'training_input_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256')}
        trace.update(seed=seed,arm=arm,nonpadding_token_presentations=3168000,final_sha256=previous.state_hash(state),
            loss_history=[dict(mean_ce=1.,pair_max=1.5,selected=1. if arm == 'mean_ce' else 1.5)],
            optimizer_group_lrs=[list(p.RATES[arm])]*p.STEPS,steps=2400,optimizer_steps=2400,optimizer_creations=1,
            policy_receipt=dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400),
            measured_training_work=dict(calls=2400,rows=115200,core_calls=9600))
        traces.append(trace)
        records.append(dict(seed=seed,arm=arm,state_sha256=trace['final_sha256'],evaluation_policy='native_before',
            raw={mode:fixtures.tree_copy(arm_raw[arm]) for mode in ('evaluation','replay')},
            receipts={mode:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for mode in ('evaluation','replay')}))
    # The real parent scorers, full raw validators, replay checks, normal counts,
    # terminal reductions, fixed gate and result schema remain active.
    with patch.object(p,'check_trace'),x.guarded.no_neural():
        _,saved = p.analyze(traces,records,states,data,cx,tables,targets)
    if saved['candidate_gate'] is not False or saved['eligible_seed_count'] != 0:
        raise AssertionError('synthetic fixture requires negative/zero-eligible parent schema')
    return traces,dict(schema='fold-c346-evaluations-v1',records=records),saved,data,cx,old,new


class C347ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.traces,cls.archive,cls.saved,cls.data,cls.cx,cls.old,cls.new = fixture()
        with cls.cx[-1].guarded.no_neural():
            cls.expected = s.analyze(cls.traces,cls.archive,cls.saved,cls.data,cls.cx)
        cls.by_state = {}
        for row in cls.expected[0]['pairs']:
            cls.by_state.setdefault((row['seed'],row['arm'],row['domain'],row['split']),[]).append(row)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)
    def summary(self): return copy.deepcopy(self.expected[2])
    def archive_copy(self): return fixtures.tree_copy(self.archive)
    def check_archive(self,archive,traces=None,saved=None):
        return s.check_archive(archive,self.traces if traces is None else traces,self.data,self.saved if saved is None else saved,self.cx)
    def pair(self,arm='pair_max',domain='original2',split='TRAIN',index=0):
        return copy.deepcopy(self.by_state[s.SEEDS[0],arm,domain,split][index])
    def logits(self): return self.archive['records'][0]['raw']['evaluation']['original']['2']['TRAIN']['repeat']['normal']
    def paths(self,root):
        out,source,data = [Path(root)/name for name in ('out','source','data')]
        for path in (out,source,data): path.mkdir()
        for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):
            (data/name).write_bytes(s.blob(value))
        (source/'training-traces.json').write_bytes(s.blob(self.traces))
        (source/'validation-summary.json').write_bytes(s.blob(self.saved))
        torch.save(self.archive,source/'evaluations.pt')
        return out,source,data
    def write_expected(self,out):
        for name,value in zip(s.OUTPUTS,(s.manifest(),*self.expected),strict=True): (out/name).write_bytes(s.blob(value))
    def altered_probabilities(self,first,second):
        z = torch.full_like(self.logits(),math.log(.1/255))
        for i,row in enumerate(self.data['TRAIN']): z[i,row['target']] = math.log(.9)
        a,b = s.diagnostic().canonical_pairs(self.data['TRAIN'])[0]
        for index,values in zip((a,b),(first,second),strict=True):
            target = self.data['TRAIN'][index]['target']
            if type(values) is float:
                probability = math.exp(-values); z[index].fill_(math.log((1-probability)/255)); z[index,target] = -values
            else:
                wanted,rival = values; z[index].fill_(math.log((1-wanted-rival)/254))
                z[index,target] = math.log(wanted); z[index,200] = math.log(rival)
        return z
    def observed_pair(self,z,arm):
        row = self.pair(arm); row.update(s.diagnostic().terminal_view(z,self.data['TRAIN'])[0])
        row['collapsed'] = row['predictions'][0] == row['predictions'][1]
        return row

    def test_01_sealed_manifest_scope_and_actual_test_inventory(self):
        s.validate_seal(); self.assertEqual(s.identities(),p.identities()); self.assertEqual(s.coordinates(),list(itertools.product(p.SEEDS,p.CONTROLS,p.DOMAINS,p.SPLITS)))
        self.assertEqual(s.ACCEPTANCE_BASE,'c0597bbc24ca3db2761763b65cfe8521af7d1b2e')
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.MODULES),(p.SOURCE_COUNT+7,p.INPUT_COUNT+497+7,p.MODULES+2))
        modules = ('tests_lm.test_v05_c347_saved_loss_transition','tests_lm.test_v05_c347_execution')
        own = unittest.TestLoader().loadTestsFromNames(modules)
        self.assertEqual(own.countTestCases(),s.OWN_TESTS); self.assertEqual(s.FULL_TESTS,p.FULL_TESTS+own.countTestCases())
        self.assertEqual(len(s.OWN),7); self.assertEqual(len(s.OUTPUTS),4)
    def test_02_saved_only_work_keeps_all_three_arms_and_both_controls(self):
        self.assertEqual((s.ARMS,s.CONTROLS,s.CANDIDATE),(p.ARMS,p.CONTROLS,p.CANDIDATE))
        for key in ('train_steps','model_forward_calls','gradient_calls','optimizer_steps','model_state_loads','new_checkpoint_writes','network_calls'):
            self.assertEqual(s.WORK[key],0)
        self.assertEqual((s.WORK['evaluation_bundle_loads'],s.WORK['training_trace_loads']),(1,1))
        self.assertFalse(s.manifest()['capability_gate_applicable']); self.assertFalse(s.manifest()['production_adoption'])
    def test_03_canonical_nonbinary_data_and_distinct_query_targets(self):
        self.assertEqual(self.data,fixtures.fixtures.data_fixture())
        self.assertEqual({r['target'] for rows in self.data.values() for r in rows},{48,49,50,51})
        self.assertEqual([len(self.data[k]) for k in s.SPLITS],[192,96])
        for rows in self.data.values():
            pairs = s.diagnostic().canonical_pairs(rows); self.assertEqual(2*len(pairs),len(rows))
            for a,b in pairs:
                self.assertNotEqual(rows[a]['query'],rows[b]['query']); self.assertNotEqual(rows[a]['target'],rows[b]['target'])
    def test_04_saved_ce_matches_independent_full256_logsumexp(self):
        z = self.logits(); y = torch.tensor([r['target'] for r in self.data['TRAIN']]); expected = torch.logsumexp(z,1)-z[torch.arange(len(y)),y]
        actual = s.diagnostic().terminal_view(z,self.data['TRAIN'])
        for row,(a,b) in zip(actual,s.diagnostic().canonical_pairs(self.data['TRAIN']),strict=True):
            for value,i in zip(row['per_query_ce'],(a,b),strict=True): self.assertAlmostEqual(value,float(expected[i]),places=13)
    def test_05_all256_classes_and_first_index_ties_remain_observed(self):
        z = self.logits().clone(); z[:,200] = 12.
        actual = s.diagnostic().terminal_view(z,self.data['TRAIN'])
        self.assertTrue(all(r['predictions'] == [200,200] and r['correct_answers'] == 0 for r in actual))
        tied = s.diagnostic().terminal_view(torch.zeros_like(z),self.data['TRAIN'])
        self.assertTrue(all(r['predictions'] == [0,0] for r in tied)); self.assertAlmostEqual(tied[0]['mean_ce'],math.log(256),places=14)
    def test_06_canonical_pairing_handles_nonadjacent_row_order(self):
        order = list(range(0,192,2))+list(range(1,192,2)); rows = [self.data['TRAIN'][i] for i in order]
        a = s.diagnostic().terminal_view(self.logits()[order],rows); b = s.diagnostic().terminal_view(self.logits(),self.data['TRAIN'])
        key = lambda row:tuple(row['row_ids'])
        self.assertEqual(s.blob(sorted(a,key=key)),s.blob(sorted(b,key=key)))
    def test_07_invalid_canonical_metadata_or_teacher_alignment_rejected(self):
        for kind in ('values','target','query'):
            rows = copy.deepcopy(self.data['TRAIN']); a,b = s.diagnostic().canonical_pairs(rows)[0]
            if kind == 'values': rows[a]['values'][0] = 9
            elif kind == 'target': rows[a]['target'] = rows[b]['target']
            else: rows[a]['query'] = rows[b]['query']
            with self.assertRaises((ValueError,KeyError)): s.diagnostic().terminal_view(self.logits(),rows)
    def test_08_wrong_shape_dtype_nonfinite_or_overflow_rejected(self):
        z = self.logits()
        for invalid in (z[:191],z[:,:255],z.float(),torch.full_like(z,float('nan')),torch.full_like(z,float('inf'))):
            with self.assertRaises(ValueError): s.diagnostic().terminal_view(invalid,self.data['TRAIN'])
        huge = torch.full_like(z,1e308)
        for i,row in enumerate(self.data['TRAIN']): huge[i,row['target']] = -1e308
        with self.assertRaises(ValueError): s.diagnostic().terminal_view(huge,self.data['TRAIN'])
    def test_09_correctness_labels_include_one_correct_pair_in_W(self):
        self.assertEqual([s.transition(a,b) for a,b in ((True,True),(True,False),(False,True),(False,False))],list(s.TRANSITIONS))
        a,b = self.pair(),self.pair(s.CANDIDATE); b['predictions'][1] = b['predictions'][0]
        b.update(correct_answers=1,both_correct=False,collapsed=True)
        row = s.matched_pair(a,b)
        self.assertEqual(row['pair_transition'],'CW'); self.assertEqual(row['query_transitions'],['CC','CW'])
        with self.assertRaises(ValueError): s.transition(1,False)
    def test_10_collapse_partitions_do_not_assert_correctness(self):
        self.assertEqual([s.collapse_transition(a,b) for a,b in ((False,False),(False,True),(True,False),(True,True))],list(s.COLLAPSE_TRANSITIONS))
        a,b = self.pair(),self.pair(s.CANDIDATE); b['predictions'] = list(reversed(b['targets']))
        b.update(correct_answers=0,both_correct=False,collapsed=False)
        row = s.matched_pair(a,b)
        self.assertEqual(row['collapse_transition'],'distinct_to_distinct'); self.assertEqual(row['pair_transition'],'CW')
    def test_11_multiclass_regression_can_lower_ce_and_rescue_raise_ce(self):
        correct = self.altered_probabilities(math.log(10.),.1)
        wrong = self.altered_probabilities((.4,.5),.1)
        regressed = s.matched_pair(self.observed_pair(correct,'pair_max'),self.observed_pair(wrong,s.CANDIDATE))
        rescued = s.matched_pair(self.observed_pair(wrong,'pair_max'),self.observed_pair(correct,s.CANDIDATE))
        self.assertEqual(regressed['query_transitions'][0],'CW'); self.assertLess(regressed['query_ce_deltas'][0],0.)
        self.assertEqual(rescued['query_transitions'][0],'WC'); self.assertGreater(rescued['query_ce_deltas'][0],0.)
    def test_12_pairmax_delta_tracks_a_changed_maximum_member(self):
        a = self.observed_pair(self.altered_probabilities(1.,3.),'pair_max')
        b = self.observed_pair(self.altered_probabilities(2.5,2.),s.CANDIDATE); row = s.matched_pair(a,b)
        self.assertLess(a['per_query_ce'][0],a['per_query_ce'][1]); self.assertGreater(b['per_query_ce'][0],b['per_query_ce'][1])
        self.assertAlmostEqual(row['pair_max_delta'],-.5,places=13)
        self.assertNotAlmostEqual(row['pair_max_delta'],max(row['query_ce_deltas']),places=10)
    def test_13_empty_strata_have_zero_sums_and_null_means(self):
        value = s.loss_statistics([],[],576)
        nullable = ('control_mean','candidate_mean','delta_mean','delta_min','delta_max')
        self.assertEqual(value,{k:None if k in nullable else 0. for k in s.METRIC_FIELDS})
        for key in s.METRIC_FIELDS:
            bad = dict(value); bad[key] = 0. if key in nullable else .1
            with self.assertRaises(ValueError): s.check_loss_statistics(bad,0,576)
    def test_14_signed_contribution_uses_full_domain_denominator(self):
        value = s.loss_statistics([1.,3.],[2.,5.],10)
        self.assertEqual(value['delta_mean'],1.5); self.assertEqual(value['delta_contribution'],.3)
        negative = s.loss_statistics([2.,5.],[1.,3.],10); self.assertEqual(negative['delta_contribution'],-.3)
        for invalid in (dict(value,delta_contribution=1.5),dict(value,delta_sum=4.),dict(value,candidate_mean=4.)):
            with self.assertRaises(ValueError): s.check_loss_statistics(invalid,2,10)
        cancellation = s.loss_statistics([1e16,1.],[1e16,2.],2)
        self.assertEqual(cancellation['delta_sum'],1.)
        self.assertNotEqual(cancellation['delta_sum'],cancellation['candidate_sum']-cancellation['control_sum'])
        self.assertEqual((cancellation['delta_min'],cancellation['delta_max']),(0.,1.))
        s.check_loss_statistics(cancellation,2,2)
    def test_15_archive_schema_seed_order_omission_and_duplicates_rejected(self):
        for kind in ('schema','seed','reverse','missing','duplicate'):
            archive = self.archive_copy()
            if kind == 'schema': archive['schema'] = 'fold-c344-evaluations-v1'
            elif kind == 'seed': archive['records'][0]['seed'] = 344001
            elif kind == 'reverse': archive['records'].reverse()
            elif kind == 'missing': archive['records'].pop()
            else: archive['records'][1] = archive['records'][0]
            with self.assertRaises(ValueError): self.check_archive(archive)
    def test_16_saved_trace_hash_policy_receipt_and_trace_cohort_bound(self):
        for key,value in (('state_sha256','f'*64),('evaluation_policy','after'),('receipts',{'evaluation':{},'replay':{}})):
            archive = self.archive_copy(); archive['records'][0][key] = value
            with self.assertRaises(ValueError): self.check_archive(archive)
        for kind in ('seed','final_sha256','missing'):
            traces = copy.deepcopy(self.traces)
            if kind == 'missing': traces.pop()
            else: traces[0][kind] = 344001 if kind == 'seed' else 'f'*64
            with self.assertRaises(ValueError): self.check_archive(self.archive,traces=traces)
    def test_17_saved_replay_drift_and_argmax_flip_rejected(self):
        for delta in (.01,20.):
            archive = self.archive_copy(); views = archive['records'][0]['raw']['replay']['interior']['TRAIN']['balanced']
            z = views['normal'].clone(); z[0,200] += delta; views['normal'] = z
            with self.assertRaises(ValueError): self.check_archive(archive)
    def test_18_accepted_parent_result_is_complete_and_negative_zero(self):
        result = self.expected[2]; p.check_summary(result['parent_validation_summary'])
        self.assertEqual(s.blob(result['parent_validation_summary']),s.blob(self.saved))
        self.assertFalse(self.saved['candidate_gate']); self.assertEqual(self.saved['eligible_seed_count'],0)
        self.assertEqual(s.blob(result['terminal']),s.blob(self.saved['terminal']))
        self.assertEqual(s.blob(result['terminal_contrasts']),s.blob(self.saved['terminal_contrasts']))
    def test_19_normal_counts_cannot_drift_from_saved_parent(self):
        archive = self.archive_copy()
        for mode in ('evaluation','replay'):
            views = archive['records'][0]['raw'][mode]['original']['2']['TRAIN']['repeat']; z = views['normal'].clone()
            z[0].fill_(-4.); z[0,200] = 20.; views['normal'] = z
        with self.assertRaisesRegex(ValueError,'normal bindings'): self.check_archive(archive)
    def test_20_terminal_loss_drift_is_rejected_even_when_predictions_match(self):
        archive = self.archive_copy()
        for mode in ('evaluation','replay'):
            views = archive['records'][0]['raw'][mode]['original']['2']['TRAIN']['repeat']; z = views['normal'].clone()
            z[0,self.data['TRAIN'][0]['target']] += .1; views['normal'] = z
        records = self.check_archive(archive)
        with self.assertRaisesRegex(ValueError,'terminal binding'): s.normal_observations(records,self.data,self.saved)
    def test_21_exact_rescue_regression_counts_bind_parent_contrasts(self):
        for row in self.expected[2]['comparisons']:
            answer = {g['transition']:g['count'] for g in row['answer_transitions']}; pair = {g['transition']:g['count'] for g in row['pair_transitions']}
            n = row['normal_contrast']
            self.assertEqual((answer['WC'],answer['CW'],pair['WC'],pair['CW']),(n['rescued'],n['regressed'],n['pair_rescued'],n['pair_regressed']))
            self.assertEqual((answer['WC']-answer['CW'],pair['WC']-pair['CW']),(n['answer_gain'],n['query_pair_gain']))
    def test_22_all_saved_answers_pairs_profiles_and_languages_preserved(self):
        rows = self.expected[0]['pairs']; self.assertEqual((len(rows),sum(len(r['per_query_ce']) for r in rows)),(38880,77760))
        self.assertEqual({r['language'] for r in rows},{'en','ja'}); self.assertEqual(len(self.by_state),180)
        for (_,_,domain,split),group in self.by_state.items():
            self.assertEqual(len(group),288 if split == 'TRAIN' else 144)
            self.assertEqual({r['profile'] for r in group},set(s.diagnostic().profiles(domain)))
    def test_23_every_comparator_and_all_three_exhaustive_partitions_saved(self):
        value = self.expected[1]; self.assertEqual(len(value['pairs']),25920)
        self.assertEqual(sum(len(r['query_transitions']) for r in value['pairs']),51840)
        self.assertEqual(len(value['comparisons']),120)
        for key in ('answer_transitions','pair_transitions','collapse_transitions'):
            self.assertEqual(sum(len(r[key]) for r in value['comparisons']),480)
        self.assertEqual({r['control_arm'] for r in value['pairs']},set(s.CONTROLS))
    def test_24_each_collapse_partition_recovers_parent_origin_destination_counts(self):
        parent_terminal = {(r['seed'],r['arm'],r['domain'],r['split']):r for r in self.saved['terminal']}
        for row in self.expected[2]['comparisons']:
            counts = {g['transition']:g['count'] for g in row['collapse_transitions']}
            a,b = [parent_terminal[row['seed'],arm,row['domain'],row['split']]['normal']['collapsed_pairs'] for arm in (row['control_arm'],s.CANDIDATE)]
            self.assertEqual(counts['same_to_distinct']+counts['same_to_same'],a)
            self.assertEqual(counts['distinct_to_same']+counts['same_to_same'],b)
    def test_25_each_partition_separately_recovers_parent_loss_differences(self):
        for row in self.expected[2]['comparisons']:
            for key,metrics in (('answer_transitions',('ce',)),('pair_transitions',('mean_ce','pair_max')),('collapse_transitions',('mean_ce','pair_max'))):
                for metric in metrics:
                    actual = math.fsum(g[metric]['delta_contribution'] for g in row[key])
                    self.assertAlmostEqual(actual,row[('mean_ce' if metric == 'ce' else metric)+'_delta'],places=12)
    def test_26_pair_matching_rejects_metadata_and_arm_mismatch(self):
        for key,invalid in (('row_ids',['different','IDs']),('targets',[48,99]),('language','unknown'),('entities',['x','y']),
                            ('values',[5,6]),('permutation',[1,0]),('seed',346002),('domain','interior4'),('profile','shared_suffix'),('arm','pair_max')):
            a,b = self.pair(),self.pair(s.CANDIDATE); b[key] = invalid
            with self.assertRaises(ValueError): s.matched_pair(a,b)
    def test_27_observation_duplicate_missing_and_wrong_control_rejected(self):
        for kind in ('duplicate','missing','control'):
            values = dict(pairs=list(self.expected[0]['pairs']))
            if kind == 'duplicate': values['pairs'][1] = values['pairs'][0]
            elif kind == 'missing': values['pairs'].pop()
            else: values['pairs'][0] = dict(values['pairs'][0],arm='unregistered')
            with self.assertRaises(ValueError): s.decomposition(values,self.saved)
    def test_28_summary_coordinate_seed_control_and_order_tampering_rejected(self):
        for kind in ('seed','control_arm','candidate_arm','reverse','missing'):
            value = self.summary()
            if kind == 'reverse': value['comparisons'].reverse()
            elif kind == 'missing': value['comparisons'].pop()
            else: value['comparisons'][0][kind] = 344001 if kind == 'seed' else 'unregistered'
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_29_summary_empty_group_means_sums_and_labels_cannot_be_repaired(self):
        for key,invalid in (('control_mean',0.),('candidate_mean',0.),('delta_min',0.),('delta_max',0.),('delta_sum',.01),('delta_contribution',.01)):
            value = self.summary(); group = value['comparisons'][0]['answer_transitions'][1]
            self.assertEqual(group['count'],0); group['ce'][key] = invalid
            with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary(); value['comparisons'][0]['answer_transitions'][1]['transition'] = 'CC'
        with self.assertRaises(ValueError): s.check_summary(value)
    def test_30_summary_loss_delta_mean_and_denominator_tampering_rejected(self):
        for key in ('control_sum','candidate_sum','delta_sum','control_mean','candidate_mean','delta_mean','delta_contribution'):
            value = self.summary(); value['comparisons'][0]['answer_transitions'][0]['ce'][key] += .01
            with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary(); value['comparisons'][0]['mean_ce_delta'] += .01
        with self.assertRaises(ValueError): s.check_summary(value)
        for key,difference in (('delta_min',.1),('delta_max',-.1)):
            value = self.summary(); metric = value['comparisons'][0]['answer_transitions'][0]['ce']; metric[key] = metric['delta_mean']+difference
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_31_summary_normal_gains_and_collapse_counts_are_bound(self):
        for kind in ('rescued','regressed','pair_rescued','pair_regressed','answer_gain'):
            value = self.summary(); value['comparisons'][0]['normal_contrast'][kind] += 1
            with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary(); groups = value['comparisons'][0]['collapse_transitions']; groups[0]['count'] -= 1; groups[1]['count'] += 1
        with self.assertRaises(ValueError): s.check_summary(value)
    def test_32_summary_cannot_promote_parent_gate_or_eligible_seeds(self):
        for key,invalid in (('candidate_gate',True),('eligible_seed_count',1),('paired_conditions_valid',False)):
            value = self.summary(); value['parent_validation_summary'][key] = invalid
            with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary(); value['diagnostic_complete'] = False
        with self.assertRaises(ValueError): s.check_summary(value)
    def test_33_summary_hashes_work_fields_and_nonfinite_values_are_checked(self):
        for key in ('source_trace_sha256','source_parent_summary_sha256','observations_sha256','decomposition_sha256'):
            value = self.summary(); value[key] = 'invalid'
            with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary(); value['source_parent_summary_sha256'] = 'f'*64
        with self.assertRaises(ValueError): s.check_summary(value)
        for key,invalid in (('normal_answers',True),('matched_pairs',25919),('train_steps',1)):
            value = self.summary(); value[key] = invalid
            with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary(); value['comparisons'][0]['answer_transitions'][0]['ce']['delta_sum'] = float('nan')
        with self.assertRaises(ValueError): s.check_summary(value)
    def test_34_production_run_uses_real_loader_once_and_performs_no_neural_work(self):
        with tempfile.TemporaryDirectory() as root:
            out,source,data = self.paths(root); observed = []; torch_load = torch.load
            def recording(path): observed.append(Path(path)); return read(path)
            with patch.object(torch,'load',wraps=torch_load) as load,patch.object(s,'load_inputs',wraps=s.load_inputs) as inputs,self.cx[-1].guarded.no_neural():
                value = s.run_diagnostic(out,source,data,self.cx,recording)
            self.assertEqual(inputs.call_count,1); self.assertEqual(load.call_count,1)
            self.assertEqual(load.call_args.args[0],source/'evaluations.pt'); self.assertEqual(load.call_args.kwargs,dict(map_location='cpu',weights_only=True))
            self.assertEqual(observed.count(source/'training-traces.json'),1); self.assertEqual(observed.count(source/'validation-summary.json'),1)
            self.assertEqual({path.name for path in observed},{'dataset.json','original-prompts.json','interior-prompts.json','training-traces.json','validation-summary.json'})
            self.assertEqual(s.blob(value),s.blob(self.expected[2])); self.assertEqual({path.name for path in out.iterdir()},set(s.OUTPUTS))
            for name,wanted in zip(s.OUTPUTS,(s.manifest(),*self.expected),strict=True): self.assertEqual((out/name).read_bytes(),s.blob(wanted))
    def test_35_fresh_semantic_recheck_reconstructs_all_four_saved_artifacts(self):
        with tempfile.TemporaryDirectory() as root:
            out,source,data = self.paths(root); self.write_expected(out)
            with self.cx[-1].guarded.no_neural(),patch.object(s,'analyze',wraps=s.analyze) as analyze:
                value = s.semantic_recheck(out,source,data,self.cx,read)
            self.assertEqual(analyze.call_count,1); self.assertEqual(s.blob(value),s.blob(self.expected[2]))
    def test_36_semantic_recheck_rejects_tampering_in_every_output(self):
        with tempfile.TemporaryDirectory() as root:
            out,source,data = self.paths(root)
            for name in s.OUTPUTS:
                self.write_expected(out); value = read(out/name)
                if name == 'audit-plan.json': value['candidate'] = 'mean_ce'
                elif name == 'normal-pair-observations.json': value['pairs'][0]['language'] = 'unknown'
                elif name == 'loss-transition-decomposition.json': value['pairs'][0]['pair_max_delta'] += .01
                else: value['observations_sha256'] = 'f'*64
                (out/name).write_bytes(s.blob(value))
                with patch.object(s,'reconstructed',return_value=self.expected),self.assertRaisesRegex(ValueError,name):
                    s.semantic_recheck(out,source,data,self.cx,read)
    def test_37_canonical_data_and_prompt_tampering_rejected_by_real_loader(self):
        with tempfile.TemporaryDirectory() as root:
            _,source,data = self.paths(root)
            for name in ('dataset.json','original-prompts.json','interior-prompts.json'):
                path = data/name; before = path.read_bytes(); value = read(path); value['unknown_extra'] = 'tamper'; path.write_bytes(s.blob(value))
                with self.assertRaises((ValueError,KeyError)): s.load_inputs(source,data,self.cx,read)
                path.write_bytes(before)
    def test_38_reconstruction_detects_source_mutation_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            out,source,data = self.paths(root); saved = copy.deepcopy(self.saved)
            def mutate(*args): saved['evaluation_policy'] = 'mutated'; return self.expected
            with patch.object(s,'load_inputs',return_value=(self.traces,self.archive,saved,self.data)),patch.object(s,'analyze',side_effect=mutate):
                with self.assertRaisesRegex(ValueError,'mutation'): s.reconstructed(source,data,self.cx,read)
            (out/s.OUTPUTS[0]).write_bytes(b'preserve existing output')
            with patch.object(s,'reconstructed',return_value=self.expected),self.assertRaises(FileExistsError): s.run_diagnostic(out,source,data,self.cx,read)
            self.assertEqual((out/s.OUTPUTS[0]).read_bytes(),b'preserve existing output')
    def test_39_reporting_emits_all_comparisons_parent_binding_and_provenance(self):
        emitted = []; actual = s.report_results(self.expected[2],lambda label,row:emitted.append((label,row)))
        self.assertEqual(actual,s.WORK)
        for label,count in (('C347 parent terminal objective',180),('C347 parent terminal contrast',120),('C347 loss transition decomposition',120)):
            self.assertEqual(sum(name == label for name,_ in emitted),count)
        self.assertEqual(dict(emitted)['C347 preserved parent result'],dict(candidate_gate=False,eligible_seed_count=0))
        self.assertEqual(dict(emitted)['C347 source provenance']['source_trace_sha256'],s.digest(self.traces))
    def test_40_loss_signs_are_descriptive_and_parent_negative_is_never_upgraded(self):
        s.check_summary(self.expected[2]); rows = self.expected[1]['pairs']
        deltas = [delta for row in rows for delta in row['query_ce_deltas']]
        self.assertTrue(any(d < 0 for d in deltas)); self.assertTrue(any(d > 0 for d in deltas))
        self.assertTrue(self.expected[2]['diagnostic_complete']); self.assertFalse(self.expected[2]['parent_validation_summary']['candidate_gate'])
        self.assertEqual(s.digest(self.expected[0]),self.expected[2]['observations_sha256'])
        self.assertEqual(s.digest(self.expected[1]),self.expected[2]['decomposition_sha256'])
