# C309 preregistration — unchanged core-LR policy on fresh seeds

Experiment:C309-v5b-core-lr-replication. Stage:V5-B-CORE-LR-REPLICATION.
Acceptance base:1e534105f5ac29b4e6f128adc3b47baa4e31966b.
C308 ACCEPTED PASS (bounded capability). C306/C307 remain negative. Gate F NOT PASSED.
C310 NOT REGISTERED. Do not reinterpret C308 as diagnostic-only PASS or as Gate F completion.

## One question and fixed comparison

Does the unchanged C308 core_slow policy achieve the same all-five unseen-five gate in one new
paired initialization/order cohort,with BOTH original controls retained? C308 gave5/5 for both
core_slow and core_frozen,and4/5 for full_train. It did not establish superiority to freezing.
This replication is specified before its outcomes;no ratio sweep,winning-seed selection,model
reuse or additional length is introduced. Fresh seeds are not fresh datasets or blinded replication.

New initial seeds309001..309005;order seeds309101..309105 paired by index. All15 cells retained:
full_train:all14256 weights train at0.005;
core_frozen:3328core weights stay at their own random initialization;10928noncore train at0.005;
core_slow(candidate):all14256 train;coreLR0.0005,noncoreLR0.005.
Every arm has its own independent copy of the same initialized model at each seed. No successful
old core or learned checkpoint is reused. Report the new cohort separately from C308;never pool
old successes into the new all-five test. Do not continue collecting seed cohorts until success.

## Exact policy preservation

Actual accepted C304 LengthReadout,64slots,14256stored parameters;core forward and input backward
remain present in all arms. No detached signal,learned gain,auxiliary objective or model change.
Use exact C308.configure,parameter_groups,optimizer_for,verify_optimizer and first_batch_probe.
These functions are seed-independent;child owns seed-sensitive factory,schedule,fit and analysis.
No accepted module constant/function is modified or monkeypatched by the scientific path.
policy_contract compares original and child data/optimizer/schedule/gate constants and requires
new seed sets. Full/frozen preserve one optimizer group;slow preserves separate noncore/core groups.

Ordinary meanCE,one AdamW per state,betas(.9,.999),eps1e-8,weight_decay0,1200updates.
Global norm1 clips active parameters in original model parameter order before AdamW. The nominal
coreLR ratio remains0.1. Do not shrink core gradients before clipping or change group order.
Every update verifies optimizer membership and LRs;all1200 LR/loss/gradient/event records are saved.

Schedule remains300epochs*4,96intact question pairs,24pairs/48rows per update. Private permutation
seed=order+306000+epoch;length=2+epoch%3;profile=(epoch//3+epoch%3)%3. Global fitRNG612000 resets
per model. Each logical row receives100 exposures at each of2/3/4;each profile400updates. Old
numeric offsets are deliberate policy constants,not stale experiment IDs. Only initialization
and order seeds change relative to C308,apart from experiment identity/bookkeeping/validation.
No5,HOLDOUT or masked input is optimized. No extra steps,early stop or intermediate-state choice.

Operational first-seed probe reuses C308's full/frozen gradient check and full/slow first update:
initial logits/noncore gradients agree;frozen core has no gradients while encoder receives signal;
full/slow preclip gradients match;first core delta ratio0.1 and same noncore delta within1e-12.
Copies are discarded and original initial fingerprints rechecked. Two probe updates are operational,
not scientific work. This is not a claim about update ratios after learning trajectories diverge.

## Parent writer semantics and exact verification

C308 scientific execution:2fc902e8c7f57579087a61e25e7c1e88f8c66090.
Published log:045de9e384e6d19f35b48722a55b3fac1062ddbd.
Summary:runs/c308-v5b-core-lr-02b24ac7b9da4a36a14a5545bd42aab6/summary.json.
SHA256:42a2dbc75c6bf958bff26315f918fc999728196eac7fe890eee28aa392f63c8a.
Parent source:fold_lm/v05_benchmarks/model_c308_core_learning_rate.py.
Parent blob:f4e41f0d37b1aa5cbba536e5da984ab556eea2c5.
C304 wide source blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify35 ordered summary hashes BEFORE exact C308.verify_artifacts(parent_dir,34ancestors,
acceptedHEAD). Tail comes from immutable C308.parent_hashes(). Require statusPASS,all_groups_matched,
all_replays,exact15 original seed flags and both paired-five contingencies. Every old flag passes
except full_train308002;even that state has fitted_train_direct_pass=True. The exact summary hash
seals all7 descriptors and the parent reconstructs original scores/gradients/core and LR invariants.
The writer saved FINAL frozen model outputs,not action-selected or intermediate predictions.

Read only verified dataset.json/length-datasets.json for new learning;check canonical hashes,
prompt regeneration and unchanged original masks. Never use old output predictions as targets or
old trained-models.pt as initial state. Data SHA1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Prompts SHAecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d.

Sole direct import C308. Its context supplies C307,C306probe,C305no-neural,C304scorer/replay,
pair builder,C287normalizer,C283transfer and original backend. Retain all694 source pins and1295
protected inputs,including real repository-local context/core/factory-language helpers and every
C304.PINNED source. Add OWN6 and8 parent files:source700/protected1309. No exclusions added and no
accepted source/test/preregistration/log/dispatcher edits. Old files remain immutable.

## Primary gate,comparison and limits

Freeze15final states;evaluate2/3/4/5 at all original profiles,languages,splits and normal/evidence-
blind/query-blind views. Save/reload all15 states strictly and replay every view with logit drift
<=1e-9 and exact argmax. Core hash must stay unchanged only for frozen;full and slow core must change.
Primary PASS iff ALL5 NEW core_slow states pass EVERY original five-character local/masked
criterion:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Valid miss is ACCEPTED VALID NEGATIVE;no averaging or old/new pooling substitutes for this gate.

Report15 seed records,120length/split partitions,80candidate-versus-each-control count contrasts,
15configured/actual gradient summaries and two paired-five contingencies. All relative results
remain visible even if candidate5/5. Matching frozen5/5 is not pass-count superiority;matching all
controls5/5 cannot establish an advantage. No universal reliability,optimal ratio,core-necessity,
arbitrary-length competence,production adoption or automatic Gate F completion follows.
Frozen trainable capacity/clipping/backward work differ;same steps/forward count are not equal
backward FLOPs or runtime. Repeating the same templates does not measure general language ability.

## Workload,persistence and authoring gates

Science:15models*1200=18000updates;864000training rows;21240forwards;1175040total row presentations;
84960core calls;15strict state loads;one new model-bundle write/read;network0. Same as C308.
Operational probes,tests and recursive old-artifact validation are separate costs.
Seven outputs:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c309-core-lr-replication-models-v1 and fold-c309-core-lr-replication-eval-v1.
Full data/tensors/weights stay local/ignored. Console mirrors compact receipt and aggregates.
Numeric postcheck reconstructs all LR/event/score invariants without a model forward.

Own32/modules194/loaded4910/focused4909. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:9350f7a5ec4e91a3292f6ecce041bc3ec09f1fa1a8372a4178b58d0ceb4df74d.
Commit,re-fetch and perform separate post-authoring review of OWN6 before activation or command.
Authoring tests compare the actual child1200-step loops against isolated accepted C308 definitions
for ALL3 arms with new seed inputs,without mutating imported modules. Check policy drift,optimizer
membership/LR histories,initial equality,independent storage,run/bundle ordering,protection,UTF8/
CP932,global bindings,CLI indices and byte/semantic tampering. Software fixtures are not FOLD ability.
Windows Validate still requires real35parents/pins,actual-model probes,own32 and full4909 tests.
Retain the active_v2 dispatcher/selected-launcher/runner ParseFile chain. Validate failure skips
science/publication. Integrity failures repair SAME C309 without policy/seed/threshold changes.
C310 waits for formal C309 judgment. C308's accepted bounded PASS and Gate F status stay separate.
