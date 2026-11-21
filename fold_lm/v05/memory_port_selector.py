"""Minimal learned Port Selector for V5-F memory routing.

The selector maps a query descriptor to a memory-port index. It does not inspect memory values,
Reader outputs, scope, provenance, or coverage state. Those stay outside this module so learned
port routing can be isolated experimentally.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class MemoryPortSelectorConfig:
    input_width: int = 4
    hidden_width: int = 8
    port_count: int = 2

    def __post_init__(self) -> None:
        for name in ("input_width", "hidden_width", "port_count"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


class MemoryPortSelector(nn.Module):
    """Choose a memory port from query features only."""

    def __init__(self, config: MemoryPortSelectorConfig) -> None:
        super().__init__()
        if not isinstance(config, MemoryPortSelectorConfig):
            raise TypeError("config must be MemoryPortSelectorConfig")
        self.config = config
        self.network = nn.Sequential(
            nn.Linear(config.input_width, config.hidden_width),
            nn.GELU(),
            nn.Linear(config.hidden_width, config.port_count),
        )

    def forward(self, query_features: torch.Tensor) -> torch.Tensor:
        if not isinstance(query_features, torch.Tensor):
            raise TypeError("query_features must be torch.Tensor")
        if query_features.ndim != 2 or query_features.shape[-1] != self.config.input_width:
            raise ValueError(
                f"query_features must have shape [batch, {self.config.input_width}]"
            )
        if not query_features.is_floating_point():
            raise TypeError("query_features must use a floating dtype")
        if not torch.isfinite(query_features).all():
            raise ValueError("query_features must be finite")
        return self.network(query_features)


def parameter_count(model: MemoryPortSelector) -> int:
    if not isinstance(model, MemoryPortSelector):
        raise TypeError("model must be MemoryPortSelector")
    return sum(parameter.numel() for parameter in model.parameters())
