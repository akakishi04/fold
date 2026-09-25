# C260 preregistration — paired training-time core ablation

Experiment:C260-v5b-paired-core-free-training.
Stage:V5-B-PAIRED-CORE-FREE-TRAINING.
C259 ACCEPTED VALID NEGATIVE;C258 diagnostic PASS;C257 valid negative;C256 bounded PASS remain.
Gate E PASSED;Gate F NOT PASSED. C261 NOT REGISTERED.

## One question

Can a core-free pre-core residual reader meet the bounded recombination criteria under six-order
training,relative to a fresh Full aligned reader with identical surviving initial parameters,
logical batches and800-update budget? This is a training-time structural ablation,not a frozen
inference intervention or a production architecture change. Do not assume the core caused C259's miss.

## Accepted parent and actual loader

Acceptance/base:e3311dd21eb5b7235e02dc0d6b59352086691fcb.
Acceptance:docs/experiment-ledger-addendum-c259-c260.md.
C259 execution:78f0811c390d11256e748b1f955f505ad803de49.
Published log:9f7abcc2ea2d88b78a2348e693b2850874f56cb6.
Publisher SHA256:85d7d49b6db16a3b06492b94b686de796dd8866e397798e489555612b2b96a43.
Summary SHA256:e005a223fd138ef43e6a3a4664c31a7f2f64482f8325252ba11ad2fdf2562ab1.
Path:runs/c259-v5b-order-coverage-7042b90d1ed54cc0858291e661d329e8/summary.json.

Required artifacts:
-coverage-plan.json:2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56.
-evaluations.pt:25282bfeace30ec5fd9be8e46c0aa7f8b3e243a8d0fa2606d656dae5d462e01d.
-measurements.json:b833dbdd66373396ba3345385bd92e48a002b1377a0993a217d34ae0d7898862.
-trained-models.pt:372fab6bbff0c7160c9b89ca8f7147db0f923ef1205f2799466a85f9b61ef3a7.
-validation-summary.json:117d4a99611e1aab0109f67e3d4d3012855b22d75d336833557db769519a8b16.

load_parent verifies the summary hash,then calls actual C259.verify_artifacts(parent_dir,PARENT_EXECUTION).
Require status FAIL,seed_pass_counts two_order2/six_order4,ten measurement records and exact artifact
identities. The parent validator reconstructs saved final metrics and checks hashes;it does not
initialize C260 from the learned states. Parent artifacts are provenance only. precheck calls this
loader. Never require the scientifically negative parent to have capability PASS.

## Arms and initialization

Fresh seeds260001..260005,all included. Build one actual C252.AlignedPrecoreReadout using C256.make_model
and the protected C231 factory for each seed. Clone the Full template without modifying accepted code.
with_core:unchanged actual C252 forward,14256 stored/trainable parameters.
without_core:CoreFreeReadout copies the template backbone and reader,sets only the copied backbone.core
to None,and directly uses its encoder,reader,readout normalization and decoder.10928 parameters;
3328 core parameters are removed,not retained as inactive capacity padding.

Both share identical surviving initial state tensors,checked with a fingerprint excluding only
backbone.core.*. Entire state dictionaries and initial logits need NOT be equal,as architectures differ.
There is no shared tensor storage or accepted checkpoint initialization. Full reference is retained.
Parameter counts are not claims that every parameter receives a nonzero gradient on every task.

The core-free forward validates the same NEXT-only48-slot input,encodes actual masked causal GRU
states,and takes pre-core EOS as both query input and residual base. It applies the copied reader's
query/key maps,divides attention scores by4,excludes PAD,reads the weighted pre-core memory,and decodes
LayerNorm(pre_core_EOS + reader.output(memory)). The Full residual base is actual post-core EOS.
This jointly removes the state-update path and changes the residual base to the state before it;
do not reinterpret it as an isolated one-weight change or proof of one internal algorithm.
The core-free path never calls backbone.forward or a core. The Full path retains both original task
routes,even though only NEXT is selected. Two internal steps x two evaluated routes = four core
calls per Full model forward. Core calls are counted independently of wrapper forwards.

## Fixed data, training and sampling

Both arms use the C259 SIX-order training policy. Actual C256.dataset and C257.novel_dataset hashes:
original ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b;
extra 9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Same balanced12 TRAIN/12 HOLDOUT distinct-value assignments,English/Japanese identifiers,three queries,
all6 orders,query at end,delimiters,48-slot BOS/bytes/EOS/PAD contract. No target/oracle metadata input.
Original144 plus extra288 rows per split;432 total,216 per language. HOLDOUT never enters optimization.

Actual C259.training_tables builds TRAIN-only3x144x48 tokens and144 targets.
For step s,epoch=s//3,block=s%3. randperm144 uses seed+256000+epoch;take the block of48;
pair=epoch%3 for BOTH arms. Order pairs are012/210,021/102,120/201,selected with the original row bit.
Every complete9 steps covers all6 orders once for each of72 base questions.800-step tail is fixed:
pair updates267/267/266. Matched logical-batch digest and common initial fingerprint are mandatory.

800 updates/model,batch48;AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0;global gradient clip1.
CPU float64,threads2,deterministic algorithms. Fit RNG seed+259000 resets per arm.
No extra steps,early stop,checkpoint/seed selection,changed split or gate relaxation.
Removal of parameters also changes optimizer state and the global-clipping gradient vector;
these are consequences of the structural ablation,not independently isolated interventions.
Neither parameter count,FLOPs nor wall-clock budget is matched. No efficiency superiority claim.

## Fixed gate and reporting

Use actual C256.metrics/cell_pass for original orders and actual C257.new_metrics/new_cell_pass/
six_order_metrics for the four additional orders and six-order consistency.
Each seed must pass both languages and both assignment splits:
-original accuracy>=.90,order_pair>=.80,query_triplet>=.80,evidence_drop>=.35,query_drop>=.35;
-each additional order separately accuracy>=.90,query_triplet>=.80,evidence/query drops>=.35;
-all-six-order consistency>=.80.
Extra cells36 answers/12 query triplets require33/36 and10/12;six-order groups require29/36.
C260 primary PASS iff ALL FIVE without_core seeds pass. A valid miss is ACCEPTED VALID NEGATIVE.
with_core gates are separate and cannot rescue/fail the primary gate. Both branches may pass or fail.
Report all cells,seed outcomes,and ten HOLDOUT paired language comparisons of all-order accuracy
and all-six consistency,without_core minus with_core. Primary PASS alone is not comparative superiority.
No significance or initialization-population guarantee from these five pairs.

## Workload and persistence

Ten models:8000 updates/384000 training presentations.
Per model:training+final812 forwards/40992 rows;strict replay12/2592.
Total8240 model forwards/435840 rows;240 final/replay evaluation forwards.
Full core calls3248 during training/final plus48 replay per model;five Full models total16480.
Core-free arm core calls0,NOT zero model inference. No external network calls.
One new10-state bundle write/load;ten strict state loads. Construction of fresh wrappers for replay
is not new training. Parent saved-output recomputation and historical tests are separate work.

Six ignored artifacts plus summary.json:core-plan.json,dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json.
Model schema fold-c260-core-models-v1:ten states in seed/arm order;core-free states omit core keys.
Evaluation schema fold-c260-core-eval-v1:final original/extra logits,initial/common/final fingerprints,
fit metadata,forward/core counters and replay results. No initial/intermediate logits masquerade as final.
Actual C259.replay_one strict-loads each appropriate architecture,checks final fingerprint,all-view
logit error<=1e-9 and exact argmax,then records12 forwards/2592 rows. C260 additionally counts core calls.
Postcheck hashes all artifacts and reconstructs metrics/gates/comparisons from persisted final logits,
without constructing models or loading learned weights again. JSON values must match exactly.

## Protection and authoring

Inherit400 source pins/659 protected inputs;add parent summary+SIX artifacts and OWN6:
406 source pins/672 inputs. Direct deciding dependency union36 includes five C231 LM sources,
C230..C259 helpers and C260. No accepted source/test/script or shared dispatcher changes.
OWN6:
-fold_lm/v05_benchmarks/model_c260_core_free_training.py
-tests_lm/test_v05_c260_core_free_training.py
-tools/run_c260.ps1
-tools/invoke_c260.ps1
-docs/experiment-ledger-addendum-c260-preregistration.md
-docs/v5b-core-free-training-v0.1.md
Own24;modules145;loaded3406/focused3405. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae.

Before activation re-fetch all six committed files. Match tested code/script bytes to returned Git
blob identities;execute exact own24,compile/import,global-name audit,hashes,counts,CLI/parser ordering,
parent signatures and path semantics. Test fixtures explicitly replace the Full core and parent
adapters;they are not production learned-model evidence. Test11 executes the real new800-step
core-free training loop on a synthetic template;test19 substitutes training to test ten-state
orchestration/persistence. The constructed3406-ID fixture validates filtering,not3405 historical tests.
Record actual checks and pending authoritative checks in the handoff. Do not issue a launcher before
committed-byte post-authoring review PASS. Windows ParseFile remains mandatory on the user's runtime.

## Scope and stop

All fact orders are training-visible in both arms;no unseen-order claim. Repeatedly inspected authored
tasks and fresh seeds are not independent general benchmarks. Neither result authorizes removal of
FOLD's core from the design,Gate F promotion,production adoption or a general superiority conclusion.
Integrity faults:INVALID / RETRY SAME C260. Valid miss:accept negative without tuning.
Operational skips precede logging. Log-only publication failure:repair without retraining.
No paid API,external corpus,model expansion,accepted-file cleanup,history rewrite or CI changes.
Judge C260 before C261.
