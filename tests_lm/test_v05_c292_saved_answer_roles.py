"""C292 behavioral fixtures; no assertion of user-local scientific completion."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c292_saved_answer_roles as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for perm,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(id=str((language,e,v,perm,q)),language=language,entities=list(e),values=list(v),
                                    permutation=list(perm),query=q,target=48+v[e.index(q)]))
    return data


def fixtures():
    data=dataset();z={}
    for s,rows in data.items():
        z[s]=torch.zeros((len(rows),256),dtype=torch.float64)
        z[s][torch.arange(len(rows)),torch.tensor([r["target"] for r in rows])]=4.
    records=[];metrics=[]
    for seed,arm in b.identities():
        raw={t:{s:{p:{v:z[s] for v in ("normal","evidence_blind","query_blind")} for p in profiles} for s in data} for t,profiles in b.PROFILES.items()}
        metric=dict(seed=seed,arm=arm)
        for t,profiles in b.PROFILES.items():
            metric[t]=dict(totals=[dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
                                  for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in profiles for l in ("en","ja")])
        records.append(dict(seed=seed,arm=arm,raw=raw));metrics.append(metric)
    return records,data,metrics


def parent_fixture():
    return dict(experiment_id="C291-v5b-answer-wise-hardest-rival-margin",commit_sha=b.PARENT_EXECUTION,status="FAIL",
                source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n,sha256="a"*64) for n in b.PARENT_OUTPUTS],
                validation_summary=dict(seed_results=b.expected_results(),candidate_gate=False,all_groups_matched=True,all_replays=True))


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<598:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1081)}


class Audit:
    @staticmethod
    def sha(path):
        path=Path(path);return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "a"*64
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n):return Path(root)/n
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


def observed(row,prediction):
    return dict(**{k:row[k] for k in ("language","entities","values","permutation","query")},
                task="quad",split="HOLDOUT",profile="quadrupled",source_id=row["id"],**b.answer_role(row,prediction))


class C292Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();torch.set_num_threads(2)
        cls.report,cls.summary=b.analyze(*fixtures());cls.row=dataset()["TRAIN"][0]
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)

    def test_01_real_seal(self):
        b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals(self):
        for value in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError):b.validate_seal()

    def test_03_four_roles(self):
        row=self.row
        self.assertEqual([b.answer_role(row,p)["role"] for p in (48,49,50,65)],list(b.ROLES))

    def test_04_query_and_fact_order(self):
        r=copy.deepcopy(self.row);r["query"]=r["entities"][1];r["target"]=49
        self.assertEqual(b.answer_role(r,48)["role"],"other_fact")
        before=b.answer_role(r,49);r["permutation"].reverse();self.assertEqual(b.answer_role(r,49),before)
        r["entities"].reverse();r["values"].reverse();self.assertEqual(b.answer_role(r,49),before)

    def test_05_bad_fact_domain(self):
        for fn in (lambda r:r.update(values=[0,0]),lambda r:r.update(values=[0,4]),lambda r:r.update(entities=[0,0]),lambda r:r.update(permutation=[0,2])):
            r=copy.deepcopy(self.row);fn(r)
            with self.assertRaises(ValueError):b.answer_role(r,48)

    def test_06_wrong_target_binding(self):
        r=copy.deepcopy(self.row);r["target"]=49
        with self.assertRaisesRegex(ValueError,"target/value binding"):b.answer_role(r,48)

    def test_07_bad_prediction(self):
        for pred in (-1,256,48.,True):
            with self.assertRaises(ValueError):b.answer_role(self.row,pred)

    def test_08_exhaustive_256_class_partition(self):
        rows=[b.answer_role(self.row,p) for p in range(256)];x=b.tally(rows)
        self.assertEqual(x["role_counts"],dict(zip(b.ROLES,(1,1,2,252),strict=True)))
        self.assertEqual((x["rows"],x["correct"],x["errors"]),(256,1,255))

    def test_09_confusion_and_empty(self):
        x=b.tally([b.answer_role(self.row,49)]*3);self.assertEqual(x["confusion"],[[48,49,3]])
        with self.assertRaises(ValueError):b.tally([])
        with self.assertRaises(ValueError):b.tally([dict(role="invented")])

    def test_10_collapse_requires_both_queries(self):
        rows=dataset()["TRAIN"][:2];obs=[observed(r,48) for r in rows]
        self.assertEqual(b.collapse(obs),1)
        with self.assertRaises(ValueError):b.collapse(obs[:1])

    def test_11_exact_changes_and_same_role_changes(self):
        good=[observed(self.row,48)];bad=[observed(self.row,50)];otherbad=[observed(self.row,51)]
        self.assertEqual(b.compare(bad,good)["rescued"],1);self.assertEqual(b.compare(good,bad)["regressed"],1)
        x=b.compare(bad,otherbad);self.assertEqual(x["argmax_flips"],1)
        self.assertEqual(x["transitions"]["absent_known_value->absent_known_value"],1)

    def test_12_comparison_identity(self):
        a=[observed(self.row,48)];c=copy.deepcopy(a);c[0]["source_id"]="different"
        with self.assertRaises(ValueError):b.compare(a,c)

    def test_13_complete_inventory(self):
        self.assertEqual(len(self.report["observations"]),38880)
        self.assertEqual(len(self.report["profile_language"]),540)
        self.assertEqual((len(self.summary["partitions"]),len(self.summary["value_pairs"]),len(self.summary["comparisons"])),(90,540,60))
        self.assertEqual(sum(x["rows"] for x in self.summary["comparisons"]),25920)
        self.assertTrue(all(x["correct"]==x["rows"] for x in self.summary["partitions"]))

    def test_14_missing_record_profile_view(self):
        for fn in (lambda r:r.pop(),lambda r:r[0]["raw"]["quad"]["TRAIN"].pop("quadrupled"),lambda r:r[0]["raw"]["quad"]["TRAIN"]["quadrupled"].pop("normal")):
            records,data,metrics=fixtures();fn(records)
            with self.assertRaises(ValueError):b.analyze(records,data,metrics)

    def test_15_logit_contract(self):
        for fn in (lambda z:z.float(),lambda z:z[:,:255],lambda z:z.clone().requires_grad_(),lambda z:z+float("nan")):
            records,data,metrics=fixtures();views=records[0]["raw"]["two_char"]["TRAIN"]["doubled"]
            views["normal"]=fn(views["normal"])
            with self.assertRaisesRegex(ValueError,"saved logits"):b.analyze(records,data,metrics)

    def test_16_data_duplicate_or_missing(self):
        for fn in (lambda d:d["TRAIN"].pop(),lambda d:d["TRAIN"][1].update(id=d["TRAIN"][0]["id"])):
            records,data,metrics=fixtures();fn(data)
            with self.assertRaises(ValueError):b.analyze(records,data,metrics)

    def test_17_parent_counts_must_match(self):
        records,data,metrics=fixtures();metrics[0]["two_char"]["totals"][0]["correct"]-=1
        with self.assertRaisesRegex(ValueError,"parent normal totals"):b.analyze(records,data,metrics)

    def test_18_value_pair_denominators(self):
        for group in self.summary["value_pairs"]:self.assertEqual(group["rows"],72)
        for group in self.summary["partitions"]:
            selected=[x for x in self.summary["value_pairs"] if all(x[k]==group[k] for k in ("seed","arm","task","split"))]
            self.assertEqual(sum(x["rows"] for x in selected),group["rows"])

    @contextlib.contextmanager
    def load_fixture(self):
        paths=[(Path("/c292-fixture")/str(i)/"summary.json").resolve() for i in range(18)]
        old=(NS(PARENT_SHA="c"*64),NS(SUMMARY_SHAS=("d"*64,)*15))
        parent=NS(PARENT_SHA="b"*64,context=lambda:old,validate_result=Mock(),verify_artifacts=Mock())
        records,data,metrics=fixtures();payload=parent_fixture();parent.verify_artifacts.return_value=(payload,metrics)
        wanted=[b.PARENT_SHA,"b"*64,"c"*64]+["d"*64]*15;mapping=dict(zip(map(str,paths),wanted,strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:data),p267=NS(validate_data=Mock()))
        with patch.object(b,"context",return_value=(parent,c)),patch.object(torch,"load",return_value=dict(schema="fold-c291-answer-margin-eval-v1",records=records)):
            yield paths,mapping,parent,payload

    def test_19_all_hashes_before_dispatch(self):
        with self.load_fixture() as (paths,mapping,parent,payload):
            self.assertEqual(b.load_parent(paths)[0],payload)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_20_parent_result_and_source(self):
        for fn in (lambda p:p.update(status="PASS"),lambda p:p["source_blobs"].clear(),lambda p:p["validation_summary"]["seed_results"].pop()):
            with self.load_fixture() as (paths,_,_,payload):
                fn(payload)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_21_no_neural_guards_restore(self):
        for fn in (lambda:torch.nn.Identity()(torch.ones(1)),lambda:torch.nn.Linear(1,1).load_state_dict({}),lambda:torch.save({},"FORBIDDEN.pt")):
            with b.no_neural(),self.assertRaisesRegex(RuntimeError,"C292 forbids"):fn()
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_22_actual_protection_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(591)]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1066-len(inputs)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();summary=directory/"summary.json";summary.write_text("summary",encoding="utf-8")
            mapping={str(summary.resolve()):b.PARENT_SHA};artifacts=[]
            for n in b.PARENT_OUTPUTS:
                p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            payload=dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,c)),patch.object(b,"load_parent",return_value=(payload,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*18,root))),(598,1081))
                missing=types.ModuleType("missing");missing.__file__=str(root/"unprotected.py");c.missing=missing
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([summary]*18,root)

    def test_23_result_contract(self):
        b.validate_result(result_fixture(self.summary))
        for key in b.ZERO_KEYS:
            p=result_fixture(copy.deepcopy(self.summary));p["validation_summary"][key]=False
            with self.assertRaises(ValueError):b.validate_result(p)
        p=result_fixture(copy.deepcopy(self.summary));p["validation_summary"]["value_pairs"].pop()
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_24_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),b.manifest()["focused_tests"])
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        records,data,metrics=fixtures()
        with patch.object(b,"context",return_value=(None,NS(audit=Audit()))),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=(parent_fixture(),records,data,metrics)):
            yield

    def test_25_roundtrip_and_no_overwrite(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*18,output_dir=out,expected_head="f"*40)
            q,_=b.verify_artifacts(out,["x"]*18,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*18,output_dir=out,expected_head="f"*40)

    def test_26_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*18,output_dir=out,expected_head="f"*40)
            path=out/"answer-role-report.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*18,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*18,"f"*40)

    def test_27_phase_order_and_compact_receipt(self):
        events=[];original=b.analyze
        def pc(*a):events.append("precheck");return protection()
        def analyze(*a):events.append("analyze");return original(*a)
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,patch.object(b,"precheck",side_effect=pc),patch.object(b,"analyze",side_effect=analyze),contextlib.redirect_stdout(io.StringIO()) as capture:
            b.run(summaries=["x"]*18,output_dir=Path(tmp)/"run",expected_head="f"*40)
        self.assertEqual(events,["precheck","analyze","precheck"]);self.assertNotIn("input_sha256",capture.getvalue())
        self.assertLess(len(capture.getvalue()),4000)

    def test_28_cli(self):
        args=["prog","--summaries"]+[str(i) for i in range(18)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),18)

    def test_29_utf8_default_independence(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_30_runner_blocks_and_paths(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:20]",blocks[2]);self.assertIn("head = sys.argv[20]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),18)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_31_context_and_module_inventory(self):
        c=NS();parent=NS(context=lambda:(1,2,3,4,5,6,c),regression_modules=lambda root:["fixture"+str(i) for i in range(176)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c291_answer_margin=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            self.assertEqual(b.context(),(parent,c));self.assertEqual(len(b.regression_modules(Path.cwd())),177)
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c291_answer_margin"])

    def test_32_guard_and_test_count(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])


if __name__=="__main__":unittest.main()
