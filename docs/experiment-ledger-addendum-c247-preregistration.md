# C247 preregistration — normal-exposure-matched control

Experiment:C247-v5b-normal-exposure-control.
Stage:V5-B-NORMAL-EXPOSURE-CONTROL.
C246 ACCEPTED VALID NEGATIVE; C248 NOT REGISTERED. Gate E PASSED; Gate F NOT PASSED.
This document registers a new control. The authoritative handoff activates it after committed-byte
post-authoring review. It does not revise any preceding generalization criterion or verdict.

## One scientific question

Is C246's ordinary-example exposure sufficient for the original TRAIN criteria without its
interleaved masked updates? Primary endpoint is TRAIN fitting at matched NORMAL exposure.
The normal HOLDOUT endpoint is reported as secondary, not used to relabel a control PASS as
successful generalization. No assumed outcome, extra-budget rescue or rerun of C246 is authorized.

## Parent identities and writer semantics

Acceptance/base commit:8559c95ec1716cc507f77f3d9271e19dcbd8ca28.
Acceptance record:docs/experiment-ledger-addendum-c246-c247.md.
C246 scientific execution HEAD:c17195b7c0f80ae7dd60050e25dca6a3effc21fb.
Published log commit:30142c60dedf52537c9cef26b35ca2909446b5ee.
Publisher log SHA256:ceaec8ba66f2609acf18663c76b7925fb8053a91f8d199075b50d697ae566362.
Summary SHA256:9a462485dffc948674b7752012893a8175cdb5de251f179763ae03e26659623a.
Local summary:runs/c246-v5b-training-erasure-471de735eb204a129692672d2849c270/summary.json.
Require exact execution-valid FAIL and outcomes TRAIN_CRITERIA_MISS:10,RECOMBINATION_MISS:2.

Required artifact SHA256 values:
- measurements.json:81b6aaa5ae69be11e49bb0e64dff0763d8f12437393df18ff4c7ca346d8d908b
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
- trained-models.pt:8282b378bea2c6ff166fb18ed9345bfee71ab5ac2080204a43251229f8b6fd34
- training-plan.json:761b00863243d9118cd85058f585b7e3592404c677b8d8f548be45ed2fd05db8
- validation-summary.json:68ccff53230dc8ab8fcf24d542547ade89f63335c4fd508db401ff0e68b80cf3

Read C246's exact summary through C246.validate_result. Reproduce the parent measurement summary
with C246.summarize(records,C244,C242), not a guessed one-argument signature. Its writer stored
initial_sha256 before training, final_sha256 after training, final/predictions on original inputs,
and unchanged C244.final as c244_comparator. C247 must retain these distinct meanings.

The child loader reads the C246 split and measurements directly, verifies the fixed partition,
all identities, valid distinct initial/final fingerprints, comparator metric schema and discrete
parent metrics through C243.discrete_metrics. C246 parent records remain in their original schema;
C247's different200-update records are never fed into a400-update parent summarizer.
C247 context roles:C246 parent,C244 base,C242 fitting,C234 binding,C231 factory,accepted audit helper.
No parent checkpoint is deserialized or evaluated; its bytes remain integrity-protected.

## Matched normal sequence and changed budget

Keep C244/C246 TRAIN64/HOLDOUT32, row order, bytes, targets, provenance and original three scoring
views. Every model starts fresh using seeds234001/234002/234003, in seed/full then seed/gru_only
order. Require exact C246 initial fingerprints, which were matched to C244 before-training states.
Construct the common-backbone GRU-only copy before either paired member trains.
Full13488/GRU-only10160 parameters,width16,48 slots,unrestricted256-byte argmax unchanged.

C247 alternates old32 and added32 normal batches for200 updates,100 per block. Each TRAIN row
receives100 ordinary presentations, matching C246's normal subset. Zero-based child step j maps
to C246 step 4*(j//2)+2+j%2. Audit all200 indices and original selected views to confirm they are
normal and identical. No selectively erased TRAIN tokens are constructed by this scientific path.
No removed update is replaced by zero loss, a dummy forward or an optimizer-only step.

AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,CPU float64,threads2,
deterministic algorithms fixed. Fit executable AST equals C244.fit except progress label.
STEPS is intentionally200, while C244/C246 STEPS must remain400; all other training constants match.
Actual optimizer forward tokens are independently checked against the C244 normal row schedule.

This matches normal-example exposure, not total optimizer updates. Removing masked updates alters
Adam moments and step counters as well as mixed-task gradients. The control cannot isolate a
unique mechanism. Its role is to check whether normal-budget reduction alone is sufficient to
explain a corresponding loss of TRAIN fit. It neither extends nor rescues accepted experiments.

## Primary TRAIN gate, secondary HOLDOUT and comparison

Use actual C242.evaluate,validate_metrics,cell_pass and C234 rendering/metrics. Initial evaluation
is TRAIN only. Original HOLDOUT reaches a model only after200 updates and checkpoint replay.
No evaluation drives early stopping, hyperparameters, seed replacement, best checkpoint or more work.

Primary:every Full seed/language TRAIN cell must satisfy original criteria:
normal accuracy>=0.90;fact/query/order paired both-correct>=0.80;both mask drops>=0.35.
TRAIN has32 rows/language and16 pairs/type, requiring at least29/32 answers and13/16 pairs.
GRU-only TRAIN gate is independent. status PASS iff full_train_control_gate is True.
A valid primary miss is ACCEPTED VALID NEGATIVE for this limited TRAIN-sufficiency control.
A primary PASS is not a diagnostic-execution-only PASS, but its scientific claim is TRAIN fitting only.

Also score HOLDOUT16 rows/language and8 pairs/type under the same thresholds. Report secondary
joint TRAIN+HOLDOUT family gates separately. They do not determine the primary verdict and cannot
promote Gate F. Never imply that primary PASS establishes unseen-pair success.

Store C246.final as c246_comparator and its c244_comparator unchanged. Both refer to exactly the
same rows; they are reused accepted evidence, not newly repeated baselines. For each seed/family/
language report current TRAIN/HOLDOUT, prior accuracies and deltas. Comparison labels use full
TRAIN criteria:BOTH_TRAIN_PASS,CONTROL_TRAIN_PASS_ONLY,C246_TRAIN_PASS_ONLY,NEITHER_TRAIN_PASS.
A control-only pass excludes reduced normal count alone as the explanation for that matched miss.
A control miss is compatible with an insufficient normal budget but does not exclude other effects.
No statistical independence, significance, core superiority or internal-cause claim is made.

## Workload, integrity, artifacts and protection

6x200=1200 updates/38400 normal training presentations,zero masked updates.
Per model:initial TRAIN3 forwards/192 rows;final TRAIN3+HOLDOUT3/288 rows;replay both/288 rows.
Totals90 evaluation forwards/4608 scoring rows;1290 full-model forwards/43008 total rows.
Before replay209 calls/6880 rows per model;after215/7168. One six-state checkpoint bundle.
No parent model forward, external data or scientific network call. Fixture tests are separate work.

Reuse C244.replay_one with C242 fitting; its6-forward/288-row replay contract does not require400
training steps. Require final fingerprints, exact argmax replay and raw-logit/metric error<=1e-9.
Use a child summarizer requiring block_updates=[100,100], not C244's200/200 requirement.
Require changed weights, no evaluation mutation, actual update/forward/row counts and all file pins.
Any source/artifact/schema/nonfinite/initialization/replay/test/count fault is INVALID / RETRY SAME C247.

Inherit C246322 source pins/502 inputs,add its summary+five artifacts and OWN6:328 pins/514 inputs.
Direct dependency union23:five C231 LM_SOURCES plus C230 through C247 helper/entry modules.
No accepted source/test/log or shared launcher is modified. Own tests reuse C246's already-pinned
synthetic helper classes; those test helpers are never invoked by the scientific run.

Own tests24;modules132;loaded3098/focused3097. Only the inherited exact exclusion remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Construct actual runtime suites/unique IDs; a synthetic filter test is not a historical test pass.
OWN6:the C247 benchmark,test,runner,launcher,this document and docs/v5b-normal-exposure-control-v0.1.md.
Ignored outputs:control-plan.json,split-dataset.json,trained-models.pt,measurements.json,validation-summary.json.
Bundle schema:fold-c247-normal-exposure-v1;six ordered states. Summary includes primary TRAIN gates,
secondary joint gates,12 comparison cells,count fields and integrity flags. Postcheck verifies
plan/partition,hashes/sizes,summary,initial/comparator identities and child discrete replay.
Manifest SHA256:f9558bfead121a605f8cc2dd776eed5db6db981c1c20b675d44d49d4b95a502c.

## Review and stop

Re-fetch all six committed files after authoring. Match the four complete code/script blob IDs
to locally tested bytes,compile/import,run24 own tests,inspect free names,parent writer/summary/
replay signatures,normal subsequence,workload,gate scope,CLI argv and parser/publication ordering.
Record review HEAD, actual checks and pending checks in handoff. Parent excerpts/scaffolding and
synthetic models are not a full-checkout or actual-checkpoint scientific run.

Dispatcher/launcher/runner ParseFile precedes Python/source/parent/control precheck,then24 own tests,
3097 focused tests,C247 training,postcheck and remote log publication. Operational branch/tree/HEAD/
ACTIVE mismatch skips before execution and publication. Repair transport-only failure without
retraining. No threshold rescue,inference masking,larger model,paid API,external corpus,cleanup,
history rewrite or production change. Numeric-memory tuning paused. Judge C247 before C248.
