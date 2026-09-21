# C209 acceptance / C210 handoff

## Formal judgment

**C209 — ACCEPTED PASS.**
**C210 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C209:
- scientific execution HEAD: `a9e4bdae10b574eb5fd66f4a3dc027bab5a18194`
- published log commit: `dae623b349a12764c7ee4705ee2a32adddf8b59c`
- log SHA256: `778e8d87a20afbdb488c169c8acb73b0876fbd34e7b6cc9cb4940c286c898d41`
- summary: `runs/c209-v5e-visible-only-projection-4136fdb65cb643ffab274a898153d92c/summary.json`
- summary SHA256: `49476c781212f87a2782fdb6b042582dcd18941642b452855bb92690f90facc3`
- focused regression: **1973/1973** in 62.210s
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- model forward calls0
- scorer usedFalse
- trusted runtime mutatedFalse

## Deciding evidence

- episodes144
- original fact counts:1->16,2->112,4->16
- synthetic TRUE facts272
- non-OBSERVED status normalizations32
- exhaustive semantic assignments736
- semantic errors0
- source unchanged144
- source digest match144
- original-index mapping valid144
- observed originals preserved144
- normalized nonobserved safe144
- dummy contract valid144
- dummy missing errors0
- C178 necessity-compatible144
- C188 target-compatible144
- combined-compatible144
- equal source units50
- equal projected units50
- pair projection errors0
- candidate_gate_passed True

## Scientific interpretation

A deterministic visible-only model-input projection can bridge the general C207 structured-v2
development schema to the frozen legacy C181/C1887-node/4-fact input contract without scorer data,
without modifying trusted runtime/evidence state and without changing the Boolean function.

This removes the representation-compatibility blocker measured by accepted-valid-negative C208.

C209 does not establish that the frozen learned candidate makes good decisions after projection.

## Next boundary

The Gate E contract now permits the separate **baseline-development measurement** required before
numerical margins are fixed.

C210 should isolate one question:

> On the frozen C207 development manifest, what raw matched performance and cost measurements are
> produced by the projected frozen candidate cohort, an internal-only baseline and the registered
> canonical fixed-acquisition baseline under the same runtime/answer boundary?

C210 must:
- use all nine frozen C181/C188 base/head pairs as development candidate identities;
- use C209 projection only for candidate model input;
- use the original C207 structured-v2 TaskView as trusted runtime state;
- use the same production acquisition lifecycle for candidate and fixed baseline;
- use one shared bounded C171/production-derived verifier answer resolver for all policies;
- load scorer metadata only for environment construction and post-hoc scoring, never candidate or
  baseline policy input;
- measure raw per-episode/per-family resolution, abstention, acquisition, user-turn, provider-call,
  fault and compute counts;
- record internal-only and fixed-acquisition baselines;
- set **no performance acceptance margin** and select **no winning candidate**;
- create no independent holdout and make no final Gate E claim.

The later C after C210 may freeze candidate identity and numerical decision margins using only this
development measurement, before any deciding holdout is evaluated.
