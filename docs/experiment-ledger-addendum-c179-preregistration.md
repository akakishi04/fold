# C179 preregistration — shared-update graph, sequence versus syntax links

V5-E. Registered after C178 acceptance commit53061385e2b2c41106727f3a9346dda5518aff97.
Repository akakishi04/fold;branch feat/sft-target-loss;use final registration HEAD.
**C179 ACTIVE / NOT YET JUDGED. C180 NOT REGISTERED. Gate E NOT PASSED.**
C178/C176 remain ACCEPTED VALID NEGATIVE. C174/C175/C177 retain their narrow PASS.
Historical sources,checkpoints,results and preregistrations are unchanged.

## One scientific question

With identical visible inputs,shared-cell weights,training schedule and dense application
counts,does wiring neural state updates along supplied syntax children improve necessity
classification over wiring the same updates along a sequential two-state history?

C178 leaf annotation did not consistently improve classification;ordering declined in
all3pairs on both splits. Its existing secondary tables already resolve that diagnostic.
The remaining composition of node states is a concrete hypothesis,not an observed cause.
Do not claim that C178 proved the flat MLP impossible or that this experiment repairs it.

Changed variable WITHIN C179:which earlier hidden states feed the two cell state inputs.
Both arms are NEW instances of the SAME shared-update architecture. This is not a tree
model versus a smaller flat MLP,not a continuation of C178 weights,and not a modification
of the production FOLD core. There is no claim of parity with the prior flat MLP's FLOPs.

## Common input and network

Both arms use unchanged C178 prepare_pair(raw)[1]:72scaled fields,with ALREADY VISIBLE
presence/raw bit copied beside referencing FACT leaves. The full fact table,original
syntax fields,negation and resources remain. This common preparation removes leaf lookup
as a BETWEEN-ARM variable;it does not promote the failed C178 annotation as a validated
improvement. No unknown fact,expected dependency,truth table or group label is provided.

Model schema c179-shared-graph-64-v1;representation c178-scaled-visible-leaf-binding-v1.
Seven nodes are visited in the original child-before-parent order. At EVERY node:

    local six fields + left state64 + right state64
      -> shared Linear134x128 -> ReLU -> Linear128x64 -> ReLU
      -> learned state64

The same unconstrained cell weights are reused exactly seven times in BOTH arms.
The final state64 is concatenated with original header4+fact table16+runtime10 and passed
to a shared-format Linear94x2 head. There is no intermediate label,truth-valued latent
constraint,programmed NOT/AND/OR operation or proof checker. Root NECESSITY is the only
training label. A zero-weight model cannot solve the task by falling through to a solver.

SEQUENCE_LINKS:node i reads states from nodes i-1 and i-2,using zero for a nonexistent
predecessor. It still receives all ordered node fields,including the true child indices;
syntax is not hidden or relabeled. This is an ordinary bounded sequential shared-update
control with two state inputs,not a sequence fed deliberately false fact values.

TREE_LINKS:internal nodes read their actual supplied left/right child states. FACT leaves
read two zero states. The supplied FACT/internal distinction chooses routing;AND versus
OR and negation are only numerical input features to learned weights,not evaluated code.
Both paths construct the same growing state bank and perform two gathers and one cell
application per node. There is no early exit,sparse zero shortcut or adaptive step count.

The topology changes path lengths,which previous states interact,and effective learning
bias. A gain supports this topology package,not a unique internal reasoning mechanism.
Known syntax routing and visible binding are handwritten. Learned AST extraction from
raw natural language is not tested. State is local diagnostic working data,not EvidenceState.

## Paired initialization,workload and accounting

Seeds179001/179002/179003. For each seed initialize one model,deep-copy its weights and
change only the arm's link rule. Both arms use the same new fit loop,ordinary UNWEIGHTED
cross entropy,Adam lr0.001,betas(.9,.999),eps1e-8,weight_decay0,amsgradFalse,foreachFalse.
2000updates/model,batch256;uniform rows with replacement,private row RNG seed+1000000.
CPUfloat32,two threads,deterministic algorithms. No C176 weighting,auxiliary labels,
checkpoint continuation,clipping,learning-rate search,early stopping or seed replacement.
All six FINAL checkpoints are saved/reloaded before ANY evaluation/resubstitution score.
Checkpoint metadata binds model schema,representation,seed,arm,steps and weight fingerprint.

Both arms have25726independent trainable scalars;the shared cell is NOT counted seven
times as seven sets of independent parameters. Both perform177596dense forward MACs
per input row:7*(134*128+128*64)+94*2. A MAC here is one multiply-accumulate,not one FLOP.
This excludes biases,activations,validation,index gathering,backpropagation,optimizer,
serialization and other Python costs. Report actual per-fit and per-inference wall clock,
not a claimed latency improvement. Forward/cell counters are diagnostic meters and never
enter the model inputs or learned state.

Historical flat C174/C178 MLP26114 uses25856dense forward MACs/row;the new shared models
have fewer parameters but about6.869times as many forward MACs. Do not attribute gains
versus HISTORICAL flat scores solely to topology or claim matched efficiency across them.
The controlled scientific comparison is TREE versus SEQUENCE INSIDE C179,where dense
workload,parameters,weights and sampled rows are aligned. Sequential mode always runs
first;runtime-order and hardware-temperature confounds preclude speed claims.

|Work|Registered total|
|---|---:|
|New initialization seeds / models|3 / 6|
|Parameters per model|25726|
|Node-cell applications per input row|7|
|Training forwards / optimizer updates|12000|
|Training batch-level cell calls|84000|
|Sampled training rows|3072000|
|Pilot / TRAIN-resubstitution predictions|56376 / 254664|
|Inference batches / batch-level cell calls|312 / 2184|
|Prepared source rows / visible-leaf lookups / copied fields|51840 / 207360 / 414720|
|New checkpoint roundtrip loads / old loads|6 / 0|
|Acquisition / proof calls / evidence writes / network|0 / 0 / 0 / 0|

Historical toy training in regression is outside these registered benchmark counters.
Reuse unchanged C174 NPZ/metadata:TRAIN36groups/524templates/42444rows;
PILOT4groups/116templates/9396rows. No data regeneration,selection or new semantic holdout.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
The four repeatedly inspected pilot groups are DEVELOPMENT data. New initialization
seeds do not make the result an independent generalization test or final Gate E result.

## Exact endpoint and disposition

Primary:equal mean balanced accuracy within missing counts1,2,3 on reused PILOT_EVAL.
Use the SAME joint gate form as C178,but the new comparison is TREE versus SEQUENCE.
For EACH seed,require ALL:
1. TREE primary strictly exceeds SEQUENCE;
2. TREE original four-group macro BA is not lower;
3. TREE count1 NEEDS recall strictly improves;
4. TREE count3 SUFFICIENT recall strictly improves;
5. both TREE aggregate class recalls are strictly above0.5.

No seed average hides failure. Ties fail1/3/4;equality is allowed only for condition2.
Raw two-logit argmax is used;no threshold selection,calibration,semantic repair or fallback.
These directional development criteria are not practical reliability or significance.
Even a PASS does not establish superiority over the historical flat MLP,FOLD-core quality,
fact/tool selection,learned proof generation,safe live execution or Gate E completion.

PASS:valid complete execution satisfying the joint gate.
VALID NEGATIVE:finite complete valid execution missing any gate condition. Preserve all
models and results;do not change topology,seeds,updates,thresholds or cases to pass C179.
INVALID / RETRY SAME C179:source/hash/schema drift,unpaired initialization/batches,
nonfinite numerical state,incomplete workload,unexpected exception or protection failure.
Restore execution validity,not scientific settings. Preserve invalid.json/completed fits.
Finite scientific FAIL writes outputs and exits0 for normal postchecks.

## Batched secondary reporting

Both TRAIN and PILOT retain raw logits/predictions,all group/count confusion matrices,
within-count and matched-visible AUC,and paired rescues/regressions by missing count.
Reuse unchanged C178 score helpers and C177 ordering/transition helpers. No second audit
is needed merely to recover these tables. Pure count0/4 BA/AUC remain null;accuracy stays
reported. Overlapping pair combinations are not independent samples. Secondary tables
cannot replace a failed primary classification gate. No candidate is deployed by C179.

## Protection and artifacts

C178 parent runs/c178-v5e-leaf-binding-e16d745f5b3242728e9c561023938719/summary.json;
SHA25619bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8.
Execution snapshot e9ee578a80b63e72a33414b62ba17a0111329ddb.
Also require C177,C176,C174 summaries and artifacts via unchanged C178 precheck.
All33prior artifacts,including old weights,are hashed by name/size;old weights are not loaded.
Historical64source pins=60C178pins+four C178own files pinned at e9ee578a.
Four new own files checked against execution HEAD;105protected input paths total.
C37 and composition fixture have additional outer runner guards. Standalone paths only.

Fresh UUID output:shared-graph-plan.json BEFORE training,shared-input-audit.json,
six checkpoints,pilot-predictions.json,training-predictions.npz(with logits and identities),
complete summary.json. Ten listed artifacts excluding summary;hashes and actual bytes kept.
Scientific manifest8e4fce52612b7e01fbd4f9f58ccb3dd8eee1bfbea16dd9d50ef5f39aca712456.
No historical source,preregistration,model or result is modified.

## Verification and run

32/32 new helper tests passed using actual new module under torch2.10CPU/NumPy2.3.5.
They check link routing with captured cell inputs/outputs,both seven-call meters,25726
parameters,177596dense MACs,finite gradients,no input/weight mutation,paired initialization
and toy fitting,raw argmax,checkpoint metadata,strict gate and malformed graph rejection.
Toy fitting uses TWO synthetic rows and TWO updates per arm,not registered pilot data.
Float32 batch-permutation output comparison uses rtol1e-5/atol1e-7,not claimed bitwise
invariance across tensor layouts. No result threshold or scientific gate was relaxed.
Python compiled;three embedded runner Python blocks parsed. These helper tests do NOT
exercise the complete inherited source/artifact chain or old C178 input preparation.
Full1089regressions,WindowsPowerShell,complete prior-module/data integration and the
registered six-model2000-update experiment have NOT been executed by reviewer.

**1089focused tests expected=1057+32,63modules**,one regression then one CPU paired batch.
Run tools/run_c179.ps1 -C178Summary ... -C177Summary ... -C176Summary ... -C174Summary ...
-ExpectedHead ... . Progress:precheck,regression,plan,seed/arm every500updates,3paired BA
lines,RESULT/POSTCHECK. Preserve full log even if scientific_status=FAIL.
Judge C179 -> ledger/handoff -> next design. **No C180 before formal judgment.**
