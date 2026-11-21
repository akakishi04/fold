# V5-B value-balanced minibatches — C312

C311's slow309002 five-HOLDOUT errors are17 unmentioned digits and2 other-fact values.
13 of19 failures already occur at length4;6 are introduced at5. Errors span all4 HOLDOUT value
pairs. This does not prove a batching cause or show that unseen-length transfer is solved.

C312 returns to a training intervention:at fixed core_slow,compare random versus value-balanced
minibatches while retaining exactly the original TRAIN examples,epoch counts and render schedule.
Every candidate minibatch has3 intact query pairs from each of8 TRAIN ordered-value strata.
The same random rank supplies both schedules;all96 pairs are consumed once per epoch. Both arms
have1200updates and100 exposures/row/length. No held-out pair is introduced as augmentation.

This differs from C296's mixing of identifier lengths/profiles. Here each epoch's length/profile
remains unchanged;only value-pair batch allocation and its induced temporal order differ.
It is a conditional test on core_slow,not a claim that batch imbalance,attention or memorization
caused the old failure. Compare all new seed pairs and all original normal/masked gates. Do not
select the best outcome or reinterpret balanced gradients as guaranteed better generalization.
