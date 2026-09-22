# C222 preregistration — withdrawal and hypothesis lifecycle

**C221 ACCEPTED PASS. C222 ACTIVE / NOT YET JUDGED. C223 NOT REGISTERED.**
Gate E PASSED. Gate F NOT PASSED.

## One changed condition

Extend the accepted frozen live stack to one continuing withdrawal/hypothesis lifecycle. Ask whether
a revoked observation stays unpublished when a same-named hypothesis exists in another scope, while
an unrelated observed anchor remains usable. No production module is changed or added.

Operation kinds and hypothesis construction remain oracle. Writer factor+relation, Coverage,
Selector and Reader are the accepted frozen checkpoints. No retraining, new CI, acquisition,
indexing, memory-cost optimization or Actions-storage work.

## Accepted parent and protection

Scientific HEAD: `ed82010bede050c0209be8b540d83cc544fa6bd4`.
Published log commit: `438de3443827bada6d4dcdb02b37404aca4194a0`.
Summary SHA256: `70cee94a95b20d538d86a041a3518151f019e03d15594132720c041224859766`.
Validation artifact SHA256: `c3ed8f149357c27281122b3cab9876b371d8da25a57dd536fa4e1b32f0a7ab0c`.
Local accepted summary:
`runs/c221-v5f-live-coverage-dispatch-cbcaaf2ea8b94d7a8b748426810f442b/summary.json`.

Validate the C221 result using its actual validator/gate and registered execution identity. Preserve
all165 parent source pins and195 protected inputs, including all inherited frozen checkpoints.
Reuse C220's fingerprint-checked restoration helpers through the accepted C221 checkpoint root.
Require all parent output sizes/SHA values and the validation artifact identity to match.

## Fixed trajectory

One bank/state trajectory per Writer checkpoint. Three trajectories total.

| Stage | project/beta Coverage | Answer class | Symbolic beta state | memory/evidence/time/epoch |
|---|---|---:|---|---|
| anchor_only | MISSING | none | MISSING | 1/1/1/1 |
| beta_hot | HOT_REQUIRED | 2 | SUPPORTED | 2/2/2/1 |
| beta_committed | SUPPORTED | 2 | SUPPORTED | 2/2/2/2 |
| beta_replaced | SUPPORTED | 0 | SUPPORTED | 3/3/3/2 |
| beta_retracted | MISSING | none | RETRACTED | 4/4/4/2 |
| shadow_assumed | MISSING | none | RETRACTED | 5/4/4/2 |
| shadow_ended | MISSING | none | RETRACTED | 6/4/4/2 |
| project_ended | OUT_OF_SCOPE | none | OUT_OF_SCOPE | 7/4/4/2 |

Anchor: learned ASSERT global/alpha class1, committed before the first snapshot. Every stage must
still yield alpha answer class1. Beta is first written as class2, replaced with class0, then revoked.
The later ASSUME uses sandbox/beta with beta-class-2, deliberately matching the old factor name/value
but not the project scope. END_SCOPE sandbox then END_SCOPE project do not advance evidence clocks.

Symbolic/export audits require the exact status/relation/provenance tuples in code, observed-only
exports, live hypothesis provenance only inside sandbox and unchanged H2 W/b after RETRACT through
the remaining stages. Coverage MISSING means lack of current authoritative support; MemoryRead
RETRACTED remains distinct and must not expose the old relation.

## Query and control matrix

Each of81 frozen checkpoint combinations queries alpha and beta at all8 stages:1296 decisions.
Readable decisions891 =648 anchor +243 beta. Suppressions405.

Successful main calls: Coverage1296 /Selector891 /provider891 /bank891 /Reader891.
Correct alpha anchor answers648. Beta answers after RETRACT must be0.
Normal suppressed queries must make zero downstream calls.

At beta_retracted and shadow_assumed force the Coverage proposal to SUPPORTED while still invoking
and recording the original classifier. Two controls x81 combinations =162.
Require BLOCKED_MISSING, no answer and trace coverage/selector/provider.
Control calls: Coverage162 /Selector162 /provider162 /bank0 /Reader0.

Expected labels are scorer-only; fresh current-state requests enter the unchanged C221 dispatcher.
No stale request closure or cached Reader answer is reused.

## Workload and fixed gate

Seeds unchanged:
Writer218001/218002/218003; Coverage219001/219002/219003;
Selector217001/217002/217003; Reader216001/216002/216003.

CPU, threads2, deterministic algorithms; inherited float32 neural /float64 numeric path.
Writer forwards3. At PASS total model forwards3405, calculated as3+1296+891+891+162+162.
Training0. Checkpoint fingerprints before/after identical.

PASS requires:
-1296 main successes;
-162 control successes;
-648 anchor successes;
-405 correct suppressions;
-no post-RETRACT beta answers;
-no suppressed downstream calls;
-three exact passing trajectory audits;
-exact successful main/control call dictionaries;
-Writer accuracy1.0, unchanged fingerprints, model forwards3405, training0.

Complete metric/answer/audit failures are scientific FAIL. Malformed artifacts, source drift,
regression errors or operation exceptions preventing a complete trajectory are INVALID / RETRY SAME
C222. Do not alter thresholds after seeing a run. Count deviations driven by completed model
predictions are gate metrics, not validator prerequisites.

## Files and counts

OWN6 (there is deliberately no new production module):
- `fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py`
- `tests_lm/test_v05_c222_withdrawal_lifecycle.py`
- `tools/run_c222.ps1`
- `tools/invoke_c222.ps1`
- this preregistration
- `docs/v5f-withdrawal-hypothesis-lifecycle-v0.1.md`

Source pins171 = parent165 + OWN6.
Protected inputs207 = parent195 + parent summary/artifacts6 + OWN6.
Deciding dependency set17: C220 direct set14 + C220 benchmark + memory_dispatch + C221 benchmark.
All repository helpers actually called must be in parent/OWN protection, including lazy imports.

Output artifacts5: lifecycle-plan, timeline-audit, live-decisions, forced-allow-decisions,
validation-summary. Raw outputs/checkpoints remain under ignored runs/.

New tests32; modules107; loaded2402; focused2401. Keep only the already registered exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
No accepted historical source/test is edited or removed.

Manifest SHA256:
`1b94c0af7c1d828f54c5519dd9169a9e2a7985ddd91b155a72d312d39e26a828`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `3ef62466b555fc1df70abdc8fb92b825b7999f76`.
Scope: committed-source review and targeted synthetic authoring tests, not formal C222 science.

Remote benchmark/test/runner/launcher content was fetched after all files were committed. Its Git
blob IDs match the tested author copies exactly:

| File | Git blob |
|---|---|
| C222 benchmark | e8956469df17dc922c7ef26e57a83f999766e21d |
| C222 tests | 5936e58d1f7dfdcedde98fe1da7ddf0981b75407 |
| run_c222.ps1 | 7dfb5257eabb5f0dd0151f378b86b930cf31ad71 |
| invoke_c222.ps1 | e5326abf1e163f4d6159f9a498662c065be03158 |

The local memory_dispatch copy used in synthetic tests also matches accepted blob
`da7efd7cf6c1c9a748ed35953df1a26a6e4c30fe`.

After remote identity comparison,30 targeted tests were rerun:30 PASS,0 failures/errors,
0.173 seconds in Python3.13.5 /PyTorch2.10.0+cpu /NumPy2.3.5. Synthetic model/provider/audit fixtures
exercised1296 main and162 forced-allow decisions and exact call accounting. The manifest self-hash
matched,32 new methods were enumerated, Python files and all three embedded runner Python blocks
compiled. These are not numerical-parent or accepted-checkpoint scientific results.

Git comparison from the published C221 log commit shows only the new C222/acceptance files and
unpinned handoff changes: no accepted production source, historical test, dependency or log was
edited/deleted. Source review checked the actual parent request builder's scope/factor/observed
preconditions, symbolic RETRACT/ASSUME/END_SCOPE semantics, one-bank trajectory construction, fresh
request binding, expected-label separation, C221 summary fields, checkpoint restoration call chain,
171/207 accounting,17 deciding dependencies, full launcher guards and CLI argument order.

An initial author-side forward-total arithmetic error was caught before registration and corrected
to3405. No scientific condition changed during committed-source review.

Not executed here: `test_31_actual_accepted_memory_timeline`,
`test_32_actual_historical_suite_counts`, actual accepted numerical trajectory, full2401 historical
regression, Windows PowerShell AST parsing, local-only accepted artifact precheck and frozen-model
C222 science. They remain mandatory on the user's checkout. No synthetic/stub evidence is called
a pass of those checks. The runner executes all32 own tests before full regression and science.

## Interpretation and stop

1296 decisions are a small synthetic trajectory crossed with checkpoint combinations, not1296
independent new tasks. Snapshots retained for evaluation are not a production memory-cost claim.
Fresh requests are built from each current state; arbitrary old request/cache freshness is not
covered. No acquisition, learned operation-kind selection or hypothetical answer generation.

Judge C222 before any C223 registration. Gate F remains NOT PASSED.
