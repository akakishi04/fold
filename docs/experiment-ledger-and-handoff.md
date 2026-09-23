# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C237 ACCEPTED PASS (diagnostic integrity only). C238 ACTIVE / NOT YET JUDGED. C239 NOT REGISTERED.**
C238 is the unique ACTIVE experiment, a minimal TRAIN sampler intervention, not a Gate F run.
C236 and C234 remain ACCEPTED VALID NEGATIVE. C235 remains diagnostic-integrity PASS only.
Post-authoring review is PASS; authoritative runtime prechecks and regression remain mandatory.

## Latest accepted evidence — C237

Scientific execution HEAD: `2dec1314181d62fbdf0a7d4c52007a9360921fd2`.
Published log commit: `f59b0012e488978f5733c4e8669eabc74ae47ad6`.
Log SHA256: `f4f6328ca74d96f21ee498da3d1d06f2e754d2abb70a51f0a15a0eccc22361db`.
Summary SHA256: `056fcbe4ebd2f888c0d5d5aa2761a18cd4229ed4af428e8e298d7af3abf55b32`.
Local summary: `runs/c237-v5b-frozen-signal-audit-8dbdc04fdad84f49b41a78388ad0b7fb/summary.json`.

24 own tests PASS in1.565s;2857 focused tests PASS in62.308s.
36 model forwards/576 row presentations;zero training.144 paired plus192 masked contrasts;12 cells.
Parent/passive replays and unchanged fingerprints PASS. Persisted trace/contrast replay PASS.
268 source pins/394 inputs protected;tracked tree clean;execution HEAD preserved;run_execution_valid=True.

All48 query-change and48 assignment-swap pairs have different encoder EOS vectors, but all keep
the same answer and0/48 pairs are both correct. Every printed cell has nonzero maximum downstream
readout/logit response. This is numerical sensitivity, not learned binding or a causal diagnosis.
Acceptance uses published execution/postcheck evidence, not an independent rerun of local models;
selected log ranges were read and the full-log SHA is the publisher's recorded digest.

Acceptance/artifact details: `docs/experiment-ledger-addendum-c237-c238.md`.
Acceptance commit: `4794376d53aba9e01c780b8569f1db75f64ca952`.
Acceptance/handoff base: `6c3d4150f42cd43592b5c5a1ef1c18dab9396270`.
No C236 verdict change, generalization or Gate F promotion.

## Preserved C236 comparator

C236 ACCEPTED VALID NEGATIVE. All12 cells:50% accuracy,0/4 fact/query pairs,zero mask drops.
Execution HEAD: `0bc91722ca27803f065d2458505b502a2d01e50f`.
Summary SHA256: `0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec`.
Local summary: `runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json`.
Details: docs/experiment-ledger-addendum-c236-c237.md.
Do not rerun or modify C236. Its initial/final measurements remain separate identities.
C235: diagnostic integrity PASS, failure already on complete TRAIN; its initial invalid attempt
remains recorded. C234/C233 remain valid negatives; C232 remains bounded template-byte learning only.

## Active C238 — complete-cohort sampler

Experiment: C238-v5b-complete-cohort-sampler.
Stage: V5-B-COMPLETE-COHORT-SAMPLER.

One question: with C236's16 TRAIN rows, model, optimizer and400-step budget fixed, does presenting
every row twice in every32-row batch permit minimal seen-TRAIN fitting?
C237 did not identify sampling as the cause. This is a preregistered hypothesis/intervention.

Changed: only the batch-index policy relative to C236. Random32-with-replacement becomes
[0,1,...,15,0,1,...,15] at every step, preserving original cohort order. Every row is presented
800 times per model. Coverage, joint-factor balance and stochastic-gradient variability change
together; the outcome cannot isolate label imbalance alone.

Held fixed: same16 rows, both languages, normal/evidence-blind/query-blind renderer and target bytes;
unrestricted256-byte scoring; Full13488/GRU-only10160 parameters, width16/48 slots;
seeds234001/234002/234003; fresh C236 initial states, not continued final checkpoints.
Match initial_sha256 exactly and initial_probe within1e-9 before any update. Make the common-weight
GRU-only copy before either paired model trains. Reuse accepted C236 final measurements as the
comparator, with no comparator retraining or new comparator forwards.

AdamW lr0.005, betas(0.9,0.999),eps1e-8,weight_decay0,clip1.0,batch32,400 steps/model.
CPU float64,threads2,deterministic algorithms. No loss/architecture/production runtime change.
An executable AST audit allows only the one ids assignment and progress tag to differ from
accepted C236.fit; the training constants must match. The unused local sampler generator is
retained for exact source comparison but never supplies C238 indices.

Fixed scientific workload:6 fresh models x400 =2400 training steps/76800 answer presentations;
54 initial/final/checkpoint-replay forwards/864 evaluation rows;2454 total forwards/77664 rows;
one six-state checkpoint bundle;zero held-out rows or scientific network calls.

Fixed primary gate: every Full seed/language cell must satisfy C236's exact accuracy>=0.90,
fact/query both-correct>=0.80 and evidence/query mask drops>=0.35. With8 rows and4 pairs per
language, exact and pair thresholds require8/8 and4/4. GRU-only gate is separate, not a substitute.
A valid Full miss is ACCEPTED VALID NEGATIVE; an integrity fault is INVALID / RETRY SAME C238.
Even a PASS is only16 seen-prompt fitting, potentially memorization, not unseen binding, useful
language, core superiority, C236 rescue or Gate F completion.

Protection:274 source pins/406 protected inputs;direct dependency union14;OWN6.
Own tests24;modules123;loaded2882/focused2881. Only inherited exact historical exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five local ignored outputs: sampler-plan.json,probe-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Checkpoint schema fold-c238-complete-cohort-v1; six ordered state dicts.
Postcheck revalidates hashes/sizes,plan/cohort,summary,comparator_final and initial identities/metrics.
It adds no model forwards. No accepted source/test/log is edited.

Manifest SHA256: `ae9d0b7e92ee7024b57210f1779aebbfc0757fa995acbdf6f9359b2f23664232`.
Cohort SHA256: `bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c`.
Design: `docs/v5b-complete-cohort-sampler-v0.1.md`.
Registration: `docs/experiment-ledger-addendum-c238-preregistration.md`.
Preregistration commit: `5788eb7598ac3f8f446852d93caa599bcc9fd6e4`.
Use tools/invoke_active.ps1 with the final activation/handoff branch HEAD returned with the command,
not the C237 execution HEAD or preregistration HEAD before this activation.

## C238 post-authoring review

`post_authoring_review = PASS`

Review HEAD: `5788eb7598ac3f8f446852d93caa599bcc9fd6e4`.
Scope: authoring review with synthetic execution; not a formal C238 scientific result.

All six OWN files were re-fetched from the committed review HEAD after authoring finished.
Their remote Git blob identities were mechanically matched against locally tested bytes:
-benchmark: `a77bedb5a33f84675b55d13fed347b2d87d12e63`
-tests: `7b5c63c62a82769b3286e7dff9e9c4b40a2a2b35`
-runner: `41793133962b847d9d3014cc29b6103f8c18c30a`
-launcher: `8e23366ac84fcfb82f2ed579d908282ce42412c1`
-preregistration: `7a931a66abedbc62d4bdc7ad20b0c513bb9139e3`
-design: `88273e869271134e54cb775becc9da6f9e68e830`.

Comparison from acceptance base6c3d4150 to review HEAD changes exactly those six additions.
No accepted parent source/test/log or shared launcher changed.

Checks actually executed after remote readback:
-UTF-8/NUL and all six Git blob checks;
-Python compile/import of complete new benchmark/test modules;
-all24 new tests PASS in2.252s, with actual own-loader count and unique test IDs;
-manifest and independently reconstructed16-row cohort digests match registered values;
-executable fit AST comparison against fetched C236.fit helper source passes with only the
 registered ids replacement/progress tag; altered loss or learning-rate constants are rejected;
-actual fit forwards use all16 rows twice per batch; invalid cohort counts/nonfinite inputs rejected;
-initial-state mismatch rejects before fit; parent before/after field adapters and summary checked;
-actual train_one and accepted C236 replay helper tested with instrumented toy models, verifying
406+3 forwards and12896+48 rows per model;
-actual six-model run and persisted postcheck exercised with synthetic models and substituted
 loader/protection/context;2454 forwards,save/reload,comparator checks and tamper/HEAD rejection;
-actual load_inputs exercised on synthetic hash-matched cohort and C236-shaped measurement files;
-source AST confirms loader/common-copy-before-training and save/load/replay call ordering;
-three embedded Python blocks compile and precheck argv1/2,postcheck argv1/2/3/4 match invocation;
-free-global/import binding audit reports zero unresolved names in both new Python modules.

Parent C236 writer/replay source and C237 context/adapter were re-read: initial_probe/initial_sha256
are pre-training, final_probe is trained; C238 uses fresh models and the accepted final comparator,
not a trained parent initialization. Dependencies in the deciding path remain covered by the14-module
union. Historical counts are accepted C237122 modules/2858 loaded plus the new24-test module:
123 modules/2882 loaded, with the same one exclusion leaving2881.

Reviewer environment: Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. This is isolated namespace scaffolding
with fetched C236/C237 helper excerpts, not a full repository checkout. The new source/test files
are complete and hash-matched; the parent excerpt scaffolding is reviewer-only and not committed.
The full historical suite was NOT constructed or run here. Windows PowerShell AST, accepted
user-local artifact precheck and the actual six FOLD/GRU scientific models were NOT executed here.
Those checks are not represented as PASS. They remain mandatory in the authoritative runner.

Launcher/runner inspection confirms branch/tree/HEAD/ACTIVE guards before logging/publication,
PowerShell ParseFile before each selected invocation, fixed parent paths and C238-only publication.
Only this unpinned handoff activation/review record changes after the review HEAD. Re-read final
handoff and verify final branch HEAD before returning the execution ExpectedHead.

## Stop and scope

Gate F NOT PASSED; numeric-memory tuning paused. Preserve accepted sources/tests/logs and
 tools/run_c167.ps1. No history rewrite, cleanup, paid API, external corpus or larger model.
24 own tests ->2881 focused tests ->C238 probe ->artifact postcheck ->remote log publication.
Stop same C238 on an integrity fault; repair transport-only failure without retraining.
Judge C238 before C239 registration.
