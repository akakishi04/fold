# C323 preregistration — saved fact-order response bias

Experiment: `C323-v5b-saved-fact-order-bias`, stage `V5-B-SAVED-FACT-ORDER-BIAS`.
Acceptance base: `a0e2221eb8f12b5a2cc8f325876a8752ed1b9eb1`.
C322 ACCEPTED PASS (diagnostic integrity only); C321 remains ACCEPTED VALID NEGATIVE;
C320 remains bounded capability PASS. Gate F NOT PASSED; C324 NOT REGISTERED.

## One scientific question

When a previously failing four-character question changes only the **order of the two facts**,
while the actual facts/values and queried entity are held constant, is the model's wrong answer
tracking first/last fact position rather than the requested entity? Compare C322's saved
`interior` task and its saved original `old4` control for all10 existing C319 checkpoints,
both readout policies, all three name families, English and Japanese, TRAIN/HOLDOUT value splits.
No new input synthesis, model inference, training, seeds, checkpoint loading or decoder changes.

## Fixed matching and evidence

Use the 8,640 original C322 normal-query pairs (10 models x2 conditions x432 query pairs).
For each fixed `(seed,arm,condition,split,profile,language,entities,values)`, require **exactly**
two records corresponding to fact order `(entityA,entityB)` and `(entityB,entityA)`. Each
record already contains normal argmax answers for both queries. Construct exactly4,320
**four-answer counterfactual groups**. Their factual targets remain two distinct values.
Resolve source logical IDs from the SHA-verified C321 canonical dataset via actual C322 loader.
Verify each pair's row IDs, query entities, target digits, fact-order permutation, profile-slot
mapping, and stored correct/same-prediction flags. Do not assume adjacent rows, sort by prediction,
or choose the better fact-order result.

For each group report `correct` (0..4), `four_correct`, `collapsed_orders` (0..2), whether the
model answers **both queries with the first fact's value in both orders**, similarly for the
last fact, whether the same value is returned for all four answers, and whether each named
query's argmax survives the fact-order swap. Also record counts of answers selecting first-fact,
last-fact or a class outside the two fact values; the three categories must sum to four.
All observations are descriptive: `first_fact_both_orders` does not prove a learned recency
rule, and a correct answer does not establish the mechanism used to obtain it.

Aggregate exactly240 `(seed,arm,condition,split,profile,language)` groups, and four complete
arm/condition totals. Their `answers`, `correct`, `query_pairs`, `collapsed_orders` must exactly
match the immutable C322 `overall` counts `answers`, `correct`, `pairs`, `same_prediction`.
`old4` is the positive control using the same checkpoints; paired records are dependent
observations, not4,320 independent trained models. Preserve all originally published C321
and C322 capability flags and local/masked criteria.

## Evidence contract / stopping

C322 scientific execution HEAD: `b7943ab4435d68d2716e6137b596042b777f2efb`.
Published log commit: `278e883bd5b6555aa2bef8a43e1634dc5e44e6f0`.
C322 summary: `runs/c322-v5b-query-contrast-f164844010f04c24bcfda4a743b44a72/summary.json`.
SHA256: `fdcf1f2ac893a46c900e50db93740004926c70765ca269ba0cfe7474bf4c5796`.
C322 source Git blob `c93fb85922c5907c424698897de4af2888f81f77`.

Verify all49 ordered summary hashes **before** full C322.verify_artifacts with48 ancestors,
accepted execution HEAD and four immutable parent JSON artifacts, then load C322's canonical
logical dataset through its exact verified C321 ancestor contract. Require complete original
C322 status/summary/4 overall groups; never infer fields from filenames or skip parent semantic
checks. Parent `query-pairs.json` is a saved-result artifact, not new model inference.

Retain all778 inherited source pins/1467 protected inputs. Add OWN6, C322 summary+4 artifacts,
then protect current source: **784 pins /1478 inputs**. Check all actual lazy/local helper and
factory-language module paths; no pin waiver, accepted mutation or new historical-test exclusion.
New source imports the C322 benchmark only through its explicit context factory.

Outputs: `audit-plan.json`, `order-counterfactuals.json`, `measurements.json`,
`validation-summary.json` and `summary.json`; JSON only, no checkpoint or tensor archive.
No-neural postcheck re-derives all groups from the same verified C322 parent outputs,
compares JSON hashes/sizes and enforces no overwrite. New model calls, optimizer updates,
model state loads, new checkpoint writes and network requests all **0** in C323 diagnostic.
Recursive parent checks and real regression still require CPU and memory.

Own24; modules208; loaded5294; focused5293, with sole inherited exact C204 dynamic-state
exclusion unchanged. Manifest SHA256 `8c4e9152cb11d1492cd7d88cf7caafef40a901de6c68aa44e404c1c46ff7c5de`.
A valid C323 execution is **ACCEPTED PASS for diagnostic integrity** regardless of the
observed order bias. A source/shape/semantic/replay/persistence failure is INVALID and must
be repaired within C323. None of these outcomes establish arbitrary name matching, a unique
causal source of the C321 failure, or Gate F completion.

## Runtime and operational performance

Commit and re-fetch all6 source/test/runner/launcher/prereg/design bytes; run all24 software
controls under normal and CP932-default emulation before post-authoring PASS. User Windows
Validate must check49 actual archived parents, all784/1478 pins/inputs, own24 and the entire
5,293-test inherited ordered suite in one process, and ParseFile on all selected PowerShell.
Retain direct UTF8 runner logs, fixture-boundary timings, faulthandler, decimal/hex exits,
old preflight-log preservation, and fail-before-science behavior. No automatic retry, test
skipping or optimizer/architecture change to make validation faster.

C322's 5,269 regression tests took1245.157s; many prior accepted modules individually require
roughly30-51s. Parent hashing and serialized-output checks may contribute, but the recorded
regression suite is a major **measured** cost. Do not claim bulk attestation reduces the suite's
test runtime. Evaluate safe test-control-plane improvements in a separate reviewed change.
C324 is not registered until C323's execution is formally judged.
