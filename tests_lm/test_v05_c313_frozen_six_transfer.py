"""Software fixtures for C313; not evidence of real FOLD checkpoint competence."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c313_frozen_six_transfer as b


def dataset():
    out={"TRAIN":[],"HOLDOUT":[]}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (values[1]-values[0])%4==2 else "TRAIN"
        for perm,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f"{lang}:{entities}:{values}:{perm}:{query}",entities=list(entities),values=list(values),language=lang,
                permutation=list(perm),query=query,target=48+values[entities.index(query)]))
    return out


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def old_prompts(data):
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:b.render(r,n,p,v) for v in b.VIEWS})
                           for r in data[s]] for p in b.PROFILES} for s in b.SPLITS} for n in (2,3,4,5)}


def check_logits(z,n):
    b.require(isinstance(z,torch.Tensor) and z.shape==(n,256) and z.dtype==torch.float64
              and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logit contract")


def raw(data,fail=False):
    out={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64)
        y=torch.tensor([r["target"] for r in data[s]]); z[torch.arange(len(y)),y]=4.
        if fail and s=="HOLDOUT": z[0,70]=9.
        out[s]={p:{v:z for v in b.VIEWS} for p in b.PROFILES}
    return out


def replay_error(a,c,data,backend):
    b.require(set(a)==set(c)==set(map(str,(2,3,4,5))),"old lengths")
    error=0.
    for n,s,p,v in itertools.product(a,b.SPLITS,b.PROFILES,b.VIEWS):
        x,z=a[n][s][p][v],c[n][s][p][v]; check_logits(x,len(data[s])); check_logits(z,len(data[s]))
        error=max(error,float((x-z).abs().max())); b.require(error<=1e-9 and torch.equal(x.argmax(1),z.argmax(1)),"old replay")
    return error


def score(data,raw,c):
    totals=[]
    for s in b.SPLITS:
        y=torch.tensor([r["target"] for r in data[s]])
        correct=sum(int((raw[s][p]["normal"].argmax(1)==y).sum()) for p in b.PROFILES); size=3*len(y)
        totals.append(dict(split=s,rows=size,correct=correct,direct_pass=correct==size,full_pass=correct==size))
    return dict(passed=all(t["full_pass"] for t in totals),totals=totals)


def scoring():
    wide=NS(render=b.render,prefix_tensor=prefix,replay_error=replay_error,score_length=score)
    diag=NS(normalize_task=lambda z,*_:z["totals"],partition=lambda rr:{k:v for k,v in rr[0].items() if k!="split"})
    c=NS(p267=NS(check_logits=check_logits))
    return wide,diag,c


def fixtures():
    data=dataset(); perfect=raw(data); failure=raw(data,True); records=[]; anchors=[]
    for flag in b.expected_parent_flags():
        seed,arm=flag["seed"],flag["arm"]
        old={str(n):perfect if flag["length_pass"][str(n)] else failure for n in (2,3,4,5)}
        h=b.digest([seed,arm]); anchors.append(dict(seed=seed,arm=arm,final_sha256=h,raw=old))
        records.append(dict(seed=seed,arm=arm,final_sha256=h,raw=dict(before=old,six=perfect,after=old),replay_errors=[0.,0.],
            weights_preserved=True,hooks_restored=True,forward_calls=243,row_presentations=23328,core_forward_calls=972))
    return data,anchors,records


def parent_payload():
    return dict(experiment_id="C312-v5b-value-balanced-minibatches",commit_sha=b.PARENT_EXECUTION,status="FAIL",
        source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB},
        artifacts=[dict(file=n) for n in ("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")],
        validation_summary=dict(seed_results=b.expected_parent_flags(),candidate_gate=False,all_pairs_matched=True,all_replays=True))


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB; pins[b.WIDE_SOURCE]=b.WIDE_BLOB
    while len(pins)<724: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1357)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n
    @staticmethod
    def git(root,*args): return b"f"*40 if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b""


def payload(summary):
    pins,protected=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["primary_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],
        validation_summary=summary,gate_f_candidate=False,production_adoption=False)


def fingerprint(m):
    h=hashlib.sha256()
    for n,z in sorted(m.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().numpy().tobytes())
    return h.hexdigest()


class Core(torch.nn.Module):
    def __init__(self): super().__init__(); self.weight=torch.nn.Parameter(torch.tensor(.2,dtype=torch.float64))
    def forward(self,x): return x+self.weight


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.core=Core(); self.bias=torch.nn.Parameter(torch.arange(256,dtype=torch.float64)/256); self.mutate=False
    def forward(self,x,t):
        assert x.shape==(len(x),64) and t.shape==(len(x),)
        h=x[:,0].to(torch.float64)
        for _ in range(4): h=self.core(h)
        if self.mutate:
            with torch.no_grad(): self.bias.add_(.01)
        return h[:,None]+self.bias[None,:]


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def mh(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def ch(*args): cores[0]+=1
    a=model.register_forward_hook(mh); c=model.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: a.remove(); c.remove()


def evaluate_old(m,prompts,data,c):
    wide=NS(prefix_tensor=prefix)
    return {str(n):b.evaluate_six(m,prompts[str(n)],data,wide,c) for n in (2,3,4,5)}


def toy_backend():
    return NS(base=NS(fingerprint=fingerprint),p267=NS(check_logits=check_logits,counted=counted),core=None)


class C313Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.deterministic=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data,cls.anchors,cls.records=fixtures(); cls.old=old_prompts(cls.data); cls.six=b.six_prompts(cls.data)
        cls.wide,cls.diag,cls.c=scoring(); cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,cls.wide,cls.diag,cls.c)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.deterministic)

    def test_01_seal(self): b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()

    def test_03_canonical_data(self): self.assertEqual(b.digest(self.data),b.DATA_SHA)

    def test_04_original_prompt_bytes(self):
        self.assertEqual(b.digest(self.old),b.PROMPTS_SHA); b.check_prompts(self.data,self.old,self.six,self.wide)

    def test_05_six_context_bound(self):
        texts=[r["views"][v] for s in b.SPLITS for p in b.PROFILES for r in self.six[s][p] for v in b.VIEWS]
        self.assertEqual(max(len(x.encode("utf-8")) for x in texts),61)
        for text in texts:
            x=prefix(text); k=len(text.encode("utf-8")); self.assertEqual(int(x[k+1]),258); self.assertTrue(bool((x[k+2:]==256).all()))
        with self.assertRaises(ValueError): prefix("甲"*22)

    def test_06_masks_preserve_contract(self):
        r=self.data["TRAIN"][0]
        self.assertEqual(b.render(r,6,"repeat","evidence_blind").count("?"),2)
        self.assertTrue(b.render(r,6,"repeat","query_blind").endswith(";?="))
        self.assertEqual(b.render(r,6,"repeat").count("="),3)

    def test_07_novelty_and_no_new_tokens(self):
        old={r["views"]["normal"] for n in self.old.values() for s in n.values() for pp in s.values() for r in pp}
        new={r["views"]["normal"] for s in self.six.values() for pp in s.values() for r in pp}
        self.assertEqual(len(new),864); self.assertFalse(old&new)
        self.assertLessEqual(set("".join(new).encode("utf-8")),set("".join(old).encode("utf-8")))

    def test_08_invalid_render_and_tamper(self):
        for n in (1,7,True):
            with self.assertRaises(ValueError): b.render(self.data["TRAIN"][0],n,b.PROFILES[0])
        six=copy.deepcopy(self.six); six["TRAIN"]["repeat"][0]["views"]["normal"]="wrong"
        with self.assertRaises(ValueError): b.check_prompts(self.data,self.old,six,self.wide)

    def test_09_parent_primary_distinction(self):
        flags=b.expected_parent_flags(); self.assertEqual(sum(r["quint_pass"] for r in flags),9)
        self.assertEqual(b.PRIMARY_ARM,"random_pairs"); self.assertEqual(len(b.identities()),10)

    def test_10_transition_oracle(self):
        rows=[dict(target=48),dict(target=49),dict(target=50),dict(target=51)]
        def z(pred):
            out=torch.zeros((4,256)); out[torch.arange(4),torch.tensor(pred)]=1.; return {p:dict(normal=out) for p in b.PROFILES}
        t=b.transition(z([48,49,70,71]),z([48,70,50,71]),rows)
        self.assertEqual(t,dict(rows=12,both_correct=3,new_error=3,recovered=3,both_wrong=3,same_wrong=3))

    def test_11_analysis_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["five_to_six"])),(10,20,20))
        b.validate_result(payload(self.summary))

    def test_12_six_negative_no_secondary_rescue(self):
        rr=copy.deepcopy(self.records); rr[0]["raw"]["six"]=raw(self.data,True)
        _,s=b.analyze(rr,self.anchors,self.data,self.wide,self.diag,self.c); p=payload(s); b.validate_result(p)
        self.assertEqual(p["status"],"FAIL"); self.assertEqual(s["six_pass_counts"]["value_balanced"],5)
        p["status"]="PASS"
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_13_secondary_failure_does_not_rewrite_primary(self):
        rr=copy.deepcopy(self.records)
        for r in rr:
            if r["arm"]=="value_balanced": r["raw"]["six"]=raw(self.data,True)
        _,s=b.analyze(rr,self.anchors,self.data,self.wide,self.diag,self.c)
        self.assertTrue(s["primary_gate"]); b.validate_result(payload(s))

    def test_14_cohort_and_fingerprint(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.anchors,self.data,self.wide,self.diag,self.c)
        rr=copy.deepcopy(self.records); rr[0]["final_sha256"]="changed"
        with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.wide,self.diag,self.c)

    def test_15_control_reproduction(self):
        rr=copy.deepcopy(self.records); rr[0]["raw"]["after"]={n:raw(self.data,True) for n in ("2","3","4","5")}
        with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.wide,self.diag,self.c)
        rr=copy.deepcopy(self.records); rr[0]["replay_errors"]=[.1,0.]
        with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.wide,self.diag,self.c)

    def test_16_six_logit_and_freeze_contract(self):
        rr=copy.deepcopy(self.records); rr[0]["raw"]["six"]=raw(self.data); rr[0]["raw"]["six"]["TRAIN"]["repeat"]["normal"]=torch.zeros(1)
        with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.wide,self.diag,self.c)
        with self.assertRaises(ValueError): b.evaluate_six(Toy(),self.six,self.data,self.wide,self.c)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c313-fixture")/str(i)/"summary.json").resolve() for i in range(39)]; p=parent_payload()
        parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(38)),OUTPUTS=tuple(a["file"] for a in p["artifacts"]),
                  verify_artifacts=Mock(return_value=(p,{})),validate_result=Mock())
        mapping=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:self.data if p.name=="dataset.json" else self.old),p267=NS(validate_data=lambda _:None))
        archive=dict(schema="fold-c312-value-batches-eval-v1",records=self.anchors)
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),None,self.wide,None,c)),patch.object(torch,"load",return_value=archive):
            yield paths,mapping,parent,p,archive

    def test_17_all39_parent_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p,_):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)]; mapping[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)]=old

    def test_18_parent_contract_rejections(self):
        for mutate in (lambda p,a:p.update(status="PASS"),lambda p,a:a.update(schema="wrong"),lambda p,a:p["artifacts"].pop()):
            with self.loader_fixture() as (paths,_,_,p,a):
                mutate(p,a)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_19_source_input_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB}
            while len(pins)<718: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1343-len(protected)):
                p=root/("input"+str(i)); p.write_text("data",encoding="utf-8"); protected[str(p.resolve())]=Audit.sha(p)
            folder=root/"parent"; folder.mkdir(); path=folder/"summary.json"; path.write_text("summary",encoding="utf-8"); special={str(path.resolve()):b.PARENT_SHA}; arts=[]
            for desc in parent_payload()["artifacts"]:
                p=folder/desc["file"]; p.write_text("artifact",encoding="utf-8"); arts.append(dict(file=p.name,sha256=Audit.sha(p)))
            def sha(p): return special.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.context=lambda:(); parent.PINNED={b.PARENT_SOURCE:b.PARENT_BLOB}
            wide=NS(PINNED={b.WIDE_SOURCE:b.WIDE_BLOB},context=lambda:())
            c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),safe_child=Audit.safe_child,
                protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp}))
            with patch.object(b,"context",return_value=(parent,None,None,wide,None,c)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=protected,artifacts=arts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*39,root))),(724,1357))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*39,root)

    def test_20_actual_inference_call_counts_and_strict_state(self):
        m=Toy(); m.eval(); m.requires_grad_(False); c=toy_backend(); wide=NS(prefix_tensor=prefix,evaluate=evaluate_old,replay_error=replay_error)
        anchor=dict(seed=b.SEEDS[0],arm=b.ARMS[0],final_sha256=fingerprint(m),raw=evaluate_old(m,self.old,self.data,c))
        with contextlib.redirect_stdout(io.StringIO()): r=b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.six,wide,c)
        self.assertEqual(r["forward_calls"],243); self.assertEqual(r["replay_errors"],[0.,0.]); self.assertEqual(fingerprint(m),anchor["final_sha256"])
        state=copy.deepcopy(m.state_dict()); state["bias"]+=1.
        with self.assertRaises(ValueError): b.infer_one(m,state,anchor,self.data,self.old,self.six,wide,c)

    def test_21_mutating_model_rejected(self):
        m=Toy(); m.mutate=True; m.eval(); m.requires_grad_(False); c=toy_backend(); wide=NS(prefix_tensor=prefix,evaluate=evaluate_old,replay_error=replay_error)
        anchor=dict(seed=b.SEEDS[0],arm=b.ARMS[0],final_sha256=fingerprint(m))
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(ValueError,"preservation"):
            b.infer_one(m,m.state_dict(),anchor,self.data,self.old,self.six,wide,c)

    def test_22_runtime_preflight_actual_path(self):
        models={a:Toy() for a in b.ARMS}; states=[m.state_dict() for m in models.values()]; anchors=[dict(final_sha256=fingerprint(m)) for m in models.values()]
        parent=NS(load_bundle=lambda _:states,make_models=lambda *a:models); c=toy_backend()
        with patch.object(b,"context",return_value=(parent,None,None,self.wide,None,c)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.old,anchors)),contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*39,Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        wide,diag,c=scoring(); c.audit=Audit(); events=[]
        def load(_): events.append("bundle"); return [{}]*10
        def infer(*a): events.append("infer"); return self.records[b.identities().index((a[2]["seed"],a[2]["arm"]))]
        def pc(*a): events.append("precheck"); return protection()
        parent=NS(load_bundle=load,make_models=lambda *a:dict.fromkeys(b.ARMS))
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),None,wide,diag,c)),patch.object(b,"load_parent",return_value=({},self.data,self.old,self.anchors)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"infer_one",side_effect=infer): yield events

    def test_23_production_run_dispatch_persistence(self):
        saved=[]; real=torch.save
        def save(obj,path): saved.append(Path(path).name); real(obj,path)
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=save),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*39,output_dir=out,expected_head="f"*40)
            self.assertEqual(events.count("bundle"),1); self.assertEqual(events.count("infer"),10); self.assertEqual(saved,["evaluations.pt"])
            q,_=b.verify_artifacts(out,["x"]*39,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*39,output_dir=out,expected_head="f"*40)

    def test_24_bytes_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*39,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*39,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*39,"f"*40)

    def test_25_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5029)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_26_cli_context_modules_guard(self):
        args=["prog","--summaries"]+[str(i) for i in range(39)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),39)
        parent=NS(context=lambda:tuple(range(9)),regression_modules=lambda _:["m"+str(i) for i in range(197)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c312_value_balanced_batches=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(parent,1,3,4,6,8)); self.assertEqual(len(b.regression_modules(Path.cwd())),198)
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_27_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for p in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))

    def test_28_runner_indices(self):
        import re
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"runner","exec")
        self.assertIn("sys.argv[2:41]",blocks[2]); self.assertIn("head = sys.argv[41]",blocks[2]); self.assertIn("len(sys.argv) == 42",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),39)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_29_no_optimizer_in_scientific_path(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,patch.object(torch.optim,"AdamW",side_effect=AssertionError("training forbidden")),contextlib.redirect_stdout(io.StringIO()):
            b.run(summaries=["x"]*39,output_dir=Path(tmp)/"run",expected_head="f"*40)

    def test_30_actual_accepted_render_prefix(self):
        root=Path(__file__).resolve().parents[1]; path=root/b.WIDE_SOURCE; tree=ast.parse(path.read_text(encoding="utf-8"))
        space=dict(torch=torch,require=b.require,SLOTS=64,EVAL_LENGTHS=(2,3,4,5),PROFILES=b.PROFILES,VIEWS=b.VIEWS)
        names=("render","name_map","prefix_tensor")
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(path),"exec"),space)
        b.check_prompts(self.data,self.old,self.six,NS(render=space["render"],prefix_tensor=space["prefix_tensor"]))

    def test_31_actual_scorer_adapter(self):
        root=Path(__file__).resolve().parents[1]; path=root/b.WIDE_SOURCE; tree=ast.parse(path.read_text(encoding="utf-8"))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="score_length")
        space=dict(require=b.require,SPLITS=b.SPLITS,PROFILES=b.PROFILES,LEGACY_PROFILES={3:("tripled","shared_prefix2","shared_suffix2")})
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),"exec"),space)
        received=Mock(return_value={"passed":True}); c=NS(c270=NS(score=received),p267=object()); z=raw(self.data)
        self.assertEqual(space["score_length"](self.data,z,c),{"passed":True})
        a=received.call_args.args[1]; self.assertEqual(set(a["TRAIN"]),set(space["LEGACY_PROFILES"][3])); self.assertIs(a["TRAIN"]["tripled"],z["TRAIN"]["repeat"])

    def test_32_result_scope_work_and_count(self):
        for change in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"].update(primary_arm="value_balanced")):
            p=payload(copy.deepcopy(self.summary)); change(p)
            with self.assertRaises(ValueError): b.validate_result(p)
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)
        self.assertEqual(b.manifest()["raw_logit_payload_bytes"],10*(10368*2+2592)*256*8)


if __name__=="__main__": unittest.main()
