# C229 acceptance and C230 boundary

## Formal verdict

**C229 ACCEPTED PASS (diagnostic audit). Gate F remains NOT PASSED.**

Scientific execution HEAD: `339697addb6a2b8c88bad5890456fcf7b41ce398`.
Published log commit: `4fdf39f7c8b506fa1d1d010ca68bd86d35cc92b3`.
Log SHA256: `31a1f14892cc0d94bf350100e5239fda44bee798b5a53ace2ef4d55085514db6`.
Summary SHA256: `b71769d8c22ef72436b5952406632deafd100c44ed72da8f4c71c93133a0fe37`.
Local summary:
`runs/c229-v5f-cost-profile-02c07c2130ab49acbf1558009be3b3b3/summary.json`.

Artifacts:
- function-profiles.json: `d323c8af2c491bc1759fbf7455cb3dcb0b165ac6c1c988185e40eadc527b1df5`
- measurements.json: `c96d4154a0aef79fb50b5a34e8c7f5fad10262ebb9a79e02614d0b2a36e74786`
- profile-plan.json: `3f9ce8c054db73843455447d6dc74426be570e50857cc220a3927f8777bd3723`
- quality-checks.json: `a816a2829a9923afed5398ac65c616934aeff47dfef156676329d83435553904`
- validation-summary.json: `08d0113b747fe902d99dedc3204775d22ae9e59cb4dc2f0fa80532ff6cb79551`

## Validity and deciding evidence

Published execution reports2625/2625 regression OK in65.339s, all12 dimension/burst cells,
all_quality_parity, parent_export_parity, all_call_counts_pass, profiler_restored and
function_profile_gate True. Protected inputs and clean tracked tree preserved; run_execution_valid
True. Acceptance uses published console evidence and recorded local artifact checks; reviewing the
log is not a rerun of the user's local artifacts.

## Representative diagnostic: n256,16 queries/update

Twelve updates and192 queries per arm. Candidate query self-time total under cProfile was
52,237,500ns. ResponseCapsule.response cumulative time was40,931,400ns (78.36% of that total),
including nested operations. Its own self time was10,742,700ns (20.57%).

Other candidate query self times:
- Cholesky:6,590,500ns,192 calls;
- symmetry allclose:5,823,400ns,192 calls;
- solve:5,740,300ns,192 calls;
- isfinite:5,502,400ns,576 calls;
- cholesky_ex:3,155,100ns,192 calls.

_read_parts cumulative time was3,853,300ns (7.38%). These cumulative percentages overlap child
self times and must not be added together. Profiler overhead perturbs timing; none of these amounts
is a guaranteed removable cost or a new speed benchmark.

The same cell's candidate update diagnostic includes24 H2CapsuleState constructions,48 clone
calls and12 aggregate rebuilds. This supports allocation/validation as update work, but does not
justify saying clones or Python objects alone explain the query loss.

Important correction to the earlier hypothesis: H2 already retains aggregate W/b. The all-committed
C228 workload does not re-sum all H2 factors for each query. Query _read_parts handles an empty hot
set, adds its zero contribution and builds metadata. Full H2 rebuilds occur on updates.

## Interpretation

The first optimization target is repeated W-dependent response preparation and checks, not a
speculative broad state-machine rewrite. ResponseCapsule.response recomputes Cholesky(K), the
SPD test for I+L.T@W@L, and solve preparation for I+W@K on each query even though this workload's W
is unchanged. Bias/current-state checks must remain live.

C227/C228's unfavorable unprofiled results stand. C229 does not establish faster H1/H2, smaller
whole-system memory, general language quality or Gate F completion.

## Next bounded intervention

C230 should test an explicit checked reduced-system preparation cache, without editing accepted
reference sources. Keep the same12 cells, raw data, state operations and strong full-factor/rhs
comparator. Reuse only W-dependent preparation; recompute current bias response on every query.
Guard capsule/base/cache mutation and exact aggregate-W equality; changed W requires explicit new
preparation. No answer cache, safety removal, new training or workload change.

Measure unprofiled original / prepared-reduced / full-factor-reuse paths, all preparation and retained
cache costs, current-answer parity and stale/mutated rejection. Do not require a favorable speed
ratio for a valid audit. After this intervention, decide adoption scope or stop this optimization
track instead of indefinitely seeking a favorable workload. No C231 is registered here.

C230 is NOT REGISTERED by this acceptance commit; see its separate preregistration and authoritative
handoff for execution permission.
