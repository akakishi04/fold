# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C299 ACCEPTED PASS (diagnostic integrity only). C300 NOT REGISTERED.**
C298/C297 remain diagnostic PASS;C296 remains ACCEPTED VALID NEGATIVE.
No ACTIVE experiment until next preregistration and review.
Scientific execution:1ef1436febee7b2a70b2b91cb7a5dcb2a9e04d0c.
Published log:e1013d119956a3be000667ce6ac468d7eabb8cdf. Do not rerun C299.

## Latest accepted evidence — C299

Acceptance:docs/experiment-ledger-addendum-c299-c300.md.
Summary:runs/c299-v5b-core-grid-d118c6d85dfa47dbaac6ce40655b2fe6/summary.json.
Summary SHA256:d0b2c055e190a313e5abc399716e2ec0cddfb104cc447a6216f2fab0ed312851.
Own32/focused4557 PASS;source640/protected1176;run_execution_valid=True.
Manifest796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846.
All3 same-source diagonals reproduce C298 with max logit error0.0.
Quad remaining x core:[[T,F,F],[F,F,F],[T,F,T]]. Seen tasks:[[T,F,F],[T,T,T],[T,T,T]].
Remaining297001 with core297002/297003 fails seen-length TRAIN and HOLDOUT;with core297001 succeeds.
Remaining297002 fails quad with all3 cores. No universal donor or unique cause is established.

## Next registration boundary

Proposed frozen diagnostic:separate post-core residual and added-reader output contributions at
their actual pre-normalization sum. Keep all9 learned states;no new training or output filtering.
Require original all-view predictions before/after intervention and unchanged weights/hooks.
C300 has no execution command until its six OWN files are committed,re-fetched and reviewed.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c299-pre-acceptance.md.
Git blob:a21cc63b792e937df0c703f46ec017c678024eb3. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
