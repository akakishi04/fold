# C323 independent post-authoring review

post_authoring_review = PASS
Review HEAD:c2a9812ce53564aefd602c18e96af11e047745da.
Acceptance base:a0e2221eb8f12b5a2cc8f325876a8752ed1b9eb1.
Scope:committed Git bytes/static audit and executed local software tests,NOT genuine C323 scientific result.

## Immutable authoring inputs and file identity

Six OWN files were refetched from the committed HEAD after authoring,with bytes/length and
Git blob IDs independently compared against the same local software files tested after
remote fetch. Exact SHA matches6/6:
- fold_lm/v05_benchmarks/model_c323_saved_fact_order_bias.py
  9d9dc794ce95d14755e0916b21ebebe2ae2ac176,20034 UTF8 bytes.
- tests_lm/test_v05_c323_saved_fact_order_bias.py
  9d0907c697e2b6500063755546c89c74eb402e5b,17958bytes.
- tools/run_c323.ps1
  2d83a44b4fb7cf713a69080552f6a0de9cbcbf96,9377bytes.
- tools/invoke_c323.ps1
  b5446a817ae83ac6de60b9da1dc501593217609d,8005bytes.
- docs/experiment-ledger-addendum-c323-preregistration.md
  fdd2efdbcddd909d9423c58d6f399b3498dde6dc,6309bytes.
- docs/v5b-saved-fact-order-bias-v0.1.md
  0f081ebd32aa6696bf373aa6f80023906aec0354,1302bytes.
Authoring commit adds exactly these6 files against acceptance;no accepted artifacts/tests,
historical log,preregistration or dispatcher modified. New files retain tested LF/UTF8 bytes.

## Independent post-refetch software tests actually executed

One uninterrupted entire unittest module with normal default:Ran24,OK,0failures,
0errors,process exit0,0.978s.
One uninterrupted entire unittest module under default-CP932 emulation:
Ran24,OK,0failures,0errors,process exit0,1.030s.
Both runs were conducted AFTER all6 remote blobs had been refetched and local hashes matched.
CP932 emulates io.text_encoding when encoding is unspecified,across import/setUp/tests/tearDown;
this is not a complete Windows execution. Environment:Linux/Python3.13.5/
PyTorch2.10.0+cpu/NumPy2.3.5. Actual accepted Windows Python3.13.15/PyTorch2.10.0+cu130,
PowerShell7 and local parent archives unavailable here.

Both Python AST files compiled;all three embedded Python here-string blocks in runner compile.
Manifest canonical self-hash 8c4e9152cb11d1492cd7d88cf7caafef40a901de6c68aa44e404c1c46ff7c5de matches.
OWN6/docs constants,49 launcher parent paths descending C322..C274,postcheck argv[2:51],
head argv[51],argc52,full regression5286loaded/5293focused? Correction:
528? See exact prereg: loaded5294/focused5293;review validates these.
Python full-suite test simulation verifies5294 distinct loaded IDs with sole inherited C204
exclusion =>5293 focused IDs. No new test exclusion.

## Deciding path/source semantics

Child imports exactly one repository science module directly:C322. It obtains original
logical data and C322 saved query-pairs.json through full verified C322→C321 ancestor path,
not a new model/checkpoint. 49 SHA-256 parent summary identities checked BEFORE parent verify.
Exact C322.verify_artifacts invoked with48 prior summaries and accepted scientific execution HEAD.
Parent PASS is diagnostic-only;4 JSON artifacts sealed;query-pair inventory8640 and logical
TRAIN192/HOLDOUT96 source row identities fixed.

Each pair's canonical A/B row-ID/entity/value/target/fact permutation/profile mapping is checked;
neither query nor fact-order orientation depends on observed predictions or correctness.
Two inverse fact permutations form one four-response counterfactual:4320 total.
Report first-fact/last-fact answer counts,first-/last-both-order heuristics,
all-four-value lock,query stability under permutation,and correctness.
Conservation of all17280answers,8640 parent pairs,240 group summaries and4 accepted
C322 overall reconciliations is mandatory. Both arms and old4/interior controls remain.
No new model calls/training/state loads/optimizer/tensor checkpoint or restricted decoder.

Synthetic fixtures independently test the paired-order classification:query-correct original4,
first-fact-following, last-fact-following and value-locked cases are disjoint where expected.
Bad source IDs/targets/overlapping permutations,duplicate/lost C322 pairs, altered parent
aggregates,wrong provenance and corrupted JSON fail. Full source coverage uses784/1478
temporary protected-file fixtures and rejects missing imported helpers. All49 wrong parent
summary hashes were exercised before parent verify dispatch in mocked loader path.
The actual child run,JSON persistence,reconstruction,resealed semantic tampering,
no-overwrite and no-neural/no-optimizer restrictions passed on controlled fixtures.

## Runtime and stop boundary

Postcheck independently reloads parent evidence and reconstructs all JSON under no-neural guard;
at output time source/protected hashes and tracked tree are verified. Four artifacts plus
summary;all large raw C322 tensor data remain local and unmodified. Parent C322
log_sha256 and accepted summary_sha256 remain pinned,not rewritten.
The runner keeps one Python process for all historical focused regression tests in exact order,
UTF8 direct progress logs,fixture-boundary timing,faulthandler,and native decimal/hex exit values.
Launcher Validate runs parent checks,OWN24 and focused5293 BEFORE science or publication.
No parent overrides,scientific changes or test bypass implemented to reduce elapsed time.

C322 focused5269 previously consumed1245.157s (~20m45s) and remains an observed cost.
This authoring review did NOT execute the real focused5293 suite or profile Windows I/O.
Its purpose is software contract readiness,not a claim of reduced runtime.
Windows Validate still must confirm49 real parent archives,all784/1478 pin/inputs,
ParseFile for dispatcher/launcher/runner,the actual own24 and full5293 regression,
before the scientific C323 audit is allowed to start. If any check fails,retry SAME C323;
no C324 registration. C322 diagnostic PASS,C321 valid negative,C320 bounded PASS and
Gate F NOT PASSED remain separate and unchanged.
