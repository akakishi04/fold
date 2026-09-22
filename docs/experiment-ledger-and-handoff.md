# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C224 ACCEPTED PASS. C225 ACTIVE / NOT YET JUDGED. C226 NOT REGISTERED.**
C225 is unique ACTIVE. Post-authoring review is pending; do not execute yet.

## Accepted C224 — measurement audit, not storage superiority

Scientific execution HEAD: `41ca548ed065b3e6dedd50dbc42ebb1b8df5f512`.
Published log commit: `134d96995e77df0bcdd25fc046ad2b205a5c3644`.
Log SHA256: `85c1aaabd0a9d7248cf0a563fd8741a27e2dca6bc7c8a4992b37e94aefcda15d`.
Summary SHA256: `d47f17ed6a467e5203f3bf5e39e5d023cfa469320f4636ca05d13d0673b09f88`.
Local summary:
`runs/c224-v5f-history-cost-audit-7d510ad2c98647bfbabeabe91de81381/summary.json`.
Validation SHA: `5be4146f3139b761837bcbe0cad25db02c46035351e3d76b1a75a1ebd00211f2`.
Measurements SHA: `2e09353e3899f45bb2ee3598a61e72e1602858ae446a43de306abd07acbb832a`.

Regression2465/2465 OK; all four quality-parity checks passed; run_execution_valid True;
protected inputs and tracked tree preserved. Audit accepted from published evidence plus recorded
local artifact checks, not reviewer-side re-execution of the user's files.

| History events | Candidate export bytes | Replay export bytes | Candidate query median ms | Replay query median ms |
|---|---:|---:|---:|---:|
| 8 | 5743 | 4285 | 0.3086 | 0.3069 |
| 32 | 11181 | 9044 | 0.5951 | 1.2293 |
| 128 | 33100 | 28113 | 0.5490 | 3.1948 |
| 512 | 121183 | 104657 | 0.6936 | 8.6449 |

Storage deltas+1458/+2137/+4987/+16526 bytes: no measured storage superiority.
Candidate warm raw rereads0; replay1579/6338/25407/101951 bytes per query.
Timing is descriptive (three measured trials), canonical exports are not native checkpoint sizes,
and reachable-data estimates are not process RAM/VRAM peaks. Two live factors only.

Full verdict and caveats: `docs/experiment-ledger-addendum-c224-c225.md`.
Avoided replay is not yet a capsule-specific benefit: a plain current state can avoid replay too.

## Accepted V5-F chain and limits

C213 semantics; C214 numeric closure; C215 H1/H2 commit; C216 Reader; C217 Selector;
C218 structured Writer; C219 Coverage; C220 offline composition; C221 live dispatch;
C222 withdrawal/hypothesis isolation; C223 explicit-publication request freshness;
C224 raw-retaining history-cost audit.

No broad natural-language/generalization, learned operation kind, acquisition, concurrent/cache
freshness, bounded many-factor indexing or total memory-cost superiority is established.
Gate F remains NOT PASSED.

## Active C225 — stateful baseline attribution

Experiment `C225-v5f-stateful-baseline-attribution`.
Stage `V5-F-STATEFUL-BASELINE-ATTRIBUTION`.

One question: what does the current H1/H2 representation add beyond ordinary incrementally retained
MemoryState when raw history, source index and numeric bridge are held equal?

Keep the C224 H1/H2 candidate unchanged. New baseline updates plain MemoryState once per event,
retains it and uses full_reference(state) per query without raw replay. Both retain identical raw and
index bytes and the same complete bridge. Common bridge overhead includes its unused compiled
capsule on the symbolic arm; do not claim an independently minimized baseline.

History sizes8/32/128/512; two live factors; same raw hashes; float64 tolerance1e-10;
one warmup+three measured queries per arm/size; alternating query order. Record construction,
index/export costs and descriptive timings separately. No production change, optimization,
new semantic task, inference/training or data deletion.

Require full symbolic/provenance and numeric parity, unchanged states, exact archive/export
accounting and zero warm raw rereads for both arms. H1/H2 candidate export inventories must match
accepted C224 bytes. Cost superiority is measured separately and is not an audit PASS requirement.

Source pins190; protected inputs244; direct dependencies23; OWN6; artifacts5.
New tests32; modules110; loaded2498 /focused2497 with the same exact historical exclusion1.
Manifest: `0520afee3c0b25ca1da8f28be3534115d72b1abbe4252628312fd2d321b24e66`.
Registration: `docs/experiment-ledger-addendum-c225-preregistration.md`.
Design: `docs/v5f-stateful-baseline-attribution-v0.1.md`.

## C225 post-authoring review

**post_authoring_review = PENDING**

Author-side30 targeted tests passed on synthetic fixtures;32 methods enumerate. Actual parent
numeric-backend test, full2497 historical regression, Windows AST parsing and local artifact/C225
science have not run here. Re-fetch committed files and compare tested copies before review PASS.
The authoritative runner executes all32 new tests, then2497 focused tests, then the comparison.

## Historical maintenance and stop

Previous full state: `134d96995e77df0bcdd25fc046ad2b205a5c3644:docs/experiment-ledger-and-handoff.md`.
Preserve all accepted sources and `tools/run_c167.ps1` historical regression infrastructure.
No cleanup, history rewrite, new CI, unrelated architecture changes or Actions-storage work.
Judge C225 before C226. Gate F remains NOT PASSED.
