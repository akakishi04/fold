"""C334 software tests. Synthetic scorers/checkpoints/proofs are not FOLD results."""
from __future__ import annotations
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
from fold_lm.v05_benchmarks import model_c334_frozen_policy_crossover as s

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c334_tests_executor', ROOT/'tools/c334_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def same(a, b):
    e.require(a.shape == b.shape and a.dtype == b.dtype and bool(torch.isfinite(a).all()) and bool(torch.isfinite(b).all()), 'finite logits')
    error = float((a-b).abs().max())
    e.require(error <= 1e-9 and torch.equal(a.argmax(-1), b.argmax(-1)), 'control logits/argmax')
    return error


def raw(marker):
    def views():
        return {v:torch.zeros((2,256),dtype=torch.float64) for v in ('normal','evidence_blind','query_blind')}
    v = dict(original={str(n):{sp:{p:views() for p in (('repeat',) if n==1 else ('repeat','shared_prefix','shared_suffix'))}
                              for sp in ('TRAIN','HOLDOUT')} for n in range(1,7)},
             interior={sp:{p:views() for p in ('u_dominant','balanced','v_dominant')} for sp in ('TRAIN','HOLDOUT')})
    # A synthetic scorer tag, not a real FOLD prediction/target.
    v['original']['2']['TRAIN']['repeat']['normal'][:,255] = marker
    return v


def tag(v):
    return int(v['original']['2']['TRAIN']['repeat']['normal'][0,255])


def correct(marker, domain):
    i, rest = divmod(marker,100); train, infer = divmod(rest,10)
    if domain in ('original2','original3','original4'):
        return 288
    if domain == 'original6':
        return 276+i+2*train+infer*(1-3*train)
    if domain == 'original5':
        return 288-2*train-infer
    return 288-(5 if i==3 and train else 0)-infer


def contrast(a, b, domain):
    x, y = correct(a,domain), correct(b,domain); gain = y-x
    return dict(answers=288,query_pairs=144,control_correct=x,candidate_correct=y,
        control_both_correct=x-144,candidate_both_correct=y-144,answer_gain=gain,query_pair_gain=gain,
        rescued=max(gain,0),regressed=max(-gain,0),pair_rescued=max(gain,0),pair_regressed=max(-gain,0))


def compare(a, b, *args):
    return dict(original_by_length={str(n):contrast(tag(a),tag(b),'original'+str(n)) for n in range(2,7)},
                interior=contrast(tag(a),tag(b),'interior4'))


def flags(marker):
    passed = {d:correct(marker,d)==288 for d in s.DOMAINS}
    return dict(original_pass={str(n):passed['original'+str(n)] for n in range(2,7)},
        interior_pass=passed['interior4'],retention_pass=all(passed[d] for d in s.DOMAINS[:-1]),
        failures={d:dict(local=int(not passed[d]),order=int(not passed[d])) for d in s.DOMAINS})


def contrast_check(z):
    e.require(set(z)=={'answers','query_pairs','control_correct','candidate_correct','control_both_correct','candidate_both_correct',
                      'answer_gain','query_pair_gain','rescued','regressed','pair_rescued','pair_regressed'}, 'contrast fields')
    e.require(all(type(v) is int for v in z.values()) and z['answers']==288 and z['query_pairs']==144, 'contrast types')
    e.require(z['candidate_correct']-z['control_correct']==z['answer_gain']==z['rescued']-z['regressed'], 'answer contrast')
    e.require(z['candidate_both_correct']-z['control_both_correct']==z['query_pair_gain']==z['pair_rescued']-z['pair_regressed'], 'pair contrast')


def invariant(a, b, data):
    count = 0
    def walk(x,y):
        nonlocal count
        for k,v in x.items():
            if isinstance(v,dict): walk(v,y[k])
            elif k=='query_blind': same(v,y[k]); count+=1
    walk(a,b); e.require(count==38,'query blind coverage')
    for split in ('TRAIN','HOLDOUT'):
        for view in ('normal','evidence_blind','query_blind'):
            same(a['original']['1'][split]['repeat'][view],b['original']['1'][split]['repeat'][view])


def fingerprint(state):
    return hashlib.sha256(b''.join(k.encode()+v.detach().numpy().tobytes() for k,v in sorted(state.items()))).hexdigest()


class Tiny(torch.nn.Module):
    def __init__(self, marker):
        super().__init__(); self.tag = torch.nn.Parameter(torch.tensor([marker],dtype=torch.float64))
        self.read = torch.nn.Module(); self.read.output = torch.nn.Linear(1,256,bias=False,dtype=torch.float64)
        with torch.no_grad(): self.read.output.weight.fill_(.02)
        self.mode = 'native_before'; self.stats = None
    def forward(self,tokens,tasks):
        if self.stats is not None:
            self.stats['calls']+=1;self.stats['query_calls']+=2;self.stats['rows']+=len(tokens)
            self.stats['grad_calls']+=int(torch.is_grad_enabled())
        x = torch.ones((len(tokens),1),dtype=torch.float64)
        if self.mode=='first_mean' and tokens[0,0]==6: x*=1.5
        return self.read.output(x)


@contextlib.contextmanager
def toy_readout(model, wide, mode):
    old,oldstats = model.mode,model.stats; value = dict(calls=0,query_calls=0,rows=0,grad_calls=0)
    model.mode=mode;model.stats=value
    try: yield value
    finally: model.mode=old;model.stats=oldstats


def fixture():
    """Full ten-state inventory with explicit synthetic legacy scorer callbacks."""
    prior,records,seedflags,states = [],[],[],[]
    for i,seed in enumerate(s.SEEDS):
        for t,arm in enumerate(s.ARMS):
            base_marker=100*i+10*t; model=Tiny(base_marker); state=copy.deepcopy(model.state_dict()); states.append(state)
            ownmarker=base_marker+t; original=raw(ownmarker); policies={m:s.policy(arm,m) for m in s.MODES}
            prior.append(dict(seed=seed,arm=arm,state_sha256=fingerprint(state),readout_mode='native_before' if arm=='native' else 'first_mean',
                raw={m:copy.deepcopy(original) for m in ('evaluation','replay')},receipts={m:dict(s.RECEIPT) for m in ('evaluation','replay')}))
            records.append(dict(seed=seed,arm=arm,state_sha256=fingerprint(state),policies=policies,
                raw={m:raw(base_marker+s.ARMS.index(policies[m])) for m in s.MODES},receipts={m:dict(s.RECEIPT) for m in s.MODES}))
            seedflags.append(dict(seed=seed,arm=arm,**flags(ownmarker)))
    pairs=[dict(seed=seed,**compare(prior[2*i]['raw']['evaluation'],prior[2*i+1]['raw']['evaluation'])) for i,seed in enumerate(s.SEEDS)]
    saved=dict(candidate_gate=False,seed_results=seedflags,paired_comparisons=pairs)
    data={sp:[{'language':'en'},{'language':'ja'}] for sp in ('TRAIN','HOLDOUT')}
    old={str(n):{'TRAIN':{'repeat':[{'views':{'normal':'6' if n==6 else '1','query_blind':'1'}}]}} for n in (1,6)}
    base=NS(validate_raw=Mock(),check_dependencies=Mock(),peak_rss=lambda:1)
    q=NS(same=same,invariant_views=invariant,summarize_mode=lambda v,*a:({},flags(tag(v))),compare=Mock(side_effect=compare),readout=toy_readout)
    calls=[]
    def measure(model,mode,*args):
        e.require(not model.training and all(not v.requires_grad for v in model.parameters()),'eval/frozen')
        calls.append((int(model.tag.item()),mode))
        return raw(int(model.tag.item())+int(mode=='first_mean')),dict(s.RECEIPT)
    q.measure=Mock(side_effect=measure)
    def policy_mode(arm):
        e.require(arm in s.ARMS,'arm');return 'native_before' if arm=='native' else 'first_mean'
    p=NS(readouts=lambda:q,source=lambda:NS(base=lambda:base),policy_mode=policy_mode,state_hash=fingerprint,
         make_model=Mock(side_effect=lambda seed,x:Tiny(100*(seed-s.SEEDS[0]))),load_states=Mock(return_value=states),
         load_data=Mock(return_value=(data,old,{})),contrast_check=contrast_check,
         check_summary=Mock(side_effect=lambda v:e.require(v['candidate_gate'] is False and len(v['seed_results'])==10,'synthetic parent')))
    x=NS(wide=NS(prefix_tensor=lambda text:torch.full((64,),int(text),dtype=torch.int64)),
         c=NS(p267=NS(check_logits=lambda a,n:e.require(a.shape==(n,256) and bool(torch.isfinite(a).all()),'preflight logits'))))
    return NS(prior=prior,archive=dict(schema='fold-c334-crossover-v1',records=records),saved=saved,data=data,p=p,q=q,base=base,cx=(None,None,None,None,None,x),calls=calls)


def fake_recovery():
    def flatten(values):
        for v in values:
            if isinstance(v,unittest.TestSuite): yield from flatten(v)
            else: yield v
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==i
                  and row['plan_sha256']==ph and row['module']==g['module'],'module ABI')
        e.require(row['result']['success_ids']==g['test_ids'],'success IDs')
        e.require(launcher in (row['pid'],row['parent_pid']),'PID relationship')
        return 'direct' if launcher==row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',validate_module_evidence=Mock(side_effect=validate),
              allowed_module=lambda x:type(x) is str and (re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',x) is not None or x=='tests_tools.test_c324_locked_hash_r4'))


def fake_plan():
    groups=[];n,rem=divmod(5978,223)
    for i in range(223):
        name='tests_tools.test_c324_locked_hash_r4' if i==0 else f'tests_lm.fixture_{i:03d}'
        groups.append(dict(module=name,test_ids=[name+f'.Fixture.test_{j:03d}' for j in range(n+(i<rem))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C334Tests.test_{i:02d}' for i in range(32)]))
    ids=[t for g in groups for t in g['test_ids']]
    return dict(schema='fold-c334-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-32])


def fake_module(folder,plan,i,ph):
    g=plan['groups'][i];pid,parent=20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,plan_sha256=ph,module=g['module'],
        pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_text('explicit synthetic collaborator proof',encoding='utf-8')
    return pid if i%2==0 else parent


def proofs(folder):
    rows=[]
    for i in range(223):
        (folder/f'module-{i:03d}.json').write_bytes(b'{}');(folder/f'module-{i:03d}.log').write_bytes(b'fixture')
        rows.append(dict(index=i,receipt_sha256=e.sha(folder/f'module-{i:03d}.json'),log_sha256=e.sha(folder/f'module-{i:03d}.log')))
    e.save(folder/'regression-plan.json',{});e.save(folder/'regression-result.json',{})
    e.save(folder/'regression-evidence.json',{'modules':rows})
    return dict(tests=5978,modules=223,plan_sha256=e.sha(folder/'regression-plan.json'),result_sha256=e.sha(folder/'regression-result.json'),evidence_sha256=e.sha(folder/'regression-evidence.json'))


class C334Tests(unittest.TestCase):
    def test_01_manifest_and_mutation(self):
        s.validate_seal()
        with patch.object(s,'ARMS',s.ARMS[::-1]),self.assertRaises(ValueError):s.validate_seal()
    def test_02_actual_loader_and_accounting(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),32)
        self.assertEqual(s.FULL_TESTS,5978+32);self.assertEqual(s.INPUT_COUNT,2969+455+6)
        self.assertEqual(s.SOURCE_COUNT,859+6);self.assertEqual(s.WORK['model_forward_calls'],10*3*171)
    def test_03_both_training_arm_policy_sequences(self):
        self.assertEqual([s.policy('native',m) for m in s.MODES],['native','first_mean','native'])
        self.assertEqual([s.policy('first_mean',m) for m in s.MODES],['first_mean','native','first_mean'])
        for arm,mode in [('selected','cross'),('native','best'),(True,'cross')]:
            with self.assertRaises(ValueError):s.policy(arm,mode)
    def test_04_raw_tree_all114leaves(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            a=raw(1);self.assertEqual(s.same_tree(a,copy.deepcopy(a)),0)
            del a['interior']['TRAIN']['balanced']
            with self.assertRaises(ValueError):s.same_tree(a,a)
    def test_05_tiny_logit_drift_does_not_allow_argmax_flip(self):
        f=fixture();a=raw(1);b=copy.deepcopy(a)
        a['interior']['TRAIN']['balanced']['normal'][:,1]=1e-12
        b['interior']['TRAIN']['balanced']['normal'][:,0]=1e-12
        with patch.object(s,'trained',return_value=f.p),self.assertRaisesRegex(ValueError,'argmax'):s.same_tree(a,b)
    def test_06_nonfinite_and_wrong_dtype_rejected(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            for bad in (torch.full((2,256),float('nan'),dtype=torch.float64),torch.zeros((2,256),dtype=torch.float32)):
                a=raw(1);a['interior']['TRAIN']['balanced']['normal']=bad
                with self.assertRaises(ValueError):s.same_tree(a,a)
    def test_07_actual_C332_archive_loader(self):
        f=fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'trained',return_value=f.p):
            folder=Path(tmp);torch.save(dict(schema='fold-c332-evaluations-v1',records=f.prior),folder/'evaluations.pt')
            self.assertEqual(len(s.load_prior(folder)),10)
            torch.save(dict(schema='fold-c329-evaluations-v1',records=f.prior),folder/'evaluations.pt')
            with self.assertRaises(ValueError):s.load_prior(folder)
    def test_08_prior_identity_and_boolean_receipts_rejected(self):
        for kind in ('policy','order','count'):
            f=fixture()
            if kind=='policy':f.prior[1]['readout_mode']='native_before'
            elif kind=='order':f.prior.reverse()
            else:f.prior[0]['receipts']['evaluation']['grad_calls']=False
            with tempfile.TemporaryDirectory() as tmp,patch.object(s,'trained',return_value=f.p):
                path=Path(tmp);torch.save(dict(schema='fold-c332-evaluations-v1',records=f.prior),path/'evaluations.pt')
                with self.assertRaises(ValueError):s.load_prior(path)
    def test_09_complete_analysis_factorial_sign(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            metrics,v=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
            self.assertEqual((len(metrics),len(v['effects']),len(v['factorial'])),(10,10,30))
            row=next(r for r in v['factorial'] if (r['seed'],r['domain'])==(332001,'original6'))['answers']
            self.assertEqual([row[k] for k in ('native_native','native_first_mean','first_mean_native','first_mean_first_mean')],[276,277,278,276])
            self.assertEqual(row['interaction'],-3)
    def test_10_diagonal_cannot_rewrite_parent_counts(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            _,v=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
            changed=copy.deepcopy(v['parent_validation_summary']);changed['paired_comparisons'][0]['original_by_length']['6']['candidate_correct']+=1
            with self.assertRaisesRegex(ValueError,'diagonal'):s.factorial(v['effects'],changed)
    def test_11_summary_rejects_missing_states_work_and_false_parent(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            _,v=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
            for kind in ('state','work','parent'):
                z=copy.deepcopy(v)
                if kind=='state':z['effects'].pop()
                elif kind=='work':z['model_forward_calls']-=1
                else:z['parent_validation_summary']['candidate_gate']=True
                with self.assertRaises(ValueError):s.check_summary(z)
    def test_12_flags_and_factorial_tamper(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            _,v=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
            for kind in ('flag','factorial'):
                z=copy.deepcopy(v)
                if kind=='flag':z['effects'][0]['own']['failures']['original6']['local']=0
                else:z['factorial'][0]['answers']['interaction']+=1
                with self.assertRaises(ValueError):s.check_summary(z)
    def test_13_no_input_mutation_and_all_raw_validators(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p):
            before=s.digest(f.saved);a=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
            b=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
            self.assertEqual(s.blob(a),s.blob(b));self.assertEqual(s.digest(f.saved),before)
            self.assertEqual(f.base.validate_raw.call_count,100);self.assertEqual(f.q.compare.call_count,30)
    def test_14_wrong_cross_policy_or_work_receipt_fails(self):
        for kind in ('policy','receipt','state'):
            f=fixture();r=f.archive['records'][1]
            if kind=='policy':r['policies']['cross']='first_mean'
            elif kind=='receipt':r['receipts']['cross']['calls']=170
            else:r['state_sha256']='f'*64
            with patch.object(s,'trained',return_value=f.p),self.assertRaises(ValueError):s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
    def test_15_own_before_and_own_after_must_replay(self):
        for mode in ('own_before','own_after'):
            f=fixture();f.archive['records'][1]['raw'][mode]['interior']['TRAIN']['balanced']['normal'][0,1]=1.
            with patch.object(s,'trained',return_value=f.p),self.assertRaises(ValueError):s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
    def test_16_query_blind_same_weight_control(self):
        f=fixture();f.archive['records'][1]['raw']['cross']['interior']['TRAIN']['balanced']['query_blind'][0,1]=1.
        with patch.object(s,'trained',return_value=f.p),self.assertRaises(ValueError):s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
    def test_17_full_paired_diagonal_includes_individual_rescues(self):
        f=fixture();z=f.saved['paired_comparisons'][0]['original_by_length']['6'];z['rescued']+=1;z['regressed']+=1
        with patch.object(s,'trained',return_value=f.p),self.assertRaisesRegex(ValueError,'paired diagonal'):s.analyze(f.archive,f.prior,f.data,f.cx,f.saved)
    def test_18_production_probe_writer_and_saved_reconstruction(self):
        f=fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'trained',return_value=f.p),contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);parent=root/'source';out=root/'out';parent.mkdir();out.mkdir()
            torch.save(dict(schema='fold-c332-evaluations-v1',records=f.prior),parent/'evaluations.pt')
            value=s.run_probe(out,parent,parent,f.cx,root,{},f.saved,e.read)
            self.assertEqual(len(f.calls),30);self.assertEqual(f.p.make_model.call_count,10)
            for i,arm in enumerate(a for _,a in s.identities()):
                self.assertEqual([m for _,m in f.calls[3*i:3*i+3]],[f.p.policy_mode(s.policy(arm,m)) for m in s.MODES])
            self.assertEqual(s.blob(s.semantic_recheck(out,parent,parent,f.cx,f.saved,e.read)),s.blob(value))
            self.assertEqual(set(p.name for p in out.iterdir()),set(s.OUTPUTS))
    def test_19_probe_detects_weight_mutation_before_next_mode(self):
        f=fixture();original=f.q.measure.side_effect
        def mutate(model,*args):
            result=original(model,*args)
            with torch.no_grad():model.tag.add_(1)
            return result
        f.q.measure.side_effect=mutate
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'trained',return_value=f.p),contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);torch.save(dict(schema='fold-c332-evaluations-v1',records=f.prior),root/'evaluations.pt')
            with self.assertRaisesRegex(ValueError,'mutated'):s.run_probe(root,root,root,f.cx,root,{},f.saved,e.read)
            self.assertEqual(f.q.measure.call_count,1)
    def test_20_saved_semantics_rejects_resealed_JSON(self):
        f=fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'trained',return_value=f.p):
            root=Path(tmp);parent=root/'p';out=root/'o';parent.mkdir();out.mkdir()
            torch.save(dict(schema='fold-c332-evaluations-v1',records=f.prior),parent/'evaluations.pt')
            metrics,v=s.analyze(f.archive,f.prior,f.data,f.cx,f.saved);torch.save(f.archive,out/'evaluations.pt')
            for n,x in [('diagnostic-plan.json',s.manifest()),('measurements.json',metrics),('validation-summary.json',v)]:e.save(out/n,x)
            v['factorial'][0]['answers']['interaction']+=1;(out/'validation-summary.json').write_bytes(s.blob(v))
            with self.assertRaisesRegex(ValueError,'reconstruction'):s.semantic_recheck(out,parent,parent,f.cx,f.saved,e.read)
    def test_21_actual_preflight_order_with_Torch_toy(self):
        f=fixture()
        with patch.object(s,'trained',return_value=f.p),contextlib.redirect_stdout(io.StringIO()) as log:
            s.native_preflight(ROOT,f.cx,ROOT,{},e.read)
            self.assertIn('forwards=28',log.getvalue());self.assertEqual(f.p.make_model.call_count,1)
    def test_22_exact_nested_helper_bridge(self):
        objects=[object() for _ in range(8)];parent,c332,c331,r,c330,runtime,legacy,locks=objects
        inherited=(c332,(c331,(r,c330,runtime,legacy,locks)));h=e.bridge(parent,inherited)
        self.assertIs(h['recovery'],r);self.assertIs(h['c330'],c330);self.assertIs(h['runtime'],runtime)
        with self.assertRaises(ValueError):e.bridge(parent,(c331,(r,c330,runtime,legacy,locks)))
    def test_23_parent_contract_rejects_smaller_maps_wrong_verdict(self):
        ps=NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='m',WORK={'x':0})
        parent=NS(spec=lambda:ps,PARENT_SUMMARY='s',PARENT_ENVELOPE='v')
        pins={e.P_PATH:e.P_BLOB,**{f'p{i}':'a' for i in range(858)}};inputs={f'i{i}':'b' for i in range(2969)}
        r=dict(schema='fold-c333-diagnostic-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='PASS',diagnostic_execution_valid=True,
            capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,manifest_sha256='m',source_blobs=pins,input_sha256=inputs,
            validation_summary={'parent_validation_summary':{'candidate_gate':False}})
        v=dict(schema='fold-c333-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='PASS',manifest_sha256='m',scientific_work={'x':0},
            scientific_summary_sha256=e.PARENT_SUMMARY,source_count=859,input_count=2969,source_blobs=pins,input_sha256=inputs,parent_summary_sha256='s',parent_envelope_sha256='v',
            immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
            final_reference_rechecks=2969,hash_stats={'final_reference_rechecks':2969},regression=e.receipt(e.PARENT_HEAD,5978))
        e.parent_contract(r,v,parent)
        for key,value in [('source_count',853),('input_count',2508),('scientific_status','FAIL'),('final_reference_rechecks',2968)]:
            bad=copy.deepcopy(v);bad[key]=value
            with self.assertRaises(ValueError):e.parent_contract(r,bad,parent)
    def test_24_snapshot_all449proofs_and_full_child_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pins,inputs,tree={},{},{}
            for i in range(859):
                name=f'ancestor/{i}.py';p=root/name;p.parent.mkdir(parents=True,exist_ok=True);v=f'# fixture{i}\n'.encode();p.write_bytes(v)
                pins[name]=hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest();tree[name]=pins[name];inputs[e.canonical(p)]=e.sha(p)
            inputs.update({f'synthetic{i}':'a'*64 for i in range(2969-859)})
            for name in s.OWN:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);v=name.encode();p.write_bytes(v);tree[name]=hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
            folder=root/e.PARENT_FOLDER;out=folder/'science';out.mkdir(parents=True)
            for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
            evidence=proofs(folder);e.save(out/'summary.json',{'artifacts':[]})
            e.save(folder/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation=evidence))
            p=NS(spec=lambda:NS(OUTPUTS=s.OUTPUTS),snapshot=Mock(return_value=({}, {},pins,inputs)),build_plan=Mock(return_value={}),verify_tests=Mock(return_value=evidence))
            legacy=NS(tree_blobs=lambda root:tree,descriptors=lambda out,items,names,h:{e.canonical(out/n):h(out/n) for n in names})
            h=dict(parent=p,inherited=object(),recovery=object(),legacy=legacy)
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(folder/'execution-envelope.json')),patch.object(e,'parent_contract'):
                _,_,a,b=e.snapshot(root,h,e.sha);self.assertEqual((len(a),len(b)),(865,3430))
                self.assertEqual(p.verify_tests.call_args.args,(folder,e.PARENT_HEAD,{},h['recovery']))
                (folder/'module-222.log').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'proof bytes'):e.snapshot(root,h,e.sha)
    def test_25_immediate_C333_JSON_dispatch_and_protected_data(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);state=root/'c332/science';data=root/'c329/science';state.mkdir(parents=True);data.mkdir(parents=True)
            for p,names in ((state,('evaluations.pt','trained-models.pt','measurements.json','validation-summary.json')),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                for n in names:(p/n).write_bytes(b'{}')
            inputs={e.canonical(p):e.sha(p) for folder in (state,data) for p in folder.iterdir()}
            q=NS(semantic_recheck=Mock(return_value={'saved':True}));h=dict(parent=NS(spec=lambda:q,PARENT_FOLDER='c332'),c330=NS(PARENT_FOLDER='c329'))
            x=NS(c=NS(p267=NS(validate_data=lambda v:None)),guarded=NS(no_neural=contextlib.nullcontext))
            cx=(None,None,NS(new_prompts=lambda d:{},check_prompts=lambda *a:None),None,None,x)
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            trained=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {},{}))
            with patch.object(s,'trained',return_value=trained):
                self.assertEqual(e.parent_semantics(root,h,{'validation_summary':{'saved':True}},inputs),(state,data,cx))
                q.semantic_recheck.assert_called_once_with(root/e.PARENT_FOLDER/'science',state,e.read)
                del inputs[e.canonical(state/'trained-models.pt')]
                with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':{'saved':True}},inputs)
    def test_26_regression_plan_actual_own_loader_and_mixed_namespace(self):
        plan,digest=fake_plan();r=fake_recovery();h=dict(recovery=r,parent=NS(build_plan=Mock(return_value={'groups':plan['groups'][:-1]})),inherited=object())
        with patch.object(e,'BASE_IDS_SHA',digest):
            actual=e.build_plan(ROOT,HEAD,h);self.assertEqual(len(actual['groups']),224);self.assertEqual(len(actual['groups'][-1]['test_ids']),32)
            for kind in ('drop','duplicate','reorder','namespace'):
                bad=copy.deepcopy(plan)
                if kind=='drop':bad['groups'].pop()
                elif kind=='duplicate':bad['groups'][0]['test_ids'][1]=bad['groups'][0]['test_ids'][0]
                elif kind=='reorder':bad['groups'][0]['test_ids'].reverse()
                else:bad['groups'][0]['module']='invalid.module'
                with self.assertRaises(ValueError):e.validate_plan(bad,HEAD,r)
    def test_27_collector_and_verifier_use_same_accepted_PID_ABI(self):
        plan,digest=fake_plan();r=fake_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:fake_module(folder,plan,i,h))
            self.assertEqual(e.verify_tests(folder,HEAD,plan,r)['tests'],6010);self.assertEqual(r.validate_module_evidence.call_count,448)
            (folder/'module-223.log').write_bytes(b'tampered')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_28_module_child_and_failure_stop_before_diagnosis(self):
        plan,digest=fake_plan();r=fake_recovery();g=plan['groups'][0];r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'helpers',return_value={'recovery':r}),patch.object(e,'guard'),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
            probe=Mock()
            with self.assertRaises(ValueError):e.execute_stages(lambda:None,Mock(side_effect=ValueError('fixture')),probe,Mock(),Mock())
            probe.assert_not_called()
    def test_29_Git_UTF8_source_bytes_and_launcher_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C334 fixture'),('config','user.email','c334@example.invalid')]:subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();p=root/'docs/experiment-ledger-and-handoff.md';p.write_text('## Formal state\nC334 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            head=e.git(root,'rev-parse','HEAD');e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            p.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.guard(root,head)
            x=root/'x';e.save(x,{'名前':'甲乙'});self.assertEqual(e.read(x),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(x,{})
            for text in ('{"a":1,"a":2}','NaN','Infinity'):
                x.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(x)
            rawbytes=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+rawbytes).hexdigest()
            for v in (rawbytes,rawbytes.replace(b'\n',b'\r\n')):x.write_bytes(v);e.source_bytes(x,oid)
        launcher=(ROOT/'tools/invoke_c334.ps1').read_text(encoding='utf-8')
        for term in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(launcher.index(term),launcher.index('$log ='))
        self.assertIn('-ExperimentId C334',launcher)
    def test_30_worker_real_crossover_writer_with_synthetic_infrastructure(self):self.worker_fixture(False)
    def test_31_worker_regression_failure_and_fresh_verifier_flags(self):self.worker_fixture(True)
    def worker_fixture(self,bad):
        f=fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(s,'trained',return_value=f.p),contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/child';folder.mkdir(parents=True);state=root/'source';state.mkdir()
            torch.save(dict(schema='fold-c332-evaluations-v1',records=f.prior),state/'evaluations.pt')
            pins={f'p{i}':'a'*40 for i in range(865)};inputs={f'i{i}':'b'*64 for i in range(3430)};calls=[]
            class Cache:
                entries={};stats={'final_reference_rechecks':3430};sha=staticmethod(e.sha)
                def __init__(self,*a,**k):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            runtime=NS(native_runtime=lambda:(NS(__version__='synthetic'),NS(__version__='synthetic')))
            legacy=NS(descriptors=lambda out,items,names,h:e.require(items==e.artifacts(out),'artifact binding'))
            cx=(*f.cx[:-1],NS(**vars(f.cx[-1]),guarded=NS(no_neural=contextlib.nullcontext)))
            parent={'validation_summary':{'parent_validation_summary':f.saved}}
            def snap(*a):calls.append('snapshot');return parent,{},pins,inputs
            def semantics(*a):calls.append('parent');return state,state,cx
            def regression(*a):
                calls.append('tests')
                if bad:raise ValueError('fixture regression failure')
                e.save(folder/'regression-result.json',e.receipt(HEAD,6010))
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=dict(runtime=runtime,locks=locks,recovery=None,legacy=legacy)),patch.object(e,'snapshot',side_effect=snap),patch.object(e,'parent_semantics',side_effect=semantics),patch.object(e,'run_logged',side_effect=regression),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value={'tests':6010,'modules':224}):
                if bad:
                    with self.assertRaises(ValueError):e.scientific_worker(root,folder,HEAD)
                    self.assertFalse((folder/'science/summary.json').exists());self.assertEqual(f.q.measure.call_count,0)
                else:
                    e.scientific_worker(root,folder,HEAD);self.assertEqual(calls,['snapshot','parent','tests','final','release'])
                    e.verify_outputs(root,folder,HEAD);value=e.read(folder/'science/summary.json')
                    self.assertFalse(value['capability_gate_applicable']);value['capability_gate_applicable']=True
                    (folder/'science/summary.json').write_bytes(s.blob(value))
                    with self.assertRaisesRegex(ValueError,'diagnostic flags'):e.verify_outputs(root,folder,HEAD)
    def test_32_actual_nonzero_process_controller_no_retry_CLI(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'error.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
            with patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as runner:
                with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
                self.assertEqual(runner.call_count,1)
        result=subprocess.run([sys.executable,str(ROOT/'tools/c334_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','invalid'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(result.returncode,0);self.assertIn('invalid choice',result.stderr)


if __name__=='__main__':unittest.main()
