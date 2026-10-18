"""C331 software fixtures; synthetic historical inventories are not native science."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c331_frozen_first_mean_query as s

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c331_executor_tests', ROOT/'tools/c331_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def span(tokens):
    return (tokens >= 10) & (tokens <= 12)


class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.values = torch.nn.Parameter(torch.arange(64*16, dtype=torch.float64).reshape(1,64,16)/100)
    def forward(self, tokens):
        return (self.values.expand(len(tokens),-1,-1),)


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone = torch.nn.Module(); self.backbone.local_encoder = Encoder()
        self.read = torch.nn.Module(); self.read.query = torch.nn.Linear(16,16,bias=False,dtype=torch.float64)
        self.read.output = torch.nn.Linear(16,256,bias=False,dtype=torch.float64)
        with torch.no_grad():
            self.read.query.weight.copy_(torch.eye(16,dtype=torch.float64))
            self.read.output.weight.copy_(torch.arange(256*16,dtype=torch.float64).reshape(256,16)/4096)
    def forward(self, tokens, tasks):
        z = self.backbone.local_encoder(tokens)[0]*(tokens != 256)[:,:,None]
        mask = span(tokens); pos = torch.arange(64).expand_as(tokens)
        mean = (z*mask[:,:,None]).sum(1)/mask.sum(1,keepdim=True)
        last = z[torch.arange(len(z)),torch.where(mask,pos,-1).max(1).values]
        a = self.read.query(mean); b = self.read.query(last)
        return self.read.output(.5*(a+b))


def tokens(one=False):
    x = torch.full((2,64),256,dtype=torch.int64)
    x[:,2] = 10
    if not one: x[:,3:5] = 11
    return x


def state_hash(model):
    return hashlib.sha256(b''.join(z.detach().numpy().tobytes() for z in model.state_dict().values())).hexdigest()


def raw_fixture():
    data = {'TRAIN':[{'language':'en'},{'language':'ja'}], 'HOLDOUT':[{'language':'en'},{'language':'ja'}]}
    def views(): return {k:torch.zeros((2,256),dtype=torch.float64) for k in ('normal','evidence_blind','query_blind')}
    raw = dict(original={str(n):{sp:{p:views() for p in (('repeat',) if n==1 else ('repeat','shared_prefix','shared_suffix'))} for sp in data} for n in range(1,7)},
               interior={sp:{p:views() for p in ('u_dominant','balanced','v_dominant')} for sp in data})
    return raw,data


def contrast(gain=0):
    return dict(answers=288,query_pairs=144,control_correct=100,candidate_correct=100+gain,
        control_both_correct=50,candidate_both_correct=50+gain,rescued=max(gain,0),regressed=max(-gain,0),
        pair_rescued=max(gain,0),pair_regressed=max(-gain,0),answer_gain=gain,query_pair_gain=gain)


def summary():
    flags = dict(original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True,
                 failures={**{'original'+str(n):dict(local=0,order=0) for n in range(2,7)},'interior4':dict(local=0,order=0)})
    effects = [dict(seed=seed,arm=arm,native=copy.deepcopy(flags),first_mean=copy.deepcopy(flags),
                   original_by_length={str(n):contrast() for n in range(2,7)},interior=contrast()) for seed,arm in s.identities()]
    return dict(diagnostic_complete=True,all_native_replays=True,all_invariant_views=True,all_weights_preserved=True,effects=effects,**s.WORK)


def parent_fixture():
    pins = {e.R_PATH:e.R_BLOB,**{f'p{i}':'a'*40 for i in range(840)}}; inputs = {f'i{i}':'b'*64 for i in range(1596)}
    val = dict(parent_candidate_gate=False,parent_paired_success_count=1,seed_results=[])
    science = NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='c'*64,WORK={'forwards':0})
    r = NS(contract=lambda:{'revision':'fixture'})
    base = NS(spec=lambda:science,PARENT_SUMMARY='d'*64,PARENT_ENVELOPE='f'*64)
    result = dict(schema='fold-c330-diagnostic-v1',experiment_id='parent',stage='stage',commit_sha=e.PARENT_HEAD,status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        execution_revision='C330-R1.2',recovery_manifest_sha256=e.RECOVERY_SHA,recovery_manifest=r.contract(),manifest_sha256='c'*64,
        source_blobs=dict(pins),input_sha256=dict(inputs),validation_summary=val)
    env = dict(schema='fold-c330-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='PASS',
        scientific_summary_sha256=e.PARENT_SUMMARY,execution_revision='C330-R1.2',recovery_manifest_sha256=e.RECOVERY_SHA,
        recovery_manifest=r.contract(),manifest_sha256='c'*64,scientific_work=science.WORK,source_count=841,input_count=1596,
        source_blobs=pins,input_sha256=inputs,parent_summary_sha256=base.PARENT_SUMMARY,parent_envelope_sha256=base.PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=1596,hash_stats={'final_reference_rechecks':1596},regression=e.receipt(e.PARENT_HEAD,5850))
    return result,env,r,base


def synthetic_recovery():
    """Explicit collaborator double; real accepted R1.2 executes in historical tests."""
    import re
    def allowed(name): return type(name) is str and re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',name) is not None
    def validate(row,group,head,index,ph,pid,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==index
                  and row['module']==group['module'] and row['plan_sha256']==ph,'module ABI arguments')
        e.require(row['result']['success_ids']==group['test_ids'] and row['result']['tests']==len(group['test_ids']),'all tests')
        e.require(pid==row['pid'] or pid==row['parent_pid'],'PID topology')
        return 'direct' if pid==row['pid'] else 'redirected-child'
    return NS(allowed_module=allowed,EXCLUDED='excluded',validate_module_evidence=Mock(side_effect=validate))


def synthetic_plan():
    groups=[]
    q,rem=divmod(5850,220)
    for i in range(220):
        name=f'tests_lm.fixture_{i:03d}';groups.append(dict(module=name,test_ids=[name+f'.C.test_{j:03d}' for j in range(q+(i<rem))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C.test_{i:03d}' for i in range(48)]))
    ids=[v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c331-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,
                test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-48])


def write_test(folder,plan,index,ph):
    g=plan['groups'][index];pid=20000+index;parent=10000+index
    e.save(folder/f'module-{index:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=index,
           plan_sha256=ph,module=g['module'],pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{index:03d}.log').write_text('explicit synthetic collaborator log',encoding='utf-8')
    return parent if index%2 else pid


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for a in [('checkout','-qb',e.BRANCH),('config','user.name','C331 fixture'),('config','user.email','c331@example.invalid')]:
        subprocess.run(['git','-C',str(root),*a],check=True,capture_output=True)
    (root/'docs').mkdir();(root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC331 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
    return e.git(root,'rev-parse','HEAD')


class C331Tests(unittest.TestCase):
    def test_01_manifest(self):
        s.validate_seal()
        with patch.object(s,'MODES',('changed',)),self.assertRaises(ValueError):s.validate_seal()
    def test_02_inventory_work_and_no_new_training(self):
        self.assertEqual(len(s.identities()),10);self.assertEqual(s.WORK['model_forward_calls'],10*3*171)
        self.assertEqual(s.WORK['row_presentations'],10*3*16416);self.assertEqual(s.WORK['core_forward_calls'],4*s.WORK['model_forward_calls'])
        self.assertEqual(s.WORK['train_steps'],0);self.assertEqual(s.INPUT_COUNT,1596+449+6);self.assertEqual(s.SOURCE_COUNT,841+6)
    def test_03_actual_own_loader(self):
        loaded=unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE)
        self.assertEqual(loaded.countTestCases(),48);self.assertEqual(s.FULL_TESTS,5850+loaded.countTestCases())
    def test_04_pooled_exact_positions(self):
        model=Toy();x=tokens();z=model.backbone.local_encoder(x)[0]
        mean,first,last=s.pooled(z,x!=256,span(x))
        self.assertTrue(torch.equal(mean,z[:,2:5].mean(1)));self.assertTrue(torch.equal(first,z[:,2]));self.assertTrue(torch.equal(last,z[:,4]))
    def test_05_control_is_native_exact(self):
        m=Toy();x=tokens();t=torch.zeros(2,dtype=torch.int64);expected=m(x,t);before=state_hash(m)
        with s.readout(m,NS(span_mask=span),'native_before') as stats:actual=m(x,t)
        self.assertTrue(torch.equal(actual,expected));self.assertEqual(state_hash(m),before);self.assertEqual(stats['query_calls'],2)
    def test_06_first_mean_formula_second_branch_retained(self):
        m=Toy();x=tokens();z=m.backbone.local_encoder(x)[0];mean,first,last=s.pooled(z,x!=256,span(x))
        expected=m.read.output(.5*(m.read.query(.5*(mean+first))+m.read.query(last)))
        with s.readout(m,NS(span_mask=span),'first_mean'):actual=m(x,torch.zeros(2,dtype=torch.int64))
        self.assertTrue(torch.equal(actual,expected))
    def test_07_intervention_changes_multi_byte_toy(self):
        m=Toy();x=tokens();t=torch.zeros(2,dtype=torch.int64);native=m(x,t)
        with s.readout(m,NS(span_mask=span),'first_mean'):changed=m(x,t)
        self.assertFalse(torch.equal(native,changed))
    def test_08_single_byte_invariant(self):
        m=Toy();x=tokens(True);t=torch.zeros(2,dtype=torch.int64);native=m(x,t)
        with s.readout(m,NS(span_mask=span),'first_mean'):changed=m(x,t)
        self.assertTrue(torch.equal(native,changed))
    def test_09_query_blind_single_position_invariant(self):
        m=Toy();x=tokens(True);x[:,2]=12;t=torch.zeros(2,dtype=torch.int64);native=m(x,t)
        with s.readout(m,NS(span_mask=span),'first_mean'):changed=m(x,t)
        self.assertTrue(torch.equal(native,changed))
    def test_10_byte_endpoint_not_complete_character(self):
        z=torch.arange(64*16,dtype=torch.float64).reshape(1,64,16);valid=torch.ones((1,64),dtype=torch.bool);sp=torch.zeros_like(valid);sp[:,10:13]=True
        _,first,last=s.pooled(z,valid,sp);self.assertTrue(torch.equal(first,z[:,10]));self.assertFalse(torch.equal(first,last))
    def test_11_padding_does_not_enter_pool(self):
        x=tokens();valid=x!=256;sp=span(x);z=torch.randn((2,64,16),dtype=torch.float64);before=s.pooled(z,valid,sp)
        z[~valid]=1e6;after=s.pooled(z,valid,sp)
        self.assertTrue(all(torch.equal(a,b) for a,b in zip(before,after)))
    def test_12_bad_span_rejected(self):
        z=torch.ones((2,64,16),dtype=torch.float64);valid=torch.ones((2,64),dtype=torch.bool)
        for sp in (torch.zeros_like(valid),torch.ones((2,63),dtype=torch.bool),valid.float()):
            with self.subTest(),self.assertRaises(ValueError):s.pooled(z,valid,sp)
    def test_13_invisible_span_rejected(self):
        z=torch.ones((2,64,16),dtype=torch.float64);valid=torch.zeros((2,64),dtype=torch.bool)
        with self.assertRaises(ValueError):s.pooled(z,valid,~valid)
    def test_14_nonfinite_local_rejected(self):
        x=tokens();z=torch.ones((2,64,16),dtype=torch.float64);z[0,2,0]=float('nan')
        with self.assertRaises(ValueError):s.pooled(z,x!=256,span(x))
    def test_15_unknown_mode_rejected(self):
        with self.assertRaises(ValueError):
            with s.readout(Toy(),NS(span_mask=span),'best_of_two'):pass
    def test_16_hook_restoration_after_success(self):
        m=Toy();before=s.hooks(m)
        with s.readout(m,NS(span_mask=span),'first_mean'):m(tokens(),torch.zeros(2,dtype=torch.int64))
        self.assertEqual(s.hooks(m),before)
    def test_17_hook_restoration_after_exception(self):
        m=Toy();before=s.hooks(m)
        with patch.object(m.read.query,'forward',side_effect=RuntimeError('fixture')):
            with self.assertRaises(RuntimeError):
                with s.readout(m,NS(span_mask=span),'first_mean'):m(tokens(),torch.zeros(2,dtype=torch.int64))
        self.assertEqual(s.hooks(m),before)
    def test_18_query_provenance_rejects_non_native_input(self):
        m=Toy();h=m.read.query.register_forward_pre_hook(lambda mod,args:(args[0]+1,))
        try:
            with self.assertRaisesRegex(ValueError,'provenance'):
                with s.readout(m,NS(span_mask=span),'first_mean'):m(tokens(),torch.zeros(2,dtype=torch.int64))
        finally:h.remove()
    def test_19_autograd_not_silently_detached(self):
        m=Toy();x=tokens();t=torch.zeros(2,dtype=torch.int64)
        with s.readout(m,NS(span_mask=span),'first_mean'):loss=m(x,t).sum()
        loss.backward();self.assertIsNotNone(m.backbone.local_encoder.values.grad)
        self.assertGreater(float(m.backbone.local_encoder.values.grad[:,2].abs().sum()),0)
    def test_20_selected_input_gradient_finite_difference(self):
        m=Toy();x=tokens();t=torch.zeros(2,dtype=torch.int64);w=m.backbone.local_encoder.values
        def calc():
            with s.readout(m,NS(span_mask=span),'first_mean'):return m(x,t)[0,3]
        calc().backward();analytic=float(w.grad[0,2,0]);eps=1e-5
        with torch.no_grad():
            w[0,2,0]+=eps;hi=float(calc());w[0,2,0]-=2*eps;lo=float(calc());w[0,2,0]+=eps
        self.assertAlmostEqual(analytic,(hi-lo)/(2*eps),places=8)
    def test_21_strict_logit_and_argmax_control(self):
        a=torch.tensor([[0.,1.]],dtype=torch.float64);self.assertEqual(s.same(a,a),0)
        for b in (torch.tensor([[1.,0.]],dtype=torch.float64),torch.tensor([[0.,float('nan')]],dtype=torch.float64)):
            with self.assertRaises(ValueError):s.same(a,b)
    def test_22_all_query_blind_controls(self):
        a,d=raw_fixture();s.invariant_views(a,copy.deepcopy(a),d)
        b=copy.deepcopy(a);b['interior']['TRAIN']['balanced']['query_blind'][0,1]=1
        with self.assertRaises(ValueError):s.invariant_views(a,b,d)
    def test_23_english_single_byte_control(self):
        a,d=raw_fixture();b=copy.deepcopy(a);b['original']['1']['TRAIN']['repeat']['normal'][0,1]=1
        with self.assertRaises(ValueError):s.invariant_views(a,b,d)
    def test_24_complete_control_inventory(self):
        a,d=raw_fixture();del a['interior']['TRAIN']['balanced']
        with self.assertRaises(ValueError):s.invariant_views(a,copy.deepcopy(a),d)
    def test_25_summary_accepts_benefit_and_harm(self):
        v=summary();s.check_summary(v)
        v['effects'][0]['original_by_length']['6']=contrast(-5);s.check_summary(v)
    def test_26_summary_count_and_gate_binding(self):
        for key in ('model_forward_calls','model_state_loads'):
            v=summary();v[key]-=1
            with self.assertRaises(ValueError):s.check_summary(v)
        v=summary();v['effects'][0]['first_mean']['failures']['original6']['local']=1
        with self.assertRaises(ValueError):s.check_summary(v)
    def test_27_summary_contrast_conservation(self):
        v=summary();v['effects'][0]['interior']['rescued']=1
        with self.assertRaises(ValueError):s.check_summary(v)
    def test_28_actual_parent_evidence_loader(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for n in ('dataset.json','original-prompts.json','interior-prompts.json'):e.save(p/n,{})
            v=dict(schema='fold-c329-evaluations-v1',trajectories=[],records=[dict(seed=seed,arm=arm) for seed,arm in s.identities()])
            torch.save(v,p/'evaluations.pt');self.assertEqual(len(s.load_evidence(p,e.read)[3]),10)
            v['schema']='fold-c328-evaluations-v1';torch.save(v,p/'evaluations.pt')
            with self.assertRaises(ValueError):s.load_evidence(p,e.read)
    def test_29_production_run_probe_order_and_no_training(self):
        class Model(torch.nn.Module):
            def __init__(self):super().__init__();self.w=torch.nn.Parameter(torch.ones(1,dtype=torch.float64))
        prior=[dict(seed=seed,arm=arm,state_sha256='fingerprint') for seed,arm in s.identities()]
        p=NS(load_bundle=lambda path:[Model().state_dict() for _ in prior],state_hash=lambda v:'fingerprint',make_model=lambda *a:Model(),base=lambda:NS(check_dependencies=lambda *a:None))
        calls=[]
        def measure(model,mode,*a):calls.append(mode);return {},{}
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'source',return_value=p),patch.object(s,'load_evidence',return_value=({}, {}, {},prior)),patch.object(s,'measure',side_effect=measure),patch.object(s,'analyze',return_value=([],summary())),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp);s.run_probe(out,out,(None,),ROOT,{},[],e.read)
            self.assertEqual(calls,list(s.MODES)*10);self.assertEqual(set(x.name for x in out.iterdir()),set(s.OUTPUTS))
    def test_30_saved_reconstruction_dispatch_and_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);torch.save({'schema':'fixture'},out/'evaluations.pt')
            for name,value in (('diagnostic-plan.json',s.manifest()),('measurements.json',[]),('validation-summary.json',summary())):e.save(out/name,value)
            with patch.object(s,'load_evidence',return_value=({}, {}, {},[])),patch.object(s,'analyze',return_value=([],summary())):
                s.semantic_recheck(out,out,(),[],e.read);(out/'validation-summary.json').write_text('{}',encoding='utf-8')
                with self.assertRaises(ValueError):s.semantic_recheck(out,out,(),[],e.read)
        # Exercise production analysis, with explicitly synthetic legacy scorers.
        raw,data=raw_fixture();prior=[];records=[];flags=[]
        for seed,arm in s.identities():
            prior.append(dict(seed=seed,arm=arm,state_sha256='f'*64,raw=copy.deepcopy(raw)))
            records.append(dict(seed=seed,arm=arm,state_sha256='f'*64,raw={m:copy.deepcopy(raw) for m in s.MODES},
                receipts={m:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for m in s.MODES}))
            flags.append(dict(seed=seed,arm=arm,original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True))
        base=NS(validate_raw=Mock(),replay_error=Mock(return_value=0.),
            templates=NS(INTERIOR_PROFILES=('u_dominant','balanced','v_dominant')),
            heldout_contrast=Mock(return_value=contrast()))
        cx=(None,None,NS(score_new=lambda *a:{'passed':True}),None,None,
            NS(wide=NS(score_length=lambda *a:{'passed':True}),c=None))
        local=NS(adapted_score=lambda *a:([{'passed':True}]*72,[{'passed':True}]*36,True))
        with patch.object(s,'source',return_value=NS(base=lambda:base)),patch.object(s,'localizer',return_value=local):
            archive=dict(schema='fold-c331-query-probe-v1',records=records)
            metrics,value=s.analyze(archive,prior,data,cx,flags)
            self.assertEqual(len(metrics),10);self.assertTrue(value['diagnostic_complete'])
            self.assertEqual(base.validate_raw.call_count,30);self.assertEqual(base.heldout_contrast.call_count,60)
            archive['records'][0]['state_sha256']='changed'
            with self.assertRaises(ValueError):s.analyze(archive,prior,data,cx,flags)
    def test_31_parent_full_recovery_contract(self):e.parent_contract(*parent_fixture())
    def test_32_parent_small_map_or_wrong_recovery_rejected(self):
        for target,key,value in ((0,'execution_revision','C330-R1.1'),(1,'source_count',838),(1,'input_count',1593),(1,'final_reference_rechecks',1595)):
            args=parent_fixture();args[target][key]=value
            with self.subTest(),self.assertRaises(ValueError):e.parent_contract(*args)
    def test_33_parent_regression_receipt_and_capability_semantics(self):
        args=parent_fixture();args[0]['capability_gate_applicable']=True
        with self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[1]['regression']['skipped']=1
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_34_all443parent_test_files_are_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);items=[]
            for i in range(220):
                (folder/f'module-{i:03d}.json').write_bytes(b'{}');(folder/f'module-{i:03d}.log').write_bytes(b'fixture')
                items.append(dict(index=i,receipt_sha256=e.sha(folder/f'module-{i:03d}.json'),log_sha256=e.sha(folder/f'module-{i:03d}.log')))
            e.save(folder/'regression-plan-r1.json',{});e.save(folder/'regression-result.json',{})
            e.save(folder/'regression-isolation-r1.json',{'modules':items})
            env={'regression_isolation':dict(tests=5850,modules=220,plan_sha256=e.sha(folder/'regression-plan-r1.json'),result_sha256=e.sha(folder/'regression-result.json'),evidence_sha256=e.sha(folder/'regression-isolation-r1.json'))}
            self.assertEqual(len(e.parent_test_files(folder,env,e.sha)),443)
            (folder/'module-219.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,env,e.sha)
    def test_35_new_plan_adds_exact_own_loader(self):
        fixture,digest=synthetic_plan();r=synthetic_recovery();r.flatten=lambda suite:(t for group in suite for t in group)
        r.build_plan=Mock(return_value={'groups':fixture['groups'][:-1]})
        with patch.object(e,'BASE_IDS_SHA',digest):
            plan=e.build_plan(ROOT,HEAD,(r,NS(),None,None,None));self.assertEqual(len(plan['groups']),221)
            self.assertEqual(len(plan['groups'][-1]['test_ids']),48);self.assertTrue(all('.C331Tests.' in x for x in plan['groups'][-1]['test_ids']))
    def test_36_plan_missing_duplicate_or_unknown_module(self):
        p,digest=synthetic_plan();r=synthetic_recovery()
        with patch.object(e,'BASE_IDS_SHA',digest):
            e.validate_plan(p,HEAD,r)
            for kind in ('missing','duplicate','prefix'):
                bad=copy.deepcopy(p)
                if kind=='missing':bad['groups'].pop()
                elif kind=='duplicate':bad['groups'][0]['test_ids'][1]=bad['groups'][0]['test_ids'][0]
                else:bad['groups'][0]['module']='evil.module'
                with self.subTest(),self.assertRaises(ValueError):e.validate_plan(bad,HEAD,r)
    def test_37_collect_and_fresh_verifier_delegate_accepted_pid_ABI(self):
        plan,digest=synthetic_plan();r=synthetic_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:write_test(folder,plan,i,h))
            result=e.verify_tests(folder,HEAD,plan,r);self.assertEqual(result['tests'],5898)
            self.assertEqual(r.validate_module_evidence.call_count,442)
            (folder/'module-220.log').write_bytes(b'tampered')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_38_test_failure_stops_without_aggregate(self):
        plan,digest=synthetic_plan();r=synthetic_recovery();calls=[]
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)
            def run(i,h):calls.append(i);raise ValueError('fixture module failure')
            with self.assertRaises(ValueError):e.collect_tests(folder,HEAD,plan,r,run)
            self.assertEqual(calls,[0]);self.assertFalse((folder/'regression-result.json').exists())
    def test_39_module_CLI_calls_exact_accepted_module_runner(self):
        plan,digest=synthetic_plan();r=synthetic_recovery();g=plan['groups'][0]
        r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'helpers',return_value=(r,None,None,None,None)),patch.object(e,'guard'),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);v=e.read(folder/'module-000.json')
            self.assertEqual(v['schema'],'fold-c330-r1-module-v2');self.assertEqual(v['commit_sha'],HEAD);self.assertEqual(v['parent_pid'],e.os.getppid())
    def test_40_git_guard_and_active_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);head=git_fixture(root);e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError):e.guard(root,head)
        self.assertFalse(e.active('## Formal state\nC330 ACTIVE / NOT YET JUDGED'))
    def test_41_strict_utf8_json_and_exclusive_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x';e.save(p,{'名前':'甲乙'});self.assertEqual(e.read(p),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(p,{})
            for v in ('{"a":1,"a":2}','NaN'):
                p.write_text(v,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(p)
    def test_42_source_lf_crlf_and_tamper(self):
        raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x'
            for v in (raw,raw.replace(b'\n',b'\r\n')):p.write_bytes(v);e.source_bytes(p,oid)
            p.write_bytes(b'bad')
            with self.assertRaises(ValueError):e.source_bytes(p,oid)
    def test_43_actual_process_nonzero_and_no_retry(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'failure.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
    def test_44_stages_do_not_probe_after_failed_regression(self):
        probe=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):e.execute_stages(lambda:None,Mock(side_effect=ValueError('fixture')),probe,Mock(),Mock())
        probe.assert_not_called()
        calls=[]
        def step(n,v):
            def run():calls.append(n);return v
            return run
        with contextlib.redirect_stdout(io.StringIO()):e.execute_stages(step('pre',None),step('tests',{}),step('probe',{'x':1}),step('saved',{'x':1}),step('final',[]))
        self.assertEqual(calls,['pre','tests','probe','saved','final'])
    def test_45_saved_output_byte_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
            e.bound_semantics(out,lambda:1)
            def mutate():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,mutate)
    def test_46_launcher_preflight_and_route(self):
        text=(ROOT/'tools/invoke_c331.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C331',text);self.assertIn('c331_execution.py',(ROOT/'tools/run_c331.ps1').read_text(encoding='utf-8'))
    def test_47_actual_worker_control_path_with_synthetic_dependencies(self):
        for bad in (False,True):self.worker_fixture(bad)
    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);calls=[];value=summary()
            pins={f'p{i}':'a'*40 for i in range(s.SOURCE_COUNT)};inputs={str(root/f'i{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={};stats={'final_reference_rechecks':s.INPUT_COUNT};sha=staticmethod(e.sha)
                def __init__(self,*a,**k):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            runtime=NS(native_runtime=lambda:(NS(__version__='synthetic'),NS(__version__='synthetic')))
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),);p=NS(base=lambda:NS(check_dependencies=lambda *a:None,peak_rss=lambda:1))
            def snap(*a):calls.append('snapshot');return {'validation_summary':{'seed_results':[]}},{},pins,inputs
            def parent(*a):calls.append('parent');return root/'source',cx
            def tests(*a):
                calls.append('tests')
                if bad:raise ValueError('fixture')
                e.save(folder/'regression-result.json',e.receipt(HEAD,s.FULL_TESTS))
            def probe(out,*a):
                calls.append('probe')
                for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
                return value
            def saved(*a):calls.append('saved');return value
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(NS(),NS(),runtime,None,locks)),patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=parent),patch.object(s,'source',return_value=p),patch.object(e,'run_logged',side_effect=tests),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value={}),patch.object(s,'native_preflight',side_effect=lambda *a:calls.append('pre')),patch.object(s,'run_probe',side_effect=probe),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError):e.scientific_worker(root,folder,HEAD)
                    self.assertNotIn('probe',calls)
                else:
                    e.scientific_worker(root,folder,HEAD);self.assertEqual(calls,['snapshot','parent','pre','tests','probe','saved','final','release'])
                    self.assertFalse(e.read(folder/'science/summary.json')['capability_gate_applicable'])
    def test_48_controller_no_retry_and_CLI_mode(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as call,contextlib.redirect_stdout(io.StringIO()) as log:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(call.call_count,1);self.assertIn('run_execution_valid = false',log.getvalue())
        p=subprocess.run([sys.executable,str(ROOT/'tools/c331_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(p.returncode,0);self.assertIn('invalid choice',p.stderr)


if __name__=='__main__':unittest.main()
