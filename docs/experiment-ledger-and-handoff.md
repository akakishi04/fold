# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C301 ACCEPTED VALID NEGATIVE. C302 NOT REGISTERED.**
C300 remains diagnostic PASS. No ACTIVE experiment until separate next-C preregistration/review.
Scientific execution:d67c900c588ff0e4c8974cd8f80721da381a8770.
Published log:871d5c55a0cb8139a1ff95fbfce95b7472bf16fa. Do not rerun C301.

## Latest accepted evidence — C301

Acceptance:docs/experiment-ledger-addendum-c301-c302.md.
Summary:runs/c301-v5b-residual-gain-8e72f4cf3e744128b905da20770c9f5b/summary.json.
Summary SHA256:19d5a94c3ce5d2bef94683b05983c44b1e76f452490e184f8ffde7b934d559c1.
Own40/focused4637 PASS;source652/protected1202;all_pairs_matched=True;run_execution_valid=True.
Manifest:c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9.
Fixed/learned quad2/1,seen tasks2/3,TRAIN direct3/3,HOLDOUT direct2/3.
301005 gains seen-length passes;301003 loses quad;301001/301004 still fail TRAIN.
All5 candidate gains fall below1(range0.733068..0.868403),but weights and training trajectories
also changed. This is not support for universal attenuation or a causal role for the final gain.

## Next registration boundary

Compare both saved weight sets at gain1 and the same seed's TRAIN-learned gain,with original
before/after controls. No new training or gain sweep. C302 requires its own committed-byte review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c301-pre-acceptance.md.
Git blob:c5d7e6c0f8d62a9d49be03fb13b742c63246f195. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
