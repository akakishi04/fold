# C331 preregistration -- frozen first/mean-query blend

Date:2026-10-18 Japan time. Acceptance base:b195a3962dd868ffa430500ca3bf6ae87dc44b1d.
Experiment:C331-v5b-frozen-first-mean-query;stage:V5-B-FROZEN-FIRST-MEAN-QUERY.
C330 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY),R1.2. C329 remains VALID NEGATIVE.
Gate F NOT PASSED;C332 NOT REGISTERED. No execution command before committed-byte
post-authoring review PASS and a separate authoritative ACTIVE registration.

## One question and the exact intervention

At the fixed C329 checkpoints,does supplying first-query-byte local information to
the mean-query branch change long shared-suffix binding while retaining other tasks?
C330 found46 residual local failures:original5=5,original6=32,interior4=9. None was
mask-only. All original5 failures and31/32original6 failures used shared_suffix names.
That motivates a readout probe;it does NOT prove the readout caused the errors.

The native C304/C278 path makes two calls to the same read.query projection,from
(1) mean of local states over the query span and(2) local state at its last byte.
Native attention results are combined by the existing forward. C331 changes ONLY
the first call's input to .5*(span_mean+first_query_byte_local_state). The second
last-byte input,query projection weights,memory,attention operations and output
averaging/residual path are unchanged. This is averaging REPRESENTATIONS BEFORE the
learned query projection/attention,not averaging three attention outputs. Two query
calls remain;no new parameters or a third attention call. Fixed coefficient.5,no search.

The endpoint is a UTF8 BYTE,not the end of the first Unicode character. For Japanese
names this distinction is important and is retained,not silently decoded into a
character-aware policy. No labels,entity IDs,profile-specific branch,correct output,
HOLDOUT choice or successful-checkpoint selection enters the intervention.
C317 previously REPLACED the last branch with the first at older checkpoints. This
probe instead keeps the last branch and changes the mean branch,at C329 states.
A favorable result would not establish that training can exploit this policy.

## Frozen cohort and controls

All10C329 saved states:seeds329001..329005,source arms prefix1200/extended2400.
Do not select only extended states or the one full-success seed. C329's accepted
five-trajectory/ten-state checkpoint schema is loaded unchanged and fingerprinted.
For each state run all registered original1..6/interior4 evaluations in this order:
native_before,first_mean,native_after. No intervening weight update or model selection.
Load each saved state once;check its full weight fingerprint after every mode.
Every mode uses the actual native model and the same dataset,prompt bytes and targets.
Hooks validate native query-input provenance and are removed even on exception.
No accepted module/global/function is patched;only child-owned transient hooks.

Native_before must reproduce the accepted C329 raw logits within1e-9 with exact
argmax. Native_after must match native_before by the same checks. All38query-blind
raw-view tensors must remain unchanged by first_mean within1e-9/exact argmax. The
English original1 views must likewise remain unchanged:their query span has one
byte. Japanese original1 is not described as a one-byte invariant. No tolerance or
control condition may be weakened after inspecting results.

Score native_before and first_mean using unchanged C324/C304/C321/C270 scorers.
Retain local/masked/order gates.90/.80/.35/.35/.80,all TRAIN/HOLDOUT languages/profiles,
normal answer and both-query-correct counts,and per-length rescued/regressed counts.
Use the accepted C330 localizer to count failed local/order criteria without
changing its categories. Reconstruct native per-state gates against accepted C330.
Do not sum overlapping local/order failures into independent examples. Original1
remains descriptive;full raw data are saved for its controls.

## Fixed workload and meaning of PASS

10frozen model instances,10saved-state loads,1checkpoint-bundle load.
30full evaluations:171model forwards/16416row presentations/684core forwards each.
Total5130model forwards,492480rows,20520core forwards,10260query projection calls.
20scored state/policy records. New training/gradient/optimizer steps and checkpoints0.
Raw saved-logit payload1008599040bytes;this is not serialized total size or peak RAM.
Three-mode outputs are intentionally saved,not just a success receipt for after-mode.
Native preflight is separately scoped:one discarded model,nonzero output weights,
12forwards/12rows/0updates over English original1/6 normal/query-blind examples.
It checks the control against native forward and invariant candidate views,and
executes the candidate even on the non-single-byte input. No probe initializes a
scientific state. Unit-test gradient checks are software work,not scientific fitting.

PASS means all inventories,original-logit replay,weight preservation,controls and
saved reconstruction are valid. Improvement,tie or harm are all valid diagnostic
outcomes. There is no capability-gate threshold tuned to make the probe pass.
capability_gate_applicable=false,gate_f_candidate=false,production_adoption=false.
This is an untrained inference intervention,not evidence of trained performance,
arbitrary-length reasoning,a capacity limit,causal explanation or Gate F passage.
No better wall-clock or memory claim follows from unchanged parameter/query counts.

## Immediate parent and supplementary evidence

Accepted C330 execution:a92b0096949c4176f793dc2b57e910149222efb0.
Publication:50e931bc13b9af8a6b25acae104a12f27d4eeaff.
Folder:runs/c330-localization-688c9a321f204989b6a694820eaab9bd/.
PrimarySHA:f7c1a6567f2ab9929528722bfc699b8228275e8cb185c31f1de87e5260278691.
EnvelopeSHA:ad30fc8f64775ebe93f9c2650bc74dc809583c877397a94889745b3e388381ad.
Require fold-c330-diagnostic-v1/fold-c330-execution-envelope-v1,PASS,diagnostic valid,
capability not applicable,and EXACT execution_revision C330-R1.2 with recovery hash:
cb09791f16e446ad2e1116981700c5be26997865d2da2eef89e76acdad1df8b9.
Validate the whole recovery contract object,not just its revision string.
Both result/envelope must carry the same841-source/1596-input maps. Validate full5850
receipt,complete1596final rereads and parent saved-semantic completion. Reconstruct
C330 JSON diagnosis from its protected C329 source measurements with the unchanged
C330.semantic_recheck. No recursive older semantic bodies or parent model forwards.

The accepted C330 envelope also binds443supplementary regression outputs:
regression-plan-r1.json,regression-isolation-r1.json,regression-result.json and220
module JSON/log pairs. Validate their hashes,exact selected5850IDs,all started/success
IDs,module exit0,PID topology and log markers with unchanged accepted R1.2 helpers.
These files are mandatory protected inputs,not optional transport data. Their
inventory plus4diagnostic outputs,primary and envelope is449parent output files.

Protection:847sources=841inherited+6own;2051inputs=1596inherited+449parentfiles+6own.
All deciding direct/lazy dependencies remain pinned,including accepted R1.2 executor/
32tests/contract and original C330/C329/C324/readout/scorer modules. Never revert to
838/1593or841/1596 merely to simplify the next adapter. The C329 tensors/data used by
the probe must already be in the inherited protected map and are rechecked as bytes.
No accepted C330 or older file is rewritten. Native R4 read leases,independent first
hashes and ALL2051final uncached rereads remain mandatory. No unlocked fallback.

## Full regression with the accepted process relationship

Original5850ordered test-ID SHA:
f7c7f355197393a53f0d9d8f3f4c8a044e4b365719a4894090017e206e709dc6.
Append48own tests:5898selected/221modules,5899before the sole inherited exact C204
mutable-ACTIVE exclusion. No new skips/exclusions,cached success or automatic retry.
Keep ordered fresh sequential processes per module;preserve the tests_tools registry.
The new C331 plan binds all5898IDs,HEAD and scientific manifest. A module child uses
C331 guards and delegates ordinary unittest execution and evidence checking to the
accepted R1.2 helper. The inherited generic module ABI fold-c330-r1-module-v2 is
reused but is bound to the NEW C331 HEAD/plan/index/module. This is not another C330
experiment or a claim that the parent run was reexecuted. C331 aggregate schemas:
fold-c331-regression-plan-v1/fold-c331-regression-v1. Parent5850plan is independently
reconstructed and verified before new regression.

Retain launchPID,workerPID,parentPID. Allow only direct or immediate-child relation;
require complete canonical begin/end markers and every successful test ID. Fresh
verification reuses the same validator. No equality-only PID regression. All5898tests
must pass before the frozen probe. Module-level OK is not full regression success.

## Files, flow and authoring boundary

New own files:benchmark,executor,48-test module,run_c331,invoke_c331,this contract.
Four science outputs:diagnostic-plan.json,evaluations.pt,measurements.json,
validation-summary.json. The evaluation archive schema fold-c331-query-probe-v1
has ordered10records,each bound to source state hash and all3raw modes/receipts.
Primary/envelope:fold-c331-diagnostic-v1/fold-c331-execution-envelope-v1.
Both retain complete source/input unions;envelope binds new full-regression evidence.
Hash/size-bind outputs before/after saved reconstruction and before final records.
A fresh verifier reconstructs parent/test evidence and child metrics again without
model forwards. It does not replay historical optimizer updates or rerun all models.

Route:active_v2 ->invoke_c331 ->run_c331 ->c331_execution controller/worker ->locked
accepted C330/R1.2 evidence ->native readout preflight ->5898isolated tests ->30frozen
evaluations ->saved reconstruction ->2051final rereads ->fresh verifier ->log push.
Local:runs/c331-query-probe-<id>/science with enclosing regression-plan/evidence/result
and221module JSON/log pairs. Publish only console to c331/latest.log+latest.json.
All ten effect records are printed;full local cells and raw logits stay local/hashed.
No training-step progress is expected. Stop on any source/input/test/PID/control/
nonfinite/replay/schema/semantic/weight mutation. SAME C331 on INVALID,no C332.
Publication-only failure repairs publication without rerunning the probe.

After source/tests/runner/launcher/contract commit,reread every committed file and
compare raw Git blobs with tested local files;rerun48tests,CP932-default-open emulation,
UTF8/NUL/compile/import/free-global audit. Explicitly label toy models,synthetic
historical inventories and collaborator doubles. They are not full native5898tests
or genuine FOLD checkpoint execution. Retain user-side PowerShell AST checks through
dispatcher,selected launcher and runner before a scientific log is created.
No CI,paidservice,package reinstall,artifact deletion or accepted-result changes.

Manifest SHA256:8644f03a61e1dbdbb44a31514a392fd18cdb7ce71c190ee1a1fd2a8c759c30f8.
