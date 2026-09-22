# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C222 ACCEPTED PASS. C223 NOT REGISTERED.**
No C experiment is ACTIVE during next-experiment authoring.

## Accepted C222

Scientific execution HEAD: `ae4286ac9b79cd34eb8bdfd1d72ae2e27c308889`.
Published log commit: `ad285c5a318d7ac7b0067e07ffe06fb02edfb8e8`.
Log SHA256: `a0c24da2aebbab381a9325457bc12f7c6fd2046c36f9fdc32a5fd6fc7391fb5c`.
Summary SHA256: `18321ace4ade112fe227d4836867223a5ec609761c89015b704e9e14b629c62e`.
Local summary:
`runs/c222-v5f-withdrawal-lifecycle-60ba479f7d2b46ff957b5d2a21bf865c/summary.json`.

2401/2401 regression OK; main1296/1296; controls162/162; alpha anchor648/648;
suppression405/405; beta answers after withdrawal0; suppressed downstream calls0;
lifecycle/provenance/export audits3/3; fingerprints unchanged; training0; forwards3405.
Protected inputs preserved; run_execution_valid True.

Full verdict/artifact identities: `docs/experiment-ledger-addendum-c222-c223.md`.
Evidence is published console/metadata and recorded local artifact checks, not reviewer-side
re-execution of local checkpoints. One continuing synthetic trajectory per Writer is crossed with
81 checkpoint combinations;1296 decisions are not independent unseen tasks.

## Accepted V5-F chain and limits

C213 MemoryOp/provenance; C214 numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage;
C220 offline composition; C221 causal live dispatch; C222 withdrawal/hypothesis isolation.

All learned components remain structured-input pilots. Not established: natural language,
learned operation kinds, broad unseen tasks, retained old-request/cache freshness, acquisition,
bounded indexing or total memory-cost superiority. Gate F remains NOT PASSED.

C222 uses fresh requests made from current state. It does not test reuse of the older closures
created by C221 request_for(). This freshness boundary is the next single intervention.

## Next boundary

C223 proposed: session-owned request leases that reject retained requests after state publication,
before Coverage/Selector/provider/Reader invocation. Keep C222 lifecycle and all learned checkpoints
fixed. Verify fresh-result parity, old-request rejection, representation-only commit invalidation,
and explicit unguarded replay controls. No answer cache, training, acquisition or cost claim.

## Historical evidence and maintenance

Prior full state:
`ad285c5a318d7ac7b0067e07ffe06fb02edfb8e8:docs/experiment-ledger-and-handoff.md`.
Gate E decisive log: `docs/experiment-run-logs/c212/latest.log`.
Preserve accepted sources and `tools/run_c167.ps1` historical regression infrastructure.
No cleanup, history rewrite, new CI or Actions-storage work. Actions storage is handled separately.

## Stop condition

C223 remains NOT REGISTERED until authoring and committed-source review complete.
Gate F remains NOT PASSED.
