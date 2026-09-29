# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C279 ACCEPTED PASS (diagnostic integrity only). C280 ACTIVE / NOT YET JUDGED. C281 NOT REGISTERED.**
C279 execution b07425eddfab2d4f3f6bacd8dff02295b44f3063 is authoritative.
C279 PASS means saved C278 failure-profile audit integrity only; capability_gate_applicable=False.
C279 shows the mean_final_dual residual is concentrated in shared_suffix2, with evidence_drop failures worsening there despite broad gains elsewhere.
Gate F remains NOT PASSED. C280 is the unique ACTIVE capability experiment; no production adoption, seed selection, support retuning, or C281 registration.

## Latest accepted science — C279

Acceptance:docs/experiment-ledger-addendum-c279-c280.md.
Execution:b07425eddfab2d4f3f6bacd8dff02295b44f3063.
Published log:ad5eed44f8ba66d29cda9627d54245b56fb8ff13.
Summary:runs/c279-v5b-saved-dual-audit-e6d76ea781994de085b16ea8e7a6b972/summary.json.
Summary SHA256:a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False;model_forward_calls=0.

Triple criterion delta candidate-control:
-accuracy -78;
-query_pair_accuracy -78;
-two_order_accuracy -39;
-query_drop -49;
-evidence_drop -10.

shared_prefix2 HOLDOUT delta:
-accuracy -29;
-query_pair_accuracy -29;
-two_order_accuracy -14;
-query_drop -17;
-evidence_drop -10.

shared_suffix2 TRAIN delta:
-accuracy -12;
-query_pair_accuracy -12;
-two_order_accuracy -4;
-query_drop -3;
-evidence_drop +4.

shared_suffix2 HOLDOUT delta:
-accuracy -9;
-query_pair_accuracy -9;
-two_order_accuracy -8;
-query_drop -7;
-evidence_drop +5.

Interpretation:mean_final_dual broadly improves direct discrimination,query dependence and two-order
consistency. The remaining asymmetry is shared_suffix2 evidence dependence: evidence_drop failure
counts increase while almost every other registered criterion improves. C280 should test whether
removing query/self tokens from the memory-attention support fixes that residual without changing
query vectors,parameters,training policy or gate. C280 is not registered in this acceptance commit.

## Latest accepted science — C278

Acceptance:docs/experiment-ledger-addendum-c278-c279.md.
Execution:ca6e45cc90b3b48e3d56c10acde72e35574878fd.
Published log:f74d8b1d340a7c744948b39645a1f4d30f1ea524.
Summary:runs/c278-v5b-mean-final-dual-c1d5206c6c6a48ab98acd15c5cb8aa71/summary.json.
Summary SHA256:557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.

Pass counts:
-mean_span: two-char5/5; triple0/5; whole0/5.
-mean_final_dual: two-char5/5; triple0/5; whole0/5.

Aggregate triple correct/collapse across TRAIN+HOLDOUT:
-mean_span:3938/4320 correct;314 collapsed pairs.
-mean_final_dual:4207/4320 correct;95 collapsed pairs.

HOLDOUT shared_prefix2:
-mean_span401/480 correct;63 collapse.
-mean_final_dual476/480 correct;3 collapse.

HOLDOUT shared_suffix2:
-mean_span416/480 correct;30 collapse.
-mean_final_dual438/480 correct;29 collapse.

Interpretation:separate mean/final attention is a strong shared-prefix improvement but not a complete
three-character solution. The residual failure is concentrated in shared_suffix2 and varies by seed.
C279 should diagnose the persisted fixed-criterion failure profile before another architecture change.
C279 is not registered in this acceptance commit.

## Latest accepted science — C277

Acceptance:docs/experiment-ledger-addendum-c277-c278.md.
Execution:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
Published log:7a46048503459aa7e03982b22c8dc8cf5ad2f976.
Summary:runs/c277-v5b-saved-lr-audit-7e9cad9663144ae9bdbacda802c21306/summary.json.
Summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False;model_forward_calls=0.

C277 triple criterion delta(candidate-control):
-accuracy -37;
-query_pair_accuracy -37;
-two_order_accuracy -18;
-evidence_drop +3;
-query_drop +1.

Stable/control-good seeds276001/276002/276004/276005 worsen in aggregate:
accuracy+1;query_pair+1;evidence_drop+12;query_drop+15;two_order+3.
The overall lr0.0025 improvement is therefore dominated by broad recovery seed276003.

shared_suffix2 HOLDOUT candidate-control:
accuracy-7;query_pair-7;two_order-5;evidence_drop+4;query_drop+5.
Lower lr improves direct answer/query discrimination but weakens registered mask sensitivity.

C276 remains ACCEPTED VALID NEGATIVE.
C275/C274 remain ACCEPTED PASS for diagnostic integrity only.
C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in bounded scope.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Active C280 — evidence-only dual memory support

Experiment:C280-v5b-evidence-only-dual-memory.
Stage:V5-B-EVIDENCE-ONLY-DUAL-MEMORY.
Registration:docs/experiment-ledger-addendum-c280-preregistration.md.
Design:docs/v5b-evidence-only-dual-memory-v0.1.md.
Acceptance base:9299883b69eadb049675b775fc4a152e7ab1f225.
Parent C279 execution:b07425eddfab2d4f3f6bacd8dff02295b44f3063.
Parent C279 summary SHA256:a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb.

One question:with identical fresh paired CE training,does keeping C278's mean/final query vectors but
restricting both attention softmaxes to evidence positions before the visible query bytes improve
reliable two/three-character binding relative to C278's all-valid-token memory support?

Fresh seeds280001..280005;arms all_token_dual and evidence_only_dual.

all_token_dual is the actual C278 MeanFinalDualReadout.
evidence_only_dual has the same14256 parameters/state keys and identical mean/final query vectors.
The sole intervention is softmax key-value support:
-valid positions strictly before the first visible query byte;
-final separator semicolon included;
-visible query bytes,final equals,EOS and padding excluded;
-two separate masked softmaxes retained;
-retrieved memories averaged;
-shared read.output applied once.

Training/evaluation:
-96 paired TRAIN groups;
-800 updates/model,10 models,8000 updates total;
-AdamW lr0.005,mean CE only;
-384000 training rows;
-9080 total model forwards;
-487680 row presentations;
-36320 core calls;
-C267 two-character plus C270 three-character fixed gates;
-candidate PASS iff all five evidence_only_dual states pass both complete tasks.

Protection:
-source pins526;
-protected inputs926;
-direct deciding dependencies56;
-own tests24;
-modules165;
-loaded3886/focused3885;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac.

## C280 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = ac3ab86e424c2d17bf1e8696c511dbb6654c3894

Compared C279 acceptance9299883b69eadb049675b775fc4a152e7ab1f225 to review target:
only C280 OWN6 paths differ.

Committed OWN6 blobs:
-source:b0fbd492675ff8d147af13573b26c09c3d4afcab
-test:37c1b8968cdaf63d671eae2e42f25663a3a33a3e
-runner:8af69a6aadbda6b8e8cdae7f7be5d9bcc7c1b47c
-launcher:66f28fe95de9d26b928908aeecd726e6934959dd
-prereg:e646dd6fb10d13e38f1f33c0b5552ac205598745
-design:6d40125fe6d784f7a0c8abaea1cad14f93ea49d3

Static review confirms exactly24 own tests;no NUL/PENDING seal;source/prereg manifest agreement;
actual C278 MeanFinalDualReadout control;candidate keeps identical mean/final queries and shared
query/key/output parameters;both candidate softmaxes use evidence=valid & pos<first_query_byte;
final separator semicolon is included while query bytes/EOS are excluded;two softmaxes and one
post-average output remain;C279 parent verification is Module-call blocked;C279/C278/C277/C276/C275/C274
summary identities are independent;source526/protected926/direct-dependency56 contracts are explicit;
runner py_compiles before science and requires own24+focused3885;launcher resolves authoritative C280
and runs Validate before Execute.

## C280 authoring preflight recovery

Initial activation HEAD47b6990c87872a4f7b9167f8b5d6bed04c8c94a0 reached runtime Validate and stopped before
scientific execution because precheck used an inverted manifest-seal guard: it rejected the exact
sealed SHA as "manifest not sealed". invocation_skipped=AUTHORING_RUNTIME_PREFLIGHT_FAILED;
experiment_executed=False;execution_log_publish_attempted=False.

Recovery changes only:
-fold_lm/v05_benchmarks/model_c280_evidence_only_dual_memory.py: replace the inverted equality guard
 with a 64-lowercase-hex seal-shape check; the existing exact manifest digest equality remains.
-tests_lm/test_v05_c280_evidence_only_dual_memory.py: extend existing test01 to lock the repaired guard.

Recovery commit:ac3ab86e424c2d17bf1e8696c511dbb6654c3894.
Compared with activation HEAD47b6990c87872a4f7b9167f8b5d6bed04c8c94a0,only those two files
changed. Scientific conditions,manifest content/digest,arms,seeds,schedule,optimizer,attention
support,thresholds and workload are unchanged.

Remote-byte recovery review = STATIC PASS / RUNTIME GATE PENDING.
The repaired source keeps manifest SHA c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac,
uses the evidence-only support mask unchanged,retains two candidate softmaxes/one output,and keeps
source526/protected926/direct-dependency56 contracts. Own test definition count remains24.

No complete user-local runtime is available to reviewer. Therefore own24,focused3885,PowerShell
ParseFile,parent artifact replay and real ten-model training are NOT claimed executed here.
Mode Validate is authoritative.

## C280 execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C280 ->
Mode Validate(parent/source/artifact precheck526/926 + sealed manifest,own24,focused3885) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,both-task evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C280.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without changing
the evidence-support boundary inside C280.
C281 stays unregistered until C280 is judged. Gate F NOT PASSED.

## Completed C279 — saved mean/final dual-query failure-profile audit

Experiment:C279-v5b-saved-dual-failure-profile-audit.
Stage:V5-B-SAVED-DUAL-FAILURE-PROFILE-AUDIT.
Registration:docs/experiment-ledger-addendum-c279-preregistration.md.
Design:docs/v5b-saved-dual-failure-profile-audit-v0.1.md.
Acceptance base:b3745f7d90565297cd4d19024d7da4fd62954251.
Parent C278 execution:ca6e45cc90b3b48e3d56c10acde72e35574878fd.
Parent C278 summary SHA256:557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b.

One question:for accepted C278 saved outputs,which fixed gate criteria remain responsible for
mean_final_dual three-character failures by seed,split and profile,and is the residual failure
specifically concentrated in shared_suffix2 mask sensitivity/two-order behavior rather than direct
answer discrimination?

C279 is saved-output diagnostic only:
-model_forward_calls=0;
-row_presentations=0;
-core_forward_calls=0;
-train_steps=0;
-new_checkpoint_writes=0;
-model_state_loads=0.

Primary registered views:
-all triple criterion failure counts and candidate-minus-control deltas;
-shared_prefix2 HOLDOUT;
-shared_suffix2 TRAIN and HOLDOUT;
-per-seed triple deltas278001..278005;
-signed negative-margin ranges and exact failed records.

Formal PASS means diagnostic integrity only. capability_gate_applicable=False.
Gate F remains NOT PASSED regardless of diagnostic values.

Protection:
-source pins520;
-protected inputs916;
-direct deciding dependencies55;
-own tests24;
-modules164;
-loaded3862/focused3861;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
daeea4cfcf5083ec9a5237ea092f0c11ac7ab3cf38b76e9cdf62f60c4fea1af7.

## C279 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 8f14be01ac0e1cdf15e5edf990a18292d7dbb048

Committed OWN6 blobs:
-source:6302d7c6ddddd86d5ce8e70367746f39211f04ed
-test:aba202e52bb1977ca8eba2efeb10b0bdab6161fe
-runner:408f0d63053c25e4016ed168e17bc1c3b0b07ac8
-launcher:17e34313205ed479b10dec718188b3ff923b42c3
-prereg:2031e328d5d548e38e2d0501d7c8a934101965f7
-design:602d25fc03609b238c8b456218c59083b0c429b3

Static review confirms no NUL/PENDING seal;exact24 own test definitions;manifest/prereg seal agreement;
C278 verify_artifacts is the parent loader;parent verification is enclosed by a neural Module-call
block;C278/C277/C276/C275/C274 summary identities are independent;all seven C278 artifacts are
hash-pinned;source520/protected916/direct-dependency55 contracts are explicit;the direct dependency
pattern includes through C278;runner performs py_compile,parent precheck,own24 and semantic focused
suite before Execute;launcher requires authoritative C279 ACTIVE and publishes only C279.

No complete user-local runtime is available to reviewer. Therefore own24,focused3861,PowerShell
ParseFile,parent artifact replay and saved diagnostic reconstruction are NOT claimed executed here.
Mode Validate is authoritative.

## C279 execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C279 ->
Mode Validate(parent/source/artifact precheck520/916 + sealed manifest,own24,focused3861) ->
authoring_runtime_preflight=PASS ->
Mode Execute(saved diagnostic only,zero model forwards,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C279.
C280 stays unregistered until C279 is judged. Gate F NOT PASSED.

## Completed C278 — mean-span plus final-boundary dual attention

Experiment:C278-v5b-mean-final-dual-query.
Stage:V5-B-MEAN-FINAL-DUAL-QUERY.
Registration:docs/experiment-ledger-addendum-c278-preregistration.md.
Design:docs/v5b-mean-final-dual-query-v0.1.md.
Acceptance base:8a9340c5165754080ea729cf013b6015035df824.
Parent C277 execution:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
Parent C277 summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.
C276/C275/C274 parent summary SHA256:
6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f /
1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb /
0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

One question:with identical fresh paired CE training,does keeping the mean visible query-span signal
and final visible query-boundary signal separate through their attention softmaxes,then averaging
retrieved memories,improve reliable two/three-character binding relative to mean-span attention alone?

Fresh seeds278001..278005;arms mean_span and mean_final_dual.
mean_span is the actual C269 SpanQueryReadout.
mean_final_dual has exactly the same14256 parameters/state keys and uses:
-mean visible query-span pre-core state -> shared read.query -> masked attention A;
-final visible query-byte pre-core state -> same read.query -> masked attention B;
-same read.key(local memory);
-memory=(memory_mean+memory_final)/2;
-shared read.output once;
-unchanged post-core residual/readout_norm/decoder.

For a one-byte query,mean and final states are identical,so candidate reduces exactly to the control
attention computation. No supervision metadata enters model.forward.

Training:
-exact C267 two-character dataset SHA256
 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
-96 paired TRAIN groups;
-randperm seed+278000+epoch;
-24 pairs/48 rows per batch;
-profile=epoch%3;
-800 updates/200 epochs;
-each TRAIN row200 exposures;
-profile updates268/268/264;
-fit RNG seed+279000;
-mean CE only;
-AdamW lr0.005,betas.9/.999,eps1e-8,weight_decay0,clip1;
-CPU float64,threads2,deterministic.

Evaluation:
1.original C267 two-character task;
2.C270 unseen three-character task SHA256
 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Fixed gates remain:
accuracy>=.90;query_pair>=.80;evidence_drop>=.35;query_drop>=.35;two_order>=.80.

Primary PASS iff all five mean_final_dual states pass every original and triple criterion.
mean_span is matched control only and cannot rescue/fail candidate.

Workload:
-models10;
-train_steps8000;
-training_rows384000;
-model_forward_calls9080;
-row_presentations487680;
-core_forward_calls36320;
-one10-state bundle write/load;
-10 strict state loads;
-new_checkpoint_writes1.

Protection/runtime:
-source pins514;
-protected inputs902;
-direct deciding dependencies54;
-own24;
-modules163;
-loaded3838/focused3837;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
791f287f21bcadd6c708496cd6922a2ef82a2ab94d2cf12ab5c3d669e1917dec.
The same seal appears in benchmark and preregistration. C278 own test24 requires current handoff
agreement while ACTIVE,then immutable c278-c279 acceptance addendum after acceptance.
Registration cardinalities are manifest-derived at runtime.

## C278 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 84b562cf8124ea5d5df0cf13bc66c52908745290

Compared C277 acceptance8a9340c5165754080ea729cf013b6015035df824 to review target:
only C278 OWN6 paths differ.

Committed OWN6 blobs:
-source:0aa8d65874f4a021e21d04948ffd0a1d5615248b
-test:2b4fa04bae8e8a595ff65c0ca6922516a24bcb6b
-runner:b6ac1dd52c85873aa845afd2cd073b3f64eff3bb
-launcher:b6f935b0469628f9cd8e45983f2e91bb6798b2d0
-prereg:82180666515009feb53c3c655c222324c127bedd
-design:c2b83e54a170482873d73abeb61191e3c8fab8d1

Static review confirms exactly24 own tests;Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED
before scientific logging;manifest-derived514/902 registration;four parent hashes modeled
independently in source and test fixture;actual C269 SpanQueryReadout control;two separate candidate
softmaxes with shared parameters and post-retrieval averaging;candidate5/5 gate;unique ordered run
phase markers;and lifecycle-aware own seal plus legacy C272 compatibility seal.

No complete user-local runtime is available to reviewer. Therefore own24,focused3837,PowerShell
ParseFile,parent artifact replay and real ten-model training are NOT claimed executed here.
Mode Validate is authoritative.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C278 ->
Mode Validate(parent/source/artifact precheck514/902 + sealed manifest,own24,focused3837) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,both-task evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C278.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without another
fusion tweak inside C278.
C279 stays unregistered until C278 is judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
