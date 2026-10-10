# C317 formal acceptance — diagnostic integrity PASS

C317 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY). C318 NOT REGISTERED here.
C316/C315 remain valid negatives. C308 bounded PASS and Gate F NOT PASSED unchanged.

## Evidence and validity

Scientific execution:3ecd3a638726f86b294f0fe94d53a2fc5d082e01.
Publication:a948757c3f2a0e524bdef50521cf4034b900fc2a.
Log SHA256:f21c40608fa03f6f66400766de053caf2a63dec76ffb568271cd9f7fd02d941d;1022646bytes.
Summary:runs/c317-v5b-query-endpoint-88ae97edc7d44cd3bcd9732e66c8b14e/summary.json.
Summary SHA256:09632cda7689c9b23229ec993d19c108ac23a7bb142285cd58b11bcc713d8cb5.
Own32/focused5149 PASS;focused5149 completed in569.368s. Sources748/inputs1407.
All10 frozen checkpoints completed original/first-byte/original passes. Both old-output
replay errors are0.0 for every state;all degenerate one-byte controls hold. Preserved
weights/hooks,stored reconstruction PASS,run_execution_valid=True,clean tree/HEAD preserved.
Publication touches only c317/latest.json and latest.log. No training or new model checkpoint.

## Deciding results

Original both arms:5/5 at lengths2,3,4,5;4/5 at6. Replacing the last query-byte anchor
with the first yields0/5 for BOTH arms at EVERY scored length2..6. This is a large
loss of local/masked gate coverage,not zero answer accuracy. Do not adopt this substitution.
Example,not all-group aggregate:one_to_four316005 length6 HOLDOUT shared_prefix normal
English48/48->24/48 and Japanese48/48->23/48. Shared_suffix English48/48 remains unchanged,
Japanese48/48->43/48. Successes and harms depend on context;do not generalize one group.

## Interpretation boundary and next question

C317 changes an input to an already trained shared query projection. It does NOT compare
models trained for first versus last anchoring and does not prove first-byte information
intrinsically useless or identify the unique source of six-character errors.
The native mean-plus-last readout was jointly trained. To separate sensitivity to the
new first-byte input from contribution of the two existing branches,propose a frozen
mean-only versus last-only branch-isolation diagnostic with original-before/after controls.
Preserve all10 C316 states and all1..6 inputs. Preserve total memory scale by duplicating
one native query branch in the two existing projections;do not halve the memory term.
Keep original computation/weights and no answer-dependent endpoint selection. This is
not a trained replacement,capacity improvement or Gate F promotion. Register/review separately.
