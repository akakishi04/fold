# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C197 ACCEPTED PASS. C198 ACTIVE / NOT YET JUDGED. C199 NOT REGISTERED.**

## Accepted C197

Scientific execution HEAD:
`7d9a09bba9ac2286806f40bc20c6ce45a21cb279`

Published log commit:
`b6f2cb6334c22f435320e0f2204b894152bd4797`

Log SHA256:
`2053ea31d161e732fb496ea1213612bafc4869df75aef3bdaa3ecbcd460581c6`

Summary SHA256:
`632e8af4a215d12adc83aa015da855c63605205c87832aa6a511dabfc4fd1ca5`

C197 deciding result:
- focused regression **1653/1653**
- ALLOWED 9/9 accepted C196/C194 replay
- PROVIDER_FAILURE_AFTER_RESERVATION 85824/85824
- provider calls 85824
- publications 0
- receipts 0
- retries 0
- fact mutation 0
- fake SUFFICIENT 0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

The earlier execution at
`675af144558c9528a8cde9e79d20a0c447736b72`
is retained as **INVALID EXECUTION** only and contributes no scientific evidence.

Accepted claim: the bounded result-aware generic loop preserves a post-reservation provider
failure as `UNRESOLVED_ACQUISITION_PROVIDER_FAILURE` without retry or fabricated evidence.

## Active C198

Experiment:
`C198-v5e-stale-reservation-generic-loop`

Stage:
`V5-E-STALE-RESERVATION-GENERIC-LOOP`

One changed condition:
after the first successful RETRIEVE reservation, the trusted scheduler advances
`evidence_time` and `revision` exactly +1 before dispatch. Facts/resources/authority and
source binding remain otherwise fixed.

Arms:
1. **ALLOWED** — exact accepted C197 allowed replay.
2. **STALE_RESERVATION_AFTER_RESERVATION** — reservation succeeds, trusted refresh invalidates
   the reservation, dispatch must return `REJECTED / STALE_RESERVATION`.

Required stale-arm terminal behavior:
- generic-loop status `UNRESOLVED_ACQUISITION_STALE_RESERVATION`;
- provider calls 0;
- actual provider reads 0;
- publications 0;
- receipts 0;
- retries 0;
- fact mutation 0;
- fake SUFFICIENT 0;
- final resources internal10 / acquisitions3 / available1 / permitted1 / outcomeNONE / step10;
- final evidence_time and revision exactly initial+1;
- pending none.

Workload:
- 2 x85824 episodes;
- 9 selector blocks / arm;
- expected regression **1677 =1653+24**;
- expected modules **83**;
- source pins151;
- protected paths401;
- artifacts5;
- no new training/fresh seeds/network/proof checking/answer generation;
- production runtime modified False;
- Gate E candidate False.

Manifest:
`e108bcaefdb882f05420c078a4866272afe375d48e62e50ac726241fed2a44e9`

C198 uses an explicit loader for the accepted C197 prediction artifact and verifies the
2x9x9536 parent schema before execution. The one-row integration coverage fixes call ordering:
reservation -> trusted refresh -> stale dispatch, with a provider sentinel that fails if called.

## Stop condition

Judge C198 before any C199 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/nonfinite/regression/incomplete/protection failure -> INVALID / RETRY SAME C198.

**Gate E remains NOT PASSED regardless of C198 until a later explicitly registered Gate E
completion experiment satisfies its own contract.**
