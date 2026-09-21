# C213 preregistration — V5-F memory operation contract

**C212 ACCEPTED PASS / GATE_E_PASSED. C213 ACTIVE / NOT YET JUDGED. C214 NOT REGISTERED.**
Gate F remains **NOT PASSED**.

## Scientific question

Can a deterministic V5-F memory bridge preserve ASSERT/RETRACT/REPLACE/ASSUME/END_SCOPE/QUERY
semantics across factor identity, scope, exact memory revision and provenance while exporting only
observed records into authoritative V5 EvidenceState?

C213 isolates this semantic boundary before any learned memory policy or FOLD-R numeric capsule is
introduced.

## Accepted parent

C212:
- execution HEAD:
  `4d1436c1ba12721b1c802fb5d76e359b3a62841f`
- published log commit:
  `3163014d0672ab8905a06c37ae6698e9ea9c80bc`
- log SHA256:
  `146dee38ca4823ac0bf8aeabd9c4defec92d967b184adc7e5f441b5526943ca0`
- summary SHA256:
  `3685c37dd6e2c7fea92723548446b86f4ee8d068f7dd00afe3e2337f8bca8bce`
- formal outcome:
  **GATE_E_PASSED**
- policy-episode evaluations432
- source pins99
- protected inputs189

Accepted Gate E decision artifact SHA256:

`41cb9aa4bc092934eff080cc07d16edbb692822526d5d81ae35ed8d7abccab0a`

## Changed variable

New production reference module:

`fold_lm/v05/memory_bridge.py`

It adds only:
- canonical memory operation types;
- immutable hot-memory reference state;
- exact memory revision;
- evidence revision/evidence time separation;
- factor/scope lifecycle;
- read status contract;
- observed-only EvidenceState export.

## Held constant / not introduced

C213 has:
- learned Writer False;
- learned Reader False;
- Port Selector False;
- FOLD-R capsule False;
- H1/H2 compiler False;
- model forward calls0;
- training0;
- fresh seeds0;
- network0.

No existing Gate E candidate or acquisition policy is changed.

## Existing provenance prerequisite

The existing V5 state contract is pinned exactly:

`fold_lm/v05/state.py`
blob:
`aa3f4938f6b5d403d8ee05c4220f686695cef3f0`

Its authoritative rule remains:

- `EvidenceState` accepts only `ProvenanceKind.OBSERVED`;
- hypothesis provenance cannot silently enter authoritative evidence.

## Operation vocabulary

```text
ASSERT
RETRACT
REPLACE
ASSUME
END_SCOPE
QUERY
```

Observed mutations:
- ASSERT;
- REPLACE;
- RETRACT.

They advance:
- memory revision;
- evidence revision;
- evidence time monotonically.

Hypothesis/scope mutations:
- ASSUME;
- END_SCOPE.

They advance memory revision only.

## Read-status contract

Exact distinct statuses:

```text
SUPPORTED
MISSING
RETRACTED
OUT_OF_SCOPE
STALE_REVISION
```

Required distinctions:
- retracted != missing;
- ended scope -> OUT_OF_SCOPE;
- old requested revision -> STALE_REVISION;
- never-seen factor in live scope -> MISSING.

## Edit rules

ASSERT:
- requires fresh `(scope_id,factor_id)`;
- observed provenance only.

REPLACE:
- requires a live observed factor;
- preserves factor identity;
- replaces relation/provenance.

RETRACT:
- requires a live observed factor;
- removes live record;
- leaves tombstone.

ASSUME:
- requires non-global live scope;
- creates hypothesis provenance;
- never advances evidence revision/time.

END_SCOPE:
- global scope forbidden;
- cannot silently discard live observed records;
- removes scoped hypothesis state;
- scope becomes OUT_OF_SCOPE.

Mutating operation with stale expected memory revision:
- rejected;
- no state change.

QUERY with stale expected memory revision:
- non-mutating `STALE_REVISION` read result.

## Registered deterministic fixture

Successful mutations6:

```text
ASSERT global/alpha
REPLACE global/alpha
ASSERT project/beta
RETRACT global/alpha
ASSUME sandbox/temp
END_SCOPE sandbox
```

Reads8.

Required status totals:

```text
SUPPORTED       3
MISSING         2
RETRACTED       1
STALE_REVISION  1
OUT_OF_SCOPE    1
```

Required final state:

```text
memory_revision      6
evidence_revision    4
evidence_time        3
live records         1
tombstones           1
ended scopes         1
final exported obs   1
final export binding 1
hypothesis exported  0
```

Required rejection controls:

```text
stale mutation rejected             True
END_SCOPE with observed record      rejected
mutation into ended scope           rejected
```

## C213 PASS gate

C213 PASS requires all registered fixture counts/statuses exactly, plus:

- assumption read provenance kind = hypothesis;
- hypothesis export count0;
- final export contains only current observed beta;
- final EvidenceState revision4/time3;
- learned writer calls0;
- learned reader calls0;
- FOLD-R capsule calls0;
- model forward calls0;
- accepted C212 Gate E evidence remains unchanged.

A semantic count/status miss is a complete scientific FAIL for this contract.

Source/hash/schema/regression/incomplete-run failure is INVALID / RETRY SAME C213.

## Interpretation boundary

PASS means the reference memory operation boundary is coherent enough to serve as the next V5-F
foundation.

PASS does not establish:
- numerical response-capsule correctness under edits;
- compression/correction closure;
- H1/H2 memory-bank behavior;
- learned Writer/Reader/Router quality;
- natural-language memory extraction;
- Gate F.

## Historical regression immutability

Inherited exact exclusion:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
2084 loaded candidates
-1 exact historical mutable-state test
=2083 focused regression tests
```

## Authoring quality gate

C213 OWN:
- `fold_lm/v05/memory_bridge.py`
- `fold_lm/v05_benchmarks/gate_f_c213_memory_operation_contract.py`
- `tests_lm/test_v05_c213_memory_operation_contract.py`
- `tools/run_c213.ps1`
- `tools/invoke_c213.ps1`
- this preregistration;
- `docs/v5f-memory-operation-contract-v0.1.md`.

Expected:
- source pins107;
- protected inputs203;
- output artifacts5;
- new tests28;
- regression modules98;
- focused regression **2083**.

Scientific manifest SHA256:

`daadfa2445e72512553e400373a0a479850bf8d5657713d068f0a164e488cc79`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:

- accepted C212 identity and Gate E decision artifact;
- V5 state provenance blob;
- exact MemoryOp field contract;
- observed versus hypothesis revision behavior;
- factor/scope lifecycle;
- EvidenceState export filtering;
- read-status distinctions;
- stale mutation immutability;
- no numeric capsule/learned memory path;
- semantic regression counts;
- Python free-name/import bindings;
- runner argv indexes/order;
- PowerShell parser chain;
- source/protected/test/module/artifact counts;
- C214 non-registration.

Until review passes:

`post_authoring_review = PASS`

review HEAD:
`42b8ae80733e6c5547ba0f679c27aa0cec40dd7a`

Committed remote review verified accepted C212/Gate E identity and decision artifact, exact V5 state
provenance blob, all seven C213 OWN files, manifest/hash registration, 107 source pins /203
protected inputs, 28 tests, semantic2084-loaded/2083-kept regression accounting, zero unbound
executable c### aliases, exact six-operation/eight-read fixture, distinct read-status contract,
observed/hypothesis revision split, observed-only EvidenceState export, stale-write rejection,
scope/factor lifecycle, runner argv[1..17]/postcheck argv19 wiring, launcher parser ordering and
accepted C212 local summary path, and C214 non-registration.

No learned Writer/Reader, Port Selector, FOLD-R capsule, H1/H2 compiler or model-forward path is
present in C213.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected:
- active_experiment C213;
- repository/Python preflight;
- source/artifact precheck PASS;
- focused regression2083/2083;
- deterministic memory-contract fixture;
- RESULT / POSTCHECK;
- remote log publication.

Judge C213 before any C214 registration.
