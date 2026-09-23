# C242 preregistration — balanced value recombination

Experiment:C242-v5b-balanced-value-recombination.
Stage:V5-B-BALANCED-VALUE-RECOMBINATION.
C241 ACCEPTED VALID NEGATIVE; C243 NOT REGISTERED. Gate E PASSED; Gate F NOT PASSED.
This document registers C242. Execution requires independent committed-byte post-authoring review
and activation in the authoritative handoff. No automatic C243 run.

## One question

Can fresh models trained with variable entity values and both fact positions solve held-out
combinations of the same four values under the fixed400-step/batch32 complete-cohort recipe?
This addresses C241's evidence-redundant TRAIN distribution rather than blaming the architecture.
It is a new bounded recombination task, not a matched one-variable accuracy comparison to C241.

## Accepted evidence and inputs

Acceptance record:docs/experiment-ledger-addendum-c241-c242.md.
Acceptance/base commit:0caa412ce1ce6452d721adac19d2d37f6e3d0128.
C241 execution HEAD:b7b33718da1edd94cc1ed113baa6e56cc27dc3e4.
Published log commit:a53a96e6e2ec716d33ab3f7f8ae9cb2d49d110a0.
Publisher-recorded log SHA256:5067ca2deefdc14b03e72500918bc2eae134f8a01b1751e1be450a93275f50f8.
C241 summary SHA256:b228992dfd5d85e59d7c45d1dd899145588978a19ade0817a547d740e8c67e26.
C241 local summary:runs/c241-v5b-assignment-holdout-445ca70720c948e7966236416922e580/summary.json.
Require exact valid negative and cell_outcomes TRAIN_FIT_MISS:12; do not require a parent PASS.

Required C241 artifacts:
- assignment-plan.json:1552239e7701744af508ba41ac4b620898d219380b377be1c5671b816dbac1f8
- measurements.json:2ad0f83840e01fa2f074b0a313261b8c662ec4d40a9c8a13d0a24be0c0506111
- split-dataset.json:1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a
- trained-models.pt:102102b1f7318ca1fc720afda96c9118a526ea48eb007ef8ed76bfa586dca9aa
- validation-summary.json:389555ca1313aa86e3635a28397ac98613206373b9b6bbe15eaf1e69a2889917

The full C234 dataset is already protected by the C241 input chain:
runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/dataset.json.
Required SHA256:72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85.
Check its exact resolved path in inherited input_sha256 and file hash; do not count it again.
Call actual C234.validate_dataset, then select the registered rows. Do not substitute the test fixture.

Parent record adapter:actual C241.summarize must reproduce its saved validation_summary.
Validate six ordered seed/family records and initial_sha256 format, distinct from final_sha256.
C241's writer stores initial_sha256 before training and final_sha256 afterward. New models must
match the former. No trained parent checkpoint is loaded, even though all artifact bytes are protected.
C241 final metrics use query/order pairs and four rows per language; do not misread them as C234 metrics.

## Partition and necessary-information audit

Select objects[0,1] from the576-row source dataset and preserve original row bytes/order.
TRAIN ordered value pairs:(0,1),(1,0),(2,3),(3,2).
HOLDOUT:the other eight ordered distinct pairs from0,1,2,3.
For each pair include both fact orders,queries,languages. TRAIN32/HOLDOUT64.
Split canonical JSON SHA256:9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0.

No prompt/ID/assignment-group overlap. Every language/query/order/target combination appears
once in TRAIN, twice in HOLDOUT. Every individual value/entity-value pairing has TRAIN support.
Only pair combinations are held out; no unseen word/entity/digit claim. Original source split
labels remain provenance. C242's outer partition controls optimizer membership in fresh models.
Some rows were examined in earlier research; this is not a claim of a pristine external benchmark.

Before training, group identical masked rendered inputs and compute their majority-label ceiling.
Evidence-masked maximum is25%, query-masked maximum50% on both splits. Query-only ceiling25%;
C240's fixed-query-position rule50%. These are exact finite-data controls, not model accuracy tests.
Fail precheck on a mismatch. No row IDs/targets/rule outputs enter model input.

## Fixed conditions and changed dimensions

Fresh seeds234001/234002/234003; Full13488/GRU-only10160 parameters,width16,48 slots.
Copy common backbone into the GRU-only comparator before either model trains. Require exact C241
initial fingerprints. Same C234 byte renderer and256-way unrestricted argmax.
CPU float64,threads2,deterministic algorithms. AdamW lr0.005,betas(0.9,0.999),eps1e-8,
weight_decay0,clip1,batch32,400 updates/model. Final step400 only.

C242.fit executable AST equals C241.fit except its progress tag; constants remain identical.
The helper now uses all32 TRAIN indices once instead of8 indices repeated4 times. Training
presentation count remains fixed; per-row repetitions fall1600->400 and diversity/digit coverage
increase. These are disclosed consequences, not independently identified causes.
Only TRAIN is evaluated initially. Fit accepts TRAIN tokens/targets only. HOLDOUT first reaches
the model after step400; no early stopping,tuning,selection or extra update uses HOLDOUT scores.

## Scoring and fixed gate

Use actual C234.evaluate/metrics/paired_accuracy; these derive counts from rows, so do not use a
parent fixed-size validator. In each split both value assignments exist for every unordered pair,
making fact-swap pairs valid. Add order-pair both-correct:matched assignment/query, reversed order.

TRAIN has16 rows/language and8 pairs each of fact/query/order; HOLDOUT32 rows/language and16 pairs each.
Require on BOTH splits for every Full seed/language cell:
accuracy>=0.90; fact/query/order pair accuracy>=0.80; evidence/query drop>=0.35.
Discrete minima:TRAIN15/16 correct and7/8 pairs;HOLDOUT29/32 correct and13/16 pairs.
GRU-only gate is independent, not a substitute or superiority test.
Report TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS with the actual metrics beside each label.
A valid primary miss is ACCEPTED VALID NEGATIVE; a pass is limited recombination evidence.
Neither outcome changes C241 or promotes Gate F.

## Workload and integrity

Six models x400 =2400 updates/76800 training presentations.
Per model:initial TRAIN3 forwards/96 rows;final TRAIN3+HOLDOUT3/288 rows;reload both/288 rows.
Total90 scoring forwards/4032 scoring rows;2490 total model forwards/80832 total presented rows.
Before reload409 calls/13184 rows per model;reload adds6/288;final415/13472.
One new six-state checkpoint bundle; no parent model inference or scientific network calls.

Require initial identity, changed weights, non-mutating evaluation, actual hook counts, strict
checkpoint schema/order/final fingerprint, exact prediction replay and logit/metric error<=1e-9.
Any source,artifact,schema,nonfinite,initialization,replay,test or workload fault is INVALID / RETRY SAME C242.
The masked-input audit does not replace scientific model evaluation.

## Source protection, tests and artifacts

Inherit C241292 source pins/442 protected inputs. Add C241 summary+five artifacts and OWN6:
298 source pins/454 inputs. C234 data already protected. No accepted source/test/log is modified.
Direct dependency union18:five C231 LM_SOURCES plus C230 through C242 benchmark/helper entry points.

OWN6:
- fold_lm/v05_benchmarks/model_c242_balanced_recombination.py
- tests_lm/test_v05_c242_balanced_recombination.py
- tools/run_c242.ps1
- tools/invoke_c242.ps1
- this preregistration
- docs/v5b-balanced-recombination-v0.1.md

Own tests24;modules127;loaded2978/focused2977. Only the inherited exact exclusion remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Actual runtime suite construction enforces counts/unique IDs; no new exclusions or mutable-ACTIVE assertions.

Five ignored local artifacts:recombination-plan.json,split-dataset.json,trained-models.pt,
measurements.json,validation-summary.json. Checkpoint schema fold-c242-recombination-v1;six ordered states.
Records store initial_train,final[TRAIN/HOLDOUT][language],predictions[split][view],fingerprints,fit and counters.
Summary uses train_steps,answer_presentations,model_forward_calls,row_presentations; do not assume
older total_* key names. Postcheck verifies all hashes/sizes,plan,partition,summary and initial identities.
Only console log and publisher receipt go to docs/experiment-run-logs/c242/latest.*.
Manifest SHA256:8088155ef7ba95eb47a8a7ae3790247ff20d61804ac08c7fc1b1ed2f0c645760.

## Review and stop

Re-fetch all six committed OWN files after authoring; match code/script Git blobs to tested bytes,
compile/import, run24 own tests, audit free names/parent semantics/fit AST, metric schemas,
mask ambiguity, leakage, counts and embedded Python/CLI argument order. Exercise the actual run,
save/reload and postcheck using synthetic models. Such checks are not the actual FOLD scientific run.
Record exact review HEAD and checks/limitations in handoff before issuing the launch command.

Dispatcher/launcher/runner PowerShell ParseFile precedes execution. Then Python syntax and
parent/data precheck ->24 own tests ->2977 focused tests ->C242 probe ->postcheck ->log publication.
Wrong branch/dirty tree/stale HEAD/ACTIVE mismatch skips before logging. Transport-only failure
does not justify retraining. Full Windows AST/regression/accepted local-artifact checks are not
reported PASS until actually performed. No paid API, external corpus, larger model, cleanup,
history rewrite or production runtime change. Numeric-memory tuning stays paused. Judge C242 before C243.
