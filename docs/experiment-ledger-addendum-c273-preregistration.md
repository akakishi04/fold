# C273 preregistration — paired dual-boundary attention

Experiment:C273-v5b-paired-dual-boundary-attention.
Stage:V5-B-PAIRED-DUAL-BOUNDARY-ATTENTION.
Acceptance base:ced412ce712fae1d3de1fdfdb2b12cc0ef41f3f5.
C272 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C274 NOT REGISTERED.

## One scientific question

Does keeping FIRST and FINAL visible query-boundary signals separate through their attention
softmaxes,then averaging the two retrieved memories,improve reliable two/three-character binding
relative to averaging the two boundary states before attention?

## Parent evidence

C272 execution:8142385889335b778f49963bb4b55570165aeb26.
C272 summary:runs/c272-v5b-query-boundaries-db1ee90fff94483191730b4a6e711da6/summary.json.
C272 summary SHA256:0955fb7f6af7400aa08799a1f369f9acc7f6730a9401478c4283401d89693f12.

Require C272 status FAIL,candidate_gate=False,whole-state pass counts
mean_span0/boundary_pair0,two-character pass counts4/4 and triple pass counts0/0.

Required C272 artifact SHA256:
-architecture-plan.json 89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
-dataset.json 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-trained-models.pt fe3c2d665463a08278931fbcf8b86badcacffa2147f3ac84bffcea81f28e1dc5
-evaluations.pt 84857eeb894a19b3b7f8d48075329b541ef31a32f93ec15819ab4ebd7efa1d82
-measurements.json fe9230c4eaa785dcd9eaa9f4803511bffbfaba8a3659496dc704b79485e6a8bd
-validation-summary.json 48d3ce50567fb3e58345aee73c4a942d820926cec524b1af332bd503056036ef

C272 artifacts are provenance only. C273 uses fresh initialization.

## Arms

Fresh seeds273001..273005.

boundary_pair:
actual C272 BoundaryPairReadout. read.query input is
0.5*(first visible query-byte state + final visible query-byte state), then one attention softmax.

dual_boundary:
same14256 parameters,state_dict keys and exact initial values.
Compute q_first=read.query(first_state) and q_last=read.query(last_state) with the SAME query weights.
Compute two score fields against the SAME read.key(memory),two masked softmaxes,and
read_memory=0.5*(memory_first+memory_last). Apply the shared read.output ONCE to that mean memory.
Post-core residual and decoder path remain unchanged.

No target/entity/profile/split/pair metadata enters model.forward. For a one-byte query,
first==last and the two paths are identical.

## Training

Exact C267 two-character dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Use96 same-facts/different-query TRAIN pairs.
For seed/epoch:randperm96 seed+273000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+274000 reset per arm.

Both arms use mean CE only,AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0,global clip1.
CPU float64,threads2,deterministic. No early stop,extra training,seed replacement,checkpoint selection
or HOLDOUT optimization.

## Evaluation and fixed gate

Evaluate both final states on:
1.original C267 two-character task;
2.C270 triple dataset SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged thresholds:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.
HOLDOUT answer cells8 rows require8/8.

Primary PASS iff all FIVE dual_boundary states pass every original and triple criterion.
boundary_pair is a matched control and cannot rescue/fail candidate.
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
-fold-c273-dual-boundary-models-v1
-fold-c273-dual-boundary-eval-v1.

## Protection/runtime

Expected source pins484;protected inputs840;direct deciding dependencies49.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules158;loaded3718/focused3717.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256:fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f.
After all manifest-changing edits,the final committed manifest is resealed and copied identically
into benchmark,preregistration and handoff before activation.

Registration cardinalities have one executable source of truth:manifest().
Use Validate->Execute. Validate must pass parent/source/artifact precheck,own24 and focused3717
before scientific logging begins.

## Stop

A valid candidate miss is ACCEPTED VALID NEGATIVE. Do not retune dual-attention weights,seed set,
training length,data or thresholds after results. Integrity failure retries SAME C273.
No Gate F promotion,production adoption,external corpus,paid API,cleanup,history rewrite or CI change.
