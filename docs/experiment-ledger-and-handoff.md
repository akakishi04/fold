# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C233 ACCEPTED VALID NEGATIVE. C234 ACTIVE / NOT YET JUDGED. C235 NOT REGISTERED.**
C234 is unique ACTIVE. Source review passed; all execution preflights remain mandatory.

## Accepted C233 — no consistent core advantage

Scientific execution HEAD: `fedf6c3e5c163d449d1ad793a87d4fa6952deb1d`.
Published log commit: `519d71abe912639869130cb4dff3f196e166b92f`.
Log SHA: `63e5b22242720deac9b33999cf38b2331ad4069604b866c0801ab6cec0a9a651`.
Summary SHA: `5e9895008ebf02c72c3b5c00a8668f1c8078feef94dd2fc1eff192d41e8709bf`.
Local summary: `runs/c233-v5b-core-ablation-f73f95f4afa44668a64b953f1bbad723/summary.json`.
Validation SHA: `c839db0ed26f0369dcedb6227ae5278ca60904d8636da0d00e49da02d75998e4`.
Comparisons SHA: `7ad45aac3d70cc2a5d8054b4dfcaae36ad169f2434981904e8b657eb053b872c`.
Checkpoint SHA: `0bbe764c832d2fb33b3f51e3838c7178ab7121cf6c2f72a25bda43b2cb0722a3`.

2753/2753 regression OK in53.150s. Three GRU-only models completed400 steps each,1200 total and38400
sampled byte presentations. Parent/full and baseline replay checks, protected inputs, artifact
checks and clean tree passed. run_execution_valid True; baseline_qualified True; all_replays True.
Only log/receipt published. Verdict is from published evidence and recorded local postchecks.

| Seed | Full EN BPB | GRU-only EN | Full JA BPB | GRU-only JA |
|---:|---:|---:|---:|---:|
| 232001 | 0.541317 | 0.491041 | 0.524732 | 0.435336 |
| 232002 | 0.426583 | 0.502808 | 0.551532 | 0.521941 |
| 232003 | 0.479750 | 0.499719 | 0.448819 | 0.469008 |

Full wins3, GRU-only wins3, ties0. Registered full-win gate required6/6; serialized scientific_status
FAIL/core_ablation_gate False is an accepted valid negative, not an execution error. Do not rerun
or soften the gate. Record: docs/experiment-ledger-addendum-c233-c234.md, acceptance commit
`3d3f6ad6f9903085ca083fbfc77bf0d4d77a93d7`.

The smaller ordinary recurrent backbone is competitive on this fixed template task. C232's learning
cannot be attributed uniquely to the core. This is not a statistical equivalence result or proof
that the core is useless on all tasks. Three seeds, four reused held-out pairs, one training recipe
and unequal capacity13488/10160 limit the claim. C232's bounded learning result remains accepted.

## Active C234 — contextual binding, not another template-loss rescue

Experiment C234-v5b-contextual-binding-pilot.
Stage V5-B-CONTEXTUAL-BINDING-PILOT.

One question: can the unchanged full model select the queried object's observed value and change
its answer correctly when the facts or queried object change? Retain GRU-only as a comparator.
No architecture change, learned-memory integration, larger model, external data or C233 gate change.

Examples: box=0;book=3;box= ->0; same facts query book ->3; swap values query box ->3.
English object names box/book/ball/umbrella; Japanese 箱/本/玉/傘; values0/1/2/3.
Only the separate requested answer byte is trained/scored; unconstrained256-way byte output.

576 rows from72 binding groups x2 languages x2 fact orders x2 queried objects. Hold out complete
co-occurring value pairs {0,3}/{1,2}. TRAIN384 rows/48 groups; EVAL192 rows/24 groups. Every individual
object/value pairing appears in TRAIN; all rendering/query variants of a binding stay together.
Per-language EVAL96, balanced digits. First/last-fact baseline50%; constant25%.

Paired normal-input tests require both answers correct when swapping assigned values or queried
object.48 pairs per language of each type, sharing the same96 rows. Also mask observed values or
queried object separately and measure accuracy drops. Masks are out-of-distribution controls,
not independently sufficient evidence of understanding.

Fresh seeds234001/234002/234003. Copy common INITIAL weights before either family trains.
Full13488 /GRU-only10160; CPU float64, threads2; AdamW lr0.005, clip1.0, batch32,400 steps/model,
identical TRAIN sampler seed+1000. Six models/2400 steps/76800 answer presentations. No tuning,
early stop, seed replacement or learned-weight continuation from C232/C233.

Primary full-model gate, every seed/language: exact answer accuracy>=90%, fact-pair>=80%,
query-pair>=80%, evidence-mask drop>=35 percentage points, query-mask drop>=35 percentage points.
Report identical GRU gate independently; no full-versus-GRU superiority requirement/claim.
Check fingerprints, all normal/masked logits replay <=1e-9, exact predicted-byte replay.

Parent244 sources/346 inputs ->250 sources/358 inputs. OWN6, direct dependencies10, artifacts5.
New tests32; modules119; loaded2786/focused2785 with inherited exact exclusion1.
Data SHA: `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`.
Manifest SHA: `0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38`.
Registration: docs/experiment-ledger-addendum-c234-preregistration.md.
Design: docs/v5b-contextual-binding-v0.1.md.

## C234 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `6247f1282600bc3a3b4444f0e51e42c157c8b855`.
Scope: committed-source review plus targeted synthetic authoring execution, not formal science.

All four remote code/test/PowerShell files were re-fetched and their Git blobs matched tested
copies exactly. After comparison30 targeted tests reran:30 PASS,0 failures/errors,1.0841s on
Python3.13.5 / PyTorch2.10.0+cpu / NumPy2.3.5.32 methods enumerated; Python sources and three embedded
runner blocks compiled; unresolved globals0; data/manifest hashes matched. CLI argv precheck[1],
postcheck[1,2,3]; all branch/tree/HEAD/ACTIVE/parser guards precede logging/publication.

Tests used synthetic parent interfaces with real GRU/optimizer layers; full-run fit was simulated.
Grouping, balance, paired controls, masks, TRAIN-only sampling, exact-byte scoring, checkpoint
replay and valid-negative output/postchecks were exercised without held-out quality tuning.
Source review checked accepted-negative parent semantics, helper/model factories,250/358 protection
and ten dependencies. Git comparison changes only new acceptance/C234 files and this unpinned
handoff; accepted sources/tests/logs are untouched. Only review documents change after review HEAD.

Not run here: test31 actual parent/model TRAIN-only smoke, test32/full2785 historical suite,
Windows PowerShell AST, user-local accepted artifacts or formal2400-step training. Container DNS
cannot resolve raw.githubusercontent.com and pwsh is absent; connector source reads succeed.
Pending checks are not represented as already passed. The authoritative runner requires32 own
tests and2785 focused tests before science; defects stop execution and publish console evidence.

## Numeric-memory track and stop

C230 prepared route remains optional; local numeric-memory tuning stays paused. Gate F is open,
not waived. Preserve all accepted sources/tests and tools/run_c167.ps1. No cleanup/history rewrite,
new CI, paid API, external corpus or Actions-storage changes.

Prior handoff:519d71abe912639869130cb4dff3f196e166b92f:docs/experiment-ledger-and-handoff.md.
Judge C234 before C235 registration. A complete finite ability miss is a valid negative; source,
artifact, schema, nonfinite or replay failure is INVALID / RETRY SAME C234. Gate F NOT PASSED.
