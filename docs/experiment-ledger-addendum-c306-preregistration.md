# C306 preregistration — core freezing under broad length coverage

Experiment:C306-v5b-broad-length-core-freeze. Stage:V5-B-BROAD-LENGTH-CORE-FREEZE.
Acceptance base:73282101c89ac14cf5aa55d6d91c4bedc87b176d.
C305 ACCEPTED PASS (diagnostic integrity only);C304 remains valid negative;Gate F NOT PASSED.
C307 NOT REGISTERED. C306 is a new candidate comparison,not another zero-neural diagnosis.

## One question and rationale

At identical2/3/4 training,does freezing the initially random recurrent core improve reliable
unseen5 performance relative to full training? C305 found418 of430 candidate five-HOLDOUT errors
already wrong at4. It did not prove a core mechanism. C303's core_frozen4/5 quad result motivates
this separately preregistered transfer of a training policy,not automatic adoption. Do not compare
old48-slot/800-update scores causally with this64-slot/1200-update cohort.

Use fresh paired seeds306001..306005 and order seeds306101..306105. Arms:full_train and core_frozen.
No C303/C304 learned states or chosen successful initialization donors are reused. Both arms
start with identical full state dictionaries and independent parameter storage per seed.

## Changed and fixed conditions

Only backbone.core requires_grad flags and corresponding optimizer membership change. Keep the
exact accepted C304 LengthReadout;no new wrapper,forward hook,detach,stop-gradient,coefficient,
loss term,output filtering,core removal,or inference-path change. The frozen core remains at its
own seed's initial random values throughout optimization. Its forward calculation still runs,
and differentiation THROUGH its inputs still reaches the local encoder. All noncore parameters
remain trainable. Verify identical initial outputs and noncore pre-clip gradients on a discarded
first-TRAIN-batch probe,core gradients absent only in the frozen arm,and nonzero encoder signal.
Probe copies are never used as trained models and receive no optimizer update.

Stored parameters14256 in BOTH arms. Trainable14256 versus10928;core3328. Record every update's
actual gradient-receiving parameter count and the union of receiving names/sizes. A configured
trainable parameter is not automatically counted as receiving a gradient. Global clipping and
backward cost can differ when fewer parameters train. This is a training-policy package,not
matched trainable capacity/backward FLOPs or proof of core necessity/irrelevance.

Both arms:ordinary mean CE,one AdamW1200 updates,lr.005,betas(.9,.999),eps1e-8,weight_decay0,
clip norm1 with nonfinite rejection. Use only normal TRAIN logical rows192,96 intact query pairs.
300epochs*4batches of24pairs/48rows. Private randperm96(order+306000+epoch);length=2+epoch%3;
profile=(epoch//3+epoch%3)%3. This preserves C304's broad-arm allocation without coupling each
length to one profile. Every TRAIN row100 exposures at each2/3/4;each profile400 updates.
Reset fit RNG612000 independently per model. Same actual events and first CE within each pair.
No fifth-length,HOLDOUT or masked example enters optimization;no early stop or checkpoint selection.

Use common64slots and actual accepted backend;C304's exact input/render/span and readout functions
are reused. The exact validated old data and all2/3/4/5 strings are unchanged. No truncation or
language removal. Model state inventories and initial hashes stay identical to the48-slot
reference because frame size changes no learned parameter. This is not a new frame experiment.

## Parent contract and dependency audit

C305 execution:9c8beb3c66548c1e68def4ea2ced93acc0067e6e.
Publication:f89d33f9dd0dd84a54f045541117ca48a4f0a342.
Summary:runs/c305-v5b-length-overlap-4d5851c168fc401cbc5926f1d1ca841c/summary.json.
SHA256:dd8580fe7f544b2e94688c4236cb862cfc77bb57984b04e5116a2c2cd8cc4734.
C305 source:fold_lm/v05_benchmarks/model_c305_saved_length_overlap.py.
Git blob:e822f5680193951cbc9270cb70cb0d4d5fcb12b6.
C304 source:fold_lm/v05_benchmarks/model_c304_length_breadth.py.
Git blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify32 ordered hashes BEFORE exact C305.verify_artifacts(parent_dir,31 ancestors,execution_HEAD).
Order:C305,C304,...,C274. Tail from C305.PARENT_SHA plus C304.parent_hashes(C303). The C305 verifier
returns ONE payload dict,not a (payload,metrics) tuple;the child uses its actual return schema.
Require diagnostic PASS,capability_gate_applicableFalse,exact original parent flags,720 reconciled
totals/120 partitions and its3-artifact inventory. The exact summary seals all artifact descriptors.
C305 has no dataset/checkpoint output. Read C304 dataset.json from the SECOND summary's directory
only after its recursive verification,then C304.prompt_dataset/validate_prompts enforce canonical
data hashes and all parent renderer identities. Do not train on C305 aligned predictions.

C304 train_one/analyze enforce full-core training and old seed identities,so are NOT reused as
cohort loaders or training loops. C306 owns make_models,schedule,fit,train_one,analyze and result
schema. It reuses C304 LengthReadout,training_tables,schedule_stats,score_length,evaluate/replay_one
and the exact scorer/normalizer underneath. C304 replay_one accepts a model/state/record and
checks final fingerprint,all lengths/views <=1e-9 and exact argmax plus108/10368/432 counts.
Each child saved record contains actual final logits,not predictions from an intermediate step.

Sole direct import C305. Its context gives C304 and the inherited core bundle;C304 context yields
C301 pair helper access,C287 normalizer,C283 renderer/scorer and the original backend. All676
inherited sources/1257 protected inputs remain checked. Explicitly verify C305/C304 blobs and
all C304.PINNED backend/core/reader/scorer sources. Actual pair/context/core/factory language-module
files must be covered. Add OWN6+4 C305 summary/artifacts:source682/protected1267. No parent source,
test,preregistration,log or dispatcher edits;no additional regression exclusions.

## Evaluation,primary gate and preservation

After training,freeze the final model and score2/3/4/5 at all original profiles/languages/value
splits and normal/evidence-blind/query-blind views. All10 trained states are saved and strict-loaded,
then all views replayed. Candidate core hashes must equal initialization;full-train core hashes
must differ. Model state remains unchanged during scoring/replay. Save core initial/final hashes,
all1200 CE values,events,gradient names/counts and logits. No inference-time adaptation.

Primary PASS iff ALL5 core_frozen states pass EVERY original-style five-character local/masked
criterion. Thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
A valid primary miss is ACCEPTED VALID NEGATIVE. Report control and candidate separately,including
80 length/split partitions,40 paired correct-count contrasts and10 gradient-receiver summaries.
An absolute5/5 is not automatically superiority to a5/5 control or arbitrary-length competence.
Core_frozen may fit TRAIN while failing HOLDOUT;those results must remain visible. Gate F and all
old verdicts stay unchanged. No best-seed selection or universal freezing recommendation follows.

## Workload,artifacts and review boundary

10models*1200=12000updates;576000 training rows.10*(1200+108+108)=14160forwards;
783360 total row presentations;56640core calls.10 strict state loads,one model-bundle write/read,
network0. Backward cost is NOT equal between arms;no timing/speed claim from forward counts.
Operational first-batch probes,regression fixtures and recursive parent checks are separate.
Seven outputs:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json. Schemas:
fold-c306-broad-core-models-v1 and fold-c306-broad-core-eval-v1. Full datasets,states and tensor
archives remain local/ignored. Console publishes a compact receipt and aggregate results only.
Numerical postcheck revalidates parent data and reconstructs the results without model execution.

Own32/modules191/loaded4814/focused4813;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27.
Commit/re-fetch/review OWN6 before activation and command release. Require real child call order,
loader dispatch,source/global binding,UTF8/CP932 and semantic suite-ID checks. Verify actual C304
readout/evaluate/replay definitions with controlled backbone fixtures,not substitute scientific
results. Windows Validate must check32 real parents/pins,new initial models/gradients,schedules,
own32 and all4813 inherited tests. Preserve dispatcher/launcher/runner ParseFile chain.
Validate failure skips science/publication;integrity failure repairs SAME C306 at fixed conditions.
C307 remains unregistered until formal judgment.
