# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C314 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C315 NOT REGISTERED.**
No ACTIVE experiment pending separate authoring/review/activation.
C313/C312 remain valid negatives;C308 bounded PASS and C309 negative remain unchanged.
Latest accepted scientific execution:41d132a50b246de5357a3878606a1ac7776c830d.
Latest accepted publication:ec39b319d333527d4786ac6299ded6faa6a1601b. Do not rerun C314.

## Latest accepted evidence — C314

Acceptance:docs/experiment-ledger-addendum-c314-c315.md.
Summary:runs/c314-v5b-six-boundary-31c4ca923fa8459cbe9afde6fade9c83/summary.json.
SHA256:daa6403d0eb00399cecb73e83693db41dbbb42151b979080d904428da5484e51.
Own24/focused5053 PASS;730sources/1369inputs;run_execution_valid=True.
8640 paired rows/17280 answers;five correct8637,six correct8548.
Both correct8548,new errors89,both wrong3,same wrong3,recovered0.
120 local totals and20 transition totals match;zero neural work.
Representative random312001 shared-suffix errors:English6/144,Japanese19/144;
random312002 shared-prefix errors:English5/144,Japanese0/144.
Errors at27-token English inputs rule out a Japanese-near64 explanation for every error,
but this is not causal separation of language,position or representation mechanisms.
Diagnostic PASS does not alter C313 six capability negative or Gate F.

## Next registration boundary

User-proposed single-character training:compare2/3/4 versus1/2/3/4 at equal total updates,
unchanged core_slow and trained maximum4;evaluate held-out5/6 and retain seen-length scores.
Use fresh paired seeds,canonical single-character profile and no HOLDOUT training.
Per-length exposure dilution must be reported. No C315 command until committed-byte review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical lifecycle tests.

## Historical state

Pre-acceptance handoff:docs/handoff-history/c314-pre-acceptance.md.
Git blob:bac2b81fbaec1a30776ae75063d38808231d13f0.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
