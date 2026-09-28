# V5-B saved learning-rate failure-profile audit v0.1 — C277

C276 validly failed its all-five capability gate. Lowering AdamW lr from0.005 to0.0025 improved
two-character retention from4/5 to5/5 and removed the broad control failure at seed276003, but both
arms remained0/5 on the complete three-character task. Aggregate shared-prefix/tripled answers
improved at0.0025, while shared-suffix collapse worsened.

C277 introduces no new model architecture, training, inference, checkpoint, seed, threshold or
dataset. It audits the accepted C276 persisted measurements to answer one question:

How did lr0.0025 change the exact fixed-gate failure profile relative to lr0.005, by criterion,
seed,split and profile, especially shared_suffix2?

For every C276 fixed answer-cell criterion and two-order criterion, reconstruct signed threshold
margins and failure membership. Persist arm-specific counts and candidate-minus-control deltas for:
- accuracy;
- query_pair_accuracy;
- evidence_drop;
- query_drop;
- two_order_accuracy.

Primary reports:
1. all triple-task failures by criterion for lr005 versus lr0025;
2. shared_suffix2 failures by criterion and split;
3. seed276003 recovery;
4. seeds276001/276002/276004/276005 where candidate pooled totals may improve or worsen.

C277 formal PASS means only diagnostic execution/integrity: accepted C276 artifacts verify without
neural Module calls, saved measurements reconstruct exactly, and all registered attribution tables
persist/reconstruct. It is not a capability PASS and cannot promote Gate F.

Use the result to decide whether the next intervention should target optimizer reliability further
or return to the shared-suffix representation/task structure.
