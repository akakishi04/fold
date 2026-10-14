# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 ACTIVE / NOT YET JUDGED. C325 NOT REGISTERED.**
C324 is the sole ACTIVE paired interior-coverage training experiment. No C324
scientific execution or result has yet been accepted. Do not rerun C323.
C322 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C321 remains ACCEPTED VALID
NEGATIVE (interior-order0/5); C320 remains bounded ACCEPTED PASS. Earlier verdicts unchanged.
Latest accepted execution:1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4.
Latest accepted publication:e434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
C323 acceptance commit:88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.

## C323 accepted evidence

Acceptance:docs/experiment-ledger-addendum-c323-c324.md.
Summary:runs/c323-v5b-fact-order-f1b710e74fbe495aba6410d0d9530248/summary.json.
Summary SHA256:fcc87597395300e45eacabaa94b87b6910093669532279f9ed6c67ec3f84af1f.
Log SHA256:ba9f788c326b6c4bc3a86a9d6bde542410fffa73d50c0d961707fd2a3980b8f8;
1072473 bytes, uploaded bytes independently matched metadata. Own24/full5293 PASS;
regression1214.580s,failures0/errors0,exit0;source784/protected1478;
persisted_fact_order PASS,tracked tree clean,run_execution_valid=True.
Independent console reaggregation:240 groups,4 matched totals,4320 counterfactuals,
8640 question pairs,17280 answers. No scientific rerun.
Old4 both arms4320/4320 correct. Interior mean_last2211/4320 correct,
first-both15/1080,last-both113/1080,all-four answer lock814/1080.
Interior last_only2292/4320,first-both29/1080,last-both95/1080,lock809/1080.
Output-class lock dominates consistent first/last following in this cohort;
not a claim that all logits are query-invariant or an internal causal explanation.
Retain the historical runpy warning. C323 PASS is diagnostic integrity,not improvement.

## Active C324 — equal-budget interior-order TRAIN coverage

Experiment:C324-v5b-interior-coverage-training.
Stage:V5-B-INTERIOR-COVERAGE-TRAINING.
Registration:docs/experiment-ledger-addendum-c324-preregistration.md.
Design:docs/v5b-interior-coverage-training-v0.1.md.
Review:docs/c324-post-authoring-review.md.
Source/preregistration commit:926659460e7d93207122e8d19e5b26bb3f578ac8.
Acceptance base:88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.
post_authoring_review = PASS.
Review target HEAD:926659460e7d93207122e8d19e5b26bb3f578ac8.
Use the exact activation HEAD supplied with the launcher command,not the earlier
source commit. Activation changes control documentation only;all8 OWN blobs unchanged.

Question:does explicitly training the C321 interior-order distinction improve
HOLDOUT binding while retaining original name tasks,at the same architecture/budget?
Arms:original/interior4;both native mean_last. Change only three length4 TRAIN tables;
keep length2/3 strings,logical rows/targets,paired initial weights,schedules,optimizer,
steps,language/order/value split fixed. No pretrained-state reuse or last_only arm.
Fresh seeds324001..324005;paired orders324101..324105. Ten14256-parameter models,
3328 core parameters,64slots,width16,CPUfloat64,2threads,deterministic.
1200 steps/model,48rows/step;each TRAIN row100 exposures per length2/3/4.
C315 schedule;C308 core_slow AdamW(.005 other/.0005 core),ordinary meanCE,clip1.

Fixed gate:ALL5 candidate models pass all interior local/masked/both-order criteria
AND original2..6 retention AND strict positive paired HOLDOUT correct-answer count
AND strict positive paired HOLDOUT both-query-correct count. Original1 descriptive.
Existing thresholds:accuracy.90,querypair.80,evidence/querydrops.35,twoorder.80.
Each seed/arm HOLDOUT contrast288 answers/144pairs;report rescues and new errors.
Success is explicitly trained-template/held-out-value learning,NOT frozen unseen-name
transfer. Failure does not prove structural impossibility. Gate F stays NOT PASSED.

## C324 protection, outputs and workload

Before parent dispatch:50 ordered hashes C323..C274. Parent is C323 JSON diagnostics,
not a model bundle. After recursive verification use C319 JSON at parent index4,
check canonical hashes and C321 renderer semantics. TRAIN projections only enter fit.
Preserve784 parent pins/1478 inputs;add8 OWN and5 C323 outputs =>792 pins/1491 inputs.
Direct helper and model-class dependency protection required;no omitted-path waiver.
Manifest:b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.

Scientific total:10 models,12000 updates,576000 training rows,15420 model forwards,
904320 total row presentations,61680 core forwards,10 checkpoint state reloads,
1 child checkpoint bundle load for replay,1 new bundle write,0 network calls.
Eight artifacts plus summary;raw logits336199680 bytes excluding archive/fit overhead.
Checkpoint replay:full tensor schema/digest/fingerprint,logits<=1e-9,exact256-way argmax.
No-neural saved verification reconstructs every JSON/summary and checks input/output
hashes/sizes. A finite gate FAIL is saved and can be ACCEPTED VALID NEGATIVE.

## Authoring review boundary and execution

All8 committed OWN files reread and Git blobs independently matched local bytes.
Local authoring own64 PASS1.075s;CP932-default-file-open emulation own64 PASS1.213s;
LinuxPython3.13.5/PyTorch2.10.0+cpu,explicit synthetic parent/model fixtures and tiny
2-update arithmetic control. FourPython sources/3runner here-strings compile;
free-global audit clean. This is NOT the real Windows50-parent/full5357 run.

Regression:own64=component20+benchmark44;210modules,5358loaded,5357selected.
Only inherited C204 mutable-state exclusion remains;no historical-test edits.
Real loader checks actual unique ordered test IDs and runs one process before science.
No skipped tests,parallel fixture shortcuts,automatic retry or promised speedup.
Dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile path preserved.
50 fixed paths checked;postcheck argv=output,HEAD,50parents (argc53,parents at3).

Use explicit PowerShell7,ff-only pull,and tools/invoke_active_v2.ps1.
Expected:active_experiment=C324 ->50 real parents/792/1491 checks ->native TRAIN
forward/backward probe ->own64 ->full5357 ->authoring_runtime_preflight PASS ->
10 paired fits with200-step progress ->both-task evaluation ->10 checkpoint replays
->persisted_training_evaluation PASS ->run_execution_valid=True ->log publication.
Scientific execution has not run in authoring. Any preflight/error/SKIPPED stops;
fix sameC324 and do not startC325. Log-only push failure does not authorize retraining.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-C324-activation:docs/handoff-history/c324-pre-activation.md.
Git blob:bd744641aba2033c6679a340fe081225c7fcb90b.
Component-only progress:docs/handoff-history/c324-component-authoring-progress.md.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
