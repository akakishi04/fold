# V5-B saved answer-role audit — C292

C291's answer-wise auxiliary and CE each passed4/5 quad gates;pair_sum passed2/5. Answer_margin
helped answer counts on291003 but did not clear that seed's seen-length HOLDOUT. Its normal
TRAIN examples were all correct. This does not establish superiority over ordinary CE.

The next question is not another coefficient setting. An incorrect answer could be the value
attached to the other presented entity,or a value absent from both facts. These imply different
observable failure patterns and should not be lumped together as a single binding error.
C292 separates them using the verified logical data and frozen full256-class predictions.

This is descriptive,not causal. Emitting the other value does not prove an attention misroute;
emitting an absent value does not prove memorization. No restricted decoder is introduced and
no prediction is corrected. All masks and capability gates remain the original parent's gates.
The complete cohort and value splits stay fixed. Exact paired changes prevent equal aggregate
accuracy from concealing a trade between in-context errors and unsupported outputs.
