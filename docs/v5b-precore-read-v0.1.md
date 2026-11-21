# V5-B pre-core memory with post-core query v0.1 — C251

## Question

Does changing only Full's reader memory source from post-core states to pre-core local encoder
states improve the same five initialization blocks, while retaining the core for the query and
ordinary residual path? This is an adaptive architecture comparison, not a C250 retry.

C250 reproduced individual successes, but Full/token_read passed only2/5 whole seeds, versus4/5
for GRU/token_read. This motivates a matched Full comparison; it does not prove that the core
caused the failure or that GRU is generally superior. No seed,failed result or language is dropped.

## Exact computational change

C250 Full:the query, residual pooled state, keys and values all come from final core outputs.
C251 Full:query and residual pooled state remain the actual final core EOS state. Keys/values use
local causal GRU token outputs multiplied by the original nonPAD mask, exactly the context entering
the core. Both core routes and all original internal steps still execute unchanged.

The original C248 ResidualHead is reused:Wq/Wk/Wo,16-dimensional states,768 additional weights,
softmax temperature divisor4,all nonPAD positions including BOS/EOS/query tokens. No new parameters,
new learned gate,fact parser,answer-location labels,additional loss or output-class restriction.
The entire backbone and head train jointly. The memory tensor is not detached; its gradients reach
the encoder. The query path still reaches the core. Memory source changes both the forward
computation and gradient paths,so improvement does not isolate information loss or a unique cause.

The wrapper calls the original backbone once. Local/core hooks validate that memory equals the
actual context passed into the core, that both routes run the expected number of times, and that
the query is the post-core EOS state actually supplied to readout_norm. Every hook is removed even
on exceptions. Padding is masked using the inherited reader behavior. No public runtime is changed.

## Matched experiment

Use all five C250 seeds250001..250005,including successful250003/250005 and failed seeds.
Use Full only:five fresh candidate models. Reuse the accepted C250 Full/token_read endpoints as
the post-core comparator; do not retrain them or select the better of repetitions. No additional
GRU or EOS control is required for this specific Full memory-source comparison.

Before training,match both the bare backbone fingerprint and the full wrapper/head initial
fingerprint to the corresponding C250 saved initial states. The original head seed+248000 and
zero output projection remain unchanged. The zero residual makes initial outputs equal despite
the different memory source. Reuse the C250 fresh-reference initial TRAIN metrics, not trained
weights. No accepted checkpoint is deserialized.

Same TRAIN64/HOLDOUT32,byte strings,row order,targets,provenance and three original scoring views.
Same actual C248.train_one/fit,400 updates,batch32,old32/added32 alternating normal batches,
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,CPU float64,threads2,determinism.
Total parameters14256=13488+768. No extra training or inference masking. HOLDOUT is evaluated only
after step400 and reload; it never changes optimizer settings,endpoint or seed selection.

## Gate and accounting

Primary:every candidate seed passes both languages and both splits under the existing criteria:
accuracy>=0.90;fact/query/order pair>=0.80;both mask drops>=0.35.
TRAIN32 rows/language requires29/32 and13/16 pairs;HOLDOUT16 requires15/16 and7/8 pairs.
Report per-cell metrics,whole-seed pass count out of5 and paired differences versus C250.
Even one failed seed retains an overall valid negative. A pass remains limited to this reused
internal task and seed batch. It is not an external replication or production/Gate F adoption.

5x400=2000 updates/64000 training presentations. Each model415 forwards/13568 rows including
initial/final/reloaded scoring. Total2075 model forwards/67840 rows;75 evaluation forwards.
No new-reference or comparator forwards. One new five-state checkpoint bundle.

A valid miss is ACCEPTED VALID NEGATIVE. Source/artifact/schema/count/initialization/nonfinite/
replay/test faults are INVALID / RETRY SAME C251. Do not rescue C250 or change its verdict.
Preserve accepted sources/tests/logs. No paid API,external corpus,model expansion,cleanup or
history rewrite. Numeric-memory and erasure-mixture tuning remain paused. Judge C251 before C252.
