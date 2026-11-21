from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
import zipfile

import torch
from fold_lm.v05_benchmarks import gate_f_c225_stateful_baseline as b


class Kind(str, Enum):
    ASSERT = "ASSERT"
    REPLACE = "REPLACE"


@dataclass(frozen=True)
class Provenance:
    source_id: str


@dataclass(frozen=True)
class Record:
    scope_id: str
    factor_id: str
    relation_key: str
    provenance: Provenance


@dataclass(frozen=True)
class State:
    memory_revision: int = 0
    records: tuple = ()


@dataclass(frozen=True)
class Op:
    kind: Kind
    expected_memory_revision: int
    scope_id: str
    factor_id: str
    relation_key: str
    source_id: str
    evidence_time: int


def apply(state, op):
    if state.memory_revision != op.expected_memory_revision:
        raise ValueError("stale fixture revision")
    table = {(r.scope_id, r.factor_id): r for r in state.records}
    table[(op.scope_id, op.factor_id)] = Record(op.scope_id, op.factor_id, op.relation_key,
                                               Provenance(op.source_id))
    return State(state.memory_revision + 1, tuple(table[k] for k in sorted(table))), None


@dataclass
class Bridge:
    base: torch.Tensor
    def full_reference(self, state):
        values = torch.zeros(2, dtype=torch.float64)
        for record in state.records:
            values[0 if record.factor_id == "alpha" else 1] = (int(record.relation_key[-1])-1)*3/17
        return SimpleNamespace(status=SimpleNamespace(value="SUPPORTED"), value=values)


@dataclass
class Bank:
    numeric: Bridge
    extra: torch.Tensor
    def read(self, state):
        return self.numeric.full_reference(state)
    def to_memory_state(self, state):
        return state


class Helpers:
    """Explicit synthetic fixture; not represented as the accepted numeric implementation."""
    blob = staticmethod(b.blob)
    @staticmethod
    def ledger(n):
        chunks = []
        for i in range(n):
            factor = "alpha" if i == 0 else "beta"
            semantic = 1 if i == 0 else (i-1)%3
            chunks.append(b.blob(dict(schema="fold-cost-event-v1", kind="ASSERT" if i < 2 else "REPLACE",
                factor=factor, scope="global" if factor == "alpha" else "project",
                relation=f"{factor}-class-{semantic}", source_id=f"cost:{i+1:08d}", time=i+1,
                text=f"{factor} の観測値を {semantic-1} と記録する。")))
        return b"".join(chunks)
    @staticmethod
    def events(raw, meter):
        meter["raw_bytes"] += len(raw)
        for line in raw.splitlines():
            meter["events"] += 1
            yield json.loads(line)
    @staticmethod
    def source_index(raw):
        result, offset = {}, 0
        for line in raw.splitlines(keepends=True):
            result[json.loads(line)["source_id"]] = (offset, offset+len(line))
            offset += len(line)
        return result
    @staticmethod
    def validate_index(raw, index):
        for source, (start,end) in index.items():
            if json.loads(raw[start:end])["source_id"] != source:
                raise ValueError("index mismatch")
    @staticmethod
    def memory_op(memory, state, event):
        return Op(Kind(event["kind"]), state.memory_revision, event["scope"], event["factor"],
                  event["relation"], event["source_id"], event["time"])
    @classmethod
    def build_candidate(cls, backend, raw):
        state, meter = b.build_symbolic(backend, raw, cls)
        return Bank(Bridge(torch.eye(2)), torch.eye(2)), state, meter
    @staticmethod
    def query_candidate(bank, state, meter):
        return bank.read(state)
    @staticmethod
    def canonical(value):
        if isinstance(value, bytes):
            return dict(raw_hex=value.hex())
        if isinstance(value, torch.Tensor):
            return dict(tensor=True, dtype=str(value.dtype), shape=list(value.shape), values=value.tolist())
        if is_dataclass(value):
            return dict(type=type(value).__name__, fields={f.name:Helpers.canonical(getattr(value,f.name)) for f in fields(value)})
        if isinstance(value, dict):
            return {k:Helpers.canonical(v) for k,v in value.items()}
        if isinstance(value, (tuple,list)):
            return [Helpers.canonical(v) for v in value]
        return value
    @classmethod
    def resident_estimate(cls, value):
        return dict(synthetic_estimate_bytes=len(cls.blob(cls.canonical(value))))
    @staticmethod
    def row_gate(row):
        return row.get("synthetic_parent_valid") is True


def backend():
    return SimpleNamespace(memory=SimpleNamespace(MemoryState=State, apply_memory_op=apply))


class C225Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row, cls.checks, cls.cf, cls.sf = b.measure(Helpers, backend(), 8)

    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()), b.MANIFEST_SHA)

    def test_02_all_raw_hashes_match_registered_parent(self):
        for n,h in zip(b.SIZES,b.RAW_HASHES,strict=True):
            self.assertEqual(b.hashlib.sha256(Helpers.ledger(n)).hexdigest(),h)

    def test_03_symbolic_build_consumes_each_event_once(self):
        raw=Helpers.ledger(32)
        state,meter=b.build_symbolic(backend(),raw,Helpers)
        self.assertEqual(meter,dict(raw_bytes=len(raw),events=32))
        self.assertEqual((state.memory_revision,len(state.records)),(32,2))

    def test_04_symbolic_latest_value_and_anchor(self):
        state,_=b.build_symbolic(backend(),Helpers.ledger(8),Helpers)
        by={r.factor_id:r.relation_key for r in state.records}
        self.assertEqual(by,{"alpha":"alpha-class-1","beta":"beta-class-0"})

    def test_05_current_provenance_retained(self):
        state,_=b.build_symbolic(backend(),Helpers.ledger(8),Helpers)
        self.assertEqual([r.provenance.source_id for r in state.records],["cost:00000001","cost:00000008"])

    def test_06_query_symbolic_has_no_raw_argument(self):
        self.assertEqual(tuple(inspect.signature(b.query_symbolic).parameters),("bridge","state"))
        source=inspect.getsource(b.query_symbolic)
        self.assertNotIn("events(",source)
        self.assertIn("bridge.full_reference(state)",source)

    def test_07_query_calls_full_solve_on_same_state(self):
        state=State();seen=[]
        bridge=SimpleNamespace(full_reference=lambda x:seen.append(x) or "result")
        self.assertEqual(b.query_symbolic(bridge,state),"result")
        self.assertIs(seen[0],state)

    def test_08_measurement_gate_passes_synthetic_backend(self):
        self.assertTrue(b.row_gate(self.row))
        self.assertEqual(len(self.checks),b.WARMUPS+b.REPEATS)

    def test_09_both_arms_have_zero_query_raw_replay(self):
        for key in ("candidate_query_trials","symbolic_query_trials"):
            self.assertTrue(all(t["raw_bytes"] == t["events"] == 0 for t in self.row[key]))

    def test_10_both_arms_retain_identical_raw_and_index(self):
        for name in ("evidence.ndjson","source-index.json"):
            self.assertEqual(self.cf[name],self.sf[name])

    def test_11_state_is_exported_in_both_arms(self):
        self.assertIn("state-and-bank.json",self.cf)
        self.assertIn("state-and-bridge.json",self.sf)
        self.assertIn("cost:00000008",self.sf["state-and-bridge.json"].decode())

    def test_12_canonical_inventory_is_exact(self):
        for files in (self.cf,self.sf):
            for name,item in b.inventory(files).items():
                self.assertEqual(item,dict(bytes=len(files[name]),sha256=b.hashlib.sha256(files[name]).hexdigest()))

    def test_13_omitted_baseline_index_rejected(self):
        row=deepcopy(self.row);del row["symbolic_files"]["source-index.json"]
        self.assertFalse(b.row_gate(row))

    def test_14_changed_raw_identity_rejected(self):
        row=deepcopy(self.row);row["raw_sha256"]="0"*64
        self.assertFalse(b.row_gate(row))

    def test_15_incorrect_total_bytes_rejected(self):
        row=deepcopy(self.row);row["symbolic_total_export_bytes"]-=1
        self.assertFalse(b.row_gate(row))

    def test_16_symbolic_state_mismatch_rejected(self):
        row=deepcopy(self.row);row["symbolic_state_equal"]=False
        self.assertFalse(b.row_gate(row))

    def test_17_provenance_mismatch_rejected(self):
        row=deepcopy(self.row);row["provenance_resolves"]=False
        self.assertFalse(b.row_gate(row))

    def test_18_numeric_quality_mismatch_rejected(self):
        row=deepcopy(self.row);row["quality_pass"]=False
        self.assertFalse(b.row_gate(row))

    def test_19_mutated_state_rejected(self):
        row=deepcopy(self.row);row["query_state_unchanged"]=False
        self.assertFalse(b.row_gate(row))

    def test_20_hidden_replay_rejected(self):
        row=deepcopy(self.row);row["symbolic_query_trials"][0]["events"]=8
        self.assertFalse(b.row_gate(row))

    def test_21_larger_storage_still_valid_audit(self):
        self.assertGreater(self.row["storage_delta_bytes"],0)
        self.assertTrue(b.row_gate(self.row))
        self.assertFalse(b.manifest()["superiority_required_for_pass"])

    def test_22_all_sizes_required(self):
        self.assertFalse(b.gate(b.summarize([self.row])))
        rows=[b.measure(Helpers,backend(),n)[0] for n in b.SIZES]
        self.assertTrue(b.gate(b.summarize(rows)))

    def test_23_timing_does_not_select_verdict(self):
        rows=[b.measure(Helpers,backend(),n)[0] for n in b.SIZES]
        for row in rows:
            row["candidate_query_median_ns"]=10**12
        self.assertTrue(b.gate(b.summarize(rows)))

    def test_24_parent_adapter_checks_order_and_raw_identity(self):
        rows=[dict(history_events=n,raw_sha256=h,synthetic_parent_valid=True)
              for n,h in zip(b.SIZES,b.RAW_HASHES,strict=True)]
        self.assertEqual(tuple(b.parent_measurement_adapter(rows,Helpers)),b.SIZES)
        with self.assertRaises(ValueError):
            b.parent_measurement_adapter(rows[::-1],Helpers)

    def test_25_parent_adapter_rejects_invalid_or_incomplete(self):
        rows=[dict(history_events=n,raw_sha256=h,synthetic_parent_valid=False)
              for n,h in zip(b.SIZES,b.RAW_HASHES,strict=True)]
        for bad in (rows,rows[:2],{}):
            with self.assertRaises(ValueError):
                b.parent_measurement_adapter(bad,Helpers)

    def test_26_archive_exact_bytes_and_members(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"x.zip"
            with zipfile.ZipFile(path,"w") as archive:
                for arm,files in (("candidate",self.cf),("symbolic",self.sf)):
                    for name,data in files.items():
                        archive.writestr("8/"+arm+"/"+name,data)
            b.verify_archive(path,[self.row])
            with zipfile.ZipFile(path,"a") as archive:
                archive.writestr("unexpected",b"x")
            with self.assertRaises(ValueError):
                b.verify_archive(path,[self.row])

    def test_27_archive_content_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"x.zip"
            with zipfile.ZipFile(path,"w") as archive:
                for arm,files in (("candidate",self.cf),("symbolic",self.sf)):
                    for name,data in files.items():
                        archive.writestr("8/"+arm+"/"+name,data+b"bad")
            with self.assertRaises(ValueError):
                b.verify_archive(path,[self.row])

    def test_28_no_production_or_training_claim(self):
        m=b.manifest()
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_f_candidate"])
        self.assertEqual(m["learned_model_forward_calls"],0)

    def test_29_runner_and_launcher(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c225.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c225.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2497",run)
        self.assertIn("tests_lm.test_v05_c225_stateful_baseline",run)
        self.assertIn("c224-v5f-history-cost-audit-7d510ad2c98647bfbabeabe91de81381",launch)
        self.assertIn("RUNNER_PARSE_ERROR",launch)
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))

    def test_30_parent_artifact_and_candidate_parity_are_used(self):
        source=inspect.getsource(b.run)
        self.assertIn("parent_measurement_adapter",source)
        self.assertIn('row["candidate_files"] == parent_rows[size]["candidate_files"]',source)
        self.assertIn("verify_archive",source)

    def test_31_actual_accepted_backend(self):
        p=b.parent_module()
        row,checks,_,_=b.measure(p,p.base_module(),8)
        self.assertTrue(b.row_gate(row))
        self.assertTrue(all(c["max_abs_error"] <= b.TOLERANCE for c in checks))

    def test_32_actual_historical_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(110,2498))
        self.assertEqual(b.regression_suite(root).countTestCases(),2497)


if __name__ == "__main__":
    unittest.main(verbosity=2)
