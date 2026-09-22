# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C223 ACCEPTED PASS. C224 NOT REGISTERED.**
No experiment is ACTIVE while C224 is authored.

## Accepted C223

Scientific execution HEAD: `cdcc1d4211a149003f44dbdbd18a7e5367c013ab`.
Published log commit: `6e96f798b4c931247f58ab9982b617780d0ee9db`.
Log SHA256: `aff5dbc06d2c85ae54b2181dd2605c09dab66388f758626ce8e3e056bdbe0601`.
Summary SHA256: `1b08cf76a1c233ce849f2b7fe81dbb7fa44120e59a75b32e2f42c4ebccdad2ca`.
Local summary:
`runs/c223-v5f-request-freshness-56cfd6d212764ccf98e7789aa964de52/summary.json`.
Validation SHA: `b52c9d95bb89dca5061d2ccff4aab90276ea5dc4edba2d653b1d9fdc03d12db2`.

2435/2435 focused regression OK. Fresh1296/1296 and parent parity1296/1296;
stale rejection4536/4536 with no exposed result or downstream calls; current repeats81/81;
unguarded replay controls324/324; fingerprints unchanged; training0; model forwards4134.
Protected inputs preserved; run_execution_valid True.
Full verdict: `docs/experiment-ledger-addendum-c223-c224.md`.
Evidence is published console/metadata plus recorded local checks, not a reviewer re-run of local
checkpoint bytes. The checkpoint matrix is not a large independent unseen-task holdout.

## Accepted V5-F chain and limits

C213 MemoryOp/provenance; C214 numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage;
C220 offline composition; C221 causal dispatch; C222 withdrawal/hypothesis isolation;
C223 explicitly published-state request freshness.

All learned components remain tiny structured-input pilots. Native operation-kind selection,
natural language, broad generalization, acquisition, concurrent/cache freshness, bounded indexing
and total-memory-cost superiority remain unestablished. Gate F is not passed.

## Next boundary

C224 proposed question: compare the existing H1/H2 memory reference with full-history replay as
revision history grows, explicitly retaining/counting raw evidence, source lookup index, provenance
and numeric state. This is a cost-attribution measurement, not a new optimizer or Gate F decision.

Do not confuse measurement PASS with storage superiority. Retaining full raw evidence may make the
candidate larger even when warm numeric queries avoid rereading it. State this tradeoff explicitly.
Keep the live factor count small/fixed and report that this does not test many-factor read scaling.

## Historical maintenance and stop

Prior handoff: `6e96f798b4c931247f58ab9982b617780d0ee9db:docs/experiment-ledger-and-handoff.md`.
Preserve accepted source pins and `tools/run_c167.ps1` historical regression infrastructure.
No cleanup, history rewrite, new CI or Actions-storage changes.
C224 stays NOT REGISTERED until its registration/review are complete. Gate F remains NOT PASSED.
