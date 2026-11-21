# V5-B final-boundary optimizer reliability v0.1 — C276

C275 established that the four near-passing C274 final-boundary seeds all share answer-accuracy and
query-pair failures, while mask-drop failures are not common to all of them. Seed274003 is a broad
failure across every criterion class. C273/C274 also show that the current architecture can reach
very strong or locally complete states, but reliability varies sharply across fresh seeds.

C276 tests one optimization hypothesis without changing architecture, loss, data, steps, gates or
checkpoint policy:

- lr005: final_boundary with the accepted AdamW learning rate0.005.
- lr0025: the exact same final_boundary architecture and training policy with learning rate0.0025.

Fresh seeds276001..276005. Within each seed the two arms start from identical14256-parameter tensors
with disjoint storage and use identical paired minibatch order. Both train for exactly800 updates on
the C267 two-character TRAIN split with ordinary mean CE. No extra steps, early stopping, checkpoint
selection or post-hoc seed replacement.

Evaluate every final model on the complete original two-character task and the C270 unseen
three-character task. The candidate lr0025 PASS condition is unchanged in spirit from prior
capability tests: all five candidate states must pass BOTH complete fixed tasks. lr005 is a matched
control and cannot rescue or fail the candidate.

A PASS would support the claim that a more conservative fixed optimizer step improves fresh-seed
reliability in this bounded task. It would not prove arbitrary-name generalization or Gate F
completion. A valid miss is accepted without trying additional learning rates inside C276.
