# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C249 ACCEPTED PASS (diagnostic integrity only). C250 ACTIVE / NOT YET JUDGED. C251 NOT REGISTERED.**
C250 is the unique ACTIVE experiment:unchanged readout recipe across five new paired initializations.
Post-authoring review PASS;authoritative Windows prechecks/full regression/scientific training pending.
C248 remains ACCEPTED VALID NEGATIVE,including its failed seed234002. No production adoption.

## Latest accepted evidence — C249

Scientific execution HEAD:9d28b7420e69efe57555b7db2ccbb0eec6f3d302.
Published log commit:cac4102c0798800f3925c02cb1b38b20cd7ef8a4.
Publisher log SHA256:607db37473a7f8ed17b0692d798df582e3433f79f03be5514f2c5cb0928c5ca0.
Log bytes:618591.
Summary SHA256:3b95e6ca6b7ba645e13367a483f55fd75a9e112f3f928b2e1cdaf69913be0500.
Local summary:runs/c249-v5b-frozen-read-ablation-9da92553f325421d8acd94d8cccc3b98/summary.json.

24 own tests PASS in6.295s;3145 focused tests PASS in142.198s.
340 source pins/538 inputs preserved;12 frozen models,180 forwards/8640 row presentations;
5184 retained logit rows/72 contrast cells;zero new training/checkpoint writes.
All original prediction/metric replays,restoration replays,unchanged weights and persisted-logit/
contrast recomputation PASS. Tracked tree/execution HEAD preserved;run_execution_valid=True.
Publication is one commit after scientific execution,changing only c249/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges and recorded local postchecks,not an independent
complete-log byte rehash or reviewer execution of actual accepted learned checkpoints.

Normal HOLDOUT correct counts,pooled three seeds/two languages per family,each /96:

| Family/arm | Intact | Residual off | Uniform read |
|---|---:|---:|---:|
|Full/token_read|73|22|24|
|GRU-only/token_read|88|25|27|
|Full/eos_adapter|41|38|not applicable|
|GRU-only/eos_adapter|41|41|not applicable|

Readers together:161/192 intact,47/192 residual-off,51/192 uniform. All8 previously perfect
reader cells fall from16/16 to3/16 or4/16 off,and to2/16 or4/16 uniform. Unsuccessful seed234002
is retained:Full intact5/16,4/16;off3/16,4/16;uniform4/16,4/16. GRU intact12/16,12/16;
off5/16,5/16;uniform6/16,7/16. Original predictions/logits return after intervention removal.

These frozen networks depend on the added residual and learned nonuniform weighting under the
specified interventions. This is not a separately trained no-branch/uniform model,proof of a
unique semantic mechanism,or a reliability estimate. Co-adaptation/internal distribution shifts
remain interpretation limits. Some EOS controls also lose TRAIN accuracy;equal pooled accuracy
can hide answer flips and offsetting gains/losses. No efficiency or core-superiority claim.
Acceptance/artifacts:docs/experiment-ledger-addendum-c249-c250.md.
Acceptance/base commit:4410c888f658621e7bbd5a8f655add32aa51dfa3.

## Preserved earlier boundaries

C248:8/12 reader seed/family/language cells pass original TRAIN/HOLDOUT criteria;4 miss.
The matched EOS control has0/12 HOLDOUT passes. Only three paired initializations were tested.
Reader11 better/1 tied/0 worse versus EOS on normal HOLDOUT;all-seed primary gate still FAIL.
C247 normal-budget control,C246 erasure mixture,C244/C242 recombination,C241 evidence-use and
C239 order-transfer negatives remain unchanged. C245/C243/C240/C237/C235 remain diagnostics;
C238 remains seen16-prompt fitting only. All accepted evidence/recovery records are preserved.

## Active C250 — five new paired initializations

Experiment:C250-v5b-fresh-seed-readout-replication.
Stage:V5-B-FRESH-SEED-READOUT-REPLICATION.
One question:does the unchanged C248 reader-versus-EOS recipe reproduce its bounded result on
five prospectively fixed new initialization blocks250001,250002,250003,250004,250005?
Every seed includes Full/GRU-only and token_read/eos_adapter,20 new models total. Never replace,
drop or rerun a seed after a valid performance result. Old seed234002 is not rescued or erased.

Reuse actual unchanged C248.ReadoutPilot,ResidualHead,train_one,fit,balanced_indices and C244.replay_one.
Head seed offset remains+248000. Backbone/head seeds change together,so their effects are not
separately identified. Extra768 parameters in both arms:Full14256,GRU-only10928,width16/48 slots,
zero head output projection,all nonPAD positions eligible,byte input/unrestricted256-class output.
Keep C248 TRAIN64/HOLDOUT32 row bytes/order/provenance and original three scoring views.
400 updates/model,batch32,normal old32/added32 alternating200 cycles,AdamW lr0.005,betas(0.9,0.999),
eps1e-8,weight_decay0,clip1,CPU float64,threads2,deterministic algorithms. No new loss,erasure,
architecture change,early stop or best-checkpoint selection. Console adapter only relabels progress.

Construct Full and its common-weight GRU-only copy before either arm trains. For each new seed/
family,measure one fresh backbone reference on TRAIN's three views only. Record initial fingerprint
and initial_train metrics;do not require historical old-seed values. Each arm deepcopies this same
source backbone. C248.train_one checks exact backbone initial identity and zero-residual initial
metrics before fitting. Shared source must remain unchanged between arms. Ten references are kept.
No parent trained checkpoint is loaded. Reference measurements do not evaluate HOLDOUT.
Final HOLDOUT is scored only after400 updates and reload,not used to change training.

PRIMARY:all five new Full/token_read models pass BOTH languages and BOTH TRAIN/HOLDOUT under
original criteria:accuracy>=0.90;fact/query/order pair>=0.80;both mask drops>=0.35.
TRAIN32 rows/language,16 pairs:minima29/32 and13/16. HOLDOUT16 rows,8 pairs:minima15/16 and7/8.
Report all family/arm gates independently,all cell outcomes,20 model-level seed_results,whole-seed
both-language pass counts out of5 per family/arm,and20 paired language comparisons. Languages/
family/arm cells are correlated;there are five new paired seed blocks,not20 independent seeds.
A valid miss is ACCEPTED VALID NEGATIVE. A primary PASS concerns only this fixed batch/task,
not universal reliability,external-test performance,core superiority,production adoption or Gate F.
The task/HOLDOUT is reused from adaptive research,not a pristine external benchmark. C248 unchanged.

Workload:20x400=8000 updates/256000 training presentations. Each trained model415 forwards/13568 rows,
including original initial/final/reloaded scoring.20 models=8300/271360. Ten bare-reference
backbones add30 forwards/1920 TRAIN rows. GRAND TOTAL8330 forwards/273280 rows;330 evaluation
forwards;one new20-state bundle. Reference overhead is not omitted. No accepted-parent model inference.

C250 context:C249 parent,C248 reader,C244 base,C242 fitting,C234 binding,C231 factory,audit helper.
C250.load_inputs accepts C248 summary and correctly calls C249.load_inputs,which reads C248's
own records. It never calls C248.load_inputs,which expects C247. Old records only verify accepted
inputs;new initial references are generated independently. No parent globals/functions are patched.
Child summarizer and bundle handle20 identities;do not feed them to a12-model parent summarizer.
C244 replay contract6 forwards/288 rows remains valid for each individually trained model.

Protection:346 source pins/550 inputs;direct dependency union26;OWN6.
Own tests24;modules135;loaded3170/focused3169;only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Six ignored outputs:replication-plan.json,split-dataset.json,initial-references.json,trained-models.pt,
measurements.json,validation-summary.json. Bundle schema fold-c250-fresh-seeds-v1,20 ordered states.
Postcheck verifies source/input/artifact hashes,plan/partition,new initial references,child summary,
all original gate counts and discrete metrics from saved predictions without more model forwards.

C248 source summary:runs/c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22/summary.json.
Its SHA256:99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6.
Partition SHA256:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
Manifest:4f2bffab4fff98193a2756fe65d0403d955711f23b18e548698f45d7f93c9cee.
Design:docs/v5b-fresh-seed-replication-v0.1.md.
Registration:docs/experiment-ledger-addendum-c250-preregistration.md.
Preregistration/review HEAD:802927a7755d53e1f1523e317869646beb32aa7e.
Use tools/invoke_active.ps1 with final activation HEAD,not this pre-activation review HEAD.

## C250 post-authoring review

`post_authoring_review = PASS`
Review HEAD:802927a7755d53e1f1523e317869646beb32aa7e.
All six OWN files re-fetched after authoring. Full local UTF-8 file Git-blob hashes mechanically
match every remote reviewed identity,including both documents:
-benchmark:50d9fa788d6b697e1cfd171ee4f32213e2229853
-tests:e64630a8b680bb460183cd38b8ff90ac7a5a7e8a
-runner:26bdec80d3222abfc6c506d57a5fc7aa0208816b
-launcher:e76a3476913c9ab4f04b764161e5052ddeb914ee
-design:3005a3010f592c5f7ee045adc097274b57ecc256
-preregistration:9986ecb87245c66a61d41713de82541c584350fa.
Acceptance-base to review comparison changes exactly six additions,no accepted code/test/log edits.

Actually executed:complete new Python compile/import,UTF-8/NUL checks and recursive symbol-table
free-global/import audit with0 unresolved references in both new Python files.24 own tests PASS
before publication in8.391s and again after remote readback/hash checks in7.983s.
Manifest/independently reconstructed partition hashes pass. Tests count actual24 unique tests and
exercise a constructed3170-case exclusion filter yielding3169;that is not historical regression.
Tests cover fresh-reference3/192 accounting,no HOLDOUT reference,mutation/hook cleanup,old-seed
rejection,paired backbone equality,one-seed miss retained,full/GRU/control gate independence,
seed-level versus language-level counts and required mask criteria at100% normal accuracy.

The actual inherited C248 training helper/fit and C244 replay helper were exercised using
transcribed parent excerpts and synthetic networks. The new20-model run performed400 updates per
toy model plus10 fresh references,checkpoint save/reload and persisted postcheck,including
wrong-HEAD/reference-artifact tamper rejection. The head uses the actual transcribed ResidualHead;
zero-output initialization,768 parameters,RNG preservation and original seed offset were tested.
Synthetic ToyWrapper is a linear-backbone protocol double,not the actual GRU/FOLD or production
ReadoutPilot. Full-path authoring test substitutes only its model wrapper,metrics/protection/input
adapters within scoped patches. Scientific code does not call test helpers or patch parent code.

Three embedded Python blocks compile;precheck argv1/2 and postcheck argv1/2/3/4 match calls. Launcher
branch/tree/HEAD/ACTIVE guards,ParseFile-before-publication and exact C249/C248 paths were reviewed.
Source AST confirms loader/common-backbone-copy/reference before training and save/load/replay
order. C248/C244 writer,training,replay and context signatures were read from immutable sources;
no historical initial fields are reused for different seeds. All26 direct dependencies are pinned.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,in an isolated workspace with complete
new files and review-only C248/C244 excerpts. GitHub DNS resolution failed;connector supplied repo
content. No complete clone or full checkout was obtained. Both pwsh/powershell executables absent.
NOT executed here:full3169 historical regression,Windows PowerShell AST,user-local accepted-parent
artifact precheck,actual production GRU/FOLD training on the five new seeds. None is reported PASS.
Those remain mandatory in the authoritative runner. New-seed scientific results remain unknown.

Only this unpinned handoff changes after review HEAD. Re-read final handoff and verify branch HEAD
before issuing ExpectedHead. Do not advance the branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory/erasure-mixture tuning paused. Preserve accepted sources/tests/logs
and tools/run_c167.ps1. No paid API,external corpus,model expansion,production adoption,cleanup or
history rewrite.24 own tests ->3169 regression ->C250 replication ->postcheck ->log publication.
Integrity faults stop same C250;valid misses do not trigger retries. Repair log-only transport
without retraining. Judge C250 before registering C251.
