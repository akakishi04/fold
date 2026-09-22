# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C228 ACCEPTED PASS. C229 ACTIVE / NOT YET JUDGED. C230 NOT REGISTERED.**
C229 is unique ACTIVE. Source review passed; all execution preflights remain mandatory.

## Accepted C228 — audit PASS, update/query speed loss

Scientific execution HEAD: `0b78d33987d0e123efff58675693c4f19b81953e`.
Published log commit: `68cba193bb1affe648f522f41ce6444f8c39e168`.
Log SHA: `9ca6822e5c36b02d2129398aa1bec7b130b2fb00d82a83371a2f27b30d51fd91`.
Summary SHA: `44ddf79b6ae1aadb5fb28e37e8528e40c1384b13a152283badbb9eb1be20e9a6`.
Local summary: `runs/c228-v5f-update-query-76eea62720cf4857a7122cd48c400f1a/summary.json`.
Validation SHA: `29779710b3826659244ea89f3c57f8dffdc0b824fe0247a205150b63ce8f617b`.
Measurements SHA: `36bf474db858daf9ccb6a01f5b13d4980edf1dda904c5d9c7bfa124501eb1aab`.

2593/2593 regression OK in82.134s. All12 cells present; all_quality_parity True;
initial_parent_parity True; update_query_audit_gate True; protected inputs preserved;
tracked tree clean; run_execution_valid True. Publication changed only console log/receipt.
Acceptance uses published evidence and recorded local artifact checks, not reviewer reruns of
user-local artifacts. Full verdict: docs/experiment-ledger-addendum-c228-c229.md.

Ratios below are H1/H2 median update+query time divided by checked-factor/rhs-refresh time:

| Numerical dimension | 1 query/update | 4 queries/update | 16 queries/update |
|---|---:|---:|---:|
| 2 | 2.9389 | 4.0935 | 5.3713 |
| 16 | 2.8493 | 3.4496 | 4.5254 |
| 64 | 2.7944 | 4.1732 | 4.5535 |
| 256 | 1.5900 | 1.9038 | 2.1844 |

Current H1/H2 is slower in every measured cell, about1.59x to5.37x. Including bias-only updates did
not establish speed superiority. Correctness/measurement PASS is not an efficiency PASS.
Three descriptive timing trials, two live factors, matrix-invariant bias changes only; not a general
architecture impossibility result. No matrix-changing, many-factor, natural-language or peak-memory
conclusion. Gate F remains NOT PASSED.

## Accepted chain and remaining boundaries

C213 semantics; C214 numeric closure; C215 H1/H2 commit; C216 Reader; C217 Selector;
C218 structured Writer; C219 Coverage; C220 offline composition; C221 causal dispatch;
C222 withdrawal/hypothesis isolation; C223 explicit-publication request freshness;
C224 replay cost; C225 stateful comparator; C226 dimensions; C227 checked factor reuse;
C228 matrix-invariant update/query cost.

C227 removed C226's large-n query advantage with factor reuse. C228 preserves that unfavorable
result with bias updates. Diagnose implementation cost before proposing an optimization or another
favorable workload. Numerical shrinkage alone is not proof of end-to-end speed or storage benefit.

## Active C229 — function-level cost attribution

Experiment C229-v5f-update-query-function-profile.
Stage V5-F-UPDATE-QUERY-FUNCTION-PROFILE.

One question: which actual functions account for the current candidate update/query work on the
unchanged C228 workload? No production optimization, new data, safety relaxation or training.

Keep the same12 dimension/burst cells,32-event prefix,12 replacements, two live factors and2-port
interface. Rebuild each cell once with profiling off and once on. Four separate cProfile accumulators:
candidate_update, candidate_query, cached_update, cached_query. Initial construction, correctness
oracle, snapshots and exports are outside profile regions. Both paths use accepted implementations.

Record complete function identities, total/primitive calls, self and cumulative times; retain top10
self-time functions per phase for console review. Verify candidate apply12/read12*q and cached
refresh12/query12*q,12 entries per phase, no external profiler overwritten and hook restoration.
Require all current answers/state/provenance within1e-10 and exact final export inventory parity
with accepted C228 in both modes.

Profiler times are perturbed diagnostics, not a new speed benchmark or exact removable overhead.
Do not sum nested cumulative times or subtract an unmeasured constant profiling cost. There is no
required dominant function or improvement percentage. Audit PASS remains separate from efficiency.

Source pins214; protected inputs292; dependencies27; OWN6; artifacts5.
New tests32; modules114; loaded2626 /focused2625 with inherited exact exclusion1.
Manifest: `3f9ce8c054db73843455447d6dc74426be570e50857cc220a3927f8777bd3723`.
Registration: docs/experiment-ledger-addendum-c229-preregistration.md.
Design: docs/v5f-update-query-function-profile-v0.1.md.

## C229 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `0224a865538394a39277ad71c77776f4e162f2c5`.
Scope: committed-source review and targeted authoring execution, not formal science.

All four re-fetched code/test/PowerShell Git blobs matched the tested local copies. After that
comparison30 targeted tests reran:0 failures/errors,0.721s;32 methods enumerated; manifest matched;
both Python files and three embedded runner Python blocks compiled; unbound global references0;
CLI indices precheck[1]/postcheck[1..3]. Actual cProfile/torch callback counts, exception/hook
restoration, external-profiler protection, self/cumulative separation, parent adapter and synthetic
12-cell run/output/postchecks were exercised. Synthetic fixtures are not the accepted full backend.

Source review checked actual parent signatures/fields, profile boundaries, qualified-name count
identities, exact final-export parity paths,27 deciding dependencies,214/292 accounting, complete
launcher guards and C230 non-registration. Git compare shows only new files and the unpinned
handoff; no accepted source, historical test, log or dependency was edited/deleted.
Existing dispatcher parses the selected launcher and the launcher parses its runner before science.

Not executed here: test31 actual parent trajectory/export/profile counts, test32/full2625 historical
regression, Windows PowerShell AST parsing, local parent-artifact precheck or formal C229 profiling.
Clone failed DNS resolution. Review PASS does not claim those execution checks passed. The runner
executes32 own tests,2625 focused tests and only then profiling; failure stops before the next phase
and publishes the console log. After the review HEAD only review documentation changes.

## Historical maintenance and stop

Prior handoff: 68cba193bb1affe648f522f41ce6444f8c39e168:docs/experiment-ledger-and-handoff.md.
Preserve all accepted source pins and tools/run_c167.ps1 historical regression infrastructure.
No cleanup, history rewrite, new CI, Actions-storage work or unrelated architecture change.
Judge C229 before C230. Gate F remains NOT PASSED.
