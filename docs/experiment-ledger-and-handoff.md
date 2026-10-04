# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C300 ACCEPTED PASS (diagnostic integrity only). C301 NOT REGISTERED.**
No ACTIVE experiment until next preregistration/review. C299 remains diagnostic PASS.
Scientific execution:b1d24f9ca330711802eb450f86fc3b4c64d88666.
Published log:14e8a6972c0364a30ddb755c5d45d678d5673bea. Do not rerun C300.

## Latest accepted evidence — C300

Acceptance:docs/experiment-ledger-addendum-c300-c301.md.
Summary:runs/c300-v5b-readout-terms-ba7889d232f342d591bb8b75f48cb853/summary.json.
Summary SHA256:440d5dcd9b8293f3925f394fa9ea1fc08d9754dfd67fc411340c5d6d1548fed3.
Own40/focused4597 PASS;source646/protected1191;run_execution_valid=True.
All9 original states/logits reproduce before and after interventions with maximum drift0.0;
weights and hooks unchanged. Full seen tasks7/9 and quad3/9. Residual-only0/9 throughout.
Reader-only seen tasks6/9 and quad4/9. One quad rescue coexists with seen-task regressions
and substantial additional errors in another failed cell. No unconditional ablation adoption.

## Next registration boundary

Test one learned global residual-gain parameter against fixed original gain1,from equal initial
function and fresh paired seeds. Use TRAIN only and preserve original evaluation gates. No command
until all OWN files are committed,re-fetched,reviewed and tested. C302 NOT REGISTERED.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c300-pre-acceptance.md.
Git blob:a0e0da00bd423469dc2c994afebb2b455c4bda7d. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
