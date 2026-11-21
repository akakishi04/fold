# C182 formal verdict — ACCEPTED VALID NEGATIVE

V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
This acceptance precedes any C183 registration. C183 NOT REGISTERED at acceptance.
Gate E NOT PASSED. C181 ACCEPTED PASS and all historical judgments remain unchanged.

## 1. Formal verdict

C182-v5e-frozen-fact-renaming / V5-E-FROZEN-FACT-RENAMING:
**ACCEPTED VALID NEGATIVE** against the unchanged zero-error/all-model/all-permutation gate.
All work completed. INTERNAL_SEMANTICS seed181003 has one error and one decision flip
at nonidentity permutation17, old-to-new zero-based mapping(2,3,1,0).
Seeds181001 and181002 have zero errors across all216108 renamed inputs each.
Seed181003 has216107/216108 correct. Candidate total648323/648324 correct
(99.9998457561%), but a single error fails the registered gate. No average-score rescue.
Do not rerun C182, retune checkpoints, drop seed181003, or change the threshold/cases.

## 2. Execution validity and identity

Execution HEAD8ee4942d7b4ec73ac65de8d6f17f59c297c6ee99.
1185/1185 focused tests passed in43.599s. Source/artifact precheck PASS.
Postcheck: protected_inputs preserved; tracked_tree clean; execution_HEAD preserved;
run_execution_valid=True. Existing C145 scalar-conversion warning did not fail tests.

Summary: runs/c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4/summary.json
Summary SHA256: 06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73
Canonical reconstructed summary83982bytes; exact hash match with runner output.
Uploaded log287823bytes; SHA256:
ec89e4ea2ba4ebfc68c658897c8aa03a7af410ce53741b5977d3cba8240e93ee.

Six C181 checkpoints reused; source seeds181001/181002/181003; no fresh seed/training.
311040 original TRAIN/PILOT predictions replayed: all12replay records have exact
raw decisions AND max_abs_logit_difference=0.0 (registered tolerance1e-6 unchanged).
216108 transformed inputs=9396x23;1296648 predictions across six models;
648324candidate predictions;total1607688inference rows/1692batches/11844cell calls.
76historical source pins,151protected input paths,five output artifacts.
Teacher/auxiliary/acquisition/proof/evidence/network calls0. No production change.
Reported benchmark40.0362668s is environment-specific, not a speed claim.

Outputs preserved:
- renaming-plan.json:10276bytes,df6ed6dbd743a4fce535966fe777fcafe6e43d3c61fa9b211d2316623e0bc13a
- frozen-replay.json:2085bytes,a535ad72dbc73ba70d053a19072f5e5743c1195d0515c86a59f42f3cc8490860
- transform-audit.json:5131bytes,caf92aef10696a0674674d9e1283cc4b17b70d74be14317a0b5ed6d0ecd33c59
- renaming-results.json:603262bytes,72d8d75594fcd33df4d5b7962cc4ef9002380ce898e900a171201e28449aa903
- renamed-predictions.npz:9576402bytes,547c714453caf40b1f5d8d5335c19a73a2b020816aec2c2399533f6cc2655f1d

Reviewer reconstructed summary and recalculated all60confusion-based tables including
six groupmacro means;checked group/count sums,six error-exchange tables,138record
coverage/sums,12identity replays and the unchanged gate. No discrepancy.
The five separate artifacts,original data and checkpoint bytes were NOT supplied to
the reviewer. No independent local model replay or1185test rerun. A local git clone
failed DNS resolution; this was not a checkout. Do not conflate arithmetic audit with
checkpoint replay or independently verified error-row identity.

## 3. Metrics and error boundary

|Seed|Arm|Errors/216108|Decision flips|Ordinary accuracy|
|---|---|---:|---:|---:|
|181001|FINAL_ONLY|54828|8115|0.7462935199067133|
|181001|INTERNAL_SEMANTICS|0|0|1|
|181002|FINAL_ONLY|55768|169|0.7419438428933681|
|181002|INTERNAL_SEMANTICS|0|0|1|
|181003|FINAL_ONLY|54330|6667|0.7485979232605919|
|181003|INTERNAL_SEMANTICS|1|1|0.9999953726840284|

The candidate error is false SUFFICIENT: label NEEDS_OBSERVATION(1),prediction0.
It belongs to semantic group3 and missing-count1. Aggregate candidate181003 confusion
is [[155112,0],[1,60995]]. It occurs once, not23different failures.
All other68candidate model/permutation cells have zero errors. All138including controls
complete. The row index,formula,observed values and logit margin are not present in
this console summary; recover them from the hashed saved prediction NPZ and source
rows before naming a concrete counterexample. Do not invent them from the group ID.
One-based renaming is1->3,2->4,3->2,4->1; records move together with references.

## 4. Scientific interpretation

Frozen C181 base -> meaning-preserving renaming -> unchanged learned inference
-> one incorrect necessity decision. Broad measured robustness is strong but exact
invariance is false. C181's original perfect-score result remains valid in its scope.
A naming/layout change can cross a decision boundary despite identical logical meaning.
This is not evidence that the whole intermediate-supervision improvement disappeared,
nor permission to adopt a perfect autonomous information-acquisition policy.

## 5. Confounds and next boundary

The transform preserves bound leaf information; it changes both numeric leaf fact IDs
seen by the shared cell AND the positional fact table seen by the final readout.
The current result does not isolate which route caused the error. Do not dismiss it as
roundoff without margins and matched replay, or infer the bypass is uniquely responsible.
C180 studied removal of the bypass with retraining; that differs from frozen path
attribution on a C181 checkpoint.

All tasks reuse four inspected DEVELOPMENT semantic groups; permutations/models are
correlated,not independent samples. No untouched holdout,larger/repeated-variable logic,
language,live target selection or Gate E claim. Freeze all six checkpoints and all
outcomes. First resolve this counterexample without fitting or repairing a candidate;
a later registration must state the diagnostic question and its non-adoption boundary.

## 6. Handoff

C182 ACCEPTED VALID NEGATIVE; C181 ACCEPTED PASS; no active next experiment until a
separate C183 preregistration. Preserve environment,protected C37/fixture and history.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate research tracks.
