# Structured Task Interface v0.2 — per-fact acquisition channels

v0.2 is an **opt-in additive policy-input contract**. It does not replace or reinterpret
`structured_task_input.py` v1, and it does not grant execution authority.

## Purpose

Gate E requires facts whose appropriate information source differs:
- `RETRIEVE` — registered data/provider lookup;
- `OBSERVE` — environment/sensor observation;
- `ASK_USER` — information available only from the user interface.

v1 exposes global tool availability and permission but no fact-specific acquisition mechanism.
Without that distinction a learned policy cannot infer which tool is semantically applicable to
a selected missing fact.

## Numeric layout

```text
features[0:72]   = exact canonical structured-task-input-v1 packet
features[72:84]  = 4 fact slots x 3 channel-eligibility bits
                   [RETRIEVE, OBSERVE, ASK_USER]
```

Unused fact-slot channel padding is exactly zero.

The v1 prefix must decode independently under the unchanged v1 decoder. v2 never silently
adapts to a v1 consumer; consumers must explicitly declare the v2 schema.

## Meaning of channel bits

A channel bit says only:

> this acquisition mechanism is semantically applicable to this fact.

It does **not** mean:
- provider currently exists;
- execution is permitted;
- budget is available;
- the action has been authorized;
- acquisition succeeded;
- the fact value is known.

Current availability and permission remain the separate v1 resource masks. The trusted action
runtime remains authoritative and must re-check every actual proposal.

Multiple channels may be eligible. All-zero eligibility is representable for a fact with no
declared acquisition mechanism.

## Leakage boundary

Channel metadata must not contain or derive from:
- hidden fact value;
- answer label;
- necessity label;
- evaluator dependency;
- future acquisition result.

Paired hidden completions therefore receive identical v2 packets whenever their visible state
and declared channel metadata are identical.

## Scope

v0.2 only establishes the input boundary required for later learned acquisition-channel
selection. It is not itself a tool selector, provider router, learned policy, Gate E baseline,
or final Gate E evaluation.
