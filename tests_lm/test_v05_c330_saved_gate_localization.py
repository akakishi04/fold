"""C330 software fixtures. Synthetic metrics/parent/leases are not FOLD results."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import itertools
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
from fold_lm.v05_benchmarks import model_c330_saved_gate_localization as s

ROOT=Path(__file__).resolve().parents[1]
_loader=importlib.util.spec_from_file_location('_c330_test_executor',ROOT/'tools/c330_execution.py')
e=importlib.util.module_from_spec(_loader);_loader.loader.exec_module(e)


def score(mode='pass'):
    cells=[];orders=[];totals=[]
    for split,profile,lang in itertools.product(s.SPLITS,s.SCORER_PROFILES,s.LANGUAGES):
        n=16 if split=='TRAIN' else 8
        correct=n if mode in ('pass','mask_only') else n*3//4
        both=n//2 if correct==n else n//4
        ed=0. if mode=='mask_only' else .25 if mode=='mixed' else .75
        qd=.5 if mode in ('pass','mask_only') else .25 if mode=='mixed' else .75
        for entities in s.SUBSETS:
            for perm in (entities,entities[::-1]):
                cells.append(dict(split=split,profile=profile,language=lang,entities=list(entities),permutation=list(perm),
                    rows=n,correct=correct,accuracy=correct/n,query_pair_accuracy=both/(n//2),collapsed_pairs=0,pairs=n//2,
                    evidence_drop=ed,query_drop=qd,answer_nll=.03,passed=mode=='pass'))
            order_correct=n if correct==n else n//2
            orders.append(dict(split=split,profile=profile,language=lang,entities=list(entities),groups=n,
                both_correct=order_correct,accuracy=order_correct/n,passed=order_correct/n>=.80))
        totals.append(dict(split=split,profile=profile,language=lang,rows=n*6,correct=correct*6,pairs=n//2*6,collapsed_pairs=0))
    return dict(cells=cells,two_order=orders,totals=totals,passed=mode=='pass')


def fixture(control_mode='pass',candidate_mode='pass'):
    metrics=[]
    for seed,arm in itertools.product(s.SEEDS,s.ARMS):
        mode=control_mode if arm=='prefix1200' else candidate_mode
        metrics.append(dict(seed=seed,arm=arm,original={str(n):score(mode) for n in range(2,7)},interior=score(mode),single_character={}))
    return metrics,reference_summary(metrics)


def reference_summary(metrics):
    flags=[];pairs=[]
    for r in metrics:
        flags.append(dict(seed=r['seed'],arm=r['arm'],original_pass={n:v['passed'] for n,v in r['original'].items()},
            interior_pass=r['interior']['passed'],retention_pass=all(v['passed'] for v in r['original'].values())))
    def held(score):
        cc=[r for r in score['cells'] if r['split']=='HOLDOUT']
        return sum(r['correct'] for r in cc),int(sum(r['query_pair_accuracy']*r['pairs'] for r in cc))
    def compare(a,c):
        ac,ap=held(a);cc,cp=held(c)
        return dict(answers=288,query_pairs=144,control_correct=ac,candidate_correct=cc,control_both_correct=ap,candidate_both_correct=cp,
            answer_gain=cc-ac,query_pair_gain=cp-ap,rescued=max(cc-ac,0),regressed=max(ac-cc,0),pair_rescued=max(cp-ap,0),pair_regressed=max(ap-cp,0))
    for i,seed in enumerate(s.SEEDS):
        a,c=metrics[2*i:2*i+2];old={n:compare(a['original'][n],c['original'][n]) for n in a['original']};inside=compare(a['interior'],c['interior'])
        og=sum(v['answer_gain'] for v in old.values());pg=sum(v['query_pair_gain'] for v in old.values())
        passed=flags[2*i+1]['interior_pass'] and flags[2*i+1]['retention_pass'] and inside['answer_gain']>0 and inside['query_pair_gain']>0 and og>=0 and pg>=0
        pairs.append(dict(seed=seed,control_interior_pass=flags[2*i]['interior_pass'],candidate_interior_pass=flags[2*i+1]['interior_pass'],
            control_retention_pass=flags[2*i]['retention_pass'],candidate_retention_pass=flags[2*i+1]['retention_pass'],interior=inside,
            original_by_length=old,original_answer_gain=og,original_pair_gain=pg,interior_answer_gain=inside['answer_gain'],
            interior_pair_gain=inside['query_pair_gain'],paired_success=passed,shared_prefix_preserved=True))
    return dict(seed_results=flags,paired_comparisons=pairs,candidate_gate=all(r['paired_success'] for r in pairs),paired_success_count=sum(r['paired_success'] for r in pairs))


def parent_fixture():
    pins={**e.BOOTSTRAP,**{f'p{i}':'a'*40 for i in range(832-len(e.BOOTSTRAP))}}
    inputs={f'i{i}':'b'*64 for i in range(1577)}
    r=dict(schema='fold-c329-science-v1',experiment_id='parent',stage='stage',commit_sha=e.PARENT_EXECUTION,status='FAIL',
        diagnostic_execution_valid=True,gate_f_candidate=False,production_adoption=False,source_blobs=dict(pins),input_sha256=dict(inputs),
        manifest_sha256='c'*64,validation_summary={'candidate_gate':False,'paired_success_count':1})
    v=dict(schema='fold-c329-execution-envelope-v1',commit_sha=e.PARENT_EXECUTION,scientific_summary_sha256=e.PARENT_SUMMARY,
        scientific_status='FAIL',source_count=832,input_count=1577,source_blobs=pins,input_sha256=inputs,manifest_sha256='c'*64,
        scientific_work={'models':5},parent_summary_sha256='d'*64,parent_envelope_sha256='f'*64,
        immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=1577,hash_stats={'final_reference_rechecks':1577},
        regression=dict(commit_sha=e.PARENT_EXECUTION,tests=5770,failures=0,errors=0,skipped=0,successful=True))
    p=NS(validate_seal=lambda:None,EXPERIMENT_ID='parent',STAGE='stage',OWN=(e.P_PATH,e.E_PATH),MANIFEST_SHA='c'*64,WORK={'models':5})
    helper=NS(check_validation=lambda v:None,BOOTSTRAP={},PARENT_SUMMARY='d'*64,PARENT_ENVELOPE='f'*64)
    return r,v,p,helper


def receipt():return dict(commit_sha='a'*40,tests=s.FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C330 fixture'),('config','user.email','c330@example.invalid')]:
        subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    (root/'docs').mkdir();(root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC330 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
    return e.git(root,'rev-parse','HEAD')


class C330Tests(unittest.TestCase):
    def test_01_manifest_and_tamper(self):
        s.validate_seal()
        with patch.object(s,'THRESHOLDS',(.89,.8,.35,.35)),self.assertRaises(ValueError):s.validate_seal()
    def test_02_semantic_scope_and_zero_model_work(self):
        self.assertEqual(s.WORK['local_cells'],5*2*6*72);self.assertEqual(s.WORK['order_cells'],5*2*6*36)
        self.assertEqual(s.WORK['local_transitions'],5*6*72);self.assertEqual(s.WORK['order_transitions'],5*6*36)
        for k in ('train_steps','model_forward_calls','gradient_calls','model_state_loads','optimizer_steps','new_checkpoint_writes'):self.assertEqual(s.WORK[k],0)
        self.assertEqual(s.SOURCE_COUNT,832+6);self.assertEqual(s.INPUT_COUNT,1577+10+6);self.assertEqual(s.FULL_TESTS,5770+s.OWN_TESTS)
    def test_03_exact_profile_semantics(self):
        for domain in s.DOMAINS:
            cc,_,_=s.adapted_score(score(),domain)
            names=s.INTERIOR_PROFILES if domain=='interior4' else s.ORIGINAL_PROFILES
            self.assertEqual({r['profile']:r['input_profile'] for r in cc},dict(zip(s.SCORER_PROFILES,names)))
            self.assertTrue(all(r['name_family_seen_in_training']==(domain not in ('original5','original6')) for r in cc))
    def test_04_number_type_rejections(self):
        for v in (True,float('nan'),float('inf'),'1'):
            with self.subTest(),self.assertRaises(ValueError):s.number(v,0,1,'value')
    def test_05_exact_threshold_boundaries(self):
        values=dict(zip(s.CRITERIA,s.THRESHOLDS));self.assertFalse(any(s.failure_flags(values).values()))
        for key in s.CRITERIA:
            v=dict(values);v[key]-=1e-12;self.assertTrue(s.failure_flags(v)[key])
    def test_06_four_exclusive_patterns(self):
        for mode in s.PATTERNS:
            cc,_,_=s.adapted_score(score(mode),'original4');self.assertEqual({r['pattern'] for r in cc},{mode})
    def test_07_flag_schema_rejection(self):
        for flags in ({},dict.fromkeys(s.CRITERIA,0)):
            with self.subTest(),self.assertRaises(ValueError):s.pattern(flags)
    def test_08_local_writer_schema_exact(self):
        row=score()['cells'][0];row['new_field']=1
        with self.assertRaises(ValueError):s.local_cell(row)
    def test_09_source_cell_order_not_matching_policy(self):
        a=score();b=copy.deepcopy(a);b['cells'].reverse();b['two_order'].reverse()
        self.assertEqual(s.adapted_score(a,'original2'),s.adapted_score(b,'original2'))
    def test_10_duplicate_coordinates_rejected(self):
        z=score();z['cells'][-1]=copy.deepcopy(z['cells'][0])
        with self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_11_missing_coordinates_rejected(self):
        z=score();z['two_order'].pop()
        with self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_12_outside_coordinate_rejected(self):
        z=score();z['cells'][0]['profile']='quadrupled'
        with self.assertRaises(ValueError):s.adapted_score(z,'original4')
    def test_13_bool_entity_not_integer(self):
        z=score();z['cells'][0]['entities'][0]=False
        with self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_14_normal_count_binding(self):
        for k,v in [('rows',15),('pairs',7),('correct',True),('accuracy',.9375)]:
            row=score()['cells'][0];row[k]=v
            with self.subTest(),self.assertRaises(ValueError):s.local_cell(row)
    def test_15_query_pair_grid(self):
        row=score()['cells'][0];row['query_pair_accuracy']=.91
        with self.assertRaises(ValueError):s.local_cell(row)
    def test_16_query_pair_joint_count_constraints(self):
        row=score()['cells'][0];row['query_pair_accuracy']=.5
        with self.assertRaises(ValueError):s.local_cell(row)
    def test_17_collapse_does_not_include_both_correct(self):
        row=score()['cells'][0];row['collapsed_pairs']=1
        with self.assertRaises(ValueError):s.local_cell(row)
    def test_18_masked_accuracy_reconstructed_and_validated(self):
        row=s.local_cell(score()['cells'][0]);self.assertEqual(row['evidence_blind_correct'],4);self.assertEqual(row['query_blind_correct'],8)
        for value in (.333,1.1):
            row=score()['cells'][0];row['evidence_drop']=value
            with self.subTest(),self.assertRaises(ValueError):s.local_cell(row)
    def test_19_nonfinite_or_negative_nll(self):
        for v in (-.1,float('nan'),True):
            row=score()['cells'][0];row['answer_nll']=v
            with self.subTest(),self.assertRaises(ValueError):s.local_cell(row)
    def test_20_saved_pass_cannot_override_criteria(self):
        row=score('mask_only')['cells'][0];row['passed']=True
        with self.assertRaises(ValueError):s.local_cell(row)
    def test_21_order_counts_and_flags(self):
        for k,v in [('both_correct',15),('accuracy',.8),('passed',False),('groups',8)]:
            z=score();z['two_order'][0][k]=v
            with self.subTest(),self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_22_order_cannot_contradict_normal_answers(self):
        z=score();row=z['two_order'][0];row.update(both_correct=8,accuracy=.5,passed=False);z['passed']=False
        with self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_23_totals_conservation(self):
        z=score();z['totals'][0]['correct']-=1
        with self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_24_domain_pass_not_average(self):
        z=score('mixed');z['passed']=True
        with self.assertRaises(ValueError):s.adapted_score(z,'original2')
    def test_25_complete_analysis_parent_reconciled_and_inputs_immutable(self):
        args=fixture('normal_binding_only','pass');before=s.digest(args);loc,trans,summary=s.analyze(*args)
        self.assertEqual(len(loc['cells']),4320);self.assertEqual(len(loc['two_order']),2160)
        self.assertEqual(len(trans['local']),2160);self.assertEqual(len(trans['two_order']),1080)
        self.assertTrue(summary['parent_candidate_gate']);self.assertEqual(summary['parent_paired_success_count'],5)
        self.assertEqual(s.digest(args),before)
    def test_26_checkpoint_selection_rejected(self):
        args=fixture();args[0].pop()
        with self.assertRaises(ValueError):s.analyze(*args)
    def test_27_parent_deciding_counts_reconciled(self):
        args=fixture();args[1]['paired_comparisons'][0]['interior']['candidate_correct']-=1
        with self.assertRaises(ValueError):s.analyze(*args)
    def test_28_parent_flags_and_fixed_gate_unchanged(self):
        args=fixture();args[1]['seed_results'][0]['interior_pass']=False
        with self.assertRaises(ValueError):s.analyze(*args)
        args=fixture();args[1]['candidate_gate']=True
        with self.assertRaises(ValueError):s.analyze(*args)
    def test_29_transition_keeps_rescue_and_regression(self):
        a=s.local_cell(score('normal_binding_only')['cells'][0]);c=s.local_cell(score('mask_only')['cells'][0])
        r=s.transition(a,c);self.assertEqual(r['rescued'],['accuracy','query_pair_accuracy']);self.assertEqual(r['regressed'],['evidence_drop'])
        self.assertFalse(r['control_pass']);self.assertFalse(r['candidate_pass'])
    def test_30_transition_requires_exact_coordinates(self):
        a=s.local_cell(score()['cells'][0]);c=copy.deepcopy(a);c['permutation'].reverse()
        with self.assertRaises(ValueError):s.transition(a,c)
    def test_31_overlapping_criteria_not_independent_failure_counts(self):
        _,_,v=s.analyze(*fixture('mixed','mixed'));row=v['strata'][0]
        self.assertEqual(row['failed_cells'],30);self.assertEqual(sum(row['criteria'].values()),120)
        self.assertEqual(row['patterns'],{'pass':0,'normal_binding_only':0,'mask_only':0,'mixed':30})
    def test_32_summary_inventory_and_partition(self):
        _,_,v=s.analyze(*fixture())
        for kind in ('count','strata','transition'):
            bad=copy.deepcopy(v)
            if kind=='count':bad['local_cells']-=1
            elif kind=='strata':bad['strata'][0]['patterns']['pass']-=1
            else:bad['transition_summary'][0]['stable_pass']-=1
            with self.subTest(),self.assertRaises(ValueError):s.check_summary(bad)
    def test_33_actual_writer_loader_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);po=root/'parent';out=root/'child';po.mkdir();out.mkdir();metrics,summary=fixture('mixed','pass')
            e.save(po/'measurements.json',metrics);e.save(po/'validation-summary.json',summary)
            v=s.run_diagnostic(out,po,e.read);self.assertEqual(v,s.semantic_recheck(out,po,e.read));self.assertEqual(set(p.name for p in out.iterdir()),set(s.OUTPUTS))
            with self.assertRaises(FileExistsError):s.run_diagnostic(out,po,e.read)
    def test_34_saved_diagnostic_semantic_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);po=root/'p';out=root/'c';po.mkdir();out.mkdir();m,v=fixture()
            e.save(po/'measurements.json',m);e.save(po/'validation-summary.json',v);s.run_diagnostic(out,po,e.read)
            (out/'transitions.json').write_text('{}',encoding='utf-8')
            with self.assertRaises(ValueError):s.semantic_recheck(out,po,e.read)
    def test_35_output_byte_binding(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
            self.assertEqual(e.bound_semantics(out,lambda:1)[0],1)
            def mutate():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,mutate)
    def test_36_utf8_strict_json_exclusive_writes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';e.save(p,{'名前':'甲乙'});self.assertEqual(e.read(p),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(p,{})
            for text in ('{"x":1,"x":2}','NaN','Infinity'):
                p.write_text(text,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError):e.read(p)
    def test_37_lf_crlf_and_mutation(self):
        raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in (raw,raw.replace(b'\n',b'\r\n')):p.write_bytes(text);self.assertEqual(e.source_bytes(p,oid),text)
            for text in (b'bad',b'a\nb\r\n'):
                p.write_bytes(text)
                with self.subTest(),self.assertRaises(ValueError):e.source_bytes(p,oid)
    def test_38_real_git_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);head=git_fixture(root);e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,'a'*40)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError):e.guard(root,head)
    def test_39_formal_unique_active_and_launcher(self):
        self.assertTrue(e.active('## Formal state\nC330 ACTIVE / NOT YET JUDGED\n## History\nC329 ACTIVE / NOT YET JUDGED'))
        for t in ('## History\nC330 ACTIVE / NOT YET JUDGED','## Formal state\nC329 ACTIVE / NOT YET JUDGED','## Formal state\nC330 ACTIVE / NOT YET JUDGED\nC331 ACTIVE / NOT YET JUDGED'):self.assertFalse(e.active(t))
        text=(ROOT/'tools/invoke_c330.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C330',text);self.assertIn('run_c330.ps1',text)
    def test_40_actual_own_suite_semantic_count(self):
        class Case(unittest.TestCase):
            def __init__(self,i):super().__init__();self.number=i
            def id(self):return 'fixture.'+str(self.number)
        def flatten(suite):
            for t in suite:
                if isinstance(t,unittest.TestSuite):yield from flatten(t)
                else:yield t
        inherited=[Case(i) for i in range(5770)];helper=NS(suite=lambda *a:inherited)
        b=NS(EXCLUDED='excluded',regression_modules=lambda r:list(range(210)));r6=NS(flatten=flatten,RECOVERY_MODULES=('a','b','c'))
        self.assertEqual(e.suite(ROOT,b,helper,None,None,None,None,r6).countTestCases(),s.FULL_TESTS)
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),s.OWN_TESTS)
        inherited[-1]=inherited[0]
        with self.assertRaises(ValueError):e.suite(ROOT,b,helper,None,None,None,None,r6)
    def test_41_actual_helper_loader_checks_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'p.py';raw=b'def helpers(root):\n    return (1,2,3,4,5,6)\n';p.write_bytes(raw)
            oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            with patch.object(e,'E_PATH','p.py'),patch.object(e,'BOOTSTRAP',{'p.py':oid}),patch.object(e,'git',return_value=oid):
                self.assertEqual(e.helpers(root)[1:],(1,2,3,4,5,6));p.write_bytes(b'bad')
                with self.assertRaises(ValueError):e.helpers(root)
    def test_42_parent_valid_negative_and_partial_success(self):e.parent_contract(*parent_fixture())
    def test_43_parent_wrong_schema_flags_counts_or_receipts(self):
        for target,key,value in [(0,'schema','fold-c328-science-v1'),(0,'status','PASS'),(0,'diagnostic_execution_valid',False),(1,'source_count',826),(1,'input_count',1561),(1,'final_reference_rechecks',1576),(1,'saved_semantic_reconstruction',False)]:
            args=parent_fixture();args[target][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[1]['regression']['skipped']=1
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_44_parent_direct_pin_protection(self):
        args=parent_fixture();args[0]['source_blobs'][e.P_PATH]='0'*40;args[1]['source_blobs'][e.P_PATH]='0'*40
        with self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[1]['scientific_summary_sha256']='bad'
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_45_parent_writer_loader_signature(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True);data={'TRAIN':[]};old={};new={}
            for n,v in [('dataset.json',data),('original-prompts.json',old),('interior-prompts.json',new)]:e.save(out/n,v)
            p=NS(OUTPUTS=('dataset.json','original-prompts.json','interior-prompts.json'),blob=s.blob,semantic_recheck=Mock(return_value=([],{'candidate_gate':False})))
            b=NS(digest=s.digest,DATA_SHA=s.digest(data),PROMPTS_SHA=s.digest(old))
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda *a:None)))
            cx=(None,None,NS(new_prompts=lambda *a:new,check_prompts=lambda *a:None),None,x)
            e.parent_semantics(root,{'validation_summary':{'candidate_gate':False}},p,b,cx,{e.canonical(out/n):e.sha(out/n) for n in p.OUTPUTS})
            self.assertEqual(p.semantic_recheck.call_args.args,(out,data,old,new,cx,e.read))
    def test_46_actual_worker_diagnostic_not_capability(self):self.worker_fixture(False)
    def test_47_actual_worker_failed_regression_stops_diagnostic(self):self.worker_fixture(True)
    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);folder=root/'runs/x';folder.mkdir(parents=True);calls=[]
            pins={f'p{i}':'a'*40 for i in range(s.SOURCE_COUNT)};inputs={str(root/f'i{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={};stats={'final_reference_rechecks':s.INPUT_COUNT}
                def __init__(self,*a,**kw):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            r4=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),);b=NS(context=lambda:cx,check_dependencies=lambda *a:None,peak_rss=lambda:1)
            _,_,value=s.analyze(*fixture());p=NS(base=lambda:b)
            def snap(*a):calls.append('snapshot');return {'validation_summary':{'candidate_gate':False,'paired_success_count':0}},{},pins,inputs
            def parent_data(*a):calls.append('parent')
            def tests(*a):
                calls.append('tests');r=receipt()
                if bad:r.update(failures=1,successful=False)
                e.save(folder/'regression-result.json',r)
            def diag(out,*a):
                calls.append('diagnose')
                for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
                return value
            def saved(*a):calls.append('saved');return value
            runtime=NS(__version__='synthetic')
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(NS(),NS(),NS(),NS(native_runtime=lambda:(runtime,runtime)),NS(),r4,None)),patch.object(s,'parent',return_value=p),patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=parent_data),patch.object(e,'subprocess_run',side_effect=tests),patch.object(s,'run_diagnostic',side_effect=diag),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError):e.scientific_worker(root,folder,'a'*40)
                    self.assertNotIn('diagnose',calls)
                else:
                    e.scientific_worker(root,folder,'a'*40)
                    self.assertEqual(calls,['snapshot','parent','tests','diagnose','saved','final','release'])
                    child=e.read(folder/'science/summary.json');self.assertEqual(child['status'],'PASS');self.assertFalse(child['capability_gate_applicable']);self.assertFalse(child['validation_summary']['parent_candidate_gate'])
    def test_48_controller_no_retry_cli_failure_and_pure_diagnostic(self):
        for bad in (False,True):
            with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run',side_effect=ValueError('stop') if bad else None) as child,contextlib.redirect_stdout(io.StringIO()) as out:
                root=Path(d)
                if bad:
                    with self.assertRaises(ValueError):e.run(root,root/'runs/x','a'*40)
                    self.assertEqual(child.call_count,1);self.assertIn('run_execution_valid = false',out.getvalue())
                else:e.run(root,root/'runs/x','a'*40);self.assertEqual([r.args[-1] for r in child.call_args_list],['science','verify'])
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):e.subprocess_run(ROOT,Path(d),'a'*40,'invalid-mode')
            self.assertIn('invalid choice',(Path(d)/'invalid-mode.log').read_text(encoding='utf-8'))
        self.assertNotIn('torch',inspect.getsource(s.run_diagnostic));self.assertIn('load_parent_measurements',inspect.getsource(s.run_diagnostic))
        self.assertNotIn('patch',inspect.getsource(e.scientific_worker))


if __name__=='__main__':unittest.main()
