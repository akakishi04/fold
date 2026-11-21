# C297 preregistration — initialization/order crossed training diagnostic

Experiment:C297-v5b-initialization-order-grid. Stage:V5-B-INITIALIZATION-ORDER-GRID.
Acceptance base:8e76dbbaa2a58658b80f60e2d90ee9acbe23f8b8.
C296 ACCEPTED VALID NEGATIVE;Gate F NOT PASSED;C298 NOT REGISTERED.

## One question and scope

In a complete fixed3x3 grid,does failure follow initial weights,example shuffle,or their particular
combination? Prior experiments coupled these random streams under a single seed. This diagnostic
separates their assignments without claiming either caused the previous C296 outcomes.
Three NEW initial seeds297001/297002/297003 crossed with three NEW order seeds297101/297102/297103.
Every cell is run once,all nine remain,none is selected for deployment or as a replacement result.
There is no learned-policy candidate and no newly relaxed capability gate. C297 PASS means only
complete diagnostic execution,matching,replay and reconstruction. Even nine task failures do not
invalidate a correctly executed diagnostic. All original task passes/failures are reported separately.
This does not turn C296's3/5 into PASS. No automatic Gate F promotion or production adoption.

## Held constant and independent streams

Ordinary mean CE only;blocked rendering-homogeneous minibatches;actual C278 MeanFinalDualReadout,
14256 independent parameters,48-token context,CPU float64,2threads,deterministic algorithms.
Build each of three initial models once and deep-copy it into the three order columns;check exact
fingerprints and storage independence. No parent weights continue into this experiment.
All9 cells use exactly800 updates and one fresh AdamW with lr.005,betas.9/.999,eps1e-8,
weight_decay0,gradient clipping1 and nonfinite-error checks. No auxiliary loss,LR decay or restarts.

Shuffle uses only a private Generator seeded order_seed+297000+epoch. In200 epochs of4 updates,
shuffle96 intact TRAIN query pairs;24 pairs/48 rows per batch. Length=epoch%2,profile=epoch%3.
Canonical row and rendering multiplicities are equal across all cells:100 exposures/row/length.
Rows differ only in initialization;columns differ only in the pair-order stream. The remaining
fit-time global Torch RNG is reset to597000 in EVERY cell,not derived from either factor.
Initialization construction uses initial_seed;order_seed never enters the model constructor.
Labels,order IDs,initial IDs and pair metadata never enter model.forward. It receives tokens plus
existing zero task IDs. Tokens encode two/three-character normal TRAIN inputs only;no HOLDOUT,
quad or masked input is optimized. TRAIN-value quad means untrained length,not length4 training.

Store int64[800,24,4] actual event tensors and their hashes for every fit,800 pre-update minibatch
CE values,initial/final fingerprints and the fixed RNG/optimizer identity. Check identical initial
fingerprints within each row and identical schedule hashes within each column. Require three
distinct initial fingerprints and three distinct schedule hashes;reject duplicate factor levels.
Same initial does NOT imply same losses once the first batches differ. Do not assert a false
loss-prefix equality. Evaluation/previous cells cannot affect a later cell's fixed fit RNG.

## Measurements,limits and fixed scoring

After fitting,freeze each model;use unchanged original two/three/quad normal/evidence-blind/
query-blind evaluation. Independently strict-load all9 final states and replay every view with
raw-logit drift<=1e-9 and exact argmax,fingerprint and operation-count agreement.
Thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Report three3x3 full-task pass matrices,nine cell results and54 final model/task/split partitions,
including TRAIN/HOLDOUT normal accuracy,loss,collapse and criterion failures from the old normalizer.

For each task and value split,report the3x3 accuracy matrix and final normal-NLL matrix:12 grids.
Also report row/column means and the exact additive decomposition x_ij=grand+row_i+column_j+residual_ij.
SS_initial=3*sum(row_i^2);SS_order=3*sum(column_j^2);SS_interaction=sum(residual_ij^2).
Require their sum to equal total centered SS. Constant grids have zero SS;no division-by-zero
ratios or false explanatory percentages. This describes these chosen nine outcomes,NOT population
variance components,statistical significance or a universal causal diagnosis. One observation/cell
provides no independent error estimate;three fixed factor levels are a bounded diagnostic pilot.
A narrow all-pass grid may be uninformative about failure modes;report that rather than select
harder seeds after looking. A bad row/column is not permission to discard that seed.

## Parent writer/loader and protection

C296 execution:3d52da4b565d05727b604560bbf60710dd9536e2.
Published log:16d3800de33edda84b88904b805029912de4ddc0.
Summary:runs/c296-v5b-render-batches-653d5ee53ab747f69da1611a8fc69630/summary.json.
SHA256:d48c4c6725cecdf9e15034448186fe39b7e8b86b45f7a6418c839e2536f1093b.
Parent source:fold_lm/v05_benchmarks/model_c296_render_balanced_batches.py.
Parent blob:ae4fd7a45ec9306b1b81a82f8707269f1d88277b.
Verify23 ordered summary hashes BEFORE calling exact C296.verify_artifacts with22 ancestor paths
and its accepted execution HEAD:C296,C295,C294,C293,C292,C291,C290,C289,C288..C274. Ancestor hashes
come from source-pinned constants. Exact C296 summary seals its eight output descriptors;verifier
reconstructs normal/masked gates,render plans and paired state metadata. Require original FAIL,
quad counts blocked2/balanced3,all_pairs_matched/all_replays True and candidate_gate False.
Read already verified C296 dataset/triple/quad JSONs;check the original canonical data SHA256s.

Sole direct repository import C296. Reuse its pairs_from_rows and render_batch only after checking
actual contracts. Its context supplies C294 no-neural guard,C287 normalizer,C284 evaluator/replayer,
C283 quad scorer,C282 tables and the core bundle. Those helpers accept result labels as metadata;
new grid identity fields are not silently passed to C296's two-arm validator. New records use
initial_seed/order_seed;normalize_task receives initial seed and an explicit order label.
No monkeypatches or modifications of accepted parent modules occur in scientific execution.
Retain all622 inherited source pins and1131 protected inputs;check actual local context/core
module coverage. Add OWN6 and9 parent summary/artifacts:source628/protected1146.

## Workload and artifacts

9*800=7200 optimizer updates;345600 training-row presentations. Per cell800 training+81 final
scoring+81 strict replay forwards=962. Total8658 forwards,485568 row presentations,34632 core calls.
One9-state bundle write/load,9 strict model-state loads,network0. Operational tests and old saved
artifact reconstruction are separate from scientific neural counts. This diagnostic DOES train
nine new models;unlike prior saved-output diagnostics its neural workload is not zero.

Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus full summary.json.
Model schema:fold-c297-grid-models-v1. Evaluation schema:fold-c297-grid-eval-v1;all nine raw final
logit records and fit histories. Compact receipt and54 partitions/12 grids in console;full maps,
weights and tensors remain local/ignored. Numerical postcheck rebuilds everything from saved outputs
under the inherited no-neural guard. It does not retrain or call a model.
Own32/modules182/loaded4494/focused4493. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:6fc874b494cdc0b9dea5c55b57e482ef8eca50cc9790abc62840cf29e52bb903.

## Review/execution/stop

Commit,re-fetch all six OWN files and independently review before activation/command release.
Require explicit UTF-8 reads,CP932-default checks,Python globals/import audit,actual fixture fit
and production call-order tests. Mandatory Windows Validate:23 parent hashes/full reconstruction,
628/1146 protection,real schedules/inputs,all3 initial-model groups,own32 and full4493 suite.
Preserve dispatcher/launcher/runner ParseFile chain. Validate failure skips science/publication.
Any integrity failure retries SAME C297. Valid complete diagnostic is ACCEPTED PASS for integrity
ONLY,regardless of individual model capability scores. No deployment selection,Gate F promotion,
C296 verdict revision or changing factor seeds after results. C298 waits for C297 formal judgment.
