# C278 acceptance and C279 saved dual-query failure audit

## Formal verdict

C278 ACCEPTED VALID NEGATIVE. The preregistered mean_final_dual candidate passed0/5 whole-state
gates. The matched mean_span control also passed0/5. Both arms passed5/5 on the original
two-character task and0/5 on the complete unseen three-character task. candidate_gate=False.
Gate F NOT PASSED.

Scientific execution HEAD:ca6e45cc90b3b48e3d56c10acde72e35574878fd.
Published log commit:f74d8b1d340a7c744948b39645a1f4d30f1ea524.
Publisher log SHA256:c3aed185a8381db1ff9d970a2e3edbc5750080a00f9c52fe8678032b62593ffd.
Publisher log bytes:844793.
Summary:runs/c278-v5b-mean-final-dual-c1d5206c6c6a48ab98acd15c5cb8aa71/summary.json.
Summary SHA256:557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b.

## Execution validity

The pre-science runtime gate passed before science: parent/source/artifact precheck514/902,
sealed manifest791f287f21bcadd6c708496cd6922a2ef82a2ab94d2cf12ab5c3d669e1917dec,
own24 PASS and focused3837 PASS. Ten fresh matched models completed800 updates each.
Total8000 optimizer updates,384000 training rows,9080 model forwards,487680 row presentations and
36320 core calls. One10-state bundle write/load and10 strict state loads completed.
all_pairs_matched=True;all_replays=True. Persisted reconstruction passed;tracked tree and execution
HEAD were preserved. run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.

## Deciding metrics

Whole-state pass counts:
-mean_span:0/5;
-mean_final_dual:0/5.

Original two-character subgate:
-mean_span:5/5;
-mean_final_dual:5/5.

Unseen three-character subgate:
-mean_span:0/5;
-mean_final_dual:0/5.

Aggregate three-character answers across TRAIN+HOLDOUT:
-mean_span:3938/4320 correct;314 collapsed pairs;
-mean_final_dual:4207/4320 correct;95 collapsed pairs.

Primary profile contrasts:

|split/profile|mean_span correct|mean_final_dual correct|mean_span collapse|mean_final_dual collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|958/960|960/960|1|0|
|TRAIN shared_prefix2|813/960|958/960|145|2|
|TRAIN shared_suffix2|872/960|895/960|74|61|
|HOLDOUT tripled|478/480|480/480|1|0|
|HOLDOUT shared_prefix2|401/480|476/480|63|3|
|HOLDOUT shared_suffix2|416/480|438/480|30|29|

Per-seed aggregate three-character correct/collapse:
-278001: control831/864,25 collapse;candidate863/864,0 collapse.
-278002: control793/864,56 collapse;candidate857/864,3 collapse.
-278003: control787/864,59 collapse;candidate827/864,26 collapse.
-278004: control740/864,100 collapse;candidate807/864,55 collapse.
-278005: control787/864,74 collapse;candidate853/864,11 collapse.

## Scientific interpretation

Separating the mean visible query-span and final visible query-boundary through independent attention
softmaxes is a substantial improvement over mean-span attention for shared_prefix2 and reduces
aggregate collapse strongly. The intervention is therefore not inert.

However,the candidate remains0/5 on the complete three-character task. shared_suffix2 improves only
modestly in aggregate and remains heterogeneous across seeds. The current evidence therefore points
to a residual criterion/profile-specific failure rather than a global inability to train the dual
readout.

Before another fusion rule,extra parameter path or optimizer change is introduced,the exact fixed
criterion failures should be attributed from the persisted C278 measurements.

## Non-claims

Do not claim mean_final_dual solves three-character binding because pooled accuracy rises sharply.
Do not tune the averaging weight,add another query branch,change lr,extend training,replace seeds or
relax fixed gates inside C278. Do not promote Gate F.

## Accepted artifacts

-architecture-plan.json:791f287f21bcadd6c708496cd6922a2ef82a2ab94d2cf12ab5c3d669e1917dec;2855 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-trained-models.pt:a86f34ed93dd8b3d0f2e46e960f134571223f2146b31763202b4f11b778f52d5;1238007 bytes.
-evaluations.pt:1ee106c701ee4ca6048c6bc9200bee343f57a7cfe88d2c201aa920ada8c2bfdc;106277991 bytes.
-measurements.json:ae12d78b16787622efc62206775a7ec7e9e021a8085b7c42a8bea8efbb90e24f;524977 bytes.
-validation-summary.json:01a2dd82e73cfcc06feffa14b0edb5c5f2df7af0f0366f5b0cc3142e3862678c;22946 bytes.

## Next question, not activation

For accepted C278 saved outputs,which fixed gate criteria remain responsible for the
mean_final_dual three-character failures by seed,split and profile,and is the residual failure
specifically concentrated in shared_suffix2 mask sensitivity/two-order behavior rather than direct
answer discrimination?

C279 should be saved-output diagnostic only with zero training and zero model forwards.
Verify/reconstruct accepted C278 artifacts with Module calls blocked,then attribute every failed
answer-cell and two-order criterion for both arms. Primary views should include all triple failures,
shared_prefix2 HOLDOUT,shared_suffix2 TRAIN/HOLDOUT and per-seed triple deltas. Formal PASS means
audit integrity only,not capability success. Gate F remains NOT PASSED.

C279 requires separate preregistration,implementation,final manifest sealing,committed-byte review
and runtime Validate. C280 NOT REGISTERED.
