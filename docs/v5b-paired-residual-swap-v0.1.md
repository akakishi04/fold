# V5-B paired residual swap v0.1 — C254

## One question

Does the trained post-core residual contribute information specific to the recipient's queried
entity, beyond a contribution that also works for a paired prompt? Keep the recipient's learned
reader output fixed and replace only the post-core residual with a paired donor's saved vector.

C253 showed that removing the residual often reduced accuracy, but sometimes left all answers
correct. Zeroing or substituting a pre-core vector changed activation scale/distribution. C254
instead permutes actual post-core vectors within a matched seed/split/language/view. The empirical
residual multiset is unchanged. This is still an off-training-distribution feature recombination,
not a proof of an internal semantic algorithm or the core's necessity during learning.

## Fixed donor conditions

For every row and all five C252 seeds, use four modes in order:

| Mode | Residual donor | Recipient reader output |
|---|---|---|
| self | Original row | Unchanged original |
| order_swap | Same facts and queried entity, opposite fact order | Unchanged original |
| query_swap | Same facts and fact order, opposite queried entity | Unchanged original |
| restored | Original row again | Unchanged original |

Example recipient:box=0;book=1;box=.
The query donor is box=0;book=1;book=; the order donor is book=1;box=0;box=.
Only the donor's saved post-core EOS vector is used. The recipient's original read vector,decoder,
normalization and target remain fixed. No donor answer is provided as a model input.

Donors are fixed by language,assignment-group,order and query metadata, not by a correct prediction,
loss or favorable effect. They never cross seed,language,TRAIN/HOLDOUT or view. Each mapping is a
bijection and its own inverse; altered modes have no fixed points. Query-pair targets differ and
order-pair targets agree. Targets validate the pair contract but do not choose a donor.

## Reuse of saved computation

C253 outputs.pt stores original logits and intact pre/post/read vectors from the five accepted
C252 learned states. Replay all C253 archive-derived metrics/contrasts before using those tensors.
Instantiate the actual C252 model and strictly load its same final state through C253.frozen_model.
The model stays eval/requires_grad=False. Execute ONLY its LayerNorm and decoder on:

z = saved_post[donor_index] + saved_read[recipient_index].
logits = decoder(LayerNorm(z)).

The original LayerNorm shape,epsilon,weights,bias and decoder weights/bias are retained directly
from the accepted model. No encoder,core,reader or full-model forward is allowed; hooks reject any
such call. The saved components are not modified in place. Parameter fingerprints stay identical.

Self must reproduce all original C253 intact logits within1e-9 and predictions exactly before any
swapped scoring. Restored must reproduce self. For query_blind inputs, query-pair prompts are
identical:their saved post vectors must match exactly and query_swap must reproduce self. This is
an internal negative control,not an accuracy gate. Use all original scoring views and pairs.

## Outputs and accounting

Five models x4 modes x2 splits x3 views =120 frozen head evaluations/5760 head rows.
These are NOT full-model forwards:encoder/core/reader/full-model forwards0 and training0.
One C252 checkpoint bundle load,five strict final-state loads,no new learned checkpoint.
Each head evaluation calls LayerNorm and decoder once. Head calls/rows are counted with hooks.
Archive loads,hashing,metric calculations and serialization remain real work. Precheck/postcheck
repeat validation of the same saved data,not independent samples or additional scientific trials.

Report each mode's normal accuracy,NLL,fact/query/order pair metrics and mask drops. For order_swap
and query_swap versus self, report flips,correct-to-wrong,wrong-to-correct,accuracy/NLL deltas and
agreement with the donor's target. Keep all seed/language cells,including failed seed250002.
Donor-target agreement is descriptive and is not classified as semantic understanding.

Store head logits in head-outputs.pt plus swap-plan.json,diagnostics.json,contrasts.json and
validation-summary.json. Postcheck recomputes derived results from stored head outputs and the
original archive;it does not execute the model or head again.

## Interpretation and stop

Greater sensitivity to query swaps than meaning-preserving order swaps would support a bounded
query-specific dependency in the frozen residual/read combination. It would not uniquely locate
knowledge,exclude nonlinear normalization effects,or show that the same residual is needed during
training. Low sensitivity would not establish a globally constant or irrelevant core.

PASS means diagnostic integrity regardless of accuracy changes. This is not a new generalization
trial,architecture adoption or repair. C252 stays ACCEPTED VALID NEGATIVE;C253 stays diagnostic PASS;
Gate F stays NOT PASSED. No learning-rate/seed/data tuning,external corpus,paid API,cleanup,history
rewrite or production modification. Judge C254 before registering C255.
