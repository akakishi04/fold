# V5-B mean-plus-final dual query v0.1 — C278

C277 showed that lowering lr mainly rescued one broad bad seed and did not generally improve the
already-stable cohort. In shared_suffix2,lr0.0025 reduced answer/query-pair failures but increased
evidence/query-drop failures. The next intervention therefore returns to query representation.

C269 established reliable two-character binding with mean query-span pooling.
C274 established that final_boundary is broadly stronger than first_boundary.
C273 tested first+final dual attention and did not solve the task.
The specific combination mean-span + final-boundary has not been tested.

C278 compares:
- mean_span: the actual C269 SpanQueryReadout.
- mean_final_dual: identical parameters/state keys; one query from the mean visible query-span
  pre-core state and one from the final visible query-byte pre-core state. Both use the same
  read.query/read.key weights,produce separate masked softmaxes,retrieve separate memories,and
  average those memories before the single shared read.output and unchanged post-core residual.

Fresh seeds278001..278005. Both arms start from identical14256-parameter tensors with disjoint
storage and use identical paired minibatches. Train exactly800 updates with mean CE and AdamW
lr0.005. No additional loss,parameters,training steps,checkpoint selection or seed replacement.

Evaluate every final state on the complete C267 two-character task and C270 unseen three-character
task using the unchanged accuracy/query-pair/evidence-drop/query-drop/two-order gates.

Primary candidate PASS requires all five mean_final_dual states to pass BOTH complete tasks.
mean_span is the matched control and cannot rescue or fail the candidate.

A valid candidate miss is accepted without another fusion tweak inside C278.
