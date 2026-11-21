# C331 acceptance / C332 authoring boundary

Review date: 2026-10-19 Japan time.
C331 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). The frozen first/mean intervention is NOT adopted.
C330 remains accepted diagnostic PASS; C329 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C332 is not registered or authorized by this acceptance.

## Evidence identity and execution

Execution:36444b77b48ac1be5545a5346454142eb1955fb0.
Publication:41bd1ec9309c3d7e3d573abd70d0441f57ca6d0e; sole parent equals execution.
Metadata/log:docs/experiment-run-logs/c331/latest.json and latest.log.
Publisher reports210476Windows bytes and SHA256:
457e94f5afafa8d437b9b9f61155dc70dc1892e628449050cabed1f3fb432110.
Git log blob:f08c18c65d4d36660198f0d17dd0332f68bbfc19.
Metadata blob:28964bef5106ae6fab783b9353d429f9a28f425d.

Native locks, accepted C330 semantics and full parent test-evidence checks passed.
Registration847sources/2051inputs; native12-forward preflight passed.
Full5898tests/221modules PASS;failures/errors/skips0;1355.667seconds including module
orchestration. Ordered test-ID SHA256:
31527c05d53e04cb8dd4804f7a3d255b90c7f5b35880d12e2b69f9abd6993adb.
All10states completed native_before/first_mean/native_after with unchanged weights.
Saved reconstruction,all2051final uncached rereads,fresh parent/test/output verification
passed. Regression/science/verify exit0;run_execution_valid=true.
Scientific work5130model forwards,492480rows,20520core forwards,10260query projections,
10state loads,1bundle load;training/gradients/new checkpoints0. Preflight/tests and
saved/parent checks have separate work scopes. Controls enforce1e-9 and exact argmax;
a passing receipt does not assert independently measured zero drift.

Local folder:runs/c331-query-probe-60e1b2a8ebe1465dba86f31409a6a9d1/.
Primary science/summary.json SHA256:
28f5aa242fdb26674e4f1b2bde6e752c8e4b7fea88c1fb19b6157a796acd4376.
Mandatory execution-envelope.json SHA256:
3b3bb3a591b225d8f03d30c374c47d2307d2ca744061601aa2fd2f3356b046a0.
Manifest8644f03a61e1dbdbb44a31514a392fd18cdb7ce71c190ee1a1fd2a8c759c30f8.
Primary/envelope schemasfold-c331-diagnostic-v1/fold-c331-execution-envelope-v1.
The4science outputs+summary+envelope and445bound regression files(3records+221JSON/log
pairs) make451mandatory immediate-parent files. Inherit full847/2051unions.

## Deciding HOLDOUT counts

Each domain below pools the same288logical/profile answers across5seeds (denominator
1440),not1440independent new problems. Native -> frozen first_mean:

|Domain|prefix1200|extended2400|
|---|---|---|
|original2|1439->1435|1440->1420|
|original3|1439->1430|1440->1421|
|original4|1438->1416|1440->1424|
|original5|1418->1364|1431->1382|
|original6|1338->1279|1386->1337|
|interior4|1206->1195|1427->1387|

Extended2400 per-seed original6 answer gains(329001..329005):-14,-25,-10,+3,-3.
Original6 paired correct counts673->628/720;gain-45. Interior pairs708->668/720.
Original2..6 pooled answers7137->6984/7200,gain-153;prefix7072->6924,gain-148.
Extended2400 full interior gates4/5->2/5;original2..6 retention1/5->0/5.
Failed local cells46->181/2160;failed order cells17->88/1080. Preserve correlated
assessment semantics;do not add local/order counts as independent error events.
All five original5 comparisons worsen. Only329004 improves original6 answers;
its query-pair gain is0 and its original5answers fall2. No seed selection for adoption.
Seed329002 incurs losses even on original2..4;the harm is not isolated to long names.

## Interpretation, limits and next question

The exact untrained.5first/mean substitution is harmful overall and is not adopted.
Native replay and invariants passed,so this is a valid measurement,not technical
INVALID. It does not prove that first-byte information is useless,that mean pooling
caused C330's errors,or that a model trained with this readout would behave similarly.
It also does not support changing the coefficient,thresholds or selecting a seed.

A bounded next question is whether TRAINING and evaluating with the same fixed
first_mean readout can outperform native mean/last training at equal2400-update
budgets. Use paired fresh initializations,identical repeated batch4 schedules,
optimizer/data/architecture and fixed.5coefficient. Train all pairs before evaluation;
no accepted checkpoint initializes fitting. This changes train/inference policy
consistently rather than adding another frozen coefficient search.
Implementation,explicit new primary gate,preregistration,committed-byte review and
ACTIVE registration must precede a C332 command. No C333,CI,paidservice or reinstall.

## Review boundary

Reviewed exact-ref startup,regression completion,all ten completion messages,all ten
complete effect records and terminal verification. Independently summed the printed
deciding counts. Did not independently rehash the original Windows log,load the local
model archives,recalculate logits or inspect all221local module receipts. The native
executor/fresh verifier report those checks. Older C323/C324 attachments are not
current evidence. No past verdict or failed-attempt archive is overwritten.
