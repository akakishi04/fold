# C179 acceptance — syntax routing alone did not improve the joint endpoint

Judged 2026-09-18 JST. V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
Read the unchanged C179 preregistration and experiment conversation handoff protocol.

## Formal verdict

**C179 ACCEPTED VALID NEGATIVE. Gate E NOT PASSED. C180 NOT REGISTERED here.**
C178/C176 remain ACCEPTED VALID NEGATIVE. C174/C175/C177 keep their scoped PASS.
All earlier results, checkpoints, scientific conditions and source files remain unchanged.
Do not repeat C179 with altered seeds, steps, topology, thresholds or selected cases.

## Execution validity and identity

Execution HEAD ec1db352749e4931d59aa7a21f1766347cbf918e.
Source/artifact precheck PASS; 1089/1089 focused tests in 18.163 seconds.
Six completed models, seeds179001/179002/179003, SEQUENCE_LINKS versus TREE_LINKS.
Each pair has identical initial parameter hashes and sampled row-index schedule hashes.
Same bound input, ordinary unweighted CE, 2000updates/model, batch256, Adam0.001,
CPUfloat32/two threads; torch2.10.0+cu130, NumPy2.3.5.
25726 parameters and177596 dense forward MACs/row in EACH arm; shared cell used seven times.
12000 training forwards/updates,84000 batch-cell calls,3072000 sampled rows.
56376 pilot and254664 training-resubstitution predictions;312 inference batches/2184 cells.
51840 prepared rows,207360 visible-fact lookups,414720 copies. Six new checkpoint
roundtrips; historical checkpoint loads0. Acquisition/proof/evidence/network all0.
64 historical source pins,105 protected input paths,10 output artifacts.
Runner postchecks: protected inputs preserved; tracked tree clean; execution HEAD preserved;
run_execution_valid=True. Existing C145 warning is in passing regression,not invalidity.
Benchmark wall clock229.15039540000726s is not serving latency or a speed comparison.

Report: runs/c179-v5e-shared-graph-49f8f07577d74b8dace13a677691fe99/summary.json
Report SHA256:ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b
Uploaded log397367bytes;SHA25672067532bc30ae65a74bad6969f68cdec9315871b1c7f7fbca8a37bad27ab0f3.
Canonical reconstructed summary202097bytes;hash matches the runner report.
shared-graph-plan.json8111bytes;559038d8a7662b9b44b2f56ad2d1cca5c38a1e0e434a132961faa53bcf18594b.
shared-input-audit.json253bytes;0e1d98a059d85bd51917d90d0a30b26c9ec5ebabc400615bc242bc4d4e5bfa17.
Scientific manifest8e4fce52612b7e01fbd4f9f58ccb3dd8eee1bfbea16dd9d50ef5f39aca712456.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Parent C178 SHA25619bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8.

## Deciding metrics

Percentages below. Primary is the equal mean BA for missing counts1/2/3.
The controlled comparison is TREE versus SEQUENCE within C179,not versus old flat models.

|Seed|Primary sequence|Tree|Original group-macro sequence|Tree|
|---|---:|---:|---:|---:|
|179001|55.997137|55.945188|72.390953|73.083223|
|179002|56.195368|55.837081|74.826300|73.660051|
|179003|55.576182|54.993144|73.862668|72.230882|

|Seed|Count1 NEEDS recall sequence -> tree|Count3 SUFFICIENT recall sequence -> tree|
|---|---|---|
|179001|243/768 ->264/768|31/312 ->21/312|
|179002|264/768 ->264/768|3/312 ->24/312|
|179003|183/768 ->132/768|18/312 ->43/312|

Five-condition vectors in preregistered order:
179001:[false,true,true,false,true];179002:[false,false,false,true,true];
179003:[false,false,false,true,true]. All three primary comparisons fail;none passes
all conditions. The exact tie in179002 count1 is not an improvement. Both aggregate TREE
recalls exceed0.5 in all seeds,which does not cancel the other failures.

## Secondary results, not replacement gates

Pilot within-count AUC sequence ->tree:
1790010.5981094343->0.5957367053;
1790020.5970071903->0.5924469594;
1790030.5970062917->0.5970316035.
Same-visible-key AUC0.5944899488->0.6000350343,
0.5993403885->0.5997209336,0.6026324055->0.5998417416.
No consistent ordering improvement rescues the classification gate.
Pilot rescues/new errors127/123,102/119,213/204;TRAIN570/515,521/429,860/956.
Row-level error count and group/count-balanced metrics weight examples differently;
small row-accuracy gains in two seeds do not invalidate their primary declines.

TRAIN mixed-count BA improves in all three:
0.6174360733->0.6210722396;0.5960514463->0.6249539340;0.6048092939->0.6088923675.
TRAIN groupmacro0.7569708382->0.7603757601,
0.7706691749->0.7667367963,0.7591935651->0.7470182977.
The training set is not solved either;do not characterize this solely as evaluation-only
failure or automatically prescribe more width or updates. Pure counts0/4 stay perfect
and their absent-class BA/AUC remain null.

## Scientific interpretation and confounds

Under the specified data,backbone,root-only supervision and workload,syntax-child links
did not yield the required joint classification improvement over sequential state links.
This does not prove that composition is irrelevant,that tree networks cannot solve
necessity,or that the FOLD shared core is incapable. It rejects this bounded comparison.
Both arms used the same seven cell applications and dense MAC budget;historical flat
models used substantially fewer MACs,so no cross-experiment efficiency attribution follows.
Routing and visible binding are handwritten;no hidden values or Boolean evaluator enter
model inference. Same four repeatedly inspected DEVELOPMENT groups,not independent holdout.

The source has a concrete additional path: readout receives root64 plus header4,facts16,
runtime10. Raw facts therefore reach the final linear head without passing through the
syntax composition. That route may support fact-pattern shortcuts,but its actual causal
role is UNTESTED. A future isolated ablation can mask just this redundant facts16 readout
path while keeping the facts visible at leaves and retaining both arms' tree computation.
This is not a claim that the path is a bug or that such an ablation will succeed.
Existing ordering/error tables are sufficient;no repeated unchanged-score audit is needed.

## Review scope and disposition

Reviewer reconstructed the full summary/hash and independently recomputed312 confusion
metric tables,72 ordering tables,12 exact AUC means,36 exchange tables,all per-count/group
sums,three five-condition verdicts,paired fit hashes and workload/cell counters.
1089 test-name entries and24 progress lines agree with the recorded complete workload.
The10 separate output artifacts,raw data/logits/checkpoints and shared-input-audit bytes
were NOT independently reread;user1089tests and six full fits were NOT rerun.
Preserve all results. No C179 rerun or deployment. C180 remains unregistered at this
acceptance-only boundary;the next scientific design requires separate preregistration.
