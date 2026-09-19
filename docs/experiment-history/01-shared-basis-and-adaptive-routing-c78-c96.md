# Shared-Basis and adaptive routing — C78-C96

## Scientific subject

This sequence established two foundations:

1. whether Shared-Basis can reduce model/storage/VRAM cost without losing the accepted dense semantics;
2. whether a small learned controller can skip unnecessary computation and remain practical at large width.

## Shared-Basis integration — C78-C83

### C78 — production opt-in integration
Valid execution, but the preregistered production integration gate failed because long-training
validation tensors exceeded the fixed allclose criterion. Scores and semantics still matched.
This was a **scientific negative**, not evidence that inference algebra was wrong.

### C79 — arithmetic-drift diagnosis
PASS. Reusing the C78 failure seeds localized the discrepancy to floating-point arithmetic order
during GEMM-native optimization. Production layout + materialized arithmetic matched the reference
exactly.

### C80 — execution policy
PASS. Accepted policy:

```text
training  -> materialized arithmetic
inference -> GEMM-native arithmetic
```

The same persistent Shared-Basis checkpoint is used in both modes.

### C81 — large-shape runtime / resident-memory
PASS on widths up to 5120 and selected rank fractions. At width5120 the Shared/Dense median latency
ratios remained within the preregistered 1.20 ceiling and outputs were allclose.

### C82 — serialized artifact
PASS. Representative width3072 serialized ratios:
- 1/16: 0.713668
- 1/8: 0.760522
- 3/16: 0.807377

No materialized routed-weight bank was stored in the Shared-Basis state_dict.

### C83 — operational VRAM/headroom
PASS. At width5120 all tested profiles saved >0.15 GiB device headroom versus Dense; measured gains
were roughly 0.20-0.33 GiB depending on rank fraction and batch.

**Gate C passed in this registered scope after C83.**

## Adaptive learned routing — C84-C96

### C84-C85 — action semantics and router plumbing
C84 established the oracle rule HOLD->ANSWER/no-op and UPDATE->COMPUTE.
C85 showed the supervised production-facing router could reproduce that simple action policy.

### Sparse-runtime diagnosis
The next experiments separated logical compute reduction from actual eager runtime cost. The tiny
shape showed that fewer logical updates did not automatically mean lower latency; sparse indexing
and router overhead could dominate.

### C90-C95 — compact control-lane diagnosis
- C90 selected hidden width4 as the smallest passing compact router at the small task.
- C91 was a **valid negative** at widths3072/5120: the selected full-width hidden4 router lost
  routing quality, so its low runtime numbers were not accepted as speed evidence.
- C92 showed this was broader than simple delayed convergence of hidden4.
- C93-C94 isolated a fixed-width control lane as substantially more width-independent.
- C95 passed prospective fresh-seed held-out validation with action accuracy and minimum class recall 1.0.

### C96 — production control-lane runtime/VRAM
PASS:
- held-out and runtime action accuracy: 1.0
- minimum class recall: 1.0
- logical compute reduction: 50%
- worst learned/fixed device ratio: 0.649631
- worst learned/fixed wall ratio: 0.653782
- router/core persistent ratio maximum: 1.3481e-06
- outputs allclose

**Gate D passed in the registered synthetic adaptive-routing/runtime scope after C96.**

## Durable conclusions

- Shared-Basis is operationally useful only with an explicit arithmetic policy: materialized train,
  GEMM-native inference.
- Operational VRAM/headroom, not just checkpoint bytes, is the primary "lightness" metric.
- Dynamic routing can save real runtime at large width, but only after decoupling the controller
  representation from core width.
- Logical sparsity by itself is not runtime speed evidence.

## Cleanup implication

Many one-off C78-C95 diagnostic runners can eventually become archive candidates, but the production
Shared-Basis/controller implementations, Gate C/D decision documents, and tests that protect their
accepted contracts remain active architecture evidence.
