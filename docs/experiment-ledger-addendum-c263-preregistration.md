# C263 preregistration — learning rate by minibatch chronology

Experiment:C263-v5b-learning-rate-order. Stage:V5-B-LEARNING-RATE-ORDER.
C262 ACCEPTED VALID NEGATIVE. Gate E PASSED; Gate F NOT PASSED. C264 NOT REGISTERED.

## One question and fixed contrast

Does lowering AdamW learning rate from0.005 to0.001 reduce sensitivity to forward versus
reverse minibatch chronology while retaining the fixed task criteria at800 updates?
This is one predefined2x2 experiment,not a learning-rate sweep. Both chronologies remain.
The smaller rate is a hypothesis,not a promised improvement; slower learning or underfitting
is a valid negative and must not trigger more steps or a replacement rate within C263.

## Accepted parent

Acceptance/base:9edbef91d9a5bc81427b93003bae9127032643be.
Acceptance:docs/experiment-ledger-addendum-c262-c263.md.
Execution:28030ad02e69a9ae7236fca7f7e84a61f3c89c46.
Published log:4dc8fec24578efa5f7d8abfea17c56be2dc23673.
Publisher log SHA256:9dc5f6850866548f8f1e3a6681e2aab58069c36526d3355321ae814c05d502f7.
Summary SHA256:9cda47219d6e376516044d5807e546a8c13110f584f139bda2a3da8800b2d93d.
Summary:runs/c262-v5b-batch-order-b955446fc91846aa9fea770cd36b9276/summary.json.

Required artifact SHA256:
-batch-plan.json:2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c;
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;
-evaluations.pt:f360dccf8b5523b27755e87734b0ae1c1b4ab8628b4e9c3fb32ada20f102db2f;
-measurements.json:13ffc5ce99372df17914f5a8cc07e03ba63e74cd091a24e650db62c6273e5e8d;
-trained-models.pt:84ce31fe704c193a9a5f17a0e9023b9f6d4dc84fd25badafd118a95738595713;
-validation-summary.json:d2843f6443c759795f50f81e68fc35cf742c28f3657716812207b756aab4c864.

load_parent checks the summary hash then calls actual C262.verify_artifacts(parent_dir,
PARENT_EXECUTION). That function replays saved final logits,metrics and exposure schedules;
it does not rerun parent model inference. Require status FAIL,forward_blocks0/reverse_blocks2,
ten parent measurement records and all six exact artifact identities. precheck invokes
load_parent. No parent learned weights initialize C263; parent artifacts are provenance.

## Four arms and pairing

Seeds263001..263005,all fresh,all included. For each,create one actual C252 Full aligned
reader through C256.make_model and C231 factory,then deep-copy its complete initial state
into standard_forward,standard_reverse,lower_forward,lower_reverse in this order.
Both standard arms use0.005;both lower arms0.001. All models14256 parameters.
No tensor sharing,architecture changes,core-free variant,accepted checkpoint reuse or
failed-seed rescue. The same-order rate pair sees identical batches at each update.
All four have identical exact final exposure counts;forward/reverse chronology differs.

Keep AdamW betas0.9/0.999,eps1e-8,weight_decay0,global gradient clip1,batch48,800 updates.
Reset fit RNG to seed+259000 for each arm. CPU float64,threads2,deterministic algorithms.
Learning rate is the only changed optimizer setting. Gradients and optimizer states may
subsequently diverge as consequences of that change. No early stopping,checkpoint selection,
extra steps,seed replacement,rate schedule or post-result change of criteria.

## Data and chronology

Use the DISTINCT-value C256 assignment partition and C257 all-six-order rendering,not
C261 repeated-value rows. Original dataset SHA256:
ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
Extra dataset SHA256:
9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Each original split has144 rows;extra288;total432,216 per language. Twelve TRAIN and
12 HOLDOUT assignments,three distinct values0..3,three queries,EN/JA identifiers and
48-slot byte encoding remain. Actual C259.training_tables uses TRAIN only; HOLDOUT
never enters optimization. No target,entity-index or permutation metadata is model input.

Same C262 chronology rule but fresh seeds:epoch=step//3,offset=step%3;
randperm144(seed+256000+epoch);48-row blocks;fact-order pair=epoch%3.
Complete epochs use blocks0,1,2 versus2,1,0. The last two steps798/799 use0,1 versus1,0;
block2 is absent in both. Example order inside each minibatch is unchanged. Fact-order
pair updates267/267/266. No extra step is added to complete the last epoch.
Save and recompute chronology SHA256,432 exact prompt exposure counts and their SHA256.
Within every four-model group,initial fingerprints and exposures match. Rate pairs with
the same order have identical chronology hashes;forward/reverse hashes must differ.
This changes when complete minibatches are processed,not how facts inside a prompt are ordered.

## Capability gate versus comparative evidence

Use actual C260.score,which calls the protected C256/C257 scoring functions. For each
language and both TRAIN/HOLDOUT assignment splits:
-original accuracy>=.90,order_pair>=.80,query_triplet>=.80,evidence_drop>=.35,query_drop>=.35;
-EACH extra order accuracy>=.90,query_triplet>=.80,evidence/query drops>=.35;
-all-six-order consistency>=.80.
Extra36-answer/12-triplet cells require33/36 and10/12; six-order groups require29/36.
No metric or threshold is changed from the prior distinct-value task.

C263 primary capability PASS requires all TEN lower-rate states to pass:both chronologies,
all five seeds. Standard-rate gates and each of four arm pass counts are separate.
This is a new treatment gate,not retrospective relaxation of C262's joint ten-state gate.
A standard-rate miss cannot fail or rescue the lower-rate capability result. A complete
valid lower-rate miss is ACCEPTED VALID NEGATIVE,including insufficient learning at800 steps.

Report20 rate contrasts (lower minus standard at the same order/seed/language),20 order
contrasts (reverse minus forward at each rate/seed/language),and10 interaction records.
Every contrast has216 matched HOLDOUT answers,accuracy/six-order scores and directional
answer flips. Use actual C262.compare_answers; reconcile correct-count changes with
wrong-to-correct minus correct-to-wrong counts. Interaction disagreement_delta equals
lower-rate order disagreements minus standard-rate order disagreements;negative is fewer
changed answers. Also report each rate's worst chronology accuracy in the same cell.

These interactions are descriptive,not an added result-selected PASS threshold. Small
or zero disagreement is not useful robustness when both models are wrong. Primary PASS
alone also does not establish learning-rate benefit:both rates can pass equally. Do not
infer statistical significance,population guarantees,or a unique optimizer mechanism.

## Workload and persistence

20 models x800=16000 updates,768000 training rows. Per model training+final812 forwards/
40992 rows;strict replay12/2592. Total16480 wrappers/871680 rows;65920 Full core calls;
480 final/replay evaluation forwards. This is twice C262's model workload,not hidden reuse.
One new20-state bundle write/load;20 strict state loads;network calls0.

Six ignored artifacts plus summary.json:rate-plan.json,dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Model schema fold-c263-rate-models-v1
stores20 final states in seed/arm order. Evaluation schema fold-c263-rate-eval-v1 stores
final original/extra logits,initial/final identities,actual fit/schedule metadata and counters.
Use actual C262.replay_one -> C259.replay_one:strict state loading,final fingerprint,
exact argmax,raw logits within1e-9,12/2592 replay workload and48 core calls per model.
Saved postcheck rebuilds metrics,all contrasts/interactions and schedules from persisted
records without another model construction,forward or learned-bundle load. Approximate
raw final-logit payload106 MB plus weights/records; no storage or speed benefit claim.
Source/artifact hashing,parent replay,unit tests and serialization are separate work.

## Protection and authoring

Inherit418 pins/697 inputs;add OWN6 and parent summary+SIX artifacts:424 pins/710 inputs.
Direct deciding dependency union39=five C231 LM sources,C230..C262 helpers and C263.
No accepted source/test/runner/dispatcher is edited. OWN6:
-fold_lm/v05_benchmarks/model_c263_learning_rate_order.py;
-tests_lm/test_v05_c263_learning_rate_order.py;
-tools/run_c263.ps1;
-tools/invoke_c263.ps1;
-this preregistration;
-docs/v5b-learning-rate-order-v0.1.md.
Own24;modules148;loaded3478/focused3477. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305.

Own tests explicitly import the accepted C262 synthetic Tiny/Factory/Base/Orders/Trainer/
Scorer/Audit fixtures,not its TestCase. They also call C262.compare_answers and replay_one.
Test07 exercises the actual new800-update loop on Tiny;test20 substitutes training while
executing real20-state orchestration,persistence and replay. These are authoring tests,
not real FOLD capability evidence. The dummy3478-ID suite checks filtering only.
Before activation re-fetch all committed OWN files,match executable bytes to tested copies,
execute own24,compile/import,global binding and fixed-hash audits;check parent API semantics,
resource counts,CLI indices and parser-before-logging order. State any limited parent
checkout or synthetic adapter use in the handoff. Windows parser/full3477/real parent
artifacts and actual20-model training remain mandatory on the user's authoritative runtime.

## Stop and interpretation

All six fact orders are training-visible and the authored task family has been inspected.
Fresh seeds are not a new independent general benchmark. No general-language,core-superiority,
automatic learning-rate adoption or Gate F claim. Do not tune after reading results.
Integrity faults retry SAME C263;valid misses are accepted without changing data,seeds,
budget or rates. Operational skips precede logging. Log-only transport failures are
repaired without repeating training. No paid API,external corpus,model expansion,cleanup,
history rewrite or CI change. Judge C263 before C264.
