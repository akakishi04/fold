"""Authoring/runtime tests; synthetic fixtures are not C325 scientific outcomes."""
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
from unittest.mock import patch
import torch
from fold_lm.v05_benchmarks import model_c325_mixed_name_coverage as s

ROOT=Path(__file__).resolve().parents[1]
_loader=importlib.util.spec_from_file_location('_c325_execution_tests',ROOT/'tools/c325_execution.py')
e=importlib.util.module_from_spec(_loader); _loader.loader.exec_module(e)


def events():
    value=torch.empty((1200,24,4),dtype=torch.int64)
    ids=torch.arange(192).reshape(4,24,2)
    for epoch in range(300):
        value[4*epoch:4*epoch+4,:,0]=(2,3,4)[epoch%3]
        value[4*epoch:4*epoch+4,:,1]=(epoch//3+epoch%3)%3
        value[4*epoch:4*epoch+4,:,2:]=ids
    return value


def gate_rows():
    return [dict(seed=seed,candidate_interior_pass=True,candidate_retention_pass=True,
        original_answer_gain=1,original_pair_gain=1,interior_answer_gain=0,interior_pair_gain=0) for seed in s.SEEDS]


def contrast(gain):
    return dict(answers=288,query_pairs=144,control_correct=100,candidate_correct=100+gain,
        control_both_correct=50,candidate_both_correct=50+gain,rescued=gain,regressed=0,
        pair_rescued=gain,pair_regressed=0,answer_gain=gain,query_pair_gain=gain)


def validation():
    rows=[]; pairs=[]
    for seed in s.SEEDS:
        for arm in s.ARMS:
            passed={str(n):arm=='mixed4' or n<5 for n in range(2,7)}
            rows.append(dict(seed=seed,arm=arm,original_pass=passed,retention_pass=all(passed.values()),interior_pass=True))
        pairs.append(dict(seed=seed,control_retention_pass=False,candidate_retention_pass=True,
            control_interior_pass=True,candidate_interior_pass=True,original_answer_gain=50,original_pair_gain=50,
            interior_answer_gain=0,interior_pair_gain=0,interior=contrast(0),
            original_by_length={str(n):contrast(10) for n in range(2,7)},paired_success=True))
    return dict(candidate_gate=True,paired_success_count=5,seed_results=rows,paired_comparisons=pairs,
                all_pairs_matched=True,all_replays=True,**s.WORK)


def parent_fixture():
    primary={e.B_PATH:e.BOOTSTRAP[e.B_PATH],**{f'primary{i}':'a'*40 for i in range(791)}}
    extra=(e.R4_PATH,e.R6_PATH,*tuple(f'extra{i}' for i in range(8)))
    added={name:e.BOOTSTRAP.get(name,'b'*40) for name in extra}
    inputs={f'input{i}':'c'*64 for i in range(1501)}
    result=dict(commit_sha=e.PARENT_EXECUTION,status='FAIL',validation_summary=dict(candidate_gate=False),
                source_blobs=primary,input_sha256={k:v for i,(k,v) in enumerate(inputs.items()) if i<1491})
    envelope=dict(schema='fold-c324-r6-execution-envelope-v1',role='C324-R6-SCIENTIFIC-RECOVERY',
        commit_sha=e.PARENT_EXECUTION,scientific_summary_sha256=e.PARENT_SUMMARY,scientific_status='FAIL',
        source_count=802,input_count=1501,source_blobs={**primary,**added},input_sha256=inputs,
        base_scientific_manifest_sha256='d'*64,scientific_work={'models':10},
        regression=dict(commit_sha=e.PARENT_EXECUTION,tests=5490,failures=0,errors=0,skipped=0,successful=True),
        verifier_stats={name:dict(executions=1,failures=0,reused=9 if i==0 else 0) for i,name in enumerate(sorted(e.VERIFIERS))},
        real_parent_loader_calls=1,parsed_parent_reads=3,final_reference_rechecks=1501,
        hash_stats=dict(final_reference_rechecks=1501),saved_semantic_reconstruction=True)
    b=NS(validate_seal=lambda:None,validate_result=lambda r:None,MANIFEST_SHA='d'*64,WORK={'models':10})
    r6=NS(EXTRA=extra,FIXED=dict(e.BOOTSTRAP))
    return result,envelope,b,r6


def receipt():
    return dict(commit_sha='a'*40,tests=s.FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)


def git_fixture(path):
    subprocess.run(['git','init','-q',str(path)],check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C325 fixture'),('config','user.email','c325@example.invalid')]:
        subprocess.run(['git','-C',str(path),*args],check=True,capture_output=True)
    (path/'docs').mkdir(); (path/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC325 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(path),'add','.'],check=True)
    subprocess.run(['git','-C',str(path),'commit','-qm','synthetic fixture'],check=True)
    return e.git(path,'rev-parse','HEAD')


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear=torch.nn.Linear(64,256,bias=False,dtype=torch.float64)
    def forward(self,tokens,tasks):
        return self.linear(tokens.to(torch.float64)/64)


def toy_inputs():
    torch.manual_seed(9); model=Toy()
    original={key:torch.arange(192*64).reshape(192,64)%7 for key in [(4,'repeat')]}
    interior={key:torch.flip(z,[1])+2 for key,z in original.items()}
    ev=torch.zeros((1,24,4),dtype=torch.int64); ev[:,:,0]=4; ev[:,:,2:]=torch.arange(48).reshape(1,24,2)
    def check(z,n):
        s.require(z.shape==(n,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),'toy finite logits')
    x=NS(policy=NS(optimizer_for=lambda m,p:torch.optim.AdamW(m.parameters(),lr=.005,weight_decay=0.),
                   verify_optimizer=lambda *a:None),c=NS(p267=NS(check_logits=check)))
    return model,{'original':original,'interior4':interior},torch.arange(192)%4+48,ev,x


class C325Tests(unittest.TestCase):
    def test_01_manifest_seal(self): s.validate_seal()

    def test_02_manifest_tamper(self):
        with patch.object(s,'STAGE','tampered'),self.assertRaises(ValueError): s.validate_seal()

    def test_03_fresh_paired_cohort(self):
        self.assertEqual(s.SEEDS,tuple(range(325001,325006)))
        self.assertEqual(s.ORDERS,tuple(range(325101,325106)))
        self.assertEqual(len(set(s.identities())),10)
        self.assertFalse(set(s.SEEDS)&set(range(324001,324006)))

    def test_04_work_and_protection(self):
        self.assertEqual(s.WORK['train_steps'],10*1200)
        self.assertEqual(s.WORK['training_rows'],10*1200*48)
        self.assertEqual(s.WORK['model_forward_calls'],10*(1371+171))
        self.assertEqual(s.WORK['row_presentations'],10*(74016+16416))
        self.assertEqual(s.SOURCE_COUNT,802+len(s.OWN))
        self.assertEqual(s.INPUT_COUNT,1501+10+len(s.OWN))
        self.assertEqual(len(s.OUTPUTS),8)

    def test_05_complete_schedule(self): s.validate_schedule(events())

    def test_06_schedule_shape_and_dtype(self):
        for value in (events()[:-1],events().float()):
            with self.subTest(),self.assertRaises(ValueError): s.validate_schedule(value)

    def test_07_schedule_duplicate_row(self):
        z=events(); z[0,0,2]=z[0,0,3]
        with self.assertRaises(ValueError): s.validate_schedule(z)

    def test_08_schedule_bad_domain(self):
        z=events(); z[:4,:,0]=5
        with self.assertRaises(ValueError): s.validate_schedule(z)

    def test_09_schedule_split_epoch(self):
        z=events(); z[0,0,1]=1
        with self.assertRaises(ValueError): s.validate_schedule(z)

    def test_10_schedule_wrong_exposure(self):
        z=events(); z[:4,:,0]=3
        with self.assertRaises(ValueError): s.validate_schedule(z)

    def test_11_control_family_all_interior(self):
        z=events(); f=s.families(z,'interior4')
        self.assertEqual(int(f.sum()),400)
        self.assertTrue(torch.equal(f==1,z[:,0,0]==4))

    def test_12_mixed_exact_half(self):
        z=events(); f=s.families(z,'mixed4')
        self.assertEqual(int(f.sum()),200)
        self.assertEqual(int((f[::4]==1).sum()),50)

    def test_13_no_pair_or_source_mutation(self):
        z=events(); old=z.clone(); s.families(z,'mixed4')
        self.assertTrue(torch.equal(z,old))

    def test_14_per_row_family_exposures(self):
        z=events(); rows=s.family_stats(z,s.families(z,'mixed4'))['family_row_exposures']
        for key,n in {'2:0':100,'2:1':0,'3:0':100,'3:1':0,'4:0':50,'4:1':50}.items(): self.assertEqual(rows[key],[n]*192)

    def test_15_unknown_arm_rejected(self):
        with self.assertRaises(ValueError): s.families(events(),'selected_success')

    def test_16_original_family_first_then_alternating(self):
        z=events(); f=s.families(z,'mixed4'); seen=[int(f[i]) for i in range(0,1200,4) if int(z[i,0,0])==4]
        self.assertEqual(seen,[0,1]*50)
        self.assertTrue(all(len(set(f[i:i+4].tolist()))==1 for i in range(0,1200,4)))

    def test_17_family_schedule_no_rng_consumption(self):
        state=torch.random.get_rng_state(); s.families(events(),'mixed4')
        self.assertTrue(torch.equal(state,torch.random.get_rng_state()))

    def test_18_numeric_loop_reference_parity(self):
        m,t,y,z,x=toy_inputs(); ref=copy.deepcopy(m)
        s.train_steps(m,t,y,z,torch.zeros(1,dtype=torch.int64),x)
        opt=torch.optim.AdamW(ref.parameters(),lr=.005,weight_decay=0.); opt.zero_grad()
        loss=torch.nn.functional.cross_entropy(ref(t['original'][4,'repeat'][:48],torch.zeros(48,dtype=torch.int64)),y[:48]); loss.backward()
        torch.nn.utils.clip_grad_norm_(ref.parameters(),1.,error_if_nonfinite=True); opt.step()
        self.assertTrue(all(torch.equal(a,b) for a,b in zip(m.parameters(),ref.parameters())))

    def test_19_changed_family_changes_updates(self):
        m,t,y,z,x=toy_inputs(); other=copy.deepcopy(m)
        s.train_steps(m,t,y,z,torch.zeros(1,dtype=torch.int64),x)
        s.train_steps(other,t,y,z,torch.ones(1,dtype=torch.int64),x)
        self.assertTrue(any(not torch.equal(a,b) for a,b in zip(m.parameters(),other.parameters())))

    def test_20_nonfinite_training_stops_before_step(self):
        m,t,y,z,x=toy_inputs()
        with patch.object(m,'forward',return_value=torch.full((48,256),float('nan'),dtype=torch.float64)),self.assertRaises(ValueError):
            s.train_steps(m,t,y,z,torch.zeros(1,dtype=torch.int64),x)

    def test_21_gate_all_five(self): self.assertEqual(s.fixed_gate(gate_rows()),(True,[True]*5))

    def test_22_gate_every_condition_required(self):
        for key,value in [('candidate_interior_pass',False),('candidate_retention_pass',False),('original_answer_gain',0),
                          ('original_pair_gain',0),('interior_answer_gain',-1),('interior_pair_gain',-1)]:
            z=gate_rows(); z[2][key]=value
            with self.subTest(key=key): self.assertEqual(s.fixed_gate(z),(False,[True,True,False,True,True]))

    def test_23_failed_seed_not_averaged(self):
        z=gate_rows(); z[4]['candidate_retention_pass']=False
        self.assertFalse(s.fixed_gate(z)[0])

    def test_24_gate_duplicate_or_reordered_seed(self):
        for z in (gate_rows()[:-1],list(reversed(gate_rows())),[gate_rows()[0]]*5):
            with self.subTest(),self.assertRaises(ValueError): s.fixed_gate(z)

    def test_25_bool_is_not_gain(self):
        z=gate_rows(); z[0]['original_answer_gain']=True
        with self.assertRaises(ValueError): s.fixed_gate(z)

    def test_26_zero_original_gain_not_improvement(self):
        z=gate_rows(); z[0]['original_pair_gain']=0
        self.assertFalse(s.fixed_gate(z)[0])

    def test_27_equal_interior_is_retained(self): self.assertTrue(s.fixed_gate(gate_rows())[0])

    def test_28_interior_regression_rejected(self):
        z=gate_rows(); z[0]['interior_answer_gain']=-1
        self.assertFalse(s.fixed_gate(z)[0])

    def test_29_duplicate_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; p.write_text('{"x":1,"x":2}',encoding='utf-8')
            with self.assertRaises(ValueError): e.read(p)

    def test_30_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in ('NaN','Infinity','-Infinity'):
                p.write_text(text,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError): e.read(p)

    def test_31_utf8_json_and_exclusive_write(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; e.save(p,{'名前':'あいうえ'}); self.assertEqual(e.read(p),{'名前':'あいうえ'})
            with self.assertRaises(FileExistsError): e.save(p,{'new':True})

    def test_32_source_lf_and_crlf(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for value in (raw,raw.replace(b'\n',b'\r\n')):
                p.write_bytes(value); self.assertEqual(e.source_bytes(p,oid),value)

    def test_33_source_corruption_and_mixed_endings(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for value in (b'changed',b'a\nb\r\n'):
                p.write_bytes(value)
                with self.subTest(),self.assertRaises(ValueError): e.source_bytes(p,oid)

    def test_34_real_git_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=git_fixture(root); e.guard(root,head)
            self.assertIn('docs/experiment-ledger-and-handoff.md',e.tree_blobs(root))

    def test_35_real_git_dirty_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=git_fixture(root)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError): e.guard(root,head)

    def test_36_real_git_stale_head(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); git_fixture(root)
            with self.assertRaises(ValueError): e.guard(root,'a'*40)

    def test_37_only_unique_formal_active(self):
        self.assertTrue(e.active('## Formal state\nC325 ACTIVE / NOT YET JUDGED\n## History\nC324 ACTIVE / NOT YET JUDGED'))
        for text in ('## History\nC325 ACTIVE / NOT YET JUDGED',
                     '## Formal state\nC324 ACTIVE / NOT YET JUDGED',
                     '## Formal state\nC325 ACTIVE / NOT YET JUDGED\nC326 ACTIVE / NOT YET JUDGED'):
            self.assertFalse(e.active(text))

    def test_38_parent_composite_contract(self):
        with patch.object(e,'canonical',side_effect=str): e.parent_contract(*parent_fixture())

    def test_39_parent_wrong_identity_and_counts(self):
        for key,value in [('schema','wrong'),('commit_sha','a'*40),('scientific_status','PASS'),('source_count',792),('input_count',1491)]:
            r,v,b,r6=parent_fixture(); v[key]=value
            with self.subTest(key=key),patch.object(e,'canonical',side_effect=str),self.assertRaises(ValueError): e.parent_contract(r,v,b,r6)

    def test_40_parent_source_and_input_unions(self):
        for kind in ('source','input','bootstrap'):
            r,v,b,r6=parent_fixture()
            if kind=='source': r['source_blobs']['primary0']='0'*40
            elif kind=='input': r['input_sha256']['input0']='0'*64
            else: v['source_blobs'][e.R4_PATH]='0'*40
            with self.subTest(kind=kind),patch.object(e,'canonical',side_effect=str),self.assertRaises(ValueError): e.parent_contract(r,v,b,r6)

    def test_41_parent_incomplete_verification(self):
        for key,value in [('real_parent_loader_calls',0),('parsed_parent_reads',2),('final_reference_rechecks',1500),('saved_semantic_reconstruction',False)]:
            r,v,b,r6=parent_fixture(); v[key]=value
            with self.subTest(key=key),patch.object(e,'canonical',side_effect=str),self.assertRaises(ValueError): e.parent_contract(r,v,b,r6)
        r,v,b,r6=parent_fixture(); v['verifier_stats'][next(iter(v['verifier_stats']))]['executions']=0
        with patch.object(e,'canonical',side_effect=str),self.assertRaises(ValueError): e.parent_contract(r,v,b,r6)

    def test_42_parent_regression_incomplete(self):
        for key,value in [('tests',5489),('skipped',1),('failures',1),('successful',False)]:
            r,v,b,r6=parent_fixture(); v['regression'][key]=value
            with self.subTest(key=key),patch.object(e,'canonical',side_effect=str),self.assertRaises(ValueError): e.parent_contract(r,v,b,r6)

    def test_43_descriptor_bytes_and_path(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'ok'; p.write_bytes(b'abc'); row=dict(file='ok',sha256=e.sha(p),serialized_bytes=3)
            self.assertEqual(e.descriptors(root,[row],('ok',),e.sha),{e.canonical(p):e.sha(p)})
            for modified in ({**row,'serialized_bytes':4},{**row,'sha256':'0'*64}):
                with self.subTest(),self.assertRaises(ValueError): e.descriptors(root,[modified],('ok',),e.sha)
            with self.assertRaises(ValueError): e.descriptors(root,[dict(file='../ok',sha256='',serialized_bytes=0)],('../ok',),e.sha)

    def test_44_production_order_retains_valid_negative(self):
        calls=[]
        def op(name,value):
            def run(): calls.append(name); return value
            return run
        with contextlib.redirect_stdout(io.StringIO()):
            e.execute_stages('a'*40,op('preflight',None),op('regression',receipt()),op('fit',{'candidate_gate':False}),
                op('saved',([],{'candidate_gate':False})),op('final',[]))
        self.assertEqual(calls,['preflight','regression','fit','saved','final'])

    def test_45_failed_regression_never_fits(self):
        fit=unittest.mock.Mock(); bad={**receipt(),'failures':1,'successful':False}
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages('a'*40,lambda:None,lambda:bad,fit,lambda:None,lambda:None)
        fit.assert_not_called()

    def test_46_saved_mismatch_never_finalizes(self):
        final=unittest.mock.Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages('a'*40,lambda:None,receipt,lambda:{'gate':False},lambda:([],{'gate':True}),final)
        final.assert_not_called()

    def test_47_semantic_suite_inventory(self):
        class Case(unittest.TestCase):
            def __init__(self,i): super().__init__(); self.number=i
            def id(self): return 'fixture.'+str(self.number)
        inherited=[Case(i) for i in range(5490)]
        r6=NS(flatten=lambda suite:iter(suite),combined_suite=lambda b,root:inherited,RECOVERY_MODULES=('a','b','c'))
        b=NS(EXCLUDED='excluded',regression_modules=lambda root:list(range(210)))
        # The real own loader is used; the historical fixture is explicit and is not run.
        def flatten(suite):
            for test in suite:
                if isinstance(test,unittest.TestSuite): yield from flatten(test)
                else: yield test
        r6.flatten=flatten
        full=e.suite(ROOT,b,r6); self.assertEqual(full.countTestCases(),s.FULL_TESTS)
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),s.OWN_TESTS)
        inherited[-1]=inherited[0]
        with self.assertRaises(ValueError): e.suite(ROOT,b,r6)

    def test_48_real_subprocess_error_preserved(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(d)
            with self.assertRaises(ValueError): e.subprocess_run(ROOT,folder,'a'*40,'invalid-mode')
            self.assertIn('invalid choice',(folder/'invalid-mode.log').read_text(encoding='utf-8'))

    def test_49_saved_validation_positive(self): e.check_validation(validation())

    def test_50_saved_validation_negative(self):
        value=validation(); value['seed_results'][1]['original_pass']['4']=False
        value['seed_results'][1]['retention_pass']=False
        value['paired_comparisons'][0]['candidate_retention_pass']=False
        value['paired_comparisons'][0]['paired_success']=False
        value['candidate_gate']=False; value['paired_success_count']=4
        e.check_validation(value)

    def test_51_saved_count_conservation(self):
        for key in ('answer_gain','rescued','candidate_correct'):
            value=validation(); value['paired_comparisons'][0]['interior'][key]+=1
            with self.subTest(key=key),self.assertRaises(ValueError): e.check_validation(value)

    def test_52_saved_work_and_cohort(self):
        value=validation(); value['train_steps']-=1
        with self.assertRaises(ValueError): e.check_validation(value)
        value=validation(); value['seed_results'].pop()
        with self.assertRaises(ValueError): e.check_validation(value)

    def test_53_real_safe_model_bundle(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'models.pt'; value=dict(schema='fold-c325-models-v1',identities=[list(x) for x in s.identities()],
                readout_policy='mean_last',states=[{'w':torch.zeros(2,dtype=torch.float64)} for _ in range(10)])
            torch.save(value,p); self.assertEqual(len(s.load_bundle(p)),10)
            value['identities'].reverse(); torch.save(value,p)
            with self.assertRaises(ValueError): s.load_bundle(p)

    def test_54_committed_source_call_order_contract(self):
        tree=ast.parse(inspect.getsource(e.scientific_worker)); names=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                f=node.func; names.append(f.attr if isinstance(f,ast.Attribute) else f.id if isinstance(f,ast.Name) else '')
        for name in ('snapshot','parent_semantics','execute_stages','runtime_preflight','run_science','semantic_recheck'):
            self.assertIn(name,names)
        self.assertNotIn('patch',names)
        self.assertTrue(set(e.BOOTSTRAP)<= {e.B_PATH,e.R4_PATH,e.R6_PATH})

    def test_55_controller_failure_no_auto_retry(self):
        with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run',side_effect=ValueError('native failure')) as run,contextlib.redirect_stdout(io.StringIO()) as out:
            root=Path(d)
            with self.assertRaises(ValueError): e.run(root,root/'runs'/'child','a'*40)
            self.assertEqual(run.call_count,1); self.assertIn('run_execution_valid = false',out.getvalue())

    def test_56_controller_science_then_fresh_verify(self):
        with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run') as run,contextlib.redirect_stdout(io.StringIO()) as out:
            root=Path(d); e.run(root,root/'runs'/'child','a'*40)
            self.assertEqual([c.args[-1] for c in run.call_args_list],['science','verify'])
            self.assertIn('run_execution_valid = true',out.getvalue())


if __name__=='__main__': unittest.main()
