# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C290 ACCEPTED PASS (diagnostic integrity only). C291 NOT REGISTERED.**
C289 remains ACCEPTED VALID NEGATIVE. No ACTIVE experiment until next preregistration/review.
Scientific execution:327e0a2e45270a4eb60f43daf8cca5c21242987c.
Published log:76706cdc46914e67957abb37fcb75c46d1af0eaa.

## Latest accepted evidence — C290

Acceptance:docs/experiment-ledger-addendum-c290-c291.md.
Summary:runs/c290-v5b-pair-margin-dd335cb112744775980aa441008b9a7f/summary.json.
Summary SHA256:1f4a3c16130b4c4517ddc7b5c09d7404ed83652fd0d6ce8b9a2438195a9cb11e.
Own40/focused4245 PASS;source586/protected1056;run_execution_valid=True.
Manifest SHA256:123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.
19440 saved query pairs,90 partitions,60 paired comparisons;scientific neural calls/training0.
Original C289 masked/full gates reconstructed without changes. C290 PASS means diagnostic integrity only.
Quad HOLDOUT auxiliary arms meet144/144 margins but still miss1 answer on289002/289003 and4 on289005.
Aligned always/early NORMAL predictions match exactly for289002..289005;289001 differs.
A met pair-sum margin is not a guarantee of individual256-class answer correctness.
Do not infer a uniquely causal representation/optimizer failure or retune old conditions.
C289 quad gates remain ce_only3/5,pair_always0/5,pair_early0/5.

## Next registration boundary

No C291 command until its six OWN files are committed,re-fetched and independently reviewed.
Use C290.verify_artifacts for C290's diagnostic output schema,not a training-checkpoint loader.
Any future training must use new seeds and concurrent controls;do not select C289 successes.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

The complete pre-acceptance C290 handoff is docs/handoff-history/c290-pre-acceptance.md,
Git blob722d41d5b2f7076827c5a7d0bdb2ecbbdc92b5da. Older handoffs remain unchanged.
Only this Formal state is authoritative. Accepted source/tests/preregistrations/logs and protected
dispatchers remain immutable;historical ACTIVE instructions are not executable.
