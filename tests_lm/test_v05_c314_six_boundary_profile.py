"""C314 software contracts: synthetic evidence is not a FOLD capability result."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c314_six_boundary_profile as b


def dataset():
    out={"TRAIN":[],"HOLDOUT":[]}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (values[1]-values[0])%4==2 else "TRAIN"
        for order,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f"{lang}:{entities}:{values}:{order}:{query}",entities=list(entities),values=list(values),
                language=lang,permutation=list(order),query=query,target=48+values[entities.index(query)]))
    return out


def render(row,n,profile,view):
    chars="abc" if row["language"]=="en" else "甲乙丙"; a,z=row["entities"]
    names={a:chars[a]*n,z:chars[z]*n}
    if profile=="shared_prefix": names[z]=chars[a]*(n-1)+chars[z]
    if profile=="shared_suffix": names[z]=chars[z]+chars[a]*(n-1)
    facts=[names[e]+"="+("?" if view=="evidence_blind" else str(row["values"][row["entities"].index(e)])) for e in row["permutation"]]
    return ";".join(facts)+";"+("?" if view=="query_blind" else names[row["query"]])+"="


def prompts(data,n):
    return {s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in ("normal","evidence_blind","query_blind")})
                  for r in data[s]] for p in b.PROFILES} for s in b.SPLITS}


def raw(data):
    out={}
    for split in b.SPLITS:
        out[split]={}
        for p in b.PROFILES:
            z=torch.zeros((len(data[split]),256),dtype=torch.float64)
            for i,row in enumerate(data[split]): z[i,row["target"]]=4.
            out[split][p]={v:z for v in ("normal","evidence_blind","query_blind")}
    return out


def annotations(records,data):
    metrics=[]; transitions=[]
    for r in records:
        seed,arm=r["seed"],r["arm"]; totals=[]
        for split in b.SPLITS:
            counts=dict(rows=0,both_correct=0,new_error=0,recovered=0,both_wrong=0,same_wrong=0)
            for profile,old_name in zip(b.PROFILES,b.OLD_PROFILES,strict=True):
                five=r["raw"]["before"]["5"][split][profile]["normal"].argmax(1).tolist()
                six=r["raw"]["six"][split][profile]["normal"].argmax(1).tolist()
                for i,row in enumerate(data[split]):
                    a=five[i]==row["target"]; z=six[i]==row["target"]
                    counts["rows"]+=1
                    counts["both_correct" if a and z else "new_error" if a else "recovered" if z else "both_wrong"]+=1
                    counts["same_wrong"]+=int(not a and not z and five[i]==six[i])
                for lang in b.LANGUAGES:
                    ids=[i for i,row in enumerate(data[split]) if row["language"]==lang]
                    totals.append(dict(split=split,profile=old_name,language=lang,rows=len(ids),correct=sum(six[i]==data[split][i]["target"] for i in ids)))
            transitions.append(dict(seed=seed,arm=arm,split=split,**counts))
        metrics.append(dict(seed=seed,arm=arm,six_score=dict(totals=totals)))
    return metrics,dict(seed_results=b.expected_parent_results(),five_to_six=transitions,
        six_pass_counts=dict(random_pairs=2,value_balanced=1),primary_arm="random_pairs",primary_gate=False,all_replays=True)


def evidence():
    data=dataset(); old={str(n):prompts(data,n) for n in (2,3,4,5)}; six=prompts(data,6)
    z=raw(data); records=[]
    for seed,arm in b.identities():
        records.append(dict(seed=seed,arm=arm,weights_preserved=True,hooks_restored=True,raw=dict(before={"5":z},six=z,after={"5":z})))
    metrics,s=annotations(records,data)
    return data,old,six,records,metrics,s


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<730: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1369)}


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
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


@contextlib.contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("neural execution")),\
         patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("model load")),\
         patch.object(torch,"save",side_effect=AssertionError("tensor write")),\
         patch.object(torch.optim,"AdamW",side_effect=AssertionError("optimizer")):
        yield


class C314Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); torch.set_num_threads(2)
        cls.data,cls.old,cls.six,cls.records,cls.metrics,cls.parent_summary=evidence()
        cls.report,cls.summary=b.analyze(cls.records,cls.data,cls.metrics,cls.parent_summary,cls.old,cls.six)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)

    def test_01_manifest_and_utf8(self):
        b.validate_seal(); root=Path(__file__).resolve().parents[1]
        for name in b.OWN:
            text=(root/name).read_text(encoding="utf-8"); self.assertTrue(text); self.assertNotIn("\x00",text)
        self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))

    def test_02_bad_seal(self):
        for seal in ("UNSEALED","0"*64):
            with patch.object(b,"MANIFEST_SHA",seal),self.assertRaises(ValueError): b.validate_seal()

    def test_03_canonical_data_and_prompts(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA); self.assertEqual(b.digest(self.old),b.OLD_PROMPTS_SHA); self.assertEqual(b.digest(self.six),b.SIX_PROMPTS_SHA)

    def test_04_independent_margin_oracle(self):
        z=torch.randn((5,256),dtype=torch.float64,generator=torch.Generator().manual_seed(19)); before=z.clone(); targets=[48,49,50,51,48]
        pred,margins,ties=b.logit_features(z,targets)
        for i,values in enumerate(z.tolist()):
            self.assertEqual(pred[i],values.index(max(values)))
            self.assertEqual(margins[i],values[targets[i]]-max(v for j,v in enumerate(values) if j!=targets[i]))
            self.assertEqual(ties[i],values.count(max(values))>1)
        self.assertTrue(torch.equal(z,before))

    def test_05_ties_are_not_answer_repairs(self):
        z=torch.zeros((2,256),dtype=torch.float64); z[:,48:50]=5.
        pred,margin,tie=b.logit_features(z,[48,49])
        self.assertEqual(pred,[48,48]); self.assertEqual(margin,[0.,0.]); self.assertEqual(tie,[True,True])

    def test_06_invalid_logits(self):
        for z in (torch.zeros(1),torch.zeros((1,256)),torch.full((1,256),float("nan"),dtype=torch.float64),torch.zeros((1,256),dtype=torch.float64,requires_grad=True)):
            with self.assertRaises(ValueError): b.logit_features(z,[48])
        with self.assertRaises(ValueError): b.logit_features(torch.zeros((1,256),dtype=torch.float64),[True])

    def test_07_answer_roles_full_output_domain(self):
        row=self.data["TRAIN"][0]; target=row["target"]; other=48+row["values"][1-row["entities"].index(row["query"])]; absent=next(x for x in range(48,52) if x not in (target,other))
        self.assertEqual([b.answer_class(row,p) for p in (target,other,absent,52,0)],list(b.CLASSES)+["other_output"])
        with self.assertRaises(ValueError): b.answer_class(row,True)

    def test_08_transition_counts_independent(self):
        rows=[]
        for a,z,p,q in (("correct","correct",48,48),("correct","other_fact",48,49),("other_fact","correct",49,48),("other_fact","other_fact",49,49)):
            rows.append(dict(class5=a,class6=z,prediction5=p,prediction6=q,margin5=1.,margin6=.5,tie5=False,tie6=False,tokens5=24,tokens6=27))
        got=b.aggregate(rows)
        self.assertEqual([got[k] for k in b.TRANSITIONS],[1]*4); self.assertEqual(got["same_wrong"],1); self.assertEqual(got["margin_decreased"],4)

    def test_09_nonfinite_statistics_and_score_shift(self):
        for xs in ([],[float("inf")],[float("nan")]):
            with self.assertRaises(ValueError): b.numeric_summary(xs)
        z=torch.arange(256,dtype=torch.float64).repeat(2,1)
        self.assertEqual(b.logit_features(z,[48,49]),b.logit_features(z+100.,[48,49]))

    def test_10_inventory_and_reconciliation(self):
        self.assertEqual((len(self.report["paired_rows"]),len(self.report["groups"]),len(self.report["parent_transitions"])),(8640,120,20))
        self.assertEqual(sum(g["rows"] for g in self.report["groups"]),8640); b.validate_result(payload(self.summary))
        for group in self.report["groups"]:
            self.assertEqual((group["tokens5"],group["tokens6"]),([24],[27]) if group["language"]=="en" else ([54],[63]))

    def test_11_source_alignment_not_guessed(self):
        old=copy.deepcopy(self.old); old["5"]["TRAIN"]["repeat"][0]["source_id"]="other"
        with self.assertRaises(ValueError): b.analyze(self.records,self.data,self.metrics,self.parent_summary,old,self.six)
        records=copy.deepcopy(self.records); records[0]["raw"]["six"]["TRAIN"]["repeat"]["normal"]=torch.zeros((1,256),dtype=torch.float64)
        with self.assertRaises(ValueError): b.analyze(records,self.data,self.metrics,self.parent_summary,self.old,self.six)

    def test_12_new_errors_stay_in_their_group(self):
        records=list(self.records); records[0]=copy.deepcopy(records[0]); records[0]["raw"]["six"]=raw(self.data)
        i=next(i for i,r in enumerate(self.data["HOLDOUT"]) if r["language"]=="ja")
        records[0]["raw"]["six"]["HOLDOUT"]["shared_suffix"]["normal"][i,70]=9.
        metrics,s=annotations(records,self.data); report,summary=b.analyze(records,self.data,metrics,s,self.old,self.six)
        bad=[g for g in report["groups"] if g["new_error"]]
        self.assertEqual(len(bad),1); self.assertEqual((bad[0]["language"],bad[0]["profile"],bad[0]["new_error"]),("ja","shared_suffix",1))
        self.assertEqual(summary["six_correct"],8639); b.validate_result(payload(summary))

    def test_13_changed_parent_totals_rejected(self):
        metrics=copy.deepcopy(self.metrics); metrics[0]["six_score"]["totals"][0]["correct"]-=1
        with self.assertRaisesRegex(ValueError,"local score"): b.analyze(self.records,self.data,metrics,self.parent_summary,self.old,self.six)
        s=copy.deepcopy(self.parent_summary); s["five_to_six"][0]["new_error"]+=1
        with self.assertRaisesRegex(ValueError,"transition reconciliation"): b.analyze(self.records,self.data,self.metrics,s,self.old,self.six)

    def test_14_incomplete_cohort(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,self.metrics,self.parent_summary,self.old,self.six)
        records=list(self.records); records[0]=records[1]
        with self.assertRaises(ValueError): b.analyze(records,self.data,self.metrics,self.parent_summary,self.old,self.six)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c314-fixture")/str(i)/"summary.json").resolve() for i in range(40)]
        names=("evaluation-plan.json","six-dataset.json","evaluations.pt","measurements.json","validation-summary.json")
        p=dict(experiment_id="C313-v5b-frozen-six-transfer",commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
               artifacts=[dict(file=n) for n in names],validation_summary=copy.deepcopy(self.parent_summary))
        parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(39)),OUTPUTS=names,
                  verify_artifacts=Mock(return_value=(p,self.metrics)),validate_result=Mock())
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True))
        files={"dataset.json":self.data,"length-datasets.json":self.old,"six-dataset.json":self.six}
        c=NS(audit=NS(sha=lambda p:hashes[str(p)],read_json=lambda p:files[p.name]),p267=NS(validate_data=lambda _:None))
        archive=dict(schema="fold-c313-six-transfer-eval-v1",records=self.records)
        with patch.object(b,"context",return_value=(parent,NS(no_neural=no_neural),None,c)),patch.object(torch,"load",return_value=archive):
            yield paths,hashes,parent,p,archive

    def test_15_all40_hashes_before_verifier(self):
        with self.loader_fixture() as (paths,hashes,parent,p,_):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); hashes[str(path)]=old

    def test_16_parent_scope_and_writer_schema(self):
        for mutate in (lambda p,a:p.update(status="PASS"),lambda p,a:a.update(schema="wrong"),lambda p,a:p["artifacts"].pop(),lambda p,a:p["validation_summary"].update(primary_arm="value_balanced")):
            with self.loader_fixture() as (paths,_,_,p,a):
                mutate(p,a)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_17_actual_precheck_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB}
            while len(pins)<724: pins["accepted/"+str(len(pins))]="a"*40
            for name in list(pins)+list(b.OWN):
                path=root/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(name,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1357-len(inputs)):
                path=root/("input"+str(i)); path.write_text("data",encoding="utf-8"); inputs[str(path.resolve())]=Audit.sha(path)
            folder=root/"parent"; folder.mkdir(); path=folder/"summary.json"; path.write_text("summary",encoding="utf-8"); special={str(path.resolve()):b.PARENT_SHA}; arts=[]
            for name in ("evaluation-plan.json","six-dataset.json","evaluations.pt","measurements.json","validation-summary.json"):
                file=folder/name; file.write_text("artifact",encoding="utf-8"); arts.append(dict(file=name,sha256=Audit.sha(file)))
            def sha(path): return special.get(str(Path(path).resolve()),Audit.sha(path))
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.context=lambda:(NS(context=lambda:()),)
            wide=NS(PINNED={},context=lambda:()); c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,
                git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp}))
            p=dict(source_blobs=pins,input_sha256=inputs,artifacts=arts)
            with patch.object(b,"context",return_value=(parent,None,wide,c)),patch.object(b,"load_parent",return_value=(p,)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*40,root))),(730,1369))
                first=next(iter(inputs)); Path(first).write_text("changed",encoding="utf-8")
                with self.assertRaisesRegex(ValueError,"changed input"): b.precheck([path]*40,root)
                Path(first).write_text(b.PARENT_SOURCE,encoding="utf-8")
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*40,root)

    @contextlib.contextmanager
    def run_fixture(self):
        calls=[]; c=NS(audit=Audit()); p=dict(validation_summary=self.parent_summary)
        def load(*_): calls.append("loader"); return p,self.records,self.data,self.metrics,self.old,self.six
        def pre(*_): calls.append("precheck"); return protection()
        with patch.object(b,"context",return_value=(None,NS(no_neural=no_neural),None,c)),patch.object(b,"precheck",side_effect=pre),patch.object(b,"load_parent",side_effect=load): yield calls

    def test_18_production_order_no_neural_persistence(self):
        with self.run_fixture() as calls,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*40,output_dir=out,expected_head="f"*40)
            self.assertEqual(calls,["precheck","loader","precheck"])
            q,_=b.verify_artifacts(out,["x"]*40,"f"*40); self.assertEqual(p,q)
            self.assertEqual({x.name for x in out.iterdir()},set(b.OUTPUTS)|{"summary.json"})
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*40,output_dir=out,expected_head="f"*40)

    def test_19_byte_and_semantic_tampering(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*40,output_dir=out,expected_head="f"*40); path=out/"boundary-report.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*40,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*40,"f"*40)

    def test_20_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["fixture."+str(i) for i in range(5053)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_21_cli_context_dryrun_guard(self):
        args=["program","--summaries"]+[str(i) for i in range(40)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),40)
        parent=NS(context=lambda:tuple(range(6)),regression_modules=lambda _:["m"+str(i) for i in range(198)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c313_frozen_six_transfer=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(parent,1,3,5)); self.assertEqual(len(b.regression_modules(Path.cwd())),199)
        with self.run_fixture() as calls,contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*40,Path.cwd()); self.assertEqual(calls,["precheck","loader"])
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_22_runner_indices_and_utf8_calls(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for text in blocks: compile(text,"embedded","exec")
        self.assertIn("sys.argv[2:42]",blocks[2]); self.assertIn("sys.argv[42]",blocks[2]); self.assertIn("len(sys.argv) == 43",blocks[2])
        ids=re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher)
        self.assertEqual(ids,[str(i) for i in range(313,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))

    def test_23_scope_conservation_and_test_count(self):
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"].update(new_error=1)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c313_frozen_six_transfer"])

    def test_24_actual_parent_transition_function(self):
        path=Path(__file__).resolve().parents[1]/b.PARENT_SOURCE; tree=ast.parse(path.read_text(encoding="utf-8"))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="transition")
        space=dict(torch=torch,require=b.require,PROFILES=b.PROFILES)
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),"exec"),space)
        old=self.records[0]["raw"]["before"]["5"]["TRAIN"]; six=self.records[0]["raw"]["six"]["TRAIN"]
        expected=self.report["parent_transitions"][0]
        actual=space["transition"](old,six,self.data["TRAIN"])
        self.assertEqual(actual,{k:expected[k] for k in actual})


if __name__=="__main__": unittest.main()
