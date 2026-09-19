# FOLD Experiment Ledger and Handoff

> Authoritative current state. Read AGENTS.md and docs/experiment-conversation-handoff-protocol.md.
> Current response format (v2) is authoritative.

## Environment

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; authoritative Python
`.venv-py31315\Scripts\python.exe`.

Remote logs: `docs/experiment-run-logs/c###/latest.log` + `latest.json`.
Scientific execution HEAD and published log commit are distinct identities.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.

**C190 ACCEPTED PASS. C191 NOT REGISTERED at this acceptance commit.**
C189/C188/C187/C186/C185/C184/C183/C181 PASS; C182 VALID NEGATIVE.
C180/C179/C178/C176 VALID NEGATIVE; C174/C175/C177 scoped PASS.

C190 successful scientific execution HEAD:
`b3d04dae6ed621deba987162b3d63c8f815bbe72`.

C190 published log commit:
`e47a6692ab7286f9f5ceecd4d987ad08a85ae25b`.

C190 summary:
`runs/c190-v5e-iterative-multimissing-fce03e62811c4166a11280c32ecfc534/summary.json`
SHA256 `6902f97fd1fbcb1eb878884594a333ae41a0d35c83b872d287439386f7fabd59`.

## Accepted C190

1485/1485 tests; precheck PASS; run valid True; protected/tree/HEAD preserved.
9 blocks /85824 coherent-world episodes.

All scientific errors zero.
First reads85824.
Post1 NEEDS / second reads34948.
Post2 NEEDS8352 =928 per selector.
Total reads120772.
Initial C189 replay exact: argmax errors0; logit deltas0.0.

Claim: same frozen C181+C188 path supports two sequential learned targets and two real
C172/C173 acquisitions with correct post-state necessity in this bounded dev family.

Non-claim: third acquisition, arbitrary loop, learned tool/provider, independent final holdout,
language/larger expressions, answer/proof, Gate E.

## Next design

C191 one question:
with original internal budget12 unchanged, can post2 NEEDS episodes perform exactly one third
learned target/acquisition from the same coherent world, publish the last missing fact,
consume the remaining3 internal units exactly, and stop with internal_remaining0 without a
fourth learned decision?

No resource increase. No new training. No new seed. No third-post learned sufficiency decision.
C192 remains unregistered until C191 judgment.
