# V5-B training-time core ablation v0.1 — C260

## Why this comparison

C259's six-order training improved the measured paired outcomes,but only4/5 treatment seeds passed.
The remaining seed fits its TRAIN assignments and still fails HOLDOUT. This does not identify the
core as the cause. Before adding more mechanisms,measure what the core contributes under this
same six-order training policy. The Full path remains an unchanged experimental reference.

One question:can the local-encoder plus aligned-reader path,without the state-update core,meet the
same bounded assignment criteria when trained from scratch,relative to the Full reader?
This is a structural ablation during learning,not removal of a pathway only after co-adaptation.

## Two branches

with_core:actual C252 aligned pre-core query/key/value reader,added to actual post-core EOS,
followed by the original normalization and decoder.14256 parameters.
without_core:copy the same encoder,reader,normalization and decoder,remove the copied core,and add
the reader output to pre-core EOS instead.10928 parameters.3328 core parameters are absent from
this branch's state dictionary,not retained as zero-use padding.

The new forward uses the actual causal GRU encoder and the same query/key maps,score scale,PAD mask,
weighted memory and output map. It does not replace the reader with an oracle or sort the prompt.
There are no core calls in the ablated branch. The Full path still evaluates both teacher routes
for two internal steps;the experiment separately counts four core calls per Full model forward.

Five fresh seeds260001..260005 create paired models with exactly equal surviving initial state.
Initial logits and complete state dictionaries need not match because the pathways differ.
Both branches are trained;neither is initialized from accepted learned checkpoints or chosen only
because an earlier seed failed. This does not modify the production/default architecture.

## What is held fixed

Same C256 assignment split,three distinct values per assignment,bilingual identifiers,all six fact
orders and48-byte-slot contract. Same six-order schedule as C259:paired logical questions and targets,
three48-row blocks per epoch,and three cycling order pairs.800 updates per model,including the fixed
incomplete tail;no HOLDOUT assignment is optimized. Same AdamW settings and per-arm RNG reset.

The pair is not parameter- or FLOP-matched. Removing the core changes parameter count,optimizer state,
gradient paths and the vector subject to global clipping. These are part of the specified structural
ablation. A gain cannot uniquely identify the internal cause of C259's remaining miss.

## Gate and measurements

Retain C259's original-order and per-additional-order criteria,mask-drop thresholds,and all-six-order
consistency requirement. Primary PASS requires all five core-free seeds to satisfy all conditions
on both languages and both assignment splits. Full-reference results are reported independently.
All ten paired HOLDOUT language comparisons include all-order accuracy and six-order consistency.
A primary PASS does not by itself establish an advantage:both branches could pass. A valid miss is
accepted negative rather than repaired by extra steps,selected seeds or relaxed thresholds.

All evaluated orders were taught in both branches. Success is held-assignment performance under
covered orders,not unseen-order transfer or general language understanding.

## Cost, evidence and stopping

Ten models,8000 updates,384000 training presentations. Final scoring plus strict checkpoint replay
bring the total to8240 model forwards/435840 row presentations. The five Full branches execute16480
core calls in total;core-free branches execute none. Parent validation and historical tests are
separate computational work. The two branches are not a wall-clock-matched speed benchmark.

Save ten final states and final per-view output tensors. Strict loading verifies fingerprints,
raw-logit error<=1e-9 and exact argmax. Persisted postcheck reconstructs metrics and comparisons from
saved tensors without another model evaluation. Protect406 source pins and672 inputs.
Own24 and focused3405 must pass before formal training. Parse dispatcher,launcher and runner first.
Only text execution logs are published;checkpoints and generated data remain in ignored runs/.

C259 remains accepted negative whatever C260 finds. No core removal from the design,production
adoption,Gate F promotion,external corpus,paid API,cleanup or CI changes follow automatically.
C261 is unregistered and must wait for C260 judgment.
