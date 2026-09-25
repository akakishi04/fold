# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C259 ACCEPTED VALID NEGATIVE. C260 ACTIVE / NOT YET JUDGED. C261 NOT REGISTERED.**
C260 is the unique ACTIVE experiment:V5-B paired training-time core ablation.
C259's six-order treatment passed4/5 seeds,not the preregistered5/5;two-order control passed2/5.
C258 remains diagnostic PASS;C257 remains accepted valid negative;C256 bounded PASS remains.
No production architecture change,core-superiority claim,general-language claim or Gate F promotion.
All accepted evidence and invalid-attempt recovery records remain preserved.

## Latest accepted evidence — C259

Scientific execution HEAD:78f0811c390d11256e748b1f955f505ad803de49.
Published log commit:9f7abcc2ea2d88b78a2348e693b2850874f56cb6.
Publisher log SHA256:85d7d49b6db16a3b06492b94b686de796dd8866e397798e489555612b2b96a43.
Log bytes:744908.
Summary SHA256:e005a223fd138ef43e6a3a4664c31a7f2f64482f8325252ba11ad2fdf2562ab1.
Local summary:runs/c259-v5b-order-coverage-7042b90d1ed54cc0858291e661d329e8/summary.json.
Acceptance:docs/experiment-ledger-addendum-c259-c260.md.
Acceptance/base commit:e3311dd21eb5b7235e02dc0d6b59352086691fcb.

Own24 PASS in5.001s;focused3381 PASS in146.224s.
400 source pins/659 protected inputs passed. Ten models completed800 updates each:
8000 updates,384000 training presentations,8240 model forwards,435840 total row presentations.
Paired initial states and logical-batch schedules matched. Full/backbone/head weight-change guards,
strict checkpoint fingerprint/logit/argmax replay,persisted final-logit metric recomputation,
protected inputs,clean tracked tree and execution HEAD preservation all passed.
New10-state bundle writes1/loads1;strict state loads10. run_execution_valid=True.
scientific_status=FAIL;candidate_gate=False;all_pairs_matched/all_replays/all_weights_changed=True.

Acceptance uses immutable published log ranges,publication metadata and recorded local postchecks.
The reviewer did not independently execute the user-local learned checkpoints or rehash the whole
744908-byte log. Publisher-reported SHA256 is not an independent complete-byte rehash.
The log-only publication commit changes only c259/latest.json and latest.log.

Deciding HOLDOUT results across all6 orders:216 answers and36 all-six-correct groups per language.

|Seed|Two EN /216|Two JA /216|Six EN /216|Six JA /216|Six consistency EN /36|Six consistency JA /36|Two gate|Six gate|
|---:|---:|---:|---:|---:|---:|---:|---|---|
|259001|207|216|216|216|36|36|EXTRA_ORDER_MISS|PASS|
|259002|66|69|128|128|15|16|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|259003|139|143|216|216|36|36|ORIGINAL_CRITERIA_MISS|PASS|
|259004|216|216|216|216|36|36|PASS|PASS|
|259005|216|216|216|216|36|36|PASS|PASS|

Pooled six-order treatment1984/2160(91.8519%);two-order control1704/2160(78.8889%).
Five of ten seed/language pairs improve and five tie;none declines in either all-order accuracy or
all-six consistency. These are descriptive paired results,not significance or population guarantees.
The original primary gate requires every candidate seed,language,split and registered criterion.
A pooled mean or improvement over controls cannot rescue4/5 into PASS.

Failing treatment seed259002 fits TRAIN216/216 in both languages and36/36 all-six groups.
HOLDOUT128/216 in both languages;original-order accuracy45/72 EN and44/72 JA;
original query-triplets6/24 EN and5/24 JA. Extra-order counts EN20,23,21,19 and JA20,22,21,21 /36.
The remaining failure is not confined to one formerly unseen permutation and is not an execution error.
More steps,seed replacement or a different gate are not authorized as a C259 retry.

Interpretation:broader order coverage helps these paired measurements but does not ensure reliable
held-assignment recombination across all five initializations. All6 orders were TRAIN-seen for the
treatment,so success is not unseen-order transfer. This repeatedly inspected authored family is not
an independent general benchmark. The results do not identify the core as the cause of the miss.

Accepted C259 artifacts:
-coverage-plan.json:2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb;2900 bytes.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:25282bfeace30ec5fd9be8e46c0aa7f8b3e243a8d0fa2606d656dae5d462e01d;53123591 bytes.
-measurements.json:b833dbdd66373396ba3345385bd92e48a002b1377a0993a217d34ae0d7898862;63863 bytes.
-trained-models.pt:372fab6bbff0c7160c9b89ca8f7147db0f923ef1205f2799466a85f9b61ef3a7;1238007 bytes.
-validation-summary.json:117d4a99611e1aab0109f67e3d4d3012855b22d75d336833557db769519a8b16;3152 bytes.

## Preserved earlier evidence and recovery

C258 diagnostic PASS only:8640 saved answers attributed;no new model calls or training.
Execution:e31d4c28a00bc11fb5db3c2ba1b093e4eae15538;log:62aac236dc90643dc57b3ed51855f79aeb22f1cd.
Summary SHA256:f6ccc7dc1b8c60c1f1e6bc7587bd9853eeb6bea6e1f7a010fd99de068bbd0ecc.
Summary:runs/c258-v5b-middle-slot-93386fd77e3749bab4122685ff57720d/summary.json.
Acceptance:docs/experiment-ledger-addendum-c258-c259.md.
Candidate novel HOLDOUT253 errors:251 other-entity values,2 absent values. b errors141/480 versus
pooled a/c112/960;among b errors,middle distractor64,other distractor75,absent2. Not a universal
middle-value mechanism;seed256005 EN reverses the pooled b-vs-a/c direction. Exploratory only.

C257 ACCEPTED VALID NEGATIVE:unseen-order candidate2/5;passed256001/256004;
256002/256003/256005 NEW_ORDER_MISS. Novel HOLDOUT1187/1440;pooled mean does not replace its gate.
Execution016785f35605a3eef5f94d42f0b86cb2fc4d9dfe;log4a322950685b80d7748aa525608555149c2c2ffd.
Summary SHA256:596df75ccc89c5a12c964c2e6be1fc689e5773f4c0a857f90fdcedd4df9b8816.
Summary:runs/c257-v5b-unseen-order-705d486739b44a56bbed34fae66ace89/summary.json.
Acceptance:docs/experiment-ledger-addendum-c257-c258.md. EOS original criteria were already unmet;
do not count them as five new independent failures solely caused by the order change.

C256 bounded PASS:reader5/5,TRAIN720/720,HOLDOUT718/720;EOS0/5,HOLDOUT248/720.
Executiondb9f3cb90d9268066c34fc91300193058301f06c;log5695706c6306156fa079ce092581270ca781af71.
Summary SHA256:56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184.
Summary:runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.
Acceptance:docs/experiment-ledger-addendum-c256-c257.md.
Its first precheck failure remains INVALID in docs/experiment-ledger-addendum-c256-execution-recovery.md:
execution1029158a60d40df24f599fb719411dbde2ffec06;log2dc541041c772d5b9a449bd247862ad906a9b5c8.
The fixed-manifest-fingerprint and whitespace-sensitive test repairs did not change scientific conditions.

C255 diagnostic PASS:145/160 self versus140/160 value-swap HOLDOUT.
Execution6b577da1edc7339dbfd68b3127870074de218e48;log48856dd7dabb84f1f8a71158d03a5ee9db2fd255.
Acceptance:docs/experiment-ledger-addendum-c255-c256.md;both invalid attempts remain in its recovery addendum.
C254 query96/160,order141/160,self145/160;diagnostic. C253 pre-residual107/160,reader-only117/160,
self145/160;diagnostic. C2524/5,not5/5:accepted valid negative;C2512/5;C250Full2/5,GRU4/5,EOS0/5.
C249 diagnostic;C248 bounded transfer but failed all-seed gate. C247/C246/C244/C242/C241/C239 remain
accepted negatives;C245/C243/C240/C237/C235 diagnostics;C238 seen-prompt fit only. C232/C233 are not
general-language or core-superiority claims. Preserve accepted sources/tests/logs and tools/run_c167.ps1.

## Active C260 — paired training-time core ablation

Experiment:C260-v5b-paired-core-free-training.
Stage:V5-B-PAIRED-CORE-FREE-TRAINING.
One question:can a core-free pre-core residual reader satisfy bounded recombination criteria under
six-order training,relative to a fresh Full aligned reader with identical surviving initial state,
logical questions and800-update budget?

Fresh seeds260001..260005,all included. No accepted checkpoint,activation or optimizer state initializes
training;do not choose only an earlier failing seed. The unchanged Full reference remains available.
with_core:actual C252.AlignedPrecoreReadout via C256.make_model and C231 factory,14256 parameters.
without_core:copy the same backbone and reader,set copied backbone.core=None,and use actual masked
causal GRU states. Pre-core EOS supplies the query and residual base;copied reader query/key maps,
score scale4,PAD mask,weighted local memory,output map,normalization and decoder are retained.
10928 parameters;3328 core parameters removed,not retained as inactive capacity padding.
No backbone.forward or core call in the new forward. Full remains post-core EOS plus reader output.

Match every surviving initial tensor via fingerprint excluding only backbone.core.*;no shared tensor
storage. Full state dictionaries and initial logits need not match across different architectures.
Structural change removes the state-update path and substitutes pre-core EOS as residual base.
This is not a single-weight intervention. Parameters,FLOPs,optimizer state,gradient paths,global
clipping vector and wall-clock are not matched. No unique mechanistic or efficiency superiority claim.
The experiment does not remove the core from FOLD's design or production configuration.

Both arms use the C259 six-order TRAIN policy. Original C256 dataset SHA256:
ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
Extra C257 dataset SHA256:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Keep12 TRAIN/12 HOLDOUT assignments,distinct values,identifiers,query,delimiters and48-slot byte format.
Original144+extra288 rows/split=432,216/language. No HOLDOUT optimization or oracle metadata input.
Actual C259.training_tables constructs TRAIN-only3x144x48 inputs and144 targets.
Step s:epoch=s//3,block=s%3;randperm144 seeded seed+256000+epoch;take48-row block;pair=epoch%3.
Pairs012/210,021/102,120/201 use the original row's order bit. Same logical batches and targets per pair.
Every complete9 steps covers all6 orders once per72 base questions. Fixed800-step tail267/267/266.
AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global clip1;batch48;800 updates/model.
CPU float64,threads2,deterministic;fit RNG seed+259000 resets for each arm.
No extra steps,early stop,checkpoint selection,seed replacement or threshold change.

Gate:ALL FIVE without_core seeds pass both languages and both assignment splits.
Original C256 criteria:accuracy>=.90,order_pair>=.80,query_triplet>=.80,evidence/query drops>=.35.
Each additional order separately:accuracy>=.90,query_triplet>=.80,evidence/query drops>=.35.
All-six consistency>=.80. Extra cells36 answers/12 query-triplets:minima33/36 and10/12.
All-six groups36/language/split:minimum29/36. Use actual C256/C257 scoring helpers.
Full gates are reported separately and cannot rescue/fail the core-free primary gate.
Report every cell plus ten paired HOLDOUT language comparisons of all-order accuracy and six-order
consistency,without_core minus with_core. Primary PASS alone is not comparative superiority.
All6 orders are TRAIN-seen for both arms;no unseen-order or independent-general-benchmark claim.

Workload:10 models,8000 updates,384000 training presentations. Per model train+final812 forwards/
40992 rows;strict replay12/2592. Total8240 model forwards/435840 rows;240 evaluation/replay forwards.
Full evaluates two routes for two internal steps,four core calls per wrapper forward.
Full per-model core3248 train/final+48 replay;five Full models total16480. Core-free core calls0,
not zero wrapper inference. Separate hook counters validate this. One new10-state bundle write/load;
ten strict state loads. Historical tests,parent-file hashing/saved-logit replay are separate work.

Six ignored artifacts plus summary.json:core-plan.json,dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json. Bundle schema fold-c260-core-models-v1;core-free states
omit core keys. Eval schema fold-c260-core-eval-v1 stores final logits,identity/fit/resource/replay records.
Actual C259.replay_one strict-loads matching architecture,checks fingerprint,exact argmax and logit
error<=1e-9;C260 additionally verifies core counts. Persisted postcheck rebuilds all scores and
comparisons from saved final tensors without another model construction or learned-bundle load.

Parent loader hashes the C259 summary and calls actual C259.verify_artifacts(parent_dir,PARENT_EXECUTION).
Require its valid-negative status FAIL,two_order2/six_order4,ten records and exact six artifact hashes.
It replays parent saved output metrics,not parent learned-model inference or initialization.
precheck calls this loader before source/input protection checks.

Protection:406 source pins/672 inputs. Inherit400/659;add parent summary+SIX artifacts+OWN6.
Direct deciding dependency union36 includes five C231 LM sources,C230..C259 helpers,and C260.
Own24;modules145;loaded3406/focused3405. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae.
Registration:docs/experiment-ledger-addendum-c260-preregistration.md.
Design:docs/v5b-core-free-training-v0.1.md. C259 acceptance and C260 registration are separate commits.

## C260 post-authoring review

post_authoring_review = PASS
review_target_HEAD = a19658ef1737a42a3cf92996b3a12bddfde9405b
Scope:committed-byte authoring validation,NOT a formal C260 scientific run.

All six committed OWN files were re-fetched and read at the review target.
Complete locally tested source,test,runner and launcher bytes were independently Git-blob hashed
and matched to the remotely returned identities before the final exact test run:
-benchmark:e80ec370be5503eaf324955f6ecf803272dec4c1;23072 bytes.
-tests:9c9acfd99a0900b8e385a4bbb1de0a0bdee62177;24388 bytes.
-runner:fae62f39989276a17c2484dfa193bf5d9131260c;5177 bytes.
-launcher:63cc4442fb4407845a40bcdabe41da0bf2bd4fe6;2642 bytes.
Re-read document identities:preregistration e24d9045f8b4cc7e0564ac0f406986504f3ed441;
design33156c2ecf513c50f0f2c5685e56f2782459e5b1. These documents were text-reviewed;do not claim
an independent local full-byte rehash of the two documentation files.

First complete own run:24/24 PASS in11.162s.
After committed-file readback and executable-file blob matching:24/24 PASS in11.859s.
No source/test correction was needed after that first complete passing run.
Executed UTF-8/NUL checks,Python compile/import,recursive bytecode global-name binding audit
(zero unresolved names),fixed manifest hash,both dataset hashes,and semantic24-test count PASS.
Three embedded Python blocks compile;CLI indices precheck1,regression none,postcheck1/2/3.
Exact source call-order tests inspect run/precheck and dedented CoreFreeReadout.forward source.
Operational guards and runner parser occur before execution/logging/publication.

Own tests use explicit synthetic Template/FixtureCore and Base/Orders/Parent/Audit adapters.
The surrogate Full core does NOT implement the real FOLD core. The new core-free class itself,
its formula,PAD/EOS checks,gradient propagation,parameter removal and surviving-state pairing are
executed. Test11 runs actual800-step C260 train_one and strict replay on that core-free fixture;
test10 uses a reduced3-step test-only fit;test19 substitutes training records while executing the
actual ten-model orchestration and persisted postcheck. Test18 exercises actual load_parent dispatch
with a mocked parent validator. Test21 constructs3406 dummy IDs to test exclusion,not3405 regressions.
No synthetic result is learned-model capability evidence or execution of the complete parent graph.

Actual C252 readout,C231 factory,language_task encode_local/validation/forward,core parameter layout,
and C259 training_tables/evaluate/replay interfaces were inspected from protected source.
The new residual path and4-per-forward Full core count match those contracts. Parent artifact schemas,
source coverage,count arithmetic,workload,gate constants and launcher paths were reviewed.
The compared changes since C259 execution contain only C259 logs,C259 acceptance and six new C260
files;no accepted source/test/script or shared dispatcher was modified. Only this handoff follows.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No full historical checkout or user-local
learned artifacts were available;GitHub DNS failed in the container. PowerShell absent,so Windows
System.Management.Automation.Language.Parser.ParseFile was NOT executed by the reviewer.
Standard command parses dispatcher;dispatcher parses selected launcher;launcher parses runner.

Pending authoritative checks:Windows parser chain,actual406/672 source/artifact precheck,own24 in
user runtime,full3405 regression,ten actual-model training runs,real strict-checkpoint replay,
persisted postcheck and log publication. None is claimed complete by the authoring review.
Use the FINAL activation branch HEAD,not review_target_HEAD,parent execution or log commit.
Re-read the final branch ref before issuing ExpectedHead.

## Execution and stop

Use tools/invoke_active.ps1;Formal state contains exactly one ACTIVE token resolving to C260.
Launcher parent:runs/c259-v5b-order-coverage-7042b90d1ed54cc0858291e661d329e8/summary.json.
Order:dispatcher/launcher/runner ParseFile -> Python compile+parent/task precheck -> own24 ->
focused3405 -> ten-model paired training -> strict checkpoint replay -> persisted postcheck -> log publication.
Progress:model1/10..10/10;each model step200/400/600/800. A completed valid FAIL is a scientific
negative,not INVALID,and must not be rescued by retraining or threshold/seed changes.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE are operational SKIPPED before
logging;no scientific execution or log publication. Source/artifact/schema/nonfinite/identity/count/
replay/test faults stop and retry SAME C260 after minimal repair. C261 waits for C260 judgment.
Log-only publication failure is repaired without repeating completed training.
The user normally sends only 'finished';fetch docs/experiment-run-logs/c260/latest.json/latest.log.
Do not advance this branch with unrelated documentation while the formal run/log publication is active.

Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite or CI changes. Preserve all earlier evidence,recovery records and tools/run_c167.ps1.
Judge C260 before C261.
