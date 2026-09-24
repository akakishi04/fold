# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C250 ACCEPTED VALID NEGATIVE. C251 ACTIVE / NOT YET JUDGED. C252 NOT REGISTERED.**
C251 is the unique ACTIVE experiment:Full pre-core reader memory with the post-core query retained.
Post-authoring review PASS;authoritative Windows prechecks/full regression/scientific training pending.
C249 remains diagnostic-integrity PASS;C248 remains ACCEPTED VALID NEGATIVE. No production adoption.

## Latest accepted evidence — C250

Scientific execution HEAD:7a9d48a99c1ca67c9eb05d0f68e7b4fa1284c881.
Published log commit:fc7d48e36e81d7b9fc8188f656771c757c398894.
Publisher log SHA256:45c93f81d69889217e60206cbd035a977ca1b2d1852c5ec464603cc3085d3098.
Log bytes:636029.
Summary SHA256:c965176039448ac99e812ad4abfce78950aafc271c65d4676bd47fe7aa59dc07.
Local summary:runs/c250-v5b-fresh-seed-replication-9bf33a726c614e558f446871954550d7/summary.json.

24 own tests PASS in18.959s;3169 focused tests PASS in180.676s.
346 source pins/550 protected inputs.20 models x400=8000 updates/256000 training presentations.
Ten fresh initial references added30 forwards/1920 rows;total8330 forwards/273280 rows.
All initial and checkpoint/prediction replays,head/whole-model weight updates,reference identity,
protected inputs,tracked tree and execution HEAD checks passed;run_execution_valid=True.
Scientific status FAIL;all four aggregate family/arm gates False.
Publication is one commit after execution and changes only c250/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges and recorded user-local postchecks,not an independent
full-log byte rehash or reviewer execution of the actual trained checkpoints.

All40 model/language cells pass the original TRAIN criteria. Full/token_read seed250001 EN has
31/32 normal TRAIN correct;other cells32/32. Do not state that every TRAIN answer was correct.
Reader cell outcomes:BOTH_PASS12,RECOMBINATION_MISS8. EOS outcomes:RECOMBINATION_MISS20.

HOLDOUT correct counts (each EN and JA cell is out of16):

| Seed | Full reader EN | Full reader JA | GRU reader EN | GRU reader JA |
|---:|---:|---:|---:|---:|
|250001|3|8|16|16|
|250002|6|8|16|16|
|250003|16|16|16|16|
|250004|2|2|5|6|
|250005|16|16|16|16|

Whole-seed both-language passes:Full reader2/5;GRU reader4/5;both EOS families0/5.
Pooled descriptive HOLDOUT:Full reader93/160 vsEOS49/160;GRU reader139/160 vsEOS99/160.
Reader-minus-EOS comparisons:15 improving cells,0 ties,5 worse. The20 comparison cells share five
paired initialization blocks;they are not20 independent training replicates.

The reading benefit repeats beyond C248's original seeds,but initialization robustness is not
established and the reader is not uniformly superior to EOS. GRU reader passes more seeds in this
batch;this motivates a matched Full experiment,not a claim that the FOLD core is harmful or generally
inferior. The adaptive small task is not an independent external benchmark. No causal mechanism,
population reliability,production adoption or Gate F claim follows.
Acceptance/artifact identities:docs/experiment-ledger-addendum-c250-c251.md.
Acceptance/base commit:bafec255be01fce2fea9b34c0e50410ecd724240.
Preserve all five new-seed outcomes and the original C248 failure;no seed replacement or retry.

## Preserved earlier boundaries

C249 diagnostic PASS:frozen readers depend on their residual and learned nonuniform weighting;
pooled intact161/192,off47/192,uniform51/192. This is not a newly trained ablated-model comparison.
C248:8/12 reader seed/family/language cells met joint criteria;4 missed. EOS0/12 HOLDOUT passes.
C247 normal-budget control,C246 erasure mixture,C244/C242 recombination,C241 evidence-use and
C239 order-transfer negatives remain unchanged. C245/C243/C240/C237/C235 remain diagnostics;
C238 remains seen16-prompt fitting only. Preserve all accepted evidence and recovery records.

## Active C251 — pre-core memory, post-core query

Experiment:C251-v5b-precore-memory-postcore-query.
Stage:V5-B-PRECORE-MEMORY-POSTCORE-QUERY.
One question:does using causal encoder states as Full's reader memory improve the same five-seed
result while keeping its actual post-core query and ordinary residual path?

C250 Full reads keys/values from final core token states and queries with final core EOS.
C251 reads keys/values from masked local GRU outputs,exactly the context entering the core.
Query and residual pooled state remain the actual final NEXT core EOS. Both original core routes
and every internal step continue to run. The core is not removed or frozen. No memory detach:
backbone and head train jointly. The source change changes computation/gradient paths and cannot
uniquely diagnose core information destruction or a specific internal cause.

The experiment-only wrapper PrecoreReadout reuses unchanged C248.ResidualHead:768 added parameters,
Wq/Wk/Wo,width16,original head seed+248000,zero output projection. Full total14256=13488+768.
It captures masked local encoder states,checks equality to actual core context inputs,and checks
post-core EOS equality to the real readout_norm input. Hooks are scoped to each call and removed
on success or exception. Original nonPAD eligibility includes BOS/EOS/query tokens;no fact parser,
entity IDs,answer-location labels,extra loss,new gate or added projection is introduced.
No accepted model source or production runtime is modified.

Use all five seeds250001..250005,including successful250003/250005 and every failed seed.
Five fresh Full candidates only. Reuse accepted C250 Full/token_read endpoints as the post-core
comparator;do not retrain comparators or add a new GRU/EOS sweep. This is an adaptive matched
comparison,not a prospective new-seed replication. No favorable-seed selection or extra budget.

Match both bare backbone initial_sha256 from C250 initial-references and full wrapper/head
initial_sha256 from its measurements before optimization. Same state-dict keys,values,dtypes and
shapes;the production fingerprint uses these,not the Python class name. Reuse original initial
TRAIN metrics for zero-residual replay. No accepted trained parent state is loaded.

Fixed C250 TRAIN64/HOLDOUT32,byte strings,row order,targets,source provenance and original three
scoring views. Actual unchanged C248.train_one/fit;400 updates,batch32,old32/added32 alternating,
normal inputs only,AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,CPU float64,threads2,
deterministic algorithms. Result arm metadata becomes precore_read after training;no parent
function/global is patched. Console adapter relabels progress only. HOLDOUT first reaches a model
after step400;no tuning,early stopping,checkpoint selection or subsequent updates use its results.

Primary:all five candidates pass BOTH languages and BOTH TRAIN/HOLDOUT with unchanged criteria:
accuracy>=0.90;fact/query/order pair>=0.80;both mask drops>=0.35.
TRAIN32 rows/language and16 pairs require29/32 and13/16;HOLDOUT16 rows/8 pairs require15/16 and7/8.
Report all10 cell outcomes,whole-seed pass counts out of5,and accuracy deltas against immutable
C250 Full/token_read. A valid miss is ACCEPTED VALID NEGATIVE;any integrity fault is INVALID /
RETRY SAME C251. A pass is bounded to this reused task/seed comparison,not external validation,
core superiority,production adoption or Gate F. C250's verdict is unchanged for every outcome.

Workload:5x400=2000 updates/64000 training presentations. Each model415 forwards/13568 rows
including initial/final/reloaded evaluation. Total2075 full-model forwards/67840 row presentations;
75 scoring forwards. Zero new bare-reference or comparator forwards. One five-state checkpoint.
Before replay409 calls/13280 rows;replay adds6/288. Same C244.replay_one and C242 evaluation.

Parent adapter reads C250's own split,initial-references and measurements directly. Do not call
C250.load_inputs,which accepts C248 evidence. Validate actual C250 result and summarize all20
records with all10 references,then independently replay discrete parent metrics through C243.
Select exactly five Full/token_read records and five Full references. Child postcheck preserves
all comparator.final values and matched initial identities,plus hashes/sizes,plan,split,summary
and discrete metrics from child predictions. Exact prediction and1e-9 raw-logit/metric replay required.

Protection:352 source pins/563 inputs;direct dependency union27;OWN6.
C250 has SIX artifacts:550 inherited inputs+parent summary/six artifacts7+OWN6=563,not562.
Own tests24;modules136;loaded3194/focused3193;only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Tests reuse already-pinned C250 synthetic helpers;scientific code never imports test utilities.
Five ignored outputs:precore-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Bundle schema fold-c251-precore-read-v1,five seed/full/precore_read states.
Manifest SHA256:2f72dec74e0fe27e9a9aba129dd1064b34a467363b5a8dc9f5a7a3a2c636fc87.
Partition SHA256:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
Design:docs/v5b-precore-read-v0.1.md.
Registration:docs/experiment-ledger-addendum-c251-preregistration.md.
Preregistration/review HEAD:ccde18c4f8718796ea340514ab7fce8c1971d6f6.
Use tools/invoke_active.ps1 with the final activation HEAD,not the preregistration or C250 HEAD.

## C251 post-authoring review

`post_authoring_review = PASS`
Review HEAD:ccde18c4f8718796ea340514ab7fce8c1971d6f6.
All six OWN files were re-fetched after authoring at this immutable HEAD. Complete local UTF-8
Git blob hashes mechanically match all six remote identities:
-benchmark:63a6707ef15ce926690a64a7e1bf2fc18a19eef5
-tests:e28fc2f92c74997dda8587932b591bdff832ff0c
-runner:f9a1b8673c827b94d51bc426f983f84b3021cf21
-launcher:97c14d962e3931063b5f82406c60f2913a0214d6
-design:b854b2bc758c83c48597da188686c1a618c21459
-preregistration:d7fb210c9f93e76c0236df84262e392979568fae.
Acceptance-to-review comparison changes exactly six added files,no accepted file edits.

Actually executed on matching complete new files:
-Python compile/import and UTF-8/NUL checks;recursive symbol-table global/import audit with zero
 unresolved names in the new benchmark and test module;
-24 own tests PASS before publication in13.804s and again after remote readback/hashes in12.303s;
-manifest and exact reconstructed partition hashes;actual own suite count and unique IDs;
-constructed3194-case exclusion-filter check yielding3193,not a full historical-suite execution;
-identical initial state keys/values and zero-residual output versus original C248 wrapper;
-explicit capture proves pre-core memory and post-core query,plus manual reader-formula agreement;
-nonzero reader gradients to query/key,encoder and core,without detached memory;
-padding exclusion,core-context mismatch rejection,invalid task/EOS rejection,hook cleanup and
 no evaluation weight mutation;
-all-seed/mask/full-criteria gate checks,comparator separation,wrong initial/count/nonfinite rejection;
-child loader selects all five comparators from parent-shaped20-record synthetic data;
-real new wrapper and inherited training/replay helper path executed on synthetic causal encoders/
 cores,including400 updates per toy model and the complete five-model save/reload/postcheck path;
-wrong-HEAD,artifact tamper and initial mismatch rejection;all5 candidate outcomes retained;
-three embedded Python blocks compile,precheck argv1 and postcheck argv1/2/3 checked;
-launcher path,ACTIVE/branch/tree/HEAD guards and ParseFile-before-publication inspected;
-AST call ordering and absence of detach/parent-checkpoint initialization in wrapper verified.

Additional untrained connectivity smoke used transcribed production computational-path excerpts
of ShortByteLanguageModel and HighPrecisionFixedRoutingCore with real PyTorch GRU on synthetic
byte prompts. It checked14256 parameters,identical zero-head outputs,encoder/core gradients and
hook cleanup. Those excerpts omitted production input-validation code and used a nonexperiment
untrained seed;this was not a full production-file or scientific-checkpoint evaluation.
The actual repository language_task.py/core source and C231 fingerprint were read to verify
masking,two-route timing,EOS provenance and state-dict identity semantics.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5 in an isolated workspace,not a full checkout.
Complete new files were tested with review-only C248 training/wrapper and C244 replay excerpts,
C250 helper excerpts and import scaffolding. Parent C250 validate_result/summarize were substituted
in the isolated loader test;the published scientific path calls the real protected functions.
The new five-model authoring run used synthetic encoders/cores and substituted evaluation,
protection and input adapters. No actual C251 scientific five-seed FOLD run was performed.
GitHub DNS resolution failed,so connector reads supplied repository bytes. pwsh/powershell absent.
NOT executed here:full3193 historical regression,Windows PowerShell AST,accepted user-local parent
artifact precheck,actual C250 comparator checkpoint replay or scientific C251 training.
None is represented as PASS. All applicable authoritative runtime checks remain mandatory.

Only this unpinned activation/review handoff changes after review HEAD. Re-read final handoff and
verify branch HEAD before returning ExpectedHead. Do not advance the branch during the user's run.

## Stop and scope

Gate F NOT PASSED;numeric-memory and erasure-mixture tuning paused. Preserve accepted sources,
tests,logs and tools/run_c167.ps1. No paid API,external corpus,larger model,production adoption,
cleanup or history rewrite.24 own tests ->3193 regression ->C251 training ->postcheck ->log publication.
Integrity faults stop same C251;valid misses do not trigger retries. Repair log-only transport
without retraining. Judge C251 before registering C252.
