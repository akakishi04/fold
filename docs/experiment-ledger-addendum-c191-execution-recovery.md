# C191 execution recovery


## First C191 invalid attempt — wording-only unit-test assertion

Execution HEAD: `329c40c4d418eebeffbbda6cc2513e35c6aeef86`
Published log commit: `66010b575cb42008eea7404265da8372e265d36e`
Log SHA256: `16d2c7b3ea9b2e214ad1df0fa6d873b45d1fcf882a588b64b56cace30bb5066c`.

Source/artifact precheck passed. All 1509 tests ran; exactly one C191 test failed before
benchmark execution:

`test_20_target2_scope_declared_trivial`

The manifest correctly states:
`post2 NEEDS has exactly one unobserved fact; target mask leaves one legal fact`.

The test incorrectly searched for the different phrase `sole remaining unknown`.
Recovery changes only the test assertion to match the already-registered manifest wording.
No benchmark source, manifest, hash, seeds, checkpoints, cohort, gate, threshold, resource
budget or interpretation changes.

C191 remains ACTIVE / NOT YET JUDGED. Retry SAME C191. C192 remains unregistered.
