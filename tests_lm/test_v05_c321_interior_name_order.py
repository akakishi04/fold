"""C321 software controls. Synthetic models and scores are not FOLD capability evidence."""
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
import subprocess
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c321_interior_name_order as b

OLD=b.SCORER_PROFILES

def profiles(n): return OLD[:1] if n==1 else OLD

def dataset():
    out={s:[] for s in b.SPLITS}
    for ent,val,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (val[1]-val[0])%4==2 else "TRAIN"
        for order,q in itertools.product((ent,ent[::-1]),ent):
            out[split].append(dict(id=f"{lang}:{ent}:{val}:{order}:{q}",entities=list(ent),values=list(val),language=lang,permutation=list(order),query=q,target=48+val[ent.index(q)]))
    return out

def old_prompts(data):
    def render(r,n,p,v):
        i,j=r["entities"]; chars="abc" if r["language"]=="en" else "甲乙丙"; u,w=chars[i],chars[j]
        names={i:u*n,j:w*n if p==OLD[0] else u*(n-1)+w if p==OLD[1] else w+u*(n-1)}
        values=dict(zip(r["entities"],r["values"],strict=True))
        return ";".join(names[k]+"="+("?" if v=="evidence_blind" else str(values[k])) for k in r["permutation"])+";"+("?" if v=="query_blind" else names[r["query"]])+"="
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in b.VIEWS}) for r in data[s]] for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}

def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)

def check_logits(z,n):
    b.require(isinstance(z,torch.Tensor) and z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")

def fingerprint(m):
    h=hashlib.sha256()
    for n,z in sorted(m.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

class Audit:
    @staticmethod
    def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else "a"*64
    @staticmethod
    def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n

@contextlib.contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("model forbidden")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("state forbidden")): yield

@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def mh(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def ch(*_): cores[0]+=1
    a=model.register_forward_hook(mh); c=model.backbone.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: a.remove(); c.remove()


def accepted_functions():
    root=Path(__file__).resolve().parents[1]; base=root/"fold_lm/v05_benchmarks"
    env=dict(torch=torch,require=b.require,Counter=Counter,SLOTS=64,SPLITS=b.SPLITS,PROFILES=OLD,LEGACY_PROFILES={3:("tripled","shared_prefix2","shared_suffix2")})
    tree=ast.parse((base/"model_c304_length_breadth.py").read_text(encoding="utf-8"))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="LengthReadout")
    forward=copy.deepcopy(next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="forward")); forward.name="forward"
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ("span_mask","score_length")]+[forward]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"C304 accepted functions","exec"),env)
    env315=dict(torch=torch,require=b.require,itertools=itertools,SPLITS=b.SPLITS,VIEWS=b.VIEWS,profiles=profiles)
    tree=ast.parse((base/"model_c315_single_character_mix.py").read_text(encoding="utf-8"))
    names=("evaluate","validate_raw","replay_error"); nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"C315 accepted functions","exec"),env315)
    env319=dict(torch=torch,require=b.require,contextmanager=contextlib.contextmanager,ARMS=b.ARMS)
    tree=ast.parse((base/"model_c319_trained_last_readout.py").read_text(encoding="utf-8"))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ("hook_snapshot","trained_readout")]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"C319 accepted functions","exec"),env319)
    return env,NS(**{n:env315[n] for n in names},profiles=profiles,context=lambda:()),NS(**{n:env319[n] for n in ("hook_snapshot","trained_readout")},context=lambda:(None,NS(guard=lambda *a:None)))

class Encoder(torch.nn.Module):
    def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,tokens): return (self.embed(tokens),)
class Core(torch.nn.Module):
    def __init__(self): super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
    def forward(self,state,local,route_index): return torch.tanh(self.linear(state)+.1*local)
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


def logical_score(data,raw,c):
    totals=[]
    for s in b.SPLITS:
        y=torch.tensor([r["target"] for r in data[s]])
        correct=sum(int((raw[s][p]["normal"].argmax(1)==y).sum()) for p in raw[s]); rows=3*len(y)
        totals.append(dict(split=s,rows=rows,correct=correct,direct_pass=correct==rows,full_pass=correct==rows))
    return dict(passed=all(r["full_pass"] for r in totals),totals=totals)

def new_raw(data,labels=b.PROFILES,fail=False):
    raw={}
    for s in b.SPLITS:
        y=torch.tensor([r["target"] for r in data[s]]); z=torch.zeros((len(y),256),dtype=torch.float64); z[torch.arange(len(y)),y]=5.
        if fail and s=="HOLDOUT": z[0,70]=9.
        raw[s]={p:{v:z for v in b.VIEWS} for p in labels}
    return raw

def original_flags():
    return [dict(seed=s,arm=a,length_pass={str(n):not(s==319005 and a=="last_only" and n==6) for n in range(2,7)}) for s,a in b.identities()]

def fixtures(data):
    anchors=[]; records=[]
    for flag in original_flags():
        old={str(n):new_raw(data,profiles(n),n==6 and not flag["length_pass"]["6"]) for n in range(1,7)}
        key=dict(seed=flag["seed"],arm=flag["arm"],readout_policy=flag["arm"],final_sha256=b.digest([flag["seed"],flag["arm"]]))
        anchors.append(dict(**key,raw=old)); records.append(dict(**key,raw=dict(before=old,interior=new_raw(data),after=old),
            receipts={m:dict(calls=n,query_calls=2*n,rows=96*n,grad_calls=0) for m,n in zip(b.MODES,(144,27,144),strict=True)},replay_errors=[0.,0.],weights_preserved=True,hooks_restored=True))
    return anchors,records

def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update({b.PARENT_SOURCE:b.PARENT_BLOB,b.MODEL_SOURCE:b.MODEL_BLOB})
    while len(pins)<772: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1455)}

def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if s["primary_gate"] else "FAIL",diagnostic_execution_valid=True,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False)

class C321Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data=dataset(); cls.old=old_prompts(cls.data); cls.new=b.new_prompts(cls.data); cls.env,base,cls.owner=accepted_functions()
        cls.parent=NS(DATA_SHA="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",PROMPTS_SHA="2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd",expected_parent_results=original_flags)
        cls.x=NS(parent=base,p312=NS(context=lambda:()),wide=NS(span_mask=cls.env["span_mask"],prefix_tensor=prefix,score_length=logical_score,context=lambda:()),guarded=NS(no_neural=no_neural),
                 diag=NS(normalize_task=lambda z,*_:z["totals"],partition=lambda z:{k:v for k,v in z[0].items() if k!="split"}),c=NS(audit=Audit(),base=NS(fingerprint=fingerprint),p267=NS(check_logits=check_logits,counted=counted),core=None,factory=NS(language_module=lambda:None)))
        cls.anchors,cls.records=fixtures(cls.data); cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,cls.parent,cls.x)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)
    def toy(self):
        torch.manual_seed(14); m=Toy(self.env["forward"]); m.eval(); m.requires_grad_(False); return m
    def test_01_seal(self):
        b.validate_seal()
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()
    def test_02_hand_checked_names(self):
        row=self.data["TRAIN"][0]
        self.assertEqual([tuple(b.name_pair(row,p).values()) for p in b.PROFILES],[("aaba","abaa"),("aabb","abab"),("babb","bbab")])
        for rows in self.data.values():
            for row,p in itertools.product(rows,b.PROFILES):
                a,z=b.name_pair(row,p).values(); self.assertEqual((a[0],a[-1],Counter(a)),(z[0],z[-1],Counter(z))); self.assertNotEqual(a,z)
    def test_03_independent_prompt_parser(self):
        for rows in self.data.values():
            for row,p in itertools.product(rows,b.PROFILES):
                first,second,query=b.render(row,p).split(";"); facts=dict((n,int(v)) for n,v in (f.split("=") for f in (first,second)))
                self.assertEqual(facts[query[:-1]],row["target"]-48)
                for view in b.VIEWS: self.assertEqual(b.render(row,p,view).count("="),3)
                self.assertEqual(b.render(row,p,"evidence_blind").count("?"),2); self.assertTrue(b.render(row,p,"query_blind").endswith(";?="))
    def test_04_canonical_inputs_bounds_span(self):
        self.assertEqual(b.digest(self.data),self.parent.DATA_SHA); self.assertEqual(b.digest(self.old),self.parent.PROMPTS_SHA)
        b.check_prompts(self.data,self.old,self.new,self.parent,self.x)
        self.assertEqual(max(len(r["views"]["normal"].encode("utf-8"))+2 for s in self.new.values() for pp in s.values() for r in pp),45)
    def test_05_tamper_and_bad_render(self):
        bad=copy.deepcopy(self.new); bad["TRAIN"][b.PROFILES[0]][0]["target"]=70
        with self.assertRaises(ValueError): b.check_prompts(self.data,self.old,bad,self.parent,self.x)
        with self.assertRaises(ValueError): b.render(self.data["TRAIN"][0],"missing")
        with self.assertRaises(ValueError): b.render(self.data["TRAIN"][0],b.PROFILES[0],"unknown")
    def test_06_immutability_and_question_pairs(self):
        before=b.blob(self.data); rng=torch.random.get_rng_state().clone(); b.new_prompts(self.data)
        self.assertEqual(before,b.blob(self.data)); self.assertTrue(torch.equal(rng,torch.random.get_rng_state()))
        for s,p in itertools.product(b.SPLITS,b.PROFILES):
            for i in range(0,len(self.data[s]),2):
                a,z=self.new[s][p][i:i+2]; self.assertEqual(a["views"]["normal"].rsplit(";",1)[0],z["views"]["normal"].rsplit(";",1)[0]); self.assertNotEqual(a["target"],z["target"])
    def test_07_actual_scorer_adapter(self):
        raw=new_raw(self.data); scorer=Mock(return_value={"passed":True}); x=NS(wide=NS(score_length=self.env["score_length"]),c=NS(c270=NS(score=scorer),p267=NS(check_logits=check_logits)))
        self.assertEqual(b.score_new(raw,self.data,x),{"passed":True})
        adapted=scorer.call_args.args[1]
        for a,z in zip(b.PROFILES,("tripled","shared_prefix2","shared_suffix2"),strict=True): self.assertIs(adapted["TRAIN"][z],raw["TRAIN"][a])
    def test_08_cohort_primary_and_comparator(self):
        rr=copy.deepcopy(self.records); rr[0]["raw"]["interior"]=new_raw(self.data,fail=True)
        _,s=b.analyze(rr,self.anchors,self.data,self.parent,self.x); p=payload(s); b.validate_result(p)
        self.assertEqual((s["pass_counts"]["last_only"],p["status"]),(5,"FAIL")); p["status"]="PASS"
        with self.assertRaises(ValueError): b.validate_result(p)
    def test_09_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["reproductions"])),(10,20,10)); b.validate_result(payload(self.summary))
    def test_10_provenance_and_missing_state(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.anchors,self.data,self.parent,self.x)
        for key,val in (("readout_policy","wrong"),("final_sha256","wrong"),("replay_errors",[.1,0.]),("weights_preserved",False)):
            rr=copy.deepcopy(self.records); rr[0][key]=val
            with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.parent,self.x)
    def test_11_raw_contract(self):
        for mutation in (lambda z:z.pop("HOLDOUT"),lambda z:z["TRAIN"][b.PROFILES[0]].pop("query_blind"),lambda z:z["TRAIN"][b.PROFILES[0]].update(normal=torch.zeros(1))):
            z=new_raw(self.data); mutation(z)
            with self.assertRaises(ValueError): b.score_new(z,self.data,self.x)
    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c321")/str(i)/"summary.json").resolve() for i in range(47)]; hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*[str(i%10)*64 for i in range(46)]),strict=True))
        rows=[dict(seed=s,arm=a,layout_pass={k:not(s==319002 and a=="last_only" and k=="short_long") for k in ("short_long","long_short")},all_layouts_pass=not(s==319002 and a=="last_only")) for s,a in b.identities()]
        e=dict(experiment_id="C320-v5b-frozen-unequal-name-lengths",commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=dict(seed_results=rows,primary_gate=True))
        tail_hashes=tuple(list(hashes.values())[1:])
        p=NS(DATA_SHA=self.parent.DATA_SHA,PROMPTS_SHA=self.parent.PROMPTS_SHA,OUTPUTS=b.OUTPUTS,parent_hashes=lambda _:tail_hashes,verify_artifacts=Mock(return_value=(e,[])),validate_result=Mock(),load_parent=Mock(return_value=({},self.data,self.old,self.anchors)))
        x=copy.copy(self.x); x.c=NS(audit=NS(sha=lambda p:hashes[str(p)]))
        with patch.object(b,"context",return_value=(p,None,x)): yield paths,hashes,p,e
    def test_12_all47_hash_guards(self):
        with self.loader_fixture() as (paths,hashes,p,e):
            self.assertEqual(b.load_parent(paths)[0],e); p.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION); p.load_parent.assert_called_once_with(paths[1:])
            for path in paths:
                saved=hashes[str(path)]; hashes[str(path)]="f"*64; p.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                p.verify_artifacts.assert_not_called(); hashes[str(path)]=saved
    def test_13_parent_scope_and_artifacts(self):
        for fn in (lambda e:e.update(status="FAIL"),lambda e:e["artifacts"].pop(),lambda e:e["validation_summary"].update(primary_gate=False)):
            with self.loader_fixture() as (paths,_,p,e):
                fn(e)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_14_protected_files_and_helpers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.MODEL_SOURCE:b.MODEL_BLOB}
            while len(pins)<766: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): path=root/n; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1443-len(inputs)):
                path=root/("input"+str(i)); path.write_text("input",encoding="utf-8"); inputs[str(path)]=Audit.sha(path)
            folder=root/"parent"; folder.mkdir(); summary=folder/"summary.json"; summary.write_text("summary",encoding="utf-8"); arts=[]
            for n in b.OUTPUTS: path=folder/n; path.write_text("artifact",encoding="utf-8"); arts.append(dict(file=n,sha256=Audit.sha(path)))
            def sha(path): return b.PARENT_SHA if Path(path)==summary else Audit.sha(path)
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); owner=NS(context=lambda:())
            x=NS(parent=NS(context=lambda:()),p312=NS(context=lambda:()),wide=NS(context=lambda:()),c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp})))
            with patch.object(b,"context",return_value=(parent,owner,x)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=arts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*47,root))),(772,1455)); x.c.missing=types.ModuleType("missing"); x.c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([summary]*47,root)
    def test_15_actual_native_inference_both_policies(self):
        for arm in b.ARMS:
            m=self.toy()
            with torch.no_grad(),self.owner.trained_readout(m,self.x.wide,arm): raw=self.x.parent.evaluate(m,self.old,self.data,self.x.wide,self.x.c)
            anchor=dict(seed=b.SEEDS[0],arm=arm,readout_policy=arm,final_sha256=fingerprint(m),raw=raw)
            with contextlib.redirect_stdout(io.StringIO()): r=b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.new,self.owner,self.x)
            self.assertEqual(r["replay_errors"],[0.,0.]); self.assertEqual(sum(z["calls"] for z in r["receipts"].values()),315)
    def test_16_bad_state_and_frozen_enforcement(self):
        m=self.toy(); anchor=dict(seed=b.SEEDS[0],arm="mean_last",readout_policy="mean_last",final_sha256="wrong")
        with self.assertRaises(ValueError): b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.new,self.owner,self.x)
        with self.assertRaises(ValueError): b.evaluate_new(m,self.new,self.data,self.x)
        with torch.no_grad(),self.assertRaises(ValueError): b.evaluate_new(m.train(),self.new,self.data,self.x)
    def test_17_runtime_preflight(self):
        models={a:self.toy() for a in b.ARMS}; states=[m.state_dict() for m in models.values()]; anchors=[dict(final_sha256=fingerprint(m)) for m in models.values()]
        owner=copy.copy(self.owner); owner.load_bundle=lambda _:states; owner.make_models=lambda *a:models
        with patch.object(b,"context",return_value=(self.parent,owner,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.old,anchors)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*47,Path.cwd())
    @contextlib.contextmanager
    def run_fixture(self):
        events=[]; owner=copy.copy(self.owner)
        def load(path): events.append(("load",path)); return [{}]*10
        def infer(*a): events.append(("infer",a[2]["arm"])); return self.records[b.identities().index((a[2]["seed"],a[2]["arm"]))]
        owner.load_bundle=load; owner.make_models=lambda *a:dict.fromkeys(b.ARMS)
        with patch.object(b,"context",return_value=(self.parent,owner,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.old,self.anchors)),patch.object(b,"infer_one",side_effect=infer): yield events
    def test_18_run_loader_roundtrip_no_training(self):
        paths=["C320/summary.json","C319/summary.json"]+["x"]*45; save=torch.save; saved=[]
        def saver(obj,path): saved.append(Path(path).name); save(obj,path)
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=saver),patch.object(torch.optim,"AdamW",side_effect=AssertionError("training")),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=paths,output_dir=out,expected_head="f"*40); q,_=b.verify_artifacts(out,paths,"f"*40)
            self.assertEqual(q,p); self.assertEqual([v for k,v in events if k=="load"],[Path(paths[1]).resolve().parent/"trained-models.pt"]); self.assertEqual(sum(k=="infer" for k,v in events),10); self.assertEqual(saved,["evaluations.pt"])
    def test_19_tampering_and_no_overwrite(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*47,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*47,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*47,"f"*40)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*47,output_dir=out,expected_head="f"*40)
    def test_20_suite_semantic_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5245)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())
    def test_21_cli_context_count(self):
        argv=["program","--summaries"]+[str(i) for i in range(47)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),47)
        p=NS(context=lambda:("owner","x"),regression_modules=lambda root:["m"+str(i) for i in range(205)]); package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c320_unequal_name_lengths=p
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(p,"owner","x")); self.assertEqual(len(b.regression_modules(Path.cwd())),206)
    def test_22_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))
    def test_23_runner_contract(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"embedded","exec")
        self.assertIn("sys.argv[2:49]",blocks[2]); self.assertIn("head = sys.argv[49]",blocks[2]); self.assertIn("len(sys.argv) == 50",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(320,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1")); self.assertIn("regression_exit_hex",runner); self.assertIn("faulthandler.enable",blocks[1])
    def test_24_manifest_counts_scope(self):
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24); self.assertEqual(b.manifest()["raw_logit_payload_bytes"],3150*96*256*8)
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"].update(primary_arm="last_only")):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)

if __name__=="__main__": unittest.main()
