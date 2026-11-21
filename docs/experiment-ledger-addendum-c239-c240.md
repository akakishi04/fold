# C239 acceptance and C240 positional-rule audit boundary

## Formal verdict

**C239 ACCEPTED VALID NEGATIVE — learned TRAIN order, failed held-out order.**
C238 remains ACCEPTED PASS for fitting16 seen prompts. Gate E PASSED; Gate F NOT PASSED.
Neither Full nor GRU-only satisfies the registered order-transfer gate.

Scientific execution HEAD: `c847609c8d045c9c5db4ec882bf336a9671180ff`.
Published log commit: `5207d3b378ae56502a78dc9a5bb6f843cf389795`.
Publisher-recorded log SHA256: `9e139f0544b49cb1185ce285a7b7c2c7ccb5ad394198040be4845648aa3697ee`.
Log bytes:545773. Summary SHA256:
`500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af`.
Local summary: `runs/c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5/summary.json`.

The log commit is one commit after execution and changes only c239/latest.log/latest.json.
Acceptance uses retrieved log ranges and recorded user-local postcheck, not an independent
checkpoint rerun or full-log byte rehash. Preserve original evidence and do not rerun C239.

## Execution validity

24 own tests PASS in4.351s;2905 focused tests PASS in78.219s.
Python syntax, parent/source/artifact/partition prechecks and training AST checks PASS.
280 source pins/418 protected inputs. All6 models completed400 updates:2400 training steps,
76800 training answer presentations,2490 total forwards and77520 total row presentations.
Initial-state guards, checkpoint/prediction replays, changed weights and non-mutating evaluation
passed. Persisted partition/initial-identity replay PASS; inputs preserved; tracked tree clean;
execution HEAD preserved; run_execution_valid=True.
Scientific status FAIL; full_order_gate=False; gru_order_gate=False.

## Deciding metrics

All12 seed/family/language cells pass every TRAIN criterion:accuracy4/4, fact/query pairs2/2,
evidence/query drops0.50. Every cell is ORDER_HOLDOUT_MISS, not TRAIN_FIT_MISS.
HOLDOUT exact correct counts (4 questions per language):

| Seed | Full EN | Full JA | GRU-only EN | GRU-only JA |
|---:|---:|---:|---:|---:|
|234001|1/4|1/4|0/4|1/4|
|234002|0/4|0/4|0/4|0/4|
|234003|0/4|0/4|1/4|0/4|

Every HOLDOUT fact/query pair both-correct score is0/2. Masked accuracy is0.50; the corresponding
normal-minus-mask drops are-0.25 or-0.50. HOLDOUT answer NLL spans5.580094-8.135931 at logged precision;
TRAIN NLL spans0.000383-0.000753. All unchanged registered holdout criteria fail.

## Interpretation and non-claims

The fixed complete-cohort recipe fits the learned order but does not transfer to the reversed
presentation of the same facts. This separates successful fitting from this specific generalization
failure. C238 was not invalidated:its seen-prompt claim remains correct and was narrower.

C239 does not prove prompt-table memorization, a particular positional algorithm, architecture-wide
impossibility, a unique encoder/readout cause, or Full/GRU superiority. Failure on a four-question
cell is not a formal chance/significance test. The restricted training order confounds entity
identity with its position. A positional-shortcut explanation is plausible but not yet established.
An incorrect byte need not be the other supplied digit:inspect saved predictions before claiming so.

## Accepted artifacts

- holdout-plan.json:4eca2f0276b521286729f1819abd929a035659a589488b332fe976d392b4dac0 (2640 bytes)
- measurements.json:872e534c5fb5f26fede0c4947b34344adc39a8e956bc453fed96763e757677c8 (12444 bytes)
- split-dataset.json:6f47a61c0ec4de616e77dab803ad964a9243e627b8a06f3e987d2824f8951731 (2676 bytes)
- trained-models.pt:2e3cf24b8feabead8f7470ebf271d27347ed0cf79aa873c30be68329a833d687 (601940 bytes)
- validation-summary.json:c65f6e6226630e5017c5cfa240116ad76106ec07a490d053216bde0a9a8b1849 (335 bytes)

## Next question — saved-prediction positional-rule audit

Without any new training or inference, do C239's exact saved answers match an explicit
query-to-fixed-position rule, correct entity binding, always-first/last selection or constant-digit
responses? Match TRAIN/HOLDOUT counterparts and report wrong-other-entity versus out-of-value bytes.
Recompute all discrete parent metrics from all three saved prediction views before interpretation.

This is descriptive analysis of already accepted outputs, not an additional capability trial or
independent evidence sample. A matching rule does not prove the model internally executes it.
On TRAIN, correct binding and the fixed-position rule coincide; on this binary HOLDOUT the latter
coincides with the other entity's value. Report these identifiability limits explicitly.
Do not recompute NLL without logits, invert model answers as a repair, load/train checkpoints,
change C239 or promote Gate F. Separate C240 preregistration/review controls activation.
