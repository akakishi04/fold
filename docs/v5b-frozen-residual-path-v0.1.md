# V5-B frozen post-core residual diagnostic v0.1 — C253

## One question

How much of the accepted C252 models' answer performance depends on their post-core EOS residual,
when the already-trained pre-core reader is held fixed?

C252 put both the attention query and its K/V memory before the FOLD core. The core still contributes
through the post-core EOS vector added to the reader output. Its four successful seed blocks do not
by themselves establish that this remaining post-core contribution is necessary during answering.
This diagnostic measures that dependency without another training recipe or a favorable-seed choice.

## Exact interventions

For every one of the five C252 Full models, in this fixed order:

| Mode | Input to the unchanged LayerNorm and decoder |
|---|---|
| intact | post-core EOS + learned reader output |
| pre_residual | pre-core local-encoder EOS + the same reader output |
| reader_only | the same reader output, without an EOS residual base |
| restored | original post-core EOS + reader output |

Each mode scores original TRAIN64/HOLDOUT32 using normal,evidence_blind,query_blind inputs.
No bytes,targets,positions,query identities,weights or prediction classes are changed.
The failed C252 seed250002 is retained alongside250001/250003/250004/250005.

Both original core routes still execute for every internal step. These are substitutions in a
frozen computation, not a newly trained core-free model and not a runtime-speed benchmark.
The diagnostic still pays the cost of computing the core, even when its vector is not forwarded.

## Implementation boundary

Instantiate the exact C252 AlignedPrecoreReadout, load each accepted final state strictly, verify
its final_sha256 and14256 parameters, then set eval mode and requires_grad=False.
Use scoped hooks outside the existing wrapper. The existing wrapper installs its own normalization
pre-hook during forward, after the diagnostic's pre-hook. The diagnostic first captures the original
post-core residual; the parent's hook then adds its normal reader output.

At the normalization output hook, require the actual input to equal captured post+read. The intact
and restored modes return the original output unchanged. The two interventions recompute
functional layer_norm on pre+read or read, using the SAME normalized_shape,weight,bias and epsilon.
There is no recursive normalization module call or extra full-model forward. Each altered forward
performs one additional normalization computation, explicitly counted separately.

Capture pre-core EOS,final NEXT-route core EOS,query projection input and reader projection output.
Require the query input to equal pre-core EOS,original residual to equal actual final NEXT EOS,
and original route/hook call counts. All three pre/post/read component tensors must be exactly
identical across modes for a given input. Only the downstream residual combination changes.
All hooks, including the parent wrapper's hooks, must be removed on success or exception.

## Validity and measured outcomes

Run intact first and compare all three prediction arrays and every saved parent metric, including
NLL, to C252 before starting either altered mode. A mismatch stops the same diagnostic.
Check frozen weight fingerprints after every forward. After interventions, restored logits must
match intact within1e-9 and all argmax outputs must match exactly.

Retain raw logits and component vectors, and independently reconstruct accuracy,NLL,fact/query/
order both-correct metrics and mask drops. Both value assignments and both orders are present in
each split, so all original pair definitions remain valid. No masked row ID is supplied to the model.

For each intervention,seed,split and language report original/changed correct counts,answer flips,
wrong-to-correct and correct-to-wrong transitions,accuracy/NLL delta,raw-logit maximum difference,
and original pre/post/read mean vector norms. These are descriptive measures,not a new accuracy gate.

## Workload and interpretation limits

Five models x4 modes x2 splits x3 views =120 full-model forwards.
Each model sees4x3x(64+32)=1152 rows;total5760. Additional normalization recomputations60.
One parent bundle deserialization,five strict state loads,zero training,zero new learned checkpoints.
Raw-output archive serialization is real work,not a checkpoint rewrite or an extra independent sample.

PASS means diagnostic integrity only,regardless of whether an intervention improves,damages or
leaves the scores unchanged. It does not change C252,establish seed robustness or promote Gate F.
A decline may reflect co-adaptation or changed activation scale/distribution at LayerNorm,not a
unique reasoning mechanism. Unchanged performance means that vector was dispensable under this
frozen intervention,not that the core was irrelevant to learning or other tasks. Pre-core EOS already
summarizes the whole prompt;pre_residual is not an isolated raw-token control.
No answer repair,production adoption,model expansion,external corpus or paid API. Judge C253 before C254.
