# C209 preregistration — visible-only candidate projection

**C208 ACCEPTED VALID NEGATIVE. C209 ACTIVE / NOT YET JUDGED. C210 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can a deterministic visible-only candidate projection transform every frozen C207 structured-v2
packet into the legacy C181/C188 seven-node/four-fact model-input contract while:

- preserving Boolean semantics for every completion;
- preserving original fact order/indices;
- keeping synthetic padding facts impossible as acquisition targets;
- never reading scorer data;
- never mutating the trusted runtime/evidence TaskView?

C209 performs **no learned forward**.

## Accepted parent

C208:
- execution HEAD:
  `60d7b38bd0d44662f58b55b32cb09c4d9472f8fe`
- summary SHA256:
  `413e88c73c9f7af5403f8f4afa13d9b9245d3201788c41bb5713abc6d7125dc4`
- status:
  **ACCEPTED VALID NEGATIVE**

Frozen C207 visible artifact:

`c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`

C208 established:
- as-is combined compatibility16/144;
-128 incompatible;
- dominant blocker legacy7-node/4-fact shape;
- C188 also rejects stale/conflict when shape is legal.

## Projection intervention

New explicit model-input-only module:

`fold_lm/v05/candidate_input_projection.py`

Projection schema:

`fold-candidate-input-projection-v1`

Rules:

1. preserve original fact indices/order;
2. preserve an original OBSERVED fact exactly, including value/reference;
3. every other original fact becomes UNOBSERVED only in the candidate projection;
4. normalized projection facts carry no value/reference;
5. append OBSERVED TRUE architectural constants until there are4 facts;
6. after each appended TRUE fact, append `old_root AND TRUE`;
7. resulting candidate packet must contain exactly7 nodes and4 facts;
8. padding facts map to no original fact (`-1`) and remain OBSERVED;
9. trusted source v2 packet remains unchanged and is never replaced by the projection.

Padding constants are architectural model-input constants, not external observations or trusted
runtime evidence.

## Fixed workload / structural totals

Frozen episodes:

```text
144
```

Original fact-count distribution:

```text
1 fact    16
2 facts  112
4 facts   16
```

Required synthetic TRUE facts:

```text
272
```

Required non-OBSERVED status normalizations beyond already-UNOBSERVED:

```text
32
```

These are the16 STALE +16 CONFLICT visible cases.

## Exhaustive semantic control

For every episode enumerate every completion of the **original** facts, fixing all padding facts TRUE.

Registered assignments:

```text
16 one-fact  * 2  =  32
112 two-fact * 4  = 448
16 four-fact *16  = 256
------------------------
total              = 736
```

Required semantic errors:

```text
0 /736
```

## Pair-preservation control

C207 has exactly50 dependence units whose two source-visible packets are byte-identical.

Required:

```text
equal source units      50
equal projected units   50
projection pair errors   0
```

Projection must not introduce condition-specific distinctions into an originally identical pair.

## Candidate-contract controls

For every projected packet:

- C178 `prepare_pair` must accept;
- C188 `missing_mask` must accept;
- C188 `leaf_positions` must accept.

Required:

```text
necessity-compatible    144
target-compatible       144
combined-compatible     144
dummy-missing errors      0
```

All original indices0..N-1 remain unchanged.

Every dummy indexN..3 must:
- map to -1 / no original fact;
- be OBSERVED TRUE;
- never appear as missing under C188.

## Source/runtime purity controls

Required over all144 episodes:

```text
source packet unchanged        144
source digest matched          144
index mapping valid            144
observed originals preserved   144
nonobserved normalized safely  144
dummy contract valid           144
trusted_runtime_mutated        False
scorer_used                    False
model_forward_calls            0
```

## Fixed PASS gate

All registered structural, semantic, pair, validator and purity counts above must match exactly.

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C209**.

## Scope / non-claims

C209 registers:
- candidate-interface projection addedTrue;
- model forward calls0;
- scorer usedFalse;
- baseline measurementFalse;
- training0;
- fresh seeds0;
- network calls0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS means only that the representation intervention is feasible and semantics-preserving.

PASS does not establish:
- learned necessity/target quality after projection;
- channel/action quality;
- baseline performance;
- Gate E numerical margins;
- independent holdout;
- final Gate E.

## Historical regression immutability

Inherited exact historical exclusion remains:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
1974 loaded candidates
-1 exact historical mutable-state test
=1973 executed focused regression tests
```

## Authoring quality gate

C209 OWN:
- `fold_lm/v05/candidate_input_projection.py`
- `fold_lm/v05_benchmarks/gate_e_c209_visible_only_candidate_projection.py`
- `tests_lm/test_v05_c209_visible_only_candidate_projection.py`
- `tools/run_c209.ps1`
- `tools/invoke_c209.ps1`
- this preregistration;
- `docs/visible-only-candidate-projection-v0.1.md`

Expected:
- source pins77;
- protected inputs149;
- output artifacts5;
- new tests24;
- focused regression **1973**;
- regression modules **94**.

Scientific manifest SHA256:

`c6faab8b8b74fdf6b15dc7dbe3481def184e0dbdb04859a0b9e9ff90660b3879`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently re-fetched and reviewed for:

- accepted-valid-negative C208 identity/source artifacts;
- frozen C207 visible artifact identity;
- projection uses only structured-v2 visible state;
- no scorer artifact load/use;
- original runtime packet immutability;
- original fact-index preservation;
- dummy TRUE construction and non-missing control;
- exhaustive736-assignment semantic equivalence;
-50 equal-source-unit preservation;
- actual C178/C188 validator acceptance;
- semantic regression counts from actual loader/suite;
- Python free-name/import bindings across projection/benchmark/tests;
- PowerShell dispatcher -> launcher -> runner parser chain;
- runner CLI argument order/indexes;
- source/protected/test/module/artifact counts;
- C210 non-registration.

Until review passes:

`post_authoring_review = PASS`

review HEAD:
`1ad5adabf83307bf492ddeeaca03a40fb4ba0cf1`

Committed remote review verified accepted-valid-negative C208 identity and all6 C208 OWN blobs,
frozen C207 visible identity, projection module imports only standard library + structured-v1/v2,
no scorer/benchmark dependency in the projection API, original fact-index/status transformation
rules, TRUE-padding/AND wrappers, source-packet immutability,736 exhaustive semantic checks,
50 equal-source-unit preservation, actual C178/C188 validator calls, 24 C209 tests,
semantic1974-loaded/1973-kept regression accounting, zero unbound executable c### aliases across
projection/benchmark/tests, runner CLI indexes, dispatcher->launcher->runner PowerShell parser
chain, 77 source pins /149 protected inputs /5 artifacts, and C210 non-registration.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:
- active_experiment = C209
- C209 repository preflight
- Python syntax preflight
- source/artifact precheck PASS
- focused regression1973/1973
- RESULT
- POSTCHECK
- remote log publication

Judge C209 before any C210 registration.
