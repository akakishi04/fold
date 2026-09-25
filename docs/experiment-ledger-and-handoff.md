# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C254 ACCEPTED PASS (diagnostic integrity only). C255 ACTIVE / INVALID ATTEMPT RECOVERY. C256 NOT REGISTERED.**
C255 remains the unique ACTIVE experiment:V5-B fixed-query value-assignment residual swap.
Two C255 attempts are INVALID:the first stopped in own tests;the second passed own24+3289 regression
but stopped at the first actual diagnostic model on an over-strict evidence-blind activation check.
The same-C numeric-replay repair has been reviewed;authoritative retry is pending.
No production adoption or new model-capability claim. C252 remains ACCEPTED VALID NEGATIVE.
C253/C254 remain diagnostic PASS;all earlier verdicts are unchanged.

## Latest accepted evidence — C254

Scientific execution HEAD:4e6e5abf5a6a3c97e784868b9fc5e016fc1cf77c.
Published log commit:4fb92919e1da8146fcfe14d779f6b5a91008316a.
Publisher log SHA256:8f13b86ea18c7522170046bf6a70e49f7d334b2d5dca74c8261d007f089901e3.
Log bytes:656074.
Summary SHA256:96f0a3eaafbf0b9fc62e7e9f789344eac45497b2679662525ea54993803535f5.
Local summary:runs/c254-v5b-paired-residual-e324dc81a0364f92820cf8da7f3a0172/summary.json.

24 own tests PASS in3.084s;3265 focused tests PASS in231.431s.
370 source pins/599 inputs protected. All five frozen models,120 head evaluations/5760 head rows.
Full-model/encoder/core/reader forwards0;training0;parameter-bundle loads1;strict state loads5;
new learned checkpoint writes0. Intact/restored logits and query-blind control replay PASS.
Weights/inputs preserved;persisted head-output replay PASS;tracked tree clean;execution HEAD
preserved;run_execution_valid=True. This is diagnostic integrity,not an accuracy-improvement gate.

HOLDOUT exact correct counts,EN/JA,denominator16 per language:

| Seed | Self | Order swap | Query swap |
|---:|---:|---:|---:|
|250001|16,16|16,16|16,15|
|250002|9,9|8,7|3,2|
|250003|16,16|16,16|8,8|
|250004|15,16|15,15|11,11|
|250005|16,16|16,16|12,10|

HOLDOUT totals145/160 self,141/160 order_swap,96/160 query_swap.
TRAIN totals320/320 self,319/320 order_swap,212/320 query_swap.
Query-swap HOLDOUT:50 correct-to-wrong,1 wrong-to-correct,61 total flips,21 donor-target matches.
Order-swap HOLDOUT:7 correct-to-wrong,3 wrong-to-correct,10 total flips.
Query-swap HOLDOUT accuracy declines in9 language cells and is unchanged in250001 EN;order-swap
accuracy declines in3 and is unchanged in7. Query-swap NLL increases in all10 HOLDOUT cells.
The initial conversational aggregate94 was arithmetic error,explicitly corrected to96 before acceptance.

With reader vectors fixed,query donors have much larger effects than order donors in this frozen
comparison. This supports query-specific dependency,but does not yet separate query-name information
from value-assignment information or establish a unique binding algorithm. Many wrong outputs do
not match the donor target. The interventions recombine jointly trained features off-distribution;
LayerNorm/co-adaptation and correlation across the small repeated task remain interpretation limits.

Acceptance/artifact identities:docs/experiment-ledger-addendum-c254-c255.md.
Acceptance/base commit:5764f3e18a09452739029c3accd7740686d8d7fe.
Publication follows execution by one commit and changes only c254/latest.log/latest.json.
Acceptance is based on retrieved immutable log ranges,metadata and recorded local postchecks,
not a reviewer rerun of actual checkpoints or independent full-log byte hash. No C254 rerun needed.

## Preserved earlier boundaries

C253 frozen residual removal:original145/160,pre-residual107/160,reader-only117/160 HOLDOUT;
residual dependence differs across models and is not training-time core necessity.
C252 pre-core query/memory with post-core residual:4/5 joint seed passes,not5/5.
C251 pre-core memory/post-core query:2/5;C250 Full post-core reader2/5,GRU reader4/5,EOS0/5.
C249 established frozen reader dependency. C248 showed bounded transfer but missed its all-seed gate.
C247/C246/C244/C242/C241/C239 remain accepted negatives;C245/C243/C240/C237/C235 remain diagnostics;
C238 seen-prompt fit only. C232 bounded byte learning and C233 competitive GRU-only results are not
broad-language or core-superiority claims. All original sources,results and recovery evidence remain.

## Active C255 — fixed-query value residual swap

Experiment:C255-v5b-value-residual-swap.
Stage:V5-B-VALUE-RESIDUAL-SWAP.
One question:with query name and fact order fixed,does changing the donor's entity-value assignment
change recipient answers when only the donor residual is used and the recipient reader stays fixed?
This is the complementary value-assignment contrast to C254's question/order contrasts.

Example recipient box=0;book=1;box= and donor box=1;book=0;box=.
Donor keys are language,object pair,reversed value tuple,order,query. Require within-seed/split/view
scope,complete unique pairs,bijection,involution,no fixed points. Labels only validate different
paired targets,not donor selection or input. Same five seeds250001..250005,TRAIN64/HOLDOUT32,
original bytes/provenance/labels/views;no success-based selection or new learning.

Mode order:self,value_swap,coherent_swap,restored.
Self/restored use post_i+read_i;value_swap uses post_d+read_i;coherent_swap uses post_d+read_d.
Apply the accepted original LayerNorm and decoder. Coherent_swap is a positive replay control and
must match the original DONOR logits/argmax,including its errors. Do not score it against the
recipient label or call its result capability improvement. It is not an answer repair.
In evidence_blind views,paired fact-swapped prompts coincide:post/read vectors must match exactly
and value_swap must reproduce self. Self/restored must reproduce original raw logits<=1e-9 and
exact predictions. Parameter fingerprints are checked after every head evaluation.

Read C253 saved intact post/read activations,load exact C252 final states strictly via C253.frozen_model,
freeze eval/gradients,and execute ONLY normalization/decoder. Guards forbid full-model/backbone/
encoder/core/reader forward calls. Preserve all source tensors. Same14256-parameter learned models;
no new model,weights,optimizer,seed,budget or input modification. No scientific network call.

Loader roles:C255.load_inputs(c254,c253,c252) calls actual C254.load_inputs(c253,c252),which supplies
parts,C252 final refs,C253 original entries;then it reads C254 head-outputs.pt and replays the
C254 archive through C254.analyze(...,C253.metrics),matching all JSON and summary outputs.
C254's records are immutable order/query comparators;do not call its loader with C254 summary.
C252/C253 parents are inherited hashed inputs,not double-counted. Parent outputs are final learned
activations/logits,not initial states or synthetic fixtures.

Scientific workload:120 HEAD evaluations/5760 HEAD rows;full/encoder/core/reader forwards0;training0.
One C252 parameter bundle load,5 strict model-state loads,new learned checkpoint writes0.
Each model24 norm and24 decoder calls/1152 rows. Three scored modes give60 diagnostic cells;
20 value-vs-self contrast cells. Coherent control excluded from recipient-accuracy reporting.
Store all four-mode logits;postcheck recomputes metrics,controls,comparators and JSON without scoring.
Archive/hash work and historical fixture tests have separate real costs;not new independent samples.

PASS is diagnostic integrity only,no required direction of accuracy or donor-target score.
Report flips,transitions,accuracy/NLL changes and immutable C254 query/order metrics per cell.
Value sensitivity would be bounded dependency evidence,not unique semantic or causal identification,
training-time necessity,external validation,production adoption or Gate F completion. Query- and
value-swapped donors share a target in this two-entity fixture,so equal effects are not unique evidence
for target-value coding. These contrasts should inform an explicit next capability/stability decision,
not an indefinite extension of microtask diagnostics. Judge C255 before registering C256.

Protection:376 source pins/611 inputs;explicit dependency union31;OWN6.
Own tests24;modules140;loaded3290/focused3289;only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored artifacts:value-plan.json,head-outputs.pt,diagnostics.json,contrasts.json,validation-summary.json.
Archive schema fold-c255-value-head-outputs-v1 stores outputs,not learned parameters.
Manifest:e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a.
Design:docs/v5b-value-residual-swap-v0.1.md.
Registration:docs/experiment-ledger-addendum-c255-preregistration.md.
Preregistration/review HEAD:f7d5dc354f942a1ea7a43b264fc8629fe37ca9be.
Use tools/invoke_active.ps1 with the final activation HEAD,not this earlier review HEAD.

## C255 execution recovery and post-repair review

### Invalid attempt1 — authoring test bitwise replay

Execution HEAD:70ca4c4c71f7e304d0a78313e642f5fdb57d4da2.
Log commit:372ef97671bdec0dc7db07e8dea456e60c7f2f02.
Log SHA256:d9db7508f1ad693884c4854121453375782d0f358855eda3f3164dbc22ddb285.
Preflight/archive passed;own tests23/24 PASS. Test07 required bitwise `torch.equal` for coherent
recomputed donor logits even though the registered science contract is raw-logit max error<=1e-9
plus exact argmax. Regression/science did not run;run_execution_valid=False.
Minimal repair changed only test07 to the existing `b.replay(...)` contract.
Repair commit:f10a493f5ea6a92f06bd3a0860444b69c64de5a1.

### Invalid attempt2 — evidence-blind activation bitwise identity

Execution HEAD:275754bf58adbac6fdef92a34b6d2c309be0548b.
Log commit:b7496ffd46c12d469e9478eed05d3c81b9c780dc.
Log SHA256:933ccbc8613f06f94f9cc6184e052f5ed290b22b81b04ca48e76323fe3e25f34.
This attempt passed preflight/source/archive,all24 own tests and all3289 focused regression tests.
The actual C255 diagnostic then began and stopped on model1 at:
`ValueError: masked fact-pair identity`.
No complete scientific result exists;run_execution_valid=False.

The failing guard required bitwise equality between the saved post/read activations of paired
evidence-blind rows. Those paired rendered prompts are semantically identical by construction:
language,object order and query are fixed and both fact values are erased. However the accepted
numerical replay policy for C255 is TOL=1e-9,not cross-row bitwise activation identity.
This guard therefore rejected before the registered output-level negative control could be judged.

Second minimal repair changes only:
- benchmark evidence-blind post/read comparison:bitwise equality -> max-abs<=the unchanged TOL=1e-9;
- authoring evidence-blind output assertion:bitwise equality -> existing `b.replay` <=TOL.
The evidence-blind value-swap output still requires raw-logit replay<=1e-9 and exact argmax.
Donor mapping,all five seeds,data,model/head formula,metrics,workload,capability gate and TOL are
unchanged. No accuracy/scientific threshold was relaxed and no accepted parent source was edited.

Scientific benchmark repair commit:ff8dbe38a6cafa778d09e8f8237d2f5d7f984d18.
Test alignment commit:7fdc5790a0b53c5b8aa5b171c85ed70e3f29dd88.
Recovery record commit:f18e3bfcd6c82801cdb1dac2ad1e66d8782fcc7b.
Recovery doc:docs/experiment-ledger-addendum-c255-execution-recovery.md.

`post_repair_review = PASS`
Review HEAD:f18e3bfcd6c82801cdb1dac2ad1e66d8782fcc7b.
Remote source/test/recovery bytes were re-fetched after repair. Invalid-log-tip to review comparison
contains exactly the benchmark one-line activation guard change,the test one-line negative-control
change,and recovery documentation. Runner,launcher,donor construction,metrics,manifest,TOL,
preregistration and design are unchanged. The benchmark still checks finite CPU float64 tensors,
fixed donors,frozen weights,head-only counters,self/coherent/restored replay and evidence-blind
output replay through the <=1e-9/exact-argmax helper. Test07 remains on that same replay helper.

No new scientific evidence was generated during review. The exact repaired own24,3289 historical
suite,Windows ParseFile,user-local accepted artifacts and actual C255 diagnostic remain mandatory
in the authoritative retry. The runner stops before accepting science on any remaining fault.

Only this handoff changes after the recovery review. Use its final recovery HEAD for retry and do
not advance the branch during that run.

## Stop and scope

Gate F NOT PASSED;numeric-memory/erasure-mixture tuning paused. Preserve accepted sources/tests/logs
and tools/run_c167.ps1. No paid API,external corpus,model expansion,production adoption,cleanup or
history rewrite.24 own tests ->3289 regression ->C255 head-only diagnostic ->postcheck ->publication.
Integrity failures stop same C255;transport-only failures are repaired without repeating head scoring.
Judge C255 before C256.
