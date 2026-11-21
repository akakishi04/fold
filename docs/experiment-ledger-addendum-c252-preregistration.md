# C252 preregistration — pre-core query alignment

Experiment:C252-v5b-precore-query-alignment.
Stage:V5-B-PRECORE-QUERY-ALIGNMENT.
C251 ACCEPTED VALID NEGATIVE;C253 NOT REGISTERED. Gate E PASSED;Gate F NOT PASSED.
This is a new matched architecture comparison,not a retry or seed replacement.

## Scientific question

With C251's pre-core K/V memory fixed,does changing only the attention-query source from
post-core EOS to pre-core local-encoder EOS improve the same five Full seed blocks?

Acceptance/base commit:c217a7562c1c396d1a390e8e250083521ef027a5.
Acceptance record:docs/experiment-ledger-addendum-c251-c252.md.
C251 execution HEAD:9fb7e7cfec2521815258cf2f0c3b433bcea6419d.
Published log commit:36555face557650c73521ef0709063ba4ae7f8c7.
Publisher log SHA256:0cf296dca8d7633cd3b4d8547a5b2be408d21675a961355743006ee01a25e694.
Summary SHA256:55038562223ac2bf87db09d2f102d9bd0ca6aacaeaf1381186a836330e26578c.
Local summary:runs/c251-v5b-precore-read-dcc6ca85fe504ea7a71db741ab1558b1/summary.json.
Require exact valid FAIL,seed_pass_count2,comparator_seed_pass_count2 and
cell_outcomes BOTH_PASS4/RECOMBINATION_MISS6.

Required parent artifacts:
- measurements.json:c98c5e6bbe313eac35895290d06f002756816918d7341de946941ab70ed0c398
- precore-plan.json:2f72dec74e0fe27e9a9aba129dd1064b34a467363b5a8dc9f5a7a3a2c636fc87
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
- trained-models.pt:0fce9c6e666360cf28a3723f870565a7aa1308bfa2a9a524c9a804080dc1e5c1
- validation-summary.json:f4b5128aeb4d730a4227a2c820cdc21874ae269c3ea3c3f669d0202390227da2

## Parent semantics and inputs

Read C251's own split and measurements directly. Validate C251 summary with its real
validate_result and summarize(records,C242). Recompute all parent discrete metrics from saved
prediction arrays before using the five endpoints as comparators.

C251 record meanings:
- backbone_initial_sha256 = bare Full backbone before training;
- initial_sha256 = complete wrapper/head before training;
- initial_train = zero-residual initial TRAIN metrics;
- final/final_sha256/predictions = after400 updates;
- c250_comparator = inherited C250 evidence only.

C252 uses backbone_initial_sha256 and initial_train to construct the fresh training reference,
and requires its complete wrapper fingerprint to equal C251.initial_sha256. It never loads the
accepted trained C251 checkpoint as initialization.

## Changed variable

C251 and C252 have identical trainable state and initialization.
C251 uses pre-core K/V memory but q=Wq*h_postcore.
C252 uses the same pre-core K/V memory and q=Wq*h_precoreEOS.
The residual base passed onward remains h_postcore.

The new AlignedPrecoreReadout:
- captures raw local-encoder sequence and applies the original nonPAD mask;
- requires that masked sequence to equal the context entering every core call;
- verifies both routes execute for all internal steps;
- verifies final NEXT core EOS equals the actual readout_norm input;
- computes query from the matching pre-core EOS;
- computes key/value read over the same pre-core sequence;
- adds the learned reader output to the post-core EOS residual base.

The original C248 ResidualHead modules and seed+248000 initialization are reused.
No extra parameters:backbone13488+reader768=14256.
No detach,parser,gold location,extra loss,new gate or output restriction.
Changing the query source changes both forward behavior and gradient flow;do not claim a unique
inference-time mechanism from the result.

## Fixed training and gate

Seeds250001..250005,all retained.
Exact C251/C250 TRAIN64/HOLDOUT32 rows,order,targets and three views.
Unchanged C248.train_one/fit and C244.replay_one.
400 updates/model,batch32,normal old32/added32 alternating.
AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,clip1.
CPU float64,threads2,deterministic algorithms.
No early stop,failed-seed replacement,extra steps or HOLDOUT-driven choice.

Primary PASS iff all five candidates pass both languages and both splits:
accuracy>=0.90;fact/query/order pair>=0.80;evidence/query drops>=0.35.
TRAIN minima29/32 answers and13/16 pairs;HOLDOUT15/16 and7/8.
Report all10 language cells,whole-seed pass count,cell outcomes and paired HOLDOUT deltas
against immutable C251. Do not average away a failed seed.

A valid gate miss is ACCEPTED VALID NEGATIVE. Any source/artifact/schema/count/nonfinite/replay/
initialization/test fault is INVALID / RETRY SAME C252. C251 remains accepted for every outcome.

## Workload and protection

Five models x400=2000 updates/64000 presentations.
Each has409 forwards/13280 rows before reload plus6/288 replay=415/13568.
Totals2075 forwards/67840 rows;75 evaluation forwards.
No new reference/comparator forward,one five-state bundle,no parent inference/network call.

Inherit C251352 source pins/563 protected inputs.
Add parent summary+five artifacts and OWN6:358 source pins/575 protected inputs.
Direct dependency union28:five C231 LM sources plus C230 through C252 benchmark/helper modules.
Own tests24;modules137;loaded3218/focused3217.
Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.

OWN6:
- fold_lm/v05_benchmarks/model_c252_precore_query_alignment.py
- tests_lm/test_v05_c252_precore_query_alignment.py
- tools/run_c252.ps1
- tools/invoke_c252.ps1
- this preregistration
- docs/v5b-precore-query-alignment-v0.1.md

Five ignored artifacts:alignment-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Bundle schema fold-c252-precore-query-v1.
Manifest SHA256:f662c4d9c5588bbc0662ae9f578dd59068354a76951bf7192f18f8e53166fd9b.

## Review and stop

After all six files exist,re-fetch committed bytes,verify blob identities,compile/import,run24
own tests and audit free names,parent schema,query/memory/residual provenance,gradients,PAD masking,
hook cleanup,counts,CLI and parser/publication ordering. Synthetic authoring tests are not
scientific evidence. Full3217 regression,Windows PowerShell AST,user-local parent checks and actual
five-model training remain authoritative-run requirements.

Do not issue a launcher until post-authoring review PASS is recorded in the handoff.
Judge C252 before registering C253.
