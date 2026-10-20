# C335 preregistration -- alternating TRAIN readouts, native-only evaluation

Date:2026-10-20 Japan time. Stage:V5-B-ALTERNATING-READOUT-TRAINING.
Experiment:C335-v5b-alternating-readout-training.
Acceptance base:6033993736efa1ed65e645fd0c11d801de25b15c.
C334 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY),C332 VALID NEGATIVE.
Gate F NOT PASSED;no first_mean/off-diagonal/production adoption or C336 registration.
Separate committed-byte review PASS and ACTIVE registration precede any user command.

## One scientific question

Does equal-budget exposure to both readout policies during TRAIN improve original6
binding while retaining other domains when BOTH arms evaluate using native mean/last?
C334's fixed-state crossover found original6 answers NN/NF/FN/FF=1405/1356/1403/1412
and pairs685/639/687/696. Neither global inference swap repaired the capability gap.
This motivates,not proves,the value of mixed training exposure. C335 is not a claim
that the C334 interaction identified an internal mechanism or a successful policy.

Fresh seeds335001..335005 and event-order seeds335101..335105;arms native/alternating.
Create each pair with identical fresh native weights in independent storage BEFORE
training either arm. Do not resume C332/C329 weights or select successful old seeds.
Only TRAIN readout exposure changes. Both arms evaluate and replay with native_before.
There is no first_mean evaluation,ensemble,test-time averaging or per-example policy
choice. The experiment is deliberately not a general invariance proof.

## Exact training policy and fixed exposures

Retain the accepted native14256parameters/core3328,64slots/64byte frame,CPUfloat64,
2threads,core_slow parameter grouping. Reuse the C331 readout context without editing
accepted modules/globals/functions. Native uses span_mean at the first query and
last-byte local representation at the second. first_mean changes only the first
input to .5*(span_mean+first-query-byte-local),retaining the second last-byte query.
This is a UTF8 BYTE position,not a complete Japanese character. Coefficient.5 is fixed.

Both arms execute the same C326 batch4/two_to_four TRAIN schedule of1200events twice,
with192logical TRAIN rows and48presentations per update. C335 changes no examples,
targets,event order,family masks,loss,capacity,optimizer or total update count.
No original5/6 name-family exposure is added. Per-row two-cycle family exposures
are original2=200,original3=200,original4=100,interior4=100.

For zero-based step k,let event=k%1200,cycle=k//1200. The native arm always uses
native_before. The alternating arm uses READOUTS[(event+cycle)%2],where READOUTS is
(native_before,first_mean). The second cycle reverses parity. Thus every identical
TRAIN event is processed ONCE by each policy,not twice by the same parity policy.
The candidate has1200native and1200first_mean forwards;the comparator has2400native.
This explicitly halves native-policy exposure in the candidate. Equal total compute
is not a claim that the original native-policy exposure is unchanged.

One actual model forward,one mean cross-entropy backward and one optimizer update
per event;no two-policy averaged loss or double-update budget. Exact policy sequence
and per-policy actual call/query/row/grad receipts are saved and verified. Hooks
are installed for that step and removed even on exception;no global monkeypatch.

Optimizer is the unchanged core_slow factory:AdamW,noncore.005/core.0005,betas.9/.999,
eps1e-8,weight_decay0;global gradient clip1. Fixed FIT_RNG612000 in both arms.
One optimizer spans all2400steps. Weights and optimizer states at1200/continuation
must match exactly;no restart or hidden schedule change. No intermediate evaluation,
early stopping,coefficient tuning or checkpoint selection. Train ALL10models before
any saved-model scientific evaluation. The comparator shares the same step-level
readout-context plumbing,so only the selected policy sequence differs.

## Evaluation, fixed gate and outcome meanings

Evaluate all original1..6/interior4,TRAIN/HOLDOUT,en/ja,profiles,entity sets,fact orders
and normal/evidence-blind/query-blind views with unchanged accepted scorers. Original1
remains descriptive/control-only. Keep thresholds.90/.80/.35/.35/.80 for accuracy,
query-pair,evidence-drop,query-drop,both-order. No HOLDOUT data enter optimize.

Each final state is safely saved,reloaded and evaluated,then reloaded and replayed
with native_before in BOTH arms. All114raw-view tensors must be finite CPUfloat64,
within1e-9maximum absolute drift AND exactargmax. Verify weight fingerprints after
each evaluation and dataset/prompt memory fingerprint after all execution. No demand
for equal query-blind outputs across DIFFERENTLY trained models is introduced.

The fixed capability gate retains the C332 form on the NEW cohort:
1. All5alternating models pass every existing original2..6 and interior4 gate.
2. Every pair has nonnegative original6answer/pair gains,pooled original2..5answer/
   pair gains,and interior4answer/pair gains versus its freshly trained native control.
3. Aggregate original6answer gain AND aggregate original6pair gain are strictly positive.
Per-pair ties are allowed;aggregate improvement remains required. A perfect comparator
may prevent strict aggregate improvement;that is retained as negative evidence,not
permission to relax thresholds or change the task after observing results.

scientific_status=PASS iff the fixed gate passes;otherwise FAIL. A technically valid
FAIL is VALID NEGATIVE,not a retry request. Numerical/replay/source/test/schema or
input-protection failures are INVALID SAME C335. Even scientific PASS does not itself
pass Gate F,authorize production,or show arbitrary-length/general-language ability.
No cross-experiment comparison of different seeds is used as the deciding comparator.

## Work, records and software boundary

10training models and10evaluation models;10final checkpoints in1new bundle.
24000updates/backward calls,1152000TRAIN row presentations.20full evaluation/replay
passes*171forwards=3420additional model forwards. Total27420forwards,1480320rows,
109680core forwards,54840query projection calls,20state loads,1bundle load.
No network calls. Raw saved-logit payload672399360bytes is not total serialization
size,peak RAM or guaranteed runtime. Per-step hook overhead is not claimed free.

Native preflight is separate:check all5real schedules and both2400-step policy plans;
one discarded native model with deterministic nonzero read.output weight,original/
interior English+Japanese examples,6forwards/12rows/4backward/0updates. Verify native
parity,finite gradients and unchanged preflight weights. No preflight state enters
scientific training. Regression toy gradients/training are software work,not cohort.

Six science outputs:experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Bundle schema
fold-c335-trained-models-v1 stores ordered identities/states. Evaluation archive
fold-c335-evaluations-v1 stores10records with seed,arm,state_sha256,evaluation_policy,
raw(evaluation/replay),receipts. Trace stores actual per-step mode and per-policy
counts,boundary/continuation,loss/rates/gradients,event order and input fingerprints.
Saved semantic reconstruction verifies the complete trace,states and scorer outputs,
not a numerical replay of the24000optimizer updates. Primaryfold-c335-trained-v1 and
companionfold-c335-execution-envelope-v1 both bind the complete source/input maps.

## Immediate accepted parent and source protection

C334execution:c6e9ead698ed053d2e96a93ff13febffb3d1b049.
Publication:82592e96643a9bf7c554e05c432b91b0eb1b79b2.
Folder:runs/c334-policy-crossover-2a49146b93204814986d1a320cd5f78f/.
PrimarySHA12130d6d096cd287a7f415108b5f71738bcc86d8ef439c7930ba4b0a390fbf81.
MandatoryenvelopeSHA1efb6d154a4c617da3547e9fce3c22fc224caf36fa32aea81d00eabec6bbea68.
Require diagnosticPASS,capability_not_applicable,exact manifests/work,identical
865source/3430input maps,complete6010tests and3430final uncached rereads.
The preserved C332 negative summary remains negative.

Pin C334executor5121773202174b7dec5eb50e26a95c613fe1df17 before loading. Its helpers
return named parent/inherited/recovery/c330/runtime/legacy/locks fields. Reuse its
snapshot to reconstruct all ancestor maps/proofs,then add ALL457parent outputs:
4science+primary+envelope+3regression records+224module JSON/log pairs. The451test
proofs are mandatory,including all exact test success/PID/log-marker semantics.
Child protection871sources=865+6;3893inputs=3430+457+6. No smaller-map fallback.

Immediate parent reconstruction calls C334.semantic_recheck(C334science,C332science,
C329data,cx,C332validation_summary,read) under no_neural. No older semantic bodies,
model inference or historical optimizer replay. C334's helper named parent is C333,
whose PARENT_FOLDER identifies C332;its c330 helper identifies C329 data. The child
adapter checks these source tensors/data belong to inherited protected inputs.
Readout/scorer/factory/curriculum/optimizer dependencies are already in inherited
source maps;all deciding direct/lazy imports remain pinned. Child does not call the
old C332 seed-restricted make_model/schedule with new seeds:its own factory/schedule
retain the same underlying native constructions and use registered C335seeds.

Native R4 read leases span parent/full-regression/training/saved verification. Keep
independent initial hashes and ALL3893final uncached rereads. Byte/size-bind all6
outputs around reconstruction and before primary/envelope writes. Fresh verification
checks parent,all new module proofs,source/input/output bytes and saved child semantics.
No unlocked fallback,accepted-file edit,artifact deletion or environment reinstall.

## Full regression, invocation and stops

Preserve all6010ordered test IDs;baseSHA
bc0ed7043461ce8da75c28ab9fcf1c84f5718d8493d5af705c9bc9c730b3065e.
Append48own tests:6058selected/225modules,6059before sole inherited exactC204mutable-
ACTIVE exclusion. No new exclusion,skip,cached success or retry. Sequential fresh
process per module;unchanged R1.2 generic ABI/PID/log validation,including direct or
immediate-child relationships. C335 owns guard/plan/CLI;all6058success before training.
Schemasfold-c335-regression-plan-v1/fold-c335-regression-v1;per-module generic
fold-c330-r1-module-v2 bound to NEW C335HEAD/plan/module/index.

Own six files:benchmark,executor,48-test module,runner,launcher,this contract.
Route:active_v2 ->invoke_c335 ->run_c335 ->controller/science ->locked C334parent
->native alternating TRAIN preflight ->6058tests ->10paired trainings ->native saved
evaluation/replay ->saved reconstruction ->3893final rereads ->fresh verifier ->push.
Local:runs/c335-alternating-training-<id>/science and module proofs/worker logs/envelope.
Console only mirrored to docs/experiment-run-logs/c335/latest.log/latest.json.
Print200-step training progress through2400,then10saved-native-evaluation markers,
all5paired comparisons and10state gates. Complete requires persisted_alternating_training
PASS,execution_envelope_verified andrun_execution_valid=true,including scientificFAIL.
Future parent inventory must include453new test proofs(3+225*2)+8science/summary/
envelope files=461outputs. Do not omit supplementary regression evidence.

Before user authorization,retrieve all six committed files through EOF and compare
Git blob IDs to tested local bytes;rerun48tests plus CP932-default-open emulation,
UTF8/NUL/compile/import and recursive global-binding audit. Real toy2400-step loops
and independent reference updates do NOT constitute native FOLD training or Windows
full6058execution. Label synthetic historical inventories/scorers/leases explicitly.
PowerShell dispatcher/selected launcher/runner AST preflights remain mandatory in
the user-side path. Do not claim author PowerShell execution when unavailable.

Wrong/stale/dirty/ambiguousACTIVE/dependency/AST conditions skip before science and
publication. No automatic retry on technical failure. No rerun for a valid negative
or publication-only failure. NoC336,CI,paidservices,package installation,gate relaxation,
post-hoc seed/policy selection or accepted-model retraining is authorized.

ManifestSHA256:946639b00b62504f89faf0c5a8a0b14fba375da031f1b17b11436a61b1ec48b0.
