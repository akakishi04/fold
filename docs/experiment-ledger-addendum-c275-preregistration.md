# C275 preregistration — saved gate-failure audit

Experiment:C275-v5b-saved-gate-failure-audit.
Stage:V5-B-SAVED-GATE-FAILURE-AUDIT.
Acceptance base:ecd58ccf5f59887955048a6f23f77e340981e239.
C274 ACCEPTED PASS for diagnostic integrity only. Gate F NOT PASSED. C276 NOT REGISTERED.

## One scientific question

For the accepted C274 saved states,which exact fixed gate components cause final_boundary to fail
the three-character task despite near-perfect pooled answers in four seeds,and are those failures
concentrated in seed274003 or distributed across the near-passing seeds?

## Parent evidence

C274 execution:90f76a8f017d562caded127821852654b8e3d061.
C274 summary:runs/c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178/summary.json.
C274 summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

Require C274 status PASS,diagnostic_complete=True,capability_gate_applicable=False,
task pass counts first_boundary two_char0/triple0 and final_boundary two_char4/triple0.

Required C274 artifact SHA256:
-architecture-plan.json a288c48c3b9282be070f12fdc567d8c8e09bbed8003a6321792ce517a5c255e7
-dataset.json 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-trained-models.pt 3a8cf72756e1112341bf8ad88e45ad124f876a608586d3dc4955cd11a16c1231
-evaluations.pt ca1124810acd5f7d86ec614a900fbe5dbd3f37278005266616e666ce8e4ebf25
-measurements.json dcbddf4c4f614e8c8b224ecba4b656a5109e5dab0de1d4a2bde8ddae0858ecca
-validation-summary.json 79d1ef4ee89f067977dd1704f4c0424453018dc5c989e3afe2d7f935cb5ef2f9

## Inputs and no-new-science-execution rule

C275 performs:
-zero training;
-zero model forward calls;
-zero core calls;
-zero checkpoint writes;
-zero learned-state selection.

Call C274.verify_artifacts with torch.nn.Module._call_impl patched to raise,so parent verification
cannot silently perform inference. Then read the accepted measurements.json and reconstruct the
same C274 metrics before auditing failures.

No thresholds are changed:
-answer accuracy0.90;
-query-pair0.80;
-evidence-drop0.35;
-query-drop0.35;
-two-order0.80.

## Failure audit

For every answer cell in both two_char and triple metrics:
-record seed,arm,task,split,profile,language,entities,permutation;
-record rows/correct,pairs/collapsed_pairs;
-record the four metric values and signed threshold margins;
-record the exact set of failed criteria.

For every two_order record:
-record seed,arm,task,split,profile,language,entities;
-record accuracy and signed margin to0.80;
-record failure iff margin<0.

Aggregate:
-counts by arm/task/criterion;
-counts by seed/criterion;
-counts by split/profile/criterion;
-minimum and maximum negative margin per criterion;
-primary final_boundary triple failure table;
-near-pass cohort274001/274002/274004/274005 versus broad seed274003.

Do not infer a winner from counts. C275 only attributes registered gate failures.

## Formal status

C275 status PASS iff:
-parent C274 bytes and saved reconstruction verify;
-exactly10 parent metric records are present in accepted order;
-all cell/two-order failure records are internally consistent with each parent's passed field;
-the primary final_boundary triple audit covers all five seeds;
-persisted audit-plan,failure-audit and validation-summary reconstruct exactly with Module calls blocked;
-no source/input/provenance guard fails.

PASS means DIAGNOSTIC INTEGRITY ONLY. capability_gate_applicable=False;gate_f_candidate=False.
Gate F remains NOT PASSED regardless of observed attribution.

## Artifacts and workload

Artifacts:
-audit-plan.json
-failure-audit.json
-validation-summary.json
plus summary.json.

No learned artifact is written.
model_forward_calls=0;row_presentations=0;core_forward_calls=0;train_steps=0;
new_checkpoint_writes=0;model_state_loads=0.

Expected source pins496;protected inputs868;direct deciding dependencies51.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules160;loaded3766/focused3765.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256:18af6d20c41fbb2e0bff672ac4e82e9e06eb324bc9c56ef53f409621ac95e102.
Registration cardinalities are manifest-derived at runtime.
After all manifest-changing edits,seal benchmark/prereg/handoff identically before activation.

Use Validate->Execute. Inherited handoff compatibility seals remain append-only.
C276 stays unregistered until C275 is judged.
