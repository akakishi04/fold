# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C274 ACCEPTED PASS (diagnostic integrity only). C275 ACTIVE / NOT YET JUDGED. C276 NOT REGISTERED.**
C274 execution90f76a8f017d562caded127821852654b8e3d061 is authoritative.
C274 scientific_status=PASS means directional diagnostic integrity only;capability_gate_applicable=False.
first_boundary measured two_char0/5,triple0/5;final_boundary measured two_char4/5,triple0/5.
C275 is the unique ACTIVE experiment and is a saved-output gate-failure audit with zero neural calls.
No Gate F promotion,capability winner,production adoption or C276 registration.

## Latest accepted science — C274

Acceptance:docs/experiment-ledger-addendum-c274-c275.md.
Execution:90f76a8f017d562caded127821852654b8e3d061.
Published log:acb1236f5299052662525deec2b00f0bb415338b.
Summary:runs/c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178/summary.json.
Summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False.
Task pass counts:first_boundary two_char0/5,triple0/5;final_boundary two_char4/5,triple0/5.

Directional aggregate HOLDOUT triple:
-first_boundary tripled392/480,shared_prefix2314/480,shared_suffix2360/480;
-final_boundary tripled432/480,shared_prefix2426/480,shared_suffix2409/480.
final_boundary is broadly stronger,but no final state obtains complete triple PASS.
Near-passing final seeds274001/274002/274004/274005 have pooled triple HOLDOUT280/284/281/288
of288;seed274003 is a broad miss at134/288. The remaining fixed gate failures require attribution.

C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Active C275 — saved gate-failure audit

Experiment:C275-v5b-saved-gate-failure-audit.
Stage:V5-B-SAVED-GATE-FAILURE-AUDIT.
Registration:docs/experiment-ledger-addendum-c275-preregistration.md.
Design:docs/v5b-saved-gate-failure-audit-v0.1.md.
Acceptance base:ecd58ccf5f59887955048a6f23f77e340981e239.
Parent C274 execution:90f76a8f017d562caded127821852654b8e3d061.
Parent summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

One question:which exact fixed gate components cause final_boundary to fail the three-character task
despite near-perfect pooled answers in four seeds,and are those failures concentrated in broad
seed274003 or also distributed across274001/274002/274004/274005?

C275 performs zero training,zero model forwards,zero core calls,zero checkpoint writes and zero
learned-state selection. It verifies C274 accepted artifacts with torch.nn.Module._call_impl blocked,
reconstructs the accepted measurements exactly,and audits only persisted metrics.

Fixed thresholds are unchanged:
-accuracy0.90;
-query-pair accuracy0.80;
-evidence-drop0.35;
-query-drop0.35;
-two-order accuracy0.80.

For every answer cell,record signed threshold margins and failed criteria.
For every two-order record,record signed margin to0.80.
Aggregate failures by arm/task/criterion,seed/criterion,and split/profile/criterion.
Primary focus is final_boundary + triple task with explicit near-seed versus broad-seed split.

Formal C275 PASS means diagnostic execution/integrity only:
-parent C274 bytes and saved reconstruction verify;
-all registered cell/two-order failure records are internally consistent;
-primary final-boundary triple audit covers all five seeds;
-persisted audit-plan/failure-audit/validation-summary reconstruct exactly;
-no provenance guard fails.
PASS cannot declare a capability winner or promote Gate F.

Workload:
-model_forward_calls0;
-row_presentations0;
-core_forward_calls0;
-train_steps0;
-new_checkpoint_writes0;
-model_state_loads0.

Artifacts:audit-plan.json,failure-audit.json,validation-summary.json plus summary.json.

Protection/runtime:
-source pins496;
-protected inputs868;
-direct deciding dependencies51;
-own24;
-modules160;
-loaded3766/focused3765;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
18af6d20c41fbb2e0bff672ac4e82e9e06eb324bc9c56ef53f409621ac95e102.
The same seal appears in benchmark and preregistration. C275 own test24 requires current handoff
agreement while ACTIVE,then immutable c275-c276 acceptance addendum after acceptance.
Registration cardinalities are manifest-derived at runtime.

## C275 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 13fe00d659a429c629490a44130501d5d3f8adad

Compared C274 acceptance ecd58ccf5f59887955048a6f23f77e340981e239 to review target:
only C275 OWN6 paths differ.

Committed OWN6 blobs:
-source:f398811f6a4f5df67eeeb7e3e4774ca3846fc2e3
-test:95cff37115cf1c26880e2ddd2feaf18a0202af14
-runner:182a64e0ea06884c9ff807e17b53ce238f01da2b
-launcher:66f41bf7c8695ab5122975a77a8d03df5b7ff851
-prereg:0a67e6259c7a370f336c4485ea68f02e3f3df92f
-design:be6be1223133c5f07907685de50f067de00e3ba8

Static review confirms exactly24 own tests;three runner Python blocks;explicit unittest.mock.patch
import;Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED before scientific logging;unique
ordered run phase markers;manifest-derived496/868 registration;zero neural workload;parent C274
diagnostic contract;diagnostic-only formal status;and lifecycle-aware own seal plus legacy C272 seal.

No complete local checkout/PowerShell runtime is available to the reviewer. Therefore own24,
focused3765,PowerShell ParseFile,parent artifact replay and real saved-audit execution are NOT claimed
executed here. Mode Validate is authoritative.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C275 ->
Mode Validate(parent/source/artifact precheck496/868 + sealed manifest,own24,focused3765) ->
authoring_runtime_preflight=PASS ->
Mode Execute(saved metrics attribution only,zero neural calls,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C275.
If run_execution_valid=True and scientific_status=PASS,accept it as DIAGNOSTIC PASS ONLY.
Use the attribution result to decide C276;do not infer a capability winner from C275 itself.
C276 stays unregistered until C275 is judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
