# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C226 ACCEPTED PASS. C227 ACTIVE / NOT YET JUDGED. C228 NOT REGISTERED.**
C227 is unique ACTIVE. Source review passed; all execution preflights remain mandatory.

## Accepted C226 — dimension audit, limited query crossover

Scientific execution HEAD: `17284250b25bdb5160d5d3ffa95501a4f5070e03`.
Published log commit: `2e4d4c01a9c37409cf4ebbc6c620c748b61e6156`.
Log SHA: `783aac9892f63d9540480919f3a8b365789c29e5b3e4c0c83d5542078b9019bd`.
Summary SHA: `ba4465c8c84e8fd54da1f7096a18056b7e53e6689a6ba3df5e1f9c559a7fac08`.
Local summary:
`runs/c226-v5f-dimension-scaling-b1186f4e625e45e0909c44ed8c585937/summary.json`.
Validation SHA: `ec05f980af138ef10f243c2a75788d50f7322f47bd5b8309b7e896c398ccaad7`.
Measurements SHA: `f312af884dc6ee11bf02bf8b1aa3022531b3d599307571172557abc242519f44`.

Regression2529/2529 OK; full symbolic/provenance/numeric parity at four dimensions;
n2 C225 export inventories unchanged; checked candidate solve size2 versus full2/16/64/256;
run_execution_valid True; protected inputs and tracked tree preserved.
Acceptance uses published evidence and recorded local artifact checks, not reviewer-side rerun of
user-local artifacts. Full verdict: `docs/experiment-ledger-addendum-c226-c227.md`.

| Numerical variables | H1/H2 query ms | Stateful full solve ms | H1/H2 bytes | Symbolic bytes |
|---|---:|---:|---:|---:|
| 2 | 0.4370 | 0.2398 | 11181 | 10764 |
| 16 | 0.4615 | 0.2410 | 12715 | 12298 |
| 64 | 0.4817 | 0.3805 | 29419 | 29002 |
| 256 | 0.4089 | 1.1633 | 280561 | 280144 |

At n256 the measured H1/H2 median is0.3515 times the repeated-full-solve median (about2.85x faster).
It is slower at the other sizes. Storage+417 bytes at every size: no total-storage win. Maximum
instrumented discrepancy2.78e-17 within1e-10. Both paths avoid raw replay.

Three-trial descriptive timings, two live factors, sparse coupled input on dense kernels and shared
complete bridge only. The baseline refactorizes on every unchanged-state query. Factor reuse and
answer caching were not compared. Do not claim general speed or memory superiority or Gate F.

## Accepted V5-F chain and limits

C213 semantics; C214 numeric closure; C215 H1/H2 commit; C216 Reader; C217 Selector;
C218 structured Writer; C219 Coverage; C220 offline composition; C221 causal dispatch;
C222 withdrawal/hypothesis isolation; C223 explicit-publication request freshness;
C224 raw-retaining replay-cost audit; C225 stronger stateful comparator; C226 dimension audit.

C225 showed no storage/query-time advantage at n2 versus ordinary state retention.
C226 adds only a scoped large-n crossover against repeated dense full solves.
No broad language/generalization, native operation selection, acquisition, concurrency/answer-cache
freshness, bounded many-factor indexing or total memory-cost superiority is established.
Gate F remains NOT PASSED.

## Active C227 — checked factor reuse attribution

Experiment `C227-v5f-checked-factor-reuse-attribution`.
Stage `V5-F-CHECKED-FACTOR-REUSE-ATTRIBUTION`.

One question: on the same frozen C226 states, does H1/H2 retain a measured advantage when a full-system
comparator reuses a checked Cholesky factor instead of repeating the factorization every query?

Keep dimensions2/16/64/256, history32, two live factors, rank/readout2 and the exact matrix/raw family.
Original H1/H2 and symbolic exports must match accepted C226 bytes at every dimension.
Add only a benchmark-local full-factor/rhs cache; no accepted production code, safety check or weight
is altered. Cache checks exact state/bridge binding and tensor identity/version stamps; full SPD
check occurs at preparation. This is a frozen-state comparator, not general cache invalidation.

Three arms: unchanged H1/H2, original stateful full_reference, cached Cholesky/cholesky_solve.
All retain complete raw/index/bridge; cached arm counts additional factor/rhs and metadata.
Extra retained cache tensor bytes48/2176/33280/526336. Shared baseline bridge still contains unused
compiled capsule. Same final answers could also be memoized; no optimal-baseline claim.

One warmup+three measured queries per arm/dimension, cyclic order, CPU threads2, float64 tolerance1e-10.
Record construction, cache preparation, index/export costs and reachable data separately.
Instrument untimed preparation/query calls: cached query uses cholesky_solve n without refactorization;
original arms retain their C226 checked call paths. Archive/member bytes and state/provenance/response
parity required. Audit PASS does not require measured speed/storage superiority.
No training, production optimization, many-factor query, answer-cache implementation or Gate F decision.

Source pins202; protected inputs268; dependencies25; OWN6; artifacts5.
New tests32; modules112; loaded2562 /focused2561 with the inherited exact exclusion1.
Manifest: `4ea370a98b04bff4364f2ec8dccbc5fff658c1d4529a13ee6c3fc1d0c0cfa23d`.
Registration: `docs/experiment-ledger-addendum-c227-preregistration.md`.
Design: `docs/v5f-checked-factor-reuse-v0.1.md`.

## C227 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `70586952bbaa23d1d5d7cf9efe521dc3b9ea8557`.
Scope: committed-source review and targeted authoring tests, not formal science.

All four re-fetched remote code/test/PowerShell blobs match the executed local copies. After the
comparison,30 targeted tests reran (0 failures/errors,2.491 seconds);32 methods enumerated;
manifest matched; both Python files and all three embedded runner Python blocks compiled;
unbound executable c### aliases0; CLI indices precheck[1]/postcheck[1..3].

Real torch Cholesky/cholesky_solve versus solve was checked at all four dimensions on synthetic
bridge fixtures, including nonfinite/non-SPD/capability rejection, exact snapshot bindings and
mutation stamps. Trace restoration, archives and synthetic run loader/export/postcheck order passed.
Source review checked actual parent helper/signature/field meanings, original two-arm byte parity,
checked factor preparation, complete retention/cache accounting, untimed trace isolation,25 deciding
dependencies,202/268 arithmetic, launcher guards and C228 non-registration. Git compare shows only
new files and the unpinned handoff; no accepted source/test/log/dependency edit or deletion.

Not executed locally: actual parent backend/export test31, historical test32/full2561 suite, Windows
PowerShell AST parse, local user-artifact precheck or formal C227 measurement. Clone failed DNS
resolution. Synthetic bridges/run fixtures are not represented as full-backend or historical tests.
Authoritative runner executes all32 own tests, then2561 focused tests, then measurement; a failure
stops before the next phase and logs are published. Review PASS does not waive those gates.
After the review HEAD only review documentation changes; scientific conditions remain fixed.

## Historical maintenance and stop

Prior handoff: `2e4d4c01a9c37409cf4ebbc6c620c748b61e6156:docs/experiment-ledger-and-handoff.md`.
Preserve all accepted source pins and `tools/run_c167.ps1` historical regression infrastructure.
No cleanup, history rewrite, new CI, unrelated architecture or Actions-storage work.
Judge C227 before C228. Gate F remains NOT PASSED.
