# C240 preregistration — saved-prediction positional-rule audit

Experiment:C240-v5b-saved-positional-rule-audit.
Stage:V5-B-SAVED-POSITIONAL-RULE-AUDIT.
C239 ACCEPTED VALID NEGATIVE; C238 minimal seen-TRAIN fitting PASS.
Gate E PASSED; Gate F NOT PASSED. C241 NOT REGISTERED.
This document registers C240. Authoritative handoff controls activation after remote-readback review.

## One scientific question

Do the fixed, saved C239 final answers agree with a query-to-fixed-position rule, correct entity
binding, always-first/last rules or constant-digit responses? This is descriptive error analysis,
not new inference, training, capability testing or causal identification.

## Parent evidence

Acceptance:docs/experiment-ledger-addendum-c239-c240.md.
Acceptance record commit:b739256640949f69a6ca781d31cde108cbe1edf6.
Acceptance/handoff base:006551cd8b91e04534f253b5cf3942a12b84f7f8.
C239 execution HEAD:c847609c8d045c9c5db4ec882bf336a9671180ff.
Published log commit:5207d3b378ae56502a78dc9a5bb6f843cf389795.
Log SHA256:9e139f0544b49cb1185ce285a7b7c2c7ccb5ad394198040be4845648aa3697ee.
Summary SHA256:500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af.
Local summary:runs/c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5/summary.json.
Require the exact execution-valid negative, with cell_outcomes ORDER_HOLDOUT_MISS:12.

Required artifact SHA256 values:
- holdout-plan.json:4eca2f0276b521286729f1819abd929a035659a589488b332fe976d392b4dac0
- measurements.json:872e534c5fb5f26fede0c4947b34344adc39a8e956bc453fed96763e757677c8
- split-dataset.json:6f47a61c0ec4de616e77dab803ad964a9243e627b8a06f3e987d2824f8951731
- trained-models.pt:2e3cf24b8feabead8f7470ebf271d27347ed0cf79aa873c30be68329a833d687
- validation-summary.json:c65f6e6226630e5017c5cfa240116ad76106ec07a490d053216bde0a9a8b1849

## Fixed records and writer semantics

Use all six models in order234001/full,234001/gru_only,234002/full,234002/gru_only,
234003/full,234003/gru_only. The C239 writer saves final[TRAIN/HOLDOUT][en/ja] and
predictions[TRAIN/HOLDOUT][normal/evidence_blind/query_blind] after training. Its replay_one
verifies these predictions after checkpoint loading. Read those final outputs, not initial_train,
not an earlier final_probe schema and not a regenerated model prediction.

The C239 summary is checked with its actual validate_result. Its actual summarize must reproduce
the saved summary. The C240 adapter validates split/view keys,8 byte predictions per view,0..255
integer range, replay flags and all discrete final metric fields. Recompute accuracy, fact/query
paired accuracy, mask accuracy and drops within1e-9. NLL is finite/hash-protected but cannot be
recomputed from argmax bytes; do not claim NLL or logit replay. nll_recomputed=False.

Partition identity is the exact C239 outer mapping,8 TRAIN/order0 and8 HOLDOUT/order1 rows,4 rows
per language per split. Preserve all row bytes including inherited split="TRAIN" provenance.
Check prompt/target semantics, partition balance, unique IDs and disjoint prompt strings. Rules
are post-inference calculations from objects/values/query/order, never model inputs or corrections.
The checkpoint artifact is hashed for protection but is NOT deserialized, loaded or evaluated.

## Fixed rule definitions and contrasts

Six normal-view rules, no post-result rule selection:
1. entity: value assigned to the queried object;
2. query_fixed_position: object0/box selects rendered first value, object1/book selects rendered second;
3. first: rendered first value independent of query;
4. last: rendered second value independent of query;
5. constant_0;
6. constant_1.

Record integer agreement counts for every seed/family/split/language cell, plus correct,
other_entity and outside_supplied counts. Retain unrestricted outputs; wrong bytes must not be
silently remapped to the other digit. Do not average away individual seed/language conditions.

Match TRAIN and HOLDOUT by language, assignment/group and queried object. Their target is the
same, while fact order differs. Save the two answers, same-answer flag, both-correct flag and
both-fixed-position-match flag for all pairs. The six rule outputs and all three actual prediction
views are retained in per-normal-row records for auditability.

Identifiability limits are fixed:entity=fixed-position on all TRAIN rows; on this binary HOLDOUT,
fixed-position=other entity. A rule match therefore cannot uniquely identify an internal algorithm.
No new precision/sensitivity/accuracy threshold decides the diagnostic's scientific status.

## Changed, held constant and workload

Change only offline scoring/diagnostic measurements. Hold all C239 data, saved predictions,
checkpoints, architectures, training history, masks, labels, seeds, verdict and evidence fixed.
New training steps0, model forward calls0, checkpoint loads0, checkpoint writes0, network calls0.
Reading/hashing checkpoint bytes is not deserializing a checkpoint. File/JSON work still has cost.

Primary analysis scope:6 models x2 splits x3 views x8 saved answers =288 unique saved predictions.
Normal rows96;6 rule comparisons each =576 comparisons. Order-matched pairs48.
24 diagnostic cells (6x2x2),4 normal rows each. Precheck/postcheck repeat validations of the same
records; these are not additional independent samples. Historical regression fixture work is
separate from C240's zero-model-work scientific analysis.

PASS means diagnostic integrity only:exact evidence identity, source protection, valid byte schema,
parent summary/discrete-metric replay, complete counts, and exact persisted-analysis recomputation.
No required rule agreement. An input/source/artifact/schema/nonfinite/replay/count failure is
INVALID / RETRY SAME C240. C239's negative and Gate F NOT PASSED remain unchanged for any outcome.

## Protection, test suite and outputs

Inherit C239280 source pins/418 inputs. Add its summary and five artifacts (6), and OWN6 (6):
286 source pins/430 protected inputs. Reject duplicate parent/OWN paths. Source-pinned dependency
union16 includes the five C231 LM_SOURCES and C230 through C240 benchmark/helper entry points;
all actually called parent/context/audit helpers remain protected. No accepted source/test/log edited.

OWN6:
- fold_lm/v05_benchmarks/model_c240_saved_position_audit.py
- tests_lm/test_v05_c240_saved_position_audit.py
- tools/run_c240.ps1
- tools/invoke_c240.ps1
- this preregistration
- docs/v5b-saved-positional-rule-audit-v0.1.md

Own tests24;modules125;loaded2930/focused2929. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Counts and unique IDs are enforced with actual unittest suites. Historical mutable-ACTIVE assertions
are not introduced. Full historical suite results are not presumed from arithmetic.

Five local-only artifacts under ignored runs/:audit-plan.json,row-audit.json,paired-orders.json,
diagnostics.json,validation-summary.json. Summary.json stores execution identity, source/input pins,
artifact hash/size entries and bounded integrity flags. Postcheck reloads original parent inputs,
recomputes every derived record and compares all five files exactly, without model forwards.
Only console log and publisher receipt go to docs/experiment-run-logs/c240/latest.*.
Manifest SHA256:31d2b0579d65b354979ef1d98e3012a57a95820e2f12cd729c931c8d8525bc25.

## Authoring review and stop

After all six OWN files are committed, re-fetch them at a fixed review HEAD, match code/script blobs
to tested bytes, compile/import, rerun24 own tests, audit free-name binding, parent field semantics,
metric-key spelling, rule degeneracies, source coverage, counts and embedded Python/CLI ordering.
Test the actual loader, actual run with synthetic saved records, persisted postcheck, wrong-head and
tamper rejection. Synthetic data is not C239 evidence and no synthetic result may support a claim.
Record actual checks and limitations in handoff before activation.

Dispatcher/launcher/runner ParseFile precede execution. Branch/dirty-tree/stale-HEAD/ACTIVE mismatch
skips before logging/publication. Authoritative sequence:syntax/source/artifact/discrete-replay
precheck ->24 own tests ->2929 focused tests ->C240 audit ->postcheck ->remote log publication.
Windows AST, full regression and user-local parent checks are not reported PASS without execution.

No answer inversion/repair, new training, architecture change, larger model, paid API, external
corpus, cleanup/history rewrite or production change. Numeric-memory tuning stays paused.
Preserve tools/run_c167.ps1 and all accepted evidence. Judge C240 before registering C241.
