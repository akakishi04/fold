# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and the Current response format (v2) in
`docs/experiment-conversation-handoff-protocol.md`.
Repository: akakishi04/fold. Branch: feat/sft-target-loss. Local: M:\asobiba\fold.
Authoritative runtime: Python 3.13.15 / PyTorch 2.10.0+cu130 / NumPy 2.3.5.
Entry: explicit PowerShell 7, dispatcher ParseFile, tools/invoke_active_v2.ps1.
Accepted sources, tests, logs, contracts and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C327 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C328 ACTIVE / NOT YET JUDGED. C329 NOT REGISTERED.**
C326 remains ACCEPTED VALID NEGATIVE. All earlier verdicts are unchanged.
Do not rerun C327 or earlier accepted experiments. C328 is a new fitting comparison.
C328 authoring approval is not a scientific verdict or native full-regression PASS.

## Latest accepted evidence -- C327

Acceptance commit: d96e7ff66f76463e6fe39ca159e687f7d26d2011.
Report: docs/experiment-ledger-addendum-c327-c328.md.
Scientific execution: 847c924f50303d93ed4df7acec74b77209b7d261.
Published log commit: 926113e7602f1ee36445cde9bbf90eab1539ace1.
The publication parent equals the scientific execution HEAD.
Published metadata: 35743 Windows bytes; log SHA256:
cbff015cbec04a51270a9b3410ede85391879e2bdbc2dc4ea34db2b203595cb5.
Git log blob: 54c0f9301e34cb12e87c89e7551e0c83394a0298.

The reviewer read native preflight, full-regression completion, all40 alignment
aggregates, all10 model completions and terminal verification, then independently
summed counts. No independent whole-log rehash, local gradient recomputation or
checkpoint replay is claimed. Older C323/C324 attachments are not C327 evidence.

All5658 tests across216 modules passed, with zero failures/errors/skips; 864.515s.
Ordered suite-ID digest:
47c7f39d55ebfe22be9a4e65d33bb1b1b56bba1087700e2ba0953330d53cb7b1.
Native locks, parent semantics and gradient preflight passed with820 sources and1549
inputs. All10 fixed models completed60 gradient pairs:240 forwards/gradients,23040
rows and960 core forwards; zero updates, optimizer steps or new checkpoints.
Reverse repeats, unchanged weights, saved geometry reconstruction, all1549 final
uncached rereads and fresh-envelope verification passed. All process exits were0;
diagnostic_status=PASS and run_execution_valid=true.

Each of40 groups has6 defined cosines. The denominator is30 objective pairs per arm
or60 pooled. Negative-dot counts, epoch4/batch4: all7/11, core11/14, reader10/9,
other6/10. Joint strict descent counts: all25/25, core21/19, reader22/27, other26/26.
Pooled negative counts are18/25/19/16 and joint-descent counts50/40/49/52 of60 in
all/core/reader/other order. The all group overlaps its partitions; these are not240
independent tasks. Reader means read.* only. Negative dot alone does not rule out
common descent. These are terminal Euclidean first-order observations, not finite
AdamW behavior, optimizer moment history, full-trajectory causality or original6
measurements. No capability improvement, unseen-template, Gate F or production claim.

Parent folder: runs/c327-gradient-1cf048a0cd9449b6af6485a4802c46ca/.
Primary science/summary.json SHA256:
c4a061e158a1bd617fb7638bb034b7aa3ef78da06b15062474ff986d1f347719.
Mandatory execution-envelope.json SHA256:
fb44749ce38e0b0909238c51c13bbb1eb95e1898369313fb34d95483a543e535.
The four parent outputs are diagnostic-plan.json, gradients.pt, measurements.json
and validation-summary.json. With summary and envelope there are SIX parent files.

## C328 registration and completed post-authoring review

Experiment: C328-v5b-late-rate-decay. Stage: V5-B-LATE-RATE-DECAY.
Contract: docs/experiment-ledger-addendum-c328-preregistration.md.
Review: docs/c328-post-authoring-review.md.
Source/preregistration review target:
6296eae8209f674da2ae9cff4516857e010c1d59.
post_authoring_review = PASS.
Use the subsequent final activation HEAD supplied in the user command, not the
source-only review target or an old C327 execution/publication HEAD.

All six committed own files were reread completely; their Git blobs matched
independently hashed local bytes. After reread: normal64/64 PASS in3.711s and
CP932-default-text-open emulation64/64 PASS in3.642s, with no failures/errors/skips.
UTF-8, no-NUL, compilation and import checks passed; undefined globals were0.
Author environment: Linux Python3.13.5 / Torch2.10.0+cpu / NumPy2.3.5, two threads.
Real Git/files/subprocess/Torch arithmetic and the production1200-update toy loop
were tested. Its800-update boundary state/optimizer hashes and loss prefixes match;
moments survive the switch and final states differ. Actual worker control was tested
with explicitly synthetic parent/lease/model callbacks. This is NOT native Windows,
real-parent FOLD training or full5722 historical-regression success. No author-side
PowerShell AST execution is claimed; the mandatory user-side AST chain is retained.

## C328 one question and fixed intervention

At fixed1200 updates and the C326 batch4 curriculum, does reducing both group learning
rates by0.1 after800 completed updates improve interior binding while retaining
original2..6 performance, relative to constant rates? This is a prospective test,
not a causal conclusion from C327.

Fresh seeds:328001..328005. Order seeds:328101..328105. Arms:constant/late_tenth.
Ten new models are trained; no accepted checkpoint initializes fitting and C327
saved gradients are not training inputs. Both arms use native mean_last,14256
parameters including3328 core parameters,64 slots,CPU float64 and two threads.
Logical rows, targets, row order, profile sequence and C326 batch4 masks are paired.
Each TRAIN row receives original2/original3 each100 times and original4/interior4
each50 times. Data remains192 TRAIN/96 HOLDOUT rows. Each update contains24 intact
query pairs/48 rows; length4 updates contain11..13 original pairs, not exact12/12.
All five actual schedules validate in preflight. Outcomes never select the data.

The immutable C308 core_slow factory creates one AdamW optimizer per model.
Noncore LR=.005; core LR=.0005; betas=(.9,.999), eps=1e-8, weight_decay=0,
global clipping=1, ordinary mean CE, FIT_RNG=612000.
Updates1..800 use the original rates in both arms. For801..1200, constant stays
unchanged and late_tenth changes ONLY group LR to.005*.1 and.0005*.1.
No optimizer reset/recreation, moment scaling, gradient scaling/detach, default,
group membership or parent-global change is allowed. Every update validates the
optimizer identity, non-LR settings and exact registered rates.
Before update801, paired full-state/optimizer hashes and first800 losses must match.
Moment/state hashes must also match before and after LR assignment. All traces and
receipts are saved. This records boundary hashes and loss prefixes, not every
intermediate weight tensor. Prefix mismatch is INVALID, not a scientific negative.

Scientific work:10 models,12000 updates,576000 training-row presentations,15420 model
forwards,904320 total row presentations,61680 core forwards,10 state reloads,
one replay-bundle read and one new model-bundle write. Hashing and scheduling add
real overhead. Separate native preflight uses one discarded fresh probe with6
forwards/2 backward evaluations,12 rows and0 optimizer steps, plus all five schedules.
Software tests and parent/saved verification are separately scoped.

ALL FIVE candidates must pass complete interior AND original2..6 gates. Per seed,
interior HOLDOUT answer AND both-query-pair gains must be strictly positive, while
pooled original2..6 gains in both counts must be nonnegative. Existing local/masked/
order thresholds.90/.80/.35/.35/.80 stay unchanged; length1 is descriptive.
Report complete cells, seed flags, per-length contrasts and rescues/regressions.
No pooled override, seed selection, threshold relaxation or rate/budget/switch search.
Seen template families and reused logical splits are not independent new tasks or
unseen-template generalization, general LLM capability, Gate F or production adoption.
Manifest SHA256:
75f3de53837dcc64127b72f541ded650436b3a6ac46686bd9d8ff2aa8b89a226.

## C328 parent semantics, protection and execution

The immediate parent is the C327 diagnostic. Validate exact primary/envelope hashes,
PASS/capability-false flags, manifest/work, full5658 receipt, semantic completion,
final1549 rereads and identical820-source/1549-input unions. Verify every inherited
source Git blob and input byte. Add C327's four outputs plus summary/envelope.
Use the immutable C327 executor's fixed C326 folder/hash for canonical TRAIN data
and saved logits; require those files already in inherited input protection and
validate canonical data/prompts. Unchanged C327.semantic_recheck reconstructs its
gradient archive under no_neural. No parent forward or recursive older semantic
body runs, but all older bytes remain checked.

Protection:826 sources=820 inherited+6 own;1561 inputs=1549 inherited+6 diagnostic
parent files+6 own. The benchmark, executor, tests, runner, launcher and contract,
all direct/lazy ancestors, C308 optimizer and recovery helpers/tests are covered.
No smaller-map fallback. Unchanged R4 native Windows read leases stay held through
the worker, with independent first-read reference hashes and all1561 final uncached
rereads. No unlocked fallback, cross-run cache, source mutation or artifact deletion.

Route: invoke_active_v2 -> invoke_c328.ps1 -> run_c328.ps1 -> c328_execution.py
controller -> worker -> C327/C326 persisted checks -> native preflight -> ordinary
full regression ->10 fits/evaluations and paired800-boundary checks ->10 checkpoint
replays -> saved reconstruction ->1561 final rereads -> primary/envelope -> fresh
byte verifier -> standard console publication.
The complete suite is5722 tests/217 modules:5658 inherited+64 own,5723 before the
sole inherited C204 exclusion. No new exclusions/skips/cached test results.
Actual distinct IDs/counts are checked and their ordered digest printed. Regression
runs in a separate ordinary interpreter. Only all5722 success permits fitting.

Eight local outputs:experiment-plan.json,dataset.json,original-prompts.json,
interior-prompts.json,trained-models.pt,evaluations.pt,measurements.json,
validation-summary.json. Hash/size-bind them before and after saved reconstruction,
then recheck before writing the summary/envelope. Saved reconstruction checks actual
traces, masks, boundary hashes, checkpoint digests and metrics, not a1200-update
history rerun. The fresh process checks exact unions, every source/input/output
byte/size, manifest, cohort, full test receipt and fixed-gate/count bindings.
Both primary and companion envelope carry complete826/1561 protection maps.

Outputs stay local under runs/c328-late-rate-<id>/science/, together with enclosing
execution-envelope.json,regression-result.json and science/regression/verify logs.
Only console text goes to docs/experiment-run-logs/c328/latest.log and latest.json.
Keep test dots, ordered digest,10-second heartbeats,200-update CE/LR progress,
seed/pair results and compact domain statistics. Full cell metrics remain saved.

## Expected progress and stopping

active_experiment=C328 -> accepted_C327_composite_snapshot
-> native_TRAIN_and_schedule_preflight -> full_regression_unmodified_separate_process
-> scientific_training_10_models -> first800_weights_optimizer=IDENTICAL
-> saved_training_reconstruction -> final_uncached_input_recheck
-> persisted_training_evaluation=PASS -> execution_envelope_verified
-> run_execution_valid=true -> console publication.
Scientific PASS/FAIL is separate from execution validity. LR changes after update800.

Stale host/branch/HEAD, dirty tracked tree, nonunique ACTIVE, dependency or AST failure
is SKIPPED before scientific logging/publication. Source/input/schedule/800-prefix/
optimizer/test/nonfinite/replay/semantic/envelope failure stops SAME C328; preserve
evidence and do not retry automatically. A finite scientific FAIL with valid
execution is negative evidence. Repair publication alone without refitting.
No C329, CI, paid service, package installation, cache deletion or old-result edits.

The user may report only finished. Fetch remote latest metadata/log and separate the
scientific execution HEAD from its descendant publication commit. Do not ask for old
C323/C324/C326/C327 attachments. For a valid C328, complete acceptance AND next-C
design, implementation, preregistration, committed-byte review, activation and launcher
in the SAME response. For INVALID, repair the same C328. Do not advance this branch
for unrelated work while the user is running an ACTIVE experiment.

## History and inherited compatibility seal

Pre-acceptance C327 handoff: docs/handoff-history/c327-pre-acceptance.md.
C327 acceptance and C328 registration are distinct commits. All older accepted and
invalid recovery evidence remains in existing documents/commits; no verdict erased.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
