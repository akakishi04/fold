# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C310 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C311 NOT REGISTERED.**
No ACTIVE experiment until C311 committed-byte review PASS and separate activation.
C309 remains ACCEPTED VALID NEGATIVE. C308 remains bounded ACCEPTED PASS.
Latest accepted scientific execution:bdbf7c4c410ceb9d621ae5d3ecf86e764061550b.
Latest accepted published log:45da9b7b1f63375bf0af251a7f65cc0c83b76765.
Do not rerun C310; it is not evidence of broader capability or Gate F completion.

## Latest accepted evidence — C310

Acceptance:docs/experiment-ledger-addendum-c310-c311.md.
Summary:runs/c310-v5b-value-renaming-580abae854514a7fb49fe1f702f4b50d/summary.json.
SHA256:eec24c37d318d0634623185193b50a4a7e4fb82abd6abe350a4712f807d59961.
Own32/focused4941 PASS;source706/protected1323;run_execution_valid=True.
Manifest0b4304400ddb57789a52aefb0bfe84690df7bb3fee9ef4c63e842fecfd595596.
Original C309 results and720 split/profile/language totals all reconstructed.
Saved original51840 predictions;1140480 dependent changed-input value-renaming comparisons.
Equivariant changed-input counts:
full_train378610/380160,core_frozen374320/380160,core_slow377774/380160.
Total1130704/1140480,9776 violations.
Identity51840/51840 consistent;absent-value swaps51643/51840 consistent (197 violations).
TRAIN->TRAIN483756/483840,TRAIN->HOLDOUT272840/276480,
HOLDOUT->TRAIN272840/276480,HOLDOUT->HOLDOUT101268/103680.
The mirrored cross-split directions are not independent tests.
Failed309002 five-character equivariant counts:
full18502/19008;frozen16912/19008;slow18178/19008.
Always preserve original correctness: equivariant wrong outputs remain wrong.
No new model calls,training,model state loads or checkpoints.

## Next registration boundary

One proposed C311 question: are C309's errors concentrated in particular ordered
held-out value pairs/target-value bindings and persistent across2/3/4/5 rather than
new failures caused primarily by five-character extension?
Use verified C310 value-renaming-report.json predictions/row_ids and C309 verified dataset.
Keep names,profiles,language,query,fact order,original splits,masks,all 15 models and 5 seeds.
Classify every wrong answer as other-fact value,unmentioned digit,or nondigit class.
No neural computation,no parent change,no new learning or seed search.
C311 registration,tests,post-authoring review and activation are NOT yet done.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Pre-acceptance handoff:docs/handoff-history/c310-pre-acceptance.md.
Git blob:13a3e8802eb936f1c7d015249419998f2071ccb1.
Earlier handoffs referenced in that immutable historical file.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
