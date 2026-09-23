# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C238 ACCEPTED PASS (minimal seen-TRAIN fitting). C239 ACTIVE / NOT YET JUDGED. C240 NOT REGISTERED.**
C239 is the unique ACTIVE experiment, a fresh fact-order holdout, not a Gate F run.
C236 remains ACCEPTED VALID NEGATIVE; C237 remains diagnostic-integrity PASS only.
Post-authoring review is PASS; authoritative runtime prechecks and regression remain mandatory.

## Latest accepted evidence — C238

Scientific execution HEAD: `a7999c92e2f6f071c045de268feaf5ddd6f438ac`.
Published log commit: `93a86ea4493c4c6bf20b046b56c29e8bccc322f9`.
Log SHA256: `da9386a9f351ebf9aeec18df7057aac9971c4b068fbe337efdcf7363260b8e60`.
Summary SHA256: `06ab54549477894ea17f986364cacc6b3b7d25ff2dea70b18e98e2a957c80363`.
Local summary: `runs/c238-v5b-complete-cohort-sampler-df6538e306784434bdcbb2848e4c278d/summary.json`.

24 own tests PASS in3.553s;2881 focused tests PASS in72.485s.274 source pins/406 protected inputs.
Six models x400 updates:2400 steps/76800 answer presentations;2454 total forwards/77664 rows.
Initial/final replays, changed weights and recorded C236 comparator checks PASS.
Protected inputs preserved;tracked tree clean;execution HEAD preserved;run_execution_valid=True.

All12 cells:100% accuracy (8/8),fact/query pairs4/4,evidence/query mask drops50 percentage points.
C236 had50% accuracy,0/4 pairs and0 mask drops. Both Full and GRU-only now pass every criterion.
The registered sampler intervention was sufficient for this observed improvement, but does not
isolate coverage versus balance versus gradient variability. Memorization remains possible.
No general-language, unseen-generalization, core-superiority or Gate F claim.

Acceptance/artifact identities: docs/experiment-ledger-addendum-c238-c239.md.
Acceptance record commit: `72907fe195f56b886a9bc9b9fc0db6c83f9cbda2`.
Acceptance/handoff base before C239 authoring: `74100dd8c7b151f0cdd44e36ef846825614d7836`.
Acceptance is based on published evidence/postcheck, not a reviewer checkpoint rerun or full-log rehash.

## Preserved earlier evidence

C237 diagnostic PASS: internal numerical responses without correct answer switching.
Details: docs/experiment-ledger-addendum-c237-c238.md.
C236 valid negative on16 prompts with random replacement batches; do not rewrite or rerun it.
Details: docs/experiment-ledger-addendum-c236-c237.md.
C235 diagnostic PASS: failure already on complete TRAIN, not only EVAL; first invalid attempt preserved.
C234/C233 remain valid negatives; C232 remains bounded template-byte learning only.

## Active C239 — fresh fact-order holdout

Experiment: C239-v5b-fact-order-holdout.
Stage: V5-B-FACT-ORDER-HOLDOUT.

One question: can complete-cohort training on order0 transfer to the matched order1 prompts that
are withheld from the newly initialized model's training?

Changed: same fixed16-row pool is partitioned into order0 TRAIN8 and order1 HOLDOUT8.
TRAIN is box then book; HOLDOUT reverses the fact order. Both contain both0/1 assignments,
queries and languages. Exact prompts/row IDs are disjoint; underlying fact groups deliberately
remain shared. This tests presentation-order transfer, not unseen facts/entities/values.
Rows retain parent split="TRAIN" provenance; the outer C239 partition defines optimizer membership.

Held fixed: same Full13488/GRU-only10160 parameters,width16/48 slots,byte renderer,256-way output,
three views,seeds234001/234002/234003,AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,
clip1,batch32,400 steps/model,CPU float64,threads2,deterministic algorithms.
Fresh models must match C238 initial_sha256; NEVER continue from C238 trained states, which saw
both orders. Make the common-weight GRU-only copy before either member trains.
The fit body is AST-matched to C238 apart from the progress label. The index helper repeats all8
TRAIN rows4 times per batch. Repetition per retained row increases800->1600 as a cohort consequence.
This is not a matched all16 resubstitution-accuracy comparison to C238.

TRAIN only is evaluated before training. Fit receives TRAIN tensors/targets only. HOLDOUT is
first rendered for model evaluation after the400-step endpoint; it cannot control training,
early stopping, checkpoint/seed selection or further updates.
The actual C234 renderer/evaluator/paired metrics are reused. Parent C238 metrics have8 rows per
language (the preregistration's parent-schema wording must be read as8, not4). C239 metrics have4
rows per language per split and use a separate explicit validator, not the parent's8-row validator.

Fixed workload:6 models x400 =2400 training steps/76800 answer presentations.
Per model:initial TRAIN3 +final TRAIN3/HOLDOUT3 +reloaded TRAIN3/HOLDOUT3 =15 scoring forwards.
90 scoring forwards/720 rows;2490 total forwards/77520 rows. One six-state checkpoint bundle.
Before reload409 forwards/12872 rows per model;after reload415 forwards/12920 rows.
No parent model forward, external data or scientific network call.

Primary gate: every Full seed/language cell must pass BOTH TRAIN and HOLDOUT criteria:
accuracy>=0.90,fact/query paired both-correct>=0.80,evidence/query mask drops>=0.35.
Discrete exact/pair requirements are4/4 and2/2 per language/split. GRU-only gate is independent.
Report TRAIN_FIT_MISS,ORDER_HOLDOUT_MISS,BOTH_PASS separately using all criteria,not accuracy only.
A valid primary miss is ACCEPTED VALID NEGATIVE; an integrity fault is INVALID / RETRY SAME C239.
Even PASS is only this one-direction order transfer,not general understanding or Gate F completion.

Protection:280 source pins/418 protected inputs;direct dependency union15;OWN6.
Own tests24;modules124;loaded2906/focused2905 with only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:holdout-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Checkpoint schema fold-c239-order-holdout-v1;six ordered state dicts.
Guard initialization,weight updates,non-mutating evaluation,actual workload and exact prediction /
1e-9 logit/metric replay for both partitions. Postcheck verifies hashes,split,plan,summary,initial IDs.

Manifest SHA256: `4eca2f0276b521286729f1819abd929a035659a589488b332fe976d392b4dac0`.
Split SHA256: `6f47a61c0ec4de616e77dab803ad964a9243e627b8a06f3e987d2824f8951731`.
Design: docs/v5b-fact-order-holdout-v0.1.md.
Registration: docs/experiment-ledger-addendum-c239-preregistration.md.
Preregistration commit: `b3ee017e52c328a6a429f0d61b998b7d9a63b03a`.
Use tools/invoke_active.ps1 with the final activation/handoff HEAD,not the older C238 or review HEAD.

## C239 post-authoring review

`post_authoring_review = PASS`
Review HEAD: `b3ee017e52c328a6a429f0d61b998b7d9a63b03a`.
Scope: authoring/static and synthetic-path checks,not a formal C239 scientific result.

All6 OWN files were re-fetched from the committed review HEAD after authoring finished.
The four source/script Git blob IDs were mechanically matched to the locally tested full files:
-benchmark:d5d06c817bc821917d901545dd859c759b13cdfc
-tests:3dcb31da9e87f7927719fc05cc5187a94b24398d
-runner:5a56f38bf7888f6d9a2512bc5c8eb6827c042208
-launcher:2955f7f3126b6048094d6fe66c340f2d7e9497b1
Reviewed preregistration blob:ad2f4c55ee1c4ed6340ff585b508f711cdc8d665.
Reviewed design blob:cbd2d076dcbd0fb039a9409d4f90a7314a5059c2.
Comparison from acceptance base74100dd8 to review HEAD changes exactly these6 additions.
No accepted source/test/log or shared launcher is edited.

Checks actually executed after remote readback:
-UTF-8/NUL and full-file Git blob checks for both Python files and both PowerShell files;
-Python compile/import;free-global/import binding audits:zero unresolved names in both Python files;
-all24 own tests PASS in2.550s after readback (earlier authoring run2.738s);
-actual own unittest loader count and unique IDs;
-manifest and independently reconstructed pool/partition hashes;
-fit AST equality against an independently transcribed immutable C238 fit excerpt from remote,
 with constant-change rejection;the helper is deliberately8x4 rather than16x2;
-actual fit input capture confirms each batch contains TRAIN8 four times and no order1 row;
-actual train_one rejects wrong initial state before fit and refuses holdout evaluation before fit ends;
-training/reload hooks confirm409+6 calls and12872+48 rows per model on synthetic models;
-synthetic six-model run,checkpoint save/reload and persisted postcheck including tamper/HEAD rejection;
-loader path on synthetic parent-shaped files,initial/final identity separation and partition checks;
-source AST confirms loader/common-copy-before-training and save/load/replay order;
-three embedded runner Python blocks compile;precheck argv1,postcheck argv1/2/3 and invocation order.

Parent C234 evaluator/paired-metric source was read:it derives subgroup sizes from rows and supports
these complete pairs. C238 writer/context/fit and the inherited C236 metric contract were reviewed:
initial fields precede training;parent metrics have8 rows/language,new split metrics have4.
No parent trained checkpoint is used as initialization. New child loaders are used by the run path.
Launcher inspection confirms branch/tree/HEAD/ACTIVE guards before logging and ParseFile before
runner invocation. Full historical counts are inherited2882 plus24 =2906,excluding the same1 =2905.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,isolated package scaffolding and
synthetic models,with a C238 fit excerpt,NOT a complete repository checkout. The container's
GitHub access attempt failed DNS resolution. The connector supplied source reads/writes.
NOT executed here:full2905-test historical regression,Windows PowerShell AST,accepted user-local
artifact precheck,or the six actual FOLD/GRU scientific models. None is represented as PASS.
These remain mandatory in the authoritative launcher/runner before scientific acceptance.

Only this unpinned activation/review handoff changes after review HEAD. Re-read this final file and
verify branch HEAD before returning ExpectedHead. Do not change the branch during the user's run.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted sources/tests/logs and
 tools/run_c167.ps1. No history rewrite,cleanup,paid API,external corpus,larger model or production change.
24 own tests ->2905 focused tests ->C239 fresh order-holdout ->artifact postcheck ->remote log publication.
Stop same C239 on integrity faults;repair transport-only failure without retraining.
Judge C239 before registering C240.
