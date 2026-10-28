# C340 acceptance and C341 saved-gate diagnosis

Date: 2026-10-29 Japan time.
C340 ACCEPTED VALID NEGATIVE. C339 remains ACCEPTED PASS(DIAGNOSTIC INTEGRITY).
Gate F NOT PASSED. No production adoption. C341 is not activated by this acceptance.

## Execution identity and validity

Execution15f88d08071ac0b36551fb2f61b3e10dbd0c6445.
Publication586c03adad82d0ff53d0815f55c88ee44fc67239;its sole parent is the execution.
Publication changes only docs/experiment-run-logs/c340/latest.log and latest.json.
Metadata259456Windowsbytes/SHA256
7f8714065eef730e686e1d68f1073c1f4edd8ba8e35eceba3f2c224c67d6b49d.
The Git LF log has256332bytes;reconstructing CRLF gives the exact published size/hash.

All6258tests/231modules PASS,0failures/errors/skips,2430.257seconds.
Begin/complete records match across consecutive module indices0..230.
Ordered test-ID SHA807b1fd8cbefff30b4d73e3f62b5a24170b014064e4e4a0a487800f8827ccd17.
All6243final uncached rereads and independent902source/6243inputverification complete.
Science/regression/verifyexit0;run_execution_valid=true. Native preflight completed.
All10fresh fits reached2400updates before any scientific saved evaluation/replay.
Scientific24000updates/27420forwards;10final states/evaluation-and-replay records.
Persisted reconstruction and fresh verification completed with no integrity error.

Folder runs/c340-length5-training-0c8af407e2564082b7221f1c95ddb709/.
Primary263902957881a2a6a9bff426f540b7e05e8b43be46c1ce6e546e235cf0db7b7e.
Envelopea4b32eebbff72a6e6637bed1ef23e881dee77e9747b467d80349095909613c9a.
Manifest8016f388949a574a3609a563d1005c99b1c83455cd31148471f60a7c9b832914.
A successor preserves ALL473parent outputs:6science+primary+envelope+465regression
proof files(3records+231module receipt/log pairs),in addition to902sources/6243inputs.

The complete console was inspected,all5paired contrasts and10state records were
reconciled,and the preregistered fixed_gate reproduces false/[true,false,false,false,true].
The original7source blobs are unchanged from reviewed sourceHEADd074f34 through
execution/publication. Accepted parent helper pins/manifests load unchanged.
This remote audit does not independently rerun Windows native leases,rehash local-only
checkpoints or replay optimizer steps;those claims rely on the published native
executor/fresh-verifier evidence and its pinned implementation.

## Deciding metrics

All figures below pool5seeds*3profiles*bothlanguages in normal HOLDOUT. Each arm/domain
has1440answers and720query pairs. A query pair asks for both entities under the same
fact order;both-order scoring is a separate gate.

|Domain|Correct control->candidate|Both-query-correct control->candidate|Answer rescued/regressed|
|---|---:|---:|---:|
|original2|1438->1440|718->720|2/0|
|original3|1440->1440|720->720|0/0|
|original4|1439->1433|719->713|1/7|
|original5|1430->1440|710->720|10/0|
|original6|1396->1439|681->719|44/1|
|interior4|1374->1434|662->714|61/1|

|Seed|Original6 answer/pair gains|Pooled original2..5 gains|Interior4 gains|Candidate full gate|
|---|---:|---:|---:|---|
|340001|+22/+18|+8/+8|0/0|PASS|
|340002|+5/+4|+4/+4|+60/+52|FAIL:interior4|
|340003|+6/+6|-7/-7|0/0|FAIL:original4|
|340004|0/0|0/0|0/0|FAIL:original6|
|340005|+10/+10|+1/+1|0/0|PASS|

Only2/5candidate states satisfy the full gate,versus0/5control states. The candidate
also violates per-seed short-domain retention at340003. Therefore the registered
conjunction is false despite strict original6cohort gains(+43answers/+38pairs).
No threshold,cohort,seed,comparator or gate was changed after observing the result.

Candidate340002 has6normal interior4errors(4wrong_observed/2absent_digit),5failed
local cells and2failed order cells. Candidate340003 has7normal original4errors
(6wrong_observed/1absent_digit),4failed local cells and2failed order cells.
Candidate340004 has1normal original6error(absent_digit),1failed local cell and0failed
order cells. The console counts do not identify the exact split/profile/language or
criterion of those failed cells;do not infer a masked-control failure from aggregate
accuracy alone. Per-cell evidence remains in the saved measurements.

## Interpretation and boundaries

At this fixed fresh cohort/update budget,the length5training boundary improves
normal original6transfer substantially and improves interior4overall. The loss of
original4exposure is accompanied by a specific original4regression,but this does not
prove an internal causal mechanism. Full all-seed robustness and retention are unmet.
VALID NEGATIVE here preserves the failed preregistered conjunction and the useful
improvements;it does not mean the intervention has no effect.

Candidate original5TRAIN prompts were fitted;original6was not fitted in either arm.
TRAIN/HOLDOUT labels describe value-combination partitions. Candidate original4was
removed from that named training domain,while interior4remained. Equal2400updates
did not equal nonpadding exposure:3110400control/3225600candidate tokens per model,
including BOS/EOS. No universal length generalization,optimal curriculum,production
adoption or Gate F completion is established.

## Next bounded question

C341 should localize the existing fixed local-binding,masked-dependence and both-order
gate failures using ALL saved C340measurements. Match every seed/arm/domain/split/
profile/language/entity-set/order,including successes. Reconstruct parent flags,
failure counts and normal HOLDOUT counts,then report rescued/regressed/persistent
gate criteria and their exact coordinates. Gate-cell changes are not individual
answer changes;preserve that distinction and C340's raw-verified answer transitions.

No new training,model forward,new prompt,weight selection,inference mask or threshold
sweep. An immediate repeated training run would not resolve which remaining gate
is failing. Diagnostic PASS means complete consistent reconstruction only.

Reuse immutable C330/C333-style localization helpers with a C340-specific adapter.
Correct the old helper's static training-exposure annotation for BOTH arms:control
has original2/3/4+interior4,candidate original2/3/5+interior4;original6never. Distinguish
domain exposure from whether a TRAIN/HOLDOUT prompt was actually fitted. The accepted
helper itself remains unchanged. Complete implementation,preregistration,independent
committed-byte review and separate activation are required before a user command.
