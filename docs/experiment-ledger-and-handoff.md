# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Standalone root paths `fold_lm/`, `docs/`, `tests_lm/`, `tools/`; no monorepo `fold/` prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Diagnostic probes CPU float32/two threads; RTX4070TiSUPER installed.

Read `AGENTS.md`, `docs/experiment-conversation-handoff-protocol.md`, this file,
and the latest accepted/preregistered addenda. Formal experiment responses:
verdict -> validity -> deciding metrics -> interpretation -> confounds -> ledger ->
next single design -> implementation/preregistration -> reproducible command -> stop.

After judging one experiment, prepare at most the next one in the SAME RESPONSE.
Use separate acceptance and preregistration commits. Never skip judgment, mutate earlier
scientific conditions, or register C+2 before C+1 is judged.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C188 ACCEPTED PASS. C189 NOT REGISTERED at this acceptance commit.**
C187/C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS.
All earlier judgments and checkpoints remain unchanged.

C188 execution HEAD:
`683d795b12d4f0aada4850dcac2a010e699882ad`.

## Latest accepted C188

Experiment:
`C188-v5e-multimissing-target-selection` /
`V5-E-MULTIMISSING-TARGET-SELECTION`.

Execution:
- 1413/1413 focused tests, 43.155s
- source/artifact precheck PASS
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- diagnostic execution valid True
- production runtime modified False
- Gate E candidate False

Parent C187 summary:
`910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`.

C188 summary:
`runs/c188-v5e-multimissing-target-selection-81830a0e8ba741519c9172bdf2f7a7bc/summary.json`
SHA256:
`2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153`.

Uploaded log:315279bytes;SHA256
`8f8308404031fc894db07360f80b54eebff3c64db05fc84e7eb50fba5dc1887b`.
Reconstructed canonical summary79138bytes/exact hash match.

### Deciding result

Frozen accepted C181 INTERNAL_SEMANTICS bases:
181001/181002/181003.

Fresh C188 target-head seeds:
188001/188002/188003.

Nine total selectors; each uses frozen seven-node hidden states plus fact leaf-position
one-hot; 29249 trainable head parameters; C181 bases never updated.

Primary PILOT discriminating cohort528:
- missing2=376
- missing3=152

TRAIN-only syntax-blind frequency reference:
- m2 268/376 = .7127659574468085
- m3 128/152 = .8421052631578947
- macro .7774356103023516

Every one of 9 selectors:
- m2 376/376 = **1.0**
- m3 152/152 = **1.0**
- macro **1.0**
- selected_observed **0**

Strict gate passes 9/9; no averaging/best-head rescue.

Secondary full multi-missing PILOT NEEDS1768:
- missing2 1152/1152
- missing3 616/616
- every selector 1768/1768 = **1.0**

For each fresh head seed, all three frozen-base copies have identical initial target-head
fingerprint and identical minibatch schedule hash.

Workload:
3 frozen base loads;9 target heads;18000 target updates;4608000 sampled TRAIN rows;
16776 frozen base feature rows;18 base forwards/126 cell calls;15912 PILOT selector
predictions;0 actual acquisitions/network/evidence writes/answers/proofs.

### Claim boundary

C188 supports only:
on the registered C174 development family, a small learned target selector on frozen
accepted C181 internal states can choose an influential missing fact among multiple
unknown facts better than the registered TRAIN-only syntax-blind reference.

Do NOT claim:
live target acquisition, learned tool/provider choice, retry/stopping, global information
gain optimality, repeated-variable/larger-expression/language generalization, independent
final holdout, answer/proof generation, production adoption or Gate E completion.

The same four PILOT semantic groups are repeatedly inspected development groups and the
target teacher is programmed logical supervision.

Reviewer independently reaggregated the 9 strict gates, primary/secondary hit counts,
paired head construction and workload from the uploaded complete RESULT summary.
Separate C188 artifacts/NPZ/checkpoint bytes and user regression execution were not
independently rerun.

## Next single design

Proposed C189 scientific question:

**Can one frozen accepted C181 necessity base + one frozen accepted C188 selector head,
sharing one initial forward, choose an influential target in a multi-missing row, drive
exactly one real C172/C173 RETRIEVE of that selected external fact, and then correctly
reclassify the actual updated state?**

Design constraints:
- reuse all 9 accepted C188 base/head combinations;
- no new training or fresh seed;
- identity/original C174 local fact layout only;
- both possible selected-fact bits;
- all1768 PILOT NEEDS rows with missing2/3; 528 discriminating rows remain target-choice
  deciding subset;
- one actual read/admission maximum; no second acquisition even if post state remains NEEDS;
- no answer/proof;
- initial C181 necessity and learned target emitted from one shared frozen base forward;
- post decision is necessity-only;
- target teacher and post logical label are scoring-only and never enter policy/provider.

C189 must be separately preregistered after this acceptance commit. C190 remains unregistered.

## Evidence chain / persistent limits

C187 summary SHA `910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`.
C186 SHA `e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82`.
C185 SHA `843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949`.
C184 SHA `7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04`.
C181 SHA `bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`.
Dataset SHA `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.

No natural-language, larger/repeated-variable, multi-step target planning, learned-tool,
answer/proof, independent final Gate E claim. Multi-Axis/MA-1 and PC-ALM/FHLC remain
separate tracks. No history rewrite.
