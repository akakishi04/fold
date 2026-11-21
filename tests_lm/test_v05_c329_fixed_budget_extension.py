"""C329 software fixtures, not native Windows or scientific FOLD results."""
from __future__ import annotations
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import numpy as np
import torch
from fold_lm.v05_benchmarks import model_c329_fixed_budget_extension as s

ROOT = Path(__file__).resolve().parents[1]
_loader = importlib.util.spec_from_file_location('_c329_test_executor', ROOT/'tools/c329_execution.py')
e = importlib.util.module_from_spec(_loader); _loader.loader.exec_module(e)


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone = torch.nn.Module()
        self.backbone.core = torch.nn.Linear(2, 2, bias=False, dtype=torch.float64)
        self.head = torch.nn.Linear(2, 256, bias=False, dtype=torch.float64)
    def forward(self, tokens, tasks):
        return self.head(self.backbone.core(tokens.to(torch.float64)/10))


def optimizer(model):
    core = list(model.backbone.core.parameters()); ids = {id(p) for p in core}
    return torch.optim.AdamW([dict(params=[p for p in model.parameters() if id(p) not in ids], lr=.005),
                             dict(params=core, lr=.0005)], lr=.005, betas=(.9,.999), eps=1e-8, weight_decay=0.)


def toy():
    torch.manual_seed(91); model = Toy(); calls = []
    tokens = torch.tensor([[1,2],[3,4],[2,1],[4,3]], dtype=torch.int64)
    targets = torch.tensor([48,49,48,49], dtype=torch.int64)
    def select(tables, event, mask):
        calls.append(event); return tokens + int(event) % 3, torch.arange(4)
    def check(z, n):
        s.require(z.shape == (n,256) and z.dtype == torch.float64 and bool(torch.isfinite(z).all()), 'toy logits')
    def verify(opt, m, arm):
        s.require(type(opt) is torch.optim.AdamW and [g['lr'] for g in opt.param_groups] == list(s.RATES), 'toy policy')
    x = NS(policy=NS(optimizer_for=lambda m,a:optimizer(m), verify_optimizer=verify), c=NS(p267=NS(check_logits=check)))
    return model, tokens, targets, NS(select_tokens=select), x, calls


def run_toy(prefix=2):
    m,t,y,p,x,calls = toy()
    with patch.object(s,'PREFIX',prefix), patch.object(s,'TOTAL',2*prefix), patch.object(s,'curriculum',return_value=p), contextlib.redirect_stdout(io.StringIO()):
        trace, states = s.optimize(m, {}, y, list(range(prefix)), [None]*prefix, x)
    return m,t,y,p,x,calls,trace,states


def gates():
    return [dict(seed=k, candidate_interior_pass=True, candidate_retention_pass=True,
                 original_answer_gain=0, original_pair_gain=0, interior_answer_gain=1, interior_pair_gain=1) for k in s.SEEDS]


def contrast(gain=0):
    return dict(answers=288, query_pairs=144, control_correct=100, candidate_correct=100+gain,
        control_both_correct=50, candidate_both_correct=50+gain, rescued=max(0,gain), regressed=max(0,-gain),
        pair_rescued=max(0,gain), pair_regressed=max(0,-gain), answer_gain=gain, query_pair_gain=gain)


def validation(negative=False):
    seeds, pairs = [], []
    for seed in s.SEEDS:
        for arm in s.ARMS:
            seeds.append(dict(seed=seed, arm=arm, original_pass={str(n):True for n in range(2,7)},
                              retention_pass=True, interior_pass=not negative))
        pairs.append(dict(seed=seed, control_retention_pass=True, candidate_retention_pass=True,
            control_interior_pass=not negative, candidate_interior_pass=not negative, original_answer_gain=0,
            original_pair_gain=0, interior_answer_gain=1, interior_pair_gain=1, interior=contrast(1),
            original_by_length={str(n):contrast() for n in range(2,7)}, shared_prefix_preserved=True, paired_success=not negative))
    return dict(candidate_gate=not negative, paired_success_count=0 if negative else 5, seed_results=seeds,
                paired_comparisons=pairs, all_shared_prefixes=True, all_replays=True, **s.WORK)


def receipt():
    return dict(commit_sha='a'*40, tests=s.FULL_TESTS, failures=0, errors=0, skipped=0, successful=True)


def parent_fixture():
    pins = {**e.BOOTSTRAP, **{f'pin{i}':'a'*40 for i in range(826-len(e.BOOTSTRAP))}}
    inputs = {f'input{i}':'b'*64 for i in range(1561)}
    r = dict(schema='fold-c328-science-v1', experiment_id='parent', stage='stage', commit_sha=e.PARENT_EXECUTION,
        status='FAIL', diagnostic_execution_valid=True, gate_f_candidate=False, production_adoption=False,
        source_blobs=dict(pins), input_sha256=dict(inputs), manifest_sha256='c'*64, validation_summary={'candidate_gate':False})
    v = dict(schema='fold-c328-execution-envelope-v1', commit_sha=e.PARENT_EXECUTION, scientific_summary_sha256=e.PARENT_SUMMARY,
        scientific_status='FAIL', source_count=826, input_count=1561, source_blobs=pins, input_sha256=inputs,
        manifest_sha256='c'*64, scientific_work={'train_steps':12000}, parent_summary_sha256='d'*64, parent_envelope_sha256='e'*64,
        immediate_parent_semantic_reconstruction=True, ancestor_semantic_reruns=0, saved_semantic_reconstruction=True,
        final_reference_rechecks=1561, hash_stats={'final_reference_rechecks':1561},
        regression=dict(commit_sha=e.PARENT_EXECUTION, tests=5722, failures=0, errors=0, skipped=0, successful=True))
    p = NS(validate_seal=lambda:None, EXPERIMENT_ID='parent', STAGE='stage', OWN=(e.P_PATH,e.E_PATH), MANIFEST_SHA='c'*64, WORK={'train_steps':12000})
    helper = NS(check_validation=lambda v:None, BOOTSTRAP={}, PARENT_SUMMARY='d'*64, PARENT_ENVELOPE='e'*64)
    return r,v,p,helper


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)], check=True)
    for args in [('checkout','-qb',e.BRANCH),('config','user.name','C329 fixture'),('config','user.email','c329@example.invalid')]:
        subprocess.run(['git','-C',str(root),*args], check=True, capture_output=True)
    (root/'docs').mkdir(); (root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC329 ACTIVE / NOT YET JUDGED\n', encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'], check=True)
    subprocess.run(['git','-C',str(root),'commit','-qm','fixture'], check=True)
    return e.git(root,'rev-parse','HEAD')


class C329Tests(unittest.TestCase):
    def test_01_manifest(self):
        s.validate_seal()
        with patch.object(s,'TOTAL',2500), self.assertRaises(ValueError):
            s.validate_seal()
    def test_02_fresh_cohort_and_accounting(self):
        self.assertEqual(s.SEEDS, tuple(range(329001,329006))); self.assertEqual(s.ORDERS, tuple(range(329101,329106)))
        self.assertEqual(len(s.identities()),10); self.assertEqual(s.WORK['train_steps'],5*2400)
        self.assertEqual(s.WORK['model_forward_calls'],5*2400+20*171)
        self.assertEqual(s.WORK['row_presentations'],5*2400*48+20*16416)
        self.assertEqual(s.WORK['core_forward_calls'],4*s.WORK['model_forward_calls'])
        self.assertEqual(s.WORK['model_state_loads'],20)
    def test_03_protection_and_suite_arithmetic(self):
        self.assertEqual(s.SOURCE_COUNT,826+len(s.OWN)); self.assertEqual(s.INPUT_COUNT,1561+10+len(s.OWN))
        self.assertEqual(s.FULL_TESTS,5722+s.OWN_TESTS); self.assertEqual(len(set(s.OWN)),6)
    def test_04_hash_order_and_value(self):
        self.assertEqual(s.state_hash({'a':1,'b':torch.ones(2)}),s.state_hash({'b':torch.ones(2),'a':1}))
        self.assertNotEqual(s.state_hash(torch.ones(2)),s.state_hash(torch.zeros(2)))
    def test_05_hash_types_shape_and_bad_values(self):
        self.assertNotEqual(s.state_hash(torch.ones(2)),s.state_hash(torch.ones(1,2)))
        self.assertNotEqual(s.state_hash([1]),s.state_hash((1,)))
        self.assertNotEqual(s.state_hash(torch.ones(2)),s.state_hash(torch.ones(2,dtype=torch.float64)))
        for v in (float('nan'),torch.tensor(float('inf')),{True:1},object()):
            with self.subTest(), self.assertRaises(ValueError): s.state_hash(v)
    def test_06_snapshot_is_deep_and_no_optimizer_mutation(self):
        m,_,_,_,_,_=toy(); opt=optimizer(m); before=s.state_hash(opt.state_dict()); w=s.state_hash(m.state_dict())
        state,r=s.checkpoint(m,opt,1200)
        self.assertEqual(r['optimizer'],before); self.assertEqual(r['weights'],w)
        state[next(iter(state))].zero_(); self.assertEqual(s.state_hash(m.state_dict()),w)
    def test_07_two_cycles_real_arithmetic(self):
        m,t,y,p,x,calls,r,states=run_toy(2)
        self.assertEqual(calls,[0,1,0,1]); self.assertEqual(r['event_indices'],calls)
        ref,_,_,_,_,_=toy(); opt=optimizer(ref); prefix=None
        for i in range(4):
            opt.zero_grad(set_to_none=True); F=torch.nn.functional
            F.cross_entropy(ref(t+i%2,torch.zeros(4,dtype=torch.int64)),y).backward()
            torch.nn.utils.clip_grad_norm_(ref.parameters(),1.,error_if_nonfinite=True); opt.step()
            if i==1: prefix={k:v.detach().clone() for k,v in ref.state_dict().items()}
        self.assertEqual(s.state_hash(states[0]),s.state_hash(prefix)); self.assertEqual(s.state_hash(states[1]),s.state_hash(ref.state_dict()))
    def test_08_real2400_updates_and_preserved1200_prefix(self):
        m,t,y,p,x,calls=toy(); created=[]; original=x.policy.optimizer_for
        def factory(model,arm): created.append(model); return original(model,arm)
        x.policy.optimizer_for=factory
        with patch.object(s,'curriculum',return_value=p), contextlib.redirect_stdout(io.StringIO()):
            r,states=s.optimize(m,{},y,list(range(1200)),[None]*1200,x)
        self.assertEqual(len(created),1); self.assertEqual(calls,list(range(1200))*2)
        self.assertEqual(r['continuation'],{k:r['checkpoints'][0][k] for k in ('weights','optimizer')})
        self.assertEqual(r['optimizer_group_lrs'],[list(s.RATES)]*2400)
        self.assertEqual(s.state_hash(states[0]),r['checkpoints'][0]['weights'])
        self.assertNotEqual(s.state_hash(states[0]),s.state_hash(states[1]))
        self.assertEqual(r['intermediate_evaluations'],0)
    def test_09_no_automatic_budget_extension(self):
        m,_,y,p,x,_=toy(); x.policy.optimizer_for=Mock()
        with self.assertRaises(ValueError): s.optimize(m,{},y,[],[],x)
        x.policy.optimizer_for.assert_not_called()
    def test_10_nonfinite_stops_before_snapshot(self):
        m,_,y,p,x,_=toy()
        with patch.object(s,'curriculum',return_value=p), patch.object(m,'forward',return_value=torch.full((4,256),float('nan'),dtype=torch.float64)), patch.object(s,'checkpoint') as checkpoint, self.assertRaises(ValueError):
            s.optimize(m,{},y,list(range(1200)),[None]*1200,x)
        checkpoint.assert_not_called()
    def test_11_snapshot_corruption_stops_continuation(self):
        m,_,y,p,x,_=toy(); original=s.checkpoint
        def corrupt(*args):
            state,r=original(*args); r['optimizer']='a'*64; return state,r
        with patch.object(s,'PREFIX',2), patch.object(s,'TOTAL',4), patch.object(s,'curriculum',return_value=p), patch.object(s,'checkpoint',side_effect=corrupt), self.assertRaises(ValueError):
            s.optimize(m,{},y,[0,1],[None,None],x)
    def test_12_rate_drift_stops(self):
        m,_,y,p,x,_=toy()
        def wrong(model,arm):
            opt=optimizer(model); opt.param_groups[0]['lr']=.001; return opt
        x.policy.optimizer_for=wrong
        with patch.object(s,'curriculum',return_value=p), self.assertRaises(ValueError):
            s.optimize(m,{},y,list(range(1200)),[None]*1200,x)
    def test_13_checkpoint_hashes_match_live_state(self):
        m,_,_,_,_,_,r,states=run_toy()
        self.assertEqual(s.state_hash(m.state_dict()),r['checkpoints'][1]['weights'])
        self.assertEqual([z['step'] for z in r['checkpoints']],[2,4])
        self.assertEqual(s.state_hash(states[1]),r['checkpoints'][1]['weights'])
    def test_14_native_schedule_dispatch_and_fresh_order(self):
        planner=Mock(return_value=torch.zeros((1200,24,4),dtype=torch.int64)); validator=Mock()
        x=NS(parent=NS(plan_for_order=planner),p312=object(),pairs=object()); rows=[{}]*192
        with patch.object(s,'curriculum',return_value=NS(validate_schedule=validator)):
            s.schedule(329003,rows,x)
        self.assertEqual(planner.call_args.args[0],329103); self.assertEqual(planner.call_args.args[1],'two_to_four')
        validator.assert_called_once()
        for seed in (328001,True,329001.):
            with self.subTest(),self.assertRaises(ValueError): s.schedule(seed,rows,x)
    def test_15_exact_trace_validation_and_tamper(self):
        m,_,_,_,_,_,r,states=run_toy(2)
        events=torch.arange(12).reshape(3,4);mask=torch.zeros((3,2),dtype=torch.int64)
        r.update(seed=329001,steps=4,training_rows=115200,schedule_events=events,template_pair_events=mask,
            family_exposure_per_cycle={'exposure':1},schedule_sha256=s.digest(events.tolist()),mask_sha256=s.digest(mask.tolist()),
            policy_receipt=dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400))
        p=NS(family_mask=lambda *a:mask,exposure=lambda *a:{'exposure':1})
        with patch.object(s,'PREFIX',2),patch.object(s,'TOTAL',4),patch.object(s,'schedule',return_value=events),patch.object(s,'curriculum',return_value=p):
            s.check_trace(r,329001,[],None)
            for key,value in [('event_indices',[0,1,1,0]),('optimizer_creations',2),('intermediate_evaluations',1),('continuation',{}),('mask_sha256','bad')]:
                bad=copy.deepcopy(r);bad[key]=value
                with self.subTest(key=key),self.assertRaises(ValueError):s.check_trace(bad,329001,[],None)
    def test_16_safe_bundle_complete_checkpoint_identities(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'m.pt';v=dict(schema='fold-c329-models-v1',identities=[list(x) for x in s.identities()],readout_policy='mean_last',states=[{'w':torch.ones(2)} for _ in range(10)])
            torch.save(v,path);self.assertEqual(len(s.load_bundle(path)),10)
            v['identities'].reverse();torch.save(v,path)
            with self.assertRaises(ValueError):s.load_bundle(path)
    def test_17_gate_requires_complete_cohort(self):
        self.assertEqual(s.fixed_gate(gates()),(True,[True]*5))
        for rows in (gates()[:-1],gates()[::-1],[gates()[0]]*5):
            with self.subTest(),self.assertRaises(ValueError):s.fixed_gate(rows)
    def test_18_each_gate_condition_required(self):
        for key,v in [('candidate_interior_pass',False),('candidate_retention_pass',False),('interior_answer_gain',0),('interior_pair_gain',0),('original_answer_gain',-1),('original_pair_gain',-1)]:
            rows=gates();rows[2][key]=v
            with self.subTest():self.assertEqual(s.fixed_gate(rows),(False,[True,True,False,True,True]))
    def test_19_boolean_gain_is_not_count(self):
        rows=gates();rows[0]['interior_answer_gain']=True
        with self.assertRaises(ValueError):s.fixed_gate(rows)
    def test_20_contrast_conservation_and_bounds(self):
        e.check_contrast(contrast(-2))
        for k in ('answers','rescued','pair_rescued','answer_gain','query_pair_gain'):
            r=contrast(2);r[k]+=1
            with self.subTest(),self.assertRaises(ValueError):e.check_contrast(r)
    def test_21_validation_keeps_valid_negative(self):
        e.check_validation(validation());e.check_validation(validation(True))
    def test_22_validation_tamper(self):
        for kind in ('work','cohort','prefix','gain','gate'):
            v=validation()
            if kind=='work':v['model_state_loads']=10
            elif kind=='cohort':v['seed_results'].pop()
            elif kind=='prefix':v['paired_comparisons'][0]['shared_prefix_preserved']=False
            elif kind=='gain':v['paired_comparisons'][0]['original_answer_gain']=1
            else:v['candidate_gate']=False
            with self.subTest(),self.assertRaises(ValueError):e.check_validation(v)
    def test_23_accepted_negative_parent(self):
        e.parent_contract(*parent_fixture())
        for change in ('PASS','wrong'):
            args=parent_fixture();args[0]['status']=change
            with self.subTest(),self.assertRaises(ValueError):e.parent_contract(*args)
    def test_24_parent_science_schema_not_diagnostic(self):
        args=parent_fixture();args[0]['schema']='fold-c327-diagnostic-v1'
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_25_invalid_negative_not_accepted(self):
        args=parent_fixture();args[0]['diagnostic_execution_valid']=False
        with self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[0]['validation_summary']['candidate_gate']=True
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_26_parent_exact_full_protection(self):
        for key,value in [('source_count',820),('input_count',1549)]:
            args=parent_fixture();args[1][key]=value
            with self.subTest(),self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[0]['source_blobs'].pop(e.E_PATH)
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_27_parent_direct_pin_and_hash(self):
        args=parent_fixture();args[1]['scientific_summary_sha256']='bad'
        with self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[0]['source_blobs'][e.P_PATH]='bad';args[1]['source_blobs'][e.P_PATH]='bad'
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_28_parent_regression_semantics_and_rereads(self):
        for key,value in [('final_reference_rechecks',1560),('saved_semantic_reconstruction',False),('ancestor_semantic_reruns',1)]:
            args=parent_fixture();args[1][key]=value
            with self.subTest(),self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[1]['regression']['skipped']=1
        with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_29_strict_json_and_utf8_exclusive_save(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';e.save(p,{'名前':'甲乙'});self.assertEqual(e.read(p),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(p,{})
            for text in ('{"a":1,"a":2}','NaN','Infinity'):
                p.write_text(text,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError):e.read(p)
    def test_30_source_lf_crlf_and_tamper(self):
        raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for v in (raw,raw.replace(b'\n',b'\r\n')):p.write_bytes(v);self.assertEqual(e.source_bytes(p,oid),v)
            for v in (b'a\nb\r\n',b'bad'):
                p.write_bytes(v)
                with self.subTest(),self.assertRaises(ValueError):e.source_bytes(p,oid)
    def test_31_real_git_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);head=git_fixture(root);e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,'a'*40)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError):e.guard(root,head)
    def test_32_only_unique_formal_active(self):
        self.assertTrue(e.active('## Formal state\nC329 ACTIVE / NOT YET JUDGED\n## History\nC328 ACTIVE / NOT YET JUDGED'))
        for text in ('## History\nC329 ACTIVE / NOT YET JUDGED','## Formal state\nC328 ACTIVE / NOT YET JUDGED','## Formal state\nC329 ACTIVE / NOT YET JUDGED\nC330 ACTIVE / NOT YET JUDGED'):
            self.assertFalse(e.active(text))
    def test_33_actual_own_suite_loader_and_duplicate_rejection(self):
        class Case(unittest.TestCase):
            def __init__(self,i):super().__init__();self.number=i
            def id(self):return 'fixture.'+str(self.number)
        def flatten(suite):
            for t in suite:
                if isinstance(t,unittest.TestSuite):yield from flatten(t)
                else:yield t
        inherited=[Case(i) for i in range(5722)]
        b=NS(EXCLUDED='excluded',regression_modules=lambda root:list(range(210)))
        helper=NS(suite=lambda *a:inherited);r6=NS(flatten=flatten,RECOVERY_MODULES=('a','b','c'))
        self.assertEqual(e.suite(ROOT,b,helper,None,None,None,r6).countTestCases(),s.FULL_TESTS)
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),s.OWN_TESTS)
        inherited[-1]=inherited[0]
        with self.assertRaises(ValueError):e.suite(ROOT,b,helper,None,None,None,r6)
    def test_34_stage_order_valid_negative(self):
        calls=[]
        def step(name,v):
            def run():calls.append(name);return v
            return run
        with contextlib.redirect_stdout(io.StringIO()):e.execute_stages('a'*40,step('preflight',None),step('tests',receipt()),step('fit',{'gate':False}),step('saved',([],{'gate':False})),step('final',[]))
        self.assertEqual(calls,['preflight','tests','fit','saved','final'])
    def test_35_preflight_failure_prevents_regression(self):
        tests=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):e.execute_stages('a'*40,Mock(side_effect=ValueError('native')),tests,Mock(),Mock(),Mock())
        tests.assert_not_called()
    def test_36_regression_failure_prevents_fitting(self):
        fit=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):e.execute_stages('a'*40,lambda:None,lambda:{**receipt(),'failures':1},fit,Mock(),Mock())
        fit.assert_not_called()
    def test_37_saved_mismatch_prevents_finalization(self):
        final=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):e.execute_stages('a'*40,lambda:None,receipt,lambda:{'gate':False},lambda:([],{'gate':True}),final)
        final.assert_not_called()
    def test_38_semantic_output_byte_binding(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in s.OUTPUTS:(root/name).write_bytes(b'fixture')
            self.assertEqual(e.bound_semantics(root,lambda:'ok')[0],'ok')
            def mutate():(root/s.OUTPUTS[0]).write_bytes(b'bad')
            with self.assertRaises(ValueError):e.bound_semantics(root,mutate)
    def test_39_controller_no_retry_and_output_bounds(self):
        for fail in (False,True):
            with tempfile.TemporaryDirectory() as d,patch.object(e,'guard'),patch.object(e,'subprocess_run',side_effect=ValueError('native') if fail else None) as child,contextlib.redirect_stdout(io.StringIO()) as out:
                root=Path(d)
                if fail:
                    with self.assertRaises(ValueError):e.run(root,root/'runs/x','a'*40)
                    self.assertEqual(child.call_count,1);self.assertIn('run_execution_valid = false',out.getvalue())
                else:
                    e.run(root,root/'runs/x','a'*40);self.assertEqual([c.args[-1] for c in child.call_args_list],['science','verify'])
                with self.assertRaises(ValueError):e.run(root,root/'outside','a'*40)
    def test_40_actual_subprocess_cli_rejection(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):e.subprocess_run(ROOT,Path(d),'a'*40,'invalid-mode')
            self.assertIn('invalid choice',(Path(d)/'invalid-mode.log').read_text(encoding='utf-8'))
    def test_41_launcher_and_numeric_source_contract(self):
        text=(ROOT/'tools/invoke_c329.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C329',text);self.assertIn('run_c329.ps1',text)
        tree=ast.parse(inspect.getsource(s.optimize))
        attrs=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertEqual(attrs.count('optimizer_for'),1);self.assertEqual(attrs.count('manual_seed'),1)
        self.assertNotIn('evaluate',attrs);self.assertNotIn('patch',inspect.getsource(e.scientific_worker))
    def test_42_production_science_finishes_fits_before_any_evaluation(self):
        calls=[];cx=(None,);b=NS(check_dependencies=lambda *a:None,replay_error=lambda *a:0.)
        prepared={'original':({},torch.zeros(192,dtype=torch.int64)),'interior4':({},torch.zeros(192,dtype=torch.int64))}
        p=NS(previous=lambda:NS(training=lambda *a:prepared))
        def train(seed,*a):calls.append('fit');return {'seed':seed},[{'w':torch.ones(2)*seed},{'w':torch.ones(2)*(seed+1)}]
        def measure(*a):calls.append('eval');return {},{}
        with tempfile.TemporaryDirectory() as d,patch.object(s,'base',return_value=b),patch.object(s,'curriculum',return_value=p),patch.object(s,'train_one',side_effect=train),patch.object(s,'make_model',return_value=object()),patch.object(s,'measure',side_effect=measure),patch.object(s,'analyze',return_value=([],{'candidate_gate':False})),contextlib.redirect_stdout(io.StringIO()):
            out=Path(d);v=s.run_science(out,{}, {},{},cx,ROOT,{})
            self.assertFalse(v['candidate_gate']);self.assertEqual(calls,['fit']*5+['eval']*20)
            self.assertEqual(set(p.name for p in out.iterdir()),set(s.OUTPUTS))
            archive=torch.load(out/'evaluations.pt',weights_only=True)
            self.assertEqual([(r['seed'],r['arm']) for r in archive['records']],s.identities())
    def test_43_production_worker_valid_negative(self):self.worker_fixture(False)
    def test_44_production_worker_regression_failure_no_fit(self):self.worker_fixture(True)
    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);folder=root/'runs/x';folder.mkdir(parents=True);calls=[]
            pins={f'p{i}':'a'*40 for i in range(s.SOURCE_COUNT)};inputs={str(root/f'i{i}'):'b'*64 for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={};stats={'final_reference_rechecks':s.INPUT_COUNT}
                def __init__(self,*a,**kw):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            r4=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),);b=NS(context=lambda:cx,check_dependencies=lambda *a:None,peak_rss=lambda:1)
            v=validation(True)
            def snapshot(*a):calls.append('snapshot');return {},{},pins,inputs
            def data(*a):calls.append('parent');return {'TRAIN':[]},{},{}
            def preflight(*a):calls.append('preflight')
            def tests(*a):
                calls.append('tests');r=receipt()
                if bad:r.update(failures=1,successful=False)
                e.save(folder/'regression-result.json',r)
            def fit(out,*a):
                calls.append('fit')
                for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
                return v
            def saved(*a):calls.append('saved');return [],v
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(NS(),NS(),NS(native_runtime=lambda:(torch,np)),NS(),r4,None)),patch.object(e,'parent',return_value=NS()),patch.object(s,'base',return_value=b),patch.object(e,'snapshot',side_effect=snapshot),patch.object(e,'parent_semantics',side_effect=data),patch.object(e,'subprocess_run',side_effect=tests),patch.object(s,'runtime_preflight',side_effect=preflight),patch.object(s,'run_science',side_effect=fit),patch.object(s,'semantic_recheck',side_effect=saved):
                if bad:
                    with self.assertRaises(ValueError):e.scientific_worker(root,folder,'a'*40)
                    self.assertNotIn('fit',calls)
                else:
                    e.scientific_worker(root,folder,'a'*40)
                    self.assertEqual(calls,['snapshot','parent','preflight','tests','fit','saved','final','release'])
                    self.assertEqual(e.read(folder/'science/summary.json')['status'],'FAIL')
                    self.assertEqual(e.read(folder/'execution-envelope.json')['input_count'],s.INPUT_COUNT)
    def test_45_exact_snapshot_complete_unions_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);pins={};inputs={}
            def write(name,value):
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value)
                return p
            def oid(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            for i in range(1561):
                name=f'ancestor/{i}.py';raw=f'x={i}\n'.encode();path=write(name,raw);inputs[e.canonical(path)]=e.sha(path)
                if i<826:pins[name]=oid(raw)
            tree=dict(pins)
            for name in s.OWN:
                raw=('own:'+name).encode();write(name,raw);tree[name]=oid(raw)
            po=root/e.PARENT_FOLDER/'science';po.mkdir(parents=True)
            outputs=tuple(s.OUTPUTS)
            for name in outputs:(po/name).write_bytes(b'parent')
            e.save(po/'summary.json',{'artifacts':[]});e.save(po.parent/'execution-envelope.json',{'source_blobs':pins,'input_sha256':inputs})
            desc=lambda out,*a:{e.canonical(out/n):e.sha(out/n) for n in outputs}
            legacy=NS(descriptors=desc,tree_blobs=lambda root:tree);cache=NS(sha=e.sha)
            with patch.object(e,'PARENT_SUMMARY',e.sha(po/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(po.parent/'execution-envelope.json')),patch.object(e,'parent_contract'):
                _,_,sources,protected=e.snapshot(root,NS(OUTPUTS=outputs),NS(),legacy,cache)
                self.assertEqual(len(sources),s.SOURCE_COUNT);self.assertEqual(len(protected),s.INPUT_COUNT)
                (root/'ancestor/42.py').write_bytes(b'corrupt')
                with self.assertRaises(ValueError):e.snapshot(root,NS(OUTPUTS=outputs),NS(),legacy,cache)
    def test_46_real_helper_loader_bootstrap_order(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);path=root/'parent.py';raw=b'def helpers(root):\n    return (1,2,3,4,5)\n';path.write_bytes(raw)
            oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            with patch.object(e,'E_PATH','parent.py'),patch.object(e,'BOOTSTRAP',{'parent.py':oid}),patch.object(e,'git',return_value=oid):
                result=e.helpers(root);self.assertEqual(result[1:],(1,2,3,4,5))
                path.write_bytes(b'bad')
                with self.assertRaises(ValueError):e.helpers(root)
    def test_47_parent_semantics_calls_actual_parent_signature(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True)
            data={'TRAIN':[]};old={};new={}
            for name,v in [('dataset.json',data),('original-prompts.json',old),('interior-prompts.json',new)]:e.save(out/name,v)
            p=NS(OUTPUTS=('dataset.json','original-prompts.json','interior-prompts.json'),blob=s.blob,semantic_recheck=Mock(return_value=([],{'candidate_gate':False})))
            b=NS(digest=s.digest,DATA_SHA=s.digest(data),PROMPTS_SHA=s.digest(old))
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda *a:None)))
            cx=(None,None,NS(new_prompts=lambda *a:new,check_prompts=lambda *a:None),None,x)
            inputs={e.canonical(out/n):e.sha(out/n) for n in p.OUTPUTS}
            self.assertEqual(e.parent_semantics(root,{'validation_summary':{'candidate_gate':False}},p,b,cx,inputs),(data,old,new))
            self.assertEqual(p.semantic_recheck.call_args.args,(out,data,old,new,cx,e.read))
    def test_48_saved_semantic_reader_dispatch_and_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);archive=dict(schema='fold-c329-evaluations-v1',trajectories=[],records=[])
            torch.save(archive,out/'evaluations.pt');values=(s.manifest(),{},{},{},[],{'candidate_gate':False})
            names=(s.OUTPUTS[0],s.OUTPUTS[1],s.OUTPUTS[2],s.OUTPUTS[3],s.OUTPUTS[6],s.OUTPUTS[7])
            for name,v in zip(names,values):e.save(out/name,v)
            with patch.object(s,'load_bundle',return_value=[]),patch.object(s,'analyze',return_value=([],{'candidate_gate':False})) as analyze:
                self.assertEqual(s.semantic_recheck(out,{},{},{},(),e.read),([],{'candidate_gate':False}))
                self.assertEqual(analyze.call_args.args[0]['schema'],'fold-c329-evaluations-v1')
                (out/s.OUTPUTS[7]).write_text('{"candidate_gate":true}',encoding='utf-8')
                with self.assertRaises(ValueError):s.semantic_recheck(out,{},{},{},(),e.read)


if __name__ == '__main__':
    unittest.main()
