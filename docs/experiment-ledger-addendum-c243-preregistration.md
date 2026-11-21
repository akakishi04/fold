# C243 preregistration — saved recombination error audit

Experiment:C243-v5b-saved-recombination-error-audit.
Stage:V5-B-SAVED-RECOMBINATION-ERROR-AUDIT.
C242 ACCEPTED VALID NEGATIVE; C244 NOT REGISTERED. Gate E PASSED; Gate F NOT PASSED.
This registers C243. The authoritative handoff activates it only after committed-byte review.

## One question

Do saved C242 HOLDOUT errors select the other supplied value, an absent value consistent with the
fixed training-pair relation, or another output byte? This is descriptive error localization,
not a new capability trial or causal experiment. No model or training intervention is permitted.

## Accepted evidence and parent contracts

Acceptance/base commit:17d5cd5d82c584faaee0b02d52a22776c9ef47a3.
Acceptance record:docs/experiment-ledger-addendum-c242-c243.md.
C242 scientific execution HEAD:372c2c37429acece3f06a9b4521313da4b3d5f8e.
Published log commit:998b34447fc1ac5c4a0f2c42b0a4eb1958b87eb0.
Publisher log SHA256:490be44e71cbaab6169f4965ce7983c0276a543523921ef1c162b7574dcacd9e.
Summary SHA256:d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb.
Local summary:runs/c242-v5b-balanced-recombination-530e801ba23f496aa8e0a588e0d52982/summary.json.
Require the exact execution-valid FAIL summary with RECOMBINATION_MISS:12. Do not require parent PASS.

Required C242 artifacts:
- measurements.json:dcc69fcc29f3de2baf8a53082afd83dfa259d98a631689d2b916879b4b1a46f4
- recombination-plan.json:8088155ef7ba95eb47a8a7ae3790247ff20d61804ac08c7fc1b1ed2f0c645760
- split-dataset.json:9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0
- trained-models.pt:a71531049d76a89b29a9e9f38dfda47cda79c50c071aab32beb8bbfda481f387
- validation-summary.json:5ac81c55f5d56e3984be7b769ae8a040a8965f16584c19c67423405f962cd3da

Call C242.validate_result on the parent summary and C242.summarize on its measurements; equality
with the accepted validation_summary is required. The C242 writer creates final[split][language]
and predictions[split][view] after step400; its checkpoint replay verifies those predictions.
Read those fields, not initial_train or an older final_probe. Identity order remains
234001/full,234001/gru_only,234002/full,234002/gru_only,234003/full,234003/gru_only.

Check exact split hash; TRAIN32/HOLDOUT64; targets, group/row/prompt disjointness and the partner
relation derived from TRAIN co-occurrences. Preserve original provenance fields and all row bytes.
The three views are normal,evidence_blind,query_blind. Predictions are integer bytes0..255 with
32 or64 entries as appropriate; do not narrow them to digit candidates.

The child adapter independently recomputes all discrete parent metrics from those answers:
rows,accuracy,evidence_blind_accuracy,query_blind_accuracy,evidence_drop,query_drop,
fact_pair_accuracy,query_pair_accuracy,order_pair_accuracy. Match all fields within1e-9 and
reject nonfinite values, wrong keys, replay flags, sizes or identities. answer_nll is checked
finite/nonnegative and protected by artifact hash only; nll_recomputed=False. No logit replay claim.

## Frozen analysis specification

The TRAIN-derived partner map is exactly0->1,1->0,2->3,3->2. It is not fitted to HOLDOUT outputs.
Ten fixed normal-view rules:entity,other_entity,partner_of_other,query_fixed_position,first,last,
constant_0,constant_1,constant_2,constant_3. For partner_of_other, obtain the nonqueried entity's
value from the row and return its TRAIN partner. Rules use values/query/order, not saved targets.
No rule answer enters a model, changes the saved prediction or supplies a repaired score.

Mutually exclusive error categories use this precedence:
correct,other_supplied,absent_partner_of_other,absent_partner_of_queried,other_byte.
On TRAIN, entity=partner_of_other and other_entity=partner_of_queried, so the first categories
win. On every cross-pair HOLDOUT the four digit answers are distinct and exhaust0..3. This is a
classification identity, not proof of how the model computes. Keep other bytes separate.

Per seed/family/split/language report all five category counts and all ten rule-match counts.
Retain row-level values,query,order,target,all three saved answers and offline rule outputs.
Also retain all fact/query/order pairs with IDs,answers,same-answer and both-correct flags.
Pair keys match the actual C234/C242 implementation:fact uses unordered value pair/order/query;
query uses assignment group/order;order uses assignment group/query. Fact/query targets differ,
order targets agree. Each language has8 pairs per kind on TRAIN and16 on HOLDOUT.

## Workload, gate and outputs

6x(32+64)x3=1728 unique saved predictions;576 normal rows;5760 rule comparisons;
864 pair records;24 diagnostic cells. These count primary evidence records, not repeated reads.
Scientific training steps, model forwards, checkpoint loads/writes and network calls are zero.
The accepted checkpoint is byte-hashed but never deserialized. Regression fixtures/file work are
not included in the zero-model-work scientific claim.

PASS is diagnostic integrity only, with no required rule agreement. Source/input identities,
parent summary and discrete-metric replay, exact counts and persisted recomputation must hold.
Any protection/schema/nonfinite/replay/workload fault is INVALID / RETRY SAME C243. Rule mismatch
is a valid diagnostic outcome. Neither C242's verdict nor Gate F is changed.

Five ignored local outputs:audit-plan.json,row-errors.json,pair-audit.json,diagnostics.json,
validation-summary.json. Summary.json records execution HEAD, source/input identities and artifact
hashes/sizes. Postcheck reconstructs every output from the original parent files and compares them
exactly without extra inference. Console log/receipt alone go to docs/experiment-run-logs/c243/latest.*.

Manifest SHA256:02f2420c59bfa7a232686ea42cf2ed47ee6c17ebe2714e81a2fbc169a8e70379.

## Protection and tests

Inherit C242298 source pins/454 inputs; add its summary+five artifacts and OWN6:
304 source pins/466 protected inputs. Reject duplicate paths. Direct dependency union19 covers
five C231 LM_SOURCES plus C230 through C243 entry/helper modules, including lazy context calls.
No accepted source/test/log/shared launcher is changed.

OWN6:
- fold_lm/v05_benchmarks/model_c243_saved_recombination_audit.py
- tests_lm/test_v05_c243_saved_recombination_audit.py
- tools/run_c243.ps1
- tools/invoke_c243.ps1
- this preregistration
- docs/v5b-saved-recombination-audit-v0.1.md

Own tests24;modules128;loaded3002/focused3001. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Actual loaders and unique test IDs enforce counts. A synthetic constructed-suite check tests the
filter logic but is not represented as a run of the full historical suite.

## Review and execution boundary

Re-fetch all six committed OWN files after authoring. Match code/script Git blobs to locally
tested bytes; compile/import and execute24 own tests; audit free-global bindings, parent writer
semantics, call ordering, split/manifest hashes, metric keys, category identifiability, exact paths,
CLI argument order and parser-before-execution. The actual loader/run/postcheck are exercised with
synthetic files and substituted parent/protection adapters; those are not actual C242 predictions.
Record review HEAD, actual checks and pending Windows/local-artifact checks in handoff.

Dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile -> Python/source/parent
precheck ->24 own tests ->3001 focused tests ->C243 audit ->postcheck ->log publication.
Wrong branch, dirty tracked tree, stale ExpectedHead or ACTIVE mismatch skips before logging.
Do not bypass tests or rerun a completed audit for transport-only failure.

No model modification, more training, answer inversion, larger model, paid API, external corpus,
history rewrite or cleanup. No causal claim, independent replication, generalization gain or
core-superiority claim. Numeric-memory tuning remains paused. Judge C243 before registering C244.
