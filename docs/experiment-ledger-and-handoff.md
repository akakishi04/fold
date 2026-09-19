# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C194 ACCEPTED PASS. C195 NOT REGISTERED at this acceptance commit.**

C194 scientific execution HEAD:
`32e62fe1b2e8318daa766aff1bfcc1f0fc49d95a`
C194 published log commit:
`eaa3169e31e88eba0ec99a64c557099ba1a4f71e`
C194 summary SHA:
`6cdb274da944bc87cea29f2e093d4acdec6035dae6978adaf469f1d9b4dfa084`.

C194:1581/1581;85824 episodes; all scientific errors0; C193 replay prediction/logit
errors0; parent block mismatches0; first reads85824; second34948; third8352;
final authoritative decision rows8352.

Claim:
one generic state-driven bounded decide/acquire/reobserve loop reproduces accepted C193
exactly. Hand-unrolled phase orchestration is no longer required for this development-family
closure.

## Next design

C195 one question:
with the generic C194 loop held fixed and only initial internal budget changed13->12, does
the loop reproduce accepted C191 budget-exhaustion behavior safely?

Reference:
accepted C191 budget12 predictions/read depths/final resources.

Expected boundary:
third acquisition may consume the final3 internal units; the next scheduler debit must fail
without state mutation, provider read, publication, or fake final SUFFICIENT decision.

C196 remains unregistered until C195 judgment.
