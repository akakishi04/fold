# V5-B saved fact-order bias diagnostic — C323

C321 failed new equal-length, equal-endpoint, equal-character-count names on both frozen policies.
C322 showed 90%+ query-pair argmax collapse but non-identical scores; output response was weak,
not mathematically constant. C323 asks a narrower question using **the same saved logits**:
are the collapsed predictions better described as following the first or last written fact?

Hold the names, two values and requested entity constant; use both permutations of the two
facts. Each permutation has both query directions, so four predictions can be classified as
first-following, last-following, all-value-locked, or a more complex mixture without changing
inputs or selecting a better model. Reconcile every answer and collapsed pair back to C322's
published 256-class results. Include the original correctly learned four-character patterns as
positive controls and all models, languages, value splits and name families.

If a position heuristic dominates, design a fresh controlled training intervention later;
this diagnostic alone neither proves the internal mechanism nor validates a fix. If not,
character-order representations and attention/reader mechanisms remain possible hypotheses.
No new training or neural calls; Gate F remains NOT PASSED.
