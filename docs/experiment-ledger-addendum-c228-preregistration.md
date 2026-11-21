# C228 preregistration — bias-update/query amortization

**C227 ACCEPTED PASS. C228 ACTIVE / NOT YET JUDGED. C229 NOT REGISTERED.**
Gate E PASSED; Gate F NOT PASSED.

## One scientific question

On the same initial C227 states, what are update-plus-query costs when12 observed beta replacements
are interleaved with1/4/16 queries each, compared with checked full-factor reuse plus rhs refresh?

Changed condition: frozen-state querying becomes a fixed bias-only update stream. The benchmark-local
comparator must correctly rebind the rhs/current state while retaining the checked factor whenever
aggregate W is unchanged. No accepted production code, threshold, weight or historical test changes.

## Parent evidence

Scientific HEAD: `1ada3a45be61e524cf09ff9fa7c6d56efcbf29ee`.
Published log commit: `5adea153611ebe4b6788526ab71fad5b6a0027a9`.
Summary SHA: `4e2a5282f5923b80272afd6476bf2a5ff62a672825cee6d442b0bac4325f9b75`.
Validation SHA: `bbb5ffefd2a0aad3c5e332ba1f50e2a87e15463267129bf657512a044c198d05`.
Measurements SHA: `68234a510756ac5d80a5a1ee770a393ad8dce656a8c395ce8ca73be80b3eac16`.
Local summary:
`runs/c227-v5f-factor-reuse-8abdfa3dfbd141db94ce9afd0e4c171a/summary.json`.

The child validates the accepted parent summary, all202 source pins,268 inherited protected inputs,
all five artifacts and the actual parent row schema/semantics. A dedicated adapter requires ordered
2/16/64/256 measurements passing parent.row_gate. Child run calls that adapter before measurement.

## Fixed data/workload

Dimensions2/16/64/256; two live factors; update/readout rank2; original matrix and six relations.
Original32-event prefix SHA:
`735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`.
Append events33..44 of the same C224 ledger generator. Complete SHA:
`493140c7cbc874c90066da8defe3785a0b667f6c2e2edbdbcc2b55bd5e595f11`.

Queries per update1/4/16;12 updates per trajectory;12 cells. One warm trajectory and three measured
trajectories per cell. Every trajectory starts from the same accepted prefix. Each arm makes
12/48/192 queries per trajectory. Arm order alternates by trial and update.

CPU threads2, deterministic algorithms, float64 numerical path, tolerance1e-10.
No learned model forwards or training.

## Comparator semantics

Do not refactorize merely because evidence changed. The registered replacements have identical W
and changed bias only. The benchmark-local RHSCache retains the inherited checked full factor,
refreshes a finite rhs and rebinds to the new immutable MemoryState after validating W equality and
bridge/cache/guard tensor stamps. Matrix-changing updates are explicitly outside this test.

Candidate apply/commit/read code remains unchanged. Full_reference on each current symbolic state
is used as an untimed independent numerical reference for every query output of both measured arms.
Do not permit old values to count as current correct answers.

## Cost accounting

Both retain complete original evidence, source byte-range index, current state and full shared
bridge. The cached arm additionally counts L, rhs, W equality guard and binding/stamp metadata.
Extra numerical storage must be8*(n*n+n+4) bytes. Base comparator bridge includes its unused compiled
capsule, consistent with the parent; not an independently minimal baseline.

Record common numeric setup and index construction, per-arm initial construction/preparation,
update phases, query phases and export separately. Updates include event parsing, raw/index append,
MemoryOp application and commit or rhs refresh. Stream totals are update+query sums per trajectory.
Cold-inclusive totals add the registered common and per-arm setup phases identically; they are not
whole-application wall clocks. Validation, instrumentation, bookkeeping, initial dictionary copies
and export are excluded from those sums. Export is separately recorded.

Untimed state snapshots and result buffers used by the audit are excluded from logical serving-state
retention estimates. No process-peak RAM/VRAM or native-checkpoint compression claim is made.

## Fixed quality/measurement gate

Require all12 cells present, in dimension/burst order, and:
- both original initial export inventories exactly match accepted C227 for that dimension;
- every update preserves full symbolic-state/provenance parity;
- every individual query matches current full_reference within1e-10;
- same factor object retained over12 rhs refreshes;
- checked preparation trace shows exactly one full Cholesky;
- separate untimed replay of all12 refreshes shows zero refactorizations;
- final candidate query trace remains cholesky2/cholesky_ex2/solve2;
- final cached query trace is cholesky_solve n;
- query state unchanged, complete identical raw/index retention;
- final canonical exports identical across repeats;
- full cache bytes counted; archive members/bytes exact;
- all protected inputs and sources unchanged.

Audit PASS is independent of favorable costs. Unfavorable time/storage results remain unfavorable.
A complete measured parity or trace failure is a scientific FAIL; source/artifact/schema/regression
or incomplete execution is INVALID / RETRY SAME C228. Gate F remains NOT PASSED.

## Authoring registration

OWN6:
- `fold_lm/v05_benchmarks/gate_f_c228_update_query_cost.py`
- `tests_lm/test_v05_c228_update_query_cost.py`
- `tools/run_c228.ps1`
- `tools/invoke_c228.ps1`
- this preregistration
- `docs/v5f-bias-update-query-amortization-v0.1.md`

Source pins208. Protected inputs280 = inherited268 + parent summary/artifacts6 + OWN6.
Direct deciding dependencies26 = previous set25 plus C227 benchmark; all parent/OWN pinned.
Artifacts5: update-plan.json, update-exports.zip, measurements.json, quality-checks.json,
validation-summary.json. Generated data and measurement artifacts remain ignored under runs/.

New tests32; regression modules113; loaded2594 /focused2593. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA:
`bd9e450beebb183dd953928a1e5894bcbd76f33aa25de3bcca27ef05277b1096`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `80715f33b47e8e2bb95d5832124245bd2f1b9cfe`.
Scope: committed-source identity/review and targeted authoring execution, not formal science.

All four code/test/PowerShell files were re-fetched after authoring. Complete remote Git blob IDs
matched the actually executed local copies:
- benchmark: `dffc4778412bcec7e0adff63b78027f93b00a584`;
- tests: `0a9bf9c10bccb77c89e9358b68cb1bb1bfec2737`;
- runner: `2e5ddbece39b08fe92404777c0642136a1b58d78`;
- launcher: `3bf14d5436b16b6a31b2c99c4fa3a7896953428e`.

After comparison,30 targeted tests reran:30 PASS,0 failures,0 errors in0.123 seconds,
Python3.13.5 / PyTorch2.10.0+cpu, threads2.32 methods enumerated. Both Python files and three embedded
runner Python blocks compiled. Manifest/ledger hashes matched; argv indices are precheck[1] and
postcheck[1..3]; no unbound executable c### module alias was introduced.

Real torch rhs-refresh/factor solve versus full solve was exercised at all four dimensions on
synthetic parent-interface fixtures, including unchanged factor identity, old-state rejection,
base/guard mutation rejection, unsupported or matrix-changing updates, and nonfinite rhs rejection.
Synthetic file/row/run fixtures checked ledger identities, cache accounting, repeat/warmup handling,
all12-cell traversal, parent-adapter invocation, archive bytes and output/postcheck ordering.

Independent source review checked actual parent C224/C225/C226/C227 helper signatures and field
meanings, bias-only factor reuse, full current-reference quality comparisons, timing/trace separation,
initial two-arm export parity, shared cold-setup accounting,26 dependencies and208/280 arithmetic,
complete branch/tree/HEAD/ACTIVE/parser guards, and C229 non-registration. Git compare from the
published C227 commit shows only new files plus the unpinned handoff, with no accepted source,
historical test, log or dependency modified/deleted. C227 execution-to-publication comparison
contains only the dedicated latest.log/latest.json additions.

Not executed in the reviewing environment: test31 actual parent trajectory/export anchor,
test32/full2593 historical suite, Windows PowerShell AST parsing, user-local artifact precheck or
formal C228 measurements. Clone failed because github.com DNS did not resolve. Synthetic fixtures
are not represented as accepted-backend or historical-regression execution.

The authoritative runner executes32 own tests, then2593 focused tests, then science. Failed checks
stop before the next phase and the console log is published. Review PASS does not waive these gates.
Only review documentation changes after the review HEAD; scientific conditions remain fixed.

## Stop and interpretation limits

Use invoke_active.ps1 and the final reviewed HEAD. Judge C228 before C229.
No cleanup, history rewrite, new CI, Actions-storage change or unrelated feature.
No matrix-changing workload, many-factor query, answer cache, sparse solver, generalization,
language or Gate F conclusion is implied by this small cost audit.
