# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C291 ACCEPTED VALID NEGATIVE. C292 NOT REGISTERED.**
C290 remains ACCEPTED PASS (diagnostic integrity only). No ACTIVE experiment until next review.
Scientific execution:8d33edabbc7a91654a3da6056091cec2d84d9a24.
Published log:49f30351a7687884bf0b9a6f2ddd304de8c26d1e.
The earlier CP932 failure was recovered. Do not rerun C291 or change its gates.

## Latest accepted evidence — C291

Acceptance:docs/experiment-ledger-addendum-c291-c292.md.
Summary:runs/c291-v5b-answer-margin-7f15f2dbf9ca4a16a2ba0ce2271a3421/summary.json.
Summary SHA256:271cc816f49fd7d53714508fee284bbf9f93783b3e74ac2728fc2a5286d740fa.
Own40/focused4285 PASS;source592/protected1066;run_execution_valid=True.
Manifest99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.
Quad CE4/5,pair_sum2/5,answer_margin4/5. Two/three4/5/4;TRAIN direct5/5/5;HOLDOUT direct4/5/4.
CE and candidate fail seen-length HOLDOUT on291003 despite normal TRAIN fitting;pair_sum passes
seen-length gates on that seed but fails quad. No superiority to CE or production adoption.

## Next registration boundary

Next question:classify each saved C291 error as another fact's value,an absent known value,or a
non-value output. Preserve all15 models and all normal evaluation rows;do not infer hidden causes.
No new neural execution or loss sweep is proposed. C292 command requires committed-byte review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c291-pre-acceptance.md.
Its Git blob is96a00899912c1564f4bb9575445ecce08372a819. Earlier handoffs remain unchanged.
Only this Formal state is authoritative;historical ACTIVE commands must not be executed.
Accepted sources/tests/logs/preregistrations and protected dispatchers are immutable.
