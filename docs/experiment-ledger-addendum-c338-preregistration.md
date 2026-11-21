# C338 preregistration -- paired supplied-value support training

Date: 2026-10-25 Japan time.
Experiment: C338-v5b-value-support-training. Stage: V5-B-VALUE-SUPPORT-TRAINING.
Acceptance base:8b7cdc54a7a735320617e1650cd349efb5850288.
C337 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C335 remains VALID NEGATIVE.
Gate F NOT PASSED. Source publication is not activation. Require committed-byte
post-authoring review PASS and a separate ACTIVE registration before a user command.

## One question

Does extra TRAIN supervision of probability mass on the two supplied values reduce
outside-pair errors while retaining correct within-pair binding and all old gates?
C337's inspected seed335002 HOLDOUT strata show both outside-value competition and
incorrect within-pair ranking. This motivates a loss intervention, not a claim that
loss weighting caused those failures. No claim that support supervision suffices.

## Exact single changed variable

Both arms use the unchanged native mean/last readout during TRAIN, evaluation and
saved replay. No alternating/first_mean policy, new attention, parameters, input
channel, decoder, candidate selector or ensemble is added.

For logits z over all256 byte classes, queried target t, and the TWO distinct values
S already present in that TRAIN example, define batch means:
CE = mean(logsumexp(z_all256) - z_target), implemented by ordinary cross_entropy.
SupportNLL = mean(logsumexp(z_all256) - logsumexp(z_S)).
Control native: L=CE. Candidate support_loss: L=CE+SupportNLL.
The coefficient is fixed at1.0 for the candidate and0.0 for the control; no sweep.
Alpha0 returns the original cross_entropy tensor exactly. Both arms compute the
support term for telemetry, but only the candidate includes its gradient.
Compute directly in float64 logit space; reject nonfinite source/derived values.
No clipping of loss, chosen epsilon, probability flooring or binary-only conversion.

CE decomposes as SupportNLL + conditional within-pair CE. Thus the candidate doubles
the support part, not an independent new information source. The support term alone
does not identify which supplied value is queried. Its sorted two-class labels are
query/order invariant and use only TRAIN row values0..3, encoded48..51. They never
enter model.forward or inference. The larger objective can change clipping and
optimizer updates; do not claim equal FLOPs, gradient norms or effective learning
rate merely because model-forward/update counts match. No learning-rate compensation.

## Fresh paired cohort and fixed data

Seeds338001..338005; order seeds338101..338105. Five paired fresh initializations,
ten models. Construct both members of each pair before fitting either; require
identical full initial state/core fingerprints and disjoint parameter storage.
Do not resume, fine-tune, select or discard C335/C332 saved models or seed335002.
Do not select a favorable new seed after evaluation.

Canonical logical data remain192TRAIN/96HOLDOUT, fixed SHA:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Two distinct values are drawn from0..3; HOLDOUT pairs(0,2),(1,3),(2,0),(3,1).
Keep data IDs, row order, all original/interior prompt bytes and the split unchanged.
Preparation reuses C332/C329/C326/C324 TRAIN-only tables and canonical validators.
Support labels are192x2 int64, sorted, distinct,0..3-byte-valued, and target-containing.
They are included in the training-input fingerprint and saved trace support hash.

Use unchanged C326 batch4 family allocation and two_to_four event schedule,1200events
repeated twice. Same paired events/masks/targets/rates/FIT_RNG612000. TRAIN name
families original2,3,4 and interior4 only; no original5/6 exposure. Effective per-row
exposures remain200/200/100/100 respectively. No intermediate evaluation/selection.
2400updates/model; one unchanged core_slow AdamW optimizer throughout both cycles,
noncoreLR.005/coreLR.0005,betas.9/.999,eps1e-8,weight_decay0,globalgradclip1.
Require post1200 weight/optimizer hashes to match pre1201 continuation. No reset.

Native architecture14256parameters/core3328,64slots,CPUfloat64,2threads. Every TRAIN
step is one native forward, two query projections, one backward and optimizer step.
The existing native readout wrapper validates provenance; only loss is changed.
Save detached deep-copied final states; finish ALL fitting before scientific scoring.

## Evaluation, diagnostics and fixed gate

Every final state is loaded/evaluated/reloaded/replayed with native_before. Preserve
all114raw views:original1..6/interior4,TRAIN/HOLDOUT,allprofiles/languages,normal and
masked controls. Require <=1e-9 raw drift AND exactargmax via unchanged replay helper.
State/data/prompt fingerprints must remain unchanged. Original1 stays descriptive.
No provided-pair restriction or label-assisted answer replacement in evaluation.

Use unchanged C331/C324 original/interior scorers and HOLDOUT paired contrasts.
Existing local thresholds remain accuracy.90,query-pair.80,evidence-drop.35,
query-drop.35,both-order.80. Retain rescued/regressed answers and pairs per domain.
For all six gated domains, use accepted C337.audit_logits only as OFFLINE scoring
on raw normal HOLDOUT logits. Report correct/wrong_observed/absent_digit/
outside_catalog counts,288answers/domain/state. Outside errors are the last two
categories combined; outside_catalog is not synonymous with a nondigit.

C338 PASS requires ALL of:
1. All5 candidate states pass complete original2..6 AND interior gates.
2. For EVERY paired seed AND EACH of those six domains, HOLDOUT correct-answer and
   both-query-correct counts do not decrease, and outside-pair errors do not increase.
3. Across the fixed cohort/domains, correct answers AND both-query-correct pairs
   strictly increase AND outside-pair errors strictly decrease.
No pooling of short domains hides local harm. Exact ties are allowed per domain,
but a saturated or tied cohort with no strict improvement is VALID NEGATIVE.
These are new preregistered C338 criteria, not a revision of earlier gates/verdicts.
A decrease in outside errors alone is not PASS if wrong-observed errors replace them.
No hypothesis-specific numerical benefit is required for execution validity.

## Fixed workload and author/native preflight boundary

10training models+10evaluation model instances;10final states;24000updates/backward
calls/optimizer steps;1152000TRAIN row presentations.20saved-state evaluation/replay
passes*171forwards=3420evaluation forwards. Total27420model forwards,1480320rows,
109680core forwards,54840query projection calls,20saved-state loads,1bundle load,
1new checkpoint bundle write. Scientific networkcalls0. Raw-logit payload672399360
bytes is not serialization total or peakRAM. Extra loss reductions are not free.
Semantic-check tensor reads,software tests and preflight are excluded from cohort work.

Separate discarded native preflight validates all5schedules, sorted support labels,
and native original/interior English/Japanese loss/backward paths with nonzero
reader output weights.6forwards/12rows/4backward/0optimizer updates. Both arms have
identical native outputs in this probe; objective gradients may differ. Probe
weights are checked unchanged and never reused as a scientific initialization.

## Immediate C337 parent and complete byte protection

Accepted execution:aae0a83742d56df9dcfe059f3b6ad81e26798505.
Publication:38b129ee5569b288c52539eb31caa0853381f2e5.
Folder:runs/c337-value-support-bca3d06eebf74f74a1b1038c5cb38627/.
Primary415784b8d7d468a6d3f102775e29ae887fcb01ebc5718abef35dc9439fd6a0b8.
Envelope12df1d44c5973f9bb5ac7bd2ce766b4bf1fb5204bb3d064c44d6a9f09c7b237e.
Require exact diagnostic schemas,PASS,complete flags,883/4827matching maps,
6122regression tests,all4827final uncached rereads and preserved C335negative.
Pin C337executor5ac766d9721b1a563fa137fbdd40625b0e4117b6 and benchmark
 e9f9249fdad6114d4943a6ee0aa1d0cd66a08227 before importing its helper chain.
Helper bridge is a dictionary, not an old tuple.

Reconstruct inherited maps with unchanged C337.snapshot. Add ALL463parent outputs:
4scienceJSON+primary+envelope+457regression proofs(3+227JSON/logpairs).
Validate full parent ordered IDs, test success/PID/log evidence, byte hashes.
New protection889sources=883+6;5296inputs=4827+463+6. Exact finite native
max_files=INPUT_COUNT=5296. No default4096,eviction,unlocked fallback or proof omission.
Keep read leases through scientific work, initial independent hashes and ALL5296
final uncached rereads. Accepted source/test/contracts/logs are never edited.

Immediate semantic dispatch is C337.semantic_recheck(C337science,C336science,
C335science,C329data,C336validation_summary,read). Load the protected C336 summary
from its own summary.json and verify the accepted C337.PARENT_SUMMARY hash; C337's
new summary does NOT embed the older full validation_summary. No stale field guess.
Parent reconstruction runs under no_neural and does not replay historical models
or recurse into older semantic bodies. All ancestor bytes remain protected.
Training context/data use unchanged C332/C329/C324 helpers. Direct/lazy modules are
inherited source pins, including C337audit_logits and its C336profiles dependency.

## Full regression, artifacts, route and stopping

Preserve all6122ordered parent IDs, SHA
3f5e74b88652cf88f37150b087d52ef6f6086138f9b05ccafc4674893d84d6ca.
Append48own tests:6170selected/228modules,6171before the sole inherited exactC204
mutable-ACTIVE exclusion. No new exclusions/skips/cached successes or automatic retry.
Fresh sequential ordinary module processes,accepted C330R1.2 direct/immediate-child
PID evidence and exact begin/endmarkers. Generic module ABI binds NEW C338HEAD/plan.
Child owns guard/plan/CLI;new plan/evidence schemas fold-c338-regression-plan-v1 and
fold-c338-regression-v1. All6170must pass before scientific fitting.

Six own files:benchmark,executor,48tests,runner,launcher,this contract.
Six science outputs:experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Checkpoint schema
fold-c338-trained-models-v1 and evaluation schemafold-c338-evaluations-v1 bind ordered
seed/arm identities, state fingerprints, native evaluation policy and all raw views.
Primaryfold-c338-trained-v1;envelopefold-c338-execution-envelope-v1 retain889/5296maps.
Hash/size-bind all6outputs around saved reconstruction and before final records.
Fresh verifier checks parent/new module proofs and saved metrics without retraining.
It does not independently replay24000optimizer steps; traces are evidence, not that claim.

Route:active_v2->invoke_c338->run_c338->c338_execution->native locks/parent snapshot
->immediate C337semantic reconstruction->discarded native preflight->6170isolatedtests
->10fresh models trained->native saved evaluation/replay->saved reconstruction
->5296final uncached rereads->independent fresh verifier->console-onlypublication.
Localruns/c338-support-training-<id>/science with228moduleJSON/logpairs and regression
plan/evidence/result. Only console to c338/latest.log+latest.json. Print every200updates,
all5paired comparisons and all10state results including outside-pair counts.
Future successor must retain459regression proofs+8science/summary/envelope=467outputs.

Status FAIL with valid persistence/fresh verification is a VALID NEGATIVE, not a
retry reason. Any source/input/test/PID/nonfinite/gradient/pairing/replay/schema/
semantic failure is INVALID SAMEC338. Publication-only failure repairs publication,
not training. Stale/published guards are not bypassed by changing ExpectedHead.
NoC339,GateF,productionadoption,CI,paidservice,reinstall or data deletion authorized.

## Mandatory committed-byte author review

Reread all6committed files through EOF, match local tested Git blobs, rerun48tests
normally and with CP932-default-open emulation. Audit compile/import/UTF8/noNUL/
undefined globals,manifest/counts,actual loader IDs,source-level parent dispatch and
loss/scientific-variable boundaries. Detect no-aux and target-only-support mutations.
Test actual child optimize/train wrapper with a small Torch model for2400updates per
arm against an independent reference. This is NOT native FOLD learning evidence.
Exercise real child analysis/snapshot/worker/fresh-verifier paths with explicit
synthetic legacy/scorer/lock collaborators. Local-only verbatim C267dataset,
C336profiles and C337audit_logits extracts support targeted tests; never commit them
or claim complete historical modules/full6170Windows execution. Native PowerShell
AST checks remain mandatory via dispatcher,launcher and runner before logging.

Manifest SHA256:d2c6bcbadfa3f04c35cad137fece59c9499f8b5de37589425479b05376b9fe73.
