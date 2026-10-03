# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C297 ACCEPTED PASS (diagnostic integrity only). C298 ACTIVE / NOT YET JUDGED. C299 NOT REGISTERED.**
C296 remains ACCEPTED VALID NEGATIVE. C298 is the unique ACTIVE component-initialization diagnostic.
Latest accepted scientific execution:18576c2df5f928d5904bd99bd39a2de58c5736da.
Latest accepted published log:d541b5a370adbe4b80064294076d98be7c2a75d5.
Do not rerun C297 or promote its diagnostic PASS to a capability gate.

## Latest accepted evidence — C297

Acceptance:docs/experiment-ledger-addendum-c297-c298.md.
Acceptance commit:fe56cfdd4d393ae5d6a3d268eaa66f19a0b5a578.
Summary:runs/c297-v5b-init-order-1e8b2002a1e142db81c0c8b5d51a1b4a/summary.json.
Summary SHA256:9bfceee367a11edfe9ae5b62f381cdaf183ef357109f5dff7b345a11e3180aba.
Own32/focused4493 PASS;source628/protected1146;run_execution_valid=True.
Manifest6fc874b494cdc0b9dea5c55b57e482ef8eca50cc9790abc62840cf29e52bb903.
Two/three all9 pass. Quad rows(initial297001..3) x columns(order297101..3):
[[True,True,True],[False,False,False],[True,True,True]].
Initial297002 quad normal errors vary18/1/18 with order;do not call order irrelevant.
Its TRAIN-value/HOLDOUT-value counts are566/280,576/287,565/281 out of576/288.
All seen-length normal answers are correct in all9 cells;earlier TRAIN failure was not reproduced.
The other6 cells have864/864 normal quad answers correct and full masked/task gates passed.
Finite-grid association is not population variance,an independently replicated mechanism,or an
architectural diagnosis. No old gate changes or best-seed deployment.

## Active C298 — backbone/reader component initialization grid

Experiment:C298-v5b-component-initialization-grid. Stage:V5-B-COMPONENT-INITIALIZATION-GRID.
Registration:docs/experiment-ledger-addendum-c298-preregistration.md.
Design:docs/v5b-component-initialization-v0.1.md.
Review:docs/c298-post-authoring-review.md.
Acceptance base:fe56cfdd4d393ae5d6a3d268eaa66f19a0b5a578.
Authoring/review target:0705f8022c060d30bc04a52d18531f33d60e1d6c.

One question:at the first original C297 order297101,does outcome follow backbone initial parameters,
added-reader initial parameters,or their combination? Cross ALL3 original component levels297001,
297002,297003 into9 cells. Previously observed levels make this a targeted follow-up,NOT fresh-seed
replication. Do not select only failed/successful levels or deploy a winning combination.
One fixed order cannot establish order-independent component effects. It is not order297102,
which happened to leave fewer errors. No best-order selection or trained-model continuation.

Actual C278 MeanFinalDualReadout:backbone13488 parameters plus added read768=14256,48-token context.
Read is the query/key/output residual reader,not the entire vocabulary classifier. Construct all3
normal reference initial models,deep-copy the row model and replace read with an independent copy
from the column reference. Only UNTRAINED weights are combined. Train all parameters. Assert exact
module/state boundary,same component fingerprints per row/column,distinct3 levels,no shared storage,
and exact normal initial state on each diagonal. Architecture/decoder/input masks remain unchanged.

All9 cells use exact C297 blocked schedule order297101,private shuffle order+297000+epoch,
200epochs*4updates,96 intact pairs,24pairs/48rows per update,length=epoch%2,profile=epoch%3.
Each row receives100 exposures at each trained length. Global fit RNG597000 fixed in every cell.
Ordinary mean CE;one AdamW800steps,lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1.
Only normal two/three-character TRAIN;no HOLDOUT,quad,masked examples,auxiliary loss or LR decay.
Tokens and existing zero task IDs enter forward,not labels,component identities or metadata.

Same-component diagonals retrain from scratch and MUST reproduce C297 order297101:exact initial/
final fingerprints,all800 CE values,identical events/hash,and all task/view logits<=1e-9 with exact
argmax via C284.replay_error. Both old successes and failure remain controls. A mismatch is INVALID;
do not relax this requirement or infer scientific improvement from mismatched reproduction.
Reference anchors are saved outputs,not initialization weights. No additional forward for comparison.

Freeze every final model;score old two/three/quad normal/evidence-blind/query-blind gates. Strict-load
all9 archived states and replay every view. Thresholds stayaccuracy.90,query_pair.80,evidence_drop.35,
query_drop.35,two_order.80. PASS means diagnostic completeness,component provenance,diagonal agreement,
replay and saved reconstruction ONLY. Capability failures remain separately visible. Gate F unchanged.
Report9 cell results,3 task matrices,54 partitions and12 numeric accuracy/NLL grids. Existing C297
finite-grid decomposition is relabeled backbone/reader;do not claim population variance or a unique
internal cause. Whole backbone includes several mechanisms;further isolation is not already proven.

## Parent contract,workload and protection

Verify24 summary hashes before exact C297.verify_artifacts with23 ancestor paths and its accepted
execution HEAD. Its exact summary seals all8 output descriptors. Require diagnostic PASS,complete
old9-cell grid and the exact original task matrices. Read only verified canonical data JSONs and
fold-c297-grid-eval-v1 saved records. Three order297101 rows are the immutable reproduction anchors.
Sole direct import C297;reuse C296 pair/render,C294 no-neural,C287 partition,C284 replay/evaluate,
C283 quad,C282 tables/core through inspected context. C297.check_fit is reused;its grid analyze is not.
Retain628 parent source pins and1146 inputs plus context/core module coverage;add OWN6 and9 parent
summary/artifacts:source634/protected1161. No accepted file or dependency waiver.

Work:9models,7200updates,345600training rows,8658forwards,485568row presentations,34632core calls,
one9-state checkpoint bundle write/load,9strict state loads,network0. This diagnostic trains9 new
models;it is NOT saved-only. Operational tests/preflight and inherited reconstruction are separate.
Eight outputs plus summary:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c298-components-models-v1 and fold-c298-components-eval-v1. Retain component initial hashes,
full800 CE/events and final logits. Full maps/tensors remain local/ignored;console compact aggregates.
Own32/modules183/loaded4526/focused4525;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local behavioral fixtures).
All6 OWN files re-fetched at0705f8022c060d30bc04a52d18531f33d60e1d6c;whole-file blobs matched6/6.
Post-match normal own32 PASS in7.268s;whole-suite CP932-emulated own32 PASS in8.095s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;Python2 files and3 embedded blocks compile;unresolved globals0;
UTF-8/no-NUL;manifest matches. Actual toy800-step loop agrees with an independent reference on all
losses/weights;one-optimizer/fixed-RNG tests pass. Component grid,diagonal mismatch,loader/pin guards,
run ordering,bundle replay dispatch,persistence/tampering and explicitUTF-8 checks pass.
Toy inputs encode targets for software-control tests. Parent archives,Git,models/scorers and suite
members are substituted where needed;this is NOT FOLD capability or the actual4525-test suite.
Real Windows24-parent verification,pins,actual component/diagonal preflight,PowerShell ParseFile,
full4525 suite and9 real FOLD training/scoring/replay cells remain mandatory local gates.
Activation must preserve all6 reviewed OWN blobs and all accepted files/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C298 -> Validate(24parents,634/1161 protection,
real component grid/diagonal initial hashes and schedule,own32,focused4525) -> authoring_runtime_preflight
PASS -> Execute(9cells*800updates,old-diagonal reproduction,strict replay,grid reconstruction) -> publish.
Validate failure skips science/publication. Scientific integrity or diagonal mismatch retries SAME C298.
Do not change factor levels,order,cohort,LR,budget,thresholds or select successful cells after results.
C299 is unregistered until C298 formal judgment. Gate F remains NOT PASSED.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c297-pre-acceptance.md.
Git blob28b902f8b9d1da261638b14a492cb2a19d3b1c21. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
