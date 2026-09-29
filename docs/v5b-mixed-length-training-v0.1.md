# V5-B fixed-budget length coverage — C282

C281 reconstructs heterogeneous effects of evidence-only attention support. The apparent overall
mask-criterion improvement is heavily influenced by the shared bad seed280004. More importantly,
both tasks and both arms have zero mask-only failing answer cells:normal answer/query-pair
correctness also fails wherever an answer cell fails. This does not prove mask criteria universally
redundant,but it weakens the preceding isolated-evidence-dependence explanation.

C282 changes training length coverage rather than another query/support parameter. Both arms use
the actual C278 all-token mean/final dual readout. Two-character-only training is compared with
alternating two- and three-character normal TRAIN examples. Logical rows,target assignments,
minibatch pairing,800-step budget,optimizer and capacity are held constant. Every logical row still
appears200 times;the candidate allocates100 to each length instead of200 to two-character forms.

The purpose is to distinguish a length-extrapolation barrier from a failure to learn these bindings
even with direct coverage at the registered budget. It is not a capability shortcut:the candidate
no longer qualifies as unseen-length transfer. Its held-out evaluation tests unseen value
combinations at seen lengths. C270's original transfer failures remain accepted and unchanged.

A candidate PASS would justify studying how to obtain transfer beyond covered lengths in a later
experiment. A miss would point back toward learnability/optimization at fixed capacity and budget,
not prove any universal inability. Neither result automatically promotes Gate F.

Implementation keeps inherited models,renderers,scorers and checkpoint-replay functions unchanged.
The child owns length scheduling,TRAIN-table selection and exposure validation. It records hashes
of the complete training table and logical/rendered schedules,tests both valid and invalid seals,
and verifies control/candidate roles through actual result validation rather than source-only claims.
