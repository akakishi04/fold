# C335 post-authoring review

Date:2026-10-20 Japan time.
post_authoring_review = PASS
Committed source/preregistration review target:
9b570b8792d2ce0e64b1380dabf536f0aa163802.
Acceptance base:6033993736efa1ed65e645fd0c11d801de25b15c.
This is authoring approval,not native Windows/full6058 regression or a C335 outcome.
Use the subsequent documentation-only activation HEAD in the user command.

## Committed-byte reread and identity

All six committed files were retrieved at the exact source commit and read through
EOF after publication. Benchmark ranges1..120,121..240,241..361;executor1..135,
136..270,271..402;tests1..110,111..220,221..330,331..440,441..510,511..566;
both complete PowerShell files;contract1..95,96..185. Their returned Git blob IDs
match independently calculated IDs of the local raw files tested below.

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c335_alternating_readout_training.py|f850270aefe9d3cd352ef5d4f48b06bc7ed770da|
|tools/c335_execution.py|49e2a9c8103851ccfffaa283d4fd8943170fbaf3|
|tests_lm/test_v05_c335_alternating_readout_training.py|342f7723678de5f9bd8cad1b8e4e9a5e75840b37|
|tools/run_c335.ps1|ee99451d6d316691d93f304a9b74d8b51c1449f6|
|tools/invoke_c335.ps1|fd091bdc601cb1686a9c4adcb6f8b2a4e18ba728|
|docs/experiment-ledger-addendum-c335-preregistration.md|fb19e6e26ade4ac177f12dcf796623df8ec956c7|

Remote compare against603399 confirms exactly these six additions. Accepted source,
tests,contracts,logs and dispatchers are unchanged. No source amendment was needed
in this committed-byte review. Acceptance,source and review/activation are separate.

## Actual checks after remote reread

Normal48/48 PASS,0failures/errors/skips,12.254008969999859seconds.
CP932-default-text-open emulation48/48 PASS,0failures/errors/skips,11.829706333000104seconds.
Each ran in a separate author Python invocation. CP932 wraps both builtins.open and
io.open only when text encoding is unspecified;explicit encodings/binary modes remain.
All six files decode UTF8 without NUL and have no trailing whitespace. All three
Python files compile/import. Recursive LOAD_GLOBAL audit of227function/method/nested
code objects finds0undefined globals. Actual48unique ordered test-ID SHA256:
6aaa58498500d22272ee4ab13771d2c7a5932514733029180c0bbc232063963f.
Manifest self-hash validates:
946639b00b62504f89faf0c5a8a0b14fba375da031f1b17b11436a61b1ec48b0.
Local file blob IDs match the remotely reread IDs before/after these checks.

Author environment:LinuxPython3.13.5/Torch2.10.0+cpu/NumPy2.3.5,2Torch threads.
The local tree contains the six authored files,not a complete repository checkout.
No installation,paid computation or CI. No native PowerShell executable is available;
its AST execution was not performed here. Native user-side dispatcher/launcher/runner
AST checks remain mandatory. CP932 emulation is not native Windows locale testing.
These checks do NOT establish actual FOLD training,C332/C334 artifact replay or native
Windows6058historical test success. Synthetic collaborators are detailed below.

Completed mutation control:replace child policy_plan in memory by all-native for
both arms. Test04(per-event policy coverage) and test13(actual trained-state difference)
each fail their explicit assertions:2tests,2expected failures,0errors/skips,7.614seconds.
The real production optimize loop runs under that mutant with the toy collaborators.
The function is restored,manifest validates again,and all six file hashes are unchanged.
An earlier author-only mutation invocation selecting04/12 exceeded its30second command
limit after printing04FAIL and starting12;it is NOT counted as a completed mutation
check. The completed04/13check above supplies the recorded control. Neither invocation
is a scientific run or a failure of the reviewed normal suite.

## Changed variable, training arithmetic and independent reference

Only TRAIN policy exposure changes;both arms evaluate native_before. Fresh335001..5
initializations and335101..5event-order seeds are explicit. The child factory follows
the inspected C332 native construction while permitting only the new seeds. It does
not feed new seeds to the seed-restricted accepted C332.make_model or schedule.
Each pair is created before either arm trains,with equal initial state hashes and
non-overlapping parameter storage. No accepted weights are resumed or selected.

The alternating plan uses(event+cycle)%2 over two1200-event cycles. Opposite second-
cycle parity makes every identical event see native_before and first_mean once each.
The comparator uses native twice. No extra examples,loss terms,model parameters,
forward calls or updates are introduced. Candidate native-policy exposure is halved;
equal total exposure is not equal native-only exposure. All policy modes and measured
per-policy call/query/row/gradient receipts are retained and checked.

C332 optimize/source was inspected:meanCE,globalclip1,the unchanged core_slow optimizer,
fixed rates and one optimizer across2400updates. C335 preserves this arithmetic and
boundary/continuation weight+optimizer hashes. It changes the per-step readout context,
using the accepted C331 implementation for both comparator and candidate. Each step
has one forward/backward/update;hooks are removed before the next step,also on error.
There is no average of two policy losses or hidden doubled budget.

The own tests actually run production optimize for2400updates on a small Torch model
for EACH arm. A separately written reference loop constructs AdamW independently,
selects batches and policy parity without the production planner/context/optimizer
wrapper,and also runs2400updates for each arm. All2400CE values and final state hashes
match exactly for both arms. The two policies produce different trained states from
equal initial states. This is strong software-arithmetic evidence on a toy,NOT an
actual14256parameter FOLD model or the scientific10model cohort. The native readout,
curriculum and dependency callbacks are explicit toy collaborators in these checks.

Additional tests cover one-forward receipts,optimizer continuation,gradient inventories,
deep state copies,exception cleanup,native preflight backward execution,trace tampering,
bad mode/seed types,per-event coverage and missing/boolean counts. The native user
preflight still exercises the actual accepted readout and real schedules before full
regression. It uses a discarded model;no preflight state enters the training cohort.

## Writer, evaluation, gate and valid-negative semantics

The actual run_training orchestration is tested using real Torch model state loading,
archive writes and saved reconstruction with synthetic training/measurement/scorer
callbacks. It performs all10training calls before any of20evaluation/replay calls;
every evaluation callback requires native_before. Bundle/evaluation schemas and
ordered identities are C335-specific. No C332 archive is accidentally dispatched as
C335. The actual analyze function verifies ten traces and records against states,
paired initial/schedule/input/rate equality,policy plans and complete domain metrics.

Accepted C334.same_tree checks all114raw tensor leaves and exact argmax as well as
1e-9drift;it is already in the inherited source map. Accepted C331summarize/compare and
C332contrast_check retain old scorer thresholds and per-answer/pair rescues/regressions.
Synthetic scorers in author fixtures are explicitly not native FOLD quality results.
The child gate tests require all5candidate full passes,per-pair nondegradation and
strict positive cohort original6answer AND pair gains;ties alone do not pass.

scientific_worker and verify_outputs FUNCTION tests preserve a technically valid
negative,write scientific_statusFAIL and successfully verify it. A forgedPASS is
rejected. Failed regression never reaches training. The fresh production verifier
will run in a separate user process;the author fixture calls its function with
synthetic ancestor/runtime/lease callbacks,not an independent native parent replay.
Saved reconstruction checks traces/states/metrics,not numerical reexecution of all
historical optimizer updates. All scientific outcomes remain unfabricated until run.

## Parent evidence, protection and regression bridge

Immediate parent is accepted C334diagnosticPASS with exact summary/envelope hashes,
865sources/3430inputs,6010tests and3430final uncached rereads. Its whole negative C332
validation summary is preserved. The parent executor is pinned before import.
C334.helpers returns named parent/inherited/recovery/c330/runtime/legacy/locks fields.
Its parent field is C333,whosePARENT_FOLDER is C332;its c330 field points to C329data.
The six-argument C334semantic_recheck receives the correct three folders,cx,saved C332
summary andread. A production-path adapter fixture checks that exact signature.
Older scientific semantic bodies and model forward calls are not rerun.

All451C334test proofs plus4science/summary/envelope=457parent files are included.
Actual temporary-file tests exercise the full parent-output union and detect tampered
last-module logs. The older input/source maps in those tests are synthetic. Native
snapshot reconstructs and compares the real maps using unchanged C334 helpers and
validates every parent test ID,success receipt,PID topology and canonical log marker.
Protection871sources=865+6,3893inputs=3430+457+6;no smaller-map or receipt-only fallback.
All direct/lazy deciding readout,factory,optimizer,curriculum,scorer and recovery imports
are inherited dependencies;new own source paths are added before scientific work.

The new test plan preserves6010ordered IDs and appends the actual48-test loader for
6058tests/225modules. Historical inventory/receipts in author tests are synthetic and
are not claimed as an actual6010run. Native module execution/checks reuse unchanged
R1.2 generic evidence ABI under C335guards/HEAD/plan. Direct/immediate-child PID rules
remain;no equality-only assumption. Collector/verifier tests check450delegations and
log tampering,missing/duplicate/reordered tests,mixed namespaces and first-error stop.
No new exclusions/skips/cached success or retries. The sole inherited C204 exclusion
and its immutable replacement remain unchanged.

Native R4leases cover parent/tests/training/reconstruction. All3893inputs get final
uncached rereads;all6science outputs are byte/size-bound around saved reconstruction
and before primary/envelope writing. Fresh verification rechecks complete maps,
new225module proofs,workload,manifest,valid scientific verdict and saved metrics.

## Invocation and approval boundary

Both new PowerShell scripts and the unchanged active_v2 dispatcher were reread.
The user entry parses the dispatcher;it parses the selected launcher;the launcher
parses itself and runner before logging. Branch/HEAD/tracked-tree/uniqueACTIVE and
dependency checks also precede publication. PythonCLI names/arguments,output prefix
andC335log publication agree. No native author PowerShell AST success is claimed.

The final review/ACTIVE commit is documentation-only. Authoring review PASS permits
one registered native execution;it does not predict its scientific verdict. Technical
failures preserve the attempt and repair SAME C335. A valid negative is accepted,
not retried. Publication-only failures repair publication without training again.
NoC336,GateF,production adoption,paidservices,CI,installation,artifact deletion,
accepted-source mutation or post-hoc threshold/seed/policy selection is authorized.
