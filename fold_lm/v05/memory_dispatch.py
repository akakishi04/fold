"""Coverage-first dispatch. Expected labels and precomputed answers are not inputs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import torch
from torch import nn


@dataclass(frozen=True)
class ReadOutcome:
    status: str
    selected: torch.Tensor | None = None
    bank_reads: int = 0

    def __post_init__(self) -> None:
        if self.status not in ("READABLE", "MISSING", "OUT_OF_SCOPE", "NUMERIC_UNSAFE"):
            raise ValueError("unknown provider status")
        if type(self.bank_reads) is not int or self.bank_reads not in (0, 1):
            raise ValueError("bank_reads must be zero or one")
        if self.status == "READABLE":
            if not isinstance(self.selected, torch.Tensor):
                raise TypeError("readable provider needs a tensor")
            if self.selected.shape != (1, 1) or not self.selected.is_floating_point():
                raise ValueError("selected feature must be floating [1,1]")
            if not bool(torch.isfinite(self.selected).all()):
                raise ValueError("nonfinite selected feature")
        elif self.selected is not None:
            raise ValueError("blocked provider cannot expose a value")


@dataclass(frozen=True)
class QueryRequest:
    coverage_features: torch.Tensor
    query_features: torch.Tensor
    provider: Callable[[int], ReadOutcome]


@dataclass(frozen=True)
class DispatchResult:
    coverage: int
    port: int | None
    answer: int | None
    action: str
    trace: tuple[str, ...]
    bank_reads: int = 0


def _predict(model: nn.Module, x: torch.Tensor, width: int, classes: int) -> int:
    if not isinstance(x, torch.Tensor):
        raise TypeError("features must be a tensor")
    if x.shape != (1, width) or not x.is_floating_point():
        raise ValueError("invalid feature shape or dtype")
    if not bool(torch.isfinite(x).all()):
        raise ValueError("nonfinite features")
    with torch.no_grad():
        logits = model(x)
    if not isinstance(logits, torch.Tensor) or logits.shape != (1, classes):
        raise ValueError("invalid model output shape")
    if not logits.is_floating_point() or not bool(torch.isfinite(logits).all()):
        raise ValueError("invalid model output values")
    return int(logits.argmax(dim=-1).item())


def dispatch_query(request: QueryRequest, coverage_model: nn.Module,
                   selector_model: nn.Module, reader_model: nn.Module) -> DispatchResult:
    """Call downstream components only after the learned Coverage result permits it."""
    if not isinstance(request, QueryRequest):
        raise TypeError("request must be QueryRequest")
    if not callable(request.provider):
        raise TypeError("provider must be callable")
    trace = ["coverage"]
    predicted = _predict(coverage_model, request.coverage_features, 7, 4)
    if predicted in (2, 3):
        action = "SUPPRESS_MISSING" if predicted == 2 else "SUPPRESS_OUT_OF_SCOPE"
        return DispatchResult(predicted, None, None, action, tuple(trace))
    trace.append("selector")
    port = _predict(selector_model, request.query_features, 4, 2)
    trace.append("provider")
    supplied = request.provider(port)
    if not isinstance(supplied, ReadOutcome):
        raise TypeError("provider must return ReadOutcome")
    if supplied.status != "READABLE":
        return DispatchResult(predicted, port, None, "BLOCKED_" + supplied.status,
                              tuple(trace), supplied.bank_reads)
    trace.append("reader")
    answer = _predict(reader_model, supplied.selected, 1, 3)
    return DispatchResult(predicted, port, answer, "ANSWER", tuple(trace), supplied.bank_reads)
