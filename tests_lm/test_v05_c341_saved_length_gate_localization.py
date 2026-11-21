"""C341 software tests: canonical rows and real scorers, explicitly synthetic logits."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c341_saved_length_gate_localization as s
from fold_lm.v05_benchmarks import model_c340_length5_training as p
from fold_lm.v05_benchmarks import model_c330_saved_gate_localization as q
from tests_lm import test_v05_c340_length5_training as previous_tests
from tests_lm import test_v05_c333_paired_gate_localization as scalar_fixtures


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fixture():
    """Run accepted scalar scorers on invented logits; never load or train a model."""
    previous = p.previous(); cx = previous.source().base().context(); x = cx[-1]
    data = x.c.p267.dataset(); old = x.parent.prompt_dataset(data,x.p313); new = cx[2].new_prompts(data)
    tables,y = p.prepared(data,old,new,cx)
    base = previous_tests.fixtures.raw_fixture(data,'native')
    for domain in [*base['original'].values(),base['interior']]:
        for split,profiles in domain.items():
            for views in profiles.values():
                for kind,z in views.items():
                    z.fill_(-4.)
                    if kind == 'normal':
                        for i,row in enumerate(data[split]):z[i,row['target']] = 4.
                    else:z[:,48] = 4.
    def failure(raw,domain,kind):
        profiles = raw['interior'] if domain=='interior4' else raw['original'][domain[-1]]
        selected = profiles['HOLDOUT']['v_dominant' if domain=='interior4' else 'shared_suffix']
        ids = [i for i,r in enumerate(data['HOLDOUT']) if r['language']=='en' and r['entities']==[0,1] and r['permutation']==[0,1]]
        if kind in ('normal','mixed'):
            z = selected['normal'].clone(); selected['normal'] = z
            for i in ids[:2]:
                row = data['HOLDOUT'][i]; z[i].fill_(-4.); z[i,48+row['values'][1-row['entities'].index(row['query'])]] = 4.
        if kind in ('mask','mixed','query'):
            name = 'query_blind' if kind=='query' else 'evidence_blind'
            z = selected[name].clone(); selected[name] = z
            for i in ids:z[i].fill_(-4.);z[i,data['HOLDOUT'][i]['target']] = 4.
    traces,records,states = [],[],[]
    for seed,arm in s.identities():
        raw = previous_tests.tree_copy(base)
        if seed==s.SEEDS[0] and arm=='original4':failure(raw,'original6','normal')
        if seed==s.SEEDS[1] and arm=='original5':failure(raw,'interior4','mask')
        if seed==s.SEEDS[2] and arm=='original5':failure(raw,'original4','normal');failure(raw,'original5','mixed')
        if seed==s.SEEDS[3] and arm=='original5':failure(raw,'original6','query')
        state = {'synthetic_state':torch.tensor([float(seed),float(arm=='original5')],dtype=torch.float64)}; states.append(state)
        trace = {key:'paired' for key in ('initial_sha256','core_initial_sha256','logical_training_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')}
        trace.update(seed=seed,arm=arm,training_input_sha256=arm,final_sha256=previous.state_hash(state),
            nonpadding_token_presentations=p.TRAIN_TOKENS[arm]); traces.append(trace)
        records.append(dict(seed=seed,arm=arm,state_sha256=previous.state_hash(state),evaluation_policy='native_before',
            raw={mode:previous_tests.tree_copy(raw) for mode in ('evaluation','replay')},
            receipts={mode:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for mode in ('evaluation','replay')}))
    # The fixture claims no optimizer/trace execution. Real token, raw-logit, scorer,
    # support/count, pair-comparison and parent-summary validation paths still run.
    with patch.object(p,'check_trace'),x.guarded.no_neural():
        metrics,saved = p.analyze(traces,records,states,data,cx,tables,y)
    if saved['candidate_gate'] is not False or saved['eligible_seed_count'] != 2:
        raise AssertionError('synthetic fixture must reproduce a valid negative with two eligible states')
    return metrics,saved,cx


class C341ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.metrics,cls.saved,cls.cx = fixture()
        cls.expected = s.analyze(cls.metrics,cls.saved)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)
    def inputs(self):return copy.deepcopy((self.metrics,self.saved))
    def output(self):return copy.deepcopy(self.expected)
    def test_01_manifest_cohort_and_zero_neural_work(self):
        s.validate_seal();self.assertEqual(s.identities(),p.identities());self.assertEqual(s.DOMAINS,p.DOMAINS)
        for name in ('train_steps','model_forward_calls','gradient_calls','optimizer_steps','model_state_loads','new_checkpoint_writes','network_calls'):
            self.assertEqual(s.WORK[name],0)
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.MODULES),(p.SOURCE_COUNT+7,p.INPUT_COUNT+473+7,p.MODULES+2))
    def test_02_real_parent_writer_fixture_and_projection_keys(self):
        p.check_summary(self.saved);rows=s.parent_projection(self.saved)
        self.assertEqual(len(rows),10);self.assertEqual(set(rows[0]),set(s.STATE_KEYS))
        self.assertEqual(set(self.saved['seed_results'][0]),{*s.STATE_KEYS,'support','training_nonpadding_tokens'})
    def test_03_complete_coordinates_and_strata(self):
        local,changes,value = self.expected
        self.assertEqual((len(local['cells']),len(local['two_order']),len(changes['local']),len(changes['two_order'])),(4320,2160,2160,1080))
        self.assertEqual((len(value['strata']),len(value['transition_summary'])),(144,30));self.assertFalse(value['parent_validation_summary']['candidate_gate'])
    def test_04_analysis_deterministic_and_inputs_unchanged(self):
        inputs=self.inputs();before=s.digest(inputs);actual=s.analyze(*inputs)
        self.assertEqual(s.blob(actual),s.blob(self.expected));self.assertEqual(s.digest(inputs),before)
    def test_05_coordinate_reordering_preserves_match_identity(self):
        metrics,saved=self.inputs()
        for record in metrics:
            for score in [*record['score']['original'].values(),record['score']['interior']]:score['cells'].reverse();score['two_order'].reverse()
        self.assertEqual(s.blob(s.analyze(metrics,saved)),s.blob(self.expected))
    def test_06_reversed_or_incomplete_cohort_rejected(self):
        for kind in ('reverse','drop'):
            metrics,saved=self.inputs()
            if kind=='reverse':metrics.reverse()
            else:metrics.pop()
            with self.assertRaises(ValueError):s.analyze(metrics,saved)
    def test_07_old_flat_score_wrapper_rejected(self):
        metrics,saved=self.inputs();row=metrics[0];row.update(row.pop('score'))
        with self.assertRaisesRegex(ValueError,'measurements record'):s.analyze(metrics,saved)
    def test_08_missing_domain_rejected(self):
        metrics,saved=self.inputs();del metrics[0]['score']['original']['6']
        with self.assertRaises(ValueError):s.analyze(metrics,saved)
    def test_09_duplicate_local_and_order_coordinates_rejected(self):
        for key in ('cells','two_order'):
            metrics,saved=self.inputs();rows=metrics[0]['score']['original']['2'][key];rows[1]=copy.deepcopy(rows[0])
            with self.assertRaises(ValueError):s.analyze(metrics,saved)
    def test_10_false_saved_pass_and_totals_rejected(self):
        for key in ('passed','totals'):
            metrics,saved=self.inputs();value=metrics[0]['score']['original']['6']
            if key=='passed':value[key]=True
            else:value[key][0]['correct']-=1
            with self.assertRaises(ValueError):s.analyze(metrics,saved)
    def test_11_explicit_parent_adapter_rejects_old_or_unknown_fields(self):
        for kind in ('missing','extra','failure_type'):
            saved=copy.deepcopy(self.saved)
            if kind=='missing':saved['seed_results'][0].pop('failures')
            elif kind=='extra':saved['seed_results'][0]['old_unknown_field']=1
            else:saved['seed_results'][0]['failures']['original6']['local']=True
            with self.assertRaises(ValueError):s.parent_projection(saved)
    def test_12_arm_specific_name_exposure(self):
        for arm,seen in (('original4',{'original2','original3','original4','interior4'}),('original5',{'original2','original3','original5','interior4'})):
            for domain in s.DOMAINS:
                rows=[r for r in self.expected[0]['cells'] if r['arm']==arm and r['domain']==domain]
                self.assertTrue(all(r['name_family_seen_in_training'] is (domain in seen) for r in rows))
    def test_13_train_value_partition_is_not_always_fitted_prompt(self):
        for arm,domain in (('original4','original5'),('original5','original4'),('original4','original6'),('original5','original6')):
            value=s.training_exposure(arm,domain,'TRAIN');self.assertTrue(value['value_combination_seen_in_training']);self.assertFalse(value['normal_prompt_seen_in_training'])
        for arm in s.ARMS:
            value=s.training_exposure(arm,arm,'TRAIN');self.assertTrue(value['normal_prompt_seen_in_training']);self.assertFalse(value['masked_views_seen_in_training'])
            value=s.training_exposure(arm,arm,'HOLDOUT');self.assertFalse(value['normal_prompt_seen_in_training']);self.assertFalse(value['value_combination_seen_in_training'])
    def test_14_legacy_metadata_corrected_without_mutating_helper_or_scores(self):
        score=self.metrics[1]['score']['original']['5'];before=s.blob(score)
        old=q.adapted_score(score,'original5')[0];new=s.adapted_score(score,'original5','original5')[0]
        self.assertFalse(old[0]['name_family_seen_in_training']);self.assertTrue(new[0]['name_family_seen_in_training'])
        self.assertEqual(s.blob(score),before);self.assertFalse(q.adapted_score(score,'original5')[0][0]['name_family_seen_in_training'])
    def test_15_exact_thresholds_and_no_epsilon(self):
        values=dict(zip(q.CRITERIA,q.THRESHOLDS,strict=True));self.assertFalse(any(q.failure_flags(values).values()))
        for criterion in q.CRITERIA:
            lowered=dict(values);lowered[criterion]-=1e-12;self.assertTrue(q.failure_flags(lowered)[criterion])
        self.assertEqual(s.manifest()['thresholds']['both_order'],.8)
    def test_16_all_exclusive_binding_mask_patterns(self):
        for kind,wanted in (('pass','pass'),('normal','normal_binding_only'),('mask','mask_only'),('mixed','mixed')):
            cells,_,_=s.adapted_score(scalar_fixtures.score(kind),'original5','interior4')
            selected=[r for r in cells if r['pattern']!='pass'];self.assertEqual(len(selected),0 if wanted=='pass' else 1)
            if selected:self.assertEqual(selected[0]['pattern'],wanted)
        observed={r['pattern'] for r in self.expected[0]['cells']};self.assertEqual(observed,set(q.PATTERNS))
    def test_17_deficits_are_values_to_unchanged_thresholds(self):
        local=self.expected[0]
        for row in local['cells']:
            for criterion,threshold in zip(q.CRITERIA,q.THRESHOLDS,strict=True):
                self.assertEqual(row['thresholds'][criterion],threshold);self.assertEqual(row['deficits'][criterion],max(0.,threshold-row[criterion]))
                self.assertEqual(row['deficits'][criterion]>0,row['failures'][criterion])
        for row in local['two_order']:self.assertEqual(row['deficit'],max(0.,.8-row['accuracy']))
    def test_18_rescue_regression_orientation_and_two_exposures(self):
        _,changes,value=self.expected
        rescued=[r for r in changes['local'] if r['seed']==s.SEEDS[0] and r['domain']=='original6' and 'accuracy' in r['rescued']]
        self.assertEqual(len(rescued),1);self.assertFalse(rescued[0]['control_pass']);self.assertTrue(rescued[0]['candidate_pass'])
        both=next(r for r in changes['local'] if r['domain']=='original4' and r['split']=='TRAIN')
        self.assertTrue(both['control_exposure']['normal_prompt_seen_in_training']);self.assertFalse(both['candidate_exposure']['normal_prompt_seen_in_training'])
        regressed=[r for r in changes['local'] if 'accuracy' in r['regressed']];self.assertTrue(regressed)
    def test_19_cross_coordinate_transition_rejected(self):
        cells=self.expected[0]['cells'];a,b=cells[:2]
        with self.assertRaises(ValueError):s.matched_transition(a,b)
    def test_20_parent_failure_counts_reconciled(self):
        metrics,saved=self.inputs();saved['seed_results'][0]['failures']['original6']['local']+=1
        with self.assertRaisesRegex(ValueError,'parent flags'):s.analyze(metrics,saved)
    def test_21_parent_correct_and_pair_counts_reconciled(self):
        metrics,saved=self.inputs();ref=saved['paired_comparisons'][0]['original_by_length']['2']
        ref['control_correct']-=1;ref['candidate_correct']-=1;ref['control_both_correct']-=1;ref['candidate_both_correct']-=1
        for row in saved['seed_results'][:2]:row['support']['original2']['correct']-=1;row['support']['original2']['wrong_observed']+=1
        p.check_summary(saved)
        with self.assertRaisesRegex(ValueError,'HOLDOUT counts'):s.analyze(metrics,saved)
    def test_22_parent_extra_support_and_tokens_are_validated(self):
        for field in ('support','tokens'):
            saved=copy.deepcopy(self.saved)
            if field=='support':saved['seed_results'][0]['support']['original5']['correct']+=1
            else:saved['seed_results'][0]['training_nonpadding_tokens']-=1
            with self.assertRaises(ValueError):s.parent_projection(saved)
    def test_23_summary_tamper_rejected(self):
        for kind in ('metadata','pattern','transition','inventory','state'):
            value=self.output()[2]
            if kind=='metadata':value['strata'][0]['normal_prompt_seen_in_training']=False
            elif kind=='pattern':value['strata'][0]['patterns']['mask_only']+=1
            elif kind=='transition':value['transition_summary'][0]['rescued']+=1
            elif kind=='inventory':value['failure_inventory']['local']+=1
            else:value['seed_results'][0]['failures']['original6']['local']+=1
            with self.assertRaises(ValueError):s.check_summary(value)
    def test_24_parent_negative_and_two_eligible_states_preserved(self):
        for key,value in (('candidate_gate',True),('eligible_seed_count',3)):
            saved=copy.deepcopy(self.saved);saved[key]=value
            with self.assertRaises(ValueError):s.parent_projection(saved)
        self.assertEqual(s.parent_projection(self.saved)[0]['seed'],s.SEEDS[0])
    def files(self,root):
        parent=root/'parent';out=root/'out';parent.mkdir();out.mkdir()
        for name,value in zip(('measurements.json','validation-summary.json'),(self.metrics,self.saved),strict=True):(parent/name).write_bytes(s.blob(value))
        return parent,out
    def test_25_real_writer_loader_reconstruction_and_exclusive_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent,out=self.files(Path(tmp))
            with patch.object(s,'load_parent_measurements',wraps=s.load_parent_measurements) as load:
                value=s.run_diagnostic(out,parent,read);rebuilt=s.semantic_recheck(out,parent,read)
                self.assertEqual(load.call_count,2);self.assertEqual(load.call_args.args,(parent,read))
            self.assertEqual(s.blob(value),s.blob(rebuilt));self.assertEqual(set(path.name for path in out.iterdir()),set(s.OUTPUTS))
            with self.assertRaises(FileExistsError):s.run_diagnostic(out,parent,read)
    def test_26_resealed_local_metadata_does_not_bypass_reconstruction(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent,out=self.files(Path(tmp));s.run_diagnostic(out,parent,read);path=out/'localization.json';value=read(path)
            value['cells'][0]['normal_prompt_seen_in_training']=False;path.write_bytes(s.blob(value))
            with self.assertRaisesRegex(ValueError,'reconstruction'):s.semantic_recheck(out,parent,read)
    def test_27_resealed_transition_values_do_not_bypass_reconstruction(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent,out=self.files(Path(tmp));s.run_diagnostic(out,parent,read);path=out/'transitions.json';value=read(path)
            row=next(r for r in value['local'] if r['rescued']);row['rescued'],row['regressed']=row['regressed'],row['rescued'];path.write_bytes(s.blob(value))
            with self.assertRaisesRegex(ValueError,'reconstruction'):s.semantic_recheck(out,parent,read)
    def test_28_reporting_emits_every_failure_in_both_arms(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent,out=self.files(Path(tmp));value=s.run_diagnostic(out,parent,read);emit=Mock();inventory=s.report_failures(out,read,emit)
            local=[call.args[1] for call in emit.call_args_list if call.args[0]=='C341 failed local']
            orders=[call.args[1] for call in emit.call_args_list if call.args[0]=='C341 failed both_order']
            self.assertEqual(inventory,value['failure_inventory']);self.assertEqual(len(local),inventory['local']);self.assertEqual(len(orders),inventory['two_order'])
            self.assertEqual({r['arm'] for r in local},set(s.ARMS));self.assertTrue(all(not r['passed'] for r in local+orders))
            self.assertEqual(emit.call_args.args,('C341 failure inventory',inventory))
    def test_29_failure_report_coordinates_orders_and_values_complete(self):
        local=self.expected[0]
        required={'seed','arm','domain','split','profile','input_profile','language','entities','name_length',*s.training_exposure('original4','original2','TRAIN')}
        for row in local['cells']:
            if not row['passed']:self.assertTrue(required|{'permutation','failures','thresholds','deficits'}<=set(row))
        for row in local['two_order']:
            if not row['passed']:
                self.assertTrue(required|{'fact_orders','accuracy','threshold','deficit'}<=set(row))
                self.assertEqual(row['fact_orders'],[row['entities'],row['entities'][::-1]])
    def test_30_diagnostic_never_loads_weights_or_calls_neural_module(self):
        with self.cx[-1].guarded.no_neural(),patch.object(torch,'load',side_effect=AssertionError('unexpected weight load')):
            self.assertEqual(s.blob(s.analyze(self.metrics,self.saved)),s.blob(self.expected))
    def test_31_nonfinite_and_inconsistent_masked_counts_rejected(self):
        for field,value in (('answer_nll',float('nan')),('evidence_drop',.123)):
            metrics,saved=self.inputs();metrics[0]['score']['original']['2']['cells'][0][field]=value
            with self.assertRaises(ValueError):s.analyze(metrics,saved)
    def test_32_parent_answer_rescues_remain_distinct_from_gate_cell_rescues(self):
        local,changes,value=self.expected
        cell_rescues=sum('accuracy' in row['rescued'] for row in changes['local'])
        answer_rescues=sum(row['original_by_length']['6']['rescued'] for row in self.saved['paired_comparisons'])
        self.assertEqual((cell_rescues,answer_rescues),(1,2))
        self.assertEqual(s.blob(value['parent_validation_summary']),s.blob(self.saved))
        self.assertNotEqual(s.digest(local),s.digest(changes))


if __name__=='__main__':unittest.main()
