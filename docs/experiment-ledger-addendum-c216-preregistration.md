# C216 preregistration — V5-F learned Reader pilot

**C215 ACCEPTED PASS. C216 ACTIVE / NOT YET JUDGED. C217 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## One scientific question

Given correct H1/H2 memory and an oracle-selected port, can a learned Reader alone recover the
three-way semantic value on held-out factor-pair compositions and remain invariant across
HOT/COMMITTED placement?

## Parent checkpoint

C215 is the new accepted checkpoint root for C216.

Scientific execution HEAD:
`663f42ca21f977b6530e4df8709fc306c2ebd8c9`

Summary SHA256:
`96b3e5b9cf465b9dea33920de095fc5d7d8e4c0cba960d64597c95fc15eda237`

Validation artifact SHA256:
`1aa90b651d2f25a2ae72173e2e4e072236572e4057f40a35180a592980e90bd3`

C216 does not require the runner to receive the entire historical C199-C214 local summary chain.
Instead it validates the accepted C215 summary/artifacts, validates C215's 122 registered source
blobs against the current committed tree, and extends that fixed checkpoint with C216 OWN files.

## Changed variable

Learned Reader only:
`fold_lm/v05/memory_reader.py`.

Reader input width1; hidden width8; classes3; parameters43.

No query ID or memory status feature enters the Reader.

## Fixed data/split

- semantic values [-1,0,+1];
-9 alpha/beta pair combinations;
- TRAIN pairs6;
- EVAL pairs3: (0,1),(1,2),(2,0);
- HOT and COMMITTED placements;
- alpha and beta queries;
-36 total rows /24 TRAIN /12 EVAL;
- balanced TRAIN [8,8,8];
- balanced EVAL [4,4,4];
- data SHA `ab0c6da658576d12fc786ad3dfcef94f3acc063d8263dd175d67eec7af6a14eb`.

Port selection is oracle and outside Reader.

## Fixed training

Seeds 216001/216002/216003.

Adam, lr0.02, betas0.9/0.999, eps1e-8, weight decay0,400 full-batch steps per seed,
float32 CPU, threads2, deterministic algorithms.

Total registered workload:
- models3;
- steps1200;
- examples28800;
- Reader forwards1215;
- oracle selector calls36;
- oracle Writer operations18;
- chunk commits18;
- network calls0.

## PASS gate

For all three seeds:
- TRAIN accuracy1.0;
- EVAL accuracy1.0;
- HOT EVAL accuracy1.0;
- COMMITTED EVAL accuracy1.0;
- HOT/COMMITTED prediction mismatches0;
- zero-readout EVAL accuracy exactly1/3;
- checkpoint roundtrip exact.

A complete execution that misses any registered criterion is a scientific FAIL.

Syntax/source/artifact/count/checkpoint/runner defects are INVALID / RETRY SAME C216.

## Scope / non-claims

Writer remains oracle.
Port Selector remains oracle.
Coverage classifier remains absent.
No language mapping.
No Gate F decision.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_reader.py`
- `fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py`
- `tests_lm/test_v05_c216_learned_reader.py`
- `tools/run_c216.ps1`
- `tools/invoke_c216.ps1`
- this preregistration
- `docs/v5f-learned-reader-pilot-v0.1.md`

Expected:
- source pins129;
- protected inputs135;
- artifacts5;
- C216 tests36;
- regression modules101;
- loaded tests2186;
- exact historical exclusion1;
- focused regression2185.

Manifest SHA256:

`5332239247d95f6bcd98e328e12f8596aed765b4fa8780b71e1bfb5329fe521a`

Direct repository dependencies must all be pinned:
- memory_bank.py
- memory_bridge.py
- memory_capsule_bridge.py
- memory_reader.py
- C175 audit helper
- C205 regression helper
- C215 benchmark/checkpoint contract

## Post-authoring review

`post_authoring_review = PENDING`

Do not issue the C216 execution command before committed remote bytes are independently reviewed for:
- parent C215 identity/artifact hashes;
-129/135 accounting;
- dataset hash and pair split;
- Reader input isolation;
- no query/status leakage;
- fixed training workload;
- manifest hash;
-36 tests /101 modules /2186->2185 counts;
- free-name/import bindings;
- direct dependency pins;
- runner CLI indexes;
- complete PowerShell source-string assertions;
- C217 non-registration.
