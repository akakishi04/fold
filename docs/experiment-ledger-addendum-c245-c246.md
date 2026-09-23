# C245 acceptance and C246 training-only distractor-erasure boundary

## Formal verdict

**C245 ACCEPTED PASS — diagnostic integrity only.**
C244 remains ACCEPTED VALID NEGATIVE. Gate E PASSED; Gate F NOT PASSED.
No model improvement, new generalization or unique causal mechanism is accepted by this diagnostic.

Scientific execution HEAD:db838801cc139b4578c2aa002cbc001c58fa1e91.
Published log commit:4ef5145ef98617183761d80652135466479394e7.
Publisher-recorded log SHA256:3f1c23b26b97029dc326a8007616aade19741896f443bbbf79c5221fe02abb13.
Log bytes:590659.
Summary SHA256:ae2f2a940a7c9f903bac8f8f472680654abe305df897d011e61a355e4d9d9d88.
Local summary:runs/c245-v5b-selective-evidence-484b9afa921e4fe4a3430a1d7a88e4d4/summary.json.

The publication is one commit after execution and changes only c245/latest.log/latest.json.
Acceptance uses immutable retrieved log ranges and recorded user-local postcheck, not a reviewer
rerun of actual checkpoints or an independent full-log byte rehash.

## Execution validity

24 own tests PASS in3.542s;3049 focused tests PASS in94.725s.
316 source pins/490 inputs protected. Six frozen C244 models completed60 forwards/2880 row
presentations, with zero new training and zero checkpoint writes. All original-view predictions
and metrics including NLL replayed, all fingerprints remained unchanged, and persisted logits
reconstructed the diagnostic. Tracked tree clean;execution HEAD preserved;run_execution_valid=True.

## Deciding measurements

Counts pooled over3 seeds x2 languages; each family has96 HOLDOUT answers.

| Family | Normal | Queried value hidden | Other value hidden |
|---|---:|---:|---:|
|Full|39/96|4/96|59/96|
|GRU-only|41/96|2/96|82/96|
|Both, descriptive pooling only|80/192|6/192|141/192|

Hiding the queried value reduced HOLDOUT accuracy in all12 cells. Hiding only the other value
increased it in all12 cells. For other-value erasure,64 normal-wrong answers became correct while
3 normal-correct answers became wrong, a net gain of61. These are paired input interventions on
fixed models, not additional independent training replicates.

Full HOLDOUT other-hidden accuracy by seed EN/JA:234001 9/16,10/16;234002 9/16,8/16;
234003 10/16,13/16. GRU-only:234001 16/16,16/16;234002 12/16,13/16;234003 12/16,13/16.

TRAIN normal accuracy remains100%. Other-value erasure gives Full118/192 and GRU-only164/192;
its effect is therefore not uniformly beneficial across the original TRAIN/HOLDOUT inputs.

## Interpretation and limits

The results support investigating sensitivity to the nonqueried factual value. They do not prove
that a named component is defective or that the model learned a clean internal binding algorithm.
Selective '?' inputs were not in training. Removing a value also identifies the remaining value
as the answer-bearing field, creating an easier copy-style input; that is not ordinary task success.

Critically, when the other value is hidden, the distinct masked prompt sets in TRAIN and HOLDOUT
coincide:all query/entity/value/order/language combinations are already represented. TRAIN repeats
each masked form twice and HOLDOUT once. The matching masked scores are thus not evidence of
held-pair generalization. Original unmasked HOLDOUT remains the capability endpoint.

Queried-value masking also has different ambiguity properties across splits:TRAIN's exact
identical-input ceiling is50%, HOLDOUT's100% due to its pair structure. Do not treat accuracy on
these inputs as a common chance level. No input-mask production fix is adopted here.

## Accepted artifacts

- diagnostic-plan.json:50cadf2e5b9bc0c1a1fab5f29652afd5b5c2f0eeaed3be919cdadb3ebcebf1ac
- diagnostics.json:231a1d10b186a0d57be227ab4dd38829ee459d142926e7be2859dd88b6fdd048
- intervention-inputs.json:91e207dde4e080a52040bcf39b6f1236af7053a703a684ba94a8c6c47dfe0c22
- outputs.json:aaab0bc28bf01aed325d4bbe55cd89b00e7ea2957b8db5f0930aa350da862607
- validation-summary.json:2dc4f24dd318dd37ed848994b175bb929d830f7c70549d95df492feedaa3d8a3

## Next question, not registration

Can training-only erasure of the nonqueried value on half the scheduled presentations improve
normal, fully observed HOLDOUT performance at the exact C244 architecture, initial states,
partition, row schedule, optimizer and400-update/76800-presentation budget?

Use fresh models, not continued C244 checkpoints. Keep the original old/added block row schedule.
In a four-update cycle use masked-old,masked-added,normal-old,normal-added. Each of64 TRAIN rows
receives100 normal and100 other-hidden presentations. Final update is normal-added.
There is no extra auxiliary forward/loss, larger batch or new data. Apply erasure using the visible
query, not the target label. Its explicit selection cue is training supervision and must be disclosed.

Judge only the original normal/evidence-blind/query-blind evaluation inputs and unchanged C244
criteria on the identical TRAIN64/HOLDOUT32. Do not use selectively masked HOLDOUT as success
or introduce a query-conditioned mask at normal inference. Compare with C244's saved same-row
metrics. This may fail if the model learns a separate easy masked task without transferring it.
C246 requires separate preregistration and committed-byte authoring review before activation.
