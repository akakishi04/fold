# C325 acceptance / C326 boundary

Reviewed 2026-10-16 (Japan time).
C325 ACCEPTED VALID NEGATIVE. Scientific status FAIL; candidate_gate false;
run_execution_valid true. Gate F NOT PASSED. C324 and all earlier verdicts unchanged.
This is not an execution failure and does not authorize refitting C325.
C326 NOT REGISTERED at this acceptance; no ACTIVE experiment until separately reviewed activation.

## Identity and review scope

Scientific execution HEAD: f95895313da81634976d0ff2761efdd793888c2b.
Published log commit: c030498473daf1155bc5cba6e358f944ec8fce1a.
Publication parent equals that scientific HEAD, checked from Git commit metadata.
Remote console: docs/experiment-run-logs/c325/latest.log and latest.json.
Published metadata reports 149964 original Windows bytes and SHA256
c54a2ec2d20bd94990fa0eac79dc14e98a5db83dc53a06299c809757fa72dfa5.
Git log blob: be7fd195c778574f21dcc9bb1bcee90200ee5352.
The reviewer read remote registration, regression completion, scientific progression,
all ten seed flags, all five paired contrasts and the complete terminal verification
receipt. The reviewer independently summed the paired count tables; this is NOT a
whole-log independent rehash, full local-cell reconstruction or independent model
replay. No claim of independently opening local tensor/summary/envelope bytes.
The old C323/C324 uploads are not evidence of this new C325 execution.

Local output: runs/c325-mixed-name-26478978a92c42d2980095d76d6e4339/.
Primary science/summary.json SHA256:
e3e9808fea616ecc27e2644f808553f16fb6a11203284bdea5c2cf63b32006e8.
Execution-envelope.json SHA256:
e40a7e93159cdf33b94b11e8ee8df197da66949d121dd52eb8c6036db99440b9.
These hashes and local artifact verification are reported by the registered execution.

## Execution validity

Native read-lock probe PASS. Accepted C324 composite evidence and persisted parent
semantics validated, without ancestor semantic reruns or parent model forwards.
808 source pins / 1517 protected inputs; unchanged manifest
03ed2ba1d2d2951087c70ce41ddf39756674a30ac4cef56671e158eb80fff3d0.
Native TRAIN/readout/gradient preflight PASS.
Full regression: 5546 tests / 214 modules, 0 failures/errors/skips, 724.969 seconds.
Ordered test-ID digest reported:
23df14a0e694c961b7522dd0b21803eae3a1ab55f56d795ba33d32ffc1135498.
Ten new models, 1200 updates/model; ten checkpoint replays. Persisted training /
evaluation semantic verification PASS. Final uncached rereads: all 1517 inputs.
Fresh-process execution_envelope_verified: 808 sources,1517 inputs,5546 tests.
Regression/science/verify exits all 0. Terminal run_execution_valid=true.
Retain inherited warnings; this was not claimed to be warning-free.
No source/test/gate correction or successful-seed selection is used for acceptance.

## Deciding counts (HOLDOUT)

Each seed has 288 interior answers / 144 query pairs; original2..6 totals have
1440 answers /720 pairs per seed. Same logical cases repeated across seeds.

| Seed | Interior answers control -> mixed | Interior pairs control -> mixed | Original answer gain | Original pair gain | Mixed interior gate | Mixed original retention |
|---|---|---|---:|---:|---|---|
|325001|288 ->185|144 ->72|75|67|FAIL|FAIL|
|325002|152 ->97|48 ->18|208|158|FAIL|FAIL|
|325003|58 ->74|0 ->0|264|95|FAIL|FAIL|
|325004|278 ->225|136 ->95|57|48|FAIL|FAIL|
|325005|288 ->246|144 ->103|135|113|FAIL|PASS|

Pooled interior answers1064/1440 ->827/1440; pairs472/720 ->288/720.
Pooled original2..6 answers5573/7200 ->6312/7200; pairs2439/3600 ->2920/3600.
Original counts by length2..6 (denominator1440 each):
control1210,1204,1116,1038,1005; mixed1276,1269,1265,1256,1246.
Interior answer gains -103,-55,+16,-53,-42; pair gains -72,-30,0,-41,-41.
Mixed interior gate0/5; retention1/5; composite0/5.
Control interior gate2/5; retention0/5. Do not call the control uniformly reliable.
The existing per-cell/masked/order gates are stricter than pooled accuracy and unchanged.

## Interpretation and limits

At this fixed budget, the 50/50 epoch-level mixture improves pooled original-task
counts in every paired seed, but loses interior binding in four seeds and does not
meet the all-five joint criterion. This rejects this registered candidate, not the
possibility of learning both families. Seed325003 is weak in both arms and retained.
Do not infer a gradient-conflict mechanism or compare across C324/C325 as a controlled
seed-independent effect. No sequential-forgetting, unseen-template, general-LLM,
statistical independence, Gate F or production adoption claim.

## Next one-question direction -- not registration

Test temporal granularity at fixed family exposure: whole-epoch switching versus
within-update mixing. Preserve logical row/pair order and exactly match each query
pair's original/interior exposure within each profile, not just aggregate 50/50.
Any deterministic allocation must use row identities and schedule only, never labels,
losses or HOLDOUT. No ratio/architecture/learning-rate search is authorized here.

A successor must inherit all808 accepted source pins and1517 input hashes, verify
both primary summary and envelope, all immediate outputs and persisted C325 semantics,
and extend the whole5546-test inventory without new historical exclusions.
Separate this acceptance from next-C source/preregistration/review/activation.
