"""In-process request freshness for explicitly published immutable session states.

This is a correctness boundary, not a security sandbox or a general answer cache.
State updates must use publish(); in-place tensor mutation and concurrent access are outside scope.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from torch import nn
from . import memory_dispatch as live


@dataclass(frozen=True)
class RequestLease:
    owner: object
    generation: int
    request: live.QueryRequest


@dataclass(frozen=True)
class LeaseResult:
    status: str
    result: live.DispatchResult | None
    trace: tuple[str, ...]
    bank_reads: int = 0


class RequestSession:
    """Bind requests and validate them against this session's monotonic publication generation."""
    def __init__(self, state: object,
                 factory: Callable[[object, str], live.QueryRequest]) -> None:
        if not callable(factory):
            raise TypeError("factory must be callable")
        self._owner = object()
        self._generation = 0
        self._state = state
        self._factory = factory

    @property
    def generation(self) -> int:
        return self._generation

    def publish(self, state: object) -> None:
        # Every explicit publication invalidates old leases, including representation-only commits.
        # Publishing identical state is conservative invalidation, not an equality comparison.
        self._generation += 1
        self._state = state

    def bind(self, query: str) -> RequestLease:
        if not isinstance(query, str) or not query:
            raise ValueError("query must be nonempty text")
        generation = self._generation
        request = self._factory(self._state, query)
        if generation != self._generation:
            raise RuntimeError("state changed while binding request")
        if not isinstance(request, live.QueryRequest):
            raise TypeError("factory must return QueryRequest")
        return RequestLease(self._owner, generation, request)

    def execute(self, lease: RequestLease, coverage_model: nn.Module,
                selector_model: nn.Module, reader_model: nn.Module) -> LeaseResult:
        if not isinstance(lease, RequestLease):
            raise TypeError("lease must be RequestLease")
        if lease.owner is not self._owner:
            return LeaseResult("WRONG_SESSION", None, ("freshness",))
        if lease.generation != self._generation:
            return LeaseResult("STALE_REQUEST", None, ("freshness",))
        result = live.dispatch_query(lease.request, coverage_model, selector_model, reader_model)
        trace = ("freshness",) + result.trace
        if lease.generation != self._generation:
            # Synchronous callback publication must not publish an obsolete answer.
            return LeaseResult("CHANGED_DURING_DISPATCH", None, trace, result.bank_reads)
        return LeaseResult("CURRENT", result, trace, result.bank_reads)
