from copy import deepcopy
from dataclasses import dataclass, replace
from enum import Enum
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch
from fold_lm.v05_benchmarks import gate_f_c224_history_cost_audit as b


class Kind(str,Enum):
    ASSERT="ASSERT"
    REPLACE="REPLACE"


class Status(str,Enum):
    COMMITTED="COMMITTED"
    SUPPORTED="SUPPORTED"


@dataclass(frozen=True)
class Prov:
    source_id:str


@dataclass(frozen=True)
class Record:
    scope_id:str
    factor_id:str
    relation_key:str
    provenance:Prov


@dataclass(frozen=True)
class Mem:
    memory_revision:int=0
    records:tuple=()


@dataclass(frozen=True)
class Op:
    kind:Kind
    expected_memory_revision:int
    scope_id:str
    factor_id:str
    relation_key:str
    source_id:str
    evidence_time:int


def apply(mem,op):
    assert mem.memory_revision == op.expected_memory_revision
    table={(r.scope_id,r.factor_id):r for r in mem.records}
    table[(op.scope_id,op.factor_id)]=Record(op.scope_id,op.factor_id,op.relation_key,Prov(op.source_id))
    return Mem(mem.memory_revision+1,tuple(table[k] for k in sorted(table))),None


@dataclass(frozen=True)
class H2:
    W:torch.Tensor
    b:torch.Tensor


@dataclass(frozen=True)
class State:
    memory_revision:int
    mem:Mem
    h2:H2


@dataclass
class Bridge:
    base:torch.Tensor
    def full_reference(self,mem):
        values=torch.zeros(2,dtype=torch.float64)
        for r in mem.records:
            values[0 if r.factor_id == "alpha" else 1]=(int(r.relation_key[-1])-1)*3/17
        return SimpleNamespace(status=Status.SUPPORTED,value=values)


@dataclass
class Bank:
    numeric:Bridge
    def initial_state(self):
        return State(0,Mem(),H2(torch.zeros((2,2)),torch.zeros(2)))
    def apply(self,state,op):
        mem,_=apply(state.mem,op)
        return State(mem.memory_revision,mem,state.h2),None
    def commit(self,state):
        return replace(state,h2=H2(torch.eye(2)*0.25,self.numeric.full_reference(state.mem).value)),Status.COMMITTED
    def read(self,state):
        return self.numeric.full_reference(state.mem)
    def to_memory_state(self,state):
        return state.mem


def backend():
    return SimpleNamespace(c216=SimpleNamespace(build_bank=lambda:Bank(Bridge(torch.eye(2)))),
        memory=SimpleNamespace(MemoryState=Mem,MemoryOp=Op,MemoryOpKind=Kind,apply_memory_op=apply))


class C224Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row,cls.checks,cls.candidate,cls.baseline=b.measure(backend(),8)

    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_registered_raw_hashes(self):
        for n in b.SIZES:
            self.assertEqual(b.sha_bytes(b.ledger(n)),b.manifest()["ledger_sha256"][str(n)])

    def test_03_ledger_event_shapes(self):
        rows=[json.loads(x) for x in b.ledger(8).splitlines()]
        self.assertEqual(len(rows),8)
        self.assertEqual([r["kind"] for r in rows],["ASSERT","ASSERT"]+["REPLACE"]*6)
        self.assertEqual([r["time"] for r in rows],list(range(1,9)))

    def test_04_semantic_cycle_and_fixed_anchor(self):
        rows=[json.loads(x) for x in b.ledger(8).splitlines()]
        self.assertEqual(rows[0]["relation"],"alpha-class-1")
        self.assertEqual([r["relation"] for r in rows[1:4]],
                         ["beta-class-0","beta-class-1","beta-class-2"])

    def test_05_index_uses_utf8_byte_offsets(self):
        raw=b.ledger(8);index=b.source_index(raw)
        self.assertTrue(b.validate_index(raw,index))
        self.assertGreater(len(raw),len(raw.decode("utf-8")))
        for source,(start,end) in index.items():
            self.assertEqual(json.loads(raw[start:end])["source_id"],source)

    def test_06_incomplete_index_rejected(self):
        raw=b.ledger(8);index=b.source_index(raw);index.pop(next(reversed(index)))
        with self.assertRaises(ValueError):
            b.validate_index(raw,index)

    def test_07_duplicate_sources_rejected(self):
        line=b.ledger(2).splitlines(keepends=True)[0]
        with self.assertRaises(ValueError):
            b.source_index(line+line)

    def test_08_corrupt_range_rejected(self):
        raw=b.ledger(8);index=b.source_index(raw);index[next(iter(index))]=(1,5)
        with self.assertRaises(ValueError):
            b.validate_index(raw,index)

    def test_09_actual_replay_byte_event_counters(self):
        raw=b.ledger(8);meter=dict(raw_bytes=0,events=0)
        self.assertEqual(len(list(b.events(raw,meter))),8)
        self.assertEqual(meter,dict(raw_bytes=len(raw),events=8))

    def test_10_tensor_export_contains_values_dtype_and_shape(self):
        x=torch.tensor([[1.,2.]],dtype=torch.float64)
        item=b.canonical(x)
        self.assertEqual(item,dict(tensor=True,dtype="torch.float64",shape=[1,2],values=[[1.,2.]]))

    def test_11_nonfinite_export_rejected(self):
        for value in (float("nan"),torch.tensor([float("inf")])):
            with self.assertRaises(ValueError):
                b.canonical(value)

    def test_12_all_dataclass_fields_exported(self):
        self.assertEqual(set(b.canonical(Record("a","b","c",Prov("d")))["fields"]),
                         {"scope_id","factor_id","relation_key","provenance"})

    def test_13_unknown_export_object_rejected(self):
        with self.assertRaises(TypeError):
            b.canonical(object())

    def test_14_reachable_object_estimate_deduplicates(self):
        raw=b"x"*10000
        one=b.resident_estimate([raw])
        two=b.resident_estimate([raw,raw])
        self.assertLess(two["total_estimated_data_bytes"]-one["total_estimated_data_bytes"],100)

    def test_15_shared_tensor_storage_estimate_deduplicates(self):
        x=torch.zeros(20,dtype=torch.float64)
        size=b.resident_estimate([x,x[:10]])
        self.assertEqual(size["unique_cpu_tensor_storage_bytes"],160)

    def test_16_instrumented_measurement_function_completes(self):
        self.assertTrue(b.row_gate(self.row))
        self.assertEqual(len(self.checks),4)

    def test_17_raw_query_work_is_separate_from_build(self):
        self.assertEqual(self.row["candidate_build_work"]["events"],8)
        self.assertTrue(all(t["events"] == 0 for t in self.row["candidate_query_trials"]))
        self.assertTrue(all(t["events"] == 8 for t in self.row["baseline_query_trials"]))

    def test_18_no_raw_deletion_to_manufacture_savings(self):
        self.assertEqual(self.candidate["evidence.ndjson"],self.baseline["evidence.ndjson"])
        self.assertGreater(self.row["storage_delta_bytes"],0)
        self.assertTrue(b.row_gate(self.row))
        self.assertFalse(b.manifest()["superiority_required_for_audit_pass"])

    def test_19_omitted_cost_component_fails_audit(self):
        row=deepcopy(self.row);row["candidate_total_export_bytes"]-=row["raw_bytes"]
        self.assertFalse(b.row_gate(row))

    def test_20_bad_numeric_quality_fails_audit(self):
        row=deepcopy(self.row);row["quality_pass"]=False
        self.assertFalse(b.row_gate(row))

    def test_21_wrong_replay_work_fails_audit(self):
        row=deepcopy(self.row);row["baseline_query_trials"][0]["events"]=0
        self.assertFalse(b.row_gate(row))

    def test_22_source_provenance_and_symbolic_state_checked(self):
        self.assertTrue(self.row["provenance_resolves"])
        self.assertTrue(all(c["symbolic_state_equal"] for c in self.checks))

    def test_23_larger_history_retains_two_live_factors(self):
        row,_,_,_=b.measure(backend(),32)
        self.assertEqual(row["live_factors"],2)
        self.assertEqual(row["source_index_entries"],32)
        self.assertGreater(row["raw_bytes"],self.row["raw_bytes"])
        self.assertTrue(b.row_gate(row))

    def test_24_candidate_query_has_no_raw_replay_or_hidden_baseline(self):
        source=inspect.getsource(b.query_candidate)
        self.assertNotIn("events(",source)
        self.assertNotIn("query_replay",source)
        self.assertIn("bank.read(state)",source)

    def test_25_no_training_or_production_modification_claim(self):
        m=b.manifest()
        self.assertEqual(m["new_training_steps"],0)
        self.assertFalse(m["learned_heads_exercised"])
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_f_candidate"])

    def test_26_artifact_inventory_matches_exact_bytes(self):
        for files in (self.candidate,self.baseline):
            inventory=b.file_inventory(files)
            for name,data in files.items():
                self.assertEqual(inventory[name],dict(bytes=len(data),sha256=b.sha_bytes(data)))

    def test_27_measurement_gate_requires_all_registered_sizes(self):
        s=b.summarize([self.row])
        self.assertFalse(b.gate(s))
        s["history_sizes"]=list(b.SIZES)
        self.assertFalse(b.gate(s))
        self.assertTrue(b.gate(b.summarize([b.measure(backend(),n)[0] for n in b.SIZES])))

    def test_28_runner_and_launcher_contract(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c224.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c224.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2465",run)
        self.assertIn("tests_lm.test_v05_c224_history_cost_audit",run)
        self.assertIn("c223-v5f-request-freshness-56cfd6d212764ccf98e7789aa964de52",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))

    def test_29_actual_accepted_numeric_backend(self):
        row,checks,_,_=b.measure(b.base_module(),8)
        self.assertTrue(b.row_gate(row))
        self.assertTrue(all(c["max_abs_error"]<=b.TOLERANCE for c in checks))
        self.assertGreater(row["candidate_resident_estimate"]["unique_cpu_tensor_storage_bytes"],0)

    def test_30_actual_historical_regression_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(109,2466))
        self.assertEqual(b.regression_suite(root).countTestCases(),2465)


if __name__ == "__main__":
    unittest.main(verbosity=2)
