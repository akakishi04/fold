# V5-B saved gate-failure audit v0.1 — C275

C274 completed as a diagnostic-integrity PASS. final_boundary was substantially stronger than
first_boundary and four final-boundary seeds had near-perfect pooled three-character HOLDOUT answer
totals, yet every final-boundary state failed the complete three-character task gate.

C275 introduces no new model architecture, training, inference, checkpoint, seed, threshold or
dataset. It audits the already accepted C274 persisted measurements.

The one question is:
Which exact fixed gate components reject final_boundary on the three-character task, and are those
failures concentrated in the broad bad seed274003 or also present in the four near-passing seeds?

For every C274 arm/seed/task answer cell, reconstruct margins to the fixed thresholds:
- normal answer accuracy minus0.90;
- query-pair accuracy minus0.80;
- evidence-drop minus0.35;
- query-drop minus0.35.

For every two-order record, reconstruct accuracy minus0.80.

Persist every negative-margin failure with its seed,arm,task,split,profile,language,entity subset and
visible order where applicable. Aggregate counts by criterion,seed,split,profile and arm.
Predeclare the primary focus as final_boundary + triple task. Explicitly separate:
- broad seed274003;
- near-passing seeds274001,274002,274004,274005.

C275 formal PASS means only that accepted C274 artifacts were verified without neural Module calls,
the saved metrics were reconstructed exactly, all registered failure-attribution records were
produced, and the persisted audit revalidates. It is diagnostic integrity only.
No capability winner or Gate F promotion is possible in C275.

The diagnostic result should determine whether C276 should address normal answer binding,
query-pair discrimination,mask sensitivity,two-order consistency,or optimization reliability.
