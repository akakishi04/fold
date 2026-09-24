# C254 preregistration — paired post-core residual swap

Experiment:C254-v5b-paired-residual-swap.
Stage:V5-B-PAIRED-RESIDUAL-SWAP.
C253 ACCEPTED PASS for diagnostic integrity only;C255 NOT REGISTERED.
Gate E PASSED;Gate F NOT PASSED. Acceptance and registration are separate commits.
Activation requires committed-byte authoring review and authoritative handoff update.

## One question

Does a frozen post-core residual contribute information specific to the recipient query beyond
what can be supplied by a paired prompt,with the recipient's reader output unchanged?
Compare query-swapped residuals against meaning-preserving order-swapped residuals. No new training.

Acceptance/base commit:bd1b88a27ab4aaa5712d06bc178158e6f410a7ff.
Acceptance record:docs/experiment-ledger-addendum-c253-c254.md.
C253 execution HEAD:13523ebefc482f3b230101d9a89938bda79c69e5.
Published log commit:aca5849d45c9f6c6323db84dc9896a4092144fa0.
Publisher log SHA256:a7690d0e6db2108b4f3e6329e12fbb9a14d8049ba0fbf5ceefc661c02d118880.
Parent summary SHA256:2d65feaed637c71728cd8ed1cc60f54306a7fb733b43c6b695e86f0313f27e47.
Parent path:runs/c253-v5b-frozen-residual-97fc39ef6e8b42cba8c2d1933ddfcbf6/summary.json.
Require exact execution-valid diagnostic PASS via C253.validate_result.

C253 required artifact SHA256 values:
-contrasts.json:e364a74cb9338d7be8c57e85bcbac63e77d169847e83c358175b4e7caaa416d7
-diagnostics.json:5647cbff9a4d214e3c83e77f689e9fde18955c5aef1dba71647c3db9cdd3c6bb
-outputs.pt:3e8ba69a46323ed4c47c143f7cacd23ddd42c64cc7a5dbd3973cfd9bff32147c
-residual-plan.json:c48689b9cebedc757261ded1912dbb597884f19ac007d971bcd7bfbfbfd8307d
-validation-summary.json:b9cefa29b067961cb9dd181e5ab8be63352b795ee7e91540a63cc2b13d971685

C252 is already inherited/protected,not counted as a new parent input:
summary SHA256:18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e.
path:runs/c252-v5b-precore-query-ea8199d8ca794acba051ca5f65a391b3/summary.json.
C252 checkpoint SHA256:024e8081fae8bc45ce449b3bdf53745499911ca631387620a6575e2312c5b6c3.
Check the resolved C252 summary path against inherited input_sha256 and all inherited file hashes.

## Parent schema and exact source of evidence

C253 outputs.pt schema is fold-c253-frozen-outputs-v1 with ordered entries for seeds250001..250005.
Each entry stores final_sha256,outputs[mode][split][view],components[mode][split][view][pre/post/read],
workload and frozen flags. These are learned endpoint activations,NOT trainable parameter states.
Use only its intact post/read activations for new head scoring.

Call actual C253.load_inputs(c252_summary):despite its module number,this helper reads C252.
Then C253.analyze(parts,entries,refs) must reproduce all four C253 JSON artifacts and its summary,
including original C252 predictions/metrics,unchanged components and restored outputs.
Do not call this parent loader with the C253 summary or substitute a guessed record schema.
C254 has its own load_inputs(c253_summary,c252_summary) and run calls that adapter explicitly.

C252.load_bundle verifies the accepted five-state schema/order. C253.frozen_model(ref,state,C252,
factory) instantiates the actual C252.AlignedPrecoreReadout,strictly loads its final state,checks
14256 parameters/fingerprint and freezes gradients/eval. No training or partial checkpoint loading.
C254 then calls only model.backbone.readout_norm and decoder. It never calls the full model,
backbone,encoder,core or reader. Scoped guards reject any such forward,including nested calls.

## Fixed donor design

Original TRAIN64/HOLDOUT32,rows/targets/provenance,three input views and all five seeds are unchanged.
No subset selection of previously successful seeds. Mode order:self,order_swap,query_swap,restored.
For each recipient i:
-self/restored:donor=i;
-order_swap:same language,assignment-group,queried entity;opposite fact order;
-query_swap:same language,assignment-group,fact order;opposite queried entity.

Mappings use visible row metadata only. Targets check equal/different pair invariants but never
select indices. Require unique keys and IDs,complete counterparts,equal facts,bijection,involution
and no self donors for the altered modes. Never cross seed,split,language or view.
The exact empirical multiset of post-core residuals is preserved within each condition.
Recipient reader vectors never change or receive a donor's answer as input.

Compute decoder(LN(saved_post[donor]+saved_read[recipient])) with the accepted model's original
normalization shape/epsilon/weight/bias and decoder. Addition/indexing cannot mutate saved inputs.
All intermediate/output tensors must be finite CPU float64. Threads2,deterministic algorithms.

## Diagnostic integrity gate

Self runs first for all original views/splits and must reproduce C253 intact raw256-way logits
within1e-9 and argmax arrays exactly before scoring altered modes. Restored must reproduce self.
For query_blind inputs the paired query prompts are identical:require saved paired post tensors
to be exactly equal and query-swapped outputs to reproduce self. This is a structural negative
control,not a requirement that the model answer correctly.

Check the complete model fingerprint after every head call;parameters remain frozen.
Require24 LayerNorm and24 decoder calls per model,1152 head rows. Hook cleanup occurs on exceptions.
Any source/artifact/schema/donor/nonfinite/replay/test/count fault is INVALID / RETRY SAME C254.
PASS means diagnostic integrity,no threshold on accuracy changes,donor-target agreement or model
success. C252 and C253 verdicts remain unchanged. No automatic C255 or Gate F promotion.

## Metrics, accounting and saved artifacts

Use actual C253.metrics for normal accuracy,NLL,fact/query/order pairs and original mask scores.
Report all80 mode/seed/split/language cells. For both changed modes versus self,40 contrast cells
record original/changed correct counts,flips,wrong-to-correct,correct-to-wrong,accuracy/NLL deltas,
and donor-target matches. Shared questions and seeds are correlated observations,not independent samples.

5 models x4 modes x2 splits x3 views=120 head evaluations/5760 head rows.
Full-model/encoder/core/reader forwards0;training0;new learned checkpoint writes0.
One C252 checkpoint bundle deserialization and five strict model-state loads in the scientific run.
Precheck and postcheck repeat parent archive reads and metric validation;these reads are not zero
cost,not additional independent trials,and not full-model forwards. Historical test fixtures are
separate work and can execute their own toy/historical model computations.

Five ignored outputs:swap-plan.json,head-outputs.pt,diagnostics.json,contrasts.json,validation-summary.json.
head-outputs.pt schema fold-c254-head-outputs-v1 stores five ordered records of head logits,counters,
weight identities and replay flags. It contains no trained parameters. Postcheck reloads original
parent evidence and the new output archive,reconstructs all metrics/contrasts/replay controls,
compares JSON exactly and verifies hashes/sizes without new head or model forwards.

## Protection and review

Inherit C253364 source pins/587 inputs;add its summary+five artifacts and OWN6:
370 source pins/599 protected inputs. Explicit deciding-path union30:five C231 LM_SOURCES plus
C230 through C254 helper/entry modules. No accepted sources/tests/logs/shared launcher are edited.
Own tests24;modules139;loaded3266/focused3265. Only inherited exact historical exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Own counts/IDs and runtime suite construction are checked semantically,not by source-literal matches.

OWN6:benchmark model_c254_paired_residual_swap.py,test_v05_c254_paired_residual_swap.py,
tools/run_c254.ps1,tools/invoke_c254.ps1,this preregistration,docs/v5b-paired-residual-swap-v0.1.md.
Manifest SHA256:cfbf05fc55fe6c87a0b738bfab7f4c676bb75ed503883cb399898f7936641276.

After all six files are committed,re-fetch remote bytes,compare source/script blob hashes to the
actual tested complete files,rerun exact24 own tests,compile/import and audit free globals,donor
semantics,source protection,parent signatures,head-only accounting,CLI indices and parser ordering.
Self-contained synthetic own tests are not a full-checkout regression or actual trained-model run.
Record actual checks and pending authoritative Windows/accepted-artifact checks before activation.

## Interpretation and stop

Query-swap sensitivity relative to order-swap sensitivity can support query-specific dependence
under this intervention. It does not prove a unique internal algorithm,training-time necessity,
external generalization or architectural superiority. Permutation preserves residual marginal
statistics but changes their joint pairing with reader features;nonlinear LayerNorm/co-adaptation
can still matter. Weak sensitivity does not prove all core computations irrelevant.

Dispatcher/launcher/runner ParseFile precede Python/source/archive precheck,24 own tests,3265
focused tests,head diagnostic,postcheck and publication. Operational branch/tree/HEAD/ACTIVE
mismatch skips before logging. Repair log-only transport without repeated head evaluation.
No paid API,external corpus,model expansion,production adoption,cleanup or history rewrite.
Numeric-memory and erasure-mixture tuning remain paused. Judge C254 before C255.
