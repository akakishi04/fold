# C255 preregistration — fixed-query value residual swap

Experiment:C255-v5b-value-residual-swap.
Stage:V5-B-VALUE-RESIDUAL-SWAP.
C254 ACCEPTED PASS (diagnostic integrity only);C256 NOT REGISTERED.
Gate E PASSED;Gate F NOT PASSED. Activation follows committed-byte authoring review.

## One question and accepted identities

Does the post-core residual contribute value-assignment-specific information when query identity
and fact order are fixed,with the original recipient reader contribution unchanged?
This complements C254's query versus order swaps. No new training or capability promotion.

Acceptance/base commit:5764f3e18a09452739029c3accd7740686d8d7fe.
Acceptance:docs/experiment-ledger-addendum-c254-c255.md.
C254 execution HEAD:4e6e5abf5a6a3c97e784868b9fc5e016fc1cf77c.
Published log commit:4fb92919e1da8146fcfe14d779f6b5a91008316a.
Publisher log SHA256:8f13b86ea18c7522170046bf6a70e49f7d334b2d5dca74c8261d007f089901e3.
C254 summary SHA256:96f0a3eaafbf0b9fc62e7e9f789344eac45497b2679662525ea54993803535f5.
C254 path:runs/c254-v5b-paired-residual-e324dc81a0364f92820cf8da7f3a0172/summary.json.

C254 required artifact identities:
-contrasts.json:562e6fae59bd1cb79dcefd1191445277d53735c2bec1ee1cbfc08726cd5b80b2
-diagnostics.json:2c98ffc583768f43aa3311d7164828163888da19f18594d36ce49840b75990e2
-head-outputs.pt:ad4bfefa0380323fb5c408c1f9de4778d2e04c09637bae44049efb7df5f2d5a1
-swap-plan.json:cfbf05fc55fe6c87a0b738bfab7f4c676bb75ed503883cb399898f7936641276
-validation-summary.json:f204facbb500f7bc43db578e39231c8c2bc39dd07c7c399dcbef1de3ca3b9d95

C253 summary is already inherited:
SHA256:2d65feaed637c71728cd8ed1cc60f54306a7fb733b43c6b695e86f0313f27e47.
Path:runs/c253-v5b-frozen-residual-97fc39ef6e8b42cba8c2d1933ddfcbf6/summary.json.
C252 summary is already inherited:
SHA256:18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e.
Path:runs/c252-v5b-precore-query-ea8199d8ca794acba051ca5f65a391b3/summary.json.
Do not double-count these earlier inputs. All original checkpoint and activation files remain hashed.

## Exact parent loader and writer semantics

C254.load_inputs(c253_summary,c252_summary) returns parts,C252 final refs,C253 original entries.
It replays C253 evidence. The new C255.load_inputs explicitly calls that two-argument parent adapter,
then reads C254 head-outputs.pt (schema fold-c254-head-outputs-v1,records),not parameter states.
C254.analyze(parts,prior_records,original,C253.metrics) must reproduce all parent JSON outputs and
validation_summary. Each prior record contains outputs[self/order_swap/query_swap/restored] and
final_sha256 of the same C252 learned model. These are immutable comparators,not new model runs.

C253 original entries contain components[intact][split][view][post/read] and original logits.
These are final learned activations. Do not replace them with initial-state fields or a generated
fixture. C252.load_bundle loads the five trained states once. C253.frozen_model strictly restores
actual C252.AlignedPrecoreReadout,checks14256 parameters/final_sha256,and freezes gradients/eval.
C255 calls ONLY its original readout_norm and decoder. All protected lazy context paths are retained.

## Fixed interventions and controls

All five seeds250001..250005,exact TRAIN64/HOLDOUT32,three original views and every original row
remain fixed. No successful-seed subset or new learner. Canonical split SHA256:
e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.

Donor selection uses (language,objects,values,order,query),reversing only values.
Same language/query/order/object pair and same unordered value set;reversed entity-value assignment.
No cross-seed/split/view donors. Unique keys/IDs,complete counterpart,bijection,involution and no
fixed points are required. Target labels only validate different paired targets,not index selection.

Mode order:self,value_swap,coherent_swap,restored.
-self/restored:decoder(LN(post_i+read_i));
-value_swap:decoder(LN(post_d+read_i));
-coherent_swap:decoder(LN(post_d+read_d)).
Use original norm shape,epsilon,weights,bias and decoder. Do not change any parameter or saved tensor.

Self must reproduce original C253 and C254 self logits<=1e-9 and exact argmax before altered modes.
Coherent_swap must reproduce the corresponding original DONOR logits and argmax,including donor
errors. It is a positive replay control;never interpret recipient-label accuracy for this mode.
Restored must reproduce self. Evidence-blind paired fact inputs coincide:require exact post/read
identity and unchanged value-swapped outputs. No new input masking or target information is added.

Guard complete model/backbone/encoder/core/reader forward calls. Require frozen fingerprints after
each head computation. Hook counts verify24 norm and24 decoder calls/1152 rows per model. Remove
hooks on success or exception. Require finite CPU float64 logits/components;threads2,deterministic.

## Gate, accounting and metrics

PASS is diagnostic integrity only. No criterion on accuracy drops,donor-target match,or a previously
failing seed. Any source/artifact/schema/nonfinite/donor/replay/count/test error is INVALID / RETRY
SAME C255. C252,C253,C254 and Gate F statuses do not change under any observed performance pattern.

5x4x2x3=120 head forwards/5760 head rows. Full-model/encoder/core/reader forwards0,new training0,
new learned checkpoint writes0. One parameter-bundle load,five strict state loads. Archive loading,
validation,JSON work and historical test fixtures have separate real costs. They are not new samples.
Three scored modes(self,value_swap,restored) give60 diagnostic cells;20 value-vs-self contrast cells.
Coherent control logits are retained but not scored against recipient labels.

Use C253.metrics for accuracy,NLL,fact/query/order pairing and mask drops. New contrasts contain
original/changed correct counts,correct-to-wrong,wrong-to-correct,flips,donor-target matches,
accuracy/NLL deltas and full original C254 order/query-swap metrics recomputed from their saved logits.
The comparator output head is not rerun. Correlated cells are not independent trials or significance tests.

Five ignored outputs:value-plan.json,head-outputs.pt,diagnostics.json,contrasts.json,validation-summary.json.
New archive schema fold-c255-value-head-outputs-v1 has five records of four-mode raw logits,counters,
final identities and replay flags,not parameter states. Postcheck reconstructs all metrics,controls,
comparators and JSON exactly from original/new archives without any head or full-model forward.

## Source and authoring contract

Inherit C254370 source pins/599 inputs. Add its summary+five artifacts and OWN6:
376 source pins/611 protected inputs. Explicit dependency union31=five C231 LM_SOURCES plus
C230..C255 entry/helper modules. No accepted sources/tests/logs/shared launcher are edited.
Own tests24;modules140;loaded3290/focused3289. Only inherited exact exclusion remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.

OWN6:
-fold_lm/v05_benchmarks/model_c255_value_residual_swap.py
-tests_lm/test_v05_c255_value_residual_swap.py
-tools/run_c255.ps1
-tools/invoke_c255.ps1
-this preregistration
-docs/v5b-value-residual-swap-v0.1.md
Manifest SHA256:e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a.

After committing all six files,re-fetch their bytes at one review HEAD,match complete code/script
blob hashes to tested files,compile/import,run exact24 own tests and audit globals,donor selection,
parent schemas/signatures,negative/coherent/restored replay,workload and CLI/parse ordering.
Tests are self-contained synthetic heads/activations;the loader/run adapters are explicitly mocked.
Those tests are not a complete historical regression or an accepted-artifact scientific run.
Record actual checks and pending Windows/full-suite/user-local checks before activation.

## Scope and stopping boundary

Swaps preserve the residual multiset but disturb its joint distribution with reader features.
Value sensitivity is not unique semantic/causal identification or evidence of training-time core
necessity. Query- and value-swapped donors share a target on this binary relation;matching effects
would not uniquely distinguish target-value coding from correlated features. No production adoption.
After this complementary contrast,select an explicit capability/stability decision rather than
indefinitely expanding the same small-fixture diagnostic chain. C256 is not registered here.

Dispatcher/launcher/runner ParseFile ->syntax/source/archive checks ->24 own ->3289 regression ->
C255 head diagnostic ->postcheck ->publication. Operational branch/tree/HEAD/ACTIVE mismatch skips
before logging. Transport-only failures are repaired without repeated scientific scoring.
No paid API,external corpus,model expansion,cleanup or history rewrite. Judge C255 before C256.
