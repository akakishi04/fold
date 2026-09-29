# C278 preregistration — mean-span plus final-boundary dual attention

Experiment:C278-v5b-mean-final-dual-query.
Stage:V5-B-MEAN-FINAL-DUAL-QUERY.
Acceptance base:8a9340c5165754080ea729cf013b6015035df824.
C277 ACCEPTED PASS for diagnostic integrity only. Gate F NOT PASSED. C279 NOT REGISTERED.

## One scientific question

With identical fresh paired CE training,does keeping the mean visible query-span signal and final
visible query-boundary signal separate through their attention softmaxes,then averaging their
retrieved memories,improve reliable two/three-character binding relative to mean-span attention
alone?

## Parent evidence

C277 execution:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
C277 summary:runs/c277-v5b-saved-lr-audit-7e9cad9663144ae9bdbacda802c21306/summary.json.
C277 summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.

Require C277 status PASS,diagnostic_complete=True,capability_gate_applicable=False,
model_forward_calls=0,triple criterion delta
accuracy-37/query_pair-37/evidence_drop+3/query_drop+1/two_order-18,and shared_suffix2 HOLDOUT delta
accuracy-7/query_pair-7/evidence_drop+4/query_drop+5/two_order-5.

Required C277 artifact SHA256:
-audit-plan.json 50796e76783611eb04649fd47c450f3fe47d05a34fc0c787168fa38e612d8de9
-failure-profile.json f1a0f3e087f3ecc3afafaa56d600168018572e7450c0f79204ed5a6d6d972acc
-validation-summary.json b8ac20e2a2ac7ea2c6306f71d6f121580cb2d0c635b92605263e2e759c76a9db

C277 verifier also requires:
-C276 summary SHA256 6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f
-C275 summary SHA256 1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb
-C274 summary SHA256 0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0

C277 and older artifacts are provenance only. C278 uses fresh initialization.

## Arms

Fresh seeds278001..278005.

mean_span:
actual C269 SpanQueryReadout:
- pre-core local states over C269.query_span_mask;
- arithmetic mean of visible query-span states;
- shared read.query/key/output;
- one masked attention softmax.

mean_final_dual:
- same14256 parameters and state_dict keys as mean_span;
- mean visible query-span pre-core state -> shared read.query -> attention softmax A;
- final visible query-byte pre-core state -> same read.query -> attention softmax B;
- same read.key(local memory) for both;
- retrieve memory_mean and memory_final separately;
- final memory=(memory_mean+memory_final)/2;
- shared read.output exactly once;
- unchanged post-core residual/readout_norm/decoder.

For a one-byte query span,mean state equals final state and the two candidate attentions are
identical. No target/entity/profile/split/pair metadata enters model.forward.

## Training

Exact C267 two-character dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Use96 same-facts/different-query TRAIN pairs.
For seed/epoch:randperm96 seed+278000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+279000 reset per arm.

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

Primary PASS iff all FIVE mean_final_dual states pass every original and triple criterion.
mean_span is the matched control and cannot rescue/fail candidate.
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
-fold-c278-mean-final-models-v1
-fold-c278-mean-final-eval-v1.

## Protection/runtime

Expected source pins514;protected inputs902;direct deciding dependencies54.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules163;loaded3838/focused3837.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256 is PENDING_FINAL_SEAL during authoring.
Registration cardinalities are manifest-derived at runtime.
After all manifest-changing edits,seal benchmark/prereg/handoff identically before activation.
Multi-parent fixtures must model C277/C276/C275/C274 hashes independently.

Use Validate->Execute. Inherited handoff compatibility seals remain append-only.

## Stop

A valid candidate miss is ACCEPTED VALID NEGATIVE. Do not try another fusion rule inside C278,
change lr,extend training,replace seeds or relax gates after results. Integrity failure retries SAME
C278. C279 remains unregistered until C278 is judged.
