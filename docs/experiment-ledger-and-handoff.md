# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Standalone root paths `fold_lm/`, `docs/`, `tests_lm/`, `tools/`; no monorepo `fold/` prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Diagnostic probes CPU float32/two threads; RTX4070TiSUPER installed.
Protected C37 `runs/chatgpt-last-result.json` SHA256:
`FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931`.
Protected `runs/fixtures/v05-c-composition-20260921.pt` SHA256:
`A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E`.

Read `AGENTS.md`, `docs/experiment-conversation-handoff-protocol.md`, this file,
`docs/experiment-ledger-addendum-c187-c188.md`, then the active experiment
preregistration when one exists.

Required response order for formal experiment work:
verdict -> validity -> metrics -> interpretation -> confounds -> ledger -> next design ->
implementation/preregistration -> reproducible PowerShell -> progress -> log collection -> stop.

User clarification: do NOT split result acceptance and preparation of the next single
experiment into separate responses requiring another "continue" request. After judging
and saving the current experiment, complete the next design, implementation, available
validation, preregistration and runnable command IN THE SAME RESPONSE. Separate acceptance
and preregistration commits are appropriate; a separate user turn is not required.
Never skip judgment, execute an unregistered experiment, or advance past the next unresolved C.
If blocked, state the concrete incomplete operation; never claim unperformed work.
Never alter checkpoints, seeds, cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C187 ACCEPTED PASS. No active experiment at this acceptance commit. C188 NOT REGISTERED.**
C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS;
C170-C173 PASS; C160/C168/C169 VALID NEGATIVE.
All previous judgments and checkpoints remain unchanged.

C187 successful execution HEAD:
`bbb79df40f3428f358bec7381cd872efa7845e63`.

## Latest accepted C187

Experiment:
`C187-v5e-restricted-acquisition-necessity` /
`V5-E-RESTRICTED-ACQUISITION-NECESSITY`.

Execution:
- focused regression **1377/1377**, 49.777s
- source/artifact precheck PASS
- 80/80 blocks, 296960 episodes
- six frozen C181 checkpoints, source seeds181001/181002/181003
- no training/fresh seed/teacher/auxiliary head/threshold repair
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False
- run execution valid True

Candidate result:
each of the three INTERNAL_SEMANTICS models ran 37120 episodes with **zero failures**.
Per candidate: 7680 proposals, 4608 denied proposals, 3072 allowed reads/publications,
zero initial/missed/unnecessary/post/false-sufficient/contract errors, and zero initial
decision flips from unrestricted C185.

All candidates:
- episodes111360
- proposals23040
- denied13824
- reads/admissions9216
- skips88320
- failures0
- restricted provider calls0

The restriction arms change one initial execution coordinate only:
RETRIEVE permission, RETRIEVE availability, or acquisition budget.
Semantic NEEDS remains correct while C172/C173 independently blocks IO.
Allowed controls still read/admit exactly once.

All-policy totals include deliberately weak controls and MUST NOT be read as candidate
errors: failed65052, false-sufficient-after-denial72, provider calls31744,
publications31744, contract errors0.

56376 static original predictions replay exactly with max logit delta0.
Total neural rows320708 / 360 batches / 2520 shared-cell calls.
Actual file reads31744, bytes6983680. No answer/proof/network/core EvidenceState writes.

Scope boundary:
```text
frozen learned necessity
-> handwritten sole-unknown target / fixed RETRIEVE
-> C172/C173 authority
-> allowed read/admission OR denied zero-IO
-> actual current state
-> frozen reclassification
```

This is evidence for semantic-necessity / execution-authority separation only in the
bounded one-missing development family. It is NOT learned multi-target selection, learned
tool choice, retry/alternative policy, answer/proof generation, language generalization,
independent final confirmation, production adoption or Gate E completion.

## Evidence / reviewer scope

C187:
`runs/c187-v5e-restricted-acquisition-cc3717a5a9994142a9147953dce83573/summary.json`
SHA256:
`910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`.

The uploaded RESULT summary was reconstructed exactly and the 80 records, candidate
per-seed totals, all-policy totals, provider/publication arithmetic and fixed gate were
independently reaggregated. Separate artifacts/full NPZ/traces/checkpoints/data and the
user's 1377 tests were not independently rerun by the reviewer.

C186:
`runs/c186-v5e-nonadmission-0d274f54409144cf83899758d020e82b/summary.json`
SHA256 `e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82`.

C185:
`runs/c185-v5e-single-missing-acquisition-72d30a1a4e114de5b981352de26055e6/summary.json`
SHA256 `843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949`.

C184:
`runs/c184-v5e-canonical-indices-5e2a159b64164b3a919762ebdbdc4f90/summary.json`
SHA256 `7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04`.

C183 SHA `ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24`.
C182 SHA `06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73`.
C181 SHA `bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`.
Dataset SHA256 `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.

Historical C186 invalid 32MiB-loader attempt remains INVALID EXECUTION, not a second
scientific result. The accepted C185-specific NPZ recovery loader is not a generic
unbounded loader.

## Accepted chain / limits

C181 proper-node TRAIN supervision produced zero errors on 9396 PILOT and 42444 TRAIN
per candidate, but uses additional programmed TRAIN supervision and the four PILOT groups
are repeatedly inspected development groups.
C182 found one renaming error / 648324 candidate predictions.
C183 localized that counterexample to tree-side representation sensitivity.
C184 established reversible LOCAL fact-index normalization as an engineering contract,
not learned naming invariance.
C185 connected frozen necessity to real bounded successful acquisition.
C186 established correct reclassification after non-admission following a read attempt.
C187 established correct necessity under initial permission/availability/budget restriction
while authority independently prevents IO.

No natural-language, larger/repeated-variable, multi-target, learned-tool, answer/proof,
or final Gate E claim follows from this chain.

## Next design / separate tracks

Next proposed one-question experiment:
**learned selection of WHICH missing fact is influential when more than one fact is
unobserved**, with the accepted C181 base frozen.

Keep it offline first. Do not combine first learned target selection with live C172/C173
execution in the same C number. Use TRAIN-only target teachers/reference statistics and
the same held-out development split; explicitly report that it is not independent final
confirmation.

C188 must be separately preregistered after this acceptance commit. No C188 execution
before that registration. C189 remains unregistered.

Gate E full candidate/baselines/splits/numerical contract still required.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate research tracks.
No reset/rebase/history rewrite/historical artifact commit_sha edit.
