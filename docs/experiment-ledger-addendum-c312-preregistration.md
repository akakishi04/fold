# C312 preregistration — TRAIN value-balanced minibatches

Experiment:C312-v5b-value-balanced-minibatches. Stage:V5-B-VALUE-BALANCED-MINIBATCHES.
Acceptance base:b583d14164fed3f6f03e0385e5d8c443138171f9.
C311 diagnostic PASS;C309 valid negative;C308 bounded PASS;Gate F NOT PASSED.
C313 NOT REGISTERED. No scientific C312 result yet.

## One question

At the unchanged core_slow policy,does balancing the original TRAIN ordered-value pairs in
EACH minibatch improve unseen-five reliability compared with the original random-pair batching?
C311 found broad held-out errors,mostly unmentioned digits in the slow309002 state,with13/19
five-errors already wrong at four. It did NOT establish minibatch imbalance as a cause.
This is an intervention in batching,not a causal explanation inferred from those diagnostics.

## Exact arms and randomization

Fresh initialization seeds312001..312005;paired order seeds312101..312105. Two arms:
random_pairs and value_balanced. Both use core_slow:core.0005,other.005. No full_train/frozen arm
is required for this conditional batching question. Keep all5 paired seeds,including failures.
Same accepted C278/LengthReadout architecture:14256 parameters,3328 core,64slots,all trainable.
No learned checkpoint reuse,successful-core selection,new parameter,loss term or teacher.

Original TRAIN has8 ordered distinct value pairs with difference1 or3 modulo4. Each value
stratum contains12 intact query pairs (24 rows). Original HOLDOUT has difference2 and is NEVER
added to TRAIN,including through value renaming. Both questions for each fact pair stay together.

At each of300 epochs draw the SAME randperm96 using a private Generator(order+306000+epoch).
random_pairs:take four consecutive24-pair batches exactly as C309's schedule algorithm.
value_balanced:split that SAME rank sequence into8 stable stratum lists,each12 entries. Batch j
selects entries3*j..3*j+2 from EVERY stratum,then restores their relative order from the global
rank sequence. No extra RNG or deterministic value-sorted within-batch order is introduced.
Each batch has24 pairs/48rows,3pairs per value stratum and12 targets per digit0..3.
Every epoch consumes exactly the same96 pairs once in both arms. Length index=epoch%3 and
profile=(epoch//3+epoch%3)%3 in all four updates. Every logical row is shown100 times at EACH
trained length2/3/4;all three profiles have400 updates. Same total1200updates/model.
The intervention changes both batch composition and temporal order. It cannot isolate gradient
noise,implicit regularization,forgetting or target-frequency effects from each other.

The first actual minibatches differ,so their first losses are NOT required equal. Initial weights
and a SAME-INPUT forward/preclip-gradient/one-update probe must match instead. Runtime preflight
also reproduces C309's old random schedules at all five old order seeds using the new constructor.
This compatibility check does not retrain or select old outcomes.

## Unchanged optimization,inputs and gates

Ordinary mean cross-entropy;one AdamW1200updates;betas.9/.999,eps1e-8,weight_decay0,global normclip1
before step in original parameter order. FIT_RNG612000 per model. Reuse exact accepted C308
configure/parameter_groups/optimizer_for/verify_optimizer with policy name core_slow in BOTH arms.
No gradient scaling before clipping,no lr decay,no early stopping. Training only normal2/3/4
TRAIN. All5/HOLDOUT/masked input views remain evaluation-only. CPUfloat64,threads2,deterministic.

Primary:ALL5 value_balanced models pass every original local/masked five-character gate.
Thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Full256-class
argmax remains;no answer correction,restricted decoder or success-only cohort. Report all2/3/4/5
scores,TRAIN/HOLDOUT,paired-five outcomes and40 correct-count contrasts. An absolute5/5 PASS is
not automatically superiority over random batching or general FOLD/MinePilot competence.
No pooling with C308/C309 to pass. Gate F remains NOT PASSED regardless of this narrow result.

## Parent semantics and source protection

C311 execution:a777fc793b2affe287d055733b012ea919504446.
Publication:d894b4b26ffb821bcd89db17b70d4f9798d3e1ee.
Summary:runs/c311-v5b-error-context-2e3d082f8a9a4045b09dbe38a62ca6a8/summary.json.
SHA256:9bfdad83b33d24a986c3f76ef0e40d0ad323698b28826f80f659ff5fa6e0cdec.
C311 source blob:d02444686ac736bc1c4f22b98b549307014e6ad4.
Verify38 summary hashes BEFORE C311.verify_artifacts(parent_dir,37ancestors,acceptedHEAD).
C311 produces diagnostic JSON,NOT a model bundle. Its verifier returns(payload,error_report) and
recursively verifies C310/C309 saved predictions and data. The new fit does not train on the report.
Read original C309 dataset.json/length-datasets.json at paths[2] only after that full verification;
revalidate canonical hashes and render semantics. Do not guess that C311 wrote those two files.

Sole direct import C311. Traverse its C310/C309 context to accepted C308 policy,C304 tables/render/
LengthReadout/evaluate/score/replay,C296 pair helper,C287 normalizer and original backend modules.
All these helpers remain source-pinned. Exact parent/C309/C308/C304 identities are explicit PINNED;
retain C304.PINNED and actual repository-local context/core/factory-language dependency coverage.
Retain all712 parent source pins and1333 protected inputs;add OWN6 plus4 C311 summary/artifacts:
source718/protected1343. No accepted source/test/log/dispatcher or regression exclusion changes.

## Work,persistence and verification

10 new models*1200=12000updates,576000training rows. Initial evaluation108forwards/model and
strict checkpoint replay108/model. Total14160forwards,783360row presentations,56640core calls;
10 strict model state loads,one new10-state bundle write/read,network0. Operational discarded
same-input probes,recursive parent checks and software tests are separate costs.

Seven artifacts:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json.
Schemas:fold-c312-value-batches-models-v1 and fold-c312-value-batches-eval-v1. Preserve initial/final
whole/core fingerprints,all1200CE values,optimizer-group LRs,gradient-receiver accounting,
actual schedule tensor and1200x8 value-count matrix per model. Full original final logits are
saved for all four lengths and all views. Strict-loaded states reproduce all logits<=1e-9 and
exact argmax;reconstruct scores,plans,counts and paired results from the saved data. No overwrites.
Full tensors/maps stay local/ignored;compact receipt and all10results/80partitions/40contrasts
are logged. Do not confuse model count or row presentations with independent observations.

Own32/modules197/loaded4998/focused4997;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:5c543202a3c252e69f3f099b369ef9905e39662a37947c8904756b17700fab2c.
Commit/refetch/review OWN6 before activation. Require UTF8/CP932,free globals0,manifest seal,
all3 embedded Python blocks and38input CLI indices. Semantic suite-ID counting is mandatory.
Windows Validate:38real parents,718/1343pins,allnew plan budgets/strata,old random-schedule
compatibility,real common-input probe,own32,full4997 regression and dispatcher/launcher/runner
ParseFile chain. Validate failure skips science/publication. Any integrity failure repairs SAME
C312 without changing scientific conditions. A valid primary failure is ACCEPTED VALID NEGATIVE.
C313 waits for formal C312 judgment;do not retune strata,LRS,seeds or thresholds after results.
