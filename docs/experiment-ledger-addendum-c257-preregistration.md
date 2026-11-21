# C257 preregistration — frozen unseen fact-order transfer

Experiment:C257-v5b-unseen-fact-order-transfer.
Stage:V5-B-UNSEEN-FACT-ORDER-TRANSFER.
C256 ACCEPTED PASS within its three-entity value-assignment scope. C258 NOT REGISTERED.
Gate E PASSED; Gate F NOT PASSED. No production adoption.

## One question

Without further training, do all five accepted aligned-reader C256 models retain their capability
when the same facts are presented in the four permutations never used by C256?
This is an order-transfer capability evaluation, not a learned-weight change or internal-state swap.

## Accepted parent and identities

Acceptance/base commit:ee4c282687c71bed407ecb687659edd7103c740d.
Acceptance record:docs/experiment-ledger-addendum-c256-c257.md.
C256 execution HEAD:db9f3cb90d9268066c34fc91300193058301f06c.
Published log commit:5695706c6306156fa079ce092581270ca781af71.
Publisher log SHA256:4f21d18bec9eb3ae937c42be9d8af3091d67a241a53a85820afd3e6694110ce6.
Summary SHA256:56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184.
Summary path:runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.

Required artifacts:
-dataset.json:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b
-measurements.json:f7d11d7592769e54824d3d7dccc4e481029dc5157b6c35c333831408d7b032c8
-task-plan.json:43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1
-trained-models.pt:72d9ada52e48395290200c1c6918d7eef091aebd44a3d2a6176dc1dd442dae3a
-validation-summary.json:a25fe29ed2deb33ceab64c0f7d7e450e6a143ea5c0bc428eea20b9d45dff8bc2

Actual C256.verify_artifacts(parent_folder,PARENT_EXECUTION) validates the parent summary/artifacts
and returns its ten measurements. Require status PASS and seed_pass_counts candidate5/control0.
Its final/predictions/final_sha256 describe the final800-update states, not the initial state.
C256.load_bundle supplies ten states ordered by seed and then arm. C256.make_model supplies the
actual C252 aligned reader or C248 EOS adapter. Strict-load each matching final state and verify
its fingerprint/14256 parameters before scoring. Freeze all parameters and model modes.
Do not use the C252 two-entity checkpoints or C255 diagnostic activations.

## Exact input change

Original known orders:(0,1,2),(2,1,0). New orders:(0,2,1),(1,0,2),(1,2,0),(2,0,1).
Only the visible order of facts changes. Entity names, assignments, query, target, delimiters,
byte encoding, fixed48 slots and final model weights remain unchanged.
The query remains at the end. Do not sort a novel prompt back to a known order before the model.

Use both original assignment splits and both languages. C256 TRAIN/HOLDOUT labels retain their
original meaning, but neither split is used for training in C257. Preserve all five seeds and both
arms. The original two orders have144 rows per split. The four new orders have288 rows per split.
Each novel row stores canonical source_id; all assignment sets and target labels are preserved.
New dataset SHA256:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
All six orders together move every entity through every position, including the formerly fixed
middle entity b/乙. No target/oracle/entity index is passed outside visible input bytes.

## Evaluation and integrity

Per model sequence:
-original C256.evaluate on both splits/all3 views;
-verify original predictions exactly and all original metrics including NLL within1e-9;
-only then evaluate four novel orders on both splits/all3 views;
-repeat original evaluation and verify raw-logit restoration within1e-9 and exact argmax;
-verify unchanged complete parameter fingerprint and18 forwards/3456 rows.

Original C256 raw logits are not stored in its accepted artifacts. Initial anchor comparison is
therefore against its saved metrics and prediction arrays. C257 restoration compares newly saved
anchor logits from the same run. Do not claim replay against nonexistent C256 raw logits.
New and restored outputs must be finite CPU float64; eval/requires_grad=False; threads2;
deterministic algorithms. No optimizer, gradient update, model selection or seed replacement.

## Fixed scientific gate

Primary PASS requires every aligned-reader seed to pass both languages and both assignment splits:
1. Original C256 cell criteria remain satisfied.
2. Each of the four new orders separately has accuracy>=0.90, query_triplet_accuracy>=0.80,
   evidence_drop>=0.35 and query_drop>=0.35.
3. All-six-order consistency>=0.80: an assignment/query group is correct only when all six orders
   produce the right target.

Per new order/language/split:36 rows and12 query triplets; integer minima33/36 and10/12.
Per language/split all-six-order score:36 groups; integer minimum29/36 complete groups.
All new order cells are reported separately; a pooled mean cannot hide one weak permutation.
EOS control gates and all per-order metrics are reported independently. Its old criterion failures
remain performance results, not replay faults. Do not claim an additional independent control
failure merely because its already-failed original C256 gate remains unmet.

Whole-seed outcomes:ORIGINAL_CRITERIA_MISS, NEW_ORDER_MISS, SIX_ORDER_MISS or PASS.
A complete valid criterion miss is ACCEPTED VALID NEGATIVE. Any source/artifact/shape/nonfinite/
identity/replay/count/test fault is INVALID / RETRY SAME C257. No C256 verdict is revised.

## Workload and artifacts

Per model:original6 forwards/864 rows;novel6/1728;restoration6/864.
Ten models total180 full-model forwards/34560 row presentations.
Zero training steps;one accepted checkpoint-bundle load;ten strict state loads;zero new learned
checkpoint writes. Historical regression fixtures and file validation are separate computational work.

Five ignored outputs:order-plan.json,order-dataset.json,eval-outputs.pt,measurements.json,
validation-summary.json, plus summary.json. eval-outputs.pt has schema fold-c257-order-eval-v1,
records in seed/arm order, final fingerprints, counters and anchor/novel/restored logits.
It stores evaluation tensors, not newly learned parameters. Postcheck reconstructs all old/new
metrics and six-order groups from stored logits, validates original saved predictions and restoration,
and compares persisted JSON and artifact hashes without further model forwards.

## Protection and authoring review

Inherit C256382 source pins/623 protected inputs. Add parent summary+five artifacts and OWN6:
388 pins/635 inputs. Direct dependency union33 includes the five C231 LM sources, protected
C230 through C256 benchmark/helper modules, and the C257 benchmark. A bounded filename expression
selects exactly that inherited module range and requires its complete33-entry count.
No accepted source/test/log or shared dispatcher is changed.

OWN6:
-fold_lm/v05_benchmarks/model_c257_unseen_fact_order.py
-tests_lm/test_v05_c257_unseen_fact_order.py
-tools/run_c257.ps1
-tools/invoke_c257.ps1
-this preregistration
-docs/v5b-unseen-fact-order-v0.1.md

Own tests24;modules142;loaded3338/focused3337. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36.
The fixed hash is checked against actual manifest bytes; it is not assigned dynamically at runtime.
Source/input-count failures and hash failures have separate expected/actual diagnostics.

Before activation re-fetch all committed files, match code/script blob hashes to actual tested
copies, rerun exact24 own tests, compile/import, audit free globals and parent signatures, verify
fixed hashes, permutation groups, gates, counts, CLI indices and parser-before-publication ordering.
Own tests explicitly use synthetic lookup models and substituted parent/audit adapters; they must
never be represented as learned-model capability evidence or execution of the complete parent graph.
Record actual and pending checks in the authoritative handoff. Do not issue a launcher before review.

## Boundaries and stop

A PASS establishes bounded frozen transfer to these permutations, not general language, arbitrary
contexts, unseen entities, FOLD-core superiority, deployment readiness or Gate F. No automatic
architecture adoption. Do not tune based on the new order results or add them to training in C257.
No paid services, external corpus, cleanup, history rewrite or CI work.
Dispatcher/launcher/runner syntax checks precede parent/order precheck,24 own tests,3337 regression,
frozen evaluation,postcheck and publication. Operational skips occur before experiment logging.
Repair log-only publication without rerunning completed evaluation. Judge C257 before C258.
