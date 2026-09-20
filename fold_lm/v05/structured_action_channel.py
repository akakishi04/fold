"""Opt-in selected-fact to acquisition-channel proposal mapper.

This module is deliberately small. It translates an already-selected fact index plus
structured-task-input-v2 semantic channel metadata into one typed ActionProposal.
It does not infer necessity, change the selected fact, inspect hidden values, execute a
provider or apply runtime availability/permission/budget policy. structured_action_runtime.step
remains the trusted authority boundary.
"""
from __future__ import annotations

from . import structured_action_runtime as action
from . import structured_task_input_v2 as v2


def propose_selected(view: v2.TaskView, state: action.RuntimeState, fact_index: int) -> action.ActionProposal:
    if type(view) is not v2.TaskView:
        raise TypeError("structured-v2 TaskView required")
    if type(state) is not action.RuntimeState:
        raise TypeError("RuntimeState required")
    if state.view != view.base:
        raise ValueError("v2 base and runtime state must be identical")
    if type(fact_index) is not int or not 0 <= fact_index < len(view.base.facts):
        raise ValueError("Selected fact index out of range")

    channels = v2.declared_channels(view, fact_index)
    if len(channels) != 1:
        raise ValueError("Selected fact must declare exactly one acquisition channel")

    return action.propose(state, channels[0], fact_index=fact_index)
