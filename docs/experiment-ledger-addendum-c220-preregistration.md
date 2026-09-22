# C220 preregistration — frozen learned stack integration

**C219 ACCEPTED PASS. C220 ACTIVE / NOT YET JUDGED. C221 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## One scientific question

Can the accepted learned Writer, Coverage classifier, Port Selector and Reader compose end-to-end
with all checkpoints frozen and no retraining across ASSERT/HOT/COMMIT/REPLACE plus
MISSING/OUT_OF_SCOPE query states?

## Parent checkpoint

C219 scientific execution HEAD:
`5a613ed07c34d1735d20c5849464116cc00d333c`

C219 summary SHA256:
`dbf54bd3cdc5b2fbd82a68a62bcdbaad806b8946b817776d94527a5bdcbaee14`

C219 validation artifact SHA256:
`a380cbb38c686757d4a296c8e557d7b2f304ea72ce4b583185c02099958685d4`

Frozen checkpoint artifacts:

```text
Coverage  1ba50ab3b621b75a0b5c0528f2eb03c6f11e8a0000122563357709d386cee0a1
Writer    3313bb507527b7e4798333c8b8c7f1e0e2ea2f9f2cd513060b505184c87d5c9d
Selector  ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215
Reader    bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af
```

C220 validates all151 C219 source pins and all169 inherited protected inputs, then extends that
checkpoint with C220 OWN files.

## Changed condition

No learned model changes.

New deterministic integration boundary only:

`fold_lm/v05/memory_stack.py`

Coverage gate:
- SUPPORTED/HOT_REQUIRED -> READ;
- MISSING -> distinct MISSING suppression;
- OUT_OF_SCOPE -> distinct OUT_OF_SCOPE suppression.

## Episode plan

Eight episodes:

```text
MISSING alpha
OUT_OF_SCOPE beta
HOT alpha
SUPPORTED alpha
HOT beta
SUPPORTED beta
REPLACE alpha
REPLACE beta
```

Episode SHA:
`99f84e9d05327c8c483b45928676009f6be198e5d568a285d2e893e1279e144f`.

6 readable /2 non-readable.

81 checkpoint combinations.
648 integrated decisions.
486 readable decisions.
162 non-readable decisions.

## Fixed workload

No new training.

```text
Writer forwards      3
Coverage forwards    9
Selector forwards    3
Reader forwards     27
total forwards      42

Writer op slots     18
oracle init writes  12
END_SCOPE ops        3
commit slots        18
```

Operation kind remains oracle ASSERT/REPLACE/END_SCOPE.

## PASS gate

Required exactly:

- all four checkpoint-family roundtrips true;
- Writer target accuracy1.0;
- Selector route accuracy1.0;
- Coverage teacher accuracy1.0;
-81 checkpoint combinations;
-648 decisions;
- integration accuracy1.0;
- expected Coverage accuracy1.0;
- readable answer accuracy1.0;
- non-readable suppression accuracy1.0;
- MISSING/OOS confusions0;
- HOT/COMMITTED mismatches0;
- operation failures0;
- new training steps0.

Complete execution missing a scientific criterion = FAIL.
Source/artifact/schema/regression defects = INVALID / RETRY SAME C220.

## Scope / non-claims

No learned operation-kind selection.
No RETRACT/ASSUME integration.
No acquisition integration.
No natural language.
No joint training.
No memory-cost Gate F comparison.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_stack.py`
- `fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py`
- `tests_lm/test_v05_c220_frozen_learned_stack.py`
- `tools/run_c220.ps1`
- `tools/invoke_c220.ps1`
- this preregistration
- `docs/v5f-frozen-learned-stack-integration-v0.1.md`

Expected:
- source pins158;
- protected inputs182;
- artifacts5;
- C220 tests38;
- regression modules105;
- loaded tests2336;
- exact historical exclusion1;
- focused regression2335.

Manifest SHA256:
`12b5995967abba8c89f2a07c01e6e29afbd96b02db4a0561872a70201deeab52`

Direct repository dependencies:14; all must be parent/OWN pinned.

## Post-authoring review

`post_authoring_review = PENDING`

Do not execute C220 until committed remote bytes are independently reviewed for:
- accepted C219 summary/artifact identity;
- all four frozen checkpoint artifacts/fingerprints;
-151 parent source pins /169 inherited protected inputs;
-158/182 accounting;
- episode plan hash and exact8-state lifecycle;
- actual-state versus expected Coverage semantics;
- distinct MISSING/OOS suppression;
- frozen Writer/Coverage/Selector/Reader forward counts;
-81-combination/648-decision accounting;
- scientific FAIL versus INVALID boundary;
-38 tests /105 modules /2336->2335;
- free-name/import bindings;
- direct dependency coverage;
- runner argv indexes;
- complete PowerShell source-string contract;
- C221 non-registration.
