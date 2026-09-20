# C203 preregistration — mixed-channel multi-step replay

**C202 ACCEPTED PASS. C203 ACTIVE / NOT YET JUDGED. C204 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can the full accepted C199 ALLOWED multi-step necessity/target decision trace be replayed exactly
while fact-specific acquisition channels switch within an episode, using the accepted C201 mapper
and real C202/C173 acquisition lifecycle, without cross-channel provider work, value/fact mutation
errors, resource drift or loss of final SUFFICIENT closure?

This is a mixed-channel orchestration diagnostic. It adds no training and no learned forward calls.

## Fixed learned decision source

Accepted C199:

- execution HEAD:
  `48100f36f4f1acdf44d5cb1d508b907e19724c10`
- summary SHA256:
  `0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`

C203 uses only the accepted C199 ALLOWED saved necessity/target predictions.

No new model inference, target repair, relabeling or thresholding occurs.

Fixed parent replay totals:

```text
episodes             85824
learned decisions    214948
acquisitions         129124
final SUFFICIENT     85824
```

## Input reconstruction

Protected C174 parent:

- summary SHA256:
  `3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36`

C203 loads only the protected C174 `pilot-data.npz` feature array and indexes it using the
accepted C199 `row_indices`.

The C199 `world_codes` restore the same coherent C190 source world for each episode.

Initial runtime resources are the accepted budget13 coordinates:

```text
internal_remaining      13
acquisitions_remaining  4
available               [true,false,false]
permitted               [true,false,false]
last_outcome            NONE
internal_step           7
```

## Fixed fact-to-channel layout

Exactly one layout is registered:

```text
fact0 -> RETRIEVE
fact1 -> OBSERVE
fact2 -> ASK_USER
fact3 -> RETRIEVE
```

This mapping is fixed before execution and is not learned.

## Decision/action separation

Before every replayed learned decision:

```text
available = [true,false,false]
permitted = [true,false,false]
```

Then:
1. trusted scheduler charges the accepted decision cost;
2. C199 saved necessity prediction is read;
3. if NEEDS, C199 saved target index is read;
4. trusted scheduler temporarily changes only availability/permission to
   `[true,true,true]`;
5. structured-v2 wraps all four facts with the fixed one-hot channel layout;
6. C201 mapper produces the typed proposal for the unchanged selected fact;
7. existing ActionRuntime + AcquisitionOwner reserve/dispatch/publish;
8. parent RETRIEVE-only masks are restored before the next replayed decision.

Authority refreshes do not change budgets, facts, evidence time or revision.

## Expected projection

Before any C203 dispatch, the accepted C199 artifact is deterministically projected through the
fixed channel layout.

For every block the projection fixes:
- number of replayed decisions;
- number of acquisitions;
- final SUFFICIENT count;
- exact RETRIEVE / OBSERVE / ASK_USER acquisition counts;
- exact number of within-episode channel switches.

The actual C203 trace must equal this projection exactly.

Global fixed totals additionally require:

```text
decisions           214948
acquisitions        129124
final SUFFICIENT    85824
```

The exact per-channel totals and exact switch count are parent-artifact projections, not values
chosen after seeing C203 results.

At least one within-episode channel switch must exist.

## Per-acquisition contract

For every replayed NEEDS+target acquisition:

- target must currently be UNOBSERVED;
- typed proposal action equals the fixed channel for that fact;
- typed proposal fact_index equals the accepted C199 target;
- ActionResult = PENDING / ACQUISITION_RESERVED;
- DispatchResult = PUBLISHED / OBSERVATION_ADMITTED;
- matching channel provider call delta=1;
- nonmatching channel provider call delta=0;
- one new receipt matches action/fact/value;
- selected fact becomes OBSERVED at the coherent C190 world bit;
- every nonselected fact is byte-for-byte unchanged from immediately before the acquisition;
- after publication parent authority masks are restored.

## Final resource contract

For an episode with:
- `D` replayed decisions;
- `A` admitted acquisitions;

required final resources:

```text
internal_remaining      = 13 - D - 3*A
acquisitions_remaining  = 4 - A
internal_step           = 7 + D + 3*A
available               [true,false,false]
permitted               [true,false,false]
last_outcome            NONE
pending                 none
runtime terminal        none
receipt count           A
```

Every episode must terminate on the final accepted SUFFICIENT decision.

## Fixed PASS gate

Nine block records must all satisfy:

- episodes9536;
- actual decisions == parent projection;
- actual acquisitions == parent projection;
- final SUFFICIENT == parent projection;
- actual channel counts == parent projection;
- actual channel switches == parent projection;
- all C203 scientific error counters0;
- projection_error0.

Global:

```text
episodes             85824
decisions            214948
acquisitions         129124
final SUFFICIENT     85824
failures             0
projection errors    0
channel counts       == frozen parent projection
channel switches     == frozen parent projection
channel switches     > 0
```

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/import/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C203**.

No result may change the layout, parent trace, workload or gate under C203.

## Scope / non-claims

C203 registers:
- training0;
- fresh seeds0;
- learned forward calls0;
- network0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS establishes only mixed-channel multi-step execution of an already accepted learned decision
trace.

PASS does not establish:
- learned channel preference;
- live re-inference under 84-feature v2 inputs;
- real sensor/user transport;
- final mixed-family answer quality;
- final Gate E completion.

## Authoring quality gate

C203 OWN:
- `fold_lm/v05_benchmarks/gate_e_c203_mixed_channel_multistep_replay.py`
- `tests_lm/test_v05_c203_mixed_channel_multistep_replay.py`
- `tools/run_c203.ps1`
- `tools/invoke_c203.ps1`
- this preregistration;
- `docs/mixed-channel-multistep-replay-v0.1.md`

Expected:
- source pins31;
- protected inputs53;
- output artifacts5;
- new tests28;
- focused regression **1813 =1785+28**;
- regression modules **88**.

Scientific manifest SHA256:

`2b9723733441019df8d73fa40fcf1421023c4765cbe6fdc91a31b2765b447ae6`

## Post-authoring review requirement

Before execution, committed remote bytes for benchmark/tests/runner/launcher/preregistration/docs
and parent artifact contracts must be independently re-fetched and reviewed.

The first reviewed execution attempt at
`13b1db0c595f6d4900a038693f6c0d87728e3996`
was INVALID in regression because test22 inspected the wrong function namespace. The scientific
manifest and gate remain unchanged.

The recovery changed only that source-audit test and strengthened the repository review rule.

`post_authoring_review = PASS`

revised review HEAD:
`d7d79dc2b51a424f4c49b59244e2a7a27456ce29`

The revised review mechanically evaluated every C203 source-string assertion against the exact
function source it inspects, including caller/callee ownership and live-inference call guards.

## Execution / stop

Use the final reviewed registration HEAD as `ExpectedHead`.

Expected progress:
- C203 repository preflight
- C203 authoring syntax preflight
- source_and_artifact_precheck PASS
- focused regression1813/1813
-9 block progress lines
- RESULT
- POSTCHECK
- remote log publication

Judge C203 before any C204 registration.
