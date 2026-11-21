# C214 preregistration — V5-F memory capsule closure

**C213 ACCEPTED PASS. C214 ACTIVE / NOT YET JUDGED. C215 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## Scientific question

When accepted C213 observed edit semantics are projected into the existing fixed-port FOLD-R
response capsule, do supported edit sequences produce the same readout as an independent full-memory
reference within registered float64 tolerance?

C214 changes only the semantic-to-numeric bridge. It does not introduce learned memory routing.

## Accepted parent

C213:
- execution HEAD:
  `f59f615b5d409400c9fc5247270a37960ffac197`
- published log commit:
  `78751428cc8397c82488dfd4bf205aa9ac62bc97`
- log SHA256:
  `18a09bfbe223d87f1e0f6b317d07fa72e324485c7af7aa2993f9d6e388850944`
- summary SHA256:
  `370ee39bcd32da4ce797ecfb21ce3b863013c788f6daaaf0fb9a10edac643b43`
- validation-summary SHA256:
  `fca1e55a4da9715292523c84bb490dda7dcb75aead4cf9ad98f76fc0a867b521`
- status:
  **ACCEPTED PASS**

Accepted C213 semantics:
- operations6;
- reads8;
- final memory revision6;
- final evidence revision4;
- exported hypotheses0;
- stale mutation rejected;
- observed-scope END rejected;
- ended-scope mutation rejected.

## Existing numeric prerequisite

Existing fixed-port response capsule source:

`fold_lm/capsule.py`

blob:

`7f1090fe95b2e3eab3967d00c6730165e34fadfb`

No capsule algebra change is allowed inside C214.

## Changed variable

New production reference adapter:

`fold_lm/v05/memory_capsule_bridge.py`

It:
- reads accepted `MemoryState`;
- ignores hypothesis records;
- maps live observed relation keys through a fixed explicit relation-to-port registry;
- sums current factor contributions;
- evaluates the existing response capsule;
- exposes SUPPORTED / OUT_OF_SCOPE / NUMERIC_UNSAFE;
- provides an independent full-system solve comparator.

## Held constant / absent

C214 has:
- learned Writer False;
- learned Reader False;
- Port Selector False;
- H1/H2 compiler False;
- model forward calls0;
- training0;
- fresh seeds0;
- network0.

No Gate E policy/candidate is changed.

## Registered numeric fixture

Dimensions:

```text
variables      4
update rank    2
readout dim    2
dtype          float64
```

Safe relation registry:

```text
rel-alpha-v1
rel-alpha-v2
rel-beta-v1
```

Unsafe control relation:

```text
rel-unsafe
```

Main sequence snapshots7:

```text
initial
ASSERT alpha/v1
REPLACE alpha/v2
ASSERT beta
RETRACT alpha
ASSUME sandbox/temp
END_SCOPE sandbox
```

Required observed-factor counts:

```text
[0,1,1,2,1,1,1]
```

All seven capsule/full-reference statuses must be SUPPORTED.

Registered absolute error ceiling:

```text
max_abs_error <= 1e-10
```

## Hypothesis isolation

After RETRACT alpha, only observed beta remains.

ASSUME temp carries an intentionally unmapped hypothesis relation. Because hypotheses are not
authoritative observed memory, capsule output must remain exactly unchanged.

END_SCOPE sandbox must also leave the observed numeric readout unchanged.

Required:

```text
assumption_readout_delta = 0.0
end_scope_readout_delta  = 0.0
```

## Capability / numerical controls

Unknown observed relation:
- capsule status OUT_OF_SCOPE;
- full-reference status OUT_OF_SCOPE;
- no value exposed.

Registered `rel-unsafe` update:
- capsule status NUMERIC_UNSAFE;
- full-reference status NUMERIC_UNSAFE;
- no value exposed.

OUT_OF_SCOPE and NUMERIC_UNSAFE are distinct outcomes.

## Final semantic state

Required main sequence:

```text
memory_revision        6
evidence_revision      4
evidence_time          3
final exported obs     1
final exported factor  beta
```

## C214 PASS gate

PASS requires:
- exactly7 supported main snapshots;
- all capsule/full-reference statuses match;
- max absolute error <=1e-10;
- factor-count sequence exactly [0,1,1,2,1,1,1];
- final C213 semantic clocks remain6/4/3;
- final exported factor is beta only;
- hypothesis isolation deltas exactly0;
- OUT_OF_SCOPE control exact;
- NUMERIC_UNSAFE control exact;
- non-supported controls expose no value;
- learned Writer/Reader/Port Selector/model-forward calls0;
- accepted C213/C212 evidence remains unchanged.

A complete valid numeric/semantic mismatch is a scientific FAIL for C214.

Source/hash/schema/regression/incomplete-run defects are INVALID / RETRY SAME C214.

## Interpretation boundary

PASS establishes deterministic semantic-to-fixed-port response-capsule closure only.

It does not establish:
- learned Port Selector coverage;
- H1/H2 memory bank behavior;
- chunk commit;
- natural-language Writer/Reader;
- compression or latency advantage;
- Gate F.

## Historical regression immutability

Inherited exact exclusion:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
2116 loaded candidates
-1 exact historical mutable-state test
=2115 focused regression tests
```

## Authoring quality gate

C214 OWN:
- `fold_lm/v05/memory_capsule_bridge.py`
- `fold_lm/v05_benchmarks/gate_f_c214_memory_capsule_closure.py`
- `tests_lm/test_v05_c214_memory_capsule_closure.py`
- `tools/run_c214.ps1`
- `tools/invoke_c214.ps1`
- this preregistration;
- `docs/v5f-memory-capsule-closure-v0.1.md`.

Expected:
- source pins115;
- protected inputs217;
- output artifacts5;
- new tests32;
- regression modules99;
- focused regression **2115**.

Scientific manifest SHA256:

`dc2354bd35d94ef0d8b7e5f4c6bed820f5166f0ce20948df612b30d1b0465915`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:

- accepted C213 summary/validation identity;
- fixed response-capsule source identity;
- exact relation-to-port fixture;
- capsule/full-reference formula parity;
- hypothesis exclusion from numeric updates;
- replacement/retraction factor semantics;
- OUT_OF_SCOPE versus NUMERIC_UNSAFE distinction;
- error tolerance and seven-snapshot counts;
- no learned routing/H1-H2/model path;
- semantic regression counts;
- Python free-name/import bindings;
- runner argv indexes/order;
- PowerShell parser chain;
- source/protected/test/module/artifact counts;
- C215 non-registration.

Until review passes:

`post_authoring_review = PASS`

review HEAD:
`7453cf9b62b86a3970e2a549028d604e329ec525`

Committed remote review verified accepted C213 summary/validation identity, exact existing response-
capsule source identity, all seven C214 OWN files, manifest registration,115 source pins /217
protected inputs,32 tests, semantic2116-loaded/2115-kept regression accounting, zero unbound
executable c### aliases, exact18 parent-summary runner argv and postcheck argv[1..20] wiring,
launcher parser-before-execution ordering and accepted C213 local summary path.

The numeric fixture was independently recomputed: all seven safe snapshots remain SPD, capsule vs
full-reference maximum absolute error is approximately 1.11e-16 (well below the registered 1e-10
ceiling), and the registered unsafe control has a negative minimum eigenvalue while the safe
relations do not. Hypothesis records are excluded before relation lookup, preserving C213
authoritative-observation semantics. C215 remains unregistered.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected:
- active_experiment C214;
- repository/Python preflight;
- source/artifact precheck PASS;
- focused regression2115/2115;
- seven capsule/full-reference snapshots;
- capability/numerical controls;
- RESULT / POSTCHECK;
- remote log publication.

Judge C214 before any C215 registration.
