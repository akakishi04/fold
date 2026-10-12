# C320 formal acceptance — bounded unequal-name-length capability PASS

C320 ACCEPTED PASS. This is the preregistered unequal-length capability criterion,
not diagnostic integrity alone. C319 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED.
C321 NOT REGISTERED at this acceptance commit.

## Evidence identity

Scientific execution:0e4687acfa72355cbddc47c3ceb98700354fe34d.
Publication:7a693b5d7747ab67146a8c2fa2f996cb10b5054d.
Console:docs/experiment-run-logs/c320/latest.log.
Log SHA256:34570e813588d80f63f2ac3e49fa9eeb909aab7c1c9475bb7de90c503e851093;965523bytes.
Summary:runs/c320-v5b-unequal-names-d1599525908a404998a52011a5567b81/summary.json.
Summary SHA256:9e41e82228f26cf525ee54e4097abd493a339641d6b3d3f5b2a6d10ba8868431.
Manifest34ac7cbac03191c2e64ae05887f7d04cbc90c3cf0a73e18427708c1bbeed307d.

## Validity and recovery closure

Own24 and focused5221 passed. The full original ordered single-process regression completed
5221 tests in735.042s,failures0/errors0,exit0/0x00000000. No test was dropped or substituted.
The earlier preflight interruption did not recur. Its root cause remains unknown:successful
instrumented retry is not proof of a repaired C174/thread/native/OOM cause.
All10 frozen checkpoint evaluations and original-output replays completed;both reproduction
errors0.0 for every state. all_replays=True,persisted_unequal_names=PASS,
run_execution_valid=True,tracked tree clean,execution HEAD preserved. Publication modifies
only latest.json/latest.log. Source766/input1443 maintained. Training0.

## Deciding results and interpretation

mean_last5/5 passes short_long(2,4),5/5 long_short(4,2),5/5 BOTH. The primary is satisfied.
last_only4/5 short_long,5/5 long_short,4/5 BOTH. Only last_only319002 short_long HOLDOUT fails,
with287/288 normal answers correct;its TRAIN576/576. All other normal partitions are perfect.
For mean_last all5*2layouts*864=8640 normal answers are correct. This pooled count does not
replace the separate local/masked gates. All original C319 per-state gates are preserved.

These frozen equal-length-trained models handle a new within-question mixture of lengths2/4.
The unequal lengths themselves create discriminative cues,so this is not proof of matching
name contents independent of length,first/last symbols or character counts. Same checkpoints,
value split and synthetic name families;no new-seed replication or Gate F claim.

## Proposed next boundary,not registration

Test frozen C319 states with four-character name pairs sharing first and last characters AND
the same character multiset,but differing in internal order. This removes those simple cues
without increasing length or adding vocabulary. Preserve all10 states,their trained readout,
all original bilingual logical rows/splits/views,and original-output before/after controls.
No retraining or selection of only successful states. Register and review before execution.
