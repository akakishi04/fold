# C230 preregistration — checked reduced preparation reuse

**C229 ACCEPTED PASS. C230 ACTIVE / NOT YET JUDGED. C231 NOT REGISTERED.**
Gate E PASSED. Gate F NOT PASSED.

## One question

Does checked reuse of W-dependent reduced-system preparation improve the same bias-update/query
workload while preserving current answers, state/provenance and safe invalidation?

One intervention: optional prepared capsule response. No accepted reference source is modified.
Keep the strong full-factor/rhs-refresh comparator, raw data, numerical matrix family, all12 cells
and state transitions unchanged. No new learned weights, tasks or safety removal.

## Accepted parent

Scientific HEAD: `339697addb6a2b8c88bad5890456fcf7b41ce398`.
Published log commit: `4fdf39f7c8b506fa1d1d010ca68bd86d35cc92b3`.
Summary SHA: `b71769d8c22ef72436b5952406632deafd100c44ed72da8f4c71c93133a0fe37`.
Measurements SHA: `c96d4154a0aef79fb50b5a34e8c7f5fad10262ebb9a79e02614d0b2a36e74786`.
Quality SHA: `a816a2829a9923afed5398ac65c616934aeff47dfef156676329d83435553904`.
Validation SHA: `08d0113b747fe902d99dedc3204775d22ae9e59cb4dc2f0fa80532ff6cb79551`.
Local summary:
`runs/c229-v5f-cost-profile-02c07c2130ab49acbf1558009be3b3b3/summary.json`.

Validate the accepted parent summary, all214 source pins,292 protected inputs and five artifacts.
The actual parent measurements schema is validated by parent.row_gate; the quality-check record
contains unprofiled/profiled lists and final `inventory`. Load and validate both artifacts through
the dedicated adapter in precheck and run. Do not treat profiler timings as speed evidence.

## Fixed workload and treatment

Dimensions2/16/64/256; queries/update1/4/16;32 initial events plus12 observed beta replacements;
two live factors, rank2/readout2. Use C228 ledger_parts and existing matrix/state factories.
Float64 CPU, threads2, deterministic algorithms, tolerance1e-10.

Arms: original H1/H2, prepared H1/H2, existing full-factor/rhs-refresh comparator.
One warm trajectory plus three measured trajectories per cell. Rotate arm order by trial+update.

Prepare the reduced path once on the prefix: finite/shape/exact symmetry checks, Cholesky(K), SPD
check I+L.T W L, pivoted LU of I+W K. Each query checks identity/version/inference flags, unchanged
base/registry/cache tensors and exact W equality; recomputes rhs from current bias; performs
lu_solve and finite result check. No bias or final answer retained. Invalid/stale preparation is
rejected; no silent fallback. CPU float64 unbatched inference only, no autograd or concurrency.

Both H1/H2 arms retain original update/commit, _read_parts, BankRead construction and metadata.
The prepared route is opt-in; original serving and historical reference tests remain unchanged.

## Fixed measurement/quality gate

Require all12 cells in fixed order, and:
- every current answer of all arms matches independent full_reference within1e-10;
- complete current symbolic-state/provenance parity after every update;
- complete identical original evidence and index retention;
- queries do not mutate their state;
- original candidate/cached final inventories exactly match accepted C229;
- prepared base exports equal original candidate, plus separately counted new cache;
- all final export inventories identical across repeats;
- preparation trace Cholesky2/cholesky_ex2/LU-factor2;
- prepared query trace LU-solve2, no query refactorization;
- original and full-cache query traces unchanged;
- reduced/full factors retain identity over12 updates;
- added reduced numerical storage72B, with metadata additionally exported/counted;
- archive members and bytes match inventories;
- all inputs/source protections preserved.

Measure preparation, construction, update, query and storage costs separately. Cold-inclusive totals
sum registered phases, not application elapsed time; validation/snapshots/traces/export are excluded
from the sums and export is separately reported. Reachable retention estimates are not process peak
RAM/VRAM. Three-trial timings are descriptive.

Audit PASS is independent of speed/storage superiority. Complete measured quality/trace failures are
scientific FAIL. Source/artifact/schema/regression, unexpected unsafe input or incomplete execution
is INVALID / RETRY SAME C230. No Gate F decision.

## Authoring registration

OWN7:
- `fold_lm/v05/prepared_capsule.py`
- `fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py`
- `tests_lm/test_v05_c230_prepared_capsule.py`
- `tools/run_c230.ps1`
- `tools/invoke_c230.ps1`
- this preregistration
- `docs/v5f-checked-reduced-preparation-v0.1.md`

Source pins221. Protected inputs305 = inherited292 + parent summary/artifacts6 + OWN7.
Direct deciding dependencies29 = prior27 plus C229 benchmark and prepared_capsule module.
Artifacts5: reuse-plan.json, reuse-exports.zip, measurements.json, quality-checks.json,
validation-summary.json. Generated outputs remain ignored under runs/.

New tests40; modules115; loaded2666 /focused2665. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA:
`c93b9845cd10c4cab316b01da41f3e03f443f75b078c8912fc27c6c23c299b95`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `dd973c4415422b3a15b229ecb18443ca75cd7cc7`.
Scope: committed-source review and targeted authoring execution, not formal science.

Re-fetched all five code/test/PowerShell files. Complete Git blob identities matched the tested
copies:
- prepared_capsule.py: f0e8d5338ea974a52ee77d3354fc6abd4993dfa0
- C230 benchmark: fe5d0dfb1e4d145b5d589a13ccb55effde28efab
- C230 tests: ecd824a60c9b8b3c1363328d75c909e13a0bda0c
- run_c230.ps1: 314f15cba80da0178bbb6e6593b18124c7e1e873
- invoke_c230.ps1: b1885a07c28ba6036d2f5e1bf9c75e9685b1b432

After comparison,38 targeted tests reran:0 failures/errors,0.971 seconds.40 methods enumerated.
Manifest matched, all three Python sources and three embedded runner Python blocks compiled,
runner argv indices precheck[1]/postcheck[1..3], unbound global references0. Additional reviewer
probe confirmed changing a capsule tensor's requires_grad flag after preparation invalidates reuse.

Numerical tests use exact fetched capsule.py blob7f1090fe95b2e3eab3967d00c6730165e34fadfb and actual
PyTorch2.10.0+cpu LU/full solves on synthetic matrices at all four dimensions. Updated bias, signed
safe/unsafe W, mutation rejection, cache bytes and kernel traces passed. Synthetic parent adapters,
archive integrity, warmup order and12-cell run/output/postcheck fixtures passed; these fixtures are
not the accepted complete memory backend.

Source review checked real parent helper signatures and quality artifact field meanings, current
bias and explicit matrix-invalidation semantics, unchanged reference/result construction, timing
versus trace boundaries,29 dependency coverage,221/305 arithmetic, all launcher guards and C231
non-registration. Git compare from the C229 publication commit shows only new acceptance/C230 files
and the unpinned handoff. No accepted source, test, log or dependency was edited or deleted.

Not executed here: test39 actual parent bank/export trajectory, test40/full2665 historical regression,
Windows PowerShell AST parse, user-local artifact precheck or formal C230 measurements. Clone failed
DNS resolution. Review PASS does not waive those checks or claim a speedup. The authoritative runner
executes40 own tests,2665 focused tests, then science, and stops/publishes logs on failure.
Only review documentation changes after the review HEAD; scientific conditions remain fixed.

## Stop

Judge C230 before C231. Preserve all accepted files and tools/run_c167.ps1. No cleanup/history
rewrite/CI addition/Actions-storage work. After this intervention decide adoption scope or stop the
local optimization track rather than continue searching indefinitely for a favorable comparison.
