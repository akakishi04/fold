# Structured Action Channel v0.1 — selected fact to typed action

This is an **opt-in reference mapper** between structured-task-input-v2 and the existing
structured action runtime.

## Contract

Input:

```text
v2 TaskView
trusted RuntimeState whose state.view == v2.base
already-selected fact_index
```

Required selected fact metadata:

```text
exactly one declared semantic channel:
RETRIEVE or OBSERVE or ASK_USER
```

Output:

```text
ActionProposal(
  action=<the declared channel>,
  fact_index=<unchanged selected fact index>,
  expected_state_sha256=<current trusted state digest>
)
```

## Separation of concerns

The mapper does **not**:
- infer whether more information is needed;
- select or repair the fact index;
- inspect a hidden fact value;
- choose among multiple eligible channels;
- intersect semantic eligibility with runtime permission/availability;
- reserve budget;
- call a provider;
- publish evidence.

The existing `structured_action_runtime.step()` remains authoritative for:
- permission;
- availability;
- already-observed checks;
- acquisition budget;
- pending intent;
- runtime version/state identity.

A declared channel may therefore still be denied by runtime authority.

## Scope

v0.1 supports exactly-one declared channel for the selected fact. Zero-channel and
multi-channel facts are rejected by this mapper rather than guessed.

This is a reference integration boundary. It is not a learned tool preference policy and
does not establish final Gate E performance.
