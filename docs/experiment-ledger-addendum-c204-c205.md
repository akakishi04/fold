# C204 acceptance / C205 handoff

## Formal judgment

**C204 — ACCEPTED VALID NEGATIVE.**
**C205 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful valid C204 execution:
- scientific execution HEAD: `0ef49a4f97b516a00066df4986c062f98fda676d`
- published log commit: `df0a850ee298c643a7b775988cef69cd24b42655`
- log SHA256: `f1c4db1a22d61b0ebfc09ff21937e500eefe6f43f1d198b3c2920fcc07c2b56a`
- log bytes: 325219
- summary: `runs/c204-v5e-live-v2-mixed-channel-91f31086978f4d2fa54dfe8abcf78200/summary.json`
- summary SHA256: `9c02e4dbd497fbc91ae25c02f4cc5a3baad0af8cf9cc296f2bac0f6f8ffe72e9`
- focused regression: **1846/1846** in 43.726s
- all9 live blocks completed
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False

## Deciding evidence

Behavioral/runtime equivalence succeeded:
- episodes85824
- decisions214948
- acquisitions129124
- final SUFFICIENT85824
- structured-v2 packets214948
- learned input rows214948
- v2 prefix errors0
- necessity prediction errors0
- target prediction errors0
- RETRIEVE88918 / OBSERVE21252 / ASK_USER18954
- channel switches32564
- runtime/scientific/projection failures0

The preregistered numeric replay tolerance did **not** pass:
- max necessity logit delta = `5.0067901611328125e-06`
- max target logit delta = `5.7220458984375e-06`
- fixed tolerance = `1e-6`

Therefore:
- scientific_status FAIL
- candidate_gate_passed False
- execution validity True

This is accepted as a valid negative result. The threshold is not relaxed after observation.

## Scientific interpretation

The accepted frozen C181/C188 models can be recomputed live from the exact72-feature canonical
prefix of structured-v2 states without any argmax/action divergence. The full mixed-channel loop
reproduces the accepted C199/C203 decision and runtime trajectory exactly.

However, C204 does not establish logit replay equivalence at the preregistered1e-6 tolerance.
Numerically, live logits differ by roughly2.4e-6..5.7e-6 depending on block while preserving every
recorded decision.

## Confound / next boundary

C199 phase0 inference was generated on the **1768 unique observable PILOT states** and then expanded
to9536 coherent worlds via `local_rows`.

C204 instead recomputed phase0 directly on the **9536 expanded rows**, which contain repeated
observable inputs associated with different hidden coherent worlds. Since `combined_predict`
batches rows in chunks of1024, the numerical matrix workload/batch composition differs even though
the canonical72-feature rows themselves are identical.

Later C199 phases are already live active-cohort inference, so the smallest next attribution
question is phase0 batching.

C205 must not change the1e-6 threshold. It should compare, for each of the9 accepted model pairs:

A. canonical unique structured-v2 phase0:
```text
1768 unique current states
-> v2 encode
-> exact72 prefix
-> frozen inference
-> expand outputs by accepted local_rows
```

B. expanded-direct structured-v2 phase0:
```text
9536 world-expanded current states
-> v2 encode
-> exact72 prefix
-> frozen inference directly on all9536 rows
```

Both paths use the same checkpoint, BATCH1024, CPU float32, threads2, deterministic algorithms and
the same C199 phase0 reference.

Scientific question:

> Are the C204 gate-breaking logit maxima fully reproduced by phase0 expanded-direct batching,
> while canonical unique structured-v2 batching remains within the original1e-6 tolerance?

If yes, the valid negative is attributable to batch-composition numeric replay rather than v2
prefix/state or behavioral-policy drift. This is attribution only; it does not retroactively turn
C204 into PASS.
