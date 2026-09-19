# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Standalone root paths `fold_lm/`, `docs/`, `tests_lm/`, `tools/`; no monorepo `fold/` prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.

Read `AGENTS.md`, `docs/experiment-conversation-handoff-protocol.md`, this file,
`docs/experiment-ledger-addendum-c188-c189.md`, and
**`docs/experiment-ledger-addendum-c189-preregistration.md`**.

Formal work order:
verdict -> execution validity -> deciding metrics -> interpretation -> confounds ->
ledger -> next one-question design -> implementation/preregistration -> command -> stop.

After judging one experiment, prepare at most the next one in the SAME RESPONSE, using a
separate acceptance commit followed by a separate preregistration commit. Never modify
earlier scientific conditions to obtain PASS.

Execution-log handoff: after each formal run, mirror only `runs/chatgpt-last.log` to
`docs/experiment-run-logs/c###/latest.log` plus `latest.json` using
`tools/publish_experiment_log.ps1`, commit/push that documentation, then the user may simply
say 「終わった」. The next assistant fetches the remote published log and verifies metadata/SHA.
Binary/data/run artifacts remain local-only.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C188 ACCEPTED PASS. C189 ACTIVE / NOT YET JUDGED. C190 NOT REGISTERED.**
C187/C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS.
All previous judgments/checkpoints remain unchanged.

C188 execution HEAD:
`683d795b12d4f0aada4850dcac2a010e699882ad`.

C188 acceptance commit:
`2edadff6f8fab1c3c26da46adee630d12e433be8`.

## Accepted C188

C188 summary:
`runs/c188-v5e-multimissing-target-selection-81830a0e8ba741519c9172bdf2f7a7bc/summary.json`
SHA256:
`2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153`.

1413/1413 tests; source/artifact precheck PASS; protected inputs preserved;
diagnostic execution valid True; production runtime modified False.

All 9 frozen-base/fresh-head selectors:
- primary discriminating PILOT528: 528/528 target hits
- missing2:376/376
- missing3:152/152
- equal macro1.0
- selected observed0
- full multi-missing secondary1768/1768

Formal TRAIN-only syntax-blind reference macro:
`.7774356103023516`.

All same-head-seed copies preserved paired initial head fingerprint and minibatch schedule.
No base update, acquisition, answer, proof or network call occurred in C188.

C188 claim is bounded to learned influential-fact selection on the repeatedly inspected
four-group C174 development family. No live target acquisition, tool choice, iterative
planning, language/larger/repeated-variable generalization, final holdout or Gate E claim.

Uploaded C188 log315279bytes SHA256
`8f8308404031fc894db07360f80b54eebff3c64db05fc84e7eb50fba5dc1887b`.
Canonical summary79138bytes/reconstructed hash exact.

## C189 invalid-attempt recovery

First C189 attempt at execution HEAD `8733da67f8fee522d4deb2417c942ac734b582a9`
is **INVALID EXECUTION**: source/artifact precheck failed before regression/model work
because the registered C189 benchmark source contained NUL/non-UTF-8 bytes
(`SyntaxError: source code string cannot contain null bytes`).

Published invalid log:
`docs/experiment-run-logs/c189/latest.log` at log commit
`a7fe8158df96f41541579be4f35722daf81e6687`,
SHA256 `3bf74d001b1ec24cc202df77a9ab7ebe3ff5f17ff4122aafd3b643d5d0d7a5b2`.

Recovery changes only source serialization/implementation validity. Scientific manifest,
seeds, checkpoints, cohort, workload, gate and interpretation remain unchanged.
Retry SAME C189; C190 remains unregistered.

## C189 second invalid-attempt recovery

Second attempt at execution HEAD `e8e09e267d686427f2e3381e171e9f54b34533f6` is also
**INVALID EXECUTION** before regression/model work. UTF-8 import succeeded, then the fixed
scientific-manifest SHA guard failed because the constant was a transcription error.
Canonical manifest SHA is
`e1ba8c1b84dc016410e91432eadfc53e28a46dd49cb91bf015d3336f37e8402e`.
No manifest field, seed, checkpoint, cohort, workload, gate, threshold or interpretation changed.
Published second-invalid log commit: `0f0594ddb9dd0a607451318d7ba33a6ecd061a7e`;
log SHA256 `438ebe247d303d555719b679208e99d11224aae4d556182af4b8dd5d80ce6bca`.
Retry SAME C189; C190 remains unregistered.

## C189 third invalid-attempt recovery

Third attempt at execution HEAD `5af67ef5e9b71a640f0787877af2e8cd7bb5ca2d` passed precheck and entered focused regression.
The regression stopped at 1449 tests with exactly six new C189 acquisition-test failures.
The synthetic C189 unit-test helper encoded evidence_time/revision as 0/0, unlike real C174
rows and registered providers which use 1/1. C173 correctly rejected those synthetic dispatches
as SOURCE_EPOCH_MISMATCH before provider IO. This is a test-fixture defect, not candidate evidence.
Published log commit: `1da20c1db1f3127be3070c4f76088b7292fe7426`;
log SHA256 `c2e8f17ed9b5ab934dc525707c6a70bf67c4141717ff5a174f60dcc90365090e`.
Recovery changes only test fixture epoch/revision to 1/1. Retry SAME C189; C190 remains unregistered.

## Active C189 — live learned multi-missing target acquisition

Experiment:
`C189-v5e-live-multimissing-target-acquisition` /
`V5-E-LIVE-MULTIMISSING-TARGET-ACQUISITION`.

Question:
Can frozen accepted C181 necessity plus frozen accepted C188 target selection share one
initial forward, send the raw learned selected fact through a real bounded C172/C173
RETRIEVE exactly once, and correctly reclassify the actual post-admission state?

### Held fixed

- all 3 accepted C181 INTERNAL_SEMANTICS bases:181001/2/3
- all 9 accepted C188 base/head combinations; head seeds188001/2/3
- C174 TRAIN/PILOT data and semantic groups
- C172 action runtime / C173 acquisition lifecycle
- C185 external opaque fact identities and single-fact source contract
- raw argmax / no repair
- no new training, fresh seed, answer or proof

### Deliberate simplification

C189 uses **identity/original C174 local fact layout only**.
Do not add a renaming perturbation here; C184/C185 already measured that engineering
boundary and first live target integration should not conflate another representation shift.

### Cohort / episodes

All1768 PILOT NEEDS rows with missing2/3:
- missing2=1152
- missing3=616
- discriminating target subset=528

Cross all9 selectors with selected-fact source bit0/1:
**31824 live episodes /18 blocks**.

### Initial combined decision

Start original resources12internal/4acquisitions/step7.
Trusted scheduler charges one decision before encoding:
11internal/4acquisitions/step8.

One frozen C181 TREE_LINKS forward:
- C181 readout emits NEEDS/SUFFICIENT;
- same seven cell states feed paired frozen C188 target head;
- observed facts masked;
- raw target argmax retained.

Target feature path uses cell states+leaf-position only, so runtime resource coordinates
do not enter the target head. Formal live target scores must replay C188 within atol1e-6.

### Dynamic external endpoint binding

Owners initially carry exact RuntimeState but no RETRIEVE endpoint.
After the raw learned target is produced, trusted scaffolding binds the matching external
single-fact endpoint while preserving RuntimeState exactly.

Then raw learned local target enters C172 `RETRIEVE`; C173 may read/publish only that fact.
Eight C185-format sources are fixed, one per external fact and bit.

This endpoint binding does not inspect teacher labels or hidden completions.

### Post decision

Exactly one acquisition maximum. Normal successful path:
initial decision1 + action1 + dispatch2 + post decision1 =
final7internal/3acquisitions/step12.

Frozen C181 makes one post-acquisition necessity-only decision.
If still NEEDS, stop unresolved; **no second acquisition**.
SUFFICIENT remains only a classification, not an answer.

### Scoring only

- initial target correctness: C188 influential-target set
- post necessity correctness: C174 logical necessity on actual final visible facts

Neither teacher enters policy, endpoint selection, proposal or provider.

### Parent replay

Before live episodes replay all15912 accepted C188 full-multi-missing target predictions:
exact argmax, finite unknown-target logit delta<=1e-6.

### Fixed gate

Every one of18 blocks must have:
- episodes1768 / discriminating528
- initial necessity errors0
- all-target errors0
- discriminating target errors0
- target replay errors0
- selected observed0
- live target logit delta<=1e-6
- missed acquisition0
- post necessity errors0
- contract errors0
- reservations/provider calls/publications1768
- decision charges3536
- internal charged8840
- post sufficient+post needs=1768

No averaging/head rescue. Valid finite failure => ACCEPTED VALID NEGATIVE.
Source/hash/schema/replay/nonfinite/incomplete/protection failure => INVALID, retry SAME C189.

### Workload / protection

- base loads3
- target-head loads9
- training0 / fresh seeds0
- static target replay15912
- static base feature rows5304 / forwards6 / cellcalls42
- live initial base rows31824
- live target rows31824
- live post base rows0..31824
- total base rows max68952
- ideal reads/publications31824
- network/coreEvidenceState/answer/proof0
- production runtime modifiedFalse
- Gate E candidateFalse
- historical source pins107
- protected paths258
- outputs13 excluding summary

Scientific manifest:
`6acccb0b116a57a34e4f91733d0a15ac345d144ba9b6cb0db8a1e7af4ecf0e47`.

New files:
- `fold_lm/v05_benchmarks/gate_e_c189_live_multimissing_target.py`
- `tests_lm/test_v05_c189_live_multimissing_target.py`
- `tools/run_c189.ps1`
- `docs/experiment-ledger-addendum-c189-preregistration.md`

Expected regression:
**1449 =1413 existing+36 new;74 modules.**

Reviewer syntax-compiled new Python sources and executed pure manifest/gate checks.
Complete repo/C172/C173 integration cannot be rerun in reviewer sandbox because no complete
checkout/GitHub DNS. Formal C189 remains unexecuted.

## Evidence chain / persistent limits

C187 SHA `910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`.
C186 SHA `e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82`.
C185 SHA `843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949`.
C184 SHA `7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04`.
C181 SHA `bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`.
Dataset SHA `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.

No iterative target planning, learned tool/provider/retry/stopping, language, larger or
repeated-variable expression, answer/proof or independent final Gate E claim follows.

Do not register/execute C190 before C189 judgment. Multi-Axis/MA-1 and PC-ALM/FHLC remain
separate tracks. No history rewrite.
