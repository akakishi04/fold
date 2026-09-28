# C273 operational preflight recovery — mutable handoff regression dependency

## Status

C273 remains ACTIVE / NOT YET JUDGED. The user invocation at HEAD
a63c9aaa7b41fa109542da1be4f6b5789fb717a0 stopped in Mode Validate during the focused regression.
own24 had already passed. Scientific execution did not start and no scientific log publication was
attempted. This is an operational regression-compatibility defect, not a C273 scientific result.

## Root cause

The inherited accepted C272 own test
tests_lm.test_v05_c272_query_boundaries.C272Tests.test_24_manifest_seal_and_dispatcher_pins
unconditionally reads docs/experiment-ledger-and-handoff.md and requires the C272 manifest seal
89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604 to be present.

That assertion was valid while C272 was ACTIVE. After C272 was accepted, the C273 activation handoff
was rewritten around C273 and no longer contained the old C272 seal. Because the accepted C272 test
is itself pinned by C272 provenance, editing it would violate the parent source/input contract.
The inherited focused regression therefore correctly exposed a lifecycle mismatch in the test/handoff
contract. The failure is not in C273 model code or scientific data.

The user's failure output included the current handoff body because unittest's failed assertIn
printed the searched string, matching this dependency. Repository inspection confirms the current
handoff lacks the C272 seal while the inherited C272 test requires it.

## Repair

Immediate compatibility:
- add an append-only "Inherited regression compatibility seals" section to the current handoff;
- retain the C272 manifest seal there permanently while the pinned C272 test remains in focused
  regression;
- C273 own test24 now asserts this legacy seal during own24, so accidental removal is detected in
  seconds before the full focused suite.

Future lifecycle-safe rule:
- C273 and later tests may require their own seal in current handoff only while that experiment is
  ACTIVE;
- after acceptance, the same test resolves its seal from the immutable c###-c(next) acceptance
  addendum rather than current mutable handoff;
- static review must classify every inherited handoff-reading test before activation;
- no extra regression exclusion is added.

This rule is recorded in docs/experiment-authoring-runtime-gate.md under
"Mutable handoff lifecycle rule".

## Scientific invariants

C273 hypothesis,dual-boundary architecture,parameters,data,seeds,paired CE schedule,optimizer,
800-update budget,fixed gates,manifest contents and sealed manifest SHA remain unchanged.
The C273 manifest seal remains:
fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f.

Retry SAME C273 through Validate->Execute after static review and handoff compatibility update.
C274 remains unregistered.
