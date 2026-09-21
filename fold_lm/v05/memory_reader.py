"""Minimal learned Reader for an oracle-selected FOLD-R memory port.

The Reader intentionally does not choose a port and does not inspect memory status, scope, factor
identity, provenance, or query IDs. Those responsibilities stay outside this module so Reader
learning can be isolated experimentally.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class MemoryReaderConfig:
    input_width: int = 1
    hidden_width: int = 8
    answer_classes: int = 3

    def __post_init__(self) -> None:
        for name in ("input_width", "hidden_width", "answer_classes"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


class MemoryReader(nn.Module):
    """Decode already-selected numeric memory features into semantic answer classes."""

    def __init__(self, config: MemoryReaderConfig) -> None:
        super().__init__()
        if not isinstance(config, MemoryReaderConfig):
            raise TypeError("config must be MemoryReaderConfig")
        self.config = config
        self.network = nn.Sequential(
            nn.Linear(config.input_width, config.hidden_width),
            nn.GELU(),
            nn.Linear(config.hidden_width, config.answer_classes),
        )

    def forward(self, selected_features: torch.Tensor) -> torch.Tensor:
        if not isinstance(selected_features, torch.Tensor):
            raise TypeError("selected_features must be torch.Tensor")
        if selected_features.ndim != 2 or selected_features.shape[-1] != self.config.input_width:
            raise ValueError(
                f"selected_features must have shape [batch, {self.config.input_width}]"
            )
        if not selected_features.is_floating_point():
            raise TypeError("selected_features must use a floating dtype")
        if not torch.isfinite(selected_features).all():
            raise ValueError("selected_features must be finite")
        return self.network(selected_features)


def parameter_count(model: MemoryReader) -> int:
    if not isinstance(model, MemoryReader):
        raise TypeError("model must be MemoryReader")
    return sum(parameter.numel() for parameter in model.parameters())
