# V5-B query endpoint v0.1 — C271

C269 established that visible query-span pooling can make the trained two-character name family reliable across five seeds. C270 then showed that the same frozen mean-pooled reader does not reliably transfer to unseen three-character shared-prefix/shared-suffix names, even though simple tripled names are easy.

C271 tests one structural hypothesis: arithmetic mean pooling may dilute the byte position at which similar query names diverge. Compare two fresh, exactly matched readers:
- mean_span: the accepted C269 span_query architecture;
- endpoint_span: identical parameters and state layout, but read.query receives the pre-core local state at the final visible query byte, immediately before the final '='.

The local encoder is causal, so the endpoint state can carry the preceding query bytes without averaging all query positions. This is a motivation, not a claimed mechanism.

Both arms use fresh seeds271001..271005, identical initial tensors, the exact C267 two-character TRAIN/HOLDOUT dataset, identical paired48-row batches, ordinary CE only, AdamW lr0.005 and800 updates. No C269/C270 learned checkpoint initializes C271.

Evaluate every final model on both:
1. the original C267 two-character task; and
2. the C270 unseen three-character task (tripled/shared_prefix2/shared_suffix2).

Primary PASS requires all five endpoint_span seeds to satisfy every fixed gate on BOTH tasks. mean_span is a matched control and cannot rescue the candidate.

A PASS would support endpoint query state as a better bounded length/composition transfer design under this task. It would not prove arbitrary-name understanding, general parsing, or Gate F completion. A valid miss is accepted without retuning pooling, seeds, steps, thresholds, or training data.
