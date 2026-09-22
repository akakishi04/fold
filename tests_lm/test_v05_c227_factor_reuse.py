import ast
import copy
import hashlib
import inspect
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import torch
from fold_lm.v05_benchmarks import gate_f_c227_factor_reuse as b


def bridge_fixture(n=2):
    J=torch.eye(n,dtype=torch.float64)*4
    for i in range(1,n-1):
        J[i,i+1]=J[i+1,i]=-0.25
    if n>2:
        J[0,2]=J[2,0]=-0.25
    U=torch.zeros((n,2),dtype=torch.float64); U[0,0]=U[1,1]=1
    W=torch.eye(2,dtype=torch.float64)*0.25
    bias=torch.tensor([0.,-0.75],dtype=torch.float64)
    bridge=SimpleNamespace(_J=J,_eta=torch.zeros(n,dtype=torch.float64),_U=U,
        _Q=U.mT.contiguous(),_registry={"r":SimpleNamespace(W=W,b=bias)})
    bridge._aggregate=lambda state:(SimpleNamespace(value="SUPPORTED"),W,bias,())
    state=SimpleNamespace(memory_revision=32,evidence_revision=32,evidence_time=32)
    return bridge,state


def fake_files(n):
    common={"evidence.ndjson":b"raw","source-index.json":b"index"}
    candidate=dict(common,**{"state-and-bank.json":b"candidate"})
    symbolic=dict(common,**{"state-and-bridge.json":b"symbolic"})
    cached=dict(symbolic,**{"factorization-cache.json":b"cache"})
    return dict(candidate=candidate,symbolic=symbolic,cached=cached)


def fake_row(n):
    files=fake_files(n)
    row=dict(numeric_dimension=n,history_events=32,raw_sha256=b.RAW_SHA,live_factors=2,
        symbolic_state_equal=True,provenance_resolves=True,query_state_unchanged=True,
        quality_pass=True,parent_exports_equal=True,cache_factor_shape=[n,n],cache_rhs_shape=[n],
        additional_cache_tensor_bytes=8*(n*n+n),cache_prepare_trace=b.expected_trace(n,"prepare"),
        query_traces={a:b.expected_trace(n,a) for a in b.ARMS})
    for arm in b.ARMS:
        row[arm+"_files"]={k:dict(bytes=len(v),sha256=hashlib.sha256(v).hexdigest()) for k,v in files[arm].items()}
        row[arm+"_total_export_bytes"]=sum(map(len,files[arm].values()))
        row[arm+"_query_median_ns"]=100
        row[arm+"_query_trials"]=[dict(elapsed_ns=100,raw_bytes=0,events=0) for _ in range(3)]
    return row


class C227Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_parent_identity(self):
        self.assertEqual(b.PARENT_EXECUTION,"17284250b25bdb5160d5d3ffa95501a4f5070e03")
        self.assertEqual(b.PARENT_SHA,"ba4465c8c84e8fd54da1f7096a18056b7e53e6689a6ba3df5e1f9c559a7fac08")

    def test_03_no_automatic_superiority(self):
        m=b.manifest()
        self.assertFalse(m["superiority_required_for_pass"])
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_f_candidate"])

    def test_04_fixed_arms_and_dimensions(self):
        self.assertEqual(b.ARMS,("candidate","symbolic","cached"))
        self.assertEqual(b.DIMENSIONS,(2,16,64,256))
        self.assertEqual(b.HISTORY_EVENTS,32)

    def test_05_precision_and_workload(self):
        m=b.manifest()
        self.assertEqual((m["warmups"],m["repeats"],m["numeric_tolerance"]),(1,3,1e-10))
        self.assertEqual((m["new_training_steps"],m["learned_model_forward_calls"]),(0,0))

    def test_06_actual_torch_cache_matches_full_solve(self):
        for n in b.DIMENSIONS:
            bridge,state=bridge_fixture(n)
            cache=b.prepare_cache(bridge,state)
            _,W,bias,_=bridge._aggregate(state)
            expected=bridge._Q@torch.linalg.solve(bridge._J+bridge._U@W@bridge._U.mT,
                                                bridge._eta+bridge._U@bias)
            error=float(torch.max(torch.abs(b.query_cached(cache,bridge,state)-expected)))
            self.assertLessEqual(error,b.TOLERANCE)

    def test_07_cache_holds_full_factor_and_rhs(self):
        for n in b.DIMENSIONS:
            bridge,state=bridge_fixture(n);cache=b.prepare_cache(bridge,state)
            self.assertEqual((tuple(cache.L.shape),tuple(cache.rhs.shape)),((n,n),(n,)))
            self.assertEqual(cache.L.untyped_storage().nbytes()+cache.rhs.untyped_storage().nbytes(),8*(n*n+n))

    def test_08_prepare_is_checked_cholesky(self):
        bridge,state=bridge_fixture(16)
        _,trace=b.trace_call(lambda:b.prepare_cache(bridge,state))
        self.assertEqual(trace,b.expected_trace(16,"prepare"))

    def test_09_query_uses_factor_without_refactor(self):
        bridge,state=bridge_fixture(16);cache=b.prepare_cache(bridge,state)
        _,trace=b.trace_call(lambda:b.query_cached(cache,bridge,state))
        self.assertEqual(trace,b.expected_trace(16,"cached"))

    def test_10_unknown_relation_rejected(self):
        bridge,state=bridge_fixture();bridge._aggregate=lambda s:(SimpleNamespace(value="OUT_OF_SCOPE"),None,None,())
        with self.assertRaises(ValueError):b.prepare_cache(bridge,state)

    def test_11_nonfinite_rejected(self):
        bridge,state=bridge_fixture();bridge._eta[0]=float("nan")
        with self.assertRaises(ValueError):b.prepare_cache(bridge,state)

    def test_12_non_spd_rejected_no_jitter(self):
        bridge,state=bridge_fixture();bridge._J[0,0]=-4
        with self.assertRaises(RuntimeError):b.prepare_cache(bridge,state)

    def test_13_other_state_object_rejected(self):
        bridge,state=bridge_fixture();cache=b.prepare_cache(bridge,state)
        with self.assertRaises(ValueError):b.query_cached(cache,bridge,copy.copy(state))

    def test_14_other_bridge_object_rejected(self):
        bridge,state=bridge_fixture();cache=b.prepare_cache(bridge,state)
        with self.assertRaises(ValueError):b.query_cached(cache,copy.copy(bridge),state)

    def test_15_mutated_rhs_rejected(self):
        bridge,state=bridge_fixture();cache=b.prepare_cache(bridge,state);cache.rhs.add_(1)
        with self.assertRaises(ValueError):b.query_cached(cache,bridge,state)

    def test_16_mutated_registry_rejected(self):
        bridge,state=bridge_fixture();cache=b.prepare_cache(bridge,state);bridge._registry["r"].W.add_(1)
        with self.assertRaises(ValueError):b.query_cached(cache,bridge,state)

    def test_17_trace_restores_functions(self):
        original=(torch.linalg.cholesky,torch.cholesky_solve)
        bridge,state=bridge_fixture();b.trace_call(lambda:b.prepare_cache(bridge,state))
        self.assertEqual(original,(torch.linalg.cholesky,torch.cholesky_solve))

    def test_18_trace_restores_on_exception(self):
        original=(torch.linalg.cholesky,torch.cholesky_solve)
        def fail():raise RuntimeError("fixture")
        with self.assertRaises(RuntimeError):b.trace_call(fail)
        self.assertEqual(original,(torch.linalg.cholesky,torch.cholesky_solve))

    def test_19_measured_order_covers_each_start(self):
        orders=[b.query_order(i) for i in range(1,4)]
        self.assertEqual({x[0] for x in orders},set(b.ARMS))
        self.assertTrue(all(set(x)==set(b.ARMS) for x in orders))

    def test_20_parent_adapter_rejects_order_and_missing_rows(self):
        parent=SimpleNamespace(row_gate=lambda r,p:True,parent_module=lambda:None)
        rows=[fake_row(n) for n in b.DIMENSIONS]
        self.assertEqual(tuple(b.parent_adapter(rows,parent)),b.DIMENSIONS)
        with self.assertRaises(ValueError):b.parent_adapter(rows[::-1],parent)
        with self.assertRaises(ValueError):b.parent_adapter(rows[:-1],parent)

    def test_21_original_inventories_compare_both_arms(self):
        row=fake_row(2);other=copy.deepcopy(row)
        self.assertTrue(b.original_exports_equal(row,other))
        other["symbolic_files"]["state-and-bridge.json"]["bytes"]+=1
        self.assertFalse(b.original_exports_equal(row,other))

    def test_22_gate_requires_complete_cache_bytes(self):
        row=fake_row(16);self.assertTrue(b.row_gate(row))
        row["additional_cache_tensor_bytes"]-=8
        self.assertFalse(b.row_gate(row))

    def test_23_unfavorable_time_does_not_fail_audit(self):
        rows=[fake_row(n) for n in b.DIMENSIONS]
        for row in rows:row["candidate_query_median_ns"]=100000
        self.assertTrue(b.gate(b.summarize(rows)))

    def test_24_quality_failure_rejects_audit(self):
        row=fake_row(2);row["quality_pass"]=False
        self.assertFalse(b.row_gate(row))

    def test_25_query_refactorization_rejects_gate(self):
        row=fake_row(2);row["query_traces"]["cached"]=b.expected_trace(2,"symbolic")
        self.assertFalse(b.row_gate(row))

    def test_26_archive_exact_members(self):
        rows=[fake_row(n) for n in b.DIMENSIONS]
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"exports.zip"
            with zipfile.ZipFile(path,"w") as z:
                for n in b.DIMENSIONS:
                    for arm,files in fake_files(n).items():
                        for name,data in files.items():z.writestr(f"{n}/{arm}/{name}",data)
            b.verify_archive(path,rows)
            with zipfile.ZipFile(path,"a") as z:z.writestr("extra",b"bad")
            with self.assertRaises(ValueError):b.verify_archive(path,rows)

    def test_27_archive_corrupt_bytes_rejected(self):
        rows=[fake_row(n) for n in b.DIMENSIONS]
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"exports.zip"
            with zipfile.ZipFile(path,"w") as z:
                for n in b.DIMENSIONS:
                    for arm,files in fake_files(n).items():
                        for name,data in files.items():z.writestr(f"{n}/{arm}/{name}",b"bad")
            with self.assertRaises(ValueError):b.verify_archive(path,rows)

    def test_28_runner_launcher_and_python_blocks(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c227.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c227.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2561",run)
        self.assertIn("tests_lm.test_v05_c227_factor_reuse",run)
        self.assertIn("c226-v5f-dimension-scaling-b1186f4e625e45e0909c44ed8c585937",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertLess(run.index("authoring_selftest = PASS"),run.index("& $Python -u -c $Regression"))
        import re
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S)
        self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"runner-embedded","exec")

    def test_29_source_safety_and_binding(self):
        source=inspect.getsource(b)
        self.assertNotIn("check=False",source)
        self.assertNotIn("torch.optim",source)
        tree=ast.parse(source)
        refs={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute)
            and isinstance(n.value,ast.Name) and n.value.id.startswith("c") and n.value.id[1:].isdigit()}
        self.assertEqual(refs,set())

    def test_30_synthetic_run_exercises_adapter_export_and_postcheck(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);parent_file=root/"summary.json";parent_file.write_text("{}")
            anchors=[fake_row(n) for n in b.DIMENSIONS]
            (root/"measurements.json").write_bytes(b.blob(anchors))
            protection={}
            for i in range(268):
                path=root/f"input{i}";path.write_bytes(b"x")
                protection[str(path)]=hashlib.sha256(b"x").hexdigest()
            pins={f"source{i}":"x" for i in range(202)}
            calls=[]
            def git(root,*args):
                return b"HEAD" if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b""
            audit=SimpleNamespace(git=git,sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                                  read_json=lambda p:json.loads(Path(p).read_text()))
            helpers=SimpleNamespace(base_module=lambda:SimpleNamespace(audit=audit))
            symbolic=SimpleNamespace(parent_module=lambda:helpers)
            parent=SimpleNamespace(parent_module=lambda:symbolic,row_gate=lambda r,p:True)
            def precheck(*args):calls.append("precheck");return {},pins,protection
            def measure(p,n):calls.append(n);return fake_row(n),[],fake_files(n)
            with patch.object(b,"parent_module",return_value=parent),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"measure_dimension",side_effect=measure),patch("sys.stdout",new=io.StringIO()):
                result=b.run(c226_summary=parent_file,output_dir=root/"out",expected_head="HEAD")
            self.assertEqual(result["status"],"PASS")
            self.assertEqual(calls,["precheck",2,16,64,256,"precheck"])
            self.assertEqual(len(result["artifacts"]),5)

    def test_31_actual_parent_backend_and_export_anchor(self):
        parent=b.parent_module()
        row,checks,files=b.measure_dimension(parent,2)
        anchor=parent.measure_dimension(parent.parent_module(),2)[0]
        row["parent_exports_equal"]=b.original_exports_equal(row,anchor)
        self.assertTrue(b.row_gate(row))
        self.assertEqual(len(checks),4)
        self.assertEqual(set(files),set(b.ARMS))

    def test_32_actual_historical_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(112,2562))
        self.assertEqual(b.regression_suite(root).countTestCases(),2561)


if __name__ == "__main__":
    unittest.main(verbosity=2)
