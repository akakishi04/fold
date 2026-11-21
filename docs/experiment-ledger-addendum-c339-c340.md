# C339 acceptance and C340 preparation boundary

Date: 2026-10-26 Japan time.
C339 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C338 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. No production adoption. C340 not authorized by this acceptance.

## Execution identity and audit boundary

Execution f58c22f83fe7c41c451d5d0bcf26c249ab21908b.
Publication 71585b7eb2da7685915bb30b43376b1ea1ffec9b; sole parent equals execution.
Metadata: docs/experiment-run-logs/c339/latest.json.
Log: docs/experiment-run-logs/c339/latest.log.
Publisher reports1162990Windowsbytes, SHA256
cbeeda6e5743c753e77deaacb17944384a7cba2e765e093a769c8aea211d3121.
Git log blob1fad3a0a07f7cef539af69b01fd86f39d7793cd4.
The >1MB Contents endpoint returned empty content; the Git blob GET supplied the
actual decoded log. Empty Contents content was NOT interpreted as an empty run.

Full6202tests/229modules passed,0failures/errors/skips,2178.897seconds including
process orchestration. Ordered-ID SHA:
b5d92857cbb2c72d61a1e2a9af242f57e283fd7c26e5e6e86661d6cbdb35fbf4.
Native locks, parent reconstruction, saved diagnosis,all5769final uncached rereads,
independent verifier895sources/5769inputs, science/verifyexit0 and
run_execution_valid=true were inspected. Diagnostic51840answers/25920pairedanswers,
10states,720strata/360pairedstrata; new model forwards/updates0.

Folder runs/c339-support-transfer-38b97ac63a92445cb0b212d1fe9a73fe/.
Primary science/summary.json SHA:
304dec1fcbb6532da968fd21c337f39079f4abb1cc305893722e466636ef4dbf.
Envelope SHA:
db81d2dba1bd8a1b2f850c3b5a7833a9b95b7a24d8cddc984fc1e3a5e1195be3.
Manifest3f3380eac1a0e5d0c076825081c10edfa86bed75e02b2c1b5ee23ebf21dc42f1.
A successor must preserve467parent outputs:4science+summary+envelope+461regression
proofs(3records+229module JSON/logpairs), not merely the scientific summary.

Remote review inspected metadata,lineage,startup/fullregression/terminalverification
and selected deciding strata/transitions,especially seed338004 and adjacent338003.
This is not an independent whole-Windows-log rehash, all720strata audit, local receipt
rehash, raw-logit recomputation, model replay or claim of exhaustive mechanistic proof.
The native executor/fresh verifier performed the complete registered reconciliation.

## Deciding example: seed338004, original6, shared_suffix

These are explicitly SELECTED strata, not a pooled all-seed effect.

|Language/split|Arm|Answers|Correct|Absent digit|Wrong observed|Support NLL|Within-pair NLL|
|---|---|---:|---:|---:|---:|---:|---:|
|English TRAIN|native|96|96|0|0|0.00005805120435|0.001818936639|
|English TRAIN|support_loss|96|92|0|4|0.00002555873797|0.098734314608|
|Japanese TRAIN|native|96|77|0|19|0.00009878585767|0.390209312217|
|Japanese TRAIN|support_loss|96|59|0|37|0.00003265526138|0.752655779681|
|English HOLDOUT|native|48|48|0|0|0.001756743144|0.000004616032|
|English HOLDOUT|support_loss|48|41|3|4|0.098728385823|1.108003290225|
|Japanese HOLDOUT|native|48|33|7|8|0.580477295184|1.424069392878|
|Japanese HOLDOUT|support_loss|48|19|21|8|1.447742212025|2.240395231518|

Outside-catalog and exact ties are0 in these eight strata. Lower NLL is better.
TRAIN here identifies the canonical VALUE-COMBINATION partition. Original6 prompts
were never presented during fitting, even when their split field says TRAIN.
Do not call those longer TRAIN-split prompts memorized training examples.

For this seed, support improves on the familiar-value partition but within-pair
binding deteriorates. On held-out values both components deteriorate. Japanese
HOLDOUT rescued11/regressed25;20previously correct answers became absent-digit
predictions. English HOLDOUT rescued0/regressed7. Japanese TRAIN rescued14/regressed32.
This is not uniformly a candidate-support problem or a harmless change in confidence.
Seed338003's original6 TRAIN suffix differs:English rescued5/regressed3 and Japanese
rescued25/regressed7,with improved mean support/within NLL. Preserve seed heterogeneity.

C338 totals remain original6correct1389->1375,outside27->49; original5correct1426->1423,
outside2->7. Candidate full gates0/5. C339 PASS changes none of those capability verdicts.

## Bounded next question

Do not immediately sweep support-loss coefficients or choose favorable checkpoints.
Test a different variable: at the same 2400-update budget with ordinary CE and native
readout, replace only original-length4 TRAIN tokens by canonical length5 TRAIN tokens.
Keep original2/3 and interior4 training, value split, targets, schedule/masks and
matched fresh paired initialization. Original6 remains unseen in both training arms.
This tests whether moving the original-name training boundary improves six-character
transfer without losing shorter tasks. It changes exposure, not parameter capacity,
and cannot prove a universal length-generalization mechanism. Separate implementation,
preregistration, committed-byte review and activation are mandatory.

## 2026-10-28 verification and transcription correction

The original acceptance text transcribed the publisher byte count and SHA256
incorrectly. The two values above now match latest.json at the original publication
71585b7eb2da7685915bb30b43376b1ea1ffec9b. No log, experiment source, preregistration,
saved artifact or scientific verdict was changed, and no experiment was rerun.
The Git LF log is1159184bytes with3806LF line endings and SHA256
630cf6309fe1e6e0c5ec036c538642b5948b18387da522a542537104de57d316.
Reconstructing its Windows CRLF representation independently gives1162990bytes and
the exact published cbeeda6e... SHA256 above. This verifies transport bytes; it does
not independently rehash the local-only tensors/checkpoints or their input maps.

All720logged strata and360paired-transition records were read. The following
descriptive totals pool ALL5seeds,ALL3profiles,and BOTH languages in normal HOLDOUT.
Each arm/domain contains1440answers; NLL means are weighted by answer count.

|Domain|Correct native->support_loss|Absent digit native->support_loss|Mean support NLL native->support_loss|Mean within-pair NLL native->support_loss|
|---|---:|---:|---:|---:|
|original5|1426->1423|2->7|0.004792198->0.010109601|0.108096118->0.067590749|
|original6|1389->1375|27->49|0.059862129->0.082290481|0.148967192->0.142362736|

Outside-catalog errors are0 in these pooled domains. Original2/3/4/interior4 remain
1440/1440correct per arm/domain. The pooled long-name within-pair NLL improves while
support NLL and exact correctness deteriorate; the seed338004 example above must not
be generalized into a claim that within-pair binding uniformly deteriorates.
These descriptive pooled values neither introduce a new gate nor change C338's
VALID NEGATIVE or C339's DIAGNOSTIC INTEGRITY PASS. Gate F remains NOT PASSED.
