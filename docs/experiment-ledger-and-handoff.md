# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C223 ACCEPTED PASS. C224 ACTIVE / NOT YET JUDGED. C225 NOT REGISTERED.**
C224 is unique ACTIVE. Source review passed; all execution preflights remain mandatory.

## Accepted C223

Scientific execution HEAD: `cdcc1d4211a149003f44dbdbd18a7e5367c013ab`.
Published log commit: `6e96f798b4c931247f58ab9982b617780d0ee9db`.
Log SHA256: `aff5dbc06d2c85ae54b2181dd2605c09dab66388f758626ce8e3e056bdbe0601`.
Summary SHA256: `1b08cf76a1c233ce849f2b7fe81dbb7fa44120e59a75b32e2f42c4ebccdad2ca`.
Local summary:
`runs/c223-v5f-request-freshness-56cfd6d212764ccf98e7789aa964de52/summary.json`.
Validation SHA: `b52c9d95bb89dca5061d2ccff4aab90276ea5dc4edba2d653b1d9fdc03d12db2`.

2435/2435 regression OK; fresh1296/1296 and exact parent parity1296/1296;
stale rejection4536/4536, no exposed result or downstream calls; current repeats81/81;
unguarded replay controls324/324; fingerprints unchanged; training0; model forwards4134.
Protected inputs preserved; run_execution_valid True.
Full verdict: `docs/experiment-ledger-addendum-c223-c224.md`.
Evidence is published console/metadata plus local recorded artifact checks, not reviewer-side
re-execution of user checkpoint bytes. The matrix is not thousands of independent unseen tasks.

## Accepted V5-F chain and limits

C213 MemoryOp/provenance; C214 numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage;
C220 offline composition; C221 causal dispatch; C222 withdrawal/hypothesis isolation;
C223 explicitly published-state request freshness.

Tiny structured-input pilots only. Natural language, native operation selection, broad generalization,
acquisition, concurrent/cache freshness, bounded indexing and total-cost superiority remain open.
Gate F is not passed.

## Active C224 — raw-retaining history cost audit

Experiment `C224-v5f-raw-retaining-history-cost-audit`.
Stage `V5-F-RAW-RETAINING-HISTORY-COST-AUDIT`.

One question: as revision history grows with two live factors, what are the actual retained
memory-backend bytes and warm raw-reread costs of the existing H1/H2 reference versus full-history
replay when raw evidence, source index, provenance and complete numeric state are counted?

No production source change, model inference/training, compression optimization or cleanup.
History sizes8/32/128/512, fixed alpha anchor and cyclic beta REPLACE. Both arms keep identical full
raw UTF-8 evidence. Candidate retains current bank/state and a fully costed benchmark source-index
sidecar. Baseline keeps raw history plus the same bridge, replaying into a fresh state every query.

One warmup+three measured queries per size/arm. Require complete final symbolic/provenance parity,
SUPPORTED numeric max-abs error<=1e-10, unchanged query state, exact raw/index/export inventories,
candidate warm raw-rereads0 and baseline full N-event/raw-byte reread every measured query.

Report uncompressed canonical export totals and component file bytes, a separately labeled reachable
Python/CPU tensor data-memory estimate, construction/index costs and descriptive query timing.
Native checkpoint format, allocator/process peaks and neural-model RAM are not measured. Do not
present canonical export or reachable-data estimates as total application memory.

**Audit PASS is not storage superiority.** Candidate storage may be larger because it retains raw
history plus extra state/index. Report storage deltas and avoided reread work separately.
This is not many-live-factor scaling or Gate F completion.

Source pins184; protected inputs232; dependencies22; OWN6; outputs5.
New tests30; modules109; loaded2466 /focused2465 with inherited exact exclusion1.
Manifest: `0097887642e62a0c2e332d6b68a6dbcb769e829a1970387c3e0aa4ad28343103`.
Registration: `docs/experiment-ledger-addendum-c224-preregistration.md`.
Design: `docs/v5f-history-cost-audit-v0.1.md`.

## C224 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `a8e0eeb370d37d367defeca967a4bc33b418029d`.
Scope: committed-source audit plus targeted synthetic-backend authoring validation, not science.

All four code/test/PowerShell remote blob IDs match the tested copies. After comparison,28 targeted
tests reran (0 failures/errors,0.079 seconds);30 methods enumerated; manifest self-hash matched;
Python and three embedded runner blocks compiled; unbound executable c### aliases0.
Synthetic measurements covered all four history lengths and raw/index/provenance/file-inventory/
replay-count controls. Higher candidate storage is explicitly permitted by measurement PASS.

Source review checked actual symbolic replay/full-reference contracts, candidate no-raw query path,
complete bank/state export, source byte-range index, archive readback, parent helper/field meanings,
22 dependency membership,184/232 accounting, CLI argv[1]/postcheck[1..3], early own-test ordering
and launcher guards. Git compare shows no accepted source/test/log/dependency change or deletion.
After the review HEAD only review documentation changes; scientific conditions remain fixed.

Not executed here: the accepted numeric-backend new test, full historical2465 regression test,
Windows PowerShell AST parse and local parent-artifact/C224 science. No mock-backend results are
represented as those checks. The real runner executes all30 own tests, then2465 focused tests,
then the cost audit. Failure stops before the next phase and the console log is published.

## Historical maintenance and stop

Prior state: `6e96f798b4c931247f58ab9982b617780d0ee9db:docs/experiment-ledger-and-handoff.md`.
Preserve accepted sources and `tools/run_c167.ps1` historical regression infrastructure.
No history rewrite, cleanup, new CI or Actions-storage work.
Judge C224 before C225. Gate F remains NOT PASSED.
