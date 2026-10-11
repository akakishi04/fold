# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C319 ACCEPTED VALID NEGATIVE. C320 NOT REGISTERED.**
No ACTIVE experiment until separate committed-byte review and activation.
C318/C317 diagnostic PASS,C316/C315 negatives,C308 bounded PASS and old verdicts unchanged.
Latest accepted execution:529c54ef63b1015b25632b8123a9a552eebcd263.
Latest accepted publication:3abe218dc9191d26963e5b5022d4d1983300084d. Do not rerun C319.

## Latest accepted evidence — C319

Acceptance:docs/experiment-ledger-addendum-c319-c320.md.
Summary:runs/c319-v5b-trained-last-0f94e96bbbba43b395fcf8eab1e38246/summary.json.
SHA256:48815ca382d0da078da12ec2d54f2c42261e94498b682f679d8f46d746ec0580.
Own24/focused5197 PASS;760sources/1429inputs;run_execution_valid=True.
Both arms5/5 at2..5;six mean_last5/5,last_only4/5.
Paired six4both,1control_only,0candidate_only,0both_fail.
last_only319005 six TRAIN567/576,HOLDOUT283/288;paired mean_last575/576,288/288.
The latter passes full gates despite one normal error;do not substitute pooled perfection.
No support for adopting trained last-only as a reliability improvement in this cohort.

## Next registration boundary

Proposed C320:frozen unequal name lengths2+4/4+2 within the same question,all10 C319 models,
respective trained readout policies intact. Original1..6 before/after reproduce. No retraining.
Prospective primary all5 retained mean_last models pass both new layouts;last_only comparison
retained. This addresses equal-length-name restriction,not six failure repair or fresh-seed proof.
No command until next OWN files committed,refetched,reviewed and activated.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-acceptance:docs/handoff-history/c319-pre-acceptance.md.
Git blob:8f9b42fffeb109f5ce31ff4bae80468cce6da386.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
