"""C343: real canonical scorers on explicitly synthetic saved logits, never a fit."""
from __future__ import annotations
import copy
import inspect
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c343_saved_mixed_length_localization as s
from fold_lm.v05_benchmarks import model_c342_mixed_length45_training as p
from fold_lm.v05_benchmarks import model_c330_saved_gate_localization as q
from tests_lm import test_v05_c340_length5_training as source_tests
from tests_lm import test_v05_c333_paired_gate_localization as scalar_fixtures


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def tree_copy(value):
    return source_tests.tree_copy(value)


def fixture():
    """Invent predictions, then run the unchanged C342 writer's scientific scorers."""
    previous = p.previous(); cx = previous.source().base().context(); x = cx[-1]
    data = x.c.p267.dataset(); old = x.parent.prompt_dataset(data,x.p313); new = cx[2].new_prompts(data)
    tables,y = p.prepared(data,old,new,cx); base = source_tests.fixtures.raw_fixture(data,'native')
    for domain in [*base['original'].values(),base['interior']]:
        for split,profiles in domain.items():
            for views in profiles.values():
                for view,z in views.items():
                    z.fill_(-4.)
                    if view == 'normal':
                        for i,row in enumerate(data[split]): z[i,row['target']] = 4.
                    else: z[:,48] = 4.
    def change(raw,domain,split,positions,kind,view='normal'):
        tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
        profile = 'balanced' if domain == 'interior4' else 'shared_suffix'
        views = tree[split][profile]; z = views[view].clone(); views[view] = z
        ids = [i for i,r in enumerate(data[split]) if r['language']=='ja' and r['entities']==[1,2] and r['permutation']==[1,2]]
        for position in positions:
            i = ids[position]; row = data[split][i]; other = 48+row['values'][1-row['entities'].index(row['query'])]
            prediction = {'correct':row['target'],'wrong_observed':other,'outside_catalog':7,
                'absent_digit':next(t for t in range(48,52) if t not in (row['target'],other))}[kind]
            z[i].fill_(-4.); z[i,prediction] = 4.
    traces,records,states = [],[],[]
    for seed,arm in s.identities():
        raw = tree_copy(base)
        if seed == s.SEEDS[0]:
            if arm == 'original5':
                change(raw,'interior4','HOLDOUT',(0,1,2,3),'wrong_observed')
                change(raw,'original4','HOLDOUT',(0,),'outside_catalog')
                change(raw,'original2','HOLDOUT',range(8),'correct','query_blind')
            else:
                change(raw,'interior4','HOLDOUT',(2,4),'wrong_observed')
                change(raw,'interior4','HOLDOUT',range(8),'correct','query_blind')
                change(raw,'interior4','TRAIN',(0,1,2),'absent_digit')
        if seed == s.SEEDS[1] and arm == 'original5':
            change(raw,'original4','HOLDOUT',(0,1),'wrong_observed')
        if seed == s.SEEDS[2] and arm == 'mixed45':
            change(raw,'original6','HOLDOUT',(0,1,2,3,4),'absent_digit')
        if seed == s.SEEDS[4]:
            change(raw,'interior4','HOLDOUT',(0,1),'absent_digit' if arm == 'original5' else 'wrong_observed')
        state = {'synthetic_state':torch.tensor([float(seed),float(arm=='mixed45')],dtype=torch.float64)}; states.append(state)
        trace = {key:'paired' for key in ('initial_sha256','core_initial_sha256','logical_training_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')}
        trace.update(seed=seed,arm=arm,training_input_sha256=arm,actual_training_stream_sha256=arm,
            length_mask_sha256=arm,final_sha256=previous.state_hash(state),nonpadding_token_presentations=p.TRAIN_TOKENS[arm])
        traces.append(trace)
        records.append(dict(seed=seed,arm=arm,state_sha256=previous.state_hash(state),evaluation_policy='native_before',
            raw={mode:tree_copy(raw) for mode in ('evaluation','replay')},
            receipts={mode:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for mode in ('evaluation','replay')}))
    # No optimizer trajectory is claimed by this fixture. Canonical input, raw-logit,
    # replay, scorer, support, individual contrasts and C342 summary checks stay real.
    with patch.object(p,'check_trace'),x.guarded.no_neural():
        metrics,saved = p.analyze(traces,records,states,data,cx,tables,y)
    if saved['candidate_gate'] is not False or saved['eligible_seed_count'] != 2:
        raise AssertionError('synthetic all-cohort fixture must retain the accepted negative/two eligible contract')
    return metrics,saved,data,dict(schema='fold-c342-evaluations-v1',records=records),cx,old,new


class C343ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.metrics,cls.saved,cls.data,cls.archive,cls.cx,cls.old,cls.new = fixture()
        with cls.cx[-1].guarded.no_neural():
            cls.expected = s.analyze(cls.metrics,cls.saved,cls.data,cls.archive,cls.cx)
        cls.observations,cls.pairs,cls.support = s.normal_observations(cls.archive['records'],cls.data)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)
    def saved_copy(self): return copy.deepcopy(self.saved)
    def summary_copy(self): return copy.deepcopy(self.expected[2])
    def archive_copy(self): return tree_copy(self.archive)
    def paths(self,folder):
        root = Path(folder); parent = root/'parent'; data = root/'data'; out = root/'out'
        for path in (parent,data,out): path.mkdir()
        for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):
            (data/name).write_bytes(s.blob(value))
        (parent/'measurements.json').write_bytes(s.blob(self.metrics)); (parent/'validation-summary.json').write_bytes(s.blob(self.saved))
        torch.save(self.archive,parent/'evaluations.pt')
        return out,parent,data
    def write_expected(self,out):
        for name,value in zip(s.OUTPUTS,(s.manifest(),*self.expected),strict=True): (out/name).write_bytes(s.blob(value))
    def test_01_manifest_registered_counts_and_zero_neural_work(self):
        s.validate_seal(); self.assertEqual(s.identities(),p.identities()); self.assertEqual(s.DOMAINS,p.DOMAINS)
        self.assertRegex(s.manifest()['acceptance_base'],'^[0-9a-f]{40}$')
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.MODULES),(p.SOURCE_COUNT+7,p.INPUT_COUNT+481+7,p.MODULES+2))
        for k in ('train_steps','model_forward_calls','gradient_calls','optimizer_steps','model_state_loads','new_checkpoint_writes','network_calls'):
            self.assertEqual(s.WORK[k],0)
    def test_02_parent_projection_uses_real_eight_field_writer(self):
        p.check_summary(self.saved); projected = s.parent_projection(self.saved)
        self.assertEqual(len(projected),10); self.assertEqual(set(projected[0]),set(s.STATE_KEYS))
        self.assertEqual(set(self.saved['seed_results'][0]),{*s.STATE_KEYS,'support','training_nonpadding_tokens'})
        self.assertEqual(s.blob(self.expected[2]['parent_validation_summary']),s.blob(self.saved))
    def test_03_complete_gate_normal_and_pair_inventories(self):
        local,trans,value = self.expected
        self.assertEqual([len(local[k]) for k in ('cells','two_order')],[4320,2160])
        self.assertEqual([len(trans[k]) for k in ('local','two_order','normal_answers','query_pairs')],[2160,1080,25920,12960])
        self.assertEqual([len(value[k]) for k in ('strata','transition_summary','normal_support','normal_transition_summary')],[144,30,120,60])
        self.assertEqual({r['transition'] for r in trans['normal_answers']},set(s.CHANGES))
    def test_04_exact_domain_exposure_counts_in_both_arms(self):
        expected = {'original5':[200,200,0,100,0,100],'mixed45':[200,200,50,50,0,100]}
        for arm in s.ARMS:
            for domain,count in zip(s.DOMAINS,expected[arm],strict=True):
                row = s.training_exposure(arm,domain,'TRAIN')
                self.assertEqual(row['domain_presentations_per_logical_train_row'],count)
                self.assertEqual(row['domain_presentations_per_logical_row'],count)
                self.assertIs(row['normal_prompt_seen_in_training'],count>0)
    def test_05_train_values_do_not_imply_seen_prompt_and_masks_never_fit(self):
        for arm,domain,split in itertools.product(s.ARMS,s.DOMAINS,q.SPLITS):
            row = s.training_exposure(arm,domain,split)
            self.assertFalse(row['masked_views_seen_in_training'])
            self.assertIs(row['value_combination_seen_in_training'],split=='TRAIN')
            self.assertIs(row['normal_prompt_seen_in_training'],split=='TRAIN' and s.EXPOSURES[arm][domain]>0)
            if split=='HOLDOUT': self.assertEqual(row['domain_presentations_per_logical_row'],0)
        self.assertFalse(s.training_exposure('original5','original4','TRAIN')['normal_prompt_seen_in_training'])
        self.assertTrue(s.training_exposure('mixed45','original4','TRAIN')['normal_prompt_seen_in_training'])
    def test_06_old_helper_annotations_replaced_without_global_mutation(self):
        score = self.metrics[1]['score']['original']['5']; before = s.blob(score)
        self.assertFalse(q.adapted_score(score,'original5')[0][0]['name_family_seen_in_training'])
        row = s.adapted_score(score,'mixed45','original5')[0][0]
        self.assertTrue(row['name_family_seen_in_training']); self.assertEqual(row['domain_presentations_per_logical_train_row'],50)
        self.assertEqual(s.blob(score),before); self.assertFalse(q.adapted_score(score,'original5')[0][0]['name_family_seen_in_training'])
    def test_07_all_binding_mask_patterns_and_order_gate_are_retained(self):
        self.assertEqual({r['pattern'] for r in self.expected[0]['cells']},set(q.PATTERNS))
        for kind,wanted in (('pass','pass'),('normal','normal_binding_only'),('mask','mask_only'),('mixed','mixed')):
            cells,_,_ = s.adapted_score(scalar_fixtures.score(kind),'mixed45','interior4')
            failed = [r for r in cells if not r['passed']]
            self.assertEqual(len(failed),int(kind!='pass'))
            if failed: self.assertEqual(failed[0]['pattern'],wanted)
        self.assertTrue(any(not r['passed'] for r in self.expected[0]['two_order']))
    def test_08_exact_thresholds_and_descriptive_deficits(self):
        values = dict(zip(q.CRITERIA,q.THRESHOLDS,strict=True)); self.assertFalse(any(q.failure_flags(values).values()))
        for key in q.CRITERIA:
            changed = dict(values); changed[key] -= 1e-12; self.assertTrue(q.failure_flags(changed)[key])
        for row in self.expected[0]['cells']:
            self.assertEqual(row['deficits'],{k:max(0.,t-row[k]) for k,t in zip(q.CRITERIA,q.THRESHOLDS,strict=True)})
        for row in self.expected[0]['two_order']: self.assertEqual(row['deficit'],max(0.,.8-row['accuracy']))
    def test_09_gate_coordinate_matching_is_not_positional_zip(self):
        metrics = copy.deepcopy(self.metrics)
        for row in metrics:
            for score in [*row['score']['original'].values(),row['score']['interior']]:
                score['cells'].reverse(); score['two_order'].reverse()
        local,trans,_ = s.localize(metrics,self.saved)
        self.assertEqual(s.blob(local),s.blob(self.expected[0])); self.assertEqual(s.blob(trans['local']),s.blob(self.expected[1]['local']))
    def test_10_parent_projection_rejects_missing_unknown_and_boolean_fields(self):
        for kind in ('missing','extra','bool','support','tokens','pair_extra'):
            saved = self.saved_copy(); row = saved['seed_results'][0]
            if kind=='missing': row.pop('failures')
            elif kind=='extra': row['unexpected']=0
            elif kind=='bool': row['failures']['original2']['local']=False
            elif kind=='support': row['support']['original2']['correct']-=1
            elif kind=='pair_extra': saved['paired_comparisons'][0]['unexpected']=0
            else: row['training_nonpadding_tokens']-=1
            with self.assertRaises((ValueError,KeyError)): s.parent_projection(saved)
    def test_11_parent_negative_and_two_eligible_are_not_promoted(self):
        for key,value in (('candidate_gate',True),('eligible_seed_count',3)):
            saved = self.saved_copy(); saved[key]=value
            with self.assertRaises(ValueError): s.parent_projection(saved)
        self.assertFalse(self.expected[2]['parent_validation_summary']['candidate_gate'])
        self.assertEqual(self.expected[2]['parent_validation_summary']['eligible_seed_count'],2)
    def test_12_canonical_data_identity_rejects_target_and_split_changes(self):
        for kind in ('target','split'):
            data = copy.deepcopy(self.data)
            if kind=='target': data['TRAIN'][0]['target']+=1
            else: data['TRAIN'][0],data['HOLDOUT'][0]=data['HOLDOUT'][0],data['TRAIN'][0]
            with self.assertRaises(ValueError): s.check_archive(self.archive,data,self.metrics,self.cx)
    def test_13_archive_schema_complete_cohort_and_order(self):
        for kind in ('schema','reverse','missing','duplicate'):
            archive = self.archive_copy()
            if kind=='schema': archive['schema']='fold-c340-evaluations-v1'
            elif kind=='reverse': archive['records'].reverse()
            elif kind=='missing': archive['records'].pop()
            else: archive['records'][1]=archive['records'][0]
            with self.assertRaises(ValueError): s.check_archive(archive,self.data,self.metrics,self.cx)
    def test_14_saved_policy_hash_and_receipt_validation(self):
        for key,value in (('evaluation_policy','first_mean'),('state_sha256','bad'),('receipts',{})):
            archive=self.archive_copy(); archive['records'][0][key]=value
            with self.assertRaises(ValueError): s.check_archive(archive,self.data,self.metrics,self.cx)
        archive=self.archive_copy(); archive['records'][0]['receipts']['evaluation']['grad_calls']=1
        with self.assertRaises(ValueError): s.check_archive(archive,self.data,self.metrics,self.cx)
    def test_15_full_views_dtype_finiteness_and_detachment_checked(self):
        for kind in ('view','dtype','nan','grad'):
            archive=self.archive_copy(); views=archive['records'][0]['raw']['evaluation']['original']['2']['TRAIN']['repeat']
            if kind=='view': views.pop('query_blind')
            elif kind=='dtype': views['normal']=views['normal'].float()
            else:
                views['normal']=views['normal'].clone()
                if kind=='nan': views['normal'][0,0]=float('nan')
                else: views['normal'].requires_grad_(True)
            with self.assertRaises(ValueError): s.check_archive(archive,self.data,self.metrics,self.cx)
    def test_16_replay_logits_and_argmax_are_exactly_validated(self):
        archive=self.archive_copy(); views=archive['records'][0]['raw']['replay']['interior']['TRAIN']['balanced']
        views['normal']=views['normal'].clone(); views['normal'][0,0]+=2e-9
        with self.assertRaises(ValueError): s.check_archive(archive,self.data,self.metrics,self.cx)
        left=torch.zeros((1,256),dtype=torch.float64); right=left.clone(); right[0,1]=1e-12
        self.assertLess(float((left-right).abs().max()),1e-9); self.assertNotEqual(left.argmax(1).item(),right.argmax(1).item())
        # The production helper also checks argmax, independently of the tolerance.
        archive=self.archive_copy()
        for mode,z in (('evaluation',left),('replay',right)):
            views=archive['records'][0]['raw'][mode]['interior']['TRAIN']['balanced']
            views['normal']=views['normal'].clone(); views['normal'][0]=z[0]
        with self.assertRaises(ValueError): s.check_archive(archive,self.data,self.metrics,self.cx)
    def test_17_raw_measurement_binding_rejects_consistent_replay_tamper(self):
        archive=self.archive_copy()
        for mode in ('evaluation','replay'):
            views=archive['records'][0]['raw'][mode]['original']['3']['TRAIN']['repeat']
            views['normal']=views['normal'].clone(); views['normal'][0].fill_(-4.); views['normal'][0,7]=4.
        with self.assertRaisesRegex(ValueError,'raw logits/measurements binding'): s.check_archive(archive,self.data,self.metrics,self.cx)
    def test_18_immutable_support_classifier_keeps_all_four_answer_kinds(self):
        z=torch.full((4,256),-4.,dtype=torch.float64)
        for i,pred in enumerate((48,49,50,7)): z[i,pred]=4.
        before=z.clone(); items=s.audit().audit_logits(z,[48]*4,[49]*4)
        self.assertEqual([r['kind'] for r in items],list(s.audit().KINDS)); self.assertTrue(torch.equal(z,before))
        self.assertEqual(s.audit().__name__,'fold_lm.v05_benchmarks.model_c337_saved_value_support')
    def test_19_first_index_argmax_ties_are_not_repaired(self):
        z=torch.zeros((2,256),dtype=torch.float64); z[0,48:50]=1.; z[1,7]=2.
        rows=s.audit().audit_logits(z,[49,48],[48,49])
        self.assertEqual((rows[0]['prediction'],rows[0]['kind'],rows[0]['within_pair_order']),(48,'wrong_observed','tie'))
        self.assertEqual((rows[1]['prediction'],rows[1]['kind']),(7,'outside_catalog'))
    def test_20_all_256_predictions_preserved_without_supplied_value_filter(self):
        rows=self.expected[1]['normal_answers']
        outside=[r for r in rows if r['control']['kind']=='outside_catalog']
        absent=[r for r in rows if r['candidate']['kind']=='absent_digit']
        self.assertTrue(outside and absent); self.assertTrue(all(r['control']['prediction']==7 for r in outside))
        self.assertTrue(all(r['candidate']['prediction'] not in (r['target'],r['other']) for r in absent))
    def test_21_each_source_row_and_profile_has_one_paired_answer(self):
        rows=self.expected[1]['normal_answers']
        keys={(r['seed'],r['domain'],r['split'],r['input_profile'],r['row_id']) for r in rows}
        self.assertEqual(len(keys),25920)
        lookup={r['id']:r for values in self.data.values() for r in values}
        for row in rows:
            source=lookup[row['row_id']]
            self.assertEqual({k:row[k] for k in ('language','entities','values','permutation','query','target')},
                             {k:source[k] for k in ('language','entities','values','permutation','query','target')})
            self.assertEqual(row['input_profile'],s.profiles(row['domain'])[q.SCORER_PROFILES.index(row['profile'])])
    def test_22_query_pairs_bind_both_entities_same_values_and_fact_order(self):
        rows=self.expected[1]['query_pairs']; lookup={r['id']:r for values in self.data.values() for r in values}
        self.assertEqual(len({(r['seed'],r['domain'],r['split'],r['input_profile'],tuple(r['row_ids'])) for r in rows}),12960)
        for row in rows:
            a,b=[lookup[k] for k in row['row_ids']]
            self.assertEqual([a['query'],b['query']],row['entities'])
            for key in ('entities','values','permutation','language'): self.assertEqual(a[key],b[key])
            self.assertEqual(row['control_both_correct'],all(x==y for x,y in zip(row['control_predictions'],row['targets'],strict=True)))
    def test_23_all_correctness_changes_and_wrong_to_wrong_moves(self):
        for a,b,wanted in ((False,True,'rescued'),(True,False,'regressed'),(False,False,'persistent_failure'),(True,True,'stable_correct')):
            self.assertEqual(s.correctness_transition(a,b),wanted)
        with self.assertRaises(ValueError): s.correctness_transition(0,True)
        rows=[r for r in self.expected[1]['normal_answers'] if r['transition']=='persistent_failure' and r['prediction_changed']]
        self.assertTrue(rows); self.assertTrue(any(r['control']['kind']!=r['candidate']['kind'] for r in rows))
    def test_24_positive_net_gain_keeps_individual_answer_regressions(self):
        row=next(r for r in self.expected[2]['normal_transition_summary'] if (r['seed'],r['domain'],r['split'])==(s.SEEDS[0],'interior4','HOLDOUT'))
        self.assertGreater(row['answer_gain'],0); self.assertGreater(row['regressed'],0)
        self.assertEqual(row['answer_gain'],row['rescued']-row['regressed'])
        raw=[r for r in self.expected[1]['normal_answers'] if (r['seed'],r['domain'],r['split'])==(s.SEEDS[0],'interior4','HOLDOUT')]
        self.assertEqual(sum(r['transition']=='regressed' for r in raw),row['regressed'])
    def test_25_all_sixteen_kind_transitions_conserve_marginals(self):
        for row in self.expected[2]['normal_transition_summary']:
            matrix=row['kind_transitions']; self.assertEqual(set(matrix),set(s.audit().KINDS))
            self.assertTrue(all(set(v)==set(s.audit().KINDS) for v in matrix.values()))
            self.assertEqual(sum(sum(v.values()) for v in matrix.values()),row['answers'])
            self.assertEqual(matrix['correct']['correct'],row['answer_changes']['stable_correct'])
        # Exercise every direction with unequal counts, so a transposed matrix
        # cannot pass merely because its dimensions and grand total are correct.
        codes=[(a,b) for a in range(4) for b in range(4) for _ in range(4*a+b+1)]
        observations=dict(self.observations); seed=s.SEEDS[3]; domain='original3'; split='TRAIN'; profile='repeat'
        for side,arm in enumerate(s.ARMS):
            key=seed,arm,domain,split,profile; original=observations[key]; changed=list(original)
            targets=[r['target'] for r in original[:len(codes)]]; others=[r['other'] for r in original[:len(codes)]]
            z=torch.full((len(codes),256),-4.,dtype=torch.float64)
            for i,(target,other,code) in enumerate(zip(targets,others,codes,strict=True)):
                absent=next(k for k in range(48,52) if k not in (target,other))
                z[i,(target,other,absent,7)[code[side]]]=4.
            changed[:len(codes)]=s.audit().audit_logits(z,targets,others); observations[key]=changed
        _,_,reports=s.paired_normal(self.data,observations,self.pairs)
        row=next(r for r in reports if (r['seed'],r['domain'],r['split'])==(seed,domain,split))
        expected={a:{b:4*i+j+1+int(i==j==0)*(576-len(codes)) for j,b in enumerate(s.audit().KINDS)} for i,a in enumerate(s.audit().KINDS)}
        self.assertEqual(row['kind_transitions'],expected)
    def test_26_train_and_holdout_counts_are_separate_and_complete(self):
        for row in self.expected[2]['normal_support']:
            self.assertEqual((row['answers'],row['query_pairs']),(576,288) if row['split']=='TRAIN' else (288,144))
        transitions=self.expected[1]['normal_answers']
        self.assertEqual(sum(r['split']=='TRAIN' for r in transitions),17280)
        self.assertEqual(sum(r['split']=='HOLDOUT' for r in transitions),8640)
        self.assertTrue(any(r['split']=='TRAIN' and r['candidate']['kind']!='correct' and r['candidate_exposure']['normal_prompt_seen_in_training'] for r in transitions))
    def test_27_every_normal_holdout_support_matches_parent(self):
        source={(r['seed'],r['arm']):r for r in self.saved['seed_results']}
        for row in self.expected[2]['normal_support']:
            if row['split']=='HOLDOUT':
                self.assertEqual({k:row[k] for k in ('answers',*s.audit().KINDS)},source[row['seed'],row['arm']]['support'][row['domain']])
    def test_28_every_individual_holdout_contrast_matches_parent(self):
        source={r['seed']:r for r in self.saved['paired_comparisons']}
        for row in self.expected[2]['normal_transition_summary']:
            if row['split']=='HOLDOUT':
                ref=source[row['seed']]['interior'] if row['domain']=='interior4' else source[row['seed']]['original_by_length'][row['domain'][-1]]
                self.assertEqual({k:row[k] for k in ref},ref)
    def test_29_missing_duplicated_or_reordered_summary_coordinates_rejected(self):
        for key in ('normal_support','normal_transition_summary'):
            for kind in ('drop','duplicate','reverse'):
                value=self.summary_copy()
                if kind=='drop': value[key].pop()
                elif kind=='duplicate': value[key][1]=copy.deepcopy(value[key][0])
                else: value[key].reverse()
                with self.assertRaises(ValueError): s.check_summary(value)
    def test_30_transition_conservation_and_kind_margins_reject_tampering(self):
        for key in ('answer','pair','matrix','predictions'):
            value=self.summary_copy(); row=value['normal_transition_summary'][0]
            if key=='answer': row['answer_changes']['regressed']+=1
            elif key=='pair': row['query_pair_changes']['stable_correct']-=1
            elif key=='matrix': row['kind_transitions']['correct']['correct']-=1
            else: row['predictions_changed']=-1
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_31_support_counts_and_pair_feasibility_checked(self):
        for key in ('correct','both_query_correct','answers'):
            value=self.summary_copy(); value['normal_support'][0][key]+=1
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_32_exposure_counts_cannot_be_boolean_or_claim_holdout_fitting(self):
        for key,wrong in (('domain_presentations_per_logical_train_row',True),('normal_prompt_seen_in_training',True)):
            value=self.summary_copy(); row=next(r for r in value['normal_support'] if r['split']=='HOLDOUT'); row[key]=wrong
            with self.assertRaises(ValueError): s.check_summary(value)
        value=self.summary_copy(); value['normal_transition_summary'][0]['candidate_exposure']['domain_presentations_per_logical_train_row']-=1
        with self.assertRaises(ValueError): s.check_summary(value)
    def test_33_real_saved_pipeline_and_five_argument_reconstruction(self):
        with tempfile.TemporaryDirectory() as directory:
            out,parent,data=self.paths(directory)
            with self.cx[-1].guarded.no_neural():
                value=s.run_diagnostic(out,parent,data,self.cx,read)
                rebuilt=s.semantic_recheck(out,parent,data,self.cx,read)
            self.assertEqual(s.blob(value),s.blob(rebuilt)); self.assertEqual(s.blob(value),s.blob(self.expected[2]))
            self.assertEqual({p.name for p in out.iterdir()},set(s.OUTPUTS))
        for function in (s.run_diagnostic,s.semantic_recheck):
            self.assertEqual(tuple(inspect.signature(function).parameters),('out','parent_out','data_out','cx','read'))
    def test_34_saved_raw_transition_tamper_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            out,parent,data=self.paths(directory); self.write_expected(out)
            changed=read(out/'transitions.json'); changed['normal_answers'][0]['candidate']['prediction']=7
            (out/'transitions.json').write_bytes(s.blob(changed))
            with self.cx[-1].guarded.no_neural(),self.assertRaisesRegex(ValueError,'saved diagnostic reconstruction:transitions.json'):
                s.semantic_recheck(out,parent,data,self.cx,read)
    def test_35_console_reports_all_failures_and_every_normal_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory); self.write_expected(out); emitted=[]
            with self.cx[-1].guarded.no_neural(): inventory=s.report_failures(out,read,lambda k,v:emitted.append((k,v)))
        self.assertEqual(inventory,self.expected[2]['failure_inventory'])
        self.assertEqual(sum(k=='C343 failed local' for k,_ in emitted),inventory['local'])
        self.assertEqual(sum(k=='C343 failed both_order' for k,_ in emitted),inventory['two_order'])
        self.assertEqual([v for k,v in emitted if k=='C343 normal support'],self.expected[2]['normal_support'])
        self.assertEqual([v for k,v in emitted if k=='C343 normal transition'],self.expected[2]['normal_transition_summary'])
    def test_36_full_analysis_preserves_input_values_and_saved_logits(self):
        before=p.previous().state_hash((self.metrics,self.saved,self.data,self.archive))
        with self.cx[-1].guarded.no_neural(): result=s.analyze(self.metrics,self.saved,self.data,self.archive,self.cx)
        self.assertEqual(p.previous().state_hash((self.metrics,self.saved,self.data,self.archive)),before)
        self.assertEqual(s.blob(result),s.blob(self.expected))
    def test_37_actual_deciding_helpers_and_parent_abi(self):
        self.assertIs(s.parent(),p); self.assertIs(s.localizer(),q)
        self.assertEqual(tuple(inspect.signature(p.semantic_recheck).parameters),('out','data_out','cx','read'))
        self.assertEqual(s.audit().__name__,'fold_lm.v05_benchmarks.model_c337_saved_value_support')
        self.assertEqual(p.previous().source().base().__name__,'fold_lm.v05_benchmarks.model_c324_interior_coverage_training')
        for domain in s.DOMAINS: self.assertEqual(tuple(s.profiles(domain)),tuple(s.audit().parent().profiles(domain)))
    def test_38_scalar_gate_failures_and_raw_prediction_changes_are_distinct(self):
        trans=self.expected[1]
        self.assertNotEqual(len(trans['local']),len(trans['normal_answers']))
        scalar=sum(bool(r['rescued']) for r in trans['local'])
        answers=sum(r['transition']=='rescued' for r in trans['normal_answers'])
        self.assertNotEqual(scalar,answers)
        mask_only=[r for r in self.expected[0]['cells'] if r['pattern']=='mask_only']
        self.assertTrue(mask_only); self.assertTrue(all(r['accuracy']==1. for r in mask_only))
    def test_39_diagnostic_loader_cannot_call_model_construction_or_state_load(self):
        with tempfile.TemporaryDirectory() as directory:
            out,parent,data=self.paths(directory)
            with patch.object(p,'make_model',side_effect=AssertionError('model construction forbidden')),\
                 patch.object(p,'load_states',side_effect=AssertionError('checkpoint load forbidden')),self.cx[-1].guarded.no_neural():
                inputs=s.load_inputs(parent,data,self.cx,read)
            self.assertEqual(len(inputs),4); self.assertEqual(inputs[3]['schema'],'fold-c342-evaluations-v1')
            self.assertEqual(list(out.iterdir()),[])
    def test_40_reporting_rejects_incomplete_saved_failure_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory); self.write_expected(out); local=read(out/'localization.json'); local['cells'].pop()
            (out/'localization.json').write_bytes(s.blob(local)); emit=Mock()
            with self.assertRaises(ValueError): s.report_failures(out,read,emit)
            emit.assert_not_called()


if __name__ == '__main__': unittest.main()
