# Learned necessity and semantic representation — C174-C184

## Scientific subject

This sequence asked whether the model can learn NEEDS/SUFFICIENT from structured task state, and
which representation/supervision changes actually fix the weak cases.

## Experiment timeline

| C | Verdict | Question/result |
|---|---|---|
| C174 | PASS | Learned necessity syntax ablation established the first directional learned signal. |
| C175 | PASS | Frozen predictions beat/clarified the TRAIN-only syntax-blind frequency reference. |
| C176 | VALID NEGATIVE | Conditional weighting traded errors instead of producing joint improvement. |
| C177 | PASS | Score-order audit found limited within-count ordering gains; did **not** rescue C176. |
| C178 | VALID NEGATIVE | Explicit visible-leaf binding did not yield the preregistered joint improvement. |
| C179 | VALID NEGATIVE | Tree routing vs sequence routing did not solve the endpoint. |
| C180 | VALID NEGATIVE | Direct-fact readout ablation did not solve the endpoint. |
| C181 | PASS | Proper-subexpression supervision removed all registered main errors. |
| C182 | VALID NEGATIVE | Frozen fact renaming found 1 error among 648,324 candidate transformed predictions. |
| C183 | PASS | Localized the complete C182 failure set to the tree-route naming path. |
| C184 | PASS | Handwritten reversible canonical fact-index adapter normalized the naming boundary. |

## C181 — decisive semantic-supervision result

Three INTERNAL_SEMANTICS models achieved zero main errors across every registered TRAIN and reused
PILOT row.

Representative deciding metrics:
- each candidate PILOT confusion: [[6744,0],[0,2652]]
- each TRAIN confusion: [[27816,0],[0,14628]]
- mixed-count and matched-visible AUC=1
- inference architecture remained the original base model; auxiliary teacher/head is training-only.

Scientific interpretation:

```text
TRAIN proper-node semantic labels
-> auxiliary loss
-> learned shared-cell weights
-> ordinary teacher-free base inference
-> correct main NEEDS/SUFFICIENT judgment
```

This showed that the registered base capacity could express the task; the earlier plateau was not
necessarily a hard capacity limit.

## C182-C184 — naming invariance boundary

C182's strict gate failed because seed181003 made exactly one error under one nonidentity permutation.
The aggregate accuracy was extremely high, but the preregistered all-model/all-permutation gate made
that a real VALID NEGATIVE.

C183 localized that single failure to tree-route naming rather than broadly destroying all internal
semantics.

C184 then introduced an explicit reversible canonical index adapter and passed its contract. This
is **engineering normalization**, not proof that the neural model learned naming invariance.

## What failed and should not be repeated blindly

- loss reweighting alone (C176);
- visible-fact binding alone (C178);
- tree topology alone (C179);
- direct-fact readout manipulation alone (C180).

These are valuable negatives: they narrow the plausible explanation toward internal semantic
supervision rather than surface architectural tweaks.

## Limits

- same four repeatedly inspected semantic development groups;
- hand-programmed partial Boolean semantic teacher;
- read-once four-variable family;
- no untouched final holdout;
- no general naming invariance;
- no natural language or arbitrary logical reasoning.

## Cleanup implication

C176/C178/C179/C180 scripts are likely archive candidates after dependency removal, but their
negative verdicts must remain in the report. C181 checkpoints and C184 canonicalization contract are
still active parents of later acquisition experiments.
