# C271 preregistration — paired query endpoint

Experiment:C271-v5b-paired-query-endpoint.
Stage:V5-B-PAIRED-QUERY-ENDPOINT.
Acceptance base:7d050e672758f97033fa23860af47d7a5d9cf15b.

## One question

Does replacing arithmetic mean query-span pooling with the final visible query-byte pre-core state improve transfer to unseen three-character identifiers while preserving the trained two-character task?

## Parent evidence

C270 valid execution:456deac490990f4c7f4ceb1cdf241f0c606a77de.
C270 summary SHA256:117c55f5498dec1b5e60c2a59fc571eeb485a3f6614f710348e29348e3433d5b.
C269 source summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.

Required C270 artifacts:
-transfer-plan.json 3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-eval-outputs.pt 5e9c2b5c428e0dba4c3de5ecebd5f4e3281092bcb87a52489fdce30664201f43
-measurements.json c0d66450ef2b451103db615f78be900156347f2689a0f01c6e2211062c10ce12
-validation-summary.json 20e26a038db3c4f1f54552f72a197bce587e9ba44500a0b03e918cc6d3c7bc93

Require C270 status FAIL, seed pass counts eos_query0/span_query0, candidate_gate=False. C270 is provenance only; its learned states do not initialize C271.

## Arms and training

Fresh seeds271001..271005.
-mean_span: actual C269 SpanQueryReadout.
-endpoint_span: same14256 parameters/state keys/initial values, but read.query input is the pre-core local state at the last byte in C269.query_span_mask(tokens).

No target/entity/split/profile metadata enters model.forward. Memory,query/key/output maps,attention scale4,PAD mask,Full core,post-core EOS residual,normalization and decoder stay unchanged.

Use exact C267 training dataset SHA256 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Use96 same-facts/different-query pairs; randperm96 seed+271000+epoch;24 pairs/batch; profile=epoch%3. 800 updates=200 epochs; each TRAIN row200 exposures; profile updates268/268/264. Fit RNG seed+272000 reset per arm. Both use CE only,AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global clip1,CPU float64,threads2,deterministic.

## Evaluation and gate

Evaluate both:
- original two-character C267 task;
- C270 triple dataset SHA256 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Use unchanged gates: answer accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80. HOLDOUT cells8 answers therefore require8/8. Endpoint candidate PASS requires all five seeds to pass every original and triple criterion. Control is reported separately.

## Workload

10 models;8000 optimizer updates;384000 training rows.
Per model:800 train forwards +54 final evaluation +54 strict replay =908 forwards.
Total9080 forwards,487680 row presentations,36320 core calls.
One10-state bundle write/load;10 strict state loads.
Artifacts:architecture-plan.json,dataset.json,triple-dataset.json,trained-models.pt,evaluations.pt,measurements.json,validation-summary.json plus summary.json.
Raw final logit payload contract:106168320 bytes.

## Protection/runtime

Expected:472 source pins,812 protected inputs,47 deciding dependencies.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules156;loaded3670/focused3669;sole inherited C204 exact exclusion unchanged.
Manifest SHA256:9c94e65a1be56896f757b3275dfc24f25e5c933097b31b932a43e3e2059d2be0.

Use the Validate->Execute runtime gate from docs/experiment-authoring-runtime-gate.md. Complete own24 and focused3669 must pass before scientific logging begins. C272 NOT REGISTERED.
