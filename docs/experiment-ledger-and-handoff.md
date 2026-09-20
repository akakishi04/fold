# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, and parent artifact semantic audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C203 ACCEPTED PASS. C204 ACTIVE / NOT YET JUDGED. C205 NOT REGISTERED.**

## Accepted C203

Scientific execution HEAD:
`293b440adfddcbda0a18fd66184768c27aff49a2`

Published log commit:
`618772f2736279ae6389bfc5e488d1eb7c6b2553`

Summary SHA256:
`5fb52a6f056eea1fcf2ff719a9fa8c9efa9cc0d941ea26f50fdceed4c2db56c2`

C203 deciding result:
- focused regression **1813/1813**
- episodes85824
- decisions214948
- acquisitions129124
- final SUFFICIENT85824
- RETRIEVE88918 / OBSERVE21252 / ASK_USER18954
- channel switches32564
- all scientific/runtime/projection errors0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: the accepted multi-step learned trace can execute through a fixed fact-specific
mixed-channel layout, including32564 within-episode channel switches, while preserving exact parent
depth, routing, publication, resource accounting and final SUFFICIENT closure.

## Active C204

Experiment:
`C204-v5e-live-v2-mixed-channel-loop`

Stage:
`V5-E-LIVE-V2-MIXED-CHANNEL-LOOP`

One question:
can the accepted frozen C181/C188 models be recomputed live after every mixed-channel observation,
using the exact canonical72-feature prefix of the current structured-v2 packet, while reproducing
the accepted C199 predictions/logits and preserving the accepted C203 action/runtime trace?

Changed variable:
- C203 saved-decision replay -> C204 live frozen-model inference.

Held:
- C174/C190 cohort and row/world identity;
- budget13;
- accepted C181 INTERNAL_SEMANTICS bases;
- accepted C188 selectors;
- raw argmax;
- C200 v2 contract;
- C201 mapper;
- C202/C173 lifecycle;
- C203 fixed channel layout and authority windows.

Required:
- v2 packets214948;
- learned input rows214948;
- v2 prefix errors0;
- necessity prediction errors0;
- target prediction errors0;
- necessity/target max logit deltas <=1e-6;
- decisions214948;
- acquisitions129124;
- final SUFFICIENT85824;
- RETRIEVE88918 / OBSERVE21252 / ASK_USER18954;
- channel switches32564;
- runtime/scientific/projection errors0.

Model summaries/checkpoints:
- C181 summary SHA `bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`;
- C188 summary SHA `2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153`;
-3 INTERNAL_SEMANTICS bases +9 selector checkpoints must match accepted artifacts and C199 protected hashes.

Authoring:
- expected regression **1843 =1813+30**
- expected modules **89**
- source pins37
- protected inputs79
- artifacts5
- manifest
  `3af3186623e7281c182361eafad0eb6336691e073e76e94ae089d5f2464f24af`

## Post-authoring review

**post_authoring_review = PASS**

review HEAD:
`2687da216c6c47c3a334801556c28f239cecc9ca`

The review re-fetched committed remote bytes and verified all30 source-string assertions against
their exact target functions, C181/C188 checkpoint writer/fingerprint semantics, C199 target writer
gating, deterministic CPU inference settings, structured-v2 prefix/tail isolation,
comparison-only C199 reference usage, live-inference/action ordering, the one-episode production
path, 37 source pins /79 protected inputs, runner/launcher wiring and C205 non-registration.

## Stop condition

Judge C204 before any C205 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/checkpoint/regression/incomplete/protection failure -> INVALID / RETRY SAME C204.

Gate E remains NOT PASSED.
