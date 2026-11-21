import ast
from collections import Counter
from copy import deepcopy
import inspect
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch
from torch import nn
from fold_lm.v05 import memory_dispatch as live
from fold_lm.v05_benchmarks import gate_f_c222_withdrawal_lifecycle as b


def audit_fixture():
    rows=[]
    for i,(label,_,_,status,clocks) in enumerate(b.PLAN):
        beta=dict(status=status,relation=None,provenance=None)
        bindings=[["global","alpha","alpha-class-1"]]
        if i in (1,2,3):
            relation="beta-class-0" if i == 3 else "beta-class-2"
            beta=dict(status="SUPPORTED",relation=relation,provenance="observed")
            bindings.append(["project","beta",relation])
        shadow=dict(status="MISSING",relation=None,provenance=None)
        if i == 5:
            shadow=dict(status="SUPPORTED",relation="beta-class-2",provenance="hypothesis")
        if i >= 6:
            shadow=dict(status="OUT_OF_SCOPE",relation=None,provenance=None)
        rows.append(dict(label=label,clocks=list(clocks),beta=beta,
                         anchor=dict(status="SUPPORTED",relation="alpha-class-1",provenance="observed"),
                         shadow=shadow,bindings=bindings,export_provenance=["observed"]*len(bindings),
                         h2_W=[[0.25,0.0],[0.0,0.0]],h2_b=[0.0,0.0]))
    return rows


class FixtureModel(nn.Module):
    def __init__(self,kind):
        super().__init__()
        self.kind=kind
    def forward(self,x):
        if self.kind == "coverage":
            value=3 if not x[0,4] else 1 if x[0,3] else 0 if x[0,2] else 2
            width=4
        elif self.kind == "selector":
            value=int(x[0,1]);width=2
        else:
            value=0 if x.item() < 0 else 2 if x.item() > 0 else 1
            width=3
        y=torch.zeros((1,width));y[0,value]=1
        return y


class Forced(nn.Module):
    def __init__(self,model,value):
        super().__init__()
        self.model,self.value,self.original=model,value,None
    def forward(self,x):
        logits=self.model(x);self.original=int(logits.argmax())
        logits.zero_();logits[0,self.value]=1
        return logits


def spy_request(base,bank,state,query):
    cov,answer=(0,1) if query == "alpha" else state
    role=0 if query == "alpha" else 1
    bits={0:(1,0,1),1:(0,1,1),2:(0,0,1),3:(0,0,0)}[cov]
    def provider(port):
        if cov in (2,3):
            return live.ReadOutcome("MISSING" if cov == 2 else "OUT_OF_SCOPE")
        # Make an incorrect selected port observably wrong.
        value=answer-1 if port == role else (1 if answer != 2 else -1)
        return live.ReadOutcome("READABLE",torch.tensor([[float(value)]]),1)
    return live.QueryRequest(torch.tensor([[float(role==0),float(role==1),*bits,1.,1.]]),
                            torch.tensor([[float(role==0),float(role==1),1.,1.]]),provider)


def counter(rows):
    c=Counter()
    for row in rows:
        c.update(row["trace"]);c["bank_reads"]+=row["bank_reads"]
    return {k:c[k] for k in ("coverage","selector","provider","reader","bank_reads")}


def toy_evaluation():
    parent=SimpleNamespace(parent_module=lambda:None,request_for=spy_request,live=live,
                           ForcedCoverage=Forced,calls=counter)
    snapshots={s:[(label,None,(cov,answer)) for label,cov,answer,_,_ in b.PLAN] for s in b.SEED_FAMILIES[0]}
    models={name:{seed:FixtureModel(name) for seed in seeds}
            for name,seeds in zip(("coverage","selector","reader"),b.SEED_FAMILIES[1:],strict=True)}
    main,controls=b.evaluate(parent,models,snapshots)
    audits={s:audit_fixture() for s in b.SEED_FAMILIES[0]}
    return main,controls,b.summarize(parent,main,controls,audits,1.0,True)


class C222Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main,cls.controls,cls.summary=toy_evaluation()

    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_workload_arithmetic(self):
        m=b.manifest()
        self.assertEqual(m["main_decisions"],81*8*2)
        self.assertEqual(m["control_decisions"],81*2)
        self.assertEqual(m["readable_decisions"]+m["suppressed_decisions"],1296)
        self.assertEqual(m["successful_model_forwards"],3+1296+891+891+162+162)

    def test_03_beta_readable_and_suppressed_counts(self):
        self.assertEqual(sum(p[2] is not None for p in b.PLAN),3)
        self.assertEqual(sum(p[2] is None for p in b.PLAN),5)

    def test_04_readable_score(self):
        r=live.DispatchResult(0,1,0,"ANSWER",("coverage","selector","provider","reader"),1)
        self.assertTrue(b.score_decision(r,0,0))

    def test_05_old_pre_replace_answer_rejected(self):
        r=live.DispatchResult(0,1,2,"ANSWER",("coverage","selector","provider","reader"),1)
        self.assertFalse(b.score_decision(r,0,0))

    def test_06_retired_value_cannot_be_answered(self):
        r=live.DispatchResult(2,1,0,"ANSWER",("coverage","selector","provider","reader"),1)
        self.assertFalse(b.score_decision(r,2,None))

    def test_07_missing_oos_not_interchangeable(self):
        r=live.DispatchResult(3,None,None,"SUPPRESS_OUT_OF_SCOPE",("coverage",))
        self.assertFalse(b.score_decision(r,2,None))
        self.assertTrue(b.score_decision(r,3,None))

    def test_08_suppression_cannot_hide_downstream_call(self):
        r=live.DispatchResult(2,None,None,"SUPPRESS_MISSING",("coverage","selector"))
        self.assertFalse(b.score_decision(r,2,None))

    def test_09_readable_score_requires_bank_read(self):
        r=live.DispatchResult(0,1,0,"ANSWER",("coverage","selector","provider","reader"),0)
        self.assertFalse(b.score_decision(r,0,0))

    def test_10_registered_symbolic_audit(self):
        self.assertTrue(b.audit_ok(audit_fixture()))

    def test_11_hypothesis_cannot_advance_evidence_clock(self):
        rows=audit_fixture();rows[5]["clocks"][1]=5
        self.assertFalse(b.audit_ok(rows))

    def test_12_anchor_cannot_be_lost(self):
        rows=audit_fixture();rows[4]["anchor"]["relation"]="alpha-class-2"
        self.assertFalse(b.audit_ok(rows))

    def test_13_symbolic_retracted_is_not_missing(self):
        rows=audit_fixture();rows[4]["beta"]["status"]="MISSING"
        self.assertFalse(b.audit_ok(rows))

    def test_14_hypothesis_cannot_be_exported(self):
        rows=audit_fixture();rows[5]["bindings"].append(["sandbox","beta","beta-class-2"])
        self.assertFalse(b.audit_ok(rows))

    def test_15_hypothesis_provenance_cannot_be_observed(self):
        rows=audit_fixture();rows[5]["shadow"]["provenance"]="observed"
        self.assertFalse(b.audit_ok(rows))

    def test_16_ended_shadow_scope_is_explicit(self):
        rows=audit_fixture();rows[6]["shadow"]["status"]="MISSING"
        self.assertFalse(b.audit_ok(rows))

    def test_17_hypothesis_cannot_change_authoritative_numeric_state(self):
        rows=audit_fixture();rows[5]["h2_b"]=[0.0,0.75]
        self.assertFalse(b.audit_ok(rows))

    def test_18_tombstone_cannot_expose_old_relation(self):
        rows=audit_fixture();rows[4]["beta"]["relation"]="beta-class-0"
        self.assertFalse(b.audit_ok(rows))

    def test_19_snapshot_sequence_must_be_complete(self):
        self.assertFalse(b.audit_ok(audit_fixture()[:-1]))

    def test_20_spy_live_matrix_and_gate(self):
        self.assertEqual((len(self.main),len(self.controls)),(1296,162))
        self.assertTrue(b.gate(self.summary))
        self.assertEqual(self.summary["main_calls"],b.manifest()["successful_main_calls"])

    def test_21_main_failure_is_rejected(self):
        s=deepcopy(self.summary);s["main_success"]-=1
        self.assertFalse(b.gate(s))

    def test_22_post_retraction_publication_rejected(self):
        s=deepcopy(self.summary);s["post_retract_beta_answers"]=1
        self.assertFalse(b.gate(s))

    def test_23_anchor_failure_rejected(self):
        s=deepcopy(self.summary);s["anchor_success"]-=1
        self.assertFalse(b.gate(s))

    def test_24_forced_allow_reaches_provider_not_reader(self):
        self.assertTrue(all(r["action"] == "BLOCKED_MISSING" for r in self.controls))
        self.assertTrue(all(r["trace"] == ("coverage","selector","provider") for r in self.controls))
        self.assertTrue(all(r["original_coverage"] == 2 for r in self.controls))
        self.assertEqual(self.summary["control_calls"],b.manifest()["successful_control_calls"])

    def test_25_mutated_weights_rejected(self):
        s=deepcopy(self.summary);s["fingerprints_unchanged"]=False
        self.assertFalse(b.gate(s))

    def test_26_no_optimizer_training_or_state_reset_between_stages(self):
        source=inspect.getsource(b.run)
        self.assertNotIn("torch.optim",source)
        self.assertNotIn(".backward(",source)
        trajectory=inspect.getsource(b.timeline)
        self.assertEqual(trajectory.count("bank.initial_state()"),1)
        self.assertNotIn("bank.read(",trajectory)

    def test_27_parent_adapter_matches_accepted_fields(self):
        source=inspect.getsource(b.precheck)
        self.assertIn('p["validation_summary"]',source)
        self.assertIn('p["source_blobs"]',source)
        self.assertIn('p["input_sha256"]',source)
        self.assertIn("PARENT_VALIDATION_SHA",source)

    def test_28_scope_counts_and_no_production_changes(self):
        self.assertEqual(len(b.OWN),6)
        self.assertEqual(len(b.OUTPUTS),5)
        self.assertFalse(b.manifest()["production_runtime_modified"])
        self.assertFalse(b.manifest()["old_request_reuse_tested"])
        self.assertFalse(b.manifest()["gate_f_candidate"])

    def test_29_runner_and_launcher_contract(self):
        root=Path(__file__).resolve().parents[1]
        launch=(root/"tools/invoke_c222.ps1").read_text(encoding="utf-8")
        run=(root/"tools/run_c222.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2401",run)
        self.assertIn("tests_lm.test_v05_c222_withdrawal_lifecycle",run)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertIn("c221-v5f-live-coverage-dispatch-cbcaaf2ea8b94d7a8b748426810f442b",launch)
        self.assertRegex(launch,r'\$runnerPath\s*=\s*Join-Path \$Root "tools\\run_c222.ps1"')
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))

    def test_30_python_alias_bindings(self):
        tree=ast.parse(inspect.getsource(b))
        bound={a.asname or a.name.split(".")[0] for n in ast.walk(tree)
               if isinstance(n,(ast.Import,ast.ImportFrom)) for a in n.names}
        refs={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute)
              and isinstance(n.value,ast.Name) and n.value.id.startswith("c") and n.value.id[1:].isdigit()}
        self.assertFalse(refs-bound)

    def test_31_actual_accepted_memory_timeline(self):
        base=b.parent_module().parent_module()
        rows=list(b.timeline(base,{0:0,1:1,3:3,5:5},218001))
        self.assertEqual(len({id(bank) for _,bank,_ in rows}),1)
        audits=[b.snapshot_audit(base,*row) for row in rows]
        self.assertTrue(b.audit_ok(audits))

    def test_32_actual_historical_suite_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(107,2402))
        self.assertEqual(b.regression_suite(root).countTestCases(),2401)


if __name__ == "__main__":
    unittest.main(verbosity=2)
