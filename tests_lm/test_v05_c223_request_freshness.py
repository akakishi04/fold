import ast
from copy import deepcopy
from dataclasses import fields
import inspect
import itertools
from pathlib import Path
import unittest

import torch
from torch import nn
from fold_lm.v05 import memory_request_lease as leases
from fold_lm.v05_benchmarks import gate_f_c223_request_freshness as b


class Fixed(nn.Module):
    def __init__(self,value,width):
        super().__init__()
        self.value,self.width,self.calls = value,width,0
    def forward(self,x):
        self.calls += 1
        out = torch.zeros((1,self.width))
        out[0,self.value] = 1
        return out


class ToyCoverage(nn.Module):
    def forward(self,x):
        value = 3 if not x[0,4] else 1 if x[0,3] else 0 if x[0,2] else 2
        return Fixed(value,4)(x)


class ToySelector(nn.Module):
    def forward(self,x):
        return x[:,:2].clone()


class ToyReader(nn.Module):
    def forward(self,x):
        return Fixed(0 if x.item()<0 else 2 if x.item()>0 else 1,3)(x)


def make_request(pair,query):
    _,index = pair
    _,cov,answer = b.PLAN[index]
    role = 0 if query == "alpha" else 1
    if role == 0:
        cov,answer = 0,1
    bits = {0:(1,0,1),1:(0,1,1),2:(0,0,1),3:(0,0,0)}[cov]
    def provider(port):
        if answer is None:
            return leases.live.ReadOutcome("MISSING" if cov == 2 else "OUT_OF_SCOPE")
        return leases.live.ReadOutcome("READABLE",torch.tensor([[float(answer-1)]]),1)
    return leases.live.QueryRequest(torch.tensor([[float(role==0),float(role==1),*bits,1.,1.]]),
                                    torch.tensor([[float(role==0),float(role==1),1.,1.]]),provider)


def parent_fixture():
    rows=[]
    names=("writer_seed","coverage_seed","selector_seed","reader_seed")
    for seeds in itertools.product(*b.SEED_FAMILIES):
        for label,_,_ in b.PLAN:
            for query in ("alpha","beta"):
                row=dict(zip(names,seeds,strict=True))
                expected=b.expected_result(label,query)
                rows.append(dict(row,label=label,query=query,success=True,**expected))
    return rows


def toy_matrix():
    models=dict(coverage={s:ToyCoverage() for s in b.SEED_FAMILIES[1]},
                selector={s:ToySelector() for s in b.SEED_FAMILIES[2]},
                reader={s:ToyReader() for s in b.SEED_FAMILIES[3]})
    snapshots={s:[(row[0],None,index) for index,row in enumerate(b.PLAN)] for s in b.SEED_FAMILIES[0]}
    baseline=b.parent_answers(parent_fixture())
    rows=b.evaluate(make_request,models,snapshots,baseline)
    return rows,b.summarize(*rows,1.0,True)


class C223Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.summary=toy_matrix()

    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_lease_has_no_answer_or_teacher(self):
        self.assertEqual([f.name for f in fields(leases.RequestLease)],["owner","generation","request"])

    def test_03_current_lease_runs_real_dispatch(self):
        s=leases.RequestSession((None,2),make_request)
        r=s.execute(s.bind("beta"),Fixed(0,4),Fixed(1,2),Fixed(2,3))
        self.assertEqual((r.status,r.result.answer,r.trace,r.bank_reads),
                         ("CURRENT",2,("freshness","coverage","selector","provider","reader"),1))

    def test_04_stale_rejected_before_any_model(self):
        s=leases.RequestSession((None,2),make_request);old=s.bind("beta")
        s.publish((None,4))
        c,p,r=Fixed(0,4),Fixed(1,2),Fixed(2,3)
        result=s.execute(old,c,p,r)
        self.assertEqual((result.status,result.result,result.trace,c.calls,p.calls,r.calls),
                         ("STALE_REQUEST",None,("freshness",),0,0,0))

    def test_05_old_provider_is_not_called(self):
        def poison(port):
            raise AssertionError("old provider reached")
        q=make_request((None,2),"beta")
        s=leases.RequestSession(0,lambda state,query:leases.live.QueryRequest(q.coverage_features,q.query_features,poison))
        old=s.bind("beta");s.publish(1)
        self.assertEqual(s.execute(old,Fixed(0,4),Fixed(0,2),Fixed(0,3)).status,"STALE_REQUEST")

    def test_06_fresh_after_publication_uses_new_state(self):
        s=leases.RequestSession((None,2),make_request);s.publish((None,4))
        result=s.execute(s.bind("beta"),ToyCoverage(),ToySelector(),ToyReader())
        self.assertEqual((result.status,result.result.action),("CURRENT","SUPPRESS_MISSING"))

    def test_07_representation_only_publication_invalidates(self):
        s=leases.RequestSession((None,1),make_request);old=s.bind("beta")
        s.publish((None,2))
        self.assertEqual(s.execute(old,ToyCoverage(),ToySelector(),ToyReader()).status,"STALE_REQUEST")
        r=s.execute(s.bind("beta"),ToyCoverage(),ToySelector(),ToyReader())
        self.assertEqual((r.result.coverage,r.result.answer),(0,2))

    def test_08_same_generation_lease_reusable(self):
        s=leases.RequestSession((None,2),make_request);ticket=s.bind("beta")
        a=s.execute(ticket,ToyCoverage(),ToySelector(),ToyReader())
        z=s.execute(ticket,ToyCoverage(),ToySelector(),ToyReader())
        self.assertEqual(a,z)

    def test_09_wrong_session_rejected(self):
        first=leases.RequestSession((None,2),make_request)
        second=leases.RequestSession((None,2),make_request)
        r=second.execute(first.bind("beta"),Fixed(0,4),Fixed(1,2),Fixed(2,3))
        self.assertEqual((r.status,r.result,r.trace),("WRONG_SESSION",None,("freshness",)))

    def test_10_generation_monotonic(self):
        s=leases.RequestSession((None,2),make_request)
        for i in range(5):
            self.assertEqual(s.generation,i)
            s.publish((None,2))

    def test_11_raw_unprotected_closure_reproduces_old_value(self):
        s=leases.RequestSession((None,2),make_request);old=s.bind("beta")
        s.publish((None,4))
        raw=leases.live.dispatch_query(old.request,ToyCoverage(),ToySelector(),ToyReader())
        self.assertEqual(raw.answer,2)
        self.assertEqual(s.execute(old,ToyCoverage(),ToySelector(),ToyReader()).status,"STALE_REQUEST")

    def test_12_invalid_factory_rejected(self):
        with self.assertRaises(TypeError):
            leases.RequestSession(None,None)

    def test_13_invalid_factory_return_rejected(self):
        s=leases.RequestSession(None,lambda state,query:None)
        with self.assertRaises(TypeError):
            s.bind("beta")

    def test_14_empty_query_rejected(self):
        s=leases.RequestSession((None,2),make_request)
        with self.assertRaises(ValueError):
            s.bind("")

    def test_15_invalid_lease_type_rejected(self):
        s=leases.RequestSession((None,2),make_request)
        with self.assertRaises(TypeError):
            s.execute(None,Fixed(0,4),Fixed(1,2),Fixed(2,3))

    def test_16_identical_state_publication_is_conservative(self):
        pair=(None,2);s=leases.RequestSession(pair,make_request);ticket=s.bind("beta")
        s.publish(pair)
        self.assertEqual(s.execute(ticket,ToyCoverage(),ToySelector(),ToyReader()).status,"STALE_REQUEST")

    def test_17_publication_during_bind_rejected(self):
        s=None
        def factory(state,query):
            s.publish(state)
            return make_request(state,query)
        s=leases.RequestSession((None,2),factory)
        with self.assertRaises(RuntimeError):
            s.bind("beta")

    def test_18_publication_in_provider_withholds_result(self):
        s=None
        def factory(state,query):
            q=make_request(state,query)
            def provider(port):
                s.publish((None,4))
                return q.provider(port)
            return leases.live.QueryRequest(q.coverage_features,q.query_features,provider)
        s=leases.RequestSession((None,2),factory)
        r=s.execute(s.bind("beta"),ToyCoverage(),ToySelector(),ToyReader())
        self.assertEqual((r.status,r.result),("CHANGED_DURING_DISPATCH",None))
        self.assertEqual(r.trace,("freshness","coverage","selector","provider","reader"))

    def test_19_complete_spy_matrix_gate(self):
        self.assertTrue(b.gate(self.summary))
        self.assertEqual([len(x) for x in self.rows],[1296,4536,81,324])

    def test_20_exact_fresh_invocation_counts(self):
        self.assertEqual(self.summary["fresh_calls"],b.manifest()["fresh_calls"])

    def test_21_stale_attempts_do_no_downstream_work(self):
        self.assertEqual(self.summary["stale_calls"],dict(coverage=0,selector=0,provider=0,reader=0,bank_reads=0))
        self.assertTrue(all(r["trace"] == ("freshness",) and r["result"] is None for r in self.rows[1]))

    def test_22_raw_replay_controls_expose_the_original_contract(self):
        self.assertTrue(all(r["reproduced_old"] and r["differs_current"] for r in self.rows[3]))

    def test_23_one_stale_exposure_rejects_gate(self):
        s=deepcopy(self.summary);s["stale_result_exposures"]=1
        self.assertFalse(b.gate(s))

    def test_24_one_parent_parity_error_rejects_gate(self):
        s=deepcopy(self.summary);s["parent_parity"]-=1
        self.assertFalse(b.gate(s))

    def test_25_one_replay_or_repeat_failure_rejects_gate(self):
        for field in ("repeat_success","replay_success"):
            s=deepcopy(self.summary);s[field]-=1
            self.assertFalse(b.gate(s))

    def test_26_parent_decision_adapter_validates_actual_schema(self):
        rows=parent_fixture()
        self.assertEqual(len(b.parent_answers(rows)),1296)
        rows[0]["answer"]=2
        with self.assertRaises(ValueError):
            b.parent_answers(rows)

    def test_27_parent_adapter_rejects_duplicate_or_incomplete(self):
        rows=parent_fixture();rows[-1]=rows[0]
        with self.assertRaises(ValueError):
            b.parent_answers(rows)
        with self.assertRaises(ValueError):
            b.parent_answers(rows[:-1])

    def test_28_no_training_and_expected_values_not_session_inputs(self):
        source=inspect.getsource(leases.RequestSession)
        self.assertNotIn("expected",source)
        self.assertNotIn("baseline",source)
        self.assertNotIn("optim.",inspect.getsource(b.run))
        self.assertFalse(b.manifest()["answer_cache_added"])

    def test_29_accepted_loader_and_source_registration(self):
        self.assertEqual(len(b.OWN),7)
        self.assertEqual(len(b.OUTPUTS),5)
        self.assertIn("parent_answers(",inspect.getsource(b.run))
        self.assertIn('"live-decisions.json"',inspect.getsource(b.run))

    def test_30_manifest_workload_arithmetic(self):
        m=b.manifest()
        self.assertEqual(m["stale_decisions"],sum(range(8))*2*81)
        self.assertEqual(m["successful_model_forwards"],3+sum(m[n+"_calls"][k]
            for n in ("fresh","stale","repeat","replay") for k in ("coverage","selector","reader")))
        self.assertEqual(m["new_training_steps"],0)

    def test_31_runner_and_launcher(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c223.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c223.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2435",run)
        self.assertIn("tests_lm.test_v05_c223_request_freshness",run)
        self.assertIn("c222-v5f-withdrawal-lifecycle-60ba479f7d2b46ff957b5d2a21bf865c",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))

    def test_32_new_aliases_are_bound(self):
        for module in (b,leases):
            tree=ast.parse(inspect.getsource(module))
            bound={a.asname or a.name.split(".")[0] for n in ast.walk(tree)
                   if isinstance(n,(ast.Import,ast.ImportFrom)) for a in n.names}
            refs={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute)
                  and isinstance(n.value,ast.Name) and n.value.id.startswith("c") and n.value.id[1:].isdigit()}
            self.assertFalse(refs-bound)

    def test_33_plan_and_actual_commit_revision_match_parent(self):
        parent=b.parent_module()
        self.assertEqual(tuple(row[:3] for row in parent.PLAN),b.PLAN)
        base=parent.parent_module().parent_module()
        rows=list(parent.timeline(base,{0:0,1:1,3:3,5:5},218001))
        hot,committed=rows[1][2],rows[2][2]
        self.assertEqual(hot.memory_revision,committed.memory_revision)
        self.assertEqual(committed.h2.storage_epoch,hot.h2.storage_epoch+1)

    def test_34_actual_regression_suite_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(108,2436))
        self.assertEqual(b.regression_suite(root).countTestCases(),2435)


if __name__ == "__main__":
    unittest.main(verbosity=2)
