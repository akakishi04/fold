# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C260 ACCEPTED VALID NEGATIVE. C261 ACTIVE / NOT YET JUDGED. C262 NOT REGISTERED.**
C261 is the unique ACTIVE experiment:V5-B frozen repeated-value transfer.
C260's primary without_core arm passed3/5,not5/5;the with_core reference passed4/5.
C259/C257 remain valid negatives;C258 diagnostic PASS andC256 bounded PASS remain.
No architecture selection,production adoption,core-superiority claim or Gate F promotion.
All earlier accepted evidence and invalid-attempt recovery records remain preserved.

## Latest accepted evidence — C260

Scientific execution HEAD:5788a63a692983094a9c6311c58d1440005b7fca.
Published log commit:e841aa5c312d46bfe11172af45262433cf5ec33d.
Publisher log SHA256:604163ff5f8ad3628e8b3facd49f7e97cafde04822123838b344efc893d2fd15.
Log bytes:749925.
Summary SHA256:df6780749afa707fa0c6809e76710f39cdbeac6c1b69665a064248808b1f9ab6.
Summary:runs/c260-v5b-core-free-697d8bdc3ca3411ba81f703b2f16fb96/summary.json.
Acceptance:docs/experiment-ledger-addendum-c260-c261.md.
Acceptance/base commit:a2061c1cf321771241e262def1474cb8f59dcd79.

Own24 PASS in14.466s;focused3405 PASS in147.380s.
406 source pins/672 inputs passed. Ten models completed800 updates each:
8000 updates,384000 training presentations,8240 model forwards,435840 row presentations.
Full core calls16480;core-free core calls0. One10-state bundle write/load;ten strict state loads.
Paired common-state/batch checks,weight-change checks,checkpoint-logit/argmax replay,persisted metric
recomputation,protected-input preservation,clean tracked tree andexecution HEAD checks passed.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.

Acceptance is based on immutable published log ranges,metadata andrecorded local postchecks.
The reviewer did not independently execute the learned checkpoints or rehash the entire749925-byte
log. The publisher's SHA256 is not an independent complete-byte rehash. The registered HEAD,log
metadata andprinted summary identity agree. The publication commit changes only C260 latest.*.

HOLDOUT across all6 orders,216 answers and36 all-six-correct groups per language:

|Seed|Full EN /216|Full JA /216|Free EN /216|Free JA /216|Full six EN,JA /36|Free six EN,JA /36|Full gate|Free gate|
|---:|---:|---:|---:|---:|---|---|---|---|
|260001|216|216|216|216|36,36|36,36|PASS|PASS|
|260002|216|216|115|120|36,36|13,13|PASS|ORIGINAL_CRITERIA_MISS|
|260003|216|216|216|216|36,36|36,36|PASS|PASS|
|260004|216|216|134|139|36,36|19,20|PASS|ORIGINAL_CRITERIA_MISS|
|260005|108|116|216|216|18,19|36,36|ORIGINAL_CRITERIA_MISS|PASS|

Pooled Full1952/2160(90.3704%);core-free1804/2160(83.5185%). Pooling is descriptive,not the gate.
Without_core minus with_core:four paired language accuracies lower,four tied,two higher. The direction
reverses for260005;one path does not dominate every initialization. Full14256 versuscore-free10928
parameters. The pair is not parameter/FLOP/wall-clock matched;residual base,optimizer state andthe
clipped gradient vector also change. No unique internal cause or general superiority is established.
Removing the core did not make all five states reliable. Retain both experimental paths.

Accepted artifacts:
-core-plan.json:ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae;2746 bytes.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:b109243f5b5d24ffe343586a50b97990524c7b572ec238b5e267863dbd542276;53123591 bytes.
-measurements.json:5839838218761bd608b5b79137a300649b3a5df11eb909474520a45608f3a8fa;62614 bytes.
-trained-models.pt:727ffd1320266a239d21ce172279dc2cec3be6383db74cd4a1b09addbe36976c;1075036 bytes.
-validation-summary.json:250d099db6ec58b21db06d858e9c0e0ddf8349f66b0d1936001e3874875e26a2;3298 bytes.

## Preserved earlier evidence and recovery

C259 ACCEPTED VALID NEGATIVE:six-order4/5 versus two-order2/5. Pooled HOLDOUT1984/2160 versus1704/2160.
Execution78f0811c390d11256e748b1f955f505ad803de49;log9f7abcc2ea2d88b78a2348e693b2850874f56cb6.
Summary SHA256:e005a223fd138ef43e6a3a4664c31a7f2f64482f8325252ba11ad2fdf2562ab1.
Summary:runs/c259-v5b-order-coverage-7042b90d1ed54cc0858291e661d329e8/summary.json.
Acceptance:docs/experiment-ledger-addendum-c259-c260.md. Its failing treatment seed259002 fitted
TRAIN but did not generalize to HOLDOUT;no additional steps or seed replacement were authorized.

C258 diagnostic PASS only:8640 saved answers,zero new model inference/training.
Executione31d4c28a00bc11fb5db3c2ba1b093e4eae15538;log62aac236dc90643dc57b3ed51855f79aeb22f1cd.
Acceptance:docs/experiment-ledger-addendum-c258-c259.md. Candidate novel HOLDOUT253 errors:
251 wrong displayed-entity values+2 absent values. Query b errors141/480 versus pooled a/c112/960.
Among b errors,middle64/other75/absent2:exploratory decomposition,not a universal middle-value mechanism.

C257 ACCEPTED VALID NEGATIVE:unseen-order2/5;novel HOLDOUT1187/1440.
Execution016785f35605a3eef5f94d42f0b86cb2fc4d9dfe;log4a322950685b80d7748aa525608555149c2c2ffd.
Acceptance:docs/experiment-ledger-addendum-c257-c258.md. EOS original criteria were already unmet;
do not call those five new independent failures caused by the order shift.

C256 bounded PASS:reader5/5,TRAIN720/720,HOLDOUT718/720;EOS0/5,HOLDOUT248/720.
Executiondb9f3cb90d9268066c34fc91300193058301f06c;log5695706c6306156fa079ce092581270ca781af71.
Acceptance:docs/experiment-ledger-addendum-c256-c257.md. Its precheck INVALID remains in
experiment-ledger-addendum-c256-execution-recovery.md;execution1029158a60d40df24f599fb719411dbde2ffec06,
log2dc541041c772d5b9a449bd247862ad906a9b5c8. The manifest/test repairs did not change science.

C255 diagnostic PASS:145/160 self versus140/160 value swap;both invalid attempts remain in its recovery
addendum. C254 query96/order141/self145 of160;C253 pre-residual107/reader-only117/self145;diagnostics.
C2524/5 remains valid negative;C2512/5;C250Full2/5,GRU4/5,EOS0/5. C249 diagnostic;C248 bounded transfer
but failed all-seed gate. C247/C246/C244/C242/C241/C239 remain negatives;C245/C243/C240/C237/C235
diagnostics;C238 seen-prompt fit. C232/C233 are not general-language orcore-superiority claims.
Full historical identity/review detail is preserved in acceptance/recovery addenda andthe earlier
handoff at e841aa5c312d46bfe11172af45262433cf5ec33d. Do not edit accepted sources/tests/logs orrun_c167.ps1.

## Active C261 — frozen repeated-value transfer

Experiment:C261-v5b-frozen-repeated-value-transfer.
Stage:V5-B-FROZEN-REPEATED-VALUE-TRANSFER.
Question:do all ten frozen C260 final states answer repeated-value assignments correctly without
further training? Test an unexamined distinct-value restriction rather than selecting a winner or
adding seeds until an old gate passes. Both arms andall five original seeds remain included.

Strictly load actual C260 models with seeds260001..260005,with_core14256/without_core10928 parameters.
Use C260.make_pair andload_bundle;verify final fingerprints,eval mode andrequires_grad=False.
No architecture,weight,optimizer,seed ortraining change. New wrappers receive saved final states
before any inference. No production architecture selection. Both arms are reported independently.

New data:all40 nondistinct ordered triples from0..3,not any ofthe24 distinct C260 assignments.
36 pair_equal(one equal pair) and4 all_equal. Two identifier languages x6 orders x3 queries:
1440 rows=1296 pair_equal+144 all_equal. Names,values,query placement,delimiters and48-slot byte contract
remain fixed. Target/singleton metadata is offline scoring only,never a model input. Use all orders
directly without sorting. New rows are not called TRAIN/HOLDOUT;those labels belong only to anchors.
Dataset SHA256:1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339.
Example:a=0;b=0;c=2;c= ->2,while the same facts with a= ->0.

Per model:
-actual C259.evaluate over C260 original+extra,all old splits/views:12 forwards/2592 rows;
-raw-logit replay against accepted C260 final tensors within1e-9 andexact argmax,BEFORE new input;
-new repeated-value rows in144-row chunks,3 views:30 forwards/4320 rows;
-original restoration12 forwards/2592 rows,compared to both anchor andaccepted reference;
-complete weights unchanged,54 wrapper forwards/9504 rows;Full216 core calls orcore-free0.
Old wrong answers faithfully reproduced are valid replay. They are not forced into correctness or
mistaken for new capability evidence. No old C260 capability gate is part of the new-task gate.
Total540 wrappers/95040 rows;Full core1080;training0;new learned checkpoints0;bundle loads1;strict loads10.
CPU float64,threads2,deterministic algorithms;finite outputs andexact identity/count checks required.

Parent loader:require C260 status FAIL andwith_core4/without_core3. load_reference calls actual
C260.verify_artifacts,loads fold-c260-core-eval-v1 records,and replays actual C260.analyze against
accepted measurements/summary. Final fields are final_sha256/raw.original/raw.extra,with144x256 and
288x256 logits per original split/view. Original data order must match saved references exactly.
Two parent evaluation archive loads per pass (parent verification+record acquisition);run andsaved
postcheck are two passes. Four reference archive loads total,not learned model loads.
precheck verifies parent summary/six artifact hashes andsizes,source pins andprotected inputs.

## C261 fixed gate and interpretation

Overall C261 PASS requires all ten states pass the NEW repeated-value task,i.e.BOTH arms5/5.
Report each arm independently;do not switch to the better arm orfilter prior failures after results.
Each state must satisfy24 separate language/stratum/order cells andfour six-order group scores.

pair_equal per language/order:108 answers,36 singleton questions,72 repeated-target questions,
36 three-query groups. Require total/singleton/repeated accuracy>=.90,complete-query-triplet>=.80,
and normal-minus-evidence-blind accuracy>=.35. Integer minima98/108,33/36,65/72,29/36.
Six-order consistency:108 assignment/query groups per language,minimum87/108 entirely correct.
all_equal per language/order:12 answers,accuracy>=.90(11/12),evidence_drop>=.35.
Six-order consistency:12 groups/language,minimum10/12. Query-triplets reported butnot gated;
singleton accuracy is null because no singleton exists. All-equal scores cannot prove query understanding.

Query-blind accuracy/drop are descriptive only. Selecting the repeated value gives2/3 without knowing
the query;all-equal can give1.0. Perfect normal answers can therefore yield only1/3 orzero query-mask
drop. Reusing the old.35 threshold would reject correct behavior. Singleton/repeated accuracy and
complete triplets replace that inappropriate assumption for this NEW task,not retrospectively for C260.
No new assignment result has been used to tune these gates. A valid miss is accepted negative.

Five ignored artifacts+summary:repeat-plan.json,repeat-dataset.json,eval-outputs.pt,measurements.json,
validation-summary.json. Schema fold-c261-repeat-eval-v1 stores anchor/new/restored logits andcounters.
Raw output tensor payload194641920 bytes(about195 MB decimal),plus metadata/files. No disk saving claim.
Persisted postcheck recomputes every replay,new score andgate from saved tensors without new forward,
model construction orlearned-bundle load. Parent hashing,recomputed old metrics andregressions are
additional work,not additional science samples. Only console logs are published to Git.

New assignments are unseen butpart of a repeatedly inspected authored symbolic family. C261 is a
specific distribution-shift probe,not a new independent general benchmark,natural-language ability,
core superiority,production adoption orGate F passage. C260 remains negative regardless of C261.

Protection:412 source pins/685 inputs=parent406/672 +OWN6 +parent summary andSIX artifacts.
Direct deciding dependency union37=five C231 LM sources+C230..C260 helpers+C261;lazy imports included.
Own24;modules146;loaded3430/focused3429. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301.
Registration:docs/experiment-ledger-addendum-c261-preregistration.md.
Design:docs/v5b-repeated-value-transfer-v0.1.md. C260 acceptance andC261 registration are separate commits.

## C261 post-authoring review

post_authoring_review = PASS
review_target_HEAD = fe42025f970d30291b6e9bbc50b511a3d9c096a9
Scope:committed-byte C261 authoring verification,NOT formal C261 scientific execution.

All six OWN files were re-fetched andread from the committed review HEAD after writing was complete.
The complete local executable files were independently Git-blob hashed andmatched to remote identities:
-benchmark:cb938feb12a229ad2234274d932793cf6c7ea3ab;24479 bytes.
-tests:5602ca3dd11997c945f48bccf76e1fe31fe6c682;20314 bytes.
-runner:d2b3fb177f8c6e2c56ed7021ffad5c89016a1b29;4758 bytes.
-launcher:d3633b9f31c7255b42672924425d6308fb43cbbd;2637 bytes.
Read/text-reviewed documentation identities:
-preregistration:f04e036d300a916279b17d3ff324f301366d6278;
-design:6961b8b1051679405841c8f5c4d281a4ae2234ea.
The two docs were text-reviewed,not independently locally rehashed.

First executed exact own suite:24/24 PASS in8.896s.
After full remote readback andexecutable blob matching:24/24 PASS in8.788s.
No post-first-run code/test correction was needed. Executed UTF-8/NUL checks,Python compile/import,
recursive bytecode global-name binding audit(zero unresolved names),manifest/dataset hashes,semantic
24-test count,count arithmetic,workload/tensor payload arithmetic anddependency-pattern cardinality.
Three embedded Python blocks compile;CLI indices precheck1,regression none,postcheck1/2/3.
Exact tests inspect actual run call ordering,replay barriers,mode/state guards,core/wrapper counts,
strict state-load orchestration,per-stratum/group semantics,zero denominators,wrong HEAD,corrupt
artifacts,persisted recomputation,andjoint gate accounting. Source-level checks find no training calls.

Tests use an explicitly synthetic byte-parser Oracle with placeholder parameter tensors andIdentity
core counters,plus Base/Trainer/Parent/Audit adapters. These are NOT actual FOLD models orlearned
capability evidence. Test20 executes actual C261 run/probe/analyze/persisted-postcheck with those
adapters;test19 executes its real reference-loader dispatch with a mocked parent validator.
Test21's3430 dummy IDs test the exact exclusion only,NOT3429 historical tests. No parent checkpoint
orproduction capability result was available in this review. The actual C260 context/make_pair,
load_bundle,verify_artifacts/analyze schemas andfinal-output semantics were read from protected source;
full historical import graph anduser-local parent-byte verification remain pending.

Reviewer:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Container DNS could not resolve raw.githubusercontent.com,
so no complete checkout was available. PowerShell absent;Windows ParseFile was NOT executed here.
Standard command parses dispatcher;dispatcher parses launcher;launcher parses runner before logging.
These checks remain mandatory on the user's Windows runtime. No new shared dispatcher change.
Compare from C260 log commit to review HEAD:only C260 acceptance+six new C261 files,seven additions;
no accepted source/test/log/script changed. Only this activation handoff follows review.

Pending authoritative checks:Windows parser chain,real412/685 source/artifact precheck,own24 in
user runtime,complete3429 regression,ten real frozen-model evaluations,checkpoint/anchor replay,
persisted postcheck andlog publication. None is claimed complete by authoring review.
Use FINAL activation branch HEAD,not review_target_HEAD orparent scientific/log commit.
Re-read final branch ref before providing ExpectedHead. Do not start C262 before C261 judgment.

## Execution and stop

Use tools/invoke_active.ps1. Formal state has one ACTIVE token resolving to C261.
Parent path:runs/c260-v5b-core-free-697d8bdc3ca3411ba81f703b2f16fb96/summary.json.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent/task precheck ->own24 ->focused3429
->ten frozen-model evaluations ->persisted postcheck ->log publication.
Progress:model1/10..10/10. No step200/800 training loop in this experiment. Valid FAIL is a scientific
negative,not INVALID. Do not retrain,reselect seeds,change new-task gates orrewrite old verdicts.

Wrong branch,dirty tracked tree,stale ExpectedHead orstale ACTIVE are operational SKIPPED before
logging;they run no experiment andpublish no log. Source/artifact/schema/nonfinite/identity/count/
replay/test faults stop andrequire minimal SAME C261 repair. No C262 registration on an invalid run.
Log-only publication failure is repaired without repeating completed evaluation.
The user normally sends only 'finished';fetch docs/experiment-run-logs/c261/latest.json/latest.log.
Do not advance this branch with unrelated work during user execution/log publication.

Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite orCI changes. Preserve all accepted evidence,recovery records andtools/run_c167.ps1.
Judge C261 before C262.
