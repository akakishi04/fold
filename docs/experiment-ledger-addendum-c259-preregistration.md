# C259 preregistration — paired order-coverage training

Experiment:C259-v5b-paired-order-coverage-training.
Stage:V5-B-PAIRED-ORDER-COVERAGE-TRAINING.
C258 ACCEPTED PASS(diagnostic only);C257 ACCEPTED VALID NEGATIVE;C256 bounded PASS remains.
Gate E PASSED;Gate F NOT PASSED. C260 NOT REGISTERED.

## One scientific question

At fixed architecture,initial state and800-update budget,does six-order training yield reliable
held-assignment performance across all six orders,relative to a paired two-order aligned reader?
This changes the training order policy,not the architecture. It follows the single C258 diagnostic;
there is no further saved-answer intervention chain and no attempt to rescue a failed C257 state.

## Accepted parent

Acceptance/base commit:db8fe078766353e3a3d8217eb6b595c22f10cfcd.
Acceptance:docs/experiment-ledger-addendum-c258-c259.md.
C258 execution:e31d4c28a00bc11fb5db3c2ba1b093e4eae15538.
Published log:62aac236dc90643dc57b3ed51855f79aeb22f1cd.
Publisher log SHA256:5a7ad7fff7846a76e43eec75542b8327de3a4ca42094e2c68d3e0d143dd32c64.
Summary SHA256:f6ccc7dc1b8c60c1f1e6bc7587bd9853eeb6bea6e1f7a010fd99de068bbd0ecc.
Path:runs/c258-v5b-middle-slot-93386fd77e3749bab4122685ff57720d/summary.json.

Required artifacts:
-audit-plan.json:a4f2cad192bd56dd73d867caf8453084cdd85e8e0f10f9d2496bfaa4a6c08aef.
-query-position-cells.json:d4bb64ac620e235b389447b52b4dea88b69466e4f77a3db8e363a0dfa330dea5.
-row-attribution.json:b94b0224805512c049d3a6dfcee23c682dc700c33df705a750a4f71ea8475e85.
-signature-summary.json:e40bfcd11890866e1f02e77b662151a2d414df35b6c7d12c357afd9fa93b1644.
-validation-summary.json:17d130b1b26545457a9419727548507d480aead01b02c8b6100d251969d95620.

Actual C258.validate_result must accept the diagnostic PASS with capability/causal claims false.
The child load_parent verifies summary SHA,all five artifact SHA/size pairs,actual audit-plan equality
with C258.manifest,and validation-summary equality/8640 attributed rows. These are diagnostic
provenance,not initialization weights or training inputs. No parent learned bundle is loaded.
The child's precheck calls this loader before inherited source/input protection checks.

## Model and paired initialization

Fresh seeds259001..259005. For each seed create one actual C231 Full backbone and wrap it with
actual C256.make_model(...,aligned_precore_read,seed,C252,C248),i.e.C252.AlignedPrecoreReadout.
Deep-copy the same complete initialized wrapper into two_order and six_order. Both14256 parameters,
including768 reader parameters;width16,max48 byte slots. Pre-core query and K/V;post-core EOS residual.
No EOS-adapter arm here:the controlled comparator is the SAME aligned-reader architecture.
No accepted checkpoint,activation,optimizer state or failed-seed selection initializes training.
Require matched initial full/backbone fingerprints,changed full/backbone/head final fingerprints,
and matched underlying logical-batch digests. Set fit RNG to seed+259000 separately for each arm.

## Fixed data and one changed policy

Generate the exact C256 dataset with actual C256.dataset:
SHA256 ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
TRAIN/HOLDOUT each144 original rows,12 distinct value assignments,2 languages,2 orders,3 queries.
The assignment split and its balanced entity/value marginals are unchanged;HOLDOUT is never optimized.
Generate the exact additional four orders with actual C257.novel_dataset:
SHA256 9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Additional rows288/split. All six together432/split,216/language.

Order list:012,210,021,102,120,201. Order pairs:(012,210),(021,102),(120,201).
For zero-based step s,epoch=s//3 and block=s%3. Draw one randperm(144) from seed+256000+epoch;
use its48-row block. Both arms receive the SAME assignment/language/query/target logical rows.
A row's original order bit is0 or1. In two_order use pair0 always. In six_order use pair(epoch%3).
Render ORDERS[2*pair+original_order_bit] directly. Never canonicalize it back before the model.
The renderer changes only fact order;names,values,query-at-end,delimiters and byte encoding remain.
No target/permutation/entity metadata enters the model beyond visible bytes;task IDs are all0.

Every complete3-step epoch visits144 logical rows once:each base question twice.
Every complete9-step cycle gives the six_order arm each of its72 base questions in all6 orders once.
Stop after exactly800 steps,including its preregistered incomplete final cycle/epoch;do not extend
for equal per-permutation counts. Pair-update counts:two_order[800,0,0];six_order[267,267,266].
The same logical row schedule is preserved through the tail. Stored training tables are3x144x48
TRAIN-only token IDs plus144 targets. The two_order arm indexes table0 only.

## Optimizer and workload

800 updates/model,batch48,ten models=8000 updates/384000 training presentations.
AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0;gradient clip1.
CPU float64,threads2,deterministic algorithms. No early stopping,checkpoint selection,extra steps,
seed replacement,model-size changes or result-driven threshold change.

Each final evaluation uses original6 forwards/864 rows plus extra6/1728=12/2592.
Each strict-checkpoint replay repeats12/2592. Training+final:812 forwards/40992 rows per model.
Including replay:824 forwards/43584 rows. Total8240 forwards/435840 row presentations;
240 evaluation/replay forwards. One newly trained10-state bundle write/load;ten strict state loads.
No network calls. Test fixtures and source/artifact hashing are additional work,not scientific samples.

## Fixed gate and paired comparison

Score final weights only. Use actual C256.metrics/cell_pass for original orders and actual
C257.new_metrics/new_cell_pass/six_order_metrics for the additional four and all-six consistency.
For each seed,both languages and both assignment splits:
-original C256 cells:accuracy>=0.90,order_pair>=0.80,query_triplet>=0.80,evidence_drop>=0.35,query_drop>=0.35;
-EACH additional order separately:accuracy>=0.90,query_triplet>=0.80,evidence_drop>=0.35,query_drop>=0.35;
-all-six consistency>=0.80,requiring all six versions of an assignment/query to be correct.

Additional order cells have36 rows/12 query triplets,minima33/36 and10/12.
All-six consistency has36 groups/language/split,minimum29/36. Original groups remain as in C256.
C259 primary PASS iff all five six_order seeds satisfy all criteria. A valid miss is ACCEPTED VALID
NEGATIVE. Control outcomes do not rescue or fail treatment status.
Report all original/extra cells,all-six scores,and ten paired HOLDOUT language comparisons of
all-order accuracy(/216) and six-order consistency(/36),treatment minus control.
Both arms passing is possible;primary PASS alone does not establish an order-policy advantage.
Comparative direction is descriptive across the five pairs;no significance or population guarantee.

## Persistence and integrity

Six ignored artifacts plus summary.json:
coverage-plan.json,dataset.json,trained-models.pt,evaluations.pt,measurements.json,validation-summary.json.
Model bundle schema fold-c259-order-coverage-models-v1:identities in seed/arm order and ten final states.
Evaluation schema fold-c259-order-coverage-eval-v1:ten records with initial/final fingerprints,
fit/schedule counters,final original/extra logits,and strict-replay results. These logits describe
final states,not initial states or intermediate checkpoints.
Strict reload must preserve fingerprint,exact argmax,and raw-logit replay within1e-9 for every view.
Postcheck hashes all artifacts,reads saved evaluation logits,and reconstructs all metrics/gates and
comparisons with no further model forward or learned-bundle load. Saved JSON must match exactly.
C256 raw logits were not persisted,but C259's own final raw outputs are persisted explicitly.

## Protection and authoring quality

Inherit C258394 source pins/647 inputs;add parent summary+five artifacts and OWN6:
400 source pins/659 protected inputs. Direct deciding dependency union35 comprises the five C231
LM sources,C230..C258 helpers,and C259. Lazy deciding imports are included. Accepted sources remain.
OWN6:benchmark,own tests,runner,launcher,this preregistration,and design:
-fold_lm/v05_benchmarks/model_c259_order_coverage_training.py
-tests_lm/test_v05_c259_order_coverage_training.py
-tools/run_c259.ps1
-tools/invoke_c259.ps1
-docs/experiment-ledger-addendum-c259-preregistration.md
-docs/v5b-order-coverage-training-v0.1.md

Own24;modules144;loaded3382/focused3381. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb.
Before activation re-fetch committed files,match tested complete file blobs,execute exact own24,
compile/import,check free globals,hashes,parent signatures,counts,source coverage,call order and CLI.
Own tests explicitly use synthetic Tiny/lookup-logit/Base/Orders/Audit fixtures;test09 exercises
actual800-step train_one and strict replay on Tiny,not the production C252 model. Test20's ten-model
run substitutes synthetic training records to test orchestration/persistence. No capability evidence.
Historical suite fixture counts are not execution of3381 tests. Record limitations in the handoff.

## Interpretation and stop

For six_order,all evaluated fact orders were TRAIN-visible. A PASS is held-assignment performance
under trained order coverage,NOT unseen-order transfer. The fixed data family was already inspected
in C256-C258;fresh seeds do not turn it into a new independent benchmark. Coverage and its specified
cycling policy are one training intervention;do not uniquely attribute internal mechanism or claim
FOLD-core superiority,general language,production adoption or Gate F.
No further learning after results. Integrity faults:INVALID / RETRY SAME C259. Valid criterion miss:
accept negative,do not retune. Log-only transport failure:repair publication without retraining.
Use active dispatcher;parse dispatcher/launcher/runner before execution. No paid API,external corpus,
accepted-file cleanup,history rewrite or CI change. Judge C259 before C260.
