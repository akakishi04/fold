# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C295 ACCEPTED VALID NEGATIVE. C296 NOT REGISTERED.**
C294 remains diagnostic ACCEPTED PASS. No ACTIVE experiment until next authoring/review.
Latest accepted scientific execution:c5ba373c0ed7e4699adc06cd2aac44624b4330e8.
Latest accepted published log:e213d8b56093f9ef37b1d9aeafc1d0fcd4f209d0.
Do not rerun C295,extend it further or select alternative checkpoints.

## Latest accepted evidence — C295

Acceptance:docs/experiment-ledger-addendum-c295-c296.md.
Summary:runs/c295-v5b-ce-budget-2361f7495977449a9c95d5dfff51d6ad/summary.json.
Summary SHA256:ea6e10cc0d0371b3dbf11316f37a794b97a7dbd1889053ce771644e9e96f10a5.
Own32/focused4421 PASS;616/1116 protection;run_execution_valid=True.
Manifest:b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.
Quad ce8001/5,ce16002/5. Seen tasks/TRAIN/HOLDOUT direct3/5 at both times.
295004's one quad HOLDOUT error disappears;295002/295003 remain failed even on TRAIN.
295002 HOLDOUT correct counts decline;295003 HOLDOUT NLL increases. No universal benefit.
Five uninterrupted trajectories,ten paired timepoint states;not ten independent models.
No Gate F promotion,model adoption or causal attribution to limited training budget.

## Next registration boundary

C296 candidate question:identical-budget rendering-balanced minibatches versus the existing
homogeneous batching. Preserve exact event multisets in24-update blocks and identical final8
updates;fresh paired seeds and ordinary CE only. This is not yet registered or executable.
Do not release a next command before separate committed-byte review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep the accepted legacy seal. Historical tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c295-pre-acceptance.md.
Git blob57f79ee235747822a3360a2c31abf777ad57056e. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
