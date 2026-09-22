# C220 acceptance and C221 boundary

## C220 formal verdict

**C220 ACCEPTED PASS. Gate F remains NOT PASSED.**

Scientific execution HEAD:
`6bc455fa377ec9d3c70d6d1f0922c00680fd5a04`

Published log commit:
`e194716393249373a7d1f6ab552860e851ea84d0`

Published log SHA256:
`dd9e8753ac48b74e369c2c87efdb0987da81c1b9379bab674af86252c8b7eed2`

Summary SHA256:
`45821b372bf0108e667274e2facd73b1f0a84f515a7d036e73874d9238fff5f7`

Local accepted summary:
`runs/c220-v5f-frozen-learned-stack-5bc9d133c96348de81a24d19b3ef6f93/summary.json`

## Execution validity

Published metadata identifies the registered scientific execution HEAD. The remote log reports
Python syntax/source-artifact prechecks PASS, 2335 focused tests in 45.140 seconds, OK,
`diagnostic_execution_valid = true`, `stack_gate = True`, preserved protected inputs,
a clean tracked tree and `run_execution_valid = True`.

This verdict uses the published console evidence; local-only checkpoints/artifacts have not been
copied to the reviewing environment. The runner's artifact postcheck is the recorded evidence for
their byte integrity. Scientific execution HEAD and the later log-publication commit are distinct.

## Deciding metrics

| Metric | Registered result |
|---|---:|
| Frozen checkpoint combinations | 81 |
| Decision rows | 648 |
| Readable decisions | 486 |
| Non-readable decisions | 162 |
| Integration accuracy | 1.0 |
| Expected coverage accuracy | 1.0 |
| Readable answer accuracy | 1.0 |
| Non-readable suppression accuracy | 1.0 |
| MISSING / OUT_OF_SCOPE confusions | 0 |
| HOT / COMMITTED prediction mismatches | 0 |
| Operation failures | 0 |
| Writer / Coverage / Selector / Reader forwards | 3 / 9 / 3 / 27 |
| New training steps | 0 |

All four checkpoint-family roundtrips passed. Writer target accuracy, selector route accuracy and
coverage-vs-actual-state teacher accuracy were each 1.0. Learned Writer applications18,
oracle initialization writes12, oracle END_SCOPE operations3 and chunk commits18 were recorded.

Validation artifact SHA256:
`f17175ab1f914df65a28014fbc2571c32cbeeade583ad7f38093a17a24c458cd`

Other registered artifacts:
- stack-plan.json: `c03227618834ca60f4acb6d69e151e33d9b1723c5a01bb08dd87627403336be8`
- episode-sets.json: `919222de2ca2b598dca487154cf8d7d6756eb6fe9526ba70f31f34ae6094b69f`
- combination-results.json: `96c99e94b1f5feec661e06aad2ca3f87845b2738ad29427b8fb2e8349770f0ad`
- component-fingerprints.json: `3b827a6a6ce4cdb21ef6624462926cc880088ced489bdf22ecafb26860d9d22c`

## Accepted interpretation and important qualification

The registered offline composition check passed: the separately learned frozen components produce
mutually compatible decisions/answers on eight structured synthetic episode shapes.

**648 rows are 81 checkpoint combinations times eight episode shapes, not 648 independent unseen
problems.** No claim of broad generalization, natural-language understanding, joint learning,
bounded total memory cost, RETRACT/ASSUME integration or Gate F completion follows.

Source audit of the executed C220 benchmark also establishes a narrower execution claim than the
phrase "end-to-end runtime" would suggest:

- `_capture()` uses the deterministic actual-state coverage teacher to obtain available readouts.
- `reader_predictions()` selects expected-readable labels from `episode_plan()` and computes Reader
  outputs without accepting learned Coverage predictions as an input.
- `integration_results()` combines those already-computed outputs with learned Coverage afterward.

Therefore C220 does **not** establish that a learned suppression decision prevents the actual
Selector/provider/Reader calls. Its preregistered composition result remains PASS; this missing
causal call-order test is the next intervention, not a retrospective change to C220's gate.

## C221 proposed single question

With the same frozen checkpoints, same eight episode shapes and same 81 combinations, does a
Coverage-first dispatcher actually control downstream invocation and preserve the registered answers
and distinct suppression reasons, without receiving expected labels or precomputed Reader answers?

C221 will separately measure calls and ordering and apply explicit forced-Coverage control cases.
It introduces no training, no new semantic tasks, no acquisition or memory compression optimization.
Its source/manifest/runner registration must be separate from this C220 acceptance commit.

C221 is NOT REGISTERED by this acceptance document. See authoritative handoff and the eventual
C221 preregistration for current execution permission.
