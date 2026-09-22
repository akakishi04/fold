# FOLD Experiment Ledger and Handoff

> Authoritative current state. Follow `AGENTS.md` and
> `docs/experiment-conversation-handoff-protocol.md` (Current response format v2).

Repository: `akakishi04/fold`  
Branch: `feat/sft-target-loss`  
Local repository: `M:\asobiba\fold`  
Authoritative runtime: Python 3.13.15 / PyTorch 2.10.0+cu130 / NumPy 2.3.5.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C220 ACCEPTED PASS. C221 ACTIVE / NOT YET JUDGED. C222 NOT REGISTERED.**

C221 is the unique ACTIVE experiment. Source review passed; all execution preflights remain mandatory.

## Accepted C220

Scientific execution HEAD: `6bc455fa377ec9d3c70d6d1f0922c00680fd5a04`.
Published log commit: `e194716393249373a7d1f6ab552860e851ea84d0`.
Log SHA256: `dd9e8753ac48b74e369c2c87efdb0987da81c1b9379bab674af86252c8b7eed2`.
Summary SHA256: `45821b372bf0108e667274e2facd73b1f0a84f515a7d036e73874d9238fff5f7`.

Local summary:
`runs/c220-v5f-frozen-learned-stack-5bc9d133c96348de81a24d19b3ef6f93/summary.json`.

2335/2335 regression OK; prechecks/postchecks PASS; preserved inputs; clean tracked tree;
run_execution_valid True.81 checkpoint combinations,648 decisions (486 readable /162 non-readable),
all registered accuracy metrics1.0; confusion/mismatch/operation-failure counts0; training0.

Complete verdict and caveat: `docs/experiment-ledger-addendum-c220-c221.md`.
C220 is an accepted offline composition check: Reader answers are computed before Coverage is
combined in the scorer. It did not prove causal suppression of actual downstream invocations.
The648 rows are eight reused synthetic episode shapes crossed with81 checkpoint combinations.

## Accepted V5-F chain

C213 deterministic MemoryOp/provenance; C214 fixed-port numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage; C220 offline composition.
All are accepted only within their registered small reference/pilot scope.

Natural-language interfaces, native operation selection, broad unseen-task performance,
RETRACT/ASSUME learned-stack integration, acquisition and total-memory-cost superiority are not
established. Gate F remains NOT PASSED.

## Active C221 — live Coverage dispatch

Experiment: `C221-v5f-live-coverage-dispatch`.
Stage: `V5-F-LIVE-COVERAGE-DISPATCH`.

One question: with the same frozen checkpoints and episode shapes, does learned Coverage actually
control Selector/provider/Reader invocation while preserving C220 outcomes?

Changed condition: Coverage-first runtime dispatch, with an explicit independent provider
precondition check. Expected labels and precomputed answers are not dispatcher inputs.
No retraining, new semantic tasks, acquisition, RETRACT/ASSUME or cost optimization.

Main:81 combinations x8 episodes =648 live decisions; require648 successes and parent parities,
486 readable successes,162 distinct correct suppressions and zero downstream calls on suppression.

Controls:4 forced-Coverage interventions per combination =324 decisions. Force suppression on two
readable states; force allow on MISSING/OOS and require provider preconditions to block bank/Reader.
Require exact actual traces and unchanged model fingerprints.

Successful main calls: Coverage648 /Selector486 /provider486 /bank486 /Reader486.
Successful control calls: Coverage324 /Selector162 /provider162 /bank0 /Reader0.
Writer forwards3. Total model forwards2109 at PASS; new training steps0.
Counts are invocation evidence, not a speed benchmark. Model-dependent count misses are scientific
FAIL in complete runs, not automatic INVALID.

Source pins165; protected inputs195; direct dependencies16; OWN7; output artifacts5.
C221 tests34; regression modules106; loaded2370 /focused2369 with the inherited exact exclusion1.

Manifest SHA256:
`fb387b9c026ee852f4efbabab0c71cde93e03fea443f440f7b508b8fe3c3f4d8`.

Registration: `docs/experiment-ledger-addendum-c221-preregistration.md`.
Design: `docs/v5f-live-coverage-dispatch-v0.1.md`.

## C221 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `b5ee7fc81fc342152031859377260bb6f760486d`.
Scope: committed-source audit and targeted synthetic authoring validation, not formal execution.

Remote Git blob identities of all five code/test/PowerShell files matched the tested authoring
copies. After that comparison,32 targeted tests reran successfully (0 failures/errors,1.262 seconds),
all three embedded Python runner blocks compiled, and the manifest self-hash matched. Synthetic
648-main/324-intervention dispatch and parent-field adapter fixtures passed. No accepted source,
historical test or dependency was altered or removed; Git compare showed only new files and this
unpinned handoff. Loader paths, parent field meanings,16 dependencies,165/195 accounting, CLI
ordering, complete launcher guards and C222 non-registration were source-reviewed.

Not run here: the two parent-tree-dependent C221 tests, full2369 historical regression, Windows
PowerShell AST parse and local-only accepted-checkpoint execution/precheck. No synthetic test result
is represented as those checks. The authoritative runner executes all34 new tests first, then2369
focused tests, and only then science. Parser/precheck failures stop execution and are logged.

The review after this HEAD changes only review documentation; scientific conditions remain fixed.

## Historical evidence and maintenance

Earlier detailed handoff remains at
`e194716393249373a7d1f6ab552860e851ea84d0:docs/experiment-ledger-and-handoff.md`.
Gate E decisive C212 log remains `docs/experiment-run-logs/c212/latest.log`.
Do not edit/move/delete accepted source pins. In particular preserve `tools/run_c167.ps1`, the
historical regression seed runner, blob `7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789`.

No cleanup, history rewrite, CI addition or Actions-storage change is part of C221.
Actions storage is being handled separately by the user.

## Stop condition

Judge C221 before any C222 registration.
Source/artifact/schema/regression defects: INVALID / RETRY SAME C221.
Complete gate-missing run: scientific FAIL. Gate F remains NOT PASSED.
