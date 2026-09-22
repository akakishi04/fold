# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C227 ACCEPTED PASS. C228 ACTIVE / NOT YET JUDGED. C229 NOT REGISTERED.**
C228 is unique ACTIVE. Source review passed; all execution preflights remain mandatory.

## Accepted C227 — audit PASS, no query-speed advantage

Scientific execution HEAD: `1ada3a45be61e524cf09ff9fa7c6d56efcbf29ee`.
Published log commit: `5adea153611ebe4b6788526ab71fad5b6a0027a9`.
Log SHA: `2fdc52f6f483830d85db0b0e1908d8d157067daab94142d8c0779c5248a2a24b`.
Summary SHA: `4e2a5282f5923b80272afd6476bf2a5ff62a672825cee6d442b0bac4325f9b75`.
Local summary:
`runs/c227-v5f-factor-reuse-8abdfa3dfbd141db94ce9afd0e4c171a/summary.json`.
Validation SHA: `bbb5ffefd2a0aad3c5e332ba1f50e2a87e15463267129bf657512a044c198d05`.
Measurements SHA: `68234a510756ac5d80a5a1ee770a393ad8dce656a8c395ce8ca73be80b3eac16`.

2561/2561 regression OK; all numerical/state/provenance parity checks passed;
original C226 export inventories unchanged; cached query refactorizations0 at all dimensions;
factor_reuse_audit_gate True; protected inputs/clean tree preserved; run_execution_valid True.
Acceptance uses published evidence and recorded local artifact checks, not reviewer reruns of
user-local artifacts. Full verdict: docs/experiment-ledger-addendum-c227-c228.md.

| Numerical variables | H1/H2 query ms | Factor reuse query ms | H1/H2 / reuse |
|---|---:|---:|---:|
| 2 | 0.3373 | 0.0514 | 6.5623 |
| 16 | 0.4504 | 0.0999 | 4.5085 |
| 64 | 0.4641 | 0.0921 | 5.0391 |
| 256 | 0.5179 | 0.2249 | 2.3028 |

The stronger frozen-state comparator is faster at every measured size. C226's large-n crossover
against repeated dense factorization did not survive factor reuse. No current query-speed advantage
is established. H1/H2 uses fewer exported bytes than this particular cached comparator at n256:
280561 vs552365; however it remains larger than the uncached stateful comparator. Cache factor/rhs
retention is48/2176/33280/526336 additional numerical bytes. Time/retention trade-off, not a general win.

Three descriptive timing trials, two live factors, fixed queries and shared full bridge only.
Answer caching, specialized sparse solvers and minimized baselines are not compared.

## Accepted chain and limits

C213 semantics; C214 numerical closure; C215 H1/H2 commit; C216 Reader; C217 Selector;
C218 structured Writer; C219 Coverage; C220 offline composition; C221 causal dispatch;
C222 withdrawal/hypothesis isolation; C223 explicit-publication request freshness;
C224 replay-cost audit; C225 stateful comparator; C226 numerical dimensions; C227 factor reuse.

No general language/reasoning performance, native operation selection, acquisition, concurrent
freshness, bounded many-factor indexing or overall time/storage superiority has been established.
Gate F remains NOT PASSED. Do not equate an audit PASS with a favorable efficiency result.

## Active C228 — bias-update/query amortization

Experiment C228-v5f-bias-update-query-amortization.
Stage V5-F-BIAS-UPDATE-QUERY-AMORTIZATION.

One question: how do update-plus-query costs compare when12 observed beta replacements are
interleaved with1/4/16 queries on the same initial C227 states?

Keep dimensions2/16/64/256, original32-event prefix, two live factors, rank/readout2 and matrix family.
Append events33..44 of the same C224 generator. These change bias, not aggregate W. The comparator
must be allowed to retain its checked full factor while refreshing rhs/state binding after explicit
W-equality and tensor-stamp validation. Do not weaken it by forcing unnecessary refactorization.
No accepted production code, safety check, learned checkpoint or historical test changes.

Twelve cells. One warm trajectory plus three measured trajectories per cell. Validate every query
against untimed current full_reference, plus complete state/provenance parity after every update.
Original candidate/symbolic initial exports must match C227 bytes for all dimensions. Separately
trace checked preparation, replay all12 rhs refreshes with zero refactorizations, and final queries.

Record common bank/index setup, per-arm initial construction, update and query phases, and export.
Stream totals are update+query; cold-inclusive totals add registered common/per-arm setup phases,
not whole-application elapsed time. Original raw/index/full bridge and all factor/rhs/W-guard cache
bytes are counted. Reachable-state estimates exclude audit-only snapshots; no process peak claim.
Three-trial timings remain descriptive. Audit PASS does not require faster/smaller H1/H2.
No training, matrix-changing workloads, answer caching, acquisition or Gate F decision.

Source pins208; protected inputs280; deciding dependencies26; OWN6; artifacts5.
New tests32; modules113; loaded2594 /focused2593 with inherited exact exclusion1.
Full44-event ledger SHA: `493140c7cbc874c90066da8defe3785a0b667f6c2e2edbdbcc2b55bd5e595f11`.
Manifest: `bd9e450beebb183dd953928a1e5894bcbd76f33aa25de3bcca27ef05277b1096`.
Registration: docs/experiment-ledger-addendum-c228-preregistration.md.
Design: docs/v5f-bias-update-query-amortization-v0.1.md.

## C228 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `80715f33b47e8e2bb95d5832124245bd2f1b9cfe`.
Scope: committed-source review and targeted authoring execution, not formal science.

All four re-fetched remote code/test/PowerShell blob IDs matched the executed local copies. After
comparison,30 targeted tests reran:0 failures/errors,0.123 seconds.32 methods enumerated; manifest
and ledger hashes matched; both Python files and three embedded runner Python blocks compiled;
argv indices precheck[1]/postcheck[1..3]; no unbound executable c### alias.

Actual torch rhs-refresh/factor solve versus full solve was checked at all dimensions on synthetic
parent-interface fixtures. Factor identity, mutation/capability/matrix-change/nonfinite rejection,
raw/index hashes, cache accounting and synthetic12-cell run adapter/export/postchecks passed.
Source review verified actual parent helper/signature/field meanings, matrix-invariant reuse,
timing/trace separation, initial export parity, shared cold-setup accounting,26 dependencies,
208/280 arithmetic, launcher guards and C229 non-registration. Git compare shows only new files
and the unpinned handoff, without accepted source/test/log/dependency edits or deletions.

Not executed here: test31 actual parent trajectory/export anchor, test32/full2593 historical suite,
Windows PowerShell AST parse, user-local artifact precheck or formal C228 measurements. Clone failed
DNS resolution. Synthetic fixtures are not represented as those checks. The authoritative runner
executes32 own tests,2593 focused tests, then science; failure stops before the next phase and logs
are published. Review PASS does not waive execution checks. Only review documentation changes after
the review HEAD; scientific conditions remain fixed.

## Historical maintenance and stop

Prior handoff: 5adea153611ebe4b6788526ab71fad5b6a0027a9:docs/experiment-ledger-and-handoff.md.
Preserve all accepted source pins and tools/run_c167.ps1 historical regression infrastructure.
No cleanup, history rewrite, new CI, Actions-storage work or unrelated architecture changes.
Judge C228 before C229. Gate F remains NOT PASSED.
