# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C235 ACCEPTED PASS (diagnostic integrity only). C236 ACTIVE / NOT YET JUDGED. C237 NOT REGISTERED.**
C236 is the unique ACTIVE experiment. C234 remains ACCEPTED VALID NEGATIVE.
C235 did not establish binding capability; C236 is a minimal seen-TRAIN fit probe, not a Gate F run.
Post-authoring review is PASS. The authoritative runtime prechecks and regression remain mandatory.

## Latest accepted evidence — C235

Scientific execution HEAD: `fc3311955c3dcda87b67c2ee8dd58a59fb256d6f`.
Published log commit: `71dd1bb48978a1bd0a6b71448f1ceb29011696c4`.
Log SHA256: `fb2811d896606c07bd3d6cbd28a036d30f905dfce0295ade1fde582cde14b40a`.
Summary SHA256: `a9d6daa76bab38488ec3634d186ba81a2d61ae878df80202f3084057e917b1b5`.
Local summary: `runs/c235-v5b-frozen-binding-diagnostic-17d75b38b35249a297bde78cee0f1d43/summary.json`.

24 own tests PASS in0.334s;2809 focused tests PASS in65.332s.
36 forwards /10368 row presentations /zero new training.
All parent EVAL replays and frozen-weight fingerprints pass;256 source pins/370 inputs preserved.
Tracked tree clean, execution HEAD preserved, run_execution_valid=True.
All12 cells: TRAIN_ACCURACY_BELOW_90. TRAIN accuracy47.9167%-53.125%.
TRAIN supplied-value rate100%; query-change same-answer rate78.125%-94.7917%.
Failure is already on TRAIN, not only held-out EVAL. No internal causal mechanism is established.

Acceptance: `docs/experiment-ledger-addendum-c235-c236.md`.
Acceptance record commit: `dc0b43a197bfa9061bd2454099e41111cc4dd17c`.
Acceptance/handoff base before next registration: `4e7c83ae5948ac1ee403b61f018b334f170f32c4`.
The first invalid attempt remains at log commit1615b5ce54afed8bde44ac9d326cace6c6e674d0 and in
`docs/experiment-ledger-addendum-c235-execution-recovery.md`; it is not erased by the valid retry.

## Preserved C234 evidence

C234 ACCEPTED VALID NEGATIVE; full_binding_gate=False and gru_binding_gate=False.
Scientific execution HEAD: `c225c2d82636085e2d639878738e1b9a7aa37b42`.
Published log commit: `930fa77881d60558b3199b980f139ddef8bcb6ee`.
Summary SHA256: `a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`.
Local summary: `runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/summary.json`.
Full EVAL19/96-25/96 correct; GRU-only30/96-39/96. Binding not demonstrated under the fixed recipe.
Full details/artifact identities: `docs/experiment-ledger-addendum-c234-c235.md`.
C233 remains ACCEPTED VALID NEGATIVE; C232 remains bounded template-byte learning only.

## Active C236 — minimal binding learnability

Experiment: C236-v5b-minimal-binding-learnability.
Stage: V5-B-MINIMAL-BINDING-LEARNABILITY.

One question: can the unchanged C234 model/training recipe fit a balanced minimal16-row TRAIN
binding set before model capacity or training-step budget is increased?

Changed: training cohort384 ->16 existing C234 TRAIN rows, selected by objects [0,1] and sorted
values [0,1], preserving original order. Both assignments, fact orders, queries and languages remain.
The measurement endpoint is those16 seen TRAIN rows, not C234's held-out EVAL endpoint.

Fixed: same Full13488/GRU-only10160 parameters, width16,48 slots, renderer, raw256-byte answer
scoring, normal/evidence-blind/query-blind views, answer-only loss and optimizer recipe.
Seeds234001/234002/234003; fresh models with initial fingerprints matched to C234 before-training
records. No continuation from accepted trained checkpoints. Copy the common GRU backbone before
either paired model trains.400 steps/model, batch32, AdamW lr0.005, clip1.0, betas(0.9,0.999),
eps1e-8, weight_decay0, sampler seed+1000, CPU float64, threads2, deterministic algorithms.
Executable training AST must match C234.fit except the progress tag; constants must match too.

Fixed scientific workload:
-six new models x400 =2400 training steps;
-76800 answer presentations;
-54 initial/final/checkpoint-replay evaluation forwards on16 rows;
-2454 total model forwards and77664 total row presentations;
-one checkpoint bundle write containing six states;
-zero held-out evaluation rows or network calls.

Fixed primary gate: every Full seed/language cell reaches exact accuracy>=0.90, fact/query paired
both-correct>=0.80 and evidence/query mask drops>=0.35. With8 rows and4 pairs per language,
exact and paired thresholds require8/8 and4/4. GRU-only gate is independent, not a superiority gate.
A valid primary miss is ACCEPTED VALID NEGATIVE. An integrity fault is INVALID / RETRY SAME C236.
A PASS only supports fitting this minimal seen-TRAIN set; memorization is not ruled out.
No C234 rescue, held-out-generalization claim, general-language claim or Gate F promotion.
Cohort restriction also changes repetition per row and lexical breadth; their causes are not isolated.

Protection:262 source pins /382 protected inputs; direct dependency union12; OWN6.
Own tests24; modules121; loaded2834/focused2833 with the inherited exact exclusion only:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five outputs: probe-plan.json, probe-dataset.json, trained-models.pt, measurements.json,
validation-summary.json, all under ignored runs/.
Manifest SHA256: `86f534a54964a31d0139d5a3ceb3ef4b5e3c2ab46667adb002390a5b5d347957`.
Probe SHA256: `bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c`.

Design: `docs/v5b-minimal-binding-learnability-v0.1.md`.
Registration: `docs/experiment-ledger-addendum-c236-preregistration.md`.
Preregistration commit: `28b341c09143588bfaf23c7adcacd1f1c84afb10`.
Use tools/invoke_active.ps1 with the final handoff branch HEAD returned with the execution command.
Do not use the C235 execution HEAD or assume the review HEAD includes this activation.

## C236 post-authoring review

`post_authoring_review = PASS`

Review HEAD: `28b341c09143588bfaf23c7adcacd1f1c84afb10`.
Scope: new-experiment authoring review, not a formal C236 result.

All six OWN files were re-fetched from the committed remote review HEAD after authoring finished.
Reviewed Git blobs:
-benchmark: `d77ba8570cc1eb5351d271be3a906fb24dcf7388`
-tests: `e808560446c02acddf307e4ad7723e7a50bacd41`
-runner: `4c23a1f2721fcaeb5749baae7415998c7e81a3a3`
-launcher: `9ddb7a11ae923d6701f8ff2144019eeb737899b8`
-preregistration: `19b7f5fcfe5def5c866dfa98fcb68d82e3714967`
-design: `f78593420dfec20bdf7a7402eb346a7c2949a5a1`.

Compare from acceptance base4e7c83ae to review HEAD: exactly the six OWN additions, no accepted
parent source/test/log change. The four code/script blob identities match the locally tested bytes.
Parent C234 writer source was re-read: initial_sha256 is recorded before training; baseline common
copy precedes both fits; its dataset and measurement contracts match the C236 loaders.

Checks actually executed in the isolated reviewer environment:
-Python compile/import of complete new benchmark and test modules; UTF-8/NUL checks;
-all24 new own tests PASS before publication and again after remote readback (1.210s on final run);
-actual own unittest loader constructs24 tests;
-hash-matched independent reconstruction of the accepted full C234 dataset and selected16 rows;
-manifest digest matches the registered SHA256;
-exact C234.fit function source fetched from remote and compared mechanically through
 C236.audit_fit_contract; executable AST and constants match except the progress label;
-two-step C234/C236 fit parity on identically initialized toy models yields identical fingerprints;
-real C236 train_one/replay_one helpers exercised using a toy model and instrumented evaluator,
 verifying actual forward counts, mutation guards and replay rejection; not the scientific Full/GRU run;
-three embedded Python blocks compile; precheck argv1/2 and postcheck argv1/2/3/4 ordering checked;
-source AST verifies parent loader, common-copy-before-training and save/load/replay ordering;
-Python free-global/import binding audit found zero unresolved names in the new benchmark/tests.

The runner/launcher review also verifies parser-before-publication and branch/tree/HEAD/ACTIVE
preflight boundaries. Historical module append contracts and accepted counts were inspected:
C235120 modules/2810 loaded plus the new module24 tests gives121/2834, excluding the same one
historical dynamic-state test gives2833. The full historical suite was NOT constructed or run here.

Reviewer environment: Python3.13.5 / PyTorch2.10.0+cpu / NumPy2.3.5, with isolated package scaffolding
for the new modules, not a full checkout. github.com DNS resolution prevented a complete clone.
NOT executed here: Windows PowerShell AST, full2833-test regression, accepted user-local artifact
precheck or the six-model scientific C236 probe. These are not represented as PASS. They remain
mandatory in the authoritative launcher/runner before a valid result can be accepted.

Only this unpinned handoff activation/review record changes after review HEAD. Re-read the final
handoff and verify the final branch HEAD before returning ExpectedHead to the user.

## Numeric-memory track and stop

C230 prepared route remains optional; numeric-memory tuning stays paused. Gate F is not waived.
Preserve all accepted sources/tests/logs and tools/run_c167.ps1.
No cleanup/history rewrite, paid API, external corpus, larger model or production runtime change.
24 own tests ->2833 focused tests ->C236 probe ->artifact postcheck ->remote log publication.
Stop same C236 on execution/integrity faults. Do not rerun a completed probe for log transport alone.
Judge C236 before registering C237.
