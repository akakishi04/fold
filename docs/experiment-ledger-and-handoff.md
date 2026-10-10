# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C317 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C318 NOT REGISTERED.**
No ACTIVE experiment until separate committed-byte review and activation.
C316/C315 negatives,C314 diagnostic PASS,C313/C312 negatives,C308 bounded PASS unchanged.
Latest accepted execution:3ecd3a638726f86b294f0fe94d53a2fc5d082e01.
Latest publication:a948757c3f2a0e524bdef50521cf4034b900fc2a. Do not rerun C317.

## Latest accepted evidence — C317

Acceptance:docs/experiment-ledger-addendum-c317-c318.md.
Summary:runs/c317-v5b-query-endpoint-88ae97edc7d44cd3bcd9732e66c8b14e/summary.json.
SHA256:09632cda7689c9b23229ec993d19c108ac23a7bb142285cd58b11bcc713d8cb5.
Own32/focused5149 PASS;sources748/inputs1407;run_execution_valid=True.
Both replay errors0.0 at all10 states;one-byte controls and weights/hooks preserved.
Original both arms5/5 at2..5,4/5 at6. first_byte both arms0/5 at every scored2..6.
This is diagnostic PASS,not capability PASS. Original C316 negatives remain accepted.
Example only:one_to_four316005 six HOLDOUT shared_prefix English48->24/48,Japanese48->23/48;
shared_suffix English48->48/48,Japanese48->43/48. Do not call0/5 zero answer accuracy.

## Next registration boundary

Proposed C318:compare frozen original mean-plus-last to mean-only and last-only,retaining
all10 states and all1..6 inputs. Duplicate one native query branch in the two projection
calls to preserve memory scale. Original before/after and one-byte controls required.
No training,checkpoint selection,parent mutation,Gate F promotion or unreviewed command.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical tests.

## Historical state

Pre-acceptance:docs/handoff-history/c317-pre-acceptance.md.
Git blob:40175d12ac9fce1f9922cdc8b3c717e1e023e740.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
