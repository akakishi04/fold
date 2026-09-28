# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C270 ACCEPTED VALID NEGATIVE. C271 ACTIVE / NOT YET JUDGED (PREFLIGHT RECOVERY). C272 NOT REGISTERED.**
C270 valid execution456deac490990f4c7f4ceb1cdf241f0c606a77de passed the new pre-science
Validate gate and then completed scientific execution. Both frozen C270 arms passed0/5 on the
unseen three-character task. C269 remains ACCEPTED PASS in its bounded trained-name/held-value scope.
C271 is the unique ACTIVE experiment:paired mean-span versus endpoint-span query representation.

## Latest accepted science — C270

Acceptance:docs/experiment-ledger-addendum-c270-c271.md.
Execution:456deac490990f4c7f4ceb1cdf241f0c606a77de.
Published log:e3670602568ad402d49108e6529dd4b728c2e6e8.
Summary:runs/c270-v5b-triple-identifiers-87c6c92aaa194dada7aae2b420dba776/summary.json.
Summary SHA256:117c55f5498dec1b5e60c2a59fc571eeb485a3f6614f710348e29348e3433d5b.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:eos_query0/5;span_query0/5.

Aggregate C270 candidate span_query:
-TRAIN tripled960/960,collapse0/480;
-TRAIN shared_prefix2 793/960,collapse167/480;
-TRAIN shared_suffix2 906/960,collapse43/480;
-HOLDOUT tripled480/480,collapse0/240;
-HOLDOUT shared_prefix2 381/480,collapse76/240;
-HOLDOUT shared_suffix2 446/480,collapse17/240.
Thus length3 alone is not the failure:tripled is perfect,while shared-character composition fails.
This is consistent with mean-pooling dilution but does not prove that mechanism.

The earlier C270 attempt at11ae165db9dbb73239360a20c9c7cf005cd9c19f remains INVALID history.
Recovery/runtime details remain in docs/experiment-ledger-addendum-c270-execution-recovery.md and
docs/experiment-authoring-runtime-gate.md.

## Latest accepted science — C269

Execution:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Published log:1c34b373ad9610dddcab2e7e54294fd5d4fe7cef.
Summary:runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json.
Summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.
Acceptance:docs/experiment-ledger-addendum-c269-c270.md.
span_query5/5 versus eos_query4/5 on trained two-character name profiles with held values.

## Active C271 — paired query endpoint

Experiment:C271-v5b-paired-query-endpoint.
Stage:V5-B-PAIRED-QUERY-ENDPOINT.
Registration:docs/experiment-ledger-addendum-c271-preregistration.md.
Design:docs/v5b-query-endpoint-v0.1.md.
Acceptance base:7d050e672758f97033fa23860af47d7a5d9cf15b.

One question:with identical paired CE training,does replacing arithmetic mean query-span pooling
with the pre-core local state at the FINAL visible query byte improve unseen three-character transfer
while preserving the original two-character task?

Fresh seeds271001..271005;arms mean_span and endpoint_span.
mean_span is the actual C269 SpanQueryReadout.
endpoint_span has identical14256 parameters,state keys and matched initial tensors;only read.query
source changes to the final byte position inside C269.query_span_mask(tokens).
No entity ID,target,profile,split or pair metadata enters model.forward.
Masked pre-core memory,query/key/output maps,scale4,PAD mask,Full core,post-core EOS residual,
readout_norm and decoder are unchanged.

Train both arms on exact C267 two-character data SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Use96 same-facts/different-query pairs,randperm seed+271000+epoch,24 pairs/batch,profile=epoch%3,
800 updates,200 row exposures,profile updates268/268/264. Fit RNG seed+272000 per arm.
Both use CE only;AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global clip1.

Evaluate every final state on BOTH:
1.original C267 two-character task;
2.C270 unseen three-character prompt set SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Primary PASS iff all five endpoint_span states pass every fixed criterion on both tasks.
mean_span is reference only. Fixed thresholds remain accuracy>=.90,query_pair>=.80,
evidence_drop>=.35,query_drop>=.35,two_order>=.80. HOLDOUT8-row cells require8/8.

Workload:10 models;8000 updates;384000 training rows;9080 model forwards;487680 row presentations;
36320 core calls;one10-state bundle write/load;10 strict loads. Final+replay evaluation forwards1080.
Artifacts:architecture-plan.json,dataset.json,triple-dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json plus summary.json.

Protection:472 source pins/812 protected inputs;47 deciding dependencies.
Own24;modules156;loaded3670/focused3669;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:9c94e65a1be56896f757b3275dfc24f25e5c933097b31b932a43e3e2059d2be0.

## C271 operational preflight recovery

The first C271 user invocation at activation HEAD6797e0a5ad9ee58390f455608e0d360add251fc3
stopped in Mode Validate before own tests/regression/science. No scientific log was published and
experiment_executed=False. The stop was ValueError:registration in C271.precheck.

Root cause:after preregistration,the committed manifest() text was strengthened during static review,
but the hard-coded MANIFEST_SHA was not resealed. The old value
15eeef060442ae4b17ce7d536a7a158b807170b693d3fc9f10fbea1710a9ac59 no longer matched the final
manifest bytes. Source/input count arithmetic remains registered as472/812;the first failure message
combined count/hash checks,so this recovery also separates their diagnostics.

The final committed manifest was independently reconstructed after all scientific-source edits:
9c94e65a1be56896f757b3275dfc24f25e5c933097b31b932a43e3e2059d2be0.
That value is now identical in benchmark MANIFEST_SHA,preregistration and handoff.
precheck prints actual source count,actual protected-input count and actual digest before asserting;
count mismatch and hash mismatch now have separate expected/actual error messages.

docs/experiment-authoring-runtime-gate.md now includes a mandatory Manifest sealing rule:
finish manifest-changing edits -> compute digest from final committed benchmark -> update source,
prereg and handoff -> re-fetch final bytes and recompute -> only then activate.
Any later manifest() edit invalidates the seal and requires resealing.

This was an operational preflight defect only. No C271 model was trained/evaluated,no science log
was replaced,and the scientific question,data,seeds,architecture,loss,budget and fixed gates are
unchanged. C271 remains the same experiment number.

## C271 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 5f9922702204127b7df67a3cfd9b2a27d992b7e1

Compared C270 acceptance7d050e672758f97033fa23860af47d7a5d9cf15b to review target:only C271
OWN6 paths differ. Re-fetched committed OWN6 blobs:
-source9b348dd098ecdc59fd59b8793c5c600b666f596a;
-test996141795c9d6582967ba584395cd8c5a80c44ca;
-runner1327d72130608b615c54ec65e5942da1a59817e6;
-launcher90e616bbed568af1b42a6e15d01168ecc8227ac9;
-prereg7c0d8b0af8117cfa68dc088a8a4724f4b2f84696;
-design7031d6182827f2fa4a8684fb6ff561d87c323602.

Remote static review confirms exactly24 numbered own tests,three runner Python blocks with argv sets
{1,2},{},{1,2,3,4},Validate before Execute,AUTHORING_RUNTIME_PREFLIGHT_FAILED before scientific
logging,and one unique ordered source marker for each major scientific phase. The endpoint forward
contains no target/entity/profile input and uses only the visible span endpoint.
No complete local checkout/PowerShell runtime was available to the reviewer,so own24/full3669 are
NOT claimed executed here. The user-side Mode Validate is the authoritative executable authoring gate.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C271 ->
Mode Validate(parent/source/artifact precheck472/812,own24,focused3669) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace the scientific latest log.
Execute integrity failure retries SAME C271.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without retuning.
C272 stays unregistered until C271 is validly judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
