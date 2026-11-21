"""Minimal learned semantic Writer for V5-F memory.

The Writer maps a structured observation descriptor to one of six factor+relation classes:
alpha{-1,0,+1} or beta{-1,0,+1}. Operation kind, revision and scope authorization remain outside
this module so Writer semantic/factor learning can be isolated.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class MemoryWriterConfig:
    input_width: int = 5
    hidden_width: int = 12
    relation_classes: int = 6

    def __post_init__(self) -> None:
        for name in ("input_width", "hidden_width", "relation_classes"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


class MemoryWriter(nn.Module):
    """Predict factor+relation class from observation features only."""

    def __init__(self, config: MemoryWriterConfig) -> None:
        super().__init__()
        if not isinstance(config, MemoryWriterConfig):
            raise TypeError("config must be MemoryWriterConfig")
        self.config = config
        self.network = nn.Sequential(
            nn.Linear(config.input_width, config.hidden_width),
            nn.GELU(),
            nn.Linear(config.hidden_width, config.relation_classes),
        )

    def forward(self, observation_features: torch.Tensor) -> torch.Tensor:
        if not isinstance(observation_features, torch.Tensor):
            raise TypeError("observation_features must be torch.Tensor")
        if (
            observation_features.ndim != 2
            or observation_features.shape[-1] != self.config.input_width
        ):
            raise ValueError(
                f"observation_features must have shape [batch, {self.config.input_width}]"
            )
        if not observation_features.is_floating_point():
            raise TypeError("observation_features must use a floating dtype")
        if not torch.isfinite(observation_features).all():
            raise ValueError("observation_features must be finite")
        return self.network(observation_features)


def parameter_count(model: MemoryWriter) -> int:
    if not isinstance(model, MemoryWriter):
        raise TypeError("model must be MemoryWriter")
    return sum(parameter.numel() for parameter in model.parameters())
