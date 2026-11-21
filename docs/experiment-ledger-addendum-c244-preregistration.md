# C244 preregistration — two-partner recombination

Experiment:C244-v5b-two-partner-recombination.
Stage:V5-B-TWO-PARTNER-RECOMBINATION.
C243 ACCEPTED PASS (diagnostic integrity only); C242 ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED. C245 NOT REGISTERED.
This document registers C244; the authoritative handoff activates it after committed-byte review.

## One scientific question

Can fresh models transfer to still-held value pairs when every TRAIN value has two partners,
at the same400 updates/batch32/76800 total training presentations?
This is a learning intervention motivated by C243's descriptive error analysis, not a claim that
its matching rule has been identified as the unique internal cause.

## Parent identity and immutable source data

Acceptance/base commit:432ecaa53da0f45806793865d88334fbbb90569f.
Acceptance record:docs/experiment-ledger-addendum-c243-c244.md.
C243 execution HEAD:1ff8bcfd4905b54c9f685eee26e197eb62394ab2.
Published log commit:8dbf3c9a2ed661b8b826243ee996aa1057b19eba.
Publisher-recorded log SHA256:53b5dbb8867f5f02dfd79225a0dd2e9fbf7541ef2ba98df5b6ab2e7d43784ace.
Summary SHA256:adf53e7f0306ab9d3fa209f24fb4fa1dbdc3d717037a4e7931579e670acdd2ce.
Local summary:runs/c243-v5b-saved-recombination-audit-9a4a52f99ee2402dbbc3cb303935217a/summary.json.

Required C243 artifact SHA256:
- audit-plan.json:02f2420c59bfa7a232686ea42cf2ed47ee6c17ebe2714e81a2fbc169a8e70379
- diagnostics.json:054369ba51d66be1166fff873ded22d31e683141a534937f5cfb4f4341c47347
- pair-audit.json:67fcc06862d282150fc4f5f0815d88ae52a0928c4574c698292d4ed49fb2ed72
- row-errors.json:2a89dc0e500523718bd020948a328da0418a1080c90278ed712ff5e854516620
- validation-summary.json:beb8da05e254bb9872e6a555318dd62ce6deecd9b4b3c1e20aa5a0c3ccd63e0e

C242 summary is already protected by C243:
runs/c242-v5b-balanced-recombination-530e801ba23f496aa8e0a588e0d52982/summary.json.
SHA256:d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb.
Its split-dataset SHA256:9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0.
No additional copy of that inherited input is counted in protection totals.

C244 calls C243.load_inputs on the C242 summary, not the C243 summary. That loader checks the
actual C242 summary/measurement replay and discrete predictions. The C244 loader then partitions
those rows and adapts initial_sha256. C242's writer recorded initial_sha256 before fitting,
final_sha256 afterward, and final/predictions after400 steps. Only fresh initial identities are
used for new models; trained parent checkpoint files are byte-hashed but never deserialized.

## Partition, schedule and shortcut controls

Old block32:ordered pairs(0,1),(1,0),(2,3),(3,2), exactly saved C242 TRAIN order.
Added block32:ordered pairs(0,2),(2,0),(1,3),(3,1), filtered from C242 HOLDOUT in saved order.
TRAIN64 is old followed by added. HOLDOUT32 is remaining pairs(0,3),(3,0),(1,2),(2,1), in saved order.
Every pair includes both assignments through the listed reverse pair, both orders, queries and
languages. Preserve every row's exact bytes/provenance; outer C244 membership governs training.

C244 partition SHA256:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
Require exact prompt/row-ID/assignment-group disjointness. Each32-row block contains every
language/query/order/target combination once. Every digit has exactly two distinct TRAIN partners.
The source is the existing internal research data, not an untouched external benchmark.

Before learning, check on the TRAIN union:best lookup using language/query/order/nonqueried value
has maximum accuracy50%, versus C242100%; query-only lookup25%. Identical evidence-masked input
lookup has ceiling25% and query-masked50% on each split. These are finite-data ambiguity controls,
not learned measurements. A single block still has a unique partner map, so the union qualification
must not be omitted. No step/block identifier, target or row-ID is model input.

On zero-based even steps use TRAIN indices0..31; odd steps32..63. Start with old and finish at
step400 with added. Each block gets200 updates; every row appears200 times/model. Capture actual
forward input tensors and verify their equality with the scheduled block at every training call.
Do not change phase, shuffle, extend steps or choose a better final checkpoint after results.

## Fixed model and optimization

Fresh seeds234001,234002,234003; order seed/full then seed/gru_only.
Full13488/GRU-only10160 parameters,width16,48 slots. Match exact C242 initial fingerprints and
create common-weight GRU-only copy before either paired model trains. Same byte renderer,
256-way unrestricted output, normal/evidence-blind/query-blind views.
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 updates.
CPU float64,threads2,deterministic algorithms.

The fit AST matches C242 except progress tag and one ids assignment adding the step argument.
STEPS/BATCH/LR/CLIP/TOL remain identical. C242's unused sampler generator remains inert.
Only TRAIN is evaluated initially; HOLDOUT reaches the model after step400 and during reload.
No early stopping, hyperparameter/seed/checkpoint selection or further update uses its results.
Coverage, per-row repetitions and update schedule change jointly. Last-block effects and
interference remain possible; do not claim unique causal attribution to partner multiplicity.

## Scoring, comparator and fixed gate

Reuse C242.evaluate, validate_metrics, cell_pass and prediction_record. They accept dynamic row
counts and call the actual C234 renderer/evaluator. All fact/query/order pairs are complete.
TRAIN64 has32 rows/language and16 pairs/kind; HOLDOUT32 has16 rows/language and8 pairs/kind.

For every primary Full seed/language require BOTH split criteria:
accuracy>=0.90; fact/query/order pair both-correct>=0.80; evidence/query drops>=0.35.
Integer minima:TRAIN29/32 answers and13/16 pairs;HOLDOUT15/16 and7/8 pairs.
GRU-only is independent, not a substitute for Full or a superiority gate.
Classify TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS, retaining all actual metrics.
A valid primary miss is ACCEPTED VALID NEGATIVE; an integrity fault is INVALID / RETRY SAME C244.

Rescore C242 saved predictions on exactly the remaining HOLDOUT32 via row IDs. Use all three
views and C243.discrete_metrics; do not average over C242's old HOLDOUT64 or include promoted rows.
Store c242_same_holdout_discrete per model. Report the current/old normal accuracy and delta,
with no significance, independent replication or NLL-reconstruction claim. The comparator does
not control the capability gate and requires no parent model forward.

## Workload and output contract

Six models x400 =2400 updates/76800 training presentations, unchanged from C242.
Per model:initial TRAIN3/192 rows;final TRAIN3+HOLDOUT3/288 rows;reload both/288 rows.
Total90 evaluation forwards/4608 scoring rows,2490 model forwards/81408 row presentations.
Before reload409 calls/13280 rows;reload6/288;after415/13568. Block update counts[200,200].
One new ordered six-state checkpoint bundle, schema fold-c244-two-partner-v1. Zero scientific
network calls or parent-checkpoint inference. Own/historical test fixtures are outside these totals.

Require initial identity, changed weights, evaluation non-mutation, actual schedule/forward/row
counts, strict checkpoint identity/order, exact prediction replay and raw-logit/metric error<=1e-9.
Postcheck verifies hashes/sizes, normalized plan, partition, initial/comparator identity and
recomputed child discrete metrics. Do not reconstruct parent NLL from argmax arrays.

Five ignored local artifacts:two-partner-plan.json,split-dataset.json,trained-models.pt,
measurements.json,validation-summary.json. Summary counters:train_steps,answer_presentations,
model_forward_calls,row_presentations. Measurements contain initial_train,final[split][language],
predictions[split][view],block_updates and c242_same_holdout_discrete. Only console log and receipt
are published to docs/experiment-run-logs/c244/latest.*.
Manifest SHA256:e89a41c15ef3d702c7009a9b4fc22f4e28809dea3892c5d63cf02120a1e10b0b.

## Protection and review

Inherit C243304 source pins/466 inputs; add its summary+five artifacts and OWN6:
310 source pins/478 inputs. Direct dependency union20:five C231 LM_SOURCES and C230 through
C244 helper/entry modules, including lazy imports. No accepted source/test/log/shared launcher edits.
OWN6:the C244 benchmark,test,runner,launcher,this preregistration and
 docs/v5b-two-partner-recombination-v0.1.md.
Own tests24;modules129;loaded3026/focused3025. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
The actual historical loader enforces unique IDs/counts; synthetic filter tests are not a full-suite run.

After all six files are committed, retrieve them again at a fixed review HEAD, match code/script
blob identities to tested bytes, compile/import, rerun24 own tests and audit free names, exact
parent schemas, fit AST, mask/shortcut controls, actual loader/evaluation order, output schema,
CLI argv positions and parser/publication boundary. Record actual checks and limitations in handoff.
The reviewer must not claim Windows AST, full historical regression or actual local artifacts passed
unless performed. Synthetic models and parent excerpts are authoring validation, not scientific results.

Standard path:outer dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile ->
Python/source/parent/data precheck ->24 own tests ->3025 focused tests ->C244 ->postcheck ->log push.
Branch/tree/stale-HEAD/ACTIVE mismatch skips before logging; no source guard or test bypass.
Transport-only failure is repaired without retraining. Gate F NOT PASSED;numeric-memory tuning
paused. No general language/core superiority/unique causal mechanism claim,larger model,paid API,
external corpus,cleanup or history rewrite. Judge C244 before registering C245.
