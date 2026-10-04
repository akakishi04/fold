"""C304 contract, integration and synthetic control tests; no capability claims."""
import ast
from collections import Counter,defaultdict
import contextlib
import copy
from dataclasses import dataclass
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import torch
from torch import nn
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c304_length_breadth as b

SUBSETS=((0,1),(0,2),(1,2))


def dataset():
    result={s:[] for s in b.SPLITS}
    for e,v,lang in itertools.product(SUBSETS,itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if v in ((0,2),(1,3),(2,0),(3,1)) else "TRAIN"
        for perm,q in itertools.product((e,e[::-1]),e):
            result[split].append(dict(id=f"{lang}:{e}:{v}:{perm}:{q}",entities=list(e),values=list(v),language=lang,permutation=list(perm),query=q,target=48+v[e.index(q)]))
    return result


def pairs(rows):
    groups={}
    for i,r in enumerate(rows):groups.setdefault((r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"])),[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)
PS=NS(pairs_from_rows=pairs)


def check_logits(z,n):b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")

def validate_data(d):b.require(d==dataset() and b.digest(d)==b.DATA_SHA,"logical data")

def legacy_render(r,profile,view="normal"):
    n=next(n for n,ps in b.LEGACY_PROFILES.items() if profile in ps and (profile!="shared_prefix" or n==2))
    chars=("a","b","c") if r["language"]=="en" else ("甲","乙","丙")
    i,j=r["entities"];u,v=chars[i],chars[j];k=b.LEGACY_PROFILES[n].index(profile)
    names={i:u*n,j:v*n if k==0 else u*(n-1)+v if k==1 else v+u*(n-1)}
    values=dict(zip(r["entities"],r["values"],strict=True))
    return ';'.join(f'{names[x]}={"?" if view=="evidence_blind" else values[x]}' for x in r["permutation"])+ ';'+('?' if view=='query_blind' else names[r['query']])+'='


def load_symbols(path,names,space):
    nodes=ast.parse(path.read_text(encoding="utf-8")).body
    selected=[n for n in nodes if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
    b.require({n.name for n in selected}==set(names),"accepted definition inventory")
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),"exec"),space)


def real_class_factory():
    root=Path(__file__).resolve().parents[1]
    space=dict(__name__=__name__,torch=torch,nn=nn,F=F,dataclass=dataclass,Counter=Counter,req=b.require,require=b.require,
        PAD=256,BOS=257,EOS=258,BYTE_VOCAB_SIZE=259,OUTPUT_BYTE_CLASSES=256,TASK_NEXT=0,TASK_INSTRUCTION=1,ARMS=("token_read","eos_adapter"))
    load_symbols(root/"fold_lm/v05/modules.py",("LearnedCoreConfig","_ResidualMLP","HighPrecisionFixedRoutingCore"),space)
    load_symbols(root/"fold_lm/v05/language_task.py",("LanguageTaskConfig","ShortByteLanguageModel"),space)
    load_symbols(root/"fold_lm/v05_benchmarks/model_c248_residual_token_read.py",("ResidualHead",),space)
    load_symbols(root/"fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py",("MeanFinalDualReadout",),space)
    def new(seed):
        torch.manual_seed(seed)
        return space["ShortByteLanguageModel"](space["LanguageTaskConfig"](max_tokens=48,width=16,modules=2,internal_steps=2)).double().eval()
    return NS(c278=NS(MeanFinalDualReadout=space["MeanFinalDualReadout"]),factory=NS(new_model=new),reader=NS(ResidualHead=space["ResidualHead"]),
        c269=NS(query_span_mask=b.span_mask),base=NS(fingerprint=fingerprint))


def fingerprint(model):return b.digest({k:v.detach().tolist() for k,v in model.state_dict().items()})


def real_scorer():
    root=Path(__file__).resolve().parents[1]
    space=dict(__name__=__name__,torch=torch,F=F,defaultdict=defaultdict,itertools=itertools,require=b.require,SPLITS=b.SPLITS,VIEWS=b.VIEWS,PROFILES=b.LEGACY_PROFILES[3])
    load_symbols(root/"fold_lm/v05_benchmarks/model_c270_frozen_triple_identifiers.py",("score",),space)
    return NS(c270=NS(score=space["score"],render=legacy_render),p267=NS(validate_data=validate_data,check_logits=check_logits,SUBSETS=SUBSETS,render=legacy_render))


def raw_fixture(data,passed=True):
    raw={}
    for s,rows in data.items():
        y=torch.tensor([r['target'] for r in rows]);z=torch.zeros((len(rows),256),dtype=torch.float64);z[torch.arange(len(rows)),y]=5.
        if not passed:z[0,70]=9.
        blind=torch.zeros_like(z);blind[:,70]=5.
        raw[s]={p:dict(normal=z.clone(),evidence_blind=blind.clone(),query_blind=blind.clone()) for p in b.PROFILES}
    return raw


def software_scorers():
    def score(data,raw,p267):
        totals=[]
        for split,rs in data.items():
            y=torch.tensor([r['target'] for r in rs]);n=len(rs)*3
            correct=sum(int((z['normal'].argmax(1)==y).sum()) for z in raw[split].values())
            totals.append(dict(split=split,rows=n,correct=correct,direct_pass=n==correct,final_normal_nll=.1))
        return dict(passed=all(r['direct_pass'] for r in totals),totals=totals)
    diag=NS(normalize_task=lambda scored,*_:scored['totals'],partition=lambda rows:{k:v for k,v in rows[0].items() if k!='split'})
    c=NS(c270=NS(score=score,render=legacy_render),p267=NS(validate_data=validate_data,check_logits=check_logits,render=legacy_render))
    return diag,c


def fixture_records():
    data=dataset();rs=[]
    for seed,arm in b.identities():
        events=b.schedule(seed,arm,data['TRAIN'],PS)
        f=dict(steps=1200,training_rows=57600,optimizer_creations=1,fit_rng=b.FIT_RNG,ce_history=[.1]*1200,schedule_events=events,**b.schedule_stats(events))
        rs.append(dict(seed=seed,arm=arm,parameters=14256,slots=64,initial_sha256='a'*64,final_sha256='b'*64,core_changed=True,checkpoint_roundtrip=True,reload_max_error=0.,fit=f,
            forward_calls=1308,row_presentations=67968,core_forward_calls=5232,replay_forward_calls=108,replay_row_presentations=10368,replay_core_forward_calls=432,
            raw={str(n):raw_fixture(data) for n in b.EVAL_LENGTHS}))
    return rs,data


class Toy(nn.Module):
    def __init__(self):
        super().__init__();self.backbone=nn.Module();self.backbone.core=nn.Linear(4,4,dtype=torch.float64);self.embedding=nn.Embedding(259,4,dtype=torch.float64);self.decoder=nn.Linear(4,256,dtype=torch.float64)
    def forward(self,x,t):
        assert x.shape==(len(x),64) and t.shape==(len(x),)
        z=self.embedding(x[:,0])
        for _ in range(4):z=torch.tanh(self.backbone.core(z))
        return self.decoder(z)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0];cores=[0]
    def mh(m,a,o):calls[0]+=1;calls[1]+=len(a[0])
    def ch(m,a,o):cores[0]+=1
    h=model.register_forward_hook(mh);g=model.backbone.core.register_forward_hook(ch)
    try:yield calls,cores
    finally:h.remove();g.remove()


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'a'*64
    @staticmethod
    def read_json(p):return json.loads(Path(p).read_text(encoding='utf-8'))
    @staticmethod
    def safe_child(root,n):return Path(root)/n
    @staticmethod
    def git(root,*a):
        if a[0]=='rev-parse':return b'ffffffffffffffffffffffffffffffffffffffff\n'
        if a[0]=='branch':return b'feat/sft-target-loss\n'
        return b''


def protection():
    pins=dict(b.PINNED);pins.update({n:'b'*40 for n in b.OWN})
    while len(pins)<670:pins['fixture/'+str(len(pins))]='b'*40
    return pins,{'fixture/input/'+str(i):'a'*64 for i in range(1243)}


def payload(s):
    pins,p=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha='f'*40,status='PASS' if s['candidate_gate'] else 'FAIL',diagnostic_execution_valid=True,source_blobs=pins,input_sha256=p,
        artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False)


class C304Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.records,cls.data=fixture_records();cls.diag,cls.c=software_scorers();cls.prompts=b.prompt_dataset(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.data,PS,cls.diag,cls.c)
        cls.x=torch.zeros((3,3,192,64),dtype=torch.int64);cls.y=torch.tensor([r['target'] for r in cls.data['TRAIN']]);cls.x[:,:,:,0]=cls.y-48
        torch.manual_seed(7);cls.initial=Toy();cls.fits={};cls.models={}
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:
                model=copy.deepcopy(cls.initial);cls.fits[arm]=b.fit(model,cls.data,cls.x,cls.y,b.SEEDS[0],arm,PS);cls.models[arm]=model
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
    def test_02_bad_seal(self):
        for value in ('PENDING','0'*64):
            with patch.object(b,'MANIFEST_SHA',value),self.assertRaises(ValueError):b.validate_seal()
    def test_03_real_data_hash(self):self.assertEqual(b.digest(self.data),b.DATA_SHA);self.assertEqual([len(self.data[s]) for s in b.SPLITS],[192,96])
    def test_04_unicode_five_no_truncation(self):
        text=b.render(self.data['TRAIN'][4],5,b.PROFILES[0]);self.assertEqual(len(text.encode('utf-8')),52)
        with self.assertRaisesRegex(ValueError,'overflow'):b.prefix_tensor(text,48)
        x=b.prefix_tensor(text);self.assertEqual(int((x!=256).sum()),54);self.assertEqual(bytes(x[1:53].tolist()).decode('utf-8'),text);self.assertEqual(int(x[53]),258)
    def test_05_longer_prefix_rejected(self):
        with self.assertRaises(ValueError):b.prefix_tensor('a'*63)
        with self.assertRaises(ValueError):b.prefix_tensor('')
    def test_06_all_prompts_and_old_renderers(self):b.validate_prompts(self.prompts,self.data,self.c,NS(render=legacy_render));self.assertEqual(sum(len(rs) for d in self.prompts.values() for sp in d.values() for rs in sp.values()),3456)
    def test_07_prompt_tamper(self):
        p=copy.deepcopy(self.prompts);p['5']['HOLDOUT'][b.PROFILES[0]][0]['target']=99
        with self.assertRaises(ValueError):b.validate_prompts(p,self.data,self.c,NS(render=legacy_render))
    def test_08_train_tables_only(self):
        x,y=b.training_tables(self.data);self.assertEqual(x.shape,(3,3,192,64));self.assertTrue(torch.equal(y,self.y))
        forbidden={b.render(r,5,p) for r in self.data['TRAIN'] for p in b.PROFILES}
        for row in x.reshape(-1,64):self.assertNotIn(bytes(row[1:(row==258).nonzero()[0,0]].tolist()).decode('utf-8'),forbidden)
    def test_09_span_japanese_and_masks(self):
        for length,p,v in itertools.product(b.EVAL_LENGTHS,b.PROFILES,b.VIEWS):
            r=self.data['TRAIN'][4];text=b.render(r,length,p,v);x=b.prefix_tensor(text)[None,:];span=b.span_mask(x)
            actual=bytes(x[span].tolist()).decode('utf-8');expected='?' if v=='query_blind' else b.name_map(r,length,p)[r['query']]
            self.assertEqual(actual,expected)
    def test_10_old_span_padding_equivalence(self):
        t=b.render(self.data['TRAIN'][4],4,b.PROFILES[1]);a=b.span_mask(b.prefix_tensor(t,48)[None,:]);z=b.span_mask(b.prefix_tensor(t)[None,:]);self.assertTrue(torch.equal(a,z[:,:48]));self.assertFalse(bool(z[:,48:].any()))
    def test_11_bad_span(self):
        with self.assertRaises(ValueError):b.span_mask(torch.zeros((1,64),dtype=torch.int64))
    def test_12_actual_parameter_and_storage(self):
        c=real_class_factory();models=b.make_models(b.SEEDS[0],c)
        self.assertEqual([sum(p.numel() for p in m.parameters()) for m in models.values()],[14256]*3)
        ptrs=[p.data_ptr() for m in models.values() for p in m.parameters()];self.assertEqual(len(ptrs),len(set(ptrs)))
        self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        self.assertTrue(all(m.backbone.config.max_tokens==m.backbone.core.config.slots==64 for m in models.values()))
    def test_13_actual_48_64_forward_gradient(self):
        c=real_class_factory();ref=c.c278.MeanFinalDualReadout(c.factory.new_model(b.SEEDS[0]),b.SEEDS[0],c.reader,b.span_mask)
        before=fingerprint(ref);report=b.compatibility_probe(ref,self.data);self.assertEqual(report['rows'],54)
        self.assertLessEqual(report['max_logit_error'],1e-9);self.assertLessEqual(report['max_gradient_error'],1e-9);self.assertEqual(before,fingerprint(ref))
    def test_14_actual_five_forward_and_backward(self):
        c=real_class_factory();m=b.make_models(b.SEEDS[0],c)[b.ARMS[2]]
        x=torch.stack([b.prefix_tensor(b.render(self.data['TRAIN'][i],5,p)) for i in (0,4) for p in b.PROFILES]);z=m(x,torch.zeros(len(x),dtype=torch.int64));check_logits(z,6)
        F.cross_entropy(z,torch.tensor([48,49,50,51,48,49])).backward();self.assertTrue(any(p.grad is not None for p in m.backbone.core.parameters()))
    def test_15_actual_hook_cleanup(self):
        c=real_class_factory();m=b.make_models(b.SEEDS[0],c)[b.ARMS[0]];before=[(len(v._forward_hooks),len(v._forward_pre_hooks)) for v in m.modules()]
        x=b.prefix_tensor('aa=0;bb=1;aa=')[None,:]
        with patch.object(m.backbone.core,'forward',side_effect=RuntimeError('injected')),self.assertRaisesRegex(RuntimeError,'injected'):m(x,torch.zeros(1,dtype=torch.int64))
        self.assertEqual(before,[(len(v._forward_hooks),len(v._forward_pre_hooks)) for v in m.modules()])
    def test_16_all_schedules_exposure(self):
        for s,a in b.identities():
            e=b.schedule(s,a,self.data['TRAIN'],PS);v=b.schedule_stats(e)
            self.assertEqual(v['per_length_row_exposures'],[[n]*192 for n in b.manifest()['per_row_length_exposure'][a]])
            self.assertEqual([sum(row[p] for row in v['length_profile_updates']) for p in range(3)],[400]*3)
    def test_17_no_length_profile_lockstep(self):
        stats=b.schedule_stats(b.schedule(b.SEEDS[0],b.ARMS[2],self.data['TRAIN'],PS))
        self.assertEqual(stats['length_profile_updates'],[[136,132,132],[132,136,132],[132,132,136]])
    def test_18_pair_order_matched(self):
        for seed in b.SEEDS:
            es=[b.schedule(seed,a,self.data['TRAIN'],PS) for a in b.ARMS]
            for e in es[1:]:self.assertTrue(torch.equal(es[0][:,:,1:],e[:,:,1:]))
        with self.assertRaises(ValueError):b.schedule(1,b.ARMS[0],self.data['TRAIN'],PS)
    def test_19_three_actual_fit_loops(self):
        for arm,f in self.fits.items():
            b.check_fit(f,b.SEEDS[0],arm,self.data,PS);self.assertLess(f['ce_history'][-1],f['ce_history'][0]);self.assertNotEqual(fingerprint(self.models[arm]),fingerprint(self.initial))
    def test_20_optimizer_and_rng_repeat(self):
        original=torch.optim.AdamW;made=[]
        def create(*a,**k):o=original(*a,**k);made.append(o);return o
        m=copy.deepcopy(self.initial);torch.manual_seed(999)
        with patch.object(torch.optim,'AdamW',side_effect=create),contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[2],PS)
        self.assertEqual(len(made),1);self.assertEqual({int(s['step']) for s in made[0].state.values()},{1200});self.assertEqual(f['ce_history'],self.fits[b.ARMS[2]]['ce_history'])
    def test_21_fit_tampering(self):
        for fn in (lambda f:f.update(steps=800),lambda f:f['ce_history'].__setitem__(4,float('nan')),lambda f:f['per_length_row_exposures'][0].__setitem__(0,99)):
            f=copy.deepcopy(self.fits[b.ARMS[2]]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],b.ARMS[2],self.data,PS)
    def test_22_actual_score_adapter(self):
        c=real_scorer();score=b.score_length(self.data,raw_fixture(self.data),c);self.assertTrue(score['passed']);self.assertEqual(len(score['cells']),72)
        raw=raw_fixture(self.data);raw['HOLDOUT'][b.PROFILES[0]]['normal'][0,70]=10.
        score=b.score_length(self.data,raw,c);self.assertFalse(score['passed']);self.assertTrue(any(v['accuracy']==.875 for v in score['cells']))
    def test_23_masks_not_bypassed(self):
        raw=raw_fixture(self.data)
        for groups in raw.values():
            for view in groups.values():view['evidence_blind']=view['normal'].clone()
        self.assertFalse(b.score_length(self.data,raw,real_scorer())['passed'])
    def test_24_analysis_inventory_and_five_gate(self):
        self.assertEqual((len(self.metrics),len(self.summary['final_partitions']),len(self.summary['contrasts'])),(15,120,80));b.validate_result(payload(self.summary))
        rs=copy.deepcopy(self.records);rs[2]['raw']['5']=raw_fixture(self.data,False);_,s=b.analyze(rs,self.data,PS,self.diag,self.c)
        self.assertFalse(s['candidate_gate']);self.assertEqual(s['length_pass_counts']['5'][b.ARMS[2]],4);b.validate_result(payload(s))
    def test_25_replay_and_matching_tamper(self):
        for k,v in (('slots',48),('reload_max_error',.1),('initial_sha256','x'*64),('forward_calls',881)):
            rs=copy.deepcopy(self.records);rs[1][k]=v
            with self.assertRaises(ValueError):b.analyze(rs,self.data,PS,self.diag,self.c)
    def test_26_actual_training_and_full_replay_counts(self):
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted,check_logits=check_logits),core=None);m=copy.deepcopy(self.initial)
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_one(m,self.data,self.prompts,self.x,self.y,b.SEEDS[0],b.ARMS[2],PS,c)
        n=copy.deepcopy(self.initial);b.replay_one(n,state,r,self.prompts,self.data,c)
        self.assertEqual((r['forward_calls'],r['replay_forward_calls']),(1308,108));self.assertEqual(r['reload_max_error'],0.)
    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path('/c304-fixture')/str(i)/'summary.json').resolve() for i in range(30)]
        p301=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(27)));p302=NS(PARENT_SHA='e'*64)
        parent=NS(PARENT_SHA='d'*64,context=lambda:(p302,p301),validate_result=Mock(),OUTPUTS=tuple(str(i) for i in range(8)))
        s=dict(task_pass_counts=dict(two_char=dict(full_train=4,core_frozen=5,residual_stop=4),triple=dict(full_train=4,core_frozen=5,residual_stop=4),quad=dict(full_train=3,core_frozen=4,residual_stop=0)),candidate_gate=False,all_groups_matched=True,all_replays=True)
        p=dict(experiment_id='C303-v5b-residual-gradient-routing',commit_sha=b.PARENT_EXECUTION,status='FAIL',artifacts=[dict(file=n) for n in parent.OUTPUTS],validation_summary=s)
        parent.verify_artifacts=Mock(return_value=(p,{}));mapping=dict(zip(map(str,paths),b.parent_hashes(parent),strict=True));c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:self.data),p267=NS(validate_data=validate_data))
        with patch.object(b,'context',return_value=(parent,p301,NS(no_neural=contextlib.nullcontext),None,None,c)):yield paths,mapping,parent,p
    def test_27_all_parent_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p):
            self.assertEqual(b.load_parent(paths)[0],p);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]='f'*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old
    def test_28_bad_parent_result(self):
        with self.loader_fixture() as (paths,_,_,p):
            p['status']='PASS'
            with self.assertRaises(ValueError):b.load_parent(paths)
    def test_29_real_protection_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pins=dict(b.PINNED)
            while len(pins)<664:pins['accepted/'+str(len(pins))]='b'*40
            for n in list(pins)+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding='utf-8')
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1228-len(protected)):
                p=root/f'input{i}';p.write_text('input',encoding='utf-8');protected[str(p.resolve())]=Audit.sha(p)
            directory=root/'parent';directory.mkdir();sp=directory/'summary.json';sp.write_text('summary',encoding='utf-8');mapping={str(sp.resolve()):b.PARENT_SHA};artifacts=[]
            for i in range(8):
                p=directory/str(i);p.write_text('parent',encoding='utf-8');mapping[str(p.resolve())]='a'*64;artifacts.append(dict(file=str(i),sha256='a'*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType('parent');parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            p301=NS(context=lambda:(None,),pair_source=lambda _:PS);c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],'c'*40)+'\n').encode(),safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            value=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,'context',return_value=(parent,p301,None,None,None,c)),patch.object(b,'load_parent',return_value=(value,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([sp]*30,root))),(670,1243));c.missing=types.ModuleType('missing');c.missing.__file__=str(root/'missing.py')
                with self.assertRaisesRegex(ValueError,'unprotected'):b.precheck([sp]*30,root)
    @contextlib.contextmanager
    def run_fixture(self):
        events=[];diag,c=software_scorers();c.audit=Audit();p301=NS(context=lambda:(None,),pair_source=lambda _:PS)
        def pc(*a):events.append('precheck');return protection()
        def train(*a):events.append('train');return copy.deepcopy(self.records[b.identities().index((a[0].seed,a[0].arm))]),{}
        def replay(*a):events.append('replay')
        with patch.object(b,'context',return_value=(None,p301,NS(no_neural=contextlib.nullcontext),diag,NS(render=legacy_render),c)),patch.object(b,'precheck',side_effect=pc),patch.object(b,'load_parent',return_value=({},self.data)),patch.object(b,'make_models',side_effect=lambda seed,c:{a:NS(seed=seed,arm=a) for a in b.ARMS}),patch.object(b,'train_one',side_effect=train),patch.object(b,'replay_one',side_effect=replay):yield events
    def test_30_run_dispatch_roundtrip(self):
        with self.run_fixture() as e,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run';p=b.run(summaries=['x']*30,output_dir=out,expected_head='f'*40)
            self.assertEqual(e.count('train'),15);self.assertEqual(e.count('replay'),15);self.assertLess(max(i for i,v in enumerate(e) if v=='train'),e.index('replay'))
            q,_=b.verify_artifacts(out,['x']*30,'f'*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=['x']*30,output_dir=out,expected_head='f'*40)
    def test_31_hash_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run';p=b.run(summaries=['x']*30,output_dir=out,expected_head='f'*40);path=out/'measurements.json';path.write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'output bytes'):b.verify_artifacts(out,['x']*30,'f'*40)
            a=next(a for a in p['artifacts'] if a['file']==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/'summary.json').write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,'persisted'):b.verify_artifacts(out,['x']*30,'f'*40)
    def test_32_bundle_rejects_wrong_slots(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'model.pt';v=dict(schema='fold-c304-length-models-v1',slots=64,identities=[list(i) for i in b.identities()],states=[{}]*15);torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),15)
            v['slots']=48;torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)
    def test_33_semantic_regression_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=['fixture.'+str(i) for i in range(4749)]+[b.EXCLUDED]
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4749);self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
    def test_34_real_runtime_preflight_path(self):
        c=real_class_factory();c.p267=self.c.p267;c.c270=self.c.c270;p301=NS(context=lambda:(None,),pair_source=lambda _:PS)
        with patch.object(b,'precheck',return_value=protection()),patch.object(b,'load_parent',return_value=({},self.data)),patch.object(b,'context',return_value=(None,p301,None,None,NS(render=legacy_render),c)),contextlib.redirect_stdout(io.StringIO()):b.runtime_preflight(['x']*30,Path.cwd())
    def test_35_result_scope(self):
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p['validation_summary'].update(models=False),lambda p:p['validation_summary']['final_partitions'].pop()):
            p=payload(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)
    def test_36_cp932_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,'text_encoding',side_effect=lambda encoding,stacklevel=2:'cp932' if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding='utf-8'))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding='utf-8'))
        for p in (Path(__file__),Path(b.__file__)):
            for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='read_text':self.assertTrue(any(k.arg=='encoding' and isinstance(k.value,ast.Constant) and k.value.value=='utf-8' for k in n.keywords))
    def test_37_runner_and_paths(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding='utf-8');launcher=(root/b.OWN[3]).read_text(encoding='utf-8');blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S)
        self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn('sys.argv[2:32]',blocks[2]);self.assertIn('head = sys.argv[32]',blocks[2]);self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),30)
        self.assertLess(launcher.index('-Mode Validate'),launcher.index('-Mode Execute'));self.assertLess(launcher.index('AUTHORING_RUNTIME_PREFLIGHT_FAILED'),launcher.index('publish_experiment_log.ps1'))
    def test_38_cli_context(self):
        argv=['prog','--summaries']+[str(i) for i in range(30)]+['--output-dir','out','--expected-head','f'*40]
        with patch.object(sys,'argv',argv),patch.object(b,'run') as run:b.main();self.assertEqual(len(run.call_args.kwargs['summaries']),30)
        parent=NS(context=lambda:tuple(range(8)),regression_modules=lambda r:['f'+str(i) for i in range(188)]);package=types.ModuleType('fold_lm.v05_benchmarks');package.model_c303_residual_gradient=parent
        with patch.dict(sys.modules,{'fold_lm.v05_benchmarks':package}):self.assertEqual(b.context(),(parent,1,2,3,5,7));self.assertEqual(len(b.regression_modules(Path.cwd())),189)
    def test_39_guard_and_import(self):
        b.guard(Path.cwd(),'f'*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),'e'*40,NS(audit=Audit()))
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding='utf-8'))) if isinstance(n,ast.ImportFrom) and (n.module or '').startswith('fold_lm')];self.assertEqual(imports,['model_c303_residual_gradient'])
    def test_40_test_inventory(self):self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()['own_tests'])


if __name__=='__main__':unittest.main()
