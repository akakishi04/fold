# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md Current response format(v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Runtime Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; explicit PowerShell7/ParseFile/active_v2.
Assistant authors/tests/registers; user executes locally. No Codex handoff.
Accepted scientific sources/tests/contracts/logs and dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C338 ACCEPTED VALID NEGATIVE. C339 ACTIVE / NOT YET JUDGED. C340 NOT REGISTERED.**
C337 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY). Earlier verdicts are unchanged.
Do not rerun accepted C338/C337/C336. No production adoption or scientific C339 verdict.
C339 committed-byte post-authoring review is complete: post_authoring_review = PASS.

## Latest accepted evidence -- C338

Acceptance commit:928bc539f83a22584e71e99adac7f5031bd480d0.
Report:docs/experiment-ledger-addendum-c338-c339.md.
Scientific execution:f81a49e383e78ff503a4e4c6fe1156e7a8b75849.
Published log:579edc8f611cfc0a513ce52661582de70f8a8b50; sole parent equals execution.
Metadata/log:docs/experiment-run-logs/c338/latest.json and latest.log.
Publisher244109originalWindowsbytes;SHA256
9fdef99dd0eadce42ef5e3cd3feee8c1442a889a0e811ca80248e7e35ed60684.
Git log blob:6b1d21acf47fb75808e014010be4971e9c3754c0.
6170tests/228modules PASS,0failures/errors/skips,1916.467seconds including process orchestration.
Native locks/preflight,24000updates/10models/27420forwards,saved reconstruction,
all5296final uncached rereads and fresh verifier889sources/5296inputs passed.
Science/verifyexit0;run_execution_valid=true;scientific_statusFAIL,candidatefalse,eligible0/5.
Ordered6170testID SHA:6f9f4fb4184d9ac262bf88eb7ec49e6ee0cd5099754fbb09545461dbc147d89b.

Folder:runs/c338-support-training-5d84afb5a34c4dc0a291ca0f35b24829/.
Primary science/summary.json SHA:
67e369808641a781dd144084a4e1a77d8347a07675740b8c3c694eaedbdf3137.
Envelope:11977e359dbb65236803fb7eaa1d085728a72d27a582dcc2d76d01906e3329e5.
Manifest:d2c6bcbadfa3f04c35cad137fece59c9499f8b5de37589425479b05376b9fe73.

HOLDOUT native->support_loss across5seeds;1440answers/720pairs per domain:
original2/3/4/interior4 each1440->1440correct,720->720pairs,outside0->0.
original5 correct1426->1423,pairs706->705,outside2->7.
original6 correct1389->1375,pairs673->666,outside27->49.
All6domains8575->8558correct/8640,4259->4251pairs/4320,outside29->56,
wrong_observed36->26. Outside_catalog0 in all60 printed HOLDOUT support partitions;
outside errors there are absent0..3digits. Native fullgate1/5(seed338002),candidate0/5.
Original6seedwise answer gains-1,-7,+18,-21,-3; pair gains-1,-7,+14,-14,+1.
Original6rescues38/regressions52;original5rescues11/regressions14. No favorable-seed selection.

Fixed support-loss coefficient1 did not satisfy the hypothesis. This is not proof
that all support objectives fail or a causal explanation of internal behavior.
Fresh seed/order cohort differs fromC335; stronger control scores are not attributed
to this intervention. Objective scale/clipping may differ despite matched updates.
Remote review inspected metadata/lineage/preflight/full regression/all5comparisons/
all10state results/terminal verification. No independent Windows log hash/local proof/
checkpoint/model rerun. Old attached C323/C324 logs are NOT current evidence.

## C339 registration and completed review

Experiment:C339-v5b-saved-support-transfer;stage:V5-B-SAVED-SUPPORT-TRANSFER.
Contract:docs/experiment-ledger-addendum-c339-preregistration.md.
Review:docs/c339-post-authoring-review.md.
Source/preregistration review target:e9a806236bcb6376ca9eb7632c8c24fb7344111e.
post_authoring_review = PASS.
Use the subsequent documentation-only activation HEAD in the user command, not the
source-only target, acceptance commit or a published log HEAD.

All6committed files reread through EOF; returned Git blobs match local tested bytes.
Post-reread32/32normal PASS13.227s and32/32CP932-default-open emulation PASS14.075s,
0failures/errors/skips. UTF8/noNUL/compile/import PASS;208recursive code objects checked,
undefined globals0. Actual32testID SHA:
4e617dae39b4d8a61731f8e96cf5fb06a246d33c15448e5e733e39d08fd05e36.
Removed supportNLL mutation detected bytest04/test05(2expected assertion failures);
reversed-transition mutation detected bytest09(1expected assertion failure). Restored
functions pass those tests;all6file bytes unchanged. No committed-source correction needed.

Author LinuxPython3.13.5/Torch2.10.0+cpu/NumPy2.3.5,targeted tree,NOT full checkout.
Local-only verbatim C267dataset/C337audit+aggregate extracts never committed. Synthetic
logits/parent scorers/summaries/proof inventories/OS leases explicitly labelled. Actual
child analyze/loader/writer/reconstruction/snapshot/worker/fresh-verifier paths exercised,
not actual C338logits/checkpoints or6202native historical tests. pwsh unavailable;
native PowerShell AST not run here. Mandatory user/dispatcher/launcher/runner AST retained.

## One scientific question and fixed scope

Where does support_loss improve or degrade supplied-value support versus within-pair
binding across TRAIN/HOLDOUT and name domains? All10saved C338states,seeds338001..338005,
native/support_loss;original2..6/interior4,both splits/languages,all3profiles/domain.
No new fitting,model inference,optimizer,seed selection,decoder,candidate filter or answer repair.
Original1 not included in new diagnosis;mandatory parent semantics still validates all114raw views.
Canonical192TRAIN/96HOLDOUT0..3values,all12ordered pairs,rows/prompts/splits unchanged.
DATA_SHA:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Accepted C337audit_logits retains raw256argmax,correct/wrong_observed/absent_digit/
outside_catalog,exact ties,target-other and maxsupplied-maxoutside254 margins.
New supportNLL=logaddexp(0,LSEoutside254-LSEsupplied2),withinNLL=logaddexp(0,other-target).
Mathematical sum is ordinary target CE; retrospective label-assisted measurements,
not corrected accuracy. No epsilon/clipping/floor; finite inputs/gaps/components/differences.
Uses exact softplus identity rather than functional softplus default threshold approximation.
Paired same row_id/target/other;4x4kind transitions,two3x3sign transitions,rescue/regression,
mean candidate-minus-native NLL/margin deltas. Positive NLL delta=worse;positive margin
delta is descriptive only. Means use math.fsum. Do not infer internal causality.

Reconcile all60parent HOLDOUT support partitions and all30full paired contrasts,
including correct/pairs/rescues/regressions/gains/outside_gain. Production query pairs
group by language/entities/values/permutation and query identity. All720strata/360paired
strata,row/column/sign marginals and rescue accounting checked. Preserve C338false/eligible0.
PASS is integrity only;benefit/tie/harm retained. No Gate F pass or production adoption.

## Workload and complete evidence protection

Work10saved states,51840normal answers,25920paired answers,720strata,360paired strata,
30parent contrasts,60parent partitions. Scientific forward/train/backward/optimizer/
model state load/new checkpoint/network0. Tensor/checkpoint archive reads are evidence
work,not neural forward;software tests and parent checks separately scoped.
Manifest SHA:3f3380eac1a0e5d0c076825081c10edfa86bed75e02b2c1b5ee23ebf21dc42f1.

Parent C338 exact primary/envelope,trained schema FAIL but execution-valid/capability-applicable,
candidatefalse/eligible0,889sources/5296inputs,6170receipt,all5296rereads mandatory.
Parent executor3cc1dd228baab13a1feef96d38b8213ff53d7080 and benchmark
53185474d560e2961ff05b5484da84c8f27c956f pinned before import;dictionary helper bridge.
C338snapshot reconstructs inherited maps;add ALL467outputs=6science+summary+envelope+
459regression proofs(3+228JSON/logpairs),then6own.895sources/5769inputs.
Native R4 leases,EXACT finite max_files=INPUT_COUNT=5769;no4096default/eviction/unlocked fallback.
All5769final uncached rereads;no earlier proof omission or accepted-source/test changes.

Immediate parent loader is FOUR-argument C338.semantic_recheck(C338science,C329data,cx,read),
under no_neural. Checks weights/traces/all raw views/negative without fitting or forward.
Not old6argument C337diagnostic dispatch. Canonical data/prompt validators unchanged.
No recursive older semantic-body reruns;all older bytes and direct/lazy dependencies protected.

## Full regression, route, output and stops

6202tests/229modules=6170unchanged ordered IDs+32own;6203before sole inherited exactC204
mutable-ACTIVE exclusion. No new skip/exclusion/cached success/automatic retry. Sequential
fresh ordinary module processes with accepted C330R1.2direct/immediate-child PID proofs,
canonical begin/end markers and all test IDs. Child C339guard/CLI/plan owns new HEAD binding.
Generic module ABI fold-c330-r1-module-v2;new plan fold-c339-regression-plan-v1,
aggregate fold-c339-regression-v1. All6202tests pass before new diagnosis.

active_v2->invoke_c339->run_c339->c339_execution->native parent locks/maps/proofs
->C338semantic reconstruction->full_regression_fresh_process_per_module
->saved_support_transfer->saved_diagnostic_reconstruction->final_uncached_input_recheck
->primary/envelope->independent fresh verifier->console publication.
Role C339-SAVED-SUPPORT-TRANSFER. Print720C339stratum/360C339transition records.
No scientific training-step progress. preserved_parent_gate candidatefalse/eligible0
is NORMAL. Complete only with persisted_support_transferPASS,execution_envelope_verified,
run_execution_valid=true and successful publication,not just module OK.

Four outputs:audit-plan.json,answer-components.json,paired-transitions.json,
validation-summary.json. All byte/size-bound around reconstruction and before final records.
Primary fold-c339-diagnostic-v1;envelope fold-c339-execution-envelope-v1 retain895/5769maps.
Local runs/c339-support-transfer-<id>/science plus229module JSON/logpairs/regression records.
Console ONLY published c339/latest.*. Successor must inherit461moduleproofs+6otherfiles=467outputs.

Stale/dirty/branch/ambiguousACTIVE/dependency/AST skips before logging. Do not replace
ExpectedHead with publicationHEAD to bypass RESULT_ALREADY_PUBLISHED. Technical source/
input/test/PID/nonfinite/replay/row/contrast/semantic mismatch is INVALID SAMEC339,noC340.
Unfavorable valid diagnosis is not retry. Publication-only repair concerns publication only.
No CI,paid service,reinstall,artifact deletion,old-model training. User may report only finished;
fetch LIVE c339metadata/log and separate execution from publication. Accepted result requires
next-C implementation/preregistration/review/activation/command in the same response.
Do not delegate to Codex or move the experiment branch for unrelated work during a registered run.

## History and inherited compatibility seal

Preacceptance docs/handoff-history/c338-pre-acceptance.md. All older archives remain.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
