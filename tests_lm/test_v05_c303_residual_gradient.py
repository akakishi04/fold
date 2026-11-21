"""Software-control fixtures; synthetic learning examples are not FOLD capability evidence."""
import ast
from collections import Counter
import contextlib
import copy
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
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c303_residual_gradient as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for perm,q in itertools.product((e,e[::-1]),e):data[split].append(dict(language=lang,entities=list(e),values=list(v),permutation=list(perm),query=q,target=48+v[e.index(q)]))
    return data


def pairs(rows):
    g={}
    for i,r in enumerate(rows):g.setdefault((r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"])),[]).append(i)
    return torch.tensor([sorted(g[k],key=lambda i:rows[i]["query"]) for k in sorted(g)],dtype=torch.int64)


def render(x,y,e):return x[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),e[:,2:].flatten()],y[e[:,2:].flatten()]
PS=NS(pairs_from_rows=pairs,render_batch=render)


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((2,3,192,48),dtype=torch.int64);x[:,:,:,0]=y-48
    return x,y


class Encoder(torch.nn.Module):
    def __init__(self):super().__init__();self.embed=torch.nn.Embedding(4,16,dtype=torch.float64)
    def forward(self,x):return self.embed(x[:,0])


class Core(torch.nn.Module):
    def __init__(self):
        super().__init__();self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
        self.padding=torch.nn.Parameter(torch.zeros(3328-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x):return torch.tanh(self.linear(x))


class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__();self.local_encoder=Encoder();self.core=Core();self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64);self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.padding=torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()),dtype=torch.float64));self.local=None;self.residual=None
    def forward(self,x,t):
        self.local=self.local_encoder(x);r=self.local
        for _ in range(4):r=self.core(r)
        self.residual=r
        if r.requires_grad:r.retain_grad()
        return self.classifier(self.readout_norm(r))


class Reader(torch.nn.Module):
    def __init__(self,*_):
        super().__init__()
        for n in ("query","key","output"):setattr(self,n,torch.nn.Linear(16,16,bias=False,dtype=torch.float64))


class Toy(torch.nn.Module):
    def __init__(self,backbone=None,*_):
        super().__init__();self.backbone=Backbone() if backbone is None else backbone;self.read=Reader();self.fail=False;self.offset=0.
    def forward(self,x,t):
        def add(module,args):
            if self.fail:raise RuntimeError("injected")
            a=self.read.output(self.read.key(self.read.query(self.backbone.local)))
            return (args[0]+a+self.offset,)
        h=self.backbone.readout_norm.register_forward_pre_hook(add)
        try:return self.backbone(x,t)
        finally:h.remove()


def factory():
    def new(seed):torch.manual_seed(seed);return Backbone()
    return NS(c278=NS(MeanFinalDualReadout=Toy),factory=NS(new_model=new),reader=None,c269=NS(query_span_mask=None))


@contextlib.contextmanager
def counted(model):
    calls=[0,0];cores=[0]
    def mh(m,a,o):calls[0]+=1;calls[1]+=len(a[0])
    def ch(m,a,o):cores[0]+=1
    h=model.register_forward_hook(mh);g=model.backbone.core.register_forward_hook(ch)
    try:yield calls,cores
    finally:h.remove();g.remove()


def evaluate(model,data,*_):
    assert not model.training and not any(p.requires_grad for p in model.parameters())
    with torch.no_grad():return [model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64)).detach().clone() for _ in range(81)]


def replay_error(a,c,*_):
    error=max(float((x-y).abs().max()) for x,y in zip(a,c,strict=True));b.require(error<=1e-9,"replay");return error


def fit_fixture(seed,arm,data):
    e=b.schedule(seed,data["TRAIN"],PS)
    inv={"model.backbone.core.weight":dict(numel=3328,trainable=arm==b.ARMS[0],core=True),"model.rest":dict(numel=10928,trainable=True,core=False)}
    names=sorted(n for n,v in inv.items() if v["trainable"]);size=sum(inv[n]["numel"] for n in names)
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=b.FIT_RNG,ce_history=[.1]*800,parameter_inventory=inv,
        gradient_scalars=[size]*800,core_gradient_scalars=[3328 if arm==b.ARMS[0] else 0]*800,gradient_parameter_union=names,
        event_sha256=b.digest(e.tolist()),schedule_events=e,logits_sha256="a"*64,reader_gradient_sha256="b"*64)


def fixtures():
    data=dataset();records=[]
    for seed,arm in b.identities():
        raw={t:dict(passed=True,totals=[dict(split=s,rows=n,correct=n,direct_pass=True,final_normal_nll=.1) for s,n in (("TRAIN",576),("HOLDOUT",288))]) for t in b.TASKS}
        records.append(dict(seed=seed,arm=arm,initial_sha256="a"*64,final_sha256="b"*64,core_initial_sha256="c"*64,core_final_sha256=("d" if arm==b.ARMS[0] else "c")*64,
            fit=fit_fixture(seed,arm,data),raw=raw,formula_checks=881,forward_calls=881,row_presentations=46176,core_forward_calls=3524,
            checkpoint_roundtrip=True,reload_max_error=0.,replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,data


def scorers():
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda rr:{k:v for k,v in rr[0].items() if k!="split"})
    return diag,NS(score_quad=lambda d,r,c:r),NS(p267=NS(score=lambda d,r:r),c270=NS(score=lambda d,r,p:r))


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB;pins[b.READOUT_SOURCE]=b.READOUT_BLOB
    while len(pins)<664:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1228)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n):return Path(root)/n
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch":return b"feat/sft-target-loss\n"
        return b""


def payload(s):
    pins,p=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=p,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False)


class C303Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.records,cls.data=fixtures();cls.x,cls.y=tables(cls.data);cls.metrics,cls.summary=b.analyze(cls.records,cls.data,PS,*scorers())
        torch.manual_seed(7);cls.initial=Toy();cls.models={a:b.GradientRoute(copy.deepcopy(cls.initial),a) for a in b.ARMS};cls.fits={}
        with contextlib.redirect_stdout(io.StringIO()):
            for a,m in cls.models.items():cls.fits[a]=b.fit(m,cls.data,cls.x,cls.y,b.SEEDS[0],PS)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
    def test_02_bad_seals(self):
        for h in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",h),self.assertRaises(ValueError):b.validate_seal()
    def test_03_factory_counts(self):
        models=b.make_models(b.SEEDS[0],factory());self.assertEqual([sum(p.numel() for p in m.parameters()) for m in models.values()],[14256]*3)
        self.assertEqual([sum(p.numel() for p in m.parameters() if p.requires_grad) for m in models.values()],[14256,10928,10928])
        self.assertEqual(len({b.fingerprint(m) for m in models.values()}),1)
    def test_04_invalid_arm_seed(self):
        with self.assertRaises(ValueError):b.GradientRoute(Toy(),"wrong")
        with self.assertRaises(ValueError):b.make_models(301001,factory())
    def test_05_initial_outputs_reader_grads(self):
        models=b.make_models(b.SEEDS[0],factory());b.initial_probe(models,self.x[0,0,:48],self.y[:48])
    def test_06_distinguish_core_freeze_and_stop(self):
        grads={}
        for a in b.ARMS:
            m=b.GradientRoute(copy.deepcopy(self.initial),a);F.cross_entropy(m(self.x[0,0,:48],torch.zeros(48,dtype=torch.int64)),self.y[:48]).backward()
            grads[a]=m.backbone.local_encoder.embed.weight.grad.clone()
            if a==b.ARMS[2]:self.assertIsNone(m.backbone.residual.grad)
            else:self.assertIsNotNone(m.backbone.residual.grad);self.assertGreater(float(m.backbone.residual.grad.abs().sum()),0.)
        self.assertTrue(torch.equal(grads[b.ARMS[0]],grads[b.ARMS[1]]));self.assertFalse(torch.equal(grads[b.ARMS[1]],grads[b.ARMS[2]]))
    def test_07_independent_stop_gradient_reference(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);ref=copy.deepcopy(self.initial);ref.backbone.core.requires_grad_(False)
        x=self.x[0,0,:48];y=self.y[:48];F.cross_entropy(m(x,torch.zeros(48,dtype=torch.int64)),y).backward()
        local=ref.backbone.local_encoder(x);r=local
        for _ in range(4):r=ref.backbone.core(r)
        a=ref.read.output(ref.read.key(ref.read.query(local)));z=ref.backbone.classifier(ref.backbone.readout_norm(r.detach()+a));F.cross_entropy(z,y).backward()
        self.assertEqual(b.tensor_hash((n,p.grad) for n,p in m.model.named_parameters()),b.tensor_hash((n,p.grad) for n,p in ref.named_parameters()))
    def test_08_hook_restore(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);before=b.hook_snapshot(m)
        for _ in range(3):m(self.x[0,0,:4],torch.zeros(4,dtype=torch.int64))
        self.assertEqual(b.hook_snapshot(m),before);self.assertEqual(m.verified_calls,3)
    def test_09_exception_restore(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);m.model.fail=True;before=b.hook_snapshot(m)
        with self.assertRaisesRegex(RuntimeError,"injected"):m(self.x[0,0,:4],torch.zeros(4,dtype=torch.int64))
        self.assertEqual(b.hook_snapshot(m),before)
    def test_10_wrong_sum_dtype(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);m.model.offset=.5
        with self.assertRaisesRegex(ValueError,"actual C278 sum"):m(self.x[0,0,:4],torch.zeros(4,dtype=torch.int64))
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]).float()
        with self.assertRaisesRegex(ValueError,"summands"):m(self.x[0,0,:4],torch.zeros(4,dtype=torch.int64))
    def test_11_factory_storage(self):
        models=b.make_models(b.SEEDS[0],factory());ptrs=[p.data_ptr() for m in models.values() for p in m.parameters()];self.assertEqual(len(ptrs),len(set(ptrs)))
    def test_12_schedule_all_five(self):
        hashes=[]
        for seed in b.SEEDS:
            e=b.schedule(seed,self.data["TRAIN"],PS);self.assertEqual(e.shape,(800,24,4));hashes.append(b.digest(e.tolist()))
            for l in range(2):self.assertTrue(torch.equal(torch.bincount(e[e[:,:,0]==l][:,2:].flatten(),minlength=192),torch.full((192,),100)))
        self.assertEqual(len(set(hashes)),5)
    def test_13_schedule_determinism(self):
        self.assertTrue(torch.equal(b.schedule(b.SEEDS[0],self.data["TRAIN"],PS),b.schedule(b.SEEDS[0],self.data["TRAIN"],PS)))
        with self.assertRaises(ValueError):b.schedule(1,self.data["TRAIN"],PS)
    def test_14_actual_three_fits(self):
        for arm,f in self.fits.items():
            b.check_fit(f,b.SEEDS[0],arm,self.data,PS);self.assertEqual(self.models[arm].verified_calls,800);self.assertLess(f["ce_history"][-1],f["ce_history"][0])
            same=b.fingerprint(self.models[arm].backbone.core)==b.fingerprint(self.initial.backbone.core);self.assertEqual(same,arm!=b.ARMS[0])
            self.assertNotEqual(b.fingerprint(self.models[arm].read),b.fingerprint(self.initial.read))
    def test_15_rng_one_optimizer(self):
        real=torch.optim.AdamW;made=[]
        def make(*a,**k):o=real(*a,**k);made.append(o);return o
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);torch.manual_seed(33)
        with patch.object(torch.optim,"AdamW",side_effect=make),contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],PS)
        self.assertEqual(len(made),1);self.assertEqual({int(v["step"]) for v in made[0].state.values()},{800});self.assertEqual(f["ce_history"],self.fits[b.ARMS[2]]["ce_history"])
    def test_16_target_alignment(self):
        y=self.y.clone();y[0]=99
        with self.assertRaises(ValueError):b.fit(b.GradientRoute(Toy(),b.ARMS[0]),self.data,self.x,y,b.SEEDS[0],PS)
    def test_17_fit_tampering(self):
        for fn in (lambda f:f.update(steps=799),lambda f:f["core_gradient_scalars"].__setitem__(2,3328),lambda f:f["gradient_parameter_union"].append("missing")):
            f=copy.deepcopy(self.fits[b.ARMS[2]]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],b.ARMS[2],self.data,PS)
    def test_18_matched_group(self):
        b.check_group(self.records[:3]);rr=copy.deepcopy(self.records[:3]);rr[2]["fit"]["reader_gradient_sha256"]="z"*64
        with self.assertRaises(ValueError):b.check_group(rr)
    def test_19_analysis_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(15,90,60));b.validate_result(payload(self.summary))
    def test_20_five_of_five(self):
        rr=copy.deepcopy(self.records);rr[2]["raw"]["quad"]["passed"]=False;_,s=b.analyze(rr,self.data,PS,*scorers());self.assertFalse(s["candidate_gate"]);b.validate_result(payload(s))
    def test_21_core_replay_tamper(self):
        for k,v in (("core_final_sha256","z"*64),("reload_max_error",.1),("formula_checks",880)):
            rr=copy.deepcopy(self.records);rr[1][k]=v
            with self.assertRaises(ValueError):b.analyze(rr,self.data,PS,*scorers())
    def test_22_actual_train_replay(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);p301=NS(counted=counted);ev=NS(evaluate=evaluate,replay_error=replay_error);c=NS(base=NS(fingerprint=b.fingerprint))
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_one(m,self.data,None,None,self.x,self.y,b.SEEDS[0],PS,p301,ev,None,c)
        n=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);b.replay_one(n,state,r,self.data,None,None,p301,ev,None,c)
        self.assertEqual(r["reload_max_error"],0.);self.assertEqual((m.verified_calls,n.verified_calls),(881,81))
    def test_23_strict_replay_state(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2])
        with self.assertRaisesRegex(ValueError,"strict state"):b.replay_one(m,m.state_dict(),dict(final_sha256="x"*64),None,None,None,None,None,None,NS(base=NS(fingerprint=b.fingerprint)))

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path('/c303-fixture')/str(i)/'summary.json').resolve() for i in range(29)];data={n:{"file":n} for n in b.OUTPUTS[1:4]}
        p301=NS(context=lambda:(NS(context=lambda:(NS(DATA_HASHES=tuple(map(b.digest,data.values()))),)),),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(27)))
        p=dict(experiment_id='C302-v5b-frozen-gain-weight-cross',status='PASS',commit_sha=b.PARENT_EXECUTION,source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.READOUT_SOURCE:b.READOUT_BLOB},
            artifacts=[dict(file=n) for n in 'abcd'],validation_summary=dict(task_pass_counts=b.expected_parent_counts(),diagnostic_complete=True,capability_gate_applicable=False,all_weights_preserved=True,all_hooks_restored=True))
        parent=NS(PARENT_SHA='e'*64,OUTPUTS=tuple('abcd'),verify_artifacts=Mock(return_value=(p,{})),validate_result=Mock())
        hashes=(b.PARENT_SHA,parent.PARENT_SHA,*p301.parent_hashes(None));mapping=dict(zip(map(str,paths),hashes,strict=True));c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:data[p.name]))
        with patch.object(b,'context',return_value=(parent,p301,NS(no_neural=contextlib.nullcontext),None,None,None,None,c)):yield paths,mapping,parent,p
    def test_24_all29_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p):
            self.assertEqual(b.load_parent(paths)[0],p);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]='f'*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old
    def test_25_parent_contract(self):
        for fn in (lambda p:p.update(status='FAIL'),lambda p:p['source_blobs'].pop(b.PARENT_SOURCE),lambda p:p['validation_summary'].update(all_weights_preserved=False)):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError):b.load_parent(paths)
    def test_26_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE,b.READOUT_SOURCE]+[f'accepted/{i}' for i in range(656)];pins=dict.fromkeys(names,'b'*40);pins[b.PARENT_SOURCE]=b.PARENT_BLOB;pins[b.READOUT_SOURCE]=b.READOUT_BLOB
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding='utf-8')
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1217-len(protected)):
                p=root/f'input{i}';p.write_text('input',encoding='utf-8');protected[str(p.resolve())]=Audit.sha(p)
            directory=root/'parent';directory.mkdir();path=directory/'summary.json';path.write_text('summary',encoding='utf-8');mapping={str(path.resolve()):b.PARENT_SHA};artifacts=[]
            for n in 'abcd':
                p=directory/n;p.write_text('parent',encoding='utf-8');mapping[str(p.resolve())]='a'*64;artifacts.append(dict(file=n,sha256='a'*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType('parent');parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            p301=NS(context=lambda:(None,),pair_source=lambda _:PS);c=NS(audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],'c'*40)+'\n').encode(),safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            p=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,'context',return_value=(parent,p301,None,None,None,None,None,c)),patch.object(b,'load_parent',return_value=(p,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*29,root))),(664,1228));c.missing=types.ModuleType('missing');c.missing.__file__=str(root/'missing.py')
                with self.assertRaisesRegex(ValueError,'unprotected helper'):b.precheck([path]*29,root)

    @contextlib.contextmanager
    def run_fixture(self):
        diag,transfer,c=scorers();c.audit=Audit();events=[];p301=NS(context=lambda:(None,),pair_source=lambda _:PS)
        def train(*a):events.append('train');r=copy.deepcopy(self.records[b.identities().index((a[0].seed,a[0].arm))]);return r,{}
        def replay(*a):events.append('replay')
        def pc(*a):events.append('precheck');return protection()
        def load(*a):events.append('load_parent');return {},self.data,{'triple':1},{'quad':1}
        with patch.object(b,'context',return_value=(None,p301,NS(no_neural=contextlib.nullcontext),diag,None,transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,'precheck',side_effect=pc),patch.object(b,'load_parent',side_effect=load),patch.object(b,'make_models',side_effect=lambda s,c:{a:NS(seed=s,arm=a) for a in b.ARMS}),patch.object(b,'train_one',side_effect=train),patch.object(b,'replay_one',side_effect=replay):yield events
    def test_27_run_order_roundtrip(self):
        with self.run_fixture() as e,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run';p=b.run(summaries=['x']*29,output_dir=out,expected_head='f'*40);self.assertEqual(e[:2],['precheck','load_parent']);self.assertEqual((e.count('train'),e.count('replay')),(15,15))
            self.assertLess(max(i for i,v in enumerate(e) if v=='train'),e.index('replay'));q,_=b.verify_artifacts(out,['x']*29,'f'*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=['x']*29,output_dir=out,expected_head='f'*40)
    def test_28_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run';p=b.run(summaries=['x']*29,output_dir=out,expected_head='f'*40);path=out/'measurements.json';path.write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'output bytes'):b.verify_artifacts(out,['x']*29,'f'*40)
            a=next(a for a in p['artifacts'] if a['file']==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/'summary.json').write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,'persisted'):b.verify_artifacts(out,['x']*29,'f'*40)
    def test_29_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=['fixture.'+str(i) for i in range(4709)]+[b.EXCLUDED]
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4709);self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite([Dummy('x'),Dummy('x')])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())
    def test_30_context_cli(self):
        p301=object();parent=NS(context=lambda:(p301,1,2,3,4,5,6),regression_modules=lambda r:['f'+str(i) for i in range(187)])
        package=types.ModuleType('fold_lm.v05_benchmarks');package.model_c302_frozen_gain_cross=parent
        with patch.dict(sys.modules,{'fold_lm.v05_benchmarks':package}):self.assertEqual(b.context(),(parent,p301,1,2,3,4,5,6));self.assertEqual(len(b.regression_modules(Path.cwd())),188)
        argv=['prog','--summaries']+[str(i) for i in range(29)]+['--output-dir','out','--expected-head','f'*40]
        with patch.object(sys,'argv',argv),patch.object(b,'run') as run:b.main();self.assertEqual(len(run.call_args.kwargs['summaries']),29)
    def test_31_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'m.pt';v=dict(schema='fold-c303-gradient-models-v1',identities=[list(i) for i in b.identities()],states=[{}]*15);torch.save(v,path);self.assertEqual(len(b.load_bundle(path)),15)
            v['identities'].reverse();torch.save(v,path)
            with self.assertRaises(ValueError):b.load_bundle(path)
    def test_32_actual_preflight(self):
        c=factory();p301=NS(context=lambda:(None,),pair_source=lambda _:PS)
        with patch.object(b,'precheck',return_value=protection()),patch.object(b,'load_parent',return_value=({},self.data,None,None)),patch.object(b,'context',return_value=(None,p301,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),c)),contextlib.redirect_stdout(io.StringIO()):b.runtime_preflight(['x']*29,Path.cwd())
    def test_33_explicit_utf8(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,'text_encoding',side_effect=lambda encoding,stacklevel=2:'cp932' if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding='utf-8'))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding='utf-8'))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='read_text':self.assertTrue(any(k.arg=='encoding' and isinstance(k.value,ast.Constant) and k.value.value=='utf-8' for k in n.keywords))
    def test_34_runner(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding='utf-8');launcher=(root/b.OWN[3]).read_text(encoding='utf-8');blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S)
        self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn('sys.argv[2:31]',blocks[2]);self.assertIn('head = sys.argv[31]',blocks[2]);self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),29)
        self.assertLess(launcher.index('-Mode Validate'),launcher.index('-Mode Execute'));self.assertLess(launcher.index('AUTHORING_RUNTIME_PREFLIGHT_FAILED'),launcher.index('publish_experiment_log.ps1'))
    def test_35_result_scope(self):
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p['validation_summary'].update(models=False),lambda p:p['validation_summary'].update(candidate_gate=False)):
            p=payload(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)
    def test_36_actual_accepted_class(self):
        path=Path(__file__).resolve().parents[1]/b.READOUT_SOURCE;tree=ast.parse(path.read_text(encoding='utf-8'));node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='MeanFinalDualReadout')
        space=dict(torch=torch,nn=torch.nn,Counter=Counter,req=b.require,__name__='c303_parent_class_fixture');exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),space)
        class WideEncoder(torch.nn.Module):
            def __init__(self):super().__init__();self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
            def forward(self,x):return (self.embed(x),)
        class WideCore(Core):
            def forward(self,state,local,route_index):return torch.tanh(self.linear(state)+local*.1)
        class WideBackbone(torch.nn.Module):
            def __init__(self):
                super().__init__();self.local_encoder=WideEncoder();self.core=WideCore();self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64);self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
                self.config=NS(width=16,max_tokens=48,next_route=0,instruction_route=1,internal_steps=2);self.padding=torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
            def forward(self,x,t):
                valid=x!=256;local=self.local_encoder(x)[0]*valid[:,:,None];state=local
                for _ in range(2):nxt=self.core(state,local,route_index=0);self.core(state,local,route_index=1);state=nxt
                return self.classifier(self.readout_norm(state[torch.arange(len(x)),valid.sum(1)-1]))
        def span(x):m=torch.zeros_like(x,dtype=torch.bool);m[:,1:3]=True;return m
        torch.manual_seed(10);base=space['MeanFinalDualReadout'](WideBackbone(),1,NS(ResidualHead=Reader),span);models={a:b.GradientRoute(copy.deepcopy(base),a) for a in b.ARMS}
        x=torch.full((4,48),256,dtype=torch.int64);x[:,:4]=torch.tensor([0,1,2,258]);y=torch.tensor([48,49,50,51]);b.initial_probe(models,x,y)
        for a,m in models.items():self.assertEqual(b.hook_snapshot(m.model),b.hook_snapshot(base))
    def test_37_state_inventory_no_padding_claim(self):
        for arm,f in self.fits.items():
            inv=f['parameter_inventory'];active=f['gradient_parameter_union'];self.assertLess(sum(inv[n]['numel'] for n in active),14256)
            if arm!=b.ARMS[0]:self.assertFalse(any(inv[n]['core'] for n in active))
    def test_38_gradient_union_tamper(self):
        f=copy.deepcopy(self.fits[b.ARMS[2]]);f['gradient_parameter_union'].append(next(n for n,v in f['parameter_inventory'].items() if v['core']));f['gradient_parameter_union'].sort()
        with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],b.ARMS[2],self.data,PS)
    def test_39_forward_eval_same_without_wrapper(self):
        m=b.GradientRoute(copy.deepcopy(self.initial),b.ARMS[2]);m.eval();m.requires_grad_(False)
        with torch.no_grad():self.assertTrue(torch.equal(m(self.x[0,0,:4],torch.zeros(4,dtype=torch.int64)),m.model(self.x[0,0,:4],torch.zeros(4,dtype=torch.int64))))
    def test_40_guard_imports_count(self):
        b.guard(Path.cwd(),'f'*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),'e'*40,NS(audit=Audit()))
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding='utf-8'))) if isinstance(n,ast.ImportFrom) and (n.module or '').startswith('fold_lm')]
        self.assertEqual(imports,['model_c302_frozen_gain_cross']);self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),40)


if __name__=='__main__':unittest.main()
