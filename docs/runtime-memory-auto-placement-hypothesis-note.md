# Runtime Memory Auto-Placement Hypothesis Note

Status: **idea / hypothesis only**. This is not an accepted v0.5 requirement, not an implemented runtime contract, and not part of the active C-series experiment state.

## Idea

At model load time, let the frontend/runtime receive a user-selected memory budget (for example an allowed VRAM amount, optionally with RAM/cache limits), then automatically allocate FOLD runtime state across GPU VRAM, host RAM, and persistent storage instead of requiring the user to configure every component independently.

Example frontend intent:

```text
GPU budget: 12 GiB
Host RAM budget: 24 GiB
```

The loader/runtime would derive a placement plan such as:

```text
VRAM
- shared basis / always-hot weights
- neural router
- active/hot modules
- attention KV cache
- working-state tensors
- current FOLD-R numeric state
- execution headroom / temporary buffers

RAM
- cold or warm module representations
- evidence payload/cache selected for near-term reuse
- retrieval/index working sets
- module staging/prefetch buffers

SSD / external storage
- cold long-term memory
- inactive modules/artifacts
- raw evidence and larger retrieval stores
```

The configured number should therefore be treated as a **budget**, not as a request to fill all memory. The planner must reserve safety headroom for transient kernels, materialization/decompression buffers, CUDA graphs/workspaces where applicable, and workload-dependent KV/working-state growth.

## Why it may fit FOLD

FOLD separates total stored capability from the subset used on one inference step. Sparse routing and shared-basis/module compression make it plausible to keep the always-hot core resident while staging colder modules only when needed. A budget-driven loader could make that distinction usable from the frontend without exposing every low-level placement knob.

It could also support machine-dependent profiles without changing model semantics: a larger GPU could keep more modules/KV/cache resident, while a smaller GPU could use RAM-backed staging or tighter cache budgets.

## Candidate planner inputs

Potential inputs, if this idea is later formalized:

- maximum usable VRAM, rather than physical VRAM alone;
- optional RAM/cache limits;
- precision / quantization / codebook representation;
- maximum or target context/KV budget;
- working-state dimensions and internal-step policy;
- hot-module residency target and observed routing frequency;
- decompression/materialization workspace requirements;
- latency-vs-capacity preference;
- minimum safety headroom.

## Candidate invariants

Any future implementation should probably preserve at least these boundaries:

1. Do not silently exceed the user budget in steady-state accounting.
2. Do not count only model parameters; include KV, working state, decoded/materialized buffers, metadata and temporary workspaces as required by the existing accounting rules.
3. Placement changes must not silently alter model semantics or evidence/provenance state.
4. Missing/cold modules must have an explicit miss/staging behavior; no hidden unlimited CPU/SSD fallback when benchmarking GPU residency.
5. Report the derived plan and measured peak RAM/VRAM so automatic placement remains auditable.
6. Reserve headroom instead of filling VRAM to 100% at load time.

## Open questions

- Should the frontend expose only one VRAM budget, or separate `model`, `KV/state`, and `workspace` limits?
- Should hot/cold module placement be static at load, adaptive at runtime, or both?
- How should prefetching interact with sparse routing and compute/acquisition budgets?
- What eviction metric is appropriate: recency, routing frequency, predicted next-use, transfer cost, or a learned policy?
- Can a deterministic reference placement policy be defined before experimenting with adaptive policies?
- How much quality/latency variance is acceptable between hardware profiles while preserving the same semantic model?

## Non-claim

This note only records the hypothesis that **frontend-selected resource budgets could drive automatic runtime placement**. It does not claim that automatic allocation is currently implemented, that RAM/SSD offload will be faster than a fully resident model, or that a specific placement/eviction policy is correct.
