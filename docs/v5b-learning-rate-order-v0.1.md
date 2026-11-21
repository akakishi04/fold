# V5-B learning rate by minibatch chronology v0.1 — C263

C262 showed that changing only the order of the same minibatches changes answers and
held-assignment scores. Reversal improved some pairs and worsened others. The next
question is not whether to adopt reversal; it is whether a smaller learning rate can
make both chronologies work reliably at the same fixed training budget.

Use a predefined2x2 design:learning rate0.005 or0.001,each with forward and reverse
blocks. Five fresh seeds263001..263005 create five groups of four identical initial
Full aligned-reader models. All14256 parameters,architecture,optimizer settings other
than learning rate,and exposure totals remain the same. Same-order rate pairs see
exactly the same minibatch at each update. No old learned state is continued.

A lower learning rate might help,have no effect,or fail to learn sufficiently within
800 updates. All are reportable. Do not add steps to the lower-rate arm after observing
its loss. Do not sweep rates or discard the less favorable chronology. The experimental
change is scalar learning rate within each chronology,not a new model mechanism.

Reuse the original distinct-value assignment task and all-six-order training. Keep
HOLDOUT assignments out of optimization. The minibatches are A,B,C versus C,B,A within
each complete epoch;the final two are A,B versus B,A. Preserve each batch's contents
and internal row order. The same questions appear the same total number of times.
Both rates use the same schedule and copied initialization for a given seed/order.

The primary capability gate requires all five lower-rate models in BOTH chronologies
to pass the unchanged per-language,per-order,TRAIN/HOLDOUT and masked-input criteria.
Standard-rate gates are separate. Also report how learning rate changes paired accuracy,
all-six consistency and chronology-dependent answer disagreements. Every comparison
retains all seeds and both languages. A lower disagreement count is not beneficial
robustness if two models merely make identical wrong answers; report the worse accuracy
of the two chronologies alongside disagreement. A capability PASS alone is not evidence
that lowering the rate beats the standard setting. Comparisons remain descriptive.

There are20 model runs,not10:two rates x two chronologies x five seeds. Each has800
updates,batch48. Total16000 updates,768000 training inputs,16480 model forwards and
871680 input rows including final scoring/strict replay. This doubles C262's model
workload. One20-state final bundle is written/loaded,20 states strictly loaded.
Final-logit raw payload is about106 MB,plus checkpoint and metadata. Historical tests,
parent validation and hashing are additional work rather than scientific samples.

Save final logits and actual schedule metadata;recompute metrics,flips and interactions
from these artifacts. Match fingerprints,exact argmax and1e-9 logit replay. Protect424
source pins and710 inputs. Own24 and focused3477 plus Windows parser chain precede
formal training. Synthetic authoring fixtures do not establish production capability.

No C262 verdict changes. No general language,independent-benchmark,architecture winner,
production adoption or Gate F claim. Results apply to this fixed task,budget and pair
of rates. Integrity faults require same-C263 repair;valid scientific misses are accepted.
C264 remains unregistered until C263 is judged.
