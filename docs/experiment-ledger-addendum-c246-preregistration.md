# C246 preregistration — training-only distractor erasure

Experiment:C246-v5b-training-only-distractor-erasure.
Stage:V5-B-TRAINING-ONLY-DISTRACTOR-ERASURE.
C245 ACCEPTED PASS for diagnostic integrity only; C244 remains ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED. C247 NOT REGISTERED.
This document registers C246; authoritative handoff activation requires committed-byte review.

## One scientific question

At identical C244 initial states, task partition, row schedule, optimizer and training budget,
does training on other-value-erased prompts for half the scheduled presentations improve the
original normal-input held-pair endpoint? No selective mask is applied as an inference repair.

## Parent identity and schema

Acceptance/base commit:87fe39481ae65cdf2452f2cb79ba0b8f6d912a2a.
Acceptance record:docs/experiment-ledger-addendum-c245-c246.md.
C245 scientific execution HEAD:db838801cc139b4578c2aa002cbc001c58fa1e91.
Published log commit:4ef5145ef98617183761d80652135466479394e7.
Publisher log SHA256:3f1c23b26b97029dc326a8007616aade19741896f443bbbf79c5221fe02abb13.
C245 summary SHA256:ae2f2a940a7c9f903bac8f8f472680654abe305df897d011e61a355e4d9d9d88.
Local summary:runs/c245-v5b-selective-evidence-484b9afa921e4fe4a3430a1d7a88e4d4/summary.json.
Require actual C245.validate_result on this exact summary and its execution identity/status PASS.

C245 artifacts, required byte-identical:
- diagnostic-plan.json:50cadf2e5b9bc0c1a1fab5f29652afd5b5c2f0eeaed3be919cdadb3ebcebf1ac
- diagnostics.json:231a1d10b186a0d57be227ab4dd38829ee459d142926e7be2859dd88b6fdd048
- intervention-inputs.json:91e207dde4e080a52040bcf39b6f1236af7053a703a684ba94a8c6c47dfe0c22
- outputs.json:aaab0bc28bf01aed325d4bbe55cd89b00e7ea2957b8db5f0930aa350da862607
- validation-summary.json:2dc4f24dd318dd37ed848994b175bb929d830f7c70549d95df492feedaa3d8a3

C244 is already an inherited protected input:
runs/c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639/summary.json.
SHA256:a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297.
Its exact split hash:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
C246.load_inputs calls C245.load_inputs with the C244 summary, NOT the C245 summary. That loader
validates C244 measurements using C244.summarize(refs,C242) and the final-field schema.
C246 additionally checks six ordered identities, valid initial_sha256 and initial!=final.
C244's writer stored initial_sha256 before training; these fingerprints initialize the new experiment.
Final/predictions are post400-update comparator evidence. No trained parent state is loaded.

Context roles are explicit:C245 parent,C244 base,C242 fitting,C234 binding,C231 factory,audit helper.
Keep all directly called/lazily imported repository modules protected, not just the visible entry.

## Fixed partition, intervention and schedule

Preserve C244 TRAIN64/HOLDOUT32 exactly, including row order, IDs, prompts, labels and provenance.
Old TRAIN block32 is the first half; added block32 the second half. No HOLDOUT promotion.
Create two TRAIN input tensors per row:normal and other_value_blind, via actual C245.masked_prompt
and C245.tensors using actual C234 renderer/C231 prefix_tensor. Replace exactly one factual digit
with '?' based on the already-visible queried entity. No target label is used in that selection.
The remaining visible value is an explicit relevance/copying cue; this supervision is disclosed.
Keep query, byte length, EOS position and all other input tokens fixed.

Original C244 row indices stay identical at every step:zero-based even step selects0..31,
odd step selects32..63. Only the view changes in the fixed four-step cycle:
masked-old,masked-added,normal-old,normal-added. Repeat100 times; final step400 is normal-added.
Each block receives200 updates, with100 per view. Each TRAIN row gets100 normal plus100 masked
presentations. block_view_updates matrix order is block[old,added] x view[normal,other-hidden],
exactly[[100,100],[100,100]] for each model. No phase reversal or schedule tuning after results.
An independent forward hook verifies actual tokens against accepted C244 row indices and the
registered view at every optimizer call. No separate block/step/row ID is model input.

No actual normal HOLDOUT string equals a TRAIN normal or augmented string. Selectively masked
HOLDOUT strings WOULD coincide with TRAIN masked forms, so no such score is a capability endpoint.
Original evidence/query masks remain inherited controls. Do not label their overlap as unseen
capability. Only TRAIN is evaluated before fitting; normal HOLDOUT first reaches evaluation after
step400 and replay. No held-out tuning, selection, early stop, extra steps or favorable seed.

## Fixed model/optimizer and changed quantities

Fresh seeds234001/234002/234003, seed/full then seed/gru_only. Full13488/GRU-only10160 parameters,
width16,48 slots,unrestricted256-way output. Match C244 initial fingerprints. Construct common-
weight GRU-only copy before either paired fit. No continuation from C244/C245 trained states.
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 updates,CPU float64,
threads2,deterministic algorithms. Targets and answer cross-entropy stay unchanged.

The fit executable AST equals C244.fit except the progress label and wrapping the model's input
in select_view. The validation requires exactly that single input-expression change and identical
STEPS/BATCH/LR/CLIP/TOL, plus row-index parity for every one of400 updates.
No additional auxiliary loss or model forward per update. Normal presentations halve and masked
presentations replace them; total presentations remain fixed. This recipe does not isolate which
of copying cues, distractor sensitivity, input variation or fewer normal exposures explains results.

## Endpoint, unchanged gate and comparison

Use actual C242.evaluate/validate_metrics/cell_pass and underlying C234 normal/evidence_blind/
query_blind rendering, plus accepted C244.summarize and replay_one with their fitting argument.
C246 summarizes by renaming only the family gate keys to full_augmentation_gate and
gru_augmentation_gate, and adds the two view presentation totals. Parent schema is not guessed.

All Full seed/language cells must satisfy BOTH TRAIN/HOLDOUT:
normal accuracy>=0.90; fact/query/order pair scores>=0.80; evidence/query drops>=0.35.
TRAIN32 rows/language and16 pairs per kind:minima29/32 and13/16.
HOLDOUT16 rows/language and8 pairs per kind:minima15/16 and7/8.
GRU-only gate remains independent. TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS retain original
meaning. A valid primary miss is ACCEPTED VALID NEGATIVE; integrity faults are INVALID / RETRY SAME C246.

Store C244.final unchanged as c244_comparator for both identical partitions. Report each
seed/language normal accuracy and delta; do not substitute selective C245 performance or a different
subset. This is reused accepted evidence, not an independent replicated baseline. Parent NLL is
recorded evidence, not a new parent inference. New checkpoint replay includes new logits/NLL.

## Workload, integrity and storage

6x400=2400 training updates/76800 presentations,38400 normal and38400 masked.
Per model:initial TRAIN3/192 rows,final TRAIN3+HOLDOUT3/288 rows,replay both/288 rows.
90 scoring forwards/4608 scoring rows;2490 total forwards/81408 total rows.
Before reload409/13280;after415/13568 per model. One new six-state bundle, no parent checkpoint
load or model forward. Scientific network calls0. Test-fixture computation is outside these totals.

Require exact initial IDs, changed weights, non-mutating scoring, observed row/view counts,
strict checkpoint schema/order/final identity, exact prediction replay and logit/metric error<=1e-9.
Schema:fold-c246-training-erasure-v1. Postcheck verifies input/artifact hashes/sizes, plan, partition,
initial/comparator identities, summary and child discrete metrics using C243.discrete_metrics.
No extra model forward in postcheck. No accepted source, test, log or shared launcher is edited.

Inherit C245316 source pins/490 inputs; add its summary+five artifacts and OWN6:
322 source pins/502 inputs. C244 summary/artifacts are already inherited and are not double-counted.
Direct dependency union22:five C231 LM_SOURCES plus C230 through C246 entry/helper modules.
Own tests24;modules131;loaded3074/focused3073 with only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Actual historical loader enforces unique IDs/counts; a synthetic suite is not a full regression run.

OWN6:the C246 benchmark,test,runner,launcher,this preregistration and docs/v5b-training-erasure-v0.1.md.
Ignored local outputs:training-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Measurements retain initial_train,final,predictions,fit,fingerprints,
block_updates,block_view_updates and c244_comparator. Only console log/receipt go to c246/latest.*.
Manifest SHA256:761b00863243d9118cd85058f585b7e3592404c677b8d8f548be45ed2fd05db8.

## Review and stop

Re-fetch all six committed files; match tested code/script blob identities, compile/import,
rerun24 own tests, audit free globals, parent writer/loader/summarizer semantics, fit AST, schedule,
mask-token parity, data overlap, evaluator endpoint, counters, CLI argv and parser/publication order.
Record exact review HEAD, performed checks and limitations. Synthetic models/parent excerpts do
not establish actual C246 capability or a full-checkout historical test pass.

Execution:dispatcher/launcher/runner ParseFile -> Python/source/parent/input precheck ->24 own tests
->3073 focused tests ->C246 training ->artifact postcheck ->remote log publication.
Operational branch/tree/stale-HEAD/ACTIVE mismatches skip before execution/publication. Stop same
C246 on integrity faults; transport-only failures do not justify retraining. No inference mask
repair, extra steps, larger model, paid API, external corpus, cleanup/history rewrite or production
change. Gate F NOT PASSED;numeric-memory tuning paused. Judge C246 before C247 registration.
