"""C306 software controls; synthetic target-coded inputs are not generalization evidence."""
import ast
from collections import Counter,defaultdict
import contextlib
import copy
from dataclasses import dataclass,replace
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
from fold_lm.v05_benchmarks import model_c306_broad_length_core_freeze as b


def dataset():
    data={s:[] for s in ("TRAIN","HOLDOUT")}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(id=str((e,v,lang,order,q)),entities=list(e),values=list(v),language=lang,permutation=list(order),query=q,target=48+v[e.index(q)]))
    return data


def pairs_from_rows(rows):
    groups=defaultdict(list)
    for i,r in enumerate(rows):groups[(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))].append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def schedule_stats(events):
    counts=[];profiles=[]
    for k in range(3):
        selected=events[events[:,:,0]==k];counts.append(torch.bincount(selected[:,2:].flatten(),minlength=192).tolist())
        profiles.append([int(((events[:,0,0]==k)&(events[:,0,1]==p)).sum()) for p in range(3)])
    return dict(per_length_row_exposures=counts,length_profile_updates=profiles,event_sha256=b.digest(events.tolist()),
        logical_pair_sha256=b.digest(events[:,:,2:].tolist()),profile_sha256=b.digest(events[:,:,1].tolist()))


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((3,3,192,64),dtype=torch.int64);x[:,:,:,0]=y-48
    return x,y


def fingerprint(model):return b.digest({k:v.detach().tolist() for k,v in model.state_dict().items()})


class Toy(nn.Module):
    def __init__(self):
        super().__init__();self.backbone=nn.Module();self.backbone.local_encoder=nn.Embedding(4,16,dtype=torch.float64)
        self.backbone.core=nn.Linear(16,16,dtype=torch.float64)
        self.backbone.core.padding=nn.Parameter(torch.zeros(3328-272,dtype=torch.float64))
        self.read=nn.Linear(16,256,dtype=torch.float64)
        self.other=nn.Parameter(torch.zeros(14256-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
        self.calls=0;self.rows=0
    def forward(self,x,tasks):
        assert x.shape==(len(x),64) and tasks.shape==(len(x),) and not bool(tasks.any())
        self.calls+=1;self.rows+=len(x)
        return self.read(torch.tanh(self.backbone.core(self.backbone.local_encoder(x[:,0]))))


def records_fixture():
    data=dataset();records=[];pairs=NS(pairs_from_rows=pairs_from_rows)
    for seed,arm in b.identities():
        events=b.schedule(seed,data["TRAIN"],pairs)
        union={"backbone.local_encoder.weight":64,"read.weight":4096}
        if arm==b.ARMS[0]:union["backbone.core.weight"]=256
        fit=dict(steps=1200,training_rows=57600,optimizer_creations=1,fit_rng=b.FIT_RNG,trainable_parameters=b.manifest()["trainable_parameters"][arm],
            ce_history=[.1]*1200,gradient_parameter_counts=[sum(union.values())]*1200,gradient_union=union,schedule_events=events,**schedule_stats(events))
        raw={str(n):dict(passed=True,totals=[dict(split=s,rows=3*len(rr),correct=3*len(rr),direct_pass=True) for s,rr in data.items()]) for n in b.LENGTHS}
        records.append(dict(seed=seed,arm=arm,parameters=14256,slots=64,initial_sha256=b.digest(seed),final_sha256=b.digest([seed,arm]),
            core_initial_sha256="a"*64,core_final_sha256=("a" if arm==b.ARMS[1] else "b")*64,fit=fit,raw=raw,
            forward_calls=1308,row_presentations=67968,core_forward_calls=5232,checkpoint_roundtrip=True,reload_max_error=0.,
            replay_forward_calls=108,replay_row_presentations=10368,replay_core_forward_calls=432))
    return records,data


def helpers():
    pairs=NS(pairs_from_rows=pairs_from_rows);wide=NS(schedule_stats=schedule_stats,score_length=lambda data,raw,c:raw)
    diag=NS(normalize_task=lambda scored,*_:scored["totals"],partition=lambda rows:{k:v for k,v in rows[0].items() if k!="split"})
    return pairs,wide,diag,NS()


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB;pins[b.WIDE_SOURCE]=b.WIDE_BLOB
    while len(pins)<682:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1267)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):return Path(root)/name
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch":return b"feat/sft-target-loss\n"
        return b""


def payload(summary):
    pins,protected=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,gate_f_candidate=False,production_adoption=False,source_blobs=pins,input_sha256=protected,
        artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary)


@dataclass(frozen=True)
class Config:
    width:int=16
    max_tokens:int=48
    slots:int=48
    next_route:int=0
    instruction_route:int=1
    internal_steps:int=2


class Encoder(nn.Module):
    def __init__(self):super().__init__();self.embed=nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,x):return (self.embed(x),)


class Core(nn.Module):
    def __init__(self):
        super().__init__();self.linear=nn.Linear(16,16,dtype=torch.float64);self.config=Config()
        self.padding=nn.Parameter(torch.zeros(3328-272,dtype=torch.float64))
    def forward(self,state,local,route_index):return torch.tanh(self.linear(state)+.1*local)


class Backbone(nn.Module):
    def __init__(self,seed):
        super().__init__();torch.manual_seed(seed);self.local_encoder=Encoder();self.core=Core();self.config=Config()
        self.readout_norm=nn.LayerNorm(16,dtype=torch.float64);self.classifier=nn.Linear(16,256,dtype=torch.float64)
        self.padding=nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x,tasks):
        valid=x!=256;local=self.local_encoder(x)[0]*valid[:,:,None];state=local
        for _ in range(2):
            nxt=self.core(state,local,route_index=0);self.core(state,local,route_index=1);state=nxt
        return self.classifier(self.readout_norm(state[torch.arange(len(x)),valid.sum(1)-1]))


class Ref(nn.Module):
    def __init__(self,backbone,seed,*_):
        super().__init__();self.backbone=backbone;self.read=nn.Module();torch.manual_seed(seed+1)
        for n in ("query","key","output"):setattr(self.read,n,nn.Linear(16,16,bias=False,dtype=torch.float64))


def actual_wide_helpers():
    # Extract accepted definitions without executing its artifact-loader graph.
    path=Path(__file__).resolve().parents[1]/b.WIDE_SOURCE
    tree=ast.parse(path.read_text(encoding="utf-8"));wanted={"LengthReadout","span_mask","prefix_tensor","schedule_stats","evaluate","replay_error","replay_one"}
    nodes=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in wanted]
    assert {n.name for n in nodes}==wanted
    space=dict(torch=torch,nn=nn,Counter=Counter,copy=copy,replace=replace,require=b.require,digest=b.digest,
        SLOTS=64,EVAL_LENGTHS=(2,3,4,5),SPLITS=("TRAIN","HOLDOUT"),PROFILES=("repeat","shared_prefix","shared_suffix"),
        VIEWS=("normal","evidence_blind","query_blind"),itertools=itertools,__name__="c306_parent_definition_fixture")
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),"exec"),space)
    return NS(**{n:space[n] for n in wanted})


class C306Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.records,cls.data=records_fixture();cls.pairs,cls.wide,cls.diag,cls.c=helpers();cls.x,cls.y=tables(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.data,cls.pairs,cls.wide,cls.diag,cls.c)
        torch.manual_seed(123);cls.initial=Toy();cls.models={a:b.configure(copy.deepcopy(cls.initial),a) for a in b.ARMS};cls.fits={}
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:cls.fits[arm]=b.fit(cls.models[arm],cls.data,cls.x,cls.y,b.SEEDS[0],arm,cls.pairs,cls.wide)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
    def test_02_bad_seal(self):
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError):b.validate_seal()
    def test_03_actual_readout_factory_partition(self):
        wide=actual_wide_helpers();c=NS(c278=NS(MeanFinalDualReadout=Ref),factory=NS(new_model=Backbone),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        models=b.make_models(b.SEEDS[0],wide,c)
        self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        self.assertEqual([sum(p.numel() for p in m.parameters() if p.requires_grad) for m in models.values()],[14256,10928])
        ptrs=[p.data_ptr() for m in models.values() for p in m.parameters()];self.assertEqual(len(ptrs),len(set(ptrs)))
        for m in models.values():self.assertEqual((m.backbone.config.max_tokens,m.backbone.core.config.slots),(64,64))
    def test_04_initial_probe_noncore_backward(self):
        wide=actual_wide_helpers();c=NS(c278=NS(MeanFinalDualReadout=Ref),factory=NS(new_model=Backbone),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        models=b.make_models(b.SEEDS[0],wide,c);x=wide.prefix_tensor("aa=0;bb=1;aa=").expand(3,3,192,64).clone()
        result=b.first_batch_probe(models,x,self.y,b.schedule(b.SEEDS[0],self.data["TRAIN"],self.pairs))
        self.assertEqual(result["frozen_core_gradient_tensors"],0);self.assertTrue(result["encoder_receives_signal"])
        self.assertLessEqual(result["max_noncore_gradient_error"],1e-9)
    def test_05_configure_unchanged_state(self):
        m=copy.deepcopy(self.initial);before=fingerprint(m);b.configure(m,"core_frozen")
        self.assertEqual(before,fingerprint(m));self.assertFalse(any(p.requires_grad for p in m.backbone.core.parameters()))
        b.configure(m,"full_train");self.assertTrue(all(p.requires_grad for p in m.parameters()))
        with self.assertRaises(ValueError):b.configure(m,"wrong")
    def test_06_bad_factory_seed(self):
        with self.assertRaises(ValueError):b.make_models(304001,None,None)
    def test_07_all_schedules_equal_exposure(self):
        for seed in b.SEEDS:
            events=b.schedule(seed,self.data["TRAIN"],self.pairs);stats=schedule_stats(events)
            self.assertEqual(stats["per_length_row_exposures"],[[100]*192]*3)
            self.assertEqual([sum(r[i] for r in stats["length_profile_updates"]) for i in range(3)],[400]*3)
            self.assertTrue(all(v>0 for r in stats["length_profile_updates"] for v in r))
    def test_08_independent_schedule_reference(self):
        pp=pairs_from_rows(self.data["TRAIN"]);got=b.schedule(b.SEEDS[0],self.data["TRAIN"],self.pairs)
        for epoch in (0,1,2,3,299):
            perm=torch.randperm(96,generator=torch.Generator().manual_seed(b.ORDERS[0]+306000+epoch))
            self.assertTrue(torch.equal(got[4*epoch:4*epoch+4,:,2:].reshape(96,2),pp[perm]))
            self.assertTrue(bool((got[4*epoch:4*epoch+4,:,0]==epoch%3).all()))
    def test_09_seed_order_independence(self):
        a=b.schedule(b.SEEDS[0],self.data["TRAIN"],self.pairs);torch.manual_seed(999)
        self.assertTrue(torch.equal(a,b.schedule(b.SEEDS[0],self.data["TRAIN"],self.pairs)))
        self.assertFalse(torch.equal(a[:,:,2:],b.schedule(b.SEEDS[1],self.data["TRAIN"],self.pairs)[:,:,2:]))
    def test_10_invalid_pairing(self):
        bad=NS(pairs_from_rows=lambda rows:torch.zeros((96,2),dtype=torch.int64))
        with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],self.data["TRAIN"],bad)
        with self.assertRaises(ValueError):b.schedule(1,self.data["TRAIN"],self.pairs)
    def test_11_two_real_1200_step_loops(self):
        for arm,m in self.models.items():
            b.check_fit(self.fits[arm],b.SEEDS[0],arm,self.data,self.pairs,self.wide)
            self.assertEqual((m.calls,m.rows),(1200,57600));self.assertFalse(m.training)
            self.assertLess(self.fits[arm]["ce_history"][-1],self.fits[arm]["ce_history"][0])
            self.assertEqual(fingerprint(m.backbone.core)==fingerprint(self.initial.backbone.core),arm==b.ARMS[1])
    def test_12_determinism_and_optimizer_steps(self):
        m=b.configure(copy.deepcopy(self.initial),b.ARMS[1]);real=torch.optim.AdamW;created=[]
        def create(*a,**kw):o=real(*a,**kw);created.append(o);return o
        with patch.object(torch.optim,"AdamW",side_effect=create),contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[1],self.pairs,self.wide)
        self.assertEqual(len(created),1);self.assertEqual({int(v["step"]) for v in created[0].state.values()},{1200})
        self.assertEqual(f["ce_history"],self.fits[b.ARMS[1]]["ce_history"])
        coreptrs={p.data_ptr() for p in m.backbone.core.parameters()}
        self.assertFalse(coreptrs&{p.data_ptr() for p in created[0].param_groups[0]["params"]})
    def test_13_training_rejects_target_and_policy(self):
        bad=self.y.clone();bad[0]=99
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,bad,b.SEEDS[0],b.ARMS[0],self.pairs,self.wide)
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,self.y,b.SEEDS[0],b.ARMS[1],self.pairs,self.wide)
    def test_14_fit_metadata_tampering(self):
        for fn in (lambda f:f.update(optimizer_creations=2),lambda f:f["ce_history"].__setitem__(0,float("nan")),lambda f:f["gradient_union"].update({"backbone.core.weight":1})):
            f=copy.deepcopy(self.fits[b.ARMS[1]]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],b.ARMS[1],self.data,self.pairs,self.wide)
    def test_15_actual_train_one_and_parent_replay(self):
        m=b.configure(copy.deepcopy(self.initial),b.ARMS[1]);wide=actual_wide_helpers()
        @contextlib.contextmanager
        def counted(model,_):
            initial=(model.calls,model.rows);calls=[0,0];cores=[0];yield calls,cores
            calls[:]=[model.calls-initial[0],model.rows-initial[1]];cores[0]=4*calls[0]
        c=NS(base=NS(fingerprint=fingerprint),core=None,p267=NS(counted=counted,check_logits=lambda z,n:b.require(z.shape==(n,256) and bool(torch.isfinite(z).all()),"fixture logits")))
        prompts={str(n):{s:{p:[dict(views={v:"\x00" for v in ("normal","evidence_blind","query_blind")}) for r in rr] for p in ("repeat","shared_prefix","shared_suffix")} for s,rr in self.data.items()} for n in b.LENGTHS}
        # Parent evaluator's valid BOS257 would exceed the target-coded toy's four-entry embedding.
        class EvaluationToy(Toy):
            def forward(self,x,tasks):
                xx=x.clone();xx[:,0]%=4;return super().forward(xx,tasks)
        m=b.configure(EvaluationToy(),b.ARMS[1]);m.load_state_dict(self.initial.state_dict())
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_one(m,self.data,prompts,self.x,self.y,b.SEEDS[0],b.ARMS[1],self.pairs,wide,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(1308,67968))
        fresh=b.configure(EvaluationToy(),b.ARMS[1]);wide.replay_one(fresh,state,r,prompts,self.data,c)
        self.assertTrue(r["checkpoint_roundtrip"]);self.assertEqual(r["reload_max_error"],0.)
    def test_16_analysis_and_one_failed_seed(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(10,80,40))
        r=copy.deepcopy(self.records);r[1]["raw"]["5"]["passed"]=False
        _,s=b.analyze(r,self.data,self.pairs,self.wide,self.diag,self.c);self.assertFalse(s["candidate_gate"]);b.validate_result(payload(s))
    def test_17_core_and_pair_tamper(self):
        for fn in (lambda r:r[1].update(core_final_sha256="z"*64),lambda r:r[1].update(initial_sha256="z"*64),lambda r:r[1].update(reload_max_error=.1)):
            r=copy.deepcopy(self.records);fn(r)
            with self.assertRaises(ValueError):b.analyze(r,self.data,self.pairs,self.wide,self.diag,self.c)
    def test_18_result_contract(self):
        b.validate_result(payload(self.summary))
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(models=False),lambda p:p["validation_summary"]["contrasts"].pop()):
            p=payload(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c306-fixture")/str(i)/"summary.json").resolve() for i in range(32)]
        parent=NS(PARENT_SHA="c"*64,OUTPUTS=("audit-plan.json","aligned-answers.json","validation-summary.json"),no_neural=contextlib.nullcontext,expected_flags=lambda:["fixed"],validate_result=Mock(),verify_artifacts=Mock())
        wide=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(30)),prompt_dataset=lambda d:{"fixture":1},validate_prompts=Mock())
        p=dict(experiment_id="C305-v5b-saved-length-error-overlap",commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB},
            artifacts=[dict(file=n) for n in parent.OUTPUTS],validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False,parent_flags=["fixed"],reconciled_totals=720,reconciled_partitions=120))
        parent.verify_artifacts.return_value=p
        mapping=dict(zip(map(str,paths),(b.PARENT_SHA,parent.PARENT_SHA,*wide.parent_hashes(None)),strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:self.data))
        with patch.object(b,"context",return_value=(parent,wide,None,None,None,c)):yield paths,mapping,parent,p
    def test_19_32_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p):
            self.assertEqual(b.load_parent(paths)[0],p);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="f"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old
    def test_20_parent_return_schema_and_scope(self):
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p["source_blobs"].pop(b.WIDE_SOURCE),lambda p:p["artifacts"].pop()):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError):b.load_parent(paths)
    def test_21_protection_and_unpinned_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB}
            while len(pins)<676:pins["accepted/"+str(len(pins))]="b"*40
            for n in list(pins)+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1257-len(protected)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");protected[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();path=directory/"summary.json";path.write_text("summary",encoding="utf-8");mapping={str(path.resolve()):b.PARENT_SHA};artifacts=[]
            for i in range(3):p=directory/str(i);p.write_text("artifact",encoding="utf-8");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=str(i),sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE)
            wide=NS(PINNED={b.WIDE_SOURCE:b.WIDE_BLOB},context=lambda:())
            c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"c"*40)+"\n").encode(),safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            p=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,wide,None,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*32,root))),(682,1267))
                c.missing=types.ModuleType("missing");c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected"):b.precheck([path]*32,root)
    def test_22_runtime_preflight_path(self):
        wide=NS(training_tables=lambda _: (self.x,self.y),schedule_stats=schedule_stats)
        models={a:b.configure(copy.deepcopy(self.initial),a) for a in b.ARMS}
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(None,wide,self.pairs,None,None,None)),patch.object(b,"load_parent",return_value=({},self.data,{})),patch.object(b,"make_models",return_value=models),contextlib.redirect_stdout(io.StringIO()):b.runtime_preflight(["x"]*32,Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        events=[];c=NS(audit=Audit());records=copy.deepcopy(self.records);pairs,wide,diag,_=helpers()
        def train(*a):events.append("train");return records[b.identities().index((a[5],a[6]))],{}
        def replay(*a):events.append("replay")
        def pc(*a):events.append("precheck");return protection()
        wide.training_tables=lambda d:(self.x,self.y);wide.replay_one=replay
        with patch.object(b,"context",return_value=(NS(no_neural=contextlib.nullcontext),wide,pairs,diag,None,c)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",return_value=({},self.data,{"prompts":1})),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS)),patch.object(b,"train_one",side_effect=train):yield events
    def test_23_production_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*32,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[0],"precheck");self.assertEqual(events.count("train"),10);self.assertEqual(events.count("replay"),10)
            self.assertLess(max(i for i,e in enumerate(events) if e=="train"),events.index("replay"))
            q,_=b.verify_artifacts(out,["x"]*32,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*32,output_dir=out,expected_head="f"*40)
    def test_24_byte_and_semantic_tampering(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*32,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*32,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*32,"f"*40)
    def test_25_bundle_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"m.pt";p=dict(schema="fold-c306-broad-core-models-v1",slots=64,identities=[list(i) for i in b.identities()],states=[{}]*10)
            torch.save(p,path);self.assertEqual(len(b.load_bundle(path)),10);p["slots"]=48;torch.save(p,path)
            with self.assertRaises(ValueError):b.load_bundle(path)
    def test_26_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(4813)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4813);self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())
    def test_27_cli_and_context(self):
        args=["p","--summaries"]+[str(i) for i in range(32)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),32)
        p301=NS(context=lambda:(None,),pair_source=lambda _:3);wide=NS(context=lambda:(None,p301,None,4,5,6));parent=NS(context=lambda:(wide,6))
        pkg=types.ModuleType("fold_lm.v05_benchmarks");pkg.model_c305_saved_length_overlap=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":pkg}):self.assertEqual(b.context(),(parent,wide,3,4,5,6))
    def test_28_guard_and_modules(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
        with patch.object(b,"context",return_value=(NS(regression_modules=lambda _:[str(i) for i in range(190)]),)):
            self.assertEqual(len(b.regression_modules(Path.cwd())),191)
    def test_29_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))
    def test_30_runner_contract(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:34]",blocks[2]);self.assertIn("head = sys.argv[34]",blocks[2])
        self.assertEqual(len(re.findall(r"runs\\c\d{3}-.*?\\summary.json",launcher)),32)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
    def test_31_source_is_not_detached_forward(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"));node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="configure")
        self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr=="detach" for n in ast.walk(node)))
        # Behavioral confirmation: zeroing all local encoder gradients breaks the probe.
        models={a:b.configure(copy.deepcopy(self.initial),a) for a in b.ARMS}
        with torch.no_grad():models[b.ARMS[1]].backbone.local_encoder.weight.zero_()
        with self.assertRaises(ValueError):b.first_batch_probe(models,self.x,self.y,b.schedule(b.SEEDS[0],self.data["TRAIN"],self.pairs))
    def test_32_imports_and_test_count(self):
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c305_saved_length_overlap"]);self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)


if __name__=="__main__":unittest.main()
