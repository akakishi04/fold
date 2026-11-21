# C299 preregistration — recurrent-core/remaining-backbone initialization

Experiment:C299-v5b-core-initialization-grid. Stage:V5-B-CORE-INITIALIZATION-GRID.
Acceptance base:315e24172119cd85f040def1ca01a7e4c6a0dfed.
C298 ACCEPTED PASS (diagnostic integrity only);Gate F NOT PASSED;C300 NOT REGISTERED.

## One question and comparison

Does the fixed-reader/fixed-order outcome follow the initialized recurrent core,or the remainder
of the initialized backbone,or their combination? C298's quad full-gate matrix followed backbone
rows,but reader choices changed the failed row's error count2/18/14. Reader is not irrelevant.
Cross all three original sets297001/297002/297003 for each factor. Rows=remaining backbone;
columns=recurrent core. Fix additional reader297001 and order297101,the FIRST registered levels,
not a search for a winning cell. All9 cells train from scratch. This is a targeted follow-up on
known levels,not independent replication,robustness proof,or a fresh best-initializer search.

## Exact component partition

Actual C278 MeanFinalDualReadout remains unchanged:14256 parameters,48 tokens,CPU float64.
Backbone13488 partitions into backbone.core3328 and all other backbone parameters10160;
additional read768 is fixed across cells. C260's unchanged full/core-free source establishes the
3328-parameter core boundary. C278 executes that core and reads pre-core local states separately.
This experiment changes only UNTRAINED parameter values,not core presence,route count,architecture,
readout rule or masks. The remainder includes all other backbone components,not just its encoder.

Construct ordinary reference initial models for all3 seeds. Independently copy a row model,
replace its core with an independent copy from the column reference,and replace read with the
same fixed reference reader. Require module/state boundary,parameter counts,distinct factor
fingerprints,identical fixed reader,complete state order,and no shared grid parameter storage.
Fingerprint the remainder by hashing every backbone state entry except core.*. All parameters
then train normally;no learned states are transplanted and nothing is frozen during optimization.
A component effect does not establish that the core is necessary,useless,defective or superior.

## Unchanged training and reproduction anchors

Exact C297 order297101 schedule:200epochs*4,96 intact query pairs,24pairs/48rows per minibatch;
shuffle with private Generator(order+297000+epoch),length=epoch%2,profile=epoch%3. Every logical
row is used100 times per trained length. Global fit RNG597000 in every cell. Ordinary mean CE;
one AdamW800 updates,lr.005,betas(.9,.999),eps1e-8,weight_decay0,clip1,error_if_nonfinite=True.
Only two/three-character normal TRAIN inputs;HOLDOUT,quad and masked inputs are evaluation-only.
No labels or factor metadata enter forward. No auxiliary loss,LR decay,seed selection or early stop.

The three same-source diagonals reconstruct C298's column reader297001,NOT C298's diagonal
reader=backbone. Require exact initial/final full fingerprints,all800 CE values,event tensors/hash,
and all-task/all-view logits<=1e-9 with exact argmax against those3 saved anchors. This includes
the backbone297002 failed cell (2 normal quad errors),not the18-error reader297002 cell.
Both successful and failed anchors are retrained. Any mismatch is INVALID,not a scientific change.

## Parent contract and protection

C298 execution:026dc1983cbdf7c54e6bb6ba6302f04430b17a36.
Published log:5113666bdb581526cdc0f2707e493258accbc028.
Summary:runs/c298-v5b-components-13bf02bea0764e2cb8fe8802cfa52eb7/summary.json.
Summary SHA256:a57e5f2fc3071c630b6cd083f855511b035a4d8478c91e22f86fe97c373add6e.
Source:fold_lm/v05_benchmarks/model_c298_component_initialization.py.
Git blob:a1f64f270dcba45e25168841d76113a1b195aebc.
Verify25 hashes before exact C298.verify_artifacts with24 ancestor paths and accepted execution
HEAD. Order:C298,C297,...,C274;tail hashes from immutable C298.PARENT_SHA and C297.parent_hashes(C296).
The exact parent summary seals all8 artifact descriptors. Require diagnostic PASS,all_replays,
components_matched and exact matrices:seen tasks allTrue;quad [[T,T,T],[F,F,F],[T,T,T]].
Read already-verified data JSONs,recheck canonical hashes,and load fold-c298-components-eval-v1
records. Verify complete parent components;select all3 reader_seed297001 records as immutable
reproduction anchors. They contain final outputs/fit histories,not hidden states or optimizer states.
Never treat them as initial weights. New identities are remaining_seed/core_seed.

Sole direct import C298. Its inspected context exposes C297(schedule/check_fit/decompose),C296
(pair/render),C294 no-neural scope,C287 normalization,C284 original scorer/replayer,C283 quad,
C282 tables and core bundle. Do not use C298's cohort-level analyze with the new identity fields.
Retain/check all634 source pins and1161 inputs;require actual repository-local context/core modules
in that map. Preflight also checks the actual core class implementation module's pin.
Add OWN6 plus9 parent summary/artifacts:source640/protected1176. No accepted file edits or waivers.

## Measurement and meaning of PASS

Freeze final models;score unchanged two/three/quad normal,evidence-blind,query-blind tasks.
Strict-load all9 archived states and replay every view with drift<=1e-9 and exact argmax.
Thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
C299 PASS means complete diagnostic,matching,diagonal reproduction,replay and saved reconstruction
ONLY. Capability failures are reported separately. No C298 verdict or Gate F changes.
Report9 results,3 task matrices,54 final TRAIN/HOLDOUT partitions and12 accuracy/NLL grids.
C297 additive decomposition is labeled remaining/core;one run per cell and3 levels cannot yield
population variance or significance. All cells remain;no winning combination is deployed.

## Workload,persistence and stop

9*800=7200 updates;345600 training rows;8658 model forwards;485568 total row presentations;
34632 core calls. One9-state checkpoint bundle write/load,9 strict state loads,network0.
Initial templates/copies and diagonal numerical comparisons add no model forward. Operational
tests/preflight and old-artifact reconstruction are separate. This diagnostic DOES train9 models.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c299-core-models-v1 and fold-c299-core-eval-v1. Preserve initial component fingerprints,
all800 losses/events,and all final logits. Full tensors/maps remain local/ignored;compact console.
Numerical postcheck reconstructs everything under the inherited no-neural guard.
Own32/modules184/loaded4558/focused4557;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846.
Commit/re-fetch/review all6 OWN before activation. UTF-8/CP932 checks,globals,embedded Python and
CLI indices required. Windows Validate:25 parents,640/1176 protection,real grids/diagonal initial
states/schedules,own32 and full4557. Preserve dispatcher/launcher/runner ParseFile chain.
Validate failure skips science/publication. Integrity or diagonal mismatch retries SAME C299.
No factor/order/budget/threshold changes after outcomes;C300 waits for C299 formal judgment.
