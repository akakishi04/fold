# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Read `AGENTS.md`, `docs/experiment-conversation-handoff-protocol.md`, this file,
`docs/experiment-ledger-addendum-c189-c190.md`, and
`docs/experiment-ledger-addendum-c190-preregistration.md`.

Execution logs publish to `docs/experiment-run-logs/c###/latest.log` + `latest.json`.
After completion the user may say 「終わった」; fetch remote log/metadata directly.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C189 ACCEPTED PASS. C190 ACTIVE / NOT YET JUDGED. C191 NOT REGISTERED.**
C188/C187/C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS.
Earlier judgments/checkpoints remain unchanged.

C189 successful execution HEAD:
`051165ac5b14600d36f38064e36785d767de934d`.

C189 acceptance commit:
`9bd1ccc7d176a8134466eb22a3546861f1ba9a7d`.

## Accepted C189

C189 summary:
`runs/c189-v5e-live-multimissing-target-19ae6f0a2dd8402492df6beab82dc3a3/summary.json`
SHA256 `a9388db7e28e25cf1b12e7f78e3068228ee5b5562da12a3a626fe054fead4b7a`.

1449/1449 tests in47.334s; source/artifact precheck PASS; protected inputs preserved;
tracked tree clean; execution HEAD preserved; run validTrue.
Production runtime modifiedFalse; Gate E candidateFalse.

18 blocks /31824 live episodes:
failed0; initial_error0; target_error0; target_replay_error0; selected_observed0;
missed_acquisition0; post_error0; contract_error0.
Reservations/provider calls/publications31824 each; actual file reads31824.
All nine C188 target predictions replay exactly with max logit delta0.

After one actual acquisition:
- post SUFFICIENT19595
- post NEEDS12229

Thus C189 establishes bounded one-step learned target -> real C172/C173 acquisition ->
actual-state reclassification. It deliberately stops on the 12229 remaining NEEDS cases.

The three earlier C189 attempts remain execution-invalid history only:
malformed source bytes; manifest-hash transcription; synthetic test epoch mismatch.

## Active C190 — iterative learned multi-missing acquisition

Experiment:
`C190-v5e-iterative-multimissing-acquisition` /
`V5-E-ITERATIVE-MULTIMISSING-ACQUISITION`.

One question:
when the actual state remains NEEDS after the first learned acquisition, can the same
frozen C181+C188 components select a second new influential target, acquire it once through
unchanged C172/C173, and correctly classify the second actual state?

### Frozen

C181 base seeds181001/2/3; C188 head seeds188001/2/3; all9 combinations.
No training/fresh seed. Original C174 local layout. Fixed RETRIEVE/provider.

### Coherent world cohort

All1768 PILOT NEEDS rows:
- missing2=1152 ->4 consistent full worlds each =4608
- missing3=616 ->8 worlds each =4928
- total9536 episodes/selector
- 9 selectors -> **85824 episodes /9 blocks**

Each episode binds one of16 complete four-fact C173 source snapshots. Both possible
acquisitions read from the SAME snapshot. World values never enter neural input.

### Iterative path

```text
initial TaskView
-> frozen C181 necessity + frozen C188 target0
-> C172/C173 acquire target0
-> actual state1
-> frozen C181 necessity1 + frozen C188 target1
   -> if SUFFICIENT: stop
   -> if NEEDS: C172/C173 acquire new target1
-> actual state2
-> frozen C181 necessity2
-> stop even if NEEDS
```

No third acquisition.

Resources:
start12/4/step7;
first decision input11/4/8;
second decision after first acquisition7/3/12;
final decision after second acquisition3/2/16.

### Parent replay

Initial C190 outputs must exactly replay accepted C189 initial necessity/target decisions
over every duplicated world copy; necessity and finite unknown-target logits <=1e-6.

### Fixed gate

Each of9 blocks must have:
episodes9536; m2worlds4608; m3worlds4928;
zero initial/replay/target0/selected-observed/first-acquisition/post1/target1/repeat/
second-acquisition/post2/contract errors;
first reads9536;
second reads exactly equal measured logical post1 NEEDS count;
decision charges `2*9536+second`;
internal charged `5*9536+4*second`;
final sufficient+needs9536;
initial replay deltas<=1e-6.

Finite completed miss => ACCEPTED VALID NEGATIVE.
Source/hash/replay/nonfinite/incomplete/protection issue => INVALID / retry SAME C190.

### Workload / protection

Expected regression **1485 =1449+36;75 modules**.
Historical source pins111; protected paths277.
Artifacts21 excluding summary.
Manifest SHA
`3feec9c60f007ee67cecd328614dca051777d485a37d482438275e1a8c31deea`.

New files:
- `fold_lm/v05_benchmarks/gate_e_c190_iterative_multimissing_acquisition.py`
- `tests_lm/test_v05_c190_iterative_multimissing_acquisition.py`
- `tools/run_c190.ps1`
- `tools/invoke_c190.ps1`
- `docs/experiment-ledger-addendum-c190-preregistration.md`

No C191 registration before C190 judgment.

## Persistent limits

Same repeatedly inspected four development groups; no independent final confirmation.
Max2 acquisitions only; no learned tool/provider choice; no language/larger/repeated-variable,
answer/proof, production adoption or Gate E completion.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate research tracks.
No history rewrite.
