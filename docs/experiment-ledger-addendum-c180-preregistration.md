# C180 preregistration — direct raw-fact readout ablation

V5-E. Registered after C179 acceptance b10984a0535a4e22acdf050b6958162a629be28f.
Repository akakishi04/fold;branch feat/sft-target-loss;use final registration HEAD.
**C180 ACTIVE / NOT YET JUDGED. C181 NOT REGISTERED. Gate E NOT PASSED.**
C179/C178/C176 remain ACCEPTED VALID NEGATIVE. All historical results are unchanged.

## One question and source-based hypothesis

Does removing the redundant raw-fact bypass to the final readout improve necessity
classification when the SAME observed facts remain available through syntax leaves?

C179 did not yield joint improvement from tree routing versus sequential routing.
Both routes still supplied root64 plus header4,facts16,runtime10 directly to the final
linear readout. Direct observation patterns can influence the answer without traversing
the composed root. This is a plausible shortcut,NOT an established cause of C179 errors.
No saved C179 predictions or weights are changed. No duplicate unchanged-logit audit.

BOTH C180 conditions use original C179 TREE_LINKS as a common experimental substrate.
This does NOT adopt tree routing or C178 bound input as proven improvements. The paired
comparison isolates one readout edge package,not tree versus sequence or a larger model.

## Exact intervention

Use unchanged C178 prepare_pair(raw)[1] and unchanged C179 SharedGraphProbe.forward.
The original cell receives the identical72-field input and executes seven tree-linked
updates. Its last hidden state is concatenated with header4,facts16,runtime10:

    root state64 | header4 | raw facts16 | runtime10
    columns0:64    64:68       68:84        84:94

Before the original Linear94x2,insert a parameter-free dense elementwise multiplier:
- DIRECT_FACTS:all94 mask entries1.
- NO_DIRECT_FACTS:entries68:84 are0;all other entries1.

Only that sixteen-coordinate block differs. Both masks multiply all94 columns;neither
arm short-circuits matrix multiplication. All original leaf inputs,child links,shared
cell weights,root state path,header and runtime information are preserved. The complete
input packet/fact table is NOT edited or erased. No unknown value,label,teacher
necessity,truth-table output,proof repair or operator evaluation is added to inference.
Fact binding and syntax routing remain acknowledged handwritten front-end operations.

The mask affects the final direct path,not the observed facts copied at referring leaves.
In this frozen dataset facts are observed or unobserved,so no unique status information
is lost only because the separate detailed fact table is masked. No claim is made for
unseen stale/conflict/status families or universal C170 packet compatibility.
The new model schema is c180-tree-fact-readout-ablation-v1;representation remains
c178-scaled-visible-leaf-binding-v1. Checkpoints bind schema,representation,condition,
TREE_LINKS,mask slice,steps,seed and weight fingerprint. Historical checkpoints stay intact.

Mask constants are an architecture setting,not learned weights or fitted thresholds.
Same parameter count does NOT establish the same effective capacity:in NO_DIRECT_FACTS,
32 final-layer weight coordinates receive zero gradient because their inputs are zero.
The intervention changes a redundant information route,optimization and direct linear
expressivity. A positive result supports this package,not a unique causal shortcut story.
The root can still encode count-based heuristics;masking does not guarantee logical use.

## Fixed model,training and counts

Use unchanged C179 model class,cell,tree routing,fit and predict functions. The readout
is wrapped by the same mask module in both conditions. DIRECT_FACTS reproduces the
unmasked forward arithmetic under identical weights;historical seed results are not replayed.
25726 stored independent trainable scalars per model. Shared cell134->128ReLU->64ReLU,
seven applications;final dense head94->2. Same177596 dense forward MACs/row,plus94 scalar
mask multiplications/row in BOTH conditions. Costs exclude gradients,optimizer,gathers,
validation,mask allocation and Python overhead;record per-fit/inference wall clock.
Neither nominal parameters nor dense-MAC parity proves identical wall-clock or VRAM.

Seeds180001/180002/180003;two fresh models per seed,six total. Exact paired initial
weight fingerprints and sampled row-index schedules. Both use unchanged graph.fit:
ordinary UNWEIGHTED CE,Adam lr0.001,betas(.9,.999),eps1e-8,weight_decay0,
amsgradFalse,foreachFalse;2000updates/model,batch256,CPUfloat32,two threads,
deterministic algorithms,uniform-with-replacement row RNG=seed+1000000.
No extra steps,width,auxiliary targets,loss reweighting,early stopping,seed replacement,
calibration or threshold tuning. All six FINAL checkpoints saved/reloaded BEFORE scoring.

Reuse C174 original NPZ and metadata,not regenerated data:
TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Only TRAIN inputs/labels enter fitting. Same repeatedly inspected four pilot groups are
DEVELOPMENT data;new initialization seeds do not create an independent holdout.

|Work|Registered total|
|---|---:|
|New seeds/models|3/6|
|Parameters per model|25726|
|Training forwards/updates|12000|
|Training batch-cell calls|84000|
|Sampled training rows|3072000|
|Pilot/TRAIN predictions|56376/254664|
|Inference batches/batch-cell calls|312/2184|
|Readout mask calls,training plus inference|12312|
|Prepared original rows/visible leaf lookups/copied fields|51840/207360/414720|
|New checkpoint roundtrips/historical checkpoint loads|6/0|
|Acquisition/proof/evidence/network calls|0/0/0/0|

Each mask has a diagnostic call counter,not a model input or serialized learned parameter.
Counters are checked against real parent forward counters. Historical toy fits inside
regression are separate from the registered experiment workload.

## Exact decision,not a retrospective relaxation

Use the SAME joint gate form as C179,now comparing NO_DIRECT_FACTS versus DIRECT_FACTS.
Primary:equal mean balanced accuracy within missing counts1,2,3 on reused PILOT_EVAL.
For EACH of the three pairs require ALL:
1. no_direct primary strictly improves;
2. original four-group macro BA does not decline;
3. count1 NEEDS recall strictly improves;
4. count3 SUFFICIENT recall strictly improves;
5. both aggregate no_direct class recalls strictly exceed0.5.

No seed average hides failure;ties fail1/3/4,equality allowed only by2. The network's raw
argmax is the decision. No rule postprocessing,answer filtering or selected threshold.
PASS supports only this readout intervention in the fixed diagnostic setting,not useful
absolute reliability,FOLD core quality,logical mastery or Gate E completion.
VALID NEGATIVE:valid finite complete execution misses any condition. Preserve all models
and results;do not retune mask,seed,steps,loss,cases or threshold to pass under C180.
INVALID / RETRY SAME C180:source/hash/schema drift,nonfinite state,unpaired fitting,
incomplete work,unexpected exception or protection failure. Restore execution validity,
not scientific conditions. Preserve invalid.json and completed fits. Finite FAIL exits0.

## Batched secondary reporting

Save all TRAIN and PILOT raw logits/predictions,group/count confusion matrices,both
recalls,ordinary accuracy,within-count and same-visible-key AUC,and paired errors rescued
or newly introduced by missing count. Reuse unchanged C178/C177 scoring helpers.
Pure count0/4 absent-class BA/AUC remain null;accuracy is retained. Overlapping pairs are
not independent samples. AUC cannot replace a failed classification gate. No deployment.

## Protection and output

C179 parent runs/c179-v5e-shared-graph-49f8f07577d74b8dace13a677691fe99/summary.json;
SHA256ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b.
Execution snapshot ec1db352749e4931d59aa7a21f1766347cbf918e.
Also require C178,C177,C176,C174 summaries and artifacts via unchanged C179 precheck.
All43prior artifacts,including old checkpoints,are HASHED only;none of those weights loads.
Historical68source pins=64C179pins+four C179own paths pinned at ec1db352.
Four C180own files checked against current HEAD;120unique protected input paths.
C37 and composition fixture receive additional outer guards. Standalone paths only.

Fresh UUID output:fact-bypass-plan.json BEFORE training,readout-mask-audit.json,
six checkpoints,pilot-predictions.json,training-predictions.npz with logits/identities,
complete summary.json. Ten artifacts excluding summary;hashes and byte sizes saved.
No historical source,preregistration or artifact is altered.
Manifest SHA25622168a208e57615467b3d592cf1c72b27b286dbe0e8a24850bbc143b9da0e442.

## Verification / execution limits

28/28 new helper tests passed using actual C180 module and a local transcription of the
fetched C179 model/fit/predict source definitions. That review environment is NOT a full
repository checkout or a Git-blob-identical copy of the entire parent module. Its missing
historical regression-list dependency is mocked only for the additive-list unit test.
No claim of complete old-module/artifact integration is made from these helper tests.
They cover exact direct-control forward parity,mask span,root/leaf preservation,gradients,
25726parameters,both TREE modes,seven cell calls,mask meters,pairing,two-row/two-update
toy fitting,raw argmax,checkpoint binding and strict per-seed gate. PyTorch2.10CPU/NumPy2.3.5.
No registered data scores or six-model fits were computed during review.
Two new Python files compiled;three embedded runner Python scripts parsed. Full1117tests,
WindowsPowerShell,complete source/artifact chain and formal training remain UNEXECUTED.

**1117 focused tests expected=1089+28,64modules**,one regression then one paired CPU batch.
Run tools/run_c180.ps1 -C179Summary ... -C178Summary ... -C177Summary ... -C176Summary ...
-C174Summary ... -ExpectedHead ... . Progress:precheck,regression,plan,seed/arm500updates,
three paired mixed-count BA lines,RESULT/POSTCHECK. Preserve full log on finite FAIL.
Judge C180 -> ledger/handoff -> next design. **No C181 before formal judgment.**
