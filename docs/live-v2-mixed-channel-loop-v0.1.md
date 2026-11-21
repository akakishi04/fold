# Live v2 mixed-channel loop v0.1

C204 replaces C203's saved-decision replay with live frozen-model inference while preserving the
same mixed-channel runtime path.

## Decision input boundary

At every learned decision:

```text
current v1 RuntimeState
-> structured-v2 TaskView
-> v2 encode: 84 features
   [0:72] canonical v1 prefix
   [72:84] fixed fact-channel metadata
```

Only the exact72-feature prefix enters the frozen C181/C188 learned models.

The12-bit tail is routing metadata only and never enters the learned forward.

## Frozen learned models

C204 uses:
- C181 INTERNAL_SEMANTICS base checkpoints for seeds181001/181002/181003;
- C188 selector checkpoints for all9 base/head pairs.

Checkpoint files, summary hashes and model fingerprints are tied back to the accepted C199
protected input set.

No training, threshold repair, model update or saved-decision substitution occurs.

## Live loop

For every active phase:

1. parent RETRIEVE-only authority is present;
2. charge decision;
3. construct/roundtrip structured-v2;
4. verify v2 first72 == canonical v1 packet;
5. run live frozen necessity/target inference;
6. compare prediction/logits to accepted C199 ALLOWED artifact;
7. on live NEEDS, temporarily enable all three channels;
8. route live target through the fixed C203 fact-channel layout;
9. dispatch/publish through the existing lifecycle;
10. restore parent authority before the next live decision.

## Fixed expected totals

```text
episodes             85824
learned decisions    214948
model input rows     214948
acquisitions         129124
final SUFFICIENT     85824
v2 packets           214948
channel switches      32564

RETRIEVE              88918
OBSERVE               21252
ASK_USER              18954
```

Every live prediction must equal the accepted C199 reference. Necessity and target logit maximum
absolute deltas must each be <=1e-6.

## Scope

C204 proves live re-inference compatibility of the existing72-feature learned policy with the
structured-v2 mixed-channel runtime. It does not prove that the learned models use channel metadata,
learn channel preference, access real sensors/users, or complete Gate E.
