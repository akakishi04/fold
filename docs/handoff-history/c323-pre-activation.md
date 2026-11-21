# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C322 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C323 NOT REGISTERED.**
No ACTIVE experiment until separate committed-byte review and activation.
C321 remains ACCEPTED VALID NEGATIVE (interior-order0/5);
C320 remains bounded ACCEPTED PASS (unequal-length5/5 mean_last).
Every earlier verdict unchanged. Do not rerun C322.
Latest accepted scientific execution:b7943ab4435d68d2716e6137b596042b777f2efb.
Latest published log:278e883bd5b6555aa2bef8a43e1634dc5e44e6f0.

## Latest accepted evidence — C322

Acceptance:docs/experiment-ledger-addendum-c322-c323.md.
Summary:runs/c322-v5b-query-contrast-f164844010f04c24bcfda4a743b44a72/summary.json.
Summary SHA256:fdcf1f2ac893a46c900e50db93740004926c70765ca269ba0cfe7474bf4c5796.
Published log SHA256:eb081b5f0f3b421dc987c1605b21efca5312438cdcad9d70865fc0fc4f7f8e85.
Published log bytes:1173665;proven CRLF SHA matches metadata.
Own24/full5269 PASS,full suite1245.157s,0failures/0errors,exit0/0x00000000.
778 source pins/1467 protected inputs;run_execution_valid=True.
Precheck and saved query-pair reconstruction PASS;no new model forwards/training.
Saved original4 botharms4320/4320 correct,0/2160 paired answer collapse.
Interior mean_last2211/4320 correct,1996/2160 same answers,107/2160 both correct,
118/2160 both target-preference direction,1315/2160 positive contrast;
mean relative preference contrast0.6438573484898602 vs old4 24.805650267612712.
Interior last_only2292/4320,1951/2160 same answers,171/2160 both correct,
190/2160 target direction,1410/2160 positive contrast;
mean contrast0.9952475930687953 vs old4 24.404063485988974.
No exact near-offset-invariant logit pairs at tolerance1e-9 under either interior policy.
Identical argmax need not mean identical score vectors or hidden representations.
Only integrity diagnosis passes;C3210/5 and Gate F NOT PASSED.

## Next registration boundary

Proposed C323:fixed C321/C322 saved logits. For the two permutations of the
same facts/values/question,ask whether collapsed answers track first/last
fact position more than the requested entity. Reconcile original-four and
interior conditions, all10seed/arm states, all bilingual profiles/splits.
No retraining,new neural forward,stored checkpoint load,per-question model
selection,or changed capability thresholds.
Register,review,activate separately;no executable C323 yet.

## Runtime and cost audit

C322 validation full5269 historical tests took1245.157s;test module
boundaries show multiple prior c182/c304/c315/c316/c309 modules at~45-51s each.
Source/parent recursive checks may contribute additional time;individual
Git metadata commands are not established as the sole bottleneck.
Keep single-process full ordered suite and historical gates intact.
Explore safe bulk hash verification and phase timers without waiving coverage.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical tests.

## Historical state

Pre-acceptance handoff:docs/handoff-history/c322-pre-acceptance.md.
Git blob:2a0591d6a25b64d7bf7a779ad67c076a1a6ed407.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
