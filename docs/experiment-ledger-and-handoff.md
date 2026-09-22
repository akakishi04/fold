# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C222 ACCEPTED PASS. C223 ACTIVE / NOT YET JUDGED. C224 NOT REGISTERED.**
C223 is the unique ACTIVE experiment. Source review passed; execution preflights remain mandatory.

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

Full verdict: `docs/experiment-ledger-addendum-c222-c223.md`.
Evidence is published console/metadata and recorded local artifact checks, not reviewer-side
re-execution of local checkpoints. One synthetic trajectory per Writer is crossed with81
checkpoint combinations;1296 decisions are not independent unseen tasks.

## Accepted V5-F chain and limits

C213 MemoryOp/provenance; C214 numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage;
C220 offline composition; C221 causal live dispatch; C222 withdrawal/hypothesis isolation.

All learned components remain structured-input pilots. Natural language, learned operation kinds,
broad unseen tasks, retained request/cache freshness, acquisition, bounded indexing and total
memory-cost superiority are not established. Gate F remains NOT PASSED.
C222 used fresh requests; it did not test reuse of old C221 provider closures.

## Active C223 — retained request freshness

Experiment `C223-v5f-retained-request-freshness`.
Stage `V5-F-RETAINED-REQUEST-FRESHNESS`.

One question: do session-owned request leases reject old requests after publication before any
model/provider call, while fresh requests preserve C222 results?

New deterministic module `fold_lm/v05/memory_request_lease.py`; no parent production source changed.
RequestSession binds from current state and rejects other-session or old-generation leases.
Every publication increments generation, including representation-only H1/H2 commit.
No answer cache, training, acquisition, new semantic task or cost optimization.

Same C222 lifecycle and frozen checkpoints. Three sessions,7 publications/session.
Fresh1296: require1296 success and parent Coverage/answer/action/trace/bank-read parity.
Stale4536: all prior alpha/beta requests at all later publications; require STALE_REQUEST,
no exposed result and zero Coverage/Selector/provider/bank/Reader calls.
Same-generation repeats81: a current beta_committed lease must remain reusable.
Unguarded old-request controls324: HOT->COMMIT, committed->REPLACE, replaced->RETRACT,
retracted->END_SCOPE; reproduce old behavior and differ from current behavior intentionally.

Successful calls:
fresh Coverage1296 /Selector/provider/bank/Reader891;
stale all0;
repeat all81;
unguarded replay Coverage324 /Selector/provider/bank/Reader243.
Writer3; total model forwards4134; training0; unchanged fingerprints.

Source pins178; protected inputs220; deciding dependencies19; OWN7; outputs5.
New tests34; modules108; loaded2436 /focused2435; inherited exact exclusion1.
Manifest: `ef0d7db9c3ef24da2076c8811076e53c6d46abeff19b363163a0c352f0d0872d`.
Registration: `docs/experiment-ledger-addendum-c223-preregistration.md`.
Design: `docs/v5f-retained-request-freshness-v0.1.md`.

## C223 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `8ca75e5e47b9d12fdb812dca5d71b5693c9c924c`.
Scope: committed-source audit plus targeted synthetic authoring validation, not formal science.

All five new code/test/PowerShell blob IDs match the executed local copies. The accepted dispatcher
copy also matches its original blob. After remote comparison,32 targeted tests reran successfully
(0 failures/errors,0.284 seconds);34 methods enumerated; manifest matched; new Python and three
embedded runner blocks compiled. The synthetic1296-fresh/4536-stale/81-repeat/324-replay matrix
matched registered counters and rejection controls.

Source review checked owner/generation before dispatch, factory binding to current owned state,
representation-only commit invalidation, expected-label separation, old-closure replay controls,
parent adapter field semantics, helper chains,19 dependencies,178/220 protection accounting,
module/test arithmetic, runner argv[1]/postcheck argv[1..3] and launcher preflight ordering.
Git compare edits no accepted source/test/log/dependency; only new files and unpinned handoff.
Review after this HEAD changes only review documentation, not scientific conditions.

Not run here: the two parent-tree-dependent new tests, actual numeric C222 lifecycle, full2435
historical regression, Windows AST parse and local-only artifact/checkpoint science. No synthetic
result is represented as those checks. The authoritative runner executes all34 own tests first,
then2435 focused tests, then science. Failures stop before the next phase and are logged.

## Limits and historical maintenance

Explicit publication of trusted immutable state is required. In-place tensor mutation, skipped
publication, malicious bypass, concurrent/cross-process use, model-version changes and answer-cache
invalidation are outside scope. This is correctness control, not a security sandbox.
Old snapshots/requests are retained for the test only; no bounded-memory claim.

Prior full state: `ad285c5a318d7ac7b0067e07ffe06fb02edfb8e8:docs/experiment-ledger-and-handoff.md`.
Preserve accepted sources and `tools/run_c167.ps1`. No cleanup, history rewrite, new CI or
Actions-storage work. Actions storage is handled separately.

## Stop condition

Judge C223 before any C224 registration. Complete gate miss: scientific FAIL.
Source/artifact/schema/regression/incomplete-run defects: INVALID / RETRY SAME C223.
Gate F remains NOT PASSED.
