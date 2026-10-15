# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted scientific sources/tests/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 ACTIVE / INVALID ATTEMPT RECOVERY. C325 NOT REGISTERED.**
Original scientific attempt47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
recovery_action = SCIENTIFIC_R6
R5 operational qualification PASSED. A NEW full SAME-C324 scientific attempt through
R6 is authorized after its completed authoring review. Its result is NOT YET JUDGED.
Do not repeat R2/R3/R4/R5 diagnostics or the old full C324 route. No C325.
All earlier scientific verdicts remain unchanged;C321 remains VALID NEGATIVE.

## Latest R5 qualification evidence

Diagnostic execution HEAD:1beb6d60f3dd0f7c72f41c9355c96827b8da4e82.
Diagnostic publication:f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19;
publication parent matches execution HEAD.
LogSHA256:2f89e566132f0ade3660dc7c2aafb6a4946ffaa3d441341af0d39671cd663558;
15940bytes. Remote progress and complete final report read. No independent reviewer
whole-log rehash claimed. R6 checks the whole local published evidence before starting.
Exact log blobs preserved under docs/experiment-run-logs/c324/attempts/f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19/.

Worker244.561s,exit0,no timeout,stderr0,parent_validation_completed=True,
reference_recheck_completed=True. All7 C316..C322 verifier bodies completed once.
Requests/reuses by C:316=3/2;317=2/1;318=1/0;319=4/3;320=3/2;321=2/1;322=1/0.
Total16requests,7executions,9reuses,0failures. Frozen1486files;final uncached1486.
Hash61762calls,60276hits,1486unique;stream12445440511bytes;
reference24890881022bytes;logical291958419357bytes. Not physical disk traffic.
Retained metadata24083208bytes. Parent+final recheck173.9249438s excludes initial
snapshot/import time and must not replace the whole-worker244.561s figure.
Canonical data1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
original prompts2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd;
interior promptse7f9a53e162f5f0156261e33c0bac7875ee592fbd2bdb2d27faac4f3d27f5e8b.
R5 had0model forward/0training;this is not a scientific C324 PASS or native-cause proof.

## Active R6 registration and post-authoring review

Contract:docs/c324-scientific-recovery-r6.md.
Review:docs/c324-recovery-review-r6.md.
Source/review target HEAD:8fd4ef3ef287212735d568c805db8d56236c6a31.
post_authoring_review = PASS.
Use the final documentation/activation HEAD supplied in the user command,not the
source-only target or an old diagnostic HEAD. R6 scientific execution remains unjudged.

Route:active_v2 ->invoke_c324.ps1 ->invoke_c324_scientific_r6.ps1 ->
c324_scientific_recovery_r6.py ->scientific worker ->independent envelope verification
->standard C324 console-log publication. execution_role=C324-R6-SCIENTIFIC-RECOVERY;
scientific_execution_requested=True. This is NOT a600second diagnostic.

The unchanged C324 model/trainer/gates are called by a new registered orchestration.
No fold_lm/fold_reasoning/tests_lm/run_c324 changes. Original source blob stays
2fc9e31c7037313a3fadb126af9b153608c0ac6e. Main launcher adds one action plus comment;
its50parent paths and old normal body remain byte-identical to the prior route.

First acquire complete native Windows read-locked inputs and perform the actual
R5-qualified parent verification:seven first bodies real,repeat requests exact and
session-local. Then restore verifier/SHA functions and retain isolated canonical
parent dictionaries during this same locked execution. Ordered paths,all lease/path
identities and typed fingerprints are checked for every parsed-data read. No cached
child/model result,no prior-run PASS,no unlocked fallback. First real loader must
leave RNG/runtime unchanged; later data reads consume/restore no training RNG.

Batch Git source blob queries by exact validated immutable replies; live repo guards
are not cached. After parent preparation run actual native TRAIN/gradient preflight.
Run full regression in a separate ordinary interpreter with NO scientific wrappers:
5357original+37R4+48R5+48R6=5490selected,213modules,5491before the inherited single C204
exclusion. No new skipped/excluded tests. ONLY after all5490pass, run all10new models,
evaluation and10checkpoint replays. Then invoke unchanged C324.verify_artifacts to
reconstruct the saved child metrics/JSON from fresh checkpoint/evaluation loads.

Finish ALL1501uncached input rereads,release leases,and write execution-envelope.json.
A fresh process verifies the envelope,current source blobs,every input byte,primary
summary contract and every saved output's bytes/size. It does not repeat ancestor
semantic reconstruction; that full verification occurred in the locked worker.
Actual process output is streamed with10second heartbeats and phase names.
No total duration or controlled speedup promised. Native-crash cause remains unknown.

## Mandatory R6 composite protection and future inheritance

The original scientific summary remains792source/1491input by its unchanged schema.
A valid R6 execution MUST ALSO have its envelope containing the entire802source /
1501input union,full5490test receipt,seven completed verifier bodies,final1501rereads,
primary summary hash,original manifest/work,parsed-data read count and semantic
postcheck completion. Effective protection is NOT just the old792-source summary.
10supplemental files: R4/R5/R6helpers, R4/R5/R6tests, R4/R5/R6launchers, R6contract.
All direct executable dependencies and supplemental test inputs are protected.
Both primary result and envelope are required; fresh verifier checks exact unions.
Future C325 MUST validate and inherit802combined source pins. Do not take the old
primary summary alone or weaken direct-dependency protection to register C325.

Outputs local-only under runs/c324-scientific-r6-<id>/:
science/summary.json+8outputs,execution-envelope.json,snapshot-inputs.json,
regression-result.json,science.log,regression.log,verify.log. Envelope path/hash and
execution_envelope_verified are printed. Only console text is pushed to Git.
C324 runtime.elapsed_seconds covers its run phase with R6 parsed input reuse;
record it separately from snapshot/whole-worker timings. No timing-ratio claim.

## Authoring evidence and user execution

All4 committed executable/test files plus contract reread;Git blobs match local
raw bytes. After matching48newtests PASS0.935s;CP932-default-open emulation48PASS0.939s.
LinuxPython3.13.5. UTF8/noNUL/compile/free-global audit passed. Real Git/files/subprocess
checks; production-worker control integration with explicit synthetic science and
leases;failed regression cannot reach fitting. NOT Windows/full5490/FOLD-training PASS.
No author-side PowerShell AST execution; mandatory dispatcher/launcher AST chain stays.

Expected:roleR6 ->locked_parent_reconstruction ->native_TRAIN_and_gradient_preflight
->full_regression_unmodified_separate_process ->scientific_training_10_models
->saved_checkpoint_and_measurement_verification ->final_uncached_input_recheck
->execution_envelope_verified ->run_execution_valid=true ->log publication.
Errors/native fatal/source/input/test/schema/nonfinite/replay/envelope failure stop
SAME C324. Scientific status FAIL alone is not execution failure and must not trigger
retraining. Transport-only failure is repaired without repeating science. No auto retry.
User can report finished;read remote latest metadata/log and classify execution validity
separately from the science gate. metadata.execution_head will be R6 science HEAD;
published log commit is a different descendant. No old C323 attachment needed.

## Unchanged scientific question and workload

C324-v5b-interior-coverage-training;V5-B-INTERIOR-COVERAGE-TRAINING.
Original/interior4,bothmean_last;onlylength4TRAIN templates differ.
Seeds324001..324005,orders324101..324105;10models,14256parameters,64slots,
CPUfloat64,2threads,1200steps/model,48rows/step,same optimizer and learning rates.
ALL5 candidate interior/original2..6 gates plus positive paired HOLDOUT answer and
query-pair gains. Thresholds.90/.80/.35/.35/.80 unchanged. Not unseen-template success.
Child work12000updates,576000training rows,15420forwards,904320row presentations,
61680core forwards,10checkpoint reloads. No accepted scientific C324 result yet.
Original manifestb726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.

## History

Original invalid science47ccd303f4382b7938db639e86aeb151e1f83af1;
publication68397de27b4c538ddbd22dc2209fddb7afbc2409. Parent precheck8635.121s,
full5357 PASS,second parent validation native0xC0000409 before fitting.
R2imports passed;R3sample observation and R4hash-only qualification timed out at
registered caps,not scientific negatives. R5finally completed its full qualification.
Earlier logs/contracts/reviews remain in immutable history. No cache deletion,
package reinstall,hardware-fault conclusion or claim of identified native cause.
Previous handoff:docs/handoff-history/c324-before-scientific-recovery-r6.md.
C323acceptance88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf;
execution1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4;publicatione434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
Only current Formal state authorizes operations.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
