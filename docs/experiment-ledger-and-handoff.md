# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C255 ACCEPTED PASS (diagnostic integrity only). C256 ACTIVE / NOT YET JUDGED. C257 NOT REGISTERED.**
C256 is the unique ACTIVE experiment:V5-B fresh three-entity bilingual task-shift training.
No production adoption or Gate F promotion. C252 remains ACCEPTED VALID NEGATIVE.
C253/C254/C255 remain diagnostic PASS;all earlier verdicts/recovery records are preserved.

## Latest accepted evidence — C255

Scientific execution HEAD:6b577da1edc7339dbfd68b3127870074de218e48.
Published log commit:48856dd7dabb84f1f8a71158d03a5ee9db2fd255.
Publisher log SHA256:a733f750125ccacfc5ce54867bce122c91561bd105e9d1eac1adaf04ab13bc2d.
Log bytes:651389.
Summary SHA256:6c4e9a569a7c622259b501f209781b357d183dfbaf5750a6d6c939f5e59e3150.
Local summary:runs/c255-v5b-value-residual-8203653a07964d9bb549c272a8b9b943/summary.json.

24 own tests PASS in1.534s;3289 focused tests PASS in122.954s.
376 source pins/611 protected inputs. Five frozen learned models;120 head evaluations/5760 head rows.
Full-model/encoder/core/reader forwards0;training0;checkpoint bundle loads1;strict state loads5;
new learned checkpoint writes0. Self/C254-self/coherent-donor/restored/evidence-blind controls
replayed;weights and protected inputs preserved;persisted recomputation PASS.
Tracked tree clean;execution HEAD preserved;run_execution_valid=True.
Diagnostic status PASS;capability_pass_claim=False;causal_mechanism_claim=False.

HOLDOUT self correct145/160. Fixed-query reversed-value residual swap correct140/160.
Transitions:7 correct-to-wrong,2 wrong-to-correct,9 total answer flips,9 donor-target matches.
Per seed HOLDOUT EN/JA (/16):
-250001:self16,16 -> value16,16.
-250002:self9,9 -> value7,7.
-250003:self16,16 -> value16,16.
-250004:self15,16 -> value15,15.
-250005:self16,16 -> value16,16.
TRAIN self320/320 -> value309/320.

Accepted C254 comparisons on the same frozen states:
-order_swap HOLDOUT141/160;
-query_swap HOLDOUT96/160.
Thus query-identity substitution was much more disruptive than value-assignment substitution while
the recipient reader stayed fixed. Query- and value-swap donors can share the same target in this
two-entity fixture,so the difference is inconsistent with a simple target-value-only explanation.
It still does not uniquely identify an entity/query code,binding algorithm or training-time core role.

C255 is the endpoint of this two-entity frozen-intervention chain. These correlated interventions
use one repeatedly inspected authored fixture and recombine jointly trained features before
LayerNorm. They are not independent samples or a general capability benchmark.

Accepted artifacts:
-contrasts.json:ecc69baf18f5824ad3c94be836ba55b2f05ace64f5b38d42825dbce37c48f228
-diagnostics.json:111b4c2d98087f0d7e90cddda83ba53892eb74961cb4b0a564392eb36ccc51a4
-head-outputs.pt:77a4e8a54e610a40cd7be3965e863d48e4f5058efebbc49637aa40d043cf1241
-validation-summary.json:69394982329cd77f7ae0d9739f7fe97e898444e331b697fa507287120be99b63
-value-plan.json:e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a.
Acceptance:docs/experiment-ledger-addendum-c255-c256.md.
Acceptance/base commit:0455a2aed54c54fd1dbc6008cf6f7b80f0521aae.

The two earlier C255 attempts remain INVALID and are preserved in
docs/experiment-ledger-addendum-c255-execution-recovery.md:
1)70ca4c4c... stopped in own test07 before regression/science;
2)275754bf... passed own24+3289 but stopped at model1 on an over-strict bitwise masked-activation guard.
Neither contributes scientific evidence. Their repairs only aligned numerical replay checks to the
already registered TOL=1e-9/exact-argmax contract.

## Preserved earlier boundaries

C254 query/order swaps:145/160 self,141/160 order,96/160 query HOLDOUT;diagnostic only.
C253 residual removal:145/160 self,107/160 pre-residual,117/160 reader-only HOLDOUT;diagnostic only.
C252 aligned pre-core query/memory + post-core residual:4/5 whole-seed joint passes,not5/5;
ACCEPTED VALID NEGATIVE.
C251 pre-core memory/post-core query:2/5. C250 Full post-core reader2/5,GRU reader4/5,EOS controls0/5.
C249 frozen reader dependency diagnostic. C248 bounded reader transfer but failed its all-seed gate.
C247/C246/C244/C242/C241/C239 remain accepted negatives;C245/C243/C240/C237/C235 remain diagnostics;
C238 seen-prompt fit only. C232 bounded byte learning and C233 competitive GRU-only result are not
general language/core-superiority claims. Preserve all accepted evidence and recovery records.

## Active C256 — fresh three-entity task shift

Experiment:C256-v5b-three-entity-task-shift.
Stage:V5-B-THREE-ENTITY-TASK-SHIFT.
One question:does the C252 aligned pre-core reader reproduce bounded binding/recombination behavior
on a fresh three-entity bilingual assignment task with new seeds,relative to an equal-parameter
EOS-only Full adapter?

This is new training,not a frozen diagnostic and not a retry of failed C252 seed250002.
No C252/C255 learned checkpoint or saved activation initializes C256.

Task:
-entities EN:a,b,c;JA:甲,乙,丙;
-values0..3;three distinct values per assignment;
-all24 ordered assignments split into fixed balanced12 TRAIN/12 HOLDOUT assignments;
-each entity-position/value marginal is exactly3/12 on each side;
-exact assignments never cross the split;
-2 languages x2 fact orders x3 queries for every assignment;
-TRAIN144 rows,HOLDOUT144 rows;
-normal/evidence_blind/query_blind views;
-target is the digit assigned to the queried entity.
Task SHA256:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
All prompts fit the existing48-slot BOS+bytes+EOS+PAD byte contract.

Fresh seeds256001..256005.
For each seed instantiate one fresh protected Full V5-B backbone and deep-copy the exact state into:
1)aligned_precore_read=actual C252.AlignedPrecoreReadout
   (pre-core EOS query,pre-core K/V,reader residual added to actual post-core EOS);
2)eos_adapter=actual C248 Full equal-parameter EOS-only16->24->16 residual adapter.
Both add768 parameters;both total14256. Same backbone/data/batches/optimizer/budget per seed.
Parameter count is matched;FLOPs and architecture are not.

Training:
800 updates/model,batch48;10 models=8000 updates/384000 presentations.
AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0;clip1.
CPU float64,threads2,deterministic algorithms.
Every3 steps use one seed+epoch randperm of all144 TRAIN rows and its three disjoint48-row blocks.
Both arms use identical block indices. No HOLDOUT optimization,early stop,seed replacement,
checkpoint selection,extra steps or result-driven threshold change.

Per language/split metrics:
-normal accuracy;
-answer NLL;
-order_pair_accuracy over36 same-assignment/query order pairs;
-query_triplet_accuracy over24 same-assignment/order three-query groups;
-evidence/query-blind accuracies and drops.

Fixed cell criteria:
accuracy>=0.90;order_pair>=0.80;query_triplet>=0.80;
evidence_drop>=0.35;query_drop>=0.35.

PRIMARY PASS iff all five aligned_precore_read seeds pass BOTH languages on BOTH TRAIN/HOLDOUT.
EOS adapter is reported independently and cannot rescue/fail the primary status.
A complete valid miss is ACCEPTED VALID NEGATIVE.

Scientific workload:
per model800 training forwards/38400 rows +6 final/864 +6 strict replay/864.
Total8120 full-model forwards/401280 rows;120 final/replay evaluation forwards.
One10-state bundle;checkpoint writes1. Require common initial backbone,changed full/head weights,
strict state load,prediction replay,metric and raw-logit replay<=1e-9. Network calls0.

Protection:382 source pins/623 protected inputs;explicit deciding dependency union32;OWN6.
Own tests24;modules141;loaded3314/focused3313;only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Artifacts:task-plan.json,dataset.json,trained-models.pt,measurements.json,validation-summary.json.
Bundle schema fold-c256-three-entity-v1.
Manifest SHA256:31b433a189aee26a02d11d1571300b216f21ceb205d3696f90fe95d02bb20a7c.
Design:docs/v5b-three-entity-task-shift-v0.1.md.
Registration:docs/experiment-ledger-addendum-c256-preregistration.md.
Preregistration/review HEAD:380e2d9c1939d52e3f619e9160c1e44a1bdca2cb.
Use tools/invoke_active.ps1 with the final activation HEAD,not the review HEAD.

## C256 post-authoring review

post_authoring_review = PASS
Review HEAD:380e2d9c1939d52e3f619e9160c1e44a1bdca2cb.
All six OWN files were re-fetched after authoring. Reviewed Git blobs:
-benchmark:1f91f80d2ea74406fe236fd99fb1c60e2e5a2ae0
-tests:efc9fe2d805eed7b28454ab4ad77a38e31d594d9
-runner:46bbd0365002aecc1248f74887c7b3f0d205d744
-launcher:f6e3069c3d9526c3bc012dadf6d1e5f609b7fdae
-design:11e6cfbd3c4c4f8dfe08fe48975f0c98da3b2887
-preregistration:5dcb2583634fa2b1af78fa9566d7ad44f3633834.
Acceptance-base-to-review comparison contains exactly these six additions and no accepted-file edit.

Remote-byte review verified:
-24 unique own test definitions;
-no placeholder/stale C257 activation;
-manifest/task hashes and all fixed workload/protection/test-count constants;
-three embedded runner Python blocks;
-C255 authoritative parent run path;
-ACTIVE-C256 launcher guard and parser-before-publication ordering;
-logit retention for checkpoint replay;
-no unbound bare historical c### module alias (c252 occurrences are bound local/attribute names);
-direct dependency count32 and inherited source/protection arithmetic.

Independent reviewer calculations verified:
-exact task SHA256 and144/144 row counts;
-12/12 disjoint assignment split;
-every position/value marginal3/12 on both sides;
-max rendered prompt length22 bytes;
-all three-step sampler epochs cover all144 TRAIN rows exactly once;
-800 steps produce38400 training presentations/model;
-manifest SHA256 matches the registered constant.

During authoring review two issues were fixed BEFORE activation:
1)checkpoint replay initially retained token tensors instead of logits;fixed to retain final logits;
2)one-step gradient smoke initially expected query/hidden gradients despite zero output-projection
 initialization;fixed to require the output projection plus backbone-core gradient that is actually
 reachable on the first backward.
A later replay audit also made final metric comparison explicitly TOL-based.

The reviewer environment cannot clone github.com because DNS resolution fails and has no PowerShell.
Therefore NOT executed here:exact committed own24 inside the complete repository import graph,
full3313 historical regression,Windows ParseFile,user-local C255 artifact precheck,or actual
10-model C256 training. None is reported PASS. The authoritative runner performs Python syntax
preflight,own24,3313 regression and parent/task checks before any scientific training and stops
without accepting science on any failure.

Only this handoff changes after review HEAD. Re-read final branch HEAD before issuing ExpectedHead.
Do not advance the branch during the user's formal C256 run.

## Stop and scope

Gate F NOT PASSED. Preserve accepted source/tests/logs and tools/run_c167.ps1.
No paid API,external corpus,model expansion,production adoption,cleanup/history rewrite or CI addition.
C256 order:dispatcher/launcher ParseFile ->Python syntax+parent/task precheck ->own24 ->3313 regression
->10-model fixed-budget training ->checkpoint replay ->postcheck ->log publication.
Integrity faults retry same C256;valid scientific FAIL is accepted negative and does not trigger
seed/budget/threshold rescue. Transport-only log failure is repaired without retraining.
Judge C256 before C257.
