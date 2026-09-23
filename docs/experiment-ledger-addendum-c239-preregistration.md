# C239 preregistration — fresh fact-order holdout

Experiment: C239-v5b-fact-order-holdout.
Stage: V5-B-FACT-ORDER-HOLDOUT.
C238 ACCEPTED PASS for minimal seen-TRAIN fitting; C236 remains ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED. C240 NOT REGISTERED.
This document registers C239. The authoritative handoff controls activation/readiness after
independent post-authoring review of committed files.

## One scientific question

With fresh initial weights and the complete-cohort recipe, can training on order0 prompts transfer
to the matched order1 prompts that are withheld from this model's training?
This tests a limited presentation-order holdout, not new facts/entities/values or general language.

## Parent evidence and contracts

Acceptance record: docs/experiment-ledger-addendum-c238-c239.md.
Acceptance record commit:72907fe195f56b886a9bc9b9fc0db6c83f9cbda2.
Acceptance/handoff base:74100dd8c7b151f0cdd44e36ef846825614d7836.
C238 scientific execution HEAD:a7999c92e2f6f071c045de268feaf5ddd6f438ac.
Published log commit:93a86ea4493c4c6bf20b046b56c29e8bccc322f9.
Log SHA256:da9386a9f351ebf9aeec18df7057aac9971c4b068fbe337efdcf7363260b8e60.
Summary SHA256:06ab54549477894ea17f986364cacc6b3b7d25ff2dea70b18e98e2a957c80363.
Local summary:runs/c238-v5b-complete-cohort-sampler-df6538e306784434bdcbb2848e4c278d/summary.json.

Required accepted C238 artifacts:
- measurements.json:3d358412484f9f9d227ea0a37e8b5ca9de72fff980f8f7d0d32a95982b658fe7
- probe-dataset.json:bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c
- sampler-plan.json:ae9d0b7e92ee7024b57210f1779aebbfc0757fa995acbdf6f9359b2f23664232
- trained-models.pt:2a09b28dd2a10c210380cbe05eb18360f69d309e44bc3e9599f0eb3e178c624d
- validation-summary.json:8c7edfb3a5634bd06a7d3f4b15db909d7e09330e1cec844bda943a363f69670a

Require C238.validate_result to accept the exact execution-valid PASS summary, with both family
probe gates True. Hash all accepted source/input/artifact bytes, not only the subset newly read.
C239.load_inputs reads the pool and measurements, reproduces the C238 summary through its real
summarizer, checks identity order and validates parent initial_probe/final_probe using the parent
4x2-language schema. initial_sha256 is BEFORE C238 training; final_sha256 is AFTER. These are
verified from the writer and must differ. Only initial_sha256 initializes the new-model identity.
No trained parent state dict is loaded, even though its artifact remains protected.

## Partition identity and leakage boundary

From the exact16-row pool, TRAIN is every order0 row and HOLDOUT every order1 row, preserving
original order. Each contains8 rows,4 per language, both0/1 assignments and both queries.
Each language/split has2 fact pairs and2 query pairs. Targets0/1 each occur2 times/language/split.
Canonical outer {TRAIN:[...],HOLDOUT:[...]} JSON SHA256:
6f47a61c0ec4de616e77dab803ad964a9243e627b8a06f3e987d2824f8951731.

Exact prompt strings and row IDs must be disjoint. Underlying fact groups intentionally overlap;
this is a paired order test, not a group-disjoint fact or value-pair test. Preserve the parent's
split="TRAIN" provenance in each row; C239's outer partition controls training membership.

TRAIN:box then book (or the existing Japanese names). HOLDOUT:book then box. The assignment and
queried object are otherwise matched. Do not regenerate targets or change the renderer.
Holdout tensors are first evaluated only after the400-step training endpoint. The fit function
accepts TRAIN tokens/targets only. No early stopping, tuning, best-checkpoint/seed selection or
continued training based on holdout scores. Never reuse the C238 trained models, which saw both orders.

## Changed and held constant

Change training coverage/evaluation partition from16 seen prompts to8 TRAIN/8 order-held-out prompts.
The complete-cohort batch32 repeats each retained row4 times. Each TRAIN row receives1600
presentations per model, not C238's800; this is a consequence of reduced training coverage at the
same budget. This is not a single-endpoint accuracy comparison to C238's all16 resubstitution score.

Keep fresh initial weights matched to C238, seeds234001/234002/234003, Full13488/GRU-only10160
parameters, width16,48 slots, byte renderer, unrestricted256-class answer scoring and three views.
Construct the common-weight GRU-only copy before either paired model trains.
AdamW lr0.005, betas(0.9,0.999), eps1e-8, weight_decay0, clip norm1, batch32,400 steps/model.
CPU float64, threads2, deterministic algorithms. Fit body AST equals C238 except the progress tag;
only balanced_indices changes from16x2 to8x4. The unused seeded generator has no sampling effect.

Reuse actual C234 tensors/evaluate/metrics/paired_accuracy. A new C239 validator explicitly accepts
4 rows/language/split; never send these results to a parent validator requiring8 rows/language.
C239's new final record is keyed by TRAIN/HOLDOUT, not the parent final_probe schema.

## Fixed workload and gate

Six models x400 steps=2400 training steps/76800 answer presentations.
Per model:initial TRAIN3, final TRAIN3/HOLDOUT3, checkpoint replay TRAIN3/HOLDOUT3=15 scoring forwards.
90 scoring forwards x8 rows=720 scoring presentations. Totals2490 model forwards/77520 rows.
Before reload each model must count409 forwards/12872 rows; reload adds6 forwards/48 rows;
final per-model total415 forwards/12920 rows. One new checkpoint bundle containing6 states.
No parent-model inference, new external data, scientific network calls or extra training.

Require on BOTH TRAIN and HOLDOUT, for every primary Full seed/language cell:
accuracy>=0.90; fact/query paired both-correct>=0.80; evidence/query mask drops>=0.35.
The discrete accuracy/pair thresholds require4/4 rows and2/2 pairs. GRU-only gate is separate.
Classify each seed/family/language cell as TRAIN_FIT_MISS, ORDER_HOLDOUT_MISS or BOTH_PASS using
these full criteria, not accuracy alone. TRAIN_FIT_MISS does not establish an isolated transfer gap.

A valid primary pass is ACCEPTED PASS for this bounded order transfer. A valid miss is
ACCEPTED VALID NEGATIVE, not a reason to relax thresholds. Initialization, source/artifact,
nonfinite, regression, replay, mutation or workload errors are INVALID / RETRY SAME C239.
C238 and earlier verdicts remain unchanged. Gate F remains NOT PASSED in either case.

## Protection and regression

Inherit C238274 source pins/406 inputs. Add its summary and5 artifacts, then OWN6 sources:
280 source pins/418 protected inputs. Reject duplicate parent or artifact paths. Direct union15:
5 C231 LM_SOURCES and C230 through C239 benchmark/helper entry points. Accepted parent files and
shared launcher are immutable; all actually called helpers remain pinned/protected.

OWN6:
- fold_lm/v05_benchmarks/model_c239_order_holdout.py
- tests_lm/test_v05_c239_order_holdout.py
- tools/run_c239.ps1
- tools/invoke_c239.ps1
- this preregistration
- docs/v5b-fact-order-holdout-v0.1.md

Own tests24;modules124;loaded2906/focused2905. Only the inherited exact exclusion remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Use actual unittest counts and unique IDs; do not assert mutable ACTIVE state in historical tests.

## Output and review

Five local-only artifacts under ignored runs/:holdout-plan.json,split-dataset.json,trained-models.pt,
measurements.json,validation-summary.json. Checkpoint schema:fold-c239-order-holdout-v1, six states
ordered seed/full then seed/gru_only. Each record stores initial_train, final TRAIN/HOLDOUT metrics,
initial/final fingerprints, actual fit/call/row counts, predictions and checkpoint replay results.
Evaluation cannot mutate weights. Reload must match final fingerprints, exact predictions and
raw-logit/metric replay error<=1e-9. Saved postcheck revalidates hashes/sizes, partition, plan,
measurement summary and original initial identities without extra model forwards.
Only console log and receipt are published to docs/experiment-run-logs/c239/latest.*.

Manifest SHA256:4eca2f0276b521286729f1819abd929a035659a589488b332fe976d392b4dac0.

Independent post-authoring review must re-fetch all6 committed files, match source/script blobs
to locally tested bytes, compile/import, run24 authoring tests and audit parent schema/semantics,
free names/imports, fit AST, partition hash, holdout timing, counts and CLI/parser ordering.
Synthetic six-model execution and parent excerpts are not a full-checkout or formal scientific run.
Record actual checks, limitations and review HEAD in authoritative handoff before activation.

Order:dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile -> Python syntax /
source / parent / partition precheck ->24 own tests ->2905 focused tests ->C239 probe ->postcheck ->log push.
Branch/dirty-tree/stale-HEAD/ACTIVE mismatch skips before scientific execution and log publication.
Do not report Windows AST/full regression/local parent checks as PASS until executed.

## Scope and stop

Success supports only the preregistered one-direction order transfer on these nouns/values/facts.
It does not prove general understanding, unseen-entity/value transfer, useful memory, general
reasoning, core superiority or Gate F. No automatic C240, larger model, paid API, external corpus,
cleanup/history rewrite or production runtime change. Numeric-memory tuning remains paused.
Preserve tools/run_c167.ps1 and all accepted evidence. Judge C239 before registering C240.
