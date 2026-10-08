# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C312 ACCEPTED VALID NEGATIVE. C313 NOT REGISTERED.**
No ACTIVE experiment until separate registration/review/activation.
C311 remains diagnostic PASS;C308 bounded PASS and C309 valid negative remain unchanged.
Latest accepted scientific execution:f481ae2b547bccc5cd5f43ae2654f89e8fa3140f.
Latest accepted published log:16e55cffe274ac24a456cb28b650fca3140d8789.
Do not rerun C312 or reinterpret the comparator as its registered candidate.

## Latest accepted evidence — C312

Acceptance:docs/experiment-ledger-addendum-c312-c313.md.
Summary:runs/c312-v5b-value-batches-c23759c73f5c4bfbb03a7c3d9c8e8198/summary.json.
SHA256:2bb0efc9a9f128a0aeda9585dabab4ee0c672ba2e9b31f4b148cc6ba959a5ed6.
Own32/focused4997 PASS;source718/protected1343;run_execution_valid=True.
All10 training runs and strict replays completed;all_pairs_matched=True.
Both arms pass5/5 at trained lengths2,3,4. At unseen5,random5/5,balanced4/5.
Only balanced312002 fails;normal five TRAIN575/576,HOLDOUT286/288.
All other normal partitions perfect. Paired five:4both,1control_only,0candidate_only,0both_fail.
No balancing superiority;no Gate F promotion;no change to previous scientific judgments.

## Next registration boundary

Proposed C313:fixed C312 checkpoints at previously untested length6,unchanged64-slot frame.
Keep all10 models and both original arms. Retained random baseline is prospective primary;
balanced remains fully evaluated,not silently discarded. No retraining or seed search.
Original2..5 outputs must reproduce before/after. This is a new task capability probe,
not a repair of C312 or a proof of arbitrary-length transfer. No command before review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical lifecycle tests.

## Historical state

Pre-acceptance handoff:docs/handoff-history/c312-pre-acceptance.md.
Git blob:f48f0bc02fd7cd00948b9fa48d38db5d8ef1fa3d.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
