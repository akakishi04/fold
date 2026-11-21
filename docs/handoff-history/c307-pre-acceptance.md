# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C306 ACCEPTED VALID NEGATIVE. C307 ACTIVE / NOT YET JUDGED. C308 NOT REGISTERED.**
C305 remains diagnostic PASS;C304 remains valid negative. C307 is the unique ACTIVE replication.
Latest accepted scientific execution:cb2bb51a8beaa888c3a8b1fca382cd20536c923b.
Latest accepted published log:340f9034fc07df63cff928bfd13703dfee5ca379. Do not rerun C306.

## Latest accepted evidence — C306

Acceptance:docs/experiment-ledger-addendum-c306-c307.md.
Acceptance commit:0012e1fb0d293cf2082c545c92ee2d7f5a6f8e01.
Summary:runs/c306-v5b-broad-core-freeze-f8b13e726f314db09555a293f6d6bdf8/summary.json.
SHA256:5435cf83c02b75c2dd1d3c21105dcdf30e8c567c9d8672993f7676166515cff3.
Own32/focused4813 PASS;source682/protected1267;all_pairs_matched=True;run_execution_valid=True.
Manifest28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27.
Length2/3/4/5 full_train passes4/3/3/3 out of5;core_frozen passes5/5/5/4 out of5.
Fitted TRAIN direct full4/frozen5;trained-length HOLDOUT direct full3/frozen5;all-length full3/frozen4.
Candidate rescues306002 and306005,loses306003;both pass306001/306004.
All5 frozen states answer every normal2/3/4 TRAIN/HOLDOUT question correctly. At5,the sole
candidate normal error is306003 HOLDOUT287/288. All candidate5TRAIN-value rows are correct.
Pooled4319/4320 is descriptive,not the registered all-five gate. C306 remains negative.
306005 full TRAIN2/3/4/5=512/514/512/513 out576;HOLDOUT=136/130/131/130 out288.
Frozen306005 is perfect in all partitions. Actual gradient union full14256/frozen10928.
Core remains in forward and input-backward paths;no core necessity/irrelevance or speed claim.
Five paired seeds do not establish a universal freezing policy or a unique training mechanism.

## Active C307 — fresh-seed replication without policy retuning

Experiment:C307-v5b-core-freeze-replication. Stage:V5-B-CORE-FREEZE-REPLICATION.
Registration:docs/experiment-ledger-addendum-c307-preregistration.md.
Design:docs/v5b-core-freeze-replication-v0.1.md.
Review:docs/c307-post-authoring-review.md.
Acceptance base:0012e1fb0d293cf2082c545c92ee2d7f5a6f8e01.
Authoring/review target:b1394c51ad6a451c808eb16d57397595c1f30cb6.

One question:does the C306 core-freeze benefit recur on a new paired initialization/order seed
cohort under unchanged policies? Do not tune a remedy for the one remaining old error.
Fresh init seeds307001..307005,order seeds307101..307105. Repeat full_train and core_frozen
concurrently. No old model/optimizer state,successful donor,loss change,coefficient or new length.
Report the new cohort separately;keep all five controls and candidates and retain C306 negative.

Actual accepted C304 LengthReadout,64slots,14256stored parameters. Full trains14256;candidate
trains10928 with3328core weights fixed at that seed's random initialization. Core forward and
backward-to-input still execute. Compatible C306.configure/first_batch_probe are reused.
The child owns seed-sensitive factory/fit/analysis and never mutates accepted module constants.
Matched state dictionaries/independent storage within each pair;all noncore weights train.

Ordinary meanCE,one AdamW1200steps,lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1.
Same scheduling algorithm:300epochs*4,96 intact query pairs,24pairs/48rows per minibatch;
private randperm96(order+306000+epoch),length=2+epoch%3,profile=(epoch//3+epoch%3)%3.
SHUFFLE_OFFSET306000 and FIT_RNG612000 intentionally remain C306 values. Each row100exposures
per trained length2/3/4 and each profile400updates. Pairwise events and first CE must match.
Only init/order seed pairs change. No5/HOLDOUT/masked learning,no early stop or checkpoint choice.

Freeze/evaluate2/3/4/5 all original normal/evidence-blind/query-blind views. Save all10 states,
strict-load/replay with drift<=1e-9 and exact argmax. Frozen core hash equals initial;full core
changes. Retain1200losses/events,gradient-receiver union/counts and final logits. Primary PASS
iff all5 NEW candidates pass every unchanged five-character local/masked criterion. Thresholds:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Valid miss is valid negative.
Report80partitions,40contrasts,10gradient summaries and five-seed both-pass/full-only/frozen-only/
both-fail contingency. No average or old-model pooling can replace the new all-five gate.
Even a5/5 candidate is not automatic superiority to a5/5 control or universal reliability.
Fresh seeds are not fresh tasks,an external/blinded replication or Gate F completion.

## Parent contract,protection and workload

Verify33 summary hashes before exact C306.verify_artifacts(parent_dir,32ancestors,acceptedHEAD).
It returns(payload,metrics). Tail:C305summary,C304summary,C303..C274 via immutable parent helpers.
Require C306statusFAIL,all_pairs_matched/all_replays,exact10original flags and seven artifact
inventory. Its exact summary seals all descriptors and recursive verifier reconstructs old scores.
Read only verified C306 dataset.json/length-datasets.json for learning;canonical hashes checked,
C304 prompts regenerated/validated. Never use old predictions or trained checkpoints as new targets
or initial weights. C306 writer records actual final frozen evaluation logits,not interim outputs.

Sole direct import C306;context supplies C305 no-neural,C304 helpers,pair builder,C287 normalizer,
C283 transfer and original backend. Retain682 inherited sources/1267 inputs;check actual context/
core/factory-language modules and C304.PINNED. Add OWN6+8parent inputs:source688/protected1281.
No accepted sources/tests/logs/preregistrations/dispatcher or old exclusion changes.

Work:10models,12000updates,576000training rows,14160forwards,783360totalrows,56640corecalls,
10strictstate loads,one bundle write/read,network0. Same registered work as C306. Backward work
and clipping still differ between the two policies;do not claim equal FLOPs or runtime.
Operational probes/tests/parent verification are separate from science.
Seven outputs:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c307-replication-models-v1 and fold-c307-replication-eval-v1. Full data/tensors stay local/ignored;
compact receipt,aggregates and paired-five contingency in console. Numerical reconstruction
executes no model. Own32/modules192/loaded4846/focused4845;sole inherited C204 exclusion unchanged.
Manifest9662b7d5763768a09c75c961dc8f8453c40506eadcbb44639bbd50f7dca2ab8b.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static plus executed local software tests).
OWN6 fetched atb1394c51ad6a451c808eb16d57397595c1f30cb6 and matched to local Git hashes6/6.
Post-match normal own32 PASS11.677s;whole-suite CP932-emulated own32 PASS10.652s.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;bothPython/3embeddedblocks compile;globals0;
UTF8/noNUL;manifest matches. Actual child1200-step fits equal isolated accepted C306 definitions
on toy inputs for losses,gradient metadata and final weights. All5 schedules equal the old
algorithm with new seeds. Actual C304 LengthReadout fixtures verify initial outputs/noncore
gradients,core freeze,64frame/state/storage. Production run/bundle ordering and reconstruction,
33hash guards,688/1281 accounting,no overwrite and byte/semantic tampering are exercised.

Only OWN6 are byte-identical;local support is selected fetched C306/C304 definitions,not full
parent modules or a complete repository. Controlled backends,targets,Git,scorers,replay callbacks
and inherited-suite members substitute for unavailable real inputs. Core-call accounting in the
toy train_one test is a stand-in. No real FOLD performance or full4845-suite success is claimed.
Windows33parent archives/pins,actual first-batch model gradients,PowerShellParseFile,full4845
and ten actual FOLD fits/evaluations/replays remain mandatory local gates. Activation preserves
all6 reviewed OWN blobs and every accepted file/dispatcher. See review for full limitations.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C307 -> Validate(33parents,688/1281,
unchanged-policy check,all5 schedules,actual initial-state/gradient probe,own32,focused4845) ->
authoring_runtime_preflight=PASS -> Execute(10models*1200steps,2/3/4/5scores,coreinvariants,
strictreplay,savedreconstruction) -> log publication. Validate failure skips science/publication.
Integrity failure repairs SAME C307. No retuning or replacement of failed seeds. Do not repeat
seed hunting until success. C308 stays unregistered until C307 formal judgment. Gate F remains
NOT PASSED;C306's valid negative is never superseded by a favorable new cohort.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c306-pre-acceptance.md.
Git blob:bedaf979e8a04fddfd7af0ad2d7476eda74a7dd5.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
