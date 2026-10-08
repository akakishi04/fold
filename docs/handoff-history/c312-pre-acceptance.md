# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted code/tests/preregistrations/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C311 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C312 ACTIVE / NOT YET JUDGED. C313 NOT REGISTERED.**
C312 is the unique ACTIVE value-balanced minibatch experiment;no C312 scientific result yet.
C309 remains ACCEPTED VALID NEGATIVE;C308 remains bounded ACCEPTED PASS.
Latest accepted scientific execution:a777fc793b2affe287d055733b012ea919504446.
Latest accepted published log:d894b4b26ffb821bcd89db17b70d4f9798d3e1ee. Do not rerun C311.

## Latest accepted evidence — C311

Acceptance:docs/experiment-ledger-addendum-c311-c312.md.
Acceptance commit:b583d14164fed3f6f03e0385e5d8c443138171f9.
Summary:runs/c311-v5b-error-context-2e3d082f8a9a4045b09dbe38a62ca6a8/summary.json.
SHA256:9bfdad83b33d24a986c3f76ef0e40d0ad323698b28826f80f659ff5fa6e0cdec.
Own24/focused4965 PASS;source712/protected1333;run_execution_valid=True.
Manifestb9e5f42cf681031892d77f2f134bc307d56233f22e039cac13009b3cd90b34fd.
51840 original answers classified,2160 pairs,720 language groups,90 signatures;zero neural work.
Seed309002 five-HOLDOUT error counts full/frozen/slow11/49/19;unmentioned-digit10/38/17;
other_fact1/11/2;non_digit0/0/0. Four-to-five shared errors3/33/13;new five-errors8/16/6;
resolved at five0/1/0. Slow has11 questions wrong at all four lengths.
Slow errors by ordered pair(0,2)/(1,3)/(2,0)/(3,1):7/3/1/8,each72 observations.
Failures span all4 HOLDOUT pairs,not one exceptional pair. These are descriptive findings,
not proof of a batching,attention or memorization cause. Keep capability and diagnostic PASS separate.

## Active C312 — TRAIN value-balanced minibatches

Experiment:C312-v5b-value-balanced-minibatches. Stage:V5-B-VALUE-BALANCED-MINIBATCHES.
Registration:docs/experiment-ledger-addendum-c312-preregistration.md.
Design:docs/v5b-value-balanced-minibatches-v0.1.md.
Review:docs/c312-post-authoring-review.md.
Acceptance base:b583d14164fed3f6f03e0385e5d8c443138171f9.
Authoring/review target:fe23ba10bba919790f73087f53719d0f1a123fba.

One question:at unchanged core_slow and complete epoch exposure,does balancing TRAIN ordered
value pairs in each minibatch improve unseen-five reliability versus the original random batches?
Fresh initialization seeds312001..312005 and order seeds312101..312105. Two arms random_pairs
and value_balanced. Both use actual C308 core_slow policy;this is NOT a new full/frozen comparison.
No old successful/failing model selection or learned-checkpoint reuse. All5 paired seeds remain.

Original TRAIN has8 ordered-value strata (difference1/3 modulo4),12 intact query pairs per stratum.
Original HOLDOUT difference2 is never introduced into TRAIN,including through value renaming.
Each epoch shares one randperm96 Generator(order+306000+epoch). Control takes consecutive24.
Candidate picks3 from each stratum's rank-preserving12-entry list,then restores global-rank order
within each batch. Every candidate update has24pairs/48rows and12 targets per digit0..3.
Both use all96 pairs once per epoch;no new random draws or value-sorted minibatches.
Length indexepoch%3,profile(epoch//3+epoch%3)%3 stay fixed for all4updates of that epoch.
All300epochs/1200updates retained;every row100 exposures per trained length2/3/4;profiles400each.
Only batch allocation and induced temporal order change. A positive result is not a unique
causal explanation of old errors or automatic generalization to other tasks.

Model:actual unchanged C278 plus C304 LengthReadout64slots,14256parameters,3328core,all trainable.
CE only,AdamW,noncoreLR.005/coreLR.0005,betas.9/.999,eps1e-8,decay0,clip1 before step,fitRNG612000.
Reuse C308 configure/parameter_groups/optimizer_for/verify_optimizer with core_slow for both arms.
No LR decay,auxiliary loss,gradient scaling,early stop or coefficient selection.
First actual losses need not match because minibatches differ. Instead same-input initial output,
preclip gradients and one optimizer step must match on discarded copies. Initial model weights
and per-epoch examples/lengths/profiles/exposure counts remain paired. Runtime also reproduces
old C309 random schedules at all5 original order levels,without retraining old models.

Primary:all5 NEW value_balanced models pass every original local/masked five-character gate.
Accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80 remain unchanged.
Evaluate all2/3/4/5,allprofiles/languages,normal/evidence-blind/query-blind,TRAIN/HOLDOUT.
5/HOLDOUT/masked inputs remain evaluation-only. No restricted decoding or repaired answers.
Report10results,80partitions,40contrasts and paired-five outcomes;no pooling to pass.
Strict-load and replay all10 final states with<=1e-9 logit difference and exact argmax.
Core must actually change in both arms. Gate F and prior verdicts do not change automatically.

## Parent semantics,protection and work

Verify38 ordered summaries BEFORE C311.verify_artifacts(parentdir,37ancestors,acceptedHEAD).
C311 writes three diagnostic JSON artifacts,NOT models or datasets. Read original C309 dataset.json
and length-datasets.json from paths[2] only after the complete parent verification;recheck canonical
hashes,prompts and targets. The report is not used for training. C311 summary seals its3 descriptors.
Sole direct import C311;its C310/C309 contexts supply C308optimizer,C304frame/render/eval/score/replay,
original pair helper,C287normalizer and backend. Explicit PINNED plus C304.PINNED and actual local
helper coverage enforce all712 inherited sources and1333 inputs. Add OWN6 and4parentfiles:
source718/protected1343. No accepted file edits or new regression exclusions.

Science:10models,12000updates,576000training rows,14160forwards,783360row presentations,56640corecalls,
10strict state loads,one model bundle write/read,network0. Operational probes/tests and recursive
parent verification are separate. Full neural fitting is performed;this is not a saved-only audit.
Seven outputs plus summary:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Schemasfold-c312-value-batches-models-v1
and fold-c312-value-batches-eval-v1. Save actual schedules,1200x8valuecounts,losses,LR/gradient traces,
initial/final/core fingerprints and full frozen final logits. Rebuild scores and schedules during
postcheck;no overwrite. Full tensors/maps stay local/ignored;compact receipt and aggregates in log.
Own32/modules197/loaded4998/focused4997;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:5c543202a3c252e69f3f099b369ef9905e39662a37947c8904756b17700fab2c.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus actually executed local software tests).
All6 OWN fetched atfe23ba10bba919790f73087f53719d0f1a123fba and hash-matched to local bytes6/6.
After matches:normal32/32 PASS18.876s;whole-suite CP932-default-emulated32/32 PASS19.660s.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No PowerShell installed in the review environment.
UTF8/noNUL,bothPython+3embedded blocks compile,undefined globals0,manifestselfhash matches.
Allnewseed epoch/exposure/stratum invariants,independent random/balanced schedule references,
toy1200step fit vs independent loop,actual train/replay/resource paths,parenthash/pin guards,
cohort/gate/tampering/roundtrip tests pass. Tests29/30 execute accepted C309/C304/C308 helper
function ASTs on controlled data/models. Local parent support consists of fetched function slices,
not full modules/repository;not committed. Actual parent archives,Git,scorers and suite members
are substituted where unavailable. Toy label-encoded inputs/padding test software,not FOLD skill.
Real38parentarchives/Windowspins,PowerShellParseFile,actualFOLDcommon-inputprobe,all4997 regression
and ten real training/evaluation/replay runs remain mandatory Validate/Execute gates.
Activation must preserve all6 reviewed OWN files and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C312 -> Validate(38parents,718/1343,
allnew value-balanced epoch budgets,old random-schedule compatibility,common-inputprobe,own32,
focused4997) -> authoring_runtime_preflight=PASS -> Execute(10models*1200steps,alllengthscores,
strict replay,plan/score reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failures repair SAME C312 under fixed
conditions. Valid primary failure is ACCEPTED VALID NEGATIVE. No post-result retuning of batching,
seeds,LRs,budget or thresholds. C313 waits for formal C312 judgment. Gate F NOT PASSED.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve immutable accepted seals and historical lifecycle tests.

## Historical state

Pre-activation handoff:docs/handoff-history/c312-pre-activation.md.
Git blob:77f3930e1e80928a86528caec459b3bb07af6c72.
Earlier handoff:docs/handoff-history/c311-pre-acceptance.md.
Git blob:630a9de299f81d80265480c58b5cf512c5ef4ff3.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
