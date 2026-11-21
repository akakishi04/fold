# C280 preregistration — evidence-only dual memory support

Experiment:C280-v5b-evidence-only-dual-memory.
Stage:V5-B-EVIDENCE-ONLY-DUAL-MEMORY.
Acceptance base:9299883b69eadb049675b775fc4a152e7ab1f225.
C279 ACCEPTED PASS for diagnostic integrity only. Gate F NOT PASSED. C281 NOT REGISTERED.

## One scientific question

With identical fresh paired CE training,does keeping C278's mean/final query vectors but restricting
both attention softmaxes to evidence positions before the visible query bytes improve reliable
two/three-character binding relative to C278's all-valid-token memory support?

## Parent evidence

C279 execution:b07425eddfab2d4f3f6bacd8dff02295b44f3063.
C279 summary:runs/c279-v5b-saved-dual-audit-e6d76ea781994de085b16ea8e7a6b972/summary.json.
C279 summary SHA256:a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb.

Require C279 PASS,diagnostic_complete=True,capability_gate_applicable=False,model_forward_calls=0.
Require triple criterion delta accuracy-78/query_pair-78/evidence_drop-10/query_drop-49/two_order-39.
Require shared_suffix2 TRAIN delta accuracy-12/query_pair-12/evidence_drop+4/query_drop-3/two_order-4.
Require shared_suffix2 HOLDOUT delta accuracy-9/query_pair-9/evidence_drop+5/query_drop-7/two_order-8.
Require candidate shared_prefix2 HOLDOUT evidence_drop failures0 and shared_suffix2 HOLDOUT evidence_drop failures7.

Required C279 artifact SHA256:
-audit-plan.json daeea4cfcf5083ec9a5237ea092f0c11ac7ab3cf38b76e9cdf62f60c4fea1af7
-failure-profile.json b35020a8e440925599ea2c1ddf8b1b07a1f2c18a9ca53a11195f9a0f7085e7c4
-validation-summary.json 0514f2a64c1726e8765f86420bd8b2741c800df000da93f3a69ccaa1364de732

Ancestor summary SHA256:
-C278 557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b
-C277 ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13
-C276 6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f
-C275 1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb
-C274 0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0

C279 and older artifacts are provenance only. C280 uses fresh initialization.

## Arms

Fresh seeds280001..280005.

all_token_dual:
-actual C278 MeanFinalDualReadout;
-mean visible query-span pre-core state and final visible query-byte pre-core state;
-shared read.query/key/output;
-separate masked softmaxes over every valid token;
-average retrieved memories before one read.output.

evidence_only_dual:
-same14256 parameters and state_dict keys as all_token_dual;
-identical mean/final query vectors;
-identical read.query/read.key/read.output;
-only the softmax support changes;
-valid key/value positions are strictly before the first visible query byte;
-the final evidence/query separator semicolon is included;
-visible query bytes,final equals,EOS and padding are excluded;
-separate softmaxes and post-retrieval mean remain unchanged.

No target/entity/profile/split/pair metadata enters model.forward.

## Training

Exact C267 two-character dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Use96 same-facts/different-query TRAIN pairs.
For seed/epoch:randperm96 seed+280000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+281000 reset per arm.

Both arms use mean CE only,AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,global clip1.
CPU float64,threads2,deterministic algorithms.
No early stopping,extra updates,seed replacement,checkpoint selection or HOLDOUT optimization.

## Evaluation and fixed capability gate

Evaluate both final states on:
1.original C267 two-character task;
2.C270 triple dataset SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged thresholds:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.

Primary PASS iff all FIVE evidence_only_dual states pass every original and triple criterion.
all_token_dual is the matched control and cannot rescue/fail candidate.
Report complete paired correct/collapse contrasts and seed-level two/triple/whole pass counts.

## Workload and persistence

10 models;8000 updates;384000 training row presentations.
Per model:800 training forwards+54 final evaluation+54 strict replay=908.
Totals9080 model forwards,487680 row presentations,36320 core calls.
One10-state bundle write/load;10 strict state loads;new_checkpoint_writes=1.

Artifacts:
-architecture-plan.json
-dataset.json
-triple-dataset.json
-trained-models.pt
-evaluations.pt
-measurements.json
-validation-summary.json
plus summary.json.

Schemas:
-fold-c280-evidence-dual-models-v1
-fold-c280-evidence-dual-eval-v1.

## Protection/runtime

Expected source pins526;protected inputs926;direct deciding dependencies56.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules165;loaded3886/focused3885.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256:c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac.
Registration cardinalities are manifest-derived at runtime.
C279/C278/C277/C276/C275/C274 summary hashes are modeled independently.

Use Validate->Execute. A valid candidate miss is ACCEPTED VALID NEGATIVE.
Do not alter the evidence-support boundary inside C280 after results.
Integrity failure retries SAME C280. C281 remains unregistered until C280 is judged.
