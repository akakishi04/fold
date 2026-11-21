# C271 acceptance and C272 boundary-query boundary

## Formal verdict

C271 ACCEPTED VALID NEGATIVE. The preregistered endpoint_span candidate passed0/5 whole-state gates,
and the matched mean_span control also passed0/5. Both architectures passed4/5 on the original
two-character task and0/5 on the unseen three-character task. The fixed five-seed candidate gate
therefore fails. Gate F NOT PASSED. No production architecture/default change follows automatically.

Scientific execution HEAD:d1c58db43047aceaf82b0108bace9cd731f13b76.
Published log commit:de79ff4539e37a7fddff31ff91dc2b40ff77f0c2.
Publisher log SHA256:b870129e8c494c78bdcf8550dd27d0b3a214561361ddbad56be92e5597027aaa.
Publisher log bytes:825500.
Git normalized log blob:2b9dab34e766b776612901e2644089603660e7bd.
Summary:runs/c271-v5b-query-endpoint-2873a0f5afe04737ab811192ef3caf72/summary.json.
Summary SHA256:4720c3d57d69470ec1bd0564e219dcc3bdd28a555dc6c64e4f73e10b5a1ba05b.

## Execution validity

The pre-science runtime gate passed before science:parent/source/artifact precheck472/812,own24 and
focused3669 all PASS. Ten fresh matched models completed800 updates each. Total8000 optimizer
updates,384000 training rows,9080 model forwards,487680 row presentations and36320 core calls.
One10-state bundle write/load and10 strict state loads completed. all_pairs_matched=True;
all_replays=True. Persisted query-endpoint reconstruction passed;tracked tree and execution HEAD
were preserved. run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.

## Deciding metrics

Whole-state pass counts:
-mean_span:0/5;
-endpoint_span:0/5.

Original two-character subgate:
-mean_span4/5;
-endpoint_span4/5.

Unseen three-character subgate:
-mean_span0/5;
-endpoint_span0/5.

Aggregate HOLDOUT two-character answers:
-doubled:mean469/480,endpoint446/480; collapse8/240 vs16/240;
-shared_prefix:mean467/480,endpoint442/480; collapse9/240 vs16/240;
-shared_suffix:mean468/480,endpoint418/480; collapse9/240 vs35/240.

Aggregate three-character answers:

|split/profile|Mean correct|Endpoint correct|Mean collapse|Endpoint collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|943/960|927/960|13/480|29/480|
|TRAIN shared_prefix2|792/960|929/960|150/480|29/480|
|TRAIN shared_suffix2|835/960|822/960|64/480|127/480|
|HOLDOUT tripled|467/480|444/480|8/240|16/240|
|HOLDOUT shared_prefix2|367/480|439/480|65/240|16/240|
|HOLDOUT shared_suffix2|402/480|390/480|31/240|56/240|

Endpoint state sharply improves shared-prefix3-character binding, but degrades shared-suffix and
the trained two-character family. The two representations therefore exhibit complementary
strengths rather than a uniformly superior endpoint architecture.

Per-seed endpoint HOLDOUT two-character /288:
271001=288,271002=154,271003=288,271004=288,271005=288.
Per-seed endpoint HOLDOUT triple /288:
271001=282,271002=156,271003=287,271004=279,271005=269.
Seed271002 is a broad optimization/reliability miss; other endpoint seeds still fail the fixed
triple gate despite high pooled accuracy.

## Scientific interpretation

The final visible query-byte state preserves distinctions that arithmetic mean pooling dilutes when
identifiers share their prefix, but it overweights recent/suffix information and loses robustness
when identifiers share their suffix. This complementary pattern supports testing a representation
that exposes BOTH boundaries of the visible query rather than choosing only mean or endpoint.

This is still a hypothesis about the input representation, not a proven internal mechanism.
The endpoint local state is causal and may encode the whole preceding query, but the observed
suffix-sharing degradation shows that this encoding is not sufficient for the fixed gate.

## Non-claims

Do not claim that endpoint query is globally worse or mean pooling globally better. C271 uses a
small authored symbolic family and fresh five-seed cohort. Two-character and three-character names
share the same byte vocabulary, but arbitrary strings and natural language are out of scope.
Pooled improvements on shared_prefix2 cannot rescue the0/5 preregistered candidate result.
Do not tune seed271002,steps,thresholds or data after this result.

## Accepted artifacts

-architecture-plan.json:9c94e65a1be56896f757b3275dfc24f25e5c933097b31b932a43e3e2059d2be0;2836 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-trained-models.pt:dc521a1a7db84275f283f733c5f5f9ff430e82960181d3fa4f34bdef651a23c7;1238007 bytes.
-evaluations.pt:ef875757deb71e0aa2c1b476ec1a0bf4a7772bbf606d4175438b4e2fd6934845;106277991 bytes.
-measurements.json:8c19ca09141c0240ba8271cb698969146de8bb27c136a4c40b90e7dd698218f7;525083 bytes.
-validation-summary.json:e4fd1f4d0a98db134522c8c710e3cadaedfcfe77697c824448124351714610e8;22968 bytes.

## Next question, not activation

Does a fixed boundary-pair query representation, using both the FIRST and FINAL visible query-byte
pre-core states, preserve the trained two-character task while improving unseen three-character
shared-prefix/shared-suffix transfer?

C272 candidate should compute read.query input as the arithmetic mean of the first and final
positions selected by C269.query_span_mask(tokens). This adds no parameters and treats the two
query boundaries symmetrically:
-boundary information at the first byte can distinguish shared-suffix names;
-boundary information at the last byte can distinguish shared-prefix names.

Use fresh matched seeds and the exact C271 paired CE training policy. Compare boundary_pair against
the accepted mean_span architecture from identical initial tensors. Evaluate both original
two-character and C270 three-character tasks. Candidate PASS requires all five boundary_pair states
to pass BOTH fixed tasks. This is a bounded structural test, not a general parser claim.
C272 requires separate preregistration,implementation,committed-byte review and runtime Validate.
C273 NOT REGISTERED.
