"""C327 software fixtures are not scientific checkpoint measurements."""
from __future__ import annotations
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import math
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import numpy as np
import torch
from fold_lm.v05_benchmarks import model_c327_gradient_alignment as s

ROOT=Path(__file__).resolve().parents[1]
_loader=importlib.util.spec_from_file_location('_c327_tested_execution',ROOT/'tools/c327_execution.py')
e=importlib.util.module_from_spec(_loader); _loader.loader.exec_module(e)


def vec(*xs): return torch.tensor(xs,dtype=torch.float64)


def layout():
    return [dict(name=n,shape=[k],numel=k,group=s.group_of(n)) for n,k in
            [('backbone.core.w',3328),('read.w',512),('backbone.local.w',10416)]]


def validation():
    rows=[dict(seed=seed,arm=arm,group=g,pairs=6,defined_cosines=6,negative_dot=0,mean_joint_descent=6,
               cosine_min=1.,cosine_median=1.,cosine_max=1.) for seed in s.SEEDS for arm in s.ARMS for g in s.GROUPS]
    return dict(diagnostic_complete=True,capability_gate_applicable=False,sign_gate_applicable=False,
                all_weights_preserved=True,all_reverse_replays=True,aggregates=rows,**s.WORK)


def parent_fixture():
    pins={**e.BOOTSTRAP,**{f'pin{i}':'a'*40 for i in range(814-len(e.BOOTSTRAP))}}
    inputs={f'input{i}':'b'*64 for i in range(1533)}
    r=dict(schema='fold-c326-science-v1',experiment_id='parent',stage='stage',commit_sha=e.PARENT_EXECUTION,status='FAIL',
           diagnostic_execution_valid=True,gate_f_candidate=False,production_adoption=False,
           validation_summary={'candidate_gate':False},source_blobs=dict(pins),input_sha256=dict(inputs),manifest_sha256='c'*64)
    v=dict(schema='fold-c326-execution-envelope-v1',commit_sha=e.PARENT_EXECUTION,scientific_summary_sha256=e.PARENT_SUMMARY,
           scientific_status='FAIL',source_count=814,input_count=1533,source_blobs=pins,input_sha256=inputs,
           manifest_sha256='c'*64,scientific_work={'models':10},parent_summary_sha256='d'*64,parent_envelope_sha256='f'*64,
           immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
           final_reference_rechecks=1533,hash_stats={'final_reference_rechecks':1533},
           regression=dict(commit_sha=e.PARENT_EXECUTION,tests=5610,failures=0,errors=0,skipped=0,successful=True))
    p=NS(validate_seal=lambda:None,EXPERIMENT_ID='parent',STAGE='stage',OWN=(e.P_PATH,),MANIFEST_SHA='c'*64,WORK={'models':10})
    helper=NS(check_validation=lambda value:None,BOOTSTRAP={},PARENT_SUMMARY='d'*64,PARENT_ENVELOPE='f'*64)
    return r,v,p,helper


def receipt(): return dict(commit_sha='a'*40,tests=s.FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C327 fixture'),('config','user.email','c327@example.invalid')]:
        subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    (root/'docs').mkdir(); (root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC327 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True); subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
    return e.git(root,'rev-parse','HEAD')


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.w=torch.nn.Parameter(vec(.2,-.3)); self.unused=torch.nn.Parameter(vec(4.))
    def forward(self,tokens,tasks):
        v=tokens[:,0].to(torch.float64)
        return torch.stack((v*self.w[0],v*self.w[1]),dim=1)


def toy():
    m=Toy(); x=torch.tensor([[1],[2],[3]],dtype=torch.int64); y=torch.tensor([0,1,0],dtype=torch.int64)
    return m,x,y,m(x,torch.zeros(3,dtype=torch.int64)).detach()


def archive_fixture():
    data={'TRAIN':[dict(id=str(i),language='en' if i<96 else 'ja',target=i%2) for i in range(192)],'HOLDOUT':[]}
    parents=[]; records=[]; receipts=[]; loss=math.log(256)
    profiles=('u','v','w'); b=NS(templates=NS(INTERIOR_PROFILES=profiles))
    for seed in s.SEEDS:
        for arm in s.ARMS:
            z=torch.zeros((192,256),dtype=torch.float64)
            raw=dict(original={'4':{'TRAIN':{p:{'normal':z} for p in s.PROFILES}}},interior={'TRAIN':{p:{'normal':z} for p in profiles}})
            parents.append(dict(seed=seed,arm=arm,final_sha256='a'*64,raw=raw))
            receipts.append(dict(seed=seed,arm=arm,before='a'*64,after='a'*64,hooks_restored=True,no_accumulated_gradients=True,
                calls=[24,2304],core_calls=96,policy=dict(calls=24,query_calls=48,rows=2304,grad_calls=24)))
            for profile in s.PROFILES:
                for language in s.LANGUAGES:
                    ids=s.row_indices(data,language)
                    r=dict(seed=seed,arm=arm,profile=profile,language=language,rows=96,row_ids_sha256=s.digest([data['TRAIN'][i]['id'] for i in ids]),repeat_errors=[0.,0.])
                    r.update({name:dict(gradient=torch.ones(14256,dtype=torch.float64),connected=[True]*3,loss=loss,logit_error=0.) for name in ('old','interior')})
                    records.append(r)
    return dict(schema='fold-c327-gradients-v1',layout=layout(),records=records,model_receipts=receipts),parents,data,b


class C327Tests(unittest.TestCase):
    def test_01_manifest_seal(self): s.validate_seal()
    def test_02_manifest_mutation(self):
        with patch.object(s,'STAGE','changed'),self.assertRaises(ValueError): s.validate_seal()
    def test_03_complete_fixed_cohort(self):
        self.assertEqual(s.SEEDS,tuple(range(326001,326006))); self.assertEqual(len(set(s.identities())),60)
        self.assertEqual(s.ARMS,('epoch4','batch4'))
    def test_04_work_and_protection(self):
        self.assertEqual(s.SOURCE_COUNT,814+len(s.OWN)); self.assertEqual(s.INPUT_COUNT,1533+10+len(s.OWN))
        self.assertEqual(s.WORK['model_forward_calls'],10*3*2*4); self.assertEqual(s.WORK['row_presentations'],240*96)
        self.assertEqual(s.WORK['optimizer_steps'],0); self.assertEqual(s.WORK['new_checkpoint_writes'],0)
        self.assertEqual(s.manifest()['gradient_payload_bytes'],60*2*14256*8)
    def test_05_native_layout(self): self.assertEqual(s.validate_layout(layout()),{'core':3328,'reader':512,'other':10416})
    def test_06_bad_layout_rejected(self):
        for kind in ('duplicate','shape','group','total'):
            z=layout()
            if kind=='duplicate': z[2]['name']=z[1]['name']
            elif kind=='shape': z[0]['shape']=[1]
            elif kind=='group': z[0]['group']='other'
            else: z[2]['shape']=[10415]; z[2]['numel']=10415
            with self.subTest(),self.assertRaises(ValueError): s.validate_layout(z)
    def test_07_row_selection_is_train_only(self):
        data={'TRAIN':[{'language':'en' if i<96 else 'ja'} for i in range(192)],'HOLDOUT':[{'language':'en'}]*999}
        self.assertEqual(s.row_indices(data,'en'),list(range(96))); self.assertEqual(s.row_indices(data,'ja'),list(range(96,192)))
    def test_08_wrong_row_count_language(self):
        for data,language in [({'TRAIN':[],'HOLDOUT':[]},'en'),({'TRAIN':[],'HOLDOUT':[]},'selected')]:
            with self.subTest(),self.assertRaises(ValueError): s.row_indices(data,language)
    def test_09_parallel_gradients(self):
        r=s.geometry(vec(1,2),vec(2,4)); self.assertAlmostEqual(r['cosine'],1.); self.assertTrue(r['mean_is_joint_strict_descent'])
    def test_10_opposed_gradients(self):
        r=s.geometry(vec(1,0),vec(-2,0)); self.assertEqual(r['cosine'],-1.); self.assertTrue(r['negative_dot'])
        self.assertGreater(r['old_derivative_along_negative_mean'],0); self.assertFalse(r['mean_is_joint_strict_descent'])
    def test_11_orthogonal_gradients(self):
        r=s.geometry(vec(1,0),vec(0,1)); self.assertEqual(r['cosine'],0.); self.assertTrue(r['mean_is_joint_strict_descent'])
    def test_12_zero_is_undefined_not_orthogonal(self):
        r=s.geometry(vec(0,0),vec(1,2)); self.assertIsNone(r['cosine']); self.assertTrue(r['zero_old']); self.assertFalse(r['negative_dot'])
    def test_13_equal_opposition_cancels(self):
        r=s.geometry(vec(1,2),vec(-1,-2)); self.assertEqual(r['old_derivative_along_negative_mean'],0.)
        self.assertEqual(r['interior_derivative_along_negative_mean'],0.)
    def test_14_negative_dot_can_still_allow_joint_descent(self):
        r=s.geometry(vec(2,0),vec(-.5,2)); self.assertTrue(r['negative_dot']); self.assertTrue(r['mean_is_joint_strict_descent'])
    def test_15_nonfinite_and_dtype_rejected(self):
        for a,b in [(vec(float('nan')),vec(1)),(vec(float('inf')),vec(1)),(torch.ones(2),vec(1,2)),(vec(1),vec(1,2))]:
            with self.subTest(),self.assertRaises(ValueError): s.geometry(a,b)
    def test_16_partition_conservation(self):
        a=torch.arange(14256,dtype=torch.float64)/14256; b=a.flip(0); rs=s.partition_metrics(a,b,layout())
        self.assertAlmostEqual(rs['all']['dot'],sum(rs[k]['dot'] for k in s.GROUPS[1:]),places=9)
    def test_17_autograd_and_unused_connectivity(self):
        m,x,y,z=toy(); r=s.objective(m,x,y,z)
        self.assertEqual(r['connected'],[True,False]); self.assertEqual(float(r['gradient'][-1]),0.)
        self.assertTrue(all(p.grad is None for p in m.parameters()))
    def test_18_gradient_matches_finite_difference(self):
        m,x,y,z=toy(); g=s.objective(m,x,y,z)['gradient']; eps=1e-6; losses=[]
        original=m.w.detach().clone()
        for sign in (1,-1):
            with torch.no_grad(): m.w.copy_(original); m.w[0]+=sign*eps
            losses.append(float(torch.nn.functional.cross_entropy(m(x,torch.zeros(3,dtype=torch.int64)),y).detach()))
        with torch.no_grad(): m.w.copy_(original)
        self.assertAlmostEqual(float(g[0]),(losses[0]-losses[1])/(2*eps),places=7)
    def test_19_objective_never_updates_weights(self):
        m,x,y,z=toy(); before={k:v.clone() for k,v in m.state_dict().items()}; s.objective(m,x,y,z)
        self.assertTrue(all(torch.equal(v,m.state_dict()[k]) for k,v in before.items()))
    def test_20_parent_logit_mismatch_rejected(self):
        m,x,y,z=toy()
        with self.assertRaises(ValueError): s.objective(m,x,y,z+1e-4)
    def test_21_existing_gradients_rejected(self):
        m,x,y,z=toy(); m.w.grad=torch.zeros_like(m.w)
        with self.assertRaises(ValueError): s.objective(m,x,y,z)
    def test_22_reverse_repeat_order(self):
        seen=[]
        def measure(j): seen.append(j); return dict(gradient=vec(j+1),connected=[True],loss=.5,logit_error=0.)
        s.repeated_pair(measure); self.assertEqual(seen,[0,1,1,0])
    def test_23_reverse_repeat_drift(self):
        n=[0]
        def measure(j): n[0]+=1; return dict(gradient=vec(n[0]),connected=[True],loss=.5,logit_error=0.)
        with self.assertRaises(ValueError): s.repeated_pair(measure)
    def test_24_real_objective_reverse_repeat(self):
        m,x,y,z=toy(); a,b,errors=s.repeated_pair(lambda j:s.objective(m,x,y,z)); self.assertEqual(errors,[0.,0.])
        self.assertTrue(torch.equal(a['gradient'],b['gradient']))
    def test_25_full_saved_geometry_reconstruction(self):
        args=archive_fixture(); rows,value=s.analyze(*args); self.assertEqual(len(rows),60); self.assertEqual(len(value['aggregates']),40)
        self.assertTrue(all(r['negative_dot']==0 for r in value['aggregates'])); e.check_validation(value)
    def test_26_saved_archive_cohort_loss_and_replay_tamper(self):
        for kind in ('cohort','loss','row','repeat','unused'):
            args=archive_fixture(); r=args[0]['records'][0]
            if kind=='cohort': args[0]['records'].pop()
            elif kind=='loss': r['old']['loss']+=.1
            elif kind=='row': r['row_ids_sha256']='wrong'
            elif kind=='repeat': r['repeat_errors'][0]=1e-3
            else: r['old']['connected'][0]=False
            with self.subTest(kind=kind),self.assertRaises(ValueError): s.analyze(*args)
    def test_27_saved_model_receipt_tamper(self):
        args=archive_fixture(); args[0]['model_receipts'][0]['after']='changed'
        with self.assertRaises(ValueError): s.analyze(*args)
    def test_28_safe_tensor_archive_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            args=archive_fixture(); p=Path(d)/'g.pt'; torch.save(args[0],p); args=(torch.load(p,weights_only=True),*args[1:])
            self.assertEqual(len(s.analyze(*args)[0]),60)
    def test_29_duplicate_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in ('{"a":1,"a":2}','NaN','Infinity','-Infinity'):
                p.write_text(text,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError): e.read(p)
    def test_30_unicode_and_exclusive_save(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; e.save(p,{'名前':'あいうえ'}); self.assertEqual(e.read(p),{'名前':'あいうえ'})
            with self.assertRaises(FileExistsError): e.save(p,{})
    def test_31_source_lf_crlf_and_tamper(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for data in (raw,raw.replace(b'\n',b'\r\n')): p.write_bytes(data); self.assertEqual(e.source_bytes(p,oid),data)
            for data in (b'bad',b'a\nb\r\n'):
                p.write_bytes(data)
                with self.subTest(),self.assertRaises(ValueError): e.source_bytes(p,oid)
    def test_32_real_git_guard_and_dirty_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=git_fixture(root); e.guard(root,head)
            with self.assertRaises(ValueError): e.guard(root,'a'*40)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError): e.guard(root,head)
    def test_33_unique_active_section(self):
        self.assertTrue(e.active('## Formal state\nC327 ACTIVE / NOT YET JUDGED\n## History\nC326 ACTIVE / NOT YET JUDGED'))
        for text in ('## History\nC327 ACTIVE / NOT YET JUDGED','## Formal state\nC326 ACTIVE / NOT YET JUDGED',
                     '## Formal state\nC327 ACTIVE / NOT YET JUDGED\nC328 ACTIVE / NOT YET JUDGED'):
            self.assertFalse(e.active(text))
    def test_34_complete_parent_contract(self): e.parent_contract(*parent_fixture())
    def test_35_parent_identity_and_unions_rejected(self):
        for kind in ('identity','count','source','input','pin'):
            r,v,p,h=parent_fixture()
            if kind=='identity': v['scientific_status']='PASS'
            elif kind=='count': v['source_count']=808
            elif kind=='source': r['source_blobs'][e.P_PATH]='bad'
            elif kind=='input': r['input_sha256']['input0']='bad'
            else: r['source_blobs'][e.E_PATH]='bad'; v['source_blobs'][e.E_PATH]='bad'
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(r,v,p,h)
    def test_36_parent_completion_rejected(self):
        for k,value in [('saved_semantic_reconstruction',False),('final_reference_rechecks',1532),('ancestor_semantic_reruns',1)]:
            args=parent_fixture(); args[1][k]=value
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_37_full_regression_required(self):
        e.check_regression(receipt(),'a'*40)
        for k,value in [('tests',5610),('skipped',1),('failures',1),('successful',False)]:
            r=receipt(); r[k]=value
            with self.subTest(),self.assertRaises(ValueError): e.check_regression(r,'a'*40)
    def test_38_real_own_suite_inventory(self):
        class Case(unittest.TestCase):
            def __init__(self,i): super().__init__(); self.number=i
            def id(self): return 'fixture.'+str(self.number)
        inherited=[Case(i) for i in range(5610)]
        def flatten(suite):
            for t in suite:
                if isinstance(t,unittest.TestSuite): yield from flatten(t)
                else: yield t
        b=NS(EXCLUDED='excluded',regression_modules=lambda root:list(range(210)))
        helper=NS(suite=lambda *args:inherited); r6=NS(flatten=flatten,RECOVERY_MODULES=('a','b','c'))
        self.assertEqual(e.suite(ROOT,b,helper,None,r6).countTestCases(),s.FULL_TESTS)
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),s.OWN_TESTS)
        inherited[-1]=inherited[0]
        with self.assertRaises(ValueError): e.suite(ROOT,b,helper,None,r6)
    def test_39_stages_and_regression_failure(self):
        calls=[]
        def step(k,v):
            def run(): calls.append(k); return v
            return run
        with contextlib.redirect_stdout(io.StringIO()):
            e.execute_stages('a'*40,step('preflight',None),step('tests',receipt()),step('measure',{}),step('saved',([],{})),step('final',[]))
        self.assertEqual(calls,['preflight','tests','measure','saved','final'])
        measure=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages('a'*40,lambda:None,lambda:{**receipt(),'failures':1},measure,lambda:None,lambda:None)
        measure.assert_not_called()
    def test_40_preflight_failure_stops_before_tests(self):
        tests=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages('a'*40,Mock(side_effect=ValueError('gradient')),tests,Mock(),Mock(),Mock())
        tests.assert_not_called()
    def test_41_saved_bytes_bound(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in s.OUTPUTS: (root/name).write_bytes(b'fixture')
            self.assertEqual(e.bound_semantics(root,lambda:'ok')[0],'ok')
            def change(): (root/s.OUTPUTS[0]).write_bytes(b'bad')
            with self.assertRaises(ValueError): e.bound_semantics(root,change)
    def test_42_validation_has_no_sign_gate(self):
        v=validation(); e.check_validation(v)
        for r in v['aggregates']: r.update(negative_dot=6,mean_joint_descent=0,cosine_min=-1.,cosine_median=-1.,cosine_max=-1.)
        e.check_validation(v)
        for r in v['aggregates']: r.update(defined_cosines=0,negative_dot=0,cosine_min=None,cosine_median=None,cosine_max=None)
        e.check_validation(v)
    def test_43_validation_tamper(self):
        for kind in ('work','cohort','capability','sign','count'):
            v=validation()
            if kind=='work': v['optimizer_steps']=1
            elif kind=='cohort': v['aggregates'].pop()
            elif kind=='capability': v['capability_gate_applicable']=True
            elif kind=='sign': v['sign_gate_applicable']=True
            else: v['aggregates'][0]['negative_dot']=7
            with self.subTest(),self.assertRaises(ValueError): e.check_validation(v)
    def test_44_controller_science_verify_and_failure(self):
        for fail in (False,True):
            with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run',side_effect=ValueError('native') if fail else None) as child,contextlib.redirect_stdout(io.StringIO()):
                root=Path(d)
                if fail:
                    with self.assertRaises(ValueError): e.run(root,root/'runs/test','a'*40)
                    self.assertEqual(child.call_count,1)
                else:
                    e.run(root,root/'runs/test','a'*40); self.assertEqual([c.args[-1] for c in child.call_args_list],['science','verify'])
    def test_45_native_subprocess_error_preserved(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(d)
            with self.assertRaises(ValueError): e.subprocess_run(ROOT,folder,'a'*40,'invalid-mode')
            self.assertIn('invalid choice',(folder/'invalid-mode.log').read_text(encoding='utf-8'))
    def test_46_source_and_launcher_contract(self):
        tree=ast.parse(inspect.getsource(s.objective)); calls=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertIn('grad',calls); self.assertNotIn('step',calls); self.assertNotIn('backward',calls)
        text=(ROOT/'tools/invoke_c327.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'): self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C327',text)
    def test_47_worker_real_control_synthetic_dependencies(self): self.worker_fixture(False)
    def test_48_worker_failure_never_measures(self): self.worker_fixture(True)

    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d); folder=root/'runs/test'; folder.mkdir(parents=True); calls=[]
            pins={f'source{i}':'a'*40 for i in range(s.SOURCE_COUNT)}; inputs={str(root/f'input{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={}; stats={'final_reference_rechecks':s.INPUT_COUNT}
                def __init__(self,*args,**kwargs): pass
                def __enter__(self): return self
                def __exit__(self,*args): calls.append('release')
                def recheck(self): calls.append('final'); return [{'path':k,'sha256':v} for k,v in inputs.items()]
            r4=NS(WinAPI=lambda:None,lock_probe=lambda *args:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            cx=(None,None,None,None,None,NS(guarded=NS(no_neural=contextlib.nullcontext)))
            b=NS(context=lambda:cx,check_dependencies=lambda *args:None,peak_rss=lambda:1); p=NS(base=lambda:b)
            helper=NS(native_runtime=lambda:(torch,np)); v=validation()
            def snap(*args): calls.append('snapshot'); return {},{},pins,inputs
            def parent(*args): calls.append('parent'); return {'TRAIN':[]},{},{}
            def preflight(*args): calls.append('preflight')
            def tests(*args):
                calls.append('tests'); r=receipt()
                if bad: r.update(failures=1,successful=False)
                e.save(folder/'regression-result.json',r)
            def measure(out,*args):
                calls.append('measure')
                for name in s.OUTPUTS: (out/name).write_bytes(b'fixture')
                return v
            def saved(*args): calls.append('saved'); return [],v
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(helper,None,r4,None)),patch.object(s,'parent',return_value=p),\
                 patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=parent),patch.object(e,'subprocess_run',side_effect=tests),\
                 patch.object(s,'runtime_preflight',side_effect=preflight),patch.object(s,'run_diagnostic',side_effect=measure),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError): e.diagnostic_worker(root,folder,'a'*40)
                    self.assertNotIn('measure',calls)
                else:
                    e.diagnostic_worker(root,folder,'a'*40)
                    self.assertEqual(calls,['snapshot','parent','preflight','tests','measure','saved','final','release'])
                    self.assertEqual(e.read(folder/'execution-envelope.json')['source_count'],s.SOURCE_COUNT)


if __name__=='__main__': unittest.main()
