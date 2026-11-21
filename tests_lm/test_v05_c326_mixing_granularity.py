"""C326 authoring tests. Native-worker fixtures are explicitly synthetic, not science."""
from __future__ import annotations
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import numpy as np
import torch
from fold_lm.v05_benchmarks import model_c326_mixing_granularity as s

ROOT=Path(__file__).resolve().parents[1]
_loader=importlib.util.spec_from_file_location('_c326_execution_tests',ROOT/'tools/c326_execution.py')
e=importlib.util.module_from_spec(_loader); _loader.loader.exec_module(e)


def events(order=326101):
    value=torch.empty((1200,24,4),dtype=torch.int64); pairs=torch.arange(192).reshape(96,2)
    for epoch in range(300):
        rank=torch.randperm(96,generator=torch.Generator().manual_seed(order+306000+epoch))
        n=(2,3,4)[epoch%3]; p=(epoch//3+n-2)%3
        for j in range(4):
            v=value[4*epoch+j]; v[:,0]=n; v[:,1]=p; v[:,2:]=pairs[rank[24*j:24*j+24]]
    return value


def gate_rows():
    return [dict(seed=k,candidate_interior_pass=True,candidate_retention_pass=True,
        original_answer_gain=0,original_pair_gain=0,interior_answer_gain=1,interior_pair_gain=1) for k in s.SEEDS]


def contrast(gain):
    return dict(answers=288,query_pairs=144,control_correct=100,candidate_correct=100+gain,
        control_both_correct=50,candidate_both_correct=50+gain,rescued=gain,regressed=0,
        pair_rescued=gain,pair_regressed=0,answer_gain=gain,query_pair_gain=gain)


def validation():
    rows=[]; pairs=[]
    for seed in s.SEEDS:
        for arm in s.ARMS:
            passed={str(n):True for n in range(2,7)}
            rows.append(dict(seed=seed,arm=arm,original_pass=passed,retention_pass=True,interior_pass=arm=='batch4'))
        pairs.append(dict(seed=seed,control_retention_pass=True,candidate_retention_pass=True,control_interior_pass=False,
            candidate_interior_pass=True,original_answer_gain=0,original_pair_gain=0,interior_answer_gain=1,interior_pair_gain=1,
            interior=contrast(1),original_by_length={str(n):contrast(0) for n in range(2,7)},paired_success=True))
    return dict(candidate_gate=True,paired_success_count=5,seed_results=rows,paired_comparisons=pairs,
        all_pairs_matched=True,all_replays=True,all_family_exposures_matched=True,**s.WORK)


def parent_fixture():
    pins={**e.BOOTSTRAP,**{f'p{i}':'a'*40 for i in range(808-len(e.BOOTSTRAP))}}
    inputs={f'input{i}':'b'*64 for i in range(1517)}
    result=dict(schema='fold-c325-science-v1',experiment_id='parent-id',stage='parent-stage',commit_sha=e.PARENT_EXECUTION,
        status='FAIL',validation_summary={'candidate_gate':False},diagnostic_execution_valid=True,gate_f_candidate=False,
        production_adoption=False,source_blobs=dict(pins),input_sha256=dict(inputs),manifest_sha256='c'*64)
    envelope=dict(schema='fold-c325-execution-envelope-v1',commit_sha=e.PARENT_EXECUTION,scientific_summary_sha256=e.PARENT_SUMMARY,
        scientific_status='FAIL',source_count=808,input_count=1517,source_blobs=pins,input_sha256=inputs,
        manifest_sha256='c'*64,scientific_work={'models':10},parent_summary_sha256='d'*64,parent_envelope_sha256='f'*64,
        immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=1517,hash_stats={'final_reference_rechecks':1517},
        regression=dict(commit_sha=e.PARENT_EXECUTION,tests=5546,failures=0,errors=0,skipped=0,successful=True))
    p=NS(validate_seal=lambda:None,EXPERIMENT_ID='parent-id',STAGE='parent-stage',OWN=(e.P_PATH,e.E_PATH),MANIFEST_SHA='c'*64,WORK={'models':10})
    helper=NS(check_validation=lambda r:None,PARENT_SUMMARY='d'*64,PARENT_ENVELOPE='f'*64)
    return result,envelope,p,helper


def receipt(): return dict(commit_sha='a'*40,tests=s.FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C326 fixture'),('config','user.email','c326@example.invalid')]:
        subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    (root/'docs').mkdir(); (root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC326 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True); subprocess.run(['git','-C',str(root),'commit','-qm','synthetic fixture'],check=True)
    return e.git(root,'rev-parse','HEAD')


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear=torch.nn.Linear(64,256,bias=False,dtype=torch.float64)
    def forward(self,tokens,tasks): return self.linear(tokens.to(torch.float64)/64)


def toy_inputs():
    torch.manual_seed(9); m=Toy(); a=torch.arange(192*64).reshape(192,64)%7; b=a.flip(1)+2
    tables={'original':{(4,'repeat'):a},'interior4':{(4,'repeat'):b}}
    ev=torch.zeros((1,24,4),dtype=torch.int64); ev[:,:,0]=4; ev[:,:,2:]=torch.arange(48).reshape(1,24,2)
    def logits(z,n): s.require(z.shape==(n,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),'toy finite logits')
    x=NS(policy=NS(optimizer_for=lambda model,p:torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=0.),
                   verify_optimizer=lambda *args:None),c=NS(p267=NS(check_logits=logits)))
    return m,tables,torch.arange(192)%4+48,ev,x


class C326Tests(unittest.TestCase):
    def test_01_manifest(self): s.validate_seal()
    def test_02_manifest_detects_mutation(self):
        with patch.object(s,'STAGE','changed'),self.assertRaises(ValueError): s.validate_seal()
    def test_03_fresh_cohort(self):
        self.assertEqual(s.SEEDS,tuple(range(326001,326006))); self.assertEqual(s.ORDERS,tuple(range(326101,326106)))
        self.assertEqual(len(set(s.identities())),10)
    def test_04_work_and_protection(self):
        self.assertEqual(s.SOURCE_COUNT,808+len(s.OWN)); self.assertEqual(s.INPUT_COUNT,1517+10+len(s.OWN))
        self.assertEqual(s.WORK['train_steps'],10*1200); self.assertEqual(s.WORK['training_rows'],10*1200*48)
        self.assertEqual(s.WORK['model_forward_calls'],10*(1371+171)); self.assertEqual(s.WORK['row_presentations'],10*(74016+16416))
    def test_05_schedule_shape(self):
        for z in (events()[:-1],events().float()):
            with self.subTest(),self.assertRaises(ValueError): s.validate_schedule(z)
    def test_06_schedule_domain(self):
        z=events(); z[:4,:,0]=5
        with self.assertRaises(ValueError): s.validate_schedule(z)
    def test_07_schedule_duplicate_row(self):
        z=events(); z[0,0,2]=z[0,0,3]
        with self.assertRaises(ValueError): s.validate_schedule(z)
    def test_08_query_pair_identity_preserved(self):
        z=events(); a=z[4,0,2].clone(); z[4,0,2]=z[4,1,2]; z[4,1,2]=a
        with self.assertRaises(ValueError): s.validate_schedule(z)
    def test_09_epoch_profile_and_exposure(self):
        z=events(); z[0,0,1]=(int(z[0,0,1])+1)%3
        with self.assertRaises(ValueError): s.validate_schedule(z)
        z=events(); z[:4,:,0]=3
        with self.assertRaises(ValueError): s.validate_schedule(z)
    def test_10_block_control_formula(self):
        z=events(); f=s.family_mask(z,'epoch4'); indices=[i for i in range(0,1200,4) if int(z[i,0,0])==4]
        self.assertEqual([int(f[i,0]) for i in indices],[0,1]*50)
        self.assertTrue(all(bool((f[i:i+4]==f[i,0]).all()) for i in indices))
    def test_11_allocation_consumes_no_rng(self):
        z=events(); before=torch.random.get_rng_state(); s.family_mask(z,'batch4'); self.assertTrue(torch.equal(before,torch.random.get_rng_state()))
    def test_12_each_row_exact_half(self):
        z=events(); f=s.family_mask(z,'batch4'); count=torch.zeros((192,2),dtype=torch.int64)
        for ev,mask in zip(z.tolist(),f.tolist()):
            if ev[0][0]==4:
                for row,family in zip(ev,mask): count[row[2],family]+=1; count[row[3],family]+=1
        self.assertTrue(torch.equal(count,torch.full_like(count,50)))
    def test_13_exact_pair_profile_exposure(self):
        z=events(); self.assertEqual(s.exposure(z,s.family_mask(z,'epoch4')),s.exposure(z,s.family_mask(z,'batch4')))
    def test_14_every_long_update_mixed(self):
        z=events(); f=s.family_mask(z,'batch4'); counts=(f[z[:,0,0]==4]==0).sum(1)
        self.assertEqual(sorted(counts.tolist()),[11]*48+[12]*304+[13]*48)
    def test_15_short_names_unchanged(self):
        z=events(); f=s.family_mask(z,'batch4'); self.assertTrue(bool((f[z[:,0,0]!=4]==0).all()))
    def test_16_plan_is_deterministic_without_mutation(self):
        z=events(); old=z.clone(); self.assertTrue(torch.equal(s.family_mask(z,'batch4'),s.family_mask(z,'batch4'))); self.assertTrue(torch.equal(z,old))
    def test_17_integral_flow_exact(self):
        chosen,caps=s.balanced_allocation([[0,1],[0,1]],[1,1]); self.assertEqual(caps,[1,1]); self.assertEqual([sum(j in x for x in chosen) for j in (0,1)],[1,1])
    def test_18_infeasible_flow_fails_closed(self):
        with self.assertRaises(ValueError): s.balanced_allocation([[0],[0]],[1,1])
    def test_19_duplicate_edges_rejected(self):
        with self.assertRaises(ValueError): s.balanced_allocation([[0,0]],[1])
    def test_20_invalid_quota_types_and_domains(self):
        for rows,quota in [([[0]],[True]),([[0]],[-1]),([[1]],[1]),([[False]],[1])]:
            with self.subTest(),self.assertRaises(ValueError): s.balanced_allocation(rows,quota)
    def test_21_zero_flow_is_exact(self): self.assertEqual(s.balanced_allocation([[0],[0]],[0]),([set(),set()],[0,0]))
    def test_22_flow_inputs_immutable(self):
        a=[[0,1],[0,1]]; b=[1,1]; old=copy.deepcopy((a,b)); s.balanced_allocation(a,b); self.assertEqual((a,b),old)
    def test_23_edge_order_canonical(self): self.assertEqual(s.balanced_allocation([[1,0],[0,1]],[1,1]),s.balanced_allocation([[0,1],[1,0]],[1,1]))
    def test_24_unknown_arm_rejected(self):
        with self.assertRaises(ValueError): s.family_mask(events(),'selected_success')
    def test_25_control_tokens_exact(self):
        _,t,_,ev,_=toy_inputs(); tokens,ids=s.select_tokens(t,ev[0],torch.zeros(24,dtype=torch.int64)); self.assertTrue(torch.equal(tokens,t['original'][4,'repeat'][ids]))
    def test_26_query_pairs_never_split(self):
        _,t,_,ev,_=toy_inputs(); f=torch.arange(24)%2; tokens,ids=s.select_tokens(t,ev[0],f)
        for i in range(24): self.assertTrue(torch.equal(tokens[2*i:2*i+2],t['interior4' if int(f[i]) else 'original'][4,'repeat'][ids[2*i:2*i+2]]))
    def test_27_pure_interior_tokens_exact(self):
        _,t,_,ev,_=toy_inputs(); tokens,ids=s.select_tokens(t,ev[0],torch.ones(24,dtype=torch.int64)); self.assertTrue(torch.equal(tokens,t['interior4'][4,'repeat'][ids]))
    def test_28_selector_rejects_bad_mask(self):
        _,t,_,ev,_=toy_inputs()
        for f in (torch.zeros(23,dtype=torch.int64),torch.full((24,),2,dtype=torch.int64),torch.zeros(24)):
            with self.subTest(),self.assertRaises(ValueError): s.select_tokens(t,ev[0],f)
    def test_29_numeric_control_reference_parity(self):
        m,t,y,ev,x=toy_inputs(); ref=copy.deepcopy(m); s.train_steps(m,t,y,ev,torch.zeros((1,24),dtype=torch.int64),x)
        opt=torch.optim.AdamW(ref.parameters(),lr=.005,weight_decay=0.); opt.zero_grad()
        loss=torch.nn.functional.cross_entropy(ref(t['original'][4,'repeat'][:48],torch.zeros(48,dtype=torch.int64)),y[:48]); loss.backward()
        torch.nn.utils.clip_grad_norm_(ref.parameters(),1.,error_if_nonfinite=True); opt.step()
        self.assertTrue(all(torch.equal(a,b) for a,b in zip(m.parameters(),ref.parameters())))
    def test_30_mixed_tokens_change_updates(self):
        m,t,y,ev,x=toy_inputs(); ref=copy.deepcopy(m)
        s.train_steps(m,t,y,ev,torch.zeros((1,24),dtype=torch.int64),x); s.train_steps(ref,t,y,ev,(torch.arange(24)%2)[None,:],x)
        self.assertTrue(any(not torch.equal(a,b) for a,b in zip(m.parameters(),ref.parameters())))
    def test_31_nonfinite_loss_stops(self):
        m,t,y,ev,x=toy_inputs()
        with patch.object(m,'forward',return_value=torch.full((48,256),float('nan'),dtype=torch.float64)),self.assertRaises(ValueError):
            s.train_steps(m,t,y,ev,torch.zeros((1,24),dtype=torch.int64),x)
    def test_32_all_five_registered_order_seeds(self):
        for order in s.ORDERS:
            z=events(order); self.assertEqual(s.exposure(z,s.family_mask(z,'epoch4')),s.exposure(z,s.family_mask(z,'batch4')))
    def test_33_all_five_gate(self): self.assertEqual(s.fixed_gate(gate_rows()),(True,[True]*5))
    def test_34_every_gate_clause(self):
        for k,v in [('candidate_interior_pass',False),('candidate_retention_pass',False),('interior_answer_gain',0),('interior_pair_gain',0),('original_answer_gain',-1),('original_pair_gain',-1)]:
            z=gate_rows(); z[2][k]=v
            with self.subTest(key=k): self.assertEqual(s.fixed_gate(z),(False,[True,True,False,True,True]))
    def test_35_original_tie_is_retention(self): self.assertTrue(s.fixed_gate(gate_rows())[0])
    def test_36_interior_tie_not_improvement(self):
        z=gate_rows(); z[0]['interior_answer_gain']=0; self.assertFalse(s.fixed_gate(z)[0])
    def test_37_gate_duplicate_or_missing(self):
        for z in ([gate_rows()[0]]*5,gate_rows()[:-1],list(reversed(gate_rows()))):
            with self.subTest(),self.assertRaises(ValueError): s.fixed_gate(z)
    def test_38_bool_not_numeric_gain(self):
        z=gate_rows(); z[0]['original_pair_gain']=True
        with self.assertRaises(ValueError): s.fixed_gate(z)
    def test_39_failed_seed_not_pooled(self):
        z=gate_rows(); z[4]['candidate_interior_pass']=False; self.assertFalse(s.fixed_gate(z)[0])
    def test_40_unicode_and_exclusive_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; e.save(p,{'名前':'あいうえ'}); self.assertEqual(e.read(p),{'名前':'あいうえ'})
            with self.assertRaises(FileExistsError): e.save(p,{})
    def test_41_duplicate_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; p.write_text('{"a":1,"a":2}',encoding='utf-8')
            with self.assertRaises(ValueError): e.read(p)
    def test_42_nonfinite_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for value in ('NaN','Infinity','-Infinity'):
                p.write_text(value,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError): e.read(p)
    def test_43_source_lf_crlf(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in (raw,raw.replace(b'\n',b'\r\n')): p.write_bytes(text); self.assertEqual(e.source_bytes(p,oid),text)
    def test_44_source_corruption(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in (b'bad',b'a\r\nb\n'):
                p.write_bytes(text)
                with self.subTest(),self.assertRaises(ValueError): e.source_bytes(p,oid)
    def test_45_real_git_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=git_fixture(root); e.guard(root,head)
    def test_46_real_git_dirty_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=git_fixture(root); (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError): e.guard(root,head)
    def test_47_real_git_stale_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); git_fixture(root)
            with self.assertRaises(ValueError): e.guard(root,'a'*40)
    def test_48_unique_formal_active(self):
        self.assertTrue(e.active('## Formal state\nC326 ACTIVE / NOT YET JUDGED\n## History\nC325 ACTIVE / NOT YET JUDGED'))
        for t in ('## History\nC326 ACTIVE / NOT YET JUDGED','## Formal state\nC325 ACTIVE / NOT YET JUDGED','## Formal state\nC326 ACTIVE / NOT YET JUDGED\nC327 ACTIVE / NOT YET JUDGED'):
            self.assertFalse(e.active(t))
    def test_49_parent_contract(self): e.parent_contract(*parent_fixture())
    def test_50_parent_identity_counts(self):
        for k,v in [('schema','wrong'),('commit_sha','a'*40),('scientific_status','PASS'),('source_count',802),('input_count',1517-1)]:
            r,z,p,helper=parent_fixture(); z[k]=v
            with self.subTest(key=k),self.assertRaises(ValueError): e.parent_contract(r,z,p,helper)
    def test_51_parent_direct_dependency_pin(self):
        r,z,p,helper=parent_fixture(); r['source_blobs'][e.E_PATH]='0'*40; z['source_blobs'][e.E_PATH]='0'*40
        with self.assertRaises(ValueError): e.parent_contract(r,z,p,helper)
    def test_52_parent_exact_unions(self):
        for name in ('source_blobs','input_sha256'):
            r,z,p,helper=parent_fixture(); r[name][next(iter(r[name]))]='changed'
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(r,z,p,helper)
    def test_53_parent_complete_receipts(self):
        for k,v in [('immediate_parent_semantic_reconstruction',False),('ancestor_semantic_reruns',1),('saved_semantic_reconstruction',False),('final_reference_rechecks',1516)]:
            r,z,p,helper=parent_fixture(); z[k]=v
            with self.subTest(key=k),self.assertRaises(ValueError): e.parent_contract(r,z,p,helper)
    def test_54_incomplete_regression(self):
        for k,v in [('tests',5610-1),('skipped',1),('failures',1),('successful',False),('commit_sha','b'*40)]:
            row=receipt(); row[k]=v
            with self.subTest(key=k),self.assertRaises(ValueError): e.check_regression(row,'a'*40)
    def test_55_semantic_suite_inventory(self):
        class Case(unittest.TestCase):
            def __init__(self,i): super().__init__(); self.number=i
            def id(self): return 'fixture.'+str(self.number)
        inherited=[Case(i) for i in range(5546)]
        def flatten(suite):
            for test in suite:
                if isinstance(test,unittest.TestSuite): yield from flatten(test)
                else: yield test
        helper=NS(suite=lambda *args:inherited); r6=NS(flatten=flatten,RECOVERY_MODULES=('a','b','c'))
        b=NS(EXCLUDED='excluded',regression_modules=lambda root:list(range(210)))
        self.assertEqual(e.suite(ROOT,b,helper,r6).countTestCases(),s.FULL_TESTS)
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),s.OWN_TESTS)
        inherited[-1]=inherited[0]
        with self.assertRaises(ValueError): e.suite(ROOT,b,helper,r6)
    def test_56_stage_order_finite_negative(self):
        calls=[]
        def call(name,value):
            def run(): calls.append(name); return value
            return run
        with contextlib.redirect_stdout(io.StringIO()):
            e.execute_stages('a'*40,call('preflight',None),call('tests',receipt()),call('fit',{'gate':False}),call('saved',([],{'gate':False})),call('final',[]))
        self.assertEqual(calls,['preflight','tests','fit','saved','final'])
    def test_57_failed_regression_never_fits(self):
        fit=Mock(); bad={**receipt(),'failures':1,'successful':False}
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError): e.execute_stages('a'*40,lambda:None,lambda:bad,fit,lambda:None,lambda:None)
        fit.assert_not_called()
    def test_58_saved_mismatch_stops(self):
        final=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError): e.execute_stages('a'*40,lambda:None,receipt,lambda:{'a':1},lambda:([],{'a':2}),final)
        final.assert_not_called()
    def test_59_controller_order_and_no_retry(self):
        for fail in (False,True):
            with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run',side_effect=ValueError('native') if fail else None) as child,contextlib.redirect_stdout(io.StringIO()) as out:
                root=Path(d)
                if fail:
                    with self.assertRaises(ValueError): e.run(root,root/'runs/x','a'*40)
                    self.assertEqual(child.call_count,1); self.assertIn('run_execution_valid = false',out.getvalue())
                else:
                    e.run(root,root/'runs/x','a'*40); self.assertEqual([c.args[-1] for c in child.call_args_list],['science','verify'])
    def test_60_subprocess_failure_evidence(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(d)
            with self.assertRaises(ValueError): e.subprocess_run(ROOT,folder,'a'*40,'invalid-mode')
            self.assertIn('invalid choice',(folder/'invalid-mode.log').read_text(encoding='utf-8'))
    def test_61_saved_validation_and_tamper(self):
        e.check_validation(validation())
        for change in ('cohort','work','gain','conservation','exposure'):
            z=validation()
            if change=='cohort': z['seed_results'].pop()
            elif change=='work': z['train_steps']-=1
            elif change=='gain': z['paired_comparisons'][0]['interior_answer_gain']+=1
            elif change=='conservation': z['paired_comparisons'][0]['interior']['rescued']+=1
            else: z['all_family_exposures_matched']=False
            with self.subTest(change=change),self.assertRaises(ValueError): e.check_validation(z)
        z=validation(); z['seed_results'][1]['interior_pass']=False; z['paired_comparisons'][0]['candidate_interior_pass']=False
        z['paired_comparisons'][0]['paired_success']=False; z['candidate_gate']=False; z['paired_success_count']=4; e.check_validation(z)
    def test_62_semantic_bytes_bound(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in s.OUTPUTS: (root/name).write_bytes(b'fixture')
            value,bound=e.bound_semantics(root,lambda:'ok'); self.assertEqual(value,'ok'); self.assertEqual(len(bound),8)
            def tamper(): (root/s.OUTPUTS[0]).write_bytes(b'changed'); return 'bad'
            with self.assertRaises(ValueError): e.bound_semantics(root,tamper)
    def test_63_source_and_launcher_contract(self):
        source=inspect.getsource(e.scientific_worker); tree=ast.parse(source)
        names=[n.func.attr if isinstance(n.func,ast.Attribute) else n.func.id for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,(ast.Attribute,ast.Name))]
        for name in ('snapshot','parent_semantics','execute_stages','runtime_preflight','run_science','semantic_recheck','bound_semantics'): self.assertIn(name,names)
        self.assertNotIn('patch',names)
        text=(ROOT/'tools/invoke_c326.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'): self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('run_c326.ps1',text); self.assertIn('-ExperimentId C326',text)
        loop=ast.parse(inspect.getsource(s.family_mask))
        self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr in ('argmax','backward') for n in ast.walk(loop)))
    def test_64_actual_worker_with_explicit_synthetic_dependencies(self):
        for bad in (False,True): self.worker_fixture(bad)

    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d); folder=root/'runs/fake'; folder.mkdir(parents=True); calls=[]
            pins={f'source{i}':'a'*40 for i in range(s.SOURCE_COUNT)}; inputs={str(root/f'input{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={}; stats={'final_reference_rechecks':s.INPUT_COUNT}
                def __init__(self,*args,**kwargs): pass
                def __enter__(self): return self
                def __exit__(self,*args): calls.append('release')
                def recheck(self): calls.append('final'); return [{'path':k,'sha256':v} for k,v in inputs.items()]
            r4=NS(WinAPI=lambda:None,lock_probe=lambda *args:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            x=NS(guarded=NS(no_neural=contextlib.nullcontext)); cx=(None,None,None,None,None,x)
            b=NS(context=lambda:cx,check_dependencies=lambda *args:None,peak_rss=lambda:1)
            val=validation()
            def snapshot(*args): calls.append('snapshot'); return {},{},pins,inputs
            def parent(*args): calls.append('parent'); return {'TRAIN':[]},{},{}
            def preflight(*args): calls.append('preflight')
            def tests(*args):
                calls.append('tests'); row=receipt()
                if bad: row.update(failures=1,successful=False)
                e.save(folder/'regression-result.json',row)
            def fit(out,*args):
                calls.append('fit')
                for name in s.OUTPUTS: (out/name).write_bytes(b'fixture')
                return val
            def saved(*args): calls.append('saved'); return [],val
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(NS(),r4,None)),patch.object(e,'native_runtime',return_value=(torch,np)),\
                 patch.object(e,'snapshot',side_effect=snapshot),patch.object(e,'parent_semantics',side_effect=parent),patch.object(e,'subprocess_run',side_effect=tests),\
                 patch.object(s,'previous',return_value=NS()),patch.object(s,'base',return_value=b),patch.object(s,'runtime_preflight',side_effect=preflight),\
                 patch.object(s,'run_science',side_effect=fit),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError): e.scientific_worker(root,folder,'a'*40)
                    self.assertNotIn('fit',calls)
                else:
                    e.scientific_worker(root,folder,'a'*40)
                    self.assertEqual(calls,['snapshot','parent','preflight','tests','fit','saved','final','release'])
                    self.assertEqual(e.read(folder/'execution-envelope.json')['source_count'],s.SOURCE_COUNT)
                    self.assertTrue(e.read(folder/'execution-envelope.json')['saved_semantic_reconstruction'])


if __name__=='__main__': unittest.main()
