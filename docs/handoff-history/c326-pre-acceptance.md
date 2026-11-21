# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:explicit PowerShell7,ParseFile,tools/invoke_active_v2.ps1.
Accepted sources/tests/logs/contracts and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C325 ACCEPTED VALID NEGATIVE. C326 ACTIVE / NOT YET JUDGED. C327 NOT REGISTERED.**
C324 remains ACCEPTED VALID NEGATIVE;C323 diagnostic PASS;all earlier verdicts unchanged.
No rerun of accepted C325/C324 or prior recovery routes. C326 is a new experiment.
C326 scientific outcome is unknown; authoring review PASS is not scientific PASS.

## Latest accepted evidence -- C325

Acceptance commit:1a8d15e46aa0b661d5570bed662e67aa1760fc77.
Report:docs/experiment-ledger-addendum-c325-c326.md.
Scientific execution:f95895313da81634976d0ff2761efdd793888c2b.
Published log commit:c030498473daf1155bc5cba6e358f944ec8fce1a;parent matches execution.
Remote metadata:149964 original Windows bytes;logSHA256
c54a2ec2d20bd94990fa0eac79dc14e98a5db83dc53a06299c809757fa72dfa5.
Git log blob:be7fd195c778574f21dcc9bb1bcee90200ee5352.
Reviewer read remote preflight/regression/scientific/terminal receipts and all five
paired contrasts, then independently summed counts. NO independent whole-log rehash,
full local-cell reconstruction or local model replay is claimed for this review.
Do not use old attached C323/C324 logs as evidence of C325.

Native lock/parent semantics/TRAIN-gradient preflight PASS.
Full5546tests/214modules PASS,0failures/errors/skips;724.969seconds.
Ordered test-ID digest23df14a0e694c961b7522dd0b21803eae3a1ab55f56d795ba33d32ffc1135498.
Ten new models completed1200updates;ten checkpoint replays;persisted semantic PASS;
all1517 final uncached rereads;fresh envelope verified808sources/1517inputs/full5546.
Regression/science/verify exits0;run_execution_valid=true;scientific_status=FAIL.
Candidate mixed4 interior0/5,original retention1/5,composite0/5.
Control interior4 interior2/5,retention0/5;do not portray control as uniformly healthy.

HOLDOUT interior answers1064/1440 ->827/1440;pairs472/720 ->288/720.
Original2..6 answers5573/7200 ->6312/7200;pairs2439/3600 ->2920/3600.
Original answer gains by seed75,208,264,57,135;pair gains67,158,95,48,113.
Interior answer gains-103,-55,+16,-53,-42;pair gains-72,-30,0,-41,-41.
At this fixed budget the epoch-level mixture helps original tasks but loses interior
binding in four seeds. Retain weak seed325003 in both arms. No mechanism proof,
structural impossibility,unseen-template,statistical-independence,Gate F or LLM claim.

Parent folder:runs/c325-mixed-name-26478978a92c42d2980095d76d6e4339/.
Primary science/summary.json SHA256:
e3e9808fea616ecc27e2644f808553f16fb6a11203284bdea5c2cf63b32006e8.
Mandatory execution-envelope.json SHA256:
e40a7e93159cdf33b94b11e8ee8df197da66949d121dd52eb8c6036db99440b9.
Both primary and envelope contain the complete808-source/1517-input union.

## C326 registration and completed post-authoring review

Experiment:C326-v5b-mixing-granularity;stage:V5-B-MIXING-GRANULARITY.
Contract:docs/experiment-ledger-addendum-c326-preregistration.md.
Review:docs/c326-post-authoring-review.md.
Source/preregistration/review target HEAD:
895a6e29416a88a70cdd5cfb4cd6ab9444227467.
post_authoring_review = PASS.
Use the subsequent final activation HEAD supplied in the user command, not this
source-only review target or the old C325 execution/publication HEAD.

All6 committed own files reread at the exact target;Git blobs match independently
hashed local test bytes. After reread:own64PASS5.396s;CP932-default-open emulation
64PASS4.221s;0failures/errors/skips. UTF8/noNUL/compile/import PASS;undefined globals0.
Author LinuxPython3.13.5/Torch2.10.0+cpu/NumPy2.3.5. Real Git/files/subprocess/Torch
arithmetic and flow tests; actual worker with explicit synthetic scientific/lease
callbacks. NOT native Windows,real-parent-files,full5610 or scientific fitting PASS.
No author-side PowerShell AST execution claimed;mandatory user AST chain retained.

## C326 one question and scientific contract

At the same total family exposure, does within-update mixing recover interior binding
without losing original-task retention compared with complete-epoch family switching?
Control epoch4 versus candidate batch4;BOTH native mean_last.
Fresh paired seeds326001..326005;orders326101..326105;10new models,no checkpoint init.
14256parameters/core3328,64slots,CPUfloat64,2threads,4internalsteps.
1200updates/model,48rows/update;ordinary mean CE;fitRNG612000.
AdamW betas.9/.999,eps1e-8,decay0;globalclip1;baseLR.005/coreLR.0005.
Work12000updates,576000training-row presentations,15420model forwards,
904320total row presentations,61680core forwards,10checkpoint state reloads.
Allocation/preflight/tests/parent and saved verification are separately scoped.

Control follows C325 mixed4:100 length4 epochs alternate original/interior starting
original. Each192-row epoch comprises4updates/24intact query pairs each.
Both arms preserve EACH pair's family exposures within EACH profile, not just50/50.
Each row:100original2,100original3,50original4,50interior4.
Candidate uses deterministic per-profile integral flow based ONLY on schedule IDs.
Per-update old quota=floor((j+1)*T/M)-floor(j*T/M),per-pair old quota exactly control.
Chronological updates/sortedpair edges/Dinic traversal are fixed;no labels/losses/
HOLDOUT/no fallback/no RNG consumption. Each length4 update has11,12 or13oldpairs:
48,304,48updates respectively;the other pairs are interior. Never split a query pair.
Logical row order,profile sequence,targets,optimizer and model stay paired.
All5 actual masks/control-rule parity must pass preflight before regression/fitting.

ALL5 candidate models must pass complete interior AND original2..6 gates.
Per paired seed:interior HOLDOUT answer AND both-query-pair gains strictly positive;
pooled original2..6 HOLDOUT answer AND both-query-pair gains nonnegative.
Existing thresholds.90/.80/.35/.35/.80 at every local/masked/order condition unchanged.
Length1 descriptive only. Report per-domain failures and rescued/regressed cases.
No average-based override,ratio/seed/budget search or old gate rewrite.
A future PASS would test this temporal policy,not prove gradient conflict or general
language ability. Seen template families/reused logical split;Gate F not established.
Manifest SHA256:
2be1555cf0296e55f5adf2e11302d6112b9b49836781199fcb3fc126d384871e.

## C326 execution, protection and output

Route:invoke_active_v2 ->invoke_c326.ps1 ->run_c326.ps1 ->c326_execution.py
controller ->science worker ->ordinary regression child ->10fits/evaluations/replays
->saved semantic reconstruction ->final input rereads ->fresh byte verifier ->log push.
execution_role=C326-MIXING-GRANULARITY.

Validate exact accepted C325 primary+envelope,all808source/1517input identities/bytes,
manifest/work/full5546 receipt and saved semantic completion. Reconstruct immediate
C325 persisted checkpoints/evaluations/metrics using unchanged C325.semantic_recheck
under no_neural. No parent model forward/refit and no recursive older semantic reruns.
All inherited bytes still checked;never claim that older semantic bodies were rerun.
No accepted module global or function is patched.

Protect814sources=808inherited+6own;
1533inputs=1517inherited+10immediate-parent files+6own.
Includes all direct/lazy deciding dependencies and extra tests. No792-pin fallback.
Unchanged R4 native Windows read leases remain held through worker;no unlocked or
cross-run cache. All1533 inputs receive final uncached rereads. Child summary and
envelope both carry full unions. Each of8child outputs is hashed before/after semantic
reconstruction and checked again before binding it in result/envelope. Fresh process
validates exact parent/child source/input unions and every source/input/output byte,
size,manifest,fullregression and gate/cohort binding;not an additional model replay.

Native TRAIN/allocation/readout/gradient preflight then FULL5610tests/215modules:
5546inherited+64own;5611before sole inherited C204 exclusion. No new excluded/skipped
cases. Actual unique-ID suite construction,ordered-ID digest;separate unmodified
interpreter. Only all5610success permits the10new fits and10checkpoint replays.

Local-only runs/c326-mixing-<id>/science/summary.json+8outputs;
execution-envelope.json,regression-result.json,science.log,regression.log,verify.log.
Only console text published to docs/experiment-run-logs/c326/latest.log+latest.json.
Testdots,ordered-ID digest,10second heartbeats,200update progress,allseed/pair records,
compact domain minima/totals;complete cell measurements remain hashed local outputs.
This reduces console transport volume,not executed tests or saved measurement scope.

## Expected progress and stopping

active_experiment=C326 ->accepted_C325_composite_snapshot ->all5allocation plans
->native_TRAIN_and_gradient_preflight ->full_regression_unmodified_separate_process
->scientific_training_10_models ->saved_checkpoint_and_measurement_verification
->final_uncached_input_recheck ->execution_envelope_verified ->run_execution_valid=true
->standard console publication. Scientific PASS/FAIL is separate from execution validity.

Wrong branch/dirty tree/stale HEAD/nonunique ACTIVE/missing dependency/AST failure:
operational SKIPPED before scientific logging/publication. Native/source/input/flow/
test/nonfinite/checkpoint/semantic/envelope failure stops SAME C326;preserve evidence.
No automatic retries. A valid finite scientific FAIL is accepted negative evidence,
not permission to refit. Publication-only failure repaired without repeating science.
No C327,CI,package reinstall,paid service,cache deletion or old-artifact/source mutation.

User may report only finished. Read remote latest metadata/log and separate scientific
execution HEAD from descendant publication commit. Do not request old C324/C325 logs.
For a valid C326,complete acceptance plus next-C design/implementation/preregistration/
committed-byte review/activation/launcher in the SAME response,not just a design note.
For INVALID,repair same C326. During an active user run do not advance this branch
for unrelated changes;avoid breaking the user's log publication.

## History and inherited compatibility seal

Pre-acceptance C325 handoff:docs/handoff-history/c325-pre-acceptance.md.
C325 acceptance and C326 registration are distinct commits. Earlier C324 recovery
and older evidence remain in immutable reports/commits;no scientific verdict erased.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
