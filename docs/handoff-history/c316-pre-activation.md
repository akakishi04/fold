# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C315 ACCEPTED VALID NEGATIVE. C316 NOT REGISTERED.**
No ACTIVE experiment pending next committed-byte review and activation.
C314 diagnostic PASS;C313/C312 negatives;C308 bounded PASS/C309 negative remain unchanged.
Latest accepted scientific execution:5708562420e530749a8f63b1f4baf3c7e0f28029.
Latest accepted publication:0b4ce1c953d2ccf0eea04747b1194c6dd70729ee. Do not rerun C315.

## Latest accepted evidence — C315

Acceptance:docs/experiment-ledger-addendum-c315-c316.md.
Summary:runs/c315-v5b-single-mix-dbdffe0b88094f729d1dbfbcdba520f0/summary.json.
SHA256:aceda00cebf61b49e5f923bf7c426e2f4522dcac68444fc2e07b27a17b63dd66.
Own32/focused5085 PASS;736sources/1379inputs;run_execution_valid=True;all_pairs_matched=True.
Both arms5/5 at2..5;unseen6 control3/5,candidate4/5. Paired3both,1candidate_only,0control_only,1both_fail.
Candidate rescues315004 (six573/576,284/288 ->576/576,288/288).
315002 remains negative (566/576,283/288 ->574/576,286/288).
Total six normal errors22->4. Single-character candidate diagnostics all perfect;control two errors.
Fixed1200update allocation differs:control2/3/4x100,candidate1/2/3/4x75. Not isolated breadth or cause.

## Next registration boundary

Proposed C316:fresh paired initial/order seeds with identical C315 policies and budgets.
Do not change mixture,coreLR,frame,task,gates or choose successful old states. C315 verdict stays.
No command until all next files are committed,refetched,reviewed and activated.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-acceptance handoff:docs/handoff-history/c315-pre-acceptance.md.
Git blob:c5c146cad014d825bc0f2fb5320afd95ae87cce7.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
