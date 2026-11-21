# V5-B supervised query-pair assignment loss — C288

C287 located four C286 states' first failures on actual optimized normal TRAIN,not just unseen
values or longer names. Their different queries often collapsed to the same answer. Constant and
late-decayed LR both missed;decay substantially worsened seed286002. The evidence does not justify
further blind LR tuning or another failure-clustering pass before intervention.

C288 tests a training objective change with fresh seeds. Ordinary rowwise CE is retained. The
candidate additionally scores whether two existing same-facts/different-query examples assign
their two TRAIN target values correctly versus swapping those assignments. A smooth pairwise
penalty encourages question-specific answer differences. No teacher,extra data,forward call,
trainable parameter,model-input metadata or inference-time restriction is introduced.

This is not a proven remedy. The auxiliary term may be redundant with CE,change optimization scale,
trade calibration for margins,or hurt generalization. A summed pair margin alone can conceal a
weak individual answer,so CE and the unchanged cellwise gates still decide performance. A favorable
result supports this objective policy at this budget,not unique causal diagnosis of collapse.

Use identical mixed2/3 training and constant LR.005 in both arms,800 updates,all5 fresh seed pairs.
Do not warm-start only formerly failed models. Freeze final models before two/three/four scoring;
four remains untrained. Primary is the fixed all-five four-character gate;all-task and TRAIN/HOLDOUT
results are reported separately. Direct fitting diagnostics are included in the same final output.
C287 PASS remains diagnostic only;older valid negatives and Gate F are not changed by this design.
