# C203 acceptance / C204 handoff

## Formal judgment

**C203 — ACCEPTED PASS.**
**C204 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C203:
- scientific execution HEAD: `293b440adfddcbda0a18fd66184768c27aff49a2`
- published log commit: `618772f2736279ae6389bfc5e488d1eb7c6b2553`
- log SHA256: `f995c62b78b8dd23d2f29244c3ef52e4ea5243cbea6f3fbf0dacb968126ce8c2`
- log bytes: 311394
- summary: `runs/c203-v5e-mixed-channel-multistep-f8a35e95871341ddafa1a273aed80cfb/summary.json`
- summary SHA256: `5fb52a6f056eea1fcf2ff719a9fa8c9efa9cc0d941ea26f50fdceed4c2db56c2`
- focused regression: **1813/1813** in 77.135s
- all9 registered blocks completed with failed0
- source/artifact precheck PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

## Deciding evidence

- episodes85824
- learned decisions214948
- acquisitions129124
- final SUFFICIENT85824
- RETRIEVE acquisitions88918
- OBSERVE acquisitions21252
- ASK_USER acquisitions18954
- within-episode channel switches32564
- failures0
- projection errors0
- decision trace errors0
- target errors0
- route errors0
- action/dispatch/provider-channel/receipt/fact-update/resource/final-status errors0
- candidate_gate_passed True

## Scientific interpretation

C203 establishes that the accepted C199 multi-step learned decision trace can be replayed while
fact-specific acquisition channels switch within an episode. The fixed fact->channel mapping
routes through the accepted C201 mapper and real structured acquisition lifecycle, then restores
the parent RETRIEVE-only authority masks before the next replayed learned decision.

The observed per-channel totals and32564 within-episode channel switches exactly match the
pre-execution deterministic projection of the frozen parent artifact.

## Non-claims

C203 does not establish:
- live re-inference after each mixed-channel observation;
- whether the accepted learned necessity/target models remain decision-identical when driven from
  structured-v2 live states rather than a saved decision trace;
- learned preference among multiple eligible channels;
- real sensor or real user transport;
- final mixed-family Gate E quality or final Gate E completion.

## Next boundary

C204 should replace only the saved-decision replay with **live frozen-model inference**.

Hold fixed:
- accepted C181 INTERNAL_SEMANTICS necessity bases;
- accepted C188 target selectors;
- budget13 C174/C190 coherent-world cohort;
- C200 structured-v2 fact-channel metadata;
- C201 mapper;
- C202/C173 acquisition lifecycle;
- fixed C203 fact->channel layout;
- parent authority restoration before each learned decision.

At each decision:
1. build the current structured-v2 TaskView;
2. verify its first72 encoded features equal the canonical live v1 packet;
3. feed exactly that72-feature prefix to the frozen accepted necessity/target models;
4. compare live predictions/logits against the accepted C199 ALLOWED artifact for that exact
   episode/phase;
5. if live NEEDS, execute the selected fact through the fixed mixed channel;
6. restore parent authority and continue.

Scientific question:

> Can the full mixed-channel multi-step loop perform **live frozen-model re-inference** after each
> observation and remain decision/logit equivalent to accepted C199 while preserving the C203
> dispatch/resource/final-SUFFICIENT contract?

C204 adds no training and does not let channel metadata alter the existing72-feature learned
models. The v2 tail drives routing only; the canonical v1 prefix drives the frozen learned models.
