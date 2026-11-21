# C269 acceptance and C270 unseen triple-identifier boundary

## Formal verdict

C269 ACCEPTED PASS in the preregistered bounded scope. The span_query candidate passed all5/5 fresh
seeds; the matched eos_query control passed4/5. Candidate HOLDOUT normal answers are1440/1440 with
zero same-answer collapse across720 paired questions. This establishes the registered structured
query-representation result; it is not Gate F completion or a general parser claim.

Scientific execution HEAD:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Published log commit:1c34b373ad9610dddcab2e7e54294fd5d4fe7cef.
Publisher log SHA256:b96fd0d8f4e87ae1a979f86b924b140de9a501aadacdef0b7eaa6333811b5b19.
Publisher log bytes:1082084. Git normalized log blob:af6b38013e0915b67d151dde1c49710ac88035eb.
Summary:runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json.
Summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.
Acceptance uses immutable published evidence and recorded local postchecks; no independent learned
state rerun or independent full publisher-byte rehash is claimed.

## Execution validity

Own24 PASS;focused3621 PASS. Parent/source/artifact precheck460 source pins/787 protected inputs
passed. Ten models completed800 updates each:8000 optimizer updates,384000 training rows,8540 model
forwards,435840 row presentations and34160 core calls. One10-state bundle write/load and10 strict
state loads completed. all_pairs_matched=True;all_replays=True. Persisted query-span score
reconstruction passed;tracked tree clean;scientific HEAD preserved;run_execution_valid=True.
scientific_status=PASS;candidate_gate=True.

## Deciding HOLDOUT metrics

|Profile|EOS correct /480|Span correct /480|EOS collapse /240|Span collapse /240|
|---|---:|---:|---:|---:|
|doubled|427|480|12|0|
|shared_prefix|425|480|12|0|
|shared_suffix|424|480|10|0|
|all|1276/1440|1440/1440|34/720|0/720|

Seed pass counts:eos_query4/5;span_query5/5. Candidate seeds269001..269005 all pass every fixed
TRAIN/HOLDOUT/profile/language/subset/order answer,query-pair,mask and two-order criterion.
Control failure is concentrated at269002,which has124/288 pooled HOLDOUT normal correct and34
collapsed pairs;the other four control seeds and all five candidates have288/288 and zero collapse.
Pooled values describe the observed cohort but do not replace the all-five candidate gate.

## Scientific interpretation

Under the fixed paired CE training policy,explicitly constructing the reader query from the visible
query identifier span is sufficient to remove the observed fresh-seed reliability miss in this
bounded family. The candidate changes no parameter count and uses exactly matched initial tensors,
batches,data,optimizer,loss and update budget. This is stronger evidence for query-source design than
C268's output-margin intervention,which passed only3/5 under its own fresh cohort.

The result does not prove the EOS state is universally harmful,that delimiters solve arbitrary
language parsing,or that the query-span path is globally superior. All three identifier profiles
were TRAIN-seen;the positive result is held-VALUE-pair transfer under trained name structures.
The delimiter rule is explicit task structure and fact/value/name distributions remain authored.

## Accepted artifacts

-query-plan.json:cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa;2696 bytes.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
-trained-models.pt:65f3b34e163b7753ecfda2eadedeb7cd8f282a0437b6b94ec2034d2efeadea9c;1238007 bytes.
-evaluations.pt:a9212d3da65849ebc08f4f7ed1e669f73b34f897d1f4ab05b077582c1d220c29;53143103 bytes.
-measurements.json:3d64033da08d8a83b8bebe53e6acd4b85340acffb9d849ebcb7b921f480a7811;261837 bytes.
-validation-summary.json:44de8eb095ceca1f3827ec4e2ba521a750fd80e49b38235db027754dbb540e6a;6979 bytes.

## Next question, not activation

Do the same frozen C269 states transfer from TRAIN-seen two-character identifiers to unseen
THREE-character identifiers built entirely from the same familiar identifier characters?

Use three fixed new profiles for each source character pair u,v:
-tripled: uuu / vvv;
-shared_prefix2: uuu / uuv;
-shared_suffix2: uuu / vuu.
No three-character identifier string occurred in C269 optimization. Keep every logical C267
TRAIN/HOLDOUT value row,language,entity subset,fact order and both queries. Preserve the old value
split in reporting:TRAIN-value rows isolate the new-name/length shift more directly;HOLDOUT-value
rows combine that shift with the already registered held-value dimension. Both are required.

Freeze all10 C269 final states;no training or new checkpoint. Strict-load their accepted weights,
replay the accepted two-character C269 outputs before and after the new prompts,verify unchanged
full fingerprints,and score the new profiles with the same fixed answer/query-pair/mask/two-order
thresholds. Candidate interpretation remains bounded:three-character familiar-byte strings are not
arbitrary names or ordinary language. C270 requires separate preregistration,implementation and
committed-byte review before activation. C271 NOT REGISTERED.
