# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C298 ACCEPTED PASS (diagnostic integrity only). C299 NOT REGISTERED.**
C297 remains diagnostic ACCEPTED PASS;C296 remains ACCEPTED VALID NEGATIVE.
No ACTIVE experiment until next preregistration/review.
Scientific execution:026dc1983cbdf7c54e6bb6ba6302f04430b17a36.
Published log:5113666bdb581526cdc0f2707e493258accbc028. Do not rerun C298.

## Latest accepted evidence — C298

Acceptance:docs/experiment-ledger-addendum-c298-c299.md.
Summary:runs/c298-v5b-components-13bf02bea0764e2cb8fe8802cfa52eb7/summary.json.
Summary SHA256:a57e5f2fc3071c630b6cd083f855511b035a4d8478c91e22f86fe97c373add6e.
Own32/focused4525 PASS;source634/protected1161;run_execution_valid=True.
Manifest:e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62.
All3 diagonals reproduce C297 with max logit error0.0. Two/three tasks all9 pass.
Quad rows(backbone297001..3) x columns(reader297001..3):
[[True,True,True],[False,False,False],[True,True,True]].
Backbone297002 normal quad errors vary2/18/14 across reader choices. Reader is not irrelevant.
This bounded fixed-order grid does not prove a universal backbone cause or explain prior TRAIN failures.

## Next registration boundary

Investigate recurrent-core versus remaining-backbone initialization with fixed added reader/order.
Use all three original levels and exact C298 diagonal reproduction,not successful-donor selection.
No C299 command until OWN files are committed,re-fetched and reviewed.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c298-pre-acceptance.md.
Git blob:f1a6fee222da8c7c95c234935751d2c31b0ff7ea. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
