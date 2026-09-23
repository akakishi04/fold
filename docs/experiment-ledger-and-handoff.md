# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C239 ACCEPTED VALID NEGATIVE. C240 ACTIVE / NOT YET JUDGED. C241 NOT REGISTERED.**
C240 is the unique ACTIVE experiment:offline analysis of saved predictions,not a capability run.
C238 remains minimal seen-TRAIN fitting PASS; C237 remains diagnostic-integrity PASS only.
Post-authoring review is PASS. Authoritative runtime prechecks/regression remain mandatory.

## Latest accepted evidence — C239

Scientific execution HEAD:c847609c8d045c9c5db4ec882bf336a9671180ff.
Published log commit:5207d3b378ae56502a78dc9a5bb6f843cf389795.
Log SHA256:9e139f0544b49cb1185ce285a7b7c2c7ccb5ad394198040be4845648aa3697ee.
Summary SHA256:500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af.
Local summary:runs/c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5/summary.json.

24 own tests PASS in4.351s;2905 focused tests PASS in78.219s.280 source pins/418 inputs protected.
2400 training steps/76800 answer presentations;2490 total forwards/77520 rows.
All replays/weight-update checks PASS;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
All12 cells pass TRAIN:4/4 answers,2/2 fact/query pairs,0.50 mask drops.
All12 cells are ORDER_HOLDOUT_MISS:0/4 or1/4 answers,0/2 pairs,negative mask drops.

HOLDOUT correct counts:seed234001 Full EN1/4 JA1/4,GRU EN0/4 JA1/4;
seed234002 both families/languages0/4;seed234003 Full both0/4,GRU EN1/4 JA0/4.
C239 learned the training order but did not transfer to the reversed order. No causal mechanism proved.
Acceptance/artifact details:docs/experiment-ledger-addendum-c239-c240.md.
Acceptance record commit:b739256640949f69a6ca781d31cde108cbe1edf6.
Acceptance/handoff base:006551cd8b91e04534f253b5cf3942a12b84f7f8.
Published log ranges and recorded postcheck were checked;no reviewer checkpoint rerun or full-log rehash.
Do not rerun C239,alter thresholds or reinterpret C238 as a generalization result.

## Preserved earlier evidence

C238:all12 seen-TRAIN cells100%,both families pass after complete-cohort sampling.
Details:docs/experiment-ledger-addendum-c238-c239.md.
C237:internal numerical sensitivity without correct answer switching;diagnostic PASS.
C236:valid negative on the16 prompts with random replacement sampling.
C235:diagnostic PASS;failure already on complete TRAIN;first INVALID attempt preserved.
C234/C233 remain valid negatives;C232 remains bounded template-byte learning only.

## Active C240 — saved positional-rule audit

Experiment:C240-v5b-saved-positional-rule-audit.
Stage:V5-B-SAVED-POSITIONAL-RULE-AUDIT.
One question:do saved C239 answers match query-to-fixed-position behavior,correct entity binding,
always-first/last outputs or constants? This is descriptive error analysis before another intervention.

Change only offline measurements. Keep C239 data,predictions,masks,targets,checkpoints,seeds,
architectures,training history and verdict fixed. No new inference,training,checkpoint load/write.
The parent checkpoint is hashed for preservation but never deserialized or evaluated.

Read final[TRAIN/HOLDOUT][en/ja] and predictions[TRAIN/HOLDOUT][normal/evidence_blind/query_blind],
not initial_train or the older final_probe schema. Verify parent summary with actual C239 helpers.
Recompute all discrete metrics from saved predictions:accuracy,paired fact/query accuracy,
masked accuracy and drops. NLL is finite/hash-protected only;it cannot be reconstructed without
logits/probabilities. Keep nll_recomputed=False. Do not call this a new model or NLL replay.

Six fixed normal-view rules:entity,query_fixed_position,first,last,constant_0,constant_1.
query_fixed_position means object0/box query selects the rendered first value,object1/book the second.
Report per-cell agreement counts and correct/other_entity/outside_supplied categories. All byte
outputs0..255 remain possible. Do not silently convert a wrong byte into the other digit.
Match TRAIN/HOLDOUT by language,assignment/group and query;report same answer,both correct and
both fixed-position matches. Preserve individual row and paired-order evidence.

Identifiability limits:entity=fixed-position on TRAIN;fixed-position=other entity on this binary
HOLDOUT. Agreement cannot uniquely identify an internal algorithm. No answer inversion or repair.
The analysis reuses existing samples;it is not independent evidence or a capability improvement.

Primary-record counts:288 saved predictions;96 normal rows;576 rule comparisons;48 order pairs;
24 split/language diagnostic cells. New training steps0;model forward calls0;checkpoint loads/writes0.
Precheck/postcheck repeat verification,not new samples. File hashing/JSON work and historical test
fixture costs are not claimed to be zero. No scientific network calls.

C240 PASS means diagnostic integrity only,independent of rule agreement. Require exact parent and
source/artifact identity,byte/schema validation,discrete-metric replay,complete counts and persisted
analysis recomputation. Any fault is INVALID / RETRY SAME C240. No C239 reversal or Gate F promotion.

Protection:286 source pins/430 inputs;dependency union16;OWN6. Own tests24;modules125;
loaded2930/focused2929. Only inherited exact historical exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored local outputs:audit-plan.json,row-audit.json,paired-orders.json,diagnostics.json,
validation-summary.json. Summary.json records execution/protection/artifact/integrity identities.
Postcheck recomputes all derived outputs from the original parent records without model execution.

Manifest SHA256:31d2b0579d65b354979ef1d98e3012a57a95820e2f12cd729c931c8d8525bc25.
Design:docs/v5b-saved-positional-rule-audit-v0.1.md.
Registration:docs/experiment-ledger-addendum-c240-preregistration.md.
Preregistration commit:aa4f6811f201fcbcc89184ca445c500dad31edb0.
Use tools/invoke_active.ps1 with the final activation/handoff HEAD,not C239 or preregistration HEAD.

## C240 post-authoring review

`post_authoring_review = PASS`
Review HEAD:aa4f6811f201fcbcc89184ca445c500dad31edb0.
Scope:source/static and synthetic-saved-data authoring review,not formal C240 execution.

All6 OWN files were re-fetched at this committed HEAD after authoring finished. Reviewed blobs:
-benchmark:eacd759d1f0b19e0e03cd4df2c2592db85b6d883
-tests:123591244286bc2aa7238536dd4e802855bd4448
-runner:bc1b57d592925db5e3dbd8c391d9bcc921733a89
-launcher:d075d5ca8e52b690caf5aa04b610557e2a5f31e1
-preregistration:9e0463fb529ba300db9e3879c6ccc39db5be8b61
-design:5c4581b8f851438433fe46efceac6c25554c2e04.
The four code/script blob identities were mechanically matched to the full local files used for
tests. Comparison from acceptance base to review HEAD changes exactly the6 OWN additions.
No accepted source/test/log or shared launcher changes.

Actually executed after readback:
-UTF-8/NUL checks and Python compile/import for complete new source/test files;
-24 own tests PASS in0.029s;actual own loader count/unique IDs checked;
-manifest and independently reconstructed exact parent partition digests match;
-Python symbol-table/global-binding audit:zero unresolved names,including import-provided __file__;
-synthetic binding,fixed-position,first/last/constant and outside-value cases;
-explicit TRAIN/HOLDOUT rule degeneracy and matched-order counterpart checks;
-discrete metric consistency,nonfinite/schema/replay-flag and output-byte rejection;
-actual loader on synthetic parent-shaped files,with a substituted parent summarizer;
-actual run and persisted postcheck on six synthetic saved-answer records,with substituted
 context/protection/parent-loader adapters;wrong-HEAD and artifact-tamper rejection;
-source AST checks no fit/backward/step/model creation/state loading/evaluation/tokenization calls;
-three embedded Python blocks compile;precheck argv1 and postcheck argv1/2/3 match invocation;
-parent paths and parser-before-publication call ordering checked in runner/launcher.

The initial local authoring suite detected a fact_pair metric-key spelling defect;it was fixed
before source publication and all tests passed before and after remote readback. No scientific
conditions or accepted files were changed to resolve it.
C239 writer/replay/summary source was read to confirm final/predictions timing and split schema,
and its4-row-per-language metric contract. Parent imports are lazy;tests use synthetic adapters,
not the user's checkpoint or actual C239 saved predictions. No NLL reconstruction is claimed.

Reviewer runtime:Python3.13.5 in an isolated namespace workspace,not a full repository checkout.
The available container has PyTorch2.10.0+cpu/NumPy2.3.5,but C240's own tests use Python data only.
A GitHub clone/read attempt failed DNS resolution;connector tools provided repository reads/writes.
NOT executed here:full2929-test historical suite,Windows PowerShell AST,live user-local parent
artifact precheck,or C240 analysis of actual C239 predictions. These are not reported PASS.
Historical counts derive from accepted C239124 modules/2906 loaded plus24 tests;the actual runtime
suite loader must enforce125/2930/2929 and the single registered exclusion.

Only this unpinned activation/review handoff changes after review HEAD. Re-read the final handoff
and verify branch HEAD before returning ExpectedHead. Do not advance the branch during the user's run.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted sources/tests/logs and
tools/run_c167.ps1. No cleanup/history rewrite,paid API,external corpus,larger model or production change.
24 own tests ->2929 focused tests ->C240 saved-answer audit ->artifact postcheck ->remote log publication.
Stop same C240 on integrity faults;repair transport-only failure without repeating completed analysis.
Judge C240 before registering C241.
