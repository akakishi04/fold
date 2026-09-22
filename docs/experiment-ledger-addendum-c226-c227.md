# C226 acceptance and C227 boundary

## Formal verdict

**C226 ACCEPTED PASS as a measurement audit. Gate F remains NOT PASSED.**

Scientific execution HEAD: `17284250b25bdb5160d5d3ffa95501a4f5070e03`.
Published log commit: `2e4d4c01a9c37409cf4ebbc6c620c748b61e6156`.
Log SHA256: `783aac9892f63d9540480919f3a8b365789c29e5b3e4c0c83d5542078b9019bd`.
Summary SHA256: `ba4465c8c84e8fd54da1f7096a18056b7e53e6689a6ba3df5e1f9c559a7fac08`.
Local summary:
`runs/c226-v5f-dimension-scaling-b1186f4e625e45e0909c44ed8c585937/summary.json`.
Validation SHA: `ec05f980af138ef10f243c2a75788d50f7322f47bd5b8309b7e896c398ccaad7`.
Measurements SHA: `f312af884dc6ee11bf02bf8b1aa3022531b3d599307571172557abc242519f44`.

## Execution validity

Published metadata identifies the registered execution HEAD. The publication commit has that HEAD
as its parent and is the dedicated C226 log commit. The console records2529/2529 focused regression
OK (75.107 seconds), all quality parity and n2 parent-export parity true, dimension_audit_gate True,
preserved protected inputs/clean tracked tree and run_execution_valid True.

Acceptance uses published evidence and the recorded local artifact checks, not a reviewer rerun of
user-local artifacts. No historical source or threshold is changed by acceptance.

## Measurements

History32 and two live factors, update/readout rank2 fixed. Three timed query trials after one warmup;
timings are descriptive, not a statistically established superiority result.

| Numerical variables | H1/H2 query ms | Stateful full-solve query ms | H1/H2 export B | Full-solve export B |
|---|---:|---:|---:|---:|
| 2 | 0.4370 | 0.2398 | 11181 | 10764 |
| 16 | 0.4615 | 0.2410 | 12715 | 12298 |
| 64 | 0.4817 | 0.3805 | 29419 | 29002 |
| 256 | 0.4089 | 1.1633 | 280561 | 280144 |

At n256, H1/H2's measured median query is about2.85x faster (0.3515x the time). It is slower at
n2/n16/n64. All storage deltas are+417 bytes: no total-storage superiority. The raw ledger/index
and full numerical bridge remain retained in both arms. n256 H1/H2 build15.2929ms versus symbolic
state build1.0007ms, with shared bridge construction included on the H1/H2 path as registered.
These are not independent whole-arm cold-start totals.

Actual untimed traces confirm candidate cholesky2/cholesky_ex2/solve2 versus baseline
cholesky n/solve n. Maximum instrumented absolute discrepancy is2.7755575615628914e-17, below1e-10.
Both warm-query paths reread zero raw bytes. No learned-model inference or training was performed.

## Interpretation and confounds

The fixed-port numerical response can avoid solving the full n-dimensional system on every query.
The measured crossover at n256 is evidence only against the registered repeated dense full-solve
baseline. It is not a general speed win, model-intelligence result or memory-compression result.

The baseline performs a full Cholesky safety check and then a separate full solve for every query,
even while the numerical state is unchanged. A checked factorization can instead be prepared once
and reused for triangular solves. This is the next comparator, without changing the accepted H1/H2
candidate or the matrix/data family.

Other limitations remain: two live factors; structured synthetic descriptors; sparse matrices handled
by dense kernels; three timing samples; canonical exports rather than native checkpoints;
reachable-data estimates rather than peak RAM/VRAM; shared bridge includes unused capsule in the
symbolic arm. Repeated identical answers could also be memoized; factor reuse is not a claim of an
optimal baseline or an answer-cache benchmark.

## C227 proposed single question

On the same frozen final states, dimensions and retained evidence, how does the unchanged H1/H2
path compare with a stateful full-system baseline that reuses its checked Cholesky factorization?
Count factor preparation, cache bytes and warm solves separately; keep the original full-solve arm
as a reference. Require three-way numerical/provenance parity and unchanged C226 export inventories.
No new training, production optimization, many-factor task, answer cache or Gate F decision.

C227 is NOT REGISTERED by this acceptance document. Consult the authoritative handoff and C227
preregistration for execution permission.
