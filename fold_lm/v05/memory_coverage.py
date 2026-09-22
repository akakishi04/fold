"""Learned V5-F memory Coverage classifier over a bounded target-specific state summary.

Coverage is distinct from numeric safety. The learned classifier predicts one of:
SUPPORTED, HOT_REQUIRED, MISSING, OUT_OF_SCOPE.

NUMERIC_UNSAFE remains a deterministic numeric-kernel responsibility and is intentionally not a
Coverage class.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import torch
from torch import nn

from . import memory_bank as bankmod


class CoverageClass(IntEnum):
    SUPPORTED = 0
    HOT_REQUIRED = 1
    MISSING = 2
    OUT_OF_SCOPE = 3


@dataclass(frozen=True)
class MemoryCoverageConfig:
    input_width: int = 7
    hidden_width: int = 12
    class_count: int = 4

    def __post_init__(self) -> None:
        for name in ("input_width", "hidden_width", "class_count"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.class_count != len(CoverageClass):
            raise ValueError("class_count must match CoverageClass")


class MemoryCoverageClassifier(nn.Module):
    """Classify target-specific memory coverage from a bounded summary."""

    def __init__(self, config: MemoryCoverageConfig) -> None:
        super().__init__()
        if not isinstance(config, MemoryCoverageConfig):
            raise TypeError("config must be MemoryCoverageConfig")
        self.config = config
        self.network = nn.Sequential(
            nn.Linear(config.input_width, config.hidden_width),
            nn.GELU(),
            nn.Linear(config.hidden_width, config.class_count),
        )

    def forward(self, coverage_features: torch.Tensor) -> torch.Tensor:
        if not isinstance(coverage_features, torch.Tensor):
            raise TypeError("coverage_features must be torch.Tensor")
        if coverage_features.ndim != 2 or coverage_features.shape[-1] != self.config.input_width:
            raise ValueError(
                f"coverage_features must have shape [batch, {self.config.input_width}]"
            )
        if not coverage_features.is_floating_point():
            raise TypeError("coverage_features must use a floating dtype")
        if not torch.isfinite(coverage_features).all():
            raise ValueError("coverage_features must be finite")
        return self.network(coverage_features)


def target_summary(
    state: bankmod.ChunkedMemoryState,
    *,
    query_role: int,
    scope_id: str,
    factor_id: str,
    nuisance: tuple[float, float],
) -> tuple[torch.Tensor, CoverageClass]:
    """Return a bounded target-specific summary and deterministic teacher status."""

    if not isinstance(state, bankmod.ChunkedMemoryState):
        raise TypeError("state must be ChunkedMemoryState")
    if query_role not in (0, 1):
        raise ValueError("query_role must be 0 or 1")
    if not isinstance(scope_id, str) or not scope_id:
        raise ValueError("scope_id must be nonempty")
    if not isinstance(factor_id, str) or not factor_id:
        raise ValueError("factor_id must be nonempty")
    if (
        type(nuisance) is not tuple
        or len(nuisance) != 2
        or any(type(x) not in (int, float) for x in nuisance)
    ):
        raise ValueError("nuisance must be a pair of real values")

    key = (scope_id, factor_id)
    h2_keys = {(record.scope_id, record.factor_id) for record in state.h2.factors}
    hot_observed_keys = {
        (record.scope_id, record.factor_id)
        for record in state.hot_records
        if not record.assumed
    }
    scope_live = scope_id not in state.ended_scopes
    in_h2 = key in h2_keys
    in_hot = key in hot_observed_keys

    if not scope_live:
        status = CoverageClass.OUT_OF_SCOPE
    elif in_hot:
        status = CoverageClass.HOT_REQUIRED
    elif in_h2:
        status = CoverageClass.SUPPORTED
    else:
        status = CoverageClass.MISSING

    feature = torch.tensor(
        (
            1.0 if query_role == 0 else 0.0,
            1.0 if query_role == 1 else 0.0,
            1.0 if in_h2 else 0.0,
            1.0 if in_hot else 0.0,
            1.0 if scope_live else 0.0,
            float(nuisance[0]),
            float(nuisance[1]),
        ),
        dtype=torch.float32,
    )
    return feature, status


def parameter_count(model: MemoryCoverageClassifier) -> int:
    if not isinstance(model, MemoryCoverageClassifier):
        raise TypeError("model must be MemoryCoverageClassifier")
    return sum(parameter.numel() for parameter in model.parameters())
