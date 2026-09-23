# V5-B saved positional-rule audit v0.1 — C240

## Question

Do the accepted C239 answers agree with an explicit query-to-fixed-position rule rather than
entity binding, or with simpler first/last/constant outputs? This analyzes saved errors before
another learning intervention. C239 fitted order0 but failed order1 in all12 cells.
See docs/experiment-ledger-addendum-c239-c240.md for the accepted evidence.

No training, new inference or checkpoint deserialization is needed. C239 already saved all final
unrestricted-byte predictions, verified against checkpoint reloads. C240 reads that evidence,
checks its discrete metrics independently, then tabulates specified behavioral rules. It is not
an additional independent sample or a second capability test.

## Rules and identifiability

Evaluate six rules on normal, unmasked rows only, in the declared order:
- entity: return the value assigned to the queried object;
- query_fixed_position: object0/box query selects the first rendered value, object1/book query the second;
- first: always select the first rendered value, regardless of query;
- last: always select the last rendered value;
- constant_0 and constant_1: always output the corresponding digit.

The fixed-position rule captures a particular possible shortcut from order0 training, where box
always appeared first and book second. On reversed order1 prompts it would select the wrong
entity's value. This rule is NOT claimed to be the learned internal algorithm.

On TRAIN, the entity and query_fixed_position rules coincide for all8 rows. On this binary HOLDOUT,
query_fixed_position coincides with the other entity's value for all8 rows. These degeneracies
prevent unique mechanistic identification. Even perfect agreement is only behavioral consistency.
Do not rank the internal architectures using agreement scores or rename a rule match as understanding.

Rule answers are computed from factual row metadata, not the saved target field. Targets are used
only for scoring. All calculations are offline; no target or rule is supplied to a model. The
actual saved output remains any integer byte0..255. A wrong output is explicitly separated into
other_entity and outside_supplied; do not coerce an arbitrary byte into0/1.

## Input and audit path

Use the exact C239 split-dataset.json and measurements.json. The outer TRAIN/HOLDOUT mapping
controls membership. Rows preserve their original split="TRAIN" provenance. Read only
predictions[split][view] from after the400-step endpoint; initial_train is not final evidence.
The final metric schema is final[split][language], not the earlier final_probe form.

Validate all six identities, source/input/artifact hashes and accepted parent summary. Recompute
rows, accuracy, fact/query both-correct accuracy, masked accuracy and both drops from the three
saved prediction views. Match those discrete fields to C239 final metrics within1e-9.
NLL requires logits/probabilities and is not reconstructed from argmax bytes. It is checked finite
and retained under the parent artifact hash only; nll_recomputed=False must remain explicit.
The checkpoint file is hashed for preservation but never deserialized or executed by C240.

Pair each TRAIN row with the HOLDOUT row sharing language, assignment/group and query. Record
whether their answers are the same, both correct, or both match the fixed-position rule. Store
individual normal-row rule outputs, actual predictions for all views, and all paired answers.
A reversal error may match several explanations; no causal intervention is performed here.

## Workload and gate

Six saved models x2 splits x3 views x8 predictions =288 unique saved answers audited.
Normal rows96; six rules each =576 rule comparisons. Matched order pairs48. Diagnostic cells24
(6 models x2 splits x2 languages). These count primary records/comparisons, not repeated validation
reads in precheck/postcheck. Actual model forward calls0, new training0, checkpoint loads/writes0.
File reads/hashes and JSON output costs are not claimed to be zero. Regression tests may execute
their own historical fixtures; they are outside C240's scientific workload.

PASS means evidence/diagnostic integrity only, regardless of which rule agrees with the outputs.
The exact partition, prediction schema, discrete replay, counts and persisted derived artifacts
must match. Missing pins/artifacts, altered source, bad schema, nonfinite fields, replay or count
faults are INVALID / RETRY SAME C240. A low rule agreement is not an invalid diagnostic.

## Scope and stop

Do not invert/correct the model's answers, modify its architecture, add training, relax C239,
claim new generalization, identify an internal causal algorithm or promote Gate F. C238 remains
seen-TRAIN PASS; C239 remains an order-transfer valid negative. The next intervention, if warranted,
requires a separate C241 preregistration after judgment. Numeric-memory tuning stays paused.
