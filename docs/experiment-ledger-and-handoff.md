# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository: akakishi04/fold; branch: feat/sft-target-loss; local: M:\asobiba\fold.
Authoritative runtime: Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry: explicit PowerShell7, dispatcher ParseFile, tools/invoke_active_v2.ps1.
Accepted scientific sources/tests/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C324 ACCEPTED VALID NEGATIVE. C325 ACTIVE / NOT YET JUDGED. C326 NOT REGISTERED.**
C323 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C321 remains VALID NEGATIVE.
All earlier verdicts are unchanged. Do not rerun accepted C324 or its recovery routes.
C324 R6 scientific FAIL is a valid negative, not an operational failure.
Only the new C325 route below is authorized; its scientific result is not yet known.

## Latest accepted evidence -- C324 R6

Acceptance: docs/experiment-ledger-addendum-c324-c325.md.
Acceptance report commit: f0e301ac3fc40c437ba890a2683a5d3889320b01.
Acceptance handoff commit: 6c3198793f0f6b852fa96be125323763cbfdddde.
Scientific execution HEAD: fcef3d5833c31d51e261ce578209bd5acd73f59c.
Published log commit: c67be12c1a08dda49f218699ecb8896ef1cf2061.
Publication parent equals execution HEAD; only console transport advanced the ref.
Uploaded log2615255bytes; SHA256
 aa179e9f8a4d0b19bf0c5e55226731162e23cab63d2110158f8119c8742d4149.
Whole uploaded bytes matched metadata. Complete LF normalization matched the
published Git blob e992984130d23dfd3c393368d268ed8f93499d11.

Local parent folder: runs/c324-scientific-r6-6b241e7f98c94ee3846a852f39456a7f/.
Primary science/summary.json SHA256:
21e752a51809a9b400c798b24c4ff405105458965b54610cfa16f71a349fbbdd.
Mandatory execution-envelope.json SHA256:
2c6013d9b4f33fb20e79e68946ad8596d756d23694d7d04508fcd0ca0e3040c3.
The primary792source/1491input summary and mandatory802source/1501input envelope
were both verified by R6. Do not consume the primary alone or drop supplemental pins.

Full5490 tests/213modules PASS; no failure/error/skip; regression922.503s.
Seven C316..C322 verifier bodies completed once each, nine exact session reuses.
All ten models completed1200updates; ten checkpoint replays PASS; saved semantic
reconstruction and final1501uncached rereads completed. Fresh envelope verification
confirmed802sources/1501inputs/full5490. All three subprocess exits0;
run_execution_valid=true; scientific_status=FAIL; candidate_gate=false.
Independent review checked the whole console,5490distinct IDs,ten measurement records,
4320local gates and2160fact-order gates. It did not independently rerun raw checkpoints.

C324 deciding values: interior HOLDOUT answers716/1440 ->1396/1440;
both-query-correct22/720 ->685/720. Every seed improved in those pooled counts.
Candidate interior gate3/5, original2..6 retention0/5, composite0/5;
control interior0/5, retention2/5. Original2..6 gate counts control5/5/5/5/2,
candidate5/4/1/0/0. Explicit interior coverage helped binding but did not preserve the
original task range under replacement. No structural-impossibility, sequential
forgetting, unseen-template, Gate F, general LLM or MinePilot-readiness claim.
The old47ccd303f4382b7938db639e86aeb151e1f83af1 attempt remains INVALID;
its native crash cause remains unknown. No controlled runtime speedup is claimed.

## C325 registration and completed post-authoring review

Experiment: C325-v5b-mixed-name-coverage.
Stage: V5-B-MIXED-NAME-COVERAGE.
Contract: docs/experiment-ledger-addendum-c325-preregistration.md.
Review: docs/c325-post-authoring-review.md.
Source/preregistration/review target HEAD:
b5521f0db9e6b08789cc4567c35cc6a22d74dd2d.
post_authoring_review = PASS.
Use the final documentation/activation HEAD supplied in the user command, not the
source-only target. This authoring PASS is NOT a C325 scientific or full-regression PASS.

After committing all six own files, their complete remote contents were reread and
Git blobs matched independently hashed local bytes. Own56tests PASS2.272s;
CP932-default-file-encoding emulation56PASS2.525s; no failures/errors/skips.
All new Python compile/import/UTF8/noNUL checks pass; undefined globals0.
Author LinuxPython3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Fixtures include real Git/files/
subprocesses/Torch arithmetic and production stage ordering, not native Windows/full5546.
No author-side PowerShell AST execution is claimed. The mandatory dispatcher ->
launcher ->runner AST chain is retained before user-side native execution.

## C325 one question and fixed intervention

At equal architecture and total budget, can retaining half of original length-four
TRAIN exposure recover original-task retention while preserving interior binding,
relative to interior-only length-four training?

Control interior4 versus candidate mixed4; BOTH native mean_last.
Fresh seeds325001..325005, order seeds325101..325105; ten models from paired identical
initial states. No accepted C324 checkpoint is used for fitting.
Length4 has100whole epochs. Control uses100interior; candidate alternates original
then interior for50epochs each. Every192-row epoch has4updates of48rows, preserving
query pairs. Each TRAIN row receives50original4+50interior4 candidate exposures.
Length2/3 remain original with100exposures/row each. Logical order, profile schedule,
queries, values, targets, optimizer, capacity and total updates stay paired.
No post-result mixture tuning or seed selection. Both template families are seen.

14256parameters/core3328,64slots,CPUfloat64,2threads,4internalsteps.
1200updates/model,48rows/update,ordinary mean CE,fit RNG612000.
AdamW betas.9/.999,eps1e-8,weight_decay0;globalgradientclip1;
otherLR.005/coreLR.0005. Scientific work12000updates,576000training rows,
15420model forwards,904320row presentations,61680core forwards,10checkpoint replays.
Preflight,software tests,parent and saved semantic verification are separately scoped.

ALL5 candidate states must pass complete interior and original2..6 gates;
within every paired seed original2..6 pooled HOLDOUT answer AND query-pair gains
must be positive, and interior HOLDOUT answer AND query-pair gains nonnegative.
Original scorer thresholds.90/.80/.35/.35/.80 unchanged at every local/masked/order
condition. Report full cells and rescues/regressions; pooled means cannot hide failures.
Original length1 descriptive only. No unseen-template/statistical-independence or
Gate F/general-language claim follows from a future C325 PASS.

Manifest SHA256:
03ed2ba1d2d2951087c70ce41ddf39756674a30ac4cef56671e158eb80fff3d0.

## C325 execution, inheritance and outputs

Route: invoke_active_v2 ->invoke_c325.ps1 ->run_c325.ps1 ->c325_execution.py
controller ->scientific worker ->separate ordinary regression ->fit/evaluate/replay
->saved semantic reconstruction ->final input rereads ->fresh envelope verifier
->standard C325 console publication. execution_role=C325-MIXED-NAME-COVERAGE.

Validate exact accepted C324 summary+R6envelope and all802source/1501input evidence.
Read-locked parent checkpoints/evaluations are reanalyzed by unchanged C324.analyze.
No parent fitting or forward is performed. Older C316..C322 semantic verifier bodies
are NOT recursively executed again: inherit their accepted identity with complete
byte checks. This explicit C325 contract scope must not be described as fresh
ancestor semantic execution. No accepted verifier/module global is patched.

C325 protects808sources=802inherited+6own;
1517inputs=1501inherited+10immediate-parent files+6own.
All direct/lazy scientific dependencies and supplemental tests are covered.
Native R4 Windows read leases are held through all worker phases; no unlocked or
cross-run cache. All1517 inputs receive final uncached rereads. Primary result and
execution envelope both carry the full union. A fresh verifier checks every input,
source blob, output byte/size, complete regression receipt, manifest and gate binding.

Native TRAIN/readout/gradient preflight precedes FULL5546tests/214modules:
5490inherited+56new;5547before the sole inherited C204 exclusion. No new exclusion,
skip or cached test result. Run the entire suite in an unmodified separate process.
Only after all5546pass, run all ten new models and all ten checkpoint replays.

Local-only: runs/c325-mixed-name-<id>/science/summary.json plus8registered outputs;
execution-envelope.json,regression-result.json,science.log,regression.log,verify.log.
Model/tensor/data artifacts stay out of Git. Only complete console text is published
to docs/experiment-run-logs/c325/latest.log and latest.json.
Console uses streamed test dots, ordered-test-ID SHA256, ten-second heartbeats and
compact per-domain minima/totals/counts. Complete individual-cell measurements remain
in hashed local artifacts. This reduces transport volume, not test/measurement scope.

## User execution and stopping rules

Expected: active_experiment=C325 ->accepted_C324_composite_snapshot
->native_TRAIN_and_gradient_preflight ->full_regression_unmodified_separate_process
->scientific_training_10_models ->saved_checkpoint_and_measurement_verification
->final_uncached_input_recheck ->execution_envelope_verified
->run_execution_valid=true ->console publication.

Wrong branch/dirty tree/stale HEAD/nonunique ACTIVE/missing dependency/AST failure
is an operational SKIPPED before logging/publication; do not rerun an old command.
Native fatal,source/input/test/schema/nonfinite/replay/envelope failure stops SAME C325.
Scientific FAIL alone is not execution failure and never authorizes automatic refit.
Publication-only failure is repaired without repeating science. No C326 activation.
No CI,package reinstall,cache deletion,paid service or old result mutation is added.

User may report only finished. Fetch remote latest metadata/log and distinguish the
scientific execution HEAD from its descendant log-publication commit. Do not ask for
old C324 attachments again. For an accepted C325, complete its acceptance and next-C
implementation/preregistration/remote review/launcher in the SAME response; do not
stop at a design direction or ask the user to say continue. For INVALID, repair C325.

## History and inherited compatibility seal

Pre-C325 accepted handoff: docs/handoff-history/c324-accepted-before-c325.md,
exact blob cff7b99a75b307c4a3527520c95b11cc7b544694.
C324 recovery history remains in its existing contracts/reviews and the accepted
report. C324 acceptance and C325 preregistration are separate commits.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
