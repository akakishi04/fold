# V5-B frozen selective evidence v0.1 — C245

## One question

For the six frozen C244 final models, how do answers and scores respond when only the queried
entity's value is erased, versus only the other entity's value?
C244 fitted all64 TRAIN prompts but failed the remaining32 HOLDOUT prompts. Its existing masks
hide both values or the query. They do not separate the contributions of the two factual values.
This is a diagnostic before another learning intervention, not a model improvement experiment.

## Fixed inputs and interventions

Reuse byte-identical C244 TRAIN64/HOLDOUT32, row order, labels, source provenance and all six
step400 checkpoints. Keep architectures, CPU float64, two threads and deterministic algorithms.
No optimization, extra training, checkpoint selection or checkpoint write.

Retain the three original views:normal,evidence_blind,query_blind. Their predictions must exactly
reproduce C244's saved final arrays, and all original metrics including NLL must match within1e-9.
Add two views using the existing rendered prompt. Replace exactly one factual ASCII digit with '?':

Example query: box=0;book=1;box=
- queried_value_blind: box=?;book=1;box=
- other_value_blind: box=0;book=?;box=

The same intervention must follow the entity when fact order reverses. It preserves names, query,
fact order, UTF-8 byte length, EOS position and every other token. It uses the query already in the
input to locate the factual field, not the answer label. Tokens are generated with the actual
C231 prefix_tensor used by C234. Original-view tensors are cross-checked against C234.tensors;
new views must differ from normal in exactly one token, replaced by byte63.

## Measurements

For each model/split/language and all five views, save unrestricted256-byte logits and report
correct count, accuracy, answer NLL, normal-minus-view accuracy, changed-answer count,
normal-correct to masked-wrong count, normal-wrong to masked-correct count, NLL increase and
maximum absolute logit change. Correctness always refers to the original unmasked answer for
measurement purposes; it does not assert that erased inputs remain uniquely answerable.

Raw logit drift and argmax changes are separate. A common shift of all logits can leave output
probabilities unchanged; do not infer importance from raw magnitude alone. Accuracy changes,
answer flips and loss changes are reported together, not collapsed into one importance score.
Persist raw logits so postcheck can reconstruct the measurements rather than trusting printed
aggregates. All outputs remain local ignored artifacts; do not commit arrays or model files.

## Identifiability and distribution limits

These one-value masks were not in training. A response may reflect distribution shift or missing
information, not only the importance of the erased fact. The erased position is determined by the
visible query; no hidden label is supplied to the model. No internal component is intervened on.

Compute the exact best-lookup ceiling for identical masked prompts before inference. With the
queried value hidden, TRAIN has two possible answers for each remaining factual value:ceiling50%.
HOLDOUT uses only pairs0/3 and1/2, so an oracle knowing that distribution can infer the hidden value
from the other value:ceiling100%. With the other value hidden, the queried fact remains explicit
and the ceiling is100% on both splits. These are finite-data ambiguity properties, not measured
model competence or random-chance baselines. They preclude a simplistic mask-accuracy interpretation.

A greater response to one mask is a behavioral finding under that input intervention. It does
not prove a unique internal algorithm, locate a defective layer, establish general binding, or
justify masking inputs as a production repair. Even both masks yielding similar results is a
valid diagnostic outcome. Do not reverse C244's verdict or promote Gate F.

## Integrity and workload

Six models x2 splits x5 views=60 actual model forwards. Six x(64+32)x5=2880 row presentations.
Load one accepted checkpoint bundle containing six states. Strict state loading and final
fingerprint comparison are required. Freeze parameters, use eval/no_grad, require no parameter
gradients, and verify fingerprints before/after all forwards. Root hooks count actual workload
and are removed even on errors. No new training, optimizer operation or checkpoint write.

24 model/split/language diagnostic cells, each containing five-view metrics. One original-model
forward is not duplicated merely to compute metrics:original metrics are reconstructed from the
actual logits and compared with saved C244 records. Postcheck performs no additional model forward
or checkpoint load; it replays measurements and original metrics from persisted logits.

PASS means diagnostic integrity only:parent identity, original predictions/metrics replay, masks,
finite outputs, frozen weights, complete workload, protected files and persisted reconstruction.
Any integrity fault is INVALID / RETRY SAME C245. There is no masked-accuracy success threshold.
Gate F remains NOT PASSED; numeric-memory tuning paused. Judge C245 before registering C246.
