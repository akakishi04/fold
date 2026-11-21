"""Behavioral C290 fixtures; they do not claim user-local scientific results."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import math
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c290_saved_pair_margin_audit as b


def dataset():
    data={}
    for split,count in (("TRAIN",8),("HOLDOUT",4)):
        rows=[]
        for lang,e in itertools.product(("en","ja"),((0,1),(0,2),(1,2))):
            for order,j in itertools.product((e,e[::-1]),range(count)):
                for q,target in zip(e,(48,49),strict=True):
                    rows.append(dict(language=lang,entities=list(e),values=[j+10,j+20],permutation=list(order),query=q,target=target))
        data[split]=rows
    return data


def fixtures():
    data=dataset();zs={}
    for split,rows in data.items():
        z=torch.zeros((len(rows),256),dtype=torch.float64)
        z[torch.arange(len(rows)),torch.tensor([r["target"] for r in rows])]=4.
        zs[split]=z
    records=[];metrics=[]
    for seed,arm in b.identities():
        raw={};metric=dict(seed=seed,arm=arm)
        for task,profiles in b.PROFILES.items():
            raw[task]={s:{p:{v:zs[s] for v in ("normal","evidence_blind","query_blind")} for p in profiles} for s in data}
            metric[task]=dict(totals=[dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
                for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in profiles for l in ("en","ja")])
        records.append(dict(seed=seed,arm=arm,raw=raw));metrics.append(metric)
    return records,data,metrics


def parent_fixture():
    return dict(commit_sha=b.PARENT_EXECUTION,experiment_id="C289-v5b-early-pair-withdrawal",status="FAIL",
                source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256="a"*64,serialized_bytes=1) for n in b.PARENT_OUTPUTS],
                validation_summary=dict(seed_results=b.expected_results(),candidate_gate=False,
                    all_replays=True,all_groups_matched=True,all_auxiliary_prefixes_matched=True))


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<586:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1056)}


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(p):return json.loads(Path(p).read_text(encoding="utf-8"))
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


def example():
    z=torch.zeros((2,256),dtype=torch.float64);z[0,48]=2.;z[1,49]=2.
    return z,torch.tensor([48,49])


def named(values):
    return [dict(task="quad",split="HOLDOUT",profile="quadrupled",pair_key=["en",[0,1],[1,2],[0,1]],**v) for v in values]


class C290Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();torch.set_num_threads(2)
        cls.report,cls.summary=b.analyze(*fixtures())
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)

    def test_01_real_seal(self):
        b.validate_seal();self.assertEqual(b.MANIFEST_SHA,b.digest(b.manifest()))

    def test_02_bad_seals(self):
        for value in ("UNSEALED","A"*64,"0"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError):b.validate_seal()

    def test_03_zero_logits_closed_form(self):
        x=b.pair_values(torch.zeros((2,256),dtype=torch.float64),torch.tensor([48,49]))[0]
        self.assertEqual(x["assignment_gap"],0.);self.assertEqual(x["correct_answers"],0)
        self.assertAlmostEqual(x["pair_penalty"],math.log1p(math.e));self.assertAlmostEqual(x["mean_answer_nll"],math.log(256))

    def test_04_correct_assignment(self):
        x=b.pair_values(*example())[0];self.assertEqual(x["correct_answers"],2)
        self.assertTrue(x["margin_met"]);self.assertFalse(x["collapsed"])

    def test_05_swapped_assignment(self):
        z,y=example();x=b.pair_values(z.flip(0),y)[0]
        self.assertEqual(x["correct_answers"],0);self.assertEqual(x["assignment_gap"],-4.)

    def test_06_per_row_offsets(self):
        z,y=example();a=b.pair_values(z,y)[0];c=b.pair_values(z+torch.tensor([[10.],[-20.]]),y)[0]
        for key in ("assignment_gap","pair_penalty","mean_answer_nll"):self.assertAlmostEqual(a[key],c[key])
        z=torch.zeros((2,256),dtype=torch.float64);z[0,48]=z[0,49]=1e16;z[1,48]=z[1,49]=1.
        self.assertEqual(b.pair_values(z,y)[0]["assignment_gap"],0.)

    def test_07_pair_order_symmetry(self):
        z,y=example();a=b.pair_values(z,y)[0];c=b.pair_values(z.flip(0),y.flip(0))[0]
        self.assertEqual(a["assignment_gap"],c["assignment_gap"]);self.assertEqual(a["correct_answers"],c["correct_answers"])

    def test_08_margin_pass_can_miss_both_answers(self):
        z,y=example();z[:,70]=10.;x=b.pair_values(z,y)[0]
        self.assertTrue(x["margin_met"]);self.assertEqual(x["correct_answers"],0)
        self.assertEqual(b.aggregate([x])["margin_met_with_error"],1)

    def test_09_margin_pass_can_miss_one_answer(self):
        z,y=example();z[1,70]=10.;x=b.pair_values(z,y)[0]
        self.assertTrue(x["margin_met"]);self.assertEqual(x["correct_answers"],1)

    def test_10_both_correct_below_margin(self):
        z,y=example();x=b.pair_values(z*.1,y)[0]
        self.assertFalse(x["margin_met"]);self.assertEqual(x["correct_answers"],2)
        self.assertEqual(b.aggregate([x])["margin_not_met_with_both_correct"],1)

    def test_11_identical_predictions_do_not_imply_identical_logits(self):
        z,y=example();z[:,70]=10.;x=b.pair_values(z,y)[0]
        self.assertTrue(x["collapsed"]);self.assertEqual(x["assignment_gap"],4.)
        z[1]=z[0];self.assertEqual(b.pair_values(z,y)[0]["assignment_gap"],0.)

    def test_12_nonfinite_rejection(self):
        for v in (float("nan"),float("inf")):
            z,y=example();z[0,0]=v
            with self.assertRaises(ValueError):b.pair_values(z,y)

    def test_13_shape_and_dtype(self):
        for z,y in ((torch.zeros((3,256),dtype=torch.float64),torch.tensor([1,2,3])),
                    (torch.zeros((2,255),dtype=torch.float64),torch.tensor([1,2])),
                    (torch.zeros((2,256)),torch.tensor([1,2]))):
            with self.assertRaises(ValueError):b.pair_values(z,y)

    def test_14_grad_tracking_rejected(self):
        z,y=example();z.requires_grad_(True)
        with self.assertRaisesRegex(ValueError,"tensor contract"):b.pair_values(z,y)

    def test_15_label_validation(self):
        for y in (torch.tensor([-1,49]),torch.tensor([48,48]),torch.tensor([48.,49.])):
            with self.assertRaises(ValueError):b.pair_values(example()[0],y)

    def test_16_pair_index_coverage(self):
        for s,n in (("TRAIN",96),("HOLDOUT",48)):
            rows=dataset()[s];pairs=b.pair_indices(rows)
            self.assertEqual(len(pairs),n);self.assertEqual(sorted(i for _,ids in pairs for i in ids),list(range(2*n)))

    def test_17_missing_and_duplicate_query(self):
        for fn in (lambda r:r.pop(),lambda r:r[1].update(query=r[0]["query"])):
            rows=dataset()["TRAIN"];fn(rows)
            with self.assertRaises(ValueError):b.pair_indices(rows)

    def test_18_complete_audit_inventory(self):
        self.assertEqual(len(self.report["pairs"]),19440);self.assertEqual(len(self.summary["partitions"]),90)
        self.assertEqual(len(self.summary["comparisons"]),60)
        self.assertEqual(sum(x["pairs"] for x in self.summary["comparisons"]),12960)

    def test_19_parent_totals_must_reconstruct(self):
        records,data,metrics=fixtures();metrics[0]["quad"]["totals"][0]["correct"]-=1
        with self.assertRaisesRegex(ValueError,"parent normal totals"):b.analyze(records,data,metrics)

    def test_20_missing_models_profiles_and_views(self):
        for fn in (lambda r:r.pop(),lambda r:r[0]["raw"]["quad"]["TRAIN"].pop("quadrupled"),
                   lambda r:r[0]["raw"]["quad"]["TRAIN"]["quadrupled"].pop("normal")):
            records,data,metrics=fixtures();fn(records)
            with self.assertRaises(ValueError):b.analyze(records,data,metrics)

    def test_21_pair_sort_invariance(self):
        rows=dataset()["TRAIN"];pairs=b.pair_indices(rows);reverse=list(reversed(rows));other=b.pair_indices(reverse)
        self.assertEqual([k for k,_ in pairs],[k for k,_ in other])
        self.assertEqual([[rows[i]["target"] for i in ids] for _,ids in pairs],[[reverse[i]["target"] for i in ids] for _,ids in other])

    def test_22_aggregate_denominators(self):
        a=b.pair_values(*example())[0];z,y=example();z[1,70]=10.;c=b.pair_values(z,y)[0]
        x=b.aggregate([a,c]);self.assertEqual((x["pairs"],x["rows"],x["correct"],x["both_correct"],x["one_correct"]),(2,4,3,1,1))
        with self.assertRaises(ValueError):b.aggregate([])

    def test_23_no_prediction_change(self):
        a=named(b.pair_values(*example()));x=b.compare_pairs(a,a)
        self.assertEqual(x["argmax_flips"],0);self.assertEqual(x["changed_prediction_pairs"],0)

    def test_24_rescue_and_regression_direction(self):
        z,y=example();good=named(b.pair_values(z,y));bad=named(b.pair_values(z.flip(0),y))
        self.assertEqual(b.compare_pairs(bad,good)["rescued_both_correct"],1)
        self.assertEqual(b.compare_pairs(good,bad)["regressed_both_correct"],1)
        self.assertEqual(b.compare_pairs(bad,good)["argmax_flips"],2)

    def test_25_comparison_identity(self):
        a=named(b.pair_values(*example()));c=copy.deepcopy(a);c[0]["pair_key"][0]="ja"
        with self.assertRaisesRegex(ValueError,"comparison identity"):b.compare_pairs(a,c)

    def test_26_exact_parent_contract(self):
        b.validate_parent(parent_fixture())
        for fn in (lambda p:p.update(status="PASS"),lambda p:p["source_blobs"].clear(),
                   lambda p:p["artifacts"][0].update(sha256="bad"),lambda p:p["validation_summary"].update(all_auxiliary_prefixes_matched=False)):
            p=parent_fixture();fn(p)
            with self.assertRaises(ValueError):b.validate_parent(p)

    def test_27_sixteen_hashes_before_dispatch(self):
        paths=[(Path("/c290-fixture")/str(i)/"summary.json").resolve() for i in range(16)]
        wanted=[b.PARENT_SHA]+[str(i)*64 for i in range(1,10)]+["a"*64]*6
        mapping=dict(zip(map(str,paths),wanted,strict=True));records,data,metrics=fixtures()
        parent=NS(SUMMARY_SHAS=tuple(wanted[1:]),verify_artifacts=Mock(return_value=(parent_fixture(),metrics)),validate_result=Mock())
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:data),p267=NS(validate_data=Mock()))
        with patch.object(b,"context",return_value=(parent,c)),patch.object(torch,"load",return_value=dict(schema="fold-c289-early-pair-eval-v1",records=records)):
            self.assertEqual(b.load_parent(paths)[1],records)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_28_forbidden_operations_restore(self):
        for fn in (lambda:torch.nn.Identity()(torch.ones(1)),lambda:torch.nn.Linear(1,1).load_state_dict({}),lambda:torch.save({},"FORBIDDEN.pt")):
            with b.no_neural(),self.assertRaisesRegex(RuntimeError,"C290 forbids"):fn()
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_29_result_contract(self):
        b.validate_result(result_fixture(self.summary))
        for k in b.ZERO_KEYS:
            p=result_fixture(copy.deepcopy(self.summary));p["validation_summary"][k]=False
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_30_bad_result_inventory(self):
        for fn in (lambda p:p["validation_summary"]["partitions"].pop(),lambda p:p.update(gate_f_candidate=True),lambda p:p["source_blobs"].pop(b.PARENT_SOURCE)):
            p=result_fixture(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_31_actual_precheck_maps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);lm=[f"fold_lm/fixture{i}.py" for i in range(6)]
            names=[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,290)];names[-1]=b.PARENT_SOURCE
            names+=lm;names += [f"accepted/{i}.txt" for i in range(580-len(names))]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n)
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1041-len(inputs)):
                p=root/f"input{i}";p.write_text("input");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();summary=directory/"summary.json";summary.write_text("summary")
            mapping={str(summary.resolve()):b.PARENT_SHA};artifacts=[]
            for n in b.PARENT_OUTPUTS:
                p=directory/n;p.write_text("parent");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}),factory=NS(LM_SOURCES=lm))
            payload=dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts)
            with patch.object(b,"context",return_value=(None,c)),patch.object(b,"load_parent",return_value=(payload,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*16,root))),(586,1056))
                pins.pop(b.PARENT_SOURCE)
                with self.assertRaises(ValueError):b.precheck([summary]*16,root)

    def test_32_actual_suite_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),b.manifest()["focused_tests"])
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    def test_33_duplicate_suite(self):
        class Dummy(unittest.TestCase):
            def runTest(self):pass
            def id(self):return "duplicate"
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy(),Dummy()])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_34_cli(self):
        argv=["prog","--summaries"]+[str(i) for i in range(16)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(16)])

    def _run_context(self):
        records,data,metrics=fixtures()
        return patch.object(b,"context",return_value=(None,NS(audit=Audit()))),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=(parent_fixture(),records,data,metrics))

    def test_35_run_roundtrip_no_overwrite(self):
        patches=self._run_context()
        with tempfile.TemporaryDirectory() as tmp,patches[0],patches[1],patches[2],contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*16,output_dir=out,expected_head="f"*40)
            q,_=b.verify_artifacts(out,["x"]*16,"f"*40);self.assertEqual(q,p)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*16,output_dir=out,expected_head="f"*40)

    def test_36_hash_and_semantic_tamper(self):
        patches=self._run_context()
        with tempfile.TemporaryDirectory() as tmp,patches[0],patches[1],patches[2],contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*16,output_dir=out,expected_head="f"*40)
            path=out/"pair-margin-report.json";path.write_text("{}")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*16,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*16,"f"*40)

    def test_37_compact_receipt_and_phase_order(self):
        patches=self._run_context();capture=io.StringIO();events=[]
        def pc(*a):events.append("precheck");return protection()
        original=b.analyze
        def analyze(*a):events.append("analyze");return original(*a)
        with tempfile.TemporaryDirectory() as tmp,patches[0],patches[2],patch.object(b,"precheck",side_effect=pc),patch.object(b,"analyze",side_effect=analyze),contextlib.redirect_stdout(capture):
            b.run(summaries=["x"]*16,output_dir=Path(tmp)/"run",expected_head="f"*40)
        self.assertEqual(events,["precheck","analyze","precheck"])
        text=capture.getvalue();self.assertIn("summary_sha256",text);self.assertNotIn("input_sha256",text)
        self.assertLess(len(text),4000)

    def test_38_runner_blocks_and_cli(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c290.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c290.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:18]",blocks[2]);self.assertIn("head = sys.argv[18]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),16)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_39_own_inventory_and_import_binding(self):
        root=Path(__file__).resolve().parents[1]
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),40)
        self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for n in b.OWN:self.assertTrue((root/n).is_file())
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c289_early_pair_withdrawal"])

    def test_40_context_and_guards(self):
        import types
        package=types.ModuleType("fold_lm.v05_benchmarks");c=NS(audit=Audit());parent=NS(context=lambda:(0,1,2,3,4,c))
        package.model_c289_early_pair_withdrawal=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,c))
        b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)


if __name__=="__main__":unittest.main()
