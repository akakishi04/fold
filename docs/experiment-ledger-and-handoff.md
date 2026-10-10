# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C318 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C319 NOT REGISTERED.**
No ACTIVE experiment until next committed-byte review and separate activation.
C317 diagnostic PASS,C316/C315 negatives,C308 bounded PASS and other old verdicts unchanged.
Latest accepted execution:f4624509c4311b3e7b04b3d861cfcb3e9d58bfd0.
Latest accepted publication:3444c11cb68c85e35202f65f26ba258aaadc2c1a. Do not rerun C318.

## Latest accepted evidence — C318

Acceptance:docs/experiment-ledger-addendum-c318-c319.md.
Summary:runs/c318-v5b-readout-branches-bb278106ee824f26996434d7d895726a/summary.json.
SHA256:5b838ca1420dc36b146ba4afa548d889f16172bd1d1705e4f5df97a5664c5203.
Own24/focused5173 PASS;754sources/1418inputs;run_execution_valid=True.
All10 states restored original outputs with0.0 drift;single-byte controls held.
Pass counts by2/3/4/5/6:
Original,both cohorts:[5,5,5,5,4].
Mean-only,two_to_four:[4,0,0,0,0];one_to_four:[2,0,0,0,0].
Last-only,two_to_four:[5,5,5,3,2];one_to_four:[5,4,5,4,0].
Neither frozen isolation improves six reliability. Diagnostic PASS is not capability PASS.

## Next registration boundary

Proposed C319:from-scratch mean-plus-last versus last-only,with matched fresh initializations
and the existing two_to_four training allocation in both arms. Keep gradients through the
selected last-byte branch;use the same branch policy in training/evaluation/replay. No old
checkpoint reuse,seed search,outcome-dependent selection or Gate F promotion. Review first.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-acceptance:docs/handoff-history/c318-pre-acceptance.md.
Git blob:fe5fd87ac49999cc298e666d9dd887acfe7666fd.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
