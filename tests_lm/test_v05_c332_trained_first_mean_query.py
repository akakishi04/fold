"""C332 software tests; toy models and synthetic historical evidence are labeled."""
from __future__ import annotations
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import itertools
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c332_trained_first_mean_query as s
from fold_lm.v05_benchmarks import model_c331_frozen_first_mean_query as q

ROOT=Path(__file__).resolve().parents[1]
loader=importlib.util.spec_from_file_location('_c332_executor_tests',ROOT/'tools/c332_execution.py')
e=importlib.util.module_from_spec(loader);loader.loader.exec_module(e)
HEAD='a'*40


def fingerprint(v):
    """Typed tensor/state fixture hash, not a claim to revalidate accepted archives."""
    h=hashlib.sha256()
    def visit(x):
        if isinstance(x,torch.Tensor):
            t=x.detach().cpu().contiguous();h.update(str((str(t.dtype),tuple(t.shape))).encode());h.update(t.numpy().tobytes())
        elif isinstance(x,dict):
            for k in sorted(x,key=lambda k:(type(k).__name__,str(k))):h.update(repr(k).encode());visit(x[k])
        elif isinstance(x,(list,tuple)):
            h.update(type(x).__name__.encode())
            for z in x:visit(z)
        else:h.update(repr(x).encode())
    visit(v);return h.hexdigest()


def span(tokens):return (tokens>=10)&(tokens<=12)


class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__();self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
        self.position=torch.nn.Parameter(torch.randn(64,16,dtype=torch.float64)*.02)
    def forward(self,x):return (self.embed(x)+self.position[None],)


class Toy(torch.nn.Module):
    def __init__(self,seed=123):
        super().__init__();torch.manual_seed(seed);self.backbone=torch.nn.Module()
        self.backbone.local_encoder=Encoder();self.backbone.core=torch.nn.Linear(16,16,bias=False,dtype=torch.float64)
        self.read=torch.nn.Module();self.read.query=torch.nn.Linear(16,16,bias=False,dtype=torch.float64)
        self.read.output=torch.nn.Linear(16,256,bias=False,dtype=torch.float64)
    def forward(self,tokens,tasks):
        local=self.backbone.local_encoder(tokens)[0]*(tokens!=256)[:,:,None]
        mask=span(tokens);pos=torch.arange(64).expand_as(tokens)
        mean=(local*mask[:,:,None]).sum(1)/mask.sum(1,keepdim=True)
        last=local[torch.arange(len(tokens)),torch.where(mask,pos,-1).max(1).values]
        value=.5*(self.read.query(mean)+self.read.query(last))
        return self.read.output(self.backbone.core(value))


def optimizer(model):
    core=list(model.backbone.core.parameters());ids={id(v) for v in core}
    return torch.optim.AdamW([dict(params=[p for p in model.parameters() if id(p) not in ids],lr=.005),
                             dict(params=core,lr=.0005)],lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)


def numeric_fixture():
    model=Toy();tokens=torch.full((2,64),256,dtype=torch.int64);tokens[0,2:5]=torch.tensor([10,11,12]);tokens[1,2:5]=torch.tensor([12,11,10])
    y=torch.tensor([48,49],dtype=torch.int64);visits=[]
    def select(tables,event,mask):visits.append(int(event));return tokens,torch.arange(2)
    def check(z,n):s.require(z.shape==(n,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),'toy finite logits')
    def verify(opt,m,mode):s.require(type(opt) is torch.optim.AdamW and mode=='core_slow','toy optimizer')
    policy=NS(optimizer_for=Mock(side_effect=lambda m,a:optimizer(m)),verify_optimizer=verify)
    x=NS(policy=policy,wide=NS(span_mask=span),c=NS(p267=NS(check_logits=check)))
    curriculum=NS(select_tokens=select)
    source=NS(state_hash=fingerprint,curriculum=lambda:curriculum)
    return model,tokens,y,visits,x,source


def run_toy(arm='native',cycle=2):
    m,t,y,visits,x,p=numeric_fixture()
    with patch.object(s,'source',return_value=p),patch.object(s,'CYCLE',cycle),patch.object(s,'STEPS',cycle*2),contextlib.redirect_stdout(io.StringIO()):
        trace,state=s.optimize(m,arm,{},y,list(range(cycle)),[None]*cycle,x)
    return m,t,y,visits,x,p,trace,state


def contrast(gain=0):
    return dict(answers=288,query_pairs=144,control_correct=200,candidate_correct=200+gain,
        control_both_correct=80,candidate_both_correct=80+gain,rescued=max(gain,0),regressed=max(-gain,0),
        pair_rescued=max(gain,0),pair_regressed=max(-gain,0),answer_gain=gain,query_pair_gain=gain)


def summary(success=True):
    flags=[];pairs=[]
    for seed in s.SEEDS:
        for arm in s.ARMS:
            flags.append(dict(seed=seed,arm=arm,original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True,failures={}))
        old={str(n):contrast(1 if success and n==6 else 0) for n in range(2,7)}
        pairs.append(dict(seed=seed,control_full_pass=True,candidate_full_pass=True,
            six_answer_gain=old['6']['answer_gain'],six_pair_gain=old['6']['query_pair_gain'],
            short_answer_gain=0,short_pair_gain=0,interior_answer_gain=0,interior_pair_gain=0,
            original_by_length=old,interior=contrast()))
    return dict(candidate_gate=success,eligible_seed_count=5,paired_conditions_valid=True,all_replays=True,
                seed_results=flags,paired_comparisons=pairs,**s.WORK)


def parent_fixture():
    pins={e.P_PATH:e.P_BLOB,**{f'p{i}':'b'*40 for i in range(846)}};inputs={f'i{i}':'c'*64 for i in range(2051)}
    bs=NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='d'*64,WORK={'training':0})
    p=NS(spec=lambda:bs,PARENT_SUMMARY='e'*64,PARENT_ENVELOPE='f'*64)
    r=dict(schema='fold-c331-diagnostic-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        manifest_sha256=bs.MANIFEST_SHA,source_blobs=dict(pins),input_sha256=dict(inputs),validation_summary={})
    v=dict(schema='fold-c331-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='PASS',scientific_summary_sha256=e.PARENT_SUMMARY,
        manifest_sha256=bs.MANIFEST_SHA,scientific_work=bs.WORK,source_count=847,input_count=2051,source_blobs=pins,input_sha256=inputs,
        parent_summary_sha256=p.PARENT_SUMMARY,parent_envelope_sha256=p.PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,
        parent_regression_reconstructed=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=2051,hash_stats={'final_reference_rechecks':2051},regression=e.receipt(e.PARENT_HEAD,5898))
    return r,v,p


def fake_recovery():
    def allowed(name):return type(name) is str and (re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',name) is not None or name=='tests_tools.test_c324_locked_hash_r4')
    def validate(row,g,head,i,ph,pid,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==i
                  and row['plan_sha256']==ph and row['module']==g['module'],'module ABI binding')
        e.require(row['result']['success_ids']==g['test_ids'] and row['result']['tests']==len(g['test_ids']),'complete test IDs')
        e.require(pid in (row['pid'],row['parent_pid']),'PID relation')
        return 'direct' if pid==row['pid'] else 'redirected-child'
    def flatten(value):
        for x in value:
            if isinstance(x,unittest.TestSuite):yield from flatten(x)
            else:yield x
    return NS(allowed_module=allowed,EXCLUDED='excluded',validate_module_evidence=Mock(side_effect=validate),flatten=flatten)


def fake_plan():
    groups=[];n,remainder=divmod(5898,221)
    for i in range(221):
        name='tests_tools.test_c324_locked_hash_r4' if i==0 else f'tests_lm.fixture_{i:03d}'
        groups.append(dict(module=name,test_ids=[name+f'.Fixture.test_{j:03d}' for j in range(n+(i<remainder))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C332Tests.test_{i:02d}' for i in range(s.OWN_TESTS)]))
    ids=[x for g in groups for x in g['test_ids']]
    return dict(schema='fold-c332-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-48])


def fake_module(folder,plan,i,ph):
    g=plan['groups'][i];pid=20000+i;parent=10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,plan_sha256=ph,module=g['module'],
           pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_text('synthetic module evidence collaborator',encoding='utf-8')
    return pid if i%2==0 else parent


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C332 fixture'),('config','user.email','c332@example.invalid')]:
        subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    (root/'docs').mkdir();(root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC332 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
    return e.git(root,'rev-parse','HEAD')


class C332Tests(unittest.TestCase):
    def test_01_manifest_seal(self):
        s.validate_seal()
        with patch.object(s,'STEPS',2401),self.assertRaises(ValueError):s.validate_seal()
    def test_02_fixed_work_and_actual_own_loader(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),48)
        self.assertEqual(s.FULL_TESTS,5898+48);self.assertEqual(s.WORK['train_steps'],10*2400)
        self.assertEqual(s.WORK['model_forward_calls'],10*2400+20*171)
        self.assertEqual(s.WORK['row_presentations'],10*2400*48+20*16416)
        self.assertEqual(s.SOURCE_COUNT,847+6);self.assertEqual(s.INPUT_COUNT,2051+451+6)
        self.assertEqual(s.manifest()['raw_logit_payload_bytes'],10*2*16416*256*8)
    def test_03_exact_policy_selection(self):
        self.assertEqual(s.policy_mode('native'),'native_before');self.assertEqual(s.policy_mode('first_mean'),'first_mean')
        for v in ('native_after','best',None,True):
            with self.assertRaises(ValueError):s.policy_mode(v)
    def test_04_pair_initial_state_and_independent_storage(self):
        with patch.object(s,'make_model',side_effect=lambda seed,x:Toy(seed)),patch.object(s,'state_hash',side_effect=fingerprint):
            pair=s.make_pair(s.SEEDS[0],None)
            self.assertEqual(fingerprint(pair['native'].state_dict()),fingerprint(pair['first_mean'].state_dict()))
            self.assertNotEqual(next(pair['native'].parameters()).data_ptr(),next(pair['first_mean'].parameters()).data_ptr())
    def test_05_shared_pair_storage_rejected(self):
        model=Toy()
        with patch.object(s,'make_model',return_value=model),patch.object(s,'state_hash',side_effect=fingerprint),self.assertRaisesRegex(ValueError,'storage'):
            s.make_pair(s.SEEDS[0],None)
    def test_06_changed_initial_state_rejected(self):
        with patch.object(s,'make_model',side_effect=[Toy(1),Toy(2)]),patch.object(s,'state_hash',side_effect=fingerprint),self.assertRaisesRegex(ValueError,'initial'):
            s.make_pair(s.SEEDS[0],None)
    def test_07_native_updates_match_independent_reference(self):
        m,t,y,visits,x,p,trace,state=run_toy('native',2);ref=Toy();opt=optimizer(ref)
        for _ in range(4):
            opt.zero_grad(set_to_none=True);F.cross_entropy(ref(t,torch.zeros(2,dtype=torch.int64)),y).backward()
            torch.nn.utils.clip_grad_norm_(list(ref.parameters()),1.,error_if_nonfinite=True);opt.step()
        self.assertEqual(fingerprint(ref.state_dict()),fingerprint(state));self.assertEqual(visits,[0,1,0,1])
        self.assertEqual(x.policy.optimizer_for.call_count,1)
    def test_08_first_mean_updates_match_explicit_reference(self):
        m,t,y,_,_,_,trace,state=run_toy('first_mean',2);ref=Toy();opt=optimizer(ref)
        for _ in range(4):
            opt.zero_grad(set_to_none=True)
            local=ref.backbone.local_encoder(t)[0]*(t!=256)[:,:,None];sp=span(t)
            mean=(local*sp[:,:,None]).sum(1)/sp.sum(1,keepdim=True)
            value=.5*(ref.read.query(.5*(mean+local[:,2]))+ref.read.query(local[:,4]))
            logits=ref.read.output(ref.backbone.core(value));F.cross_entropy(logits,y).backward()
            torch.nn.utils.clip_grad_norm_(list(ref.parameters()),1.,error_if_nonfinite=True);opt.step()
        self.assertEqual(fingerprint(ref.state_dict()),fingerprint(state));self.assertEqual(trace['readout_mode'],'first_mean')
    def test_09_paired_readouts_change_updates_not_initialization(self):
        a=run_toy('native');c=run_toy('first_mean')
        self.assertEqual(a[-2]['initial_sha256'],c[-2]['initial_sha256'])
        self.assertNotEqual(a[-2]['final_sha256'],c[-2]['final_sha256'])
        self.assertEqual(a[-2]['optimizer_group_lrs'],c[-2]['optimizer_group_lrs'])
    def test_10_real2400_step_toy_has_one_optimizer_and_two_cycles(self):
        m,t,y,visits,x,p=numeric_fixture()
        with patch.object(s,'source',return_value=p),contextlib.redirect_stdout(io.StringIO()):
            trace,state=s.optimize(m,'first_mean',{},y,list(range(1200)),[None]*1200,x)
        self.assertEqual(len(trace['ce_history']),2400);self.assertEqual(visits,list(range(1200))*2)
        self.assertEqual(trace['optimizer_creations'],1);self.assertEqual(trace['boundary'],trace['continuation'])
        self.assertEqual(x.policy.optimizer_for.call_count,1);self.assertEqual(trace['policy_receipt'],dict(calls=2400,query_calls=4800,rows=4800,grad_calls=2400))
    def test_11_loss_nonfinite_stops(self):
        m,t,y,v,x,p=numeric_fixture();m.read.output.weight.data.fill_(float('nan'))
        with patch.object(s,'source',return_value=p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),self.assertRaises(ValueError):
            s.optimize(m,'native',{},y,[0,1],[None,None],x)
    def test_12_rate_drift_rejected(self):
        m,t,y,v,x,p=numeric_fixture()
        def factory(m,arm):opt=optimizer(m);opt.param_groups[0]['lr']=.1;return opt
        x.policy.optimizer_for=factory
        with patch.object(s,'source',return_value=p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),self.assertRaisesRegex(ValueError,'learning rates'):
            s.optimize(m,'native',{},y,[0,1],[None,None],x)
    def test_13_cycle_state_mismatch_rejected(self):
        m,t,y,v,x,p=numeric_fixture();count=[0]
        def altered(value):
            if isinstance(value,dict) and set(value)=={'state','param_groups'}:
                count[0]+=1
                if count[0]==2:return 'changed'
            return fingerprint(value)
        p.state_hash=altered
        with patch.object(s,'source',return_value=p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),self.assertRaisesRegex(ValueError,'boundary reset'):
            s.optimize(m,'native',{},y,[0,1],[None,None],x)
    def test_14_snapshot_is_detached_and_nonaliased(self):
        m,_,_,_,_,_,trace,state=run_toy();before=fingerprint(m.state_dict())
        key=next(iter(state));state[key].zero_();self.assertEqual(fingerprint(m.state_dict()),before)
        self.assertTrue(all(not v.requires_grad for v in state.values()))
    def test_15_hooks_restore_and_gradients_reach_encoder(self):
        m,_,_,_,_,_,trace,_=run_toy('first_mean')
        self.assertEqual(trace['policy_receipt']['grad_calls'],4)
        self.assertIsNotNone(m.backbone.local_encoder.embed.weight.grad)
        self.assertTrue(all(not v._forward_hooks and not v._forward_pre_hooks for v in m.modules()))
    def test_16_shortened_cycle_rejected_before_optimizer(self):
        m,t,y,v,x,p=numeric_fixture()
        with patch.object(s,'source',return_value=p),self.assertRaises(ValueError):s.optimize(m,'native',{},y,[],[],x)
        x.policy.optimizer_for.assert_not_called()
    def test_17_training_fingerprint_detects_tensor_mutation(self):
        tables={'original':{(2,'repeat'):torch.ones(2,64,dtype=torch.int64)}};y=torch.tensor([48,49]);events=torch.ones(2,3);mask=torch.zeros(2,3)
        with patch.object(s,'state_hash',side_effect=fingerprint):
            before=s.training_fingerprint(tables,y,events,mask);tables['original'][2,'repeat'][0,0]=9
            self.assertNotEqual(before,s.training_fingerprint(tables,y,events,mask))
    def test_18_schedule_calls_fresh_order_and_registered_allocator(self):
        p=NS(validate_schedule=Mock(),family_mask=Mock(return_value='mask'))
        x=NS(parent=NS(plan_for_order=Mock(return_value='events')),p312=object(),pairs=object())
        with patch.object(s,'source',return_value=NS(curriculum=lambda:p)):
            self.assertEqual(s.schedule(332003,[{}]*192,x),('events','mask'))
        self.assertEqual(x.parent.plan_for_order.call_args.args[:2],(332103,'two_to_four'));p.family_mask.assert_called_once_with('events','batch4')
        for seed in (329001,True,332001.):
            with self.assertRaises(ValueError):s.schedule(seed,[{}]*192,x)
    def test_19_prepared_uses_train_tables_and_exact_targets(self):
        keys=list(itertools.product((2,3,4),('repeat','shared_prefix','shared_suffix')))
        tables={k:torch.zeros((192,64),dtype=torch.int64) for k in keys};y=torch.full((192,),48,dtype=torch.int64)
        training=Mock(return_value={'original':(tables,y),'interior4':(tables,y.clone())})
        with patch.object(s,'source',return_value=NS(curriculum=lambda:NS(previous=lambda:NS(training=training)))):
            a,b=s.prepared({}, {}, {},());self.assertEqual(set(a),{'original','interior4'});self.assertTrue(torch.equal(b,y))
            training.return_value['interior4'][1][0]=49
            with self.assertRaisesRegex(ValueError,'targets differ'):s.prepared({}, {}, {},())
    def test_20_saved_trace_reconstruction_and_tamper(self):
        *_,trace,state=run_toy();events=torch.tensor([0,1]);mask=torch.tensor([0,0]);exposure={'fixture':[1,1]}
        trace.update(seed=332001,training_input_sha256='a'*64,schedule_sha256=s.digest(events.tolist()),mask_sha256=s.digest(mask.tolist()),family_exposure_per_cycle=exposure)
        trace['policy_receipt']=dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400)
        with patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),patch.object(s,'schedule',return_value=(events,mask)),patch.object(s,'source',return_value=NS(curriculum=lambda:NS(exposure=lambda *a:exposure))):
            s.check_trace(trace,[],None)
            for key,value in [('event_indices',[0,1,1,0]),('readout_mode','first_mean'),('optimizer_creations',2),('continuation',{})]:
                bad=copy.deepcopy(trace);bad[key]=value
                with self.subTest(key=key),self.assertRaises(ValueError):s.check_trace(bad,[],None)
    def test_21_gate_allows_saturated_seed_ties_but_requires_aggregate_gain(self):
        v=summary();pairs=v['paired_comparisons'];pairs[0]['six_answer_gain']=pairs[0]['six_pair_gain']=0
        self.assertTrue(s.fixed_gate(pairs)[0])
        for row in pairs:row['six_answer_gain']=row['six_pair_gain']=0
        self.assertFalse(s.fixed_gate(pairs)[0])
    def test_22_each_seed_and_no_regression_required(self):
        for key,value in [('candidate_full_pass',False),('six_answer_gain',-1),('six_pair_gain',-1),('short_answer_gain',-1),('short_pair_gain',-1),('interior_answer_gain',-1),('interior_pair_gain',-1)]:
            pairs=summary()['paired_comparisons'];pairs[2][key]=value
            with self.subTest():self.assertFalse(s.fixed_gate(pairs)[0])
        with self.assertRaises(ValueError):s.fixed_gate(summary()['paired_comparisons'][:-1])
    def test_23_gain_types_and_conservation(self):
        pairs=summary()['paired_comparisons'];pairs[0]['six_answer_gain']=True
        with self.assertRaises(ValueError):s.fixed_gate(pairs)
        z=contrast();z['rescued']=1
        with self.assertRaises(ValueError):s.contrast_check(z)
    def test_24_scientific_negative_is_not_execution_error(self):
        s.check_summary(summary(False));s.check_summary(summary(True))
        bad=summary(False);bad['candidate_gate']=True
        with self.assertRaises(ValueError):s.check_summary(bad)
    def test_25_summary_binds_gains_to_per_length_counts(self):
        v=summary();v['paired_comparisons'][0]['six_answer_gain']=2
        with self.assertRaises(ValueError):s.check_summary(v)
        v=summary();v['train_steps']-=1
        with self.assertRaises(ValueError):s.check_summary(v)
    def test_26_all_fits_finish_before_evaluation(self):
        calls=[];models={a:Toy() for a in s.ARMS};traces=[]
        def train(seed,arm,model,*a):calls.append('train');return dict(seed=seed,arm=arm,initial_sha256='initial'),model.state_dict()
        p=NS(base=lambda:NS(check_dependencies=lambda *a:None))
        def measure(*a):calls.append('evaluate');return {},{}
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'source',return_value=p),patch.object(s,'state_hash',side_effect=fingerprint),patch.object(s,'load_data',return_value=({'TRAIN':[]},{},{})),patch.object(s,'prepared',return_value=({},torch.zeros(1))),patch.object(s,'make_pair',return_value=models),patch.object(s,'train_one',side_effect=train),patch.object(s,'make_model',return_value=Toy()),patch.object(s,'readouts',return_value=NS(measure=measure)),patch.object(s,'analyze',return_value=([],summary(False))),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp);value=s.run_training(out,out,(None,),ROOT,{},e.read)
            self.assertFalse(value['candidate_gate']);self.assertEqual(calls,['train']*10+['evaluate']*20)
            self.assertEqual(set(x.name for x in out.iterdir()),set(s.OUTPUTS))
    def test_27_bundle_identity_order_and_safe_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'m.pt';v=dict(schema='fold-c332-trained-models-v1',identities=[list(z) for z in s.identities()],states=[{'w':torch.ones(1)} for _ in range(10)])
            torch.save(v,p);self.assertEqual(len(s.load_states(p)),10);v['identities'].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):s.load_states(p)
    def test_28_actual_saved_reconstruction_uses_new_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);torch.save(dict(schema='fold-c332-evaluations-v1',records=[]),out/'evaluations.pt')
            for name,value in (('experiment-plan.json',s.manifest()),('training-traces.json',[]),('measurements.json',[]),('validation-summary.json',summary(False))):e.save(out/name,value)
            with patch.object(s,'load_data',return_value=({}, {}, {})),patch.object(s,'load_states',return_value=[]),patch.object(s,'analyze',return_value=([],summary(False))) as analyze:
                s.semantic_recheck(out,out,(),e.read);self.assertEqual(analyze.call_args.args[0],[])
                (out/'validation-summary.json').write_text('{}',encoding='utf-8')
                with self.assertRaises(ValueError):s.semantic_recheck(out,out,(),e.read)
        # Run production analysis over the full cohort with explicitly synthetic
        # legacy scorers and trace validator. This checks pairing/writer wiring.
        states=[{'w':torch.tensor([i],dtype=torch.float64)} for i in range(10)]
        traces=[];records=[]
        for i,(seed,arm) in enumerate(s.identities()):
            trace=dict(seed=seed,arm=arm,initial_sha256='a'*64,core_initial_sha256='b'*64,
                final_sha256=fingerprint(states[i]),readout_mode=s.policy_mode(arm),training_input_sha256='c'*64,
                schedule_sha256='d'*64,mask_sha256='e'*64,family_exposure_per_cycle={},event_indices=[],optimizer_group_lrs=[])
            traces.append(trace);records.append(dict(seed=seed,arm=arm,state_sha256=trace['final_sha256'],
                readout_mode=trace['readout_mode'],raw=dict(evaluation={},replay={}),
                receipts={k:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for k in ('evaluation','replay')}))
        base=NS(validate_raw=Mock(),replay_error=Mock(return_value=0.))
        flags=dict(original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True,failures={})
        helper=NS(summarize_mode=Mock(return_value=({},flags)),compare=Mock(return_value=dict(
            original_by_length={str(n):contrast(1 if n==6 else 0) for n in range(2,7)},interior=contrast())))
        with patch.object(s,'check_trace'),patch.object(s,'state_hash',side_effect=fingerprint),patch.object(s,'source',return_value=NS(base=lambda:base)),patch.object(s,'readouts',return_value=helper):
            metrics,result=s.analyze(traces,records,states,{'TRAIN':[]},(None,))
            self.assertEqual(len(metrics),10);self.assertTrue(result['candidate_gate'])
            self.assertEqual(base.validate_raw.call_count,20);self.assertEqual(helper.compare.call_count,5)
            traces[1]['initial_sha256']='f'*64
            with self.assertRaisesRegex(ValueError,'paired training'):s.analyze(traces,records,states,{'TRAIN':[]},(None,))

    def test_29_parent_contract_is_C331_diagnostic(self):e.parent_contract(*parent_fixture())
    def test_30_parent_small_maps_or_wrong_semantics_rejected(self):
        for target,key,value in ((0,'schema','fold-c330-diagnostic-v1'),(0,'status','FAIL'),(0,'capability_gate_applicable',True),(1,'source_count',841),(1,'input_count',1596),(1,'parent_regression_reconstructed',False),(1,'final_reference_rechecks',2050)):
            args=parent_fixture();args[target][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[1]['regression']['skipped']=1
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_31_all445parent_test_proofs_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);modules=[]
            for i in range(221):
                (p/f'module-{i:03d}.json').write_bytes(b'{}');(p/f'module-{i:03d}.log').write_bytes(b'fixture')
                modules.append(dict(index=i,receipt_sha256=e.sha(p/f'module-{i:03d}.json'),log_sha256=e.sha(p/f'module-{i:03d}.log')))
            e.save(p/'regression-plan.json',{});e.save(p/'regression-result.json',{});e.save(p/'regression-evidence.json',{'modules':modules})
            env={'regression_isolation':dict(tests=5898,modules=221,plan_sha256=e.sha(p/'regression-plan.json'),result_sha256=e.sha(p/'regression-result.json'),evidence_sha256=e.sha(p/'regression-evidence.json'))}
            self.assertEqual(len(e.parent_test_files(p,env,e.sha)),445);(p/'module-220.log').write_bytes(b'bad')
            with self.assertRaises(ValueError):e.parent_test_files(p,env,e.sha)
        self.snapshot_fixture()
    def snapshot_fixture(self):
        # Actual file hashing and complete new union, with synthetic accepted-parent
        # reconstruction callbacks. Not the user's protected parent artifacts.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pins={};inputs={};tree={}
            def write(name,data):
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);return path
            def oid(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            for i in range(847):
                name=e.P_PATH if i==0 else f'ancestor/source_{i}.py';raw=f'# fixture{i}\n'.encode()
                path=write(name,raw);pins[name]=oid(raw);tree[name]=oid(raw);inputs[e.canonical(path)]=e.sha(path)
            inputs.update({f'synthetic-parent-input-{i}':'b'*64 for i in range(2051-847)})
            for name in s.OWN:
                raw=('fixture '+name).encode();write(name,raw);tree[name]=oid(raw)
            folder=root/e.PARENT_FOLDER;out=folder/'science';out.mkdir(parents=True)
            for name in q.OUTPUTS:(out/name).write_bytes(b'parent fixture')
            items=[]
            for i in range(221):
                (folder/f'module-{i:03d}.json').write_bytes(b'{}');(folder/f'module-{i:03d}.log').write_bytes(b'module fixture')
                items.append(dict(index=i,receipt_sha256=e.sha(folder/f'module-{i:03d}.json'),log_sha256=e.sha(folder/f'module-{i:03d}.log')))
            e.save(folder/'regression-plan.json',{});e.save(folder/'regression-result.json',{})
            e.save(folder/'regression-evidence.json',{'modules':items})
            proof=dict(tests=5898,modules=221,plan_sha256=e.sha(folder/'regression-plan.json'),
                evidence_sha256=e.sha(folder/'regression-evidence.json'),result_sha256=e.sha(folder/'regression-result.json'))
            e.save(out/'summary.json',dict(artifacts=[],source_blobs=pins,input_sha256=inputs))
            e.save(folder/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation=proof))
            def descriptors(path,records,names,hash_file):return {e.canonical(path/name):hash_file(path/name) for name in names}
            legacy=NS(descriptors=descriptors,tree_blobs=lambda root:tree);r=object();ph=(r,None,None,legacy,None)
            parent=NS(snapshot=Mock(return_value=({}, {},pins,inputs)),spec=lambda:q,
                build_plan=Mock(return_value={'fixture':True}),verify_tests=Mock(return_value=proof))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(folder/'execution-envelope.json')),patch.object(e,'parent_contract'):
                _,_,a,b=e.snapshot(root,(parent,ph),e.sha)
                self.assertEqual(len(a),853);self.assertEqual(len(b),2508)
                parent.snapshot.assert_called_once_with(root,ph,e.sha)
                self.assertEqual(parent.verify_tests.call_args.args,(folder,e.PARENT_HEAD,{'fixture':True},r))
                (folder/'module-220.log').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'parent module evidence'):e.snapshot(root,(parent,ph),e.sha)

    def test_32_exact_parent_semantic_loader_signature(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);source_out=root/'source/science';source_out.mkdir(parents=True);cp=root/'c330/science/summary.json';cp.parent.mkdir(parents=True)
            flags=[{'fixture':True}];e.save(cp,{'validation_summary':{'seed_results':flags}})
            for name in ('dataset.json','original-prompts.json','interior-prompts.json','evaluations.pt','trained-models.pt'):(source_out/name).write_text('{}',encoding='utf-8')
            b=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda *a:None)))
            cx=(None,None,NS(new_prompts=lambda *a:{},check_prompts=lambda *a:None),None,x)
            ps=NS(semantic_recheck=Mock(return_value={'ok':True}));p=NS(spec=lambda:ps,PARENT_FOLDER='c330')
            ph=(None,NS(PARENT_FOLDER='source'),None,None,None);inputs={e.canonical(cp):'x'}
            inputs.update({e.canonical(v):'x' for v in source_out.iterdir()})
            with patch.object(s,'source',return_value=NS(base=lambda:b)):
                e.parent_semantics(root,(p,ph),{'validation_summary':{'ok':True}},inputs)
            self.assertEqual(ps.semantic_recheck.call_args.args,(root/e.PARENT_FOLDER/'science',source_out,cx,flags,e.read))
    def test_33_plan_appends_real_loader_and_preserves_tool_namespace(self):
        plan,digest=fake_plan();r=fake_recovery();p=NS(build_plan=Mock(return_value={'groups':plan['groups'][:-1]}));ph=(r,None,None,None,None)
        with patch.object(e,'BASE_IDS_SHA',digest):
            actual=e.build_plan(ROOT,HEAD,(p,ph));self.assertEqual(len(actual['groups']),222)
            self.assertEqual(actual['groups'][0]['module'],'tests_tools.test_c324_locked_hash_r4')
            self.assertEqual(len(actual['groups'][-1]['test_ids']),48);self.assertTrue(all('.C332Tests.' in x for x in actual['groups'][-1]['test_ids']))
            self.assertEqual(p.build_plan.call_args.args,(ROOT,HEAD,ph))
    def test_34_plan_cannot_omit_duplicate_or_reorder_tests(self):
        plan,digest=fake_plan();r=fake_recovery()
        with patch.object(e,'BASE_IDS_SHA',digest):
            for kind in ('drop','duplicate','reorder','module'):
                v=copy.deepcopy(plan)
                if kind=='drop':v['groups'].pop()
                elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
                elif kind=='reorder':v['groups'][0]['test_ids'].reverse()
                else:v['groups'][0]['module']='bad.module'
                with self.subTest(),self.assertRaises(ValueError):e.validate_plan(v,HEAD,r)
    def test_35_collector_and_fresh_verifier_use_same_accepted_ABI(self):
        plan,digest=fake_plan();r=fake_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp);e.collect_tests(out,HEAD,plan,r,lambda i,h:fake_module(out,plan,i,h))
            self.assertEqual(e.verify_tests(out,HEAD,plan,r)['tests'],5946);self.assertEqual(r.validate_module_evidence.call_count,444)
            (out/'module-221.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(out,HEAD,plan,r)
    def test_36_failed_module_is_not_retried(self):
        plan,digest=fake_plan();r=fake_recovery();calls=[]
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)
            def run(i,h):calls.append(i);raise ValueError('fixture')
            with self.assertRaises(ValueError):e.collect_tests(out,HEAD,plan,r,run)
            self.assertEqual(calls,[0]);self.assertFalse((out/'regression-result.json').exists())
    def test_37_module_CLI_uses_new_guard_and_generic_receipt(self):
        plan,digest=fake_plan();r=fake_recovery();g=plan['groups'][0]
        r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'guard'),patch.object(e,'helpers',return_value=(None,(r,None,None,None,None))),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp);e.save(out/'regression-plan.json',plan);e.module_child(out,out,HEAD,0,e.sha(out/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);row=e.read(out/'module-000.json')
            self.assertEqual(row['schema'],'fold-c330-r1-module-v2');self.assertEqual(row['commit_sha'],HEAD);self.assertEqual(row['parent_pid'],e.os.getppid())
    def test_38_real_git_guard_and_unique_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);head=git_fixture(root);e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError):e.guard(root,head)
        self.assertFalse(e.active('## Formal state\nC331 ACTIVE / NOT YET JUDGED'))
    def test_39_strict_utf8_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x';e.save(p,{'名前':'甲乙'});self.assertEqual(e.read(p),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(p,{})
            for v in ('{"a":1,"a":2}','NaN','Infinity'):
                p.write_text(v,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(p)
    def test_40_source_LF_CRLF_and_tampering(self):
        raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x'
            for v in (raw,raw.replace(b'\n',b'\r\n')):p.write_bytes(v);e.source_bytes(p,oid)
            p.write_bytes(b'bad')
            with self.assertRaises(ValueError):e.source_bytes(p,oid)
    def test_41_actual_nonzero_subprocess_and_CLI_rejection(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp);log=out/'failure.log'
            with self.assertRaises(ValueError):e.run_logged(out,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
        p=subprocess.run([sys.executable,str(ROOT/'tools/c332_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(p.returncode,0);self.assertIn('invalid choice',p.stderr)
    def test_42_stage_order_and_failed_regression_blocks_training(self):
        training=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(lambda:None,Mock(side_effect=ValueError('fixture')),training,Mock(),Mock())
        training.assert_not_called();calls=[]
        def step(n,v):
            def run():calls.append(n);return v
            return run
        with contextlib.redirect_stdout(io.StringIO()):
            e.execute_stages(step('pre',None),step('tests',dict(tests=5946,modules=222)),step('train',{'gate':False}),step('saved',{'gate':False}),step('final',[]))
        self.assertEqual(calls,['pre','tests','train','saved','final'])
    def test_43_saved_output_byte_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
            e.bound_semantics(out,lambda:None)
            def mutate():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,mutate)
    def test_44_launcher_preflight_and_source_numeric_call_order(self):
        text=(ROOT/'tools/invoke_c332.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C332',text);self.assertIn('c332_execution.py',(ROOT/'tools/run_c332.ps1').read_text(encoding='utf-8'))
        tree=ast.parse(inspect.getsource(s.optimize));names=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertEqual(names.count('manual_seed'),1);self.assertEqual(names.count('optimizer_for'),1)
        self.assertNotIn('evaluate',names);self.assertNotIn('HOLDOUT',inspect.signature(s.optimize).parameters)
    def test_45_production_worker_keeps_valid_negative(self):self.worker_fixture(False)
    def test_46_production_worker_stops_after_regression_failure(self):self.worker_fixture(True)
    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);calls=[];value=summary(False)
            pins={f'p{i}':'a'*40 for i in range(s.SOURCE_COUNT)};inputs={str(root/f'i{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={};stats={'final_reference_rechecks':s.INPUT_COUNT};sha=staticmethod(e.sha)
                def __init__(self,*a,**kw):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            runtime=NS(native_runtime=lambda:(NS(__version__='synthetic'),NS(__version__='synthetic')))
            ph=(None,None,runtime,None,locks);cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            source=NS(base=lambda:NS(check_dependencies=lambda *a:None,peak_rss=lambda:1))
            def snap(*a):calls.append('snapshot');return {},{},pins,inputs
            def parent(*a):calls.append('parent');return root/'source',cx
            def tests(*a):
                calls.append('tests')
                if bad:raise ValueError('fixture')
                e.save(folder/'regression-result.json',e.receipt(HEAD,5946))
            def train(out,*a):
                calls.append('train')
                for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
                return value
            def saved(*a):calls.append('saved');return value
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(None,ph)),patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=parent),patch.object(s,'source',return_value=source),patch.object(e,'run_logged',side_effect=tests),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value=dict(tests=5946,modules=222)),patch.object(s,'native_preflight',side_effect=lambda *a:calls.append('pre')),patch.object(s,'run_training',side_effect=train),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError):e.scientific_worker(root,folder,HEAD)
                    self.assertNotIn('train',calls)
                else:
                    e.scientific_worker(root,folder,HEAD);self.assertEqual(calls,['snapshot','parent','pre','tests','train','saved','final','release'])
                    r=e.read(folder/'science/summary.json');self.assertEqual(r['status'],'FAIL');self.assertTrue(r['diagnostic_execution_valid'])
    def test_47_controller_no_retry_and_output_boundary(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as call,contextlib.redirect_stdout(io.StringIO()) as log:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(call.call_count,1);self.assertIn('run_execution_valid = false',log.getvalue())
            with self.assertRaises(ValueError):e.run(root,root/'outside',HEAD)
    def test_48_native_preflight_calls_both_backward_policies(self):
        m,t,y,_,x,p=numeric_fixture();data={'TRAIN':[{'language':'en'},{'language':'ja'}]}
        tables={family:{(4,'repeat'):t} for family in ('original','interior4')}
        p.base=lambda:NS(check_dependencies=lambda *a:None)
        with patch.object(s,'load_data',return_value=(data,{},{})),patch.object(s,'prepared',return_value=(tables,y)),patch.object(s,'schedule') as schedule,patch.object(s,'make_model',return_value=m),patch.object(s,'source',return_value=p),contextlib.redirect_stdout(io.StringIO()) as log:
            s.native_preflight(ROOT,(x,),ROOT,{},e.read)
            self.assertEqual(schedule.call_count,5);self.assertIn('backward=4;optimizer_steps=0',log.getvalue())
            self.assertIsNotNone(m.read.query.weight.grad)


if __name__=='__main__':unittest.main()
