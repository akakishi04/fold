# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Read `AGENTS.md`, `docs/experiment-conversation-handoff-protocol.md`, this file, and latest addenda.
Formal work order: verdict -> validity -> metrics -> interpretation -> confounds -> ledger ->
next one-question design -> implementation/preregistration -> command -> stop.

Execution logs are published to `docs/experiment-run-logs/c###/latest.log` + `latest.json`.
After a run the user may simply say 「終わった」; fetch the remote log/metadata directly.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C189 ACCEPTED PASS. C190 NOT REGISTERED at this acceptance commit.**
C188/C187/C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS.
All earlier judgments/checkpoints remain unchanged.

C189 successful scientific execution HEAD:
`051165ac5b14600d36f38064e36785d767de934d`.

C189 published log commit:
`54f284f9242ff6a7f797a89cedf35c2c22e76164`.

## Latest accepted C189

Experiment:
`C189-v5e-live-multimissing-target-acquisition` /
`V5-E-LIVE-MULTIMISSING-TARGET-ACQUISITION`.

1449/1449 regression in 47.334s; precheck PASS; protected inputs preserved;
tracked tree clean; scientific execution HEAD preserved; valid True.
Production runtime modified False; Gate E candidate False.

Summary:
`runs/c189-v5e-live-multimissing-target-19ae6f0a2dd8402492df6beab82dc3a3/summary.json`
SHA256 `a9388db7e28e25cf1b12e7f78e3068228ee5b5562da12a3a626fe054fead4b7a`.

Published log metadata:
SHA256 `ff92437802e69a0c93d2572b46291112ea916285f240c139fd352bb3e851141d`,
bytes342650.

Deciding totals over 18 blocks / 31824 live episodes:
- failed0
- initial_error0
- target_error0
- target_replay_error0
- selected_observed0
- missed_acquisition0
- post_error0
- contract_error0
- reservations/provider_calls/publications31824 each
- actual_file_reads31824
- decision_charges63648
- internal_charged159120

All nine accepted C188 target predictions replay exactly, max logit difference0.
After one actual acquisition:
- post SUFFICIENT19595
- post NEEDS12229
with zero logical-label error.

C189 supports only bounded live one-step integration:
frozen C181 learned necessity + frozen C188 learned target -> exact selected external fact ->
C172/C173 real read/admission -> actual updated state -> correct frozen necessity reclassification.

It does NOT establish second target selection/acquisition, learned tool/provider choice,
retry/stopping, optimal information gain, language/larger/repeated-variable generalization,
independent final holdout, answer/proof generation or Gate E completion.

The three earlier C189 attempts are execution-invalid history only:
source-byte corruption; manifest-hash transcription; synthetic test epoch mismatch.

## Next design

C190 one question:
If the actual post-first-acquisition state remains NEEDS, can the same frozen C181+C188
components choose a new valid missing target, execute one second real C172/C173 RETRIEVE
without repeating the first fact, and correctly reclassify the second actual state?

Use complete 4-bit source worlds consistent with each initial visible row so all acquisitions
within an episode share one coherent snapshot. No new training. No third acquisition.
No learned tool/provider choice. No answer/proof.

C190 must be separately preregistered. C191 remains unregistered.

## Persistent limits

Same four repeatedly inspected development semantic groups; no independent final confirmation.
C184 canonical local-index adapter is engineering evidence, not learned naming invariance.
C181 intermediate supervision is programmed TRAIN information.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate research tracks.
No history rewrite.
