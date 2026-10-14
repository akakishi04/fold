# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 ACTIVE / INVALID ATTEMPT RECOVERY. C325 NOT REGISTERED.**
C324 execution at47ccd303f4382b7938db639e86aeb151e1f83af1 = INVALID EXECUTION.
recovery_action = NATIVE_DIAGNOSTIC_R2
The sole current action is bounded native-crash diagnosis, NOT a scientific rerun.
Do not rerun C323, start C325 or retry the old full C324 command.
All earlier verdicts unchanged. C321 remains ACCEPTED VALID NEGATIVE.

## C324 R2 - actual native failure

Failed scientific execution HEAD:47ccd303f4382b7938db639e86aeb151e1f83af1.
Published failed log commit:68397de27b4c538ddbd22dc2209fddb7afbc2409.
Metadata:976635bytes;SHA2568a5e28af87430010931afef2b2da3b61590f32930bee2967daff37c8db6a3271.
Read remote beginning and final sections;metadata agrees with the user's receipt.
No independent whole-log SHA256 recomputation is claimed.
Immutable failed evidence:docs/experiment-run-logs/c324/attempts/68397de27b4c538ddbd22dc2209fddb7afbc2409/latest.*.

Initial parent artifact verification8635.121s;native gradient preflight PASS;
own64 PASS5.618s;full5357 PASS1074.995s,failures0/errors0,exit0.
Execute starts parent_artifacts BEGIN again and crashes before child fitting:
Fatal Python error:_PyEval_EvalFrameDefault:Executing a cache.
Frame:model_c242_balanced_recombination.py,parent_module,line???,invalid frame.
Native exit=-1073740791 /0xC0000409;run_execution_valid=False.
This is neither the earlier R1 operational skip nor a finite scientific negative.
The underlying trigger is not known;do not assert a disk-cache/PyTorch/CPU defect.

## Current R2 implementation and review

Recovery contract:docs/c324-native-crash-recovery-r2.md.
Review:docs/c324-recovery-review-r2.md.
Source/review target HEAD:8f7fec8371cfa5792b89587fa078ff2b6aab80fb.
post_authoring_review = PASS.
Scope:diagnostic software readiness,NOT native-failure repair or science PASS.
The final review-record HEAD in the user command is the operational execution target.

Changed only operational routing and new diagnostic/test/documentation files.
No fold_lm/fold_reasoning/tests_lm scientific source changed from the failed execution.
Current invalid-state routing:active dispatcher ->invoke_c324.ps1 ->
invoke_c324_native_diagnostic_r2.ps1 ->c324_native_diagnostic_r2.py ->STOP.
All launchers require ParseFile and branch/HEAD/tracked-tree/recovery guards.
The normal scientific body and all50 parent paths are preserved but are NOT run now.

The diagnostic runs two bounded child processes:existing cache lookup with-B;
then a fresh empty pycache_prefix with-B. Preserve existing pyc;do not delete or
reinstall. Compare loaded C242.parent_module code with freshly compiled source,
call the import-only helper4096times and C324.context3times per worker;capture
interpreter/build/GIL/library versions,stdout/stderr and native exit codes.
No full-parent verification,no model forward,no optimizer steps,no full regression.
Each worker has120s control timeout and10s heartbeat;no promised duration/speedup.
Exit0/diagnostic_completed=True does NOT mean the original crash is fixed.
Both outcomes are retained even if one fails;no automatic science retry follows.

All four committed executable/test files reread and their complete Git blobs matched.
Authoring tests:24unit+healthy subprocess+stale-cache subprocess=26passed.
LinuxPython3.13.5/PyTorch2.10.0+cpu;synthetic repository modules,not real parent archives.
No Windows end-to-end or PowerShell AST execution is claimed;AST guards stay required.

## Next user action and transport

Use the ordinary active-dispatcher command at the supplied final recovery HEAD.
Expect execution_role=C324-R2-NATIVE-DIAGNOSTIC,scientific_execution_requested=False,
existing_cache/fresh_source_cache_path outcomes,diagnostic_completed=True,
action=STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY,then standard log publication.
The user can report finished;read current remote C324/latest.* for diagnosis.
Its metadata.execution_head is now the DIAGNOSTIC execution HEAD,not scientific47ccd.
Preserve the failed scientific attempt separately. Never ACCEPT this diagnostic as
scientific C324 PASS or VALID NEGATIVE. A worker fatal/timeout is diagnostic evidence;
a launcher skip means no diagnostic ran. Neither authorizes C325 or blind repetition.

## Unchanged scientific contract - retry not yet authorized

Experiment:C324-v5b-interior-coverage-training;stage:V5-B-INTERIOR-COVERAGE-TRAINING.
Preregistration:docs/experiment-ledger-addendum-c324-preregistration.md.
Design:docs/v5b-interior-coverage-training-v0.1.md.
Original registration source926659460e7d93207122e8d19e5b26bb3f578ac8;R1source04e959b6164fe71981720f80fa788d26c169621d.
Original/interior4 arms,both native mean_last;only length4 TRAIN templates differ.
Fresh seeds324001..324005,orders324101..324105;10models of14256parameters,
64slots,CPUfloat64,2threads,1200steps/model,48rows/step;learning rates unchanged.
ALL5 candidate interior and original2..6 gates plus strict paired HOLDOUT gains.
Existing thresholds.90/.80/.35/.35/.80;no new seed search or relaxed thresholds.
50parents,792source pins/1491inputs,own64,210modules/5358loaded/5357selected.
Only inherited C204 mutable-state test exclusion;no new exclusions.
Manifest:b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
Scientific work12000updates,576000training rows,15420forwards,904320row presentations,
61680core forwards,10state reloads;checkpoint and saved-logit reconstruction required.
A later valid finite negative is retained;current fatal is not capability evidence.

## Latency priority

User requested shorter startup beginning with C325. Now measured:the first parent
verification alone took8635.121s,NOT the5357-test regression duration.
Requirements:docs/experiment-preflight-latency-followup.md and R2recovery contract.
Do not send another full multi-hour validation merely to collect runtime/code evidence.
Prioritize measured batched Git checks and equivalent deduplicated ancestor checks,
with mutation guards,reference equivalence and complete scientific regression intact.
No optimized validation cache or speedup has been activated by R2.

## C323 accepted evidence and historical state

C323 acceptance:88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.
Accepted scientific execution:1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4.
Accepted publication:e434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
Details:docs/experiment-ledger-addendum-c323-c324.md.
Before R2:docs/handoff-history/c324-before-native-crash-r2.md.
Before R1/activation:existing handoff-history snapshots remain immutable.
Only the current Formal state authorizes an action.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
