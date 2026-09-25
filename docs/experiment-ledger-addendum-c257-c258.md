# C257 acceptance and C258 question boundary

## Formal verdict

**C257 ACCEPTED VALID NEGATIVE — frozen unseen fact-order transfer.**
The execution is valid; the preregistered all-five-seed capability gate is not met.
C256 remains ACCEPTED PASS within its original three-entity value-assignment scope.
Gate E PASSED; Gate F NOT PASSED. No production adoption or core-superiority claim.

Scientific execution HEAD:016785f35605a3eef5f94d42f0b86cb2fc4d9dfe.
Published log commit:4a322950685b80d7748aa525608555149c2c2ffd.
Publisher log SHA256:6932e3f178cfadb3434a34368a3ba674489b96b6dc509b2a69da18f6a36a66a5.
Log bytes:680841.
Summary SHA256:596df75ccc89c5a12c964c2e6be1fc689e5773f4c0a857f90fdcedd4df9b8816.
Local summary:runs/c257-v5b-unseen-order-705d486739b44a56bbed34fae66ace89/summary.json.
The publication commit changes only c257/latest.json and latest.log.
Acceptance is based on retrieved immutable log ranges, publisher metadata and the recorded
local postchecks. The reviewer did not independently run the learned models or rehash the
complete680841-byte log. Publisher-reported and independently recomputed hashes are not synonyms.

## Execution validity

Own24 PASS in4.897s; focused3337 PASS in224.138s.
388 source pins/635 protected inputs verified. All ten final C256 models were evaluated:
180 model forwards/34560 row presentations, training0, one checkpoint bundle load,
ten strict state loads, zero new learned checkpoint writes.
Original metric/prediction replay, original-anchor restoration, persisted logit/metric replay,
complete weight preservation and protected inputs all passed.
Tracked tree clean; execution HEAD preserved; run_execution_valid=True.
scientific_status=FAIL; candidate_gate=False; all_replays=True; all_weights_preserved=True.

## Deciding metrics

Candidate whole-seed outcomes:256001 PASS;256002 NEW_ORDER_MISS;256003 NEW_ORDER_MISS;
256004 PASS;256005 NEW_ORDER_MISS. Thus2/5 pass, not the required5/5.
All EOS controls have ORIGINAL_CRITERIA_MISS, inherited from their C256 performance;
this is not five newly independent control failures caused exclusively by the unseen orders.

The following counts use only the four novel orders in the original HOLDOUT assignment split.
Each language column totals144 answers. Six-order columns count assignment/query groups for
which all six presentations are correct, denominator36.

| Seed | New-order EN | New-order JA | Six-order EN | Six-order JA | Whole-seed result |
|---:|---:|---:|---:|---:|---|
|256001|144/144|144/144|36/36|36/36|PASS|
|256002|117/144|120/144|23/36|23/36|NEW_ORDER_MISS|
|256003|82/144|100/144|2/36|13/36|NEW_ORDER_MISS|
|256004|143/144|144/144|35/36|36/36|PASS|
|256005|102/144|91/144|19/36|12/36|NEW_ORDER_MISS|

Pooled candidate new-order HOLDOUT1187/1440=82.4306%; this aggregate does not replace the
per-order, per-language, per-split and all-five-seed gate. Seed256002 EN bac answers33/36 but
query-triplets9/12: passing raw accuracy alone is insufficient.
Seed256003 EN acb is12/36 and cab13/36. Seed256005 JA cab is15/36.
The failed seeds also have weaknesses on novel orders of TRAIN assignments, so this is not
solely a previously unseen value-assignment issue. There was no threshold or seed rescue.

## Interpretation and non-claims

The selected reader supports bounded value-assignment transfer on the original two orders
(C256), but does not reliably transfer to all four additional permutations across these five
trained states (C257). Two models do transfer. Do not claim that the architecture cannot learn
order robustness, that all models use a positional shortcut, or that a particular core mechanism
caused the miss. The observational results do not identify a unique algorithm.
The authored task, reused data, correlated permutations and small seed set are not an external
language benchmark or independent population-level samples. Gate F remains unpassed.

## Accepted artifacts

-eval-outputs.pt:6911df9af7a10790cee9b18ff15a6b3479ca7e20046d5f6a16f95d69d068b92a;70832057 bytes.
-measurements.json:c37f98bbc13526f408b9b00adac16e90e23dc764d59ef4af1ef5e990b235eb22;61378 bytes.
-order-dataset.json:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052;92184 bytes.
-order-plan.json:18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36;2248 bytes.
-validation-summary.json:1d0d66a7550d47e34d01b5242c8ad0ef527ed7c36df66a440e31005609975d99;1268 bytes.

## Next question, not activation

Use the saved C257 outputs without model evaluation or training to ask whether novel-order
errors concentrate on query b/乙 and select the value at the middle fact position.
In C256 b/乙 was always the middle fact; in every C257 novel permutation it is first or last.
Distinct assigned values allow attribution of a wrong digit to a different displayed entity,
an absent value, or another byte. Report all queries, both arms, all seeds and both assignment
splits, with correct-case denominators and known-order baselines; do not select only failures.
This is an exploratory saved-output diagnostic motivated by already seen aggregate C257 scores,
not independent confirmation, a new capability gate, or a causal intervention.
C258 will have its own preregistration and authoring review before activation. C259 unregistered.
All earlier accepted verdicts and invalid-attempt recovery records remain preserved.
