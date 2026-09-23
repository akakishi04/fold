# C245 preregistration — frozen selective evidence

Experiment:C245-v5b-frozen-selective-evidence.
Stage:V5-B-FROZEN-SELECTIVE-EVIDENCE.
C244 ACCEPTED VALID NEGATIVE; C246 NOT REGISTERED. Gate E PASSED; Gate F NOT PASSED.
This document registers C245. The authoritative handoff activates it only after committed-byte review.

## One question

With all six C244 final models frozen, how do their answers/scores respond to erasing the queried
entity's value versus erasing only the other entity's value? This is a diagnostic, not training,
capability improvement, a unique causal-mechanism attribution or a new architecture comparison.

## Accepted parent

Acceptance/base commit:2d7fc4fabee22a7a5f718748756b952deb979f25.
Acceptance record:docs/experiment-ledger-addendum-c244-c245.md.
C244 scientific execution HEAD:d89007bc5a04c4f6b99bff966093b0e14174e04b.
Published log commit:d1e2933492cf4f4d0cbfb535c80b800c58bcadf7.
Publisher log SHA256:fad665eeb8a89322079f21425b89ae28336567574a47043b10a479303780b158.
Summary SHA256:a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297.
Local summary:runs/c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639/summary.json.
Require the exact execution-valid FAIL with cell_outcomes RECOMBINATION_MISS:12.

C244 artifacts:
- measurements.json:cd0fba1897aea554a74b984622f97fa93399baadda4fff5a757e1bfdbd24239d
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
- trained-models.pt:90c367dc4026e757ed561af75a25d529d37dd9fea404d4d6370f1bac5211b519
- two-partner-plan.json:e89a41c15ef3d702c7009a9b4fc22f4e28809dea3892c5d63cf02120a1e10b0b
- validation-summary.json:b80fea969f5329fc401c0be3470233ae50dd55319b3a83c0e0047a5fe4c0808f

Call the actual C244.validate_result on its summary. Call C244.summarize(refs,fitting), where
fitting is C242 from C244.context(), to reproduce its saved validation_summary. The parent writer
stores final[split][language], predictions[split][view] and final_sha256 after400 updates and
checks these after checkpoint reload. Use these final fields, not initial_train or initial_sha256.
Identity order is234001/full,234001/gru_only,234002/full,234002/gru_only,234003/full,234003/gru_only.

Deserialize the accepted bundle only through C244.load_bundle (schema fold-c244-two-partner-v1,
six ordered states, CPU weights_only loading). Construct the same model containers, strictly load
each state, set eval/requires_grad=False and require its actual fingerprint to equal final_sha256.
There are no new initial-state experiments, optimizer operations or writes of model checkpoints.

## Inputs, changed conditions and fixed controls

Keep the exact C244 TRAIN64/HOLDOUT32, names, digits, query, order, targets and source provenance.
Retain normal/evidence_blind/query_blind original views. Add queried_value_blind and
other_value_blind by replacing one factual ASCII digit with '?' in the real C234-rendered prompt.
Follow the queried object's identity through reversed fact order. Names and the final query are
unchanged. Use no target label to select the field. UTF-8 byte length and EOS position are preserved.

For all views use actual C231.prefix_tensor. Original tensors/targets must equal C234.tensors.
Selective tensors must differ from normal at exactly one token whose new value is byte63.
Targets remain scoring references only; they are never added to model input. The output is an
unrestricted argmax over256 real bytes, not a filtered candidate choice.

Audit identical-input best-lookup ceilings from the fixed row set:
queried_value_blind:TRAIN0.50/HOLDOUT1.00; other_value_blind:1.00 on both splits.
These are finite-dataset redundancy properties, not learned-model results or gate thresholds.
In particular HOLDOUT's pairs0/3 and1/2 permit an oracle to infer the erased queried value from
the remaining value. Selective masks were absent from training. Distribution shift and redundant
information prevent treating high/low selective accuracy as a unique mechanism diagnosis.

## Measurements and original replay

Actual model calls directly use the same token tensors, zero task IDs, eval/no_grad and CPU
float64 as the parent evaluator. Original metrics are reconstructed with actual C234.metrics
plus the same C242 order-pair formula. Match every original metric key including answer_nll and
both masked accuracies/drops within1e-9; require exact original argmax arrays for all three views.
There is no requirement that new selective answers equal the parent answers.

For each seed/family/split/language and every view report:correct,accuracy,answer_nll,
accuracy_drop=normal-view,answer_flips,correct_to_wrong,wrong_to_correct,nll_increase=view-normal,
and logit_linf=max absolute drift from normal. Preserve raw logits for all five views, both splits
and all six models. Postcheck reconstructs these statistics and original metrics from saved logits.
No extra model inference is needed for postcheck. Raw common logit shifts are not probability
changes; use accuracy, flips and loss together instead of a lone drift-based importance claim.

All correctness metrics reference the original complete prompt's target. For erased prompts,
that is a descriptive scoring convention, not a claim of uniquely answerable questions.
No positive or negative threshold on selective accuracy controls C245 PASS.

## Workload and validity gate

6 models x2 splits x5 views =60 forwards.6x(64+32)x5=2880 row presentations.
Each model10 forwards/480 rows.24 model/split/language cells, each with5-view statistics.
One accepted checkpoint bundle load containing six states; new training steps0, checkpoint writes0,
scientific network calls0. Root forward hooks count actual calls/rows and are removed on failure.
Parameters must have no gradients and remain frozen/eval. Fingerprints must match parent finals
before inference and remain unchanged afterward. Shapes must be n-by256 finite CPU float64.

PASS means diagnostic integrity only:source/input identity, valid masks/token parity, parent
prediction/metric replay, frozen states, complete fixed workload, finite outputs and exact
persisted-diagnostic reconstruction. Any fault is INVALID / RETRY SAME C245. Different selective
responses or no selective difference are both valid outcomes. C244 and Gate F remain unchanged.

## Protection, outputs and tests

Inherit C244310 source pins/478 inputs; add its summary+five artifacts and OWN6:
316 source pins/490 protected inputs. Reject duplicate parent/OWN paths. Direct dependency union21:
five C231 LM_SOURCES plus C230 through C245 helper/entry modules, including lazy imports.
No accepted parent source/test/log or shared launcher is modified.

OWN6:the C245 benchmark, test, runner, launcher, this preregistration and
 docs/v5b-selective-evidence-v0.1.md.
Own tests24;modules130;loaded3050/focused3049. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Actual suite/ID counts are enforced; a constructed-suite test is not a historical-suite execution.

Five ignored outputs:diagnostic-plan.json,intervention-inputs.json,outputs.json,diagnostics.json,
validation-summary.json. outputs.json stores per-model identity, frozen fingerprints, counters,
original metric error and raw logits keyed by split/view. The logits occupy737280 float64 values
(5898240 raw numeric bytes before JSON and metadata); actual serialized sizes are recorded rather
than equating this payload size to peak memory. Do not commit generated arrays or checkpoints.
Postcheck revalidates original inputs, hashes/sizes, plan, fingerprints, parent replay, all24 cells
and every derived metric from persisted logits. Only console log and receipt go to c245/latest.*.

Manifest SHA256:50cadf2e5b9bc0c1a1fab5f29652afd5b5c2f0eeaed3be919cdadb3ebcebf1ac.

## Authoring review and stop

Re-fetch all six committed OWN files after authoring; match complete local code/script Git blob
hashes to remote identities; compile/import; run24 own tests; audit free globals, actual parent
writer semantics, metric keys, mask positions, token parity, loader/state-load/freeze order,
counts, embedded Python argv and parser/publication boundaries. Synthetic model/data tests are
not the actual C244 checkpoint run. Record actual checks and pending checks in the handoff.

Standard path:dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile -> Python /
source/parent/input precheck ->24 own tests ->3049 focused tests ->C245 ->postcheck ->log publication.
Branch/tree/stale-HEAD/ACTIVE mismatch skips before logging. Full Windows AST, historical regression
and accepted local artifacts are not reported PASS before execution. No test bypass, answer
correction, extra training, larger model, paid API, external corpus, cleanup, history rewrite or
production modification. Repair transport-only failure without repeating completed inference.
Gate F NOT PASSED; numeric-memory tuning paused. Judge C245 before C246 registration.
