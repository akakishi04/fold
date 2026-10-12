# V5-B interior name-order transfer — C321

C320's mean_last cohort passed both unequal-length layouts. Such names can also be distinguished
by length. To probe a different boundary,keep both names four characters long with equal first/
last symbols and identical character histograms. Only the order of the two interior symbols
differs. Examples:aaba/abaa,aabb/abab,babb/bbab,with the same construction in Japanese.

No extra training or changed readout. Keep all C319 states and require original-output replay
before/after. This is a new frozen task condition,not a retuning of the previous negative readout
experiment or a claim that the prior success was invalid. The learned local encoder is not
assumed to be bag-of-characters:matching input histograms does not guarantee equal hidden means.

Success is limited to these three templates/value splits/checkpoints. Failure would locate a
name-order transfer boundary but would not isolate a unique architectural cause. Do not choose
per-row models or reduce the declared all-five/all-profile gate after observing results.
