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
recovery_action = LOCKED_HASH_R4
R3 bounded observation and publication COMPLETED. Its worker reached the configured
180s cap;parent validation did not complete. No native fatal was observed in R3.
Only R4 lock-backed hash qualification is authorized. No R2/R3 repetition,no full
scientific retry,no C325. All earlier verdicts,including C321 negative,unchanged.

## Latest R3 evidence and interpretation

Diagnostic execution HEAD:4557a1fb9344596be5faf9750eae1c67e05d0b52.
Diagnostic publication:9f9eb51b796665bfa35cb4834606ca37c40a0d2a.
Log SHA256:50da0a826c7a4644bce059a93d0e7598aeef482969cc27bf7c46bf53c4be0e7d.
Log size10698bytes. Complete remote text and final report were read;no independent
reviewer whole-log SHA256 recomputation is claimed. R4 rehashes that local published
log before launching its one child. Archived exact Git blobs under:
docs/experiment-run-logs/c324/attempts/9f9eb51b796665bfa35cb4834606ca37c40a0d2a/latest.*.

Worker elapsed180.002s,timed_out=True,returncode1,parent_validation_completed=False,
stderr0bytes. This was controller termination at the cap,not the original0xC0000409.
179samples:176real_parent_validation,3runtime_import. Nearest repository frame
C175.sha appeared171times;leaf hashlib.file_digest155,file-open16. Final stack
passes C317.verify_artifacts through C318..C324's recursive parent-validation chain.
Counts identify a priority for reducing repeated hashing;they are NOT exact call
counts,unique-file counts,unbiased time percentages or a native-crash explanation.
The R3 end-of-timeout repeated180.0 heartbeat is diagnostic-controller output noise;
R4 rate-limits heartbeats without altering historical R3 code or evidence.

R2 execution7ca1ce4ae287e58a16d7e13da99fd03fb76ca89f;
publication3de15c5b5850c732001f21b87658a5621faf7e68. Both bounded import workers
returned0 and the examined C242 function matched freshly compiled source.
This does not establish health of every cache or repair of the full native failure.
R2 evidence remains under its existing attempts/3de15c5b5850c732001f21b87658a5621faf7e68/.

## Active R4 qualification and review

Contract:docs/c324-locked-hash-recovery-r4.md.
Review:docs/c324-recovery-review-r4.md.
Source/review target HEAD:e542ee01c2af85abff4a44952d36ba34659230c4.
post_authoring_review = PASS.
Review scope:bounded operational qualification software readiness ONLY.
Use the final documentation/activation HEAD supplied with the command,not the
source-only review target or any prior R2/R3 command.

Route:active v2 ->invoke_c324.ps1 ->invoke_c324_locked_hash_r4.ps1 ->
c324_locked_hash_r4.py ->one bounded worker ->STOP and standard log publication.
Role:C324-R4-LOCKED-HASH-QUALIFICATION. No scientific execution is requested.
Only the C324 launcher's recovery-action map gains one entry;all50 parent paths
and the normal scientific body remain unchanged. No scientific tree/test/runner edits.

Candidate temporarily reuses ONLY C175.audit.sha digests within one process while
holding native Windows read HANDLEs that deny write/delete sharing. Every miss
compares streaming SHA256 to the original function under the lease. Every hit
checks held and current-path identities. At the end,restore the original function
and independently reread EVERY unique file with it before releasing all leases.
No timestamp-only cache,no persisted cache,no verifier/result memoization,no
unlocked fallback. Fail closed on mismatch,missing file,lock failure,thread drift
or4096-file bound. Accepted C175 source remains unchanged with its blob pinned.

Native worker first creates only a small new local lock-probe file and checks real
read compatibility,WRITE/DELETE-access denial while held,and release afterward.
Then check exact authoritative runtime and call the unchanged C324.load_parent ONCE
with all50ordered paths. Original no_neural plus explicit model-forward/optimizer/
scientific-entry guards remain. Parent tensor archives may be read for validation;
no full regression,no new model forward,no optimizer updates,no science autoretry.

One child,300s cap including imports,lock probe,parent validation and final rereads;
10s controller heartbeat. Cap is not total log-publication duration. Hash progress
is retained in worker stdout and included in the published console outcome.
Counters:hash_calls/cache_hits/unique_files/stream_bytes/reference_bytes/
logical_reference_bytes/final_reference_rechecks. They describe this adapter's
logical payload,not physical disk I/O. Interrupted reference bytes are requested-size
bounds. No production speedup or full-reference wall-time ratio measured yet.

Qualification requires native probe,complete parent return,canonical192/96rows,
restored original SHA,every final reference reread,complete receipt,exit0,no timeout.
Timeout means incomplete qualification;fatal/error is retained. diagnostic_completed
means the controller collected an outcome,NOT that the candidate or science passed.
Even a completed qualification does not establish the original crash is fixed.
End action:STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY. Do not repeat automatically.

## Authoring evidence and next user action

Four committed executable/test files reread and raw Git blobs matched local bytes.
37tests PASS2.320s;CP932-default-open emulation37PASS2.355s;LinuxPython3.13.5.
UTF8/noNUL,Pythoncompile,and free-global audit0unbound. Real file/subprocess checks,
explicit emulated Win32 ABI/share-access and synthetic parents;NOT native Windows
qualification. No local PowerShell AST execution claim;the mandatory ParseFile
chain remains in the user command,dispatcher and selected recovery launcher.

Use ordinary active-dispatcher command at supplied final recovery HEAD. Expect
execution_role=C324-R4-LOCKED-HASH-QUALIFICATION,scientific_execution_requested=False,
heartbeats,native-lock/parent outcome,diagnostic_report,STOP,then log publication.
The user reports finished;read remote C324/latest.*. Metadata.execution_head is
now the DIAGNOSTIC HEAD,not scientific47ccd. Preserve earlier attempt identities.
No C325. Do not request old C323 attachments or retry a multi-hour full run blindly.

## Original invalid scientific attempt

Scientific execution47ccd303f4382b7938db639e86aeb151e1f83af1;
publication68397de27b4c538ddbd22dc2209fddb7afbc2409.
LogSHA2568a5e28af87430010931afef2b2da3b61590f32930bee2967daff37c8db6a3271,976635bytes.
First parent validation8635.121s,native-gradient PASS,own64PASS5.618s,
full5357PASS1074.995s. Second parent validation in science process aborts before
child training:_PyEval_EvalFrameDefault:Executing a cache;C242.parent_module invalid
frame;exit0xC0000409;run_execution_valid=False. Underlying cause remains unknown.
No cache deletion,reinstallation or hardware diagnosis follows from these logs.
The original failed log and R2/R3 evidence remain in immutable attempts/ paths.

## Scientific contract unchanged — not currently runnable

C324-v5b-interior-coverage-training;V5-B-INTERIOR-COVERAGE-TRAINING.
Registration:docs/experiment-ledger-addendum-c324-preregistration.md.
Design:docs/v5b-interior-coverage-training-v0.1.md.
Original/interior4,bothmean_last;onlylength4TRAIN tables differ.
Seeds324001..324005,orders324101..324105;10models,14256parameters,64slots,
CPUfloat64,2threads,1200steps/model,48rows/step. Existing optimizer/gates unchanged.
ALL5 candidate interior and original2..6 gates plus positive pairedHOLDOUT answer
andquery-pair gains;not unseen-template generalization. No threshold/seed changes.
50parents,792pins/1491inputs,own64,210modules/5358loaded/5357selected;
only inheritedC204mutable-state exclusion. Full suite remains required for a later
authorized scientific run;R4does not adopt a cached historical regression PASS.
Manifest:b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
Science12000updates,576000training rows,15420forwards,904320row presentations,
61680coreforwards,10checkpoint reloads. No scientificC324 result accepted yet.

## Latency and historical state

Measured original parent delay8635.121s;not the full-regression duration.
Requirements:docs/experiment-preflight-latency-followup.md. R4 implements a targeted
hash-reuse candidate and bounded actual qualification,not a declared speedup.
Batched Git checks and broader equivalent deduplication are not silently activated.
Prior handoff:docs/handoff-history/c324-before-locked-hash-r4.md.
EarlierR1/R2/R3contracts/reviews/evidence remain historical and unchanged.
C323acceptance88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf;
execution1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4;
publicatione434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
Details:docs/experiment-ledger-addendum-c323-c324.md.
Only this Formal state authorizes the next operation.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
