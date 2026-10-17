# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format (v2) in
`docs/experiment-conversation-handoff-protocol.md`.
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.
Entry: explicit PowerShell7, dispatcher ParseFile, tools/invoke_active_v2.ps1.
Accepted sources/tests/contracts/logs/protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C328 ACCEPTED VALID NEGATIVE. C329 NOT REGISTERED.**
C327 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C326 remains VALID NEGATIVE.
No ACTIVE scientific execution is authorized by this acceptance-only handoff.
Do not rerun C328 or earlier accepted experiments. No production adoption.

## Latest accepted evidence -- C328

Report: docs/experiment-ledger-addendum-c328-c329.md.
Scientific execution HEAD:3507021e46d47f6543316d46dc4481d3ead04855.
Publication commit:edf05c01e7fcd91b95c425fca5e7c416150689aa; its parent equals execution.
Published metadata/log:docs/experiment-run-logs/c328/latest.json and latest.log.
Full5722 tests/217 modules PASS, zero failures/errors/skips,961.811s.
All10 fits,5 identical800-update boundaries,10 checkpoint replays,1561 final rereads
and fresh826-source/1561-input envelope verification passed. All exits zero;
run_execution_valid=true; scientific_status=FAIL; paired success0/5.
Interior complete gate0/5 in both arms; original2..6 retention0/5 in both arms.
Interior HOLDOUT normal answers1350->1261/1440 and both-query pairs639->576/720;
late_tenth worsened both counts in every seed. Original pooled gains-53 answers/-49
pairs across all five seeds. No pooled result overrides any local gate.
The registered late learning-rate reduction is not adopted. This says nothing about
all other rate schedules, longer training, capacity limits or general LLM capability.
Review used published execution records and complete paired counts, not independent
whole-log rehash, local logit recomputation or a checkpoint rerun. Old C323/C324
attachments are not current evidence.

## Accepted parent files for the next experiment

Folder:runs/c328-late-rate-206451e9574c4b578b5cff4201af284b/.
Primary science/summary.json SHA256:
10bf430e74311a883cbcc7a7b70b589490a98d0f6db4458bcfe8be748fbccb53.
Companion execution-envelope.json SHA256:
d675bf546fb9d46eecf86b9a53847c5c054f4de618f311e0426a195c49f7cc32.
Parent schema:fold-c328-science-v1, statusFAIL, diagnostic_execution_valid=true.
Parent envelope:fold-c328-execution-envelope-v1, scientific_statusFAIL.
Validate the negative parent as valid evidence, not as capability PASS.
Its8 outputs plus summary/envelope are10 immediate-parent files; inherit the complete
826-source/1561-input unions. Keep native leases and final uncached rereads.

## Next-step boundary

Prepare one fixed-budget comparison of fresh constant-rate trajectories at1200 versus
2400 updates; retain the same schedule, templates, optimizer and original/interior
gates. This is only a next-question note, NOT preregistration or execution approval.
Complete implementation, own tests, separate committed-byte review and activation
before delivering a command. No rate/seed/threshold search, old-result edits, CI,
paid services, package reinstall or artifact deletion.

## History and inherited compatibility seal

Pre-acceptance handoff:docs/handoff-history/c328-pre-acceptance.md.
All earlier accepted/invalid records remain in their existing documents/commits.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
