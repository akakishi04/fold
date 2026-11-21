# C326 acceptance / C327 boundary

Reviewed 2026-10-17 Japan time.
C326 ACCEPTED VALID NEGATIVE. scientific_status=FAIL; candidate_gate=false;
run_execution_valid=true. Gate F NOT PASSED. All earlier verdicts unchanged.
Do not rerun C326. C327 is not registered by this acceptance commit.

## Evidence identity and scope

Scientific execution HEAD: dbef3dbc1566ff2c8c30405e9c8d207f5e79f460.
Published log commit: 4b94198f36af10ee319cd00c5a908b95426d8464.
Publication parent equals execution HEAD, confirmed through Git commit metadata.
Remote console: docs/experiment-run-logs/c326/latest.log and latest.json.
Metadata:150874 original Windows bytes; SHA256
1f40e1038fc5d68e44fd6aa3f48668ab81795c0ebae4b3350ca9d0ccb49abecf.
Git log blob:7da0ea4c990d3ece23300e7272d99b1cd8834c23.
The reviewer read remote preflight/full regression completion, ten final seed flags,
all five paired contrasts, checkpoint-replay completion and final input/envelope
receipts. Paired counts were independently re-summed. No whole-log independent
rehash, complete cell reconstruction or independent model replay is claimed.
Earlier attached C323/C324 files are not used as evidence for C326.

Local folder:runs/c326-mixing-bbd9cd8f43db45f18b2370f2c3337dfa/.
Primary science/summary.json SHA256:
0dd7af1c69774f5d00b1ee654284c38731f4233b2b858aedcf1bf0aaa77656aa.
Mandatory execution-envelope.json SHA256:
d379e907d3d9668f47b9690cb097398005b6c0c6c349ac30082ac3590d7dc62a.
Artifact hashes and local semantic/byte checks are reported by the registered run;
the reviewer did not independently open the user's local bundles or envelope.

## Execution validity

Native read-lock, accepted C325 composite snapshot, persisted parent semantics,
all five exact-pair/profile allocation plans and native TRAIN/gradient preflight PASS.
814 source pins/1533 input hashes; unchanged manifest
2be1555cf0296e55f5adf2e11302d6112b9b49836781199fcb3fc126d384871e.
Full5610 tests/215modules PASS:0failures,0errors,0skips;765.616seconds.
Ordered test-ID digest:
c72e4cd57d59fbd975d8ed8a609117a8d0f721414ceaf49702bdfcfb1f1b5aec.
Ten models complete1200updates each;ten checkpoint replays PASS.
Saved checkpoint/measurement reconstruction PASS;all1533 final uncached input
rereads complete. Fresh envelope verifier confirms814sources/1533inputs/5610tests.
Science and verification processes exit0;run_execution_valid=true.
Warnings from inherited tests are retained;no warning-free claim.
No source,gate,threshold,seed or outcome correction was used for acceptance.

## Deciding HOLDOUT counts

Each interior domain has288answers/144pairs per seed. Original2..6 totals have
1440answers/720pairs per seed;these are repeated logical cases,not independent tasks.

|Seed|Interior answers epoch->batch|Interior pairs epoch->batch|Original answer gain|Original pair gain|Batch interior gate|Batch original retention|
|---|---|---|---:|---:|---|---|
|326001|205->236|81->97|46|39|FAIL|FAIL|
|326002|186->280|64->136|-36|-23|FAIL|FAIL|
|326003|210->288|79->144|-9|-7|PASS|FAIL|
|326004|217->268|84->124|-21|-19|FAIL|FAIL|
|326005|187->244|67->110|-13|-10|FAIL|FAIL|

Interior answers1005/1440 ->1316/1440; both-query-correct375/720 ->611/720.
Every paired seed improves both interior counts.
Original2..6 answers7048/7200 ->7015/7200;pairs3460/3600 ->3440/3600.
Original answers by length2..6 (each denominator1440):
epoch:1440,1439,1436,1395,1338;batch:1437,1434,1428,1391,1325.
Batch interior gate1/5;original retention0/5;all-five composite0/5.
Epoch interior0/5;original retention0/5. Retain every failed seed.

## Interpretation and limits

At exactly matched per-pair/per-profile exposures, the within-update policy improves
interior binding in all five pairs, but does not meet the joint criterion; original
pooled counts decrease in four pairs. Mixing granularity matters in this cohort,
but neither this nor C325 establishes gradient conflict as its cause. High pooled
accuracy cannot substitute for every registered local/masked/order gate.
No architectural-impossibility, unseen-template, sequential-forgetting, statistical
independence, general-language, Gate F or production-readiness claim is justified.

## Next one-question direction, separately registered

Rather than another unmeasured ratio change, measure the alignment of original4
and interior4 TRAIN loss gradients at ALL ten fixed C326 final checkpoints, using
matched logical rows and each profile/language separately. This is a local geometry
diagnostic with zero optimizer steps and no weight modification, not proof about
all training stages or the actual AdamW update. Report dot products, norms, cosine,
zero-gradient cases and partition-specific contributions without a desired sign gate.

A successor must validate BOTH accepted primary summary and execution envelope,
inherit all814source/1533input protections plus all immediate parent outputs, and
extend the full5610-test inventory without new exclusions. Preserve accepted files.
Separate acceptance from next-C source/preregistration/review/activation. No CI,
checkpoint selection,package reinstall,artifact deletion or automatic retry.
