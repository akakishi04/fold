# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository: akakishi04/fold; branch: feat/sft-target-loss; local: M:\asobiba\fold.
Authoritative runtime: Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry for a future registered run: tools/invoke_active_v2.ps1 through explicit
PowerShell7 and dispatcher ParseFile. There is currently NO ACTIVE experiment.
Accepted scientific sources/tests/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 ACCEPTED VALID NEGATIVE. C325 NOT REGISTERED.**
No ACTIVE experiment. Do not rerun C324 or any R2/R3/R4/R5/R6 recovery route.
C324 R6 scientific status = FAIL; run_execution_valid = true; candidate_gate = false.
The original scientific attempt 47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
All earlier scientific verdicts remain unchanged; C321 remains VALID NEGATIVE.
A finite valid negative is accepted evidence, not an invitation to repeat fitting.

## Latest accepted evidence -- C324 R6

Acceptance report: docs/experiment-ledger-addendum-c324-c325.md.
Acceptance report commit: f0e301ac3fc40c437ba890a2683a5d3889320b01.
Scientific execution HEAD: fcef3d5833c31d51e261ce578209bd5acd73f59c.
Published log commit: c67be12c1a08dda49f218699ecb8896ef1cf2061.
The publication parent equals the scientific execution HEAD.
Console: docs/experiment-run-logs/c324/latest.log + latest.json.
Whole uploaded log independently rehashed: 2615255 bytes;
SHA256 aa179e9f8a4d0b19bf0c5e55226731162e23cab63d2110158f8119c8742d4149.
The original CRLF bytes match metadata. Complete LF normalization gives the
published Git blob e992984130d23dfd3c393368d268ed8f93499d11. These are distinct
byte representations, not a mismatch to conceal or a reason to repeat science.

Local folder: runs/c324-scientific-r6-6b241e7f98c94ee3846a852f39456a7f/.
Primary science/summary.json SHA256:
21e752a51809a9b400c798b24c4ff405105458965b54610cfa16f71a349fbbdd.
Mandatory execution-envelope.json SHA256:
2c6013d9b4f33fb20e79e68946ad8596d756d23694d7d04508fcd0ca0e3040c3.
These artifact hashes and local verification are reported by the registered run;
the reviewer did not independently open the raw summary/envelope/checkpoint bytes.
The reviewer did independently check the complete uploaded console, all 5490 unique
test IDs/213 modules, ten measurement records, 4320 local cell gates, 2160 fact-order
gates and every emitted seed/pair decision. No second independent model replay is claimed.

Native read-lock and TRAIN/gradient preflight PASS. Seven C316..C322 verifier bodies
completed once each, nine exact verified reuses. Full separate-process regression
5490 PASS, zero failures/errors/skips; 922.503 seconds. Every registered model reached
1200 updates. Ten checkpoint replays PASS; saved semantic reconstruction completed;
all 1501 final uncached input rereads completed. Fresh-process envelope verification
confirmed 802 sources/1501 inputs/full5490 tests. Regression/science/verify exits are
all zero; terminal run_execution_valid=true. The negative is scientific, not operational.

## Deciding measurements and interpretation

Question: can explicit interior-order TRAIN coverage improve held-out binding while
retaining the original tasks? Both arms use native mean_last. Only length4 TRAIN
name templates differ (replacement, not additional training).
Seeds324001..324005; orders324101..324105; ten models,14256 parameters,64 slots,
CPUfloat64,two threads,1200 updates/model,48 rows/update; optimizer/rates unchanged.

Interior HOLDOUT pooled answers: original716/1440 -> interior4 1396/1440.
Interior both-query-correct: original22/720 -> interior4 685/720.
Every seed has strictly positive answer and query-pair gains.
Candidate interior gate3/5; original2..6 retention0/5; composite gate0/5.
Control interior gate0/5; original2..6 retention2/5 (control is not uniformly perfect).
Original length2..6 gate passes: control5/5/5/5/2; candidate5/4/1/0/0.
Original HOLDOUT correct counts by length2..6, each denominator1440:
control1440/1440/1440/1440/1427; candidate1440/1433/1352/1246/1195.

Thresholds .90/.80/.35/.35/.80 remain fixed and apply at every registered local
TRAIN/HOLDOUT cell/fact-order group. Pooled accuracy cannot override failing seeds.
Explicit coverage helps the tested interior distinction but does not meet the
replacement-and-retention objective. Candidate interior templates were seen during
fitting: no unseen-template generalization claim. Fresh paired initialization means
this does not establish sequential catastrophic forgetting. No architectural
impossibility, general LLM capability, Gate F or MinePilot readiness claim.

Unchanged C324 manifest:
b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
Unchanged scientific source blob: 2fc9e31c7037313a3fadb126af9b153608c0ac6e.
Child work:12000 updates,576000 training rows,15420 model forwards,
904320 row presentations,61680 core forwards,10 checkpoint state reloads.
Runtime timings have their R6 scopes; no controlled timing-ratio claim.
Original native-crash cause remains unknown.

## Mandatory composite protection for any successor

R6 contract: docs/c324-scientific-recovery-r6.md.
R6 post-authoring review: docs/c324-recovery-review-r6.md;
review target8fd4ef3ef287212735d568c805db8d56236c6a31, PASS for R6 only.
This is NOT a C325 review or authorization.

The unchanged primary result carries792 source pins/1491 inputs.
The mandatory companion execution envelope carries the full802 source/1501 input
union. Ten supplemental files cover R4/R5/R6 helpers/tests/launchers and R6 contract.
Every successor MUST validate BOTH records, exact subset/union relationships,
accepted execution identity, all source/input bytes and saved output contracts.
Inherit all802 combined source pins; never silently fall back to only792.
Protect new deciding-path direct/lazy dependencies and supplemental tests too.
Do not mutate accepted scientific files, source pins, tests, logs or contracts.
Preserve the full5490-test baseline,213 modules, and its sole inherited C204 exclusion.
Any new scientific run needs preregistration, additive regression, actual parent
writer/loader audit and committed-remote-byte post-authoring review before activation.
No new CI, package reinstall, artifact deletion, hidden cache reuse or automatic retry.

## Next work -- C325 NOT REGISTERED

Candidate question: at the same total budget, does retaining original length-four
TRAIN exposure alongside interior exposure recover original-task retention without
losing the interior improvement? A paired interior4 versus mixed4 comparison is a
direction, not a registered experiment. Exact mixture/schedule, fresh seeds, workload,
result schema and success rules still require pre-execution authoring/review.

No C325 source/test/runner/launcher review is complete; there is no C325 execution
HEAD and no user scientific command to issue. Do not ask for C324 logs again or
rerun the accepted experiment. Do not register an empty launcher or claim readiness.
Acceptance and future C325 preregistration/activation must be separate commits.

## Historical recovery evidence

Previous complete handoff is preserved at commit
c67be12c1a08dda49f218699ecb8896ef1cf2061:docs/experiment-ledger-and-handoff.md.
Earlier pre-R6 handoff: docs/handoff-history/c324-before-scientific-recovery-r6.md.
Original invalid attempt47ccd303f4382b7938db639e86aeb151e1f83af1;
publication68397de27b4c538ddbd22dc2209fddb7afbc2409. Parent precheck8635.121s,
full5357 PASS, second parent validation native0xC0000409 before fitting.
R2 import probes passed; R3/R4 qualified diagnostics timed out at registered caps;
these were not scientific negatives. R5 qualification completed, with no new training.
R5 execution1beb6d60f3dd0f7c72f41c9355c96827b8da4e82;
publicationf7a909f2e1a0b4bd5d03c0a54bcb63519b022b19;
logSHA2562f89e566132f0ade3660dc7c2aafb6a4946ffaa3d441341af0d39671cd663558.
Preserved R5 blobs: docs/experiment-run-logs/c324/attempts/f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19/.
R5 worker244.561s; seven completed verifiers/nine reuses;1486 final input rereads.
C323 acceptance88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf;
execution1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4;
publicatione434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
Only the current Formal state authorizes operations.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
