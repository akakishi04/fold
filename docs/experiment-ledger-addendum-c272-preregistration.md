# C272 preregistration — paired boundary query

Experiment:C272-v5b-paired-query-boundaries.
Stage:V5-B-PAIRED-QUERY-BOUNDARIES.
Acceptance base:968a77d2a96d28802de38204ef6c45dff99b4ccc.
C271 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C273 NOT REGISTERED.

## One question

With identical paired CE training,does a query representation using BOTH the first and final visible
query-byte pre-core states preserve the trained two-character task while improving transfer to
unseen three-character shared-prefix/shared-suffix identifiers?

## Parent evidence

C271 execution:d1c58db43047aceaf82b0108bace9cd731f13b76.
C271 summary:runs/c271-v5b-query-endpoint-2873a0f5afe04737ab811192ef3caf72/summary.json.
C271 summary SHA256:4720c3d57d69470ec1bd0564e219dcc3bdd28a555dc6c64e4f73e10b5a1ba05b.

Require C271 status FAIL,candidate_gate=False,whole-state pass counts mean_span0/endpoint_span0,
two-character pass counts4/4 and triple pass counts0/0.

Required C271 artifact SHA256:
-architecture-plan.json 9c94e65a1be56896f757b3275dfc24f25e5c933097b31b932a43e3e2059d2be0
-dataset.json 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-trained-models.pt dc521a1a7db84275f283f733c5f5f9ff430e82960181d3fa4f34bdef651a23c7
-evaluations.pt ef875757deb71e0aa2c1b476ec1a0bf4a7772bbf606d4175438b4e2fd6934845
-measurements.json 8c19ca09141c0240ba8271cb698969146de8bb27c136a4c40b90e7dd698218f7
-validation-summary.json e4fd1f4d0a98db134522c8c710e3cadaedfcfe77697c824448124351714610e8

C271 artifacts are provenance only. C272 uses fresh initialization.

## Arms

Fresh seeds272001..272005.

mean_span:
actual C269 SpanQueryReadout. read.query receives the arithmetic mean of every pre-core local state
selected by C269.query_span_mask.

boundary_pair:
same14256 parameters,state_dict keys and exact initial tensor values. read.query receives
0.5*(first_visible_query_byte_state + final_visible_query_byte_state), where both positions come
only from C269.query_span_mask. If first==last,the formula returns that state.

No entity ID,target,profile,split,pair index or other supervision metadata enters model.forward.
Masked pre-core memory,read.query/key/output maps,score divisor4,PAD masking,Full core,post-core EOS
residual,readout_norm and decoder remain unchanged.

## Training

Exact C267 two-character dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

TRAIN192/HOLDOUT96. Use96 same-facts/different-query TRAIN pairs.
For seed and epoch:randperm96 seed+272000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.
800 updates=200 complete epochs. Each TRAIN row appears200 times per arm.
Profile updates268/268/264.
Fit RNG seed+273000 reset per arm.

Both arms use mean CE only,AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,global clip1.
CPU float64,threads2,deterministic algorithms. No early stop,extra training,seed replacement,
checkpoint selection or HOLDOUT optimization.

## Evaluation and fixed gate

Evaluate both final states on:
1.original C267 two-character task;
2.C270 triple dataset SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged C267/C270 thresholds:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.
HOLDOUT answer cells8 rows require8/8.

Primary PASS iff all FIVE boundary_pair states pass every original and triple criterion.
mean_span is reported separately and cannot rescue/fail candidate.
Report paired correct/collapse contrasts for two-character HOLDOUT and both triple splits.
Pooled metrics are descriptive only.

## Workload and persistence

10 models;8000 updates;384000 training row presentations.
Per model:800 training forwards +54 final evaluation +54 strict replay =908.
Totals9080 model forwards,487680 row presentations,36320 core calls.
One10-state bundle write/load;10 strict state loads;new_checkpoint_writes=1.

Artifacts:
-architecture-plan.json
-dataset.json
-triple-dataset.json
-trained-models.pt
-evaluations.pt
-measurements.json
-validation-summary.json
plus summary.json.

Schemas:
-fold-c272-query-boundaries-models-v1
-fold-c272-query-boundaries-eval-v1.

## Protection/runtime

Expected source pins478;protected inputs826;direct deciding dependencies48.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules157;loaded3694/focused3693.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256:89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
Per docs/experiment-authoring-runtime-gate.md it MUST be computed from final committed benchmark
bytes after all manifest-changing edits,then written identically into benchmark,preregistration and
handoff,and independently rechecked BEFORE C272 becomes ACTIVE.

Use Validate->Execute. Validate must pass parent/source/artifact precheck,own24 and focused3693
before scientific logging begins.

## Stop

A valid candidate miss is ACCEPTED VALID NEGATIVE. Do not retune boundary positions,coefficients,
training length,seeds,data or thresholds after results. Integrity failure retries SAME C272.
No Gate F promotion,production adoption,external corpus,paid API,cleanup,history rewrite or CI change.
