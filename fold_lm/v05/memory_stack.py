"""Deterministic glue for composing learned V5-F memory components.

This module does not contain learned parameters. It maps a learned Coverage class to the runtime
decision of whether the selected memory port may be read, while preserving distinct suppression
reasons for MISSING and OUT_OF_SCOPE.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import torch

from .memory_coverage import CoverageClass


class StackAction(str, Enum):
    READ = "READ"
    SUPPRESS_MISSING = "SUPPRESS_MISSING"
    SUPPRESS_OUT_OF_SCOPE = "SUPPRESS_OUT_OF_SCOPE"


@dataclass(frozen=True)
class StackGate:
    coverage: CoverageClass
    action: StackAction

    @property
    def readable(self) -> bool:
        return self.action is StackAction.READ


def gate_for_coverage(value: int | CoverageClass) -> StackGate:
    try:
        status = CoverageClass(int(value))
    except (TypeError, ValueError):
        raise ValueError("unknown coverage class") from None

    if status in (CoverageClass.SUPPORTED, CoverageClass.HOT_REQUIRED):
        action = StackAction.READ
    elif status is CoverageClass.MISSING:
        action = StackAction.SUPPRESS_MISSING
    elif status is CoverageClass.OUT_OF_SCOPE:
        action = StackAction.SUPPRESS_OUT_OF_SCOPE
    else:
        raise AssertionError("unreachable")
    return StackGate(status, action)


def selected_scalar(readout: torch.Tensor, port: int) -> torch.Tensor:
    """Return one selected scalar as shape [1,1] for the learned Reader."""

    if not isinstance(readout, torch.Tensor):
        raise TypeError("readout must be torch.Tensor")
    if readout.ndim != 1 or not torch.isfinite(readout).all():
        raise ValueError("readout must be finite rank-1")
    if type(port) is not int or not 0 <= port < readout.numel():
        raise ValueError("port out of range")
    return readout[port].reshape(1, 1).to(torch.float32)
