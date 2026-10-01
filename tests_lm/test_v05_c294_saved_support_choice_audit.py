"""C294 numerical/control fixtures, not user-local scientific evidence."""
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
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c294_saved_support_choice_audit as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(id=str((language,e,v,order,q)),language=language,entities=list(e),values=list(v),permutation=list(order),query=q,target=48+v[e.index(q)]))
    return data


def fixtures():
    data=dataset();zs={};nll={}
    for split,rows in data.items():
        z=torch.zeros((len(rows),256),dtype=torch.float64);y=torch.tensor([r["target"] for r in rows])
        z[torch.arange(len(rows)),y]=4.;zs[split]=z;nll[split]=float(F.cross_entropy(z,y))
    records=[];metrics=[];partitions=[]
    for seed,arm in b.identities():
        raw={t:{s:{p:{v:zs[s] for v in ("normal","evidence_blind","query_blind")} for p in profiles} for s in data} for t,profiles in b.PROFILES.items()}
        m=dict(seed=seed,arm=arm)
        for t,profiles in b.PROFILES.items():
            m[t]=dict(totals=[dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
                             for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in profiles for l in ("en","ja")])
            for split,n in (("TRAIN",576),("HOLDOUT",288)):
                partitions.append(dict(seed=seed,arm=arm,task=t,split=split,rows=n,correct=n,
                                       output_role_counts={k:n if k=="target" else 0 for k in b.ROLES},final_normal_nll=nll[split]))
        records.append(dict(seed=seed,arm=arm,raw=raw));metrics.append(m)
    return records,data,metrics,partitions


def parent_fixture(partitions=None):
    return dict(experiment_id="C293-v5b-fact-support-loss",commit_sha=b.PARENT_EXECUTION,status="FAIL",
                source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n,sha256="a"*64) for n in b.PARENT_OUTPUTS],
                validation_summary=dict(seed_results=b.expected_results(),candidate_gate=False,all_groups_matched=True,all_replays=True,
                                        final_partitions=partitions if partitions is not None else fixtures()[3]))


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<610:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1106)}


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


def result_fixture(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
                capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


def example():
    row=dataset()["TRAIN"][0];z=torch.zeros((1,256),dtype=torch.float64);z[0,48]=4.;z[0,49]=1.
    return z,[row]


def named(values):return [dict(task="quad",split="HOLDOUT",profile="quadrupled",**v) for v in values]


class C294Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();torch.set_num_threads(2)
        cls.report,cls.summary=b.analyze(*fixtures())
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)

    def test_01_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals(self):
        for value in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError):b.validate_seal()

    def test_03_uniform_closed_form(self):
        z,rows=example();z.zero_();r=b.measure(z,rows)[0]
        self.assertAlmostEqual(r["answer_nll"],math.log(256));self.assertAlmostEqual(r["support_nll"],math.log(128))
        self.assertAlmostEqual(r["choice_nll"],math.log(2));self.assertAlmostEqual(r["support_mass"],2/256)
        self.assertEqual(r["full_prediction"],0);self.assertEqual(r["conditional_prediction"],48)
        self.assertTrue(r["choice_tie"]);self.assertTrue(r["support_outside_tie"])

    def test_04_four_categories(self):
        z,rows=example();self.assertEqual(b.measure(z,rows)[0]["kind"],b.KINDS[0])
        z[0,70]=10.;self.assertEqual(b.measure(z,rows)[0]["kind"],b.KINDS[1])
        z[0,49]=6.;self.assertEqual(b.measure(z,rows)[0]["kind"],b.KINDS[2])
        z[0,70]=0.;self.assertEqual(b.measure(z,rows)[0]["kind"],b.KINDS[3])

    def test_05_support_independent_of_query_and_order(self):
        z,rows=example();r=rows[0];support=b.fact_support(r)
        r["query"]=1;r["target"]=49;self.assertEqual(b.fact_support(r),support)
        r["permutation"].reverse();r["entities"].reverse();r["values"].reverse()
        self.assertEqual(b.fact_support(r),support)
        self.assertEqual(b.measure(z,rows)[0]["conditional_prediction"],48)

    def test_06_invalid_binding(self):
        for fn in (lambda r:r.update(target=51),lambda r:r.update(values=[0,0]),lambda r:r.update(values=[0,4]),lambda r:r.update(query=2)):
            z,rows=example();fn(rows[0])
            with self.assertRaises(ValueError):b.measure(z,rows)

    def test_07_ties_never_prefer_target(self):
        z,rows=example();rows[0]["query"]=1;rows[0]["target"]=49;z[0,48]=z[0,49]=4.
        r=b.measure(z,rows)[0];self.assertTrue(r["choice_tie"])
        self.assertEqual(r["conditional_prediction"],48);self.assertFalse(r["conditional_correct"])
        z[0,2]=4.;r=b.measure(z,rows)[0];self.assertTrue(r["support_outside_tie"]);self.assertEqual(r["full_prediction"],2)

    def test_08_full_winner_roles(self):
        z,rows=example();z[0,50]=8.;self.assertEqual(b.measure(z,rows)[0]["output_role"],"absent_known_value")
        z[0,70]=10.;self.assertEqual(b.measure(z,rows)[0]["output_role"],"non_value_byte")

    def test_09_offset_invariance(self):
        z,rows=example();a=b.measure(z,rows)[0];c=b.measure(z+1e8,rows)[0]
        for k in ("full_prediction","conditional_prediction","choice_gap","support_outside_gap"):self.assertEqual(a[k],c[k])
        for k in ("answer_nll","support_nll","choice_nll","support_mass"):self.assertAlmostEqual(a[k],c[k],places=12)

    def test_10_random_decomposition_and_independent_mask(self):
        rows=dataset()["TRAIN"][:20];z=torch.randn((20,256),dtype=torch.float64,generator=torch.Generator().manual_seed(294))
        result=b.measure(z,rows)
        for i,r in enumerate(result):
            masked=torch.full((256,),float("-inf"),dtype=torch.float64)
            masked[r["support"]]=z[i,r["support"]]
            self.assertEqual(int(masked.argmax()),r["conditional_prediction"])
            self.assertAlmostEqual(r["answer_nll"],r["support_nll"]+r["choice_nll"],places=12)
        agg=b.aggregate(result);self.assertEqual(agg["conditional_correct"]-agg["correct"],agg["kind_counts"][b.KINDS[1]])

    def test_11_support_mass_not_argmax_support(self):
        z,rows=example();z[:]=-100.;z[0,48]=z[0,49]=0.;z[0,70]=.5
        r=b.measure(z,rows)[0];self.assertGreater(r["support_mass"],.5);self.assertEqual(r["full_prediction"],70)

    def test_12_nonfinite(self):
        for v in (float("nan"),float("inf")):
            z,rows=example();z[0,70]=v
            with self.assertRaises(ValueError):b.measure(z,rows)

    def test_13_shape_dtype_and_grad(self):
        z,rows=example()
        for wrong in (z[:,:255],z.float(),z.clone().requires_grad_()):
            with self.assertRaises(ValueError):b.measure(wrong,rows)

    def test_14_parent_results_and_no_capability(self):
        rr=b.expected_results();self.assertEqual(len(rr),15)
        self.assertEqual([sum(r["quad_pass"] for r in rr if r["arm"]==a) for a in b.ARMS],[2,1,2])
        self.assertTrue(all(not r["two_char_pass"] for r in rr if r["seed"]==293004))
        self.assertFalse(b.manifest()["capability_gate_applicable"])

    def test_15_full_inventory(self):
        self.assertEqual(len(self.report["observations"]),38880);self.assertEqual(len(self.report["profile_language"]),540)
        self.assertEqual((len(self.summary["partitions"]),len(self.summary["comparisons"])),(90,60))
        self.assertEqual(sum(r["rows"] for r in self.summary["comparisons"]),25920)
        self.assertTrue(all(r["correct"]==r["conditional_correct"]==r["rows"] for r in self.summary["partitions"]))

    def test_16_missing_records_profiles_and_ids(self):
        for action in (0,1,2):
            records,data,metrics,parts=fixtures()
            if action==0:records.pop()
            elif action==1:records[0]["raw"]["quad"]["TRAIN"].pop("quadrupled")
            else:data["TRAIN"][1]["id"]=data["TRAIN"][0]["id"]
            with self.assertRaises(ValueError):b.analyze(records,data,metrics,parts)

    def test_17_parent_normal_totals(self):
        records,data,metrics,parts=fixtures();metrics[0]["two_char"]["totals"][0]["correct"]-=1
        with self.assertRaisesRegex(ValueError,"parent normal totals"):b.analyze(records,data,metrics,parts)

    def test_18_parent_roles_nll_and_unique_grid(self):
        for action in (0,1,2):
            records,data,metrics,parts=fixtures()
            if action==0:parts[0]["output_role_counts"]["other_fact"]=1
            elif action==1:parts[0]["final_normal_nll"]+=.01
            else:parts[-1]=parts[0]
            with self.assertRaises(ValueError):b.analyze(records,data,metrics,parts)

    def test_19_collapse_and_missing_pair(self):
        rows=dataset()["TRAIN"][:2];z=torch.zeros((2,256),dtype=torch.float64);z[:,48]=4.
        rr=b.measure(z,rows);self.assertEqual(b.collapse(rr),1)
        with self.assertRaises(ValueError):b.collapse(rr[:1])

    def test_20_compare_rescue_and_regression(self):
        z,rows=example();good=named(b.measure(z,rows));z[0,70]=10.;bad=named(b.measure(z,rows))
        self.assertEqual(b.compare(bad,good)["rescued"],1);self.assertEqual(b.compare(good,bad)["regressed"],1)
        self.assertEqual(b.compare(bad,good)["conditional_argmax_flips"],0)
        bad[0]["source_id"]="different"
        with self.assertRaises(ValueError):b.compare(good,bad)

    def test_21_same_kind_not_same_prediction(self):
        z,rows=example();z[0,70]=10.;a=named(b.measure(z,rows));z[0,71]=11.;c=named(b.measure(z,rows))
        r=b.compare(a,c);self.assertEqual(r["full_argmax_flips"],1)
        self.assertEqual(r["transitions"][b.KINDS[1]+"->"+b.KINDS[1]],1)
        with self.assertRaises(ValueError):b.aggregate([])

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c294-fixture")/str(i)/"summary.json").resolve() for i in range(20)]
        old=(NS(PARENT_SHA="e"*64),NS(SUMMARY_SHAS=("f"*64,)*15))
        p292=NS(PARENT_SHA="c"*64);p291=NS(PARENT_SHA="d"*64,context=lambda:old)
        parent=NS(PARENT_SHA="b"*64,context=lambda:(p292,p291),validate_result=Mock(),verify_artifacts=Mock())
        records,data,metrics,parts=fixtures();payload=parent_fixture(parts);parent.verify_artifacts.return_value=(payload,metrics)
        wanted=[b.PARENT_SHA,"b"*64,"c"*64,"d"*64,"e"*64]+["f"*64]*15;mapping=dict(zip(map(str,paths),wanted,strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:data),p267=NS(validate_data=Mock()))
        archive=dict(schema="fold-c293-support-eval-v1",records=records)
        with patch.object(b,"context",return_value=(parent,c)),patch.object(torch,"load",return_value=archive):yield paths,mapping,parent,payload,archive

    def test_22_twenty_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,payload,_):
            self.assertEqual(b.load_parent(paths)[0],payload)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_23_wrong_parent_and_archive(self):
        for action in (0,1,2):
            with self.loader_fixture() as (paths,_,_,p,archive):
                if action==0:p["status"]="PASS"
                elif action==1:p["source_blobs"].clear()
                else:archive["schema"]="wrong"
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_24_neural_guards_restore(self):
        for f in (lambda:torch.nn.Identity()(torch.ones(1)),lambda:torch.nn.Linear(1,1).load_state_dict({}),lambda:torch.save({},"FORBIDDEN.pt")):
            with b.no_neural(),self.assertRaisesRegex(RuntimeError,"C294 forbids"):f()
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_25_actual_protection_and_helper_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(603)]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1091-len(inputs)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();summary=directory/"summary.json";summary.write_text("summary",encoding="utf-8")
            mapping={str(summary.resolve()):b.PARENT_SHA};artifacts=[]
            for n in b.PARENT_OUTPUTS:
                p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*args):return (pins.get(args[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            with patch.object(b,"context",return_value=(parent,c)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*20,root))),(610,1106))
                c.missing=types.ModuleType("missing");c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([summary]*20,root)

    def test_26_result_contract(self):
        b.validate_result(result_fixture(self.summary))
        for k in b.ZERO_KEYS:
            p=result_fixture(copy.deepcopy(self.summary));p["validation_summary"][k]=False
            with self.assertRaises(ValueError):b.validate_result(p)
        p=result_fixture(copy.deepcopy(self.summary));p["validation_summary"]["comparisons"].pop()
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_27_actual_suite_id_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            s=b.regression_suite(Path.cwd());self.assertEqual(s.countTestCases(),b.manifest()["focused_tests"])
            self.assertEqual({t.id() for t in b.flatten(s)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        records,data,metrics,parts=fixtures()
        with patch.object(b,"context",return_value=(None,NS(audit=Audit()))),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=(parent_fixture(parts),records,data,metrics)):yield

    def test_28_roundtrip_order_and_no_overwrite(self):
        events=[];original=b.analyze
        def pc(*a):events.append("precheck");return protection()
        def analyze(*a):events.append("analyze");return original(*a)
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,patch.object(b,"precheck",side_effect=pc),patch.object(b,"analyze",side_effect=analyze),contextlib.redirect_stdout(io.StringIO()) as output:
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*20,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck","analyze","precheck"]);self.assertNotIn("input_sha256",output.getvalue());self.assertLess(len(output.getvalue()),4000)
            q,_=b.verify_artifacts(out,["x"]*20,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*20,output_dir=out,expected_head="f"*40)

    def test_29_byte_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*20,output_dir=out,expected_head="f"*40)
            path=out/"support-choice-report.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*20,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*20,"f"*40)

    def test_30_cp932_and_explicit_utf8(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in n.keywords))

    def test_31_runner_and_cli(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:22]",blocks[2]);self.assertIn("head = sys.argv[22]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),20)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
        argv=["prog","--summaries"]+[str(i) for i in range(20)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),20)

    def test_32_context_guard_and_count(self):
        c=NS(audit=Audit());parent=NS(context=lambda:(1,2,3,4,5,6,c),regression_modules=lambda root:["fixture"+str(i) for i in range(178)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c293_fact_support_loss=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            self.assertEqual(b.context(),(parent,c));self.assertEqual(len(b.regression_modules(Path.cwd())),179)
        b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c293_fact_support_loss"])


if __name__=="__main__":unittest.main()
