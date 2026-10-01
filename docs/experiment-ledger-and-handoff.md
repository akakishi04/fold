# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C293 ACCEPTED VALID NEGATIVE. C294 NOT REGISTERED.**
C292 remains diagnostic ACCEPTED PASS. No ACTIVE experiment before the next review.
Scientific execution:318d9fd76f4253b30d68645ee34c124457be78a3.
Published log:3d35190c718b8b3c52e5c68120358ba96811466e.
Do not rerun C293 or change its thresholds/seeds.

## Latest accepted evidence — C293

Acceptance:docs/experiment-ledger-addendum-c293-c294.md.
Summary:runs/c293-v5b-fact-support-834c844c03c84023bc4ef1c6d32e3067/summary.json.
Summary SHA256:61a92e5d5775381cc1b7ef0fa19a9fa393197afd05a7642b74b0486ab6d338e6.
Own40/focused4357 PASS;source604/protected1091;run_execution_valid=True.
Quad CE2/scaled1/support2;seen-length full4/4/4;TRAIN direct4/4/4;HOLDOUT direct4/4/4.
Candidate rescues293003 but loses293005 relative to CE. All arms fail seen-length gates on293004.
Candidate293004 HOLDOUT counts improve226->259,216->253,200->239 across2/3/4 versus CE,
but this does not clear the full gates. No robust superiority,adoption or Gate F promotion.

## Next registration boundary

Next question:for full-output errors,does the saved target-versus-other-fact ranking remain correct?
An oracle-support diagnostic may use saved logits but must not change predictions,gates or weights.
C294 command requires all6 OWN files committed,re-fetched and reviewed. C295 NOT REGISTERED.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep the accepted legacy seal. Historical tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c293-pre-acceptance.md.
Git blob041497debafe241c2ac1897def0f827f75ceff15. Earlier history remains unchanged.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
Accepted source/test/log/preregistration and protected dispatcher files remain immutable.
