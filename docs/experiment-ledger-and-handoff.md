# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C307 ACCEPTED VALID NEGATIVE. C308 ACTIVE / NOT YET JUDGED. C309 NOT REGISTERED.**
C306 remains valid negative. C308 is the unique ACTIVE core-only learning-rate comparison.
Latest accepted scientific execution:4371ad8de650261f6cdacacfd9972efcdbe970a8.
Latest accepted published log:6cdbde45709579c736d2fc0bd682f992a6d63b25. Do not rerun C307.

## Latest accepted evidence — C307

Acceptance:docs/experiment-ledger-addendum-c307-c308.md.
Acceptance commit:49bf2b96faa9afcee97bbce3840e1164b498fcd8.
Summary:runs/c307-v5b-core-replication-468c370e9c4b491585226c5492a8b52c/summary.json.
SHA256:5cb0683de649361966f2ab549aeab94d20643d64fe68d1d8bbe3497e6d637e42.
Own32/focused4845 PASS;source688/protected1281;all_pairs_matched=True;run_execution_valid=True.
Manifest9662b7d5763768a09c75c961dc8f8453c40506eadcbb44639bbd50f7dca2ab8b.
Length2/3/4/5 full passes3/3/3/3,frozen4/4/4/3. Both arms TRAIN direct4/5.
Trained-length HOLDOUT direct full3/frozen4. Both-pass2,full-only1,frozen-only1,both-fail1.
Frozen rescues307002,but loses307001 at5;both fail307005 including TRAIN. C306's five-character
pass-count advantage was not reproduced. Individual seen-length effects remain;not evidence of
zero freezing effect or a universal core mechanism. No pooling/seed hunting replaces either gate.

307001 frozen five TRAIN575/576,HOLDOUT287/288 versus full perfect;two normal errors.
307002 full fits TRAIN but HOLDOUT2/3/4=133/133/136 out288;frozen passes all lengths.
307005 full TRAIN2/3/4/5=518/525/524/517 out576,HOLDOUT103/107/107/105 out288.
Frozen307005 TRAIN517/519/514/509,HOLDOUT115/119/119/124. Freezing did not remove its TRAIN failure.

## Active C308 — core-only learning-rate attenuation

Experiment:C308-v5b-core-learning-rate. Stage:V5-B-CORE-LEARNING-RATE.
Registration:docs/experiment-ledger-addendum-c308-preregistration.md.
Design:docs/v5b-core-learning-rate-v0.1.md.
Review:docs/c308-post-authoring-review.md.
Acceptance base:49bf2b96faa9afcee97bbce3840e1164b498fcd8.
Authoring/review target:22bbc839cb24bab585573d3c4838875b43eaa431.

One question:at unchanged broad2/3/4 learning and unseen5 evaluation,does nominal coreLR0.0005
with noncoreLR0.005 improve reliability versus full learning and complete core freezing?
Ratio0.1 is a single prospective coarse choice,not an inferred optimum or a sweep. No proven
core-instability mechanism is assumed. Do not continue searching seeds until a favorable result.
Fresh initial seeds308001..308005,order seeds308101..308105;all3 concurrent arms per seed:
full_train all14256 train at0.005;
core_frozen3328core weights fixed at their own random initial values,10928noncore train at0.005;
core_slow(candidate) all14256 train,noncoreLR0.005 and coreLR0.0005.

Actual accepted C304 LengthReadout,64slots,14256stored parameters. Independent copies of identical
state within each seed. No model/data/mask/forward changes,no coefficient,detach,auxiliary loss,
core removal or adaptive unfreezing. Frozen core still computes and passes gradient to its inputs.
Core optimizer membership is checked by object IDs and backbone.core.* names. Full/frozen retain
one-group ordering;candidate uses noncore/core groups. Clip global norm1 in ORIGINAL model order
before AdamW;do not scale core gradients before clipping. Record/check group membership and LRs
at every step. Full/slow paths initially agree;later gradients/moments/weights can diverge.
Frozen capacity and backward work differ;no identical FLOPs/runtime or final1/10-update claim.

All arms ordinary meanCE,one AdamW1200steps,betas.9/.999,eps1e-8,weight_decay0.
C306/C307 scheduling algorithm unchanged:300epochs*4,96 intact query pairs,24pairs/48rows,
private randperm96(order+306000+epoch),length=2+epoch%3,profile=(epoch//3+epoch%3)%3.
FIT_RNG612000 reset per model. Each row100exposures per trained length;each profile400updates.
All initial hashes,events and firstCE agree within each three-arm group. Only normalTRAIN2/3/4
is optimized. Five-character/HOLDOUT/masked views are evaluation-only. No early stop/extra epochs.

On discarded first-seed copies,C306 full/frozen probe verifies initial output/noncore preclip
gradient agreement,absent frozen core grads and preserved encoder signal. Child full/slow probe
requires exact initial logits/allpreclip gradients,then performs one discarded update each:
core delta0.1ratio and equal noncore delta within1e-12. Original scientific models stay unchanged.
These2probe updates are operational,not the scientific budget or a checkpoint selection step.

Freeze final states;evaluate2/3/4/5 all original profiles,languages,value splits and all3 views.
Save15states,strict-load/replay each with drift<=1e-9,exact argmax,unchanged final fingerprints.
Frozen core must equal initial;full/slow core must change. Persist1200group-LR/loss/event records,
gradient-receiver union/counts,core hashes and final logits. Primary PASS iff ALL5 core_slow
models pass every original-style five-character local/masked criterion. Thresholds:accuracy.90,
query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Valid miss is ACCEPTED VALID NEGATIVE.
Report15results,120partitions,80candidate-versus-each-control contrasts,15gradient summaries and
paired-five contingencies against both controls. Candidate5/5 is not automatic relative superiority,
arbitrary-length capability,production adoption or Gate F completion. No post-hoc ratio selection.

## Parent contract,protection and workload

Verify34 summary hashes before exact C307.verify_artifacts(parent_dir,33ancestors,acceptedHEAD).
It returns(payload,metrics). Require parentFAIL,exact10seed flags,paired-five2/1/1/1,matched pairs
and replays. Exact parent summary seals7output descriptors. Writer stores final post-fit logits,
not interim/action-selected outputs. Read verified dataset/prompts only;regenerate C304 prompts
and check canonical hashes. Do not use old predictions as targets or old learned initial weights.

Only direct repository import C307;context exposes C306probe,C305no-neural,C304helpers,pairbuilder,
C287normalizer,C283transfer and backend. Child owns new-cohort policy;no parent monkeypatching.
Retain688sources/1281inputs,verify actual context/core/factory-language sources and C304.PINNED.
Add OWN6 and8parent files:source694/protected1295. Accepted files and exclusions remain unchanged.

Work15models,18000updates,864000training rows,21240forwards,1175040total row presentations,
84960core calls,15strictstate loads,one bundle write/read,network0.1.5x prior registered update/
forward workload,not exact runtime. Operational probes/tests/recursive verification are separate.
Seven outputs:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c308-core-lr-models-v1 and fold-c308-core-lr-eval-v1. Full weights/data/tensors stay ignored/local.
Console mirrors compact receipt and aggregates;numeric postcheck reconstructs without model calls.
Own32/modules193/loaded4878/focused4877;sole inherited exact C204 exclusion unchanged.
Manifestc13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static and executed local software tests).
All6 OWN refetched at22bbc839cb24bab585573d3c4838875b43eaa431 and matched to local Git hashes6/6.
Post-match normal32 PASS17.596s;entire CP932-emulated32 PASS17.232s.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. BothPython/3embeddedblocks compile;globals0;
UTF8/noNUL;manifest matches. Actual1200-step childloops tested for all arms. Full/frozen controls
match accepted extracted C307 definitions;candidate matches independent optimizer-group reference.
Initial full/slow gradient/first-step checks pass. Actual toy core forward hooks measure resource
counts;these are not measurements of the actual FOLD backend. Actual child run/bundle paths verify
15fits then15replays,roundtrip,no overwrite and byte/semantic tamper detection.

Only OWN6 are byte-identical. Parent support is selected C307schedule/fit,C306probe,C304schedule_stats
functions,not full parent modules or repository clone. Factory uses substitute LengthReadout/backend,
not actual C304 class execution in this local review. Parent archives,Git,scorers and replaycallbacks
are substitutes where unavailable. CP932 emulates Path decoding,not all Windows behavior.
Windows34parents/pins,PowerShellParseFile,actual-model gradient/optimizer probes,the full4877suite
and all15actualFOLD fits/evaluations/replays remain mandatory gates. No actual FOLD science was
run here. Activation must keep all6 reviewed blobs and all accepted code/tests/logs/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C308 -> Validate(34parents,694/1295,
all5schedules,initial full/frozen gradients and full/slow optimizer-step probe,own32,focused4877)
-> authoring_runtime_preflight=PASS -> Execute(15models*1200steps,2/3/4/5scores,coreinvariants,
strictreplay,savedreconstruction) -> logpublication. Validate failure skips science/publication.
Integrity failure repairs SAME C308. No ratio,seed,budget,freeze schedule or threshold changes
after outcomes. C309 waits for formal C308 judgment. C306/C307 negative verdicts and Gate F remain.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c307-pre-acceptance.md.
Git blob:e202ed37a170da9f2da791b4392560f1c35f0473.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
