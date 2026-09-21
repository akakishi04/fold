# C210 preregistration — baseline development measurement

**C209 ACCEPTED PASS. C210 ACTIVE / NOT YET JUDGED. C211 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

On the frozen C207 development manifest, what raw matched performance and cost measurements are
produced by:

1. the9 frozen projected C181/C188 candidate model pairs;
2. an INTERNAL_ONLY baseline;
3. the registered canonical FIXED_ACQUISITION baseline;

under the same trusted runtime and answer boundary?

C210 is a **development measurement**, not a performance acceptance test.

## Frozen parents / data

C209:
- execution HEAD:
  `a9e4bdae10b574eb5fd66f4a3dc027bab5a18194`
- summary SHA256:
  `49476c781212f87a2782fdb6b042582dcd18941642b452855bb92690f90facc3`
- status:
  **ACCEPTED PASS**

C207 development artifacts:

```text
visible SHA256
c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543

scorer SHA256
0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912
```

The C207 scorer is loaded only for environment construction and post-hoc scoring.

It is not passed to candidate or baseline policy functions.

## Policy identities

Baselines:

```text
INTERNAL_ONLY
FIXED_ACQUISITION
```

Candidate cohort:

```text
CANDIDATE-181001-188001
CANDIDATE-181001-188002
CANDIDATE-181001-188003
CANDIDATE-181002-188001
CANDIDATE-181002-188002
CANDIDATE-181002-188003
CANDIDATE-181003-188001
CANDIDATE-181003-188002
CANDIDATE-181003-188003
```

Every policy is measured on all144 development episodes.

Registered evaluations:

```text
11 policies *144 episodes =1584
```

No candidate identity is selected in C210.

## Shared answer boundary

All policies use the same disclosed answer boundary:

```text
C171 completion_values
-> C171 benchmark-only proof_fixture
-> production structured_derived_result.verify
```

This shared symbolic component is not learned FOLD reasoning.

It emits only a production VERIFIED_DERIVED result when current trusted evidence logically fixes one
Boolean conclusion.

Because no learned answer-bit generator exists in this stage, C210 reports guarded output quality
and acquisition-policy behavior. It does not silently rename this as an unguarded learned
hallucination measurement.

## INTERNAL_ONLY

No acquisition and no provider access.

Registered harness-control totals on the fixed development set:

```text
episodes144
correct48
answered48
unresolved96
acquisition attempts0
provider calls0
publications0
ASK_USER turns0
authority violations0
```

These are structural controls, not Gate E performance margins.

## FIXED_ACQUISITION

Policy:

1. run the shared resolver;
2. if unresolved, find the first non-OBSERVED original fact in canonical visible `fact_id` order
   with exactly one declared acquisition channel;
3. make at most one acquisition attempt through the production runtime;
4. run the shared resolver again.

No necessity label or source value reaches the fixed policy.

Registered harness-control totals:

```text
episodes144
correct128
answered128
unresolved16
acquisition attempts96
provider calls90
publications80
ASK_USER turns16
authority violations0
malformed publications0
```

The16 unresolved episodes are the registered malformed/unavailable fault conditions.

## Frozen candidate policy

For each of9 base/head pairs:

1. project trusted visible state through accepted C209 candidate projection;
2. run one frozen C181/C188 combined necessity/target inference over the144 initial rows;
3. if necessity says SUFFICIENT, invoke only the shared resolver on trusted original runtime state;
4. if NEEDS, execute the selected **original** fact through original structured-v2 channel metadata
   and production acquisition lifecycle;
5. permit at most one acquisition attempt;
6. after a successful publication, project updated trusted state and run one frozen necessity-only
   reclassification;
7. emit only if post necessity says SUFFICIENT and shared resolver verifies;
8. failed/denied acquisition is not retried.

Candidate policy receives no scorer argument.

## Registered environment fault behavior

Environment-only scorer metadata instantiates:

- NONE: valid bounded source;
- MALFORMED_PAYLOAD: provider called, production source validation rejects;
- MISSING_DELIVERY: provider called once and returns no delivery;
- PERMISSION_DENIED: runtime denies before provider call;
- BUDGET_EXHAUSTED: runtime denies before provider call.

Candidate and fixed baseline use the same production acquisition lifecycle.

## Raw metrics

Per policy and family record:

- episodes;
- answered / unresolved;
- useful correct resolution;
- wrong answer;
- wrong abstention;
- pre-resolved / pre-correct;
- acquisition gain;
- acquisition attempts;
- provider calls / publications;
- ASK_USER turns;
- unnecessary acquisition;
- missed necessary acquisition;
- authority violations;
- malformed-evidence publication;
- guarded unsupported assertion;
- internal charged units;
- resolver verifier calls / checked steps;
- candidate premature-sufficient;
- candidate repeated NEEDS after successful publication;
- invalid target;
- candidate inference rows/forward/cell calls.

All raw numerators are retained.

## Fixed measurement-completeness gate

C210 scientific PASS means **the registered development measurement is complete**, not that the
candidate meets a quality threshold.

Required:

- all11 policy IDs present;
- all11 policies cover144 episodes;
-1584 policy-episode records;
- all9 candidate model identities present;
- INTERNAL_ONLY harness controls exactly match their registered totals;
- FIXED_ACQUISITION harness controls exactly match their registered totals;
- guarded unsupported assertion count0 for every policy;
- authority violations0 for every policy;
- malformed-evidence publications0 for every policy;
- each candidate model has initial inference rows144;
- each candidate model total inference rows =144 + its measured successful-publication post rows.

Candidate quality values are **not** part of this PASS gate.

A complete measured poor candidate is still valid accepted C210 evidence.

## Scope / non-claims

C210 registers:

- numerical margin registrationFalse;
- candidate selectionFalse;
- independent holdout createdFalse;
- training0;
- fresh seeds0;
- network0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

C210 must not:
- rank/select a winning model pair;
- set final improvement/noninferiority/coverage/cost margins;
- generate/evaluate an independent holdout;
- declare Gate E pass/fail.

After C210, a later preregistered step may use only these development results to freeze those choices
before any deciding holdout is evaluated.

## Historical regression immutability

Inherited exact historical exclusion remains:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
1998 loaded candidates
-1 exact historical mutable-state test
=1997 executed focused regression tests
```

## Authoring quality gate

C210 OWN:
- `fold_lm/v05_benchmarks/gate_e_c210_baseline_development_measurement.py`
- `tests_lm/test_v05_c210_baseline_development_measurement.py`
- `tools/run_c210.ps1`
- `tools/invoke_c210.ps1`
- this preregistration;
- `docs/baseline-development-measurement-v0.1.md`

Expected:

- source pins87;
- protected inputs165;
- output artifacts5;
- new tests24;
- focused regression **1997**;
- regression modules **95**.

Scientific manifest SHA256:

`09a7bbc84d37c93d6e559acffc8eaa0ff5c7f902271ebefff83b15363a10cb18`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:

- accepted C209 identity and all C209 run artifacts;
- C207 visible/scorer artifact identities;
- scorer separation from all policy functions;
- fixed/internal full-development unit controls;
- production fault behavior and provider-call counts;
- candidate projection/runtime separation;
- all9 model identities and no winner selection;
- shared resolver disclosure/equality across policies;
- no numerical threshold or holdout creation;
- semantic regression counts from actual loader/suite;
- Python free-name/import bindings;
- PowerShell dispatcher -> launcher -> runner parser chain;
- runner CLI argument order/indexes;
- source/protected/test/module/artifact counts;
- C211 non-registration.

Until review passes:

`post_authoring_review = PENDING`

The first C210 measurement attempt completed numerically but is **INVALID** because the deciding
candidate path directly called `gate_e_c189_live_multimissing_target.combined_predict` and
`necessity_predict` while the C189 source file was omitted from C210's preregistered
`source_blobs` / protected-input union.

Invalid attempt:
- execution HEAD:
  `633ce9bed165d30b0adb671c1faf12d34a9ad0cc`
- published log commit:
  `482d36ca1563fc7379fa48c346e255a526a48cec`
- log SHA256:
  `158e54bde84b156ebd665285ea85f32224dc943174ed9cc46997fd71753434fd`
- numeric measurement complete:
  **True**
- formal disposition:
  **INVALID EXECUTION / RETRY SAME C210**

Recovery pins the complete deciding-path helper chain omitted from the inherited source union:

```text
C175 audit
efd1bb246442fb4f472e33e450c16b192acfa18a

C179 shared graph
504c79b6a881c64dba2494ef6ad35bffd9099f5a

C182 frozen restore
a5fb10af6238d425f82b093a0c3676d247b1f0e3

C189 live inference
b34b40d84ab6597cc1cd26e47f64d58254d3304f
```

Scientific policy identities, frozen checkpoints, development fixtures, baseline controls, metric
definitions and workload remain unchanged. Revised source/protection accounting is87/165. Revised
committed bytes must be independently reviewed before retry.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:

- active_experiment = C210
- C210 repository preflight
- Python syntax preflight
- source/artifact precheck PASS
- focused regression1997/1997
-9 candidate progress lines
- RESULT
- POSTCHECK
- remote log publication

Judge C210 before any C211 registration.
