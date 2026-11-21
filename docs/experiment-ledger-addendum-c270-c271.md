# C270 acceptance and C271 endpoint-query boundary

## Formal verdict

C270 ACCEPTED VALID NEGATIVE. The preregistered frozen span_query candidate passed0/5 states on the
unseen three-character identifier task; the frozen eos_query reference also passed0/5. The recovered
runtime-gated execution is valid and supersedes the earlier INVALID own-test attempt for scientific
judgment only. C269 remains ACCEPTED PASS in its bounded trained-name/held-value scope.
Gate F NOT PASSED. No production architecture change follows automatically.

Scientific execution HEAD:456deac490990f4c7f4ceb1cdf241f0c606a77de.
Published log commit:e3670602568ad402d49108e6529dd4b728c2e6e8.
Publisher log SHA256:048c33bee11198f3507623024573815a795eefbfc0fef854e39338f23627f329.
Publisher log bytes:1103435.
Git normalized log blob:ea0f586da1c7da35ffbb610deb763f2bc91b4870.
Summary:runs/c270-v5b-triple-identifiers-87c6c92aaa194dada7aae2b420dba776/summary.json.
Summary SHA256:117c55f5498dec1b5e60c2a59fc571eeb485a3f6614f710348e29348e3433d5b.

## Execution validity

The new pre-science runtime gate operated as intended. Validate completed before scientific logging:
parent/source/artifact precheck466/800 PASS,own24 PASS and focused3645 PASS. Only then did Execute
begin. All ten frozen C269 states were strict-loaded and evaluated;no training or new checkpoint was
performed.810 wrapper forwards,77760 row presentations and3240 core calls completed. One accepted
bundle load,10 strict state loads. all_replays=True;all_weights_preserved=True. Persisted triple-name
score reconstruction passed;tracked tree and execution HEAD were preserved.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.

The prior attempt at11ae165db9dbb73239360a20c9c7cf005cd9c19f with log commit
9d5fca7390b767cc39c001792e9e478f43e8f96e remains INVALID history because it stopped in authoring
test23 before regression/model evaluation. It is not combined with the valid run.

## Deciding metrics

Whole-state pass counts:eos_query0/5;span_query0/5.

Aggregate correct/collapse counts:

|split/profile|EOS correct|Span correct|EOS collapse|Span collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|960/960|960/960|0/480|0/480|
|TRAIN shared_prefix2|960/960|793/960|0/480|167/480|
|TRAIN shared_suffix2|879/960|906/960|79/480|43/480|
|HOLDOUT tripled|427/480|480/480|10/240|0/240|
|HOLDOUT shared_prefix2|425/480|381/480|10/240|76/240|
|HOLDOUT shared_suffix2|392/480|446/480|49/240|17/240|

Span_query therefore generalizes perfectly to the simple tripled names but fails the fixed gate on
both shared-character three-letter constructions. The most severe candidate failure is
shared_prefix2:793/960 on TRAIN-value rows and381/480 on HOLDOUT-value rows,with substantial
same-answer collapse. This occurs even when the underlying value pair was seen during C269 training,
so it is not only a held-value problem.

Per-seed candidate HOLDOUT correct /288:
269001=261,269002=258,269003=268,269004=267,269005=253.
Every candidate state therefore misses the fixed all-cell gate despite relatively high pooled
accuracy. No pooled score rescues the 0/5 preregistered result.

## Scientific interpretation

The C269 mean-pooled visible query span solves the trained two-character naming family robustly but
does not extrapolate reliably to these unseen three-character shared-prefix/suffix strings.
The perfect tripled profile shows that identifier length3 by itself is not sufficient to cause the
failure. The sharp shared_prefix2 degradation is consistent with a composition/dilution weakness:
uuu and uuv share two of three visible query characters,so arithmetic mean pooling makes most of
their query-source contribution identical. This is a hypothesis for the next controlled test,not a
claim that this is the learned internal mechanism.

C270 does not revoke C269. C269 established held-VALUE transfer for TRAIN-seen two-character naming
profiles. C270 asks a different frozen distribution-shift question and validly fails it.

## Non-claims

Do not claim arbitrary-name generalization,ordinary language failure,or that mean pooling is
universally wrong. Name length and composition changed together,all tasks are hand-authored symbolic
formats,and the same familiar byte vocabulary is reused. The eos reference also fails0/5,so C270
does not identify a globally superior baseline. No training extension or post-result profile tuning
is authorized.

## Accepted artifacts

-transfer-plan.json:3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016;2262 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-eval-outputs.pt:5e9c2b5c428e0dba4c3de5ecebd5f4e3281092bcb87a52489fdce30664201f43;159406577 bytes.
-measurements.json:c0d66450ef2b451103db615f78be900156347f2689a0f01c6e2211062c10ce12;263003 bytes.
-validation-summary.json:20e26a038db3c4f1f54552f72a197bce587e9ba44500a0b03e918cc6d3c7bc93;14233 bytes.

## Next question, not activation

Does replacing arithmetic mean query-span pooling with the FINAL visible query-byte pre-core state
improve transfer to unseen three-character identifiers while preserving the trained two-character
task?

Use fresh matched seeds and ordinary paired CE training on the exact C267 two-character dataset.
Compare:
-mean_span:the accepted C269 span_query architecture;
-endpoint_span:the same14256-parameter architecture,but read.query receives the pre-core local state
 at the last visible query byte (immediately before the final '=').

The local encoder is causal,so the endpoint state has access to all prior bytes of the query string
without averaging away the position at which similar identifiers diverge. This is the scientific
motivation;do not assert that it will solve the task in advance.

Both arms must use identical initial tensors,batches,optimizer,800-update budget and CE objective.
Evaluate both on the original two-character C267 task and the frozen C270 three-character task.
Primary candidate PASS should require all five endpoint_span seeds to preserve every original
two-character criterion AND pass every three-character TRAIN/HOLDOUT/profile criterion. mean_span
is a matched control and cannot rescue the candidate. C271 requires separate preregistration,
implementation,committed-byte review and runtime Validate gate. C272 NOT REGISTERED.
