# C253 preregistration — frozen post-core residual diagnostic

Experiment:C253-v5b-frozen-postcore-residual.
Stage:V5-B-FROZEN-POSTCORE-RESIDUAL.
C252 ACCEPTED VALID NEGATIVE;C254 NOT REGISTERED. Gate E PASSED;Gate F NOT PASSED.
Registration is separate from acceptance. The authoritative handoff activates this diagnostic
only after committed-byte authoring review;no automatic successor execution.

## Question and immutable parent

How much does answer performance in all five frozen C252 models depend on the post-core EOS
residual base, with the learned pre-core attention query,memory and reader contribution fixed?
This investigates the contribution of a specific trained output path,not training-time core necessity.

Acceptance/base commit:c647917f2ff052f0c7fe403d1355c16ba6b5da65.
Acceptance record:docs/experiment-ledger-addendum-c252-c253.md.
C252 execution HEAD:2e3102b6f1d7061afcfd0bcf996ad660fcf36a36.
Published log commit:f0882790ca5deae784513c946e5d6e60481d02f2.
Publisher log SHA256:30416c085e0f1b1cd19b6aa3df73c435a7490414c02b0546dd15c7662e4f11c2.
Parent summary SHA256:18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e.
Parent path:runs/c252-v5b-precore-query-ea8199d8ca794acba051ca5f65a391b3/summary.json.
Require exact valid FAIL,seed_pass_count4,and outcomes BOTH_PASS8/RECOMBINATION_MISS2.

Required parent artifact SHA256 values:
-alignment-plan.json:f662c4d9c5588bbc0662ae9f578dd59068354a76951bf7192f18f8e53166fd9b
-measurements.json:dc88a83ab9d8add4022ba898af9a030b787cd46e088c94b1d26e205c83c29b91
-split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
-trained-models.pt:024e8081fae8bc45ce449b3bdf53745499911ca631387620a6575e2312c5b6c3
-validation-summary.json:8442f683dfe0ed9122f476b723083d017a6cd5ef6e1087bca67dfd20fc167fbf

## Parent schema and writer semantics

Read C252's own summary,split and measurements. Do not call C252.load_inputs,which reads C251.
Call actual C252.validate_result and C252.summarize(refs,C242 fitting) on the five original records.
Require seed250001..250005,family full,arm aligned_precore_read in fixed order.
C252.final/predictions/final_sha256 represent the400-update endpoint. Its initial fields and
c251_comparator are NOT the selected model state or new diagnostic evidence.

C252.load_bundle checks schema fold-c252-precore-query-v1 and ordered five seed/full/arm states.
Instantiate actual C252.AlignedPrecoreReadout(factory.new_model(seed),seed),load_state_dict(strict=True),
verify final_sha256 and14256 parameters,and freeze eval/gradients. This is intentionally a diagnostic
of learned final states,not fresh training. Exactly one parent bundle load and five state loads.
Factory,core,renderer,normalization,decoder and wrapper sources remain immutable/protected.

## Four fixed modes and entry point

Mode order:intact,pre_residual,reader_only,restored. Every mode scores TRAIN then HOLDOUT,each with
normal,evidence_blind,query_blind in that order. Exact TRAIN64/HOLDOUT32 bytes,targets,order,provenance
and all five seeds remain fixed,including the one failed seed.

At the normalization input,replace only the residual base:
-intact:LN(post+read);
-pre_residual:LN(pre+read);
-reader_only:LN(read);
-restored:LN(post+read) through the unmodified original computation.

The reader's pre-core EOS query,pre-core K/V,projection weights and actual read vector are unchanged.
Core routes/internal steps still compute in all modes;they are not removed from workload accounting.
No input erasure,teacher location,parser,extra loss,weight update or answer correction is introduced.

Scoped diagnostic hooks register before C252 installs its own forward-scoped injection hook.
The diagnostic normalization pre-hook sees untouched post. The parent's subsequent pre-hook adds
read. The diagnostic normalization output hook verifies its args equal post+read,then optionally
returns functional layer_norm(pre+read) or layer_norm(read),with the original shape,weights,bias,epsilon.
Intact/restored return None from that hook,leaving original outputs unchanged.
The two changed modes therefore compute the original norm and one additional norm;60 additional
normalization computations are counted. No recursive module call or unregistered model forward.

Require one encoder/query/reader/normalization event per forward and original route counts.
Compare query-projection input to captured local EOS,original residual to final NEXT core EOS,
and the parent normalization argument to their exact sum. Save pre/post/read components and
require exact equality across all four modes for the same input. Preserve every parameter and
remove all hooks even after an exception. Run under CPU float64,threads2,deterministic algorithms.

## Fixed diagnostic gate

After intact's six forwards,recompute original parent final metrics and require all saved argmax
arrays to match before either intervention. Original NLL is replayed from current intact logits,
not inferred from argmax. Tolerance1e-9 for metric/logit replay;predictions exact.
Frozen fingerprint is checked after every forward. Restored outputs must return to intact raw
logits within1e-9 and exactly identical predictions. Captured reader and core components stay fixed.

PASS is integrity only:no required accuracy decline,benefit,rule match or seed-level success count.
Source/artifact/schema/nonfinite/replay/initialization/workload/test failure is INVALID / RETRY SAME C253.
C252 remains a valid negative regardless of diagnostic observations. No Gate F promotion.

## Measurements and retained evidence

Use original fact/query/order pairing,computed directly from unchanged row metadata. Compare the
new metrics implementation against the accepted C243 discrete formulas in authoring review.
Every mode/split/language reports normal accuracy,answer NLL,three pair accuracies,and original
masked accuracies/drops. Raw256-way outputs are never restricted to the supplied digits.

For pre_residual and reader_only versus intact,report per seed/split/language:
original/changed correct counts,wrong-to-correct,correct-to-wrong,answer flips,accuracy and NLL
deltas,maximum absolute normal-logit change,and original mean L2 norms of pre/post/read vectors.
Correlated conditions are not independent replicates. Preserve per-seed/per-language data.

Five models x4 modes x2 splits x3 views=120 full-model forwards;5760 row presentations.
Per model24/1152. Diagnostic cells80;contrast cells40. New training0,new checkpoint writes0,
parent bundle loads1,strict model state loads5. Scientific network calls0.
Input hashing,JSON calculations and raw-output serialization have real costs. Historical unit-test
fixtures are outside this scientific workload and may execute their own toy model computations.

Five ignored outputs:residual-plan.json,outputs.pt,diagnostics.json,contrasts.json,validation-summary.json.
outputs.pt schema fold-c253-frozen-outputs-v1 contains the five ordered entries of logits and
pre/post/read activations,not parameter states. Postcheck loads this archive with weights_only=True
and recomputes every derived metric,contrast,component-invariance and restoration check without
model inference. It compares JSON exactly and verifies input/output hashes,sizes and summary.

## Source protection and authoring checks

Inherit C252358 source pins/575 inputs;add parent summary+five artifacts and OWN6:
364 source pins/587 inputs. Deciding dependency union29:five C231 LM_SOURCES plus explicit
C230..C253 helper/entry modules. No accepted source/test/log or shared launcher is modified.
Own tests24;modules138;loaded3242/focused3241. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Actual loader counts/unique IDs remain mandatory,not source-string literal checks.

OWN6:benchmark model_c253_frozen_residual_path.py,test_v05_c253_frozen_residual_path.py,
tools/run_c253.ps1,tools/invoke_c253.ps1,this preregistration,and docs/v5b-frozen-residual-path-v0.1.md.
Manifest SHA256:c48689b9cebedc757261ded1912dbb597884f19ac007d971bcd7bfbfbfd8307d.

After publishing all6 files,re-fetch committed remote bytes,match full-file hashes,compile/import,
run exact own tests,audit free names,normalization-hook ordering,parent final-state semantics,
all direct dependencies,counts,CLI indexes and parser-before-publication guards.
Tests use self-contained synthetic parent-compatible models;they are not trained FOLD evidence.
Any additional parent-class excerpt smoke must be labeled as such,not a full-checkout test.
Record actual checks and pending Windows/full-suite/accepted-checkpoint checks in handoff.

## Scope and stop

An unchanged score means the residual vector was dispensable for that trained model under this
specific substitution,not that the core was unnecessary during learning. A decline could arise
from co-adaptation or activation-scale/distribution changes,not uniquely from lost reasoning.
Pre-core EOS is already a whole-prefix summary. No population reliability,core superiority,
production adoption or external validation claim. Query/read modifications and new learning are out of scope.

Dispatcher,selected launcher and runner ParseFile precede Python syntax/parent precheck,24 own
checks,3241 focused tests,diagnostic,postcheck and log publication. Wrong branch/dirty tree/stale
HEAD/ACTIVE mismatch skip before logging. Repair log-only transport without repeated inference.
No paid API,external corpus,larger model,cleanup,history rewrite or production change. Judge C253 before C254.
