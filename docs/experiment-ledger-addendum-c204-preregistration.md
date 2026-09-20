# C204 preregistration — live v2 mixed-channel loop

**C203 ACCEPTED PASS. C204 ACTIVE / NOT YET JUDGED. C205 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can the accepted frozen C181 necessity bases and C188 target selectors perform **live inference
after every mixed-channel observation**, using the exact canonical72-feature prefix of the current
structured-v2 packet, while reproducing the accepted C199 ALLOWED predictions/logits and preserving
the accepted C203 mixed-channel dispatch/resource/final-SUFFICIENT behavior?

This changes only saved-decision replay -> live frozen-model inference.

## Changed variable

C203:

```text
current state
-> read accepted saved necessity/target decision
-> mixed-channel acquisition
```

C204:

```text
current state
-> construct structured-v2 packet
-> exact first72 canonical v1 features
-> live frozen C181/C188 inference
-> compare to accepted C199 saved reference
-> mixed-channel acquisition
```

The12-bit structured-v2 channel tail is **not** passed to the learned models. It remains routing
metadata only.

## Held constant

- C174/C190 coherent-world cohort and row/world identities;
- budget13;
- accepted C181 INTERNAL_SEMANTICS bases;
- accepted C188 selector heads;
- raw argmax and inference implementation;
- CPU float32, torch threads=2, deterministic algorithms=True;
- C200 structured-v2 contract;
- C201 selected-fact mapper;
- C202/C173 acquisition lifecycle;
- C203 fixed fact->channel layout:
  `[RETRIEVE, OBSERVE, ASK_USER, RETRIEVE]`;
- parent RETRIEVE-only authority before every learned decision;
- temporary all-channel authority only after a live NEEDS+target;
- source values and provider fixtures;
- resource charging/accounting.

No retraining, new seed, threshold repair, target repair or saved-decision substitution.

## Accepted identities

C203:
- execution HEAD `293b440adfddcbda0a18fd66184768c27aff49a2`
- summary SHA256 `5fb52a6f056eea1fcf2ff719a9fa8c9efa9cc0d941ea26f50fdceed4c2db56c2`

C199 reference:
- execution HEAD `48100f36f4f1acdf44d5cb1d508b907e19724c10`
- summary SHA256 `0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`

C181 summary SHA256:
`bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`

C188 summary SHA256:
`2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153`

All3 INTERNAL_SEMANTICS base checkpoint files and all9 selector checkpoint files must match their
accepted summary artifact hashes and must also appear in the accepted C199 protected input hash set.

## Live structured-v2 decision input

For each active learned decision:

1. verify parent RETRIEVE-only authority;
2. charge one decision;
3. build current structured-v2 TaskView using the fixed C203 channel layout;
4. encode to84 features;
5. require:
   - v2[0:72] == canonical `structured_task_input.encode(current_v1_view).features`;
   - v2 binding == canonical v1 binding;
   - v2 encode/decode roundtrip exact;
6. feed only v2[0:72] to the frozen learned models.

Required global live decision packets:

```text
v2 packets       214948
learned rows     214948
v2 prefix errors 0
```

## Live prediction reference

The accepted C199 ALLOWED artifact is comparison-only. It does not drive C204 actions.

For each exact episode/phase:
- live necessity argmax must equal C199;
- live target argmax stored for the active phase must equal C199;
- necessity logits max absolute delta <=1e-6;
- target logits must preserve the exact finite/-inf mask;
- finite target logit max absolute delta <=1e-6.

Required global:

```text
necessity prediction errors 0
target prediction errors    0
max necessity logit delta   <= 1e-6
max target logit delta      <= 1e-6
```

Parent C199 writer semantics remain authoritative: a target-head output may be stored on a
terminal SUFFICIENT phase; it is compared as a prediction but never executed unless live necessity
is NEEDS.

## Live mixed-channel action path

When live necessity == NEEDS:
- live target must currently be UNOBSERVED;
- temporarily enable all three runtime channels;
- construct current structured-v2 channel layout;
- C201 mapper produces typed proposal for the unchanged live target;
- existing action/acquisition runtime reserves/dispatches/publishes;
- matching channel provider only;
- exact coherent-world value;
- nonselected facts unchanged;
- restore parent RETRIEVE-only authority before next live decision.

## Fixed workload / C203 equivalence

Required:

```text
blocks               9
episodes              85824
decisions             214948
model input rows      214948
v2 packets            214948
acquisitions          129124
final SUFFICIENT      85824
channel switches       32564

RETRIEVE               88918
OBSERVE                 21252
ASK_USER                18954
```

All9 block records must have:
- prediction errors0;
- prefix errors0;
- scientific/runtime errors0;
- projection_error0;
- logit deltas within tolerance.

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/model-fingerprint/regression/incomplete/protection failures are
**INVALID EXECUTION / RETRY SAME C204**.

No result may modify checkpoints, tolerance, layout, workload or reference.

## Scope / non-claims

C204 registers:
- training0;
- fresh seeds0;
- network calls0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS means that the already-accepted72-feature learned policy can be **recomputed live** from the
canonical prefix of structured-v2 states while the tail drives mixed-channel routing separately.

PASS does not establish:
- learned use of channel metadata;
- learned choice among multiple eligible channels;
- real sensor/user transport;
- independent holdout;
- final Gate E completion.

## Authoring quality gate

C204 OWN:
- `fold_lm/v05_benchmarks/gate_e_c204_live_v2_mixed_channel_loop.py`
- `tests_lm/test_v05_c204_live_v2_mixed_channel_loop.py`
- `tools/run_c204.ps1`
- `tools/invoke_c204.ps1`
- `tools/invoke_active.ps1`
- this preregistration;
- `docs/live-v2-mixed-channel-loop-v0.1.md`

Expected:
- source pins38;
- protected inputs80;
- output artifacts5;
- new tests33;
- focused regression **1846 =1813+33**;
- regression modules **89**.

The33 tests include a one-episode production-path integration:
v2 encode -> live mocked model output -> real mixed-channel mapper/action/acquisition dispatch ->
publication -> next live decision -> SUFFICIENT.

Scientific manifest SHA256:

`3af3186623e7281c182361eafad0eb6336691e073e76e94ae089d5f2464f24af`

## Post-authoring review requirement

Before execution, committed remote bytes must be re-fetched and reviewed for:
- exact source-string assertions;
- C181/C188 writer/checkpoint semantics;
- C199 stored-vs-executed target semantics;
- C204 comparison-only reference usage;
- v2 prefix/tail separation;
- live inference before action;
- authority grant/restore ordering;
- source/protected counts;
- runner/launcher argument indexing and all local run paths;
- C205 non-registration.

Until review passes:

`post_authoring_review = PENDING`

The active dispatcher and direct C204 launcher were rewritten after a PowerShell parse error. The
next review must re-check their complete committed bytes, test31-33 source assertions, selected
launcher parse guard, stale-command skip ordering, updated protocol/AGENTS execution rule and
current formal-state resolution before any execution command is issued.

## Execution / stop

Use the final reviewed registration HEAD as `ExpectedHead`. User-facing execution must call `tools/invoke_active.ps1`, not an experiment-numbered launcher.

Expected progress:
- C204 repository preflight
- C204 authoring syntax preflight
- source_and_artifact_precheck PASS
- focused regression1843/1843
-9 live block progress records
- RESULT
- POSTCHECK
- remote log publication

Judge C204 before any C205 registration.
