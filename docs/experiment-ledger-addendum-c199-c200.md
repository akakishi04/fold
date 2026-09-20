# C199 acceptance / C200 handoff

## Formal judgment

**C199 — ACCEPTED PASS.**
**C200 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C199:
- scientific execution HEAD: `48100f36f4f1acdf44d5cb1d508b907e19724c10`
- published log commit: `e22618047914b903dc6d459ba0617c05c4fa755b`
- log SHA256: `8d51629d4d597dc8c111b70443ae332ba45bb5a21eae0b193bf10194c8717318`
- log bytes: 376415
- summary: `runs/c199-v5e-attempt-limit-886ac50bbbe046ebba61316e6bf97268/summary.json`
- summary SHA256: `0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`
- focused regression: **1701/1701** in 66.544s
- all18 arm/block progress records completed
- source/artifact precheck PASS
- Python syntax preflight PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

## Deciding evidence

Two complete arms, each9 selector blocks x9536 = **85824 episodes**.

### ALLOWED
Accepted C198/C197/C196/C194 behavior was replayed exactly in registered scope.

### DISPATCH_LIMIT_ONE
Across all9 blocks:
- first provider reads: **85824**
- reference second-request / ATTEMPT_LIMIT rows: **34948**
- SUFFICIENT-after-first rows: **50876**
- second provider calls: **0**
- second publications: **0**
- no third learned decision
- candidate_gate_passed True
- all registered scientific error counters0

Rows that required a second acquisition terminated with
`UNRESOLVED_ACQUISITION_ATTEMPT_LIMIT`.
Rows made sufficient by the first admitted observation terminated normally.

## Scientific interpretation

C199 establishes that, in this bounded single-owner synchronous runtime, changing only the
trusted dispatch cap to one prevents a second provider execution/publication while preserving
the accepted first acquisition and the learned second-step decision. The generic loop preserves
the runtime `ATTEMPT_LIMIT` cause and does not fabricate completion.

## Non-claims

C199 does not establish:
- learned selection of acquisition budgets;
- retry/recovery after ATTEMPT_LIMIT;
- arbitrary concurrency or multi-process quota enforcement;
- complete Gate E nine-family behavior;
- independent final holdout;
- language, answer/proof generation, or full Gate E completion.

## Gate E readiness blocker

The Gate E v0.1 contract requires three acquisition channels in the task family:
`RETRIEVE`, `OBSERVE`, and `ASK_USER`.

The current learned path C174-C199 learns necessity and fact target, but experimental
orchestration fixes the acquisition action to RETRIEVE. The v1 structured task input exposes
global tool availability/permission but does not expose a fact-specific acquisition-channel
binding. Therefore a learned policy cannot distinguish, from the current numeric policy input,
a retrievable fact from a sensor-only or user-only fact.

Launching the three-policy Gate E development comparison now would conflate missing input
semantics with policy quality.

## Next boundary

C200 should add an **opt-in, backward-preserving structured task input v2** that:
- retains the existing72 v1 features exactly as its prefix;
- adds three policy-visible channel-eligibility bits per fact for
  RETRIEVE / OBSERVE / ASK_USER;
- carries no hidden fact value, answer label, necessity label, or evaluator dependency;
- preserves global runtime availability/permission as a separate authority layer;
- round-trips losslessly and rejects malformed/noncanonical channel metadata;
- leaves all historical v1/C170-C199 behavior untouched.

C200 is an input-contract diagnostic, not a learned tool-selection claim and not a Gate E
candidate run.
