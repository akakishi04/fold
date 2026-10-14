# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 ACTIVE / NOT YET JUDGED. C325 NOT REGISTERED.**
C324 remains the sole ACTIVE experiment. Retry SAME C324 after operational preflight
recovery R1. The first invocation was SKIPPED before science; no scientific C324
result exists to accept or classify as a valid negative. Do not rerun C323.
C322 remains diagnostic ACCEPTED PASS;C321 remains ACCEPTED VALID NEGATIVE;
C320 remains bounded ACCEPTED PASS;all earlier verdicts unchanged.
Latest accepted execution:1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4.
Latest accepted publication:e434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
C323 acceptance commit:88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.

## C324 current recovery — R1

Failed invocation target:dc66a0e14f2847c2e56f387864b384645351b28b.
Failure:AUTHORING_RUNTIME_PREFLIGHT_FAILED;experiment_executed=False;
execution_log_publish_attempted=False. User traceback stopped in model dependency
checking at installed .venv-py31315/Lib/site-packages/torch/nn/modules/sparse.py.
Parent precheck/TRAIN preparation preceded this point; native gradient probes,
own-test process/full regression/scientific fitting had not yet run in that attempt.
No published C324 scientific log commit exists for this operational skip.

Cause:repository-root containment wrongly classified nested-venv PyTorch as FOLD
source. The new shared classifier distinguishes active-interpreter installed
runtime package locations/namespaces from repository-owned source. Unpinned FOLD
modules/classes, unrelated venvs and local package shadows still fail closed.
No accepted source, pin count, protected count, gate, seed, workload or model changed.
Early preflight stage markers added; this is not a measured runtime optimization.

Recovery:docs/c324-runtime-dependency-recovery.md.
Current review:docs/c324-recovery-review-r1.md.
Recovery source HEAD:04e959b6164fe71981720f80fa788d26c169621d.
post_authoring_review = PASS.
Review target HEAD:04e959b6164fe71981720f80fa788d26c169621d.
Use the final review-record HEAD supplied with the retry command,not the failed
invocation target or the earlier source-only commit. Old C324 launch commands are stale.
Original authoring review remains historical in docs/c324-post-authoring-review.md.

Review scope:three changed remote files reread;whole-file blobs match locally
retested files. Own64 PASS after remote matching(1.495s);CP932 emulation64 PASS.
Real PyTorch Embedding reproduces the old rejection and passes the new classifier.
Windows-style runtime/local mixed graphs and namespace/path negatives covered.
No actual Windows50-parent/full5357/scientific-run success is claimed by this review.
The mandatory full ordered suite, parent validation and saved reconstruction remain.

## Active C324 — unchanged scientific contract

Experiment:C324-v5b-interior-coverage-training;stage:V5-B-INTERIOR-COVERAGE-TRAINING.
Registration:docs/experiment-ledger-addendum-c324-preregistration.md.
Design:docs/v5b-interior-coverage-training-v0.1.md.
Original source/preregistration commit:926659460e7d93207122e8d19e5b26bb3f578ac8.
Question:does explicitly training the C321 interior-order distinction improve
HOLDOUT binding while retaining original name tasks,at the same architecture/budget?
Arms:original/interior4;both native mean_last. Only three length4 TRAIN tables differ;
length2/3,logical rows/targets,paired initial weights,schedules,optimizer,steps,
language/order/value split remain fixed. No pretrained state reuse or last_only arm.
Fresh seeds324001..324005;orders324101..324105;ten14256-parameter models;
3328 core parameters,64slots,width16,CPUfloat64,2threads,deterministic.
1200steps/model,48rows/step;each TRAIN row100 exposures per length2/3/4.
C315 schedule;C308 core_slow AdamW(.005 other/.0005 core),ordinary meanCE,clip1.

Fixed gate:ALL5 candidate models pass interior local/masked/both-order criteria
AND original2..6 retention AND strict positive paired HOLDOUT correct-answer count
AND strict positive paired HOLDOUT both-query-correct count. Original1 descriptive.
Thresholds:accuracy.90,querypair.80,evidence/querydrops.35,twoorder.80.
Each seed/arm HOLDOUT contrast288answers/144pairs;report rescues and new errors.
Seen-template/held-out-value learning,NOT frozen unseen-name generalization.
Failure does not prove structural impossibility;Gate F remains NOT PASSED.

## Protection, workload and execution

50 ordered parent hashes C323..C274;recursive verification before C319 JSON at
parent index4;canonical data/prompt hashes and C321 renderer semantics;TRAIN only.
All784 ancestor pins/1478 inputs preserved;8 OWN plus5 C323 outputs =>792/1491.
Manifest unchanged:b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
Own64=20+44 with added recovery subcases,not removed IDs. Modules210,loaded5358,
selected5357. Only inherited C204 mutable-state exclusion;no additional exclusions.

Scientific totals:10models,12000updates,576000training rows,15420model forwards,
904320row presentations,61680core forwards,10state reloads,1replay bundle load,
1new checkpoint bundle write,0network calls. Eight artifacts plus summary.
Raw logits336199680bytes excluding archive/trace overhead.
Replay:tensor schema/digest/full fingerprint,logits<=1e-9,exact256-way argmax.
No-neural saved reconstruction and input/output hash/size postchecks stay mandatory.
Finite gate FAIL is saved for formal valid-negative judgment,not automatically retried.

Expected retry:ACTIVE C324 ->early preflight banner ->parent_artifacts BEGIN/PASS
->source/input guards ->TRAIN_tables_and_schedules PASS ->native dependency/gradient
checks ->own64 ->full5357 ->authoring_runtime_preflight PASS ->10paired fits with
200-step progress ->original/interior evaluation ->10checkpoint replays ->saved
verification ->run_execution_valid=True ->standard log publication.
Any exception or SKIPPED:stop,repair sameC324,do not proceedC325. A transport-only
log push failure never authorizes retraining. Preserve local preflight history.

## Startup latency request for next authoring

User explicitly requests shorter launcher-to-work time beginning with C325.
Requirements:docs/experiment-preflight-latency-followup.md. Prioritize measured
phase timings,batched exact Git source inventory and equivalent deduplication of
ancestor verification;keep mutation checks and complete ordered regression.
R1 provides stage visibility only. No cache/skip/parallel-fixture policy or speedup
has been activated. C325 scientific design awaits the formal C324 result.

## C323 accepted evidence

Acceptance:docs/experiment-ledger-addendum-c323-c324.md.
Summary:runs/c323-v5b-fact-order-f1b710e74fbe495aba6410d0d9530248/summary.json.
Summary SHA256:fcc87597395300e45eacabaa94b87b6910093669532279f9ed6c67ec3f84af1f.
Log SHA256:ba9f788c326b6c4bc3a86a9d6bde542410fffa73d50c0d961707fd2a3980b8f8;
1072473bytes;uploaded bytes matched metadata;own24/full5293 PASS1214.580s;
source784/protected1478;saved reconstruction PASS;run_execution_valid=True.
240groups,4matched totals,4320counterfactuals,8640pairs,17280answers;no rerun.
Old4 both arms4320/4320. Interior mean_last2211/4320,first-both15/1080,
last-both113/1080,all-four lock814/1080;last_only2292/4320,29/1080,95/1080,809/1080.
Diagnostic integrity only,not improvement or an internal causal explanation.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Before R1:docs/handoff-history/c324-before-runtime-dependency-recovery.md.
Before activation:docs/handoff-history/c324-pre-activation.md.
Only the current Formal state is authoritative;historical commands are not executable.
