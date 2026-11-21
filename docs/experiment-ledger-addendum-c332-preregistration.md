# C332 preregistration -- train-consistent first/mean readout

Date:2026-10-19 Japan time.
Experiment:C332-v5b-trained-first-mean-query;stage:V5-B-TRAINED-FIRST-MEAN-QUERY.
Acceptance base:bb7a025db8eb32c9de76646fc13a223e933ca155.
C331 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY);its frozen substitution is not adopted.
C329 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED;C333 NOT REGISTERED.
Separate committed-byte post-authoring review and ACTIVE registration precede a command.

## One question and intervention

Does training AND evaluating with the same fixed first_mean/last readout improve
original6 binding while retaining original2..5 and interior4,compared with native
mean/last at the same2400-update budget? C331's inference-only substitution worsened
most aggregate counts. That does not establish the performance of consistent training,
nor does it prove that train/inference mismatch caused the observed harm.

Two arms:native and first_mean. Call the unchanged accepted C331.readout on every
TRAIN forward and every evaluation/replay,using native_before for native and
first_mean for the candidate. The candidate changes only the FIRST query-projection
input from span_mean to .5*(span_mean+first_query_byte_local_state);the second last-
query-byte branch remains native. Coefficient.5 is fixed;no search or new attention.
This mixes representations BEFORE projection/attention,not three attention outputs.
The endpoint is a UTF8 byte,not a decoded Unicode character. Japanese limitations
remain explicit. No target,profile-specific choice or selected prediction enters it.

No accepted function/global/source is modified. Child-owned orchestration calls the
accepted removable hooks and preserves their input-provenance and cleanup checks.
Autograd flows through the candidate mean/first mixture;no detached teacher feature.
This is not the C317 last-to-first replacement or another frozen coefficient probe.

## Fresh paired cohort and equal training

Initialization seeds332001..332005;order seeds332101..332105. Build BOTH fresh model
instances for a seed before training either one. Require equal complete initial
state hashes and disjoint nonempty parameter storage. No accepted checkpoint is an
initialization. Train native then first_mean in each pair;all ten fits must finish
before any scientific evaluation. This order is fixed,not randomized after results.
Wall-clock arm differences are not causal performance/efficiency claims.

Both arms use native14256 parameters,3328shared-core parameters,64slots,CPUfloat64,
2Torch threads and the existing deterministic runtime. The same C308 core_slow
AdamW factory creates ONE optimizer per trajectory:noncoreLR.005/coreLR.0005,
betas(.9,.999),eps1e-8,weight_decay0;ordinary mean cross entropy,global gradient
norm clipping1. FIT_RNG612000 is set once per trajectory. No optimizer recreation,
rate decay,reseed or intermediate evaluation at the1200 boundary.

Construct the unchanged C326 batch4 mask for the new order seed's1200-event
plan_for_order(...,'two_to_four',...) schedule. Each event has24 intact query pairs,
48rows. Execute event indices0..1199 twice,in exactly the same order and masks.
C326 per-profile pair allocation retains11..13original pairs on length4 updates;
do not assert an exact12/12 split or change accepted helper globals.

Canonical data are192logical TRAIN/96HOLDOUT rows inherited from C329. Train only
original2/3/4 and interior4 name families. Each TRAIN row is presented200/200/100/100
respectively. Original5/6 remain untrained name families even on the logical TRAIN
evaluation split. Both arms have the same targets,exposure and order. Prepared
original/interior labels must agree. Hash all TRAIN tensors,labels,events and masks
before/after each fit and require identical paired input hashes. Keep the full
logical dataset/prompt JSON fingerprint unchanged across the experiment.

Persist all2400CE/rate/gradient-count/event-index traces,gradient parameter union,
initial/final model and core hashes,schedule/mask hashes and per-cycle exposure.
Hash model+optimizer immediately after1200 and before1201;require exact equality.
Final state is deep-cloned and detached without aliasing live nonempty tensors.
There is no saved1200checkpoint or checkpoint-selection rule in this experiment.
Saved reconstruction validates the recorded trajectory contract;it does not rerun
all2400historical updates or prove unrecorded intermediate parameter values.

## Evaluation, replay and fixed primary gate

After ALL ten fits,save and reload one ordered ten-state bundle. For each state,
load it into a fresh evaluation model,score using its TRAINING arm,load the same
saved state again and replay using that SAME arm. Check state hashes after each
pass and use unchanged C324 replay_error(<=1e-9,exactargmax). Save both full raw
passes,not just a replay-success label. Native/candidate models have different
trained weights:do not incorrectly demand query-blind equality across those models.

Use unchanged original1..6/interior4 normal,evidence-blind and query-blind evaluators,
original/interior scorers,paired HOLDOUT contrasts and C330 local failure summaries.
Retain every local TRAIN/HOLDOUT profile/language/entity/order condition. Thresholds
remain accuracy>=.90,query-pair>=.80,evidence-drop>=.35,query-drop>=.35,both-order>=.80.
Original1 is descriptive only. No expected-label repair or pooled-mean gate override.

C332's NEW preregistered primary gate requires ALL of the following:
1. All five first_mean models pass every original2..6 and interior4 local/masked/order gate.
2. For EACH seed,the original6 HOLDOUT answer and pair gains,pooled original2..5
   answer and pair gains,and interior4 answer and pair gains are all nonnegative.
3. Across all five seeds,original6 answer gain AND original6 pair gain are strictly positive.

Per-seed ties are allowed,including a saturated perfect native control;the cohort
still must strictly improve BOTH long-name counts. This is declared BEFORE C332
fitting,not a retrospective relaxation of C329 or C331. C329's verdict is unchanged.
Report all seeds,full local gates,and all per-length rescue/regression counts. A
scientific FAIL with valid execution is VALID NEGATIVE,not a reason to retry,select
seeds or search a different coefficient. No model is adopted by this gate alone.

## Exact work and output accounting

10training models/10evaluation models/10saved final states/10optimizer creations.
24000optimizer updates,1152000TRAIN-row presentations. Twenty evaluation/replay
passes each171model forwards/16416rows/684core forwards. Total27420model forwards,
1480320total rows,109680core forwards,54840query-projection calls. Twenty saved-state
loads,one scientific model-bundle reload and one new model-bundle write;network0.
Both evaluation and replay logits are persisted:672399360raw tensor payload bytes
(10states*2passes*16416rows*256outputs*8bytes),not336199680. This is not peak RAM or
all serialized bytes. Parent/saved verification and unit-test work are separate.

Separate native preflight validates ALL five actual schedules and one discarded
model on original/interior English+Japanese TRAIN examples. Nonzero output weights
avoid vacuous zero-reader checks. Plain native forward plus both hooked policies
produce6forwards/12rows/4backward calls/0optimizer updates. Native hook parity,
finite connected query gradients and unchanged weights are required. The discarded
model does not supply cohort weights. Toy gradient tests are software validation.

## Immediate accepted parent and complete evidence inheritance

C331 execution:36444b77b48ac1be5545a5346454142eb1955fb0.
Publication:41bd1ec9309c3d7e3d573abd70d0441f57ca6d0e.
Parent folder:runs/c331-query-probe-60e1b2a8ebe1465dba86f31409a6a9d1/.
Primary science/summary.json SHA256:
28f5aa242fdb26674e4f1b2bde6e752c8e4b7fea88c1fb19b6157a796acd4376.
Mandatory execution-envelope.json SHA256:
3b3bb3a591b225d8f03d30c374c47d2307d2ca744061601aa2fd2f3356b046a0.
Require fold-c331-diagnostic-v1/fold-c331-execution-envelope-v1,PASS,valid execution,
capability not applicable,exact manifest/work,full5898receipt,completed saved
semantics and2051final uncached rereads. Both parent maps must match847sources/2051inputs.

Use unchanged C331 executor snapshot to reconstruct its accepted source/input maps,
including the older C330-R1.2 proof files. Then bind C331's own445regression outputs:
regression-plan.json,regression-evidence.json,regression-result.json and221module
JSON/log pairs. Rebuild its exact5898-ID plan and validate all test success/PID/log
semantics using the accepted helpers. These445plus4science outputs+summary+envelope
make451mandatory immediate-parent outputs. No smaller receipt-only fallback.

Protection:853sources=847inherited+6own;2508inputs=2051inherited+451parentfiles+6own.
Accepted R1.2/C330/C331 sources,tests,contracts and all direct/lazy readout,C329,C326,
C325,C324,C308 and factory/scorer dependencies stay pinned. Every own benchmark,
executor,test,runner,launcher and this contract is protected. Historical accepted
files are never rewritten. Native R4 read leases span worker phases;independent
initial reference hashes and ALL2508final uncached rereads remain mandatory.

Reconstruct IMMEDIATE C331 scientific semantics by its unchanged
semantic_recheck(C331out,C329out,cx,C330_seed_flags,read) under no_neural. C329 data/
checkpoint and C330 seed-flag summary are already protected inherited inputs. Do
not mistake the C330 pure-JSON loader for the C331 three-mode tensor loader. Check
canonical dataset/prompt hashes and semantics. No older scientific semantic-body
recursion or parent neural forward;older byte/proof reconstruction still occurs.

## Regression, saved schemas and execution

Preserve original5898 ordered test-ID SHA:
31527c05d53e04cb8dd4804f7a3d255b90c7f5b35880d12e2b69f9abd6993adb.
Append48own tests:5946selected/222modules,5947before the sole inherited exact C204
mutable-ACTIVE exclusion. No new skips/exclusions,cached success or retry. Use fresh
sequential processes per module and C332-specific guards/CLI. Delegate ordinary
execution and generic module evidence checking to accepted C330-R1.2 helpers.
fold-c330-r1-module-v2 is an ABI bound to the NEW C332 HEAD/plan/index/module,not an
old experiment invocation. Retain direct/immediate-child PID and canonical markers;
never require launchPID==workerPID unconditionally. All5946tests must pass before fitting.

New regression plan/evidence schemas:fold-c332-regression-plan-v1/fold-c332-regression-v1.
Six scientific outputs:experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Bundle schema
fold-c332-trained-models-v1;raw archivefold-c332-evaluations-v1 holds10records with
both evaluation/replay and training policy/hash binding. Summaryfold-c332-science-v1
has scientific PASS/FAIL with diagnostic_execution_valid=true;envelope
fold-c332-execution-envelope-v1 preserves the same status and full protection maps.
capability_gate_applicable=true does NOT imply Gate F or general LLM capability.
gate_f_candidate=false;production_adoption=false.

Hash/size-bind all six outputs around saved reconstruction and before final records.
Fresh verification checks complete parent/source/input/output maps,all new222module
proofs,manifest/work,gate/count binding and saved trajectory/logit reconstruction,
without another fitted cohort or optimizer-history replay. A successor must retain
447new test-proof files(3+222*2) plus8science/summary/envelope files=455parent outputs.

Route:active_v2 ->invoke_c332 ->run_c332 ->c332_execution controller/worker ->locked
parent byte/proof/semantic checks ->native preflight ->5946isolated tests ->10fits
->saved-state evaluation/replay ->saved reconstruction ->2508final rereads ->fresh
verifier ->console publication. Localruns/c332-trained-query-<id>/science with
regression-plan/evidence/result and222moduleJSON/logpairs in the enclosing folder.
Console only publishesdocs/experiment-run-logs/c332/latest.log/latest.json;no tensors/data.
200update CE progress,ten saved-evaluation messages and all five deciding pairs.

## Authoring gate, limitations and stops

Reread all six committed files and compare Git blobs to tested local bytes;rerun48
own tests,CP932-default-text-open emulation,UTF8/no-NUL/compile/import and recursive
free-global audit. Verify production call ordering,actual writer/loader signatures,
fresh paired initialization,equal schedules,gradient routing and exact workload.
An actual2400-update tiny Torch fixture is NOT the native FOLD10-model scientific run.
Synthetic parent/scorer/lock/test-inventory collaborators must be labeled. Author
checks do not establish Windows/full5946success;mandatory user-side AST chain remains.

No causal claim about why C331 failed,optimal coefficient/budget,capacity limits,
arbitrary-length rules,independent repeated-task samples,Gate F or production quality.
Technical preflight/source/input/test/PID/nonfinite/replay/schema/semantic failures
are INVALID SAME C332,not C333. Preserve evidence,no automatic retry. Scientific
FAIL with complete integrity is negative evidence. Publication-only failures repair
publication without refitting. Stale/dirty/wrongbranch/ambiguousACTIVE/dependency/AST
failures skip before logging. Do not bypass RESULT_ALREADY_PUBLISHED using publicationHEAD.
No CI,paid services,package reinstall,artifact deletion or accepted-result changes.

Manifest SHA256:2a216840891fcc13c98890d525a23054e074d88464cf546223dd693f4cb50874.
