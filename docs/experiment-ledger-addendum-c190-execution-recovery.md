# C190 execution recovery — parent logit batch-context replay

## Formal status

**C190 remains ACTIVE / NOT YET JUDGED.**
The completed run at scientific execution HEAD
`b934eff1e06c5ce0b75e08870dfd9a6753768b21` is
**INVALID EXECUTION / RETRY SAME C190** under the preregistered parent-replay validity rule.
C191 remains NOT REGISTERED. Gate E remains NOT PASSED.

Published log commit:
`da06a4544093930bc5392e05f42ffc2a3f0ac262`.

Published log metadata:
- SHA256 `7f025f7519a0ae9e2570e4091a3ea53a21555c8864a69265f60633e82bf1f883`
- bytes 348826

Run summary:
- 1485/1485 regression PASS
- source/artifact precheck PASS
- 9/9 blocks complete
- 85824 coherent-world episodes
- run_execution_valid True at runtime/postcheck layer
- summary SHA256 `344cf2f7689ea3d8f6cc09467e48d8a42e1b1d0f3a36ddb82ca0a1d1d3b09421`

Scientific counters were all zero:
- failed0
- initial_error0
- initial_replay_error0
- target0_error0
- selected_observed0
- first_acquisition_error0
- post1_error0
- target1_error0
- repeated_target0
- second_acquisition_error0
- post2_error0
- contract_error0

Live work:
- first reads/publications85824
- logical post1 NEEDS / second reads/publications34948
- logical post2 NEEDS8352
- total file reads120772

Why INVALID rather than VALID NEGATIVE:
the preregistration explicitly classified parent replay failure as execution invalidity.
All nine blocks preserved parent argmax exactly, but raw float32 logits differed solely
under the expanded 9536-row batch context:
- necessity delta range 3.337860107421875e-06 .. 5.245208740234375e-06
- target delta range 2.384185791015625e-06 .. 5.7220458984375e-06
which exceeds the fixed <=1e-6 guard.

Recovery:
initial states duplicated only because hidden complete worlds differ; world code is not a
policy input. Recompute each unique initial TaskView once in the accepted C189 1768-row
ordering/batching, require the unchanged <=1e-6 parent replay, and memoize that frozen-model
output across its identical world copies. Saved parent outputs are comparison-only, never
policy inputs. Every world copy still owns independent runtime state and live acquisition.

No scientific gate, tolerance, seed, checkpoint, source world, cohort, action, teacher or
interpretation is changed.


## Memoization unit-test mock recovery

Execution HEAD: `40d53444067831d6ec3b1419142fdab36dd5be84`
Published log commit: `cc08b5c6c1075ae0598a7c5dca7843a854a67a60`
Log SHA256: `3acc82e2e0788fdd8796cb6f29699f97e1de4b61050802e9e7ab21d828f07fb6`.

Source/artifact precheck passed. Focused regression ran all 1485 tests and exactly two
C190 tests errored before the benchmark:

- test_16_run_block_stops_after_first_when_sufficient
- test_19_resource_state_after_one_acquisition

The execution-recovery change memoized the initial policy output, so `combined_predict`
is no longer called for phase0 inside `run_block`. Those two tests still used a call-count
mock that treated the first `combined_predict` call as phase0 and returned NEEDS/target0.
It was actually phase1, so the test attempted to reacquire the already observed first target.

Recovery changes only those mocks so their sole in-block combined call represents the
post-first-acquisition SUFFICIENT phase. Benchmark source, manifest, replay threshold,
seeds, checkpoints, cohort, worlds, gate and interpretation are unchanged.

C190 remains ACTIVE / NOT YET JUDGED. Retry SAME C190.
