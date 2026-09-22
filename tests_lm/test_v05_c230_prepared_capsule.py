import ast
import copy
import hashlib
import inspect
import io
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile
import torch
from fold_lm.capsule import compile_capsule
from fold_lm.v05 import prepared_capsule as p
from fold_lm.v05_benchmarks import gate_f_c230_prepared_capsule as b


def fixture(n=16):
    J=torch.eye(n,dtype=torch.float64)*4
    for i in range(n-1):J[i,i+1]=J[i+1,i]=0.1
    U=torch.eye(n,dtype=torch.float64)[:,:2];Q=U.mT.contiguous()
    eta=torch.arange(n,dtype=torch.float64)/(n+1)
    capsule=compile_capsule(J,eta,Q,U)
    W=torch.tensor([[.25,.05],[.05,.4]],dtype=torch.float64)
    bias=torch.tensor([.2,-.3],dtype=torch.float64)
    return capsule,W,bias,(J,eta,Q,U)


def row_fixture(n=2,q=1):
    data=b'x';item=dict(bytes=1,sha256=hashlib.sha256(data).hexdigest())
    inv={a:{'state.json':item} for a in b.ARMS}
    phases={}
    for a in b.ARMS:
        phases.update({a+'_init_ns':10,a+'_update_ns':20,a+'_query_ns':30,a+'_stream_ns':50,a+'_cold_inclusive_ns':70})
    row=dict(numeric_dimension=n,queries_per_update=q,trials=[dict(phases) for _ in range(3)],
        quality_pass=True,parent_export_parity=True,repeat_exports_equal=True,
        reduced_factor_reused=True,full_factor_reused=True,extra_reduced_tensor_bytes=72,
        retained_inventory=inv,prepare_trace=b.expected_trace('prepare',n),
        query_traces={a:b.expected_trace(a,n) for a in b.ARMS},
        stream_ratio_prepared_over_candidate=1.0,stream_ratio_prepared_over_cached=2.0)
    for a in b.ARMS:row[a+'_export_bytes']=1
    return row,[dict(passed=True)],{a:{'state.json':data} for a in b.ARMS}


class C230Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_actual_reference_source_identity(self):
        import fold_lm.capsule as module
        data=Path(module.__file__).read_bytes().replace(b'\r\n',b'\n')
        self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),
                         '7f1090fe95b2e3eab3967d00c6730165e34fadfb')

    def test_03_response_matches_reference(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        torch.testing.assert_close(p.response(cache,c,W,bias,context=ctx),c.response(W,bias),rtol=0,atol=1e-10)

    def test_04_four_dimensions_match_full_solve(self):
        for n in b.DIMENSIONS:
            c,W,bias,ctx=fixture(n);J,eta,Q,U=ctx
            cache=p.prepare(c,W,context=ctx)
            result=p.response(cache,c,W,bias,context=ctx)
            torch.testing.assert_close(result,Q@torch.linalg.solve(J+U@W@U.mT,eta+U@bias),rtol=0,atol=1e-10)

    def test_05_bias_changes_reuse_factor_but_not_answer(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);factor=cache.LU;results=[]
        for k in range(12):
            value=bias+k*.01
            out=p.response(cache,c,W,value,context=ctx);results.append(out)
            torch.testing.assert_close(out,c.response(W,value),rtol=0,atol=1e-10)
        self.assertIs(cache.LU,factor);self.assertFalse(torch.equal(results[0],results[-1]))

    def test_06_no_bias_or_answer_retained(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        self.assertEqual(set(vars(cache)),{'capsule','W','LU','pivots','stamps'})
        self.assertEqual(p.extra_tensor_bytes(cache),72)

    def test_07_non_spd_update_rejected(self):
        c,W,_,ctx=fixture()
        with self.assertRaises(ValueError):p.prepare(c,-torch.eye(2,dtype=torch.float64)*100,context=ctx)

    def test_08_nonfinite_preparation_rejected(self):
        c,W,_,ctx=fixture();W[0,0]=float('nan')
        with self.assertRaises(ValueError):p.prepare(c,W,context=ctx)

    def test_09_nonsymmetric_update_rejected(self):
        c,W,_,ctx=fixture();W[0,1]=2
        with self.assertRaises(ValueError):p.prepare(c,W,context=ctx)

    def test_10_batched_shape_explicitly_out_of_scope(self):
        c,W,_,ctx=fixture()
        with self.assertRaises(ValueError):p.prepare(c,W.unsqueeze(0),context=ctx)

    def test_11_nonfinite_current_bias_rejected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);bias[0]=float('inf')
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_12_wrong_dtype_rejected(self):
        c,W,_,ctx=fixture()
        with self.assertRaises(ValueError):p.prepare(c,W.float(),context=ctx)

    def test_13_autograd_explicitly_out_of_scope(self):
        c,W,_,ctx=fixture();W.requires_grad_(True)
        with self.assertRaises(ValueError):p.prepare(c,W,context=ctx)

    def test_14_K_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);c.K.add_(0)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_15_y0_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);c.y0.add_(1)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_16_V_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);c.V.mul_(2)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_17_g_replacement_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);c.g=c.g.clone()
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_18_context_replacement_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=(ctx[0].clone(),)+ctx[1:])

    def test_19_context_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);ctx[0].add_(0)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_20_LU_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);cache.LU.add_(0)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_21_pivot_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);cache.pivots.add_(0)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_22_W_guard_mutation_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx);cache.W.add_(0)
        with self.assertRaises(ValueError):p.response(cache,c,W,bias,context=ctx)

    def test_23_changed_W_requires_reprepare(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        with self.assertRaises(ValueError):p.response(cache,c,W+torch.eye(2,dtype=torch.float64),bias,context=ctx)

    def test_24_equal_new_W_allowed(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        torch.testing.assert_close(p.response(cache,c,W.clone(),bias,context=ctx),c.response(W,bias),rtol=0,atol=1e-10)

    def test_25_capsule_binding_detected(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        with self.assertRaises(ValueError):p.response(cache,copy.copy(c),W,bias,context=ctx)

    def test_26_finite_signed_update_accepted(self):
        c,W,bias,ctx=fixture();W=-torch.eye(2,dtype=torch.float64)*.1
        cache=p.prepare(c,W,context=ctx)
        torch.testing.assert_close(p.response(cache,c,W,bias,context=ctx),c.response(W,bias),rtol=0,atol=1e-10)

    def test_27_checked_preparation_trace(self):
        c,W,_,ctx=fixture();_,trace=b.trace_call(lambda:p.prepare(c,W,context=ctx))
        self.assertEqual(trace,b.expected_trace('prepare',16))

    def test_28_query_trace_has_no_refactorization(self):
        c,W,bias,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        _,trace=b.trace_call(lambda:p.response(cache,c,W,bias,context=ctx))
        self.assertEqual(trace,b.expected_trace('prepared',16))

    def test_29_trace_wrappers_restored_on_error(self):
        original=torch.linalg.solve
        with self.assertRaises(ZeroDivisionError):b.trace_call(lambda:1/0)
        self.assertIs(torch.linalg.solve,original)

    def test_30_bad_preparation_does_not_change_reference(self):
        c,W,bias,ctx=fixture();before=c.response(W,bias)
        with self.assertRaises(ValueError):p.prepare(c,-torch.eye(2,dtype=torch.float64)*100,context=ctx)
        self.assertTrue(torch.equal(before,c.response(W,bias)))

    def test_31_parent_adapter_actual_quality_schema(self):
        rows=[dict(numeric_dimension=n,queries_per_update=q) for n in b.DIMENSIONS for q in b.BURSTS]
        checks=[dict(r,inventory=dict(candidate={},cached={}),unprofiled=[dict(passed=True)]*12,
                     profiled=[dict(passed=True)]*12) for r in rows]
        parent=SimpleNamespace(row_gate=lambda r:True)
        self.assertEqual(len(b.load_anchors(rows,checks,parent)),12)
        with self.assertRaises(ValueError):b.load_anchors(rows,checks[::-1],parent)
        checks[0]['profiled'][0]={'passed':False}
        with self.assertRaises(ValueError):b.load_anchors(rows,checks,parent)

    def test_32_audit_pass_independent_of_speed_ratio(self):
        rows=[row_fixture(n,q)[0] for n in b.DIMENSIONS for q in b.BURSTS]
        for r in rows:r['stream_ratio_prepared_over_cached']=1000
        self.assertTrue(b.gate(b.summarize(rows)))
        rows[0]['query_traces']['prepared']=[]
        self.assertFalse(b.gate(b.summarize(rows)))

    def test_33_archive_integrity(self):
        rows=[row_fixture()[0]]
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.zip'
            with zipfile.ZipFile(path,'w') as z:
                for arm in b.ARMS:z.writestr('2/1/'+arm+'/state.json',b'x')
            b.verify_archive(path,rows)
            with zipfile.ZipFile(path,'a') as z:z.writestr('extra',b'y')
            with self.assertRaises(ValueError):b.verify_archive(path,rows)

    def test_34_warmup_measurement_dispatch_and_parity(self):
        row,checks,files=row_fixture();inv=row['retained_inventory']
        prepared_inv=dict(inv['candidate'],**{'prepared-capsule.json':dict(bytes=1,sha256='z')})
        result=dict(inventory=dict(candidate=inv['candidate'],prepared=prepared_inv,cached=inv['cached']),
            quality=True,extra_reduced_tensor_bytes=72,prepare_trace=b.expected_trace('prepare',2),
            query_traces=row['query_traces'],checks=[],phases=row['trials'][0],files=files,resident={},
            reduced_factor_reused=True,full_factor_reused=True)
        with patch.object(b,'trajectory',return_value=result) as spy:
            measured,_,_=b.measure_cell(None,2,1,dict(candidate=inv['candidate'],cached=inv['cached']))
        self.assertEqual([c.args[-1] for c in spy.call_args_list],[0,1,2,3])
        self.assertEqual(len(measured['trials']),3)
        self.assertTrue(b.row_gate(measured))

    def test_35_runner_cli_and_own_tests_before_regression(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/'tools/run_c230.ps1').read_text(encoding='utf-8')
        launch=(root/'tools/invoke_c230.ps1').read_text(encoding='utf-8')
        self.assertIn('expected_focused_tests = 2665',run)
        self.assertIn('c229-v5f-cost-profile-02c07c2130ab49acbf1558009be3b3b3',launch)
        self.assertLess(launch.index('::ParseFile'),launch.index('$failure = $null'))
        self.assertIn('RUNNER_PARSE_ERROR',launch)
        self.assertLess(run.index('authoring_selftest = PASS'),run.index('& $Python -u -c $Regression'))
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,'embedded-python','exec')

    def test_36_source_bindings_and_current_bias(self):
        tree=ast.parse(inspect.getsource(b))
        aliases={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name)
                 and n.value.id.startswith('c') and n.value.id[1:].isdigit()}
        self.assertFalse(aliases)
        self.assertIn('bias-W@capsule.g',inspect.getsource(p.response))
        self.assertNotIn('check=False',inspect.getsource(b)+inspect.getsource(p))
        self.assertIn('bank.numeric.full_reference',inspect.getsource(b.trajectory))

    def test_37_cache_export_contains_all_extra_tensors(self):
        c,W,_,ctx=fixture();cache=p.prepare(c,W,context=ctx)
        helpers=SimpleNamespace(canonical=lambda x:x.tolist())
        export=json.loads(b.cache_export(cache,helpers))
        self.assertTrue({'W','LU','pivots','tensor_versions','references'}<=set(export))
        self.assertNotIn('bias',export);self.assertNotIn('answer',export)

    def test_38_synthetic_run_adapter_export_postcheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);summary=root/'summary.json';summary.write_text('{}')
            rows=[dict(numeric_dimension=n,queries_per_update=q) for n in b.DIMENSIONS for q in b.BURSTS]
            qualities=[dict(r,inventory=dict(candidate={},cached={}),unprofiled=[dict(passed=True)]*12,
                            profiled=[dict(passed=True)]*12) for r in rows]
            (root/'measurements.json').write_bytes(b.blob(rows));(root/'quality-checks.json').write_bytes(b.blob(qualities))
            pins={str(i):'x' for i in range(221)};protected={}
            for i in range(305):
                path=root/f'input{i}';path.write_bytes(b'x');protected[str(path)]=hashlib.sha256(b'x').hexdigest()
            audit=SimpleNamespace(sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                read_json=lambda p:json.loads(Path(p).read_text()),
                git=lambda root,*args:b'HEAD' if args[0]=='rev-parse' else b'feat/sft-target-loss' if args[0]=='branch' else b'')
            parent=SimpleNamespace(row_gate=lambda r:True);seen=[]
            def check(*args):seen.append('check');return {},pins,protected
            def cell(c,n,q,anchor):seen.append((n,q));return row_fixture(n,q)
            with patch.object(b,'parent_module',return_value=parent),patch.object(b,'context',return_value=SimpleNamespace(audit=audit)),patch.object(b,'precheck',side_effect=check),patch.object(b,'measure_cell',side_effect=cell),patch('sys.stdout',new=io.StringIO()):
                result=b.run(c229_summary=summary,output_dir=root/'out',expected_head='HEAD')
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(seen,['check']+[(n,q) for n in b.DIMENSIONS for q in b.BURSTS]+['check'])
            self.assertEqual(len(result['artifacts']),5)

    def test_39_actual_parent_export_and_fast_bank(self):
        parent=b.parent_module();c=b.context(parent)
        baseline=parent.trajectory(c.update,2,1,False)
        row,_,_=b.measure_cell(c,2,1,baseline['retained_inventory'])
        self.assertTrue(b.row_gate(row))

    def test_40_actual_historical_suite_count(self):
        root=Path(__file__).resolve().parents[1];names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(115,2666))
        self.assertEqual(b.regression_suite(root).countTestCases(),2665)


if __name__=='__main__':unittest.main(verbosity=2)
