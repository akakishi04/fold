# C300 preregistration — frozen readout-term ablation

Experiment:C300-v5b-frozen-readout-term-ablation. Stage:V5-B-FROZEN-READOUT-TERM-ABLATION.
Acceptance base:c726cc8d1c587328943229276d6588fb59386a06.
C299 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED. C301 NOT REGISTERED.

## One question and scope

Which frozen C299 predictions improve or regress when either tensor in the final pre-normalization
readout sum is suppressed? All9 learned remaining/core combinations stay in the cohort,including
all failures. No further component-seed search,new training,weight splicing or output filtering.
This intervenes on inference-time contribution,not the mechanism that caused a training outcome.

C299 quad matrix:[[T,F,F],[F,F,F],[T,F,T]];seen tasks:[[T,F,F],[T,T,T],[T,T,T]].
In particular,remaining297001 with core297002/297003 also fails seen-length TRAIN. There is no
universal successful core donor. The same-source diagonals reproduced C298 exactly. Do not turn
this diagnostic follow-up into an easier capability gate or a best-cell deployment policy.

## Exact tensor semantics and intervention

The accepted actual C278 MeanFinalDualReadout forward adds two width16 tensors before readout_norm:
r = the post-core next-route EOS residual;
a = read.output((memory_mean+memory_final)/2),from query/key attention over masked pre-core local states.
The additional reader is NOT the vocabulary classifier. The classifier and normalization remain
unchanged in all conditions. In fixed order for every model:
1.full_before:normalizer input r+a,unchanged;
2.residual_only:normalizer input r;
3.reader_only:normalizer input a;
4.full_after:normalizer input r+a,unchanged/restoration control.

All upstream computation,including every core call and the added-reader computation,STILL executes.
Only the tensor supplied to normalization changes. Neither branch's role proves core necessity,
core dispensability,or a speed benefit. r contains effects of the entire backbone,not just a core
parameter block. Layer normalization means this is not additive attribution in final-logit space.
The jointly trained model did not optimize either ablated condition;distribution-shift effects
are expected possibilities,not invalidity or evidence of a universal architectural remedy.

Use temporary instance hooks,not modifications or monkeypatches of accepted module source.
Capture r before C278's dynamically installed normalizer hook;capture a at read.output. Register
a second normalizer pre-hook during the local-encoder call,after C278 installed its own hook.
Require exact equality of the actual normalizer input and captured r+a on EVERY forward before
any replacement. Validate width16,batch,dtype,finite values and single call/capture counts.
The original C278 forward and its provenance assertions remain active. Baseline modes return None
from the late hook so the original normalizer input is used unmodified. Hooks are removed on normal
completion AND exceptions;existing hook registries must be restored. Frozen eval/no_grad only.
No labels,candidate sets,task solutions or component metadata enter the model or the intervention.

## Reproduction and frozen controls

Strict-load each accepted C299 final checkpoint once;require its exact final fingerprint.
All parameters remain frozen. Full_before and full_after must reproduce the original C299 saved
raw logits at all3 tasks,all profiles,TRAIN/HOLDOUT and normal/evidence-blind/query-blind views:
maximum drift<=1e-9 and exact argmax using the accepted C284.replay_error. Compare full_before
to full_after as well. Require unchanged weight fingerprints and hook registries after every mode.
An identity,restoration,hook,weight or count failure is INVALID / RETRY SAME C300.

Do not select a branch per question or report the better of two ablations as model accuracy.
Both ablations are applied to all questions and masks. Original fixed thresholds remain
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. All mode-specific task gates
are descriptive. C300 PASS means complete valid intervention/reproduction/reconstruction ONLY,
not successful capability,Gate F,adoption or changed prior verdicts.

## Parent writer/loader and exact protection

C299 execution:1ef1436febee7b2a70b2b91cb7a5dcb2a9e04d0c.
Published log:e1013d119956a3be000667ce6ac468d7eabb8cdf.
Summary:runs/c299-v5b-core-grid-d118c6d85dfa47dbaac6ce40655b2fe6/summary.json.
Summary SHA256:d0b2c055e190a313e5abc399716e2ec0cddfb104cc447a6216f2fab0ed312851.
Parent source:fold_lm/v05_benchmarks/model_c299_core_initialization.py.
Parent blob:b97749c29217b0ad9c57a4bf61d668684e391880.
Readout source:fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py.
Readout blob:0aa8d65874f4a021e21d04948ffd0a1d5615248b.

Verify26 ordered summary hashes before C299.verify_artifacts with25 ancestors and its accepted
execution HEAD. Tail hashes are C299.parent_hashes(C298). The exact summary commits every parent
artifact descriptor. Require original diagnostic PASS,full9 cohort,components_matched/all_replays,
capability_gate_applicable=False and the exact original matrices. The parent verifier rebuilds
all previous gates and diagonal controls under its no-neural guard. Recheck canonical data hashes.
Read fold-c299-core-eval-v1 for final raw-output anchors,NOT training losses as final predictions.
Then use C299.load_bundle for fold-c299-core-models-v1 and its9 ordered trained states. The scientific
inference path invokes that actual loader;it does not initialize new trained models or omit failures.

Direct repository import C299 only;its context supplies C294 no-neural,C287 normalizer,C284
scorer/replay,C283 quad,C282 tables and original core/model modules. C299.make_grid constructs
compatible model instances before strict-loading their trained states. Instantiation has no
scientific forward and does not constitute training. All640 parent source pins/1176 protected
inputs remain checked,including actual repository-local context/helper modules and exact C278.
Add OWN6 plus9 parent inputs:source646/protected1191. Accepted files remain immutable.

## Reporting,workload and persistence

9 saved models *4 passes *81 forwards per pass =2916 model forwards;279936 row presentations;
11664 core calls. Training0;9 model-state loads;one existing checkpoint bundle read;new checkpoints0;
network0. This is NOT a zero-inference saved-log audit. The mandatory operational smoke uses one
real trained state and5 forward calls outside the separately counted scientific workload.
Operational regression fixtures and recursive old-artifact verification are likewise separate.

Report36 model/mode results,216 model/mode/task/split partitions,and108 ablation-vs-baseline
comparisons comprising46656 normal-row matches. Include exact argmax changes,rescued answers and
regressed answers with denominators;do not count wrong-to-wrong changes as rescues. Keep masked
gates,normal NLL and collapse from the exact old normalizer. Nine reproduction receipts preserve
before/after/restoration errors. All4 mode-specific task matrices are retained.

Outputs:intervention-plan.json,intervention-evaluations.pt,measurements.json,validation-summary.json,
plus summary.json. This child does NOT write new dataset copies or trained-models.pt. Numerical
archive schema:fold-c300-readout-terms-eval-v1;all9 records keep all4 final raw-output passes,
per-mode hook attestations,original final fingerprints and reproduction errors. Raw float64 logits
have573308928 payload bytes across all passes;archive size includes overhead. No memory/speed claim.
Full tensors/maps remain local/ignored. The console emits a compact receipt and aggregates.
Postcheck validates every output hash/size and independently recomputes scores,comparisons and
original-baseline agreement from the archive under the inherited no-neural guard.

## Authoring/runtime gates

Own40/modules185/loaded4598/focused4597;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30.
Commit/re-fetch/review OWN6 before activation and command release. Test actual dynamic C278 class
hook ordering using its accepted class AST with a controlled backbone,plus numerical intervention
and failure cleanup tests. That fixture is not actual FOLD capability. Test explicit UTF-8/CP932,
parent dispatch,counts,CLI,suite IDs and production call ordering. Runtime Validate requires all26
real parents,pins,the actual trained-model intervention smoke,own40 and full4597 regression.
Preserve dispatcher/launcher/runner ParseFile. Validate failure skips science/publication.
Any scientific integrity issue retries SAME C300. C301 waits for C300 formal judgment.
