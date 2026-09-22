# C226 preregistration — fixed-port numerical dimension scaling

**C225 ACCEPTED PASS. C226 ACTIVE / NOT YET JUDGED. C227 NOT REGISTERED.**
Gate E PASSED; Gate F NOT PASSED.

## One scientific question

With two update/readout coordinates fixed, how do the existing H1/H2 and incremental-symbolic
full-solve paths compare as the coupled full numerical system grows to2,16,64,256 variables?

This follows C225's unfavorable small-system comparison. It changes dimension/matrix family, not
production algorithms, semantic tasks, number of live factors, learned weights or safety checks.
No optimization, raw deletion, inference/training, cleanup or cost-superiority requirement.

## Parent identity

Scientific HEAD: `6669add6de53247e60731a3f23e7bed9350deec3`.
Log commit: `88395cb0d44b0ca02fcb106967b97d966dcbe1b3`.
Summary SHA: `b54943514cebb06161851e6a79c9eb4e8fd6766429f6f2e0e2f34c79c52a78ad`.
Validation SHA: `94e2028aaaff24f9cc03480abde49c2e41674d833141745e6bc34f9852620a29`.
Measurements SHA: `50e82a0a655ab63ddf00da04edab1995c7b99064ae493ba5320a0d2f348362a2`.
Local summary:
`runs/c225-v5f-stateful-baseline-4df0cd59e7c34942a3d33b0932863b0f/summary.json`.

Validate all190 parent source blobs,244 inherited protected inputs and all five parent outputs.
The parent measurements adapter requires complete ordered history sizes and the real parent row gate.
The history32 point is the n=2 anchor; both candidate and symbolic export inventories must match.

## Fixed numerical family

Dimensions2/16/64/256; update rank2; readout dimension2; live observed factors2; history32 events.
Use the original C225 raw ledger and six relation contributions.
Raw SHA: `735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`.

J has diagonal4, zero direct edge(0,1), off-diagonal -0.25 on edges(1,2)..(n-2,n-1) and(0,2)
for n>2. eta=0; U selects axes0/1; Q=U.T. All hidden coordinates are connected to visible ports.
At n=2 the original factory is returned unchanged; no extra coupling exists.

Tensor identities (J,eta,Q,U in ordered little-endian float64 with explicit shapes):
- n2: `c18286d29c755f6cabcb4a7ba4c0735deb843120310f5cf6fa48b41f534ee3b8`
- n16: `c7761d3a5c887ac8c0404a6539ec1cc0c3abdb8d9c61469ad8f295696691d8e8`
- n64: `91f45756cf2e27e6c76cf0784b68ed1998fbe03e10224d384e1faf611c827db1`
- n256: `116cf8b6c351f0b96e012134d747466deb7966a2dc7fc36b8f659be3b8f13340`.

## Fixed measurement

Reuse C225.measure and C224 cost helpers without editing their files. Local factory injection only;
no monkey-patching of accepted bank/module definitions. Full original raw/index/bridge retained
and counted in both arms, including unused compiled capsule in the full-solve arm.

One warmup+three measured queries, alternating arm order, float64 tolerance1e-10, CPU threads2,
deterministic algorithms. Record candidate/symbolic construction and index/export cost separately.
Higher-n candidate construction includes the small template setup plus larger bridge compilation.

Add one untimed instrumented query per arm/dimension. Wrap actual torch.linalg calls and restore
functions on success/error. Require traces:
- H1/H2: cholesky2, cholesky_ex2, solve2 at every n;
- symbolic: cholesky n, solve n.

No removed safety check or hidden full-solve fallback. Compare instrumented responses too.

## Fixed audit gate

All four dimensions required, in registered order. Require:
- inherited correctness, full symbolic/provenance parity, state non-mutation and file inventory gate;
- exact full-system tensor identities and original raw identity;
- two live factors and fixed update/readout rank;
- zero warm raw rereads for both arms;
- matching n=2 candidate AND symbolic export inventories against C225;
- exact solve/safety-check matrix-shape traces;
- max absolute numeric error<=1e-10;
- complete verified ZIP_STORED archive;
- new training/model forwards0.

No storage or speed-superiority threshold. Higher retained bytes/slower timings are reported as
unfavorable, not hidden by audit PASS. A complete correctness/accounting gate miss is scientific FAIL;
source/artifact/schema/regression/incomplete-run defects are INVALID / RETRY SAME C226.

## Interpretation limits

Numerical variables are not neural parameters, layers, concepts or live-factor count. Only two
observed factors are tested. Sparse coupled inputs use the existing dense baseline; no claim against
specialized sparse/banded or factorization-cache implementations. Both keep the entire full bridge.
Canonical exports and reachable-data estimates are not native checkpoint or process RAM/VRAM peaks.
Three timing trials are descriptive. No natural language, bounded indexing, production optimization,
new safety guarantee or Gate F decision.

## Registration

OWN6:
- `fold_lm/v05_benchmarks/gate_f_c226_dimension_scaling.py`
- `tests_lm/test_v05_c226_dimension_scaling.py`
- `tools/run_c226.ps1`
- `tools/invoke_c226.ps1`
- this preregistration
- `docs/v5f-fixed-port-dimension-scaling-v0.1.md`

Source pins196 =190+6. Protected inputs256 =244+6 parent summary/artifacts+6 OWN.
Direct dependencies24 = C225 deciding dependency set23 + C225 benchmark. No accepted file changes.
Outputs5: dimension-plan.json, dimension-exports.zip, measurements.json, quality-checks.json,
validation-summary.json. Generated data stays under ignored runs/; console publishes measurements.

New tests32; modules111; loaded2530 /focused2529. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA:
`77a17f1330f62a1278922d40cb7313c610a7caa29c653b618b5f1e43f872a093`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `af962bad1b00835ecfd193e2de565f2b9131842a`.
Scope: committed-source review and targeted authoring tests, not the formal experiment.

Re-fetched all four committed code/test/PowerShell files and verified complete Git blob identity
against the local copies used for testing:

| File | Reviewed blob |
|---|---|
| C226 benchmark | 82b3c44cc8ae6c36321860453410badc3e139024 |
| C226 tests | 33f8139fb02503bd273e0c3b8f20495fe336f4db |
| run_c226.ps1 | 0e86e6460a11abc6764265a1b7b89e92adaaae38 |
| invoke_c226.ps1 | c8a4a1fd88d4be0700b5a86a7b7c3abb8b0e5875 |

After that comparison,30 targeted tests reran with0 failures/errors in1.053 seconds.
Local Python3.13.5 / PyTorch2.10.0+cpu, threads2.32 methods enumerated; manifest/tensor identities
matched; Python sources and all three embedded runner Python blocks compiled; unbound c### aliases0.

Tests include coupled-matrix connectivity/SPD/rank, actual trace/restoration behavior, and the actual
accepted capsule compiler/response at all four dimensions. The fetched capsule.py exactly matches
Git blob `7f1090fe95b2e3eab3967d00c6730165e34fadfb`; this kernel is not a synthetic implementation.
Other adapter/accounting tests use explicitly synthetic bank/parent-row fixtures.

Source review checked C225/C224 loader and artifact field meanings, the unchanged original n=2
factory and both-arm export anchor, complete raw/index/full-bridge cost accounting, actual checked
solve call order,24 dependencies,196/256 protection arithmetic, argv[1]/postcheck[1..3], early own-test
ordering and launcher guards. Git compare from the published C225 log shows only new files and the
unpinned handoff: no accepted source/test/log/dependency changed or deleted. C227 remains unregistered.

Not run locally: full parent bank/cost-helper integration test31, full historical test32/2529 suite,
Windows PowerShell AST parsing, user-local artifact precheck or formal C226 measurements. Clone was
attempted and failed DNS resolution; the fetched-source sandbox is not a full repository checkout.
Neither synthetic fixtures nor the isolated real-kernel test is represented as those pending checks.
The authoritative runner executes all32 own tests, then2529 focused tests, then the dimension audit.
Failures stop before the next phase and are logged. Review PASS does not replace runtime preflights.

After the review HEAD only review documentation changes; no scientific conditions were altered.

## Stop

Use the active dispatcher and final reviewed HEAD. Judge C226 before C227.
No cleanup, history rewrite, new CI or Actions-storage work. Gate F remains NOT PASSED.
