# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C297 ACCEPTED PASS (diagnostic integrity only). C298 NOT REGISTERED.**
C296 remains ACCEPTED VALID NEGATIVE. No ACTIVE until the next preregistration/review.
Scientific execution:18576c2df5f928d5904bd99bd39a2de58c5736da.
Published log:d541b5a370adbe4b80064294076d98be7c2a75d5.
Do not rerun C297 or promote its diagnostic PASS to a capability gate.

## Latest accepted evidence — C297

Acceptance:docs/experiment-ledger-addendum-c297-c298.md.
Summary:runs/c297-v5b-init-order-1e8b2002a1e142db81c0c8b5d51a1b4a/summary.json.
Summary SHA256:9bfceee367a11edfe9ae5b62f381cdaf183ef357109f5dff7b345a11e3180aba.
Own32/focused4493 PASS;source628/protected1146;run_execution_valid=True.
Two/three all9 pass. Quad rows(initial297001..3) x columns(order297101..3):
[[True,True,True],[False,False,False],[True,True,True]].
Initial297002's quad normal errors vary18/1/18 with order;do not call order irrelevant.
All seen-length normal answers correct;the earlier TRAIN failure was not reproduced in this grid.
Finite-grid association is not population variance,an independently replicated mechanism,or an
architectural diagnosis. No old gate changes or best-seed deployment.

## Next registration boundary

Proposed next bounded question:backbone versus added-reader initialization with all three original
levels crossed at a fixed order. Same-component diagonals must reproduce C297 from fresh training.
No next command until reviewed OWN files are committed and re-fetched.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c297-pre-acceptance.md.
Git blob28b902f8b9d1da261638b14a492cb2a19d3b1c21. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
