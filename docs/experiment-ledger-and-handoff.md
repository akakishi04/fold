# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C255 ACCEPTED PASS (diagnostic integrity only). C256 ACTIVE / INVALID ATTEMPT RECOVERY. C257 NOT REGISTERED.**
C256 is the unique ACTIVE experiment:V5-B fresh three-entity bilingual task-shift training.
The first attempt stopped in parent/task precheck before own tests, regression or training.
Its manifest fingerprint was registered incorrectly. That error and a separately reproduced
formatting-sensitive launcher test are repaired; post-repair review PASS within the scope below.
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
Manifest SHA256:43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1.
Design:docs/v5b-three-entity-task-shift-v0.1.md.
Registration:docs/experiment-ledger-addendum-c256-preregistration.md.
Original registration HEAD:380e2d9c1939d52e3f619e9160c1e44a1bdca2cb.
Current recovery review HEAD:4afbfbe60417d228b6268b2652d536f3b67206f6.
Use tools/invoke_active.ps1 with the final recovery HEAD,not the original activation or review HEAD.

## C256 execution recovery and post-repair review

Failed execution HEAD:1029158a60d40df24f599fb719411dbde2ffec06.
Invalid log commit:2dc541041c772d5b9a449bd247862ad906a9b5c8.
Invalid log SHA256:5e774f0043a8f4661bbda08fe1ccaa8f728b1e10315947677d7ee6a40f62dce8.
The1008-byte log ends at ValueError: counts/manifest during parent/task precheck.
Python syntax passed;own tests/regression/training did not run. The precheck lies before the
runner's experiment try/finally,so this log has no POSTCHECK/run_execution_valid line.
Do not invent such a line or a C256 scientific score.

The immutable failed-run benchmark's actual manifest digest is43948ceb...ae53b1,not the recorded
31b433a1...bb20a7c. Complete source bytes were matched to original blob
1f91f80d2ea74406fe236fd99fb1c60e2e5a2ae0 before computing this. The previous review statement that
manifest SHA matched the constant was incorrect;it is superseded by this executed review.
The log's combined check did not print the actual counts. The hash condition is independently
false;the unchanged382/623 count requirements remain mandatory and are now logged separately.

The original24 test methods were also actually exercised in the limited review environment:
22 PASS,one manifest-hash failure and one launcher-order error. Test24 required the literal
'$failure = $null',while the valid launcher used '$failure=$null'. This further authoring defect
was repaired before another user retry.

Minimal changes:
-correct the fixed manifest fingerprint,not the manifest payload or hash-validation policy;
-add validate_registration to print actual counts/hash and reject count/hash mismatches separately;
-expand existing test01 with wrong-count/wrong-hash rejection cases;
-make test24 whitespace-independent while retaining parser-before-execution ordering;
-correct the C256 preregistration fingerprint and document the invalid attempt.

Manifest JSON and dataset JSON remain byte-identical. AST comparison confirms all existing
benchmark functions except precheck are unchanged;only validate_registration is added.
No model,seed,data,sampler,optimizer,steps,metric,threshold,tolerance,workload or accepted file changes.
Own24/focused3313 counts and the sole historical exclusion are unchanged. Runner/launcher unchanged.

Source repair commit:1a03d784c97d8190cd9c527b3aa498ea3b4027a1.
Test repair commit:d05ed16a733c693e8cb14783d40c47f48af55bae.
Preregistration correction/review HEAD:4afbfbe60417d228b6268b2652d536f3b67206f6.
Recovery record:docs/experiment-ledger-addendum-c256-execution-recovery.md.

post_repair_review = PASS
Review scope:complete C256 source/test/script byte checks and executed limited-dependency own tests;
NOT a complete historical checkout or authoritative Windows result.

Re-fetched source/test identities match the locally executed complete files:
-benchmark:56968388f643d8929f8911d93dfc4301941bd924;
-tests:a3e1c67d7f0d625cbc30f4e27936268adaef426e;
-unchanged runner:46bbd0365002aecc1248f74887c7b3f0d205d744;
-unchanged launcher:f6e3069c3d9526c3bc012dadf6d1e5f609b7fdae.

Executed after repair:compile/import,zero unresolved globals,manifest and dataset regeneration,
negative registration cases,unchanged scientific-function ASTs,and all24 own test methods.
24/24 PASS in0.836s before publication and0.787s after remote readback/blob matching.
The run includes initialization,capacity,gradients,state-preserving evaluation,checkpoint-logit
replay,metrics/gates,and the three embedded Python blocks/CLI argument checks.

Important scope:review-only b.context was replaced with namespaces using retrieved C231 factory,
language_task,modules,C248 and C252 computational source excerpts. These include the actual
GRU/core/reader computations,not a toy linear replacement. The committed test file retains the
real b.context;the full historical import graph and user-local parent artifact checks were not
executed in the review. The constructed3314-ID test validates filtering only,not3313 historical tests.
Reviewer:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. GitHub DNS failed in the container;PowerShell absent.
Still pending and required on the user's environment:Windows ParseFile,complete parent/source
precheck,exact own tests through real repository imports,full3313 regression,and formal10-model
training. None of those pending checks is reported as authoritative PASS.

Only recovery/handoff documentation follows the review. Re-read the final branch HEAD before
returning ExpectedHead. Do not advance this branch during the user's formal C256 retry.

## Stop and scope

Gate F NOT PASSED. Preserve accepted source/tests/logs and tools/run_c167.ps1.
No paid API,external corpus,model expansion,production adoption,cleanup/history rewrite or CI addition.
C256 order:dispatcher/launcher ParseFile ->Python syntax+parent/task precheck ->own24 ->3313 regression
->10-model fixed-budget training ->checkpoint replay ->postcheck ->log publication.
Integrity faults retry same C256;valid scientific FAIL is accepted negative and does not trigger
seed/budget/threshold rescue. Transport-only log failure is repaired without retraining.
Judge C256 before C257.
