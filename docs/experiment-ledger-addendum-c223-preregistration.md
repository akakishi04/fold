# C223 preregistration — retained request freshness

**C222 ACCEPTED PASS. C223 ACTIVE / NOT YET JUDGED. C224 NOT REGISTERED.**
Gate E PASSED. Gate F NOT PASSED.

## One question and changed condition

Can a session-owned monotonic request lease prevent reuse of old C221 request closures after state
publication, while preserving current C222 decisions with all learned checkpoints frozen?

Change only the deterministic session/request freshness boundary. Keep the exact C222 lifecycle,
all learned checkpoints, operation kinds, scopes and query descriptors. No answer cache, training,
acquisition, new semantic tasks or memory-cost optimization.

## Accepted parent

Scientific HEAD: `ae4286ac9b79cd34eb8bdfd1d72ae2e27c308889`.
Published log commit: `ad285c5a318d7ac7b0067e07ffe06fb02edfb8e8`.
Summary SHA256: `18321ace4ade112fe227d4836867223a5ec609761c89015b704e9e14b629c62e`.
Validation SHA256: `9d6916dfcaec497680b94ae2b280dc9ab98f3da17aac7447a8b2e8b150d9b40b`.
Lifecycle plan SHA256: `1b94c0af7c1d828f54c5519dd9169a9e2a7985ddd91b155a72d312d39e26a828`.
Local summary:
`runs/c222-v5f-withdrawal-lifecycle-60ba479f7d2b46ff957b5d2a21bf865c/summary.json`.

All171 parent source pins and207 protected inputs are validated, including inherited checkpoint
artifacts. Reuse the same C220 fingerprint-checked model restoration and C222 timeline helpers.
Validate all five C222 output artifacts. The actual parent live-decisions fields are adapted and
checked for1296 unique successful seed/label/query identities and Coverage/answer/action/trace/
bank-read meanings. Parent answers are scorer-only and never enter RequestSession.

## Frozen families and lifecycle

Writer218001/218002/218003; Coverage219001/219002/219003;
Selector217001/217002/217003; Reader216001/216002/216003.

One continuing bank/state chain per Writer; same eight C222 stages, alpha and beta queries.
Create a session at anchor_only and publish each subsequent snapshot:7 publications/session.
Publishing always increments generation; it does not modify semantic/evidence clocks.

Fresh requests must reproduce1296/1296 accepted parent decisions. A current beta_committed request
is reused without publication for81 positive controls.

## Retained request matrix

Both requests from every previous snapshot are attempted at every later publication:
28 prior/current pairs x2 queries x81 checkpoint combinations =4536 stale attempts.

Require4536 STALE_REQUEST results, no exposed DispatchResult, trace exactly `freshness`, and zero
Coverage/Selector/provider/bank/Reader calls. Include the representation-only commit with unchanged
memory_revision and incremented storage_epoch.

## Unguarded replay controls

Four intentionally unguarded old beta requests per checkpoint combination:
- current beta_committed, old beta_hot;
- current beta_replaced, old beta_committed;
- current beta_retracted, old beta_replaced;
- current project_ended, old beta_retracted.

The unchanged C221 dispatcher must reproduce the old recorded behavior and differ from current
behavior in all324 controls. This exposes the reason for the new guard; it does not authorize
bypassing it in normal execution. The corresponding guarded old requests are part of the stale matrix.

## Fixed PASS gate

Fresh decisions/success/parent parity1296; stale decisions/success4536; same-generation repeats81;
unguarded replay controls324. All four groups require100% registered success.
Stale result exposures0. Writer target accuracy1.0. Model fingerprints unchanged. Training0.

Successful invocation counts:

| Group | Coverage | Selector | Provider | Bank reads | Reader |
|---|---:|---:|---:|---:|---:|
| Fresh | 1296 | 891 | 891 | 891 | 891 |
| Stale guarded | 0 | 0 | 0 | 0 | 0 |
| Same-generation repeats | 81 | 81 | 81 | 81 | 81 |
| Unguarded replay controls | 324 | 243 | 243 | 243 | 243 |

Writer forwards3. Total model forwards4134 at PASS. CPU, threads2, deterministic algorithms.
No throughput or total-memory-cost claim is made from these counters.

A complete run missing prediction/parity/rejection/control/call-count criteria is scientific FAIL.
Malformed source/artifact/model output, incomplete matrix or schema defect is INVALID / RETRY SAME
C223. Successful model-dependent counters are not imposed as execution-validity preconditions.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_request_lease.py`
- `fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py`
- `tests_lm/test_v05_c223_request_freshness.py`
- `tools/run_c223.ps1`
- `tools/invoke_c223.ps1`
- this preregistration
- `docs/v5f-retained-request-freshness-v0.1.md`

Source pins178 = parent171 + OWN7.
Protected inputs220 = inherited207 + parent summary/artifacts6 + OWN7.
Deciding dependencies19 = C220 direct set14 + C220 benchmark + memory_dispatch + C221 benchmark +
C222 benchmark + new memory_request_lease. Every used repository helper, including lazy imports,
must be covered. No accepted production source/test is changed, moved or removed.

Artifacts5: freshness-plan, fresh-decisions, stale-decisions, replay-controls, validation-summary.
Raw outputs and checkpoint files remain ignored under runs/.

New tests34; modules108; loaded2436; focused2435. Retain only the inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA256:
`ef0d7db9c3ef24da2076c8811076e53c6d46abeff19b363163a0c352f0d0872d`.

## Post-authoring review

`post_authoring_review = PENDING`

Author environment: Python3.13.5 /PyTorch2.10.0+cpu /NumPy2.3.5.
32 targeted tests executed successfully,0 failures/errors,0.306 seconds. All34 methods enumerated;
new Python sources and three embedded runner Python blocks compiled; manifest hash matched.
The dispatcher copy used in testing matches the accepted Git blob
`da7efd7cf6c1c9a748ed35953df1a26a6e4c30fe`.

Synthetic model/provider fixtures exercised the full1296-fresh/4536-stale/81-repeat/324-replay
matrix, exact invocation counters, wrong-session and synchronous-publication controls, and the
parent-field adapter. This is authoring validation, not science using accepted checkpoint bytes.

Not run in the authoring environment: the two parent-tree-dependent new tests, actual numeric C222
trajectory, full2435 historical regression, Windows PowerShell AST parser and local-only parent
artifact/checkpoint science. A repository clone was attempted but DNS resolution was unavailable.
No mock or synthetic result is represented as any of those checks.

After all files are committed, retrieve the actual remote files, compare their blob IDs with tested
copies and independently review generation/owner/factory binding, actual call ordering, parent
artifact semantics,19 dependency coverage,178/220 accounting, manifest, suite arithmetic, exact
runner arguments, PowerShell preflight and C224 non-registration. Record the review HEAD and limits.
The authoritative runner executes all34 new tests before the2435 focused suite, then science.

## Interpretation and stop

Explicit publication of trusted immutable state is required. In-place tensor mutation, skipped
publication, malicious bypass, concurrent execution, cross-process leases, model-version changes
and answer-cache invalidation are outside scope. This is an in-process correctness boundary, not
security enforcement. Old snapshots retained for evaluation do not demonstrate bounded storage.

The fixture remains one synthetic lifecycle crossed with81 checkpoint combinations, not thousands
of independent unseen problems. Judge C223 before any C224 registration. Gate F remains NOT PASSED.
