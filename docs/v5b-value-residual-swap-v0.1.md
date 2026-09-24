# V5-B fixed-query value residual swap v0.1 — C255

## One question

With the recipient reader output fixed, does the frozen post-core residual depend on the value
assignment when the query name and fact order stay the same? C254 established stronger sensitivity
to a different queried entity than to a different fact order, but did not separate a query-name
signal from information about which value is assigned to that entity. This is the complementary
assignment intervention, not another attempt to repair the failed seed.

## Interventions and controls

Recipient example:box=0;book=1;box=.
Donor example:box=1;book=0;box=.
Both have the same object names, question, fact order, language and supplied value set. Only the
assignment of the two values is reversed. The donor is selected by prompt metadata, not its label,
correctness, loss or effect. Target labels validate that paired answers differ; they do not select
or enter the computation. Each within-split mapping is an involution with no fixed point.

All five accepted C252 seeds250001..250005 and exact TRAIN64/HOLDOUT32 remain fixed.
Use C253 intact saved post/read vectors and the same accepted C252 LayerNorm/decoder weights.

| Mode | Residual | Reader contribution | Purpose |
|---|---|---|---|
| self | Recipient | Recipient | Original-logit replay |
| value_swap | Donor | Recipient | Scientific dependency contrast |
| coherent_swap | Donor | Donor | Reproduce original donor logits |
| restored | Recipient | Recipient | Restore original computation |

The coherent mode is only a positive replay control. It is NOT scored against the recipient label,
counted as a new accuracy improvement, or used to correct an answer. Its outputs must exactly
reproduce the recorded donor's argmax and agree with its raw logits within1e-9. Donor errors are
reproduced as errors; this control does not require the donor to answer correctly.

In evidence_blind inputs both supplied digits are erased. The fixed-query/order fact-swapped pair
then has identical rendered input. Require exact equality of its saved post/read vectors and
unchanged value-swapped logits. This is the negative control. No new input masking is added.

## Frozen scoring and comparison

Load the same five learned C252 states strictly through C253.frozen_model, check final fingerprints,
freeze gradients and eval mode. Execute only the existing LayerNorm and decoder on saved vectors.
The full model, backbone, encoder, core and reader are guarded against accidental forward calls.
No training, parameter update, new model design, seed selection, or new learned checkpoint.

Reuse C254's recorded self/order_swap/query_swap logits as immutable comparator evidence. First
replay the entire accepted C254 archive through its actual analyze function and the C253 metrics.
Do not recalculate those model/head outputs. C255's newly reconstructed self must also equal C254
self. Score original accuracy,NLL,pair metrics and mask drops for self,value_swap,restored only.

Each seed/split/language contrast records correct counts,answer flips,correct-to-wrong,
wrong-to-correct,donor-target matches,accuracy/NLL deltas and the unchanged C254 order/query metrics.
No average or favorable subset replaces individual model/language results.

## Cost and gate

Five models x4 modes x2 splits x3 views=120 head evaluations/5760 head rows.
Full-model/encoder/core/reader forwards0;new training0;one accepted parameter-bundle load and5 strict
model-state loads;new learned checkpoints0. Each mode uses30 head forwards across the five models.
There are60 scored diagnostic cells and20 value-swap contrast cells. The coherent mode is an
integrity control, not included in those accuracy-cell counts. Repeated validation/archive reads
and historical unit-test fixture work are separate real costs, not new independent samples.

PASS means diagnostic integrity, irrespective of any accuracy effect. Check parent bytes, replay,
paired donors, finite outputs, source protection, frozen weights, actual head counters, coherent
and restored replay, and persisted metric recomputation. Any integrity fault stops the same C255.

## Limits and next-decision boundary

A change after swapping the value assignment supports value-sensitive dependency of this frozen
residual/read combination, not a unique binding algorithm. The recipient and donor features are
still combined off their training distribution; LayerNorm/co-adaptation can matter. Equal errors
or equal accuracy do not imply identical internal signals. Query- and value-swapped donors can
share a target on this two-entity task, so equal intervention effects would not uniquely identify
whether a residual codes a target value, an entity, or another correlated feature.

These complementary question/order/value contrasts should inform the next capability or stability
experiment, not indefinitely extend this same microtask's diagnostic chain. No automatic C256 is
registered here. C252 remains a valid negative;C253/C254 remain diagnostic PASS;Gate F NOT PASSED.
No external corpus, paid API, production adoption, cleanup or history rewrite. Judge C255 before C256.
