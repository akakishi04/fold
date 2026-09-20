# C199 preregistration — generic-loop ATTEMPT_LIMIT containment

**C198 ACCEPTED PASS. C199 ACTIVE / NOT YET JUDGED. C200 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

With the accepted C198/C197/C196 generic learned loop, budget13 cohort, frozen models and
coherent source worlds held fixed, does changing only trusted
`AcquisitionOwner.max_dispatches` from3 to1 safely stop a required second acquisition as
`ATTEMPT_LIMIT` after one successfully admitted observation?

Rows whose learned necessity policy becomes SUFFICIENT after the first observation must still
terminate normally and must not be forced into the limit path.

## Single changed condition

ALLOWED:
```text
max_dispatches = 3
```

DISPATCH_LIMIT_ONE:
```text
max_dispatches = 1
```

Everything else is held fixed.

Intervention path for rows whose accepted C198 reference requests a second acquisition:

```text
decision0 NEEDS + target0
-> reservation0
-> provider call0
-> PUBLISHED / OBSERVATION_ADMITTED
-> decision1 NEEDS + target1
-> reservation1
-> dispatch1
-> DENIED / ATTEMPT_LIMIT
-> UNRESOLVED_ACQUISITION_ATTEMPT_LIMIT
```

The first provider/read/publication is real and unchanged. The limit is checked only on the
second dispatch. The second reservation still consumes the existing action-runtime acquisition
reservation exactly as implemented by C172/C173; C199 does not redesign refund semantics.

## Held constant

- budget13;
- C174 PILOT NEEDS cohort;
-9536 coherent-world episodes / selector;
-9 frozen C181 x C188 selector pairs;
-16 coherent C190/C191 source bindings;
-C172/C173 action/acquisition semantics;
-C196 result-aware continuation;
-C197 dispatch-reason propagation;
-C198 accepted lineage;
-teachers and raw argmax;
-checkpoints / seeds / training;
-provider implementation;
-production runtime.

No task labels, source values, model inputs, weights, thresholds or source worlds are changed.

## Accepted parent / reference

C198:
- scientific execution HEAD:
  `e5a09864497fa38a9eac8d400b5162e33e99ec0d`
- summary:
  `runs/c198-v5e-stale-reservation-c8dcde8fca5c4cc2979475d64b7c2fda/summary.json`
- summary SHA256:
  `9cbb99e6ad200c5a9b88438abf140c58dd293661d8765f3460e3d2a7c70a8e75`

C199 owns an explicit C198 prediction loader. Required prediction NPZ schema is exactly:
```text
necessity_predictions (2,9,9536,4)
necessity_logits      (2,9,9536,4,2)
target_predictions    (2,9,9536,3)
target_logits         (2,9,9536,3,4)
row_indices           (9536,)
local_rows            (9536,)
world_codes           (9536,)
```

Arm0 ALLOWED is the reference prediction/logit stream.

## Frozen second-request counts

The ATTEMPT_LIMIT cohort is not selected after seeing C199 results.
It is defined by accepted C198 ALLOWED `second_reads`:

| base | head | second requests |
|---:|---:|---:|
|181001|188001|3888|
|181001|188002|3896|
|181001|188003|3936|
|181002|188001|3816|
|181002|188002|3856|
|181002|188003|3888|
|181003|188001|3920|
|181003|188002|3888|
|181003|188003|3860|

Total:
- ATTEMPT_LIMIT rows: **34948**
- SUFFICIENT-after-first rows: **50876**

These counts are references, not fitted thresholds.

## ALLOWED arm gate

For every one of9 blocks:
- episodes9536;
- exact accepted C198/C197 allowed prediction replay;
- full necessity/target prediction errors0;
- active finite logit deltas <=1e-6;
- exact first/second/third/final row counts;
- exact provider read count;
- all accepted scientific error counters0.

## DISPATCH_LIMIT_ONE gate

Every episode:
- first acquisition is admitted normally;
- exactly one first provider call/read/publication/receipt;
- exactly two learned decisions total;
- first two necessity/target predictions and logits match C198 ALLOWED reference;
- no third learned prediction.

For accepted-reference second-request rows:
- second action PENDING / ACQUISITION_RESERVED;
- second dispatch DENIED / ATTEMPT_LIMIT;
- second provider_calls0;
- second fact_publications0;
- one total receipt;
- generic-loop status `UNRESOLVED_ACQUISITION_ATTEMPT_LIMIT`;
- no fake SUFFICIENT;
- exactly one additional observed fact total;
- final:
```text
internal_remaining      6
acquisitions_remaining  2
RETRIEVE available      1
RETRIEVE permitted      1
last_outcome            ATTEMPT_LIMIT
internal_step           14
pending                 none
runtime terminal         none
```

For accepted-reference SUFFICIENT-after-first rows:
- no second acquisition attempt;
- status `SUFFICIENT_CLASSIFICATION`;
- one total provider call/read/publication/receipt;
- exactly one additional observed fact;
- final:
```text
internal_remaining      8
acquisitions_remaining  3
RETRIEVE available      1
RETRIEVE permitted      1
last_outcome            NONE
internal_step           12
pending                 none
runtime terminal         none
```

Per block:
- first_reads9536;
- provider_calls9536;
- publications9536;
- receipts9536;
- learned_decisions19072;
- attempt_limit_rows == accepted C198 second_reads;
- sufficient_after_first + attempt_limit_rows ==9536;
- second_provider_calls0;
- second_publications0;
- all C199 error counters0.

All18 blocks must pass.

A valid complete miss is **ACCEPTED VALID NEGATIVE**.
Source/hash/schema/parent artifact/loader/nonfinite/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C199**.

No result may change the frozen limit, cohort, counts, seed set or gate.

## Interpretation boundary

PASS means only:

> under the registered single-owner synchronous runtime and the already accepted learned
> necessity/target policies, a one-dispatch trusted limit is enforced at the second dispatch
> without a second provider call/publication, without a third learned decision, and without
> fabricated completion.

PASS does not establish:
- retry/recovery after ATTEMPT_LIMIT;
- optimal or learned dispatch-budget selection;
- arbitrary concurrency / multi-process quota enforcement;
- independent final holdout;
- language, answer, proof, or full Gate E completion.

## Workload / authoring quality gate

- 2 arms x85824 episodes =171648 episodes;
- 9 blocks / arm;
- expected focused regression **1701 =1677 existing +24 new**;
- expected modules **84**;
- historical source pins **156**;
- protected paths **407**;
- output artifacts **5** excluding summary;
- no new training/fresh seeds/network/proof checking/answer generation;
- production runtime modified False;
- Gate E candidate False.

New test coverage fixes:
- manifest/self-hash;
- C198 NPZ schema and shapes;
- actual AcquisitionOwner reservation/dispatch ordering;
- a real first FileSnapshotProvider read/publication;
- second PENDING reservation followed by DENIED/ATTEMPT_LIMIT;
- zero second provider call;
- exact ATTEMPT_LIMIT resource coordinates;
- one receipt / one new observation;
- no third learned decision;
- gate-negative controls;
- source-level max_dispatches3->1 isolation.

The runner performs `py_compile` before source/artifact precheck and runs all1701 focused
tests before the scientific benchmark.

Scientific manifest SHA256:
`3bda32133c97539c4e327899e08859e57df9361caa50657e22000374e65bacec`.

## Execution / stop

Use final registration HEAD as `ExpectedHead`.

Expected progress:
- C199 repository preflight
- C199 authoring syntax preflight
- source_and_artifact_precheck PASS
- focused regression1701/1701
-18 block progress records
- RESULT
- POSTCHECK
- remote log publication

Judge C199 before any C200 registration.
