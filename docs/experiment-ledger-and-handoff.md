# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C294 ACCEPTED PASS (diagnostic integrity only). C295 NOT REGISTERED.**
No ACTIVE experiment until next preregistration/review. C293 remains ACCEPTED VALID NEGATIVE.
Scientific execution:dead7ca153a8aadb6f30135f47a59981e4b4dfcf.
Published log:de959a8147df888a6d51234fad7971f4593d25a2. Do not rerun C294.

## Latest accepted evidence — C294

Acceptance:docs/experiment-ledger-addendum-c294-c295.md.
Summary:runs/c294-v5b-support-choice-79d31882e59f46fe933bb7e863bad8e2/summary.json.
Summary SHA256:abdf1b71f56e3f452d3955277a659722ca38f95a47be1dc6ca5330e688e37e10.
Own32/focused4389 PASS;610/1106 protection;run_execution_valid=True.
Manifest:e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.
Candidate293004 HOLDOUT full/conditional correct:two259/276,triple253/269,quad239/255 out of288.
Quad candidate has16 outside-but-correct-choice,24 outside-and-wrong-choice,9 other-fact errors.
Even oracle support leaves33 errors. This is diagnostic only;no decoder/gate changes or causal proof.
User RESULT_ALREADY_PUBLISHED is the duplicate-run guard,not a missing scientific execution.

## Next registration boundary

Proposed C295:ordinary CE800 versus1600 updates on matched uninterrupted fresh trajectories.
No next command before separate authoring/review. C296 NOT REGISTERED.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep the accepted legacy seal. Historical tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c294-pre-acceptance.md.
Git blob79a5c1cc8d471e47ef143c7dd8d46c93361bc491. Accepted sources/tests/logs remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
