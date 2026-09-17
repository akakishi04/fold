# C177 acceptance — small within-count ordering gains, not a usable replacement

Judged 2026-09-18 JST. Repository akakishi04/fold; branch feat/sft-target-loss.
Read the unchanged C177 preregistration and experiment conversation protocol.

## Formal verdict

**C177 ACCEPTED PASS. C176 remains ACCEPTED VALID NEGATIVE. Gate E NOT PASSED.**
C178 is NOT REGISTERED at this acceptance-only boundary. C174/C175 and all earlier
accepted evidence retain their original verdicts and interpretation boundaries.
No threshold adjustment, model adoption, checkpoint selection or retraining is authorized
by C177's ranking PASS. It does not rescue C176's failed classification requirements.

## Execution validity and identity

Execution HEAD: 691b6df851525469889fe3640e638411ea284b58.
Source/artifact precheck PASS; 1025/1025 focused tests in 14.958 seconds.
All three analysis phases completed; 311040 saved decisions replayed;
56376 pilot score rows; 155520 aligned uniform/conditional decision-row pairs.
New training, model forwards, checkpoint deserializations, fresh seeds, threshold searches,
inference corrections, actual acquisitions, evidence writes and network calls: all 0.
83 protected input paths, 56 historical source pins and two output artifacts reported.
Runner postchecks: protected inputs preserved; tracked tree clean; execution HEAD preserved;
run_execution_valid=True. Existing C145 warning occurs in passing regression, not invalidity.
Diagnostic wall clock 4.02976080001099 seconds is not model serving latency.

Report:
runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json
Report SHA256: 99f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4
Uploaded log 226030 bytes:
aa63e74325b541ed7689fd02ce34c0bf919ca3be36375fa44af645f6cda1873e
Canonical reconstructed summary 47274 bytes; hash matches runner report.
score-order-plan.json: 6557 bytes,
390698e13539fba0182cf28906899da6fa7665eb53ef75e3c7aca9d451b2bf11.
score-order-details.json: 58158 bytes,
4ba428f8370e9549dbe85abf76627ce60f4bd005ac5ec86182f7b8daa779b12d.
Scientific manifest: 942735a9f843485eaf7b2b3b5f15cab774e749f7e52d37adcb64dcd8dcb5572e.
Parent C176 SHA256: b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
C174 SHA256: 3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.

## Deciding metrics

Primary is the equal mean AUC within missing counts 1,2,3 on reused PILOT_EVAL.
It is not accuracy and not overall AUC. Strict comparison uses saved exact fractions.

|Seed|Uniform AUC|Conditional AUC|Delta AUC points (100x difference)|
|---|---:|---:|---:|
|176001|0.5910100661914962|0.5913936600412220|+0.038359385|
|176002|0.5960457082542381|0.5963641829385455|+0.031847468|
|176003|0.5932198463519958|0.5975991306747999|+0.437928432|

Each strictly improves, satisfying the registered gate. No retrospective minimum effect
size or additional secondary gate is imposed. The effect size is nevertheless small;
this PASS does not establish statistical significance or practical reliability.

## Secondary results and scientific interpretation

Exact same visible-state key AUC uniform -> conditional:
176001: 0.5940127573209626 -> 0.5933664347153764;
176002: 0.5965195225669276 -> 0.5951966753648400;
176003: 0.5976853194162559 -> 0.6029344254373248.
Thus the stricter visible-state comparison improves in only one seed, not all three.
Count1 AUC increases in all three; count2 and count3 AUC decrease in the first two.
The registered average must not be described as a universal per-stratum improvement.

Overall AUC, which mixes missing counts, decreases in every seed:
0.7981770064536445 -> 0.7479202786142288;
0.8004425250801114 -> 0.7470458630116888;
0.7987098525878095 -> 0.7257447656953100.
These are different estimands; overall AUC cannot replace the registered primary,
nor should the primary conceal this degradation.

|Seed|Pilot errors rescued|Pilot new errors|TRAIN errors rescued|TRAIN new errors|
|---|---:|---:|---:|---:|
|176001|376|1059|2017|3958|
|176002|567|1298|2910|4762|
|176003|556|1141|2878|4434|

For missing count1, all changed raw decisions move toward NEEDS; for count3, all move
toward SUFFICIENT, on both TRAIN and PILOT. This supports a strong directional decision
shift, but is not proof of an exact constant-offset mechanism. Nonzero within-count
ordering gains rule out ONLY an account consisting exclusively of constant score shifts
within each count stratum. Do not infer unique internal reasoning from those small gains.
Classification errors are not measured hallucinations or tool executions.

## Confound audit and review scope

All six source models, original rows, logits, thresholds and checkpoints remain frozen.
Same four repeatedly inspected pilot groups; not independent confirmation. Pair totals
reuse rows and are not independent trials. TRAIN logits were not saved, so no TRAIN AUC
is claimed or filled in by model inference. No calibrated threshold or candidate selected.

Reviewer independently reconstructed the complete summary hash, recomputed 66 ordering
count tables and six exact primary fractions, checked all three deltas and gates, and
cross-checked 36 error-exchange tables against the uploaded C176 confusion matrices.
Stratum/group counts, transition sums, flip directions and zero-work counters agree.
The detailed per-group exchange tables exist only in score-order-details.json and were
NOT independently read here. Original NPZ, saved logits, checkpoints and output artifact
bytes were NOT independently reread; 1025 regressions and the formal audit were NOT rerun.
Runner hash-bound evidence and independent summary arithmetic remain distinct levels.

## Disposition and next design boundary

Preserve every prior model, log and result. Do not adopt CONDITIONAL_CE as a replacement.
The narrow score-order question is answered; avoid another unchanged-logit diagnostic
that merely searches for a favorable metric. Next design should address a concrete input
or computation bottleneck rather than tune a threshold to repair C176. Source inspection
shows the MLP receives leaf fact indices and a separate fact table, so it must learn their
binding as well as composition. An explicit copying of already visible fact fields to
referencing leaves is a possible isolated input intervention, not an observed cause or
an approved result. Any such comparison needs separate preregistration, no oracle values,
no hand-solved logical conclusion, unchanged historical code and a paired control.
C178 remains unregistered in this acceptance record.
