# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C229 ACCEPTED PASS. C230 ACTIVE / NOT YET JUDGED. C231 NOT REGISTERED.**
C230 is unique ACTIVE. Do not execute before post-authoring review PASS.

## Accepted C229 — diagnostic audit, not speed improvement

Scientific execution HEAD: `339697addb6a2b8c88bad5890456fcf7b41ce398`.
Published log commit: `4fdf39f7c8b506fa1d1d010ca68bd86d35cc92b3`.
Log SHA: `31a1f14892cc0d94bf350100e5239fda44bee798b5a53ace2ef4d55085514db6`.
Summary SHA: `b71769d8c22ef72436b5952406632deafd100c44ed72da8f4c71c93133a0fe37`.
Local summary:
`runs/c229-v5f-cost-profile-02c07c2130ab49acbf1558009be3b3b3/summary.json`.
Measurements SHA: `c96d4154a0aef79fb50b5a34e8c7f5fad10262ebb9a79e02614d0b2a36e74786`.
Quality SHA: `a816a2829a9923afed5398ac65c616934aeff47dfef156676329d83435553904`.
Validation SHA: `08d0113b747fe902d99dedc3204775d22ae9e59cb4dc2f0fa80532ff6cb79551`.

2625/2625 regression OK in65.339s. All12 cells passed quality, exact parent exports, function-call
counts and profiler restoration. function_profile_gate True; preserved inputs, clean tree and
run_execution_valid True. Verdict uses published evidence and recorded local postchecks, not a
reviewer rerun of user-local artifacts. Full verdict: docs/experiment-ledger-addendum-c229-c230.md.

Representative n256/q16 query profile:192 queries;52,237,500ns total function self time.
ResponseCapsule.response cumulative40,931,400ns =78.36%, including nested operations; its own self
is20.57%. Cholesky192, cholesky_ex192 and solve192 calls. _read_parts cumulative3,853,300ns=7.38%.
Do not add overlapping cumulative/self percentages or present profiler costs as removable time.

This points first to repeated W-dependent response preparation/checks, not a conclusion that Python
objects or clones alone dominate. H2 already retains W/b: query _read_parts does not re-sum all H2
records in this all-committed workload. Update rebuilding remains separate work.

C227/C228 unprofiled results still show H1/H2 slower than the checked full-factor/rhs comparator
(C2281.59x-5.37x across12 cells). C229 diagnosed work; it did not reverse those results or pass Gate F.

## Accepted chain and limits

C213 semantics; C214 closure; C215 H1/H2 commit; C216 Reader; C217 Selector; C218 structured Writer;
C219 Coverage; C220 offline composition; C221 causal dispatch; C222 withdrawal/hypothesis isolation;
C223 explicit request freshness; C224 replay cost; C225 stateful baseline; C226 dimensions;
C227 checked full-factor reuse; C228 bias-update/query cost; C229 scoped function profile.

These are small reference/pilot scopes, not general language/reasoning, concurrent cache correctness,
bounded many-factor indexing or whole-system efficiency evidence. Gate F remains NOT PASSED.

## Active C230 — checked reduced preparation reuse

Experiment C230-v5f-checked-reduced-preparation-reuse.
Stage V5-F-CHECKED-REDUCED-PREPARATION-REUSE.

One question: can checked reuse of W-dependent reduced preparation improve the same bias-update/query
workload without changing answers, state semantics, guards or the strong comparator?

Add optional prepared_capsule.py; leave accepted reference/runtime paths unchanged. It checks SPD at
preparation, factors I+W K with pivoted LU, and retains only W/LU/pivots plus binding/version guards.
Every query checks capsule/base/registry/cache identity/version/inference flags, exact W equality,
current bias finiteness and result finiteness. Current bias is always recomputed; no answer cache.
Changed W requires explicit new preparation. No silent fallback or safety disable. CPU float64,
unbatched inference only; no autograd/concurrency/unsafe external alias-write contract.

Same dimensions2/16/64/256, bursts1/4/16,32-event prefix+12 replacements, two live factors/rank2.
Compare original H1/H2, prepared H1/H2 and unchanged full-factor/rhs reuse with cyclic arm order,
one warm trajectory and three measured trajectories per cell. No profiler in timings.

Require every current query/state/provenance match; original two final exports equal C229 quality
artifact inventories; prepared base exports equal original plus counted cache; repeated exports
identical; checked preparation and final query traces exact. Extra reduced numerical cache72B plus
metadata, not whole memory size. Count original evidence/index/full bridge, setup/update/query/export
and reachable-state estimates. Cold-inclusive sums are registered phases, not application wall time.
Audit PASS does not require faster/smaller results. Gate F remains NOT PASSED.

Source pins221; protected inputs305; deciding dependencies29; OWN7; artifacts5.
New tests40; modules115; loaded2666 /focused2665 with inherited exact exclusion1.
Manifest: `c93b9845cd10c4cab316b01da41f3e03f443f75b078c8912fc27c6c23c299b95`.
Registration: docs/experiment-ledger-addendum-c230-preregistration.md.
Design: docs/v5f-checked-reduced-preparation-v0.1.md.

## C230 post-authoring review

**post_authoring_review = PENDING**

Initial38 targeted tests passed;40 methods enumerated. Exact fetched capsule.py reference and actual
PyTorch kernels checked numerical parity at four dimensions, updated bias, signed safe/unsafe W,
mutation rejection, trace restoration, cache bytes and synthetic adapter/archive/run wiring.
A final committed-remote reread and rerun are still required.

Not executed here: test39 actual parent bank/export trajectory, test40/full2665 historical suite,
Windows PowerShell AST, user-local artifact precheck or formal C230 measurement. Clone failed DNS
resolution. Synthetic fixtures do not replace those checks. The authoritative runner executes40 own
tests,2665 focused tests, then science, stopping and publishing logs on failure.

## Historical maintenance and stop

Prior handoff: 4fdf39f7c8b506fa1d1d010ca68bd86d35cc92b3:docs/experiment-ledger-and-handoff.md.
Preserve all accepted source pins and tools/run_c167.ps1. No cleanup/history rewrite/new CI/
Actions-storage work. Judge C230 before C231. After this bounded intervention decide adoption scope
or stop this local optimization track; do not indefinitely seek favorable workloads instead of
returning to whole-model language/reasoning evaluation.
