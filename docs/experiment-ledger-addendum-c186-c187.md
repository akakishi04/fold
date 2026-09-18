# C186 accepted result — non-admission is not sufficient evidence

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

## 1. Formal verdict

**C186 — ACCEPTED PASS.** All 80 blocks / 296,960 episodes completed. Each of the
three INTERNAL_SEMANTICS candidates has zero failed episodes, including zero false
sufficiency after non-admission. No C186 rerun. Gate E remains NOT PASSED.
C187 is NOT REGISTERED at this acceptance commit. All historical verdicts remain.

The earlier attempt at a4127d8a6bef0bf7eafd6e5d76fbb2061ab74eba remains INVALID
EXECUTION, not a second scientific run or a valid negative. The successful retry uses
6e59bcbcdf84a37c4bece228b8163042cc6ac06a, the execution-only NPZ recovery commit.
The original scientific manifest, checkpoint set, scenarios and strict gate are unchanged.
See experiment-ledger-addendum-c186-execution-recovery.md for the original failure.

## 2. Execution validity and evidence identity

Uploaded log: `貼り付けられたテキスト（1 点）(20260918-191445).txt`.
502259 bytes; SHA256 bad2b41b59cc378d569b2368466b1554693780025250ac161ac66bf96d08816e.
C185 schema precheck PASS (70810728 raw array bytes); source/artifact precheck PASS.
1341 / 1341 focused tests PASS in 62.788 s. Existing C145 scalar-conversion warning
occurs in a passing test, not an execution failure. Final protected inputs preserved,
tracked tree clean, execution HEAD preserved, run_execution_valid=True.

Result:
`runs/c186-v5e-nonadmission-0d274f54409144cf83899758d020e82b/summary.json`
SHA256 e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82.
Complete reconstructed summary:264136 bytes, exact hash match.
92 historical source pins,203 protected paths,13 output artifacts.
Six C181 checkpoints; source seeds181001/181002/181003; CPUfloat32,two threads.
No fresh seeds,training,teacher,auxiliary head,answer generation,proof calls,
network,core EvidenceState writes or production runtime modification.

All6 static replays:9396 rows each,total56376,decisions identical,max logit difference0.
All32 matched successful live blocks reproduce C185 inputs/decisions and logits,
max logit difference0. Fault-scenario first phases are guarded by the original replay
checks; individual first-phase replay deltas are not separately listed in the summary.

## 3. Metrics

|Candidate seed|Episodes|Attempts|Admitted|Non-admitted|Skipped|Failed|
|---|---:|---:|---:|---:|---:|---:|
|181001|37120|7680|3072|4608|29440|0|
|181002|37120|7680|3072|4608|29440|0|
|181003|37120|7680|3072|4608|29440|0|
|Total|111360|23040|9216|13824|88320|0|

Every candidate has zero initial_error,missed_attempt,unnecessary_attempt,post_error,
false_sufficient_after_nonadmission and contract_error. Each of the three non-admission
scenarios contributes4608 correct candidate NEEDS reclassifications across models/layouts.
The two successful scenarios contribute9216 correct SUFFICIENT reclassifications total.

All-policy totals:79360 action attempts/reservations/provider calls/real reads;
31744 publications;47616 non-admitted attempts;17459200 provider bytes (220/read).
Decision charges376320;internal charged614400. Neural initial rows222720,post rows42240;
static replay56376;total321336 neural rows,360 forward batches,2520 shared-cell calls.
Reported benchmark wall-clock284.694513s includes diagnostic work,not production latency.
Peak RAM/VRAM is not measured. Source hashing/setup/serialization IO is additional.

All-policy failed65436,initial_error65200,post_error24774,contract_error0.
These are overlapping counters,not disjoint failure counts. All failures belong to controls.
FINAL_ONLY seeds181001/181002/181003:failed9310/9440/9566;
false_sufficient_after_nonadmission110/0/126,236 total. The236 is NOT candidate failure.
MISSING_RULE:failed29440,post_error17664,37120 reads,14848 publications.
NEVER_QUERY:failed7680,0 reads,7680 missed attempts. Both deliberate control patterns match.

## 4. Scientific interpretation

The fixed candidates distinguish successful evidence admission from an attempt that
adds no usable fact in this registered setting. Normal0/1 -> observed fact -> SUFFICIENT;
missing reply,corrupt value,provider exception -> unchanged unknown -> NEEDS.
Actual consumed resources and outcomes remain visible; no reset,truth-label override,
proof correction or retry makes the decision correct. The driver uses raw argmax.

This weakens an explanation based solely on having attempted retrieval or consumed
its budget. It is not a mechanistic proof of internal representations. In particular,
PROVIDER_FAILURE and successful admission share numeric outcome0 under the existing
schema but differ in actual evidence. No new outcome code was invented.

## 5. Confounds and limits

Faults are injected AFTER a reference file read,not authentic network timeout/OS-open
failures. The runtime is handwritten and does the admission validation; target choice
is the handwritten sole-unknown selector; tool is fixed RETRIEVE. Model output is a
necessity classification,not a factual answer or a verified terminal claim.
The one-attempt stop is enforced by the driver,not a learned retry/stop policy.
No active permission denial,provider-unavailable context or exhausted acquisition
budget was tested by the frozen models here. All official requests began permitted,
available and budgeted. Model proposals vs execution authority remain a next boundary.

The3712 source rows are the same4 development groups/116templates/read-once4-variable
family. Models,layouts and scenarios are not independent semantic samples. No natural
language,larger/repeated-variable,independent final-holdout or full Gate E claim.
C181/C184/C185 PASS,C182 VALID NEGATIVE and all other prior judgments remain unchanged.

## 6. Reviewer verification boundary

Reviewer parsed the complete uploaded log, reconstructed the canonical JSON and matched
its SHA256. Independently checked80 ordered blocks,320 group tables/4480 counter
values and sums,14 global counter totals,6 static/32 successful replay records,all
candidate/control gate clauses,resource and IO arithmetic. Matched32 successful
blocks against the separately uploaded accepted C185 summary. No errors found.
Separate13 output files,fullNPZ arrays,traces,checkpoint bytes and dataset were NOT
independently reread/reexecuted. Full1341tests and296960episodes were NOT rerun here.
Local git network access failed DNS; repository source/metadata came through connector.

## 7. Next design boundary (not registration)

Do not change the frozen models to repair an already accepted result. The next proposed
comparison is semantic necessity under execution restrictions: permission denied,
provider unavailable or acquisition budget exhausted,with unchanged observations.
The model should not equate cannot acquire with already knows. Runtime must block IO
independently even for an erroneous proposal. Retain normal admitted controls and all
six checkpoints. Numerical preregistration and executable validation must precede a
new experiment. C187 is NOT REGISTERED at this acceptance commit.
