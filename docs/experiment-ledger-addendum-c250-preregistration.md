# C250 preregistration — paired fresh-seed replication

Experiment:C250-v5b-fresh-seed-readout-replication.
Stage:V5-B-FRESH-SEED-READOUT-REPLICATION.
C249 ACCEPTED PASS for diagnostic integrity;C248 remains ACCEPTED VALID NEGATIVE.
Gate E PASSED;Gate F NOT PASSED. C251 NOT REGISTERED.
This document registers C250. Committed-byte authoring review and authoritative activation are
required before execution. It is not a repair,retry or seed replacement for C248.

## One question and fixed prospective seed set

Does the unchanged C248 reader-vs-equal-parameter-EOS recipe reproduce its bounded result on
new initialization blocks250001,250002,250003,250004,250005?
Use all five in this order,each Full/GRU-only,each token_read/eos_adapter:20 models.
No favorable-seed selection,early termination after a success,extra seeds or retries for a valid
negative. The head initialization remains seed+248000;backbone/head randomness is still linked.
The seed choice is fixed before any actual model result from this batch is available.

## Parent evidence and source contracts

Acceptance/base commit:4410c888f658621e7bbd5a8f655add32aa51dfa3.
Acceptance record:docs/experiment-ledger-addendum-c249-c250.md.
C249 execution HEAD:9d28b7420e69efe57555b7db2ccbb0eec6f3d302.
Published log commit:cac4102c0798800f3925c02cb1b38b20cd7ef8a4.
Publisher log SHA256:607db37473a7f8ed17b0692d798df582e3433f79f03be5514f2c5cb0928c5ca0.
Summary SHA256:3b95e6ca6b7ba645e13367a483f55fd75a9e112f3f928b2e1cdaf69913be0500.
Local summary:runs/c249-v5b-frozen-read-ablation-9da92553f325421d8acd94d8cccc3b98/summary.json.
Require exact C249 execution-valid PASS through its actual validate_result.

C249 required artifacts:
- ablation-plan.json:9fd82672124ff0227174d7a9df894c67ca9f1958a36fad6cbc575e1179dfa414
- contrasts.json:c7bf603849b29a55a0fa7b7e4843b909df4fab7a41ab1081c4f77125b0438e22
- diagnostics.json:2e849c3d6fda7bae1b9b89325f7515f51e18886e679914a32a470234fa9d6310
- logits.json:c28e79ac452bfbc49a4904582abdc233db211ec703f1b8340f0756f389f792d0
- validation-summary.json:7613f8266a32e67e683a3b0c86aac47437b18a4b677e808a4d5a0ef5442a7aed

C248 is an inherited protected data/recipe source:
summary SHA256:99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6.
Local summary:runs/c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22/summary.json.
Partition SHA256:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
C250.load_inputs validates C248 summary,then calls C249.load_inputs with that C248 summary.
That helper reads C248's own split/measurement schema;it does not run its ablation or load weights.
Do not call C248.load_inputs,which expects C247 evidence,with a C248 summary.
C250 context roles:C249 parent,C248 reader,C244 replay base,C242 fitting,C234 binding,C231 factory,audit.

All parent bytes remain protected,including the C24925MB logits file and earlier checkpoints.
Hashing them is not deserializing or evaluating a trained checkpoint. No accepted trained weights
enter initialization;no parent inference is performed.

## Unchanged scientific recipe and new initial-reference contract

Use actual unedited C248.ReadoutPilot,ResidualHead,train_one,fit,balanced_indices and C244.replay_one.
C248.audit_recipe(C244) verifies the optimizer AST/constants and row schedule. No global parent
constant,seed set or function is monkeypatched. Relabeling progress text is console-only.
Full14256/GRU-only10928 parameters include768 added in either arm. Preserve width16,48 slots,
zero output projection,nonPAD token eligibility including BOS/EOS/question tokens,and256-class output.
TRAIN64/HOLDOUT32 row bytes/order/labels/provenance and all three scoring views remain identical.
400 updates/model,batch32,old32/added32 alternating,normal inputs only;AdamW lr0.005,betas(0.9,0.999),
eps1e-8,weight_decay0,clip1,CPU float64,threads2,deterministic algorithms.

Old-seed initial_sha256/initial_train fields cannot describe new seeds. Construct Full and the
common-weight GRU-only copy before either arm trains. For each seed/family,measure one fresh,
unmodified backbone reference on TRAIN's three views. Store seed,family,initial_sha256,initial_train,
reference_forward_calls=3,reference_row_presentations=192. HOLDOUT is not evaluated at this stage.

Each arm gets a deep copy of that backbone and its own original C248 head initialization rule.
Pass the newly measured reference,not historical C248 initial metrics,to C248.train_one.
The helper verifies backbone_initial_sha256 and zero-residual initial metrics before fitting;
its record's initial_sha256 is the wrapper/head state,not the backbone fingerprint.
After fitting,final_sha256 is the full trained wrapper and is used only for checkpoint replay.
The source backbone must remain unchanged before and after each arm. Record all10 references.

Final measurements/predictions are after step400 and replay. No HOLDOUT-driven tuning,selection or
further training. Preserve all failures. A child20-state loader/schema and child summarizer are
required;the parent's12-model identity validator must not be applied to new records.

## Gates and reporting

Retain per-language BOTH-split requirements:accuracy>=0.90;fact/query/order paired both-correct>=0.80;
evidence/query accuracy drops>=0.35. TRAIN32 rows/language and16 pairs:29/32 and13/16 minima.
HOLDOUT16 rows/language and8 pairs:15/16 and7/8 minima.
Primary PASS iff all five new Full/token_read models pass both languages and both splits.
GRU-only/token_read and both EOS-control family gates remain independent.

Classify every seed/family/language as TRAIN_CRITERIA_MISS,RECOMBINATION_MISS or BOTH_PASS.
Report seed_results for20 model identities,whole-seed both-language pass counts out of5 for each
family/arm,and20 paired reader-minus-control language comparisons. The20 cells per arm are not
20 independent initializations;the fresh paired seed count is5. Do not remove a failed language.

A valid primary miss is ACCEPTED VALID NEGATIVE. A primary pass refers to this fixed new batch,
not the old C248 experiment,universal robustness,unseen vocabulary or external task generalization.
C248 remains negative even if C250 passes. If controls also pass,do not infer reader-specific superiority.
Same parameter count does not mean same computation or optimization geometry. No significance test,
population reliability guarantee,core advantage,production adoption or Gate F promotion is claimed.

## Fixed workload and integrity

20x400=8000 updates/256000 training presentations.
Each model uses C248409 forwards/13280 rows plus C244 replay6/288=415/13568.
20 trained models total8300 forwards/271360 rows. Ten initial-reference backbones add30 forwards/
1920 TRAIN rows,so total8330 forwards/273280 row presentations. Evaluation forwards total330.
One new bundle with20 states;zero accepted-parent model forwards and zero scientific network calls.
All initial-reference overhead is scientific work,not omitted authoring overhead.

Check exact individual and aggregate counts,initial/reference pairing,head/whole-model weight
changes,final fingerprint,exact prediction replay and raw-logit/metric replay<=1e-9. One missing
reference forward,wrong old-seed identity,bad source/artifact/schema,nonfinite value,test failure,
mutation or replay fault is INVALID / RETRY SAME C250. Performance failure is not a retry reason.

## Protection, tests and outputs

Inherit C249340 source pins/538 inputs. Add C249 summary+five artifacts and OWN6:346 pins/550 inputs.
C248 sources/artifacts are already inherited and must not be double counted. Direct union26:
five C231 LM_SOURCES plus C230 through C250 benchmark/helper entry points. All deciding-path lazy
imports remain source-pinned. No accepted code/test/log or shared launcher changes.

OWN6:fold_lm/v05_benchmarks/model_c250_fresh_seed_replication.py;
tests_lm/test_v05_c250_fresh_seed_replication.py;tools/run_c250.ps1;tools/invoke_c250.ps1;
this preregistration;docs/v5b-fresh-seed-replication-v0.1.md.
Own tests24;modules135;loaded3170/focused3169;only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Actual runtime loaders enforce counts/unique IDs;synthetic count testing is not full regression.

Six ignored local artifacts:replication-plan.json,split-dataset.json,initial-references.json,
trained-models.pt,measurements.json,validation-summary.json. New bundle schema:fold-c250-fresh-seeds-v1,
20 states in seed/family/arm order. Summary has all four gates,seed_results,seed_pass_counts,
comparisons,counters including reference_forwards/reference_rows,and integrity flags.
Postcheck verifies hashes/sizes,plan,partition,stored references,summary and C243 discrete metrics
from child final predictions without new model forwards. Only console log/receipt are mirrored
into docs/experiment-run-logs/c250/latest.*.
Manifest SHA256:4f2bffab4fff98193a2756fe65d0403d955711f23b18e548698f45d7f93c9cee.

## Authoring review and stop

Re-fetch all six committed OWN files after authoring and compare complete code/script blob hashes
to tested bytes. Compile/import,run24 own tests,audit free-global bindings,parent schema/writer
semantics,source coverage,count arithmetic,shared-copy/reference timing,CLI/PowerShell ordering.
Tests may use synthetic networks and parent excerpts;report that scope rather than claiming actual
FOLD or a complete historical regression. Do not test these new seeds on actual FOLD before registration.

Dispatcher/launcher/runner ParseFile precedes Python/source/parent precheck,24 own tests,3169
focused tests,C250 replication,postcheck,remote publication. Branch/tree/HEAD/ACTIVE mismatches skip
before logging. No command is issued before post-authoring review PASS. A log-only failure is
repaired without retraining. Numeric-memory/erasure-mixture tuning stays paused. No paid API,
external data,larger model,cleanup,history rewrite or production change. Judge C250 before C251.
