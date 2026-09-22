import ast
import copy
import hashlib
import inspect
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from fold_lm.v05_benchmarks import gate_f_c229_cost_profile as b

REAL_PROFILE_CELL=b.profile_cell


def profile_fixture(q,enabled):
    specs={"candidate_update":("fold_lm/v05/memory_bank.py","ChunkedMemoryBank.apply",12),
        "candidate_query":("fold_lm/v05/memory_bank.py","ChunkedMemoryBank.read",12*q),
        "cached_update":("fold_lm/v05_benchmarks/gate_f_c228_update_query_cost.py","refresh",12),
        "cached_query":("fold_lm/v05_benchmarks/gate_f_c227_factor_reuse.py","query_cached",12*q)}
    reports={}
    for phase,(file,name,count) in specs.items():
        rows=[dict(file=file,line=1,function=name,calls=count,primitive_calls=count,self_ns=10,cumulative_ns=20)] if enabled else []
        reports[phase]=dict(enabled=enabled,invocations=12,observed_wall_ns=200,self_total_ns=10 if enabled else 0,functions=rows)
    return dict(reports=reports,checks=[dict(passed=True) for _ in range(12)],quality_pass=True,
                retained_inventory={"candidate":{"x":{"bytes":1,"sha256":"a"}},"cached":{"y":{"bytes":1,"sha256":"b"}}},
                profiler_restored=True)


def fixture_cell(n=2,q=1):
    off,on=profile_fixture(q,False),profile_fixture(q,True)
    anchor=dict(retained_inventory=off["retained_inventory"],stream_ratio_h1h2_over_cached=3.0)
    with patch.object(b,"trajectory",side_effect=[off,on]):
        return REAL_PROFILE_CELL(object(),n,q,anchor)


class C229Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_scope_is_diagnostic_not_optimization(self):
        m=b.manifest()
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["performance_superiority_required"])
        self.assertFalse(m["profiling_time_is_speed_evidence"])
        self.assertFalse(m["gate_f_candidate"])
        self.assertEqual(m["new_training_steps"],0)

    def test_03_off_callback_executed(self):
        recorder=b.PhaseRecorder(False);calls=[]
        self.assertEqual(recorder.call(lambda:calls.append(1) or 7),7)
        self.assertEqual(calls,[1]);self.assertEqual(recorder.invocations,1)
        self.assertEqual(recorder.report()["functions"],[])

    def test_04_real_profile_counts_torch_calls(self):
        recorder=b.PhaseRecorder(True)
        A=torch.eye(2,dtype=torch.float64);rhs=torch.ones(2,dtype=torch.float64)
        for _ in range(12):
            self.assertTrue(torch.equal(recorder.call(lambda:torch.linalg.solve(A,rhs)),rhs))
        report=recorder.report()
        self.assertTrue(b.report_valid(report,True))
        calls=sum(r["calls"] for r in report["functions"] if "linalg_solve" in r["function"])
        self.assertEqual(calls,12)

    def test_05_profile_exception_restores_hook(self):
        recorder=b.PhaseRecorder(True)
        def fail():raise RuntimeError("expected")
        with self.assertRaises(RuntimeError):recorder.call(fail)
        self.assertIsNone(sys.getprofile())
        self.assertEqual(recorder.invocations,1)

    def test_06_existing_profile_not_overwritten(self):
        old=sys.getprofile()
        def external(*args):pass
        sys.setprofile(external)
        try:
            with self.assertRaises(ValueError):b.PhaseRecorder(True).call(lambda:1)
            self.assertIs(sys.getprofile(),external)
        finally:sys.setprofile(old)

    def test_07_self_and_cumulative_are_separate(self):
        recorder=b.PhaseRecorder(True)
        def child():return sum(range(50))
        def outer():return child()
        recorder.call(outer)
        r=recorder.report()
        self.assertEqual(r["self_total_ns"],sum(x["self_ns"] for x in r["functions"]))
        self.assertTrue(all(x["cumulative_ns"] >= x["self_ns"] for x in r["functions"]))
        self.assertTrue(any(x["function"].endswith(".outer") for x in r["functions"]))

    def test_08_off_error_propagates(self):
        with self.assertRaises(ZeroDivisionError):b.PhaseRecorder(False).call(lambda:1/0)

    def test_09_invalid_enable_rejected(self):
        with self.assertRaises(ValueError):b.PhaseRecorder(1)

    def test_10_function_count_respects_filename_and_qualname(self):
        r=profile_fixture(4,True)["reports"]["candidate_query"]
        self.assertEqual(b.function_calls(r,"memory_bank.py","ChunkedMemoryBank.read"),48)
        self.assertEqual(b.function_calls(r,"other.py","ChunkedMemoryBank.read"),0)
        self.assertEqual(b.function_calls(r,"memory_bank.py","read"),0)

    def test_11_report_rejects_missing_profile(self):
        r=profile_fixture(1,True)["reports"]["candidate_query"];r["functions"]=[]
        self.assertFalse(b.report_valid(r,True))

    def test_12_report_rejects_negative_time(self):
        r=profile_fixture(1,True)["reports"]["candidate_query"];r["functions"][0]["self_ns"]=-1
        self.assertFalse(b.report_valid(r,True))

    def test_13_report_rejects_wrong_phase_count(self):
        r=profile_fixture(1,False)["reports"]["candidate_query"];r["invocations"]=11
        self.assertFalse(b.report_valid(r,False))

    def test_14_cell_gate(self):
        row,_,_=fixture_cell()
        self.assertTrue(b.row_gate(row))

    def test_15_parent_export_mismatch_fails(self):
        row,_,_=fixture_cell();row["parent_export_parity"]=False
        self.assertFalse(b.row_gate(row))

    def test_16_quality_mismatch_fails(self):
        row,_,_=fixture_cell();row["all_quality_parity"]=False
        self.assertFalse(b.row_gate(row))

    def test_17_call_count_mismatch_fails(self):
        off,on=profile_fixture(1,False),profile_fixture(1,True)
        on["reports"]["candidate_query"]["functions"][0]["calls"]=11
        anchor=dict(retained_inventory=off["retained_inventory"],stream_ratio_h1h2_over_cached=2.)
        with patch.object(b,"trajectory",side_effect=[off,on]):
            row,_,_=REAL_PROFILE_CELL(None,2,1,anchor)
        self.assertFalse(row["call_counts_pass"])
        self.assertFalse(b.row_gate(row))

    def test_18_complete_grid_passes(self):
        rows=[fixture_cell(n,q)[0] for n in b.DIMENSIONS for q in b.BURSTS]
        self.assertTrue(b.gate(b.summarize(rows)))

    def test_19_incomplete_grid_fails(self):
        rows=[fixture_cell(n,q)[0] for n in b.DIMENSIONS for q in b.BURSTS]
        self.assertFalse(b.gate(b.summarize(rows[:-1])))

    def test_20_unfavorable_parent_ratios_do_not_fail_audit(self):
        rows=[fixture_cell(n,q)[0] for n in b.DIMENSIONS for q in b.BURSTS]
        for row in rows:row["parent_stream_ratio"]=1000
        self.assertTrue(b.gate(b.summarize(rows)))

    def test_21_parent_adapter_validates_cell_order(self):
        rows=[dict(numeric_dimension=n,queries_per_update=q) for n in b.DIMENSIONS for q in b.BURSTS]
        self.assertEqual(len(b.parent_adapter(rows,SimpleNamespace(row_gate=lambda r:True))),12)
        with self.assertRaises(ValueError):b.parent_adapter(rows[::-1],SimpleNamespace(row_gate=lambda r:True))

    def test_22_parent_adapter_rejects_bad_gate(self):
        rows=[dict(numeric_dimension=n,queries_per_update=q) for n in b.DIMENSIONS for q in b.BURSTS]
        with self.assertRaises(ValueError):b.parent_adapter(rows,SimpleNamespace(row_gate=lambda r:False))

    def test_23_profiler_does_not_mutate_input(self):
        x=torch.eye(16,dtype=torch.float64);v=x._version;before=x.clone()
        b.PhaseRecorder(True).call(lambda:torch.linalg.cholesky(x))
        self.assertEqual(x._version,v);self.assertTrue(torch.equal(x,before))

    def test_24_reports_serialize_as_json(self):
        p=b.PhaseRecorder(True);p.call(lambda:sum(range(3)))
        data=json.loads(b.blob(p.report()))
        self.assertIn("functions",data)

    def test_25_profiles_keep_only_top_ten_in_summary(self):
        row,full,_=fixture_cell()
        self.assertEqual(set(row["function_tops"]),set(b.PHASES))
        self.assertEqual(set(full),set(b.PHASES))
        self.assertTrue(all(len(x)<=10 for x in row["function_tops"].values()))

    def test_26_runner_and_embedded_python(self):
        import re
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c229.ps1").read_text()
        launch=(root/"tools/invoke_c229.ps1").read_text()
        self.assertIn("expected_focused_tests = 2625",run)
        self.assertIn("c228-v5f-update-query-76eea62720cf4857a7122cd48c400f1a",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertLess(run.index("authoring_selftest = PASS"),run.index("& $Python -u -c $Regression"))
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S)
        self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded-python","exec")

    def test_27_free_module_aliases_and_no_optimization(self):
        source=inspect.getsource(b);tree=ast.parse(source)
        aliases={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name)
                 and n.value.id.startswith("c") and n.value.id[1:].isdigit()}
        self.assertFalse(aliases)
        self.assertNotIn("torch.optim",source);self.assertNotIn("check=False",source)
        self.assertIn("bank.numeric.full_reference(current)",inspect.getsource(b.trajectory))
        self.assertNotIn("patch.object",inspect.getsource(b.trajectory))

    def test_28_cell_executes_control_before_profile(self):
        off,on=profile_fixture(1,False),profile_fixture(1,True)
        anchor=dict(retained_inventory=off["retained_inventory"],stream_ratio_h1h2_over_cached=3.)
        with patch.object(b,"trajectory",side_effect=[off,on]) as spy:
            REAL_PROFILE_CELL(None,2,1,anchor)
        self.assertEqual([x.args[-1] for x in spy.call_args_list],[False,True])

    def test_29_stateful_callback_is_not_replaced_by_result(self):
        p=b.PhaseRecorder(True);state=[]
        for i in range(12):p.call(lambda:state.append(i))
        self.assertEqual(state,list(range(12)))
        self.assertEqual(p.report()["invocations"],12)

    def test_30_synthetic_run_calls_adapter_and_postchecks(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);parent_path=root/"summary.json";parent_path.write_text("{}")
            anchors=[dict(numeric_dimension=n,queries_per_update=q) for n in b.DIMENSIONS for q in b.BURSTS]
            (root/"measurements.json").write_bytes(b.blob(anchors))
            protected={}
            for i in range(292):
                p=root/f"input{i}";p.write_bytes(b"x");protected[str(p)]=hashlib.sha256(b"x").hexdigest()
            pins={f"source{i}":"x" for i in range(214)}
            audit=SimpleNamespace(sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                read_json=lambda p:json.loads(Path(p).read_text()),
                git=lambda r,*args:b"HEAD" if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b"")
            helpers=SimpleNamespace(base_module=lambda:SimpleNamespace(audit=audit))
            sym=SimpleNamespace(parent_module=lambda:helpers);dim=SimpleNamespace(parent_module=lambda:sym)
            factor=SimpleNamespace(parent_module=lambda:dim)
            parent=SimpleNamespace(parent_module=lambda:factor,row_gate=lambda r:True)
            seen=[]
            def pre(*a):seen.append("precheck");return {},pins,protected
            def cell(p,n,q,a):seen.append((n,q));return fixture_cell(n,q)
            with patch.object(b,"parent_module",return_value=parent),patch.object(b,"precheck",side_effect=pre),patch.object(b,"profile_cell",side_effect=cell),patch("sys.stdout",new=io.StringIO()):
                result=b.run(c228_summary=parent_path,output_dir=root/"out",expected_head="HEAD")
            self.assertEqual(result["status"],"PASS")
            self.assertEqual(seen,["precheck"]+[(n,q) for n in b.DIMENSIONS for q in b.BURSTS]+["precheck"])
            self.assertEqual(len(result["artifacts"]),5)

    def test_31_actual_parent_trajectory_and_profile_counts(self):
        parent=b.parent_module();factor=parent.parent_module()
        prefix_anchor=factor.measure_dimension(factor.parent_module(),2)[0]
        anchor=parent.measure_cell(factor,2,1,prefix_anchor)[0]
        row,_,_=b.profile_cell(parent,2,1,anchor)
        self.assertTrue(b.row_gate(row))

    def test_32_actual_historical_suite_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(114,2626))
        self.assertEqual(b.regression_suite(root).countTestCases(),2625)


if __name__=="__main__":
    unittest.main(verbosity=2)
