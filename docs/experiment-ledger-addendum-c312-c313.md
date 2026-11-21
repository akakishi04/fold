# C312 formal acceptance — valid negative

C312 ACCEPTED VALID NEGATIVE. The registered value_balanced five-character gate is4/5,
not5/5. The random_pairs comparator is5/5. Do not switch the parent primary after results.
Gate F NOT PASSED. C313 NOT REGISTERED in this acceptance commit.

## Evidence identity and validity

Scientific execution:f481ae2b547bccc5cd5f43ae2654f89e8fa3140f.
Published log:16e55cffe274ac24a456cb28b650fca3140d8789.
Log SHA256:87f29ce3c496295512deb19c95a0fbfa2d1edf2cd2d38684a273dfc24177c95a.
Log bytes:793925. Publication changes latest.json/latest.log only.
Summary:runs/c312-v5b-value-batches-c23759c73f5c4bfbb03a7c3d9c8e8198/summary.json.
Summary SHA256:2bb0efc9a9f128a0aeda9585dabab4ee0c672ba2e9b31f4b148cc6ba959a5ed6.
Manifest:5c543202a3c252e69f3f099b369ef9905e39662a37947c8904756b17700fab2c.
Own32/focused4997 PASS;source718/protected1343. All10 fits/replays completed.
all_pairs_matched=True;persisted_value_batches=PASS;run_execution_valid=True;
tracked tree clean;scientific HEAD preserved. No C312 retry justified.

## Deciding measurements

Both arms pass5/5 on lengths2,3,4. Five:random5/5,balanced4/5.
Paired five:both_pass4,control_only1,candidate_only0,both_fail0.
All trained-length normal TRAIN/HOLDOUT answers are correct in both arms.
Only balanced312002 has wrong normal outputs:five TRAIN-value575/576,
HOLDOUT-value286/288;all other normal output partitions are perfect.
Its five HOLDOUT fails local accuracy/query-pair/query-drop/two-order criteria.
The five TRAIN-value partition passes its full gates despite one error.
Do not interpret a gate failure as zero accuracy or change local thresholds.

## Interpretation boundary

No measured improvement from value-balanced batching in this cohort;do not adopt it as
a default. The three normal errors are not proof that balancing always harms generalization.
Random_pairs is the unchanged baseline,not a model selected per problem. All10 states stay.
The baseline5/5 is a bounded observation on this cohort,not independent proof of arbitrary
length or value generalization. Preserve C308/C309 and every other prior verdict.

## Next question before registration

Instead of tuning batching or retrying seeds,measure a new held-out identifier length6
using all frozen C312 models and the SAME64-slot architecture. The prospective primary
would be all5 retained random_pairs baseline models passing the existing local/masked
six-character criteria;balanced remains a full comparison cohort,including312002.
This changes the evaluated task,not the old C312 gate. No new training,seed replacement,
model/frame changes or outcome-dependent selection. Require original2..5 outputs before
and after to reproduce their C312 archives. Register/review separately before execution.
