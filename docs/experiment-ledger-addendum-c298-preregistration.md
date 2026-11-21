# C298 preregistration — backbone/reader initialization grid

Experiment:C298-v5b-component-initialization-grid. Stage:V5-B-COMPONENT-INITIALIZATION-GRID.
Acceptance base:fe56cfdd4d393ae5d6a3d268eaa66f19a0b5a578.
C297 ACCEPTED PASS (diagnostic integrity only);C296 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C299 NOT REGISTERED.

## One question and fixed scope

Does the C297 fixed-order outcome track backbone initial parameters,added-reader initial parameters,
or their combination? Cross ALL three original initialized component sets297001/297002/297003.
Rows choose backbone;columns choose added reader;all9 cells run. This is a targeted follow-up using
known factor levels,NOT fresh-seed replication or a post-hoc replacement for C297. No cell is selected
for production. Fix order297101,the first originally registered C297 order,for every cell;do not
choose the least-error order297102. Results at one order cannot establish order-independent effects.

C297 initial297002 failed quad at all3 orders,but its normal errors varied18/1/18. Other initials
passed all3. Thus gate association motivates component separation,not a claim that order is irrelevant.
All9 C297 cells fitted seen-length normal TRAIN/HOLDOUT;historical TRAIN failures were not reproduced.

## Component boundary and unchanged architecture

Use actual C278 MeanFinalDualReadout,14256 independent parameters,48-token context,CPUfloat64.
Its complete registered module boundary is backbone(13488) plus read(768). The latter is the added
query/key/output residual reading head,NOT the model's entire final vocabulary classifier. The
vocabulary output and other backbone components remain in backbone. Reassigning read changes only
its untrained parameter values;no architectural layer,input parser,mask or decoder is introduced.
Create the three normal reference initial models. Deep-copy a row's full model,replace its read
module with an independent deep-copy from the column's reference,and train all parameters.
All state keys must belong to backbone.* or read.*;same component fingerprints per row/column;
three distinct component fingerprints per factor;nine independently stored models. Diagonals
must match the complete normal reference initial state exactly. No trained states are spliced.

## Training and exact diagonal controls

Use the exact C297 blocked schedule for order297101:200epochs*4updates,96 intact TRAIN query pairs,
24pairs/48rows per batch. Private shuffle seed=order+297000+epoch;length=epoch%2;profile=epoch%3.
Every row100 exposures per trained length. Fit global RNG597000 fixed in all cells. Ordinary mean
CE only;one AdamW800steps,lr.005,betas(.9,.999),eps1e-8,weight_decay0,clip1,error_if_nonfinite=True.
No LR decay,auxiliary loss,early stop,restarts or extra data. Only normal two/three-character TRAIN;
HOLDOUT,quad and ablated inputs are evaluation-only. Quad TRAIN is a value split at an untrained length.
Models receive prefix tokens and existing zero task IDs,not labels or component/seed metadata.

The own fit loop preserves C297's arithmetic and optimizer sequence;only progress labels and cell
metadata differ. For the three diagonal cells,retrain from scratch and require exact initial AND
final fingerprints,exact800 pre-update CE values,and identical stored event tensors/hash against
C297's corresponding order297101 records. Compare every original task/view's final logits with
C284.replay_error (<=1e-9 and exact argmax). A diagonal mismatch is INVALID,not a capability result.
This reproduces both successful and failed parent cells;it does not selectively retry a failure.
All diagonal controls are executed anew and their cost included. No intermediate checkpoint choice.

## Scoring,reporting and limits

Freeze each trained model;evaluate all original two/three/quad normal,evidence-blind,query-blind
views. Strict-load all9 archived states and replay every view. Original thresholds remain
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
C298 PASS means complete diagnostic grid,component provenance,diagonal reproduction,strict replay
and saved-result reconstruction ONLY. Individual capability failures remain failures;no new easier
capability gate. No C297/C296 verdict or Gate F changes. No best-component deployment selection.

Report9 cell results,three3x3 full-task pass matrices,54 TRAIN/HOLDOUT partitions and12 numeric
accuracy/final-NLL grids. Use the existing C297 finite-grid decomposition,renaming row effects to
backbone and column effects to reader. These are descriptions of these9 dependent outcomes,
not population variance,statistical significance,hidden-state causal mechanisms or a universal
initialization remedy. Whole backbone includes several mechanisms;an effect does not isolate one.
A novel off-diagonal success cannot establish general robustness or benefit at other orders.

## Exact parent writer/loader and protection

C297 execution:18576c2df5f928d5904bd99bd39a2de58c5736da.
Published log:d541b5a370adbe4b80064294076d98be7c2a75d5.
Summary:runs/c297-v5b-init-order-1e8b2002a1e142db81c0c8b5d51a1b4a/summary.json.
SHA256:9bfceee367a11edfe9ae5b62f381cdaf183ef357109f5dff7b345a11e3180aba.
Parent source:fold_lm/v05_benchmarks/model_c297_init_order_grid.py.
Blob:49497d433c6302cd2a65635564f254edbf169104.
Verify24 ordered summary hashes BEFORE calling exact C297.verify_artifacts with23 ancestors and
accepted execution HEAD:C297,C296,...,C274. Tail hashes use immutable C297.parent_hashes(C296).
The exact summary commits its8 artifact descriptors. Require diagnostic PASS,all_replays and
grid_matched;exact matrices:seen tasks allTrue,quad [[True,True,True],[False,False,False],[True,True,True]].
Read verified canonical dataset/triple/quad JSONs and recheck SHA256s. Load evaluation archive
fold-c297-grid-eval-v1;require complete original grid. Retain all3 records whose order_seed=297101
as reproduction anchors,not initialization weights. Saved records contain final logits and pre-update
minibatch losses,not hidden activations or optimization state. No parent checkpoint is loaded to train.

Direct repository import C297 only. Its context provides C296 pair/render helpers,C294 no-neural
scope,C287 normalizer,C284 evaluator/replay_error/replay_one,C283 quad scorer,C282 tables and core.
C297.check_fit verifies its unchanged order/RNG/schedule contract. Its analyze is NOT reused because
C298 uses backbone_seed/reader_seed and a different factor grid. C287 normalization accepts labels;
C284 replay consumes final_sha256/raw and appends strict replay fields,without assuming seed/arm.
Retain all628 inherited source pins and1146 inputs;check actual repository-local context/core module
coverage and exact parent blob. Add OWN6 plus9 parent files:source634/protected1161. No old file edits.

## Workload,persistence and execution

9 newly fitted cells*800=7200 updates;345600 training-row presentations. Each cell800 training+
81 final evaluation+81 archive replay=962 forwards. Totals8658forwards,485568row presentations,
34632core calls. One9-state checkpoint bundle write/load;9 model-state loads;network0. Reference
initial templates and parameter copies involve no neural forward. Diagonal comparison reads already
computed outputs and adds no forward. Operational preflight/tests and old-parent reconstruction
are separate. This diagnostic DOES train9 models;it is not a zero-neural saved-only audit.

Eight outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Model bundle schema
fold-c298-components-models-v1;eval schema fold-c298-components-eval-v1. Save component initial hashes,
full800 CE/event traces and frozen final outputs. Postcheck reconstructs all scores and diagonal
agreements from saved outputs under no-neural guard. Full arrays/weights/maps stay local/ignored;
console has compact receipt and aggregates. Every artifact hash/size is checked.

Own32/modules183/loaded4526/focused4525;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62.
Commit/re-fetch/review all6 OWN before activation or execution command. Test actual UTF-8 inventory
under CP932-default emulation;verify Python/embedded blocks,globals,CLI indices and run ordering.
Mandatory Windows Validate:24 parents,634/1161 protection,real tokens/component grid/diagonal initial
fingerprints and schedules,own32 and full4525. Preserve dispatcher/launcher/runner ParseFile chain.
Validate failure skips science/publish;any scientific integrity issue retries SAME C298 with fixed
conditions. Complete valid diagnostic PASS does not alter any capability gate. C299 remains unregistered.
