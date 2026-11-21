"""Visible-only projection from general structured-v2 tasks to the frozen legacy candidate input.

This module is a model-input boundary only. It never mutates or replaces the trusted runtime
TaskView, never reads scorer labels, and never writes evidence.

The frozen C181/C188 candidate was trained/evaluated on a four-fact, seven-node read-once family.
For bounded smaller expressions, project by appending observed TRUE architectural constants and
wrapping the original root with AND TRUE. Original fact indices remain unchanged. Any fact that is
not currently OBSERVED is represented as UNOBSERVED in the candidate projection; its original
status/provenance remains exclusively in the trusted structured-v2 runtime view.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json

from . import structured_task_input as v1
from . import structured_task_input_v2 as v2

SCHEMA = "fold-candidate-input-projection-v1"
DUMMY_PREFIX = "__FOLD_CONST_TRUE_"
DUMMY_REFERENCE_PREFIX = "candidate-projection:true:"


def _digest(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


@dataclass(frozen=True)
class CandidateProjection:
    schema: str
    source_v2_sha256: str
    packet: v1.PolicyInput
    original_fact_count: int
    projected_to_original: tuple[int, int, int, int]
    original_statuses: tuple[str, ...]
    projected_statuses: tuple[str, str, str, str]
    dummy_fact_indices: tuple[int, ...]
    normalized_status_changes: int

    def __post_init__(self):
        if self.schema != SCHEMA or type(self.source_v2_sha256) is not str or len(self.source_v2_sha256) != 64:
            raise ValueError("Explicit candidate projection identity required")
        if type(self.packet) is not v1.PolicyInput or self.packet.schema != v1.SCHEMA:
            raise TypeError("Canonical structured-v1 candidate packet required")
        if type(self.original_fact_count) is not int or not 1 <= self.original_fact_count <= 4:
            raise ValueError("Original fact count out of range")
        if (type(self.projected_to_original) is not tuple or len(self.projected_to_original) != 4
                or self.projected_to_original[:self.original_fact_count] != tuple(range(self.original_fact_count))
                or any(x != -1 for x in self.projected_to_original[self.original_fact_count:])):
            raise ValueError("Original fact-index mapping drift")
        if (type(self.original_statuses) is not tuple
                or len(self.original_statuses) != self.original_fact_count
                or any(x not in v1.STATUSES for x in self.original_statuses)):
            raise ValueError("Original status metadata drift")
        if (type(self.projected_statuses) is not tuple or len(self.projected_statuses) != 4
                or any(x not in ("UNOBSERVED", "OBSERVED") for x in self.projected_statuses)):
            raise ValueError("Projected status contract drift")
        want_dummy = tuple(range(self.original_fact_count, 4))
        if self.dummy_fact_indices != want_dummy:
            raise ValueError("Dummy fact-index contract drift")
        if (type(self.normalized_status_changes) is not int
                or not 0 <= self.normalized_status_changes <= self.original_fact_count):
            raise ValueError("Status-normalization count drift")


def source_digest(view: v2.TaskView) -> str:
    if type(view) is not v2.TaskView:
        raise TypeError("structured-v2 TaskView required")
    return _digest(asdict(v2.encode(view)))


def project(view: v2.TaskView) -> CandidateProjection:
    """Project visible state only; never consult or mutate hidden/scorer/runtime-external state."""
    if type(view) is not v2.TaskView:
        raise TypeError("structured-v2 TaskView required")
    base = view.base
    if not 1 <= len(base.facts) <= 4:
        raise ValueError("Bounded one-to-four fact task required")

    original_digest = source_digest(view)
    original_statuses = tuple(f.status for f in base.facts)

    facts = []
    normalized = 0
    for fact in base.facts:
        if fact.status == "OBSERVED":
            facts.append(fact)
        else:
            if fact.status != "UNOBSERVED":
                normalized += 1
            facts.append(v1.Fact(fact.fact_id, "UNOBSERVED", None, ()))

    nodes = list(base.nodes)
    root = len(nodes) - 1
    original_fact_count = len(facts)

    while len(facts) < 4:
        fact_index = len(facts)
        facts.append(v1.Fact(
            f"{DUMMY_PREFIX}{fact_index}",
            "OBSERVED",
            1,
            (f"{DUMMY_REFERENCE_PREFIX}{fact_index}",),
        ))
        dummy_leaf = len(nodes)
        nodes.append(v1.Node("FACT", fact=fact_index))
        wrapper = len(nodes)
        nodes.append(v1.Node("AND", left=root, right=dummy_leaf))
        root = wrapper

    if len(nodes) != 7 or len(facts) != 4:
        raise ValueError("Projection cannot satisfy legacy seven-node/four-fact contract")

    projected = v1.TaskView(
        base.request_id,
        base.scope_id,
        tuple(nodes),
        tuple(facts),
        base.resources,
        base.evidence_time,
        base.revision,
    )
    packet = v1.encode(projected)
    if v1.decode(packet) != projected:
        raise RuntimeError("Candidate projection roundtrip drift")

    result = CandidateProjection(
        SCHEMA,
        original_digest,
        packet,
        original_fact_count,
        tuple(range(original_fact_count)) + (-1,) * (4 - original_fact_count),
        original_statuses,
        tuple(f.status for f in projected.facts),
        tuple(range(original_fact_count, 4)),
        normalized,
    )
    if source_digest(view) != original_digest:
        raise RuntimeError("Trusted source view mutated during candidate projection")
    return result
