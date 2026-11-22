"""C345 arithmetic on canonical inputs and explicitly invented saved logits/traces."""
from __future__ import annotations
import copy
import inspect
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c345_saved_objective_audit as s
from fold_lm.v05_benchmarks import model_c344_pair_max_training as p
from tests_lm import test_v05_c340_length5_training as fixtures


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fixture():
    """No training. Historical full-trace verifier alone is stubbed for invented histories."""
    previous = p.previous(); cx = previous.source().base().context(); x = cx[-1]
    data = x.c.p267.dataset(); old = x.parent.prompt_dataset(data,x.p313); new = cx[2].new_prompts(data)
    tables,targets = p.prepared(data,old,new,cx); base = fixtures.fixtures.raw_fixture(data,'native')
    for domain in [*base['original'].values(),base['interior']]:
        for split,profiles in domain.items():
            for views in profiles.values():
                for view,z in views.items():
                    z.fill_(-4.)
                    if view == 'normal':
                        for i,row in enumerate(data[split]): z[i,row['target']] = 4.
                    else: z[:,48] = 4.
    traces,records,states = [],[],[]
    for seed,arm in s.identities():
        raw = fixtures.tree_copy(base)
        if seed in s.SEEDS[:3] and arm == 'pair_max':
            for split in s.SPLITS:
                for profile in s.profiles('interior4'):
                    z = raw['interior'][split][profile]['normal'].clone()
                    for i,row in enumerate(data[split]):
                        z[i].fill_(-4.); z[i,48+row['values'][1-row['entities'].index(row['query'])]] = 4.
                    raw['interior'][split][profile]['normal'] = z
        state = {'synthetic':torch.tensor([float(seed),float(arm == 'pair_max')],dtype=torch.float64)}; states.append(state)
        trace = {key:'explicitly_synthetic' for key in ('initial_sha256','core_initial_sha256','logical_training_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','actual_exposure_per_cycle',
            'training_input_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256')}
        losses,norms = [],[]
        for step in range(s.STEPS):
            ce = .2+(step%17)/100
            if step and arm == 'pair_max': ce += .05 if seed%2 else -.05
            maximum = ce+.1
            losses.append(dict(mean_ce=ce,pair_max=maximum,selected=ce if arm == 'mean_ce' else maximum))
            norms.append((.5,1.,1.5)[step%3])
        trace.update(seed=seed,arm=arm,nonpadding_token_presentations=3168000,final_sha256=previous.state_hash(state),
            loss_history=losses,preclip_norm_history=norms,event_indices=list(range(s.CYCLE))*2,
            optimizer_group_lrs=[list(p.RATES) for _ in range(s.STEPS)])
        traces.append(trace)
        records.append(dict(seed=seed,arm=arm,state_sha256=trace['final_sha256'],evaluation_policy='native_before',
            raw={mode:fixtures.tree_copy(raw) for mode in ('evaluation','replay')},
            receipts={mode:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for mode in ('evaluation','replay')}))
    # C344's real raw validators, replay checks, full scorers, normal counts and gate
    # arithmetic remain active. This is not a fabricated scientific execution.
    with patch.object(p,'check_trace'),x.guarded.no_neural():
        _,saved = p.analyze(traces,records,states,data,cx,tables,targets)
    if saved['candidate_gate'] is not False or saved['eligible_seed_count'] != 2:
        raise AssertionError('synthetic fixture requires the accepted negative/two-eligible schema')
    return traces,dict(schema='fold-c344-evaluations-v1',records=records),saved,data,cx,tables,targets,old,new


class C345ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.traces,cls.archive,cls.saved,cls.data,cls.cx,cls.tables,cls.targets,cls.old,cls.new = fixture()
        with patch.object(p,'check_trace'),cls.cx[-1].guarded.no_neural():
            cls.expected = s.analyze(cls.traces,cls.archive,cls.saved,cls.data,cls.cx,cls.tables,cls.targets)
        cls.rows = cls.expected[1]['rows']
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)
    def trace_copy(self): return copy.deepcopy(self.traces)
    def archive_copy(self): return fixtures.tree_copy(self.archive)
    def summary_copy(self): return copy.deepcopy(self.expected[2])
    def trace_rows(self,traces):
        with patch.object(p,'check_trace'):
            return s.trace_rows(traces,self.data,self.cx,self.tables,self.targets)
    def archive_check(self,archive,traces=None,saved=None):
        return s.check_archive(archive,self.traces if traces is None else traces,self.data,
            self.saved if saved is None else saved,self.cx)
    def logits(self): return self.archive['records'][0]['raw']['evaluation']['interior']['TRAIN']['balanced']['normal']
    def paths(self,root):
        out,source,data = [Path(root)/name for name in ('out','source','data')]
        for folder in (out,source,data): folder.mkdir()
        for name,value in (('dataset.json',self.data),('original-prompts.json',self.old),('interior-prompts.json',self.new)):
            (data/name).write_bytes(s.blob(value))
        (source/'training-traces.json').write_bytes(s.blob(self.traces))
        (source/'validation-summary.json').write_bytes(s.blob(self.saved))
        torch.save(self.archive,source/'evaluations.pt')
        return out,source,data
    def write_expected(self,out):
        for name,item in zip(s.OUTPUTS,(s.manifest(),*self.expected),strict=True): (out/name).write_bytes(s.blob(item))

    def test_01_manifest_seal_fixed_scope_and_zero_neural_work(self):
        s.validate_seal(); self.assertEqual(s.identities(),p.identities()); self.assertEqual(s.DOMAINS,p.DOMAINS)
        self.assertEqual(s.manifest()['acceptance_base'],'a7174ae51f71f001901793603ab9f7ddb26ed923')
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.FULL_TESTS,s.MODULES),(p.SOURCE_COUNT+7,p.INPUT_COUNT+489+7,p.FULL_TESTS+64,p.MODULES+2))
        self.assertEqual(len(s.OWN),7); self.assertEqual(len(s.OUTPUTS),4)
        for key in ('train_steps','model_forward_calls','gradient_calls','optimizer_steps','model_state_loads','new_checkpoint_writes','network_calls'):
            self.assertEqual(s.WORK[key],0)
    def test_02_canonical_nonbinary_split_and_pair_metadata(self):
        self.assertEqual(self.data,fixtures.fixtures.data_fixture()); self.assertEqual(set(self.targets.tolist()),{48,49,50,51})
        self.assertEqual([len(self.data[split]) for split in s.SPLITS],[192,96])
        self.assertEqual([len(s.canonical_pairs(self.data[split])) for split in s.SPLITS],[96,48])
    def test_03_parent_negative_and_all_complete_normal_results_preserved(self):
        value = self.expected[2]; p.check_summary(value['parent_validation_summary'])
        self.assertEqual(s.blob(value['parent_validation_summary']),s.blob(self.saved))
        self.assertFalse(value['parent_validation_summary']['candidate_gate']); self.assertEqual(value['parent_validation_summary']['eligible_seed_count'],2)
        self.assertEqual((len(value['terminal']),len(value['terminal_contrasts'])),(120,60))
    def test_04_terminal_cross_entropy_matches_independent_logsumexp(self):
        logits = self.logits(); result = s.terminal_view(logits,self.data['TRAIN'])
        values = torch.logsumexp(logits,dim=1)-logits[torch.arange(192),self.targets]
        for row,(a,b) in zip(result,s.canonical_pairs(self.data['TRAIN']),strict=True):
            self.assertAlmostEqual(row['per_query_ce'][0],float(values[a]),places=13)
            self.assertAlmostEqual(row['per_query_ce'][1],float(values[b]),places=13)
            self.assertEqual(row['pair_max'],max(row['per_query_ce']))
            self.assertEqual(row['mean_ce'],math.fsum(row['per_query_ce'])/2)
    def test_05_all256_classes_remain_in_loss_and_argmax(self):
        z = self.logits().clone(); z[:,200] = 12.
        rows = s.terminal_view(z,self.data['TRAIN'])
        self.assertTrue(all(r['predictions'] == [200,200] and r['correct_answers'] == 0 for r in rows))
        self.assertTrue(all(r['mean_ce'] > 8. for r in rows))
    def test_06_pairing_survives_nonadjacent_row_permutation(self):
        ids = list(range(0,192,2))+list(range(1,192,2)); rows = [self.data['TRAIN'][i] for i in ids]
        actual = s.terminal_view(self.logits()[ids],rows); expected = s.terminal_view(self.logits(),self.data['TRAIN'])
        key = lambda row:tuple(row['row_ids'])
        self.assertEqual(s.blob(sorted(actual,key=key)),s.blob(sorted(expected,key=key)))
    def test_07_wrong_pair_metadata_is_rejected(self):
        rows = copy.deepcopy(self.data['TRAIN']); rows[0]['values'][0] = 9
        with self.assertRaises((ValueError,KeyError)): s.terminal_view(self.logits(),rows)
    def test_08_wrong_teacher_alignment_is_rejected(self):
        rows = copy.deepcopy(self.data['TRAIN']); rows[0]['target'] = rows[1]['target']
        with self.assertRaises(ValueError): s.terminal_view(self.logits(),rows)
    def test_09_terminal_shape_dtype_and_nonfinite_rejected(self):
        z = self.logits()
        for value in (z[:,:255],z.float(),z[:191],torch.full_like(z,float('nan')),torch.full_like(z,float('inf'))):
            with self.assertRaises(ValueError): s.terminal_view(value,self.data['TRAIN'])
    def test_10_exact_ties_keep_first256class_argmax_and_no_floor(self):
        result = s.terminal_view(torch.zeros_like(self.logits()),self.data['TRAIN'])
        self.assertTrue(all(r['predictions'] == [0,0] for r in result))
        self.assertAlmostEqual(result[0]['mean_ce'],math.log(256),places=14)
        z = torch.full_like(self.logits(),-1000.); z[torch.arange(192),self.targets] = 1000.
        self.assertTrue(all(r['mean_ce'] == 0. for r in s.terminal_view(z,self.data['TRAIN'])))
    def test_11_numerical_overflow_rejected_without_loss_repair(self):
        z = torch.full_like(self.logits(),1e308); z[torch.arange(192),self.targets] = -1e308
        with self.assertRaises(ValueError): s.terminal_view(z,self.data['TRAIN'])
    def test_12_complete_terminal_pairs_and_fitted_prompt_scope(self):
        pairs = self.expected[0]['pairs']; self.assertEqual(len(pairs),25920)
        self.assertEqual(sum(len(r['per_query_ce']) for r in pairs),51840)
        for row in self.expected[2]['terminal']:
            self.assertEqual(row['normal']['normal_prompt_seen_in_training'],row['split'] == 'TRAIN' and row['domain'] != 'original6')
            self.assertEqual(row['mean_ce']['count'],288 if row['split'] == 'TRAIN' else 144)
    def test_13_archive_normal_counts_bind_every_parent_state(self):
        saved = copy.deepcopy(self.saved); saved['seed_results'][0]['normal_by_domain']['original2']['TRAIN']['correct'] -= 1
        with self.assertRaises(ValueError): self.archive_check(self.archive,saved=saved)
    def test_14_archive_schema_order_omission_and_duplicates_rejected(self):
        for kind in ('schema','reverse','missing','duplicate'):
            archive = self.archive_copy()
            if kind == 'schema': archive['schema'] = 'fold-c342-evaluations-v1'
            elif kind == 'reverse': archive['records'].reverse()
            elif kind == 'missing': archive['records'].pop()
            else: archive['records'][1] = archive['records'][0]
            with self.assertRaises(ValueError): self.archive_check(archive)
    def test_15_state_trace_and_evaluation_policy_are_bound(self):
        for key,value in (('state_sha256','f'*64),('evaluation_policy','after')):
            archive = self.archive_copy(); archive['records'][0][key] = value
            with self.assertRaises(ValueError): self.archive_check(archive)
    def test_16_saved_replay_drift_and_argmax_flip_are_rejected(self):
        archive = self.archive_copy(); views = archive['records'][0]['raw']['replay']['interior']['TRAIN']['balanced']
        z = views['normal'].clone(); z[0,200] = 20.; views['normal'] = z
        with self.assertRaises(ValueError): self.archive_check(archive)
    def test_17_real_trace_verifier_is_dispatched_for_all_ten_states(self):
        with patch.object(p,'check_trace') as validate:
            result = s.trace_rows(self.traces,self.data,self.cx,self.tables,self.targets)
        self.assertEqual(validate.call_count,10); self.assertEqual(len(result),24000)
        for call,trace in zip(validate.call_args_list,self.traces,strict=True):
            self.assertIs(call.args[0],trace); self.assertIs(call.args[1],self.data['TRAIN'])
            self.assertIs(call.args[2],self.cx[-1]); self.assertIs(call.args[3],self.tables); self.assertIs(call.args[4],self.targets)
        # Invented traces are deliberately not accepted as real C344 trajectories.
        with self.assertRaises((ValueError,KeyError)): p.check_trace(self.traces[0],self.data['TRAIN'],self.cx[-1],self.tables,self.targets)
    def test_18_all24000_preupdate_rows_and12000_paired_steps_preserved(self):
        rows = self.expected[1]['rows']; paired = self.expected[1]['paired_rows']
        self.assertEqual((len(rows),len(paired)),(24000,12000))
        self.assertEqual(rows[2399]['step'],2400); self.assertEqual(rows[2399]['event_index'],1199)
        self.assertEqual(rows[2399]['mean_ce'],self.traces[0]['loss_history'][2399]['mean_ce'])
        self.assertEqual(self.expected[2]['source_trace_sha256'],s.digest(self.traces))
    def test_19_schedule_reconstruction_distinguishes_mixed_slot4(self):
        for row in self.rows:
            counts = row['domain_pairs']; self.assertEqual(sum(counts.values()),24); self.assertEqual(counts['original6'],0)
            if row['slot'] == 4:
                self.assertEqual(row['batch_kind'],'mixed_original45_interior4')
                self.assertTrue(5 <= counts['original4'] <= 8 and 5 <= counts['original5'] <= 8)
                self.assertTrue(11 <= counts['interior4'] <= 13)
            else:
                self.assertEqual(counts['original'+str(row['slot'])],24)
    def test_20_selected_loss_field_and_event_index_are_checked(self):
        for kind in ('selected','missing','event'):
            traces = self.trace_copy()
            if kind == 'selected': traces[0]['loss_history'][1]['selected'] += .01
            elif kind == 'missing': traces[0]['loss_history'][1].pop('pair_max')
            else: traces[0]['event_indices'][1] = 2
            with self.assertRaises(ValueError): self.trace_rows(traces)
    def test_21_norm_nonfinite_negative_or_boolean_rejected(self):
        for value in (float('nan'),float('inf'),-1.,True):
            traces = self.trace_copy(); traces[0]['preclip_norm_history'][0] = value
            with self.assertRaises(ValueError): self.trace_rows(traces)
    def test_22_fullclass_pairmax_bounds_are_not_silently_repaired(self):
        for value in (-.1,10.,float('nan'),True):
            traces = self.trace_copy(); traces[0]['loss_history'][1]['pair_max'] = value
            with self.assertRaises(ValueError): self.trace_rows(traces)
    def test_23_trace_cohort_lengths_and_step_order_are_complete(self):
        for kind in ('cohort','history','norm','index'):
            traces = self.trace_copy()
            if kind == 'cohort': traces.reverse()
            elif kind == 'history': traces[0]['loss_history'].pop()
            elif kind == 'norm': traces[0]['preclip_norm_history'].pop()
            else: traces[0]['event_indices'].reverse()
            with self.assertRaises(ValueError): self.trace_rows(traces)
    def test_24_paired_initial_weights_and_actual_inputs_remain_identical(self):
        for key in ('initial_sha256','actual_training_stream_sha256','pair_metadata_sha256'):
            traces = self.trace_copy(); traces[1][key] = 'different'
            with self.assertRaises(ValueError): self.trace_rows(traces)
    def test_25_paired_first_preupdate_objectives_are_equal(self):
        traces = self.trace_copy(); traces[1]['loss_history'][0]['mean_ce'] += .01
        with self.assertRaises(ValueError): self.trace_rows(traces)
    def test_26_all_fixed200_step_blocks_cover_whole_trajectory(self):
        rows = self.expected[2]['trace_blocks_summary']; self.assertEqual(len(rows),120)
        self.assertEqual(sum(r['steps'] for r in rows),24000)
        self.assertTrue(all(r['steps'] == 200 and r['last_step']-r['first_step'] == 199 for r in rows))
        self.assertEqual({r['block'] for r in rows},set(range(1,13)))
    def test_27_cycle_slot_profile_groups_conserve_all_pairs(self):
        rows = self.expected[2]['trace_groups_summary']; self.assertEqual(len(rows),180)
        for seed,arm in s.identities():
            group = [r for r in rows if (r['seed'],r['arm']) == (seed,arm)]
            self.assertEqual(sum(r['steps'] for r in group),2400)
            self.assertEqual({d:sum(r['domain_pairs'][d] for r in group) for d in s.DOMAINS},
                {d:96*n for d,n in p.manifest()['actual_per_row_exposure'].items()})
    def test_28_paired_differences_compare_same_metric_and_count_exact_signs(self):
        row = self.expected[2]['paired_blocks'][0]
        self.assertNotIn('selected',row['metrics']); self.assertEqual(row['metrics']['mean_ce']['zero'],1)
        self.assertEqual(row['metrics']['mean_ce']['positive'],199)
        self.assertAlmostEqual(row['metrics']['mean_ce']['mean'],.05*199/200,places=14)
        self.assertEqual(row['control_norm_gt1'],66); self.assertEqual(row['candidate_norm_gt1'],66)
    def test_29_summary_parent_and_normal_count_tampering_rejected(self):
        for kind in ('parent','normal'):
            value = self.summary_copy()
            if kind == 'parent': value['parent_validation_summary']['candidate_gate'] = True
            else: value['terminal'][0]['normal']['correct'] -= 1
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_30_terminal_objective_deltas_bind_both_arms(self):
        value = self.summary_copy(); value['terminal_contrasts'][0]['mean_ce_delta'] += 1.
        with self.assertRaises(ValueError): s.check_summary(value)
        value = self.summary_copy(); value['terminal'][0]['pair_max']['count'] -= 1
        with self.assertRaises(ValueError): s.check_summary(value)
    def test_31_trace_partition_and_selected_metric_tampering_rejected(self):
        for kind in ('boundary','mean','norm','exposure'):
            value = self.summary_copy(); row = value['trace_blocks_summary'][0]
            if kind == 'boundary': row['first_step'] = 2
            elif kind == 'mean': row['metrics']['mean_ce']['mean'] += .01
            elif kind == 'norm': row['norm_gt1'] -= 1
            else: row['domain_pairs']['original6'] = 1
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_32_paired_sign_counts_and_direction_tampering_rejected(self):
        for kind in ('sign','mean','side'):
            value = self.summary_copy(); row = value['paired_blocks'][0]
            if kind == 'sign': row['metrics']['mean_ce']['positive'] += 1
            elif kind == 'mean': row['metrics']['mean_ce']['mean'] *= -1
            else: row['control_norm_gt1'] -= 1
            with self.assertRaises(ValueError): s.check_summary(value)
    def test_33_actual_loader_reads_exact_parent_traces_and_eval_bundle(self):
        with tempfile.TemporaryDirectory() as folder:
            _,source,data = self.paths(folder); reader = Mock(side_effect=read)
            with patch.object(torch,'load',wraps=torch.load) as load:
                result = s.load_inputs(source,data,self.cx,reader)
            self.assertEqual(load.call_count,1); self.assertEqual(load.call_args.args[0],source/'evaluations.pt')
            self.assertTrue(load.call_args.kwargs['weights_only'])
            self.assertEqual(sum(call.args[0] == source/'training-traces.json' for call in reader.call_args_list),1)
            self.assertEqual(s.digest(result[0]),s.digest(self.traces)); self.assertEqual(result[3],self.data)
    def test_34_run_contract_computes_before_any_output_write(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            with patch.object(s,'reconstructed',side_effect=ValueError('invalid source')) as reconstruct:
                with self.assertRaises(ValueError): s.run_diagnostic(out,out,out,self.cx,read)
            self.assertEqual(list(out.iterdir()),[]); reconstruct.assert_called_once_with(out,out,self.cx,read)
        self.assertEqual(len(inspect.signature(s.run_diagnostic).parameters),5)
        self.assertEqual(len(inspect.signature(s.semantic_recheck).parameters),5)
    def test_35_production_saved_loader_writer_and_reconstruction_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            out,source,data = self.paths(folder)
            with patch.object(p,'check_trace'),self.cx[-1].guarded.no_neural():
                result = s.run_diagnostic(out,source,data,self.cx,read)
                replay = s.semantic_recheck(out,source,data,self.cx,read)
            self.assertEqual(s.blob(result),s.blob(self.expected[2])); self.assertEqual(s.blob(replay),s.blob(result))
            self.assertEqual({path.name for path in out.iterdir()},set(s.OUTPUTS))
    def test_36_any_saved_diagnostic_artifact_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder); self.write_expected(out)
            with patch.object(s,'reconstructed',return_value=self.expected):
                for name in s.OUTPUTS:
                    before = (out/name).read_bytes(); (out/name).write_bytes(s.blob({'altered':True}))
                    with self.assertRaises(ValueError): s.semantic_recheck(out,out,out,self.cx,read)
                    (out/name).write_bytes(before)
    def test_37_source_mutation_is_detected_around_analysis(self):
        for kind in ('trace','token','empty_family'):
            traces = self.trace_copy(); tables = fixtures.tree_copy(self.tables)
            arm = next(iter(tables)); family = next(iter(tables[arm])); key = next(iter(tables[arm][family]))
            tables[arm][family][key] = tables[arm][family][key].clone()
            payload = (traces,self.archive,self.saved,self.data,tables,self.targets)
            def malicious(*args):
                if kind == 'trace': traces[0]['loss_history'][0]['mean_ce'] += 1.
                elif kind == 'token': tables[arm][family][key][0,0] += 1
                else: tables[arm]['empty_added_family'] = {}
                return self.expected
            with patch.object(s,'load_inputs',return_value=payload),patch.object(s,'analyze',side_effect=malicious) as analyze:
                with self.assertRaises(ValueError): s.reconstructed(Path('.'),Path('.'),self.cx,read)
            analyze.assert_called_once()
    def test_38_harmful_objective_and_accuracy_values_are_valid_diagnostic_data(self):
        value = self.expected[2]; s.check_summary(value)
        harmful = [r for r in value['terminal_contrasts'] if r['domain'] == 'interior4' and r['seed'] in s.SEEDS[:3]]
        self.assertTrue(all(r['mean_ce_delta'] > 0 and r['pair_max_delta'] > 0 and r['parent_contrast']['answer_gain'] < 0 for r in harmful))
        self.assertTrue(value['diagnostic_complete']); self.assertFalse(value['parent_validation_summary']['candidate_gate'])
    def test_39_console_report_publishes_all_groups_without_selection(self):
        emit = Mock(); result = s.report_results(self.expected[2],emit)
        counts = {label:sum(call.args[0] == label for call in emit.call_args_list) for label in
            ('C345 terminal objective','C345 terminal contrast','C345 trace block','C345 trace group','C345 paired trace block','C345 paired trace group')}
        self.assertEqual(list(counts.values()),[120,60,120,180,60,90]); self.assertEqual(result,s.WORK)
        self.assertEqual(emit.call_count,631)
    def test_40_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder); self.write_expected(out); before = {name:(out/name).read_bytes() for name in s.OUTPUTS}
            with patch.object(s,'reconstructed',return_value=self.expected):
                with self.assertRaises(FileExistsError): s.run_diagnostic(out,out,out,self.cx,read)
            self.assertTrue(all((out/name).read_bytes() == raw for name,raw in before.items()))


if __name__ == '__main__':
    unittest.main()
