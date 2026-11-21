# C339 preregistration -- saved paired support transfer

Date: 2026-10-26 Japan time.
Experiment C339-v5b-saved-support-transfer; stage V5-B-SAVED-SUPPORT-TRANSFER.
Acceptance base 928bc539f83a22584e71e99adac7f5031bd480d0.
C338 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C340 NOT REGISTERED.
Source publication is not activation. Require committed-byte post-authoring review
PASS and a separate documentation-only ACTIVE registration before a user command.

## One question

Where does support-loss training improve or degrade supplied-value support versus
within-pair binding across TRAIN/HOLDOUT and name domains? C338 did not improve its
fixed cohort: original6 correct1389->1375, outside errors27->49; original5 correct
1426->1423, outside2->7. Original2/3/4/interior4 remained perfect in normal HOLDOUT.
These observations motivate an offline transfer diagnosis, not a new loss sweep.

## Fixed cohort, inputs and predictions

Use ALL ten C338 states: seeds338001..338005, arms native/support_loss. Preserve all
original2..6/interior4, both splits, both languages and all three profiles/domain.
Original1 stays outside this diagnosis exactly as in the six C338 gated domains;
parent semantic reconstruction still checks its saved views with all other views.
No fitting, optimizer, model forward, checkpoint selection, seed removal, decoder,
new prompt, candidate filter, prediction repair or change to an earlier gate.

Canonical data are192TRAIN/96HOLDOUT with frozen SHA
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Rows contain two distinct values from0..3, encoded as byte classes48..51. Preserve all
12ordered pairs across the existing split. HOLDOUT pairs remain(0,2),(1,3),(2,0),(3,1).
No binary-only fixture, altered target, new split or omitted language/profile.

C338 evaluations.pt has fold-c338-evaluations-v1, records ordered by seed/arm, and
state_sha256/evaluation_policy/raw/receipts. Both raw evaluation and replay exist;
policy is native_before. Parent reconstruction binds states to saved weights/traces
and validates all114views. Child separately checks every selected normal-view replay
within1e-9 and exact256class argmax. No second model run is performed.

## Measurements and numerical meaning

Reuse accepted C337.audit_logits without modifying it. Actual prediction remains
first-index torch.argmax over all256 classes. Report correct, wrong_observed,
absent_digit (unprovided0..3value), outside_catalog (including digits4..9, not just
nondigits). Preserve exact ties in target-other and max(supplied)-max(outside) margins.

Add two descriptive negative log-likelihood components for each saved normal answer:
- supportNLL = log(1+exp(logsumexp(254outside logits)-logsumexp(two supplied logits))).
- withinNLL = log(1+exp(other_supplied_logit-target_logit)).
These sum mathematically to ordinary target cross-entropy. Implement the softplus
identity with torch.logaddexp(0,x), without the threshold approximation in the default
functional softplus. Use float64; reject nonfinite sources, gaps, margins, components
and paired differences. No probability floor, epsilon tie, clipping or score correction.
Underflow to floating zero is not replaced with a positive floor. Means use math.fsum.

The supplied pair and true target are labels for retrospective measurement only,
never a model input or inferred answer restriction. WithinNLL is not corrected model
accuracy. Margins can change with score scale; support/within NLL changes are also
not proof of a particular internal mechanism or independent causal interventions.

For every seed/domain/split/profile/language, pair the SAME row_id, target and other
value across native and support_loss. Save4x4 answer-kind transition matrices and3x3
exact-sign transitions for both margins. Report rescued/regressed answers, and
candidate-minus-native mean changes in both NLLs and both margins. Positive NLL delta
means worse; positive margin delta means higher margin, not automatically correctness.
Retain offsets, ties and unfavorable transitions rather than just net improvement.

## Reconciliation and integrity PASS

Reconstruct all60C338 normal HOLDOUT support partitions (10states*6domains), exactly
matching answers/correct/wrong_observed/absent_digit/outside_catalog. Recompute all30
paired HOLDOUT contrasts, including correct counts, both-query-correct pairs,
rescues/regressions for answers and pairs, gains and outside_gain. Group query pairs
by language/entities/values/permutation, then the two entity queries, matching C324.
Do not treat adjacent arbitrary rows as query pairs in production.

Validate all720strata and360paired strata, row/column marginals, sign marginals,
rescue accounting, contrast support/count binding and finite means. Reconstruct all
four saved child outputs byte-canonically from the unchanged source archive again.
PASS means diagnostic integrity only. Parent candidate_gate=false/eligible0 is
preserved. Benefit,tie,harm are all acceptable diagnostic outcomes, not retry reasons.
No statistical independence claim for repeated names/profiles/seeds; no Gate F or
production adoption follows. No inference-time support mask is introduced.

## Workload and artifacts

10saved states,51840normal answers,25920paired answers,720reporting groups,
360paired groups,30parent contrasts,60parent support partitions. New scientific
model forwards,train/gradient/optimizer steps,state loads,new checkpoints,network0.
Reading tensor archives and the parent's saved checkpoint bundle is evidence work,
not new model inference; parent validation/software tests are separately scoped.

Four child files: audit-plan.json, answer-components.json, paired-transitions.json,
validation-summary.json. Per-answer details include all row identities and both
components; summary includes all strata, transitions and reconciled parent contrasts.
Primary schema fold-c339-diagnostic-v1; envelope fold-c339-execution-envelope-v1.
All four files are hash/size-bound around reconstruction and before final records.
Only console logs are published; tensors/data/full artifacts remain local under runs/.

## Accepted parent and complete protection

C338 execution f81a49e383e78ff503a4e4c6fe1156e7a8b75849.
Publication 579edc8f611cfc0a513ce52661582de70f8a8b50.
Folder runs/c338-support-training-5d84afb5a34c4dc0a291ca0f35b24829/.
Primary67e369808641a781dd144084a4e1a77d8347a07675740b8c3c694eaedbdf3137.
Envelope11977e359dbb65236803fb7eaa1d085728a72d27a582dcc2d76d01906e3329e5.
Require exact trained/execution-envelope schemas, statusFAIL with execution valid and
capability gate applicable, candidatefalse/eligible0,889/5296matching maps,6170receipt,
all5296final uncached rereads and saved semantic completion. Do NOT require a parent
PASS merely because the child is a diagnostic. Pin parent executor
3cc1dd228baab13a1feef96d38b8213ff53d7080 and benchmark
53185474d560e2961ff05b5484da84c8f27c956f before import; retain dictionary helper bridge.

Reconstruct inherited maps with unchanged C338.snapshot. Add ALL467parent outputs:
6science files+primary+envelope+459regression proofs(3records+228JSON/logpairs).
Validate all parent test IDs, success/PID/log proofs and bytes with accepted helpers.
New protection895sources=889+6;5769inputs=5296+467+6. Exact finite native
max_files=INPUT_COUNT=5769 is mandatory. Keep native R4 leases, independent initial
hashes and ALL5769final uncached rereads. No eviction/default4096/unlocked fallback.

Immediate semantics is the actual FOUR-argument trained-parent signature:
C338.semantic_recheck(C338science,C329data,cx,read), under no_neural. This checks
C338weights/traces/all raw views and its negative summary without fitting or forward.
Do not copy the old six-argument C337 diagnostic loader. Canonical data/prompt
validators are unchanged. Do not recursively rerun older semantic bodies; all older
bytes remain protected. Deciding direct/lazy modules include C338/C332/C329/C324 and
C337audit helpers, already inherited in source pins. No missing-dependency shortcut.

## Full regression and execution boundary

Preserve6170ordered parent IDs with SHA
6f9f4fb4184d9ac262bf88eb7ec49e6ee0cd5099754fbb09545461dbc147d89b.
Append32own tests:6202selected/229modules,6203before the sole inherited exact C204
mutable-ACTIVE exclusion. No new exclusion,skip,cached successes or automatic retry.
Fresh sequential ordinary module processes use accepted C330R1.2direct/immediate-child
PID validation and canonicalbegin/endmarkers. Generic module ABI binds NEWHEAD/plan.
Child aggregate schemas fold-c339-regression-plan-v1/fold-c339-regression-v1.
All6202tests pass before child diagnosis. A module-level OK is not completion.

Route active_v2->invoke_c339->run_c339->c339_execution->native locks/complete parent
snapshot->immediate C338semantics->6202isolated tests->saved_support_transfer
->saved_diagnostic_reconstruction->5769final rereads->independent fresh verifier
->console-only docs/experiment-run-logs/c339/latest.log+latest.json publication.
Local runs/c339-support-transfer-<id>/science plus229moduleJSON/logpairs and regression
plan/evidence/result. Successor must retain461moduleproofs+6science/summary/envelope=
467parent files. Print720strata/360transition records; no scientific training steps.
Complete requires persisted_support_transfer PASS,execution_envelope_verified,
run_execution_valid=true and successful publication. Parent negative remains normal.

Source/input/test/PID/nonfinite/replay/identity/reconciliation/semantic failures are
INVALID SAMEC339; noC340. Publication-only failure repairs publication, not diagnosis.
Stale/published guards must not be bypassed by using the publicationHEAD. No CI,
paidservice,reinstall,artifact deletion,old-source rewrite or accepted model retraining.

## Mandatory post-authoring review

Reread all6committed files through EOF, compare local tested Git blobs, rerun32tests
normally and with CP932-default-open emulation. Check UTF8/noNUL/compile/import/free
names,manifest/counts,actual loaderIDs,4argumentparentdispatch and source protection.
Use real production analyze/loader/writer/reconstruction/snapshot/worker/verifier
paths with explicitly synthetic logits/parent summaries/PID evidence/OS leases.
Canonical fixture must equal C267.dataset and its frozen hash, including nonbinary
values. Local-only verbatim C267writer and C337pure-helper extracts may support a
targeted Linux test tree; never commit them or claim fullhistorical/native validation.
Mutation controls must detect a removed support component and reversed transition
orientation. Native PowerShell AST checks remain mandatory through user/dispatcher/
launcher/runner before scientific logging. No execution command before review PASS.

Manifest SHA256:3f3380eac1a0e5d0c076825081c10edfa86bed75e02b2c1b5ee23ebf21dc42f1.
