# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C273 ACCEPTED VALID NEGATIVE. C274 ACTIVE / NOT YET JUDGED. C275 NOT REGISTERED.**
C273 execution1106e0898e1698a06b78ac2266c65a983aded275 is authoritative for science.
boundary_pair passed0/5 whole-state gates and dual_boundary passed1/5.
Both arms passed5/5 on the original two-character task;triple subgate was0/5 versus1/5.
C274 is the unique ACTIVE experiment and is a directional diagnostic,not a Gate F candidate.
No Gate F promotion,production adoption,seed selection or C275 registration.

## Latest accepted science — C273

Acceptance:docs/experiment-ledger-addendum-c273-c274.md.
Execution:1106e0898e1698a06b78ac2266c65a983aded275.
Published log:22b74e6a2aba7f265edf68994563f472328af241.
Summary:runs/c273-v5b-dual-boundary-b70af8ffe4b047ee95a0044e86de7a8c/summary.json.
Summary SHA256:0e764c595c64818c308779cd5190883edec0654375c82970641efa70b980f82e.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:boundary_pair0/5;dual_boundary1/5.
Two-character subgate:boundary5/5;dual5/5.
Triple subgate:boundary0/5;dual1/5.

C273 dual_boundary produced one full passing seed(273001) but degraded shared-suffix pooled behavior
relative to boundary_pair. This does not support another fusion change without first measuring the
directional first-only versus final-only components directly.

C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.

## Inherited regression compatibility seals

This section is append-only while the corresponding accepted/pinned tests remain in focused
regression. Do not remove an entry merely because a later experiment becomes ACTIVE.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is already accepted/pinned and unconditionally checks the current handoff for this
seal. Editing that accepted test would violate parent provenance,so the compatibility seal is
retained here. C273 and later tests use lifecycle-aware own-seal checks instead:current handoff while
ACTIVE,immutable acceptance addendum after acceptance.

## Active C274 — directional first/final boundary diagnostic

Experiment:C274-v5b-directional-boundary-diagnostic.
Stage:V5-B-DIRECTIONAL-BOUNDARY-DIAGNOSTIC.
Registration:docs/experiment-ledger-addendum-c274-preregistration.md.
Design:docs/v5b-directional-boundary-diagnostic-v0.1.md.
Acceptance base:b27759974db6a66f86d71b9d06afe91e0e60b593.
Parent C273 execution:1106e0898e1698a06b78ac2266c65a983aded275.
Parent summary SHA256:0e764c595c64818c308779cd5190883edec0654375c82970641efa70b980f82e.

One question:with identical fresh paired CE training,how do FIRST-only and FINAL-only visible
query-boundary states differ on shared-prefix versus shared-suffix transfer?

This is a diagnostic experiment. There is no preregistered capability winner.
Fresh seeds274001..274005;arms first_boundary and final_boundary.
Both have exactly14256 parameters,matched initial state_dict values and disjoint storage.
first_boundary feeds read.query from the first byte selected by C269.query_span_mask.
final_boundary feeds read.query from the final selected byte.
For one-byte query-blind input the two arms are identical.
Masked pre-core memory,query/key/output maps,score divisor4,PAD mask,Full core,post-core EOS residual,
readout_norm and decoder remain unchanged. No supervision metadata enters model.forward.

Training uses exact C267 two-character data SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Use96 same-facts/different-query TRAIN pairs;randperm seed+274000+epoch;24 pairs/batch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+275000 per arm. Both use CE only;AdamW lr.005,betas.9/.999,eps1e-8,
weight_decay0,global clip1;CPU float64,threads2,deterministic.

Evaluate every final state on BOTH:
1.original C267 two-character task;
2.C270 unseen three-character prompt set SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged descriptive per-cell thresholds:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.
These pass memberships are reported descriptively only.

Predeclared directional reports:
-shared_prefix2 correct/collapse:first_boundary versus final_boundary on TRAIN and HOLDOUT;
-shared_suffix2 correct/collapse:first_boundary versus final_boundary on TRAIN and HOLDOUT.
Also persist all other paired task/profile/language contrasts and original two-character retention.

Formal C274 PASS means diagnostic execution/integrity only:
-all10 states trained/evaluated;
-strict replay succeeds;
-all persisted metrics reconstruct;
-no provenance/integrity guard fails.
It does NOT declare a capability winner and cannot promote Gate F.

Workload:10 models;8000 updates;384000 training rows;9080 model forwards;487680 row presentations;
36320 core calls;one10-state bundle write/load;10 strict state loads.
Artifacts:architecture-plan.json,dataset.json,triple-dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json plus summary.json.

Protection/runtime:
-source pins490;
-protected inputs854;
-direct deciding dependencies50;
-own24;
-modules159;
-loaded3742/focused3741;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
a288c48c3b9282be070f12fdc567d8c8e09bbed8003a6321792ce517a5c255e7.
The same seal appears in benchmark and preregistration. C274 own test24 requires current handoff
agreement while ACTIVE,then immutable c274-c275 acceptance addendum after acceptance.
Registration cardinalities are manifest-derived at runtime.

## C274 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 1f5b65f12be14f0b1dcd44e41d1e9ab8d6c19359

Compared C273 acceptance b27759974db6a66f86d71b9d06afe91e0e60b593 to review target:
only C274 OWN6 paths differ.

Committed OWN6 blobs:
-source:4313384adaf31947d2422c1866cc616f9edb5ac1
-test:916ba60cf8480654fc49b7702540f385384e2c91
-runner:debc103e653519806956f69e0492c4c30467db1c
-launcher:9364cbb06dbda63e4c6a54e571bf8a64a81ed1ba
-prereg:f28188f1703335d8d4e58894886b9558787021e7
-design:2edcc528afade8d7b708aa3c631bb0bc0cc1d7c4

Static review confirms exactly24 own tests;three runner Python blocks with argv sets{1},{},{1,2,3};
Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED before scientific logging;unique ordered
scientific phase markers on distinct lines;manifest-derived490/854 registration;parent C273 negative
contract;diagnostic-only formal status;no candidate_gate/winner output;and lifecycle-aware own seal
plus legacy C272 compatibility seal.

No complete local checkout/PowerShell runtime is available to the reviewer. Therefore own24,
focused3741,PowerShell ParseFile,parent artifact replay and real ten-model training are NOT claimed
executed here. Mode Validate is the authoritative executable authoring gate.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C274 ->
Mode Validate(parent/source/artifact precheck490/854 + sealed manifest,own24,focused3741) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,both-task evaluation,strict replay,persisted diagnostic) ->
log publication.

Validate failure is operational and must not publish/replace the scientific latest log.
Execute integrity failure retries SAME C274.
If run_execution_valid=True and scientific_status=PASS,accept it as DIAGNOSTIC PASS ONLY.
Do not infer a capability winner or Gate F promotion from pooled differences.
C275 stays unregistered until C274 is judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
