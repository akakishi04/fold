# C307 preregistration — fresh-seed core-freeze replication

Experiment:C307-v5b-core-freeze-replication. Stage:V5-B-CORE-FREEZE-REPLICATION.
Acceptance base:0012e1fb0d293cf2082c545c92ee2d7f5a6f8e01.
C306 ACCEPTED VALID NEGATIVE;C305 diagnostic PASS;Gate F NOT PASSED;C308 NOT REGISTERED.

## One question and reason to replicate

Does the improvement associated with C306 core freezing recur on a preregistered NEW paired
initialization/order cohort without changing the training policy? C306 had core_frozen4/5 versus
full_train3/5 unseen-five passes. The frozen policy rescued2 seeds but lost1;its pooled4319/4320
normal answers cannot replace its unmet all-five criterion. Do not tune for that remaining error.
A new cohort addresses dependence on the particular five random initializations/orders,not new
language/task coverage or a unique mechanistic explanation. Both arms are repeated concurrently.

Fresh initialization seeds307001..307005 and order seeds307101..307105,paired by index. No old
model or optimizer state is reused. No successful seed donor,failed-model continuation,extra gain,
freeze schedule,loss adjustment or hyperparameter search. C306 remains negative whatever happens.
Report C307 separately,with all5 candidate and all5 control outcomes. No retrospective pooled gate.

## Unchanged policies and exposure

Actual accepted C304 LengthReadout,14256 stored parameters,64slots. Same raw byte prompts and
canonical data;2/3/4 normal TRAIN only;5,HOLDOUT and all masked views are evaluation-only.
full_train learns14256 parameters;core_frozen fixes its own3328 randomly initialized core weights
and trains10928. The core remains in forward and backward-to-input calculation. No detach,new
wrapper,hook,coefficient,extra loss or restricted output. The inherited C306.configure is reused.
Each pair starts from identical full state dictionaries and independent parameter storage.

Both arms use1200 uninterrupted AdamW steps,ordinary mean CE,lr.005,betas(.9,.999),eps1e-8,
weight_decay0,global norm clipping1 with nonfinite rejection. One optimizer per model;exclude
frozen core from optimizer membership. Record actual gradient-receiver counts/names separately.
Fewer trainable weights and different clipping/backward work remain part of the policy;no equal
FLOP/speed or core-necessity claim. No stopping/checkpoint selection based on evaluation results.

Use exactly the C306 scheduling ALGORITHM and offsets:300epochs*4batches,96 intact query pairs,
24pairs/48rows per update,private randperm96(order+306000+epoch),length=2+epoch%3,
profile=(epoch//3+epoch%3)%3. The offset306000 is intentional,not an old-C typo. Only the initialization
and order seeds change. Every TRAIN row100 exposures at each2/3/4,each profile400 updates. The same
fit RNG612000 is reset before each model. It does not select new model seeds or batches.
No other optimization randomness is deliberately changed. Pairwise events and first CE must match.

The child owns seed-sensitive initialization,fit,analysis and serialization;accepted parent functions
that enforce the old C306 cohort are NOT monkeypatched. Compatible C306 configure/first_batch_probe
and C304 LengthReadout/training_tables/schedule_stats/evaluate/score_length/replay_one are reused.
A test extracts the actual C306 schedule/fit definitions into an isolated TEST namespace and
compares new-cohort schedules,all1200 losses,gradient metadata and final weights against the child.
This does not mutate the accepted source/module or bypass any scientific pin. Synthetic inputs
in that test validate software equivalence,not scientific FOLD generalization.

## Parent schema,semantics and protection

C306 scientific HEAD:cb2bb51a8beaa888c3a8b1fca382cd20536c923b.
Published log:340f9034fc07df63cff928bfd13703dfee5ca379.
Summary:runs/c306-v5b-broad-core-freeze-f8b13e726f314db09555a293f6d6bdf8/summary.json.
SHA256:5435cf83c02b75c2dd1d3c21105dcdf30e8c567c9d8672993f7676166515cff3.
Source:fold_lm/v05_benchmarks/model_c306_broad_length_core_freeze.py.
Git blob:5ca6ce358a7f6fe5fc3daf3c172289d6a4f0a786.
Wide source:fold_lm/v05_benchmarks/model_c304_length_breadth.py.
Git blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify33 ordered summary hashes BEFORE exact C306.verify_artifacts(parent_dir,32ancestors,
accepted execution HEAD). C306 returns(payload,metrics),unlike diagnostic C305's single dict.
Tail hashes:C306.PARENT_SHA(C305),C305.PARENT_SHA(C304),then C304.parent_hashes(C303..C274).
The exact C306 summary seals its7 artifacts;its verifier rebuilds final scores,freeze and replay
invariants,and ancestor validity. Require valid-negative FAIL,exact10 original seed_results,
all_pairs_matched/all_replays and candidate_gateFalse. These are not interim training predictions.

Read verified C306 dataset.json and length-datasets.json;do NOT load trained-models.pt for learning.
Canonical SHA256s:dataset1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
prompts ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d.
Regenerate and validate prompts with the accepted C304 helpers and exact older renderer contracts.
C306's final logits/losses exist for evidence only;new training starts from scratch.

Sole repository import C306. context resolves C305 no-neural,C304 wide helpers,pair builder,
C287 normalizer,C283 transfer helpers and original backend. Retain all682 parent source pins and
1267 protected inputs. Check C306/C304 blobs,C304.PINNED and actual repository-local context/core/
factory-language files. Add OWN6 plus8 parent summary/artifacts:source688/protected1281. No accepted
source/test/log/preregistration/dispatcher is changed;no new historical regression exclusion.

## Gate,reporting and error preservation

After each fit,freeze and evaluate all2/3/4/5 lengths,all profiles/languages/value splits and
normal/evidence-blind/query-blind views. Strict-load all10 saved states and replay every view;
maximum logit error<=1e-9,exact argmax,and unchanged final fingerprints. Frozen core must equal
its initial hash;full-train core must change. Retain all losses,events,gradient metadata and logits.

Primary PASS iff ALL5 NEW core_frozen states pass all original-style five-character local/masked
criteria. Thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
A valid miss is ACCEPTED VALID NEGATIVE. The all-five condition is unchanged,not replaced by
one average accuracy or a count of improved samples. Show80 length/split partitions,40 paired
count contrasts,10 gradient summaries and the five-seed both-pass/full-only/frozen-only/both-fail
contingency. Show all improvements and regressions;do not suppress successful controls.

A new5/5 candidate result is not automatically superiority to a5/5 control,proof of universal
reliability,independence from this task family or Gate F completion. This is a preregistered fresh
randomness replication by the same pipeline,not an external/blinded replication. Any later pooling
is descriptive and must retain both complete cohorts and their original verdicts.

## Workload,persistence and execution

10models*1200=12000steps;576000 training rows;10*(1200+108+108)=14160model forwards;
783360 total row presentations;56640core calls;10strict state loads,one new bundle write/read,
network0. Same scientific workload as C306. Operational probes/tests and parent verification are
separate. Fixed-core backward work differs;do not infer identical runtime from equal forward counts.
Seven artifacts:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Child schemas:
fold-c307-replication-models-v1 and fold-c307-replication-eval-v1. Records keep all final logits and
1200-step traces. Full weights/data/tensors remain local/ignored. Console mirrors receipt,aggregate
results and paired-five contingency. Numeric postcheck reconstructs scores without model execution.

Own32/modules192/loaded4846/focused4845;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:9662b7d5763768a09c75c961dc8f8453c40506eadcbb44639bbd50f7dca2ab8b.
Commit,re-fetch and separately review all6 OWN before activation/command release. Check actual
parent writer/helper semantics,free names,UTF8/CP932,embedded Python,33path CLI and suite IDs.
Windows Validate:33 parents,688/1281 protection,same-policy check,all5 schedules,actual fresh model
initial-state and gradient probe,own32 and full4845. Preserve dispatcher/launcher/runner ParseFile.
Validate failure skips science/publication. Integrity failure repairs SAME C307 without policy
retuning. C308 remains unregistered until C307 formal judgment. No silent old-result rerun.
