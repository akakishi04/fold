# C274 preregistration — directional first/final boundary diagnostic

Experiment:C274-v5b-directional-boundary-diagnostic.
Stage:V5-B-DIRECTIONAL-BOUNDARY-DIAGNOSTIC.
Acceptance base:b27759974db6a66f86d71b9d06afe91e0e60b593.
C273 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C275 NOT REGISTERED.

## One scientific question

With identical fresh paired CE training,how do FIRST-only and FINAL-only visible query-boundary
pre-core states differ on shared-prefix versus shared-suffix transfer?

This is a diagnostic experiment. No candidate architecture or capability winner is preregistered.

## Parent evidence

C273 execution:1106e0898e1698a06b78ac2266c65a983aded275.
C273 summary:runs/c273-v5b-dual-boundary-b70af8ffe4b047ee95a0044e86de7a8c/summary.json.
C273 summary SHA256:0e764c595c64818c308779cd5190883edec0654375c82970641efa70b980f82e.

Require C273 status FAIL,candidate_gate=False,whole-state pass counts
boundary_pair0/dual_boundary1,two-character pass counts5/5 and triple pass counts0/1.

Required C273 artifact SHA256:
-architecture-plan.json fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f
-dataset.json 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-trained-models.pt 4e615c72c7636edf7ce8d3d28baff40f7c02f286c954e61ca9b1d08962857c6e
-evaluations.pt 8cc808e477f5297e4d4f85c35cf0bb33714cb2f7a32c08c35476bc0a7ec1a1fd
-measurements.json 8eb887d84ae4c75f4b7100e4bbd8ed594ffb83fa75d2908810814209fc601cbe
-validation-summary.json ecbb73d07a663c983b7add84ed9e168116e9118a9debeea16537f5f1ed0158cd

C273 artifacts are provenance only. C274 uses fresh initialization.

## Arms

Fresh seeds274001..274005.

first_boundary:
read.query receives the pre-core local state at the first byte selected by
C269.query_span_mask(tokens).

final_boundary:
read.query receives the pre-core local state at the final byte selected by the same mask.

Both arms retain masked pre-core memory,shared read.query/key/output parameterization,score divisor4,
PAD mask,Full core,post-core EOS residual,readout_norm and decoder. Each model has14256 parameters.
For one-byte query-blind input both arms receive the same state.
No target/entity/profile/split/pair metadata enters model.forward.

## Training

Exact C267 two-character dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Use96 same-facts/different-query TRAIN pairs.
For seed/epoch:randperm96 seed+274000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.
800 updates=200 epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+275000 reset per arm.

Both arms use mean CE only,AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,global clip1.
CPU float64,threads2,deterministic. No early stop,extra training,seed replacement,checkpoint selection
or HOLDOUT optimization.

## Evaluation and diagnostic outputs

Evaluate both final states on:
1.original C267 two-character task;
2.C270 triple dataset SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged descriptive gates:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.

Record complete per-seed task pass membership,but it does not define C274 formal PASS.
Predeclared main directional reports:
-shared_prefix2 correct/collapse: first_boundary versus final_boundary on TRAIN and HOLDOUT;
-shared_suffix2 correct/collapse: first_boundary versus final_boundary on TRAIN and HOLDOUT.
Also persist all paired task/profile/language contrasts and original two-character retention.

Formal C274 PASS iff the registered execution is valid,all10 states are evaluated/replayed,
all planned metrics are reconstructed from persisted outputs,and no integrity/provenance guard fails.
Formal PASS is diagnostic integrity only and must not be described as a capability PASS.
Gate F remains NOT PASSED regardless of directional result.

## Workload and persistence

10 models;8000 updates;384000 training row presentations.
Per model:800 train forwards +54 final evaluation +54 strict replay =908.
Totals9080 forwards,487680 row presentations,36320 core calls.
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
-fold-c274-directional-boundary-models-v1
-fold-c274-directional-boundary-eval-v1.

## Protection/runtime

Expected source pins490;protected inputs854;direct deciding dependencies50.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules159;loaded3742/focused3741.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256 is PENDING_FINAL_SEAL during authoring.
Registration cardinalities are manifest-derived at runtime.
After all manifest-changing edits,seal benchmark/prereg/handoff identically before activation.

Use Validate->Execute. Validate must pass parent/source/artifact precheck,own24 and focused3741 before
scientific logging begins. Inherited handoff compatibility seals remain append-only.

## Stop

Any valid directional outcome is accepted. Do not choose a fusion architecture inside C274,
retune seeds,or reinterpret pooled superiority as a capability winner.
Integrity failure retries SAME C274. C275 remains unregistered until C274 is judged.
