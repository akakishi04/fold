"""C338 software fixtures. Toy updates and synthetic ancestor proofs are not native results."""
from __future__ import annotations
from collections import Counter
import contextlib
import copy
import hashlib
import importlib.util
import io
import itertools
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
from fold_lm.v05_benchmarks import model_c338_value_support_training as s

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c338_test_executor',ROOT/'tools/c338_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def data_fixture():
    data = {'TRAIN':[],'HOLDOUT':[]}; held = {(0,2),(1,3),(2,0),(3,1)}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),('en','ja')):
        split = 'HOLDOUT' if values in held else 'TRAIN'
        for order,query in itertools.product((entities,entities[::-1]),entities):
            data[split].append(dict(id=f'{lang}:{entities}:{values}:{order}:{query}',entities=list(entities),values=list(values),
                language=lang,permutation=list(order),query=query,target=48+values[entities.index(query)]))
    assert s.digest(data) == '1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1'
    return data


def fingerprint(value):
    def convert(v):
        if isinstance(v,torch.Tensor):return [str(v.dtype),list(v.shape),v.detach().cpu().tolist()]
        if isinstance(v,dict):return [[str(k),convert(x)] for k,x in v.items()]
        if isinstance(v,(tuple,list)):return [convert(x) for x in v]
        return v
    return s.digest(convert(value))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); torch.manual_seed(338)
        self.backbone=torch.nn.Module();self.backbone.core=torch.nn.Linear(2,2,bias=False,dtype=torch.float64)
        self.read=torch.nn.Module();self.read.query=torch.nn.Linear(2,2,bias=False,dtype=torch.float64)
        self.read.output=torch.nn.Linear(2,256,bias=False,dtype=torch.float64)
    def forward(self,tokens,tasks):
        x=tokens.to(torch.float64)
        for _ in range(4):x=torch.tanh(self.backbone.core(x))
        return self.read.output((self.read.query(x)+self.read.query(x))*.5)


@contextlib.contextmanager
def counted_readout(model,wide,mode):
    e.require(mode=='native_before','native-only fixture')
    stats=dict(calls=0,query_calls=0,rows=0,grad_calls=0)
    def forward(m,args,out):
        stats['calls']+=1;stats['rows']+=len(args[0]);stats['grad_calls']+=int(torch.is_grad_enabled())
    def query(m,args,out):stats['query_calls']+=1
    a=model.register_forward_hook(forward);b=model.read.query.register_forward_hook(query)
    try:yield stats
    finally:a.remove();b.remove()


def toy_environment():
    data=data_fixture();y=torch.tensor([r['target'] for r in data['TRAIN']],dtype=torch.int64)
    features=torch.tensor([[i%7/7.,i%11/11.] for i in range(192)],dtype=torch.float64)
    tables={f:{(4,'repeat'):features.clone()} for f in ('original','interior4')}
    events=torch.stack([torch.arange((i%4)*48,(i%4+1)*48) for i in range(1200)])
    mask=torch.zeros((1200,48),dtype=torch.bool)
    curriculum=NS(select_tokens=lambda t,event,m:(t['original'][4,'repeat'][event],event),validate_schedule=lambda a:None,
        family_mask=lambda *a:mask,exposure=lambda *a:{'synthetic':1200})
    def optimizer(model,policy):
        core=list(model.backbone.core.parameters());core_ids={id(v) for v in core}
        return torch.optim.AdamW([{'params':[v for v in model.parameters() if id(v) not in core_ids],'lr':.005},
                                 {'params':core,'lr':.0005}],betas=(.9,.999),eps=1e-8,weight_decay=0.)
    def check_logits(z,n):e.require(z.shape==(n,256) and bool(torch.isfinite(z).all()),'toy logits')
    @contextlib.contextmanager
    def counted(model,unused):
        calls=[0,0];cores=[0]
        def forward(m,args,out):calls[0]+=1;calls[1]+=len(args[0])
        def core(m,args,out):cores[0]+=1
        a=model.register_forward_hook(forward);b=model.backbone.core.register_forward_hook(core)
        try:yield calls,cores
        finally:a.remove();b.remove()
    x=NS(policy=NS(optimizer_for=optimizer,verify_optimizer=lambda *a:None),wide=None,
         c=NS(p267=NS(check_logits=check_logits,counted=counted),core=None),parent=NS(plan_for_order=Mock(return_value=events)),p312=None,pairs=None)
    base=NS(check_dependencies=lambda *a:None,peak_rss=lambda:1)
    p=NS(state_hash=fingerprint,training_fingerprint=lambda *a:fingerprint(a),
        source=lambda:NS(curriculum=lambda:curriculum,base=lambda:base),readouts=lambda:NS(readout=counted_readout))
    return NS(data=data,y=y,supplied=s.support_labels(data['TRAIN'],y),tables=tables,events=events,mask=mask,x=x,p=p)


def independent_fit(model,env,arm,steps):
    opt=env.x.policy.optimizer_for(model,'core_slow');losses=[]
    for step in range(steps):
        ids=env.events[step%1200];opt.zero_grad(set_to_none=True)
        z=model(env.tables['original'][4,'repeat'][ids],torch.zeros(48,dtype=torch.int64))
        ce=F.cross_entropy(z,env.y[ids]);selected=z.gather(1,env.supplied[ids])
        support=(torch.logsumexp(z,1)-torch.logsumexp(selected,1)).mean()
        loss=ce if arm=='native' else ce+support
        losses.append(dict(total=float(loss.detach()),ce=float(ce.detach()),support=float(support.detach())))
        loss.backward();torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True);opt.step()
    return losses,model.state_dict()


def contrast(correct=280,gain=1,pairs=138):
    return dict(answers=288,query_pairs=144,control_correct=correct,candidate_correct=correct+gain,
        control_both_correct=pairs,candidate_both_correct=pairs+gain,rescued=max(gain,0),regressed=max(-gain,0),
        pair_rescued=max(gain,0),pair_regressed=max(-gain,0),answer_gain=gain,query_pair_gain=gain)


def check_contrast(z):
    expected=set(contrast());e.require(set(z)==expected and all(type(v) is int for v in z.values()),'contrast fields')
    e.require(z['answers']==288 and z['query_pairs']==144,'contrast denominator')
    e.require(z['answer_gain']==z['candidate_correct']-z['control_correct']==z['rescued']-z['regressed'],'answer conservation')
    e.require(z['query_pair_gain']==z['candidate_both_correct']-z['control_both_correct']==z['pair_rescued']-z['pair_regressed'],'pair conservation')


def summary_fixture(gain=1):
    flags=[];pairs=[]
    for seed in s.SEEDS:
        for j,arm in enumerate(s.ARMS):
            support={d:dict(answers=288,correct=280+j*gain,wrong_observed=4,absent_digit=4-j*gain,outside_catalog=0) for d in s.DOMAINS}
            flags.append(dict(seed=seed,arm=arm,original_pass={str(n):True for n in range(2,7)},interior_pass=True,retention_pass=True,support=support))
        pairs.append(dict(seed=seed,control_full_pass=True,candidate_full_pass=True,
            domains={d:dict(**contrast(gain=gain),outside_gain=-gain) for d in s.DOMAINS}))
    return dict(candidate_gate=gain>0,eligible_seed_count=5,paired_conditions_valid=True,all_replays=True,
        evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**s.WORK)


def raw_fixture(data,arm):
    z={}
    for sp,rows in data.items():
        value=torch.full((len(rows),256),-4.,dtype=torch.float64)
        for i,r in enumerate(rows):
            t=r['target'];other=48+r['values'][1-r['entities'].index(r['query'])];value[i,t]=3.
            if i%8==0:value[i,min(set(range(48,52))-{t,other})]=4.
            elif i%8==1 and arm=='native':value[i,other]=4.
        z[sp]=value
    def tree(profiles):return {sp:{pr:{v:z[sp].clone() for v in ('normal','evidence_blind','query_blind')} for pr in profiles} for sp in data}
    return dict(original={str(n):tree(('repeat',) if n==1 else ('repeat','shared_prefix','shared_suffix')) for n in range(1,7)},
                interior=tree(('u_dominant','balanced','v_dominant')))


def independent_compare(a,b,data,base):
    y=[r['target'] for r in data['HOLDOUT']]
    def one(x,z):
        old=[];new=[]
        for profile in x:
            old.extend(v==t for v,t in zip(x[profile]['normal'].argmax(-1).tolist(),y))
            new.extend(v==t for v,t in zip(z[profile]['normal'].argmax(-1).tolist(),y))
        op=[all(old[i:i+2]) for i in range(0,288,2)];np=[all(new[i:i+2]) for i in range(0,288,2)]
        return dict(answers=288,query_pairs=144,control_correct=sum(old),candidate_correct=sum(new),
            control_both_correct=sum(op),candidate_both_correct=sum(np),rescued=sum(not x and y for x,y in zip(old,new)),
            regressed=sum(x and not y for x,y in zip(old,new)),pair_rescued=sum(not x and y for x,y in zip(op,np)),
            pair_regressed=sum(x and not y for x,y in zip(op,np)),answer_gain=sum(new)-sum(old),query_pair_gain=sum(np)-sum(op))
    return dict(original_by_length={str(n):one(a['original'][str(n)]['HOLDOUT'],b['original'][str(n)]['HOLDOUT']) for n in range(2,7)},
                interior=one(a['interior']['HOLDOUT'],b['interior']['HOLDOUT']))


def scientific_fixture():
    data=data_fixture();traces=[];records=[];states=[]
    for seed,arm in s.identities():
        state={'w':torch.tensor([float(seed),float(arm=='support_loss')],dtype=torch.float64)};states.append(state)
        trace={k:'paired' for k in ('initial_sha256','core_initial_sha256','training_input_sha256','support_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')}
        trace.update(seed=seed,arm=arm,final_sha256=fingerprint(state));traces.append(trace)
        raw=raw_fixture(data,arm);records.append(dict(seed=seed,arm=arm,state_sha256=fingerprint(state),evaluation_policy='native_before',
            raw={m:copy.deepcopy(raw) for m in ('evaluation','replay')},receipts={m:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for m in ('evaluation','replay')}))
    def replay(a,b,*args):
        def walk(x,y):
            if isinstance(x,dict):
                e.require(set(x)==set(y),'keys')
                for k in x:walk(x[k],y[k])
            else:e.require(torch.equal(x,y),'saved logits')
        walk(a,b);return 0.
    def scored(raw,data,cx):
        return {},dict(original_pass={str(n):False for n in range(2,7)},interior_pass=False,retention_pass=False,failures={})
    base=NS(validate_raw=Mock(),replay_error=replay)
    q=NS(summarize_mode=scored,compare=independent_compare)
    p=NS(state_hash=fingerprint,source=lambda:NS(base=lambda:base),readouts=lambda:q,contrast_check=check_contrast)
    return NS(data=data,traces=traces,records=records,states=states,p=p,cx=(None,))


def fake_recovery():
    def flatten(suite):
        for x in suite:
            if isinstance(x,unittest.TestSuite):yield from flatten(x)
            else:yield x
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==i
                  and row['module']==g['module'] and row['plan_sha256']==ph,'module ABI')
        e.require(row['result']['success_ids']==g['test_ids'] and row['result']['tests']==len(g['test_ids']),'all IDs')
        e.require(launcher in (row['pid'],row['parent_pid']),'topology')
        return 'direct' if launcher==row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',allowed_module=lambda n:bool(re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',n)),
              validate_module_evidence=Mock(side_effect=validate))


def plan_fixture():
    groups=[];q,r=divmod(6122,227)
    for i in range(227):
        m=f'tests_lm.fixture_{i:03d}';groups.append(dict(module=m,test_ids=[m+f'.C.test_{j:03d}' for j in range(q+(i<r))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C338Tests.test_{i:02d}' for i in range(48)]))
    ids=[v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c338-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-48])


def proof(folder,plan,i,ph):
    g=plan['groups'][i];pid,parent=20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,module=g['module'],plan_sha256=ph,
        pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_bytes(b'explicit synthetic proof');return pid if i%2==0 else parent


def parent_fixture():
    ps=NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='manifest',WORK={})
    parent=NS(spec=lambda:ps,PARENT_SUMMARY='old-summary',PARENT_ENVELOPE='old-envelope')
    pins={e.P_PATH:e.P_BLOB,e.S_PATH:e.S_BLOB,**{f'p{i}':'a' for i in range(881)}};inputs={f'i{i}':'b' for i in range(4827)}
    r=dict(schema='fold-c337-diagnostic-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        manifest_sha256='manifest',source_blobs=pins,input_sha256=inputs,validation_summary=dict(parent_candidate_gate=False,parent_eligible_seed_count=1))
    v=dict(schema='fold-c337-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='PASS',scientific_summary_sha256=e.PARENT_SUMMARY,
        manifest_sha256='manifest',scientific_work={},source_count=883,input_count=4827,source_blobs=pins,input_sha256=inputs,
        parent_summary_sha256=parent.PARENT_SUMMARY,parent_envelope_sha256=parent.PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,
        parent_regression_reconstructed=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=4827,
        hash_stats={'final_reference_rechecks':4827},regression=e.receipt(e.PARENT_HEAD,6122))
    return r,v,parent


class C338Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();torch.set_num_threads(2);cls.env=toy_environment()
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)
    def context(self):return patch.object(s,'previous',return_value=NS(contrast_check=check_contrast))
    def test_01_manifest_and_actual_test_loader(self):
        s.validate_seal();self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),48)
        with patch.object(s,'RATES',(.1,.1)),self.assertRaises(ValueError):s.validate_seal()
        with patch.object(s,'SEEDS',(1,)),self.assertRaises(ValueError):s.validate_seal()
    def test_02_canonical_dataset_and_all_nonbinary_pairs(self):
        from fold_lm.v05_benchmarks import model_c267_name_coverage_training as original
        data=data_fixture();self.assertEqual(data,original.dataset());self.assertEqual([len(data[k]) for k in ('TRAIN','HOLDOUT')],[192,96])
        self.assertEqual(len({tuple(r['values']) for rows in data.values() for r in rows}),12)
        self.assertEqual(s.INPUT_COUNT,4827+463+6);self.assertEqual(s.FULL_TESTS,6122+48)
    def test_03_support_is_query_and_order_independent(self):
        labels=s.support_labels(self.env.data['TRAIN'],self.env.y)
        for i in range(0,192,4):self.assertTrue(torch.equal(labels[i:i+4],labels[i].expand(4,2)))
        self.assertEqual(set(map(tuple,labels.tolist())),{(48,49),(48,51),(49,50),(50,51)})
    def test_04_invalid_support_rows_rejected(self):
        for values in ([True,1],[0,0],[0,4],[0.,1.]):
            rows=copy.deepcopy(self.env.data['TRAIN']);rows[0]['values']=values
            with self.assertRaises(ValueError):s.support_labels(rows,self.env.y)
        with self.assertRaises(ValueError):s.support_labels(self.env.data['HOLDOUT'],self.env.y)
    def test_05_loss_matches_scalar_reference(self):
        z=torch.tensor([[i/80 for i in range(256)]],dtype=torch.float64);t=torch.tensor([48]);pair=torch.tensor([[48,50]])
        total,ce,support=s.objective(z,t,pair,1.)
        lse=torch.log(torch.exp(z).sum());self.assertAlmostEqual(float(ce),float(lse-z[0,48]),places=13)
        self.assertAlmostEqual(float(support),float(lse-torch.log(torch.exp(z[0,48])+torch.exp(z[0,50]))),places=13)
        self.assertEqual(float(total),float(ce+support))
    def test_06_exact_objective_decomposition(self):
        z=torch.randn((12,256),dtype=torch.float64);t=torch.tensor([48]*12);pair=torch.tensor([[48,51]]*12)
        total,ce,support=s.objective(z,t,pair,1.);within=F.cross_entropy(z[:,[48,51]],torch.zeros(12,dtype=torch.int64))
        self.assertTrue(torch.allclose(ce,support+within,rtol=0,atol=2e-15));self.assertTrue(torch.allclose(total,2*support+within,rtol=0,atol=4e-15))
    def test_07_alpha_zero_exact_CE_and_gradient(self):
        z=torch.randn((3,256),dtype=torch.float64,requires_grad=True);t=torch.tensor([48,49,50]);pair=torch.tensor([[48,51],[49,50],[48,50]])
        got=s.objective(z,t,pair,0.)[0];want=F.cross_entropy(z,t)
        self.assertTrue(torch.equal(got,want));self.assertTrue(torch.equal(torch.autograd.grad(got,z,retain_graph=True)[0],torch.autograd.grad(want,z)[0]))
    def test_08_finite_difference_gradients(self):
        z=torch.randn((2,256),generator=torch.Generator().manual_seed(338),dtype=torch.float64,requires_grad=True)
        t=torch.tensor([48,50]);pair=torch.tensor([[48,49],[50,51]]);loss=s.objective(z,t,pair,1.)[0];g=torch.autograd.grad(loss,z)[0]
        for i,j in ((0,48),(0,49),(0,7),(1,50),(1,51)):
            a=z.detach().clone();b=a.clone();a[i,j]+=1e-5;b[i,j]-=1e-5
            num=(s.objective(a,t,pair,1.)[0]-s.objective(b,t,pair,1.)[0])/(2e-5)
            self.assertAlmostEqual(float(g[i,j]),float(num),places=8)
    def test_09_support_gradient_matches_softmax_difference(self):
        z=torch.randn((2,256),dtype=torch.float64,requires_grad=True);t=torch.tensor([48,50]);pair=torch.tensor([[48,49],[50,51]])
        support=s.objective(z,t,pair,1.)[2];g=torch.autograd.grad(support,z)[0];expected=z.detach().softmax(1)
        expected.scatter_add_(1,pair,-z.detach().gather(1,pair).softmax(1));expected/=2
        self.assertTrue(torch.allclose(g,expected,rtol=1e-13,atol=1e-15))
    def test_10_loss_inputs_unchanged(self):
        z=torch.randn((2,256),dtype=torch.float64);t=torch.tensor([48,49]);pair=torch.tensor([[48,50],[49,51]])
        old=[x.clone() for x in (z,t,pair)];s.objective(z,t,pair,1.)
        self.assertTrue(all(torch.equal(x,y) for x,y in zip(old,(z,t,pair))))
    def test_11_nonfinite_and_overflow_rejected(self):
        t=torch.tensor([48]);pair=torch.tensor([[48,49]])
        for val in (float('nan'),float('inf')):
            z=torch.zeros((1,256),dtype=torch.float64);z[0,0]=val
            with self.assertRaises(ValueError):s.objective(z,t,pair,1.)
        z=torch.full((1,256),1e308,dtype=torch.float64);z[0,48:50]=-1e308
        with self.assertRaises(ValueError):s.objective(z,t,pair,1.)
    def test_12_types_shapes_and_unregistered_coefficients(self):
        z=torch.zeros((1,256),dtype=torch.float64);t=torch.tensor([48]);pair=torch.tensor([[48,50]])
        for a in (True,1,0.5,-1.,float('nan')):
            with self.assertRaises(ValueError):s.objective(z,t,pair,a)
        for q in (torch.tensor([[50,48]]),torch.tensor([[48,48]]),torch.tensor([[48,52]]),pair.float()):
            with self.assertRaises(ValueError):s.objective(z,t,q,1.)
        with self.assertRaises(ValueError):s.objective(z.float(),t,pair,1.)
    def test_13_support_term_does_not_identify_queried_value(self):
        z=torch.randn((4,256),dtype=torch.float64);pair=torch.tensor([[48,50]]*4)
        a=s.objective(z,torch.tensor([48]*4),pair,1.)[2];b=s.objective(z,torch.tensor([50]*4),pair,1.)[2]
        self.assertTrue(torch.equal(a,b))
    def test_14_support_pushes_mass_to_both_supplied_values(self):
        z=torch.zeros((1,256),dtype=torch.float64,requires_grad=True);g=torch.autograd.grad(s.objective(z,torch.tensor([48]),torch.tensor([[48,50]]),1.)[2],z)[0]
        self.assertLess(float(g[0,48]),0);self.assertLess(float(g[0,50]),0);self.assertGreater(float(g[0,7]),0)
    def short_fit(self,arm):
        model=Toy();ref=copy.deepcopy(model);f=self.env
        with patch.object(s,'previous',return_value=f.p),patch.object(s,'CYCLE',2),patch.object(s,'STEPS',4),contextlib.redirect_stdout(io.StringIO()):
            trace,state=s.optimize(model,arm,f.tables,f.y,f.supplied,f.events[:2],f.mask[:2],f.x)
        # Reference repeats the same first two batches, unlike the normal1200cycle.
        g=copy.copy(f);g.events=f.events[:2].repeat(600,1)
        losses,wanted=independent_fit(ref,g,arm,4)
        self.assertEqual(trace['loss_history'],losses);self.assertEqual(fingerprint(state),fingerprint(wanted));return trace,state
    def test_15_one_native_forward_per_update(self):
        trace,_=self.short_fit('support_loss');self.assertEqual(trace['policy_receipt'],dict(calls=4,query_calls=8,rows=192,grad_calls=4))
        f=self.env;p=copy.copy(f.p);p.load_data=lambda *a:(f.data,{},{});p.prepared=lambda *a:(f.tables,f.y)
        def same(a,b):e.require(torch.equal(a,b),'native preflight equality')
        p.readouts=lambda:NS(readout=counted_readout,same=same)
        with patch.object(s,'previous',return_value=p),patch.object(s,'make_model',side_effect=lambda *a:Toy()),contextlib.redirect_stdout(io.StringIO()):
            s.native_preflight(ROOT,(f.x,),ROOT,{},e.read)
    def test_16_zero_aux_updates_equal_independent_reference(self):self.short_fit('native')
    def test_17_support_updates_equal_independent_reference(self):self.short_fit('support_loss')
    def test_18_actual2400_updates_both_arms_and_continuation(self):
        f=self.env;final=[]
        for arm in s.ARMS:
            model=Toy();ref=copy.deepcopy(model)
            with patch.object(s,'previous',return_value=f.p),contextlib.redirect_stdout(io.StringIO()):
                trace,state=s.train_one(s.SEEDS[0],arm,model,f.tables,f.y,f.supplied,f.data['TRAIN'],(f.x,),ROOT,{})
                s.check_trace(trace,f.data['TRAIN'],f.x)
            losses,wanted=independent_fit(ref,f,arm,2400)
            self.assertEqual(trace['loss_history'],losses);self.assertEqual(fingerprint(state),fingerprint(wanted))
            self.assertEqual(trace['boundary'],trace['continuation']);self.assertEqual(len(trace['loss_history']),2400)
            final.append(fingerprint(state))
        self.assertNotEqual(*final)
    def trace_fixture(self,arm='native'):
        f=self.env;events,mask=f.events,f.mask
        t=dict(seed=s.SEEDS[0],arm=arm,coefficient=s.coefficient(arm),support_sha256=s.digest(f.supplied.tolist()),steps=2400,
            event_indices=list(range(1200))*2,schedule_sha256=s.digest(events.tolist()),mask_sha256=s.digest(mask.tolist()),
            family_exposure_per_cycle={'synthetic':1200},optimizer_group_lrs=[list(s.RATES)]*2400,
            loss_history=[dict(ce=1.,support=2.,total=1. if arm=='native' else 3.) for _ in range(2400)],
            gradient_union={'w':1},gradient_parameter_counts=[1]*2400,initial_sha256='a'*64,final_sha256='b'*64,
            core_initial_sha256='a'*64,core_final_sha256='b'*64,training_input_sha256='c'*64,
            boundary={'weights':'b'*64,'optimizer':'d'*64},continuation={'weights':'b'*64,'optimizer':'d'*64},
            optimizer_creations=1,intermediate_evaluations=0,policy_receipt=dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400))
        return t
    def trace_context(self):return patch.object(s,'previous',return_value=self.env.p)
    def test_19_trace_rejects_optimizer_restart_and_selection(self):
        with self.trace_context():
            s.check_trace(self.trace_fixture(),self.env.data['TRAIN'],self.env.x)
            for k,v in (('optimizer_creations',2),('intermediate_evaluations',1),('continuation',{'weights':'f'*64,'optimizer':'e'*64})):
                t=self.trace_fixture();t[k]=v
                with self.assertRaises(ValueError):s.check_trace(t,self.env.data['TRAIN'],self.env.x)
    def test_20_training_support_is_in_input_fingerprint(self):
        f=self.env
        with self.trace_context():
            a=s.training_hash(f.tables,f.y,f.supplied,f.events,f.mask);b=f.supplied.clone();b[0]=torch.tensor([48,51])
            self.assertNotEqual(a,s.training_hash(f.tables,f.y,b,f.events,f.mask))
    def test_21_trace_loss_arithmetic_tamper(self):
        t=self.trace_fixture('support_loss');t['loss_history'][0]['total']=1.
        with self.trace_context(),self.assertRaises(ValueError):s.check_trace(t,self.env.data['TRAIN'],self.env.x)
    def test_22_trace_support_coefficient_and_budget_tamper(self):
        for k,v in (('support_sha256','wrong'),('coefficient',True),('steps',1200),('policy_receipt',{})):
            t=self.trace_fixture();t[k]=v
            with self.trace_context(),self.assertRaises(ValueError):s.check_trace(t,self.env.data['TRAIN'],self.env.x)
    def test_23_all_fresh_schedules_use_registered_orders(self):
        x=copy.copy(self.env.x);x.parent=NS(plan_for_order=Mock(return_value=self.env.events))
        with self.trace_context():
            for seed in s.SEEDS:s.schedule(seed,self.env.data['TRAIN'],x)
            self.assertEqual([a.args[0] for a in x.parent.plan_for_order.call_args_list],list(s.ORDERS))
            with self.assertRaises(ValueError):s.schedule(335002,self.env.data['TRAIN'],x)
    def test_24_pair_created_before_training_and_independent(self):
        with self.trace_context(),patch.object(s,'make_model',side_effect=lambda *a:Toy()):
            pair=s.make_pair(s.SEEDS[0],None)
            self.assertEqual(fingerprint(pair['native'].state_dict()),fingerprint(pair['support_loss'].state_dict()))
            with torch.no_grad():next(pair['native'].parameters()).add_(1)
            self.assertNotEqual(fingerprint(pair['native'].state_dict()),fingerprint(pair['support_loss'].state_dict()))
    def test_25_fixed_gate_all5_and_strict_gains(self):
        with self.context():s.check_summary(summary_fixture())
        self.assertTrue(s.fixed_gate(summary_fixture()['paired_comparisons'])[0])
        pairs=summary_fixture()['paired_comparisons'];pairs[0]['candidate_full_pass']=False;self.assertFalse(s.fixed_gate(pairs)[0])
    def test_26_equal_results_are_valid_negative_not_retry(self):
        with self.context():s.check_summary(summary_fixture(0))
        self.assertFalse(s.fixed_gate(summary_fixture(0)['paired_comparisons'])[0])
    def test_27_one_domain_harm_cannot_hide_in_total(self):
        p=summary_fixture()['paired_comparisons'];p[0]['domains']['original2']['answer_gain']=-1
        self.assertFalse(s.fixed_gate(p)[0])
        p[0]['domains']['original2']['answer_gain']=True
        with self.assertRaises(ValueError):s.fixed_gate(p)
    def test_28_outside_errors_must_drop_without_seed_harm(self):
        p=summary_fixture()['paired_comparisons']
        for r in p:
            for z in r['domains'].values():z['outside_gain']=0
        self.assertFalse(s.fixed_gate(p)[0]);p[0]['domains']['original2']['outside_gain']=1
        self.assertFalse(s.fixed_gate(p)[0])
    def test_29_summary_partitions_and_bool_work_rejected(self):
        with self.context():
            for kind in ('work','support','contrast'):
                v=summary_fixture()
                if kind=='work':v['training_models']=True
                elif kind=='support':v['seed_results'][0]['support']['original2']['correct']+=1
                else:v['paired_comparisons'][0]['domains']['original2']['outside_gain']=0
                with self.assertRaises(ValueError):s.check_summary(v)
    def test_30_support_report_keeps_raw_outside_predictions(self):
        data=data_fixture();r=s.support_report(raw_fixture(data,'native'),data)
        self.assertEqual(set(r),set(s.DOMAINS))
        for z in r.values():self.assertEqual((z['correct'],z['wrong_observed'],z['absent_digit'],z['outside_catalog']),(216,36,36,0))
    def test_31_actual_analysis_full_cohort_and_replay(self):
        f=scientific_fixture()
        with patch.object(s,'previous',return_value=f.p),patch.object(s,'check_trace'):
            metrics,v=s.analyze(f.traces,f.records,f.states,f.data,f.cx);self.assertEqual(len(metrics),10)
            self.assertEqual(f.p.source().base().validate_raw.call_count,20);self.assertFalse(v['candidate_gate'])
            for z in v['paired_comparisons'][0]['domains'].values():self.assertEqual(z['answer_gain'],36)
            f.records[0]['raw']['replay']['interior']['HOLDOUT']['balanced']['normal'][0,0]+=1
            with self.assertRaises(ValueError):s.analyze(f.traces,f.records,f.states,f.data,f.cx)
    def test_32_analysis_pairing_and_state_tamper(self):
        for kind in ('state','pair'):
            f=scientific_fixture()
            if kind=='state':f.records[0]['state_sha256']='0'*64
            else:f.traces[1]['training_input_sha256']='changed'
            with patch.object(s,'previous',return_value=f.p),patch.object(s,'check_trace'),self.assertRaises(ValueError):
                s.analyze(f.traces,f.records,f.states,f.data,f.cx)
    def test_33_checkpoint_bundle_schema_and_identities(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'states';v=dict(schema='fold-c338-trained-models-v1',identities=[list(z) for z in s.identities()],states=[{}]*10)
            torch.save(v,path);self.assertEqual(len(s.load_states(path)),10);v['identities'].reverse();torch.save(v,path)
            with self.assertRaises(ValueError):s.load_states(path)
    def test_34_training_orchestration_finishes_all_models_before_eval(self):
        env=self.env;calls=[];p=copy.copy(env.p);p.load_data=lambda *a:(env.data,{},{});p.prepared=lambda *a:(env.tables,env.y)
        p.readouts=lambda:NS(measure=lambda *a:(calls.append('eval') or ({},{})))
        def train(seed,arm,model,*args):calls.append('train');return {},copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'previous',return_value=p),patch.object(s,'make_model',side_effect=lambda *a:Toy()), \
             patch.object(s,'train_one',side_effect=train),patch.object(s,'analyze',return_value=([],summary_fixture(0))),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp);s.run_training(out,out,(None,),ROOT,{},e.read)
            self.assertEqual(calls,['train']*10+['eval']*20);self.assertEqual(set(f.name for f in out.iterdir()),set(s.OUTPUTS))
    def test_35_saved_reconstruction_dispatch_and_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);torch.save({'schema':'fold-c338-evaluations-v1','records':[]},out/'evaluations.pt')
            e.save(out/'training-traces.json',[])
            for name,value in (('experiment-plan.json',s.manifest()),('measurements.json',[]),('validation-summary.json',summary_fixture(0))):e.save(out/name,value)
            with patch.object(s,'previous',return_value=NS(load_data=lambda *a:({}, {}, {}))),patch.object(s,'load_states',return_value=[]),patch.object(s,'analyze',return_value=([],summary_fixture(0))):
                s.semantic_recheck(out,out,(),e.read);(out/'measurements.json').write_bytes(b'{}')
                with self.assertRaises(ValueError):s.semantic_recheck(out,out,(),e.read)
    def test_36_parent_contract_complete_maps_and_semantics(self):
        e.parent_contract(*parent_fixture())
        for target,k,v in ((0,'status','FAIL'),(0,'capability_gate_applicable',True),(1,'input_count',4360),(1,'source_count',877),(1,'final_reference_rechecks',4826)):
            args=parent_fixture();args[target][k]=v
            with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_37_all457parent_module_proofs_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);items=[]
            for i in range(227):
                a=folder/f'module-{i:03d}.json';b=folder/f'module-{i:03d}.log';a.write_bytes(b'{}');b.write_bytes(b'fixture')
                items.append(dict(index=i,receipt_sha256=e.sha(a),log_sha256=e.sha(b)))
            for name,value in (('regression-plan.json',{}),('regression-result.json',{}),('regression-evidence.json',{'modules':items})):e.save(folder/name,value)
            bound=dict(tests=6122,modules=227,plan_sha256=e.sha(folder/'regression-plan.json'),evidence_sha256=e.sha(folder/'regression-evidence.json'),result_sha256=e.sha(folder/'regression-result.json'))
            self.assertEqual(len(e.parent_test_files(folder,{'regression_isolation':bound},e.sha)),457)
            (folder/'module-226.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,{'regression_isolation':bound},e.sha)
    def test_38_actual_snapshot_complete5296_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True);pins={};inputs={};tree={}
            for i in range(4827):
                name=f'old/{i}.py' if i<883 else f'data/{i}.bin';path=root/name;path.parent.mkdir(exist_ok=True);raw=str(i).encode();path.write_bytes(raw)
                inputs[e.canonical(path)]=e.sha(path)
                if i<883:pins[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();tree[name]=pins[name]
            for name in s.OWN:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);raw=name.encode();path.write_bytes(raw);tree[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            names=('audit-plan.json','answer-support.json','source-reconciliation.json','validation-summary.json')
            for n in names:(out/n).write_bytes(b'fixture')
            proofs={}
            for i in range(457):path=out.parent/f'proof-{i}';path.write_bytes(b'fixture');proofs[e.canonical(path)]=e.sha(path)
            e.save(out/'summary.json',{'artifacts':[]});e.save(out.parent/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation={}))
            def ancestor(root,prior,h):
                for name,wanted in inputs.items():self.assertEqual(h(name),wanted)
                return {},{},pins,inputs
            h=dict(parent=NS(spec=lambda:NS(OUTPUTS=names),snapshot=ancestor,build_plan=lambda *a:{},verify_tests=lambda *a:{}),prior={},recovery=None,
                legacy=NS(tree_blobs=lambda root:tree,descriptors=lambda out,items,names,h:{e.canonical(out/n):h(out/n) for n in names}))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(out.parent/'execution-envelope.json')), \
                 patch.object(e,'parent_contract'),patch.object(e,'parent_test_files',return_value=proofs):
                _,_,p,v=e.snapshot(root,h,e.sha);self.assertEqual((len(p),len(v)),(889,5296));self.assertEqual(len(inputs),4827)
    def test_39_exact_six_argument_C337_parent_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);par=root/e.PARENT_FOLDER/'science';old=root/'c336/science';src=root/'c335/science';data=root/'c329/science'
            for folder in (par,old,src,data):folder.mkdir(parents=True)
            for folder,names in ((par,('audit-plan.json',)),(old,('summary.json','query-order-quads.json')),(src,('evaluations.pt',)),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                for n in names:(folder/n).write_bytes(b'{}')
            (old/'summary.json').write_bytes(s.blob({'validation_summary':{'parent':'fixture'}}))
            inputs={e.canonical(f):e.sha(f) for folder in (par,old,src,data) for f in folder.iterdir()};saved={'child':'fixture'}
            ps=NS(OUTPUTS=('audit-plan.json',),semantic_recheck=Mock(return_value=saved))
            h=dict(parent=NS(spec=lambda:ps,PARENT_FOLDER='c336',PARENT_SUMMARY=e.sha(old/'summary.json')),
                prior={'parent':NS(PARENT_FOLDER='c335')},c330=NS(PARENT_FOLDER='c329'))
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda v:None)))
            cx=(None,None,NS(new_prompts=lambda v:{},check_prompts=lambda *a:None),None,None,x)
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            p=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {}, {}))
            with patch.object(s,'previous',return_value=p):
                self.assertEqual(e.parent_semantics(root,h,{'validation_summary':saved},inputs),(data,cx))
                ps.semantic_recheck.assert_called_once_with(par,old,src,data,{'parent':'fixture'},e.read)
                del inputs[e.canonical(src/'evaluations.pt')]
                with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':saved},inputs)
    def test_40_parent_helper_pins_before_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in (e.P_PATH,e.S_PATH):p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
            prior={k:object() for k in ('parent','prior','recovery','c330','runtime','legacy','locks')}
            parent=NS(spec=lambda:NS(validate_seal=Mock()),helpers=Mock(return_value=prior))
            with patch.object(e,'git',side_effect=[e.P_BLOB,e.S_BLOB]),patch.object(e,'source_bytes') as check, \
                 patch.object(e.importlib.util,'spec_from_file_location',return_value=NS(loader=NS(exec_module=lambda m:None))), \
                 patch.object(e.importlib.util,'module_from_spec',return_value=parent):
                self.assertIs(e.helpers(root)['prior'],prior);self.assertEqual(check.call_count,2)
    def test_41_actual_loader_plan_and_bad_inventory(self):
        plan,digest=plan_fixture();r=fake_recovery();h=dict(parent=NS(build_plan=lambda *a:{'groups':plan['groups'][:-1]}),prior={},recovery=r)
        with patch.object(e,'BASE_IDS_SHA',digest):
            got=e.build_plan(ROOT,HEAD,h);self.assertEqual(len(got['groups']),228);self.assertEqual(len(got['groups'][-1]['test_ids']),48)
            for kind in ('drop','duplicate','order'):
                v=copy.deepcopy(plan)
                if kind=='drop':v['groups'].pop()
                elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
                else:v['groups'][0]['test_ids'].reverse()
                with self.assertRaises(ValueError):e.validate_plan(v,HEAD,r)
    def test_42_collector_and_fresh_verifier_use_same_ABI(self):
        plan,digest=plan_fixture();r=fake_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:proof(folder,plan,i,h));v=e.verify_tests(folder,HEAD,plan,r)
            self.assertEqual(v['tests'],6170);self.assertEqual(r.validate_module_evidence.call_count,456)
            (folder/'module-227.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_43_module_child_delegates_exact_ids(self):
        plan,digest=plan_fixture();r=fake_recovery();g=plan['groups'][0];r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'guard'),patch.object(e,'helpers',return_value={'recovery':r}),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
    def test_44_worker_capacity_and_valid_negative_fresh_verifier(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()),self.context():
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);pins={f'p{i}':'a' for i in range(889)};inputs={f'i{i}':'b' for i in range(5296)};calls=[]
            value=summary_fixture(0)
            class Cache:
                entries={};stats={'final_reference_rechecks':5296};sha=staticmethod(e.sha)
                def __init__(self,reference,lease_factory,*,progress,max_files):e.require(type(max_files) is int and max_files==s.INPUT_COUNT==len(inputs),'exact capacity')
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            h=dict(runtime=NS(native_runtime=lambda:(NS(__version__='fixture'),NS(__version__='fixture'))),
                locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None),
                legacy=NS(descriptors=lambda out,items,*a:e.require(items==e.artifacts(out),'artifacts')),recovery=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            p=NS(source=lambda:NS(base=lambda:NS(check_dependencies=lambda *a:None,peak_rss=lambda:1)),contrast_check=check_contrast)
            def tests(*a):calls.append('tests');e.save(folder/'regression-result.json',e.receipt(HEAD,6170))
            def train(out,*a):
                calls.append('train')
                for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
                return value
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h),patch.object(e,'snapshot',return_value=({'validation_summary':{}},{},pins,inputs)), \
                 patch.object(e,'parent_semantics',return_value=(root,cx)),patch.object(e,'run_logged',side_effect=tests),patch.object(e,'build_plan',return_value={}), \
                 patch.object(e,'verify_tests',return_value=dict(tests=6170,modules=228)),patch.object(s,'run_training',side_effect=train), \
                 patch.object(s,'native_preflight',side_effect=lambda *a:calls.append('pre')),patch.object(s,'semantic_recheck',return_value=value),patch.object(s,'previous',return_value=p):
                e.scientific_worker(root,folder,HEAD);e.verify_outputs(root,folder,HEAD);self.assertEqual(calls,['pre','tests','train','final','release'])
                path=folder/'science/summary.json';v=e.read(path);self.assertEqual(v['status'],'FAIL');self.assertTrue(v['scientific_execution_valid'])
                v['status']='PASS';path.write_bytes(s.blob(v))
                with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
    def test_45_failed_regression_blocks_training(self):
        training=Mock();pre=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(pre,Mock(side_effect=ValueError('fixture')),training,Mock(),Mock())
        pre.assert_called_once();training.assert_not_called()
    def test_46_git_JSON_CRLF_and_ACTIVE_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C338 fixture'),('config','user.email','c338@example.invalid')]:subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();(root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC338 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            e.guard(root,e.git(root,'rev-parse','HEAD'))
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            path=root/'j';e.save(path,{'名前':'甲乙'});self.assertEqual(e.read(path),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(path,{})
            for value in ('{"a":1,"a":2}','NaN'):
                path.write_text(value,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(path)
            raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
            for b in (raw,raw.replace(b'\n',b'\r\n')):path.write_bytes(b);e.source_bytes(path,oid)
            path.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.source_bytes(path,oid)
        self.assertFalse(e.active('## Formal state\nC337 ACTIVE / NOT YET JUDGED\n'))
    def test_47_real_process_and_CLI_no_retry(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'x.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
        proc=subprocess.run([sys.executable,str(ROOT/'tools/c338_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(proc.returncode,0);self.assertIn('invalid choice',proc.stderr)
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as run,contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,1);self.assertIn('run_execution_valid = false',output.getvalue())
    def test_48_launcher_preflight_and_bound_output_mutation(self):
        text=(ROOT/'tools/invoke_c338.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C338',text);self.assertIn('c338_execution.py',(ROOT/'tools/run_c338.ps1').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
            def change():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,change)


if __name__=='__main__':unittest.main()
