"""Opt-in structured task input v2 with per-fact acquisition-channel metadata.

v2 is deliberately additive. The first 72 numeric features are exactly the canonical
structured-task-input-v1 packet. The final 12 numeric features are four fact slots x the
three registered acquisition channels RETRIEVE / OBSERVE / ASK_USER.

Channel eligibility describes which acquisition mechanism is semantically applicable to
a fact. It does not grant runtime authority, imply current provider availability, consume
budget, reveal a hidden value, or select an action. Runtime availability/permission remains
in the v1 resource coordinates and is enforced independently by structured_action_runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

from . import structured_task_input as v1

SCHEMA = "fold-structured-task-input-v2"
CHANNELS = v1.TOOLS
CHANNEL_WIDTH = len(CHANNELS)
FEATURE_WIDTH = v1.FEATURE_WIDTH + v1.MAX_FACTS * CHANNEL_WIDTH
T = TypeVar("T")


def _tuple(value):
    if type(value) is not tuple:
        raise TypeError("Immutable tuple required")


@dataclass(frozen=True)
class FactChannels:
    eligible: tuple[bool, bool, bool]

    def __post_init__(self):
        _tuple(self.eligible)
        if len(self.eligible) != CHANNEL_WIDTH or any(type(x) is not bool for x in self.eligible):
            raise ValueError("Exactly three Boolean acquisition-channel flags required")


@dataclass(frozen=True)
class TaskView:
    base: v1.TaskView
    channels: tuple[FactChannels, ...]

    def __post_init__(self):
        if type(self.base) is not v1.TaskView:
            raise TypeError("Canonical structured-v1 TaskView required")
        _tuple(self.channels)
        if len(self.channels) != len(self.base.facts):
            raise ValueError("One channel descriptor per fact required")
        if any(type(x) is not FactChannels for x in self.channels):
            raise TypeError("Typed FactChannels required")


@dataclass(frozen=True)
class PolicyInput:
    schema: str
    features: tuple[int, ...]
    binding: v1.Binding


def encode(view: TaskView) -> PolicyInput:
    """Losslessly append visible channel metadata to the canonical v1 packet."""
    if type(view) is not TaskView:
        raise TypeError("structured-v2 TaskView required")
    parent = v1.encode(view.base)
    features = list(parent.features)
    for i in range(v1.MAX_FACTS):
        if i < len(view.channels):
            features.extend(int(x) for x in view.channels[i].eligible)
        else:
            features.extend((0, 0, 0))
    if len(features) != FEATURE_WIDTH:
        raise RuntimeError("Feature layout implementation mismatch")
    return PolicyInput(SCHEMA, tuple(features), parent.binding)


def decode(packet: PolicyInput) -> TaskView:
    """Strict canonical decoder; channel padding and flags must be exact."""
    if type(packet) is not PolicyInput or packet.schema != SCHEMA:
        raise ValueError("Explicit structured-v2 packet required")
    if type(packet.binding) is not v1.Binding:
        raise ValueError("Canonical v1 binding required")
    _tuple(packet.features)
    if len(packet.features) != FEATURE_WIDTH:
        raise ValueError("Wrong v2 feature width")
    for value in packet.features:
        if type(value) is not int or value < 0 or value > v1.MAX_INTEGER:
            raise ValueError("Exact bounded integer required")

    parent = v1.decode(v1.PolicyInput(
        v1.SCHEMA,
        tuple(packet.features[:v1.FEATURE_WIDTH]),
        packet.binding,
    ))
    tail = packet.features[v1.FEATURE_WIDTH:]
    channels = []
    for i in range(v1.MAX_FACTS):
        values = tuple(tail[i*CHANNEL_WIDTH:(i+1)*CHANNEL_WIDTH])
        if any(x not in (0, 1) for x in values):
            raise ValueError("Channel flags must be canonical zero/one")
        if i < len(parent.facts):
            channels.append(FactChannels(tuple(bool(x) for x in values)))
        elif any(values):
            raise ValueError("Unused fact channel padding must be zero")
    view = TaskView(parent, tuple(channels))
    if encode(view) != packet:
        raise ValueError("Noncanonical v2 packet")
    return view


def declared_channels(view: TaskView, fact_index: int) -> tuple[str, ...]:
    """Return semantic channel eligibility only; this is not runtime authorization."""
    if type(view) is not TaskView or type(fact_index) is not int:
        raise TypeError("Typed v2 view and integer fact index required")
    if not 0 <= fact_index < len(view.channels):
        raise ValueError("Fact index out of range")
    spec = view.channels[fact_index]
    return tuple(name for name, allowed in zip(CHANNELS, spec.eligible, strict=True) if allowed)


def visible_usable_channels(view: TaskView, fact_index: int) -> tuple[str, ...]:
    """Policy-visible intersection of semantic eligibility and current resource masks.

    This helper is a convenience for feature inspection only. The trusted action runtime
    must still reauthorize every proposal and remains the execution authority.
    """
    declared = set(declared_channels(view, fact_index))
    resources = view.base.resources
    usable = []
    for i, name in enumerate(CHANNELS):
        if name in declared and resources.available[i] and resources.permitted[i]:
            usable.append(name)
    return tuple(usable)


def deliver(view: TaskView, consumer: Callable[[PolicyInput], T]) -> T:
    """Versioned consumption boundary; no implicit v1 or legacy adaptation."""
    if getattr(consumer, "input_schema", None) != SCHEMA:
        raise TypeError("Consumer must explicitly accept structured-v2")
    return consumer(encode(view))
