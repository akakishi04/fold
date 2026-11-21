# V5-B frozen binding diagnostic v0.1

## Why after C234

C234 is **ACCEPTED VALID NEGATIVE**. The registered contextual-binding gate failed for both the full
and GRU-only families while execution, checkpoint replay and protected-input checks all passed.
Do not rerun C234, extend its budget or relax its thresholds.

C234 measured the complete held-out EVAL split, but did not measure exhaustive TRAIN accuracy after
training. The final sampled training-batch NLL decreased, yet that is not evidence that the complete
TRAIN set was solved. Before changing architecture, optimizer, dataset or capacity, localize the
failure with the frozen step400 models.

C235 is therefore a **diagnostic audit**, not another capability trial and not a rescue of C234.

## One scientific question

With all six accepted C234 step400 models frozen, is the contextual-binding failure already present
on the complete TRAIN set, or is there a descriptive gap between TRAIN and the held-out value-pair
EVAL set?

This question is answered separately for each seed, family and language. C235 does not decide Gate F.

## Frozen inputs

Reuse exactly the accepted C234 artifacts:

- summary SHA256: `a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`
- binding-plan.json: `0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38`
- dataset.json: `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`
- measurements.json: `23f822d0a05faac176efc767b5702a21763946b295a76c503f01abc965c776c3`
- trained-models.pt: `711dd636597d5ec575136bd780ac303eb21ed6198d411f977bb20c67fd20bd26`
- validation-summary.json: `655dc04bd3509246c432eb8817699b5685ca300df612515d55358d78e634b629`

Scientific parent execution HEAD:
`c225c2d82636085e2d639878738e1b9a7aa37b42`.

All six checkpoint states are loaded in the accepted order:
three seeds `234001/234002/234003` x `full/gru_only`.
The saved model fingerprint must equal the accepted final fingerprint before any diagnostic forward.

## What changes

Only evaluation coverage changes.

C234 evaluated the 192-row EVAL split under:
- normal input;
- evidence-blind input;
- query-blind input.

C235 evaluates **both**:
- complete TRAIN: 384 rows;
- complete EVAL: 192 rows;

under the same three views and the same accepted byte adapter/evaluator.

No new example, split, token, model parameter, decoding constraint or target rule is introduced.

## Measurements

For TRAIN and EVAL, reuse the parent metrics:
- exact unconstrained byte accuracy;
- answer NLL;
- evidence-blind accuracy/drop;
- query-blind accuracy/drop;
- fact-pair both-correct accuracy;
- query-pair both-correct accuracy.

Add post-inference descriptive measurements using only model outputs plus already-fixed row metadata:
- fraction of predictions equal to either value supplied in the prompt;
- mean probability mass assigned to the two supplied values;
- agreement with first fact value;
- agreement with last fact value;
- fraction/count of query-pairs receiving the same answer despite a changed queried object;
- query-pair both-correct count.

These diagnostics are descriptive. They do not create a new success criterion for C234.

## Descriptive localization labels

For each of 12 seed/family/language cells, use the already-registered C234 90% exact-accuracy
criterion only as a localization reference:

- `TRAIN_ACCURACY_BELOW_90`: complete TRAIN accuracy <0.90.
- `TRAIN_AT_LEAST_90_EVAL_BELOW_90`: TRAIN >=0.90 and EVAL <0.90.
- `BOTH_ACCURACIES_AT_LEAST_90`: TRAIN >=0.90 and EVAL >=0.90.

These labels are **not a new Gate F or capability PASS**. In particular, the third label cannot
retroactively change C234 because C234 also required paired and masking criteria.

## Fixed workload and integrity gate

Six frozen models x two splits x three views = **36 model forward calls**.

Rows presented to model forwards:
- per model: 3 x384 TRAIN +3 x192 EVAL =1728;
- all models: **10368 evaluated rows including masks**.

New training steps: **0**.
Optimizer steps: **0**.
Checkpoint writes: **0**.
Network calls: **0**.

C235 status PASS means only that the diagnostic audit is complete and internally valid:
- all six accepted C234 models load in the fixed order;
- accepted EVAL predictions and parent metrics replay exactly within `1e-9`;
- all before/after model fingerprints are identical;
- exactly36 forwards /10368 evaluated rows are recorded;
- all12 localization cells are present;
- five registered artifacts are written and hash-checked.

Accuracy outcome never controls the C235 integrity PASS. Replay/schema/artifact/nonfinite/model
mutation/source-protection failure makes the attempt INVALID and requires RETRY SAME C235.

## Interpretation boundaries

C235 can distinguish a broad descriptive failure mode:
- low TRAIN accuracy means the fixed recipe failed even to fit the complete binding training set;
- high TRAIN but low EVAL accuracy is consistent with a held-out co-occurrence generalization gap;
- high TRAIN and high EVAL accuracy would require reconciling why the frozen C234 gate still failed
  on its other registered criteria.

C235 does **not** by itself identify the causal mechanism. It does not prove an optimizer defect,
architectural impossibility, memorization, compositional reasoning, statistical significance or
general-language capability.

Full and GRU-only remain unequal in capacity; no architecture ranking follows from this audit.

## Outputs

Five ignored run artifacts:
- diagnostic-plan.json
- diagnostics.json
- predictions.json
- model-fingerprints.json
- validation-summary.json

Plus summary.json. No C234 artifact is modified.

The manifest SHA256 is
`2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3`.

After this audit, judge the diagnostic before registering C236. Do not change training or architecture
inside C235.
