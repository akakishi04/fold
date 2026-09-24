# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C246 ACCEPTED VALID NEGATIVE. C247 ACTIVE / NOT YET JUDGED. C248 NOT REGISTERED.**
C247 is the unique ACTIVE experiment:V5-B normal-exposure-matched TRAIN control,not a Gate F run.
Post-authoring review PASS. Authoritative Windows prechecks/full regression/scientific run pending.
C245 remains diagnostic-integrity PASS;C244 remains a valid recombination negative.

## Latest accepted evidence — C246

Scientific execution HEAD:c17195b7c0f80ae7dd60050e25dca6a3effc21fb.
Published log commit:30142c60dedf52537c9cef26b35ca2909446b5ee.
Publisher log SHA256:ceaec8ba66f2609acf18663c76b7925fb8053a91f8d199075b50d697ae566362.
Log bytes:589070.
Summary SHA256:9a462485dffc948674b7752012893a8175cdb5de251f179763ae03e26659623a.
Local summary:runs/c246-v5b-training-erasure-471de735eb204a129692672d2849c270/summary.json.

24 own tests PASS in3.973s;3073 focused tests PASS in71.197s.
322 source pins/502 protected inputs.6x400=2400 updates/76800 training presentations,
38400 normal+38400 masked. All six block_view_updates=[[100,100],[100,100]].
2490 forwards/81408 total rows;all replays/weight-update checks PASS;persisted normal endpoint,
comparator and discrete replay PASS. Protected inputs/tracked tree/execution HEAD preserved;
run_execution_valid=True. Scientific status FAIL;both augmentation gates False.

Exact outcome counts:TRAIN_CRITERIA_MISS10,RECOMBINATION_MISS2.
Only GRU-only seed234001 EN/JA meets all TRAIN criteria;both still miss HOLDOUT.
Normal TRAIN counts,EN/JA per model (each /32):
Full23400118/18;23400216/16;23400317/17.
GRU23400131/32;23400218/16;23400316/22.
Normal HOLDOUT counts,EN/JA per model (each /16):
Full2340015/4;2340026/6;2340038/8.
GRU2340016/9;2340027/8;2340036/6.

Descriptive pooled TRAIN:Full102/192 andGRU135/192,versus192/192 each in C244.
Descriptive pooled HOLDOUT:Full37/96 versus39/96;GRU42/96 versus41/96.
Combined79/192 versus80/192,with5 improving cells,2 ties,5 worse. The early conversational78-count
was corrected to79 using exact integer aggregation. No significance/independent-replicate claim.
The recipe did not establish a useful improvement and often lost TRAIN fit. It did not measure
masked-training-task accuracy;do not claim that the easy masked task was learned.

Acceptance/artifact identities:docs/experiment-ledger-addendum-c246-c247.md.
Acceptance/base commit:8559c95ec1716cc507f77f3d9271e19dcbd8ca28.
Log publication is one commit after scientific execution,changing only c246/latest.log/latest.json.
Acceptance is based on retrieved immutable log ranges and recorded local postchecks,not an
independent full-log byte rehash or reviewer execution of the actual trained checkpoints.
No C246 rerun,rescue,threshold relaxation or Gate F promotion.

## Preserved earlier evidence

C245 frozen diagnostic PASS:other-value erasure improved pooled masked HOLDOUT80/192->141/192,
but selective forms overlap across TRAIN/HOLDOUT and supply a relevance/copying cue.
C244:all full TRAIN criteria pass,all12 original HOLDOUT cells miss;normal80/192 pooled.
C243/C240/C237/C235 remain diagnostics;C242 recombination negative;C241 TRAIN criteria miss despite
normal100%;C239 order-transfer negative;C238 seen16-prompt fitting PASS;C236 random-batch negative.
All accepted evidence and earlier recovery records remain unchanged.

## Active C247 — normal-exposure-matched control

Experiment:C247-v5b-normal-exposure-control.
Stage:V5-B-NORMAL-EXPOSURE-CONTROL.
One question:is C246's amount of ordinary-example training sufficient to fit TRAIN when its
masked updates are absent? Do not continue tuning the augmentation before checking this control.

Fixed C244/C246 TRAIN64/HOLDOUT32,row bytes/order/provenance/targets and original scoring views.
Fresh Full13488/GRU-only10160,width16/48 slots,seeds234001/234002/234003. Match C246 initial_sha256,
not its trained final;these initial identities came from C244. Copy common GRU backbone before
either paired model trains. No parent checkpoint load or parent inference.

C247 has200 NORMAL updates/model,old32/added32 alternating100 cycles. Each TRAIN row appears100
normal times,matching C246's normal subset. Parent step map j ->4*(j//2)+2+j%2 is audited across
all200 steps,including actual normal-view selection and row-index equality.
No selective TRAIN input,masked update,zero-loss replacement,dummy forward or idle optimizer step.
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,CPU float64,threads2,
deterministic algorithms fixed. Normal fit AST equals C244 except label;STEPS is deliberately200.
Actual optimizer input tokens are checked independently against C244 row indices.

Normal exposure matches;total optimizer steps do NOT. Removing masked gradients changes optimizer
moments and step counts. A control-only TRAIN pass rules out reduced normal count alone as the
explanation for that cell's C246 miss. A control miss is compatible with an insufficient ordinary
budget but cannot exclude additional mixed-training effects. No unique internal cause is isolated.

PRIMARY:every Full TRAIN seed/language cell meets accuracy>=0.90,fact/query/order pair>=0.80,
evidence/query drop>=0.35. TRAIN32 rows/language,16 pairs:type minima29/32 and13/16.
GRU-only TRAIN gate independent. C247 status uses full_train_control_gate. A PASS is normal-budget
TRAIN sufficiency only,not a diagnostic-only PASS and not held-out generalization.
Original HOLDOUT and secondary joint TRAIN+HOLDOUT family gates are reported separately with
unchanged criteria,but do not decide this control's primary verdict. C246/Gate F are never revised.
This endpoint change is preregistered for the different control question,not a rescue of C246.

Per-cell comparison labels:BOTH_TRAIN_PASS,CONTROL_TRAIN_PASS_ONLY,C246_TRAIN_PASS_ONLY,
NEITHER_TRAIN_PASS. Retain exact C246.final as c246_comparator and its saved C244 comparator;
both cover the identical rows and are reused accepted evidence,not newly repeated baselines.
Only TRAIN is scored initially. Original HOLDOUT reaches evaluation after step200 and reload.
No tuning,early stop,seed selection,best-checkpoint selection or automatic extra run.

Workload:6x200=1200 updates/38400 normal training presentations,zero masked updates.
90 scoring forwards/4608 scoring rows;1290 total forwards/43008 total rows.
Before replay209 calls/6880 rows per model;after215/7168. block_updates=[100,100].
One six-state bundle,schema fold-c247-normal-exposure-v1;zero scientific network calls.
Reuse C244.replay_one with fitting=C242;do NOT apply C244's400-update summarizer to child records.
Parent measurement replay uses C246.summarize(refs,C244,C242),then C243 discrete metric replay.
Child summarizer checks its own shortened-workload/primary-gate contract.

Protection:328 source pins/514 inputs;direct dependency union23;OWN6.
Own tests24;modules132;loaded3098/focused3097,only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Own tests reuse already-pinned C246 synthetic helpers;scientific code never calls test helpers.
Five ignored outputs:control-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Postcheck verifies all hashes/sizes,plan/partition,summary,initial IDs,
both unchanged comparators and child discrete metrics. Exact prediction and1e-9 logit/metric replay.

Fixed partition:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346.
Manifest:f9558bfead121a605f8cc2dd776eed5db6db981c1c20b675d44d49d4b95a502c.
Design:docs/v5b-normal-exposure-control-v0.1.md.
Registration:docs/experiment-ledger-addendum-c247-preregistration.md.
Preregistration/review HEAD:3c374bd083ae5b5594e5b35168c6f6d2c08905b0.
Use tools/invoke_active.ps1 with the final activation HEAD,not C246 or the pre-activation review HEAD.

## C247 post-authoring review

`post_authoring_review = PASS`
Review HEAD:3c374bd083ae5b5594e5b35168c6f6d2c08905b0.
Scope:committed-byte authoring and synthetic-path verification,not scientific C247 results.

All six OWN files were re-fetched after authoring. Reviewed Git blobs:
-benchmark:02030b9de03c1fa1b4aca2c53b0ae673064850a0
-tests:fe5ac42c133469a631a47f65e51252991b9d4593
-runner:8e000a3a39ec00e52fe83dafa8e22214c48e0680
-launcher:9f1bb8361cdad14ba25b58737c9bf851ff1fec22
-design:759953316670ba7927597a65452b6e6248b78e85
-preregistration:552a60c8cc8db91d0dabb41d9b5cf0f6e14b21cd.
All four complete code/script files were locally Git-blob hashed and matched the fetched identities.
Base-to-review comparison has exactly six additions,no accepted file edits. A local bracket typo
was caught by compile and fixed before any code publication or authoring test result.

Actually executed on the matched new source:
-UTF-8/NUL and Python compile/import checks;symbol-table free-global/import audit:0 unresolved names;
-24 own tests PASS before publication in3.293s and after remote readback in2.885s;
-actual own unittest count/unique IDs and a constructed3098-case exclusion filter yielding3097;
-manifest and reconstructed exact partition hashes;
-all200 mapped normal parent steps,per-row100 exposures,optimizer AST/constants and wrong-block rejection;
-actual200-update train helper and parent replay helper on toy models:209+6 forwards/6880+288 rows;
-initial-ID barrier,holdout-after-fit ordering,failed-fit hook cleanup,bad-logit replay rejection;
-primary TRAIN versus secondary HOLDOUT separation,full/GRU separation,mask criterion at100% normal;
-four comparison labels,parent record adapter and both saved comparator fields;
-synthetic six-model run/save/reload/postcheck,wrong-HEAD and artifact-tamper rejection;
-three embedded Python block compiles,CLI argv1 then1/2/3,parser-before-publication and exact parent path.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. The isolated workspace contains the
complete new code/script files,transcribed C244 fit/replay/summarize and C246 schedule/summarize
excerpts with import scaffolding,and transcribed inherited synthetic utility classes from the C246
test module. It is NOT a full checkout or execution of the real FOLD model. Parent source/signatures
and writer timing were reviewed from retrieved repository content;tests exercise those excerpts
and substitute protection/loaders/evaluators where specified. No actual accepted checkpoint was run.
The container could not resolve github.com,so there was no complete checkout. PowerShell absent.
NOT executed here:full3097 historical suite,Windows PowerShell AST,accepted user-local artifacts,
scientific C247 normal-only models. None is represented as PASS. The authoritative launcher/runner
must execute them. Count arithmetic3074+24=3098,minus the same one exclusion=3097 is enforced there.

Only this unpinned handoff changes after review HEAD. Re-read it and confirm branch HEAD before
returning ExpectedHead. Do not advance the experiment branch during the user's formal run.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted evidence and tools/run_c167.ps1.
No model expansion,paid API,external corpus,inference mask fix,cleanup,history rewrite or production change.
24 own tests ->3097 focused tests ->C247 control ->postcheck ->remote log publication.
Stop same C247 on integrity faults;repair log-only transport without retraining. Judge C247 before C248.
