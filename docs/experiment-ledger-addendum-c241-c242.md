# C241 acceptance and C242 balanced recombination boundary

## Formal verdict

**C241 ACCEPTED VALID NEGATIVE.** Gate E PASSED; Gate F NOT PASSED.
C240 remains diagnostic-integrity PASS; C239 remains a valid order-transfer negative;
C238 remains PASS only for fitting the seen16 prompts.

Scientific execution HEAD: `b7b33718da1edd94cc1ed113baa6e56cc27dc3e4`.
Published log commit: `a53a96e6e2ec716d33ab3f7f8ae9cb2d49d110a0`.
Publisher-recorded log SHA256: `5067ca2deefdc14b03e72500918bc2eae134f8a01b1751e1be450a93275f50f8`.
Log bytes:558381.
Summary SHA256: `b228992dfd5d85e59d7c45d1dd899145588978a19ade0817a547d740e8c67e26`.
Local summary: `runs/c241-v5b-assignment-holdout-445ca70720c948e7966236416922e580/summary.json`.

The publication is one commit after execution and changes only c241/latest.log/latest.json.
Acceptance uses retrieved log ranges, publisher metadata and recorded user-local postcheck.
The reviewer did not rerun the six checkpoints or independently rehash the entire log stream.

## Validity and deciding metrics

24 own tests PASS in3.739s;2953 focused tests completed successfully in92.184s.
292 source pins/442 inputs protected. Six fresh models completed400 updates each:
2400 steps/76800 training presentations/2490 total forwards/77520 total rows.
All checkpoint/prediction replays and weight-update checks PASS; persisted partition/initial-ID
postcheck PASS. Tracked tree clean; execution HEAD preserved; run_execution_valid=True.
Scientific status FAIL; full_assignment_gate=False; gru_assignment_gate=False.

All12 seed/family/language cells have identical decisive outcomes:

| Metric | TRAIN | HOLDOUT |
|---|---:|---:|
| Exact accuracy |4/4 (100%)|0/4 (0%)|
| Query-pair both-correct |2/2|0/2|
| Order-pair both-correct |2/2|0/2|
| Evidence-mask accuracy drop |0|0|
| Query-mask accuracy drop |0.50|-0.50|

TRAIN answer NLL is0.000558-0.000726; HOLDOUT8.126891-8.705085, at printed precision.
cell_outcomes is exactly TRAIN_FIT_MISS:12. This is NOT a statement that normal TRAIN answers
were wrong:TRAIN full criteria failed solely because the evidence-mask drop was0, below0.35.
Do not relabel these cells ASSIGNMENT_HOLDOUT_MISS, which requires the full TRAIN gate to pass.

## Interpretation and design limitation

The new models fit the training assignment across both positions, but do not demonstrate use of
its changing factual values:removing those values leaves TRAIN accuracy100%, and reversing the
assignment yields0%. This is consistent with the preregistered fixed entity-value shortcut.
The aggregate scores alone do not identify exact erroneous bytes or a unique internal algorithm.
No claim about every HOLDOUT answer equaling a particular digit is made without saved-byte analysis.

C241 intentionally held TRAIN assignment fixed at box=0/book=1. That makes evidence redundant for
minimizing TRAIN loss:query identity alone predicts the target. The experiment usefully exposed
this failure, but cannot by itself decide whether the architecture could learn binding from a
training distribution that requires varying both assignment and order. The prior recommendation
removed a position shortcut but left a value shortcut. This is a limitation of the experiment
we designed, not evidence that the architecture alone caused the outcome.

No verdict rescue, extra training, seed selection, threshold relaxation, core ranking, general
language claim or Gate F promotion. Preserve the accepted parent source and failed scientific gate.

## Accepted artifacts

- assignment-plan.json:1552239e7701744af508ba41ac4b620898d219380b377be1c5671b816dbac1f8
- measurements.json:2ad0f83840e01fa2f074b0a313261b8c662ec4d40a9c8a13d0a24be0c0506111
- split-dataset.json:1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a
- trained-models.pt:102102b1f7318ca1fc720afda96c9118a526ea48eb007ef8ed76bfa586dca9aa
- validation-summary.json:389555ca1313aa86e3635a28397ac98613206373b9b6bbe15eaf1e69a2889917

## Next question, not registration

Use the existing C234 byte-identical dataset restricted to box/book, with digits0,1,2,3.
TRAIN32 contains ordered assignments(0,1),(1,0),(2,3),(3,2), each with both fact orders,
both queried entities and both languages. HOLDOUT64 contains the other8 ordered distinct-value
assignments, with the same orders/queries/languages. Every individual digit and entity/value
combination appears during training; only the cross-pair combinations are held out.

Question:can fresh models trained with both variable values and positions solve held-out pair
recombinations under the fixed400-step,32-row complete-cohort budget?
Fixed query-only/constant predictors cannot exceed25% on TRAIN; fixed-position/first/last
predictors reach50%. Audit these ceilings before training. No unseen vocabulary is claimed.

Training uses every TRAIN row once/update instead of repeating8 rows4 times. Total training
presentations stay fixed, but row diversity and repeat count change, so this is not an isolated
causal comparison to C241. The training set is not expanded after observing C242 results.
A fresh model never inherits weights trained on its HOLDOUT. The original source split labels
remain provenance; the new split is explicit. C241's verdict is unchanged.

Separate C242 preregistration and committed-byte authoring review are required before activation.
