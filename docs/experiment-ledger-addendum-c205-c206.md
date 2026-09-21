# C205 acceptance / C206 handoff

## Formal judgment

**C205 — ACCEPTED PASS.**
**C206 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C205:
- scientific execution HEAD: `c78b79e95b92552c032df05220868122398fd339`
- published log commit: `fd05da86e40e81feb96a3e7b6011e9d229299176`
- log SHA256: `1dd3973c15013fb95296fda482eebe52298377c56eee3a9a50c7c3b0ee260427`
- summary: `runs/c205-v5e-phase0-batch-attribution-dfe8de2821934f1785f5ce925ca2d3c9/summary.json`
- summary SHA256: `2f60e87aa7158bf22e1a4f6b15904a4e66096a1db81a6477e0b398be87fc3c2b`
- focused regression: **1871/1871** in 43.028s
- all9 attribution blocks completed
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False

## Deciding evidence

Canonical unique structured-v2 phase0:
- total rows15912
- forward calls18
- cell calls126
- max necessity logit delta **0.0**
- max target logit delta **0.0**
- prediction errors0
- prefix mismatches0

Expanded-direct structured-v2 phase0:
- total rows85824
- forward calls90
- cell calls630
- max necessity logit delta **5.0067901611328125e-06**
- max target logit delta **5.7220458984375e-06**
- prediction errors0

Attribution:
- max C204 necessity-max match error **0.0**
- max C204 target-max match error **0.0**
- candidate_gate_passed True

## Scientific interpretation

The gate-breaking numeric replay maxima observed in C204 are fully reproduced by phase0
duplicate-expanded batching. When the same structured-v2 canonical72-feature state is inferred using
the original C199 phase0 unique-state batching, logits reproduce C199 exactly.

Therefore C204's valid negative is attributable to numerical batch-composition replay, not a
structured-v2 prefix/state semantic change or an argmax/action-policy change.

C204 remains ACCEPTED VALID NEGATIVE because its preregistered1e-6 whole-run numeric gate did not
pass. C205 does not retroactively alter that verdict.

## Next boundary

Gate E contract requires a derived-result output contract with supporting references; a logical
conclusion must not be misrepresented as an observed fact.

C171 already provides the production `structured_derived_result.verify` contract, but its proof
producer is benchmark-only and has not been connected to the accepted mixed-channel terminal states.

C206 should isolate one question:

> After replaying the accepted C203/C204 behavioral trajectory to terminal SUFFICIENT states, can
> every terminal Boolean conclusion be emitted as a `VERIFIED_DERIVED` result bound to exactly
> the actually observed supporting references, while leaving observations/resources unchanged and
> rejecting the opposite conclusion?

C206 should:
- reuse the accepted C203 behavioral trace (C204 proved live argmax identity);
- use the real C201/C202/C173 mixed-channel acquisition lifecycle to reconstruct terminal states;
- use C171 benchmark-only proof fixture solely as a reference candidate producer;
- use production `structured_derived_result.verify` as the deciding verifier;
- compare the derived value against C171's independent completion evaluator;
- require no fact to be promoted/mutated by verification;
- require opposite-value candidate rejection;
- add no training, new seed, provider family, answer-language generation or Gate E final claim.

This is an output-contract integration prerequisite, not learned proof generation.
