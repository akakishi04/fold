# FOLD experiment ledger and handoff

Updated: 2026-11-22 Japan time.
Conversation protocol:docs/experiment-conversation-handoff-protocol.md,Current response format v2.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C344 ACCEPTED VALID NEGATIVE.** Execution revision C344-R1 completed validly.
candidate_gate=false / eligible_seed_count=2. Attempt01 remains INVALID EXECUTION.
C343 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C342 remains ACCEPTED VALID NEGATIVE.
**C345 ACTIVE / NOT YET JUDGED.** Saved-objective/trajectory diagnostic only.
No production adoption. Do not rerun accepted C344. Do not prepare C346 before C345 judgment.

## Latest accepted evidence

Report:docs/experiment-ledger-addendum-c344-c345.md.
Acceptance:a7174ae51f71f001901793603ab9f7ddb26ed923.
Scientific execution:8d1e1170cd614503deab1e09474fe82de4bba561.
Publication:9d163289775373aaf62028a7b8aeacbfb41593a6,sole parent execution,only latest.log/json.
Windows log355860bytes/SHA256aba71fc3bba513a3dab51a34b46b06641b1b0f5c2fa713c201c3491643867b49.
Git LF352156bytes/3704LF reconstructs that original exactly.
Full6514tests/239modules PASS in3208.100s,zero failures/errors/skips.
All242 module/regression/science/verifier exits0;six native timeout cleanup checks PASS.
930sourcepins/8183protectedinputs;all8183final uncached rereads and fresh verifier complete.
run_execution_valid=true. All10fits finish before evaluation/replay;science24000updates/
27420model forwards/1480320rows. Saved states,exactargmax replay and arithmetic verified.
Complete10seed/120normal/5paired/60contrast records pass the immutable summary validator.

Full-gate count2/5 in both arms,but different passing seeds:control344004/344005;
candidate344001/344005. Seven of60contrasts regress on both endpoints,14/120inequalities.
Interior TRAIN answers2864->2728/2880;pairs1424->1293/1440.
Interior HOLDOUT answers1430->1331/1440;pairs712->640/720.
Strict gainsTRAIN(-136,-131),HOLDOUT(-99,-72):all negative.
Interior TRAIN rescues16/regressions152;HOLDOUT rescues10/regressions109.
All candidate interior errors are new relative to the paired control.
Original6 improves overall(TRAIN2875->2877,HOLDOUT1431->1438),but344004regresses.
Original2/3/4 perfect botharms;original5candidate has one new TRAIN error.
No optimizer,clipping,pooling or capacity cause is proven.

## C345 registration and independent review

Source/preregistration HEAD:588586870562a8f930b7e2053dcf669ee8d0b650.
Source tree:2587c2ff0086f84257ca52ddf6393b123a42d5ed.
Seven additions only,separate from C344 acceptance. Keep all seven OWN blobs unchanged.
Preregistration:docs/experiment-ledger-addendum-c345-preregistration.md.
Review:docs/c345-post-authoring-review.md.
post_authoring_review = PASS
Review target HEAD:588586870562a8f930b7e2053dcf669ee8d0b650.
An independent nonauthor fetched all7remote OWN files at that exactcommit throughEOF.
Blobs/SHA256/bytecounts match the frozen tested files. No review blockers.
Use the later documentation-only activation commit as ExpectedHead;do not use
source5885868,C344execution8d1e117,publication9d16328,acceptancea7174ae or a mainmerge.

Combined64 tests PASS:normal111.006s;CP932-default-text-open112.490s.
Failures/errors/skips/expectedfailures/unexpectedsuccesses all0.
Author environment:Linux Python3.12.14/Torch2.10.0+cpu/NumPy2.3.5.
Actual6579raw/6578selected/241modules,own40science+24infra;C3446514prefix unchanged.
Full IDsSHA256:2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Parent IDsSHA256:c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3.
Pyflakes0;267function/nestedcodeobjects/1764global loads/0unbound.
ActualPowerShell7.5.4AST dispatcher/invoke/run/standard block all0errors.
Native Windows formal C345 execution is pending;author64 tests are not the full run.

## One question and interpretation boundary

Experiment:C345-v5b-saved-objective-audit;stage:V5-B-SAVED-OBJECTIVE-AUDIT.
Manifest:5e69553fd6661ef46459883500fd719b474fd7cacbd17d002c957eb3fb2f1a9f.
Does C344 pair-max's worse binding accompany higher matched terminal pair-max loss,
or lower surrogate loss despite worse answers? Use existing seed344001..344005,
mean_ce/pair_max states and all6domains/bothsplits. No new training or model calls.

Compute full256 per-answerCE and canonical-pair meanCE/maxCE from saved normal
logits;bind all parent normal answer/pair counts and60contrasts. No label/inference
repair or selected subgroup. Terminal means are per-domain/split,not the overall
exposure-weighted training objective. Original6 TRAIN names were not fitted.

Read all24000 preupdate loss/norm rows and reconstruct actual schedules/composition.
Use all12fixed200stepblocks/state and2cycles*3slots*3profiles/state. Slot4 is mixed
original4/original5/interior4,not a pure-family loss. Norm>1 is threshold exceedance,
not exact clipping calls. Preupdate minibatch traces cannot show learned-then-lost
full-set answers or establish convergence/causal clipping/gradient starvation.
Diagnostic PASS preserves C344false/eligible2 and is not capability improvement.

## Parent artifacts and production call contracts

Folder:runs/c344-pair-max-training-76ae8eb6e3bf4d08ac577c5fde9e0caa/.
Primary610398ced893ff1d1885faf9bd02ffef57779ca2bd96bfa995b6929e6d8f20d7.
Envelopec77f0fcf5fcbbf59d3961894713dbf8dcb30ae89841df0325b980a07d8913562.
Accepted executorblob76c8663caafc97ece440df71e250e546198d425b;
benchmarkblob6261a0c267df027835093c7ce53958f8f0034186.
Parent is fold-c344-trained-v1/valid/scientificFAIL,candidatefalse/eligible2,withR1receipt.
Immediate semantic_recheck(out344,data_out,cx,read) takes4arguments underno_neural.
Child run_diagnostic/recheck(out,parent_out,data_out,cx,read) takes5arguments.
Canonical data via C332.load_data and inherited C330 parent-folder/C329 artifacts.
Never substitute C343-only schema/semantics or rerun ancestor neural computation.

Protect937sources/8679inputs=inherited8183+ALL489C344outputs+7OWN.
Parent489=sixscience+primary+envelope+481proofs;proof481=three records+239JSON/logpairs.
Native lease capacity8679;all8679finaluncachedrereads;no missingdirect/lazy dependency.
No acceptedfileedit,newexclusion,skip,eviction or unlockedfallback.
Sole inherited excluded ID:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.

## Execution and evidence budget

Route:invoke_active_v2->invoke_c345->run_c345->c345_execution.
Branch:feat/sft-target-loss. Existing .venv-py31315 remains
Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5,CPUfloat64,threads2.
Run prefix:runs/c345-saved-objective-audit-<id>/.
Branch/cleantrackedtree/ExpectedHead/uniqueACTIVE/dependencies/AST beforelogging;
stale invocation skips without experiment or logpublication.

C345execution_revision=C345-R0;timeout_cleanup_implementation=C344-R1.
The pinned parent's six-case preflight/2module barrier are reused unchanged.
Receipt keeps the accepted implementation schema and binds child executionHEAD;
the parent's original receipt separately binds its C344executionHEAD.
Sequence:sixnativechecks->leases/snapshot->C344savedsemantics->6578isolatedtests/
241processes->saveddiagnostic->savedreconstruction->8679rereads->freshverifier->logpublish.

Perchild computation/reconstruction pass:10checkpoint records,51840normalanswers,
25920querypairs,120terminal summaries,60contrasts,24000trace rows,12000pairedsteps,
120blocks,180groups,60pairedblocks,90pairedgroups. Evaluationarchive/tracefile1loadeach.
Scientificforward/backward/update/model-state-load/checkpoint-write/network all0.
Parentsemanticpasses and regressionfixture work are separate from these per-passcounts.

Four science outputs:audit-plan.json,terminal-objectives.json,training-trajectory.json,
validation-summary.json. Primaryfold-c345-diagnostic-v1;envelopefold-c345-execution-envelope-v1.
Future successor retains491outputs=4science+primary+envelope+3records+241JSON/logpairs.
Console emits all120terminal/60contrast/120block/180group/60pairedblock/90pairedgroup rows.

## Next response and stop

On completion fetch remote docs/experiment-run-logs/c345/latest.json and latest.log.
Distinguish scientific executionHEAD from publicationcommit. Check C345-R0/R1receipt,
all6578IDs/no skips/241matchingmoduleproofs,allprocessexits,937sources/8679inputs,
parentresultpreservation,complete diagnosticcount/reconstruction,allfinalrereads,
freshverifier andrun_execution_valid=true. No desiredloss-sign gate.
If valid,accept diagnosticintegrity and prepare the nextonequestion in thesameresponse.
If INVALID,repair/retry sameC345only. Logtransportfailure does not justify rerunningC344.
Freeze this branch while the user runs. Preserve all native artifacts and acceptedsourcebytes.

## History and compatibility

C345preactivation:docs/handoff-history/c345-pre-activation.md.
C344preacceptance:docs/handoff-history/c344-pre-acceptance.md.
C344attempt01:docs/experiment-run-logs/c344/attempt-01/latest.log and latest.json.
C344R1contract/review:docs/c344-recovery-r1.md,docs/c344-r1-post-authoring-review.md.
C343report:docs/experiment-ledger-addendum-c343-c344.md.
C272manifest seal:89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
