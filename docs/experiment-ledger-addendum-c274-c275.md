# C274 acceptance and C275 saved gate-failure audit

## Formal verdict

C274 ACCEPTED PASS for diagnostic integrity only. This is NOT a capability PASS and does not promote
Gate F. The registered first_boundary/final_boundary directional diagnostic completed exactly as
preregistered. No capability winner was preregistered or selected.

Scientific execution HEAD:90f76a8f017d562caded127821852654b8e3d061.
Published log commit:acb1236f5299052662525deec2b00f0bb415338b.
Publisher log SHA256:571e51b5b4785872ef83298410dbbabdfce8a09ab4e1b396339b4c0e8710ec0b.
Publisher log bytes:845983.
Git normalized log blob:5195705b709b682b7a19b407edf07642750ffa1a.
Summary:runs/c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178/summary.json.
Summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

## Execution validity

The pre-science runtime gate passed before science:parent/source/artifact precheck490/854,
sealed manifest a288c48c3b9282be070f12fdc567d8c8e09bbed8003a6321792ce517a5c255e7,
own24 PASS and focused3741 PASS. Ten fresh matched states completed800 updates each.
Total8000 optimizer updates,384000 training rows,9080 model forwards,487680 row presentations and
36320 core calls. One10-state bundle write/load and10 strict state loads completed.
all_pairs_matched=True;all_replays=True. Persisted directional metric reconstruction passed;tracked
tree and execution HEAD were preserved. run_execution_valid=True;scientific_status=PASS;
diagnostic_complete=True;capability_gate_applicable=False.

## Directional measurements

Descriptive task pass membership:
-first_boundary: two_char0/5,triple0/5;
-final_boundary: two_char4/5,triple0/5.
These are measurements only and do not define C274 formal PASS.

Aggregate HOLDOUT two-character answers:
-doubled:first395/480,final428/480;collapse44/240 vs26/240;
-shared_prefix:first325/480,final429/480;collapse92/240 vs26/240;
-shared_suffix:first390/480,final422/480;collapse50/240 vs29/240.

Aggregate triple answers:

|split/profile|First correct|Final correct|First collapse|Final collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|912/960|937/960|46/480|19/480|
|TRAIN shared_prefix2|797/960|942/960|150/480|18/480|
|TRAIN shared_suffix2|818/960|889/960|130/480|68/480|
|HOLDOUT tripled|392/480|432/480|47/240|26/240|
|HOLDOUT shared_prefix2|314/480|426/480|92/240|22/240|
|HOLDOUT shared_suffix2|360/480|409/480|78/240|34/240|

The final boundary is therefore substantially stronger in this cohort not only on shared-prefix names
but also on shared-suffix names. This weakens the earlier simple hypothesis that first and final
boundaries provide symmetric complementary evidence.

Per-seed final_boundary HOLDOUT:
-274001 two-char288/288;triple280/288;
-274002 two-char288/288;triple284/288;
-274003 two-char127/288;triple134/288;
-274004 two-char288/288;triple281/288;
-274005 two-char288/288;triple288/288.

Seed274003 is a broad optimization/reliability miss. The other four final-boundary states retain the
two-character task perfectly and have near-perfect triple HOLDOUT answer totals, yet none receives a
complete triple task PASS. Therefore the next question should identify WHICH fixed cell/gate
components reject these near-passing states before another architecture change is introduced.

## Scientific interpretation

C274 does not support treating the first visible byte state as a useful standalone complement to the
final state. Because the local encoder is causal,the final boundary state can already encode preceding
query bytes,which is consistent with its broad advantage. However,pooled answer totals alone cannot
explain why all final-boundary triple states fail the complete fixed gate.

The unresolved distinction is now between normal-answer discrimination and the auxiliary fixed
criteria:paired-query correctness,evidence/query mask drops,and two-order consistency. Those details
exist in the persisted C274 measurements and should be audited directly rather than inferred.

## Non-claims

Do not declare final_boundary a capability winner from C274. C274 was explicitly diagnostic-only.
Do not ignore seed274003 or infer that four near-perfect seeds constitute a capability PASS. Do not
retune training length,seeds,thresholds or query construction from pooled totals alone.

## Accepted artifacts

-architecture-plan.json:a288c48c3b9282be070f12fdc567d8c8e09bbed8003a6321792ce517a5c255e7;2893 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-trained-models.pt:3a8cf72756e1112341bf8ad88e45ad124f876a608586d3dc4955cd11a16c1231;1238071 bytes.
-evaluations.pt:ca1124810acd5f7d86ec614a900fbe5dbd3f37278005266616e666ce8e4ebf25;106277991 bytes.
-measurements.json:dcbddf4c4f614e8c8b224ecba4b656a5109e5dab0de1d4a2bde8ddae0858ecca;524055 bytes.
-validation-summary.json:79d1ef4ee89f067977dd1704f4c0424453018dc5c989e3afe2d7f935cb5ef2f9;35751 bytes.

## Next question, not activation

For the saved C274 states,which exact fixed gate components cause final_boundary to fail the
three-character task despite near-perfect pooled answers in four seeds,and are those failures
concentrated in answer/pair discrimination,mask-drop criteria,or two-order consistency?

C275 should be a saved-output diagnostic only:load and independently reconstruct the accepted C274
measurements with neural Module calls blocked;perform no training,no inference and no new checkpoint.
Audit every failed cell/two-order record for both arms,with a primary focus on final_boundary triple
failures. Record criterion-specific negative margins to the existing thresholds and counts by
seed/split/profile/language/subset/order. Explicitly distinguish seed274003's broad failure from
near-pass failures in274001/274002/274004/274005.

Formal C275 PASS means diagnostic execution/integrity only,not capability success. Gate F remains
NOT PASSED. C275 requires separate preregistration,implementation,final manifest sealing,committed
byte review and runtime Validate. C276 NOT REGISTERED.
