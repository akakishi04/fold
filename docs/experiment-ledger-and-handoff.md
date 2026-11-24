# FOLD experiment ledger and handoff

Updated: 2026-11-25 Japan time.
Conversation protocol:docs/experiment-conversation-handoff-protocol.md,Current response format v2.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C345 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY).** Execution C345-R0 valid.
C344 remains ACCEPTED VALID NEGATIVE,candidate_gate=false/eligible_seed_count=2.
C344attempt01 remains INVALID. No capability improvement or production adoption.
**C346 ACTIVE / INVALID ATTEMPT RECOVERY.** Attempt01 is INVALID EXECUTION; retry SAME C346.
Three-arm fixed-budget pair-max learning-rate comparison remains scientifically unjudged.
C347 NOT REGISTERED. Do not rerun accepted C344/C345.

## Current C346 documentation recovery

Contract:docs/c346-recovery-r1.md. This is documentation recovery1,not an executor revision.
The executable revision remains C346-R0;all seven original OWN blobs remain unchanged.
Scientific execution:e19e872577d7f574920e83b568499666f2cd41e4.
Failed-attempt publication:3b70c50464ac60ff202c8c8fad4d01c200ed9d06.
Exact failed logs:docs/experiment-run-logs/c346/attempt-01/latest.log and latest.json.
Original Windows158908bytes/SHA25687f33308c45d299e165923dfc4d8f7b3b82ebce87ab2876b07098ebf247f4419.
Git LF157018bytes/1890LF exactly reconstructs that original. Publication succeeded.

The C345 acceptance handoff rewrite f5fc8e8 omitted the permanent C272 compatibility seal.
Attempt01 passed six native cleanup checks,locks,parent semantics and native objective preflight,
then failed C272 test24 at module index156. 157modules began;156completed successfully.
3693tests ran:3692passed/1failure/0errors/0skips;2959tests/86modules were not reached.
No formal C346 fit,optimizer update or cohort evaluation began. No scientific verdict exists.
The final science-failed exception propagates the regression error,not a model result.

Restore the true historical C272 seal in the append-only compatibility section below.
The accepted C273 recovery and authoring-runtime gate explicitly require its retention.
No scientific/source/test/manifest change,new exclusion,skip or partial-success reuse.
Before retry,check all11live-handoff consumers C272..C282 on the final handoff bytes,
the actual6652ID inventory/6578parent prefix,the unchanged7OWN blobs and uniqueC346ACTIVE.
Every later handoff rewrite must retain the compatibility section and repeat that review.

post_authoring_review = PENDING
Independent committed-remote review and documentation-only activation remain required.
The original source-only review below is historical and does not authorize this retry.
Do not use the old executionHEAD,publicationHEAD,original sourceHEAD or a main merge.
Preserve the user-local invalid run. No automatic retry and no C347 registration.

## Latest accepted evidence

Report:docs/experiment-ledger-addendum-c345-c346.md.
Acceptance:f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2.
Scientific execution:c81ffe102c3a9280f28a68e572403549ce77fa1d.
Publication:25ff2f93ce63c9668f3111672caf75db095d2f45;soleparent execution,onlylatest.log/json.
Original Windows759318bytes/SHA2569531d1f7ae6e9be8c220954dd0f233a9c20844e94a983765d0b673105865fc9a.
Git LF755410bytes/3908lines reconstructs original exactly.
Full6578tests/241modules PASS3385.166s,failures/errors/skips0;all244process exits0.
Sixnativecleanup checks pass,C344-R1implementation receipt bound toC345head.
937sources/8679protectedinputs,all8679finaluncachedrereads,freshverifier complete.
FullID SHA2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Parent6514IDs exactorderedprefix. All630publicrecords/parentbindings verified.
Console omits source_trace_sha256:no reviewer-side fullC345summary/nativeartifact reconstruction.
Native persisted/freshsemantics explicitly attributed;run_execution_valid=true.

InteriorTRAIN meanCE .011673977->.111296027;pairmax .020316586->.192509275;
answers2864->2728/2880. HOLDOUT meanCE .025826478->.288532880;
pairmax .045815971->.499002482;answers1430->1331/1440.
All10interiorseed/split contrasts worse onbothlosses;all7answer-regressing
seed/domain/split contrasts alsohigher bothlosses;0oppositesign atthisgranularity.
344002answers+2eachsplit despitehigherlosses. Original6aggregate answers/losses improve.
Norm>1 1975->5830/12000;cycle2mixedslot4 162->1241/2000.
Not exactclippingcalls,convergence,causaloptimizer/clipping or learnedthenlost proof.
Slot4mixedoriginal4/5/interior;terminaldomainmeansnotwholeexposureweightedobjective.
Original6TRAIN names neverfitted. PreserveC344false/eligible2 andGateFNOTPASSED.

## Original C346 registration and independent review

Source/preregistration HEAD:be76c4c53c36105638e59e059af241078758b628.
Source tree:0f06d4eda13b258141fbb2259eb7843ab28fae8d.
Seven additions only,separate from C345 acceptance. Keep all seven OWN blobs unchanged.
Preregistration:docs/experiment-ledger-addendum-c346-preregistration.md.
Review:docs/c346-post-authoring-review.md.
Original source review result:PASS;its final-handoff coverage gap is recorded above.
Review target HEAD:be76c4c53c36105638e59e059af241078758b628.
An independent nonauthor retrieved and read all7remote OWN files throughEOF;
Git blobs/bytes/SHA256 match both final author runs. No review blockers.
The later documentation-only activation HEAD is the user ExpectedHead.
Do not use sourcebe76c4c,C345executionc81ffe1,publication25ff2f9,acceptancef5fc8e8
or a main merge. The source commit itself is not an activation.

Combined74 tests PASS:normal105.273s;CP932-default-text-open101.910s.
Failures/errors/skips/expectedfailures/unexpectedsuccesses all0.
All7OWN SHA256 hashes stayed unchanged and match the committed source bytes.
Author environment:Linux Python3.12.14/Torch2.10.0+cpu/NumPy2.3.5.
Actual6653raw/6652selected/243modules,OWN48science+26infra;C3456578prefix unchanged.
Full IDsSHA256:39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Parent IDsSHA256:2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Root pyflakes0;333compiledcodeobjects/2327global loads/0unbound.
ActualPowerShell7.5.4AST dispatcher/invoke/run/standardblock all0errors.
Author fixtures include synthetic training and native preflight,but no formalC346cohort.
Full Windows6652-test regression and15-model experiment remain incomplete.

## One question and intervention

Experiment:C346-v5b-pair-max-rate;stage:V5-B-PAIR-MAX-RATE.
Manifest:8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64.
Does halving both constant AdamW rates from initialization improve pair-max
interior answer/query-pair correctness and preserve every registered domain
against both default-rate pair-max and ordinary mean CE?

Freshseeds346001..346005;orderseeds346101..346105.
Arms mean_ce,pair_max,pair_max_half_rate. Defaultnoncore/core rates.005/.0005;
candidate.0025/.00025. The two pair-max arms use exactly the same unscaled
mean24maximum(full256CEqueryA,full256CEqueryB) objective.
Same initial states,paired inputs/targets/events,2400updates,48rows/24pairs perstep,
continuous AdamW,clip1,betas(.9,.999),eps1e-8,decay0. No warmup/decay/restart.
Native mean+last dual reader,14256parameters/core3328,64slots,CPUfloat64,threads2.
All15fits complete before evaluation/replay. No accepted learned-state initialization.

Same mixed45 exposure per logical TRAIN row:original2/3=200each,original4/5=50each,
original6=0,interior4=100;115200rows/3168000nonpaddingtokens per model.
HOLDOUT/masked examples never fitted;original6TRAIN names/prompts never fitted.
The factor.5 is prospectively fixed,not inferred as an optimum fromC345.
No meanCEhalf-rate arm:do not claim objective-by-rate interaction or universal rate benefit.
No convergence,gradient-starvation or clipping mechanism is identified by a PASS.

## Fixed gate and work

Conjunction:all5candidate full original2..6+interior4 gates;all120answer/pair
nonnegative inequalities vsdefaultpairmax and all120vsmeanCE;fourstrict pooled
interior TRAIN/HOLDOUT answer/pair gains vsdefaultpairmax. Report subgates separately.
Thresholds and exact scorers unchanged:.90accuracy,.80pairs,.35evidencedrop,
.35querydrop,.80bothorder. Candidate eligible count includes fullpass and bothcontrol
nonregression. A perfect primarycontrol leaves no headroom but never relaxes the gate.

15fits/15evaluationstates/15optimizers;36000updates/backwards/optimizersteps;
1728000trainingrows;41130model forwards;2220480total rows;164520corecalls;
82260querycalls;30strictstateloads;1checkpointbundleload/1newbundlewrite;network0.
Raw saved logit payload1008599040bytes. Separate native preflight:all5schedules,
1discardedmodel,3zero-stepoptimizer configurations,24forwards/96rows/12backwards/0updates.
Preflight,parentsemantics and regression fixture work are outside scientific WORK.

Save all15states,180normaldomain/split reports,120two-control contrasts,
180terminalobjective summaries and120terminal loss contrasts,all2400preupdate
loss/norm/rate rows perstate. Terminal losses are descriptive,not gate conditions.
A bindingPASS can coexist with higher losses;terminaldomainmeans are not the whole
exposure-weighted trainingobjective. Norm>1 is not an exact clipping-call count.

## Parent, protection and ABI

Immediateparent C345diagnostic:executionc81ffe102c3a9280f28a68e572403549ce77fa1d.
Folder:runs/c345-saved-objective-audit-749db4a6ede44b608c06ee1461b6e393/.
Primarycfc3fe5b8f4ec927d875e2a016a940b5d34aac9ef14d93644eeb26567c0e1f30.
Envelopee883c26d1df24d940cd51b551f06e46e7ac69da216ea6024dc299ee24d2cceab.
C345fold-c345-diagnostic-v1/valid/PASS preserves nestedC344negative/eligible2.
Do not substitute the C344trained schema for this immediateparent.

C345semantic_recheck(out345,out344,data_out,cx,read):5arguments underno_neural.
C346native_preflight(data_out,cx,root,pins,read):5;
run_training(out,data_out,cx,root,pins,read):6,outsideno_neural;
semantic_recheck(out,data_out,cx,read):4,underno_neural.
Canonicaldata via acceptedC332loader/C329artifacts;all deciding direct/lazy
repository dependencies remain source-pinned and protected.

Protect944sources/9177inputs=937+7OWN /8679+491parentoutputs+7OWN.
Parent491=4science+primary+envelope+485proofs(3+241JSON/logpairs).
All9177readleases/finaluncachedrereads;no eviction,unlockedfallback or source substitution.
Sole inherited exclusion,nonewskip or accepted-test edit:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.

## Native execution and stop

Route:invoke_active_v2->invoke_c346->run_c346->c346_execution.
Branch:feat/sft-target-loss. Existing.venv-py31315 remains
Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5. Run prefix:runs/c346-pair-max-rate-<id>/.
Branch/cleantrackedtree/ExpectedHead/uniqueACTIVE/dependencies/AST precede logging;
stale invocation skips without experiment or publication.

C346-R0 explicitly bridges C345helpers to C344-R1timeout cleanup implementation;
receipt keeps its implementation schema but binds the C346executionHEAD.
Sequence:sixnativecleanupchecks->leases/snapshot/C345savedsemantics->native
schedule/pair/optimizer/backwardpreflight->6652isolatedtests/243processes->15fits->
evaluation/replay->savedreconstruction->9177rereads->freshverifier->dedicatedlogpublish.

Sixscienceoutputs:experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json.
Primaryfold-c346-trained-v1;envelopefold-c346-execution-envelope-v1.
Future successor retains497outputs=6science+primary+envelope+489proofs(3+243JSON/logpairs).
Onlyconsolelog/receipt mirror to docs/experiment-run-logs/c346/latest.log/latest.json.

On completion fetch those remote logs;distinguish scientificexecutionHEAD from
publicationcommit. Verify all6652IDs,no skips,243moduleproofs,246process exits,
944sources/9177inputs,all6cleanupchecks,15statework/replay/complete subgates,
finalrereads,freshverifier andrun_execution_valid=true.
Valid FAIL is an accepted negative under the fixed gate. INVALID means sameC346
recoveryonly,no automaticretry or C347registration. Logtransportfailure never
justifies retraining. After valid judgment prepare the nextonequestion in the same
response. Freeze this feature branch while the user runs;preserve native artifacts.

## Inherited regression compatibility seals

Append-only historical provenance,not current ACTIVE state. Retain this section whenever
the handoff is rewritten while the inherited pinned tests remain in the regression.
The accepted C273 preflight recovery and docs/experiment-authoring-runtime-gate.md
(Mutable handoff lifecycle rule) require this specific legacy marker permanently.
C273..C278 also assert it. Do not delete it during later acceptance or activation edits.
C272manifest seal:89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.

## Historical context

docs/handoff-history/c346-pre-recovery-r1.md preserves the exact failed-attempt handoff.
docs/experiment-ledger-addendum-c273-preflight-recovery.md defines the inherited seal contract.
docs/handoff-history/c346-pre-activation.md preserves the C345accepted/C346unregistered state.
docs/handoff-history/c345-pre-acceptance.md preserves previousC345ACTIVE.
docs/experiment-ledger-addendum-c344-c345.md retains C344R1acceptance and attempt01history.
docs/cross-experiment-evidence-synthesis-2026-11-22.md and
docs/cross-experiment-evidence-index-2026-11-22.json
are unchanged C344-bounded snapshots from45c18e39399a6f5ec073257d860377ecb624bd51.
Their C345pending label is historical;the C345acceptance report provides the update.
Main integration must preserve allfeatureblobs,main-onlyfiles and that documentation history.
