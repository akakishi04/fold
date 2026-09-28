# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C272 ACCEPTED VALID NEGATIVE. C273 NOT REGISTERED.**
C272 execution8142385889335b778f49963bb4b55570165aeb26 is authoritative for science.
mean_span passed0/5 whole-state gates and boundary_pair also passed0/5.
Both passed4/5 on the original two-character task and0/5 on the unseen three-character task.
C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.
No Gate F promotion,production adoption,post-hoc seed rescue or C274 registration.

## Latest accepted science — C272

Acceptance:docs/experiment-ledger-addendum-c272-c273.md.
Execution:8142385889335b778f49963bb4b55570165aeb26.
Published log:d0fe2095579280a1d12789bfae96cd7924a00956.
Summary:runs/c272-v5b-query-boundaries-db1ee90fff94483191730b4a6e711da6/summary.json.
Summary SHA256:0955fb7f6af7400aa08799a1f369f9acc7f6730a9401478c4283401d89693f12.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:mean_span0/5;boundary_pair0/5.
Two-character subgate:mean4/5;boundary4/5.
Triple subgate:mean0/5;boundary0/5.
C273 is not yet registered.

## Latest accepted science — C271

Acceptance:docs/experiment-ledger-addendum-c271-c272.md.
Execution:d1c58db43047aceaf82b0108bace9cd731f13b76.
Published log:de79ff4539e37a7fddff31ff91dc2b40ff77f0c2.
Summary:runs/c271-v5b-query-endpoint-2873a0f5afe04737ab811192ef3caf72/summary.json.
Summary SHA256:4720c3d57d69470ec1bd0564e219dcc3bdd28a555dc6c64e4f73e10b5a1ba05b.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:mean_span0/5;endpoint_span0/5.
Two-character subgate:mean4/5;endpoint4/5.
Triple subgate:mean0/5;endpoint0/5.

Observed complementary pattern:
-endpoint improves shared-prefix triple names substantially;
-endpoint degrades shared-suffix triple names and two-character HOLDOUT;
-mean-span shows the opposite relative tendency.
This motivates a symmetric first+last boundary query but does not prove an internal mechanism.

C270 remains ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded trained-name scope.
Gate F NOT PASSED.

## C272 accepted scope and next boundary

C272 registration/recovery/runtime details remain in its preregistration,preflight recovery,
design and runtime-gate documents and the prior handoff at8142385889335b778f49963bb4b55570165aeb26.

C272 is now ACCEPTED VALID NEGATIVE. boundary_pair substantially reduced collapse and improved
shared-prefix transfer,but still failed0/5 whole-state and0/5 triple gates. The next question is
whether first/final boundaries should remain separate through their attention softmaxes rather than
being averaged into one query before attention. C273 is not yet registered.
Validate->Execute,manifest sealing and manifest-derived registration counts remain mandatory.
Gate F NOT PASSED.
