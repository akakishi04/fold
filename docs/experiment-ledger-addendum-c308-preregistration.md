# C308 preregistration — core-only learning-rate attenuation

Experiment:C308-v5b-core-learning-rate. Stage:V5-B-CORE-LEARNING-RATE.
Acceptance base:49bf2b96faa9afcee97bbce3840e1164b498fcd8.
C307 ACCEPTED VALID NEGATIVE;C306 remains negative;Gate F NOT PASSED;C309 NOT REGISTERED.

## One question and prospective choice

Does a nominal core learning rate one tenth of the noncore rate improve unseen-five reliability
versus both ordinary full learning and complete core freezing,at fixed2/3/4 training and1200steps?
C307 reproduced a seen-length count benefit but NOT C306's five-character count advantage:
full/frozen both3/5,with one rescue,one regression and one shared substantial TRAIN failure.
Neither the final residual gain nor another seed search is the intervention here.
The ratio0.1 is one prospective coarse contrast,not a measured optimal ratio or a grid search.
No inference about a proven core-instability mechanism follows from the prior outcomes.

Fresh initial seeds308001..308005;order seeds308101..308105 paired by index. Three arms:
full_train:all14256 parameters train at0.005.
core_frozen:core3328 fixed at its own random initialization;noncore10928 train at0.005.
core_slow(candidate):all14256 train;noncore10928 at0.005,core3328 at0.0005.
Retain every seed and every control. No learned checkpoint or selected successful core is reused.
Candidate5/5 is an absolute bounded gate,not automatic superiority if controls also pass5/5.

## What changes and stays fixed

Use the actual accepted C304 LengthReadout,64slots,14256 stored parameters. Unchanged forward
computation,input rendering,output classes and masks. Core remains in forward and backward-to-input
in all arms. No detach,coefficient,auxiliary loss,gradient scaling,core removal or delayed unfreezing.
The three states are independently stored copies of the same initial reference at each seed.
Core membership is checked by object identity AND the exact backbone.core.* named boundary.
Every noncore parameter remains trainable. The full/frozen controls keep the original one-group
optimizer membership and parameter order. Candidate uses two disjoint groups:noncore then core.

Ordinary mean CE;one AdamW per model,betas(.9,.999),eps1e-8,weight_decay0. Both group LRs are
constant for1200updates. Global norm clipping1 applies to trainable parameters in ORIGINAL model
parameter order,not optimizer-group order. Scaling the core gradient before AdamW is NOT this
intervention. Check group parameter identities,LRs and optimizer settings every update;persist
all1200 group-LR records,losses,gradient-receiver names/counts and schedule events.

Full and slow arms initially have identical gradients and clipping inputs;subsequent gradients
and moment estimates can diverge. Only the first matched update is required to have core delta
0.1 of control and identical noncore delta within1e-12. This does not assert a1/10 final change
or1/10 update ratio after trajectories diverge. Frozen arm changes trainable capacity,clipping
and backward work;do not describe all three arms as identical learning capacity/FLOPs/runtime.

Keep C306/C307 schedule ALGORITHM and offsets:300epochs*4,96intact query pairs,24pairs/48rows
per update;private randperm96(order+306000+epoch);length=2+epoch%3;
profile=(epoch//3+epoch%3)%3. Each TRAIN row100exposures per length and each profile400updates.
FIT_RNG612000 is reset before each model. These old numerical offsets are deliberate constants.
Only normal2/3/4 TRAIN inputs optimize parameters. Five-character,HOLDOUT and masked views are
never training inputs. No extra epochs,checkpoint choice,early stop or evaluation-derived policy.

## Initial-state and optimizer probes

On discarded copies of the first fresh seed,call the actual C306 first_batch_probe for full/frozen:
initial outputs and noncore preclip gradients agree,frozen core gets no gradient,and the encoder
still receives signal. Separately check full versus slow initial logits and ALL preclip gradients
for exact equality. Then perform one discarded optimizer update per copy and compare deltas:
core_slow delta=0.1*full delta on core,identical elsewhere,tolerance1e-12.
Original scientific models must not be updated by probes. Probe2updates are operational costs,
not scientific training. No result selection or persisted probe model is permitted.

## Parent semantics and protection

C307 scientific HEAD:4371ad8de650261f6cdacacfd9972efcdbe970a8.
Published log:6cdbde45709579c736d2fc0bd682f992a6d63b25.
Summary:runs/c307-v5b-core-replication-468c370e9c4b491585226c5492a8b52c/summary.json.
SHA256:5cb0683de649361966f2ab549aeab94d20643d64fe68d1d8bbe3497e6d637e42.
Parent source:fold_lm/v05_benchmarks/model_c307_core_freeze_replication.py.
Parent blob:02cb0d743391ef1424b537159c824c5e2bc5209b.
C304 wide source blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify34 ordered summary hashes before exact C307.verify_artifacts(parent_dir,33ancestors,
acceptedHEAD). It returns(payload,metrics). Tail hashes come from immutable C307.PARENT_SHA,
C306.PARENT_SHA,C305.PARENT_SHA and C304.parent_hashes(C303..C274). The exact parent summary
seals all seven artifact descriptors. Require statusFAIL,exact10 parent seed_results,matched
pairs/replays and both_pass2/full_only1/frozen_only1/both_fail1. No parent verdict changes.

C307 writer persists FINAL post-fit frozen evaluation logits and all1200 training losses/events;
its verifier reconstructs all original scores and invariants. Read only its verified dataset.json
and length-datasets.json for training. Recheck canonical hashes and C304 prompt regeneration.
Do not train on parent predictions or initialize from parent trained-models.pt.
Dataset SHA1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Prompts SHAecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d.

Only direct repository import is C307. Its context provides C306 probe,C305 no-neural scope,
C304 LengthReadout/tables/scoring/replay,pair builder,C287 normalizer,C283 transfer and backend.
Child owns cohort-sensitive functions;accepted module constants/functions are never monkeypatched.
Retain688source pins/1281inputs. Verify actual repository-local context/core/factory-language
helpers and all C304.PINNED blobs. Add OWN6 and8parent files:source694/protected1295.
No accepted source/test/preregistration/log/dispatcher changes or new test exclusions.

## Evaluation,gate and reporting

Freeze all15 final states;evaluate all2/3/4/5 profiles/languages/splits and normal/evidence-blind/
query-blind views. Save15states and strict-load/replay every view with logit drift<=1e-9,exact
argmax and final fingerprint preservation. Frozen core must equal its initial hash;core must
change in full/slow. Show configured trainable counts separately from actual gradient receivers.

Primary PASS iff ALL5 core_slow candidates pass EVERY unchanged five-character local/masked
criterion:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Report15 seed results,120 length/split partitions,80 correct-count contrasts against the two
controls separately,15gradient summaries,and paired-five contingency against EACH control.
Keep successes and regressions. No pooled old/new gate,per-question best-of,winning seed choice
or post-hoc ratio sweep. No new independent task coverage or general language capability claim.

## Workload,persistence and review

15models*1200=18000 scientific updates;864000training rows;21240forwards;1175040total row
presentations;84960core calls;15strictstate loads,one model-bundle write/read,network0.
This is1.5x C307's registered forward/update workload,not an exact wall-clock multiplier.
Seven outputs:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c308-core-lr-models-v1 and fold-c308-core-lr-eval-v1. Keep all LR histories and final outputs.
Full tensors,data and weights remain local/ignored;console mirrors compact receipt and aggregates.
The numeric postcheck rebuilds all outcomes without neural calls.

Own32/modules193/loaded4878/focused4877;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:c13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f.
Commit/re-fetch/separate review OWN6 before activation. Test actual optimizer groups,first-step
updates,full/frozen equivalence to accepted definitions,independent candidate reference loop,
run ordering/loader/replay,persistence,tamper detection,UTF8/CP932 and global-name binding.
Windows Validate requires34 real parents/pins,all5 schedules,actual-model probes,own32/full4877.
Retain dispatcher/launcher/runner ParseFile chain. Validate failure skips science/publication.
Any integrity failure repairs SAME C308;valid candidate miss is ACCEPTED VALID NEGATIVE.
C309 stays unregistered until formal C308 judgment. Gate F remains NOT PASSED.
