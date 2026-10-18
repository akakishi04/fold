# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md Current response format(v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Standard explicit PowerShell7,dispatcher ParseFile,tools/invoke_active_v2.ps1.
All accepted source/tests/contracts/logs,including C330-R1.2,remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C330 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C331 ACTIVE / NOT YET JUDGED. C332 NOT REGISTERED.**
C329 remains ACCEPTED VALID NEGATIVE. C330 attempts01/02/03 remain INVALID EXECUTION.
Do not rerun accepted C330/C329 or earlier experiments. No production adoption.
C331 authoring review PASS is not scientific or native full-regression PASS.

## Latest accepted evidence -- C330 R1.2

Acceptance commit:b195a3962dd868ffa430500ca3bf6ae87dc44b1d.
Report:docs/experiment-ledger-addendum-c330-c331.md.
Execution:a92b0096949c4176f793dc2b57e910149222efb0.
Publication:50e931bc13b9af8a6b25acae104a12f27d4eeaff;sole parent equals execution.
Metadata/log:docs/experiment-run-logs/c330/latest.json and latest.log.
Publisher289867Windows bytes;SHA256
ee852498382aad79a3892082a3b11a0368dc519debd5fef97279e16fa204a7ff.
Logblob:b577bf4d2bf9a626f44d7f45d897690fc63162cc.
Full5850tests/220modules PASS,failures/errors/skips0,1189.327seconds including process
orchestration. OrderedID SHA:
f7c7f355197393a53f0d9d8f3f4c8a044e4b365719a4894090017e206e709dc6.
Native parent/locks,841sources/1596inputs,all module receipts/PID checks,saved diagnosis,
all1596final uncached rereads and fresh verifier passed;all exits0;run_execution_valid=true.
The original C311 access violation was not reproduced in this isolated run;its
internal cause is NOT established or declared fixed. Prior invalid attempts retained.

Remote review covered exact-ref deciding execution records,seed flags,residual
strata/criterion transitions and terminal verification. No independent whole-Windows-
log rehash,all220local receipt reads,raw-logit recomputation or model rerun claimed.
Old attached C323/C324 files are not current evidence. Publication alone is not PASS.

C330 diagnosed4320local/2160order cells across all10checkpoints;new model forwards0.
For extended2400 only,each domain has360local/180order cells:
original2/3/4 each0failed local/0failed order;
original5:5local/2order;original6:32local/12order;interior4:9local/3order.
Total46/2160failed local and17/1080failed order;ALL local failures include normal
accuracy/query-pair errors;mask-only0. Do not add overlapping criteria as independent
samples. Original5 failures all shared_suffix English(2TRAIN/3HOLDOUT). Original6
31/32failures shared_suffix across languages/splits;one shared_prefix EnglishHOLDOUT.
Interior9failures all v_dominant and seed329002(4EnglishTRAIN,4EnglishHOLDOUT,1JapaneseHOLDOUT).
Scorer slot shared_suffix2 is opaque and is not the literal v_dominant template.
Original6 normal failures71->32(43rescued,4regressed,28persistent);order29->12.
Original5 normal25->5(21rescued,1regressed);interior97->9(88rescued,0regressed),order48->3.
C329 full interior0/5->4/5;original2..6 retention1/5->1/5;joint paired1/5negative remain.
Localization is not proof that the readout or any one mechanism caused the errors.

## C331 registration and completed committed-byte review

Experiment:C331-v5b-frozen-first-mean-query;stage:V5-B-FROZEN-FIRST-MEAN-QUERY.
Contract:docs/experiment-ledger-addendum-c331-preregistration.md.
Review:docs/c331-post-authoring-review.md.
Source/preregistration review target:5dbdd46959695f2ca48adbeea8084db5ba6a8dab.
post_authoring_review = PASS.
Use the subsequent documentation-only final activation HEAD in the user command,
not the source review target,acceptance commit or old C330 publication/execution.

All6committed files reread completely;Git blobs match independently hashed tested
local bytes. Post-reread48/48normal PASS1.868s and48/48CP932-default-text-open emulation
PASS1.537s,0failures/errors/skips. UTF8/noNUL/compile/import PASS;197code objects in
recursive undefined-global audit,0undefined. A no-op intervention mutant is detected
by both exact-formula and changed-behavior tests(2expected assertion failures).
Reviewed source files remain unchanged. AuthorLinuxPython3.13.5/Torch2.10.0+cpu/
NumPy2.3.5,2threads,targeted source tree,not full repository checkout. Toy model,
legacy scorer/checkpoint/lease callbacks and historical inventories are explicitly
synthetic. Real own Torch/file/Git/subprocess tests do NOT establish nativeWindows,
actual C329 model inference or full5898historical success. Native PowerShell AST
not run on authorhost;mandatory unchanged user-side AST chain remains.

## C331 one question, intervention and fixed scope

At frozen C329 states,does adding first-query-byte local information to the mean
query change long shared-suffix binding while retaining other tasks?
Use all10C329checkpoint states,seeds329001..329005,sourcearms prefix1200/extended2400.
No successful-seed selection,training,optimizer update,coefficient search or new
checkpoint. Preserve original1..6/interior4,allTRAIN/HOLDOUT profiles/languages/views.

Modes:native_before,first_mean,native_after,each on every checkpoint in that order.
Native first read.query input is span_mean;candidate replaces it by
.5*(span_mean+first_query_byte_local_state). Native second last-byte query remains.
This is a representation blend BEFORE query projection/attention,not three attention
outputs or a new attention head. Same14256parameters/core3328,64slots,weights,parser,
two query calls,core/attention/memory/residual path. No accepted function/global patch;
child-owned temporary hooks validate input provenance and restore on every exit.
UTF8 BYTE endpoint,not decoded first character. Japanese limitation explicit.
C317 replaced last by first at older states;C331 retains last and changes mean.

Every mode is eval/no_grad and must preserve loaded state hash. Nativebefore matches
accepted C329 logits<=1e-9/exactargmax;nativeafter matches before. All38query-blind raw
view tensors and allEnglish original1views match between native and candidate by
the same strict control. Japanese original1 is not a one-byte invariant. Dataset/
prompt memory fingerprint and protected bytes stay unchanged.

Use unchanged original/interior scorers,paired contrasts and C330 failure localization.
Retain alllocal/masked/order thresholds.90/.80/.35/.35/.80 and native gate reproduction.
Original1 remains descriptive with its raw controls saved. Save/print all10effect
records including harms,rescues/regressions,per-length correct answers/pairs and
failed local/order counts. Do not confuse overlapping criteria with independent cases.
PASS means integrity only,not improvement;benefit,tie,harm are all valid diagnostic
results. capability_gate_applicable=false;no GateF/production/trained-capacity claim.

Work:10models/10state loads/1bundle load,30evaluations*171forwards=5130model forwards,
492480rows,20520core forwards,10260query projection calls,20scored state/policy records.
Scientifictrain/gradient/optimizer steps/new checkpoint writes0. Raw-logit payload
1008599040bytes is not total serialized size or peak RAM. Separate discarded native
preflight12forwards/12rows/0updates uses nonzero output weights and Englishoriginal1/6
normal/query-blind cases. Tests/parent verification/saved reconstruction are separate.
Scientific manifestSHA:
8644f03a61e1dbdbb44a31514a392fd18cdb7ce71c190ee1a1fd2a8c759c30f8.

## Complete parent evidence and protection

C330folder:runs/c330-localization-688c9a321f204989b6a694820eaab9bd/.
Primaryscience/summary.jsonSHA:
f7c1a6567f2ab9929528722bfc699b8228275e8cb185c31f1de87e5260278691.
Mandatoryexecution-envelope.jsonSHA:
ad30fc8f64775ebe93f9c2650bc74dc809583c877397a94889745b3e388381ad.
Require exact diagnostic schemas/flags,PASS,execution_revisionC330-R1.2 and whole
recovery contract object withSHA
cb09791f16e446ad2e1116981700c5be26997865d2da2eef89e76acdad1df8b9.
Both parent maps identical841/1596;full5850receipt/1596final rereads/semantics checked.
The C330 pureJSON diagnostic is reconstructed from protected C329 measurements via
its unchangedsemantic_recheck. No recursive older semantic-body reruns or model calls.

Parent443supplementary outputs are mandatory:3regression records and220JSON/logpairs.
Reconstruct parent5850IDs,all test success/PID/log evidence with unchanged R1.2helpers.
These443plus4diagnostic outputs+primary+envelope make449parent files. ProtectALL:
847sources=841inherited+6own;2051inputs=1596inherited+449parentfiles+6own.
The accepted R1.2executor/32tests/contract and allC330/C329/readout/scorer/recovery
dependencies remain pinned. Never fall back to smaller protection maps. C329states/
data used for inference already lie in the inherited protected map.
NativeunchangedR4leases,independent initial hashes,all2051final uncached rereads required.
No unlocked fallback,accepted-source mutation,artifact deletion or environment reinstall.

## Regression, execution route, output and stops

Full5898tests/221modules=5850unchanged IDs+48own;5899before sole inherited exactC204
mutable-ACTIVE exclusion. Preserve base-ID digestf7c7f355197393a53f0d9d8f3f4c8a044e4b365719a4894090017e206e709dc6.
Fresh sequential process per module,once only. C331moduleCLI uses C331guards and
unchangedR1.2allowed_module/execute_module/check_module/validate_module_evidence.
GenericmoduleABI fold-c330-r1-module-v2 is bound to NEW C331HEAD/plan/index/module;
C331plans/evidence usefold-c331-regression-plan-v1/fold-c331-regression-v1.
Do not invoke C330-hardcoded guard/module CLI as the C331worker. Direct/immediate-child
PID/log semantics remain;no equal-PID assumption. Newfull5898success precedes probe.
Parent proof verification is not rerunning accepted parent test methods.

active_v2 ->invoke_c331 ->run_c331 ->c331_execution controller/worker ->lockedparent
snapshot+443test proofs ->native_readout_preflight ->full_regression_fresh_process_per_module
->frozen_first_mean_probe ->saved_probe_reconstruction ->final_uncached_input_recheck
->primary/envelope ->fresh byte/test/JSON/tensor reconstruction ->console publication.
No training-step progress. Ten'[C331] seed=... arm=... three_modes=COMPLETE weights=UNCHANGED'
messages,then all10C331effect records. Heartbeats10seconds. Complete only when
persisted_query_probe=PASS,execution_envelope_verified andrun_execution_valid=true.

Four science outputs:diagnostic-plan.json,evaluations.pt,measurements.json,
validation-summary.json. Archivefold-c331-query-probe-v1 contains all10states/3modes.
Primaryfold-c331-diagnostic-v1;envelopefold-c331-execution-envelope-v1 carryfull847/2051maps.
Hash/size-bind outputs around saved reconstruction and before result/envelope writing.
Fresh process rechecks all parent/input/source/output bytes,new221module proofs and
saved scientific metrics without a second model cohort or historicaloptimizer replay.
Localruns/c331-query-probe-<id>/science plus regression-plan/evidence/result.json,
221moduleJSON/logpairs,execution-envelope andworkerlogs. ConsoleONLYpublishedc331/latest.*.
A successor must also preserve/bind these445new regression evidence outputs when
inheriting C331,not only the four scientific outputs and summaries.

Stalehost/branch/HEAD/dirtytree/ambiguousACTIVE/dependency/AST checks SKIP before
science/publication. RESULT_ALREADY_PUBLISHED means inspect prior output;never replace
oldExpectedHead by a publicationHEAD to bypass it. Any technical input/test/PID/native/
control/nonfinite/weight/replay/schema/semantic failure repairs SAME C331,no C332.
A harmful but integral probe result is valid scientific evidence,not permission to
retry. Publication-only failure repairs publication alone. NoCI,paidservice,reinstall,
artifact deletion or accepted-model retraining. All3C330failedattempt archives retained.

User may report only finished. Fetch live latestmetadata/log;separate executionHEAD
frompublication;never use oldC323/C324attachments. ValidC331 requires acceptance AND
next-C implementation/preregistration/remote-byte review/activation/command in the
same response. INVALIDstayssameC331. Do not move this branch for unrelated work while
user runs the registered experiment.

## History and inherited compatibility seal

C330preacceptancehandoff:docs/handoff-history/c330-pre-acceptance.md.
All prior invalidattempts/reviews/history retained. Acceptance and C331registration separate.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
