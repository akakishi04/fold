# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold; branch:feat/sft-target-loss; local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 stays immutable/pinned.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C302 ACCEPTED PASS (diagnostic integrity only). C303 NOT REGISTERED.**
C301 remains ACCEPTED VALID NEGATIVE. No ACTIVE experiment until separate preregistration/review.
Scientific execution:cfb1092c859f9e5512dcfdd63858973ab2194710.
Published log:4ce7a79c904dac84c6916825d1d801d202580665. Do not rerun C302.

## Latest accepted evidence — C302

Acceptance:docs/experiment-ledger-addendum-c302-c303.md.
Summary:runs/c302-v5b-gain-cross-d81285be58684cbfbb6d3ec7253a42ca/summary.json.
SHA256:1054849a7c416eb0a32f53e114df5501401b3f4acfeec1f6dc5aa4276d302b10.
Own32/focused4669 PASS; source658/protected1217; run_execution_valid=True.
All10 baseline/restoration comparisons have zero logit drift; all weights/hooks preserved.
Fixed weights have quad2/5 at unit and trained gains; learned weights have quad1/5 at either.
Learned-weight seen gates are two3/5 at either gain; triple2/5 at unit and3/5 at trained gain.
301003's missing quad HOLDOUT answer is not recovered by returning the gain to1.
301005 improves substantially with learned weights even at gain1; the final coefficient also
changes some answers. Do not confuse unchanged gate counts with unchanged individual predictions.
C301 remains negative; no coefficient sweep or unconditional inference substitution is adopted.

## Next registration boundary

Investigate training-gradient flow with unchanged forward computation,not another final gain sweep.
A new comparison requires fresh pairs,explicit active-gradient/capacity accounting,OWN files,
preregistration and post-commit review. No C303 command is authorized yet.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c302-pre-acceptance.md.
Git blob:6cc34252167ace2e9ae7dab831f16ac130a9e860. Accepted files stay immutable.
Only this Formal state is authoritative; historical ACTIVE commands are not executable.
