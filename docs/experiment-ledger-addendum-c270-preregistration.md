# C270 preregistration — frozen triple-identifier transfer

Experiment:C270-v5b-frozen-triple-identifiers.
Stage:V5-B-FROZEN-TRIPLE-IDENTIFIERS.
C269 ACCEPTED PASS in its bounded query-span scope. Gate E PASSED;Gate F NOT PASSED.
C271 NOT REGISTERED.

## One scientific question

Do the same frozen C269 states transfer from TRAIN-seen two-character identifiers to unseen
three-character identifiers built entirely from familiar identifier characters?

## Fixed parent and states

Parent execution:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Parent summary:
runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json
SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.
Require status PASS,candidate_gate=True,seed counts eos_query4/span_query5 and ten records.

Required C269 artifact SHA256:
-query-plan.json:cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa;
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
-trained-models.pt:65f3b34e163b7753ecfda2eadedeb7cd8f282a0437b6b94ec2034d2efeadea9c;
-evaluations.pt:a9212d3da65849ebc08f4f7ed1e669f73b34f897d1f4ab05b077582c1d220c29;
-measurements.json:3d64033da08d8a83b8bebe53e6acd4b85340acffb9d849ebcb7b921f480a7811;
-validation-summary.json:44de8eb095ceca1f3827ec4e2ba521a750fd80e49b38235db027754dbb540e6a.

Strict-load the accepted C269 fold-c269-query-span-models-v1 bundle once. Retain seeds269001..269005
and both arms eos_query/span_query in accepted order. Recreate each exact architecture through
C269.make_arm_model,strict-load its final state,verify final_sha256,then set eval/requires_grad=False.
No new initialization,training,optimizer state or learned checkpoint is created.

## New frozen inputs

Use the exact accepted C267 logical dataset and its TRAIN192/HOLDOUT96 split. For each source
entity-character pair u,v predefine:
-tripled: uuu/vvv;
-shared_prefix2: uuu/uuv;
-shared_suffix2: uuu/vuu.

Apply each mapping consistently to fact names and query name. Preserve all three entity subsets,
EN/JA forms,both visible fact orders,both queries and target values. Values remain distinct0..3.
All new identifier strings have exactly three logical characters. Japanese names contribute all
their UTF-8 bytes. No new byte value is introduced. Normal prompts fit <=34 bytes.

New prompt artifact has192 TRAIN-value and96 HOLDOUT-value rows per profile,864 unique normal prompts
per model. It stores source_id,target and normal/evidence_blind/query_blind strings. Dataset SHA256:
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

No three-character identifier occurs in C269 training. The old value split is retained for reporting:
TRAIN-value rows isolate the name/length shift more directly;HOLDOUT-value rows combine that shift
with held values. Neither split is optimized in C270.

## Replay and evaluation sequence

For each frozen state:
1. Actual C267 evaluator on the accepted C269 two-character data:27 forwards/2592 rows.
2. Compare every raw logit with saved C269 final outputs, tolerance1e-9 and exact argmax.
3. Evaluate new three-character prompts:27 forwards/2592 rows.
4. Re-evaluate old two-character data:27 forwards/2592 rows.
5. Replay against both same-run anchor and accepted outputs and verify unchanged fingerprint.

Per model81 forwards/7776 rows/324 actual Full core calls. Totals:810 forwards,77760 row
presentations,3240 core calls. One accepted checkpoint-bundle load;ten strict state loads.
new_training_steps=0;new_checkpoint_writes=0. Raw saved anchor/new/restored tensors total
159252480 bytes before serialization metadata.

## Fixed gate

Use unchanged C267 threshold semantics with the three new profile names. Per answer cell:
accuracy>=.90,query_pair_accuracy>=.80,evidence_drop>=.35,query_drop>=.35.
Per language/subset require two-order consistency>=.80. TRAIN cells have16 answers/8 pairs;
HOLDOUT cells8 answers/4 pairs,so the90% HOLDOUT threshold means8/8. Two-order minima remain
13/16 TRAIN and7/8 HOLDOUT.

Primary PASS iff all five frozen span_query states satisfy every criterion on both splits and all
three new profiles. eos_query is reported independently. Report60 paired control/candidate
split/profile/language contrasts in answer correctness and same-answer collapse. Pooled metrics
cannot replace the five-seed gate.

## Persistence and protection

Artifacts:
-transfer-plan.json
-triple-dataset.json
-eval-outputs.pt
-measurements.json
-validation-summary.json
plus summary.json. Evaluation schema:fold-c270-triple-eval-v1. No learned state is written.

Inherit C269460 source pins/787 protected inputs. Add C269 summary+six artifacts and C270 OWN6:
466 source pins/800 protected inputs. Direct deciding dependency union46. OWN6:
-fold_lm/v05_benchmarks/model_c270_frozen_triple_identifiers.py
-tests_lm/test_v05_c270_frozen_triple_identifiers.py
-tools/run_c270.ps1
-tools/invoke_c270.ps1
-docs/experiment-ledger-addendum-c270-preregistration.md
-docs/v5b-frozen-triple-identifiers-v0.1.md

Own24;modules155;loaded3646/focused3645. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016.

## Interpretation and stop

This is a frozen distribution-shift probe,not a new broad benchmark. Name length and composition
change together. A PASS does not imply arbitrary strings,ordinary language or an internal causal
parser. A valid miss is ACCEPTED VALID NEGATIVE. Do not retrain,select states,change profile strings,
value split or thresholds after seeing results. Integrity failure retries SAME C270 only.
No paid API,external corpus,model expansion,production adoption,cleanup,history rewrite or CI change.
