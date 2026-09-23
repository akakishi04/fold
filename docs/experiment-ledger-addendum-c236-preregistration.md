# C236 preregistration — minimal TRAIN binding learnability

Experiment: C236-v5b-minimal-binding-learnability.
Stage: V5-B-MINIMAL-BINDING-LEARNABILITY.
C235 ACCEPTED PASS (diagnostic integrity only); C234 ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED. C237 is NOT REGISTERED.
C236 is registered by this document. Execution readiness and the unique ACTIVE experiment are
controlled only by the current authoritative handoff after independent post-authoring review.

## One scientific question

Can the unchanged C234 architectures and fixed400-step training recipe fit a balanced minimal
16-row object/value binding set drawn entirely from the accepted C234 TRAIN split?
This addresses failure already present on TRAIN in C235 before enlarging the model or training
budget. It is a new limited TRAIN-fit question, not a rerun/rescue of C234 or a generalization gate.

## Accepted evidence and parent contracts

Acceptance base: `4e7c83ae5948ac1ee403b61f018b334f170f32c4`.
C235 acceptance record: docs/experiment-ledger-addendum-c235-c236.md.
Acceptance record commit: `dc0b43a197bfa9061bd2454099e41111cc4dd17c`.

C235 scientific execution HEAD: `fc3311955c3dcda87b67c2ee8dd58a59fb256d6f`.
Published log commit: `71dd1bb48978a1bd0a6b71448f1ceb29011696c4`.
Log SHA256: `fb2811d896606c07bd3d6cbd28a036d30f905dfce0295ade1fde582cde14b40a`.
Summary SHA256: `a9d6daa76bab38488ec3634d186ba81a2d61ae878df80202f3084057e917b1b5`.
Local summary: `runs/c235-v5b-frozen-binding-diagnostic-17d75b38b35249a297bde78cee0f1d43/summary.json`.
The accepted diagnostic must have status PASS and diagnosis_counts exactly TRAIN_ACCURACY_BELOW_90:12.

C235 artifacts, required byte-identical:
- diagnostic-plan.json: 2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3
- diagnostics.json: a93f73fb6cb17d9a3a8067f8a4d522cafe68acad56d02200ce95de521f5a989c
- model-fingerprints.json: 28c26fa0d6ecf84db469b6ee3a945bd956489802cd4795d39b3a28c15fd7d71c
- predictions.json: 10f477d42f1b53a250c34e77616a81f17f3e92e008f9ae1619fe572a055c44d3
- validation-summary.json: 30ac8dcbe92b826e9d2f69384204ade6e6fb9fb6e07b660713325c9640385023

The already-protected C234 summary is also required:
`runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/summary.json`, SHA256
`a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`.
C234 dataset and measurements are already included in accepted C235 protected inputs. Production
loads dataset.json through C234.validate_dataset and measurements.json through
C235.validate_parent_records. initial_sha256 is the fingerprint before C234 training, as confirmed
from C234's writer; final_sha256 is NOT used as initialization. No trained parent state is loaded.

## Cohort and data identity

Parent dataset SHA256: `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`.
Select C234 TRAIN rows with objects == [0,1] and sorted(values) == [0,1], preserving original order.
Selected16-row canonical JSON SHA256:
`bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c`.

Two assignments x two fact orders x two queried objects x two languages =16 TRAIN rows.
English8/Japanese8; each target digit0/1 occurs8 times overall. Four fact pairs and four query pairs
per language. No EVAL row enters training, and no held-out rows are evaluated by C236.
The row restriction is defined without examining C236 results; no favorable row/seed selection.

## Changed and fixed

Scientific intervention: restrict training cohort from384 to16 existing rows.
Measurement window: initial/final/reloaded evaluation on those16 seen TRAIN rows, using all three
existing views. This is a changed TRAIN-fit endpoint, not a claimed controlled EVAL improvement.

Fixed: Full13488 parameters / GRU-only10160; width16;48 slots; same byte vocabulary, renderer,
answer-only cross-entropy, unconstrained256-byte argmax, architecture and common-backbone weights.
Seeds234001,234002,234003; models ordered seed/full then seed/gru_only. Reuse the seed identities to
hold initial conditions fixed, but construct fresh models. Check every initial fingerprint against
C234's saved pre-training fingerprint. Construct the independent common-weight GRU copy before
either paired model is trained. There is no continued learning from C234's trained checkpoints.

AdamW lr0.005, betas(0.9,0.999), eps1e-8, weight_decay0, clip norm1.0, batch32,400 steps/model.
CPU sampling with replacement, generator seed+1000. The new fit function must be executable-AST
identical to C234.fit except for the progress tag; constants must match as well.
CPU float64, threads2, deterministic algorithms. No early stop, best-checkpoint selection,
replacement seed, steps extension, extra data, architecture change or production runtime change.

## Fixed workload and gates

Six newly trained models x400 steps =2400 training steps /76800 answer presentations.
Each model has3 initial +3 final +3 checkpoint-replay forwards on16 rows.
Evaluation/replay:54 forwards /864 row presentations.
Total scientific model forwards2454; total row presentations77664.
One new checkpoint bundle write, containing all six states. Authoring toy-test operations are not
included in these scientific workload totals. No network calls in the scientific path.

For each seed/language cell require:
- exact TRAIN probe accuracy >=0.90;
- fact-pair both-correct accuracy >=0.80;
- query-pair both-correct accuracy >=0.80;
- normal minus evidence-blind accuracy >=0.35;
- normal minus query-blind accuracy >=0.35.
With8 rows and4 pairs per language, the discrete exact/pair thresholds require8/8 and4/4.
The primary gate is all Full cells passing. GRU-only's gate is independent; it cannot turn a Full
miss into a primary PASS and is not a superiority comparison.

A valid Full miss yields status FAIL / ACCEPTED VALID NEGATIVE. A valid Full pass yields status
PASS / ACCEPTED PASS only for the minimal seen-TRAIN fit. Neither result changes C234/C235 or Gate F.

Execution requires changed weights, original initial fingerprints, unchanged weights during
scoring, all six checkpoints reloaded with correct schema/order/final fingerprint, exact argmax
replay, raw-logit and metric replay error <=1e-9, finite outputs and exact workload accounting.
Any source/artifact/schema/replay/nonfinite/mutation/workload error is INVALID / RETRY SAME C236.

## Source protection, tests and output contracts

Inherit C235's256 source pins /370 protected inputs. Add C235 summary plus five artifacts (6),
and OWN6 sources (6):262 source pins /382 protected inputs.
C234 summary/artifacts are already protected: do not double-count them.

OWN6:
- fold_lm/v05_benchmarks/model_c236_minimal_binding.py
- tests_lm/test_v05_c236_minimal_binding.py
- tools/run_c236.ps1
- tools/invoke_c236.ps1
- this preregistration
- docs/v5b-minimal-binding-learnability-v0.1.md

Direct dependency union12: the five C231 LM_SOURCES plus C230/C231/C232/C233/C234/C235/C236
benchmark entry points. All must exist in source pins; inherited transitive dependencies remain
protected. Accepted parent source/tests/logs and tools/run_c167.ps1 are not edited.

Own tests24; module count121; loaded2834/focused2833. Only the inherited exact exclusion remains:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Count contracts use actual unittest loaders/suite counts and test-ID sets, not numeric substrings.

Five generated artifacts under ignored runs/:
probe-plan.json, probe-dataset.json, trained-models.pt, measurements.json, validation-summary.json.
Checkpoint schema fold-c236-minimal-binding-v1; identities ordered as above; six state dicts.
Measurements contain initial_probe/final_probe, fit, fingerprints, final predictions, replay
results and counters. The runner re-summarizes measurements and verifies every output hash/size.
Only console log and publisher receipt are mirrored into docs/experiment-run-logs/c236/latest.*.

Manifest SHA256: `86f534a54964a31d0139d5a3ceb3ef4b5e3c2ab46667adb002390a5b5d347957`.

## Authoring review and execution boundary

Before activation, re-fetch all six committed files and verify their identities against reviewed
bytes; compile/import source, run24 own tests, check manifest/cohort hashes, parent field semantics,
fit AST parity, loader dispatch, count arithmetic, free-name bindings, runner CLI ordering and
launcher preflight/publication boundaries. Record review HEAD and actual checks in authoritative
handoff. The full2833-test suite, Windows AST, local artifacts and six-model scientific run are
not represented as executed unless actually run. Authoring fixture/toy tests are not model results.

Execution order: outer dispatcher ParseFile -> active launcher ParseFile -> runner ParseFile ->
Python syntax and parent/source/fit-contract precheck ->24 own tests ->2833 focused tests ->
C236 probe -> artifact postcheck -> remote log publication. Operational branch/tree/HEAD/ACTIVE
mismatches skip before execution/publication. Transport-only failure does not justify rerunning
a completed scientific probe.

## Interpretation and stop

Success may be memorization of16 prompts. It does not demonstrate unseen bindings, useful language,
reasoning, learned memory or core advantage. Cohort reduction changes repeat exposure and lexical
breadth together; it does not isolate either as a cause. Failure is a fixed-recipe minimal-fit miss,
not proof of architecture-wide impossibility or a diagnosis of the optimizer.

Numeric-memory tuning stays paused. Gate F NOT PASSED. No cleanup/history rewrite, paid API,
external corpus, larger model, C234 threshold rescue or unregistered follow-on run.
Judge C236 before registering C237.
