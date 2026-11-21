# C251 preregistration — pre-core memory, post-core query

Experiment:C251-v5b-precore-memory-postcore-query.
Stage:V5-B-PRECORE-MEMORY-POSTCORE-QUERY.
C250 ACCEPTED VALID NEGATIVE;C252 NOT REGISTERED. Gate E PASSED;Gate F NOT PASSED.
This registers a new adaptive matched comparison. Readback review and authoritative activation
are required before scientific execution. It neither replaces failed seeds nor revises C250.

## One question and identity

Does using the pre-core causal encoder as Full's read-memory source, while retaining its post-core
query/residual, improve the same five seed blocks versus accepted C250 Full/token_read?
Acceptance/base commit:bafec255be01fce2fea9b34c0e50410ecd724240.
Acceptance record:docs/experiment-ledger-addendum-c250-c251.md.
C250 execution HEAD:7a9d48a99c1ca67c9eb05d0f68e7b4fa1284c881.
Published log commit:fc7d48e36e81d7b9fc8188f656771c757c398894.
Publisher log SHA256:45c93f81d69889217e60206cbd035a977ca1b2d1852c5ec464603cc3085d3098.
Summary SHA256:c965176039448ac99e812ad4abfce78950aafc271c65d4676bd47fe7aa59dc07.
Local summary:runs/c250-v5b-fresh-seed-replication-9bf33a726c614e558f446871954550d7/summary.json.
Require exact valid FAIL;seed_pass_counts token_read full2/gru_only4,eos_adapter both0.

Six protected C250 artifacts:
- initial-references.json:bef206a363baa98e58a6e16d1cb98474e7ff30986a478fca18007333234042a0
- measurements.json:ece4a95c50359349bcd7a60ad7059a8613e7d1db1cbe64ad4449340c3a396e0f
- replication-plan.json:4f2bffab4fff98193a2756fe65d0403d955711f23b18e548698f45d7f93c9cee
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
- trained-models.pt:a37074f9ab1696622b3de4e16aeb69166659f7e27734bb770b814a5466622f31
- validation-summary.json:78acad4d8776fc5caf2dcc379ace4bd2dfcf748a84ae18d214949cae014842bb

## Parent contract and comparator

C251.load_inputs reads C250's own split,initial-references and measurements, not C250.load_inputs
(which expects C248). Validate the actual C250 summary and reproduce it with
C250.summarize(records,refs,C242). Recompute discrete final metrics for all20 parent records from
all original prediction views using C243.discrete_metrics before selecting the five comparators.

C250 initial-references.initial_sha256 is the bare backbone BEFORE learning. Its measurements
backbone_initial_sha256 refers to that reference. Measurements.initial_sha256 is the full initial
wrapper/head, while final_sha256 and final/predictions refer to AFTER400 updates. C251 must match
both initial identities, reuse reference.initial_train for zero-output replay, and never load the
trained parent checkpoint. Preserve comparator.final byte-for-byte in child c250_comparator.

Select all Full/token_read seeds250001,250002,250003,250004,250005 in order. No seed/language
selection,extra seed,rerun of a valid result,checkpoint choice or larger budget. Parent references
and final comparators are reused evidence,not new inference or an independent baseline repetition.

## Changed source and retained backbone path

Use new experiment-only PrecoreReadout around the unmodified Full backbone. Reuse C248.ResidualHead
with arm token_read,head seed+248000 and zero output projection. State-dict keys/initial values
must be identical to C250's Full reader. Parameters14256,including the same768 head weights.

Capture raw local_encoder output and multiply by the existing nonPAD mask. Confirm this exact
memory equals the context argument entering every core invocation. Capture final NEXT core output
and require its EOS slot to equal actual readout_norm input. Keep query and residual at that
post-core EOS representation. Both NEXT/instruction routes and all internal_steps must still run.
Only K/V memory source changes from post-core to pre-core. Use all nonPAD positions,including
BOS/EOS/question tokens. No explicit entity IDs,answer positions,fact slots or external labels.

Do not detach memory or bypass core computation. Train backbone and head together. Source change
also changes gradient paths and joint optimization;the result cannot uniquely identify core
information destruction. Hooks are per-call,return only the registered readout replacement and
are removed on both success and exception. No accepted production source is modified.

## Fixed data and training

Byte-identical C250 TRAIN64/HOLDOUT32,original targets/order/provenance and normal/evidence_blind/
query_blind views. Use actual unchanged C248.train_one/fit and C244.replay_one with C242 fitting
and C234 renderer. The helper's reported arm is adapted only after training to child precore_read;
this is result metadata,not a patched parent training path. Console relabeling changes only C tags.

400 steps,32 rows/update,old32/added32 alternating200 cycles,normal inputs only. AdamW lr0.005,
betas(0.9,0.999),eps1e-8,weight_decay0,clip1,CPU float64,threads2,deterministic algorithms.
Before optimization require exact whole-wrapper and bare initial fingerprints and initial TRAIN
metric replay<=1e-9. No HOLDOUT before the fixed training endpoint;no holdout-driven modifications.

## Gate and workload

Primary PASS iff all five candidate seeds pass TRAIN/HOLDOUT in BOTH languages:
accuracy>=0.90;fact/query/order pairs>=0.80;both mask drops>=0.35.
TRAIN minimum29/32 answers,13/16 pairs;HOLDOUT15/16 answers,7/8 pairs per language.
Record TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS per seed/language,paired accuracy deltas,
whole-seed pass counts for candidate and immutable comparator. Do not average away a failed seed.
A valid miss is ACCEPTED VALID NEGATIVE; a pass is limited to this adaptive internal comparison.
No population reliability claim,external validation,core superiority,production adoption or Gate F.

Five candidate models x400=2000 updates/64000 training presentations.
Each inherits409 forwards/13280 rows before replay plus6/288 replay=415/13568.
Totals2075 full-model forwards/67840 row presentations,including75 scoring forwards.
Zero additional bare-reference forwards and zero comparator forwards. One new five-state bundle.
Test-fixture computations are separate from these scientific counts.

## Protection, tests and artifacts

Inherit C250346 source pins/550 inputs. Add its summary and SIX artifacts (7),then OWN6:
352 source pins/563 protected inputs. Do not apply the previous five-artifact increment by mistake.
Direct dependency union27:five C231 LM_SOURCES and C230 through C251 benchmark/helper modules.
Every actual lazy helper is protected. Preserve all accepted code/tests/logs and shared launchers.
OWN6:the C251 benchmark,test,runner,launcher,this preregistration,and docs/v5b-precore-read-v0.1.md.

Own tests24;modules136;loaded3194/focused3193. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Tests reuse already-pinned C250 synthetic fixtures/evaluator helpers. Those are not used by the
scientific path. Actual runtime loader enforces module/test counts and unique IDs.

Five ignored outputs:precore-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Checkpoint schema fold-c251-precore-read-v1:five seed/full/precore_read
identities. Preserve exact initial identity,changed head/backbone weights,actual forward counts,
exact saved/reloaded predictions and raw-logit/metric replay<=1e-9. Postcheck verifies plan,split,
hashes/sizes,child summary,original comparator/initial fields and recomputed child discrete metrics.
Manifest SHA256:2f72dec74e0fe27e9a9aba129dd1064b34a467363b5a8dc9f5a7a3a2c636fc87.

## Review and stopping

Re-fetch all six completed files at an immutable review HEAD. Match code/script blobs to tested
local files;compile/import;run24 own tests;check free names,initial/parent field timing,hook source
selection,core/query preservation,gradients,padding,exceptions,CLI indices,counts and postcheck.
The full five-model path must execute on toy encoders/cores using the real new wrapper. These
results are harness evidence only,not scientific performance. State all omitted/full-runtime checks.

Dispatcher,selected launcher and runner PowerShell ParseFile precede Python/source/parent precheck,
24 own tests,3193 focused tests,C251 training,postcheck and log publication. Branch/tree/HEAD/ACTIVE
mismatches skip before execution/logging. Integrity failures are INVALID / RETRY SAME C251,not C252.
Repair transport-only failure without retraining. No paid API,external corpus,history rewrite,
cleanup or production change. Numeric-memory/erasure tuning paused. Judge C251 before C252.
