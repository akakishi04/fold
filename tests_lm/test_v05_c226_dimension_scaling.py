from copy import deepcopy
import hashlib
import inspect
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
import zipfile

import torch
from fold_lm.v05_benchmarks import gate_f_c226_dimension_scaling as b


def parent_fixture():
    return SimpleNamespace(SIZES=(8,32,128,512), row_gate=lambda r: r.get("parent_valid") is True)


def row_fixture(n):
    files={"evidence.ndjson":dict(bytes=1,sha256=hashlib.sha256(b"x").hexdigest())}
    traces=b.expected_traces(n)
    return dict(numeric_dimension=n,actual_variable_dim=n,history_events=32,raw_sha256=b.RAW_SHA,
        update_rank=2,readout_dim=2,matrix_tensor_sha256=b.tensor_identity(b.dimension_tensors(n)),
        candidate_linalg_trace=traces["candidate"],symbolic_linalg_trace=traces["symbolic"],
        instrumented_supported=True,instrumented_max_abs_error=0.0,parent_valid=True,
        quality_pass=True,symbolic_state_equal=True,storage_delta_bytes=419,
        candidate_query_median_ns=200,symbolic_query_median_ns=100,
        candidate_query_trials=[dict(raw_bytes=0)],symbolic_query_trials=[dict(raw_bytes=0)],
        candidate_files=files,symbolic_files=deepcopy(files))


class NumericFixture:
    def __init__(self,J,eta,Q,U,contributions):
        self._J,self._eta,self._Q,self._U=J,eta,Q,U
        self._registry={"fixture":object()}
        self.variable_dim=J.shape[0]
        self.update_rank=U.shape[1]
        self.readout_dim=Q.shape[0]


class BankFixture:
    def __init__(self,numeric):
        self.numeric=numeric


def backend_fixture():
    def factory():
        return BankFixture(NumericFixture(*b.dimension_tensors(2),()))
    return SimpleNamespace(c216=SimpleNamespace(build_bank=factory))


class C226Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_registered_dimensions_and_history(self):
        self.assertEqual(b.DIMENSIONS,(2,16,64,256))
        self.assertEqual(b.HISTORY_EVENTS,32)

    def test_03_n2_anchor_tensors(self):
        J,eta,Q,U=b.dimension_tensors(2)
        self.assertTrue(torch.equal(J,4*torch.eye(2,dtype=torch.float64)))
        self.assertTrue(torch.equal(Q,U))
        self.assertTrue(torch.equal(Q,torch.eye(2,dtype=torch.float64)))
        self.assertTrue(torch.equal(eta,torch.zeros(2,dtype=torch.float64)))

    def test_04_dimensions_rank_and_readout(self):
        for n in b.DIMENSIONS:
            J,eta,Q,U=b.dimension_tensors(n)
            self.assertEqual((J.shape,eta.shape,Q.shape,U.shape),((n,n),(n,),(2,n),(n,2)))
            self.assertTrue(all(x.dtype==torch.float64 for x in (J,eta,Q,U)))

    def test_05_symmetry_and_finite(self):
        for n in b.DIMENSIONS:
            J,*_=b.dimension_tensors(n)
            self.assertTrue(torch.equal(J,J.mT))
            self.assertTrue(bool(torch.isfinite(J).all()))

    def test_06_strict_diagonal_dominance_and_spd(self):
        for n in b.DIMENSIONS:
            J,*_=b.dimension_tensors(n)
            self.assertTrue(bool((J.diagonal() > J.abs().sum(1)-J.diagonal()).all()))
            self.assertEqual(torch.linalg.cholesky(J).shape,(n,n))

    def test_07_all_hidden_coordinates_are_connected(self):
        for n in b.DIMENSIONS[1:]:
            J,*_=b.dimension_tensors(n)
            seen,frontier={0},[0]
            while frontier:
                i=frontier.pop()
                for j in range(n):
                    if i!=j and J[i,j]!=0 and j not in seen:
                        seen.add(j);frontier.append(j)
            self.assertEqual(seen,set(range(n)))

    def test_08_hidden_system_changes_visible_response(self):
        J,eta,Q,U=b.dimension_tensors(16)
        value=Q@torch.linalg.solve(J+U@(torch.eye(2,dtype=torch.float64)*0.25)@U.mT,
                                   eta+U@torch.tensor([0.,-0.75],dtype=torch.float64))
        self.assertGreater(abs(float(value[0])),1e-6)
        self.assertGreater(abs(float(value[1])+0.75/4.25),1e-6)

    def test_09_update_columns_are_independent(self):
        for n in b.DIMENSIONS:
            U=b.dimension_tensors(n)[3]
            self.assertEqual(int(torch.linalg.matrix_rank(U)),2)

    def test_10_tensor_identity_deterministic(self):
        for n in b.DIMENSIONS:
            self.assertEqual(b.tensor_identity(b.dimension_tensors(n)),
                             b.manifest()["tensor_sha256"][str(n)])
        self.assertEqual(len(set(b.manifest()["tensor_sha256"].values())),4)

    def test_11_unregistered_dimensions_rejected(self):
        for bad in (0,1,3,True,16.0,"16"):
            with self.assertRaises(ValueError):
                b.dimension_tensors(bad)

    def test_12_dimension_factory_keeps_parent_factory_unchanged(self):
        backend=backend_fixture();factory=backend.c216.build_bank
        for n in b.DIMENSIONS:
            bank=b.dimension_bank(backend,n)
            self.assertEqual(bank.numeric.variable_dim,n)
        self.assertIs(backend.c216.build_bank,factory)

    def test_13_n2_factory_returns_original_template(self):
        template=backend_fixture().c216.build_bank()
        backend=SimpleNamespace(c216=SimpleNamespace(build_bank=lambda:template))
        self.assertIs(b.dimension_bank(backend,2),template)

    def test_14_capture_delegates_and_keeps_actual_built_state(self):
        expected=(object(),object(),{"events":32})
        helpers=SimpleNamespace(value=3,build_candidate=lambda backend,raw:expected)
        proxy=b.CaptureHelpers(helpers)
        self.assertEqual(proxy.value,3)
        self.assertIs(proxy.build_candidate(None,b"x"),expected)
        self.assertIs(proxy.captured,expected)

    def test_15_trace_records_actual_matrix_shapes(self):
        J=torch.eye(16,dtype=torch.float64)
        value,trace=b.trace_query(lambda:torch.linalg.solve(J,torch.ones(16,dtype=torch.float64)))
        self.assertEqual(trace,[dict(operation="solve",matrix_shape=[16,16])])
        self.assertTrue(torch.equal(value,torch.ones(16,dtype=torch.float64)))

    def test_16_trace_preserves_safety_operations(self):
        J=torch.eye(2,dtype=torch.float64)
        def fn():
            torch.linalg.cholesky(J)
            torch.linalg.cholesky_ex(J)
            return torch.linalg.solve(J,torch.ones(2,dtype=torch.float64))
        _,trace=b.trace_query(fn)
        self.assertEqual(trace,b.expected_traces(16)["candidate"])

    def test_17_trace_restores_functions_on_exception(self):
        originals=[getattr(torch.linalg,n) for n in ("solve","cholesky","cholesky_ex")]
        def fail():
            raise RuntimeError("test failure")
        with self.assertRaises(RuntimeError):
            b.trace_query(fail)
        self.assertEqual(originals,[getattr(torch.linalg,n) for n in ("solve","cholesky","cholesky_ex")])

    def test_18_parent_adapter_checks_complete_order(self):
        rows=[dict(history_events=n,parent_valid=True) for n in (8,32,128,512)]
        self.assertIs(b.parent_anchor(rows,parent_fixture()),rows[1])
        with self.assertRaises(ValueError):
            b.parent_anchor(rows[::-1],parent_fixture())

    def test_19_parent_adapter_rejects_invalid_or_incomplete(self):
        rows=[dict(history_events=n,parent_valid=True) for n in (8,32,128,512)]
        for bad in (rows[:2],{},[dict(x,parent_valid=False) for x in rows]):
            with self.assertRaises(ValueError):
                b.parent_anchor(bad,parent_fixture())

    def test_20_row_gate_requires_parent_quality(self):
        row=row_fixture(16)
        self.assertTrue(b.row_gate(row,parent_fixture()))
        row["parent_valid"]=False
        self.assertFalse(b.row_gate(row,parent_fixture()))

    def test_21_changed_matrix_or_dimension_rejected(self):
        for key,val in (("matrix_tensor_sha256","bad"),("numeric_dimension",3),("actual_variable_dim",2)):
            row=row_fixture(16);row[key]=val
            self.assertFalse(b.row_gate(row,parent_fixture()))

    def test_22_wrong_solve_dimension_rejected(self):
        row=row_fixture(64)
        row["symbolic_linalg_trace"][-1]["matrix_shape"]=[2,2]
        self.assertFalse(b.row_gate(row,parent_fixture()))

    def test_23_unfavorable_cost_does_not_fail_measurement(self):
        rows=[row_fixture(n) for n in b.DIMENSIONS]
        for row in rows:
            row["candidate_query_median_ns"]=10**9
        s=b.summarize(rows,parent_fixture());s["n2_parent_export_parity"]=True
        self.assertTrue(b.gate(s))
        self.assertFalse(b.gate(dict(s,n2_parent_export_parity=False)))
        self.assertFalse(b.gate(dict(s,dimensions=[2])))

    def test_24_anchor_byte_inventory_requires_both_arms(self):
        row=row_fixture(2);anchor=deepcopy(row)
        self.assertTrue(b.anchor_equal(row,anchor))
        anchor["symbolic_files"]["evidence.ndjson"]["bytes"]+=1
        self.assertFalse(b.anchor_equal(row,anchor))

    def test_25_archive_exact_member_bytes(self):
        row=row_fixture(16)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"x.zip"
            with zipfile.ZipFile(path,"w") as archive:
                for arm in ("candidate","symbolic"):
                    archive.writestr("16/"+arm+"/evidence.ndjson",b"x")
            b.verify_archive(path,[row])

    def test_26_archive_unexpected_member_rejected(self):
        row=row_fixture(16)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"x.zip"
            with zipfile.ZipFile(path,"w") as archive:
                for arm in ("candidate","symbolic"):
                    archive.writestr("16/"+arm+"/evidence.ndjson",b"x")
                archive.writestr("unexpected",b"x")
            with self.assertRaises(ValueError):
                b.verify_archive(path,[row])

    def test_27_archive_corrupt_bytes_rejected(self):
        row=row_fixture(16)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"x.zip"
            with zipfile.ZipFile(path,"w") as archive:
                for arm in ("candidate","symbolic"):
                    archive.writestr("16/"+arm+"/evidence.ndjson",b"bad")
            with self.assertRaises(ValueError):
                b.verify_archive(path,[row])

    def test_28_runner_and_launcher(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c226.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c226.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2529",run)
        self.assertIn("tests_lm.test_v05_c226_dimension_scaling",run)
        self.assertIn("c225-v5f-stateful-baseline-4df0cd59e7c34942a3d33b0932863b0f",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))

    def test_29_no_training_or_disabled_safety(self):
        m=b.manifest()
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_f_candidate"])
        self.assertEqual(m["new_training_steps"],0)
        self.assertTrue(m["check_true_preserved"])
        self.assertNotIn("check=False",inspect.getsource(b))

    def test_30_actual_capsule_kernel_matches_full_system(self):
        from fold_lm.capsule import compile_capsule
        for n in b.DIMENSIONS:
            J,eta,Q,U=b.dimension_tensors(n)
            capsule=compile_capsule(J,eta,Q,U,check=True)
            W=torch.eye(2,dtype=torch.float64)*0.25
            bias=torch.tensor([0.,-0.75],dtype=torch.float64)
            value,trace=b.trace_query(lambda:capsule.response(W,bias,check=True))
            expected=Q@torch.linalg.solve(J+U@W@U.mT,eta+U@bias)
            self.assertLessEqual(float(torch.max(torch.abs(value-expected))),b.TOLERANCE)
            self.assertEqual(trace,b.expected_traces(n)["candidate"])

    def test_31_actual_parent_measurement_and_n2_anchor(self):
        parent=b.parent_module()
        row,checks,cf,sf=b.measure_dimension(parent,2)
        self.assertTrue(b.row_gate(row,parent))
        original=parent.measure(parent.parent_module(),parent.parent_module().base_module(),32)
        self.assertEqual(cf,original[2]);self.assertEqual(sf,original[3])
        self.assertEqual(len(checks),4)

    def test_32_actual_historical_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(111,2530))
        self.assertEqual(b.regression_suite(root).countTestCases(),2529)


if __name__ == "__main__":
    unittest.main(verbosity=2)
