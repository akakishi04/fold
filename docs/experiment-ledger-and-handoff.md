# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C230 ACCEPTED PASS. C231 ACTIVE / NOT YET JUDGED. C232 NOT REGISTERED.**
C231 is unique ACTIVE. Do not execute until post-authoring review passes.

## Accepted C230 — real improvement, limited adoption

Scientific execution HEAD: `58ec6d1497e4729d394307f5c1316d9e69f2ee8e`.
Published log commit: `ad8a657842491a74d8aa5e3101893aaa98a335ca`.
Log SHA: `de95033043db1b65fd929e7d2cf684e0192b8eda3ae49e74f53d97cf6394e580`.
Summary SHA: `3eeb739eaf37c8b0d1ef4f94d5eec46281ea8721c1cea67fb51234f8bd7fca7c`.
Local summary:
`runs/c230-v5f-prepared-capsule-42695282c3e6402f9fe7616ba3641099/summary.json`.
Validation SHA: `8f0ebfb7c769f1bc9eebceff02d51c55e1a94dd52ee0ec67b73650f2dda683a9`.
Measurements SHA: `d72afb4423933d673983f6ea850e8064c6b84072ae061bbca935c2f2d5705afc`.

Own40 tests OK in1.350s;2665/2665 focused tests OK in52.628s. All12 quality/export/reuse checks,
artifact checks and execution validity passed; preserved inputs and clean tree. Publication added
only console log/receipt. Acceptance is from published evidence and recorded local postchecks.
Full verdict: docs/experiment-ledger-addendum-c230-c231.md.

Prepared/original H1H2 update+query ratios range0.4464-0.6764: about32.4%-55.4% less time on this
fixture. Against full-factor reuse, prepared loses11/12 cells. Only n256/q16 is faster:
19.6411ms versus21.9916ms, about10.7% less stream time. Including setup gives29.6598ms versus
28.3935ms, so that advantage disappears. Three descriptive timing trials, not statistical evidence.

n256/q16 audit storage: prepared283799B, original283277B, full-cache555253B. Prepared adds72 numeric
bytes plus metadata (522B serialized cache). Raw/index/full bridge are retained. These are audit
exports/reachable objects, not whole application size or peak RAM/VRAM.

### Adoption and track decision

Keep prepared_capsule as an opt-in CPU-float64 fixed-W inference candidate. Do not replace the
default/reference implementation or generalize one favorable cell into a universal threshold.
Pause local numeric-memory optimization here and return to language/reasoning evaluation.
Gate F remains NOT PASSED; no requirements are waived and no Gate G promotion is implied.

## Accepted chain and limits

C213 semantics; C214 closure; C215 H1/H2 commit; C216 Reader; C217 Selector; C218 structured Writer;
C219 Coverage; C220 offline composition; C221 causal dispatch; C222 withdrawal/hypothesis isolation;
C223 explicit request freshness; C224-C228 cost comparisons; C229 profiling; C230 optional checked
reduced preparation. These remain small reference/pilot scopes, not general language ability,
concurrency-safe caches, bounded many-factor indexing or whole-system efficiency proof.

## Active C231 — V5-B language evaluation contract

Experiment C231-v5b-byte-evaluation-contract.
Stage V5-B-MODEL-EVALUATION-CONTRACT-AUDIT.

One question: can the existing uncompressed V5-B byte model be evaluated through prefix-only
likelihood and greedy generation without target leakage and with reproducible outputs/checkpoints?
This is a measurement-interface audit, not a new architecture or language-quality benchmark.

Use actual ShortByteLanguageModel from fold_lm/v05/language_task.py, not the separate legacy
FoldLanguageModel or an alleged completed v0.5 stack. It has a causal GRU front-end, fixed routing,
fixed48 slots, width16,2 modules and2 internal steps. New untrained instruments only; no training.
The learned H1/H2 stack and prepared numerical route are not connected by this experiment.

Four authored EN/JA texts (16/22/16/28 UTF-8 bytes), three seeds231001/231002/231003. Model sees only
BOS+observed prefix+prefix-boundary EOS+PAD; target byte stays scorer-only. No special-token targets.
Measure per-byte likelihood, independently verify scoring, compare batch/singleton logits, mutate
unseen suffixes, generate4 own-feedback bytes, serialize/reload and replay. Errors <=1e-9.
Actual126 forwards/seed,378 total;246 scored positions over82 unique fixture bytes; training0.
Random-model scores explicitly marked meaningful_language_score False, with no loss-quality gate.

Preserve C230221 sources/305 protected inputs. Add exact union with OWN6 and five explicitly pinned
language/import source files; reject overlap conflicts, print resolved counts. For union size S,
protected count is305+6+(S-221). All parent/helper and actual LM dependencies are protected.
New tests24; modules116; loaded2690 /focused2689 with inherited exact exclusion1. Output artifacts5.

Manifest: `745c97d3aab18c129494357cc91eb48a6e713294e437b17700be22da8bd3bf83`.
Fixture: `5dcdbd8223c0e40df8d9e3fb5c98e50873a0a014ce9a3c2e003fe74d3911ce23`.
Registration: docs/experiment-ledger-addendum-c231-preregistration.md.
Design: docs/v5b-byte-evaluation-contract-v0.1.md.

## C231 post-authoring review

**post_authoring_review = PENDING**

Initial22 targeted authoring tests passed using synthetic prefix-dependent models and actual
PyTorch scoring/serialization. Not yet executed here: the real V5-B model test, full historical
suite, Windows PowerShell AST, local accepted artifacts or formal instrument run. Do not represent
synthetic tests as those missing checks. Remote committed-source comparison and post-authoring
rerun/review remain mandatory before giving a command.

## Historical maintenance and stop

Prior handoff: ad8a657842491a74d8aa5e3101893aaa98a335ca:docs/experiment-ledger-and-handoff.md.
Preserve every accepted source/test and tools/run_c167.ps1. No cleanup/history rewrite/new CI or
Actions-storage work. Run24 own tests,2689 focused tests, then C231. Judge C231 before C232.
Do not silently adopt a larger training budget or interpret this instrument audit as useful language
performance. Gate F remains NOT PASSED.
