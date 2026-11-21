# C272 acceptance and C273 dual-boundary-attention boundary

## Formal verdict

C272 ACCEPTED VALID NEGATIVE. The preregistered boundary_pair candidate passed0/5 whole-state gates;
the matched mean_span control also passed0/5. Both passed4/5 on the original two-character task and
0/5 on the unseen three-character task. Candidate pooled metrics improve materially over mean_span
in several conditions, but the fixed all-five candidate gate remains false. Gate F NOT PASSED.

Scientific execution HEAD:8142385889335b778f49963bb4b55570165aeb26.
Published log commit:d0fe2095579280a1d12789bfae96cd7924a00956.
Publisher log SHA256:bcbdf90293df8e0ad464838dc2e857c289e59db5aa53812afef25888cb5112bf.
Publisher log bytes:832017.
Git normalized log blob:c2ff7115ae31aa43992c96184a8586be03ce2c04.
Summary:runs/c272-v5b-query-boundaries-db1ee90fff94483191730b4a6e711da6/summary.json.
Summary SHA256:0955fb7f6af7400aa08799a1f369f9acc7f6730a9401478c4283401d89693f12.

## Execution validity

The runtime Validate gate passed before scientific execution:parent/source/artifact precheck478/826,
sealed manifest89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604,
own24 PASS and focused3693 PASS. Ten fresh matched models completed800 updates each.
Total8000 optimizer updates,384000 training rows,9080 model forwards,487680 row presentations and
36320 core calls. One10-state bundle write/load and10 strict state loads completed.
all_pairs_matched=True;all_replays=True. Persisted query-boundary reconstruction passed;tracked tree
and execution HEAD were preserved. run_execution_valid=True;scientific_status=FAIL;
candidate_gate=False.

The earlier C272 preflight failures are operational history only;no science was executed/published
for those attempts and they are not combined with this result.

## Deciding metrics

Whole-state pass counts:
-mean_span:0/5;
-boundary_pair:0/5.

Original two-character subgate:
-mean_span4/5;
-boundary_pair4/5.

Unseen three-character subgate:
-mean_span0/5;
-boundary_pair0/5.

Aggregate HOLDOUT two-character answers:
-doubled:mean395/480,boundary422/480;collapse38/240 vs6/240;
-shared_prefix:mean397/480,boundary423/480;collapse36/240 vs6/240;
-shared_suffix:mean401/480,boundary419/480;collapse31/240 vs10/240.

Aggregate three-character answers:

|split/profile|Mean correct|Boundary correct|Mean collapse|Boundary collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|930/960|956/960|22/480|4/480|
|TRAIN shared_prefix2|805/960|955/960|148/480|5/480|
|TRAIN shared_suffix2|900/960|896/960|49/480|58/480|
|HOLDOUT tripled|395/480|426/480|39/240|6/240|
|HOLDOUT shared_prefix2|317/480|426/480|90/240|7/240|
|HOLDOUT shared_suffix2|376/480|387/480|42/240|32/240|

Boundary_pair therefore preserves the strong shared-prefix benefit of C271 endpoint query while
recovering much of the two-character loss and slightly improving shared-suffix HOLDOUT versus the
mean control. It still misses the strict triple gate,especially shared_suffix2,and does not remove
fresh-seed instability.

Per-seed boundary_pair HOLDOUT:
-272001 two-char288/288;triple266/288;
-272002 two-char288/288;triple284/288;
-272003 two-char288/288;triple283/288;
-272004 two-char288/288;triple284/288;
-272005 two-char112/288;triple122/288.

Seed272005 is a broad optimization/reliability miss. The other four candidate states preserve the
two-character task perfectly but still miss at least one triple cell,so the scientific negative is
not solely an artifact of the bad seed.

## Scientific interpretation

Averaging first+last query states before the attention softmax is substantially more balanced than
using only the endpoint state, but it still compresses two potentially complementary boundary
signals into one query vector before memory selection. The remaining shared-suffix errors motivate
testing whether the two boundaries should produce separate attention distributions instead of being
averaged before attention.

This is a structural hypothesis, not a claim about the learned internal mechanism. The observed
pattern is compatible with pre-softmax interference, but C272 does not prove it.

## Non-claims

Do not claim boundary_pair is generally superior,that seed272005 is ignorable,or that four good seeds
constitute a PASS. Do not retune boundary weights,seed set,training length,data or thresholds after
the result. Arbitrary strings,natural language and unbounded identifier lengths remain out of scope.

## Accepted artifacts

-architecture-plan.json:89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604;2941 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-trained-models.pt:fe3c2d665463a08278931fbcf8b86badcacffa2147f3ac84bffcea81f28e1dc5;1238007 bytes.
-evaluations.pt:84857eeb894a19b3b7f8d48075329b541ef31a32f93ec15819ab4ebd7efa1d82;106277991 bytes.
-measurements.json:fe9230c4eaa785dcd9eaa9f4803511bffbfaba8a3659496dc704b79485e6a8bd;525281 bytes.
-validation-summary.json:48d3ce50567fb3e58345aee73c4a942d820926cec524b1af332bd503056036ef;22976 bytes.

## Next question, not activation

Does keeping FIRST and FINAL query-boundary signals separate through attention,then averaging the
two retrieved memories,improve reliable two/three-character binding relative to averaging the two
boundary states before attention?

Candidate dual_boundary reuses the exact same read.query/read.key/read.output parameters twice:
q_first=query(first_state),q_last=query(last_state);each produces its own masked softmax over the same
pre-core memory;candidate memory=0.5*(read_first+read_last);read.output is applied once to that average.
No parameter is added. For one-byte query_blind input the two attentions are identical.

Compare against the C272 boundary_pair architecture from matched fresh initial tensors using the
same paired CE-only policy,original two-character task and C270 triple task. Candidate PASS requires
all five dual_boundary states to pass BOTH fixed tasks. This directly tests whether pre-softmax
boundary averaging is the remaining bottleneck. C273 requires separate preregistration,
implementation,final manifest sealing,committed-byte review and runtime Validate. C274 NOT REGISTERED.
