# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C253 ACCEPTED PASS (diagnostic integrity only). C254 ACTIVE / NOT YET JUDGED. C255 NOT REGISTERED.**
C254 is the unique ACTIVE experiment:V5-B paired residual-swap diagnostic,using saved activations
and a frozen output head only. Post-authoring review PASS;authoritative Windows/full-regression/
accepted-artifact execution pending. No production adoption or new capability claim.
C252/C251/C250/C248 remain accepted valid negatives;C249 remains diagnostic PASS.

## Latest accepted evidence — C253

Scientific execution HEAD:13523ebefc482f3b230101d9a89938bda79c69e5.
Published log commit:aca5849d45c9f6c6323db84dc9896a4092144fa0.
Publisher log SHA256:a7690d0e6db2108b4f3e6329e12fbb9a14d8049ba0fbf5ceefc661c02d118880.
Log bytes:655028.
Summary SHA256:2d65feaed637c71728cd8ed1cc60f54306a7fb733b43c6b695e86f0313f27e47.
Local summary:runs/c253-v5b-frozen-residual-97fc39ef6e8b42cba8c2d1933ddfcbf6/summary.json.

24 own tests PASS in3.166s;3241 focused tests PASS in119.771s.
364 source pins/587 protected inputs. Five frozen models;120 full-model forwards/5760 rows;
training0,new checkpoint writes0,parent bundle loads1,strict state loads5.
Parent prediction/metric/NLL replay PASS;pre/post/read components unchanged;restored output replay
PASS;weights/inputs preserved. Persisted output/component replay PASS;tracked tree clean;execution
HEAD preserved;run_execution_valid=True. Diagnostic status PASS,not capability improvement.

HOLDOUT correct counts per language (/16),English/Japanese:

| Seed | Intact | Pre-core EOS+read | Reader only |
|---:|---:|---:|---:|
|250001|16,16|15,14|16,16|
|250002|9,9|4,3|4,4|
|250003|16,16|11,12|10,12|
|250004|15,16|10,10|12,12|
|250005|16,16|14,14|16,15|

Descriptive pooled HOLDOUT145/160 intact,107/160 pre_residual,117/160 reader_only.
TRAIN320/320 intact,225/320 pre_residual,255/320 reader_only.
Pre substitution lowers all10 HOLDOUT language accuracies. Reader-only lowers7 and leaves3 unchanged
(250001 EN/JA,250005 EN);neither intervention improves a language cell. Failed seed250002 is not
rescued. All20 intervention/HOLDOUT NLL deltas are positive. Preserved argmax does not mean identical
scores:250001 reader-only HOLDOUT NLL is about0.015 versus about0.0016 intact.

The trained post-core residual supports accuracy in several learned solutions,but is not uniformly
necessary for correct answers:250001 preserves every original TRAIN/HOLDOUT answer without it.
The result does not justify removing/replacing the residual as a repair. Frozen substitutions can
alter activation direction/scale and co-adaptation at LayerNorm;they do not establish a unique
semantic mechanism,training-time necessity or superiority over a separately trained core-free model.
All C253 modes still executed the core,so no runtime-speed benefit was measured.

Acceptance/artifacts:docs/experiment-ledger-addendum-c253-c254.md.
Acceptance/base commit:bd1b88a27ab4aaa5712d06bc178158e6f410a7ff.
Publication follows execution by one commit and changes only c253/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges,metadata and recorded user-local postchecks;
no reviewer rerun of actual checkpoints or independent complete-log rehash was performed.
Do not rerun C253 or reinterpret it as a capability PASS. C252's4/5 result and negative remain intact.

## Preserved earlier boundaries

C252 pre-core query and memory/post-core residual:4/5 whole-seed joint passes,not5/5.
C251 pre-core memory/post-core query:2/5;C250 Full post-core reader2/5,GRU reader4/5,EOS controls0/5.
C249 established frozen reader-path dependence,not training-time necessity. C248 showed bounded
transfer but did not meet all-seed criteria. C247/C246/C244/C242/C241/C239 remain accepted negatives;
C245/C243/C240/C237/C235 remain diagnostics;C238 is seen-prompt fitting only. C232 bounded byte
learning and C233 competitive GRU-only baseline are not broad language/core-superiority evidence.
Preserve all accepted sources,results and recovery records.

## Active C254 — paired residual swaps

Experiment:C254-v5b-paired-residual-swap.
Stage:V5-B-PAIRED-RESIDUAL-SWAP.
One question:does the frozen post-core residual contribute information specific to the recipient's
queried entity beyond a contribution also usable from a paired prompt?

Use C253 intact saved post/read activations and the exact C252 final normalization/decoder weights.
Modes:self,order_swap,query_swap,restored. The recipient reader output remains fixed.
-order_swap:donor has identical facts/query but opposite fact order;
-query_swap:donor has identical facts/order but the opposite query;
-self/restored:original residual.
All donors stay within seed/split/language/view. Fixed metadata-defined permutations are involutions,
preserve the exact residual multiset,and have no fixed points in altered modes. No correctness/
loss-based selection. Target values validate pair semantics but do not choose donors or enter the head.

Keep all five seeds250001..250005,including failed250002;original TRAIN64/HOLDOUT32 and three views.
Compute decoder(LayerNorm(saved_post[donor]+saved_read[recipient])) with the accepted normalization
shape/epsilon/parameters and decoder. Load the full accepted model strictly for identity checks,
freeze all weights,and call ONLY its LayerNorm and decoder. Guards forbid full-model/backbone/
encoder/core/reader forwards. No learning,parameter change,new input form or answer correction.

Loader semantics:C253 outputs.pt stores activations/logits,not parameter states. C254's adapter reads
its C253 parent archive,while actual C253.load_inputs(c252_summary) retrieves C252 reference records.
C253.analyze must reproduce all parent JSONs and summary. C252.load_bundle and C253.frozen_model
supply the exact accepted final states. Do not pass C253 summary to the C253 loader that reads C252.
C252 summary/artifacts are already inherited protected inputs and are not double-counted.

Self must match saved intact logits<=1e-9 and exact argmax before swaps. Restored must match self.
Query-blind query pairs have identical inputs and saved residuals:their query-swapped logits must
match self as a structural negative control. Weights are fingerprinted after every head evaluation.
Use C253.metrics for all original scores. Persist logits;postcheck reconstructs metrics/contrasts
without further head/model calls. Report80 diagnostic cells and40 contrast cells including flips,
wrong-to-correct/correct-to-wrong,donor-target matches,accuracy/NLL deltas.

Scientific workload:120 HEAD evaluations/5760 HEAD rows,not full-model forwards.
Full-model/encoder/core/reader forwards0;training0;new learned checkpoints0.
One C252 checkpoint bundle load and5 strict state loads. Per model24 norm calls,24 decoder calls,
1152 rows. Precheck/postcheck archive re-reads,hashing and metric work are real costs but not new trials.
Historical regression fixture computation is separate from this head-only scientific workload.

PASS is diagnostic integrity only,no required accuracy direction or donor-target score. Permutation
preserves residual marginal statistics but changes joint combinations with reader outputs. Query-
specific sensitivity would be bounded intervention evidence,not proof of semantic understanding,
training-time core necessity or unique causes. Low sensitivity does not prove the core irrelevant.
No C252/C253 verdict revision,external-validation claim,production adoption or Gate F promotion.

Protection:370 source pins/599 inputs;direct dependency union30;OWN6.
Own tests24;modules139;loaded3266/focused3265;only inherited exact historical exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Outputs:swap-plan.json,head-outputs.pt,diagnostics.json,contrasts.json,validation-summary.json.
Archive schema fold-c254-head-outputs-v1 stores head logits/identities/counters,not trained parameters.
Manifest SHA256:cfbf05fc55fe6c87a0b738bfab7f4c676bb75ed503883cb399898f7936641276.
Design:docs/v5b-paired-residual-swap-v0.1.md.
Preregistration:docs/experiment-ledger-addendum-c254-preregistration.md.
Preregistration/review HEAD:5a6f421272dff912fb49930b2119bb8b336f38e8.
Use tools/invoke_active.ps1 with final activation HEAD,not the review or C253 execution HEAD.

## C254 post-authoring review

`post_authoring_review = PASS`
Review HEAD:5a6f421272dff912fb49930b2119bb8b336f38e8.
All6 OWN files re-fetched after authoring. Reviewed blobs:
-benchmark:e7084c7d6974d275d54d0ab58d9a4677b6851d6d
-tests:c1870ab6274b42c7ac8d8d6fbeda710390861c8d
-runner:a82e332819c20b34481ef1e98780ff8699dc36e4
-launcher:ebf3981cd0cd803b712c22118a9bbf2059f5e438
-design:59ffcaf328f99cab64a548d59d4b6feb1b72c46b
-preregistration:3db67cec8fa16f53fe2d5d2f3903853c37c666d2.
Complete local Git-blob hashes were mechanically checked against the four fetched code/script IDs.
Acceptance-base-to-review comparison contains exactly6 additions,no accepted file edits.

Actually executed on the matching complete new files:
-Python compile/import and UTF-8/NUL checks;recursive symbol-table audit:0 unresolved globals;
-exact24 own tests PASS before publication in1.156s and after readback/hash matching in1.007s;
-manifest self-hash and exact reconstructed partition hash;
-self/donor mappings,involutions,scope,fact/query invariants,independence from target-based selection;
-head equation,self/raw-logit restoration,query-blind identity control,source-vector nonmutation;
-forbidden full/core/reader calls,frozen-state/identity checks,head mutation rejection,hook cleanup;
-all-five head-only scoring/analysis with simulated saved activations and independent exhaustive-pair
 metric oracle;counts,contrasts,claim/schema/replay-corruption guards;
-actual loader with substituted parent archive/analyze adapters;actual run/archive/postcheck with
 synthetic frozen heads,substituted parent factories/protection,wrong-HEAD/artifact rejection;
-postcheck rejection of any repeated scoring;actual24 unique own test IDs and a constructed3266-case
 historical exclusion filter yielding3265 (not execution of the historical suite);
-three embedded Python blocks compile;CLI precheck argv1/2 and postcheck argv1/2/3/4 verified;
-exact parent paths,ACTIVE C254 guard,parser-before-publication sequence and30-entry direct union.

Parent C253 analyze/load_inputs/frozen_model/context and C252 final-state/LayerNorm/decoder path
were source-reviewed against retrieved repository content. New tests are self-contained;they use
simulated saved vectors and output heads,not actual accepted FOLD states. Parent adapters in the
loader/run tests are explicitly substituted. No complete parent import graph or accepted data run
is claimed by those tests.
Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. A full repository access attempt failed
because github.com DNS did not resolve. PowerShell is absent. NOT executed here:full3265 historical
suite,Windows ParseFile,accepted user-local parent precheck,or C254 on actual C253 activations/C252
weights. These remain mandatory in the authoritative runner and are not reported PASS.

Only this unpinned handoff changes after review HEAD. Re-read it and confirm final branch HEAD
before returning ExpectedHead. Do not advance the branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory/erasure-mixture tuning paused. Preserve all accepted evidence
and tools/run_c167.ps1. No paid API,external corpus,model expansion,production adoption,cleanup or
history rewrite.24 own tests ->3265 regression ->C254 head-only diagnostic ->postcheck ->publication.
Integrity faults stop same C254. Log-only transport failures are repaired without repeated scoring.
Judge C254 before registering C255.
