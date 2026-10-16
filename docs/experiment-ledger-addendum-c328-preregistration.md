# C328 preregistration -- fixed late learning-rate attenuation

Authoring date:2026-10-17 Japan time.
Experiment:C328-v5b-late-rate-decay;stage:V5-B-LATE-RATE-DECAY.
Acceptance base:d96e7ff66f76463e6fe39ca159e687f7d26d2011.
C327 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY);C326 remains VALID NEGATIVE.
Gate F NOT PASSED;C329 NOT REGISTERED. Separate committed-byte review and activation
are required. This protected contract is not itself permission to execute.

## One question and motivation boundary

With the fixed C326 batch4 within-update curriculum and1200updates, does reducing
both learning rates by a fixed factor0.1 after800completed updates improve interior
binding while retaining original2..6 performance, relative to constant rates?

C327 found full-vector common Euclidean first-order descent in50/60terminal objective
pairs. This does not establish that constant late learning rates caused C326 failures,
that an AdamW direction is a raw mean-gradient direction, or that a finite step helps.
C328 is a prospective optimization-policy test, not a claimed causal consequence.
No additional ratio/switch/budget/seed search is authorized by this registration.

## Fixed cohort, data and optimizer intervention

Fresh initialization seeds328001..328005;order seeds328101..328105.
Arms:constant(control),late_tenth(candidate),ten new models with paired identical
initial weights. No C326/C327 checkpoint initializes training. Both use native
mean_last,14256parameters including3328core,64slots,CPUfloat64,two threads,
deterministic algorithms. Dataset remains192TRAIN/96HOLDOUT logical rows.

Both use unchanged C326 family_mask(events,'batch4') on the new paired logical
schedules. Length/profile sequence,query pairs,row order,labels and templates are
identical. Every TRAIN row sees original2/original3 each100times and original4/
interior4 each50times. Per-pair/per-profile exposure remains exact;24intact query
pairs/update,48rows/update. Each length4 update has11..13original pairs,not a falsely
claimed exact12/12. All five actual schedules validate before regression or fitting.

The accepted C308 optimizer_for(model,'core_slow') creates one native AdamW/model:
noncore group LR.005;core group LR.0005;betas(.9,.999),eps1e-8,weight_decay0.
Ordinary mean cross entropy;global norm clipping1 on original parameter order before
optimizer.step;fit RNG612000. Both arms perform all1200updates.

- Updates1..800 inclusive:both groups retain their original learning rates.
- Updates801..1200 inclusive:constant stays.005/.0005;
  late_tenth uses(.005*.1)/(.0005*.1),approximately.0005/.00005.
- Change only each optimizer param_group['lr']. Do not recreate the optimizer,
  clear/scale moments,reset per-parameter step counters,change clipping,detach
  gradients,change defaults,alter group membership or patch any accepted global.
- Validate the native C308 optimizer at creation. The child then independently
  validates original parameter identities/order,all non-LR group settings,defaults
  and optimizer identity at every update,plus the exact registered LR.
- Before update801 persist typed hashes of the entire model state and optimizer
  state_dict. Paired hashes and all first800 CE values must match exactly.
- Hash optimizer moment/state tensors immediately before and after LR assignment;
  require exact equality. LR changes are not gradient scaling and not a restart.

Persist all1200 LR/CE/gradient traces,schedules,masks,exposure maps,boundary hashes
and switch receipts. Mismatched common prefixes are INVALID,not scientific negatives.
No HOLDOUT labels or measured success choose when/how to change the learning rate.

## Fixed workload, evaluation and gates

10models,12000updates,576000training-row presentations;15420model forwards,
904320total row presentations,61680internal core forwards;10checkpoint state reloads,
one replay-bundle read andone model-bundle write. Per model fit/eval1371forwards/
74016rows;replay171forwards/16416rows. Raw saved-logit payload336199680bytes,not total
serialized size or peak RAM. Optimizer-boundary hashing and schedule work are real
additional overhead;no controlled speedup claim is made.

Separate native preflight:allfive actual batch4 plans and one fresh ephemeral
model,original/interior inputs for English/Japanese,6forwards/2backward evaluations,
12row presentations,0optimizer steps. Its temporary output weights are deliberately
nonzero for a useful gradient probe and are never used to initialize fitting.
Software tests,parent/saved verification and preflight are outside cohort counters.

Use unchanged C324/C326 raw evaluator,masked views,original2..6 scorer and interior
scorer. Thresholds remain accuracy>=.90,both-query>=.80,evidence-blind drop>=.35,
query-blind drop>=.35,two-order>=.80 at every registered local TRAIN/HOLDOUT profile/
language/masked/order condition. Original length1 is descriptive only.

ALL FIVE candidate seeds must:
1. Pass complete interior and every original2..6 gate.
2. Increase BOTH interior HOLDOUT correct-answer and both-query-correct pair counts
   strictly versus its paired constant control.
3. Not decrease EITHER pooled original2..6 HOLDOUT count. Ties are allowed only here.

Record every seed,all local cells,per-length original contrasts,rescues and new
regressions. A pooled mean cannot hide any failed seed/local gate. Finite composite
failure is VALID NEGATIVE,not permission to retry,select a seed or relax the rule.
Both families are seen during training and logical splits are reused;this is not
unseen-template generalization,independent tasks,architectural impossibility,
general LLM capability,production adoption or Gate F passage.

## Parent writer schema and complete inheritance

Immediate parent is the accepted C327 DIAGNOSTIC,not a C326 training result.
Execution:847c924f50303d93ed4df7acec74b77209b7d261.
Publication:926113e7602f1ee36445cde9bbf90eab1539ace1.
Folder:runs/c327-gradient-1cf048a0cd9449b6af6485a4802c46ca/.
Primary science/summary.json SHA256:
c4a061e158a1bd617fb7638bb034b7aa3ef78da06b15062474ff986d1f347719.
Mandatory execution-envelope.json SHA256:
fb44749ce38e0b0909238c51c13bbb1eb95e1898369313fb34d95483a543e535.

Validate both fixed parent hashes,diagnostic PASS with capability_gate_applicable
false,original manifest/work,full5658receipt and semantic/final1549-read completion.
Both records must contain identical complete820-source/1549-input unions.
Verify every inherited source Git blob and input byte. Parent outputs are FOUR:
diagnostic-plan.json,gradients.pt,measurements.json,validation-summary.json.
These four plus summary+envelope add SIX immediate-parent files,not ten.

Use the immutable C327 executor's fixed C326 parent folder/hash for canonical
training data and saved logits. Require those C326 files already in inherited input
protection and validate canonical hashes/prompts. Reconstruct C327 gradients/metrics
with unchanged C327.semantic_recheck(C327_out,C326_out,data,read_json),under no_neural.
No parent model forward or recursive older semantic reexecution occurs in this step.
All older bytes remain checked;no accepted function/module global is patched.

Protection:826sources=820inherited+6own;
1561inputs=1549inherited+6immediate-parent files+6own files.
Own benchmark,execution helper,test module,runner,launcher,and this contract are all
protected. Direct/lazy dependencies include C327/C326/C325/C324 benchmarks/executors,
C308 optimizer and inherited recovery code/tests. No fallback to older smaller maps.
Native unchanged R4 Windows read leases stay held through all worker phases;
independent first-read reference hashes and final uncached rereads ofALL1561files.
No unlocked/cross-run cache,artifact deletion or environment modifications.

## Runner, outputs and review

64own tests;5658inherited+64=5722selected tests,217modules;
5723before the sole inherited C204 mutable-ACTIVE exclusion. No new exclusions/skips.
Actual distinct-ID suites and module counts are checked;ordered suite digest printed.
Full regression runs in a separate ordinary interpreter without scientific wrappers.
Only native preflight andALL5722success permit fitting.

Route:PowerShell7 ->invoke_active_v2 ->invoke_c328 ->run_c328 ->c328_execution
controller ->worker ->C327/C326 persisted checks ->native preflight ->ordinary full
regression ->10fits/evaluations/first800comparison ->10checkpoint replays ->saved
reconstruction ->1561final rereads ->summary/envelope ->fresh byte verifier ->log push.

Local eight science outputs:experiment-plan.json,dataset.json,original-prompts.json,
interior-prompts.json,trained-models.pt,evaluations.pt,measurements.json,
validation-summary.json. Local science/summary.json binds these hashes/sizes and the
full source/input union;companion execution-envelope.json is mandatory. Also local:
regression-result.json and science/regression/verify logs,under runs/c328-late-rate-<id>.
Never publish tensors/data;only console goes to docs/experiment-run-logs/c328/latest.*.

Bind all eight output hashes/sizes before/after saved semantic reconstruction and
recheck them before writing summary/envelope. Fresh process checks complete source/
input unions,every source/input/output byte,size,cohort,rate-policy manifest,full
regression,common-prefix flags and gate/count conservation. Semantic reconstruction
checks actual saved traces,paired boundary hashes and checkpoints. This verifier is
not a fresh rerun of the1200-step optimization history and does not claim to be.
Use10second heartbeats,200update LR/CE progress,all seed/pair records,compact domain
minima/totals;full cell metrics remain in hashed local artifacts.

Manifest SHA256:
75f3de53837dcc64127b72f541ded650436b3a6ac46686bd9d8ff2aa8b89a226.
After committing all6own files,reread complete remote bytes,compare Git blobs with
locally tested bytes,check writer/loader/call-order/free-global bindings and rerun
all64tests plus CP932-default-text-open emulation. The real1200-update toy pair
checks common800weights/moments and distinct final states;it is not a FOLD result.
Explicit synthetic worker/parent/lock fixtures are not native historical regression.
No author-side PowerShell/native Windows/full5722 success is assumed.
Retain mandatory dispatcher->launcher->runner ParseFile checks before native work.

Authoritative runtime staysPython3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
No CI,paid service,package reinstall,cache deletion or old-source/result mutation.
Stale branch/HEAD/ACTIVE/dirtytree/dependency/AST errors are operational SKIPPED before
logging/publication. Source/input/schedule/first800/optimizer/test/nonfinite/replay/
semantic/envelope failures stop SAME C328,with evidence preserved,no automatic retry.
Scientific FAIL with valid execution is accepted negative evidence. Publication-only
failure is repaired without refitting. C329 remains NOT REGISTERED.
