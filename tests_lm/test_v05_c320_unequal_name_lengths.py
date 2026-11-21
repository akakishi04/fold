"""C320 software controls; substitute scores/models are not real FOLD evidence."""
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
from fold_lm.v05_benchmarks import model_c320_unequal_name_lengths as b


def profiles(n): return b.PROFILES[:1] if n==1 else b.PROFILES


def dataset():
    out={s:[] for s in b.SPLITS}
    for ent,val,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (val[1]-val[0])%4==2 else "TRAIN"
        for order,q in itertools.product((ent,ent[::-1]),ent):
            out[split].append(dict(id=f"{lang}:{ent}:{val}:{order}:{q}",entities=list(ent),values=list(val),language=lang,permutation=list(order),query=q,target=48+val[ent.index(q)]))
    return out


def old_prompts(data):
    def render(r,n,p,v):
        i,j=r["entities"]; chars="abc" if r["language"]=="en" else "甲乙丙"
        a=chars[i]*n; z=chars[j]*n if p=="repeat" else chars[i]*(n-1)+chars[j] if p=="shared_prefix" else chars[j]+chars[i]*(n-1)
        names={i:a,j:z}; values=dict(zip(r["entities"],r["values"],strict=True))
        return ";".join(f"{names[k]}="+("?" if v=="evidence_blind" else str(values[k])) for k in r["permutation"])+";"+("?" if v=="query_blind" else names[r["query"]])+"="
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in b.VIEWS}) for r in data[s]] for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def accepted_functions():
    root=Path(__file__).resolve().parents[1]
    def extract(path,names,env):
        tree=ast.parse((root/path).read_text(encoding="utf-8")); nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
        assert {n.name for n in nodes}==set(names)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),"exec"),env); return NS(**{n:env[n] for n in names})
    env=dict(torch=torch,require=b.require,ARMS=b.ARMS,contextmanager=contextlib.contextmanager)
    p=extract(b.PARENT_SOURCE,("trained_readout","hook_snapshot"),env)
    env=dict(torch=torch,require=b.require,SPLITS=b.SPLITS,VIEWS=b.VIEWS,itertools=itertools,profiles=profiles)
    p315=extract("fold_lm/v05_benchmarks/model_c315_single_character_mix.py",("evaluate","validate_raw","replay_error"),env); p315.profiles=profiles; p315.context=lambda:()
    env=dict(torch=torch,require=b.require,SLOTS=64,Counter=Counter,SPLITS=b.SPLITS,PROFILES=b.PROFILES,LEGACY_PROFILES={3:("tripled","shared_prefix2","shared_suffix2")})
    wide=extract(b.WIDE_SOURCE,("span_mask","score_length"),env)
    tree=ast.parse((root/b.WIDE_SOURCE).read_text(encoding="utf-8")); cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="LengthReadout")
    node=copy.deepcopy(next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="forward"))
    exec(compile(ast.Module(body=[node],type_ignores=[]),"accepted_C304_forward","exec"),env)
    return p,p315,wide,env["forward"]


def fingerprint(model):
    h=hashlib.sha256()
    for n,z in sorted(model.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def check_logits(z,n):
    b.require(isinstance(z,torch.Tensor) and z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")


class Encoder(torch.nn.Module):
    def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,tokens): return (self.embed(tokens),)
class Core(torch.nn.Module):
    def __init__(self): super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
    def forward(self,state,local,route_index): return torch.tanh(self.linear(state)+local*.1)
class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder=Encoder(); self.core=Core(); self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64); self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.config=NS(max_tokens=64,width=16,next_route=0,instruction_route=1,internal_steps=2)
    def forward(self,tokens,tasks):
        valid=tokens!=256; local=self.local_encoder(tokens)[0]*valid[:,:,None]; state=local
        for _ in range(2): state=self.core(state,local,route_index=0); self.core(state,local,route_index=1)
        return self.classifier(self.readout_norm(state[torch.arange(len(tokens)),valid.sum(1)-1]))
class Toy(torch.nn.Module):
    def __init__(self,forward):
        super().__init__(); self.backbone=Backbone(); self.read=torch.nn.Module()
        for n in ("key","query","output"): setattr(self.read,n,torch.nn.Linear(16,16,bias=False,dtype=torch.float64))
        self.forward=types.MethodType(forward,self)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def mh(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def ch(*a): cores[0]+=1
    h=model.register_forward_hook(mh); k=model.backbone.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: h.remove(); k.remove()
class Audit:
    @staticmethod
    def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name): return Path(root)/name
@contextlib.contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("model forbidden")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("load forbidden")): yield


def fixture_context():
    p,p315,wide,forward=accepted_functions()
    def score(data,raw,c):
        totals=[]
        for split in b.SPLITS:
            y=torch.tensor([r["target"] for r in data[split]]); correct=sum(int((z["normal"].argmax(1)==y).sum()) for z in raw[split].values())
            totals.append(dict(split=split,rows=3*len(y),correct=correct,full_pass=correct==3*len(y),direct_pass=correct==3*len(y)))
        return dict(passed=all(r["full_pass"] for r in totals),totals=totals)
    wide.prefix_tensor=prefix; wide.context=lambda:()
    x=NS(parent=p315,wide=wide,p312=NS(context=lambda:()),guarded=NS(no_neural=no_neural),diag=NS(normalize_task=lambda z,*a:z["totals"],partition=lambda r:{k:v for k,v in r[0].items() if k!="split"}),
        c=NS(audit=Audit(),base=NS(fingerprint=fingerprint),p267=NS(check_logits=check_logits,counted=counted,validate_data=lambda _:None),c270=NS(score=score),core=None,factory=NS(language_module=lambda:None)))
    return p,x,forward


def partition_raw(data,profile_names=b.PROFILES,fail=False):
    out={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in data[s]]); z[torch.arange(len(y)),y]=4.
        if fail and s=="HOLDOUT": z[0,70]=9.
        out[s]={p:{v:z for v in b.VIEWS} for p in profile_names}
    return out


def fixtures(data):
    anchors=[]; rr=[]; normal=partition_raw(data); failure=partition_raw(data,fail=True); single=partition_raw(data,b.PROFILES[:1])
    for f in b.expected_parent_results():
        old={str(n):single if n==1 else normal if f["length_pass"][str(n)] else failure for n in range(1,7)}
        key=dict(seed=f["seed"],arm=f["arm"],readout_policy=f["arm"],final_sha256=b.digest([f["seed"],f["arm"]]))
        anchors.append(dict(**key,raw=old)); rr.append(dict(**key,raw=dict(before=old,unequal=dict.fromkeys(b.LAYOUTS,normal),after=old),
            receipts={m:dict(calls=c,query_calls=2*c,rows=96*c,grad_calls=0) for m,c in (("before",144),("unequal",54),("after",144))},
            replay_errors=[0.,0.],weights_preserved=True,hooks_restored=True))
    return anchors,rr


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update({b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB})
    while len(pins)<766: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1443)}


def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if s["primary_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False)


class C320Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); cls.rng=torch.get_rng_state(); torch.set_num_threads(2)
        cls.data=dataset(); cls.old=old_prompts(cls.data); cls.new=b.new_prompts(cls.data); cls.p,cls.x,cls.forward_fn=fixture_context(); cls.anchors,cls.records=fixtures(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,cls.x)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det); torch.set_rng_state(cls.rng)
    def toy(self):
        torch.manual_seed(10); m=Toy(type(self).forward_fn); m.eval(); m.requires_grad_(False); return m
    def test_01_manifest_and_input_hashes(self):
        b.validate_seal(); self.assertEqual(b.digest(self.data),b.DATA_SHA); self.assertEqual(b.digest(self.old),b.PROMPTS_SHA)
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()
    def test_02_all_prompt_and_native_span_contracts(self): b.check_prompts(self.data,self.old,self.new,self.x)
    def test_03_unequal_lengths_targets_and_order(self):
        for k,s,p in itertools.product(b.LAYOUTS,b.SPLITS,b.PROFILES):
            for row,item in zip(self.data[s],self.new[k][s][p],strict=True):
                facts,query=item["views"]["normal"].rsplit(";",1); parsed={n:int(v) for n,v in (t.split("=") for t in facts.split(";"))}
                self.assertEqual(sorted(map(len,parsed)),[2,4]); self.assertEqual(48+parsed[query[:-1]],row["target"])
                lens=dict(zip(row["entities"],b.LAYOUTS[k],strict=True)); self.assertEqual([len(t.split("=")[0]) for t in facts.split(";")],[lens[e] for e in row["permutation"]])
    def test_04_mask_semantics_and_no_target_render_dependency(self):
        row=copy.deepcopy(self.data["TRAIN"][0]); before=b.render(row,(2,4),"shared_suffix"); row["target"]=999
        self.assertEqual(before,b.render(row,(2,4),"shared_suffix"))
        self.assertEqual(b.render(row,(2,4),"repeat","evidence_blind").count("?"),2)
        self.assertTrue(b.render(row,(4,2),"repeat","query_blind").endswith(";?="))
    def test_05_invalid_render_or_prompt(self):
        for lens in ((0,4),(2,7),(True,4)):
            with self.assertRaises(ValueError): b.render(self.data["TRAIN"][0],lens,"repeat")
        new=copy.deepcopy(self.new); new["short_long"]["TRAIN"]["repeat"][0]["views"]["normal"]="changed"
        with self.assertRaises(ValueError): b.check_prompts(self.data,self.old,new,self.x)
    def test_06_frozen_evaluator_and_raw_domain(self):
        with self.assertRaises(ValueError): b.evaluate_new(self.toy(),self.new,self.data,self.x)
        bad=copy.deepcopy(self.records[0]["raw"]["unequal"]); bad.pop("long_short")
        with self.assertRaises(ValueError): b.validate_new(bad,self.data,self.x)
    def test_07_actual_pipeline_both_trained_policies(self):
        for arm in b.ARMS:
            m=self.toy()
            with torch.no_grad(),self.p.trained_readout(m,self.x.wide,arm): raw=self.x.parent.evaluate(m,self.old,self.data,self.x.wide,self.x.c)
            anchor=dict(seed=b.SEEDS[0],arm=arm,readout_policy=arm,final_sha256=fingerprint(m),raw=raw)
            with contextlib.redirect_stdout(io.StringIO()): r=b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.new,self.p,self.x)
            self.assertEqual(r["replay_errors"],[0.,0.]); self.assertEqual(r["receipts"]["unequal"]["calls"],54)
            self.assertEqual(fingerprint(m),anchor["final_sha256"])
    def test_08_strict_checkpoint_and_policy(self):
        m=self.toy(); anchor=dict(seed=b.SEEDS[0],arm="last_only",readout_policy="mean_last",final_sha256=fingerprint(m))
        with self.assertRaises(ValueError): b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.new,self.p,self.x)
        anchor["readout_policy"]="last_only"; anchor["final_sha256"]="wrong"
        with self.assertRaises(ValueError): b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.new,self.p,self.x)
    def test_09_reports_primary_and_scope(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["reproductions"])),(20,40,10)); b.validate_result(payload(self.summary))
        for key,val in (("gate_f_candidate",True),("production_adoption",True)):
            p=payload(self.summary); p[key]=val
            with self.assertRaises(ValueError): b.validate_result(p)
    def test_10_no_primary_swap_or_layout_averaging(self):
        rr=copy.deepcopy(self.records); rr[0]["raw"]["unequal"]["long_short"]=partition_raw(self.data,fail=True)
        _,s=b.analyze(rr,self.anchors,self.data,self.x); self.assertFalse(s["primary_gate"]); self.assertEqual(s["all_layouts_counts"]["last_only"],5); b.validate_result(payload(s))
        rr=copy.deepcopy(self.records); rr[1]["raw"]["unequal"]["short_long"]=partition_raw(self.data,fail=True)
        _,s=b.analyze(rr,self.anchors,self.data,self.x); self.assertTrue(s["primary_gate"])
    def test_11_corrupt_receipts_replays_cohort(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.anchors,self.data,self.x)
        for key,val in (("weights_preserved",False),("readout_policy","wrong"),("replay_errors",[.1,0.])):
            rr=copy.deepcopy(self.records); rr[0][key]=val
            with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.x)
    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c320-fixture")/str(i)/"summary.json").resolve() for i in range(46)]
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*[str(i%10)*64 for i in range(45)]),strict=True))
        outputs=("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
        evidence=dict(experiment_id="C319-v5b-trained-last-readout",commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n) for n in outputs],
            validation_summary=dict(seed_results=b.expected_parent_results(),candidate_gate=False,all_pairs_matched=True,all_replays=True))
        tail=tuple(list(hashes.values())[1:])
        p=NS(context=lambda:(),parent_hashes=lambda:tail,verify_artifacts=Mock(return_value=(evidence,[])),validate_result=Mock(),OUTPUTS=outputs)
        x=copy.copy(self.x); x.c=copy.copy(x.c); x.c.audit=NS(sha=lambda v:hashes[str(v)],read_json=lambda path:self.data if path.name=="dataset.json" else self.old)
        archive=dict(schema="fold-c319-trained-readout-eval-v1",records=self.anchors)
        with patch.object(b,"context",return_value=(p,x)),patch.object(torch,"load",return_value=archive): yield paths,hashes,p,evidence,archive
    def test_12_all46_parent_hash_guards(self):
        with self.loader_fixture() as (paths,hashes,p,e,a):
            self.assertEqual(b.load_parent(paths)[0],e); p.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; p.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                p.verify_artifacts.assert_not_called(); hashes[str(path)]=old
    def test_13_parent_schema_and_outcomes(self):
        for fn in (lambda e,a:e.update(status="PASS"),lambda e,a:a.update(schema="wrong"),lambda e,a:e["artifacts"].pop()):
            with self.loader_fixture() as (paths,_,p,e,a):
                fn(e,a)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_14_precheck_all_source_and_input_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB}
            while len(pins)<760: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): path=root/n; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1429-len(inputs)):
                path=root/("input"+str(i)); path.write_text("input",encoding="utf-8"); inputs[str(path)]=Audit.sha(path)
            folder=root/"parent"; folder.mkdir(); summary=folder/"summary.json"; summary.write_text("summary",encoding="utf-8"); artifacts=[]
            for i in range(7):
                path=folder/("artifact"+str(i)); path.write_text("data",encoding="utf-8"); artifacts.append(dict(file=path.name,sha256=Audit.sha(path)))
            def sha(path): return b.PARENT_SHA if Path(path)==summary else Audit.sha(path)
            p=types.ModuleType("parent"); p.__file__=str(root/b.PARENT_SOURCE); p.context=lambda:()
            x=NS(parent=NS(context=lambda:()),p312=NS(context=lambda:()),wide=NS(context=lambda:()),c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,
                git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp})))
            with patch.object(b,"context",return_value=(p,x)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*46,root))),(766,1443)); x.c.missing=types.ModuleType("missing"); x.c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([summary]*46,root)
    @contextlib.contextmanager
    def run_fixture(self):
        events=[]
        def load(path): events.append(("load",path)); return [{}]*10
        def infer(*a): events.append(("infer",a[2]["arm"])); return self.records[b.identities().index((a[2]["seed"],a[2]["arm"]))]
        p=NS(context=lambda:(None,NS(guard=lambda *a:None)),load_bundle=load,make_models=lambda *a:dict.fromkeys(b.ARMS))
        with patch.object(b,"context",return_value=(p,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.old,self.anchors)),patch.object(b,"infer_one",side_effect=infer): yield events
    def test_15_run_loader_policy_and_no_training(self):
        saved=[]; save=torch.save
        def saver(obj,path): saved.append(Path(path).name); save(obj,path)
        paths=["C319/summary.json"]+["ancestor"]*45
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=saver),patch.object(torch.optim,"AdamW",side_effect=AssertionError("training")),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=paths,output_dir=out,expected_head="f"*40)
            self.assertEqual([v for k,v in events if k=="load"],[Path(paths[0]).resolve().parent/"trained-models.pt"]); self.assertEqual(sum(k=="infer" for k,v in events),10); self.assertEqual(saved,["evaluations.pt"])
            q,_=b.verify_artifacts(out,paths,"f"*40); self.assertEqual(p,q)
    def test_16_hash_and_resealed_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*46,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*46,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*46,"f"*40)
    def test_17_no_overwrite(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()),self.assertRaises(FileExistsError): b.run(summaries=["x"]*46,output_dir=tmp,expected_head="f"*40)
    def test_18_real_policy_smoke_path(self):
        models={a:self.toy() for a in b.ARMS}; states=[m.state_dict() for m in models.values()]; anchors=[dict(final_sha256=fingerprint(m)) for m in models.values()]
        p=NS(load_bundle=lambda path:states,make_models=lambda *a:models,trained_readout=self.p.trained_readout)
        with patch.object(b,"context",return_value=(p,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.old,anchors)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*46,Path.cwd())
    def test_19_suite_semantic_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5221)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())
    def test_20_cli_context_and_module_count(self):
        argv=["program","--summaries"]+[str(i) for i in range(46)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),46)
        p=NS(context=lambda:(None,None,None,"x"),regression_modules=lambda root:["m"+str(i) for i in range(204)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c319_trained_last_readout=p
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(p,"x")); self.assertEqual(len(b.regression_modules(Path.cwd())),205)
    def test_21_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))
    def test_22_runner_cli_and_paths(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"embedded","exec")
        self.assertIn("sys.argv[2:48]",blocks[2]); self.assertIn("head = sys.argv[48]",blocks[2]); self.assertIn("len(sys.argv) == 49",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(319,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
    def test_23_scorer_reuses_logical_profile_adapter(self):
        scorer=Mock(return_value=dict(passed=True)); c=NS(c270=NS(score=scorer),p267=object()); raw=partition_raw(self.data)
        self.assertEqual(self.x.wide.score_length(self.data,raw,c),dict(passed=True))
        adapted=scorer.call_args.args[1]; self.assertIs(adapted["TRAIN"]["tripled"],raw["TRAIN"]["repeat"])
    def test_24_count_payload_and_protection(self):
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24)
        self.assertEqual(b.manifest()["raw_logit_payload_bytes"],10*(144+54+144)*96*256*8)
        p=payload(copy.deepcopy(self.summary)); p["validation_summary"]["train_steps"]=False
        with self.assertRaises(ValueError): b.validate_result(p)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c319_trained_last_readout"])


if __name__=="__main__": unittest.main()
