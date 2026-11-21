# C176 preregistration — missing-count-conditional training loss

V5-E. Registered after C175 acceptance commit847472a9f38f664b276675543935254326d45af7.
Repository akakishi04/fold;branch feat/sft-target-loss. Use final registration HEAD.
**C176 ACTIVE / NOT YET JUDGED. C175/C174 remain ACCEPTED PASS. C177 NOT REGISTERED.**
**Gate E NOT PASSED.** All historical negatives/results/preregistrations stay unchanged.

## Scientific question / rationale

Can balancing TRAIN class loss within each missing-count stratum reduce C175's count1
critical-information misses and count3 unnecessary-observation judgments, while preserving
the original group-macro endpoint, under the same model capacity and training workload?

C175 showed syntax information is useful versus its registered frequency reference, yet
visible models largely prefer SUFFICIENT with1missing and NEEDS with3missing. The same
pattern exists in training resubstitution. Frequency-biased training incentives are a
candidate explanation, NOT a proved internal mechanism. This is a targeted intervention,
not another unchanged-source diagnostic or an automatic capacity/steps increase.

Changed scientific variable: fixed per-example TRAIN loss weights only.
BOTH arms see the full ordered syntax, identical observations and resources. Same model
class, parameter count, scaling, initialization within seed, exact row-index schedule,
optimizer, updates, batch size and raw argmax evaluation. No old checkpoint continuation.
This new development design follows inspection of C175 and reuses its four pilot groups;
new initialization seeds do NOT create an independent semantic holdout or final Gate E test.

## TRAIN-only weighting, no resampling or inference correction

m = number of unobserved facts, from the original presence fields48,52,56,60.
y0 = SUFFICIENT; y1 = NEEDS_OBSERVATION. Counts are exclusively from42444 TRAIN rows.
For a stratum containing both classes, w(m,y)=N_m/(2*N_m_y).
For a pure stratum, weight=1. No smoothing, clipping, tuning or evaluation-based estimate.

| Missing m | TRAIN y0 | TRAIN y1 | Weight y0 | Weight y1 |
|---|---:|---:|---:|---:|
|0|8384|0|1|1 (unused)|
|1|12416|4352|16768/24832|16768/8704|
|2|6048|6528|12576/12096|12576/13056|
|3|968|3224|4192/1936|4192/6448|
|4|0|524|1 (unused)|1|

UNIFORM_CE uses1 for every row. CONDITIONAL_CE uses the formula. Both execute the same
new fitting loop and reduce mean(row_weight * unreduced cross entropy), dividing by
batch LENGTH256, NOT batch weight sum. In the complete TRAIN population, each mixed
stratum gives equal total weight to each class and retains its original total massN_m.
Total population weight remains42444. Individual minibatches need not have weight sum256.
Sampling is still uniform with replacement and is exactly paired; no cases are dropped,
replicated in the stored dataset or selected from PILOT_EVAL. Relative gradient weights
change by design, so this is not a claim that optimization is otherwise identical.
The uniform objective is ordinary CE mathematically; bitwise replication of C174's old
reduction implementation or weights is not claimed. Both new arms share reduction code.

No weight, true class, teacher dependency, truth table or evaluator repair enters model
inference. The network still receives only the original scaled72 numeric features.
Input zero versus unknown remains separated. Model inference and action execution stay
separate; this experiment performs no runtime acquisition or proof checking.

## Frozen model / data / workload

Reuse unchanged C174 NecessityProbe class72->128ReLU->128ReLU->2,26114parameters and
unchanged prepare(...,TASK_VISIBLE). This is a diagnostic MLP,not the FOLD shared core.
New seeds176001,176002,176003;two newly initialized paired arms each,six new models.
CPUfloat32,2threads,deterministic algorithms;2000updates/model,batch256.
Adam lr0.001,betas(.9,.999),eps1e-8,weight_decay0,amsgradFalse,foreachFalse.
Each fit has private row RNG seed=initialization seed+1000000. Save row-schedule and
initial/final parameter hashes. Match initialization and batches exactly within each pair.
Final checkpoints only;all six saved and reloaded before ANY evaluation/resubstitution score.
No early stopping,checkpoint selection,extra updates,restarted seeds or learning-rate search.

Frozen C174 NPZ and metadata are loaded and their canonical fingerprint reconstructed;
no dataset regeneration inside the benchmark. TRAIN36groups/524templates/42444rows;
PILOT_EVAL4groups/116templates/9396rows. Same original function-permutation/complement
split. No held-out row or group enters the weight constructor or fit function.
Data SHA256 eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.

Registered totals:12000training-forward/optimizer updates,3072000 sampled examples,
56376pilot predictions,254664training-resubstitution predictions,312inference batches.
Six NEW checkpoint deserializations validate roundtrip;historical checkpoint loads0.
Actual acquisitions/proof calls/evidence writes/network0. Regression toy activity is separate.

## Endpoints and exact gate

Primary intervention endpoint: arithmetic mean of balanced accuracy for missing-count
strata1,2,3 on the same PILOT_EVAL rows, each stratum equally weighted. Both labels exist
in each. This endpoint targets mixed cases instead of benefitting from pure count0/4.
This is a NEW C176 endpoint,not a retroactive C174/C175 rescoring or replacement.

Retain original macro-group BA over ALL four pilot groups as a no-degradation guard.
Also record all per-group and count0..4 confusion matrices, both class recalls, ordinary
accuracy, raw logits/predictions and train-resubstitution scores. Pure count0/4 BA remains
null;their actual accuracy is still reported. Training scores do not decide the verdict.

**PASS requires EACH of three seed pairs to satisfy ALL conditions:**
1. CONDITIONAL_CE primary strictly exceeds paired UNIFORM_CE primary.
2. Its original four-group macro BA is greater than or equal to paired UNIFORM_CE (zero tolerated decline).
3. Its count1 NEEDS recall strictly increases versus paired UNIFORM_CE.
4. Its count3 SUFFICIENT recall strictly increases versus paired UNIFORM_CE.
5. Both aggregate class recalls remain strictly above0.5.

No averaging hides a failed seed. Equal targeted scores fail;equal original macro BA is
allowed by condition2. These are directional development criteria,not statistical
significance,calibration,a practical-use threshold or reliable autonomous control.
Improving one error by predicting NEEDS for everything does not meet this joint gate.

Valid complete execution missing any condition => **ACCEPTED VALID NEGATIVE**. Save all
six models/results and do not alter loss weights,width,steps,seeds,data,thresholds or
metric strata to obtain a PASS under this number. Finite FAIL exits0 for postchecks.
Source/hash/manifest/data drift,unpaired schedules,nonfinite numerical state,unexpected
exception,incomplete workload or protection failure => **INVALID / RETRY SAME C176**.
Retain invalid.json and completed fits;restore validity,not scientific settings.
No automatic retries for better scores. No C177 before formal judgment and ledger update.

## Parent and source protection / artifacts

Parent C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json.
SHA256 d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json.
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Verify C175 two artifacts and C174 eleven artifacts by hash/size;do not deserialize old weights.
52 historical paths=48C175source_blobs+4C175own files at d54a4921. Four new C176 files
checked against execution HEAD. Standalone paths,unchanged original C174/C175 modules.
71 input paths protected;C37 and composition fixture also checked by the outer runner.
Source validation uses the unchanged C175 standalone guard,not C174's monorepo monkey-patch.

Fresh UUID output:conditional-plan.json before training,train-weight-table.json,six final
checkpoints,pilot-predictions.json,training-predictions.npz,and complete summary.json.
Hash and actual byte sizes saved. Earlier outputs remain immutable. Actual wall-clock is
reported;no inferred GPU-memory or production-latency claim. All data-derived weights are
saved before fitting,not learned or selected on pilot scores.
Scientific manifest SHA25609ce8d00f2f6d09fda96f93e51aed6c34fd5b4e74eba77d51848c8e1f8dbafa8.

## Verification / run

28/28 new actual-code helper tests passed under PyTorch2.10CPU/NumPy2.3.5. Tests cover
conditional weight mass,class mass,pure strata,zero-versus-missing,loss and analytic
gradients,paired row RNG,immutable inputs,gate failures and additive regression-list parsing.
Toy fits use an8-row artificial input and a small linear network,not the registered MLP
pilot. No registered six-model2000-update fit or pilot score was executed by the reviewer.
Python modules compiled;three embedded Python scripts parsed. Complete old-dependency
integration,1001focused tests,WindowsPowerShell and artifact-backed formal run NOT executed.
Uploaded source/test/runner Git blobs match the locally compiled/tested bytes.

**1001 focused tests expected=973+28,60modules**,once,then one CPU learning batch.
Run tools/run_c176.ps1 -C175Summary ... -C174Summary ... -ExpectedHead ... .
Progress:source_and_artifact_precheck;regression;C176plan;seed/arm every500updates;three
mixed_count_BA comparisons;RESULT/POSTCHECK. Preserve and return full log even if FAIL.
