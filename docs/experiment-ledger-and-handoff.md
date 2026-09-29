# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C280 ACCEPTED VALID NEGATIVE. C281 NOT REGISTERED. C282 NOT REGISTERED.**
Scientific execution HEAD:2c2eb8a86a03910ba9c63ff277c137d1e842a32f.
Published log commit:ae0a53cd8e0beb65ac4e1909edadecd51d833fdf.
Both arms:two-char4/5,triple0/5,whole0/5. Seed280004 fails two-char in both arms.
Do not rerun C280,select seeds,retune the support boundary,or promote Gate F.

## Latest accepted science — C280

Acceptance:docs/experiment-ledger-addendum-c280-c281.md.
Summary:runs/c280-v5b-evidence-only-dual-bb662d609be24ad9a1fd20d4aef54174/summary.json.
Summary SHA256:00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db.
Manifest SHA256:c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Published own24/focused3885 and persisted reconstruction PASS. Gate F NOT PASSED.
The initial manifest guard failure was operational preflight only,not scientific evidence.

## Next question — not yet activated

C281 should use saved C280 outputs only to identify which fixed-criterion failures evidence-only
support rescues or introduces,especially shared_suffix2,and distinguish shared seed280004 failure
from candidate-specific regression. Keep all seeds in the primary result. Zero training/forwards.
No execution command until committed-byte authoring review;C282 remains unregistered.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Historical state and recovery

The complete pre-acceptance handoff is preserved byte-for-byte at
`docs/handoff-history/c280-pre-acceptance.md` (Git blob af114ae862372baa3d49106776b078b127f8f050).
Its ACTIVE and execution instructions are historical;only this file's Formal state is current.
C279 remains ACCEPTED PASS (diagnostic integrity only);C278 remains ACCEPTED VALID NEGATIVE.
Earlier acceptances/preregistrations,accepted source/tests,logs and protected dispatchers are unchanged.
