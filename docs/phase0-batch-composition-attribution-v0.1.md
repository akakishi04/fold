# Phase-0 batch-composition attribution v0.1

C205 explains the valid-negative C204 numeric replay miss without changing the preregistered
`1e-6` tolerance.

## Parent observation

C204 reproduced all learned argmax decisions and the full C203 mixed-channel runtime trajectory, but
the maximum logit deltas were:

```text
necessity 5.0067901611328125e-06
target    5.7220458984375e-06
```

The fixed C204 tolerance was `1e-6`.

## Attribution hypothesis

C199 phase0 did not infer directly over9536 coherent-world rows. It inferred over1768 unique
observable PILOT states and expanded the saved outputs through `local_rows`.

C204 inferred directly over the9536 expanded rows.

The visible72-feature rows are semantically identical after expansion, but the floating-point batch
composition differs.

## Two registered paths

### Canonical unique

```text
1768 unique budget13 states
-> decision debit
-> structured-v2 encode
-> exact canonical72 prefix
-> frozen C181/C188 inference
-> expand outputs by accepted local_rows to9536
-> compare with C199 phase0
```

### Expanded direct

```text
9536 accepted coherent-world states
-> decision debit
-> structured-v2 encode
-> exact canonical72 prefix
-> frozen C181/C188 inference directly on9536 rows
-> compare with C199 phase0
```

For every expanded row:

```text
canonical_unique_prefix[local_rows]
==
expanded_direct_prefix
```

must hold exactly.

## Fixed workload

Across9 frozen model pairs:

```text
canonical unique rows     15,912
expanded direct rows      85,824

canonical forward calls   18
expanded forward calls    90

canonical cell calls      126
expanded cell calls       630
```

Both use:
- BATCH1024;
- CPU float32;
- torch threads2;
- deterministic algorithms;
- identical frozen checkpoints;
- identical raw argmax;
- identical structured-v2 channel layout.

## Fixed gate

Canonical unique path:
- prefix errors0;
- expanded-prefix mismatches0;
- necessity prediction errors0;
- target prediction errors0;
- max necessity logit delta <=1e-6;
- max target logit delta <=1e-6.

Expanded direct path:
- prefix errors0;
- necessity/target prediction errors0;
- both max logit deltas >1e-6.

Attribution:
- each expanded-direct necessity max equals the corresponding C204 whole-loop block max within1e-12;
- each expanded-direct target max equals the corresponding C204 whole-loop block max within1e-12.

PASS means the **gate-breaking maxima** in C204 are already completely reproduced by phase0
duplicate-expanded batching while canonical unique structured-v2 inference remains inside the
original tolerance.

It does not mean every nonzero floating-point difference in every later phase is explained, and it
does not retroactively change C204 from ACCEPTED VALID NEGATIVE to PASS.

## Scope

No acquisition, action runtime, training, new seed, network access, threshold change, or production
runtime modification occurs in C205.
