# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E PASSED**.
**C213 ACCEPTED PASS. C214 ACTIVE / NOT YET JUDGED. C215 NOT REGISTERED.**

## Accepted C210

Scientific execution HEAD:
`002543b8d1394c127b915b3bfe4591ce20c8939d`

Published log commit:
`a04e7cdc5b42939e2d65f395f12da450a896bf0f`

Log SHA256:
`f1365f6d364c5bf0729ef7240f69c2c566004eef554a35c08b8b32355039f0d3`

Summary SHA256:
`1b4242f15fdf3ca48374660d5c3339ff5c17dc9cd4f4833852f5e1bccb349366`

C210 deciding result:
- focused regression **1997/1997**
- policy-episode evaluations1584
- measurement_complete True
- run_execution_valid True
- numerical margin registration False
- candidate selection False
- independent holdout created False

INTERNAL_ONLY:
- correct48 / answered48 / unresolved96
- attempts0 / provider calls0 / publications0 / user turns0
- wrong abstention80 / wrong answers0

FIXED_ACQUISITION:
- correct128 / answered128 / unresolved16
- attempts96 / provider calls90 / publications80 / user turns16
- wrong abstention0 / wrong answers0
- authority violations0 / malformed publications0

All9 candidate model pairs are identical in full policy and per-family summaries:
- correct128 / answered128 / unresolved16
- attempts96 / provider calls90 / publications80 / user turns16
- wrong abstention0 / wrong answers0
- unnecessary acquisition0 / missed necessary acquisition0
- premature sufficient0 / repeated NEEDS0 / invalid target0
- inference rows224 / forward calls2 / cell calls14

Accepted claim: the matched development measurement is complete. This acceptance refers to the
retry execution at `002543b8d1394c127b915b3bfe4591ce20c8939d`; the earlier unprotected attempt
remains invalid historical evidence. C210 does not itself select a candidate or register numerical
acceptance margins.

## Accepted C211

Experiment:
`C211-v5e-deciding-manifest-freeze`

Stage:
`V5-E-DECIDING-MANIFEST-FREEZE`

One question:
can the complete deciding Gate E registration be frozen from accepted development evidence without
evaluating the deciding holdout?

Frozen candidate:
`CANDIDATE-181001-188001`

Tie-break requires all9 C210 candidate full policy/family summaries to be exactly equal before
lexicographic selection.

Pinned checkpoint hashes:
- base `3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289`
- selector `02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d`

C211 creates a144-episode /72-unit independent nine-family deciding holdout with expression
signatures disjoint from C207 development, freezes exact artifact hashes and registers:
- zero-episode noninferiority margins versus FIXED_ACQUISITION;
- +1-episode strict improvement margins versus INTERNAL_ONLY for two primary claims;
- one-sided exact paired McNemar with Holm alpha0.05 across exactly2 claims;
- hard-zero runtime/safety rules;
- zero-floor unsupported-assertion limitation;
- candidate compute ceilings;
- stopping/invalidity rules.

C211 performs no holdout policy/model evaluation.

Authoring:
- source pins93
- protected inputs177
- artifacts5
- tests28
- regression modules96
- focused regression2025
- manifest `8a24beda4da38c331b6c10ed4c46159073a78e1c426ccb580d9a861742e1db99`

## Post-authoring review

**post_authoring_review = PASS**

recovery review HEAD:
`93012e0607772d64c9a57040540f3b60b2b32fd1`

Recovery review verified the Boolean-negation fix on committed remote bytes: no integer negate
literals remain, six explicit Boolean negations are covered by type assertions, and all C211
scientific identities, manifest/rules, 93/177 protection accounting, 2025 regression contract,
no-evaluation boundary and C212 non-registration remain unchanged.

Do not issue C211 execution command until committed remote bytes are independently reviewed for
parent identity, candidate tie/checkpoints, holdout independence, decision rules, no-evaluation
boundary, regression counts, aliases, PowerShell parser chain and CLI indexes.


## Invalid C211 attempt

Scientific execution HEAD:
`16280454018b779aba0112e34317d2b1bd4c1f77`

Published log commit:
`ca0e0334b1a425dab002ea9df3e921a6480bb75c`

Log SHA256:
`da6840a3c6326227b9b3b932ad888bf42349bebcc0748784e87c39f69b6aebd3`

Failure phase:
- repository preflight PASS;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- focused regression started;
- inherited C100-C210 tests reached **1997 executed / all passed**;
- C211 class setup failed before its28 tests could execute.

Root cause:
`gate_e_c211_deciding_manifest_freeze.py` constructed negated leaves with integer
`negate=1`, while production `structured_task_input.Node` requires
`type(negate) is bool`. The first holdout case therefore raised
`ValueError("Invalid node kind/negation")`.

Formal disposition:
**INVALID EXECUTION / RETRY SAME C211**.

No deciding manifest was frozen and no holdout policy/model evaluation occurred.

Recovery:
- replace all six C211 `negate=1` literals with `negate=True`;
- strengthen existing C211 tests to assert Boolean negation type;
- preserve candidate, holdout construction semantics, margins, statistics, manifest SHA,
  workload and C212 non-registration;
- re-review corrected committed bytes before retry.

## Accepted C211 execution

Scientific execution HEAD:
`9cedc79a02441e9cddb0efc0c8bbc7714f9112db`

Published log commit:
`c35a76b33c1782dc6caa1916c9fc3f7658bbbba7`

Log SHA256:
`93992504ae7dae472911521e5bed336f57407e4bc8dfc3542b6e60863da1c25c`

Summary SHA256:
`97f5c1fde9128651ae842046e706219a50e0f34238b87d17d253e89d71279263`

Deciding result:
- focused regression **2025/2025**;
- status **PASS**;
- candidate_gate_passed True;
- run_execution_valid True;
- selected candidate `CANDIDATE-181001-188001`;
- holdout episodes144 / dependence units72 /16 per family;
- expression-signature overlap0;
- development unit overlap0;
- development case overlap0;
- hidden payload errors0;
- pair errors0;
- equal-visible units50;
- holdout_evaluated False;
- model_forward_calls0;
- baseline_policy_calls0.

Frozen deciding artifacts:
- visible `1197f59ab6bf659929ecb7a9f42df27ea28e81586c4602f8e1eb96da17be126b`;
- scorer `3975c10afc2e644f5279de4d46459d1aa250c6e7b381bb944b0b8cf6b585ff22`;
- units `630d9c94b4aee67f55c3f9704ad6a508679e01450da73dd18a8935b4bac8dc34`;
- decision rules `d143f2a6b4b96c672131daf22dea5c207d42375440c7d403ee95b9782fd75bcc`;
- deciding manifest `f9356e87b210bc7d836d016a9ad7a4f841a9a651b3bb9faf9428b0415df9e6d6`.

Formal disposition:
**C211 ACCEPTED PASS**.

Accepted claim: the complete Gate E deciding registration is frozen without evaluating the deciding
holdout. C211 does not itself establish Gate E performance or pass Gate E.

## Accepted C212

Scientific execution HEAD:
`4d1436c1ba12721b1c802fb5d76e359b3a62841f`

Published log commit:
`3163014d0672ab8905a06c37ae6698e9ea9c80bc`

Log SHA256:
`146dee38ca4823ac0bf8aeabd9c4defec92d967b184adc7e5f441b5526943ca0`

Summary SHA256:
`3685c37dd6e2c7fea92723548446b86f4ee8d068f7dd00afe3e2337f8bca8bce`

Formal outcome:
**GATE_E_PASSED**.

Execution validity:
- focused regression **2055/2055**;
- source/artifact precheck PASS;
-432/432 matched policy-episode evaluations;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
- candidate correct128 / answered128 / wrong abstention0 / wrong answer0;
- FIXED_ACQUISITION correct128 / answered128 / wrong abstention0;
- INTERNAL_ONLY correct48 / answered48 / wrong abstention80;
- candidate vs fixed: all overall and all per-family zero-margin noninferiority checks PASS;
- candidate vs internal useful-correct margin **+80 episodes**;
- candidate vs internal positive-acquisition-gain margin **+80 episodes**;
- both one-sided exact paired McNemar p = `8.271806125530277e-25`;
- Holm [0.025,0.05] both PASS;
- hard-zero gate PASS;
- compute ceiling PASS:144 initial +80 post =224 rows,2 forward calls,14 cell calls;
- guarded unsupported assertions0 with `NOT_DEMONSTRATED_ZERO_FLOOR` comparative limitation preserved.

Accepted claim:
within the preregistered independent144-episode Gate E holdout and shared symbolic answer boundary,
the frozen selected candidate satisfies every frozen Gate E rule.

Non-claim:
this does not establish general natural-language intelligence, FOLD-R memory integration, variable-
length I/O, Vision, or large-scale practical superiority.

## Accepted C213

Scientific execution HEAD:
`f59f615b5d409400c9fc5247270a37960ffac197`

Published log commit:
`78751428cc8397c82488dfd4bf205aa9ac62bc97`

Log SHA256:
`18a09bfbe223d87f1e0f6b317d07fa72e324485c7af7aa2993f9d6e388850944`

Summary SHA256:
`370ee39bcd32da4ce797ecfb21ce3b863013c788f6daaaf0fb9a10edac643b43`

Formal disposition:
**C213 ACCEPTED PASS**.

Execution validity:
- focused regression **2083/2083**;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- protected inputs preserved;
- tracked tree clean;
- run_execution_valid True.

Deciding metrics:
- successful memory mutations6;
- reads8;
- SUPPORTED3 / MISSING2 / RETRACTED1 / STALE_REVISION1 / OUT_OF_SCOPE1;
- final memory revision6;
- final evidence revision4;
- final evidence time3;
- final exported observations1;
- exported hypotheses0;
- stale mutation rejected True;
- observed-scope END rejected True;
- ended-scope mutation rejected True;
- learned Writer/Reader calls0;
- FOLD-R capsule calls0;
- model forward calls0.

Accepted claim:
the deterministic V5-F memory operation/scope/revision/provenance boundary is internally coherent
and can export authoritative observed evidence without promoting hypotheses.

Non-claim:
C213 does not establish FOLD-R numeric correction closure, H1/H2 memory compression, learned memory
routing, natural-language memory extraction or Gate F.

## Active C214

Experiment:
`C214-v5f-memory-capsule-closure`

Stage:
`V5-F-MEMORY-CAPSULE-CLOSURE`

One question:
when accepted C213 observed edit semantics are projected into the existing fixed-port FOLD-R
response capsule, do supported edit sequences produce the same readout as an independent full-memory
reference within registered float64 tolerance?

Changed variable:
- new `fold_lm/v05/memory_capsule_bridge.py` semantic-to-numeric adapter only.

Held constant / absent:
- learned Writer/Reader;
- Port Selector;
- H1/H2 compiler;
- language parsing;
- model inference;
- training;
- existing response-capsule algebra.

Registered fixture:
- variables4 / update rank2 / readout dim2;
-7 supported snapshots;
- factor-count sequence [0,1,1,2,1,1,1];
- capsule/full-reference max abs error <=1e-10;
- ASSUME and END_SCOPE numeric deltas0;
- unknown observed relation -> OUT_OF_SCOPE;
- unsafe registered update -> NUMERIC_UNSAFE;
- final exported observed factor beta only.

Authoring:
- source pins115;
- protected inputs217;
- artifacts5;
- tests32;
- regression modules99;
- focused regression2115;
- manifest `dc2354bd35d94ef0d8b7e5f4c6bed820f5166f0ce20948df612b30d1b0465915`.

## Post-authoring review

**post_authoring_review = PASS**

review HEAD:
`7453cf9b62b86a3970e2a549028d604e329ec525`

Committed remote review verified accepted C213 summary/validation identity, existing response-
capsule source identity, relation-to-port mapping and full-reference parity, hypothesis exclusion,
replacement/retraction semantics, OUT_OF_SCOPE vs NUMERIC_UNSAFE separation,32 tests,
semantic2116-loaded/2115-kept regression accounting, zero unbound executable aliases, exact runner
argv/postcheck wiring, launcher parser ordering,115 source pins /217 protected inputs, accepted
C213 local summary path and C215 non-registration.

Independent numeric reconstruction produced max capsule/full error approximately1.11e-16 across
the seven registered supported snapshots; all safe updates remained SPD and the unsafe control
alone crossed the SPD boundary.


## Stop condition

Judge C214 before any C215 registration.

Gate E remains **PASSED**. Gate F remains **NOT PASSED**.
