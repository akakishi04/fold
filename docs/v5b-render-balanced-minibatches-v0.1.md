# V5-B rendering-balanced minibatches — C296

C295's fixed CE extension rescued one near-complete four-character case but did not remove two
trajectories' failures on trained inputs. Further extending or adjusting another auxiliary loss
is not the only available intervention. The existing pipeline shows one rendering type for an
entire epoch:two lengths times three identifier profiles cycle across six epochs.

C296 compares that batching with a deterministic redistribution of the SAME rendered examples:
every complete24-update block contains the same six rendering queues in both arms,but the
candidate takes four intact pairs from every queue per minibatch. The final8 batches are shared.
No new data,capacity,label,loss information or per-model updates are added. Gradients now combine
rendering types within an update rather than only through optimizer history. Whether this helps
binding or untrained-length transfer is an empirical question,not a predicted result.

Ordering and within-batch composition change together;the study cannot isolate gradient conflict,
forgetting or gradient-noise effects. A failure does not prove architecture impossibility. A
success requires separate evaluation of superiority and broader generalization. Existing gates
and all seed pairs remain,with original full-class decoding and no oracle candidate restriction.
