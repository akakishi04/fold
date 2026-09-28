# C276 preregistration — final-boundary optimizer reliability

Experiment:C276-v5b-final-boundary-lr-reliability.
Stage:V5-B-FINAL-BOUNDARY-LR-RELIABILITY.
Acceptance base:2dac538eb6bc2755a589d9d9ec26135773ade4d7.
C275 ACCEPTED PASS for diagnostic integrity only. Gate F NOT PASSED. C277 NOT REGISTERED.

## One scientific question

Does a more conservative fixed AdamW learning rate0.0025 improve fresh-seed reliability of the
final_boundary architecture relative to the accepted0.005 policy,without changing architecture,
loss,data,steps or evaluation gates?

## Parent evidence

C275 execution:3cd34c37a4329f8b8a030f320f1eeefa303706e4.
C275 summary:runs/c275-v5b-gate-failure-audit-fb5be8dc32064545aa7a993b70e50706/summary.json.
C275 summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb.

Require C275 status PASS,diagnostic_complete=True,capability_gate_applicable=False,
model_forward_calls=0,and primary final-boundary triple audit coverage for all five C274 seeds.

Required C275 artifact SHA256:
-audit-plan.json 18af6d20c41fbb2e0bff672ac4e82e9e06eb324bc9c56ef53f409621ac95e102
-failure-audit.json b28b93768e979295e9b2294d150c6c6c29ec9943ef9f42b5496de023cfa83c0f
-validation-summary.json d6d4992f9ba626609d580664e4ec064b4f14003430cd74dc988a6c51cb627cab

C275 artifacts are provenance only. C276 uses fresh initialization.

## Arms

Fresh seeds276001..276005.

lr005:
C274 SingleBoundaryReadout selecting the FINAL visible query byte;AdamW lr0.005.

lr0025:
the same final-boundary reader,parameter count,state_dict keys,initial tensor values and all optimizer
settings except AdamW lr0.0025.

Both arms:
-14256 parameters;
-C269.query_span_mask;
-final selected visible query byte only;
-masked pre-core memory;
-shared read.query/key/output;
-score divisor4;
-PAD mask;
-Full core;
-post-core EOS residual;
-readout_norm and decoder unchanged.

No target/entity/profile/split/pair metadata enters model.forward.

## Training

Exact C267 two-character dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Use96 same-facts/different-query TRAIN pairs.
For seed/epoch:randperm96 seed+276000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+277000 reset per arm.

Both arms use mean CE only,AdamW betas0.9/0.999,eps1e-8,weight_decay0,global clip1.
Only learning rate differs:0.005 versus0.0025.
CPU float64,threads2,deterministic algorithms.
No early stopping,extra updates,seed replacement,checkpoint selection or HOLDOUT optimization.

## Evaluation and fixed capability gate

Evaluate both final states on:
1.original C267 two-character task;
2.C270 triple dataset SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged thresholds:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.
HOLDOUT answer cells8 rows require8/8.

Primary PASS iff all FIVE lr0025 states pass every original and triple criterion.
lr005 is the matched control and cannot rescue/fail candidate.
Report paired correct/collapse contrasts and seed-level task pass counts.

## Workload and persistence

10 models;8000 updates;384000 training row presentations.
Per model:800 training forwards +54 final evaluation +54 strict replay =908.
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
-fold-c276-final-boundary-lr-models-v1
-fold-c276-final-boundary-lr-eval-v1.

## Protection/runtime

Expected source pins502;protected inputs878;direct deciding dependencies52.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules161;loaded3790/focused3789.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256 is PENDING_FINAL_SEAL during authoring.
Registration cardinalities are manifest-derived at runtime.
After all manifest-changing edits,seal benchmark/prereg/handoff identically before activation.

Use Validate->Execute. Inherited handoff compatibility seals remain append-only.

## Stop

A valid candidate miss is ACCEPTED VALID NEGATIVE. Do not try another learning rate inside C276,
extend training,replace seeds or relax gates after results. Integrity failure retries SAME C276.
C277 remains unregistered until C276 is judged.
