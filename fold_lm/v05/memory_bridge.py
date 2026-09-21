"""V5-F reference memory-operation bridge.

This module fixes only the semantic boundary between mutable relational memory operations and the
existing V5 EvidenceState provenance contract. It is deterministic and contains no learned
Writer/Reader, no FOLD-R numeric capsule, no retrieval model, and no language parser.

Observed ASSERT/REPLACE/RETRACT operations advance evidence revision. ASSUME/END_SCOPE modify only
memory revision. Hypotheses can be queried inside their live scope but are never exported as
authoritative EvidenceState observations.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .state import EvidenceRef, EvidenceState, Provenance, ProvenanceKind

SCHEMA = "fold-v5f-memory-bridge-v1"
GLOBAL_SCOPE = "global"


def _text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


class MemoryOpKind(str, Enum):
    ASSERT = "ASSERT"
    RETRACT = "RETRACT"
    REPLACE = "REPLACE"
    ASSUME = "ASSUME"
    END_SCOPE = "END_SCOPE"
    QUERY = "QUERY"


class MemoryReadStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    MISSING = "MISSING"
    RETRACTED = "RETRACTED"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    STALE_REVISION = "STALE_REVISION"


@dataclass(frozen=True)
class MemoryRecord:
    factor_id: str
    scope_id: str
    relation_key: str
    provenance: Provenance
    assumed: bool = False

    def __post_init__(self) -> None:
        _text(self.factor_id, "factor_id")
        _text(self.scope_id, "scope_id")
        _text(self.relation_key, "relation_key")
        if not isinstance(self.provenance, Provenance):
            raise TypeError("provenance must be Provenance")
        if type(self.assumed) is not bool:
            raise TypeError("assumed must be bool")
        expected = ProvenanceKind.HYPOTHESIS if self.assumed else ProvenanceKind.OBSERVED
        if self.provenance.kind is not expected:
            raise ValueError("record/provenance kind mismatch")


@dataclass(frozen=True)
class MemoryState:
    memory_revision: int = 0
    evidence_revision: int = 0
    evidence_time: int = 0
    records: tuple[MemoryRecord, ...] = ()
    tombstones: tuple[tuple[str, str], ...] = ()
    ended_scopes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("memory_revision", "evidence_revision", "evidence_time"):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")
        if self.evidence_revision > self.memory_revision:
            raise ValueError("evidence revision cannot exceed memory revision")
        if not isinstance(self.records, tuple):
            raise TypeError("records must be a tuple")
        if not isinstance(self.tombstones, tuple) or not isinstance(self.ended_scopes, tuple):
            raise TypeError("tombstones/ended_scopes must be tuples")

        keys: set[tuple[str, str]] = set()
        ended = set(self.ended_scopes)
        if len(ended) != len(self.ended_scopes):
            raise ValueError("ended scopes must be unique")
        for scope in ended:
            _text(scope, "ended scope")
            if scope == GLOBAL_SCOPE:
                raise ValueError("global scope cannot end")

        for record in self.records:
            if not isinstance(record, MemoryRecord):
                raise TypeError("records must contain MemoryRecord")
            key = (record.scope_id, record.factor_id)
            if key in keys:
                raise ValueError("duplicate live memory factor")
            if record.scope_id in ended:
                raise ValueError("ended scope cannot retain live records")
            keys.add(key)
            if record.provenance.revision > self.evidence_revision:
                raise ValueError("record provenance is from a future evidence revision")
            if record.provenance.evidence_time > self.evidence_time:
                raise ValueError("record provenance is from a future evidence time")

        tomb = set()
        for key in self.tombstones:
            if type(key) is not tuple or len(key) != 2:
                raise TypeError("tombstone key must be (scope_id, factor_id)")
            scope, factor = key
            _text(scope, "tombstone scope")
            _text(factor, "tombstone factor")
            if key in tomb or key in keys:
                raise ValueError("duplicate/live tombstone collision")
            if scope in ended:
                raise ValueError("ended scope cannot retain tombstones")
            tomb.add(key)


@dataclass(frozen=True)
class MemoryOp:
    kind: MemoryOpKind
    expected_memory_revision: int
    scope_id: str
    factor_id: str | None = None
    relation_key: str | None = None
    source_id: str | None = None
    evidence_time: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, MemoryOpKind):
            raise TypeError("kind must be MemoryOpKind")
        if type(self.expected_memory_revision) is not int or self.expected_memory_revision < 0:
            raise ValueError("expected_memory_revision must be nonnegative")
        _text(self.scope_id, "scope_id")

        needs_factor = self.kind is not MemoryOpKind.END_SCOPE
        if needs_factor:
            if self.factor_id is None:
                raise ValueError("factor_id required")
            _text(self.factor_id, "factor_id")
        elif self.factor_id is not None:
            raise ValueError("END_SCOPE does not take factor_id")

        if self.kind in (MemoryOpKind.ASSERT, MemoryOpKind.REPLACE, MemoryOpKind.ASSUME):
            if self.relation_key is None:
                raise ValueError("relation_key required")
            _text(self.relation_key, "relation_key")
        elif self.relation_key is not None:
            raise ValueError("relation_key not allowed for this operation")

        if self.kind in (MemoryOpKind.ASSERT, MemoryOpKind.REPLACE, MemoryOpKind.RETRACT):
            if self.source_id is None or self.evidence_time is None:
                raise ValueError("observed mutation requires source_id/evidence_time")
            _text(self.source_id, "source_id")
            if type(self.evidence_time) is not int or self.evidence_time < 0:
                raise ValueError("evidence_time must be nonnegative")
        elif self.source_id is not None or self.evidence_time is not None:
            raise ValueError("non-observed operation cannot carry source/evidence time")

        if self.kind is MemoryOpKind.ASSUME and self.scope_id == GLOBAL_SCOPE:
            raise ValueError("ASSUME requires an explicit non-global scope")
        if self.kind is MemoryOpKind.END_SCOPE and self.scope_id == GLOBAL_SCOPE:
            raise ValueError("global scope cannot end")


@dataclass(frozen=True)
class MemoryRead:
    status: MemoryReadStatus
    scope_id: str
    factor_id: str
    memory_revision: int
    evidence_revision: int
    relation_key: str | None = None
    provenance: Provenance | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, MemoryReadStatus):
            raise TypeError("status must be MemoryReadStatus")
        _text(self.scope_id, "scope_id")
        _text(self.factor_id, "factor_id")
        for name in ("memory_revision", "evidence_revision"):
            if type(getattr(self, name)) is not int or getattr(self, name) < 0:
                raise ValueError("read revisions must be nonnegative")
        if self.status is MemoryReadStatus.SUPPORTED:
            if self.relation_key is None or not isinstance(self.provenance, Provenance):
                raise ValueError("SUPPORTED read requires relation/provenance")
        elif self.relation_key is not None or self.provenance is not None:
            raise ValueError("non-supported read cannot expose relation/provenance")


@dataclass(frozen=True)
class MemoryBinding:
    evidence_id: str
    factor_id: str
    scope_id: str
    relation_key: str

    def __post_init__(self) -> None:
        for name in ("evidence_id", "factor_id", "scope_id", "relation_key"):
            _text(getattr(self, name), name)


@dataclass(frozen=True)
class MemoryExport:
    evidence: EvidenceState
    bindings: tuple[MemoryBinding, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.evidence, EvidenceState):
            raise TypeError("evidence must be EvidenceState")
        if not isinstance(self.bindings, tuple):
            raise TypeError("bindings must be a tuple")
        ids = tuple(x.evidence_id for x in self.bindings)
        if ids != tuple(x.evidence_id for x in self.evidence.observations):
            raise ValueError("binding/evidence identity mismatch")


def _records(state: MemoryState) -> dict[tuple[str, str], MemoryRecord]:
    return {(x.scope_id, x.factor_id):x for x in state.records}


def _sorted_records(records: dict[tuple[str, str], MemoryRecord]) -> tuple[MemoryRecord, ...]:
    return tuple(records[k] for k in sorted(records))


def _sorted_tombstones(values: set[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(values))


def _read(state: MemoryState, op: MemoryOp) -> MemoryRead:
    assert op.factor_id is not None
    if op.expected_memory_revision != state.memory_revision:
        return MemoryRead(
            MemoryReadStatus.STALE_REVISION,op.scope_id,op.factor_id,
            state.memory_revision,state.evidence_revision,
        )
    if op.scope_id in state.ended_scopes:
        return MemoryRead(
            MemoryReadStatus.OUT_OF_SCOPE,op.scope_id,op.factor_id,
            state.memory_revision,state.evidence_revision,
        )
    key=(op.scope_id,op.factor_id)
    if key in set(state.tombstones):
        return MemoryRead(
            MemoryReadStatus.RETRACTED,op.scope_id,op.factor_id,
            state.memory_revision,state.evidence_revision,
        )
    record=_records(state).get(key)
    if record is None:
        return MemoryRead(
            MemoryReadStatus.MISSING,op.scope_id,op.factor_id,
            state.memory_revision,state.evidence_revision,
        )
    return MemoryRead(
        MemoryReadStatus.SUPPORTED,op.scope_id,op.factor_id,
        state.memory_revision,state.evidence_revision,
        record.relation_key,record.provenance,
    )


def apply_memory_op(state: MemoryState, op: MemoryOp) -> tuple[MemoryState, MemoryRead | None]:
    """Apply one exact-revision operation.

    QUERY is non-mutating and reports STALE_REVISION instead of throwing. Mutations reject stale
    expected revisions so an old Writer decision cannot silently overwrite newer memory.
    """

    if not isinstance(state, MemoryState):
        raise TypeError("state must be MemoryState")
    if not isinstance(op, MemoryOp):
        raise TypeError("op must be MemoryOp")
    if op.kind is MemoryOpKind.QUERY:
        return state,_read(state,op)
    if op.expected_memory_revision != state.memory_revision:
        raise ValueError("STALE_REVISION")
    if op.scope_id in state.ended_scopes:
        raise ValueError("OUT_OF_SCOPE")

    records=_records(state)
    tombstones=set(state.tombstones)
    ended=set(state.ended_scopes)
    next_memory=state.memory_revision+1
    next_evidence_revision=state.evidence_revision
    next_evidence_time=state.evidence_time
    key=(op.scope_id,op.factor_id) if op.factor_id is not None else None

    if op.kind is MemoryOpKind.ASSERT:
        assert key is not None and op.relation_key is not None
        assert op.source_id is not None and op.evidence_time is not None
        if key in records or key in tombstones:
            raise ValueError("ASSERT requires a fresh factor_id in scope")
        if op.evidence_time < state.evidence_time:
            raise ValueError("evidence time cannot move backward")
        next_evidence_revision+=1
        next_evidence_time=op.evidence_time
        records[key]=MemoryRecord(
            op.factor_id,op.scope_id,op.relation_key,
            Provenance(op.source_id,ProvenanceKind.OBSERVED,next_evidence_revision,op.evidence_time),
            False,
        )

    elif op.kind is MemoryOpKind.REPLACE:
        assert key is not None and op.relation_key is not None
        assert op.source_id is not None and op.evidence_time is not None
        current=records.get(key)
        if current is None or current.assumed:
            raise ValueError("REPLACE requires a live observed factor")
        if op.evidence_time < state.evidence_time:
            raise ValueError("evidence time cannot move backward")
        next_evidence_revision+=1
        next_evidence_time=op.evidence_time
        records[key]=MemoryRecord(
            op.factor_id,op.scope_id,op.relation_key,
            Provenance(op.source_id,ProvenanceKind.OBSERVED,next_evidence_revision,op.evidence_time),
            False,
        )

    elif op.kind is MemoryOpKind.RETRACT:
        assert key is not None and op.source_id is not None and op.evidence_time is not None
        current=records.get(key)
        if current is None or current.assumed:
            raise ValueError("RETRACT requires a live observed factor")
        if op.evidence_time < state.evidence_time:
            raise ValueError("evidence time cannot move backward")
        next_evidence_revision+=1
        next_evidence_time=op.evidence_time
        records.pop(key)
        tombstones.add(key)

    elif op.kind is MemoryOpKind.ASSUME:
        assert key is not None and op.relation_key is not None
        if key in records or key in tombstones:
            raise ValueError("ASSUME requires a fresh factor_id in scope")
        records[key]=MemoryRecord(
            op.factor_id,op.scope_id,op.relation_key,
            Provenance(
                f"assumption:{op.scope_id}:{op.factor_id}",
                ProvenanceKind.HYPOTHESIS,
                state.evidence_revision,
                state.evidence_time,
            ),
            True,
        )

    elif op.kind is MemoryOpKind.END_SCOPE:
        if op.scope_id == GLOBAL_SCOPE or op.scope_id in ended:
            raise ValueError("scope cannot be ended")
        if any(r.scope_id == op.scope_id and not r.assumed for r in records.values()):
            raise ValueError("cannot END_SCOPE while observed records remain in scope")
        records={k:r for k,r in records.items() if r.scope_id != op.scope_id}
        tombstones={k for k in tombstones if k[0] != op.scope_id}
        ended.add(op.scope_id)

    else:
        raise AssertionError("unreachable")

    new_state=MemoryState(
        memory_revision=next_memory,
        evidence_revision=next_evidence_revision,
        evidence_time=next_evidence_time,
        records=_sorted_records(records),
        tombstones=_sorted_tombstones(tombstones),
        ended_scopes=tuple(sorted(ended)),
    )
    return new_state,None


def export_observed(state: MemoryState) -> MemoryExport:
    """Export only current observed records into the authoritative V5 EvidenceState."""

    if not isinstance(state, MemoryState):
        raise TypeError("state must be MemoryState")
    observed=[r for r in state.records if not r.assumed]
    observed.sort(key=lambda r:(r.scope_id,r.factor_id))
    refs=[]
    bindings=[]
    for record in observed:
        evidence_id=f"memory:{record.scope_id}:{record.factor_id}"
        refs.append(EvidenceRef(evidence_id,record.provenance))
        bindings.append(MemoryBinding(
            evidence_id,record.factor_id,record.scope_id,record.relation_key
        ))
    evidence=EvidenceState(
        evidence_time=state.evidence_time,
        revision=state.evidence_revision,
        observations=tuple(refs),
    )
    return MemoryExport(evidence,tuple(bindings))
