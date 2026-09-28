# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C269 ACCEPTED PASS (bounded query-span capability). C270 ACTIVE / INVALID ATTEMPT RECOVERY. C271 NOT REGISTERED.**

C270 attempt at11ae165db9dbb73239360a20c9c7cf005cd9c19f is INVALID.
Parent/source/artifact precheck passed,but own test23 failed before focused regression or model
evaluation. There is no C270 capability result. C269 and all earlier accepted verdicts remain intact.

## Latest accepted science — C269

Scientific execution HEAD:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Published log commit:1c34b373ad9610dddcab2e7e54294fd5d4fe7cef.
Summary:runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json.
Summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.
Acceptance:docs/experiment-ledger-addendum-c269-c270.md.

run_execution_valid=True;scientific_status=PASS;candidate_gate=True.
Seed pass counts:eos_query4/5;span_query5/5.
Pooled HOLDOUT:eos1276/1440 correct with34/720 collapse;
span1440/1440 correct with0/720 collapse.
This is bounded evidence for the registered visible-query-span intervention only.
It is not arbitrary-name/general-language capability or Gate F completion.

## C270 fixed scientific question

Experiment:C270-v5b-frozen-triple-identifiers.
Stage:V5-B-FROZEN-TRIPLE-IDENTIFIERS.
Registration:docs/experiment-ledger-addendum-c270-preregistration.md.
Design:docs/v5b-frozen-triple-identifiers-v0.1.md.

Question:do the same frozen C269 states transfer from TRAIN-seen two-character identifiers to unseen
three-character identifiers composed only from familiar bytes?

Profiles are fixed:
-tripled:uuu/vvv;
-shared_prefix2:uuu/uuv;
-shared_suffix2:uuu/vuu.

Keep exact C267 logical TRAIN192/HOLDOUT96 value split,all subsets,languages,orders,queries and values.
No three-character identifier was optimized in C269. No new byte value is introduced.
No C270 training,optimizer,gradient update or learned checkpoint write.

Strict-load C269's accepted ten-state bundle once,seeds269001..269005,arms eos_query/span_query.
For each state:
1.replay accepted two-character outputs;
2.require raw-logit error<=1e-9 and exact argmax;
3.evaluate three-character prompts;
4.replay accepted two-character outputs again;
5.require unchanged full fingerprint.

Per state81 forwards/7776 rows/324 core calls.
Total810 forwards/77760 rows/3240 core calls.
Bundle loads1;strict state loads10;new training0;new checkpoints0.

Primary PASS iff all five frozen span_query states pass every fixed criterion on both value splits
and all three new profiles. eos_query is reference only. Per answer cell:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35;two-order>=.80.
HOLDOUT answer cells8 rows therefore require8/8.
Do not rescue by retraining,profile removal,seed selection or threshold changes.

Artifacts:transfer-plan.json,triple-dataset.json,eval-outputs.pt,measurements.json,
validation-summary.json plus summary.json.
Protection contract:466 source pins/800 protected inputs;46 deciding-path dependencies.
Own24;modules155;loaded3646/focused3645.
Sole inherited exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016.
Dataset SHA256:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

## Invalid attempt and root cause

Invalid execution HEAD:11ae165db9dbb73239360a20c9c7cf005cd9c19f.
Invalid log commit:9d5fca7390b767cc39c001792e9e478f43e8f96e.
Log SHA256:3de30cc6d5d66d97d234e8068a931d5ae74b9d8782e65a3b9594448aca2a7de4.
Log bytes:5560;run_execution_valid=False.

The run passed registration/source/artifact precheck466/800 and own tests01..22,24.
test23 failed with AssertionError:8 not less than8.
Focused3645 and all frozen model evaluation did not start.

Root cause:the test used ast.Call.lineno for semantic phase order while valid calls shared a physical
source line. The scientific call order itself was correct. This was a brittle authoring test.
Static review had not executed complete own24 in the authoritative Windows checkout.

Recovery record:docs/experiment-ledger-addendum-c270-execution-recovery.md.
Runtime policy:docs/experiment-authoring-runtime-gate.md.

## Recovery implementation

Scientific data,profiles,parent weights,thresholds and frozen evaluation are unchanged.

Repair:
-major run phases are one-per-physical-line;
-test23 scopes order checks to inspect.getsource(run),uses exact unique phase markers,source offsets
 and distinct-line checks rather than raw ast.Call.lineno;
-launcher/runner now implement two phases.

Mode Validate occurs BEFORE scientific logging/publication:
-Python compile;
-parent/source/artifact precheck;
-complete own24;
-complete focused3645 regression.

Validation failure returns AUTHORING_RUNTIME_PREFLIGHT_FAILED,
experiment_executed=False and execution_log_publish_attempted=False.
It does not replace docs/experiment-run-logs/c270/latest.*.

Only after Validate PASS does Mode Execute start formal science.
The preflight transcript is copied into the formal science log as evidence.
Execute rechecks branch/tree/HEAD and then performs only frozen evaluation/replay/postcheck.

This two-phase runtime gate is the required pattern for C270 and later experiments.
Do not use ast.Call.lineno alone as a semantic order proof unless distinct physical lines are
explicitly the intended contract.

## Recovery review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 889a2b4a66a8173cc89b520432ff93d2a21d16b1

Compared invalid log commit to review target:only C270 source formatting,test,runner,launcher and
the recovery/policy docs changed. No parent C269 artifact,dataset,profile,threshold,seed or model
semantics changed.

Repair blobs:
-source:88b94c92267b916b304ecd44a8d02f89ab0eb301
-test:a9a8df362573f18601aa94cbb38f28388dd63273
-runner:7f9f408b2f101eb5279aad5373d44a4fe6dc3bb4
-launcher:eb1f2eb46b8f92115ad777b9653cfdf87acf79df
-policy:a495a2759c351ed9e86b721d91294a3b10de4c51
-recovery:9d6ab508af320b61434e032f3e7cdb023baefc76

Remote review confirms exactly24 numbered own tests;runner has three embedded Python blocks with
argv sets{1},{},{1,2,3}. In run(),initial precheck->load_reference->load_bundle->probe->analyze
markers are unique,in order and on distinct lines. Launcher Mode Validate is before the formal
logging boundary and Mode Execute is after it.

The reviewer environment cannot provide a complete checkout or PowerShell runtime.
Therefore own24/full3645/ParseFile are NOT claimed executed here.
Mode Validate is the authoritative executable authoring gate.

## Execution and stop

Use tools/invoke_active_v2.ps1 with explicit PowerShell7.
Expected sequence:
legacy_dispatcher_pin=PASS -> active_experiment=C270 ->
Mode Validate(precheck,own24,focused3645) ->
authoring_runtime_preflight=PASS ->
Mode Execute(model1/10..10/10 frozen evaluation) ->
strict replay -> persisted postcheck -> log publication.

If Validate fails,stop as operational preflight failure and do not force science.
If Execute integrity fails,retry SAME C270.
If Execute completes with run_execution_valid=True and scientific_status=FAIL,accept a valid negative.
If only publication fails,repair publication without repeating evaluation.
C271 remains unregistered until C270 is validly judged.
Gate F NOT PASSED. Preserve tools/run_c167.ps1 and all accepted evidence.
