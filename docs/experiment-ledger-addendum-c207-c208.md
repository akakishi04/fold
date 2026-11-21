# C207 acceptance / C208 handoff

## Formal judgment

**C207 — ACCEPTED PASS.**
**C208 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C207:
- scientific execution HEAD: `96020d20bd73bf6e2e62d5bfb202b7b2605a2079`
- published log commit: `383033f391b65095011f3464f2c331c996706955`
- log SHA256: `ab28e9961c6b1f07c6fdd1e7f3c72df021b89f4babb3182583e7a6f9caecefd0`
- summary: `runs/c207-v5e-nine-family-dev-manifest-3079dd47bce44ed990278c52b888bae7/summary.json`
- summary SHA256: `a7e69871003ac1978e786809c822d75c0dc291cfbe14aa8709f8b12ec26e4477`
- focused regression: **1929/1929** in 59.669s
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False

## Deciding evidence

- episodes144
- dependence units72
- structured-v2 roundtrips144
- all9 families16 episodes each
- exact registered fault counts
- exact registered expected-action counts
- exact registered eligible-channel counts
- answerable_with_budget128
- duplicate IDs0
- family-count errors0
- unit errors0
- visible-schema errors0
- scorer-leakage errors0
- pair errors0
- scorer-contract errors0
- hidden-payload errors0
- candidate_gate_passed True

Frozen development artifacts:
- visible SHA256 `c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`
- scorer SHA256 `0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912`
- dependence units SHA256 `cb41d550651cb2dbb79f379bb0b6adb696914ecace02dc58cb1371f4e5a8deae`

## Scientific interpretation

C207 establishes a fixed balanced leakage-free development-data boundary for all nine Gate E v0.1
families using only existing structured-v1/v2 schemas and runtime metadata.

It does not measure candidate or baseline performance and does not create an independent holdout.

## Next boundary

Before baseline-development measurement can run, the existing frozen candidate must be able to
consume the frozen C207 visible packets under its current input contract.

Source audit after C207 shows that the accepted C181/C188 inference path is narrower than the
general structured-v1/v2 schema:

- C178 necessity representation requires exactly7 nodes,4 facts and four FACT leaves;
- C188 target input additionally requires fact status only UNOBSERVED/OBSERVED;
- C207 intentionally contains1/2-fact tasks and STALE/CONFLICT facts.

Therefore baseline-development measurement is blocked until this compatibility is measured rather
than assumed.

C208 should isolate one question:

> Can the current frozen C181/C188 candidate inference interface consume all144 frozen C207 visible
> development packets **as-is**, without representation adaptation, scorer leakage or schema
> reinterpretation?

C208 must be a no-forward compatibility diagnostic. It should test the real current C178/C188 input
validators per case/family, preserve exact C207 artifact identities and report the incompatible
surface. A valid incompatibility is ACCEPTED VALID NEGATIVE and must precede any adapter design.
