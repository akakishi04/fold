# C276 acceptance and C277 saved optimizer-failure audit

## Formal verdict

C276 ACCEPTED VALID NEGATIVE. The preregistered lr0.0025 candidate passed0/5 whole-state gates.
The matched lr0.005 control also passed0/5. lr0.0025 passed5/5 on the original two-character task
while lr0.005 passed4/5, but both arms passed0/5 on the complete unseen three-character task.
candidate_gate=False. Gate F NOT PASSED.

Scientific execution HEAD:1f1ddd09815cfcd644e90042b83aba085e40e5bb.
Published log commit:d6b1fbb566fdb99d0ca8a2d735cd29c64bcd9114.
Publisher log SHA256:690d0cd0d3a53c0c0db239a29ea4e759083c485c2819e5cdba14862896ad052c.
Publisher log bytes:831131.
Git normalized log blob:a39af2168bbc1aeda8dfcbc6fa3ce3fb397e3f21.
Summary:runs/c276-v5b-final-boundary-lr-dcd7c7c2f13d49209c05bd4b2ca43110/summary.json.
Summary SHA256:6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f.

## Execution validity

The pre-science runtime gate passed before science:parent/source/artifact precheck502/878,
sealed manifest312ed892ba64ef1b0289506d44d1e3da05eec6ee85e67b1d3b21cee282e18355,
own24 PASS and focused3789 PASS. Ten fresh matched models completed800 updates each.
Total8000 optimizer updates,384000 training rows,9080 model forwards,487680 row presentations and
36320 core calls. One10-state bundle write/load and10 strict state loads completed.
all_pairs_matched=True;all_replays=True. Persisted LR-reliability reconstruction passed;tracked tree
and execution HEAD were preserved. run_execution_valid=True;scientific_status=FAIL;
candidate_gate=False.

The earlier C276 own-test failure was operational preflight only;no science was executed or
published for that attempt.

## Deciding metrics

Whole-state pass counts:
-lr0.005:0/5;
-lr0.0025:0/5.

Original two-character subgate:
-lr0.005:4/5;
-lr0.0025:5/5.

Unseen three-character subgate:
-lr0.005:0/5;
-lr0.0025:0/5.

Aggregate HOLDOUT two-character answers:
-doubled:control456/480,candidate480/480;collapse2/240 vs0/240;
-shared_prefix:458/480 vs480/480;collapse2/240 vs0/240;
-shared_suffix:458/480 vs480/480;collapse1/240 vs0/240.

Aggregate three-character answers:

|split/profile|lr0.005 correct|lr0.0025 correct|lr0.005 collapse|lr0.0025 collapse|
|---|---:|---:|---:|---:|
|TRAIN tripled|953/960|958/960|4/480|1/480|
|TRAIN shared_prefix2|939/960|956/960|14/480|4/480|
|TRAIN shared_suffix2|831/960|823/960|112/480|137/480|
|HOLDOUT tripled|455/480|480/480|5/240|0/240|
|HOLDOUT shared_prefix2|449/480|478/480|8/240|0/240|
|HOLDOUT shared_suffix2|400/480|404/480|57/240|67/240|

lr0.0025 therefore improves two-character retention and strongly improves tripled/shared-prefix
answer totals, but it does not solve shared_suffix2 and increases shared-suffix collapse in aggregate.

Per-seed HOLDOUT candidate lr0.0025:
-276001 two-char288/288;triple268/288;
-276002 two-char288/288;triple271/288;
-276003 two-char288/288;triple279/288;
-276004 two-char288/288;triple284/288;
-276005 two-char288/288;triple260/288.

Control lr0.005:
-276001 two-char288/288;triple279/288;
-276002 two-char288/288;triple277/288;
-276003 two-char220/288;triple202/288;
-276004 two-char288/288;triple279/288;
-276005 two-char288/288;triple267/288.

The lower LR removes the broad two-character failure seen in control seed276003 and improves its
triple total substantially, but it worsens several other seeds and leaves every candidate state
below the complete three-character gate.

## Scientific interpretation

C276 partially supports the optimization-reliability hypothesis for the original two-character task:
lr0.0025 gives5/5 retention where lr0.005 gives4/5. It also removes one broad failure mode.
However, it does not improve complete three-character reliability and cannot be adopted as a solved
training policy on the preregistered criterion.

The aggregate pattern suggests two effects coexist:
1. optimizer step size influences broad seed stability;
2. shared-suffix three-character binding remains a structural/task-specific weakness that lower LR
   alone does not remove.

Before another architecture or another LR is introduced,the exact fixed-criterion failures of both
C276 arms should be audited from persisted measurements.

## Non-claims

Do not claim lr0.0025 is a capability winner because it passes5/5 two-character seeds. Do not try
lr0.00125,extend training,select good seeds or relax fixed gates inside C276. Do not conclude that
optimization is irrelevant;the recovery of seed276003 is real. The registered candidate nevertheless
fails0/5 whole-state and0/5 triple.

## Accepted artifacts

-architecture-plan.json:312ed892ba64ef1b0289506d44d1e3da05eec6ee85e67b1d3b21cee282e18355;2594 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236 bytes.
-trained-models.pt:df59b5b957cc689e622414315ef5d66462c003c992242a4db0f9879999c8385f;1238007 bytes.
-evaluations.pt:04d4b34811d57f6d4ae8e1ab62a2ff4fadc67c07ad11d776e01193104f66a5d4;106278119 bytes.
-measurements.json:b9eeb1d2ca73be7201db648cc09c00b2bb87a256f230091172bab117484da096;524855 bytes.
-validation-summary.json:7d460b7d4a81e2621c933455cbdd71a8b94c2547ab6c7ff502d190a332c83ecf;22848 bytes.

## Next question, not activation

For accepted C276 saved outputs,how does lowering lr from0.005 to0.0025 change the exact fixed-gate
failure profile by criterion,seed,split and profile,especially shared_suffix2?

C277 should be saved-output diagnostic only with zero training and zero model forwards.
Verify/reconstruct accepted C276 artifacts with Module calls blocked,then attribute every failed
answer-cell and two-order criterion for both arms. Compare criterion-count deltas candidate-control,
with primary tables for triple shared_suffix2 and seed276003 recovery versus seeds worsened by the
candidate. Formal PASS means audit integrity only,not capability success. Gate F remains NOT PASSED.

C277 requires separate preregistration,implementation,final manifest sealing,committed-byte review
and runtime Validate. C278 NOT REGISTERED.
