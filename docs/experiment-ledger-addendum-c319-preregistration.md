# C319 preregistration — train last-only from initialization

Experiment:C319-v5b-trained-last-readout. Stage:V5-B-TRAINED-LAST-READOUT.
Acceptance base:b43b820b94346be08646f8f5a0d499fb7824fb27. C318 diagnostic PASS only.
C320 NOT REGISTERED. Gate F NOT PASSED. No C319 scientific outcomes observed before registration.

## One question and prospective gate

Does a last-query-byte-only readout trained from initialization retain unseen-six reliability
compared with the native mean-plus-last readout? C318's frozen removal reduced performance,
but that intervention was outside the original training policy. This experiment gives the
single-branch function its own learning trajectory rather than replacing a jointly trained head.

Fresh paired initial seeds319001..319005 and order seeds319101..319105. Two arms:mean_last
control,last_only candidate. Train all ten states anew. No C316 checkpoint,successful core,
old prediction or C318 changed answer is used as initialization or supervision. No per-question
selection or further endpoint/mixture sweep. Primary:ALL5 candidate states pass every existing
local/masked SIX criterion. Control results are reported independently;no post-hoc primary swap.
A completed valid run missing this condition is ACCEPTED VALID NEGATIVE. Old verdicts remain.

## Fixed data and training budget

Both arms use the original two_to_four training policy:each logical TRAIN row appears100times
at each of lengths2,3,4;zero training at1,5,6. Both1200updates,48rows/update,57600training row
presentations/model. Use actual C315.plan_for_order(order,'two_to_four',...) and C312 pair inventory.
Both arms receive identical rendered batches,including the same length/profile/language/values
and intact two-query pairs. Same private order+306000+epoch permutations and same profile cycle.
No value balancing,single-character mixture,extra examples,masked training or held-out values.

All canonical C3161..6 evaluation prompts retained. Length1 has one repeat profile and is an
untrained diagnostic in both arms;2..6 have3profiles. English/Japanese,TRAIN/HOLDOUT values and
normal/evidence-blind/query-blind inputs unchanged. No truncation or64-slot extension.
Data SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Full prompt SHA256:2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd.

Actual C304 LengthReadout/C278 factory,14256stored and configured-trainable parameters,3328core,
64slots,CPUfloat64,threads2,deterministic. All weight tensors independently stored but identical
at initialization within a pair. CoreLR.0005/noncore.005 using actual C308 core_slow optimizer;
ordinary mean CE,AdamW betas.9/.999,eps1e-8,decay0,globalgradientclip1 before step,FIT_RNG612000.
No learned coefficient,new capacity,auxiliary loss,teacher,early-stop or seed replacement.

## Differentiable policy used throughout the lifecycle

The real accepted C304 forward executes. It calls read.query first on the query-span mean and
second on the last-query-byte local state,then averages two attention memories. In last_only,
replace only the FIRST native projection input with that same last-byte local state. Both calls
then use the native last anchor,retaining .5*(memory+memory),total coefficient1. Control leaves
both native inputs unchanged. Keys/shared query weights/value states/core/norm/classifier and
full256-class output remain. Byte means literal UTF8byte,not an entire Unicode character.

Unlike the frozen C318 hook,do NOT detach or no-grad the selected local representation during
training. Preserve the full autograd graph to encoder/query/core/reader parameters. Validate
native query inputs before replacement,one encoder capture/two query projections per forward,
finite CPUfloat64 Bx64x16 local tensors,gradient connectivity while grad mode is active.
Clear transient capture references after every forward without disconnecting the returned
output's autograd graph;no retained graph across optimizer steps. Cleanup hooks on exceptions.
No accepted source,method or global is monkeypatched. Child-owned temporary module hooks only.

Use the SAME readout policy during all1200updates,final1..6 evaluation,and strict checkpoint
replay. Archive per-model policy tags and hook receipts. A policy mismatch invalidates the run.
One model records1344forward calls including final evaluation,2688query calls,71424rows and
1200grad-enabled calls. Replay adds144forwards,288query calls,13824rows,zero grad-enabled calls.
Full/core weights must change during training and remain unchanged during final evaluation.
All saved outputs replay<=1e-9 absolute drift and exact argmax. No switch back to mixed inference.

## Scientific interpretation boundary

Identical initial weights need not give identical initial logits/losses because the architectures
compute different functions. Do not impose loss matching or calibrate one arm to a desired result.
Identical stored parameter count does not imply identical functional flexibility. Duplicating
last attention preserves total coefficient but not the original output vector norm/covariance.
Both attention computations remain,so no compute or memory saving claim is authorized.

PASS is bounded candidate SIX capability,not proof of superiority,universal branch necessity,
new-data generalization or Gate F. Both arms failing would leave the single-branch hypothesis
unresolved,not establish that two branches are mathematically necessary. Full training paths
differ,so the result is a learning-policy comparison,not an additive attribution to the mean.

## Parent writer and dependency protection

C318 execution:f4624509c4311b3e7b04b3d861cfcb3e9d58bfd0.
Publication:3444c11cb68c85e35202f65f26ba258aaadc2c1a.
Summary:runs/c318-v5b-readout-branches-bb278106ee824f26996434d7d895726a/summary.json.
SHA256:5b838ca1420dc36b146ba4afa548d889f16172bd1d1705e4f5df97a5664c5203.
C318 source blob:5d48dd2866b8e10a286cb5d3991e6f3ea24f952d.
C304 source blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify45 ordered summary hashes BEFORE exact C318.verify_artifacts(parentdir,44ancestors,
accepted execution HEAD). Require diagnostic PASS,the four actual artifact names and exact
original/mean-only/last-only length pass counts. C318 does NOT own a dataset or model bundle.
After its verifier,C318.load_parent on paths[1:] supplies verified canonical C316 data/prompts.
No saved model state is loaded for scientific training. The parent chain and byte hashes enforce
writer semantics rather than guessing another experiment's schema. Sole direct import is C318.
Its context yields C317/C316 and accepted C315 evaluator/scheduler/replay,C304 model/span/scorer,
C308 optimizer,C287 normalizer,C312/C296 pairing,C310 no-neural and the original backend.

Retain every754 source pin/1418 protected input,including actual repository-local lazy/context/
factory-language helpers. Add OWN6 and5 C318 parent files:760source pins/1429inputs. No accepted
source/test/preregistration/log/dispatcher edit or additional regression exclusion. Missing
scientific helper coverage is a protection failure,not grounds to waive verification.

## Outputs and execution work

Science10new models,12000updates,576000training rows,14880model forwards,852480row presentations,
59520core calls,10strict state loads,one10-state model bundle write/read,network0. Final evaluation
and replay included. Discarded operational probes,software regression and recursive ancestor
checks are separate. Raw final logits retained locally;no claim that checkpoint size is peak RAM.

Seven artifacts plus summary:architecture-plan.json,dataset.json,length-datasets.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c319-trained-readout-models-v1;fold-c319-trained-readout-eval-v1. Ordered identities include
both fresh seed and trained policy. Save every loss/LR/gradient receiver trace,actual schedule,
policy receipts,initial/final full/core fingerprints and final all-view logits. No overwrite.
No-neural postcheck reconstructs all scores,fit policies,paired outcomes and JSON descriptors;
all model/evaluation tensor hashes and sizes are checked. Full arrays remain local/ignored.

Same accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/two_order.80. Score2..6 with existing
C304/C270 scorer and C287 normalizer. Report100state/length/split partitions,20length1 descriptive
records,5paired-six outcomes and all ten gates. Do not pool old successes into the new primary.

Own24/modules204/loaded5198/focused5197. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:61d98e2b6289a9e11ac0bd915df26e7e07a932895d13b2730e2d675f3b6e0a7e.
Commit/refetch/review all6 OWN before activation. Required software tests include actual accepted
C304 forward output AND parameter-gradient comparison to an independent last-only formula,
control native gradient identity,full1200step optimizer equivalence to accepted C315 loop,
actual candidate train/evaluate/policy-specific replay,source protection,parent semantics,loader
order,persistence,tamper tests and UTF8/CP932 checks. Synthetic tests are not FOLD capability.

User Windows Validate requires45actual parents/pins,all5schedule budgets,real paired model/probes,
own24/full5197regression and dispatcher/launcher/runner ParseFile. Operational copies alone get
a small fixed nonzero output projection to avoid vacuous zero-head checks;scientific initial
weights are untouched. Compare new probe outputs to actual C318 native/last-only hooks,then
exercise backward and finite query gradients on discarded copies. Validate failure skips science
and publication. Integrity failure repairs SAME C319 with fixed science. C320 awaits formal verdict.
