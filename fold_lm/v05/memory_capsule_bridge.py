"""V5-F semantic-memory to fixed-port FOLD-R response-capsule bridge.

This is a deterministic reference adapter. It consumes accepted MemoryState records and a
predeclared relation->port-update registry. Only current OBSERVED records contribute to the numeric
capsule; hypotheses are deliberately excluded. Unknown observed relations are OUT_OF_SCOPE.
Numerically unsafe accumulated port updates are NUMERIC_UNSAFE.

No Writer/Reader/Port Selector is learned here, and this module performs no natural-language parsing.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import torch

from fold_lm.capsule import compile_capsule
from . import memory_bridge as memory


class CapsuleReadStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    NUMERIC_UNSAFE = "NUMERIC_UNSAFE"


@dataclass(frozen=True)
class PortContribution:
    relation_key: str
    W: torch.Tensor
    b: torch.Tensor

    def __post_init__(self) -> None:
        if not isinstance(self.relation_key, str) or not self.relation_key.strip():
            raise ValueError("relation_key must be nonempty")
        W = torch.as_tensor(self.W, dtype=torch.float64, device="cpu").detach().clone()
        b = torch.as_tensor(self.b, dtype=torch.float64, device="cpu").detach().clone()
        if W.ndim != 2 or W.shape[0] != W.shape[1] or b.shape != (W.shape[0],):
            raise ValueError("port contribution shape mismatch")
        if not torch.isfinite(W).all() or not torch.isfinite(b).all():
            raise ValueError("port contribution must be finite")
        if not torch.allclose(W, W.mT, rtol=0.0, atol=0.0):
            raise ValueError("port contribution W must be symmetric")
        object.__setattr__(self, "W", W)
        object.__setattr__(self, "b", b)


@dataclass(frozen=True)
class CapsuleRead:
    status: CapsuleReadStatus
    memory_revision: int
    evidence_revision: int
    observed_factor_ids: tuple[str, ...]
    value: torch.Tensor | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, CapsuleReadStatus):
            raise TypeError("status must be CapsuleReadStatus")
        if type(self.memory_revision) is not int or self.memory_revision < 0:
            raise ValueError("memory_revision must be nonnegative")
        if type(self.evidence_revision) is not int or self.evidence_revision < 0:
            raise ValueError("evidence_revision must be nonnegative")
        if not isinstance(self.observed_factor_ids, tuple):
            raise TypeError("observed_factor_ids must be tuple")
        if self.status is CapsuleReadStatus.SUPPORTED:
            if self.value is None:
                raise ValueError("SUPPORTED read requires value")
            value = torch.as_tensor(self.value, dtype=torch.float64, device="cpu").detach().clone()
            if value.ndim != 1 or not torch.isfinite(value).all():
                raise ValueError("supported value must be finite rank-1")
            object.__setattr__(self, "value", value)
        elif self.value is not None:
            raise ValueError("non-supported read cannot expose value")


class MemoryCapsuleBridge:
    """Fixed numeric capsule plus explicit relation->port update capability contract."""

    def __init__(self, J, eta, Q, U, contributions):
        J = torch.as_tensor(J, dtype=torch.float64, device="cpu").detach().clone()
        eta = torch.as_tensor(eta, dtype=torch.float64, device="cpu").detach().clone()
        Q = torch.as_tensor(Q, dtype=torch.float64, device="cpu").detach().clone()
        U = torch.as_tensor(U, dtype=torch.float64, device="cpu").detach().clone()
        if J.ndim != 2 or eta.ndim != 1 or Q.ndim != 2 or U.ndim != 2:
            raise ValueError("base tensor ranks invalid")
        n = J.shape[-1]
        if J.shape != (n, n) or eta.shape != (n,) or Q.shape[-1] != n or U.shape[0] != n:
            raise ValueError("base tensor dimensions invalid")
        if not all(torch.isfinite(x).all() for x in (J, eta, Q, U)):
            raise ValueError("base tensors must be finite")
        if J.dtype is not torch.float64:
            raise TypeError("float64 reference required")
        supplied = tuple(contributions)
        if not supplied or any(not isinstance(x, PortContribution) for x in supplied):
            raise ValueError("nonempty PortContribution registry required")
        registry = {x.relation_key:x for x in supplied}
        if len(registry) != len(supplied):
            raise ValueError("relation keys must be unique")
        rank = U.shape[1]
        if any(x.W.shape != (rank, rank) or x.b.shape != (rank,) for x in supplied):
            raise ValueError("contribution rank does not match U")
        capsule = compile_capsule(J, eta, Q, U, check=True)

        self._J = J
        self._eta = eta
        self._Q = Q
        self._U = U
        self._registry = registry
        self._capsule = capsule
        self.variable_dim = int(n)
        self.update_rank = int(rank)
        self.readout_dim = int(Q.shape[0])
        self.relation_keys = tuple(sorted(registry))

    def _aggregate(self, state: memory.MemoryState):
        if not isinstance(state, memory.MemoryState):
            raise TypeError("state must be MemoryState")
        W = torch.zeros((self.update_rank, self.update_rank), dtype=torch.float64)
        b = torch.zeros((self.update_rank,), dtype=torch.float64)
        factors = []
        for record in state.records:
            if record.assumed:
                continue
            contribution = self._registry.get(record.relation_key)
            if contribution is None:
                return CapsuleReadStatus.OUT_OF_SCOPE, None, None, tuple(factors)
            W = W + contribution.W
            b = b + contribution.b
            factors.append(record.factor_id)
        return CapsuleReadStatus.SUPPORTED, W, b, tuple(factors)

    def read(self, state: memory.MemoryState) -> CapsuleRead:
        status, W, b, factors = self._aggregate(state)
        if status is CapsuleReadStatus.OUT_OF_SCOPE:
            return CapsuleRead(
                status,state.memory_revision,state.evidence_revision,factors,None
            )
        assert W is not None and b is not None
        try:
            value = self._capsule.response(W,b,check=True)
        except (ValueError, RuntimeError):
            return CapsuleRead(
                CapsuleReadStatus.NUMERIC_UNSAFE,
                state.memory_revision,state.evidence_revision,factors,None,
            )
        return CapsuleRead(
            CapsuleReadStatus.SUPPORTED,
            state.memory_revision,state.evidence_revision,factors,value,
        )

    def full_reference(self, state: memory.MemoryState) -> CapsuleRead:
        """Independent full-system solve for validation; same capability contract."""

        status, W, b, factors = self._aggregate(state)
        if status is CapsuleReadStatus.OUT_OF_SCOPE:
            return CapsuleRead(
                status,state.memory_revision,state.evidence_revision,factors,None
            )
        assert W is not None and b is not None
        J = self._J + self._U @ W @ self._U.mT
        eta = self._eta + self._U @ b
        try:
            torch.linalg.cholesky(J)
            value = self._Q @ torch.linalg.solve(J,eta)
        except (RuntimeError, ValueError):
            return CapsuleRead(
                CapsuleReadStatus.NUMERIC_UNSAFE,
                state.memory_revision,state.evidence_revision,factors,None,
            )
        return CapsuleRead(
            CapsuleReadStatus.SUPPORTED,
            state.memory_revision,state.evidence_revision,factors,value,
        )
