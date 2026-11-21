# C190 preregistration — iterative learned multi-missing acquisition

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

Registered only after C189 acceptance commit
`9bd1ccc7d176a8134466eb22a3546861f1ba9a7d`.

**C189 ACCEPTED PASS. C190 ACTIVE / NOT YET JUDGED. C191 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## One scientific question

When the actual state remains NEEDS after the first learned target acquisition, can the same
frozen C181 necessity representation and frozen C188 learned target selector:

1. select a new currently influential missing fact,
2. execute exactly one second real C172/C173 RETRIEVE without repeating the first target,
3. and correctly classify the second actual updated state?

No new training, fresh seed, tool choice, answer/proof or third acquisition is introduced.

## Why this is the next boundary

C189 established one live learned target acquisition and correct post-state necessity.
Across the accepted C189 run, **12229 / 31824** episodes remained NEEDS after the first
acquisition. C189 deliberately stopped there.

C190 changes only that stop rule: if the actual first post-state is still NEEDS, allow one
second learned target and one second real acquisition.

## Frozen components

Reuse unchanged:
- C181 INTERNAL_SEMANTICS base seeds181001/181002/181003
- C188 target-head seeds188001/188002/188003
- all nine accepted base/head combinations
- original C174 local fact layout
- C172 structured action runtime
- C173 acquisition lifecycle
- raw argmax; no repair or calibration

No C181/C188 weight update.

## Coherent source worlds

C189 crossed only the selected fact's bit because it allowed one acquisition.

C190 may acquire two different facts, so both answers must come from one coherent source.
For each initial row enumerate **every complete 4-bit world consistent with already
observed facts**.

Initial cohort:
- 1768 PILOT NEEDS rows
- missing2 rows: 1152; each has 4 consistent worlds -> **4608 world episodes**
- missing3 rows: 616; each has 8 consistent worlds -> **4928 world episodes**
- total per selector: **9536**
- nine selectors: **85824 formal episodes / 9 blocks**

There are 16 registered complete world source files. Each file uses the unchanged C173
snapshot schema and contains all four opaque C185 external fact IDs with one coherent bit
assignment. One SourceBinding/Endpoint is fixed for the entire episode and may serve both
acquisitions.

The world code/source contents never enter neural numeric input.

## Policy path

Initial:
```text
TaskView
-> decision debit
-> ONE frozen C181 forward
   -> necessity logits
   -> seven hidden states
-> frozen C188 target head
-> target0
```

If initial NEEDS:
```text
target0 -> C172 reservation -> C173 real read/admission from episode world
-> actual state1
-> decision debit
-> ONE frozen C181 forward
   -> necessity1
   -> hidden states
-> same frozen C188 head -> target1
```

If necessity1 is SUFFICIENT, stop.

If necessity1 is NEEDS:
```text
target1 -> second C172 reservation -> same C173 world snapshot
-> actual state2
-> decision debit
-> frozen C181 necessity-only decision
-> stop regardless of NEEDS/SUFFICIENT
```

No third acquisition.

## Resource accounting

Start:
`12 internal / 4 acquisitions / step7`.

First learned decision input:
`11 / 4 / step8`.

After first action1 + dispatch2 + second learned decision1:
`7 / 3 / step12`.

If a second acquisition is taken, after action1 + dispatch2 + final decision1:
`3 / 2 / step16`.

No budget reset/clamp to training constants.

## Teachers are scoring-only

At each visible state:
- necessity scoring uses the unchanged C174 logical necessity definition;
- target scoring uses the unchanged C188 influential-target set definition.

Neither teacher enters policy input, target head, action proposal, endpoint routing or provider.

## Parent replay

C190 initial policy state is identical to accepted C189 initial live state.
Before judging iterative behavior, initial necessity/target predictions and logits must replay
the accepted C189 `episode-predictions.npz` for every expanded world copy:

- exact necessity argmax
- exact target argmax
- max abs necessity-logit difference <= 1e-6
- max abs finite unknown-target-logit difference <= 1e-6

A parent replay failure is execution invalidity.

## Fixed deciding gate

For **each of all nine** selector blocks:

- episodes = 9536
- missing2 worlds = 4608
- missing3 worlds = 4928
- initial necessity errors = 0
- initial C189 replay errors = 0
- target0 errors = 0
- selected observed facts = 0
- first acquisition errors = 0
- post1 necessity errors = 0
- target1 errors on true post1 NEEDS states = 0
- repeated first target = 0
- second acquisition errors = 0
- final post2 necessity errors = 0
- runtime/contract errors = 0
- first reservations/provider calls/publications = 9536
- second reservations/provider calls/publications =
  the measured number of logically NEEDS post1 states
- decision charges = `2*9536 + second_acquisitions`
- total internal charged = `5*9536 + 4*second_acquisitions`
- final SUFFICIENT + final NEEDS = 9536
- initial necessity/target logit replay deltas <= 1e-6

All nine blocks must pass. No average/best-head rescue.

A finite completed miss is **ACCEPTED VALID NEGATIVE**.
Source/hash/schema/parent replay/nonfinite/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C190**.

## Workload

Registered fixed maxima:
- base checkpoint loads3
- target-head loads9
- formal episodes85824
- initial base rows85824
- second-decision base/target rows measured 0..85824
- final necessity rows measured 0..85824
- max acquisitions/episode2
- max decisions/episode3
- training0 / fresh seeds0
- network0 / core EvidenceState writes0 / answer0 / proof0
- production runtime modifiedFalse
- Gate E candidateFalse

Expected focused regression:
**1485 = 1449 existing + 36 new; 75 modules.**

## Registered outputs

Exactly 21 artifacts excluding summary:
- iterative-plan.json
- parent-replay.json
- episode-results.json
- episode-traces.jsonl.gz
- episode-predictions.npz
- sources/world-00.json ... sources/world-15.json

Scientific manifest SHA256:
`ddca97a8c8de1687929b95e69f33c3073647017c3514871ae3db81d22605ef6d`.

Expected historical source pins: **111**.
Expected protected paths: **277**.

## Interpretation boundary

PASS supports only bounded two-step learned information acquisition in the repeatedly
inspected C174 development family.

PASS does NOT establish:
- arbitrary-length iterative planning;
- third-or-later acquisition;
- learned tool/provider choice;
- globally optimal information gain;
- renaming invariance in this C number;
- language/larger/repeated-variable generalization;
- independent final holdout;
- answer/proof generation;
- production adoption or Gate E completion.

Do not register C191 before C190 judgment.


## Execution-recovery note — exact-state initial-policy memoization

The first completed C190 run was scientifically error-free on all action/target/post-state
counters but failed the preregistered parent-logit replay validity guard only.

Observed expanded-batch replay maxima:
- necessity: 5.245208740234375e-06
- target: 5.7220458984375e-06
- parent necessity argmax errors: 0
- parent target argmax errors: 0

The hidden source world is not part of the initial TaskView or numeric policy input, so each
of the 4/8 world copies of one source row has the exact same initial observable state.
The recovery therefore recomputes the frozen initial policy exactly once per unique
1768-row initial cohort for each of the nine selectors, using the same ordering/batching
as accepted C189, then memoizes that output across the identical hidden-world copies.

This does NOT use C189 saved predictions as policy output. C189 saved values remain
validation-only. It does not change seeds, checkpoints, episodes, worlds, teachers, target
gate, acquisition gate, thresholds or interpretation.

Execution accounting supersedes only the redundant initial-forward workload:
- logical initial episodes: 85824
- actual unique initial policy rows: 15912 = 1768 x 9
- initial policy forwards: 18
- initial shared-cell calls: 126
- post-first and post-second live rows remain measured
- all 85824 logical episodes still execute their own C172/C173 state/action lifecycle

Scientific manifest SHA256 after this execution-only accounting clarification:
`ddca97a8c8de1687929b95e69f33c3073647017c3514871ae3db81d22605ef6d`.

The fixed replay threshold remains **<=1e-6**. No tolerance relaxation is permitted.
