import ast
import copy
from dataclasses import dataclass
import hashlib
import inspect
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

import torch
from fold_lm.v05_benchmarks import gate_f_c228_update_query_cost as b

REAL_MEASURE_CELL = b.measure_cell


@dataclass
class FixtureCore:
    state: object
    bridge: object
    L: torch.Tensor
    rhs: torch.Tensor
    stamps: tuple


def numerical_fixture(n=2):
    """Synthetic parent interface, using real torch numerical operations, not accepted artifacts."""
    J=torch.eye(n,dtype=torch.float64)*4
    for i in range(n-1):J[i,i+1]=J[i+1,i]=-0.2
    U=torch.zeros((n,2),dtype=torch.float64);U[0,0]=U[1,1]=1
    W=torch.eye(2,dtype=torch.float64)*0.25
    bridge=SimpleNamespace(_J=J,_eta=torch.zeros(n,dtype=torch.float64),_U=U,_Q=U.mT.contiguous())
    bridge._aggregate=lambda state:(SimpleNamespace(value=state.status),state.W,state.bias,())
    stamps=lambda tensors:tuple((id(t),t._version) for t in tensors)
    tensors=lambda bridge:(bridge._J,bridge._eta,bridge._U,bridge._Q)
    def prepare(bridge,state):
        if state.status!="SUPPORTED":raise ValueError("capability")
        matrix=bridge._J+bridge._U@state.W@bridge._U.mT
        rhs=(bridge._eta+bridge._U@state.bias).clone()
        if not bool(torch.isfinite(rhs).all()):raise ValueError("nonfinite")
        L=torch.linalg.cholesky(matrix)
        return FixtureCore(state,bridge,L,rhs,stamps(tensors(bridge)+(L,rhs)))
    def query(core,bridge,state):
        if core.state is not state or core.bridge is not bridge:raise ValueError("binding")
        if stamps(tensors(bridge)+(core.L,core.rhs))!=core.stamps:raise ValueError("mutation")
        return (bridge._Q@torch.cholesky_solve(core.rhs[:,None],core.L)).squeeze(-1)
    parent=SimpleNamespace(FactorCache=FixtureCore,prepare_cache=prepare,query_cached=query,
        tensor_stamps=stamps,bridge_tensors=tensors,
        cache_payload=lambda c,h:b.blob(dict(L=h.canonical(c.L),rhs=h.canonical(c.rhs))))
    def state(value=0.75):
        return SimpleNamespace(status="SUPPORTED",W=W.clone(),bias=torch.tensor([0.,value],dtype=torch.float64))
    return parent,bridge,state


def ledger(n):
    lines=[]
    for i in range(n):
        factor="alpha" if i==0 else "beta";semantic=1 if i==0 else (i-1)%3
        lines.append(b.blob(dict(schema="fold-cost-event-v1",kind="ASSERT" if i<2 else "REPLACE",
            factor=factor,scope="global" if factor=="alpha" else "project",
            relation=f"{factor}-class-{semantic}",source_id=f"cost:{i+1:08d}",time=i+1,
            text=f"{factor} の観測値を {semantic-1} と記録する。")))
    return b"".join(lines)


def fake_files():
    common={"evidence.ndjson":b"raw","source-index.json":b"index"}
    return dict(candidate=dict(common,**{"state-and-bank.json":b"candidate"}),
        cached=dict(common,**{"state-and-bridge.json":b"symbolic","rhs-reuse-cache.json":b"cache"}))


def inventory(files):
    return {k:dict(bytes=len(v),sha256=hashlib.sha256(v).hexdigest()) for k,v in files.items()}


def trace(n,arm):
    names,width={"candidate":(("cholesky","cholesky_ex","solve"),2),
                 "cached":(("cholesky_solve",),n),"prepare":(("cholesky",),n)}[arm]
    return [dict(operation=x,matrix_shape=[width,width]) for x in names]


def fake_result(n,q):
    files=fake_files()
    phases=dict(common_numeric_setup_ns=10,index_build_ns=10,candidate_init_ns=20,cached_init_ns=20,
                cache_prepare_ns=10,export_ns=10)
    for a in files:
        phases.update({a+"_update_ns":50,a+"_query_ns":100,a+"_stream_ns":150,a+"_cold_inclusive_ns":190})
    return dict(phases=phases,counts=dict(updates_per_arm=12,queries_per_arm=12*q,
        quality_results_checked=24*q,rhs_refreshes=12,initial_factorizations=1,update_refactorizations=0),
        quality=True,checks=[dict(passed=True)],query_state_unchanged=True,
        initial_inventory=dict(candidate=inventory(files["candidate"]),
            symbolic=inventory({k:v for k,v in files["cached"].items() if k!="rhs-reuse-cache.json"})),
        refresh_trace=[],prepare_trace=trace(n,"prepare"),
        candidate_query_trace=trace(n,"candidate"),cached_query_trace=trace(n,"cached"),
        files=files,inventory={a:inventory(f) for a,f in files.items()},resident={},
        extra_cache_tensor_bytes=8*(n*n+n+4))


def fixture_measure(n=2,q=1):
    result=fake_result(n,q)
    parent=SimpleNamespace(expected_trace=trace)
    anchor={a+"_files":v for a,v in result["initial_inventory"].items()}
    with patch.object(b,"trajectory",return_value=result):
        return REAL_MEASURE_CELL(parent,n,q,anchor)


class C228Tests(unittest.TestCase):
    def test_01_manifest(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_complete_ledger_and_parent_prefix(self):
        prefix,tail,whole=b.ledger_parts(SimpleNamespace(ledger=ledger))
        self.assertEqual(len(tail),12)
        self.assertEqual(prefix+b"".join(tail),whole)
        self.assertEqual(len(whole.splitlines()),44)

    def test_03_scope(self):
        m=b.manifest()
        self.assertEqual((m["new_training_steps"],m["learned_model_forward_calls"]),(0,0))
        self.assertFalse(m["superiority_required_for_pass"])
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_f_candidate"])

    def test_04_actual_torch_rhs_refresh_matches_solve(self):
        for n in b.DIMENSIONS:
            p,bridge,state=numerical_fixture(n);cache=b.prepare(p,bridge,state())
            for value in (-0.75,0.0,0.75):
                new=state(value);cache=b.refresh(p,cache,bridge,new)
                want=bridge._Q@torch.linalg.solve(bridge._J+bridge._U@new.W@bridge._U.mT,
                                               bridge._eta+bridge._U@new.bias)
                got=p.query_cached(cache.core,bridge,new)
                self.assertLessEqual(float(torch.max(torch.abs(want-got))),b.TOLERANCE)

    def test_05_factor_is_reused_exact_object(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state());L=cache.core.L
        new=b.refresh(p,cache,bridge,state(-0.75))
        self.assertIs(new.core.L,L)
        self.assertIs(new.aggregate_W,cache.aggregate_W)

    def test_06_new_core_rejects_old_state_binding(self):
        p,bridge,state=numerical_fixture();old=state();cache=b.prepare(p,bridge,old)
        new=b.refresh(p,cache,bridge,state(-0.75))
        with self.assertRaises(ValueError):p.query_cached(new.core,bridge,old)

    def test_07_changed_matrix_is_rejected(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state());changed=state()
        changed.W[0,0]+=1
        with self.assertRaises(ValueError):b.refresh(p,cache,bridge,changed)

    def test_08_base_tensor_mutation_rejected(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state());bridge._J.add_(1)
        with self.assertRaises(ValueError):b.refresh(p,cache,bridge,state())

    def test_09_matrix_guard_mutation_rejected(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state());cache.aggregate_W.add_(1)
        with self.assertRaises(ValueError):b.refresh(p,cache,bridge,state())

    def test_10_other_bridge_rejected(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state())
        with self.assertRaises(ValueError):b.refresh(p,cache,copy.copy(bridge),state())

    def test_11_unsupported_update_rejected(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state());new=state();new.status="OUT_OF_SCOPE"
        with self.assertRaises(ValueError):b.refresh(p,cache,bridge,new)

    def test_12_nonfinite_rhs_rejected(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state());new=state(float("nan"))
        with self.assertRaises(ValueError):b.refresh(p,cache,bridge,new)

    def test_13_cache_export_includes_matrix_guard(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state())
        data=json.loads(b.cache_export(p,cache,SimpleNamespace(canonical=lambda t:t.tolist())))
        self.assertEqual(data["aggregate_W"],cache.aggregate_W.tolist())
        self.assertIn("L",data["core"]);self.assertIn("rhs",data["core"])

    def test_14_append_offsets(self):
        index={};raw,event=b.append_evidence(b"before",index,b'{"source_id":"new"}\n')
        self.assertEqual(index["new"],(6,len(raw)))
        self.assertEqual(json.loads(raw[slice(*index["new"])]),event)

    def test_15_duplicate_append_rejected(self):
        with self.assertRaises(ValueError):b.append_evidence(b"",{"x":(0,1)},b'{"source_id":"x"}\n')

    def test_16_refresh_has_no_refactorization(self):
        p,bridge,state=numerical_fixture();cache=b.prepare(p,bridge,state())
        with patch.object(torch.linalg,"cholesky",side_effect=AssertionError("refactor")),patch.object(torch.linalg,"solve",side_effect=AssertionError("solve")):
            b.refresh(p,cache,bridge,state(-0.75))

    def test_17_cached_query_remains_actual_factor_solve(self):
        p,bridge,state=numerical_fixture();current=state();cache=b.prepare(p,bridge,current)
        original=torch.cholesky_solve
        with patch.object(torch,"cholesky_solve",wraps=original) as spy:
            p.query_cached(cache.core,bridge,current)
            self.assertEqual(spy.call_count,1)

    def test_18_row_gate(self):
        row,_,_=fixture_measure()
        self.assertTrue(b.row_gate(row))

    def test_19_unaccounted_cache_tensor_fails(self):
        row,_,_=fixture_measure();row["extra_cache_tensor_bytes"]-=32
        self.assertFalse(b.row_gate(row))

    def test_20_quality_failure_fails(self):
        row,_,_=fixture_measure();row["quality_pass"]=False
        self.assertFalse(b.row_gate(row))

    def test_21_unfavorable_time_is_not_audit_failure(self):
        rows=[]
        for n in b.DIMENSIONS:
            for q in b.BURSTS:
                row,_,_=fixture_measure(n,q);row["stream_ratio_h1h2_over_cached"]=100
                rows.append(row)
        self.assertTrue(b.gate(b.summarize(rows)))

    def test_22_refactor_count_invalidates_row_gate(self):
        row,_,_=fixture_measure();row["trials"][0]["update_refactorizations"]=1
        self.assertFalse(b.row_gate(row))

    def test_23_initial_anchor_compares_both_arms(self):
        r=fake_result(2,1);anchor={a+"_files":copy.deepcopy(v) for a,v in r["initial_inventory"].items()}
        self.assertTrue(b.anchor_equal(r["initial_inventory"],anchor))
        anchor["symbolic_files"]["state-and-bridge.json"]["bytes"]+=1
        self.assertFalse(b.anchor_equal(r["initial_inventory"],anchor))

    def test_24_parent_adapter_checks_order_and_gate(self):
        rows=[dict(numeric_dimension=n) for n in b.DIMENSIONS]
        self.assertEqual(tuple(b.parent_adapter(rows,SimpleNamespace(row_gate=lambda r:True))),b.DIMENSIONS)
        with self.assertRaises(ValueError):b.parent_adapter(rows[::-1],SimpleNamespace(row_gate=lambda r:True))
        with self.assertRaises(ValueError):b.parent_adapter(rows,SimpleNamespace(row_gate=lambda r:False))

    def test_25_archive_members_and_bytes(self):
        row,_,files=fixture_measure()
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"a.zip"
            with zipfile.ZipFile(path,"w") as z:
                for arm,contents in files.items():
                    for name,data in contents.items():z.writestr(f"2/1/{arm}/{name}",data)
            b.verify_archive(path,[row])
            with zipfile.ZipFile(path,"a") as z:z.writestr("extra",b"x")
            with self.assertRaises(ValueError):b.verify_archive(path,[row])

    def test_26_archive_corruption(self):
        row,_,files=fixture_measure()
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"a.zip"
            with zipfile.ZipFile(path,"w") as z:
                for arm,contents in files.items():
                    for name,data in contents.items():z.writestr(f"2/1/{arm}/{name}",b"wrong")
            with self.assertRaises(ValueError):b.verify_archive(path,[row])

    def test_27_runner_launcher_and_embedded_python(self):
        import re
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c228.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c228.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2593",run)
        self.assertIn("c227-v5f-factor-reuse-8abdfa3dfbd141db94ce9afd0e4c171a",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertLess(run.index("authoring_selftest = PASS"),run.index("& $Python -u -c $Regression"))
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded-runner","exec")

    def test_28_source_bindings_and_query_validation(self):
        source=inspect.getsource(b);tree=ast.parse(source)
        aliases={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name)
            and n.value.id.startswith("c") and n.value.id[1:].isdigit()}
        self.assertEqual(aliases,set())
        self.assertNotIn("torch.optim",source)
        self.assertNotIn("check=False",source)
        self.assertIn("bank.numeric.full_reference(current)",inspect.getsource(b.trajectory))

    def test_29_measure_cell_warmup_and_contract(self):
        row,quality,files=fixture_measure(16,4)
        self.assertEqual(len(row["trials"]),3)
        self.assertEqual([q["warmup"] for q in quality],[True,False,False,False])
        self.assertEqual(set(files),{"candidate","cached"})
        self.assertTrue(row["repeat_exports_equal"])

    def test_30_synthetic_run_executes_loader_export_postcheck(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);pf=root/"summary.json";pf.write_text("{}")
            anchors=[dict(numeric_dimension=n) for n in b.DIMENSIONS]
            (root/"measurements.json").write_bytes(b.blob(anchors))
            protected={}
            for i in range(280):
                f=root/f"input{i}";f.write_bytes(b"x");protected[str(f)]=hashlib.sha256(b"x").hexdigest()
            pins={f"source{i}":"x" for i in range(208)}
            audit=SimpleNamespace(sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                read_json=lambda p:json.loads(Path(p).read_text()),
                git=lambda r,*args:b"HEAD" if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b"")
            helpers=SimpleNamespace(base_module=lambda:SimpleNamespace(audit=audit))
            sym=SimpleNamespace(parent_module=lambda:helpers)
            dim=SimpleNamespace(parent_module=lambda:sym)
            parent=SimpleNamespace(parent_module=lambda:dim,row_gate=lambda r:True)
            seen=[]
            def pre(*a):seen.append("precheck");return {},pins,protected
            def measure(p,n,q,a):seen.append((n,q));return fixture_measure(n,q)
            with patch.object(b,"parent_module",return_value=parent),patch.object(b,"precheck",side_effect=pre),patch.object(b,"measure_cell",side_effect=measure),patch("sys.stdout",new=io.StringIO()):
                result=b.run(c227_summary=pf,output_dir=root/"out",expected_head="HEAD")
            self.assertEqual(result["status"],"PASS")
            self.assertEqual(seen,["precheck"]+[(n,q) for n in b.DIMENSIONS for q in b.BURSTS]+["precheck"])
            self.assertEqual(len(result["artifacts"]),5)

    def test_31_actual_parent_backend_trajectory(self):
        parent=b.parent_module()
        anchor=parent.measure_dimension(parent.parent_module(),2)[0]
        row,quality,_=b.measure_cell(parent,2,1,anchor)
        self.assertTrue(b.row_gate(row))
        self.assertEqual(len(quality[0]["checks"]),12)

    def test_32_actual_historical_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(113,2594))
        self.assertEqual(b.regression_suite(root).countTestCases(),2593)


if __name__=="__main__":
    unittest.main(verbosity=2)
