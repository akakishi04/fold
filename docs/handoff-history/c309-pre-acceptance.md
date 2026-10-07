# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted code/tests/preregistrations/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C308 ACCEPTED PASS. C309 ACTIVE / NOT YET JUDGED. C310 NOT REGISTERED.**
C308 PASS is bounded capability,not merely diagnostic integrity. C309 is the unique ACTIVE replication.
Latest accepted scientific execution:2fc902e8c7f57579087a61e25e7c1e88f8c66090.
Latest accepted published log:045de9e384e6d19f35b48722a55b3fac1062ddbd. Do not rerun C308.
C306/C307 valid-negative verdicts remain unchanged. No automatic Gate F or production promotion.

## Latest accepted evidence — C308

Acceptance:docs/experiment-ledger-addendum-c308-c309.md.
Acceptance commit:1e534105f5ac29b4e6f128adc3b47baa4e31966b.
Summary:runs/c308-v5b-core-lr-02b24ac7b9da4a36a14a5545bd42aab6/summary.json.
SHA256:42a2dbc75c6bf958bff26315f918fc999728196eac7fe890eee28aa392f63c8a.
Own32/focused4877 PASS;source694/protected1295;all_groups_matched=True;run_execution_valid=True.
Manifestc13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f.
Every length2/3/4/5:full_train4/5,core_frozen5/5,core_slow5/5;all-length likewise4/5,5/5,5/5.
Fitted TRAIN direct5/5 in all arms;trained-length HOLDOUT direct4/5,5/5,5/5.
Full_train308002 fits TRAIN but HOLDOUT2/3/4/5=77/79/80/81 out288;frozen/slow each288/288.
Candidate meets the absolute all-five gate but has no pass-count superiority over frozen.
Paired against full:both-pass4,candidate-only1,control-only0,both-fail0;against frozen:both-pass5.
No broad reliability,optimal-ratio,arbitrary-length or Gate F claim is authorized.
Evidence reviewed is the published immutable receipt/postcheck,not direct access to local tensors.

## Active C309 — unchanged-policy fresh-seed replication

Experiment:C309-v5b-core-lr-replication. Stage:V5-B-CORE-LR-REPLICATION.
Registration:docs/experiment-ledger-addendum-c309-preregistration.md.
Design:docs/v5b-core-lr-replication-v0.1.md.
Review:docs/c309-post-authoring-review.md.
Acceptance base:1e534105f5ac29b4e6f128adc3b47baa4e31966b.
Authoring/review target:a5df5534002eb7878b05df6fbf1a09d04925705f.

One question:does C308's core_slow all-five result recur on one new paired initialization/order
cohort with BOTH controls retained? New initial seeds309001..309005,order seeds309101..309105.
Keep15states:full_train,core_frozen,core_slow for every seed. Do not reuse old learned weights or
select favorable cores. No ratio search,new length,loss change or training-budget increase.

Actual accepted C304 LengthReadout,64slots,14256stored parameters. Full trains14256 atLR0.005.
Frozen excludes3328core parameters and trains10928noncore at0.005 while retaining core forward
and backward-to-input. Slow trains14256 with noncoreLR0.005 and coreLR0.0005. No signal detach,
learned gain,output filter or model change. All three initial states match within each seed and
have independent parameter storage. Core must remain unchanged only for frozen.

Use exact C308.configure,parameter_groups,optimizer_for,verify_optimizer and first_batch_probe.
Child owns new-seed factory,schedule,fit and analysis;no parent module mutation. policy_contract
checks unchanged optimizer/data/schedule/gates and disjoint seeds. One AdamW per model,betas.9/.999,
eps1e-8,weight_decay0,ordinary meanCE,1200updates. Global clip1 uses original model parameter order
before AdamW;do not shrink core gradients before clipping. Every step verifies and records LRs.

Keep300epochs*4,96intact pairs,24pairs/48rows per update. Shuffle seedorder+306000+epoch;
length2+epoch%3;profile(epoch//3+epoch%3)%3. FIT_RNG612000 unchanged and reset per model.
Each TRAIN row100exposures at each length2/3/4;each profile400updates. Five,HOLDOUT and masked
views are evaluation-only. No early stop,extra epochs or intermediate-checkpoint selection.

On discarded first-seed copies,the inherited probe checks full/frozen initial outputs/noncore
gradients and encoder connectivity;full/slow preclip gradients match and first core update is
0.1 of full within1e-12 with equal noncore update. Two probe updates are operational,not scientific.
Original initial fingerprints are rechecked after probing. No claim of later1/10 update ratios.

Evaluate all15final states at2/3/4/5,all profiles,languages,splits and normal/evidence-blind/query-
blind views. Save15states and strict-load/replay with drift<=1e-9 and exact argmax. Frozen core
hash stays initial;full/slow core changes. Report1200loss/LR/event records and gradient union/counts.
Primary PASS iff ALL5 NEW core_slow states pass every original five-character local/masked
criterion:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Valid miss is ACCEPTED VALID NEGATIVE. Never pool C308 successes into C309's primary gate.

Report15results,120partitions,80candidate-versus-each-control contrasts,15gradient summaries and
two paired-five contingencies. A new5/5 is not automatic superiority over a5/5 frozen control,
new task coverage,universal reliability or deployment readiness. Keep C308PASS independent of
C309's verdict. Do not keep generating cohorts until success. Gate F remains NOT PASSED.

## Parent contract,protection and workload

Verify35 ordered summary hashes before exact C308.verify_artifacts(parent_dir,34ancestors,
acceptedHEAD). Tail is immutable C308.parent_hashes(). Require statusPASS,all_groups_matched,
all_replays,exact15 parent flags and both paired-five tables. Parent summary seals7descriptors.
C308 writer stores final frozen logits and1200loss/LR/gradient/event records;its verifier rebuilds
scores and invariants. Only verified dataset.json/length-datasets.json become learning inputs.
Recheck canonical hashes/prompt regeneration;no old predictions as targets or checkpoint reuse.

Only direct import C308. Context supplies C307,C306probe,C305no-neural,C304wide,pair builder,
C287normalizer,C283transfer and backend. Retain694sources/1295inputs;check actual repository-local
context/core/factory-language modules and all C304.PINNED. Add OWN6+8parent files:700/1309.
No accepted code/test/log/dispatcher or inherited exclusion changes.

Work15models,18000updates,864000training rows,21240forwards,1175040totalrows,84960corecalls,
15strictstate loads,one bundle write/read,network0. Same as C308. Backward costs differ by policy;
equal update/forward counts are not equal backward FLOPs or runtime. Operational probes/tests/
recursive verification are separate. Seven outputs:architecture-plan.json,dataset.json,
length-datasets.json,trained-models.pt,evaluations.pt,measurements.json,validation-summary.json,
plus summary.json. Schemas:fold-c309-core-lr-replication-models-v1 and fold-c309-core-lr-replication-eval-v1.
Full data/tensors/weights remain local/ignored;compact receipt and aggregates are mirrored.
Numeric postcheck reconstructs without model execution. Own32/modules194/loaded4910/focused4909.
Sole inherited exact C204 exclusion unchanged.
Manifest9350f7a5ec4e91a3292f6ecce041bc3ec09f1fa1a8372a4178b58d0ceb4df74d.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static plus executed local software tests).
OWN6 refetched ata5df5534002eb7878b05df6fbf1a09d04925705f and matched6/6 to local Git blobs.
Post-match normal32/32 and CP932-emulated32/32 passed with0failures/0errors. Due to one-shot tool
time limits,each complete module was run as one class setup,32ordered TestCase.run calls in a
persistent Python process,and one teardown. No tests omitted. CP932 patch covered setup/alltests.
Active setup+test sums59.015s/61.138s exclude tool pauses;not standard uninterrupted runner timing.
Synthetic temporary files used/dev/shm locally;registered files unchanged. Interrupted shell runs
are not counted as successful full suites. Full method is documented in the review.

Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. BothPython/3embeddedblocks compile;globals0;
UTF8/noNUL;manifest matches. Actual child1200-step loops for all3arms match isolated C308 definitions
for losses,LR/gradient histories and final weights. All5 schedules match;optimizer/RNG/corefreeze/
clipping-order,initial-probe,35hash guards,700/1309 accounting,run/bundle/replay ordering and byte/
semantic tamper tests pass. Synthetic suite-ID test checks4910->4909,not actual legacy execution.

Only OWN6 are full byte-identical copies. Parent support is selected fetched C308/C306/C304
function definitions,not full parent modules or a repository clone. Toy target-coded inputs,
substitute LengthReadout/backend,Git,artifacts,scorers and replay callbacks are controlled fixtures.
Actual C304 model/FOLD backend and user tensors were not run locally. Windows35parents/protected
bytes,PowerShellParseFile,actual gradient/optimizer probes,full4909regression and15realFOLDfits/
evaluations/replays remain mandatory. Activation must preserve all6reviewed files and accepted code.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C309 -> Validate(35parents,700/1309,
unchanged-policy check,all5 schedules,actual initial/probe checks,own32,focused4909) ->
authoring_runtime_preflight=PASS -> Execute(15models*1200updates,2/3/4/5scores,core invariants,
strict replay,saved reconstruction) -> log publication. Validate failure skips science/publication.
Integrity failure repairs SAME C309 with fixed seeds/ratio/budget/gates. C310 waits for formal
C309 judgment. Keep C308 bounded PASS,C306/C307 negative verdicts and Gate F NOT PASSED distinct.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c308-pre-acceptance.md.
Git blob:528b2ed36503065cf218377cd353669c24ab2396.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
