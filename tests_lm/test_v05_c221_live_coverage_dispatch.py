import ast
from dataclasses import fields
import inspect
import itertools
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch
from torch import nn
from fold_lm.v05 import memory_dispatch as live
from fold_lm.v05_benchmarks import gate_f_c221_live_coverage_dispatch as b


class Fixed(nn.Module):
    def __init__(self, value, width):
        super().__init__()
        self.value, self.width, self.calls = value, width, 0
    def forward(self, x):
        self.calls += 1
        out = torch.zeros((1,self.width))
        out[0,self.value] = 1
        return out


class FixtureCoverage(nn.Module):
    def forward(self, x):
        value = 3 if not x[0,4] else 1 if x[0,3] else 0 if x[0,2] else 2
        return Fixed(value,4)(x)


class FixtureSelector(nn.Module):
    def forward(self, x):
        return x[:,:2].clone()


class FixtureReader(nn.Module):
    def forward(self, x):
        return Fixed(0 if x.item() < 0 else 2 if x.item() > 0 else 1,3)(x)


def request(cov=0, answer=2, provider=None):
    bits = {0:(1,0,1),1:(0,1,1),2:(0,0,1),3:(0,0,0)}[cov]
    if provider is None:
        def provider(port):
            if cov in (2,3):
                return live.ReadOutcome("MISSING" if cov == 2 else "OUT_OF_SCOPE")
            return live.ReadOutcome("READABLE",torch.tensor([[float(answer-1)]]),1)
    return live.QueryRequest(torch.tensor([[1.,0.,*bits,1.,1.]]),
                             torch.tensor([[1.,0.,1.,1.]]), provider)


def toy_evaluation():
    groups = {
        "coverage":{s:FixtureCoverage() for s in b.SEED_FAMILIES[1]},
        "selector":{s:FixtureSelector() for s in b.SEED_FAMILIES[2]},
        "reader":{s:FixtureReader() for s in b.SEED_FAMILIES[3]},
    }
    requests = {s:{label:request(cov,answer) for label,_,cov,answer in b.PLAN}
                for s in b.SEED_FAMILIES[0]}
    baseline = {seeds+(label,):(cov,answer) for seeds in itertools.product(*b.SEED_FAMILIES)
                for label,_,cov,answer in b.PLAN}
    main, controls = b.evaluate(requests,groups,baseline)
    return main,controls,b.summarize(main,controls,1.0,True)


class C221Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_request_has_no_scorer_fields(self):
        self.assertEqual([f.name for f in fields(live.QueryRequest)],
                         ["coverage_features","query_features","provider"])

    def test_03_supported_actual_call_order(self):
        r=live.dispatch_query(request(),Fixed(0,4),Fixed(0,2),Fixed(2,3))
        self.assertEqual((r.action,r.answer,r.trace,r.bank_reads),
                         ("ANSWER",2,("coverage","selector","provider","reader"),1))

    def test_04_hot_is_readable(self):
        r=live.dispatch_query(request(1),Fixed(1,4),Fixed(0,2),Fixed(2,3))
        self.assertEqual((r.coverage,r.action),(1,"ANSWER"))

    def test_05_missing_does_not_call_poison_provider(self):
        def poison(port):
            raise AssertionError("must not be called")
        sel,read=Fixed(0,2),Fixed(2,3)
        r=live.dispatch_query(request(2,provider=poison),Fixed(2,4),sel,read)
        self.assertEqual((r.action,r.trace,sel.calls,read.calls),
                         ("SUPPRESS_MISSING",("coverage",),0,0))

    def test_06_oos_does_not_call_selector_reader(self):
        sel,read=Fixed(0,2),Fixed(2,3)
        r=live.dispatch_query(request(3),Fixed(3,4),sel,read)
        self.assertEqual((r.action,r.answer,sel.calls,read.calls),
                         ("SUPPRESS_OUT_OF_SCOPE",None,0,0))

    def test_07_force_suppress_present_state(self):
        cov=FixtureCoverage()
        control=b.ForcedCoverage(cov,2)
        r=live.dispatch_query(request(0),control,Fixed(0,2),Fixed(2,3))
        self.assertEqual((control.original,r.coverage,r.trace),(0,2,("coverage",)))

    def test_08_false_allow_missing_is_provider_blocked(self):
        read=Fixed(1,3)
        r=live.dispatch_query(request(2),Fixed(0,4),Fixed(0,2),read)
        self.assertEqual((r.action,r.answer,read.calls,r.bank_reads),
                         ("BLOCKED_MISSING",None,0,0))
        self.assertEqual(r.trace,("coverage","selector","provider"))

    def test_09_false_allow_oos_is_provider_blocked(self):
        r=live.dispatch_query(request(3),Fixed(1,4),Fixed(0,2),Fixed(2,3))
        self.assertEqual(r.action,"BLOCKED_OUT_OF_SCOPE")

    def test_10_numeric_failure_cannot_reach_reader(self):
        q=request(provider=lambda port:live.ReadOutcome("NUMERIC_UNSAFE",bank_reads=1))
        read=Fixed(1,3)
        r=live.dispatch_query(q,Fixed(0,4),Fixed(0,2),read)
        self.assertEqual((r.action,r.bank_reads,read.calls),("BLOCKED_NUMERIC_UNSAFE",1,0))

    def test_11_provider_rejects_value_on_block(self):
        with self.assertRaises(ValueError):
            live.ReadOutcome("MISSING",torch.zeros((1,1)))

    def test_12_provider_rejects_nonfinite(self):
        with self.assertRaises(ValueError):
            live.ReadOutcome("READABLE",torch.tensor([[float("nan")]]))

    def test_13_provider_rejects_wrong_shape(self):
        with self.assertRaises(ValueError):
            live.ReadOutcome("READABLE",torch.zeros(2))

    def test_14_provider_rejects_unknown_status(self):
        with self.assertRaises(ValueError):
            live.ReadOutcome("UNKNOWN")

    def test_15_request_type_checked(self):
        with self.assertRaises(TypeError):
            live.dispatch_query({},Fixed(0,4),Fixed(0,2),Fixed(0,3))

    def test_16_bad_model_output_shape_is_invalid(self):
        with self.assertRaises(ValueError):
            live.dispatch_query(request(),Fixed(0,2),Fixed(0,2),Fixed(0,3))

    def test_17_bad_input_is_invalid(self):
        q=request()
        bad=live.QueryRequest(torch.zeros(7),q.query_features,q.provider)
        with self.assertRaises(ValueError):
            live.dispatch_query(bad,Fixed(0,4),Fixed(0,2),Fixed(0,3))

    def test_18_bad_provider_contract_is_invalid(self):
        with self.assertRaises(TypeError):
            live.dispatch_query(request(provider=lambda port:None),Fixed(0,4),Fixed(0,2),Fixed(0,3))

    def test_19_all_synthetic_cases_and_controls_execute(self):
        main,controls,s=toy_evaluation()
        self.assertEqual((len(main),len(controls)),(648,324))
        self.assertTrue(b.gate(s))

    def test_20_counters_count_invocations_not_claimed_constants(self):
        self.assertEqual(b.calls([dict(trace=("coverage","selector"),bank_reads=0)]),
                         dict(coverage=1,selector=1,provider=0,reader=0,bank_reads=0))

    def test_21_one_failure_rejects_gate(self):
        _,_,s=toy_evaluation()
        s["main_success"]-=1
        self.assertFalse(b.gate(s))

    def test_22_suppression_leak_rejects_gate(self):
        _,_,s=toy_evaluation()
        s["suppressed_downstream_calls"]=1
        self.assertFalse(b.gate(s))

    def test_23_control_failure_rejects_gate(self):
        _,_,s=toy_evaluation()
        s["control_success"]-=1
        self.assertFalse(b.gate(s))

    def test_24_parent_parity_failure_rejects_gate(self):
        _,_,s=toy_evaluation()
        s["parent_parity"]-=1
        self.assertFalse(b.gate(s))

    def test_25_intervention_calls_frozen_model_once(self):
        model=Fixed(0,4)
        control=b.ForcedCoverage(model,3)
        self.assertEqual(int(control(torch.zeros((1,7))).argmax()),3)
        self.assertEqual((control.original,model.calls),(0,1))

    def test_26_invalid_intervention_rejected(self):
        with self.assertRaises(ValueError):
            b.ForcedCoverage(Fixed(0,4),4)

    def test_27_dispatch_signature_has_no_teacher(self):
        self.assertEqual(tuple(inspect.signature(live.dispatch_query).parameters),
                         ("request","coverage_model","selector_model","reader_model"))
        source=inspect.getsource(live.dispatch_query)
        self.assertNotIn("expected",source)
        self.assertNotIn("episode_plan",source)

    def test_28_request_setup_does_not_call_bank_read(self):
        self.assertNotIn("bank.read(",inspect.getsource(b.build_requests))
        self.assertIn("bank.read(",inspect.getsource(b.request_for))

    def test_29_scorer_calls_live_dispatch_before_checking_result(self):
        source=inspect.getsource(b.evaluate)
        self.assertLess(source.index("live.dispatch_query("),source.index("expected_action ="))
        self.assertNotIn("reader_predictions",source)

    def test_30_new_python_aliases_resolve(self):
        for module in (live,b):
            tree=ast.parse(inspect.getsource(module))
            bound={a.asname or a.name.split(".")[0] for node in ast.walk(tree)
                   if isinstance(node,(ast.Import,ast.ImportFrom)) for a in node.names}
            refs={node.value.id for node in ast.walk(tree) if isinstance(node,ast.Attribute)
                  and isinstance(node.value,ast.Name) and node.value.id.startswith("c")
                  and node.value.id[1:].isdigit()}
            self.assertFalse(refs-bound)

    def test_31_powershell_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        launch=(root/"tools/invoke_c221.ps1").read_text(encoding="utf-8")
        run=(root/"tools/run_c221.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2369",run)
        self.assertIn("tests_lm.test_v05_c221_live_coverage_dispatch",run)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launch)
        self.assertIn("c220-v5f-frozen-learned-stack-5bc9d133c96348de81a24d19b3ef6f93",launch)
        self.assertRegex(launch,r'\$runnerPath\s*=\s*Join-Path \$Root "tools\\run_c221.ps1"')
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))

    def test_32_manifest_scopes_and_arithmetic(self):
        m=b.manifest()
        self.assertEqual(m["main_decisions"],m["combinations"]*len(b.PLAN))
        self.assertEqual(m["control_decisions"],m["combinations"]*len(b.CONTROLS))
        self.assertFalse(m["oracle_labels_in_dispatch"])
        self.assertFalse(m["gate_f_candidate"])
        self.assertEqual(m["new_training_steps"],0)

    def test_33_actual_historical_suite_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(106,2370))
        self.assertEqual(b.regression_suite(root).countTestCases(),2369)

    def test_34_plan_matches_accepted_parent(self):
        parent=b.parent_module()
        converted=tuple((r["label"],r["query"],int(parent.coverage.CoverageClass[r["expected_coverage"]]),
                         r["target_class"]) for r in parent.episode_plan())
        self.assertEqual(converted,b.PLAN)
        self.assertEqual(parent.EPISODE_PLAN_SHA,b.PARENT_EPISODE_SHA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
