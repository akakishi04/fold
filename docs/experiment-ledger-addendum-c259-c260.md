# C259 acceptance and C260 core-contribution boundary

## Formal verdict

C259 ACCEPTED VALID NEGATIVE. The six-order treatment passed 4/5 seeds, not the preregistered 5/5.
The two-order control passed 2/5. Neither a pooled mean nor improvement over controls rescues the gate.
C258 remains diagnostic PASS; C257 remains ACCEPTED VALID NEGATIVE; C256 bounded PASS remains.
Gate E PASSED; Gate F NOT PASSED. No production adoption or general-language claim.

Scientific execution HEAD:78f0811c390d11256e748b1f955f505ad803de49.
Published log commit:9f7abcc2ea2d88b78a2348e693b2850874f56cb6.
Publisher log SHA256:85d7d49b6db16a3b06492b94b686de796dd8866e397798e489555612b2b96a43.
Log bytes:744908.
Summary SHA256:e005a223fd138ef43e6a3a4664c31a7f2f64482f8325252ba11ad2fdf2562ab1.
Summary:runs/c259-v5b-order-coverage-7042b90d1ed54cc0858291e661d329e8/summary.json.
Publication modifies only C259 latest.log/latest.json. Acceptance uses immutable published log ranges,
metadata and recorded local postchecks, not independently executed learned checkpoints or an
independent complete-log byte rehash. The summary, metadata and registered execution HEAD agree.

## Execution validity

Own24 PASS in5.001s; focused3381 PASS in146.224s.
400 source pins/659 protected inputs passed. Ten models completed800 updates each:
8000 updates,384000 training presentations,8240 model forwards,435840 total row presentations.
Paired initial states and logical batches matched; learned full/backbone/head state changes passed.
One10-state bundle write/load;ten strict state loads; all checkpoint-logit/argmax replays passed.
Persisted final-logit metric recomputation,protected inputs,clean tracked tree and execution HEAD
preservation passed;run_execution_valid=True. Scientific status FAIL;candidate_gate=False.

## Deciding metrics

HOLDOUT across all6 fact orders,216 answers and36 all-six-correct groups per language:

|Seed|Two EN /216|Two JA /216|Six EN /216|Six JA /216|Six consistency EN /36|Six consistency JA /36|Two gate|Six gate|
|---:|---:|---:|---:|---:|---:|---:|---|---|
|259001|207|216|216|216|36|36|EXTRA_ORDER_MISS|PASS|
|259002|66|69|128|128|15|16|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|259003|139|143|216|216|36|36|ORIGINAL_CRITERIA_MISS|PASS|
|259004|216|216|216|216|36|36|PASS|PASS|
|259005|216|216|216|216|36|36|PASS|PASS|

Pooled six-order treatment1984/2160(91.8519%); two-order control1704/2160(78.8889%).
Across ten seed/language pairs,accuracy and all-six consistency improved in five and tied in five;
none decreased. These are descriptive paired comparisons,not statistical significance or a
population guarantee. Whole-seed gates also require TRAIN and all masked/per-order criteria.

Failing treatment seed259002 fits TRAIN at216/216 in each language and36/36 all-six groups.
HOLDOUT drops to128/216 in both languages. Original-order accuracy is45/72 EN and44/72 JA;
original query-triplet6/24 EN and5/24 JA. The additional four order counts EN20,23,21,19 and
JA20,22,21,21 show the failure is not confined to a single formerly unseen permutation.
Do not call this execution failure or assume more optimizer steps are required just because it misses.

## Interpretation and non-claims

Under the fixed paired training policy,broader order coverage improved these measured outcomes but
did not make held-assignment recombination reliable in all five initializations. Treatment orders
were all TRAIN-seen:success is not unseen-order transfer. One failed seed is not grounds for seed
replacement,extra training or gate relaxation. C259 remains negative regardless of subsequent work.

The small authored assignment family has been repeatedly inspected. Neither these scores nor fresh
seeds establish general language or a new independent benchmark. No unique internal cause of the
remaining miss is identified. In particular,this is not proof that the FOLD core caused the failure.

## Accepted artifacts

-coverage-plan.json:2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb;2900 bytes.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:25282bfeace30ec5fd9be8e46c0aa7f8b3e243a8d0fa2606d656dae5d462e01d;53123591 bytes.
-measurements.json:b833dbdd66373396ba3345385bd92e48a002b1377a0993a217d34ae0d7898862;63863 bytes.
-trained-models.pt:372fab6bbff0c7160c9b89ca8f7147db0f923ef1205f2799466a85f9b61ef3a7;1238007 bytes.
-validation-summary.json:117d4a99611e1aab0109f67e3d4d3012855b22d75d336833557db769519a8b16;3152 bytes.

## Next question, not activation

Does a core-free pre-core residual reader achieve the same bounded recombination criteria under
six-order training,relative to a freshly trained Full aligned reader with identical initial common
parameters,data,batches and800-update budget? This is a training-time structural ablation,not
removal of the core from the production design or a frozen inference intervention.

Use fresh seeds260001..260005,all included. Retain original Full reference. The ablated branch reads
the same local GRU states with the same learned reader,but adds its output to pre-core EOS rather
than post-core EOS and never executes the state-update core. This removes the core's parameters
and computation;do not describe the pair as parameter- or FLOP-matched. Match surviving parameters
exactly at initialization and report both counts. Comparisons cannot uniquely diagnose the failed
C259 seed or prove general architectural superiority. Register/review C260 separately;C261 unregistered.
