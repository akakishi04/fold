# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C225 ACCEPTED PASS. C226 ACTIVE / NOT YET JUDGED. C227 NOT REGISTERED.**
C226 is unique ACTIVE. Do not execute until post-authoring review passes.

## Accepted C225 — audit PASS, unfavorable measured costs

Scientific execution HEAD: `6669add6de53247e60731a3f23e7bed9350deec3`.
Published log commit: `88395cb0d44b0ca02fcb106967b97d966dcbe1b3`.
Log SHA: `f1d1bf677a49cabbb3974fce6e7077c051018335736f1a620d95034b95d57005`.
Summary SHA: `b54943514cebb06161851e6a79c9eb4e8fd6766429f6f2e0e2f34c79c52a78ad`.
Local summary:
`runs/c225-v5f-stateful-baseline-4df0cd59e7c34942a3d33b0932863b0f/summary.json`.
Validation SHA: `94e2028aaaff24f9cc03480abde49c2e41674d833141745e6bc34f9852620a29`.
Measurements SHA: `50e82a0a655ab63ddf00da04edab1995c7b99064ae493ba5320a0d2f348362a2`.

Regression2497/2497 OK; all four full symbolic/provenance/numeric parity checks passed;
accepted C224 candidate export inventories unchanged; run_execution_valid True; inputs preserved.
Acceptance uses published evidence and the recorded local artifact checks, not a reviewer rerun of
user-local artifacts. Full verdict: `docs/experiment-ledger-addendum-c225-c226.md`.

| History events | H1/H2 bytes | Stateful symbolic bytes | H1/H2 query ms | Symbolic query ms |
|---|---:|---:|---:|---:|
| 8 | 5743 | 5328 | 0.3271 | 0.2727 |
| 32 | 11181 | 10764 | 0.2232 | 0.1201 |
| 128 | 33100 | 32681 | 0.1720 | 0.0877 |
| 512 | 121183 | 120764 | 0.1789 | 0.0865 |

Storage deltas+415/+417/+419/+419 bytes; query median ratios1.1995/1.8585/1.9612/2.0682.
No measured storage or query-time win. Both arms avoid raw replay completely. Thus C224's avoided
replay was not uniquely due to capsules. Times are descriptive three-trial medians; export bytes
are canonical noncompressed audit data, not native checkpoints or total process memory.

Only two live factors and a2x2 full numerical system were tested. Baseline keeps the same full
bridge, including unused compiled capsule. Do not generalize to an independently minimized baseline.

## Accepted V5-F chain and limits

C213 semantics; C214 numeric closure; C215 H1/H2 commit; C216 Reader; C217 Selector;
C218 structured Writer; C219 Coverage; C220 offline composition; C221 causal dispatch;
C222 withdrawal/hypothesis isolation; C223 explicitly published-state request freshness;
C224 raw-retaining replay-cost audit; C225 stronger stateful comparator audit.

No broad natural language/generalization, learned operation kind, acquisition, concurrent/cache
freshness, many-factor bounded indexing or total memory-cost superiority is established.
Gate F remains NOT PASSED.

## Active C226 — fixed-port numerical dimension scaling

Experiment `C226-v5f-fixed-port-dimension-scaling`.
Stage `V5-F-FIXED-PORT-DIMENSION-SCALING`.

One question: with update/readout rank2 fixed, what happens to the existing checked H1/H2 versus
stateful dense full-solve comparison as the coupled numerical system grows2/16/64/256 variables?
These dimensions are numerical-memory variables, not neural parameters/layers or live-factor count.

Keep two live factors, history32, original raw hash, six relation contributions and state semantics.
At n2 both exported arm inventories must match C225 history32 exactly. Higher dimensions add
connected hidden coordinates using the registered strictly diagonally dominant SPD matrix family.
No disconnected padding, learned inference/training, production optimization or removed safety check.

Reuse C225 measurement and C224 helpers. Both retain full raw/index/bridge; count the complete
numeric base and compiled response, not just small port payloads. Shared baseline bridge contains
unused compiled capsule. Sparse coupled input uses existing dense solver, not a specialized solver.
One warmup+three descriptive timing trials per arm/dimension, CPU threads2, float64 tolerance1e-10.
Construction/index/export cost recorded; high-n construction includes the small template setup.

Extra untimed actual linear-algebra trace per arm/dimension:
- H1/H2: cholesky2, cholesky_ex2, solve2;
- symbolic: cholesky n, solve n.
Wrappers restore underlying functions and preserve checks. Full state/provenance/response parity,
query state non-mutation, zero warm raw replay, exact inventories and archive bytes required.
Audit PASS is not storage/speed superiority; unfavorable costs remain unfavorable. No Gate F decision.

Source pins196; protected inputs256; dependencies24; OWN6; artifacts5.
New tests32; modules111; loaded2530 /focused2529 with inherited exact exclusion1.
Manifest: `77a17f1330f62a1278922d40cb7313c610a7caa29c653b618b5f1e43f872a093`.
Registration: `docs/experiment-ledger-addendum-c226-preregistration.md`.
Design: `docs/v5f-fixed-port-dimension-scaling-v0.1.md`.

## C226 post-authoring review

**post_authoring_review = PENDING**

Before remote review,30 targeted tests passed, including the actual accepted capsule.py compiler/
response at all four dimensions and trace shapes. That fetched source matches its original blob
`7f1090fe95b2e3eab3967d00c6730165e34fadfb`. Other adapter/accounting fixtures are synthetic.
32 methods enumerated; manifest and three embedded Python runner blocks compiled/checked.
Not executed locally: full parent measurement test31, full historical test32/2529 suite, Windows
PowerShell AST parsing, user-local artifacts/precheck or C226 formal measurements.
Remote committed-source review is still required. Authoritative runner executes32 own tests first,
then2529 focused tests, then dimension measurements. Failure stops before the next phase.

## Historical maintenance and stop

Prior handoff: `88395cb0d44b0ca02fcb106967b97d966dcbe1b3:docs/experiment-ledger-and-handoff.md`.
Preserve all accepted source pins and `tools/run_c167.ps1` historical regression infrastructure.
No cleanup, history rewrite, new CI, unrelated architecture or Actions-storage work.
Judge C226 before C227. Gate F remains NOT PASSED.
