# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C306 ACCEPTED VALID NEGATIVE. C307 NOT REGISTERED.**
C305 remains diagnostic PASS;C304 remains valid negative. No ACTIVE experiment before next review.
Scientific execution:cb2bb51a8beaa888c3a8b1fca382cd20536c923b.
Published log:340f9034fc07df63cff928bfd13703dfee5ca379. Do not rerun C306.

## Latest accepted evidence — C306

Acceptance:docs/experiment-ledger-addendum-c306-c307.md.
Summary:runs/c306-v5b-broad-core-freeze-f8b13e726f314db09555a293f6d6bdf8/summary.json.
Summary SHA256:5435cf83c02b75c2dd1d3c21105dcdf30e8c567c9d8672993f7676166515cff3.
Own32/focused4813 PASS;source682/protected1267;run_execution_valid=True.
Manifest28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27.
Full/core-frozen length2/3/4/5 passes4/5,3/5,3/5,3/4. Candidate rescues306002/306005,
loses306003. All5 frozen models pass seen-length TRAIN/HOLDOUT;only one normal candidate error
remains at unseen5(306003 HOLDOUT287/288). Pooled4319/4320 is not the registered all-five gate.
Actual gradient unions14256/full and10928/frozen;core still computes and passes input gradients.
No universal freezing rule,core-necessity conclusion or production adoption follows.

## Next registration boundary

Do not retune for the remaining one error. Replicate the same paired training policies with five
fresh initialization/order seeds,unchanged data,1200 updates,64slots and scheduling algorithm.
Keep C306 negative and report new cohort separately. C307 requires OWN files,preregistration,
committed-byte post-authoring review and activation before a command is released.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c306-pre-acceptance.md.
Git blob:bedaf979e8a04fddfd7af0ad2d7476eda74a7dd5.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
