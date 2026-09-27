# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C267 ACCEPTED VALID NEGATIVE. C268 ACTIVE / NOT YET JUDGED. C269 NOT REGISTERED.**
C268 is the unique ACTIVE experiment:paired-query discrimination-loss comparison.
C267 was already executed and published;do not rerun it. mixed_names passed1/5,not5/5.
C266 remains diagnostic PASS,C265 negative,C264/C263 bounded PASS. All earlier verdicts/recoveries
remain unchanged. No default architecture/optimizer change or production adoption.

## Latest accepted evidence — C267

Scientific execution HEAD:3418e545bc261cf1bb920f2ae8f819deec69150c.
Published log commit:92b57170c6b2c3c3dc451f9d6de402114cbd6f12.
Log blob:798096cf2d24363ccf8f109ae2d6f89843b4cf8d.
Publisher log SHA256:f8ee03f3e30132601b1a6f055388a3411b93638280ff1680a6c1075aa20c852c.
Log bytes1072898;4910 lines. Metadata blob006ddc934d7d910fd332603768ce1c33d316f664.
Summary:runs/c267-v5b-name-coverage-f8a591aae4aa4b7aa373aba2e520181c/summary.json.
Summary SHA256:f5f550d362428feaee12d7eee96db4cc324cea311b9b4e91ec50e4f150ec6ef8.
Acceptance:docs/experiment-ledger-addendum-c267-c268.md.
Acceptance/base commit:9465a4bddf1182e1da3044764dec765ae5a7cacc.

Own24 PASS;focused3573 PASS. Source pins448/protected inputs761 verified. Ten models completed800
updates each:8000 updates,384000 training rows,8540 wrapper forwards,435840 row presentations,
34160 core calls. One final bundle write/load;ten strict state loads. all_pairs_matched=True;
all_replays=True. persisted_name_coverage_scores_and_pairs=PASS;protected inputs preserved;
tracked tree clean;scientific HEAD preserved;run_execution_valid=True. scientific_status=FAIL.

Acceptance uses previously retrieved full blob contents and parsed published metrics/postcheck,
plus immutable publication metadata. No independent learned-state rerun or reviewer complete-log
rehash is claimed. The contents API returned empty content for this >1 MB log;that is a retrieval
limitation,not evidence that the experiment failed or the log is absent. Never rerun on that basis.

HOLDOUT aggregate across5 seeds and2 symbolic languages,480 answers/240 query pairs per arm/profile:

|Profile|Control correct /480|Mixed correct /480|Control collapsed /240|Mixed collapsed /240|
|---|---:|---:|---:|---:|
|doubled|284|260|33|57|
|shared_prefix|248|254|88|66|
|shared_suffix|212|257|163|76|

Total744/1440 versus771/1440 correct;collapse284/720 versus199/720. These descriptions do not replace
individual cell gates. Whole-model passes:doubled_only0/5,mixed_names1/5 (267005 only).
Shared-suffix collapse decreases,but correctness remains257/480;doubled correctness worsens by24.
This is not uniform improvement. mixed_names267002 passes TRAIN criteria but fails HOLDOUT;
267001/267003 have TRAIN misses and267004 misses every TRAIN answer cell. Do not attribute every
failure solely to insufficient fit or solely to generalization. Control collision-profile TRAIN
scores are not fit-to-seen-profile scores,as doubled_only did not optimize those naming profiles.

Accepted parent artifacts:
coverage-plan.json:4f83a11bd6b2c31d7f1bd23b617772d1eab413e5099d5aafe3c4a34eb453f2d7;2631 bytes.
dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
trained-models.pt:a300bae3930b23c78bb4cd5285f581b21a243b6529eb770d24669ad25b92bd58;1238007 bytes.
evaluations.pt:e01decea02b8109fbed19cc01d03091867edac02fbaed00f2a7a78e40b4782f3;53143103 bytes.
measurements.json:d1c9404f3893d3b110fdbf58e15a4f241847fce8304d58a24ac35d1604acfb23;262390 bytes.
validation-summary.json:b8ab346a36cb2167e4d6cd0cbd3f19fefdc161b35a120fe40c33e00d4a8ec3f1;6831 bytes.

## Duplicate-launch correction and operational boundary

The user correctly reported C267 completion. The assistant mistakenly repeated the old C266 response
and C267 command instead of reading the newly published result. That duplicate command safely
SKIPPED because its3418e545 execution HEAD differed from the92b57170 log-publication HEAD.
There was no second scientific attempt and no need to rerun C267. This was an assistant workflow
error,not user error or a failed C267 experiment.

Operational commit fece51c05c2b38ffa2e96ea601fc4b8a127305b8 changed only tools/invoke_active.ps1.
Dispatcher blob:ea2e3d59cc72f0fa799f61d632f864c366099a89.
If HEAD differs but the currently active experiment's published metadata matches ExpectedHead,
it reports RESULT_ALREADY_PUBLISHED and returns without execution/publication. That means a result
is available,not that the attempt was valid or PASS. All other mismatches retain STALE_EXPECTED_HEAD.
Do not silently change ExpectedHead to current HEAD,remove safety checks,or call every mismatch a
log-only change:the notice is based on metadata,not a proof of every intervening commit's contents.

On each 'finished' message,read the current branch and the active experiment's latest metadata/log
before responding. Judge a completed result rather than replaying an older answer. Re-read the final
activation HEAD before giving any new command. Do not move the branch during a user run/publication.
The earlier dispatcher patch had static readback checks only,not Windows execution/full regression.
C268 adds a static regression contract for its result-notice and safety paths. No additional shared
dispatcher edit is part of C268. All actual inherited pin/input checks remain mandatory and unwaived.

## Preserved earlier evidence

C266 diagnostic PASS only:saved shared-suffix collapse2149/2880 pairs;C265 remains negative.
C265 whole-profile counts:doubled16/20,prefix6/20,suffix0/20;not zero answer accuracy.
C264 bounded frozen two-fact PASS for all20 states,not perfect predictions. C263 bounded capability
PASS for all20 states,with both learning rates at the final accuracy ceiling;no lower-rate benefit.
C262 chronology sensitivity remains valid evidence from a different cohort. C261 and C260 remain
valid negatives (with_core4/5,without_core3/5);C259 six-order4/5 versus two-order2/5 remains negative.
C258 diagnostic PASS,C257 unseen-order2/5 negative,C256 bounded5/5 PASS remain. All earlier diagnostic
scopes,failed gates and invalid attempts remain in acceptance/recovery addenda. Complete prior
handoff preserved at3418e545bc261cf1bb920f2ae8f819deec69150c. Do not edit accepted experimental sources,
tests,logs,checkpoints,recovery records or tools/run_c167.ps1. No cleanup/history rewrite/CI change.

## Active C268 — one question and fixed comparison

Experiment:C268-v5b-paired-query-discrimination-loss.
Stage:V5-B-PAIRED-QUERY-DISCRIMINATION-LOSS.
Question:with mixed-name coverage,paired batches,initial weights and800 updates held equal,does an
auxiliary query-discrimination loss improve held-out value binding relative to CE alone?

Fresh seeds268001..268005;arms ce_only and ce_pair_margin. One actual C252 Full aligned-reader
initialization through C256.make_model/C231 factory per seed is deep-copied to both arms.
Both14256 parameters. No accepted checkpoint or optimizer state initializes training.
Model.forward gets only visible token IDs and zero task IDs. Targets and pair identities are used
for supervised loss only. Both arms get the exact same paired minibatches and all3 name profiles.

For a same-facts pair with distinct targets t0,t1 and logits z0,z1:
    d = (z0[t0]-z0[t1]) - (z1[t0]-z1[t1])
    P = mean(relu(2.0-d)) across24 pairs
    ce_only: mean cross-entropy on48 rows
    ce_pair_margin: same CE +0.1*P
Margin2.0 and coefficient0.1 are fixed pre-result engineering choices,not optimized constants.
Control computes penalty for reporting but backpropagates exact CE. No additional neural forward is
needed;the objective uses the48 existing logits. Extra arithmetic/gradient work is not zero cost.
A zero margin penalty does not ensure correct answers;both queries can still choose the same value.
Retain CE and all correctness gates. The new gradient and its clipping behavior are part of the loss
intervention,not separately isolated causes. No loss/seed/budget tuning after results.

Data remain exactly C267's192 TRAIN/96 HOLDOUT logical rows,hash:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
HOLDOUT value pairs(0,2),(1,3),(2,0),(3,1) in every subset/language/order/profile;other8 pairs TRAIN.
All3 profiles uu/vv,uu/uv,uu/vu are TRAIN-seen in BOTH arms. Preserve actual C267 renderer and48 slots.
This small modular split is not an independent general benchmark. No held pair is optimized.

Group TRAIN by(language,entities,values,permutation),96 groups each containing both queries sorted
by entity index. Shuffle96 groups with seed+268000+epoch. Four batches of24 adjacent pairs give48
rows/update.800 steps=200 complete epochs;every TRAIN row appears200 times. Profile=epoch%3 gives
updates268/268/264. Reconstruct batch digest,exposures and profile counts from saved records.
Paired grouping differs from C267 but is shared by both new arms;only the objective changes within
C268. Do not infer a benefit of paired batching itself or historical causal diagnosis from this.
Fit RNG=seed+269000 reset per arm. AdamW lr.005,betas.9/.999,eps1e-8,wd0,global clip1.
CPU float64,threads2,deterministic.800 updates/model,batch48,no early stop/checkpoint selection.

## C268 gate,workload and source interfaces

Use actual unchanged C267.score on final tensors for all splits,profiles,languages,subsets,orders
and normal/evidence_blind/query_blind views.72 answer cells and36 two-order cells/model.
Accuracy>=.90,paired-query>=.80,evidence/query drops>=.35,two-order consistency>=.80.
TRAIN16-answer/8-query-pair cells require15/16 and7/8;HOLDOUT8-answer/4-pair cells require8/8 and4/4.
Two-order groups require13/16 TRAIN and7/8 HOLDOUT. Do not replace these with pooled averages.
Primary PASS requires ALL FIVE ce_pair_margin states to pass every criterion. Control outcomes are
separate and cannot rescue/fail the candidate. Record30 HOLDOUT contrasts of correct answers and
same-answer collapse,each48 answers/24 query pairs. Lower penalty or fewer collapsed answers alone
are not capability improvement. A candidate PASS need not be an advantage if both arms pass.
No unseen-name transfer,arbitrary strings,causal parser,production or Gate F claim follows.

Formal workload:10 models,8000 updates,384000 training rows. Per model final27 forwards/2592 rows
and strict replay27/2592. Training+final827/40992/3308 core calls;replay27/2592/108.
Total8540 forwards/435840 rows/34160 core calls;540 final/replay forwards. One new10-state bundle
write/load;10 strict state loads. Saved final raw tensors53084160 bytes plus weights/JSON;not peak RAM.
Historical tests,hashing,parent saved-metric verification and schedule generation are additional work.

load_parent calls actual C267.verify_artifacts(parent_dir,PARENT_EXECUTION),TWO arguments,with neural
Module calls blocked. Require valid-negative status FAIL,counts doubled_only0/mixed_names1,10 metrics
and exact six artifacts above. This uses saved final outputs,not old model inference or initialization.
The current C267 context supplies core/base/reader/factory helpers. Its actual counted,evaluate,
replay_one and score are used. Strict replay accepts a C268 record without imposing C267 seed IDs;
it verifies matching final fingerprint,exact argmax,max raw error<=1e-9 and27/2592/108 resource counts.

Six ignored outputs plus summary.json:loss-plan.json,dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json. Bundle schema fold-c268-query-loss-models-v1;eval schema
fold-c268-query-loss-eval-v1. Raw records contain final per-split/profile/view logits,fit schedule,
CE/penalty/total arithmetic,initial/final fingerprints and replay counts. Saved postcheck blocks
Module calls and rebuilds schedules,parent scores,contrasts and gates without a learned-bundle load.
Protection:454 pins/774 inputs=parent448/761 +OWN6 +parent summary/SIX artifacts.
Direct dependency union44=five C231 LM sources+C230..C267 helpers+C268,including lazy imports.
Own24;modules153;loaded3598/focused3597. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:cf16b504aa03e1e5f61c000c161b44c3a551fe7c103096c9119274947fb4e07b.
Registration:docs/experiment-ledger-addendum-c268-preregistration.md.
Design:docs/v5b-paired-query-loss-v0.1.md. Acceptance and new registration are separate commits.

## C268 post-authoring review

post_authoring_review = PASS
review_target_HEAD = c617275a8968975bcdcab0e19791c12f24fa6b61
Scope:committed-byte authoring validation in a limited synthetic runtime,NOT formal Full-model science.

All six committed OWN files were re-fetched and completely read (ranges where response limits
required). Complete locally tested bytes were independently Git-blob hashed and matched to remote:
-benchmark:c6086714c45c8956c591cccc66ce8336746efca9;20952 bytes.
-tests:677d020be1b6bd42fa262a76de6d840ffe82cbc1;20170 bytes.
-runner:d65a900f50b9ba20e88484206026e42897cde741;4743 bytes.
-launcher:49592ebe5b091ef052d343f03d5c42d6bef03aff;2641 bytes.
-preregistration:132e5ef2633f5ea3640ceb4b1c8e6527a424f538;11409 bytes.
-design:a56d89cb178bee16540e5208c1d0322bd7977a48;3585 bytes.
The existing dispatcher mirror also matched ea2e3d59cc72f0fa799f61d632f864c366099a89;5275 bytes.

Initial exact own suite:24/24 PASS in7.242s. After remote readback and all six matches:
24/24 PASS in7.080s. No executable correction was required between those runs.
UTF-8/NUL,Python compile/import,manifest/data hashes and three embedded Python block compilation
passed. Recursive LOAD_GLOBAL audit inspected60 functions/methods and86 code objects,using actual
globals and unwrapped functions:zero unresolved names. Semantic24-test count and CLI indices
precheck1,regression none,postcheck1/2/3 passed. Source call-order tests target actual run/fit functions.

Tests use an explicitly synthetic Tiny encoder/core and Factory/Base/Core/Audit adapters. Local
C267 helper code is a review-only excerpt adapter reconstructed from retrieved helpers,NOT a complete
byte-identical C267 module or historical checkout. It supplies dataset/render/scoring/evaluation/
counting/replay logic for authoring checks. It is not committed and does not replace the real parent.
Test12 runs actual C268800-step training on Tiny and the excerpt replay;test11 uses4 test-only steps.
Test18 substitutes training records but exercises the new ten-state orchestration,evaluation,replay,
analyze and persisted postcheck. Test17 checks real new two-argument parent dispatch against a mock
validator. Tests5-10 verify exact CE control gradients,margin signs,scalar agreement and the case
where zero penalty still yields incorrect same-answer collapse. Test21 checks targets do not enter
model.forward. Dummy3598 test IDs verify filtering only,not execution of3597 historical tests.

Test24 checks the existing patched dispatcher source:safety guards/ParseFile precede invocation,
published metadata matches experiment and ExpectedHead,nonmatching cases retain stale stop,and no
silent ExpectedHead reassignment occurs. This is not a PowerShell execution test. The inspected
C204 dispatcher contract still requires those same ordering/guard properties;full regressions remain
pending. Source/dependency counts were checked synthetically;actual inherited mappings are not waived.

Actual C267 context,score,evaluate,replay_one,record writer and two-argument verify_artifacts paths
were source-reviewed. No C268 result was used to tune the loss,data or gates. Compared with the
post-incident operational HEAD fece51c...,seven new paths only:acceptance and OWN6. No accepted
experimental source,test,runner,log,shared dispatcher or CI file changed in C268 authoring.
Only this activation handoff follows the completed review.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Full checkout and user-local accepted
artifacts were unavailable;container GitHub DNS failed. pwsh/powershell absent;Windows ParseFile
was NOT executed here. Pending authoritative checks:dispatcher/launcher/runner parser chain,real
454/774 source/artifact precheck,own24 through full dependencies,complete3597 regression,ten real
Full-model learning runs,strict checkpoint replay,persisted postcheck and log publication. None is
claimed complete by this authoring review. Use FINAL activation HEAD,not review_target_HEAD or any
C267 execution/log HEAD. Re-read final ref before issuing the user command.

## Execution and stop

Use tools/invoke_active.ps1;formal state has exactly one ACTIVE token resolving to C268.
Fixed parent:runs/c267-v5b-name-coverage-f8a591aae4aa4b7aa373aba2e520181c/summary.json.
Order:dispatcher/launcher/runner ParseFile ->Python compile/parent precheck ->own24 ->focused3597
->ten-model paired learning ->strict final checkpoint replay ->saved postcheck ->log publication.
Progress:model1/10..10/10;steps200/400/600/800 print CE and pair_penalty. Valid scientific FAIL is not
INVALID. Do not extend updates,change margin/coefficient/profile/split/seeds or thresholds to rescue it.
Wrong branch/dirty tree/unrecognized stale HEAD/ACTIVE mismatch stop before science. A recognized
published-result notice means inspect available evidence,not rerun or assume PASS. Source/schema/
nonfinite/count/replay/test faults require SAME C268 recovery;C269 waits for valid judgment.
Repair log-only publication without retraining. On 'finished',read docs/experiment-run-logs/c268/latest.*
(and actual blob content for >1 MB files),not an older experiment. Do not move branch during user run.
No paid API,external corpus,model expansion,production adoption,cleanup,history rewrite or CI change.
Gate F NOT PASSED. Preserve all accepted evidence,recoveries and tools/run_c167.ps1.
