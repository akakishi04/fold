# C277 preregistration — saved LR failure-profile audit

Experiment:C277-v5b-saved-lr-failure-profile-audit.
Stage:V5-B-SAVED-LR-FAILURE-PROFILE-AUDIT.
Acceptance base:0544885dc7db8b55b6d12c925ee6454fae88a1ea.
C276 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C278 NOT REGISTERED.

## One scientific question

How does fixed lr0.0025 change the exact fixed-gate failure profile relative to lr0.005 for the
accepted C276 final_boundary states, especially shared_suffix2 and the seed276003 recovery?

This is a saved-output diagnostic only. No capability winner is preregistered.

## Parent evidence

C276 execution:1f1ddd09815cfcd644e90042b83aba085e40e5bb.
C276 summary:runs/c276-v5b-final-boundary-lr-dcd7c7c2f13d49209c05bd4b2ca43110/summary.json.
C276 summary SHA256:6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f.

Require C276 status FAIL,candidate_gate=False,seed pass counts lr0050/lr00250,
two-character pass counts4/5 and5/5,and triple pass counts0/5 and0/5.

Required C276 artifact SHA256:
-architecture-plan.json 312ed892ba64ef1b0289506d44d1e3da05eec6ee85e67b1d3b21cee282e18355
-dataset.json 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-trained-models.pt df59b5b957cc689e622414315ef5d66462c003c992242a4db0f9879999c8385f
-evaluations.pt 04d4b34811d57f6d4ae8e1ab62a2ff4fadc67c07ad11d776e01193104f66a5d4
-measurements.json b9eeb1d2ca73be7201db648cc09c00b2bb87a256f230091172bab117484da096
-validation-summary.json 7d460b7d4a81e2621c933455cbdd71a8b94c2547ab6c7ff502d190a332c83ecf

C276 verifier also requires accepted C275 and C274 summaries:
-C275 SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb;
-C274 SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

## No-new-neural-execution rule

C277 performs:
-zero training;
-zero model forward calls;
-zero core calls;
-zero checkpoint writes;
-zero model-state loads.

Call C276.verify_artifacts with torch.nn.Module._call_impl patched to raise. Reconstruct accepted
C276 measurements exactly before any attribution.

Fixed thresholds remain:
accuracy0.90;query_pair_accuracy0.80;evidence_drop0.35;query_drop0.35;two_order_accuracy0.80.

## Failure-profile audit

For both arms,all seeds,and both tasks:
-record every failed answer-cell criterion and two-order criterion with signed margin;
-aggregate counts by arm/task/criterion;
-aggregate counts by arm/seed/criterion;
-aggregate counts by arm/split/profile/criterion;
-compute candidate-minus-control criterion-count deltas.

Primary views:
-triple all-profile criterion deltas;
-triple shared_suffix2 criterion deltas for TRAIN/HOLDOUT;
-seed276003 criterion deltas;
-near/control-stable seeds276001/276002/276004/276005 criterion deltas.

Do not infer a capability winner from fewer failures.

## Formal status

C277 status PASS iff:
-C276/C275/C274 accepted parent chains verify;
-exactly10 C276 metric records reconstruct in registered identity order;
-all fixed record pass flags equal the reconstructed threshold margins;
-arm/profile/seed failure aggregates and deltas reconstruct;
-persisted audit-plan,failure-profile and validation-summary reconstruct with Module calls blocked;
-no provenance/integrity guard fails.

PASS means DIAGNOSTIC INTEGRITY ONLY.
capability_gate_applicable=False;gate_f_candidate=False;Gate F remains NOT PASSED.

## Artifacts and workload

Artifacts:
-audit-plan.json
-failure-profile.json
-validation-summary.json
plus summary.json.

model_forward_calls=0;row_presentations=0;core_forward_calls=0;train_steps=0;
new_checkpoint_writes=0;model_state_loads=0.

Expected source pins508;protected inputs892;direct deciding dependencies53.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules162;loaded3814/focused3813.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256 is PENDING_FINAL_SEAL during authoring.
Registration cardinalities are manifest-derived at runtime.
After all manifest-changing edits,seal benchmark/prereg/handoff identically before activation.
Multi-parent test fixtures must model C276/C275/C274 hashes independently.

Use Validate->Execute. Inherited handoff compatibility seals remain append-only.
C278 stays unregistered until C277 is judged.
