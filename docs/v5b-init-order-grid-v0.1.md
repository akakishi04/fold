# V5-B initialization/order grid — C297

C296 mixed batches improved the count of fully passing quad seeds2->3 while worsening another seed
and TRAIN fitting5->4. Repeated local modifications have not established a uniformly robust policy.
Each historical seed selected both initial model weights and shuffle order,so a failed paired seed
alone cannot distinguish sensitivity to its initial state from its example stream.

C297 crosses three fresh initializations with three independent fresh shuffle streams. Hold ordinary
CE,blocked renderings,800 updates and fit-time RNG fixed. Rows share exact initialization;columns
share exact example schedules. The full nine-cell grid can show row-associated,column-associated
or combination-specific changes without another objective or architecture intervention.

This is a finite diagnostic,not a guarantee of identifying a unique cause. One run per cell and
three chosen levels do not support population variance claims or statistical tests. All-pass or
all-fail outcomes are possible and may leave the issue unresolved. Neither justifies editing the
grid after observing it. Keep old full/masked gates and report all cells. Its integrity PASS is
not a newly easier capability PASS;no winning cell becomes a deployed or official replacement model.
