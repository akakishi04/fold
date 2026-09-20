# C201 preregistration — selected learned fact to typed acquisition channel

**C200 ACCEPTED PASS. C201 ACTIVE / NOT YET JUDGED. C202 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can the already accepted learned phase-0 fact target from C199 be routed through the new
structured-task-input-v2 exactly-one channel metadata into the correct typed
RETRIEVE / OBSERVE / ASK_USER ActionProposal **without changing the selected fact and without
absorbing runtime authority into the mapper**?

This is a reference integration diagnostic. It adds no training and makes no learned
channel-preference claim.

## Mapper contract

New opt-in reference mapper:

`fold_lm/v05/structured_action_channel.py`

Input:

```text
structured-v2 TaskView
trusted RuntimeState with state.view == v2.base
already-selected fact_index
```

Required selected-fact metadata:

```text
exactly one declared channel:
RETRIEVE | OBSERVE | ASK_USER
```

Output:

```text
ActionProposal(
  action=<declared channel>,
  fact_index=<unchanged selected fact>,
  expected_state_sha256=<current trusted state digest>
)
```

The mapper does not:
- infer necessity;
- choose or repair the fact index;
- inspect hidden values;
- choose among zero/multiple channels;
- prefilter based on permission or availability;
- reserve or dispatch;
- call providers;
- publish evidence.

The existing `structured_action_runtime.step()` remains authoritative.

## Parent identities

Accepted C200:

- execution HEAD:
  `11181a355f13e7be2fda3957b9cdd45ad8868316`
- summary:
  `runs/c200-v5e-acquisition-channel-input-d892b01c24ee49cfbb87758e7a208be0/summary.json`
- summary SHA256:
  `624889546c9b484003e3f2bc79c1d746de28ea168def13da1a2dc87fde73520e`

Accepted learned-target source C199:

- execution HEAD:
  `48100f36f4f1acdf44d5cb1d508b907e19724c10`
- summary:
  `runs/c199-v5e-attempt-limit-886ac50bbbe046ebba61316e6bf97268/summary.json`
- summary SHA256:
  `0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`

C201 owns an explicit loader for C199 `episode-predictions.npz`.
Required schema/shapes:

```text
necessity_predictions (2,9,9536,4)
necessity_logits      (2,9,9536,4,2)
target_predictions    (2,9,9536,3)
target_logits         (2,9,9536,3,4)
row_indices           (9536,)
local_rows            (9536,)
world_codes           (9536,)
```

Only arm0 ALLOWED, phase0 target predictions are used.
All phase0 necessity predictions must remain NEEDS=1 and every target must be in0..3.
No new target inference or relabeling occurs.

## Registered route workload

For every accepted C199 phase0 target, C201 exercises all three exactly-one channel variants:

```text
9 blocks x 9536 episodes x 3 channels = 257472 route cases
```

Aggregated route records:

```text
9 blocks x 3 channels x 4 target indices = 108 records
```

Required:
- total route cases257472;
- RETRIEVE cases85824;
- OBSERVE cases85824;
- ASK_USER cases85824;
- route mismatches0;
- every proposal preserves selected fact_index;
- every proposal action equals the selected fact's one declared channel;
- request/scope/state digest remain current and exact.

## Runtime authority cross

**12 cases**:

```text
3 channels
x available {false,true}
x permitted {false,true}
```

The mapper must always propose the declared channel even if authority later denies it.

Expected trusted runtime outcomes across all12:

- PENDING / ACQUISITION_RESERVED:3
- DENIED / PERMISSION_DENIED:6
- DENIED / PROVIDER_UNAVAILABLE:3

Authority failures must be0.

## Already-observed controls

**3 cases**, one per channel.

The mapper still produces the declared action proposal, while trusted
`structured_action_runtime.step()` must return:

```text
DENIED / ALREADY_OBSERVED
```

All3 must pass.

## Invalid mapper controls

**7 cases** must all reject before proposal production:

- zero declared channel;
- multiple declared channels;
- negative selected index;
- out-of-range selected index;
- v2 base / runtime-state mismatch;
- wrong view type;
- wrong state type.

No fallback or guessed channel is allowed.

## Fixed PASS gate

C201 PASS requires:

```text
route_cases                 = 257472
route_records               = 108
route_mismatches            = 0

channel totals:
RETRIEVE                    = 85824
OBSERVE                     = 85824
ASK_USER                    = 85824

authority_cross             = 12
authority_failures          = 0
authority_pending           = 3
authority_permission_denied = 6
authority_unavailable       = 3

observed_controls           = 3
observed_failures           = 0

invalid_mapper_cases        = 7
invalid_mapper_rejected     = 7
```

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/import/regression/incomplete/protection failures are
**INVALID EXECUTION / RETRY SAME C201**.

No result may revise this gate under C201.

## Scope / non-claims

C201 registers:
- training steps0;
- fresh seeds0;
- learned forward calls0;
- provider calls0;
- network calls0;
- evidence writes0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS would establish only selected-fact -> exactly-one-channel proposal plumbing plus
separate runtime reauthorization.

PASS would not establish:
- learned preference among multiple eligible channels;
- learned tool selection;
- live provider execution for OBSERVE / ASK_USER;
- mixed-family answer quality;
- final Gate E completion.

## Authoring quality gate

C201 OWN:
- `fold_lm/v05/structured_action_channel.py`
- `fold_lm/v05_benchmarks/gate_e_c201_selected_fact_channel_route.py`
- `tests_lm/test_v05_c201_selected_fact_channel_route.py`
- `tools/run_c201.ps1`
- `tools/invoke_c201.ps1`
- this preregistration
- `docs/structured-action-channel-v0.1.md`

Expected:
- source pins15;
- protected inputs23;
- output artifacts5;
- new tests28;
- focused regression **1759 =1731+28**;
- regression modules **86**.

Runner performs `py_compile` on helper / benchmark / tests before source/artifact precheck,
then runs the full1759 regression before the scientific diagnostic.

Scientific manifest SHA256:

`615e3aa8374650ae95c889c6e6d9de4b6a5a076327e06838ccae1b74eb71df25`

## Post-authoring review requirement

Before the user receives an execution command, the complete committed C201
source/tests/runner/launcher/preregistration/docs must be re-fetched from remote and independently
reviewed under the repository post-authoring review rule.

Until that review passes:

`post_authoring_review = PENDING`

## Execution / stop

Use the final reviewed registration HEAD as `ExpectedHead`.

Expected progress:
- C201 repository preflight
- C201 authoring syntax preflight
- source_and_artifact_precheck PASS
- focused regression1759/1759
- selected-fact channel diagnostic
- RESULT
- POSTCHECK
- remote log publication

Judge C201 before any C202 registration.
