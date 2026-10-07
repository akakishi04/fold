# V5-B saved value-renaming diagnostic — C310

C309 fitted TRAIN at trained lengths but retained value-HOLDOUT errors. Extending the name is
therefore not the only observable failure. Compare saved answers to the same relation with values
relabeled. For example, aa=0;bb=2;aa= and aa=1;bb=3;aa= should have answers that follow the mapping
0->1,2->3. The closed dataset already includes both, so no new inference or training is needed.

Keep all15 states, all2/3/4/5 lengths and original splits. Enumerate24 bijections of0..3. Separate
changed inputs, identity controls and absent-value-only swaps. Always choosing the other fact or
a constant non-value byte can be consistent and still wrong; count both explicitly. No output
filter or better-answer substitution. Preserve argmax tie behavior and report tied maxima.

This describes observable renaming sensitivity, not a causal memory/attention explanation or
new general-language ability. Comparisons reuse outputs, reverse directions and displayed
counterparts, so their count is not an independent sample size. C310 PASS is diagnostic integrity
only. Past verdicts and Gate F stay unchanged.
