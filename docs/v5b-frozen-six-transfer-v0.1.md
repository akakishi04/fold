# V5-B frozen transfer to six characters — C313

C312 did not support adopting balanced-value minibatches:balanced4/5 vs random5/5 at unseen5.
Only balanced312002 had normal errors:one TRAIN-value and two HOLDOUT-value questions.
Do not chase those three questions with another tuned batching rule. Keep the original random
baseline,retain all balanced comparators,and test a new boundary with the same frozen states.

Training remains2/3/4. Test6 without retraining and without a larger input frame. The longest
Japanese prompt occupies63 of64 slots including BOS/EOS,so no truncation or language exclusion
is permitted. The three name families and value splits stay fixed;this is not new syntax or a
fresh data-domain evaluation. C313 tests one additional length,not arbitrary-length reasoning.

Original2..5 outputs before and after six must reproduce C312 in all normal/masked views.
The prospective primary is all5 retained random baseline states passing the six local gates.
Balanced results are reported separately,not selected per row or used to replace that primary.
A new six PASS cannot rewrite C312's negative or promote Gate F. A valid negative also does not
cancel prior bounded successes. Both outcomes locate a boundary rather than identify a cause.
