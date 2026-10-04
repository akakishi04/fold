# V5-B frozen readout-term diagnostic — C300

C299 did not isolate a universally successful core initializer. Some recombinations created
seen-length TRAIN failures,while the same core with another remaining backbone worked. Another
subdivision of initial weights would not by itself show how the trained pathways contribute.

The current model combines a post-core residual with an additional pre-core-memory reader before
normalization. C300 leaves the trained weights and every upstream computation unchanged,then
measures the result of passing either summand alone through the same normalization/classifier.
It tests all9 models and every old input,not only failed cases. A normal pass before and after
must reproduce all old predictions;temporary hooks and fingerprints must be restored.

Improvements and regressions both matter. Removing one term may rescue an answer but break many
others. It may change hidden-state scale/distribution rather than reveal a uniquely faulty
component. No per-query best-of selection,restricted answer decoder,retraining,automatic adoption
or revised capability gate is introduced. This bounded inference diagnostic cannot establish
which initialization or optimization mechanism caused the original training outcome.
