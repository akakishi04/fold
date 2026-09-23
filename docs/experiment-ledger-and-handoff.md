# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C243 ACCEPTED PASS (diagnostic integrity only). C244 ACTIVE / NOT YET JUDGED. C245 NOT REGISTERED.**
C244 is the unique ACTIVE experiment:V5-B two-partner recombination learning,not a Gate F run.
Post-authoring review PASS. Authoritative runtime prechecks/full regression/scientific run pending.
C242 remains ACCEPTED VALID NEGATIVE. No accepted capability boundary is expanded by C243.

## Latest accepted evidence — C243

Scientific execution HEAD:1ff8bcfd4905b54c9f685eee26e197eb62394ab2.
Published log commit:8dbf3c9a2ed661b8b826243ee996aa1057b19eba.
Publisher log SHA256:53b5dbb8867f5f02dfd79225a0dd2e9fbf7541ef2ba98df5b6ab2e7d43784ace.
Log bytes:573039.
Summary SHA256:adf53e7f0306ab9d3fa209f24fb4fa1dbdc3d717037a4e7931579e670acdd2ce.
Local summary:runs/c243-v5b-saved-recombination-audit-9a4a52f99ee2402dbbc3cb303935217a/summary.json.

24 own tests PASS in0.276s;3001 focused tests PASS in90.778s.
304 source pins/466 protected inputs.1728 saved answers,576 normal rows,5760 rule comparisons,
864 pair records,24 diagnostic cells. Scientific forwards/training/checkpoint loads/writes0.
All discrete replays and persisted audit recomputations passed;protected inputs/clean tracked
tree/execution HEAD preserved;run_execution_valid=True. NLL was not reconstructed from argmax.

TRAIN:192/192 normal answers correct;partner_of_other also matches192/192 by dataset identity.
HOLDOUT (each family192 answers):

| Category | Full | GRU-only | Total |
|---|---:|---:|---:|
| correct |65|66|131|
| other_supplied |9|29|38|
| absent_partner_of_other |99|67|166|
| absent_partner_of_queried |19|30|49|
| other_byte |0|0|0|

215/384 answers were absent from the prompt.166/384 match the TRAIN partner of the nonqueried
value. This is not a universal rule:the families and individual cells differ. Four named digit
categories exhaust0..3 on this HOLDOUT. Do not infer an internal algorithm or causal module from
category membership;do not treat pooled predictions as independent training experiments.
No new capability,independent replication,NLL replay,core superiority or Gate F claim.

Acceptance/artifacts:docs/experiment-ledger-addendum-c243-c244.md.
Acceptance/base commit:432ecaa53da0f45806793865d88334fbbb90569f.
The published log commit is one after execution and changes only c243/latest.log/latest.json.
Acceptance used retrieved immutable log ranges and recorded local postchecks,not a reviewer
checkpoint rerun or independent full-log byte rehash. C242 remains a valid negative.

## Preserved earlier evidence

C242:all12 TRAIN cells pass,all12 held-pair cells RECOMBINATION_MISS;one-partner TRAIN ambiguity remains.
C241:normal TRAIN100% but evidence drop0 and swapped HOLDOUT0%;full TRAIN criteria miss.
C240:diagnostic PASS;C239 errors largely matched fixed query-to-position behavior.
C239 valid order-transfer negative;C238 seen16-prompt fit PASS;C237 diagnostic PASS;
C236 random-batch valid negative;C235 diagnostic PASS;C234/C233 valid negatives.
All accepted sources/tests/logs and their earlier recovery records remain unchanged.

## Active C244 — two-partner recombination

Experiment:C244-v5b-two-partner-recombination.
Stage:V5-B-TWO-PARTNER-RECOMBINATION.
One question:can fresh models transfer to still-held pairs when every TRAIN value has two
partners,at the same400 updates,batch32 and total training presentations?

Use C242's exact saved TRAIN32/HOLDOUT64 pool. TRAIN64 is old block32 followed by added block32.
Old pairs:(0,1),(1,0),(2,3),(3,2).
Added pairs:(0,2),(2,0),(1,3),(3,1).
Remaining HOLDOUT32:(0,3),(3,0),(1,2),(2,1).
Preserve original within-block row order,prompt/target/provenance,both orders,queries,languages.
Prompt/ID/assignment-group sets are disjoint. No unseen vocabulary or pristine external-test claim.

Before training require joint language/query/order/target balance in each32-row block. On the
TRAIN union,lookup from language/query/order/nonqueried value has at most50% accuracy,not C242100%.
Query-only ceiling25%;masked evidence25%,masked query50%. These are finite-data ambiguity ceilings,
not model accuracy. Each isolated block still has a unique partner relation;do not omit that caveat.
No block/step identifier is input.

Fixed fresh models:Full13488/GRU-only10160,width16/48 slots,seeds234001/234002/234003,C242 initial
fingerprints,common-weight baseline copy before either fit,same byte renderer,256-way output.
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 updates,CPU float64,
threads2,deterministic algorithms. No trained parent checkpoint reuse.

Alternate blocks:human update1 old,update2 added,through400 added.200 updates/block and200
presentations/TRAIN row. Every actual training input batch is checked against its scheduled block.
Fit executable AST differs from C242 only in the progress tag and step-dependent ids expression.
Coverage,repetitions,schedule change jointly;last-block effects/interference remain possible.
Only TRAIN is evaluated initially;HOLDOUT after400 updates and replay,never for training or selection.

Reuse C242 dynamic-size evaluator/validator/gate and actual C234 renderer/fact/query metrics.
Both splits have complete fact/query/order pairs. Full primary requires every seed/language to
pass BOTH splits:accuracy>=0.90,all three paired criteria>=0.80,both mask drops>=0.35.
TRAIN32 rows/language,16 pairs/kind:29/32 answers and13/16 pairs minimum.
HOLDOUT16 rows/language,8 pairs/kind:15/16 answers and7/8 pairs minimum.
GRU-only gate independent. Report TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS.
A valid miss is ACCEPTED VALID NEGATIVE;integrity failure is INVALID / RETRY SAME C244.
Even PASS is this bounded transfer only,not general language,all shortcuts removed,core superiority
or unique causal attribution. Gate F remains NOT PASSED.

C242 comparator:recompute its saved discrete metrics on exactly the remaining HOLDOUT32 by row ID,
not its full HOLDOUT64 and never the promoted rows. Store c242_same_holdout_discrete and report
accuracy deltas. Comparator is reused evidence,not a fresh run;no parent NLL reconstruction.

Workload:6x400=2400 updates/76800 training presentations.90 scoring forwards/4608 scoring rows;
2490 total model forwards/81408 rows. Before reload409/13280 per model;after415/13568.
One six-state bundle,schema fold-c244-two-partner-v1;zero parent inference/scientific network calls.
Protection:310 source pins/478 inputs;direct dependency union20;OWN6.
Own tests24;modules129;loaded3026/focused3025;only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:two-partner-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. New counters retain train_steps,answer_presentations,model_forward_calls,
row_presentations. Postcheck verifies partition,initial/comparator replay,child discrete metrics,
normalized plan,hashes/sizes and summary. No protected historical file is changed.

C243 parent summary:adf53e7f0306ab9d3fa209f24fb4fa1dbdc3d717037a4e7931579e670acdd2ce.
C242 source summary:d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb.
C244 split:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
C244 manifest:e89a41c15ef3d702c7009a9b4fc22f4e28809dea3892c5d63cf02120a1e10b0b.
Design:docs/v5b-two-partner-recombination-v0.1.md.
Registration:docs/experiment-ledger-addendum-c244-preregistration.md.
Preregistration/review HEAD:71fbdada9de594170bf95fd429a75454f840f55f.
Use tools/invoke_active.ps1 with the final activation HEAD,not the review/C243 execution HEAD.

## C244 post-authoring review

`post_authoring_review = PASS`
Review HEAD:71fbdada9de594170bf95fd429a75454f840f55f.
Scope:committed-byte authoring review and synthetic-path execution,not a formal C244 result.

All six OWN files were re-fetched after authoring. Reviewed blobs:
-benchmark:a59230da23b07838582360b8e180f471c7fa7f58
-tests:be7331a63a494cf1a031001668fc4a7b8975315a
-runner:ef2513d207d6ff2867ffef231c6db7fd97c1d6b6
-launcher:2c1407899d7958136710cd56c753f900089a7048
-design:5bd70fac5fd302157d3ba53d8340e4bf926bd708
-preregistration:b293b657e8cb598d61fb588c36aa39a284754bdd.
The four complete code/script local files were mechanically hashed using Git blob framing and
matched the returned immutable remote blob IDs. Comparison from acceptance/base to review HEAD
contains exactly six additions and no parent source/test/log/shared-launcher changes.

Actually executed on those matched files:
-UTF-8/NUL checks,Python compile/import,three embedded Python block compiles;
-symbol-table free-global/import audit:zero unresolved names in the two complete new Python files;
-all24 own tests PASS before publication in5.714s and after readback in4.640s;
-actual own unittest loader count/unique IDs and a constructed3026-case filter to3025;
-source split/new split/manifest hashes,block coverage,joint balance and ambiguity-ceiling checks;
-400-step schedule enumeration verifies each of64 indices appears200 times;
-fit AST/constant comparison against the exact retrieved C242.fit excerpt;
-actual training input capture,holdout-after-fit barrier,initial mismatch rejection;
-train/replay hook counts409+6 and13280+288 rows,block counts[200,200],bad replay rejection;
-actual new six-model run/save/reload/postcheck with synthetic models and substituted parent/
 protection adapters,including wrong-HEAD/tampered-artifact rejection;
-identical-HOLDOUT comparator ignores deliberately corrupted predictions on promoted rows;
-actual loader dispatch,common-copy-before-fit,save-before-load/replay and CLI argv1/2 then1/2/3/4.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Isolated workspace contains full
new files,synthetic Binding/Fitting/Factory/Parent adapters,and a reviewer-only import scaffold
with the retrieved immutable C242.fit excerpt. This is NOT a complete repository checkout.
A git ls-remote attempt failed to resolve github.com. Connector tools supplied repository reads/
writes. The real parent C242/C243 call/schema semantics were source-reviewed;the existing evaluator
was not executed on actual FOLD models by the reviewer. No scientific C244 predictions were produced.

NOT executed here:full3025-test historical suite,Windows PowerShell AST,accepted user-local parent
artifact prechecks,or the actual six-model FOLD/GRU C244 run. These are not represented as PASS.
The ordered authoritative Windows launcher/runner must perform all those checks. Counts derive
from accepted3002 loaded plus24 new tests;the actual loader enforces3026/3025 and unique IDs.

Only this unpinned handoff activation/review changes after review HEAD. Re-read it and confirm final
branch HEAD before issuing ExpectedHead. Do not advance the branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted evidence and tools/run_c167.ps1.
No larger model,extra training presentations,paid API,external corpus,cleanup,history rewrite or
production runtime change.24 own tests ->3025 focused tests ->C244 ->postcheck ->remote log publication.
Stop same C244 on integrity faults;repair transport-only failure without retraining. Judge C244 before C245.
