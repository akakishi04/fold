# V5-B contextual binding pilot v0.1

## Why after C233

C233 is ACCEPTED VALID NEGATIVE: the full model won3/6 seed/language cells and the smaller
GRU-only model won3/6. Do not rerun that comparison until it becomes favorable. Its result stands.

C234 asks a different, more explicit capability question: can the same small models use the facts
in their current input and select the value belonging to the requested object? Loss on spelling and
punctuation is no longer the deciding metric. The ordinary GRU comparator remains in the experiment.
This is a controlled symbolic text task, not general language understanding or a public benchmark.

## Task

English object names: box, book, ball, umbrella.
Japanese object names: 箱, 本, 玉, 傘.
Values: ASCII digits0/1/2/3, with distinct values for the two objects in each example.

```text
Input:  box=0;book=3;box=      Target: 0
Input:  box=0;book=3;book=     Target: 3
Input:  box=3;book=0;box=      Target: 3
Input:  箱=0;本=3;箱=           Target: 0
```

The model receives BOS + complete observed prompt bytes + prefix-boundary EOS + PAD, using the
accepted C231 adapter. The target is a separate single byte. The observed facts deliberately
contain the values; using those facts is the task, not an accidental future-target leak.
The decoder still has256 byte classes. Score unconstrained argmax; outputs outside0/1/2/3 are wrong.
No grammar/candidate restriction converts an invalid output into a correct answer.

Train only on the requested answer position, not on every predictable character in the prompt.

## Grouped split and balance

Six unordered object pairs x12 ordered distinct value assignments =72 binding groups.
Each group has2 languages x2 fact orders x2 queried objects =8 rows. Total576.

Hold out complete co-occurring value pairs {0,3} and {1,2}, regardless of object identities, fact
order, query or language. This gives24 held-out groups /192 EVAL rows and48 TRAIN groups /384 rows.
Every individual object/value pairing is observed in TRAIN; the joint two-value contexts are held
out. All variants of an exact binding stay together. This is not vocabulary extrapolation.

Targets are balanced over all four digits within each language/split. Always returning the first
fact's value or last fact's value obtains50%; returning a constant obtains25% on EVAL. These
reference percentages are checked from generated rows rather than assumed.

Dataset SHA256:
`72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`.
Longest prompt is27 UTF-8 bytes, below the46-byte prefix limit. Partial byte handling is unchanged.

## Evidence and query use

Measure main exact answer accuracy separately in English and Japanese (96 EVAL rows each).
Also require both sides of each matched pair to be correct:

- Fact swap: same objects/order/query, swap the two observed values. Correct answer must change.
- Query swap: same facts/order, query the other object. Correct answer must change.

There are48 fact pairs and48 query pairs per language. They overlap; do not count them as96
independent problems. The same192 EVAL rows supply these paired measurements.

Two separately scored input removals:

- evidence-blind: replace both observed values with '?', retain the queried object;
- query-blind: retain observed facts, replace only the queried object with '?'.

Report normal accuracy minus each masked accuracy. Masked inputs are out of training distribution;
a drop alone does not prove understanding. Normal paired swaps are required as complementary
within-task evidence. Ambiguous masked inputs are controls, not normal answerable tasks.

## Models and fixed training

Reuse the unchanged C231 full model factory (13488 parameters) and C233 GRU-only constructor
(10160 parameters). Neither production implementation is changed. Fixed48 slots, width16,
TASK_NEXT=0; no learned memory or compressed/shared-basis runtime integration.

Fresh seeds234001/234002/234003. For each seed construct the full model, then copy its common
INITIAL embedding/GRU/norm/decoder into the GRU-only model before either is trained. Do not load
C232/C233 trained weights. Both families get identical TRAIN rows and seed-indexed minibatches.

AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0; gradient norm clip1.0; batch32;
400 steps/model; CPU float64, threads2, deterministic algorithms. Six models total:
2400 steps and76800 sampled single-byte answer presentations. Per-model budget is unchanged from
C232/C233; total new training doubles because both families are trained on the new task.
No EVAL-driven tuning, early stopping, longer runs, alternative seeds or best-checkpoint selection.

## Fixed gate and interpretation

For every full-model seed and each language require:
- exact EVAL answer accuracy >=90%;
- fact-pair both-correct rate >=80%;
- query-pair both-correct rate >=80%;
- normal minus evidence-blind accuracy >=35 percentage points;
- normal minus query-blind accuracy >=35 percentage points.

Check all same criteria for GRU-only and report its gate independently. C234's primary gate tests
full-model contextual binding, not full-model superiority. A GRU success is not hidden or counted
as a FOLD-specific result. Capacity/compute are not matched, so report no architecture ranking.
Both initial and final per-language metrics and all final predicted bytes are retained.

All model fingerprints must change during training and round-trip through checkpoints. Reload
normal/masked logits within1e-9 and exactly replay argmax bytes. No accepted parent artifact changes.
A complete finite ability miss is a valid negative. Source/artifact/schema/nonfinite/replay faults
are INVALID. C233 remains negative regardless of the new task's result. Gate F remains NOT PASSED.

## Outputs and next boundary

Five ignored run artifacts: binding-plan.json, dataset.json, trained-models.pt, measurements.json,
validation-summary.json; plus summary.json. Existing console-log publication only.

No larger model, outside corpus, paid API, CI addition, numeric-memory tuning or cleanup. Interpret
this one fixed budget before deciding whether to expand task breadth or diagnose a specific failure.
