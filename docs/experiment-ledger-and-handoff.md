# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C194 ACCEPTED PASS. C195 ACTIVE / NOT YET JUDGED. C196 NOT REGISTERED.**

C194 execution HEAD:
`32e62fe1b2e8318daa766aff1bfcc1f0fc49d95a`
C194 acceptance commit:
`53b9d957763a76003321b63af2ed4255b5a6b835`
C194 summary SHA:
`6cdb274da944bc87cea29f2e093d4acdec6035dae6978adaf469f1d9b4dfa084`.

C194:1581/1581;85824 episodes; scientific errors0; exact C193 prediction/logit/read-depth
replay; generic bounded loop equivalent to accepted hand-unrolled C193 path.

## C195 invalid-attempt recovery

First C195 attempt at execution HEAD `33da93a7e227799988cad0762b1d73e6cdefe92f`
is **INVALID EXECUTION / RETRY SAME C195**. Precheck passed; all1605 tests ran; exactly two
C195 unit tests errored before benchmark execution because the synthetic C191 reference fixture
omitted its leading batch dimension. The real C191 artifact contract is already batched.

Published log commit `f216c5f701799516a152025f3be8c3d1b08f220e`;
log SHA256 `67597c92c4b7b3e738424bc29ad242f71cd072152dc530b0d821508237d4f7ff`.

Only the test fixture rank is corrected. No scientific condition changes.
Retry SAME C195; C196 remains unregistered.

## C195 second invalid-attempt recovery

Retry at execution HEAD `4cfa9238d335f734a58cb602baa7edf369eeb6b6` is
**INVALID EXECUTION / RETRY SAME C195**. All1605 tests passed; benchmark then stopped after
the first block because C195 guessed nonexistent C191 record aliases
`second_provider_calls` and `final_needs`.

Accepted C191 actually exposes `parent_second_reads`, `third_provider_calls`,
`parent_final_needs`, and `actual_reads`. C195 now centralizes those fields through a
schema-validating `reference_block_expectations()` adapter and source-level tests reject
the bad aliases.

Published log commit `10685a707d4d80dde4a4732fca14d3cf4a2237d3`;
log SHA256 `ddccd960551ac9f71c6d92c6ed8b483ac37ff77b257208e222ce0ebb9f85be82`.

No scientific condition changes. C196 remains unregistered.

## Active C195

One variable:
initial `internal_remaining 13 -> 12`.

Generic C194 loop is reused unchanged.

Reference:
accepted C191 budget12 behavior and prediction artifact.

Question:
does the generic loop stop safely at budget exhaustion after a third acquisition, with
resources0/1/19, no fourth learned prediction, no fake SUFFICIENT, no extra read, while
earlier-resolving rows still stop normally?

Expected:
928 exhausted rows/selector, exact C191 phase0/1/2 predictions and read depths.

Expected regression1605;80 modules.
Source pins136;protected paths363;artifacts5.
Manifest:
`ebfa3e2f916368b4e2b07efa072c9f9c2b4ec62cb0c77ac69e3cb1f527b90128`.

C196 remains unregistered until C195 judgment.
