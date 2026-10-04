# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C299 ACCEPTED PASS (diagnostic integrity only). C300 ACTIVE / NOT YET JUDGED. C301 NOT REGISTERED.**
C298/C297 remain diagnostic PASS;C296 remains ACCEPTED VALID NEGATIVE.
C300 is the unique ACTIVE frozen inference diagnostic. No new training is authorized in C300.
Latest accepted scientific execution:1ef1436febee7b2a70b2b91cb7a5dcb2a9e04d0c.
Latest accepted published log:e1013d119956a3be000667ce6ac468d7eabb8cdf. Do not rerun C299.

## Latest accepted evidence — C299

Acceptance:docs/experiment-ledger-addendum-c299-c300.md.
Acceptance commit:c726cc8d1c587328943229276d6588fb59386a06.
Summary:runs/c299-v5b-core-grid-d118c6d85dfa47dbaac6ce40655b2fe6/summary.json.
Summary SHA256:d0b2c055e190a313e5abc399716e2ec0cddfb104cc447a6216f2fab0ed312851.
Own32/focused4557 PASS;source640/protected1176;run_execution_valid=True.
Manifest796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846.
All3 same-source diagonals reproduce C298 with exact initial/final hashes,800 losses and max logit error0.0.
Quad remaining x core:[[T,F,F],[F,F,F],[T,F,T]] (3/9).
Two/three:[[T,F,F],[T,T,T],[T,T,T]] (7/9 each).
Remaining297001/core297002 and remaining297001/core297003 fail seen-length TRAIN and HOLDOUT.
Their normal quad errors are198 and152;the original297001/297001 has0. Remaining297002 remains
quad-failing with every tested core (2/2/19 errors);remaining297003 has0/1/0 errors.
Same core may work in one combination and fail in another. No universal donor,unique cause,
population-variance claim,core necessity or deployment policy is established by this fixed grid.

## Active C300 — frozen pre-normalization readout-term diagnostic

Experiment:C300-v5b-frozen-readout-term-ablation. Stage:V5-B-FROZEN-READOUT-TERM-ABLATION.
Registration:docs/experiment-ledger-addendum-c300-preregistration.md.
Design:docs/v5b-frozen-readout-terms-v0.1.md.
Review:docs/c300-post-authoring-review.md.
Acceptance base:c726cc8d1c587328943229276d6588fb59386a06.
Authoring/review target:49227f1eb5b795553723d5e4188084d16b39dce3.

One question:which existing C299 predictions are rescued or lost when either summand of the final
pre-normalization readout input is suppressed? Keep all9 learned states,including every failure.
This stops initialization subdivision and instead tests frozen inference-time contributions.
No new learning,weight recombination,chosen-seed cohort,output filtering or per-query best-of.

Exact C278 sum:r+a,where r is post-core next-route EOS residual and a is read.output of the averaged
mean-span/final-boundary memory. The latter is the added reader,not the final vocabulary classifier.
All upstream computations still execute in every condition;normalizer/classifier stay unchanged.
Fixed four-pass order per model:full_before(r+a),residual_only(r),reader_only(a),full_after(r+a).
Suppressing r does NOT remove core computation;no speed/necessity/disposability claim follows.
Layer normalization and distribution changes mean this is not additive attribution of final logits.

Only temporary instance hooks intervene. Capture r before C278's dynamic norm hook and a at
read.output;install the late replacement hook during local_encoder after the original hook exists.
On EVERY model call require actual normalizer input exactly equals captured r+a,correct batch-by16
shape,CPUfloat64/finite values and one complete capture. Full modes do not replace the input.
Require frozen eval/no_grad,cleanup on success and exceptions,and original hook-registry restoration.
The accepted C278 source and its provenance assertions are unchanged and remain in the path.

Strict-load each final C299 state once and require its exact fingerprint. Full_before/full_after
must reproduce every old raw logit within1e-9 with exact argmax across all3 tasks,profiles,splits
and normal/evidence-blind/query-blind views. Compare before versus after too. Weights and hooks
must remain unchanged after every pass. Any mismatch invalidates C300,not the parent result.

Report36 model/mode results,216 final partitions,108 ablation-vs-normal comparisons(46656 matched
normal rows),9 reproduction receipts,and4 sets of task matrices. Report rescued and regressed
answers separately;wrong-to-wrong prediction changes are not rescues. All old gates are retained:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Ablated gates are descriptive.
PASS means diagnostic completeness/intervention fidelity/restoration/reconstruction ONLY. No old
verdict change,Gate F promotion or branch-selection deployment. Outcomes do not prove training causes.

## Parent contract,protection and workload

Verify26 ordered summary hashes BEFORE exact C299.verify_artifacts with25 ancestors and accepted
execution HEAD. Tail hashes use immutable C299.parent_hashes(C298). Require the exact complete
parent matrices,diagnostic PASS,components_matched/all_replays and all8 output descriptors sealed
by its summary hash. Recheck canonical data JSON hashes. Anchors are final raw outputs in
fold-c299-core-eval-v1,not pre-update losses. Use C299.load_bundle on fold-c299-core-models-v1
and preserve all9 ordered learned states. C299.make_grid creates only compatible model instances.

Sole direct import C299;context exposes C294 no-neural,C287 normalization,C284 evaluation/replay,
C283 quad,C282 tables and the actual model/core modules. Retain640 inherited source pins/1176 inputs
and repository-local helper coverage;explicitly pin C278 readout blob0aa8d65874f4a021e21d04948ffd0a1d5615248b.
Add OWN6 and9 parent files:source646/protected1191. No accepted source/test/log/dispatcher edits.

Science:9 models,training0,2916 forwards,279936 row presentations,11664 core calls,9 model-state
loads,one existing checkpoint-bundle read,new checkpoints0,network0. All earlier computation still
runs,even for suppressed terms. This is not zero-inference saved-result analysis. Operational
smoke(5 real forwards),tests and old-artifact reconstruction are outside these scientific counts.
Outputs:intervention-plan.json,intervention-evaluations.pt,measurements.json,validation-summary.json,
plus summary.json. No new dataset copies or trained-models.pt. Archive fold-c300-readout-terms-eval-v1
keeps all4 raw passes,weights/hooks attestations and reproduction errors. Raw logits573308928 bytes
before overhead. Full tensors/maps local/ignored;compact receipt and aggregates in console.
Numerical postcheck rebuilds scores and reproduction from saved tensors under no-neural scope.
Own40/modules185/loaded4598/focused4597;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static review plus executed local behavioral tests).
All6 OWN files re-fetched at49227f1eb5b795553723d5e4188084d16b39dce3 and matched to local Git blobs6/6.
After all matches:normal own40 PASS in3.704s;whole-suite CP932-emulated own40 PASS in3.812s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;both Python files and3 embedded blocks compile;custom globals0;
UTF-8/no-NUL;manifest recomputation matches. Actual accepted C278 class AST executed with fixture
backbone/reader verifies dynamic hook order and restoration;it is not actual FOLD backbone testing.
Local C278 support file is a fetched class slice,not a clone of the whole parent module,and is
not committed. Test40 on the user checkout extracts the class from the full accepted source.
Other fixtures exercise exact interventions,exception cleanup,counted4*81 inference,cohort/scoring,
26hash failures,protection,run order,archive roundtrip and tampering. No actual capability claims.

Parent archives,Git,legacy scorers/models and suite members are mocked where needed. These tests
are NOT the actual4597-test suite or real C299 checkpoint inference. CP932 emulation covers text
decoding,not Windows itself. Mandatory Windows Validate still requires26 real parent archives,
byte protection,actual frozen checkpoint/hook smoke,PowerShell parsing,own40 and focused4597.
Activation must preserve all6 reviewed OWN blobs and every accepted file/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C300 -> Validate(26parents,646/1191
protection,real frozen checkpoint+hook smoke,own40,focused4597) -> authoring_runtime_preflight=PASS
-> Execute(all9 learned models,full_before/residual_only/reader_only/full_after,old-output reproduction,
unchanged weights/hooks,numerical saved reconstruction) -> log publication.
Validate failure skips science/publication. Any identity,restoration,state,hook or integrity error
repairs SAME C300. Do not change cohort,mode order,thresholds or select successful branches/cells.
C301 remains unregistered until C300 formal judgment. Gate F NOT PASSED.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c299-pre-acceptance.md.
Git blob:a21cc63b792e937df0c703f46ec017c678024eb3. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
