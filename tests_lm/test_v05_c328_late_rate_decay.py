"""C328 authoring fixtures are software checks, not native FOLD scientific results."""
from __future__ import annotations
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import numpy as np
import torch
from fold_lm.v05_benchmarks import model_c328_late_rate_decay as s

ROOT=Path(__file__).resolve().parents[1]
_loader=importlib.util.spec_from_file_location('_c328_test_execution',ROOT/'tools/c328_execution.py')
e=importlib.util.module_from_spec(_loader); _loader.loader.exec_module(e)


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone=torch.nn.Module(); self.backbone.core=torch.nn.Linear(2,2,bias=False,dtype=torch.float64)
        self.head=torch.nn.Linear(2,256,bias=False,dtype=torch.float64)
    def forward(self,tokens,tasks): return self.head(self.backbone.core(tokens.to(torch.float64)/10))


def optimizer(model):
    core=list(model.backbone.core.parameters()); ids={id(p) for p in core}
    return torch.optim.AdamW([{'params':[p for p in model.parameters() if id(p) not in ids],'lr':.005},
                              {'params':core,'lr':.0005}],lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)


def toy():
    torch.manual_seed(91); m=Toy(); tokens=torch.tensor([[1,2],[3,4],[2,1],[4,3]],dtype=torch.int64); targets=torch.tensor([48,49,48,49],dtype=torch.int64)
    def select(tables,ev,mask): return tokens,torch.arange(4)
    def check(z,n): s.require(z.shape==(n,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),'toy logits')
    policy=NS(optimizer_for=lambda model,arm:optimizer(model),verify_optimizer=lambda opt,model,arm:s.optimizer_contract(opt,model))
    return m,tokens,targets,NS(select_tokens=select),NS(policy=policy,c=NS(p267=NS(check_logits=check)))


def populated():
    m,t,y,_,_=toy(); opt=optimizer(m); contract=s.optimizer_contract(opt,m)
    torch.nn.functional.cross_entropy(m(t,torch.zeros(4,dtype=torch.int64)),y).backward(); opt.step()
    return m,opt,contract


def gates():
    return [dict(seed=k,candidate_interior_pass=True,candidate_retention_pass=True,original_answer_gain=0,original_pair_gain=0,interior_answer_gain=1,interior_pair_gain=1) for k in s.SEEDS]


def contrast(gain):
    return dict(answers=288,query_pairs=144,control_correct=100,candidate_correct=100+gain,control_both_correct=50,candidate_both_correct=50+gain,rescued=max(0,gain),regressed=max(0,-gain),pair_rescued=max(0,gain),pair_regressed=max(0,-gain),answer_gain=gain,query_pair_gain=gain)


def validation():
    seeds=[]; pairs=[]
    for seed in s.SEEDS:
        for arm in s.ARMS: seeds.append(dict(seed=seed,arm=arm,original_pass={str(n):True for n in range(2,7)},retention_pass=True,interior_pass=arm=='late_tenth'))
        pairs.append(dict(seed=seed,control_retention_pass=True,candidate_retention_pass=True,control_interior_pass=False,candidate_interior_pass=True,original_answer_gain=0,original_pair_gain=0,interior_answer_gain=1,interior_pair_gain=1,interior=contrast(1),original_by_length={str(n):contrast(0) for n in range(2,7)},first800_matched=True,paired_success=True))
    return dict(candidate_gate=True,paired_success_count=5,seed_results=seeds,paired_comparisons=pairs,all_pairs_matched=True,all_replays=True,all_first800_matched=True,**s.WORK)


def pair_records():
    r=dict(initial_sha256='a'*64,core_initial_sha256='b'*64,fit=dict(schedule_events=torch.arange(12).reshape(3,4),template_pair_events=torch.zeros((3,2),dtype=torch.int64),family_exposure={'x':[1,1]},boundary={'weights':'c'*64,'optimizer':'d'*64},ce_history=[.1]*1200,switch={'before':'e'*64}))
    return r,copy.deepcopy(r)


def parent_fixture():
    pins={**e.BOOTSTRAP,**{f'pin{i}':'a'*40 for i in range(820-len(e.BOOTSTRAP))}}; inputs={f'input{i}':'b'*64 for i in range(1549)}
    r=dict(schema='fold-c327-diagnostic-v1',experiment_id='parent',stage='stage',commit_sha=e.PARENT_EXECUTION,status='PASS',diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,source_blobs=dict(pins),input_sha256=dict(inputs),manifest_sha256='c'*64,validation_summary={})
    v=dict(schema='fold-c327-execution-envelope-v1',commit_sha=e.PARENT_EXECUTION,scientific_summary_sha256=e.PARENT_SUMMARY,scientific_status='PASS',source_count=820,input_count=1549,source_blobs=pins,input_sha256=inputs,manifest_sha256='c'*64,scientific_work={'optimizer_steps':0},parent_summary_sha256='d'*64,parent_envelope_sha256='f'*64,immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=1549,hash_stats={'final_reference_rechecks':1549},regression=dict(commit_sha=e.PARENT_EXECUTION,tests=5658,failures=0,errors=0,skipped=0,successful=True))
    p=NS(validate_seal=lambda:None,EXPERIMENT_ID='parent',STAGE='stage',OWN=(e.P_PATH,e.E_PATH),MANIFEST_SHA='c'*64,WORK={'optimizer_steps':0})
    h=NS(check_validation=lambda value:None,BOOTSTRAP={},PARENT_SUMMARY='d'*64,PARENT_ENVELOPE='f'*64)
    return r,v,p,h


def receipt(): return dict(commit_sha='a'*40,tests=s.FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C328 fixture'),('config','user.email','c328@example.invalid')]: subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    (root/'docs').mkdir(); (root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC328 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True); subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
    return e.git(root,'rev-parse','HEAD')


class C328Tests(unittest.TestCase):
    def test_01_manifest(self): s.validate_seal()
    def test_02_manifest_tamper(self):
        with patch.object(s,'SWITCH',700),self.assertRaises(ValueError): s.validate_seal()
    def test_03_fresh_cohort(self):
        self.assertEqual(s.SEEDS,tuple(range(328001,328006))); self.assertEqual(s.ORDERS,tuple(range(328101,328106))); self.assertEqual(len(set(s.identities())),10)
    def test_04_budget_and_six_diagnostic_parent_files(self):
        self.assertEqual(s.WORK['training_rows'],1200*48*10); self.assertEqual(s.WORK['model_forward_calls'],10*(1371+171)); self.assertEqual(s.WORK['row_presentations'],10*(74016+16416))
        self.assertEqual(s.SOURCE_COUNT,820+len(s.OWN)); self.assertEqual(s.INPUT_COUNT,1549+6+len(s.OWN)); self.assertEqual(s.FULL_TESTS,5658+s.OWN_TESTS)
    def test_05_exact_switch_boundary(self):
        self.assertEqual(s.rates_for('late_tenth',799),s.RATES); self.assertEqual(s.rates_for('late_tenth',800),tuple(v*.1 for v in s.RATES))
    def test_06_constant_all_steps(self): self.assertTrue(all(s.rates_for('constant',i)==s.RATES for i in range(1200)))
    def test_07_candidate_exact_counts(self): self.assertEqual(sum(s.rates_for('late_tenth',i)==s.RATES for i in range(1200)),800)
    def test_08_rate_identity_rejections(self):
        for arm,step in [('bad',0),('constant',-1),('constant',1200),('constant',True),('constant',1.)]:
            with self.subTest(),self.assertRaises(ValueError): s.rates_for(arm,step)
    def test_09_state_hash_order(self): self.assertEqual(s.state_hash({'a':1,'b':torch.ones(2)}),s.state_hash({'b':torch.ones(2),'a':1}))
    def test_10_state_hash_value(self): self.assertNotEqual(s.state_hash(torch.ones(2)),s.state_hash(torch.zeros(2)))
    def test_11_state_nonfinite_rejected(self):
        for v in (float('nan'),torch.tensor(float('inf'))):
            with self.subTest(),self.assertRaises(ValueError): s.state_hash(v)
    def test_12_state_dtype_shape_and_container(self):
        self.assertNotEqual(s.state_hash(torch.ones(2)),s.state_hash(torch.ones(2,dtype=torch.float64))); self.assertNotEqual(s.state_hash(torch.ones(2)),s.state_hash(torch.ones(1,2))); self.assertNotEqual(s.state_hash([1]),s.state_hash((1,)))
    def test_13_state_bad_type(self):
        for v in ({True:1},{(1,):2},object()):
            with self.subTest(),self.assertRaises(ValueError): s.state_hash(v)
    def test_14_real_optimizer_contract(self):
        m,_,_,_,_=toy(); opt=optimizer(m); c=s.optimizer_contract(opt,m); s.verify_optimizer(opt,c,s.RATES)
    def test_15_optimizer_group_order_rejected(self):
        m,_,_,_,_=toy(); opt=optimizer(m); opt.param_groups.reverse()
        with self.assertRaises(ValueError): s.optimizer_contract(opt,m)
    def test_16_wrong_initial_rate(self):
        m,_,_,_,_=toy(); opt=optimizer(m); opt.param_groups[0]['lr']=.1
        with self.assertRaises(ValueError): s.optimizer_contract(opt,m)
    def test_17_wrong_betas(self):
        m,_,_,_,_=toy(); opt=optimizer(m); opt.param_groups[0]['betas']=(.8,.99)
        with self.assertRaises(ValueError): s.optimizer_contract(opt,m)
    def test_18_frozen_parameters_rejected(self):
        m,_,_,_,_=toy(); opt=optimizer(m); m.backbone.core.requires_grad_(False)
        with self.assertRaises(ValueError): s.optimizer_contract(opt,m)
    def test_19_other_group_setting_immutable(self):
        m,_,_,_,_=toy(); opt=optimizer(m); c=s.optimizer_contract(opt,m); opt.param_groups[0]['eps']=1e-6
        with self.assertRaises(ValueError): s.verify_optimizer(opt,c,s.RATES)
    def test_20_optimizer_defaults_immutable(self):
        m,_,_,_,_=toy(); opt=optimizer(m); c=s.optimizer_contract(opt,m); opt.defaults['lr']=.2
        with self.assertRaises(ValueError): s.verify_optimizer(opt,c,s.RATES)
    def test_21_optimizer_recreation_rejected(self):
        m,_,_,_,_=toy(); opt=optimizer(m); c=s.optimizer_contract(opt,m)
        with self.assertRaises(ValueError): s.verify_optimizer(optimizer(m),c,s.RATES)
    def test_22_populated_moments_preserved(self):
        m,opt,c=populated(); before=s.state_hash(opt.state_dict()['state']); weights=s.state_hash(m.state_dict()); r=s.assign_rates(opt,c,'late_tenth',800)
        self.assertEqual(r['before'],before); self.assertEqual(r['after'],before); self.assertEqual(s.state_hash(m.state_dict()),weights)
    def test_23_group_membership_immutable(self):
        m,_,_,_,_=toy(); opt=optimizer(m); c=s.optimizer_contract(opt,m); opt.param_groups[0]['params']=list(m.backbone.core.parameters())
        with self.assertRaises(ValueError): s.verify_optimizer(opt,c,s.RATES)
    def test_24_constant_switch_preserves_entire_state(self):
        _,opt,c=populated(); before=s.state_hash(opt.state_dict()); s.assign_rates(opt,c,'constant',800); self.assertEqual(s.state_hash(opt.state_dict()),before)
    def test_25_moments_not_scaled_with_rate(self):
        _,opt,c=populated(); state=copy.deepcopy(opt.state_dict()['state']); s.assign_rates(opt,c,'late_tenth',800)
        self.assertEqual(s.state_hash(state),s.state_hash(opt.state_dict()['state'])); self.assertTrue(all(float(v['step'])==1 for v in opt.state_dict()['state'].values()))
    def test_26_constant_numeric_reference_parity(self):
        m,t,y,p,x=toy(); ref=copy.deepcopy(m)
        with patch.object(s,'STEPS',4),patch.object(s,'SWITCH',2),patch.object(s,'previous',return_value=p),contextlib.redirect_stdout(io.StringIO()): s.optimize(m,{},y,[None]*4,[None]*4,'constant',x)
        opt=optimizer(ref)
        for _ in range(4):
            opt.zero_grad(set_to_none=True); torch.nn.functional.cross_entropy(ref(t,torch.zeros(4,dtype=torch.int64)),y).backward(); torch.nn.utils.clip_grad_norm_(ref.parameters(),1.,error_if_nonfinite=True); opt.step()
        self.assertTrue(all(torch.equal(a,b) for a,b in zip(m.parameters(),ref.parameters())))
    def test_27_real_1200_updates_common800_prefix(self):
        m,t,y,p,x=toy(); other=copy.deepcopy(m); created=[]; factory=x.policy.optimizer_for
        def make(model,arm): created.append(model); return factory(model,arm)
        x.policy.optimizer_for=make
        with patch.object(s,'previous',return_value=p),contextlib.redirect_stdout(io.StringIO()):
            a=s.optimize(m,{},y,[None]*1200,[None]*1200,'constant',x); c=s.optimize(other,{},y,[None]*1200,[None]*1200,'late_tenth',x)
        self.assertEqual(len(created),2); self.assertEqual(a['boundary'],c['boundary']); self.assertEqual(a['ce_history'][:800],c['ce_history'][:800]); self.assertEqual(a['switch']['before'],c['switch']['before']); self.assertEqual(c['switch']['before'],c['switch']['after'])
        self.assertEqual(a['optimizer_group_lrs'],[list(s.RATES)]*1200); self.assertEqual(c['optimizer_group_lrs'],[list(s.rates_for('late_tenth',i)) for i in range(1200)])
        self.assertNotEqual(s.state_hash(m.state_dict()),s.state_hash(other.state_dict()))
    def test_28_bad_workload_never_creates_optimizer(self):
        m,_,y,p,x=toy(); x.policy.optimizer_for=Mock()
        with self.assertRaises(ValueError): s.optimize(m,{},y,[],[],'constant',x)
        x.policy.optimizer_for.assert_not_called()
    def test_29_rate_attenuation_exact_toy_step(self):
        m,opt,c=populated(); a={k:v.clone() for k,v in m.state_dict().items()}; clone=copy.deepcopy(m); ref=optimizer(clone); ref.load_state_dict(copy.deepcopy(opt.state_dict()))
        for q in clone.parameters(): q.grad=None
        s.assign_rates(opt,c,'late_tenth',800)
        for q,z in zip(m.parameters(),clone.parameters()): q.grad=torch.ones_like(q); z.grad=torch.ones_like(z)
        opt.step(); ref.step()
        for k,v in m.state_dict().items(): self.assertTrue(torch.allclose(v-a[k],(clone.state_dict()[k]-a[k])*.1,atol=1e-14,rtol=1e-10))
    def test_30_nonfinite_before_step(self):
        m,t,y,p,x=toy()
        with patch.object(s,'previous',return_value=p),patch.object(m,'forward',return_value=torch.full((4,256),float('nan'),dtype=torch.float64)),self.assertRaises(ValueError): s.optimize(m,{},y,[None]*1200,[None]*1200,'constant',x)
    def test_31_paired_prefix_valid(self): s.check_pair(*pair_records())
    def test_32_paired_boundary_and_loss_tamper(self):
        for kind in ('weights','optimizer','loss','moments'):
            a,c=pair_records()
            if kind in ('weights','optimizer'): c['fit']['boundary'][kind]='bad'
            elif kind=='loss': c['fit']['ce_history'][799]=.2
            else: c['fit']['switch']['before']='bad'
            with self.subTest(),self.assertRaises(ValueError): s.check_pair(a,c)
    def test_33_paired_row_order_tamper(self):
        a,c=pair_records(); c['fit']['schedule_events'][0,0]=99
        with self.assertRaises(ValueError): s.check_pair(a,c)
    def test_34_paired_mask_tamper(self):
        a,c=pair_records(); c['fit']['template_pair_events'][0,0]=1
        with self.assertRaises(ValueError): s.check_pair(a,c)
    def test_35_paired_initial_and_exposure_tamper(self):
        for kind in ('initial','exposure'):
            a,c=pair_records()
            if kind=='initial': c['initial_sha256']='bad'
            else: c['fit']['family_exposure']['x']=[2,0]
            with self.subTest(),self.assertRaises(ValueError): s.check_pair(a,c)
    def test_36_full_gate(self): self.assertEqual(s.fixed_gate(gates()),(True,[True]*5))
    def test_37_each_gate_required(self):
        for key,v in [('candidate_interior_pass',False),('candidate_retention_pass',False),('interior_answer_gain',0),('interior_pair_gain',0),('original_answer_gain',-1),('original_pair_gain',-1)]:
            rows=gates(); rows[2][key]=v
            with self.subTest(key=key): self.assertEqual(s.fixed_gate(rows),(False,[True,True,False,True,True]))
    def test_38_gate_complete_cohort(self):
        for rows in (gates()[:-1],gates()[::-1],[gates()[0]]*5):
            with self.subTest(),self.assertRaises(ValueError): s.fixed_gate(rows)
    def test_39_boolean_gain_rejected_and_safe_bundle(self):
        rows=gates(); rows[0]['interior_answer_gain']=True
        with self.assertRaises(ValueError): s.fixed_gate(rows)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'models.pt'; v=dict(schema='fold-c328-models-v1',identities=[list(r) for r in s.identities()],readout_policy='mean_last',states=[{'w':torch.zeros(2)} for _ in range(10)])
            torch.save(v,path); self.assertEqual(len(s.load_bundle(path)),10); v['identities'].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): s.load_bundle(path)
    def test_40_single_failure_not_averaged(self):
        rows=gates(); rows[4]['candidate_retention_pass']=False; self.assertFalse(s.fixed_gate(rows)[0])
    def test_41_contrast_conservation(self):
        e.check_contrast(contrast(-2))
        for key in ('answer_gain','query_pair_gain','rescued','pair_rescued','answers'):
            row=contrast(2); row[key]+=1
            with self.subTest(),self.assertRaises(ValueError): e.check_contrast(row)
    def test_42_saved_validation_and_tamper(self):
        e.check_validation(validation())
        for kind in ('prefix','work','cohort','gain','gate'):
            v=validation()
            if kind=='prefix': v['paired_comparisons'][0]['first800_matched']=False
            elif kind=='work': v['train_steps']-=1
            elif kind=='cohort': v['seed_results'].pop()
            elif kind=='gain': v['paired_comparisons'][0]['interior_answer_gain']+=1
            else: v['candidate_gate']=False
            with self.subTest(kind=kind),self.assertRaises(ValueError): e.check_validation(v)
        v=validation(); v['seed_results'][1]['interior_pass']=False; v['paired_comparisons'][0]['candidate_interior_pass']=False; v['paired_comparisons'][0]['paired_success']=False; v['candidate_gate']=False; v['paired_success_count']=4; e.check_validation(v)
    def test_43_actual_diagnostic_parent_contract(self):
        e.parent_contract(*parent_fixture()); args=parent_fixture(); args[0]['schema']='fold-c326-science-v1'
        with self.assertRaises(ValueError): e.parent_contract(*args)
    def test_44_parent_union_counts(self):
        for k,v in [('source_count',814),('input_count',1533)]:
            args=parent_fixture(); args[1][k]=v
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_45_parent_not_capability_pass(self):
        args=parent_fixture(); args[0]['capability_gate_applicable']=True
        with self.assertRaises(ValueError): e.parent_contract(*args)
    def test_46_parent_source_input_binding(self):
        for kind in ('source_blobs','input_sha256'):
            args=parent_fixture(); args[0][kind][next(iter(args[0][kind]))]='bad'
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_47_parent_hash_and_direct_pin(self):
        for kind in ('hash','pin'):
            args=parent_fixture()
            if kind=='hash': args[1]['scientific_summary_sha256']='bad'
            else: args[0]['source_blobs'][e.E_PATH]='bad'; args[1]['source_blobs'][e.E_PATH]='bad'
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_48_parent_complete_regression(self):
        for key,v in [('tests',5657),('skipped',1),('successful',False)]:
            args=parent_fixture(); args[1]['regression'][key]=v
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_49_parent_final_semantic_checks(self):
        for key,v in [('final_reference_rechecks',1548),('saved_semantic_reconstruction',False),('ancestor_semantic_reruns',1)]:
            args=parent_fixture(); args[1][key]=v
            with self.subTest(),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_50_duplicate_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; p.write_text('{"a":1,"a":2}',encoding='utf-8')
            with self.assertRaises(ValueError): e.read(p)
    def test_51_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in ('NaN','Infinity','-Infinity'):
                p.write_text(text,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError): e.read(p)
    def test_52_unicode_exclusive_save(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'; e.save(p,{'名前':'あいうえ'}); self.assertEqual(e.read(p),{'名前':'あいうえ'})
            with self.assertRaises(FileExistsError): e.save(p,{})
    def test_53_source_lf_crlf_corruption(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for text in (raw,raw.replace(b'\n',b'\r\n')): p.write_bytes(text); self.assertEqual(e.source_bytes(p,oid),text)
            for text in (b'bad',b'a\nb\r\n'):
                p.write_bytes(text)
                with self.subTest(),self.assertRaises(ValueError): e.source_bytes(p,oid)
    def test_54_real_git_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=git_fixture(root); e.guard(root,head)
            with self.assertRaises(ValueError): e.guard(root,'a'*40)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError): e.guard(root,head)
    def test_55_unique_active_only_formal(self):
        self.assertTrue(e.active('## Formal state\nC328 ACTIVE / NOT YET JUDGED\n## History\nC327 ACTIVE / NOT YET JUDGED'))
        for text in ('## History\nC328 ACTIVE / NOT YET JUDGED','## Formal state\nC327 ACTIVE / NOT YET JUDGED','## Formal state\nC328 ACTIVE / NOT YET JUDGED\nC329 ACTIVE / NOT YET JUDGED'): self.assertFalse(e.active(text))
    def test_56_semantic_suite_actual_own_loader(self):
        class Case(unittest.TestCase):
            def __init__(self,i): super().__init__(); self.number=i
            def id(self): return 'fixture.'+str(self.number)
        inherited=[Case(i) for i in range(5658)]
        def flatten(suite):
            for t in suite:
                if isinstance(t,unittest.TestSuite): yield from flatten(t)
                else: yield t
        b=NS(EXCLUDED='excluded',regression_modules=lambda root:list(range(210))); helper=NS(suite=lambda *args:inherited); r6=NS(flatten=flatten,RECOVERY_MODULES=('a','b','c'))
        self.assertEqual(e.suite(ROOT,b,helper,None,None,r6).countTestCases(),s.FULL_TESTS); self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),s.OWN_TESTS)
        inherited[-1]=inherited[0]
        with self.assertRaises(ValueError): e.suite(ROOT,b,helper,None,None,r6)
    def test_57_valid_negative_production_order(self):
        calls=[]
        def step(name,v):
            def run(): calls.append(name); return v
            return run
        with contextlib.redirect_stdout(io.StringIO()): e.execute_stages('a'*40,step('preflight',None),step('tests',receipt()),step('fit',{'gate':False}),step('verify',([],{'gate':False})),step('final',[]))
        self.assertEqual(calls,['preflight','tests','fit','verify','final'])
    def test_58_preflight_failure_no_tests(self):
        tests=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError): e.execute_stages('a'*40,Mock(side_effect=ValueError('native')),tests,Mock(),Mock(),Mock())
        tests.assert_not_called()
    def test_59_regression_failure_no_fit(self):
        fit=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError): e.execute_stages('a'*40,lambda:None,lambda:{**receipt(),'failures':1},fit,Mock(),Mock())
        fit.assert_not_called()
    def test_60_saved_mismatch_no_finalize(self):
        final=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError): e.execute_stages('a'*40,lambda:None,receipt,lambda:{'gate':False},lambda:([],{'gate':True}),final)
        final.assert_not_called()
    def test_61_output_hash_binding(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in s.OUTPUTS: (root/name).write_bytes(b'fixture')
            self.assertEqual(e.bound_semantics(root,lambda:'ok')[0],'ok')
            def mutate(): (root/s.OUTPUTS[0]).write_bytes(b'bad')
            with self.assertRaises(ValueError): e.bound_semantics(root,mutate)
    def test_62_controller_no_retry_and_subprocess_evidence(self):
        for fail in (False,True):
            with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run',side_effect=ValueError('native') if fail else None) as child,contextlib.redirect_stdout(io.StringIO()) as out:
                root=Path(d)
                if fail:
                    with self.assertRaises(ValueError): e.run(root,root/'runs/x','a'*40)
                    self.assertEqual(child.call_count,1); self.assertIn('run_execution_valid = false',out.getvalue())
                else:
                    e.run(root,root/'runs/x','a'*40); self.assertEqual([c.args[-1] for c in child.call_args_list],['science','verify'])
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError): e.subprocess_run(ROOT,Path(d),'a'*40,'invalid-mode')
            self.assertIn('invalid choice',(Path(d)/'invalid-mode.log').read_text(encoding='utf-8'))
    def test_63_source_and_launcher_contract(self):
        tree=ast.parse(inspect.getsource(s.optimize)); attrs=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertEqual(attrs.count('optimizer_for'),1); self.assertIn('step',attrs)
        text=(ROOT/'tools/invoke_c328.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'): self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C328',text); self.assertIn('run_c328.ps1',text)
        self.assertNotIn('patch',inspect.getsource(e.scientific_worker))
    def test_64_actual_worker_with_synthetic_dependencies(self):
        for bad in (False,True): self.worker_fixture(bad)

    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d); folder=root/'runs/x'; folder.mkdir(parents=True); calls=[]
            pins={f'p{i}':'a'*40 for i in range(s.SOURCE_COUNT)}; inputs={str(root/f'i{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={}; stats={'final_reference_rechecks':s.INPUT_COUNT}
                def __init__(self,*args,**kwargs): pass
                def __enter__(self): return self
                def __exit__(self,*args): calls.append('release')
                def recheck(self): calls.append('final'); return [{'path':k,'sha256':v} for k,v in inputs.items()]
            r4=NS(WinAPI=lambda:None,lock_probe=lambda *args:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            cx=(None,None,None,None,None,NS(guarded=NS(no_neural=contextlib.nullcontext))); b=NS(context=lambda:cx,check_dependencies=lambda *args:None,peak_rss=lambda:1)
            v=validation()
            def snap(*args): calls.append('snapshot'); return {},{},pins,inputs
            def parent_data(*args): calls.append('parent'); return {'TRAIN':[]},{},{}
            def preflight(*args): calls.append('preflight')
            def tests(*args):
                calls.append('tests'); r=receipt()
                if bad: r.update(failures=1,successful=False)
                e.save(folder/'regression-result.json',r)
            def fit(out,*args):
                calls.append('fit')
                for name in s.OUTPUTS: (out/name).write_bytes(b'fixture')
                return v
            def saved(*args): calls.append('saved'); return [],v
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(NS(),NS(native_runtime=lambda:(torch,np)),NS(),r4,None)),patch.object(e,'parent',return_value=NS()),patch.object(s,'base',return_value=b),patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=parent_data),patch.object(e,'subprocess_run',side_effect=tests),patch.object(s,'runtime_preflight',side_effect=preflight),patch.object(s,'run_science',side_effect=fit),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError): e.scientific_worker(root,folder,'a'*40)
                    self.assertNotIn('fit',calls)
                else:
                    e.scientific_worker(root,folder,'a'*40); self.assertEqual(calls,['snapshot','parent','preflight','tests','fit','saved','final','release']); self.assertEqual(e.read(folder/'execution-envelope.json')['source_count'],s.SOURCE_COUNT)


if __name__=='__main__': unittest.main()
