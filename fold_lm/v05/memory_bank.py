"""Deterministic V5-F H1 hot-memory / H2 response-capsule bank reference.

The bank stores current live factor descriptors plus an aggregate fixed-port response-capsule
update. It stores no operation history. New observed ASSERTs enter H1 and yield HOT_REQUIRED until
chunk commit. Supported REPLACE/RETRACT of already committed factors update H2 directly from the
current protected-factor descriptor. ASSUME remains H1 hypothesis state and never enters H2.

This is a reference state machine only: no learned Writer/Reader/Port Selector or language parser.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum

import torch

from . import memory_bridge as memory
from . import memory_capsule_bridge as numeric


class BankReadStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    HOT_REQUIRED = "HOT_REQUIRED"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    NUMERIC_UNSAFE = "NUMERIC_UNSAFE"


class CommitStatus(str, Enum):
    COMMITTED = "COMMITTED"
    NOOP = "NOOP"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    NUMERIC_UNSAFE = "NUMERIC_UNSAFE"


@dataclass(frozen=True)
class H2CapsuleState:
    storage_epoch: int
    reflected_evidence_revision: int
    reflected_evidence_time: int
    W: torch.Tensor
    b: torch.Tensor
    factors: tuple[memory.MemoryRecord, ...] = ()

    def __post_init__(self) -> None:
        for name in ("storage_epoch","reflected_evidence_revision","reflected_evidence_time"):
            value=getattr(self,name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be nonnegative integer")
        W=torch.as_tensor(self.W,dtype=torch.float64,device="cpu").detach().clone()
        b=torch.as_tensor(self.b,dtype=torch.float64,device="cpu").detach().clone()
        if W.ndim!=2 or W.shape[0]!=W.shape[1] or b.shape!=(W.shape[0],):
            raise ValueError("H2 W/b shape mismatch")
        if not torch.isfinite(W).all() or not torch.isfinite(b).all():
            raise ValueError("H2 W/b must be finite")
        if not torch.allclose(W,W.mT,rtol=0.0,atol=0.0):
            raise ValueError("H2 W must be symmetric")
        keys=set()
        for record in self.factors:
            if not isinstance(record,memory.MemoryRecord) or record.assumed:
                raise ValueError("H2 factors must be observed MemoryRecord values")
            key=(record.scope_id,record.factor_id)
            if key in keys:
                raise ValueError("duplicate H2 factor")
            keys.add(key)
        object.__setattr__(self,"W",W)
        object.__setattr__(self,"b",b)


@dataclass(frozen=True)
class ChunkedMemoryState:
    memory_revision: int
    evidence_revision: int
    evidence_time: int
    h2: H2CapsuleState
    hot_records: tuple[memory.MemoryRecord, ...] = ()
    tombstones: tuple[tuple[str,str], ...] = ()
    ended_scopes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("memory_revision","evidence_revision","evidence_time"):
            value=getattr(self,name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be nonnegative integer")
        if not isinstance(self.h2,H2CapsuleState):
            raise TypeError("h2 must be H2CapsuleState")
        if self.h2.reflected_evidence_revision > self.evidence_revision:
            raise ValueError("H2 cannot reflect a future evidence revision")
        combined=tuple(sorted(
            self.h2.factors+self.hot_records,
            key=lambda r:(r.scope_id,r.factor_id),
        ))
        memory.MemoryState(
            memory_revision=self.memory_revision,
            evidence_revision=self.evidence_revision,
            evidence_time=self.evidence_time,
            records=combined,
            tombstones=self.tombstones,
            ended_scopes=self.ended_scopes,
        )
        h2_keys={(r.scope_id,r.factor_id) for r in self.h2.factors}
        hot_keys={(r.scope_id,r.factor_id) for r in self.hot_records}
        if h2_keys & hot_keys:
            raise ValueError("factor cannot exist in H1 and H2 simultaneously")


@dataclass(frozen=True)
class BankRead:
    status: BankReadStatus
    memory_revision: int
    evidence_revision: int
    storage_epoch: int
    h2_factor_ids: tuple[str, ...]
    hot_observed_factor_ids: tuple[str, ...]
    hot_hypothesis_factor_ids: tuple[str, ...]
    value: torch.Tensor | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status,BankReadStatus):
            raise TypeError("status must be BankReadStatus")
        for name in ("memory_revision","evidence_revision","storage_epoch"):
            if type(getattr(self,name)) is not int or getattr(self,name) < 0:
                raise ValueError("read revisions must be nonnegative")
        supported=self.status in (BankReadStatus.SUPPORTED,BankReadStatus.HOT_REQUIRED)
        if supported:
            if self.value is None:
                raise ValueError("supported/HOT_REQUIRED read needs value")
            value=torch.as_tensor(self.value,dtype=torch.float64,device="cpu").detach().clone()
            if value.ndim!=1 or not torch.isfinite(value).all():
                raise ValueError("read value must be finite rank-1")
            object.__setattr__(self,"value",value)
        elif self.value is not None:
            raise ValueError("non-supported read cannot expose value")


class ChunkedMemoryBank:
    def __init__(self, numeric_bridge: numeric.MemoryCapsuleBridge):
        if not isinstance(numeric_bridge,numeric.MemoryCapsuleBridge):
            raise TypeError("numeric_bridge must be MemoryCapsuleBridge")
        self.numeric=numeric_bridge
        self.rank=numeric_bridge.update_rank

    def initial_state(self) -> ChunkedMemoryState:
        return ChunkedMemoryState(
            0,0,0,
            H2CapsuleState(
                0,0,0,
                torch.zeros((self.rank,self.rank),dtype=torch.float64),
                torch.zeros((self.rank,),dtype=torch.float64),
                (),
            ),
        )

    @staticmethod
    def operation_history_entries(state: ChunkedMemoryState) -> int:
        if not isinstance(state,ChunkedMemoryState):
            raise TypeError("state must be ChunkedMemoryState")
        names={f.name for f in fields(state)}|{f.name for f in fields(state.h2)}
        if "history" in names or "operations" in names or "operation_history" in names:
            raise ValueError("hidden operation history field is forbidden")
        return 0

    def to_memory_state(self,state: ChunkedMemoryState) -> memory.MemoryState:
        if not isinstance(state,ChunkedMemoryState):
            raise TypeError("state must be ChunkedMemoryState")
        records=tuple(sorted(
            state.h2.factors+state.hot_records,
            key=lambda r:(r.scope_id,r.factor_id),
        ))
        return memory.MemoryState(
            state.memory_revision,state.evidence_revision,state.evidence_time,
            records,state.tombstones,state.ended_scopes,
        )

    def _contribution(self,relation_key):
        return self.numeric._registry.get(relation_key)

    def _aggregate_records(self,records):
        W=torch.zeros((self.rank,self.rank),dtype=torch.float64)
        b=torch.zeros((self.rank,),dtype=torch.float64)
        factor_ids=[]
        for record in records:
            if record.assumed:
                continue
            contribution=self._contribution(record.relation_key)
            if contribution is None:
                return BankReadStatus.OUT_OF_SCOPE,None,None,tuple(factor_ids)
            W=W+contribution.W
            b=b+contribution.b
            factor_ids.append(record.factor_id)
        return BankReadStatus.SUPPORTED,W,b,tuple(factor_ids)

    def _read_parts(self,state):
        hot_observed=tuple(r for r in state.hot_records if not r.assumed)
        hot_hypothesis=tuple(r for r in state.hot_records if r.assumed)
        status,hot_W,hot_b,hot_ids=self._aggregate_records(hot_observed)
        h2_ids=tuple(r.factor_id for r in state.h2.factors)
        hyp_ids=tuple(r.factor_id for r in hot_hypothesis)
        if status is BankReadStatus.OUT_OF_SCOPE:
            return status,None,None,h2_ids,hot_ids,hyp_ids
        assert hot_W is not None and hot_b is not None
        return (
            BankReadStatus.HOT_REQUIRED if hot_observed else BankReadStatus.SUPPORTED,
            state.h2.W+hot_W,state.h2.b+hot_b,h2_ids,hot_ids,hyp_ids,
        )

    def read(self,state: ChunkedMemoryState) -> BankRead:
        status,W,b,h2_ids,hot_ids,hyp_ids=self._read_parts(state)
        if status is BankReadStatus.OUT_OF_SCOPE:
            return BankRead(status,state.memory_revision,state.evidence_revision,
                            state.h2.storage_epoch,h2_ids,hot_ids,hyp_ids,None)
        assert W is not None and b is not None
        try:
            value=self.numeric._capsule.response(W,b,check=True)
        except (ValueError,RuntimeError):
            return BankRead(BankReadStatus.NUMERIC_UNSAFE,state.memory_revision,
                            state.evidence_revision,state.h2.storage_epoch,
                            h2_ids,hot_ids,hyp_ids,None)
        return BankRead(status,state.memory_revision,state.evidence_revision,
                        state.h2.storage_epoch,h2_ids,hot_ids,hyp_ids,value)

    def full_reference(self,state: ChunkedMemoryState) -> BankRead:
        status,W,b,h2_ids,hot_ids,hyp_ids=self._read_parts(state)
        if status is BankReadStatus.OUT_OF_SCOPE:
            return BankRead(status,state.memory_revision,state.evidence_revision,
                            state.h2.storage_epoch,h2_ids,hot_ids,hyp_ids,None)
        assert W is not None and b is not None
        J=self.numeric._J+self.numeric._U@W@self.numeric._U.mT
        eta=self.numeric._eta+self.numeric._U@b
        try:
            torch.linalg.cholesky(J)
            value=self.numeric._Q@torch.linalg.solve(J,eta)
        except (ValueError,RuntimeError):
            return BankRead(BankReadStatus.NUMERIC_UNSAFE,state.memory_revision,
                            state.evidence_revision,state.h2.storage_epoch,
                            h2_ids,hot_ids,hyp_ids,None)
        return BankRead(status,state.memory_revision,state.evidence_revision,
                        state.h2.storage_epoch,h2_ids,hot_ids,hyp_ids,value)

    def _h2_from_factors(self,state,factors,*,storage_epoch=None,reflect_current=False):
        ordered=tuple(sorted(factors,key=lambda r:(r.scope_id,r.factor_id)))
        status,W,b,_=self._aggregate_records(ordered)
        if status is BankReadStatus.OUT_OF_SCOPE:
            raise ValueError("OUT_OF_SCOPE")
        assert W is not None and b is not None
        reflected_revision=(
            state.evidence_revision if reflect_current
            else state.h2.reflected_evidence_revision
        )
        reflected_time=(
            state.evidence_time if reflect_current
            else state.h2.reflected_evidence_time
        )
        return H2CapsuleState(
            state.h2.storage_epoch if storage_epoch is None else storage_epoch,
            reflected_revision,reflected_time,W,b,ordered,
        )

    def apply(self,state: ChunkedMemoryState,op: memory.MemoryOp):
        """Apply accepted C213 semantics, preserving H2 placement for committed factors."""

        combined=self.to_memory_state(state)
        updated,read=memory.apply_memory_op(combined,op)
        if read is not None:
            return state,read

        old_h2_keys={(r.scope_id,r.factor_id) for r in state.h2.factors}
        new_records={(r.scope_id,r.factor_id):r for r in updated.records}
        h2_records=[]
        hot_records=[]
        for key,record in new_records.items():
            if key in old_h2_keys and not record.assumed and self._contribution(record.relation_key) is not None:
                h2_records.append(record)
            else:
                hot_records.append(record)

        # Rebuild H2 only from the current protected-factor index; no operation replay.
        new_h2=self._h2_from_factors(state,h2_records)
        hot_observed=tuple(r for r in hot_records if not r.assumed)
        if not hot_observed:
            # If H1 has no observed delta, H2's numeric state reflects current observed evidence.
            new_h2=H2CapsuleState(
                new_h2.storage_epoch,updated.evidence_revision,updated.evidence_time,
                new_h2.W,new_h2.b,new_h2.factors,
            )

        return ChunkedMemoryState(
            updated.memory_revision,updated.evidence_revision,updated.evidence_time,
            new_h2,tuple(sorted(hot_records,key=lambda r:(r.scope_id,r.factor_id))),
            updated.tombstones,updated.ended_scopes,
        ),None

    def commit(self,state: ChunkedMemoryState):
        """Move supported H1 observed records into H2 without changing semantic clocks."""

        if not isinstance(state,ChunkedMemoryState):
            raise TypeError("state must be ChunkedMemoryState")
        hot_observed=tuple(r for r in state.hot_records if not r.assumed)
        if not hot_observed:
            return state,CommitStatus.NOOP

        combined_factors=state.h2.factors+hot_observed
        status,W,b,_=self._aggregate_records(combined_factors)
        if status is BankReadStatus.OUT_OF_SCOPE:
            return state,CommitStatus.OUT_OF_SCOPE
        assert W is not None and b is not None
        try:
            self.numeric._capsule.response(W,b,check=True)
        except (ValueError,RuntimeError):
            return state,CommitStatus.NUMERIC_UNSAFE

        hypotheses=tuple(r for r in state.hot_records if r.assumed)
        h2=H2CapsuleState(
            state.h2.storage_epoch+1,
            state.evidence_revision,
            state.evidence_time,
            W,b,
            tuple(sorted(combined_factors,key=lambda r:(r.scope_id,r.factor_id))),
        )
        committed=ChunkedMemoryState(
            state.memory_revision,state.evidence_revision,state.evidence_time,
            h2,hypotheses,state.tombstones,state.ended_scopes,
        )
        return committed,CommitStatus.COMMITTED
