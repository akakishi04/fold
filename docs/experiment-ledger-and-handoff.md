# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) applies.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C190 ACCEPTED PASS. C191 ACTIVE / NOT YET JUDGED. C192 NOT REGISTERED.**

C190 execution HEAD:
`b3d04dae6ed621deba987162b3d63c8f815bbe72`
C190 acceptance commit:
`53b114aeeabbee2e5ea54ebf6f1396054b74132a`
C190 summary SHA:
`6902f97fd1fbcb1eb878884594a333ae41a0d35c83b872d287439386f7fabd59`.

C190: 1485/1485;85824 episodes; all scientific errors0; first reads85824;
second reads34948; post2 NEEDS8352; initial replay deltas0.0.

## C191 invalid-attempt recovery

First C191 attempt at execution HEAD `329c40c4d418eebeffbbda6cc2513e35c6aeef86`
is **INVALID EXECUTION**. Precheck passed; all1509 tests ran; exactly one wording-only
C191 assertion failed before benchmark execution. Manifest says `exactly one unobserved fact`,
while the test searched for `sole remaining unknown`. Only the test assertion is corrected.

Published log commit `66010b575cb42008eea7404265da8372e265d36e`;
log SHA256 `16d2c7b3ea9b2e214ad1df0fa6d873b45d1fcf882a588b64b56cace30bb5066c`.

No scientific condition changes. Retry SAME C191; C192 remains unregistered.

## Active C191

Question: with unchanged internal budget12, extend max acquisition horizon from2 to3.
On the 928 post2 NEEDS cases per selector, phase2 also exposes target2, then unchanged
C172/C173 performs one third read from the same coherent world.

After third acquisition expected resources are:
`0 internal /1 acquisition /step19`.
A fourth scheduler decision must be refused without state mutation.

Target2 has one legal unobserved fact, so C191 is runtime closure/budget evidence, not
alternative-target ranking evidence.

Same 85824 episodes /9 selectors /16 coherent source worlds.
No training/fresh seeds/resource increase/production runtime change.
Expected regression1509;76 modules.
Manifest `8cf89274974a4204156c2cb2eb1f87d101f8ab09b320dd7e649a4380ddb852f1`.
Source pins116; protected paths304; artifacts21.

No final learned post3 necessity decision in C191.
C192 remains unregistered until C191 judgment.
