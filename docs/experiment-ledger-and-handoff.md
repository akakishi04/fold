# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C304 ACCEPTED VALID NEGATIVE. C305 NOT REGISTERED.**
C303 remains ACCEPTED VALID NEGATIVE. C302 remains diagnostic PASS.
No ACTIVE experiment until separate preregistration and reviewed activation.
Scientific execution:f309fde3e2aa8df33156ce55c703c9c37c6e106b.
Published log:e54f443acbbc5e55d3dcab18d08c418d56867d1e. Do not rerun C304.

## Latest accepted evidence — C304

Acceptance:docs/experiment-ledger-addendum-c304-c305.md.
Summary:runs/c304-v5b-length-breadth-5090e7ce18a8444e9095afe14ad41266/summary.json.
SHA256:c4b0babc2f7b9ea544c96385ed386a721630ce81bfb26fcb5e1e028450670717.
Own40/focused4749 PASS;source670/protected1243;all_groups_matched=True;run_execution_valid=True.
Manifest:af8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0.
Lengths2/3/4/5 counts by four_only/three_four/two_three_four:
0/1/2;2/2/2;3/2/2;3/2/2. All-length passes0/1/2.
Same4/5 full-gate outcomes in all15 models,not proof of same individual errors.
Broader coverage did not improve five-character reliability at this budget;not adopted.
Candidate304001 fails trained-length HOLDOUT despite fitted TRAIN-direct PASS;
candidate304002/304004 fail fitted TRAIN direct. No automatic Gate F promotion.

## Next registration boundary

Next question:aligned saved-output overlap of four-character and five-character errors,
with2/3 descriptive references. No new fitting or inference is needed. Do not infer individual
error overlap from aggregate gates. C305 requires reviewed OWN files before command release.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Complete previous handoff:docs/handoff-history/c304-pre-acceptance.md.
Git blob:f421097c4157e95d0eb43e706d31fd4a4b54a4fe.
Only this Formal state is authoritative;historical ACTIVE commands must not be executed.
