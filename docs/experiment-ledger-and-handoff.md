# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Standalone root paths `fold_lm/`, `docs/`, `tests_lm/`, `tools/`; no monorepo `fold/` prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Diagnostic probes CPU float32/two threads; RTX4070TiSUPER installed.
Protected C37 `runs/chatgpt-last-result.json` SHA256
`FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931`.
Protected `runs/fixtures/v05-c-composition-20260921.pt` SHA256
`A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E`.

Read `AGENTS.md`, `docs/experiment-conversation-handoff-protocol.md`, this file,
`docs/experiment-ledger-addendum-c187-c188.md`, and
**`docs/experiment-ledger-addendum-c188-preregistration.md`**.

Formal response order:
verdict -> validity -> metrics -> interpretation -> confounds -> ledger -> next design ->
implementation/preregistration -> reproducible PowerShell -> progress -> log collection -> stop.

User clarification: after judging and saving the current experiment, prepare the next
single experiment fully in the SAME RESPONSE; do not wait for another "continue".
Separate acceptance and preregistration commits are required. Never skip judgment,
execute an unregistered experiment, or advance past the next unresolved C.
Never alter checkpoints, seeds, cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C187 ACCEPTED PASS. C188 ACTIVE / NOT YET JUDGED. C189 NOT REGISTERED.**
C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS;
C170-C173 PASS; C160/C168/C169 VALID NEGATIVE.
All earlier judgments and checkpoints remain unchanged.

C187 execution HEAD:
`bbb79df40f3428f358bec7381cd872efa7845e63`.
C187 acceptance commit:
`bdbc71ca17a7a6138f54d1188c17ce7dd33dcece`.

## Latest accepted C187

C187-v5e-restricted-acquisition-necessity /
V5-E-RESTRICTED-ACQUISITION-NECESSITY.

1377/1377 tests49.777s; source/artifact precheck PASS; 80 blocks/296960 episodes.
Each INTERNAL_SEMANTICS candidate seed181001/2/3:
37120 episodes, zero failures, zero initial/missed/unnecessary/post/false-sufficient/
contract errors, 7680 proposals,4608denials,3072allowed reads/admissions,
zero initial decision flips from unrestricted C185.

Candidates total111360episodes/23040proposals/13824denials/9216reads+admissions/
88320skips/0failures. Restricted provider calls0.
56376 original predictions replayed exactly; max logit delta0.
No training/fresh seed/teacher/auxiliary/answer/proof/network/coreEvidenceState writes.
Protected inputs preserved, tracked tree clean, execution HEAD preserved, validTrue.
Production runtime modifiedFalse; Gate E candidateFalse.

C187 supports only bounded separation:
learned semantic NEEDS remains correct when RETRIEVE is denied/unavailable/out of
acquisition budget, while unchanged C172/C173 authority independently prevents IO.
Target/tool remain handwritten and only one fact is missing. No learned alternative tool,
retry, answer/proof, language, larger/repeated-variable, independent final or Gate E claim.

C187 summary:
`runs/c187-v5e-restricted-acquisition-cc3717a5a9994142a9147953dce83573/summary.json`
SHA256 `910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`.

Reviewer reconstructed the 269632-byte canonical summary and reaggregated the 80 records,
candidate seed totals, control-inclusive totals and provider/publication arithmetic.
Separate artifacts/full NPZ/traces/checkpoints/data and user tests were not independently rerun.

## Active C188 — learned multi-missing target selection

Experiment:
`C188-v5e-multimissing-target-selection` /
`V5-E-MULTIMISSING-TARGET-SELECTION`.

One question:
Can a learned selector on frozen accepted C181 INTERNAL_SEMANTICS representations choose
a currently influential missing fact when more than one fact is unobserved, strictly
better than a TRAIN-only syntax-blind frequency reference?

This is deliberately OFFLINE. Do not connect the first learned target selector to
C172/C173 acquisition in C188. If C188 passes, live target acquisition is a later C.

### Target teacher

An unobserved fact is valid iff two completions consistent with visible observations,
differing only in that fact, yield different final outputs.
Teacher is programmed TRAIN supervision/scoring only. Unknown completion values are not
model features. Set-mass loss accepts every valid target; no arbitrary single target label.

### Cohorts

Same C174 split / same four repeatedly inspected development PILOT groups.

Primary discriminating NEEDS cohort:
- TRAIN3824: missing2=2696, missing3=1128
- PILOT528: missing2=376, missing3=152
- PILOT missing3 target-set sizes: valid1=72, valid2=80

Secondary all PILOT NEEDS with missing2/3:1768.

Exclude one-missing because target choice is trivial and already covered C185-C187.
Exclude primary rows where every unknown is influential because every choice is trivial.

### Frozen bases and selector

Use only three accepted C181 INTERNAL_SEMANTICS bare bases:
181001,181002,181003; 25726 frozen inference parameters each.

Capture all seven actual 64d shared-cell states from unchanged C181 TREE_LINKS forward.
Per candidate fact:
448 flattened hidden dimensions + leaf-position onehot7 = **455 features**.

Shared selector:
`455 -> 64 ReLU -> 1`, **29249 trainable parameters**.

Fresh target-head seeds188001/188002/188003 crossed with all3 frozen bases = **9 heads**.
For same head seed, initialization and minibatch row schedule must match across bases.

TRAIN only: 2000 updates/head, batch256, Adam lr.001, CPUfloat32/two threads,
row RNG head_seed+1000000. Base weights never update.

Set-mass loss:
`logsumexp(all unknown logits) - logsumexp(valid influential logits)`.

Inference masks observed facts using observable missingness only. Teacher absent.

### Fixed references

FIRST_UNKNOWN:
- m2 188/376 = .5
- m3 84/152 = .552631578947...
- macro .526315789473...

Formal TRAIN-only syntax-blind frequency reference:
visible fact-table key only,32 keys, no syntax/group/template/PILOT labels.
- m2 268/376 = .7127659574468085
- m3 128/152 = .8421052631578947
- macro **.7774356103023516**

### Fixed gate

For EACH of all9 selectors:
- m2 hit rate > 268/376
- m3 hit rate > 128/152
- equal m2/m3 macro > .7774356103023516
- selected observed =0
- finite raw unknown-target logits

All9 must pass. No mean/best-head/ensemble rescue. Ties fail.

Valid finite failure -> ACCEPTED VALID NEGATIVE.
Source/hash/schema/nonfinite/incomplete/prerequisite failure -> INVALID / retry SAME C188.

PASS is only bounded learned WHICH-fact evidence. It is NOT live learned acquisition,
tool/provider choice, retry/stopping, language/larger/repeated-variable generalization,
independent final confirmation, answer/proof generation or Gate E.

### Workload / implementation

Expected:
- base checkpoint loads3
- base feature rows16776 / forwards18 / cell calls126
- trained heads9
- selector updates18000
- sampled TRAIN rows4608000
- PILOT selector predictions15912
- actual acquisitions/network/evidence writes/answer/proof =0
- production runtime modifiedFalse; Gate E candidateFalse

Expected outputs:14 artifacts excluding summary.
Historical source pins103 / protected paths239.
Scientific manifest SHA256 `0f8d22b00839e5a7506d5dabc06c64a7add86eb8a00e41840414842b7a773682`.

New files:
- `fold_lm/v05_benchmarks/gate_e_c188_multimissing_target_selection.py`
- `tests_lm/test_v05_c188_multimissing_target_selection.py`
- `tools/run_c188.ps1`
- `docs/experiment-ledger-addendum-c188-preregistration.md`

Local validation before registration:
exact new module compiled;36/36 new tests PASS. Tests independently enumerate the full
C174 Boolean family and exact cohorts/references, set-mass loss, masking, deterministic
head initialization/schedules, toy fit, gate and scope.
Not yet executed: official C181 checkpoints, full repository chain, Windows PowerShell,
full regression or formal C188 training/evaluation.

Expected focused regression:
**1413 =1377 existing +36 new;73 modules.**

## Evidence chain

C186 summary SHA `e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82`.
C185 summary SHA `843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949`.
C184 summary SHA `7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04`.
C183 summary SHA `ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24`.
C182 summary SHA `06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73`.
C181 summary SHA `bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`.
Dataset SHA `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.

Historical C186 loader-recovery invalid attempt remains INVALID, not scientific evidence.
C184 local-index normalization is an engineering contract, not learned naming invariance.
C181 auxiliary TRAIN supervision is programmed extra information; not unique mechanism proof.

## Stop / separate tracks

Run only registered C188. Do not register or execute C189 until C188 result is judged,
ledger/handoff is updated, and at most one next scientific question is prepared in the
same response.

Gate E full candidate/baseline/split/numerical contract remains outstanding.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate research tracks.
No reset/rebase/history rewrite/historical artifact commit_sha edit.
