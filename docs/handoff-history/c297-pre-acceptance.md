# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C296 ACCEPTED VALID NEGATIVE. C297 ACTIVE / NOT YET JUDGED. C298 NOT REGISTERED.**
C295 remains ACCEPTED VALID NEGATIVE. C297 is the unique ACTIVE crossed training diagnostic.
Latest accepted scientific execution:3d52da4b565d05727b604560bbf60710dd9536e2.
Latest accepted published log:16d3800de33edda84b88904b805029912de4ddc0.
Do not rerun C296 or change its original all-five criterion.

## Latest accepted evidence — C296

Acceptance:docs/experiment-ledger-addendum-c296-c297.md.
Acceptance commit:8e76dbbaa2a58658b80f60e2d90ee9acbe23f8b8.
Summary:runs/c296-v5b-render-batches-653d5ee53ab747f69da1611a8fc69630/summary.json.
Summary SHA256:d48c4c6725cecdf9e15034448186fe39b7e8b86b45f7a6418c839e2536f1093b.
Own40/focused4461 PASS;source622/protected1131;run_execution_valid=True.
Manifest:b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9.
Quad blocked2/5,balanced3/5;seen tasks4/4;TRAIN direct5/4;HOLDOUT direct4/4.
Quad two rescues296001/296003 and one regression296002. Both fail296005.
Balanced296005 triple HOLDOUT80/288 versus blocked153/288;quad85/288 versus155/288.
Balanced also fails TRAIN on that seed. No uniform advantage,adoption or causal mechanism claim.

## Active C297 — crossed initialization/order training diagnostic

Experiment:C297-v5b-initialization-order-grid. Stage:V5-B-INITIALIZATION-ORDER-GRID.
Registration:docs/experiment-ledger-addendum-c297-preregistration.md.
Design:docs/v5b-init-order-grid-v0.1.md.
Review:docs/c297-post-authoring-review.md.
Acceptance base:8e76dbbaa2a58658b80f60e2d90ee9acbe23f8b8.
Authoring/review target:cd513a561ed52cca9571a959bb58c789787d9430.

One question:in a complete finite3x3 grid,does outcome variation follow parameter initialization,
example order,or the particular combination? This separates previously coupled streams without
assuming either caused C296's failures. Nine new training cells,not old checkpoint continuations.
Initial seeds297001/297002/297003 crossed with order seeds297101/297102/297103. Keep every cell.
Rows share identical initial weights;columns share identical example schedules. Three independent
parameter copies per initial group;require distinct factor levels and no shared parameter storage.
No selected-success cohort,no best-seed deployment and no result-dependent expansion.

Actual C278 MeanFinalDualReadout,14256 parameters,48-token context,CPUfloat64,2threads,deterministic.
Ordinary mean CE only and blocked homogeneous-rendering minibatches throughout. Each cell800updates,
one fresh AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1. No auxiliary loss or LR decay.
Initial seed enters only construction;private shuffle Generator uses order_seed+297000+epoch.
The remaining global fit Torch RNG is fixed597000 in ALL cells. Prior evaluation cannot change it.
200epochs*4;96 intact query pairs;24pairs/48rows per update;length=epoch%2,profile=epoch%3.
Every original TRAIN row has100 exposures at each trained length. No HOLDOUT,quad or masked inputs
are optimized. Labels and seed/order metadata never enter forward;tokens and zero task IDs only.
Persist actual int64[800,24,4] event tensors,800 minibatch CE values and initial/final fingerprints.

After training,freeze each model and evaluate all original2/3/4 tasks and masks. Strict-load9 saved
final states and replay every view with drift<=1e-9,exact argmax and unchanged fingerprints.
Original thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
C297 PASS means only diagnostic completeness,matching,replay and reconstruction. It does NOT mean
improved model capability;capability_gate_applicable=False. Even all-failed capability matrices
remain reported as failed. C296's5/5 criterion and verdict,Gate F and production adoption do not change.

Report3 task pass matrices,nine cell results,54 model/task/split partitions and12 accuracy/NLL grids.
For each numeric3x3 grid,decompose grand mean,row means,column means and residual interaction;
check SS_initial+SS_order+SS_interaction equals total centered SS. These quantities describe
only the chosen nine cells,not population variance components,p values or a unique causal mechanism.
Three fixed levels and one observation/cell form a bounded diagnostic pilot. An all-pass grid
can be uninformative about failures;do not choose harder seeds after seeing outcomes.

## Parent contract and workload

Verify23 ordered summary hashes before exact C296.verify_artifacts with22 ancestor paths and
accepted execution HEAD. Its exact summary seals eight artifact descriptors. Reconstruct all
C296 schedules and original masked/full gates;require FAIL,quad blocked2/balanced3,all_pairs_matched
and all_replays True. Only verified dataset/triple/quad JSONs feed the new cells;recheck data hashes.
Sole direct repository import:C296. Reuse its actual pair-builder/render-gather functions and
inherited C287 partition,C284 scorer/replayer,C283 quad/C282 tables through the inspected context.
New records use initial_seed/order_seed;old cohort-level analyze is never substituted for C297.
C287 normalize_task accepts seed/order as labels;C284 replay_one needs final_sha256/raw only.

All622 inherited source pins and1131 protected inputs stay checked,including actual repository-local
context/core helper coverage. Add OWN6 and9 parent files:source628/protected1146.
Work:9models,7200updates,345600training rows,8658model forwards,485568row presentations,34632core calls,
one9-state bundle write/load,9strict state loads,network0. Unlike saved-only audits,this diagnostic
DOES train new models. Operational preflight/tests and old artifact reconstruction are separate.
Eight artifacts plus summary:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Model schema
fold-c297-grid-models-v1;evaluation schema fold-c297-grid-eval-v1. Full tensors/maps stay local/ignored.
Own32/modules182/loaded4494/focused4493;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:6fc874b494cdc0b9dea5c55b57e482ef8eca50cc9790abc62840cf29e52bb903.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local behavioral fixtures).
All6 OWN files re-fetched atcd513a561ed52cca9571a959bb58c789787d9430;whole-file Git blobs matched6/6.
Post-match normal own32 PASS in4.758s;whole-suite CP932-emulated own32 PASS in4.775s.
Linux/Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;unresolved
globals0;UTF-8/no-NUL;manifest self-hash matches. Actual toy800-step fits test fixed-RNG replay,
optimizer continuity and count/freeze controls. Synthetic complete grids test matching,numerical
decomposition and the diagnostic/capability distinction. Loader/protection/run-order/persistence
and tamper tests pass. Toy inputs encode targets for software-control tests,not FOLD capability.
Parent archives,Git,old scorers/models and inherited suite members are mocked where unavailable.
Real Windows23-parent reconstruction,pins,PowerShell parsing,actual4493 suite and9 FOLD training/
scoring/replay cells remain mandatory local Validate/Execute checks. No claim they ran here.
Activation must preserve all six reviewed OWN files and all accepted code/tests/logs/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C297 -> Validate(23parent hashes,
628/1146 protection,real orders/inputs/all3 initial groups,own32,focused4493) ->
authoring_runtime_preflight=PASS -> Execute(9cells*800updates,frozen original scoring,
strict replay and grid reconstruction) -> log publication.
Validate failure skips science/publication. Any integrity failure retries SAME C297.
A valid complete diagnostic is accepted for integrity only;report all descriptive model failures.
Do not change factor seeds,budget,LR,thresholds or select successful cells after seeing results.
C298 is unregistered until C297 formal judgment. Gate F remains NOT PASSED.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c296-pre-acceptance.md.
Git blob5f738326b55e649d0d8014e12734fdb6a115dadf. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
