"""C311 authoring controls: synthetic answers are not FOLD ability evidence."""
from __future__ import annotations
import ast
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
from types import SimpleNamespace as NS
import types
import unittest
from unittest.mock import Mock,patch
from fold_lm.v05_benchmarks import model_c311_saved_error_context as b


def data_fixture():
    data = {s:[] for s in b.SPLITS}
    for entities,values,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split = "HOLDOUT" if (values[1]-values[0])%4 == 2 else "TRAIN"
        for order,query in itertools.product((entities,entities[::-1]),entities):
            data[split].append(dict(id=f"{language}:{entities}:{values}:{order}:{query}", language=language,
                                    entities=list(entities), values=list(values), permutation=list(order),query=query,
                                    target=48+values[entities.index(query)]))
    assert len(data["TRAIN"]) == 192 and len(data["HOLDOUT"]) == 96
    return data


def report_fixture(data):
    rows = data["TRAIN"]+data["HOLDOUT"]
    blocks,original = [],[]
    for seed,arm in b.identities():
        for n in b.LENGTHS:
            profiles = {p:[r["target"] for r in rows] for p in b.PROFILES}
            blocks.append(dict(seed=seed,arm=arm,identifier_length=n,predictions=profiles,
                               tied_max_indices={p:[] for p in b.PROFILES}))
            for profile in b.PROFILES:
                for split in b.SPLITS:
                    for lang in ("en","ja"):
                        count = sum(r["language"] == lang for r in data[split])
                        original.append(dict(seed=seed,arm=arm,identifier_length=n,profile=profile,split=split,
                                             language=lang,rows=count,correct=count,pairs=count//2,collapsed_pairs=0,
                                             tied_max_rows=0))
    return dict(row_ids=[r["id"] for r in rows],permutations=[list(x) for x in itertools.permutations(range(4))],
                destination_indices=[[0]*288 for _ in range(24)],predictions=blocks,
                original_totals=original,summary=dict(diagnostic_complete=True,observations=51840))


def source_guard_fixture():
    pins = {name:"b"*40 for name in b.OWN}
    pins[b.PARENT_SOURCE] = b.PARENT_BLOB
    while len(pins) < 712: pins[f"fake/{len(pins)}"] = "b"*40
    protected = {f"/fake/input/{i}":"a"*64 for i in range(1333)}
    return pins,protected


def context_audit():
    class Audit:
        @staticmethod
        def sha(path):
            path=Path(path)
            return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "a"*64
        @staticmethod
        def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
        @staticmethod
        def safe_child(folder,name): return Path(folder)/name
        @staticmethod
        def git(root,*args):
            if args[0] == "rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
            if args[0] == "branch": return b"feat/sft-target-loss\n"
            return b""
    return NS(audit=Audit())


class C311Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = data_fixture();cls.old = report_fixture(cls.data)
        cls.report, cls.summary = b.analyze(cls.old,cls.data)

    def test_01_manifest_seal(self):
        b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_seal_tamper(self):
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaisesRegex(ValueError,"manifest seal"): b.validate_seal()

    def test_03_answer_correct(self):
        r = self.data["TRAIN"][0];self.assertEqual(b.describe_answer(r,r["target"]),"correct")

    def test_04_answer_other_fact(self):
        r=self.data["TRAIN"][0]; other = 48+r["values"][1-r["entities"].index(r["query"])]
        self.assertEqual(b.describe_answer(r,other),"other_fact")

    def test_05_unmentioned_digit(self):
        r=self.data["TRAIN"][0]; other={48,49,50,51}-{48+x for x in r["values"]}
        self.assertEqual(b.describe_answer(r,min(other)),"unmentioned_digit")

    def test_06_other_class(self):
        r=self.data["TRAIN"][0];self.assertEqual(b.describe_answer(r,0),"non_digit")
        with self.assertRaises(ValueError):b.describe_answer(r,256)

    def test_07_perfect_group_inventory(self):
        self.assertEqual((len(self.report["pairs"]),len(self.report["language_splits"]),len(self.report["length_signatures"])),(2160,720,90))
        self.assertEqual(sum(x["rows"] for x in self.report["pairs"]),51840)
        self.assertTrue(all(x["rows"] == 24 and x["correct"] == 24 for x in self.report["pairs"]))
        self.assertEqual(self.summary["observations"],51840)

    def test_08_signature_all_correct(self):
        self.assertTrue(all(s["patterns"]["1111"] == s["rows"] for s in self.report["length_signatures"]))
        self.assertTrue(all(s["four_to_five"]["both_correct"] == s["rows"] for s in self.report["length_signatures"]))

    def test_09_error_persistence_and_five_introduction(self):
        raw=copy.deepcopy(self.old)
        blocks=[next(x for x in raw["predictions"] if (x["seed"],x["arm"],x["identifier_length"]) == (309002,"core_slow",n)) for n in b.LENGTHS]
        for n,blk in zip(b.LENGTHS,blocks):
            if n>=4: blk["predictions"]["repeat"][192] = 0
        # Update corresponding parent original totals to preserve independent checksum test.
        for r in raw["original_totals"]:
            if r["seed"]==309002 and r["arm"]=="core_slow" and r["identifier_length"]>=4 and r["profile"]=="repeat" and r["split"]=="HOLDOUT" and r["language"]==self.data["HOLDOUT"][0]["language"]:
                r["correct"] -= 1
        report,_=b.analyze(raw,self.data)
        s=next(x for x in report["length_signatures"] if x["seed"]==309002 and x["arm"]=="core_slow" and x["split"]=="HOLDOUT" and x["profile"]=="repeat")
        self.assertEqual(s["patterns"]["1100"],1)
        self.assertEqual(s["four_to_five"]["both_wrong"],1)

    def test_10_five_new_failure(self):
        raw=copy.deepcopy(self.old)
        blk=next(x for x in raw["predictions"] if x["seed"]==309002 and x["arm"]=="core_slow" and x["identifier_length"]==5)
        blk["predictions"]["repeat"][192]=0
        for r in raw["original_totals"]:
            if r["seed"]==309002 and r["arm"]=="core_slow" and r["identifier_length"]==5 and r["profile"]=="repeat" and r["split"]=="HOLDOUT" and r["language"]==self.data["HOLDOUT"][0]["language"]:r["correct"]-=1
        report,_=b.analyze(raw,self.data)
        s=next(x for x in report["length_signatures"] if x["seed"]==309002 and x["arm"]=="core_slow" and x["split"]=="HOLDOUT" and x["profile"]=="repeat")
        self.assertEqual(s["patterns"]["1110"],1)
        self.assertEqual(s["four_to_five"]["four_only_correct"],1)

    def test_11_pair_groups_track_other_fact(self):
        raw=copy.deepcopy(self.old);blk=raw["predictions"][0];row=self.data["TRAIN"][0]
        blk["predictions"]["repeat"][0]=48+row["values"][1-row["entities"].index(row["query"])]
        for r in raw["original_totals"]:
            if (r["seed"],r["arm"],r["identifier_length"],r["profile"],r["split"],r["language"])==(309001,"full_train",2,"repeat","TRAIN",row["language"]):r["correct"]-=1;r["collapsed_pairs"]+=1
        report,_=b.analyze(raw,self.data)
        g=next(x for x in report["pairs"] if (x["seed"],x["arm"],x["identifier_length"],x["profile"],x["values"])==(309001,"full_train",2,"repeat",row["values"]))
        self.assertEqual(g["other_fact"],1)

    def test_12_wrong_parent_total_rejected(self):
        raw=copy.deepcopy(self.old);raw["original_totals"][0]["correct"]-=1
        with self.assertRaisesRegex(ValueError,"original totals"):b.analyze(raw,self.data)

    def test_13_wrong_row_order_rejected(self):
        raw=copy.deepcopy(self.old);raw["row_ids"].reverse()
        with self.assertRaisesRegex(ValueError,"original row order"):b.analyze(raw,self.data)

    def test_14_missing_prediction_rejected(self):
        raw=copy.deepcopy(self.old);raw["predictions"][0]["predictions"]["repeat"].pop()
        with self.assertRaisesRegex(ValueError,"prediction count"):b.analyze(raw,self.data)

    def test_15_bad_tie_and_source_rejected(self):
        raw=copy.deepcopy(self.old);raw["predictions"][0]["tied_max_indices"]["repeat"]=[288]
        with self.assertRaisesRegex(ValueError,"tie indices"):b.analyze(raw,self.data)

    def test_16_error_count_conservation(self):
        with self.assertRaises(ValueError):b.count_group(["invented"])
        self.assertEqual(b.count_group(["correct","other_fact","unmentioned_digit","non_digit"]),
                         dict(rows=4,correct=1,other_fact=1,unmentioned_digit=1,non_digit=1))

    def test_17_result_schema_and_invalid_gate(self):
        pins,inputs=source_guard_fixture()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",diagnostic_execution_valid=True,
               capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,source_blobs=pins,
               input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=self.summary)
        b.validate_result(p)
        p["gate_f_candidate"]=True
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_18_parent_hash_guard_before_dispatch(self):
        paths=[(Path("/fixtures")/str(i)/"summary.json").resolve() for i in range(37)]
        hashes=[str(i%10)*64 for i in range(37)]
        mapping=dict(zip(map(str,paths),hashes))
        parent=NS(PARENT_SHA="1"*64,context=lambda:(NS(parent_hashes=lambda _:tuple(hashes[2:]),context=lambda:(None,)),None,None),
                  no_neural=contextlib.nullcontext,verify_artifacts=Mock(return_value=(dict(experiment_id=b.EXPERIMENT_ID),{})),validate_result=Mock())
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,c)),patch.object(b,"parent_hashes",return_value=tuple(hashes)):
            with self.assertRaisesRegex(ValueError,"parent identity"):b.load_parent(paths)
            self.assertEqual(parent.verify_artifacts.call_count,1)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="f"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaisesRegex(ValueError,"parent hashes"):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_19_regression_id_accounting(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=[f"fixture.{i}" for i in range(4965)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(k) for k in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4965)
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    @contextlib.contextmanager
    def run_fixture(self):
        c=context_audit(); events=[];pins,inputs=source_guard_fixture()
        parent=NS(no_neural=contextlib.nullcontext)
        def precheck(*args):events.append("precheck");return pins,inputs
        def loader(*args):events.append("load");return {},self.old,self.data
        with patch.object(b,"context",return_value=(parent,c)),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"load_parent",side_effect=loader):
            yield events

    def test_20_actual_run_load_write_verify(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)/"output";p=b.run(summaries=["x"]*37,output_dir=folder,expected_head="f"*40)
            self.assertEqual(events,["precheck","load","precheck"])
            self.assertEqual(b.verify_artifacts(folder,["x"]*37,"f"*40)[0],p)
            self.assertEqual(events[-1],"load")
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*37,output_dir=folder,expected_head="f"*40)

    def test_21_byte_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)/"output";p=b.run(summaries=["x"]*37,output_dir=folder,expected_head="f"*40)
            path=folder/"error-context-report.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(folder,["x"]*37,"f"*40)
            desc=next(x for x in p["artifacts"] if x["file"]==path.name)
            desc.update(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),serialized_bytes=path.stat().st_size)
            (folder/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(folder,["x"]*37,"f"*40)

    def test_22_cli_context_and_guard(self):
        argv=["prog","--summaries"]+[str(i) for i in range(37)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:
            b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),37)
        b.guard(Path.cwd(),"f"*40,context_audit())
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,context_audit())

    def test_23_runner_paths_embedded_blocks(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/b.OWN[2]).read_text(encoding="utf-8")
        launch=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S)
        self.assertEqual(len(blocks),3)
        self.assertIn("model_c311_saved_error_context",runner)
        self.assertIn("test_v05_c311_saved_error_context",runner)
        self.assertNotIn("value_renaming_audit",runner)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:39]",blocks[2]);self.assertIn("head = sys.argv[39]",blocks[2])
        self.assertEqual(len(re.findall(r"runs\\c\d{3}-.*?\\summary.json",launch)),37)
        self.assertLess(launch.index("-Mode Validate"),launch.index("-Mode Execute"))
        self.assertLess(launch.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launch.index("publish_experiment_log.ps1"))

    def test_24_source_utf8_imports_and_count(self):
        root=Path(__file__).resolve().parents[1]
        for name in b.OWN:self.assertTrue((root/name).read_text(encoding="utf-8"))
        tree=ast.parse((root/b.OWN[0]).read_text(encoding="utf-8"))
        imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c310_value_renaming_audit"])
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24)
        self.assertEqual(b.MANIFEST_SHA in (root/b.OWN[4]).read_text(encoding="utf-8"),True)


if __name__ == "__main__": unittest.main()
