# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C321 ACCEPTED VALID NEGATIVE. C322 NOT REGISTERED.**
No ACTIVE experiment until separate committed-byte review and activation.
C320 bounded PASS,C319 negative,and every earlier verdict remain unchanged.
Latest accepted execution:a31d5c5389f41cdb137b0bf375b7c7a99d8fb882.
Latest publication:b4e1686971d8d4a6d988a7f0e5e02a80cea6ec41. Do not rerun C321.

## Latest accepted evidence — C321

Acceptance:docs/experiment-ledger-addendum-c321-c322.md.
Summary:runs/c321-v5b-interior-order-ef98962d405b402ba3926a6d1c2625b2/summary.json.
SHA256:0e95c700cbac90025beb7baf1d65413cb1694de72b659540c2eb901f77f52fd9.
Own24/full5245 PASS;source772/protected1455;run_execution_valid=True.
Scientific exit0;capability statusFAIL. Both arms0/5. Every old replay error0.0.
mean_last normal2211/4320;last_only2292/4320. Original collapsed query-pair sums1996/2160
and1951/2160 respectively. No new scores or changed decoding used for this verdict.

## Recovery boundary

Earlier execution failed at5bffb4887a1f2729058472d875cf413bc26836e4 and published
caaa42ac45a332c8b946714919eda58c38533384. That evidence remains in immutable history.
Instrumented retry completed all stages;original root cause remains UNCONFIRMED.
Preserve direct science/stderr logging and exact exit capture. Do not claim an environment fix.

## Next registration boundary

Proposed C322:paired-query numerical diagnostic from saved C321 old4 and interior logits.
Distinguish identical argmax from output-vector collapse and weak relative preference between
the two facts' value classes. Keep all10 states,profiles,languages/splits and original scores.
No model inference,training,checkpoint loading or restricted-value decoder. Diagnostic-only
integrity gate. No command before committed-byte review;C323 not registered.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-acceptance:docs/handoff-history/c321-pre-acceptance.md.
Git blob:d05a8ffdc6eb4da12f5c864c416186be41392f78.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
