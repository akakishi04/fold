# C242 acceptance and C243 saved recombination error audit boundary

## Formal verdict

**C242 ACCEPTED VALID NEGATIVE.** Gate E PASSED; Gate F NOT PASSED.
All twelve seed/family/language cells pass all TRAIN criteria but fail HOLDOUT criteria.
C241 and earlier verdicts remain unchanged. Do not rerun, extend or rescue C242.

Scientific execution HEAD:372c2c37429acece3f06a9b4521313da4b3d5f8e.
Published log commit:998b34447fc1ac5c4a0f2c42b0a4eb1958b87eb0.
Publisher-recorded log SHA256:490be44e71cbaab6169f4965ce7983c0276a543523921ef1c162b7574dcacd9e.
Log bytes:564532. Summary SHA256:d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb.
Local summary:runs/c242-v5b-balanced-recombination-530e801ba23f496aa8e0a588e0d52982/summary.json.

The publication commit is one commit after execution and changes only c242/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges, publisher metadata and recorded local postcheck,
not an independent checkpoint rerun or a complete-byte rehash of the log.

## Execution validity

24 own tests PASS in6.420s;2977 focused tests PASS in93.412s.
Python syntax, parent/artifact/source checks and data-shortcut prechecks PASS.
298 source pins/454 protected inputs. Six models x400 steps=2400 training steps/76800 answer
presentations. 2490 total forwards/80832 row presentations. All weight-update/checkpoint/prediction
replay checks PASS. Persisted split/initial-identity check PASS; protected inputs, tracked tree and
execution HEAD preserved; run_execution_valid=True. Both recombination gates False; status FAIL.
cell_outcomes is exactly RECOMBINATION_MISS:12, not TRAIN_CRITERIA_MISS.

## Deciding metrics

Every TRAIN seed/family/language cell:16/16 correct,8/8 fact/query/order pairs, evidence drop0.75,
query drop0.50. TRAIN NLL0.001047-0.003695 at logged six-decimal precision.
HOLDOUT exact answers,32 per language:

|Seed|Full EN|Full JA|GRU-only EN|GRU-only JA|
|---:|---:|---:|---:|---:|
|234001|7/32|9/32|11/32|12/32|
|234002|13/32|12/32|13/32|12/32|
|234003|12/32|12/32|8/32|10/32|

HOLDOUT accuracy21.875%-40.625%; no cell reaches the registered90%.
Full query pairs:0/16 in all six cells. GRU-only query pairs:1/16 for each language in seed234001,
0/16 in its other four cells. HOLDOUT NLL3.947179-6.914980 at logged precision.
Pair and mask criteria also miss. Counts are exact conversions from the fixed denominators and
printed rates; no extra precision or significance inference is claimed.

## Interpretation and remaining ambiguity

Unlike C241, C242 passes both normal fitting and evidence/query masking checks on TRAIN.
The fixed recipe learned a solution for the training distribution but failed transfer to new
pair combinations of the same entities/digits. This does not establish general binding, a
unique internal algorithm, Full/core advantage or architecture-wide impossibility.

A remaining training ambiguity deserves explicit analysis:0 always co-occurs with1, and2 with3.
A predictor can infer the queried value as the training partner of the OTHER entity's value.
This rule agrees with all TRAIN targets, requires factual information and the query, yet predicts
a value absent from each cross-pair HOLDOUT context. Masking both factual values does not distinguish
that rule from correct two-entity binding. No claim is made that the actual model follows it.

## Accepted artifacts

- measurements.json:dcc69fcc29f3de2baf8a53082afd83dfa259d98a631689d2b916879b4b1a46f4 (17918 bytes)
- recombination-plan.json:8088155ef7ba95eb47a8a7ae3790247ff20d61804ac08c7fc1b1ed2f0c645760 (2707 bytes)
- split-dataset.json:9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0 (15904 bytes)
- trained-models.pt:a71531049d76a89b29a9e9f38dfda47cda79c50c071aab32beb8bbfda481f387 (601940 bytes)
- validation-summary.json:5ac81c55f5d56e3984be7b769ae8a040a8965f16584c19c67423405f962cd3da (359 bytes)

## Next question, not registration

C243 will ask whether saved HOLDOUT errors select the wrong supplied value, an absent value
consistent with the fixed training-pair association, or another byte. Analyze the six accepted
C242 final prediction arrays, not new models. Independently replay every discrete parent metric
from all views, then report fixed rule agreements, error categories and query/order pair outcomes.

No additional training, model inference, checkpoint deserialization, answer correction or NLL
reconstruction. These are the same evidence samples, not an independent replication. Rule matches
are descriptive:all four digits fall into the four specified HOLDOUT categories, so category
membership itself cannot prove a mechanism. Compare complete per-cell patterns, not cherry-picked rows.
Separate C243 preregistration/review must precede activation. C244 remains unregistered.
