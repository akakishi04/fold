# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted scientific sources/tests/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 ACTIVE / INVALID ATTEMPT RECOVERY. C325 NOT REGISTERED.**
C324 scientific execution at47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
recovery_action = PARENT_PROFILE_R3
R2 diagnostic COMPLETED;no source/cache mismatch observed in its bounded probes.
Only the R3 bounded parent-validation observation is authorized. No scientific
retry,no repetition of R2,no C325. Earlier verdicts unchanged,including C321 negative.

## Latest R2 evidence

Diagnostic execution HEAD:7ca1ce4ae287e58a16d7e13da99fd03fb76ca89f.
Diagnostic publication:3de15c5b5850c732001f21b87658a5621faf7e68.
Metadata:13208bytes,SHA2561adbf28a1975172eceed6f2b97b57c504d5093164427f6b3dec361854ac11818.
Both workers returned0 without timeout/stderr:existing_cache10.890s;
fresh_source_cache_path28.854s. Each4096 parent_module calls,3context calls,
source_matches_loaded=True,0model forwards,0training,0parent artifact verifications.
Loaded/fresh compiled code signature906d23d94088e8d5f69886f9d3208224e51dc0341ffa42fb4c0c43824addd8a6.
RuntimeGIL enabled,CPython3.13.15,torch2.10.0+cu130,numpy2.3.5.
Terminaldiagnostic_completed=True;STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY.
This is NOT proof that all pyc files are healthy or the full native failure fixed.
R2 immutable evidence:docs/experiment-run-logs/c324/attempts/3de15c5b5850c732001f21b87658a5621faf7e68/latest.*.
Reviewer read the outcomes/terminal report;no reviewer whole-log rehash claimed.
R3 rehashes the entire published local R2 log before its one child is launched.

## Active R3 operational contract

Contract/outcome:docs/c324-parent-profile-recovery-r3.md.
Review:docs/c324-recovery-review-r3.md.
Source/review target HEAD:f0598e135911bc588009dcf8fd64e9dc36493f86.
post_authoring_review = PASS.
Use the final documentation/activation HEAD supplied with the command,not the
source-only HEAD or the old diagnostic command. No C324 science is authorized.

Route:active v2 -> invoke_c324.ps1 -> invoke_c324_parent_profile_r3.ps1 ->
c324_parent_profile_r3.py -> one bounded worker -> STOP and standard log publication.
Worker calls actual unchanged C324.load_parent ONCE with the50 ordered paths.
Wall-time cap180s includes imports;10s controller heartbeat;nominal1s flushed
main-thread stack samples;depth160 cap;no locals. Existing read-only cache lookup,
no deletion/reinstall. No trace/profile hook and no verification-result cache.
Original no_neural plus explicit model-forward/optimizer/science-entry guards.
R3 uses parent tensor archives but performs no new learning or model forward.
No full regression in R3. Parent/sample/receipt failures remain explicit.
Timeout is a bounded observation,NOT scientific failure or validator success.
Sampling/GIL bias means counts are not exact call totals or unbiased time shares.
Capture retained samples even if worker times out/crashes;no automatic repeat.

Review:all4 committed file blobs matched local bytes and were reread.26software
tests passed after remote matching8.123s;LinuxPython3.13.5/PyTorch2.10.0+cpu with
explicit synthetic parents. No actual Windows/50-parent/native-fix PASS claim.
Normal scientific body and50paths remain unchanged;no scientific tree/test edits.
Expectexecution_role=C324-R3-PARENT-PROFILE,scientific_execution_requested=False,
worker_heartbeat,diagnostic_report,STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY,publish.
The user reports finished;read remote C324/latest.* and distinguish diagnostic from
scientific execution identity. Do not ask for old C323 attachments or retry blindly.

## Original invalid scientific attempt

Scientific execution47ccd303f4382b7938db639e86aeb151e1f83af1;
publication68397de27b4c538ddbd22dc2209fddb7afbc2409.
LogSHA2568a5e28af87430010931afef2b2da3b61590f32930bee2967daff37c8db6a3271,976635bytes.
First parent validation8635.121s,native-gradient PASS,own64 PASS5.618s,
full5357 PASS1074.995s. Second parent validation in science process aborts with
_PyEval_EvalFrameDefault:Executing a cache;C242.parent_module invalid frame;
exit0xC0000409,run_execution_valid=False,before child training. Cause still unknown.
Failed log archived under docs/experiment-run-logs/c324/attempts/68397de27b4c538ddbd22dc2209fddb7afbc2409/.

## Scientific contract unchanged - not currently runnable

C324-v5b-interior-coverage-training;V5-B-INTERIOR-COVERAGE-TRAINING.
Registration:docs/experiment-ledger-addendum-c324-preregistration.md.
Design:docs/v5b-interior-coverage-training-v0.1.md.
Original/interior4,bothmean_last;onlylength4TRAIN tables differ.
Seeds324001..324005,orders324101..324105;10models,14256parameters,64slots,
CPUfloat64,2threads,1200steps/model,48rows/step. Existing optimizer/gates unchanged.
ALL5 candidate interior and original2..6 gates plus positive pairedHOLDOUT answer
andquery-pair gains;not unseen-template generalization. No threshold/seed changes.
50parents,792pins/1491inputs,own64,210modules/5358loaded/5357selected;
only inheritedC204 mutable-state exclusion. Full suite remains required for a
later authorized science run;no cached regression PASS adopted by this diagnostic.
Manifest:b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
Science12000updates,576000training rows,15420forwards,904320row presentations,
61680coreforwards,10checkpoint reloads. No scientificC324 result accepted yet.

## Latency and history

Measured parent delay8635.121s;do not conflate with full-regression duration.
Requirements:docs/experiment-preflight-latency-followup.md. R3 provides bounded
measurements to target equivalent batching/deduplication,not a measured speedup.
Do not launch a multi-hour full rerun merely to gather another import diagnosis.
Prior state:docs/handoff-history/c324-before-parent-profile-r3.md.
EarlierR1/R2 contracts/reviews/evidence remain historical and unchanged.
C323 acceptance88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf;execution1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4;
publicatione434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
Details:docs/experiment-ledger-addendum-c323-c324.md.
Only this Formal state authorizes the next operation.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
