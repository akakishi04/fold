# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted code/tests/preregistrations/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C309 ACCEPTED VALID NEGATIVE. C310 NOT REGISTERED.**
C308 remains ACCEPTED PASS in its original bounded scope. No ACTIVE experiment until review.
Scientific execution:a38c6ff864ab40efa74397017cfeec9f5628ca11.
Published log:c3935db64960b7e90325672aa880318a6eed77e2. Do not rerun C309.

## Latest accepted evidence — C309

Acceptance:docs/experiment-ledger-addendum-c309-c310.md.
Summary:runs/c309-v5b-core-lr-replication-e24b3b724e47415eae204d3084a68185/summary.json.
SHA256:c8a1a2bd3d6ad4e4d6f714b38af3ce8424d314d1f5771b5fca578d49df37066c.
Own32/focused4909 PASS;source700/protected1309;run_execution_valid=True.
Manifest9350f7a5ec4e91a3292f6ecce041bc3ec09f1fa1a8372a4178b58d0ceb4df74d.
Full/frozen/slow passes lengths2/3:4/4/4;lengths4/5:3/4/4. Fitted TRAIN direct all15 pass.
309005 is rescued by frozen/slow;309002 fails five in all arms,with HOLDOUT277/239/269 out288.
Slow309002 also misses12/12/13 HOLDOUT answers at trained lengths2/3/4. No new all-five result.
Do not replace C308's bounded PASS with C309 negative,or pool old successes into the new gate.

## Next registration boundary

Next question:value-renaming consistency in existing frozen outputs across original value splits.
No extra training or LR tuning. Preserve all15 states and original predictions. Separate changed
inputs from absent-value-only permutations;consistency is not correctness. C310 awaits review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c309-pre-acceptance.md.
Git blob:14e4ded5fe6d3f5fbd26b451f1bef1016d77aebe.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
