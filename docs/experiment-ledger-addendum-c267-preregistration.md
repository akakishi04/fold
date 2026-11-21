# C267 preregistration — paired name-coverage training

Experiment:C267-v5b-paired-name-coverage-training. Stage:V5-B-PAIRED-NAME-COVERAGE-TRAINING.
C266 ACCEPTED PASS(diagnostic integrity only);C265 remains accepted valid negative.
Gate E PASSED;Gate F NOT PASSED. C268 NOT REGISTERED.
Acceptance/base:38272da75661b1f2f028719b41aa4406ee6dd26b.
Acceptance:docs/experiment-ledger-addendum-c266-c267.md.

## One question

At matched architecture,initial weights,base questions and800 updates,does explicitly training
compound-name collisions reduce same-answer collapse and support held-out value-pair answers,
relative to equal-length doubled-name-only training?
This is a new training-distribution experiment,not another frozen-output diagnostic or continuation
of a failed learned state. No change to the production model or optimizer defaults follows.

## Fresh matched arms

Seeds267001..267005. For each seed,create one unchanged actual C252 Full AlignedPrecoreReadout through
C256.make_model(C231.new_model(seed),aligned_precore_read,seed,C252,C248),then deep-copy the complete
initial wrapper into doubled_only and mixed_names. Both14256 parameters;no shared tensor storage.
No accepted learned checkpoint,optimizer state or C263 activation initializes training.
Full/backbone/reader changes are checked during the run;initial full fingerprints must match within
pairs. This is not a core-free comparison and does not remove or edit any accepted model code.

Keep two visible facts,known character pool a/b/c and 甲/乙/丙,distinct values0..3,both queried entities,
all three entity subsets,both visible fact orders,48-slot BOS/bytes/EOS/PAD contract and zero task IDs.
For source names u,v in ascending original entity-index order,profiles are fixed exactly as C265:
-doubled:uu/vv;
-shared_prefix:uu/uv;
-shared_suffix:uu/vu.
Apply the mapping consistently to facts and query. No translation back before model inference.
Only visible bytes enter the model. Targets,entity indices,profile and split labels stay offline.
Normal lengths are13 ASCII or25 Japanese bytes,matched across naming profiles for each base row.

Control doubled_only always trains on doubled names. Treatment mixed_names cycles all three
profiles. Both arms receive the same base assignment/language/subset/order/query/target at each
update. The changed variable is this specified naming-coverage policy,including its cycle.
The number of identical doubled-name presentations is necessarily lower in treatment;do not claim
per-rendered-string exposure is matched. Logical base-row exposures and total updates are matched.

## New disjoint two-fact assignment split

Do NOT reuse C264's projected TRAIN/HOLDOUT labels;those projections can overlap. C267 starts fresh.
Of the12 ordered distinct value pairs,hold out exactly(0,2),(1,3),(2,0),(3,1) in every source subset,
language,order and naming profile. The other8 pairs are TRAIN. No HOLDOUT row is optimized.
Each entity-position/value marginal is balanced:each digit occurs twice in TRAIN and once in
HOLDOUT at each logical entity position. TRAIN192 logical rows;HOLDOUT96;total288.
The held pairs differ by2 modulo4,whereas TRAIN differs by1 or3. This is a deliberately structured,
small relational split,not a random population sample. Results apply only to this split.
All rendered profiles of a held value pair stay held out. Grouping/permutation does not leak them.
Dataset SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
The finite symbolic family and these value relationships have been inspected in earlier work;
fresh weights and this explicit split do not create an independent general benchmark.

## Fixed schedule and optimization

TRAIN-only token tables have shape3x192x48 and192 target bytes. Control indexes profile0 only.
For step s:epoch=s//4,block=s%4. Construct randperm192 with seed+267000+epoch and select its48-row block.
Use the identical indices in the paired arms. Treatment profile=epoch%3;control profile=0.
800 steps comprise200 COMPLETE four-block epochs,without a partial batch or extra update.
Every logical TRAIN row appears exactly200 times in either arm. Treatment profile epochs67/67/66,
updates268/268/264;control updates800/0/0. Record actual logical-batch digest,row-exposure counts and
profile update counts;reconstruct and compare them during saved analysis. No profile selection.
Reset training RNG to seed+268000 for each arm. AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,
global gradient clip1,batch48,800 updates/model. CPU float64,threads2,deterministic algorithms.
Do not add updates,change learning rate,select seeds or pick an intermediate checkpoint after results.

## Capability gate and comparative outcome

Evaluate BOTH assignment splits,ALL3 naming profiles,all subsets/languages/orders and three views
normal,evidence_blind,query_blind. Final weights only. A model has72 answer cells and36 two-order
consistency cells. The new scorer uses the existing90%/80%/35-point criteria,with explicit new
integer denominators instead of silently passing partial rows into C264's fixed288-row scorer.

Per language/subset/order/profile/split require accuracy>=.90,complete paired-query accuracy>=.80,
evidence-mask drop>=.35 and query-mask drop>=.35. TRAIN cells16 answers/8 query pairs require15/16
and7/8. HOLDOUT cells8 answers/4 query pairs require8/8 and4/4 because of integer rounding.
Per language/subset/profile/split require two-order consistency>=.80:TRAIN13/16 groups,HOLDOUT7/8.
The HOLDOUT accuracy gate therefore requires perfect answers in each small cell;state this clearly.
No aggregate across an easy profile or language rescues a weak cell.

C267 primary PASS iff all FIVE mixed_names states satisfy all criteria on both splits and all profiles.
Control gates are reported independently and cannot fail or rescue treatment. This is a newly
registered treatment gate,not an amendment of C265's frozen all20-model test. Valid misses are
ACCEPTED VALID NEGATIVE;source/test/replay failures are INVALID and retry the same experiment only.

Also report30 paired HOLDOUT contrasts:5 seeds x3 profiles x2 languages. Each contains48 answers and
24 same-facts/different-query pairs. Report correct-answer difference and same-answer-collapse
count difference,mixed minus control. Collapse counts include identical wrong/outside answers,not
only selection of a displayed value. Correctness is reported alongside collapse to avoid calling
uniformly wrong but different answers an improvement. No extra result-selected significance gate.
A capability PASS alone does not establish treatment advantage;both arms may pass equally.
All naming profiles are TRAIN-SEEN in treatment. Success means held-VALUE-pair performance under
covered names,NOT unseen-name transfer,arbitrary-string understanding or a proven internal parser.

## Parent provenance and protected dependencies

C266 execution:b377042dcdb903a308da131feb135b0f5362d9de.
Published log:a18f2e82e9edb9e96d5b25937041be089288e6ec.
Summary:runs/c266-v5b-query-pairs-b652a5a2d2ea4dac9b913b64df6d78e0/summary.json.
Summary SHA256:5d9c79306aae5fb2fd39a82fae645a1447029cae3aedfb2bf92e953bb2435247.
All six parent artifact hashes are fixed in PARENT_ARTIFACTS and the acceptance record.
load_parent calls actual C266.validate_result and requires diagnostic PASS,correct execution and
capability_pass_claim=False. It checks every artifact hash/size,audit-plan equality to C266.manifest,
and validation-summary equality. The parent is diagnostic provenance,not learned initialization.
No parent torch archive or learned-bundle load is needed for this direct parent contract;inherited
protected files are still hashed. precheck calls the actual loader,not a guessed summary adapter.

Inherit442 source pins/748 inputs;add OWN6 and C266 summary+SIX artifacts:448 pins/761 inputs.
Direct deciding dependency union43 includes five C231 LM sources,C230..C266 helpers,andC267.
The lazy parent/factory/core contexts are included. Actual path/hash verification remains mandatory.
OWN6:benchmark,tests,runner,launcher,this preregistration and design:
fold_lm/v05_benchmarks/model_c267_name_coverage_training.py;
tests_lm/test_v05_c267_name_coverage_training.py;
tools/run_c267.ps1;tools/invoke_c267.ps1;
docs/experiment-ledger-addendum-c267-preregistration.md;docs/v5b-name-coverage-training-v0.1.md.
Own24;modules152;loaded3574/focused3573. The sole inherited exact exclusion is:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:4f83a11bd6b2c31d7f1bd23b617772d1eab413e5099d5aafe3c4a34eb453f2d7.

## Workload,persistence and review

10 models x800 updates x48 rows=8000 updates/384000 training presentations.
Per final evaluation:TRAIN two96-row chunks and HOLDOUT one96-row chunk,3 profiles x3 views,
27 forwards/2592 rows. Strict checkpoint replay repeats27/2592. Train+final827/40992;including
replay854/43584 per model. Total8540 model forwards/435840 rows/34160 Full core calls.
540 final/replay forwards. One new10-state bundle write/load and10 strict state loads.
Raw final-logit payload53084160 bytes(about53 MB decimal),plus states and JSON. Not a peak-RAM estimate.
Historical tests,parent/source hashing,schedule generation and serialization are additional work.

Six ignored artifacts plus summary.json:coverage-plan.json,dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Model schema fold-c267-coverage-models-v1;
eval schema fold-c267-coverage-eval-v1. Saved logits are final-state outputs for each split/profile/view,
not initial outputs. Strict loading requires final fingerprints,exact argmax and max raw error<=1e-9.
Saved postcheck rebuilds schedules,metrics,paired contrasts and gates without model calls or another
learned-bundle load. Iteration uses fixed SPLITS rather than serialized dictionary key order.
Only console text logs are published;weights,dataset and generated outputs stay in ignored runs/.

Authoring tests use synthetic Tiny/Factory/Base/Core/Audit fixtures,not production FOLD computation.
The800-step training loop,replay and counters are exercised on Tiny. The ten-model orchestration
test substitutes training but uses actual new evaluation/scoring/replay/persistence. The parent
validator is mocked for a temporary-file contract test. The dummy3574-ID suite checks filtering,
not execution of3573 historical tests. Prepublication tests found and fixed a JSON split-order
reconstruction bug and a same-line source-order assertion issue;no scientific results were run.
Before activation,re-fetch all committed files,match tested executable bytes,rerun own24 and audit
compile/import/free names,manifest,counts,CLI,parent semantics and parser-before-logging order.
Record limitations and review HEAD in the handoff. Windows ParseFile and full user-runtime checks
remain mandatory. No launcher before committed-byte post-authoring review PASS.

No production adoption,learning-rate/architecture default change,paid API,external corpus,cleanup,
history rewrite or CI change. Do not reclassify C266 as capability PASS or rescue C265. Operational
skips precede logging. Repair log-only publication without retraining. Judge C267 before C268.
