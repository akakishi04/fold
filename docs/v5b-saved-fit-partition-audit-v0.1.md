# V5-B saved final-fit versus generalization audit — C287

C286's cosine tail improved quad gates2/5->3/5 but did not rescue286002/286003 on any complete task.
The verified common first400 updates make this a valid late-LR comparison. They do not show whether
remaining errors arise on optimized TRAIN examples or only at held-out values and unseen length.

C287 separates those observations rather than guessing another LR/architecture change. Actual normal
TRAIN errors and final TRAIN NLL measure fitted-example performance. Seen-length HOLDOUT measures
held-out value combinations;quad tests unseen names/length on both inherited value partitions.
Direct answer/query-pair/order criteria and mask criteria are kept separate. A whole task miss does
not imply poor TRAIN fitting. A high pooled accuracy does not override a failed local gate.

The saved800-step CE history is a second,descriptive view. It comes from alternating mini-batches
at changing model states. Grouping by fixed length/profile/window prevents a change of input type
from being mistaken for a temporal loss trend. Even these grouped traces are not final full-data
losses and do not prove convergence,overfitting or an optimizer mechanism. No trace selects a model.

All10 states are retained;the diagnostic creates no independent replication. Conditional patterns
inform a subsequent preregistered question only after judgment. No new data,weights,training,
forward call,state loading or checkpoint is introduced. C286 and every prior verdict stay fixed.
