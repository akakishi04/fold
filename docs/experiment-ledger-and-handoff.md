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

## C190 invalid-attempt recovery

First C190 attempt at execution HEAD `e0e47b44dbda4a5a4ad470f42911d4ce2687e587`
is **INVALID EXECUTION**. Precheck and all 1485 focused tests passed, then the benchmark
stopped before model work because the C190 guard misread C188's discriminating
`profile["eval_m2"/"eval_m3"] = 376/152` as full-cohort counts 1152/616.

The full `evfull` mask itself is correct. Recovery checks full counts directly from
`miss[evfull]` (1152/616) and separately checks discriminating counts (376/152; total528).
No scientific condition changes. Published invalid log commit:
`8ec5932922231f0f88478bd12c5d3de89f104df7`,
log SHA256 `c875c9fab740753903636a6d9557c621ba85c8655fdd71deb47efb102e2943d6`.

Retry SAME C190; C191 remains unregistered.

## C190 completed invalid run / replay recovery

Completed C190 at execution HEAD `b934eff1e06c5ce0b75e08870dfd9a6753768b21`
ran 1485/1485 tests and all 85824 episodes. All scientific target/action/post-state/
contract counters were zero; first reads85824, second reads34948, post2 NEEDS8352.

It is nevertheless **INVALID EXECUTION / RETRY SAME C190** because the fixed parent-logit
replay <=1e-6 was exceeded under the expanded hidden-world batch layout
(max necessity5.245208740234375e-06; target5.7220458984375e-06), while all parent argmax
decisions remained exact.

Recovery memoizes one recomputed frozen initial policy output per unique observable TaskView
(1768 x9 =15912 actual initial policy rows) across its 4/8 hidden-world copies. Hidden world
is not a policy/cache key. C189 saved outputs remain validation-only. Replay tolerance stays
<=1e-6; all scientific conditions remain fixed.

Published invalid log commit `da06a4544093930bc5392e05f42ffc2a3f0ac262`.
Retry SAME C190; C191 remains unregistered.

## C190 memoization-test recovery

Retry at execution HEAD `40d53444067831d6ec3b1419142fdab36dd5be84` stopped in focused
regression: 1485 tests ran, with exactly two C190 test errors and no benchmark execution.
After initial-policy memoization, those tests still treated the first in-block
`combined_predict` call as phase0; it is now phase1, causing a synthetic attempt to
reacquire the already observed target. Only the two mocks are corrected.

Published log commit `cc08b5c6c1075ae0598a7c5dca7843a854a67a60`;
log SHA256 `3acc82e2e0788fdd8796cb6f29699f97e1de4b61050802e9e7ab21d828f07fb6`.

No scientific condition changes. Retry SAME C190; C191 remains unregistered.

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
`ddca97a8c8de1687929b95e69f33c3073647017c3514871ae3db81d22605ef6d`.

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
