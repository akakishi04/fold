# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C245 ACCEPTED PASS (diagnostic integrity only). C246 ACTIVE / NOT YET JUDGED. C247 NOT REGISTERED.**
C246 is the unique ACTIVE experiment:V5-B training-only distractor erasure with normal-input scoring.
Post-authoring review PASS. Authoritative runtime prechecks/full regression/scientific execution pending.
C244 remains ACCEPTED VALID NEGATIVE. No accepted capability boundary is expanded by C245.

## Latest accepted evidence — C245

Scientific execution HEAD:db838801cc139b4578c2aa002cbc001c58fa1e91.
Published log commit:4ef5145ef98617183761d80652135466479394e7.
Publisher log SHA256:3f1c23b26b97029dc326a8007616aade19741896f443bbbf79c5221fe02abb13.
Log bytes:590659.
Summary SHA256:ae2f2a940a7c9f903bac8f8f472680654abe305df897d011e61a355e4d9d9d88.
Local summary:runs/c245-v5b-selective-evidence-484b9afa921e4fe4a3430a1d7a88e4d4/summary.json.

24 own tests PASS in3.542s;3049 focused tests PASS in94.725s.
316 source pins/490 protected inputs. Six frozen C244 models,60 forwards/2880 rows;
zero training steps/checkpoint writes. All original predictions/metrics including NLL replayed;
fingerprints unchanged;persisted-logit diagnostic replay PASS;tracked tree clean;execution HEAD
preserved;run_execution_valid=True. The publication changes only c245/latest.log/latest.json.
Acceptance uses immutable retrieved log ranges and recorded local postchecks,not an independent
full-log byte rehash or reviewer execution of the actual trained models.

HOLDOUT counts pooled over3 seeds/2 languages,96 answers/family:

| Family | Normal | Queried value hidden | Other value hidden |
|---|---:|---:|---:|
|Full|39/96|4/96|59/96|
|GRU-only|41/96|2/96|82/96|
|Both, descriptive only|80/192|6/192|141/192|

Queried-value erasure worsened all12 cells;other-value erasure improved all12. For other erasure,
64 normal-wrong became correct and3 normal-correct became wrong,net+61. This is not independent
training replication or a capability improvement. TRAIN normal100%;other-hidden Full118/192,
GRU-only164/192,so erasure is not uniformly beneficial on the original TRAIN/HOLDOUT distribution.

Critical boundary:the other-hidden distinct input sets coincide across TRAIN/HOLDOUT. TRAIN
repeats each masked form twice;HOLDOUT once. The unchanged-query/value/order/language support
explains identical normalized masked scores. Selective masked accuracy is NOT held-pair transfer.
Erasure also marks the answer-bearing field by leaving only its value visible. Distribution shift,
copying cues and redundancy preclude a unique internal-mechanism or defective-module conclusion.
Do not adopt inference masking as a production fix or reverse C244/Gate F.

Acceptance/artifacts:docs/experiment-ledger-addendum-c245-c246.md.
Acceptance/base commit:87fe39481ae65cdf2452f2cb79ba0b8f6d912a2a.

## Preserved earlier evidence

C244:all TRAIN criteria pass;all12 HOLDOUT cells RECOMBINATION_MISS;normal80/192 pooled.
Scientific execution:d89007bc5a04c4f6b99bff966093b0e14174e04b;published log:d1e2933492cf4f4d0cbfb535c80b800c58bcadf7.
Summary:a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297.
Local:runs/c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639/summary.json.
C243 diagnostic PASS on C242 saved errors;C242 recombination negative;C241 full TRAIN criteria miss
because evidence_drop0 despite normal100%;C240 diagnostic PASS;C239 order-transfer negative;
C238 seen16-prompt fitting PASS;earlier accepted sources/tests/logs/recovery records remain unchanged.

## Active C246 — training-only distractor erasure

Experiment:C246-v5b-training-only-distractor-erasure.
Stage:V5-B-TRAINING-ONLY-DISTRACTOR-ERASURE.
One question:can other-value erasure on half the scheduled TRAIN presentations improve the
ordinary fully observed held-pair endpoint at the same C244 initial states,model and training budget?

Keep exact C244 TRAIN64/HOLDOUT32,row order,labels,provenance and row-index schedule. No held-row
promotion. Use C245.masked_prompt/tensors for TRAIN only:replace one nonqueried factual digit
with '?' based on the visible query,not the target label. Preserve every other byte and EOS.
This is explicit relevance/copying supervision;the model does not choose the erased field.

Four-update cycle:masked-old,masked-added,normal-old,normal-added,100 repetitions. Each block
receives200 updates;each row100 normal+100 masked exposures. Final step400 is normal-added.
Actual forward input tokens are checked against the C244 row indices and independent view schedule.
No step/block/row ID or separate mask flag enters the model.

Fresh models:Full13488/GRU-only10160,width16/48 slots,seeds234001/234002/234003. Match C244
initial_sha256,not trained finals. Construct common-weight GRU-only copy before either fit.
Same byte tokenizer/unrestricted256-way output,AdamW lr0.005,betas(0.9,0.999),eps1e-8,
weight_decay0,clip1,batch32,400 updates,CPU float64,threads2,deterministic algorithms.
Fit AST differs from C244 only in progress label and input-view selection. No auxiliary loss,
extra model forward or optimizer change. Normal presentations halve;total presentations do not grow.

Capability endpoint is the original C244 normal TRAIN/HOLDOUT inputs plus inherited evidence/query
mask controls. No selective masked HOLDOUT is scored as success:those forms overlap TRAIN masks.
All normal held-out strings remain disjoint from both TRAIN views. Only TRAIN evaluated initially;
HOLDOUT first reaches the model after400 updates and during reload. No tuning or early stop.

Use actual C242 evaluator/gate, C234 renderer/metrics and C244 summarize/replay helpers. C245.load_inputs
must receive the C244 summary,not the C245 one. It verifies C244.summarize(refs,C242);C246 additionally
validates initial identities. Stored c244_comparator is unchanged C244.final on the identical rows.
Report each seed/language normal accuracy and delta,not C245's easier masked score.

Primary Full gate on BOTH splits:accuracy>=0.90;fact/query/order pair>=0.80;both mask drops>=0.35.
TRAIN32 rows/language,16 pairs:minima29/32,13/16. HOLDOUT16 rows/8 pairs:minima15/16,7/8.
GRU-only independent. Preserve TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS labels and actual metrics.
A valid primary miss is ACCEPTED VALID NEGATIVE;integrity faults INVALID / RETRY SAME C246.
A pass is bounded normal-input transfer only,not general language,core superiority or Gate F.

Workload:6x400=2400 updates/76800 training rows;38400 normal+38400 masked.
90 scoring forwards/4608 scoring rows;2490 total forwards/81408 total rows.
Before reload409 calls/13280 rows per model;after415/13568. block_view_updates=[[100,100],[100,100]].
One new six-state bundle,schema fold-c246-training-erasure-v1;no parent checkpoint load/model inference.
Scientific network calls0. Original C244 final metrics are reused evidence,not new baseline inference.

Protection:322 source pins/502 inputs;direct dependency union22;OWN6. Own tests24;modules131;
loaded3074/focused3073 with only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:training-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Postcheck verifies hashes/sizes,plan,partition,initial/comparator identity,
summary and child discrete metrics via C243. New checkpoint predictions/logits/NLL must replay.

C245 summary:ae2f2a940a7c9f903bac8f8f472680654abe305df897d011e61a355e4d9d9d88.
C244 split:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
C246 manifest:761b00863243d9118cd85058f585b7e3592404c677b8d8f548be45ed2fd05db8.
Design:docs/v5b-training-erasure-v0.1.md.
Registration:docs/experiment-ledger-addendum-c246-preregistration.md.
Preregistration/review HEAD:7c1468ca9573bdb8b48bced2a5d1179e405ef66f.
Use tools/invoke_active.ps1 with the final activation HEAD,not the review or C245 execution HEAD.

## C246 post-authoring review

`post_authoring_review = PASS`
Review HEAD:7c1468ca9573bdb8b48bced2a5d1179e405ef66f.
Scope:committed-byte authoring/synthetic-path review,not a scientific C246 result.

All six OWN files were re-fetched at the immutable review HEAD after all authoring commits.
Reviewed blobs:
-benchmark:c343f5c8939ed9d5e7a9da9b65a9c9ea6fab68d5
-tests:67f097c4a5ebb5b3834493558424bf5d79bcb068
-runner:a1dad2801cf0033fd3e41c5efe2951ec05cb3d0b
-launcher:6719e3afb09d709342c395884838b3a022384221
-design:db92de280c310a5d07442d0aaf4e9d4ebf1154a5
-preregistration:f4b85b2da4e339054d1345c3bebd0126238d61a6.
The four complete local code/script files were Git-blob hashed and exactly matched the fetched
remote identities. Base-to-review comparison contains exactly six additions,no accepted edits.
A harmless runner error-message wording difference was synchronized to the fetched text before
this final byte match and test rerun;the test/benchmark scientific source did not change.

Actually executed:
-Python compile/import,UTF-8/NUL checks;symbol-table free-global/import audit:zero unresolved names
 in both new Python files;three embedded Python blocks compiled;
-all24 own tests PASS before publication in6.458s and after remote-byte matching in6.587s;
-own unittest count/unique IDs plus a constructed3074-case exclusion filter to3073;
-exact source partition/manifest hash,one-token erasure,target-not-read and data-overlap controls;
-400-step row-schedule equality and per-row100/100 exposure enumeration,final-normal phase;
-fit AST comparison against the retrieved immutable C244.fit excerpt,constant-tamper rejection;
-actual fit inputs,independent wrong-view rejection,holdout-after-fit boundary,initial mismatch barrier;
-actual training/replay counts409+6 and13280+288 rows with matrix[[100,100],[100,100]];
-six-model new run/save/reload/postcheck using toy models,substituted protected-input/loader adapters,
 and C244 replay/summarize excerpts;wrong-HEAD/tampered-output/bad-logit tests;
-error hook cleanup,family-gate separation,checkpoint order,loader/common-copy/save/replay call order;
-CLI argv1/2 then1/2/3/4,exact parent paths and parser-before-publication boundaries.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Isolated workspace contains the complete
new files,synthetic Binding/Fitting/Factory adapters and reviewer-only import scaffolding with
transcribed immutable C244 fit/balanced_indices/replay_one/summarize and C245 mask/tensor excerpts.
It is NOT a full repository checkout. github.com DNS resolution failed;connector reads supplied
repository bytes. PowerShell was unavailable. The actual C244/C245 parent schema/signatures were
source-reviewed. No actual accepted model was loaded and no scientific C246 predictions produced.

NOT executed here:full3073-test historical regression,Windows PowerShell AST,accepted user-local
artifact precheck or the six-model FOLD/GRU scientific run. None is represented as PASS.
The authoritative ordered launcher/runner must execute those checks. Counts3050+24=3074 minus
the same one exclusion=3073 are enforced by its actual runtime suite loader.

Only this unpinned activation/review handoff changes after review HEAD. Re-read it and confirm
final branch HEAD before returning ExpectedHead. Do not advance the branch during the user's run.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted sources/tests/logs and tools/run_c167.ps1.
No inference masking fix,extra training budget,larger model,paid API,external corpus,cleanup,
history rewrite or production runtime change.24 own tests ->3073 focused tests ->C246 ->postcheck ->log push.
Stop same C246 on integrity faults;repair log-only transport without retraining. Judge C246 before C247.
