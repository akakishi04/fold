# C230 acceptance and C231 evaluation boundary

## Formal verdict

**C230 ACCEPTED PASS (measurement/correctness audit). Gate F NOT PASSED.**

Scientific execution HEAD: `58ec6d1497e4729d394307f5c1316d9e69f2ee8e`.
Published log commit: `ad8a657842491a74d8aa5e3101893aaa98a335ca`.
Log SHA256: `de95033043db1b65fd929e7d2cf684e0192b8eda3ae49e74f53d97cf6394e580`.
Summary SHA256: `3eeb739eaf37c8b0d1ef4f94d5eec46281ea8721c1cea67fb51234f8bd7fca7c`.
Local summary: `runs/c230-v5f-prepared-capsule-42695282c3e6402f9fe7616ba3641099/summary.json`.

Own40 tests passed in1.350s. Focused2665 tests passed in52.628s. Source/artifact precheck,
quality parity, parent-export parity, reduced-factor reuse, artifact postcheck and final execution
validity all passed. Inputs preserved; tracked tree clean. The publication commit adds only the
console log and receipt and has the registered execution HEAD as its parent.
Acceptance relies on published evidence and recorded local postchecks, not a reviewer rerun of the
user-local artifacts.

Accepted outputs:
- measurements.json: `d72afb4423933d673983f6ea850e8064c6b84072ae061bbca935c2f2d5705afc`
- quality-checks.json: `fd69a11348aa806acc3c5d1918790e1ecd2d3b5068f037d3339ae44b9d379584`
- reuse-exports.zip: `c41e08ad164c86e3728b26deaa87ca2d329c9924f249ed08ea3c3182cc1e46a7`
- reuse-plan.json: `c93b9845cd10c4cab316b01da41f3e03f443f75b078c8912fc27c6c23c299b95`
- validation-summary.json: `8f0ebfb7c769f1bc9eebceff02d51c55e1a94dd52ee0ec67b73650f2dda683a9`

## Measured interpretation

Ratios are median prepared update+query time divided by the indicated comparator's median;
preparation and setup are separate. Ratios below1 favor the prepared route.

| n | queries/update | prepared / original H1H2 | prepared / full-factor reuse |
|---:|---:|---:|---:|
| 2 | 1 | 0.676382 | 2.208722 |
| 2 | 4 | 0.466394 | 2.003113 |
| 2 | 16 | 0.473613 | 2.615769 |
| 16 | 1 | 0.659630 | 1.921868 |
| 16 | 4 | 0.510712 | 2.167188 |
| 16 | 16 | 0.469840 | 2.492751 |
| 64 | 1 | 0.674358 | 1.887021 |
| 64 | 4 | 0.543868 | 2.303726 |
| 64 | 16 | 0.447014 | 2.302884 |
| 256 | 1 | 0.670789 | 1.333235 |
| 256 | 4 | 0.624263 | 1.269740 |
| 256 | 16 | 0.446354 | 0.893118 |

The intervention reduces update+query time by about32.4%-55.4% versus original H1H2 across all12
cells. Against the stronger full-factor comparator it is slower in11/12 cells. Only n256/q16 is
about10.7% faster in update+query time. This lone cell is not a general crossover threshold.

At n256/q16: prepared stream19.6411ms versus full-cache21.9916ms. Cold-inclusive registered phase
sums are prepared29.6598ms versus full-cache28.3935ms: including setup removes even that cell's
advantage. These are medians of three descriptive trials, not significance-tested evidence.

At the same cell, serialized audit data: original H1H2 283277B, prepared283799B, full-cache282860B
plus272393B cache =555253B. Prepared adds72 numerical bytes plus metadata (522B serialized cache),
not a claim of72B total memory. Raw evidence/index/full bridge are retained. Reachable object/tensor
estimates are not process peak RAM/VRAM or language-model size.

## Adoption decision

1. Retain the prepared route as an **opt-in, narrow CPU-float64 fixed-W inference candidate**.
2. Do not replace the reference/default runtime or infer general speed/storage superiority.
3. Keep deterministic semantic/safety reference paths and all accepted tests unchanged.
4. Stop this local numeric-memory optimization track here; do not search for another favorable
   workload merely to obtain a win. Gate F remains open rather than being waived.
5. Return to model-level language/reasoning evaluation. First establish the evaluation interface
   and its actual implementation scope before training larger models or claiming general ability.

The existing `fold_lm/v05/language_task.py` is an uncompressed V5-B fixed-slot, teacher-routed byte
front-end/core/readout, not the integrated learned H1/H2 stack and not the final V5-G runtime.
`fold_lm/model.py` is a separate older local-attention vertical slice; do not silently substitute it
for v0.5. No pending 20M-40M training proposal is formally adopted by this decision.

## Proposed next single question

C231 will audit whether the existing V5-B byte model can be evaluated through an explicit
prefix-only next-byte likelihood/generation harness without target leakage, with stable model
identity and reproducible metrics. It will use tiny untrained models only as instrument checks:
no training, no language-ability PASS, no general benchmark ranking, no memory-path modification.

C231 is NOT REGISTERED by this acceptance document; see the current handoff/preregistration.
