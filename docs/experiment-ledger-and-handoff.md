# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C252 ACCEPTED VALID NEGATIVE. C253 ACTIVE / NOT YET JUDGED. C254 NOT REGISTERED.**
C253 is the unique ACTIVE experiment:V5-B frozen post-core residual diagnostic.
Post-authoring review PASS;authoritative Windows/full-regression/accepted-checkpoint run pending.
No production adoption. C251/C250/C248 verdicts remain unchanged;C249 remains diagnostic PASS.

## Latest accepted evidence — C252

Scientific execution HEAD:2e3102b6f1d7061afcfd0bcf996ad660fcf36a36.
Published log commit:f0882790ca5deae784513c946e5d6e60481d02f2.
Publisher log SHA256:30416c085e0f1b1cd19b6aa3df73c435a7490414c02b0546dd15c7662e4f11c2.
Log bytes:626938.
Summary SHA256:18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e.
Local summary:runs/c252-v5b-precore-query-ea8199d8ca794acba051ca5f65a391b3/summary.json.

24 own tests PASS in24.330s;3217 focused tests PASS in181.128s.
358 source pins/575 protected inputs. Five models x400 updates=2000 updates/64000 training
presentations;2075 full-model forwards/67840 total row presentations. All initial/checkpoint/
prediction replays,weight updates,protected inputs,tracked tree and execution HEAD checks passed.
Persisted query-alignment/comparator/discrete replay PASS;run_execution_valid=True.
Scientific status FAIL;candidate_gate=False. Publication follows execution by one commit and
changes only c252/latest.log/latest.json. Acceptance is based on immutable published log ranges,
metadata and recorded local postchecks,not an independent full-log rehash or actual-model rerun.

All10 TRAIN language cells:32/32 normal answers,16/16 fact/query/order pairs,both mask criteria PASS.
HOLDOUT normal correct counts per language (denominator16):

| Seed | C252 EN | C252 JA | C251 EN | C251 JA | C252 whole seed |
|---:|---:|---:|---:|---:|---|
|250001|16|16|16|16|PASS|
|250002|9|9|10|9|MISS|
|250003|16|16|10|10|PASS|
|250004|15|16|6|5|PASS|
|250005|16|16|16|16|PASS|

Whole-seed both-language passes4/5 versus C2512/5. Outcomes BOTH_PASS8,RECOMBINATION_MISS2.
The candidate retains both previously passing C251 seeds and adds250003/250004. Seed250004 EN
is not perfect:15/16 answers and7/8 of each pair type,within unchanged registered thresholds.
Seed250002 has9/16 answers in both languages,fact pairs3/8,query pairs1/8,order pairs4/8,
evidence drop0.3125 and query drop0.1875. It fails several criteria,not just rounding at a threshold.
Descriptive pooled HOLDOUT145/160 versus114/160. Ten language comparisons:4 improve,5 tie,1 worse.
The cells share five reused initialization blocks and a repeatedly inspected task;no population
reliability,independent-replication or statistical-significance claim follows.

Using a pre-core query with already-pre-core memory is a promising matched change,but all-seed
reliability remains unproven. Shared source stage is not proof of identical learned query/key spaces
or a uniquely diagnosed alignment mechanism. Computation and gradient flow changed together.
Both query and reader memory now originate before the core;the core still contributes via its
post-core EOS residual. Current scores alone do not establish the necessity of that residual.

Acceptance/artifact details:docs/experiment-ledger-addendum-c252-c253.md.
Acceptance/base commit:c647917f2ff052f0c7fe403d1355c16ba6b5da65.
Do not rerun C252,replace seed250002,relax its gate or declare production adoption.

## Preserved earlier boundaries

C251 pre-core-memory/post-core-query:2/5 joint seed passes,different pass identities from C250.
C250 fresh-seed study:Full reader2/5,GRU reader4/5,both EOS controls0/5. C248 original readers
showed bounded transfer in8/12 language conditions. C249 frozen ablation established dependency
on the trained reader path,not that an ablated model could never learn from scratch.
C247 normal-budget control,C246 mixed erasure,C244/C242 recombination,C241 evidence-use,C239
order-transfer negatives remain unchanged. C245/C243/C240/C237/C235 remain diagnostics;
C238 seen-prompt fitting only. C232 bounded byte learning and C233 competitive GRU-only baseline
are not broad language or FOLD-core-superiority results. Preserve all earlier recovery records.

## Active C253 — frozen post-core residual diagnostic

Experiment:C253-v5b-frozen-postcore-residual.
Stage:V5-B-FROZEN-POSTCORE-RESIDUAL.
One question:how much of the accepted C252 models' answer performance depends on their post-core
EOS residual base,with the trained pre-core query/memory/read vector unchanged?

All five accepted C252 Full models are frozen,including failed seed250002. No training or parameter
change. Original TRAIN64/HOLDOUT32 and normal/evidence_blind/query_blind views remain byte-identical.
Fixed modes:intact -> pre_residual -> reader_only -> restored.
At the original readout normalization:
-intact uses post-core EOS + reader output;
-pre_residual uses pre-core local EOS + the same reader output;
-reader_only uses the same reader output without an EOS residual base;
-restored uses the original post-core EOS + reader output again.

Both original core routes still execute in every mode. This is an output-path intervention on
jointly trained weights,not a newly trained core-free model or a speed comparison.
Pre-core EOS itself summarizes the whole prefix. Removing/swapping post changes activation scale
and distribution,so a decline does not uniquely identify a reasoning mechanism. Unchanged accuracy
would not prove that the core was irrelevant during learning or on other tasks.

Use actual C252.AlignedPrecoreReadout,load accepted final states strictly,verify final_sha256 and
14256 parameters,then eval/requires_grad=False. C252.load_bundle validates the five ordered states.
Read C252's own split/measurements,not C252.load_inputs (which reads C251). Validate actual C252
summary and summarize(refs,C242). final/predictions/final_sha256 are the learned endpoint;initial
fields and c251_comparator are not used as current model outputs.

Scoped outer hooks capture original post before the parent wrapper adds read. At LayerNorm output,
verify original input equals post+read. Intact/restored leave the original output alone;the two
changed modes compute functional layer_norm on the new combination with identical norm parameters
and epsilon. Core route counts,query-input provenance,normalization ordering and one-time hook counts
are enforced. pre/post/read component tensors must be exactly unchanged across modes for each input.
All hooks are removed after success or exception. No parent source or method is patched.

Intact runs first and must reproduce all parent prediction arrays and final metrics including NLL
before either intervention. Weight fingerprint is checked after every forward. Restored logits
must match intact within1e-9 and argmax outputs exactly. Original inputs and256-byte output classes
remain unchanged. Raw logits and component vectors are persisted for offline recomputation.

PASS means diagnostic integrity ONLY,independent of score improvement/decline. Invalid source,
artifact,schema,nonfinite,test,replay or workload checks stop same C253. No C252/Gate F revision.
Report every mode/seed/split/language accuracy,NLL,pair metrics and masks,plus altered-minus-intact
accuracy/NLL,flips,wrong-to-correct/correct-to-wrong counts,logit differences and component norms.

Workload:5x4x2x3=120 full-model forwards/5760 row presentations;24/1152 per model.
Extra normalization recomputations60. Diagnostic cells80;contrast cells40. Parent bundle load1,
strict state loads5,new training0,new learned checkpoint writes0,scientific network calls0.
Archive/JSON/hash work and historical test fixtures are separate costs,not zero-cost inference.
Five ignored outputs:residual-plan.json,outputs.pt,diagnostics.json,contrasts.json,validation-summary.json.
outputs.pt schema fold-c253-frozen-outputs-v1 contains logits/activations,not learned parameter states.
Postcheck reconstructs all metrics/contrasts/component and restored checks without model inference.

Protection:364 source pins/587 inputs;explicit deciding dependency union29;OWN6.
Own tests24;modules138;loaded3242/focused3241. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
No new exclusions or changes to accepted sources/tests/logs/shared launchers.
Manifest SHA256:c48689b9cebedc757261ded1912dbb597884f19ac007d971bcd7bfbfbfd8307d.
Design:docs/v5b-frozen-residual-path-v0.1.md.
Preregistration:docs/experiment-ledger-addendum-c253-preregistration.md.
Preregistration/review HEAD:f498f0322e0ab1e447a3173e0e903c7781f09ab8.
Use tools/invoke_active.ps1 with the final activation HEAD,not the C252 or preregistration HEAD.

## C253 post-authoring review

`post_authoring_review = PASS`
Review HEAD:f498f0322e0ab1e447a3173e0e903c7781f09ab8.
All six OWN files re-fetched at that immutable HEAD. Complete local Git-blob hashes mechanically
match the fetched file identities:
-benchmark:048a6661c5e01506984164f7dcb8a8e06b9fb300
-tests:73da0b2d647d80fa67439cf437173f44a70daddb
-runner:874573417a419195fa36f771b839426da9669462
-launcher:edc4cee567cbce88be446a013aa5ca4fc25afcc2
-preregistration:4f3aeb9b46ad0d8c1bcfce5e4eb821dc72f1b48a
-design:6d14a2aac77acaf778a64143c81a04a3225b3965.
Acceptance-base to review comparison is exactly six additions. No accepted file was edited.

Actually executed on the complete matching new benchmark/test/script files:
-UTF-8/NUL checks,Python compile/import,and recursive symbol-table audit:zero unresolved globals;
-exact24 own tests PASS before publication in2.697s and after remote readback/hash check in2.649s;
-actual own suite count/unique IDs;constructed3242-case exclusion filter yielding3241;
-manifest self-hash and independently reconstructed exact partition hash;
-intact/original equality,manual altered equations,pre/post/read invariance,restored equality,
 full route/hook counts,freeze/mode/task/EOS/norm guards and two-layer hook cleanup;
-mutation rejection,parent-prediction mismatch stopping after six intact forwards,strict state loads;
-all-five diagnose/analyze path on synthetic models,corrupt counts/modes/components/restored logits;
-actual child run/archive/postcheck with synthetic parent-compatible models and substituted
 context/protection/input adapters,including wrong-HEAD and tampered-artifact rejection;
-postcheck forbids new model calls;capability-claim guard and parser/CLI/parent-path checks;
-three embedded Python blocks compile;precheck argv1 and postcheck argv1/2/3 verified.

The first local own-test pass exposed a test fixture replacing LayerNorm with Identity left in
training mode,so the earlier frozen-eval guard correctly triggered before the intended norm guard.
The fixture was corrected to Identity().eval() BEFORE publishing any OWN file. No scientific
condition,accepted source or runtime guard was weakened.

Additional review-only checks actually executed:
-the retrieved C252 AlignedPrecoreReadout class body was transcribed into an isolated namespace
 with a synthetic backbone/head. Its original nested hook sequence worked with all24 C253 forward
 variants for one untrained nonexperiment seed;components/restored outputs/hooks checked. This was
 not the production FOLD backbone or an accepted learned-checkpoint evaluation;
-200 randomized output sets over both exact split sizes matched independent exhaustive-pair
 enumeration for all discrete metrics. C243 pair/discrete source was also read and compared.
Actual language_task LayerNorm/decoder order and C252 context/writer/normalization injection were
source-reviewed to establish hook ordering and final-state semantics.

Reviewer runtime verified:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Complete new own tests are
self-contained and use synthetic parent-compatible models;no fake full repository import graph
was needed to execute that exact new test module. The loader unit test substitutes parent summary
functions,while the scientific path calls the actual protected parent functions.
A full GitHub checkout was attempted but github.com DNS resolution failed. PowerShell is absent.
NOT executed here:the full3241 historical suite,Windows ParseFile,the accepted user-local artifact
precheck,or the actual five C252 trained-model diagnostic. None is reported PASS;they remain mandatory
in the authoritative launcher. The constructed suite filter is not historical-suite execution.

Only this unpinned handoff changes after review HEAD. Re-read final handoff and verify branch HEAD
before giving ExpectedHead. Do not advance the branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory and erasure-mixture tuning paused. Preserve all accepted evidence
and tools/run_c167.ps1. No paid API,external corpus,model expansion,inference repair,production adoption,
cleanup or history rewrite.24 own tests ->3241 regression ->C253 diagnostic ->postcheck ->log publication.
Integrity faults stop same C253. Repair log-only transport without repeating inference. Judge C253 before C254.
