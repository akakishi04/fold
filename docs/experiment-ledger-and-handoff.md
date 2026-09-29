# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through explicit PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C285 ACCEPTED PASS (diagnostic integrity only). C286 NOT REGISTERED.**
C285 scientific execution HEAD:f2bd32785895c30defa16be7d1eca6279ba4ed23.
C285 published log commit:d8a24df7b94a1b8c3d339b868c6db4fc2ed7e3b6.
C284 remains ACCEPTED VALID NEGATIVE. No C285 rerun,seed exclusions or Gate F promotion.
No ACTIVE experiment in this acceptance commit. C286 requires separate authoring/review/activation.

## Latest accepted science — C285

Acceptance:docs/experiment-ledger-addendum-c285-c286.md.
Summary:runs/c285-v5b-saved-length-audit-94786461780e4110a04f18ca3c92c427/summary.json.
Summary SHA256:702092926265bb893babce1e5b93dd234791527344193ea876d33210e8bfdba1.
Manifest SHA256:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;capability_gate_applicable=False.
Own32/focused4045 PASS;source556/protected991;zero scientific neural calls,training,state loads,writes.
Quad control/candidate failures:accuracy50/43;query_pair48/43;evidence_drop27/27;query_drop30/38;two_order21/20.
Mixed triple-to-quad accuracy:37 persistent matched-cell failures+6 new=43;no rescues.
Seed284002 accounts for42 mixed quad accuracy failures;284001 accounts for the remaining1 (863/864).
Mixed quad mask-only failing answer cells0. Cell co-failure does not prove identical-row errors,
training-set underfit or an optimizer cause. All prior capability verdicts remain unchanged.

## Next question under consideration

Fixed-budget late learning-rate decay versus constant LR with identical mixed2/3 training.
This is not registered or executable in this acceptance commit. Do not start new science.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Prior full handoffs are preserved under docs/handoff-history/c280-pre-acceptance.md through
c285-pre-acceptance.md. The newest preserves Git blob1f9a2cc8ccb9357141b424435e6700723f385b96.
Their ACTIVE instructions are historical;only this file's Formal state is authoritative.
Accepted source/tests,preregistrations,logs and protected dispatchers are unchanged.
