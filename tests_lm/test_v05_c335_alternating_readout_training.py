"""C335 software tests; Torch toy training and synthetic ancestors are not FOLD outcomes."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c335_alternating_readout_training as s

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c335_executor_tests',ROOT/'tools/c335_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def fingerprint(value):
    h = hashlib.sha256()
    def walk(v):
        if isinstance(v,torch.Tensor):
            h.update(str((v.dtype,tuple(v.shape))).encode()); h.update(v.detach().contiguous().numpy().tobytes())
        elif isinstance(v,dict):
            h.update(b'dict')
            for k in sorted(v,key=str): walk(k); walk(v[k])
        elif isinstance(v,(tuple,list)):
            h.update(b'sequence')
            for item in v: walk(item)
        else: h.update(repr(v).encode())
    walk(value); return h.hexdigest()


class Tiny(torch.nn.Module):
    def __init__(self, seed=71):
        super().__init__(); torch.manual_seed(seed)
        self.backbone = torch.nn.Module(); self.backbone.core = torch.nn.Linear(2,2,dtype=torch.float64)
        self.read = torch.nn.Module(); self.read.query = torch.nn.Linear(2,2,bias=False,dtype=torch.float64)
        self.read.output = torch.nn.Linear(2,2,bias=False,dtype=torch.float64)
        self.mode = 'native_before'; self.receipt = None
    def forward(self,tokens,tasks):
        x = tokens[:,:2].to(torch.float64)/7
        mean = .5*(x+x.flip(-1)); first = x; last = x.flip(-1)
        a = self.read.query(.5*(mean+first) if self.mode=='first_mean' else mean)
        b = self.read.query(last)
        if self.receipt is not None:
            self.receipt['calls']+=1; self.receipt['query_calls']+=2; self.receipt['rows']+=len(tokens)
            self.receipt['grad_calls']+=int(torch.is_grad_enabled())
        return self.read.output(torch.tanh(self.backbone.core(.5*(a+b))))


@contextlib.contextmanager
def toy_readout(model,wide,mode):
    old,receipt = model.mode,model.receipt
    stats = dict(calls=0,query_calls=0,rows=0,grad_calls=0); model.mode=mode; model.receipt=stats
    try: yield stats
    finally: model.mode=old; model.receipt=receipt


def optimizer(model,policy):
    core = list(model.backbone.core.parameters()); core_ids={id(p) for p in core}
    other = [p for p in model.parameters() if id(p) not in core_ids]
    return torch.optim.AdamW([{'params':other,'lr':.005},{'params':core,'lr':.0005}],betas=(.9,.999),eps=1e-8,weight_decay=0.)


def training_fixture():
    tokens = torch.zeros((192,64),dtype=torch.int64)
    tokens[:,0] = torch.arange(192)%7+1; tokens[:,1] = torch.arange(192)%3+1
    tables={'original':{(4,'repeat'):tokens},'interior4':{(4,'repeat'):tokens.flip(0).clone()}}
    y=(torch.arange(192)%2).to(torch.int64); events=(torch.arange(1200)%192)[:,None]; mask=torch.arange(1200)%2
    def select(t,event,m):
        ids=(torch.arange(48)+int(event[0]))%192
        return t['interior4' if int(m) else 'original'][4,'repeat'][ids],ids
    curriculum=NS(select_tokens=select,validate_schedule=lambda v:None,family_mask=lambda *a:mask,
                  exposure=lambda *a:{'explicit_fixture':True})
    q=NS(readout=toy_readout,same=lambda a,b:e.require(torch.equal(a,b),'native parity'))
    base=NS(check_dependencies=Mock(),peak_rss=lambda:1,validate_raw=Mock())
    p=NS(readouts=lambda:q,source=lambda:NS(curriculum=lambda:curriculum,base=lambda:base),state_hash=fingerprint,
         training_fingerprint=lambda *a:fingerprint(a))
    x=NS(policy=NS(optimizer_for=optimizer,verify_optimizer=lambda *a:None),wide=None,
         c=NS(p267=NS(check_logits=lambda z,n:e.require(z.shape==(n,2) and bool(torch.isfinite(z).all()),'toy logits'))),
         parent=NS(plan_for_order=Mock(return_value=events)),p312=None,pairs=None)
    return NS(tables=tables,y=y,events=events,mask=mask,p=p,q=q,x=x,select=select,base=base)


def reference_fit(model,arm,f):
    # Independent loop: no production policy planner,readout context or optimizer wrapper.
    core=list(model.backbone.core.parameters()); core_ids={id(p) for p in core}
    opt=torch.optim.AdamW([{'params':[p for p in model.parameters() if id(p) not in core_ids],'lr':.005},
                          {'params':core,'lr':.0005}],betas=(.9,.999),eps=1e-8,weight_decay=0.)
    losses=[]
    for k in range(2400):
        index=k%1200; opt.zero_grad(set_to_none=True)
        model.mode='first_mean' if arm=='alternating' and ((index%2) ^ int(k>=1200)) else 'native_before'
        ids=(torch.arange(48)+int(f.events[index,0]))%192
        family='interior4' if int(f.mask[index]) else 'original'
        z=model(f.tables[family][4,'repeat'][ids],torch.zeros(48,dtype=torch.int64))
        loss=F.cross_entropy(z,f.y[ids]);losses.append(float(loss.detach()));loss.backward()
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True);opt.step()
    return losses,copy.deepcopy(model.state_dict())


def contrast(gain=0):
    return dict(answers=288,query_pairs=144,control_correct=280,candidate_correct=280+gain,
        control_both_correct=136,candidate_both_correct=136+gain,rescued=max(gain,0),regressed=max(-gain,0),
        pair_rescued=max(gain,0),pair_regressed=max(-gain,0),answer_gain=gain,query_pair_gain=gain)


def compare(a,b,*args):
    gain=int(float(b[0,0])-float(a[0,0]))
    return dict(original_by_length={str(n):contrast(gain if n==6 else 0) for n in range(2,7)},interior=contrast())


def flags():
    return dict(original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True,
                failures={d:dict(local=0,order=0) for d in ('original2','original3','original4','original5','original6','interior4')})


def flag_check(f):
    e.require(set(f)=={'original_pass','interior_pass','retention_pass','failures'},'flag fields')
    e.require(f['retention_pass'] is all(f['original_pass'].values()),'retention')
    for d,v in f['failures'].items():
        passed=f['interior_pass'] if d=='interior4' else f['original_pass'][d[-1]]
        e.require(passed is (v['local']==v['order']==0),'failure binding')


def contrast_check(v):
    e.require(all(type(z) is int for z in v.values()) and v['answers']==288 and v['query_pairs']==144,'contrast types')
    e.require(v['answer_gain']==v['candidate_correct']-v['control_correct']==v['rescued']-v['regressed'],'answer conservation')
    e.require(v['query_pair_gain']==v['candidate_both_correct']-v['control_both_correct']==v['pair_rescued']-v['pair_regressed'],'pair conservation')


def same_tree(a,b):
    e.require(a.dtype==b.dtype==torch.float64 and a.shape==b.shape and bool(torch.isfinite(a).all()) and bool(torch.isfinite(b).all()),'raw tensors')
    e.require(float((a-b).abs().max())<=1e-9 and torch.equal(a.argmax(-1),b.argmax(-1)),'saved replay')
    return float((a-b).abs().max())


def analysis_fixture(f, traces):
    q=f.q; q.compare=compare; q.summarize_mode=lambda *a:({},flags())
    f.p.contrast_check=contrast_check
    saved_traces=[];records=[];states=[]
    for i,(seed,arm) in enumerate(s.identities()):
        t=copy.deepcopy(traces[arm]); t.update(seed=seed,training_input_sha256='a'*64,
            schedule_sha256=s.digest(f.events.tolist()),mask_sha256=s.digest(f.mask.tolist()),family_exposure_per_cycle={'explicit_fixture':True})
        state=Tiny().state_dict(); state={k:v.clone() for k,v in state.items()}
        for v in state.values():v.add_(i+1)
        t['final_sha256']=fingerprint(state);t['core_final_sha256']='f'*64
        if arm=='alternating':t['initial_sha256']=saved_traces[-1]['initial_sha256'];t['core_initial_sha256']=saved_traces[-1]['core_initial_sha256']
        z=torch.tensor([[int(arm=='alternating'),2.]],dtype=torch.float64)
        records.append(dict(seed=seed,arm=arm,state_sha256=fingerprint(state),evaluation_policy='native_before',
            raw={k:z.clone() for k in ('evaluation','replay')},receipts={k:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for k in ('evaluation','replay')}))
        saved_traces.append(t);states.append(state)
    return saved_traces,records,states,{'TRAIN':[{'language':'en'},{'language':'ja'}]*96},(f.x,)


def synthetic_recovery():
    def flatten(values):
        for v in values:
            if isinstance(v,unittest.TestSuite):yield from flatten(v)
            else:yield v
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==i
                  and row['module']==g['module'] and row['plan_sha256']==ph,'module ABI')
        e.require(row['result']['success_ids']==g['test_ids'] and row['result']['tests']==len(g['test_ids']),'successful tests')
        e.require(launcher in (row['pid'],row['parent_pid']),'PID relationship')
        return 'direct' if launcher==row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',validate_module_evidence=Mock(side_effect=validate),
              allowed_module=lambda x:type(x) is str and (re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',x) is not None or x=='tests_tools.test_c324_locked_hash_r4'))


def synthetic_plan():
    groups=[];n,rem=divmod(6010,224)
    for i in range(224):
        name='tests_tools.test_c324_locked_hash_r4' if i==0 else f'tests_lm.fixture_{i:03d}'
        groups.append(dict(module=name,test_ids=[name+f'.Fixture.test_{j:03d}' for j in range(n+(i<rem))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C335Tests.test_{i:02d}' for i in range(48)]))
    ids=[t for g in groups for t in g['test_ids']]
    return dict(schema='fold-c335-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-48])


def write_module(folder,plan,i,ph):
    g=plan['groups'][i];pid,parent=20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,plan_sha256=ph,module=g['module'],
        pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_text('explicit synthetic receipt',encoding='utf-8')
    return pid if i%2==0 else parent


def write_proofs(folder):
    rows=[]
    for i in range(224):
        (folder/f'module-{i:03d}.json').write_bytes(b'{}');(folder/f'module-{i:03d}.log').write_bytes(b'fixture')
        rows.append(dict(index=i,receipt_sha256=e.sha(folder/f'module-{i:03d}.json'),log_sha256=e.sha(folder/f'module-{i:03d}.log')))
    e.save(folder/'regression-plan.json',{});e.save(folder/'regression-result.json',{})
    e.save(folder/'regression-evidence.json',{'modules':rows})
    return dict(tests=6010,modules=224,plan_sha256=e.sha(folder/'regression-plan.json'),result_sha256=e.sha(folder/'regression-result.json'),evidence_sha256=e.sha(folder/'regression-evidence.json'))


class C335Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_threads=torch.get_num_threads();torch.set_num_threads(2)
        cls.f=training_fixture();cls.traces={};cls.states={};cls.reference={}
        with patch.object(s,'previous',return_value=cls.f.p),contextlib.redirect_stdout(io.StringIO()):
            for arm in s.ARMS:
                cls.traces[arm],cls.states[arm]=s.optimize(Tiny(),arm,cls.f.tables,cls.f.y,cls.f.events,cls.f.mask,cls.f.x)
                cls.reference[arm]=reference_fit(Tiny(),arm,cls.f)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.old_threads)
    def context(self):
        return patch.object(s,'previous',return_value=self.f.p)
    def analysis(self):
        return analysis_fixture(self.f,self.traces)
    def crossing(self):
        return patch.object(s,'crossed',return_value=NS(check_flags=flag_check,same_tree=same_tree))
    def test_01_manifest_seal_and_tamper(self):
        s.validate_seal()
        with patch.object(s,'ORDERS',tuple(reversed(s.ORDERS))),self.assertRaises(ValueError):s.validate_seal()
    def test_02_actual_loader_and_workload(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),48)
        self.assertEqual(s.FULL_TESTS,6010+48);self.assertEqual(s.MODULES,224+1)
        self.assertEqual(s.SOURCE_COUNT,865+6);self.assertEqual(s.INPUT_COUNT,3430+457+6)
        self.assertEqual(s.WORK['model_forward_calls'],10*2400+20*171)
    def test_03_native_plan_has_no_mixed_forward(self):
        self.assertEqual(s.policy_plan('native'),['native_before']*2400)
    def test_04_alternating_exact_per_event_coverage(self):
        modes=s.policy_plan('alternating');self.assertEqual(modes[:4],['native_before','first_mean']*2)
        self.assertEqual(modes[1200:1204],['first_mean','native_before']*2)
        self.assertTrue(all({modes[i],modes[i+1200]}==set(s.READOUTS) for i in range(1200)))
        self.assertEqual([modes.count(m) for m in s.READOUTS],[1200,1200])
    def test_05_bad_modes_and_step_types(self):
        for arm,step in [('best',0),('native',True),('native',-1),('alternating',2400),('native',0.)]:
            with self.subTest(),self.assertRaises(ValueError):s.mode_at(arm,step)
    def test_06_no_old_state_or_extra_long_training(self):
        self.assertFalse(set(s.SEEDS)&set(range(332001,332006)))
        self.assertEqual(s.manifest()['evaluation_policy'],'native_before for both arms and evaluation/replay;no first_mean evaluation or per-example selection')
        self.assertEqual(s.manifest()['exposure_per_row'],[200,200,100,100])
    def test_07_actual_schedule_dispatch(self):
        with self.context():
            self.f.x.parent.plan_for_order.reset_mock()
            for i,seed in enumerate(s.SEEDS):
                s.schedule(seed,[{}]*192,self.f.x)
                self.assertEqual(self.f.x.parent.plan_for_order.call_args.args[:2],(s.ORDERS[i],'two_to_four'))
            with self.assertRaises(ValueError):s.schedule(332001,[{}]*192,self.f.x)
    def test_08_factory_invalid_seed_stops_before_dependencies(self):
        for seed in (True,332001,-1,'335001'):
            with self.assertRaises(ValueError):s.make_model(seed,None)
    def test_09_pair_initialization_and_independent_storage(self):
        with self.context(),patch.object(s,'make_model',side_effect=lambda *a:Tiny()):
            pair=s.make_pair(s.SEEDS[0],None);self.assertEqual(fingerprint(pair['native'].state_dict()),fingerprint(pair['alternating'].state_dict()))
            self.assertTrue(all(a.data_ptr()!=b.data_ptr() for a,b in zip(pair['native'].parameters(),pair['alternating'].parameters())))
    def test_10_pair_alias_is_rejected(self):
        model=Tiny()
        with self.context(),patch.object(s,'make_model',return_value=model),self.assertRaisesRegex(ValueError,'storage'):s.make_pair(s.SEEDS[0],None)
    def test_11_full2400_native_updates_equal_independent_reference(self):
        self.assertEqual(self.traces['native']['ce_history'],self.reference['native'][0])
        self.assertEqual(fingerprint(self.states['native']),fingerprint(self.reference['native'][1]))
    def test_12_full2400_alternating_updates_equal_independent_reference(self):
        self.assertEqual(self.traces['alternating']['ce_history'],self.reference['alternating'][0])
        self.assertEqual(fingerprint(self.states['alternating']),fingerprint(self.reference['alternating'][1]))
    def test_13_training_policy_changes_actual_updates(self):
        self.assertNotEqual(fingerprint(self.states['native']),fingerprint(self.states['alternating']))
        self.assertEqual(self.traces['native']['initial_sha256'],self.traces['alternating']['initial_sha256'])
    def test_14_loss_history_and_gradient_inventory(self):
        for t in self.traces.values():
            self.assertEqual(len(t['ce_history']),2400);self.assertTrue(all(v>=0 for v in t['ce_history']))
            self.assertGreater(sum(t['gradient_union'].values()),0);self.assertEqual(len(t['gradient_parameter_counts']),2400)
    def test_15_actual_policy_receipts_and_order(self):
        for arm,t in self.traces.items():
            self.assertEqual(t['policy_modes'],s.policy_plan(arm));self.assertEqual(t['policy_receipts'],s.policy_receipts(arm))
            self.assertEqual(t['event_indices'],list(range(1200))*2)
    def test_16_optimizer_and_weight_continuation(self):
        for t in self.traces.values():
            self.assertEqual(t['boundary'],t['continuation']);self.assertEqual(t['optimizer_creations'],1)
            self.assertEqual(t['optimizer_group_lrs'],[[.005,.0005]]*2400)
    def test_17_deep_saved_state_and_hook_cleanup(self):
        with self.context(),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),contextlib.redirect_stdout(io.StringIO()):
            m=Tiny();t,state=s.optimize(m,'alternating',self.f.tables,self.f.y,self.f.events[:2],self.f.mask[:2],self.f.x)
            self.assertEqual(m.mode,'native_before');self.assertIsNone(m.receipt)
            for k,v in m.state_dict().items():self.assertNotEqual(v.data_ptr(),state[k].data_ptr())
    def test_18_exception_restores_readout_before_any_update(self):
        m=Tiny();initial=fingerprint(m.state_dict())
        with self.context(),patch.object(m.read.output,'forward',side_effect=RuntimeError('fixture')):
            with self.assertRaises(RuntimeError):s.optimize(m,'alternating',self.f.tables,self.f.y,self.f.events,self.f.mask,self.f.x)
        self.assertEqual(m.mode,'native_before');self.assertIsNone(m.receipt);self.assertEqual(fingerprint(m.state_dict()),initial)
    def test_19_train_one_real_order_and_measured_accounting(self):
        @contextlib.contextmanager
        def counted(*a):yield [2400,115200],[9600]
        self.f.x.c.core=None
        with self.context(),patch.object(self.f.x.c.p267,'counted',counted,create=True),patch.object(s,'optimize',return_value=(copy.deepcopy(self.traces['native']),self.states['native'])),contextlib.redirect_stdout(io.StringIO()):
            t,_=s.train_one(s.SEEDS[0],'native',Tiny(),self.f.tables,self.f.y,[{}]*192,(self.f.x,),ROOT,{})
            self.assertEqual(t['schedule_sha256'],s.digest(self.f.events.tolist()))
    def test_20_native_preflight_backward_with_real_toy(self):
        data={'TRAIN':[{'language':'en'},{'language':'ja'}]*96}
        with self.context(),patch.object(self.f.p,'load_data',return_value=(data,{},{}),create=True),patch.object(self.f.p,'prepared',return_value=(self.f.tables,self.f.y),create=True),patch.object(s,'make_model',side_effect=lambda *a:Tiny()),contextlib.redirect_stdout(io.StringIO()) as log:
            s.native_preflight(ROOT,(self.f.x,),ROOT,{},e.read)
            self.assertIn('forwards=6',log.getvalue())
    def test_21_trace_actual_full_budget(self):
        traces,_,_,data,cx=self.analysis()
        with self.context():
            for t in traces:s.check_trace(t,data['TRAIN'],cx[-1])
    def test_22_trace_policy_and_boolean_receipts_rejected(self):
        traces,_,_,data,cx=self.analysis()
        for kind in ('mode','receipt','step'):
            t=copy.deepcopy(traces[1])
            if kind=='mode':t['policy_modes'][1200]='native_before'
            elif kind=='receipt':t['policy_receipts']['native_before']['calls']=True
            else:t['steps']=True
            with self.context(),self.assertRaises(ValueError):s.check_trace(t,data['TRAIN'],cx[-1])
    def test_23_trace_boundary_exposure_and_gradient_tamper(self):
        traces,_,_,data,cx=self.analysis()
        for key,value in [('continuation',{}),('schedule_sha256','changed'),('gradient_parameter_counts',[0]*2400)]:
            t=copy.deepcopy(traces[0]);t[key]=value
            with self.context(),self.assertRaises(ValueError):s.check_trace(t,data['TRAIN'],cx[-1])
    def test_24_bundle_real_safe_Torch_loader(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'state.pt';v=dict(schema='fold-c335-trained-models-v1',identities=[list(z) for z in s.identities()],states=[{}]*10)
            torch.save(v,path);self.assertEqual(len(s.load_states(path)),10)
            v['schema']='fold-c332-trained-models-v1';torch.save(v,path)
            with self.assertRaises(ValueError):s.load_states(path)
    def valid_pairs(self):
        return [dict(seed=z,candidate_full_pass=True,six_answer_gain=1,six_pair_gain=1,short_answer_gain=0,short_pair_gain=0,interior_answer_gain=0,interior_pair_gain=0) for z in s.SEEDS]
    def test_25_fixed_gate_and_individual_ties(self):
        v=self.valid_pairs();self.assertTrue(s.fixed_gate(v)[0]);v[0]['six_answer_gain']=v[0]['six_pair_gain']=0;self.assertTrue(s.fixed_gate(v)[0])
    def test_26_all_candidate_full_gates_required(self):
        v=self.valid_pairs();v[3]['candidate_full_pass']=False;self.assertFalse(s.fixed_gate(v)[0])
    def test_27_each_pair_nondegradation(self):
        for key in ('six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain'):
            v=self.valid_pairs();v[3][key]=-1;self.assertFalse(s.fixed_gate(v)[0])
    def test_28_both_aggregate_improvements_strict(self):
        for key in ('six_answer_gain','six_pair_gain'):
            v=self.valid_pairs()
            for row in v:row[key]=0
            self.assertFalse(s.fixed_gate(v)[0])
    def test_29_gate_missing_states_and_boolean_gains(self):
        v=self.valid_pairs()
        with self.assertRaises(ValueError):s.fixed_gate(v[:-1])
        v[0]['six_answer_gain']=True
        with self.assertRaises(ValueError):s.fixed_gate(v)
    def test_30_complete_production_analysis_synthetic_scoring(self):
        args=self.analysis()
        with self.context(),self.crossing():
            metrics,value=s.analyze(*args);self.assertEqual(len(metrics),10);self.assertTrue(value['candidate_gate'])
            self.assertEqual(value['evaluation_policy'],'native_before')
    def test_31_analysis_rejects_wrong_policy_weights_replay(self):
        for kind in ('policy','state','replay'):
            args=self.analysis();r=args[1][1]
            if kind=='policy':r['evaluation_policy']='first_mean'
            elif kind=='state':r['state_sha256']='f'*64
            else:r['raw']['replay'][0,0]+=1.
            with self.context(),self.crossing(),self.assertRaises(ValueError):s.analyze(*args)
    def test_32_summary_rejects_false_pass_and_gain_drift(self):
        with self.context(),self.crossing():
            _,v=s.analyze(*self.analysis())
            for key,value in [('candidate_gate',False),('model_forward_calls',1)]:
                bad=copy.deepcopy(v);bad[key]=value
                with self.assertRaises(ValueError):s.check_summary(bad)
            v['paired_comparisons'][0]['six_answer_gain']=2
            with self.assertRaises(ValueError):s.check_summary(v)
    def scientific_fixture(self):
        traces,records,states,data,cx=self.analysis();calls=[];i_train=0;i_eval=0
        def train(seed,arm,*a):
            nonlocal i_train
            calls.append('train');j=i_train;i_train+=1;return copy.deepcopy(traces[j]),copy.deepcopy(states[j])
        def measure(model,mode,*a):
            nonlocal i_eval
            e.require(len([x for x in calls if x=='train'])==10,'evaluation before all training')
            e.require(mode=='native_before','evaluation must stay native');calls.append('eval');j=i_eval//2;i_eval+=1
            return records[j]['raw']['evaluation'].clone(),dict(calls=171,query_calls=342,rows=16416,grad_calls=0)
        return NS(traces=traces,records=records,states=states,data=data,cx=cx,calls=calls,train=train,measure=measure)
    def run_scientific_fixture(self,out,f):
        with self.context(),self.crossing(),patch.object(self.f.p,'load_data',return_value=(f.data,{},{}),create=True),patch.object(self.f.p,'prepared',return_value=(self.f.tables,self.f.y),create=True),patch.object(s,'make_model',side_effect=lambda *a:Tiny()),patch.object(s,'train_one',side_effect=f.train),patch.object(self.f.q,'measure',side_effect=f.measure,create=True),contextlib.redirect_stdout(io.StringIO()):
            value=s.run_training(out,ROOT,f.cx,ROOT,{},e.read)
            restored=s.semantic_recheck(out,ROOT,f.cx,e.read)
        return value,restored
    def test_33_production_writer_trains_all_then_native_eval_only(self):
        f=self.scientific_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            value,restored=self.run_scientific_fixture(Path(tmp),f)
            self.assertEqual(f.calls,['train']*10+['eval']*20);self.assertEqual(s.blob(value),s.blob(restored))
            self.assertEqual(set(p.name for p in Path(tmp).iterdir()),set(s.OUTPUTS))
    def test_34_saved_reconstruction_rejects_resealed_json(self):
        f=self.scientific_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);self.run_scientific_fixture(out,f);(out/'validation-summary.json').write_bytes(b'{}')
            with self.context(),self.crossing(),patch.object(self.f.p,'load_data',return_value=(f.data,{},{}),create=True),self.assertRaisesRegex(ValueError,'reconstruction'):
                s.semantic_recheck(out,ROOT,f.cx,e.read)
    def test_35_actual_own_loader_appended_to_base(self):
        plan,digest=synthetic_plan();r=synthetic_recovery();parent=NS(build_plan=Mock(return_value={'groups':plan['groups'][:-1]}))
        with patch.object(e,'BASE_IDS_SHA',digest):
            v=e.build_plan(ROOT,HEAD,(parent,{'recovery':r}));self.assertEqual(len(v['groups']),225)
            self.assertEqual(len(v['groups'][-1]['test_ids']),48)
    def test_36_missing_duplicate_reordered_namespace_rejected(self):
        plan,digest=synthetic_plan();r=synthetic_recovery()
        with patch.object(e,'BASE_IDS_SHA',digest):
            e.validate_plan(plan,HEAD,r)
            for kind in ('drop','duplicate','reorder','namespace'):
                v=copy.deepcopy(plan)
                if kind=='drop':v['groups'].pop()
                elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
                elif kind=='reorder':v['groups'][0]['test_ids'].reverse()
                else:v['groups'][0]['module']='invalid.module'
                with self.assertRaises(ValueError):e.validate_plan(v,HEAD,r)
    def test_37_parent_contract_exact_diagnostic_scope(self):
        ps=NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='m',WORK={'x':0})
        p=NS(spec=lambda:ps,PARENT_SUMMARY='s',PARENT_ENVELOPE='v')
        pins={e.P_PATH:e.P_BLOB,**{f'p{i}':'a' for i in range(864)}};inputs={f'i{i}':'b' for i in range(3430)}
        r=dict(schema='fold-c334-diagnostic-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='PASS',diagnostic_execution_valid=True,
            capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,manifest_sha256='m',source_blobs=pins,input_sha256=inputs,
            validation_summary={'parent_validation_summary':{'candidate_gate':False}})
        v=dict(schema='fold-c334-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='PASS',manifest_sha256='m',scientific_work={'x':0},
            scientific_summary_sha256=e.PARENT_SUMMARY,source_count=865,input_count=3430,source_blobs=pins,input_sha256=inputs,parent_summary_sha256='s',parent_envelope_sha256='v',
            immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
            final_reference_rechecks=3430,hash_stats={'final_reference_rechecks':3430},regression=e.receipt(e.PARENT_HEAD,6010))
        e.parent_contract(r,v,p)
        for key,value in [('source_count',859),('input_count',2969),('scientific_status','FAIL'),('final_reference_rechecks',3429)]:
            bad=copy.deepcopy(v);bad[key]=value
            with self.assertRaises(ValueError):e.parent_contract(r,bad,p)
    def test_38_all457parent_files_and_full_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pins,inputs,tree={},{},{}
            for i in range(865):
                name=f'ancestor/{i}.py';p=root/name;p.parent.mkdir(parents=True,exist_ok=True);v=f'# fixture{i}\n'.encode();p.write_bytes(v)
                pins[name]=hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest();tree[name]=pins[name];inputs[e.canonical(p)]=e.sha(p)
            inputs.update({f'synthetic{i}':'a'*64 for i in range(3430-865)})
            for name in s.OWN:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);v=name.encode();p.write_bytes(v);tree[name]=hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
            folder=root/e.PARENT_FOLDER;out=folder/'science';out.mkdir(parents=True)
            parent_outputs=('diagnostic-plan.json','evaluations.pt','measurements.json','validation-summary.json')
            for name in parent_outputs:(out/name).write_bytes(b'fixture')
            proof=write_proofs(folder);e.save(out/'summary.json',{'artifacts':[]})
            e.save(folder/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation=proof))
            p=NS(spec=lambda:NS(OUTPUTS=parent_outputs),snapshot=Mock(return_value=({}, {},pins,inputs)),build_plan=Mock(return_value={}),verify_tests=Mock(return_value=proof))
            legacy=NS(tree_blobs=lambda root:tree,descriptors=lambda out,items,names,h:{e.canonical(out/n):h(out/n) for n in names})
            h=dict(recovery=object(),legacy=legacy)
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(folder/'execution-envelope.json')),patch.object(e,'parent_contract'):
                _,_,a,b=e.snapshot(root,(p,h),e.sha);self.assertEqual((len(a),len(b)),(871,3893))
                self.assertEqual(p.verify_tests.call_args.args,(folder,e.PARENT_HEAD,{},h['recovery']))
                (folder/'module-223.log').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'proof bytes'):e.snapshot(root,(p,h),e.sha)
    def test_39_immediate_C334_loader_signature_and_no_older_semantics(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);state=root/'c332/science';data=root/'c329/science';state.mkdir(parents=True);data.mkdir(parents=True)
            for p,names in ((state,('evaluations.pt','trained-models.pt')),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                for n in names:(p/n).write_bytes(b'{}')
            inputs={e.canonical(p):e.sha(p) for folder in (state,data) for p in folder.iterdir()}
            saved={'parent_validation_summary':{'candidate_gate':False}};q=NS(semantic_recheck=Mock(return_value=saved));p=NS(spec=lambda:q)
            h=dict(parent=NS(PARENT_FOLDER='c332'),c330=NS(PARENT_FOLDER='c329'))
            x=NS(c=NS(p267=NS(validate_data=lambda v:None)),guarded=NS(no_neural=contextlib.nullcontext))
            cx=(None,None,NS(new_prompts=lambda d:{},check_prompts=lambda *a:None),None,None,x)
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            previous=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {},{}))
            with patch.object(s,'previous',return_value=previous):
                self.assertEqual(e.parent_semantics(root,(p,h),{'validation_summary':saved},inputs),(data,cx))
                q.semantic_recheck.assert_called_once_with(root/e.PARENT_FOLDER/'science',state,data,cx,saved['parent_validation_summary'],e.read)
                del inputs[e.canonical(state/'trained-models.pt')]
                with self.assertRaises(ValueError):e.parent_semantics(root,(p,h),{'validation_summary':saved},inputs)
    def test_40_collector_and_fresh_verifier_use_same_PID_ABI(self):
        plan,digest=synthetic_plan();r=synthetic_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:write_module(folder,plan,i,h))
            self.assertEqual(e.verify_tests(folder,HEAD,plan,r)['tests'],6058);self.assertEqual(r.validate_module_evidence.call_count,450)
            (folder/'module-224.log').write_bytes(b'tampered')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_41_regression_failure_writes_no_success_aggregate(self):
        plan,digest=synthetic_plan();r=synthetic_recovery();call=Mock(side_effect=ValueError('fixture'))
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)
            with self.assertRaises(ValueError):e.collect_tests(folder,HEAD,plan,r,call)
            self.assertEqual(call.call_count,1);self.assertFalse((folder/'regression-result.json').exists())
    def test_42_module_CLI_uses_current_guard_and_generic_receipt(self):
        plan,digest=synthetic_plan();r=synthetic_recovery();g=plan['groups'][0];r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'helpers',return_value=(None,{'recovery':r})),patch.object(e,'guard'),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
    def test_43_real_Git_guard_and_active_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C335 fixture'),('config','user.email','c335@example.invalid')]:subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();p=root/'docs/experiment-ledger-and-handoff.md';p.write_text('## Formal state\nC335 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            head=e.git(root,'rev-parse','HEAD');e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            p.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.guard(root,head)
        self.assertFalse(e.active('## Formal state\nC334 ACTIVE / NOT YET JUDGED'))
    def test_44_strict_JSON_UTF8_exclusive_source_CRLF(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x';e.save(p,{'名前':'甲乙'});self.assertEqual(e.read(p),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(p,{})
            for text in ('{"a":1,"a":2}','NaN','Infinity'):
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(p)
            raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
            for v in (raw,raw.replace(b'\n',b'\r\n')):p.write_bytes(v);e.source_bytes(p,oid)
            p.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.source_bytes(p,oid)
    def test_45_actual_subprocess_failure_and_CLI_rejection(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'error.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
        p=subprocess.run([sys.executable,str(ROOT/'tools/c335_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','invalid'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(p.returncode,0);self.assertIn('invalid choice',p.stderr)
    def test_46_worker_accepts_valid_negative_and_fresh_verifies(self):self.worker_fixture(False)
    def test_47_worker_failure_stops_before_training(self):self.worker_fixture(True)
    def worker_fixture(self,bad):
        with self.context(),self.crossing():_,value=s.analyze(*self.analysis())
        # Keep an integral negative outcome,not a weakened scientific gate.
        value['paired_comparisons'][0]['six_answer_gain']=0;value['paired_comparisons'][0]['six_pair_gain']=0
        value['paired_comparisons'][0]['original_by_length']['6']=contrast()
        for pair in value['paired_comparisons'][1:]:
            pair['six_answer_gain']=pair['six_pair_gain']=0;pair['original_by_length']['6']=contrast()
        value['candidate_gate']=False
        with tempfile.TemporaryDirectory() as tmp,self.context(),self.crossing(),contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);calls=[]
            pins={f'p{i}':'a'*40 for i in range(871)};inputs={f'i{i}':'b'*64 for i in range(3893)}
            class Cache:
                entries={};stats={'final_reference_rechecks':3893};sha=staticmethod(e.sha)
                def __init__(self,*a,**k):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            runtime=NS(native_runtime=lambda:(NS(__version__='synthetic'),NS(__version__='synthetic')))
            legacy=NS(descriptors=lambda out,items,names,h:e.require(items==e.artifacts(out),'artifact binding'))
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            def snap(*a):calls.append('snapshot');return {},{},pins,inputs
            def parent(*a):calls.append('parent');return root,cx
            def regression(*a):
                calls.append('tests')
                if bad:raise ValueError('fixture regression failure')
                e.save(folder/'regression-result.json',e.receipt(HEAD,6058))
            def training(out,*a):
                calls.append('train')
                for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
                return value
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(None,dict(runtime=runtime,locks=locks,recovery=None,legacy=legacy))),patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=parent),patch.object(e,'run_logged',side_effect=regression),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value={'tests':6058,'modules':225}),patch.object(s,'native_preflight',side_effect=lambda *a:calls.append('pre')),patch.object(s,'run_training',side_effect=training),patch.object(s,'semantic_recheck',return_value=value):
                if bad:
                    with self.assertRaises(ValueError):e.scientific_worker(root,folder,HEAD)
                    self.assertNotIn('train',calls);self.assertFalse((folder/'science/summary.json').exists())
                else:
                    e.scientific_worker(root,folder,HEAD);self.assertEqual(calls,['snapshot','parent','pre','tests','train','final','release'])
                    e.verify_outputs(root,folder,HEAD);v=e.read(folder/'science/summary.json');self.assertEqual(v['status'],'FAIL')
                    v['status']='PASS';(folder/'science/summary.json').write_bytes(s.blob(v))
                    with self.assertRaisesRegex(ValueError,'outcome flags'):e.verify_outputs(root,folder,HEAD)
    def test_48_controller_no_retry_and_launcher_preflight(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as call,contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(call.call_count,1);self.assertIn('run_execution_valid = false',output.getvalue())
        text=(ROOT/'tools/invoke_c335.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C335',text);self.assertIn('c335_execution.py',(ROOT/'tools/run_c335.ps1').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
