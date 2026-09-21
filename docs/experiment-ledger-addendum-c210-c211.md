# C210 acceptance / C211 handoff

## Formal judgment

**C210 — ACCEPTED PASS.**
**C211 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C210:
- scientific execution HEAD: `633ce9bed165d30b0adb671c1faf12d34a9ad0cc`
- published log commit: `482d36ca1563fc7379fa48c346e255a526a48cec`
- log SHA256: `158e54bde84b156ebd665285ea85f32224dc943174ed9cc46997fd71753434fd`
- summary: `runs/c210-v5e-baseline-development-4dc4cf58d73b4621a7d7b6b96edc4fc6/summary.json`
- summary SHA256: `785c2aa2bfa29e0861c082dee0557f21cac4c2a6647268e552965c2ecd15b7a2`
- focused regression: **1997/1997** in 68.218s
- policy-episode evaluations1584
- measurement_complete True
- run_execution_valid True
- numerical_margin_registration False
- candidate_selection False
- independent_holdout_created False

## Baseline controls

INTERNAL_ONLY:
- correct48 / answered48 / unresolved96
- attempts0 / provider calls0 / publications0 / user turns0
- wrong abstention80
- wrong answers0

FIXED_ACQUISITION:
- correct128 / answered128 / unresolved16
- attempts96 / provider calls90 / publications80 / user turns16
- wrong abstention0
- wrong answers0
- authority violations0
- malformed publications0

## Candidate development result

All9 frozen C181/C188 model pairs are exactly identical in the complete registered
`policy_summary` and complete per-family `family_summary`.

Every candidate pair:
- correct128 / answered128 / unresolved16
- attempts96 / provider calls90 / publications80 / user turns16
- wrong abstention0
- wrong answers0
- unnecessary acquisition0
- missed necessary acquisition0
- premature sufficient0
- repeated NEEDS after successful publication0
- invalid target0
- inference rows224
- initial rows144 / post rows80
- inference forward calls2 / cell calls14

Therefore C210 supplies no performance basis to prefer one of the nine pairs.

## Next boundary

C211 must freeze the complete deciding registration **without evaluating the deciding holdout**.

Candidate identity rule:
- require all nine C210 candidate policy summaries and family summaries to be byte-equivalent;
- select the lexicographically smallest tied policy ID:
  `CANDIDATE-181001-188001`;
- pin base checkpoint SHA256
  `3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289`;
- pin selector checkpoint SHA256
  `02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d`;
- pin the accepted C209 projection and accepted C210 candidate/runtime policy source identities.

C211 should freeze:
- an independent144-episode /72-dependence-unit nine-family holdout manifest using semantic
  templates not present in C207 development (not mere variable renaming);
- exact visible/scorer/unit hashes;
- same baseline identities and budgets;
- exact source/fault schedule;
- output schema and shared-answer disclosure;
- hard-zero runtime/safety constraints;
- zero-loss noninferiority margins versus FIXED_ACQUISITION for useful resolution, coverage,
  wrong abstention, unnecessary acquisition and user turns;
- minimal strict +1-episode improvement margins versus INTERNAL_ONLY for useful resolution and
  acquisition gain;
- one-sided paired exact McNemar tests for the two improvement claims with Holm familywise
  alpha0.05;
- per-family no-worse-than-fixed requirements with raw numerators retained;
- post-guard unsupported assertion floor rule: candidate must remain0; strict reduction versus the
  already-zero guarded internal baseline is explicitly **not demonstrated**;
- final stopping/invalidity rules.

C211 must perform no candidate/baseline model forward and must not evaluate the holdout scorer
against a policy. It only constructs/validates and freezes the deciding manifest.

Only after C211 is accepted may a later C execute the deciding holdout once under the frozen
identity/rules.
