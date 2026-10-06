# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C307 ACCEPTED VALID NEGATIVE. C308 NOT REGISTERED.**
C306 remains valid negative. No ACTIVE experiment pending next preregistration/review.
Latest accepted scientific execution:4371ad8de650261f6cdacacfd9972efcdbe970a8.
Latest accepted published log:6cdbde45709579c736d2fc0bd682f992a6d63b25. Do not rerun C307.

## Latest accepted evidence — C307

Acceptance:docs/experiment-ledger-addendum-c307-c308.md.
Summary:runs/c307-v5b-core-replication-468c370e9c4b491585226c5492a8b52c/summary.json.
SHA256:5cb0683de649361966f2ab549aeab94d20643d64fe68d1d8bbe3497e6d637e42.
Own32/focused4845 PASS;source688/protected1281;all_pairs_matched=True;run_execution_valid=True.
Length2/3/4/5 full3/3/3/3,frozen4/4/4/3. Both arms TRAIN direct4/5.
Five-character both-pass2,full-only1,frozen-only1,both-fail1. Frozen rescues307002,but loses307001.
Both fail307005 including TRAIN;core freezing is not a universal solution. C306's five-character
count advantage was not reproduced. No result pooling or seed hunting substitutes for the gates.

## Next registration boundary

Prospective core-only learning-rate attenuation versus both full learning and frozen core.
Keep2/3/4->5,normal CE,data,budget,full-mask thresholds. No execution command before new review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c307-pre-acceptance.md.
Git blob:e202ed37a170da9f2da791b4392560f1c35f0473.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
