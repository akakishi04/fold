# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C197 ACCEPTED PASS. C198 NOT REGISTERED.**

C197 scientific execution HEAD:
`7d9a09bba9ac2286806f40bc20c6ce45a21cb279`

C197 published log commit:
`b6f2cb6334c22f435320e0f2204b894152bd4797`

C197 log SHA256:
`2053ea31d161e732fb496ea1213612bafc4869df75aef3bdaa3ecbcd460581c6`

C197 summary SHA256:
`632e8af4a215d12adc83aa015da855c63605205c87832aa6a511dabfc4fd1ca5`

C197 deciding result:
- focused regression **1653/1653**
- ALLOWED: 9/9 blocks, accepted C196/C194 behavior preserved
- PROVIDER_FAILURE_AFTER_RESERVATION: 85824/85824 failure attempts
- provider calls 85824
- publications 0
- receipts 0
- retries 0
- fact mutation 0
- fake SUFFICIENT 0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

The earlier C197 execution at
`675af144558c9528a8cde9e79d20a0c447736b72`
remains **INVALID EXECUTION** only. It stopped during source/import precheck because of malformed
literal backslash-n text and contributes no scientific evidence.

## Accepted C197 claim boundary

The bounded generic result-aware loop preserves a post-reservation provider failure as
`UNRESOLVED_ACQUISITION_PROVIDER_FAILURE`, rather than collapsing it to the action-level
reservation reason. The provider is called once, but no observation is published and the loop
does not retry or fabricate completion.

This does not establish retry policy, stale-reservation handling, attempt-limit handling,
learned provider/tool/resource policy, independent final holdout, language/answer/proof, or
full Gate E completion.

## Next boundary

C198 is not yet registered at this handoff boundary.

Next one-question intervention:
after the learned decision and successful RETRIEVE reservation, change only the trusted
TaskView evidence identity before dispatch. The dispatch should reject the old reservation as
`STALE_RESERVATION`; the generic loop must preserve that reason, perform zero provider calls,
zero publication/receipt/retry and no fake SUFFICIENT.

C198 must be authored and pass the experiment authoring quality gate before it is described as
executable.
