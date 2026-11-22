# C346 post-authoring review

Date: 2026-11-22 Japan time.
post_authoring_review = PASS
Review target HEAD:be76c4c53c36105638e59e059af241078758b628.
Source tree:0f06d4eda13b258141fbb2259eb7843ab28fae8d.
Sole parent/acceptance base:f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2.

## Independent review of committed remote bytes

A nonauthor independently fetched all seven complete OWN files through the GitHub
connector at the exact source commit and read each through EOF. Remote byte lengths,
Git blob identities and SHA256 values agree with the clean source checkout,
publication payload,root audit,and BOTH final74-test author reports. The commit
adds exactly those seven files. No accepted source,test,launcher or preregistration
was changed. No review blocker remains;no post-review source correction was needed.

Independent review receipt SHA256:
19bb4e0aaada93e23b8c56a169e602ff2256cf8eaf6ca61ea9d4f6919e94e83c.

|Path|Bytes|Git blob|
|---|---:|---|
|fold_lm/v05_benchmarks/model_c346_pair_max_rate.py|46282|684970a7a1d073f22422cb46f7f1514802af832e|
|tools/c346_execution.py|29876|7950248a3d9acd9e8eb8c7da48b1b707ea478d85|
|tests_lm/test_v05_c346_pair_max_rate.py|51569|2363e5ea696c2bef28bb2d173907f7ae5d9e331c|
|tests_lm/test_v05_c346_execution.py|37439|4cc5791bb81f6d261591243f9498cae5cdb00a94|
|tools/run_c346.ps1|966|01f631a6195c6a597e3c20a682fa5bb4ef7de657|
|tools/invoke_c346.ps1|3147|1c0464aac7be79ae0d0c122cca8365e4feb04de0|
|docs/experiment-ledger-addendum-c346-preregistration.md|11583|994b35c0549b85ebbf504b179cf2aae48c21e33a|

## Author verification of the exact reviewed files

Combined48science+26execution=74tests PASS in the Linux author environment:

|Condition|Tests|Seconds|Failures|Errors|Skips|Expected failures|Unexpected successes|
|---|---:|---:|---:|---:|---:|---:|---:|
|Normal text-open defaults|74|105.273|0|0|0|0|0|
|CP932 default text-open emulation|74|101.910|0|0|0|0|0|

Runtime:Python3.12.14/Torch2.10.0+cpu/NumPy2.3.5. Tests began at acceptance
HEADf5fc8e89b5bb3d2749df91aa3b503596a6be1fc2 with the seven completed new files
present locally. All seven SHA256 values stayed constant during both runs and
match the reviewed published source. These are author checks,not a native Windows
C346run and not tests whose starting commit was the later source publication.

Three synthetic2400-update trajectories exercise actual optimize/train_one paths,
measured train/core/query receipts,identical streams,constant rates and continuous
optimizer state. Independent first-four-update references cover every arm. A synthetic
first-update fixture verifies equal pair-max gradients/moments and half first updates
in both groups;later actual updates are not claimed to remain exactly half.
Separate native-model tests check exact core/noncore optimizer membership and reject
rate,hyperparameter or group-order drift without updating the native model.

The discarded native preflight executes24forwards/96rows/12backwards/0updates and
checks three optimizer configurations. Production-order tests observe all15fits
before30evaluation/replay calls,30state loads and one saved checkpoint-bundle reload.
Saved reconstruction uses real scorers with invented logits under no_neural.
All240individual inequality mutations and four strict-tie cases reject invalid
positive gates. Perfect-control saturation remains valid negative. Test48 confirms
that larger terminal losses cannot override a positive binding gate.

The science author's first48-test run passed112.444s. Afterwards,only test11's name
was clarified from candidate_updates to default_pairmax_updates;its body did not
change. Both FINAL74-test runs,full ordered-ID hash and this remote review use the
final name. Earlier inventory fingerprints are not used for registration.

## Independent inventory and static audit

All four Python files are UTF8/noNUL,importable and compile successfully.
Independent remote-byte walk:333compiledcodeobjects,2327LOAD_GLOBAL,0unbound names.
Pyflakes0findings. No inspect.getsource assertions were introduced. API arity and
actual behavioral dispatch are checked;no comment/docstring match is treated as
execution evidence. Count contracts use actual loaders and test IDs.

The independent loader yields6653raw candidates,6652selected IDs and243modules.
Own48+26 append to the exact6578-ID/241-group parent prefix. The sole inherited
excluded ID remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusion,skip,accepted-test edit or mutable-ACTIVE assertion was introduced.
Full ordered-ID SHA256:
39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Parent ordered-ID SHA256:
2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.

ActualPowerShell7.5.4 Parser.ParseFile evidence has zero errors for
invoke_active_v2.ps1,invoke_c346.ps1,run_c346.ps1 and the short standard user block.
The final activation HEAD is substituted into that block and parsed again before
delivery. The dispatcher parses its chosen launcher;the launcher parses itself
and runner. Branch/cleantrackedtree/ExpectedHead/uniqueACTIVE/dependencies precede
log creation/publication. Named CLI arguments and module-index/plan-hash dispatch
are consistent. Wrong or stale invocations skip without a scientific log publish.

## Scientific question and gate

Manifest8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64
matches code and preregistration. C346 is V5-B-PAIR-MAX-RATE:does fixed half-rate
pair-max improve interior answer/pair correctness and retain all domains against
both default-rate pair-max and ordinary mean CE?

All5fresh seeds346001..346005 use orders346101..346105 and three independent
identical initial states. The pair-max arms select exactly the same unscaled
full256CE maximum across canonical counterpart queries. Rates alone change from
.005/.0005 to.0025/.00025 at initialization. Continuous AdamW betas(.9,.999),eps1e-8,
decay0,clip1,2400updates,mixed45 exposure,48rows/24pairs and architecture remain fixed.
OrdinaryCE is a strong reference;there is no half-rate CE arm or factorial-interaction
claim. C345 motivated this fixed intervention but did not establish an optimal rate.

The gate is all5candidate full original2..6+interior4 passes,120nonnegative answer/
pair inequalities against each of two controls,and four pooled strict interior
TRAIN/HOLDOUT answer/pair gains against defaultpair-max. Comparator direction,
integer conservation,complete coordinates,full-pass binding and subgate totals are
validated. Zero headroom or a tie never permits reseeding or gate relaxation.
Terminal180state/domain/split summaries and120contrasts are descriptive only.
Terminaldomainmeans are not the whole exposure-weighted objective;norm>1 is not
an exact clipping count. No convergence or causal clipping mechanism is claimed.

## Parent semantics and dependency protection

Immediate parent is the accepted C345diagnostic-v1/PASS,not a substituted C344trained
schema. Exact C345summary/envelope identities and diagnostic_execution_valid=true,
capability_gate_applicable=false preserve nested C344candidatefalse/eligible2.
C345semantic_recheck(out345,out344,data_out,cx,read) uses five arguments underno_neural.
C346preflight/training/recheck use5/6/4arguments. Training/preflight are outside
no_neural;parent and saved arithmetic reconstruction are inside it.

The pinned C345executor is imported only after exact Git blob and file-byte checks.
Its helper bridge explicitly selects C344-R1cleanup via h['prior']['parent'];C345
itself does not export the required boundary. Six native checks and scoped module
cleanup keep the accepted implementation receipt while binding the child HEAD.
The parent's receipt remains bound to its original C345execution HEAD.

All direct/lazy scientific dependencies resolve through immutable C345/C344/C332/
C342/C338/C324/C331/C326 helpers and the existing model/policy context. Native runtime,
legacy verifier,recovery and read-lease implementations are also inherited/pinned.
No new unprotected deciding module was introduced. Snapshot enforces source/input
binding,collision rejection and exact inherited maps. Protection is944sources and
9177inputs=8679+491parentoutputs+7OWN,with capacity9177 and all9177uncachedfinalrereads.
Parent491outputs include4science+primary+envelope+485proofs(3+241JSON/logpairs).

## Production order, work and boundaries

Actual route:runtime/sixcleanupchecks -> locks/snapshot/immediate C345semantics ->
discarded native objectivepreflight ->6652fresh-process tests ->all15fits ->
checkpoint save/reload/evaluation/replay ->saved no-neural reconstruction ->
all9177input rereads ->separate fresh verifier ->dedicatedconsolelog publication.
No evaluation can select or stop a fit;every fit finishes before cohort evaluation.

Scientific15models/15optimizers/36000updates/1728000trainingrows reconcile with
41130model forwards,2220480totalrows,164520corecalls,82260querycalls,30stateloads,
1checkpoint-bundleload and1newbundlewrite. Observed train/evaluation receipts are
checked against the registered work. Sixscience artifacts plus primary/envelope
and489regressionproofs yield497outputs for a successor. Raw saved logits1008599040bytes.
The separate native preflight and regression fixtures are not hidden in these totals.

This independent review did not run a formal cohort,retest the full historical
regression or claim native Windows completion. Native Python3.13.15/Torch2.10.0+cu130/
NumPy2.3.5 runtime checks,Windows leases,all6652tests and efficacy results remain
for the formal execution. C344negative and GateFNOTPASSED remain unchanged.

## Activation boundary

This PASS supports a documentation-only activation after sourcebe76c4c.
Keep every reviewed OWN blob unchanged. Authoritative handoff records exactly
C346 ACTIVE / NOT YET JUDGED,post_authoring_review = PASS,and this review target.
User ExpectedHead is that later activation commit,not source,C345execution/log,
acceptance or main merge. C347 remains unregistered until C346valid judgment.
