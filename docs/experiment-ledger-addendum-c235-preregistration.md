# C235 preregistration — frozen C234 TRAIN/EVAL binding diagnostic

**C234 ACCEPTED VALID NEGATIVE. C235 ACTIVE / NOT YET JUDGED. C236 NOT REGISTERED.**
Stage V5-B-FROZEN-BINDING-DIAGNOSTIC. Gate E PASSED; Gate F NOT PASSED.

## One scientific question

With the six accepted C234 step400 models frozen, is the observed contextual-binding failure already
present on the complete TRAIN set, or is there a descriptive TRAIN-to-held-out-EVAL gap?

C235 changes evaluation coverage only. It performs no training and cannot change the C234 verdict.

## Accepted parent and artifact identity

C234 scientific execution HEAD:
`c225c2d82636085e2d639878738e1b9a7aa37b42`.

Published log commit:
`930fa77881d60558b3199b980f139ddef8bcb6ee`.

Log SHA256:
`414e2de1fafa2fe86fb84bdc18a9477100086133df938a10b0244ad446e38de8`.

Summary SHA256:
`a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`.

Local parent summary:
`runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/summary.json`.

Accepted C234 artifacts:
- binding-plan.json: `0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38`
- dataset.json: `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`
- measurements.json: `23f822d0a05faac176efc767b5702a21763946b295a76c503f01abc965c776c3`
- trained-models.pt: `711dd636597d5ec575136bd780ac303eb21ed6198d411f977bb20c67fd20bd26`
- validation-summary.json: `655dc04bd3509246c432eb8817699b5685ca300df612515d55358d78e634b629`

The parent is an accepted valid negative: status FAIL, full_binding_gate False,
gru_binding_gate False, all_replays True, all_weights_changed True and run_execution_valid True.
C235 explicitly requires that negative parent. It does not demand a parent scientific PASS.

Acceptance record:
`docs/experiment-ledger-addendum-c234-c235.md`.

## Frozen models and fixed data

Reuse all six C234 final checkpoints in their serialized order:
`234001/full`, `234001/gru_only`, `234002/full`, `234002/gru_only`,
`234003/full`, `234003/gru_only`.

Before evaluation, each loaded state must reproduce the accepted final model fingerprint.

Reuse the exact C234 dataset:
- TRAIN384 rows;
- EVAL192 rows;
- EN/JA;
- same object/value vocabulary;
- same held-out value-pair split;
- same target bytes;
- same normal/evidence-blind/query-blind renderings.

No row, split, target, prompt or checkpoint is regenerated with changed semantics.

## Changed measurement only

Evaluate the frozen models on complete TRAIN and complete EVAL under all three parent views.

Reuse C234 metrics on both splits:
- exact unconstrained answer accuracy;
- answer NLL;
- evidence/query masked accuracy and drops;
- fact-pair both-correct accuracy;
- query-pair both-correct accuracy.

Add descriptive post-inference measurements:
- supplied-value answer rate;
- mean probability mass on the two supplied values;
- first/last fact agreement;
- query-pair same-answer count/rate;
- query-pair both-correct count.

Query/target row metadata is used only after inference for scoring. It is not supplied to the model
except through the same C234 rendered prompt.

## Fixed descriptive localization

For every seed/family/language cell:
- TRAIN <0.90 -> `TRAIN_ACCURACY_BELOW_90`;
- TRAIN >=0.90 and EVAL <0.90 -> `TRAIN_AT_LEAST_90_EVAL_BELOW_90`;
- TRAIN >=0.90 and EVAL >=0.90 -> `BOTH_ACCURACIES_AT_LEAST_90`.

The0.90 reference is inherited from C234 exact-answer accuracy. These labels are diagnostic only.
They do not form a new C234 success gate and do not imply Gate F completion.

## Workload and integrity gate

Six models x two splits x three views =36 model forward calls.
Total rows presented across those forwards =10368.

New training steps0. Optimizer steps0. Checkpoint writes0. Network calls0.
CPU float64, threads2 and deterministic algorithms remain fixed.

C235 status PASS is an **integrity PASS only** and requires:
- all six parent checkpoints and identities valid;
- exact saved EVAL byte predictions replay;
- all saved EVAL parent metrics replay within1e-9;
- all model fingerprints unchanged before/after;
- exactly36 forward calls and10368 evaluated rows;
- exactly12 localization cells;
- no capability-pass claim;
- complete registered artifact/source protection.

No observed accuracy threshold can make the diagnostic execution fail. Conversely, source/artifact/
schema/nonfinite/replay/model-mutation failure is INVALID / RETRY SAME C235.

## Authoring and protection

OWN6:
- fold_lm/v05_benchmarks/model_c235_frozen_binding_diagnostic.py
- tests_lm/test_v05_c235_frozen_binding_diagnostic.py
- tools/run_c235.ps1
- tools/invoke_c235.ps1
- this preregistration
- docs/v5b-frozen-binding-diagnostic-v0.1.md

Parent C234 protection250 sources/358 inputs.
Add parent summary + five artifacts and OWN6:
**256 source pins /370 protected inputs**.

Direct dependencies11: C231 language/import sources plus C230/C231/C232/C233/C234 benchmark/helper
entry points and this C235 benchmark. Transitive dependencies remain parent-pinned.

New tests24; modules120; loaded2810/focused2809. Preserve only the inherited exact historical
exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Artifacts5:
diagnostic-plan.json, diagnostics.json, predictions.json, model-fingerprints.json,
validation-summary.json. Outputs remain under ignored runs/; console/receipt publication only.

Manifest SHA256:
`2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3`.

## Interpretation boundary

Low complete-TRAIN accuracy would show that the fixed recipe did not solve even its training
binding set. TRAIN>=0.90 with EVAL<0.90 would be consistent with a held-out co-occurrence
generalization gap. Neither outcome independently proves the causal role of optimizer, capacity,
architecture or memorization.

C235 does not rank full versus GRU-only, does not change C233/C234 verdicts, and makes no general
language/reasoning claim. Gate F remains NOT PASSED.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `21fdd412a95d9c4f024dc92c20a4dc17d3d6f955`.

Scope: committed remote source review and static contract audit, not formal C235 execution.

The committed C235 benchmark,24-test module, runner, launcher, preregistration, design and handoff
were re-fetched from the review HEAD. Reviewed Git blobs:

- benchmark: `12807b77a5f6bc36d185a931e54d651dcd557e39`
- tests: `2c880ae9b35a214d7a7e0425c5c674fad10027d3`
- runner: `f6debab11f8fb88c3519752626d6f4512ae3297d`
- launcher: `564359a1283a9bea333ce78611c085baa662d358`
- preregistration: `5922f62c6bc6f1ebfc5e10fc8b7a3876c6c07d88`
- design: `fc4de6e1f7d12e4d7edda5904b196f37c1c778e1`
- handoff: `389bffcfdf5d864ede24fee88efa6822c2fe2bf9`

Comparison from the C234 acceptance commit changes only C235 OWN6 plus the unpinned handoff.
No accepted C234 source/test/log/artifact is edited. The benchmark contains no fit call, optimizer
or torch.save path; it freezes loaded parameters, replays parent EVAL, checks pre/post fingerprints,
and fixes36 forwards/10368 rows/0 training. The test module contains exactly24 test methods.
Runner text contains exactly three embedded Python precheck/regression/postcheck blocks and fixes
loaded2810/focused2809. Launcher requires ACTIVE C235, a clean tracked tree, exact ExpectedHead,
runner PowerShell parsing and the accepted local C234 summary before publication.

The manifest was independently reconstructed from committed constants and hashes exactly to
`2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3`.

Not executed in the reviewer environment: Python py_compile, the24 authoring tests, the2809 focused
suite, Windows PowerShell AST, accepted user-local C234 artifact reads, or the36-forward diagnostic.
The isolated reviewer could not resolve github.com for a local clone. These pending runtime checks
are not represented as PASS. The authoritative runner executes syntax/precheck/24 own tests/2809
focused tests before any C235 model forward; any defect stops diagnostic execution and publishes
the operational evidence.

Only review documentation may change after this review HEAD; final review text is re-fetched before
the execution HEAD is returned.

## Stop

24 own tests ->2809 focused tests ->C235 diagnostic only.
Judge C235 before C236 registration.

No training, architecture change, larger model, external data, paid API, numeric-memory tuning,
cleanup/history rewrite or threshold rescue is part of C235.
