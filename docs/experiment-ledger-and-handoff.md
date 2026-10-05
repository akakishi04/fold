# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C305 ACCEPTED PASS (diagnostic integrity only). C306 NOT REGISTERED.**
C304 remains ACCEPTED VALID NEGATIVE. No ACTIVE experiment before next review.
Scientific execution:9c8beb3c66548c1e68def4ea2ced93acc0067e6e.
Published log:f89d33f9dd0dd84a54f045541117ca48a4f0a342. Do not rerun C305.

## Latest accepted evidence — C305

Acceptance:docs/experiment-ledger-addendum-c305-c306.md.
Summary:runs/c305-v5b-length-overlap-4d5851c168fc401cbc5926f1d1ca841c/summary.json.
SHA256:dd8580fe7f544b2e94688c4236cb862cfc77bb57984b04e5116a2c2cd8cc4734.
Own32/focused4781 PASS;source676/protected1257;run_execution_valid=True.
Manifest844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd.
Candidate five-HOLDOUT errors430,of which418 also wrong at4,new12,recovered4.
By failing seed304001/304002/304004:persistent/five-errors168/168,136/144,114/118.
Known dependent paired rows,not independent trials. TRAIN-value new five-errors13 also exist.
Overlap is not a mechanism diagnosis or proof that length is solved. C304 five gates remain3/2/2.

## Next boundary

Proposed next comparison:full_train versus core_frozen with2/3/4 TRAIN and unseen5,new paired
seeds,common64slots and1200updates. Do not adopt C303's better control without a new comparison.
No C306 command before six OWN files are committed,re-fetched and reviewed.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c305-pre-acceptance.md.
Git blob26b48f27c3610c8455347742fdd6774c01f4bd35.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
