# C225 preregistration — stateful baseline attribution

**C224 ACCEPTED PASS. C225 ACTIVE / NOT YET JUDGED. C226 NOT REGISTERED.**
Gate E PASSED; Gate F NOT PASSED.

## One scientific question

What cost remains for the current H1/H2 representation when it is compared with ordinary retained
incremental MemoryState rather than a baseline that replays the entire history on every query?

Change only the comparator. Keep the accepted H1/H2 path, raw evidence, source-index bytes, shared
numeric bridge, two live factors, history sizes and numerical precision fixed.
No production changes, optimization, neural inference/training, raw deletion or cleanup.

## Parent identity

Scientific HEAD: `41ca548ed065b3e6dedd50dbc42ebb1b8df5f512`.
Log commit: `134d96995e77df0bcdd25fc046ad2b205a5c3644`.
Summary SHA256: `d47f17ed6a467e5203f3bf5e39e5d023cfa469320f4636ca05d13d0673b09f88`.
Validation SHA256: `5be4146f3139b761837bcbe0cad25db02c46035351e3d76b1a75a1ebd00211f2`.
Measurements SHA256: `2e09353e3899f45bb2ee3598a61e72e1602858ae446a43de306abd07acbb832a`.
Local summary:
`runs/c224-v5f-history-cost-audit-7d510ad2c98647bfbabeabe91de81381/summary.json`.

Validate all184 parent source blobs,232 protected inputs and all five parent output artifacts.
Use the actual measurements schema through an adapter requiring four ordered history sizes,
registered raw identities and the parent's measurement gate. The candidate export inventory must
match the accepted C224 candidate byte-for-byte at each size; timings are not frozen outcomes.

## Fixed data and arms

History sizes:8,32,128,512; live factors2; same fixed alpha and cyclic beta replacement ledgers.

Raw SHA256 in order:
- `c940705b4253e319dce5e0e178fe262be6a1c613669b4b93eb72359136023357`
- `735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`
- `01e5c6e53a31c92b9d1fe8411b7fdbbd60d3fb709177c8d8d87ca4c95250cf4f`
- `e4c0e12499275f7925d3648eb16d7d8b3f25e0769a6bd7603ff4fc656b3b7999`

Candidate uses C224 build_candidate/query_candidate unchanged.
Symbolic baseline applies each event once using accepted MemoryState/apply_memory_op, retains the
current state, and queries it with the existing full_reference solve. It never rebuilds current
state from raw evidence on a query.

Both arms retain identical raw/index byte sequences. The complete numeric bridge is shared in scope,
including its unused compiled capsule on the full-solve arm. No common overhead is silently removed.
This is not a claim of an independently minimized baseline implementation.

## Measurement and fixed gate

One warmup + three measured queries per arm/size; alternate arm order. Float64 numeric error<=1e-10.
CPU torch threads2, deterministic algorithms. Construction and index/export costs recorded separately.
No speed threshold, no storage-superiority threshold, no hyperparameter selection.

For every history size require:
- original raw identity and two live factors in both arms;
- complete symbolic state equality, including revision and provenance;
- all measured/warmup responses SUPPORTED and numerically equal within tolerance;
- unchanged retained states after queries;
- identical raw/index exports and valid current-record source references;
- exact complete export inventories and verified archive member bytes;
- one N-event raw traversal per arm for construction;
- zero raw bytes/events traversed in every warm query in both arms.

Report candidate-minus-symbolic storage deltas and candidate/symbolic median query ratios. An audit
PASS with higher storage/latency is not an efficiency win. Timings use three trials and are descriptive.

## Cost interpretation

Retained export: uncompressed canonical JSON plus original raw bytes, not native checkpoint format.
Reachable Python/CPU-tensor data estimate is labeled separately from process RAM/VRAM peaks, which
remain unmeasured. Both arms include source-index storage; the index remains a benchmark sidecar.
This is two-live-factor/two-dimensional numeric comparison, not many-factor/large-system scaling.

Complete correctness/accounting gate miss = scientific FAIL.
Source/artifact/schema/regression/incomplete-run defects = INVALID / RETRY SAME C225.
Gate F remains NOT PASSED.

## Registration

OWN6:
- `fold_lm/v05_benchmarks/gate_f_c225_stateful_baseline.py`
- `tests_lm/test_v05_c225_stateful_baseline.py`
- `tools/run_c225.ps1`
- `tools/invoke_c225.ps1`
- this preregistration
- `docs/v5f-stateful-baseline-attribution-v0.1.md`

Source pins190 =184+6. Protected inputs244 =232+6 parent summary/artifacts+6 OWN.
Deciding dependencies23 = C224's22 plus the C224 benchmark. No accepted file is edited or removed.
Outputs5: comparison-plan.json, stateful-exports.zip, measurements.json, quality-checks.json,
validation-summary.json. Generated data stays under ignored runs/. Console log includes measurements.

New tests32; modules110; loaded2498 /focused2497. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA256:
`0520afee3c0b25ca1da8f28be3534115d72b1abbe4252628312fd2d321b24e66`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `6593e37f06a816d3154c8dd54b25fa12b869926d`.
Scope: committed-source review plus targeted synthetic authoring execution, not formal science.

All four committed code/test/PowerShell files were re-fetched. Git blob hashes matched the executed
local authoring copies exactly:
- benchmark: `02c0c82ba00207c5b9a3ffd27f80bbfbfa79f4de`;
- tests: `2ab366f351d421a2f4baa9777b5151351eeec6de`;
- runner: `fc1ffdcd62e0d526bd84ffc279dca2b838937f5e`;
- launcher: `1f874faeecb4e33104deda5f8542e16c65508583`.

After comparison,30 targeted tests reran:30 PASS,0 failures/errors,0.057 seconds on Python3.13.5,
PyTorch2.10.0+cpu and NumPy2.3.5.32 test methods enumerate. Manifest self-hash and all four original
raw hashes matched; new Python and three embedded runner blocks compiled; unbound c### aliases0.

The tests use explicit synthetic memory/cost helpers. They exercise all four sizes, ordinary state
retention, direct full-reference call dispatch, matched raw/index bytes, source/provenance/accounting,
archive-member byte readback, adapter failures and unfavorable-cost acceptance. They are not a
substitute for running the accepted numeric backend.

Remote source review checked actual parent measurements field meanings and generation semantics,
the candidate's unchanged export construction, baseline no-replay query inputs, shared bridge
accounting caveat, all23 deciding dependencies,190/244 protection arithmetic, run-path parent adapter
and archive checks, exact CLI argv[1]/postcheck[1..3], full launcher/early-test ordering and C226
non-registration. Git comparison from the C224 published log to this review HEAD shows only new
C225/acceptance files and the unpinned handoff; no accepted source/test/log/dependency edits/removals.

Not run here: test31 against the actual accepted numeric backend, test32/full2497 historical
regression, Windows PowerShell AST parsing, local parent-artifact precheck or C225 science.
Repository clone was attempted and failed DNS resolution. No synthetic helper result is represented
as accepted-backend or user-artifact execution. The authoritative runner executes all32 new tests,
then2497 historical tests, then comparison; failed preflights stop before the next phase.
After the review HEAD only review documentation changes; scientific conditions remain fixed.

## Stop

Use the active dispatcher with the reviewed final HEAD. Judge C225 before C226 registration.
No Actions-storage work, history rewrite, cleanup, new CI or unrelated architecture changes.
