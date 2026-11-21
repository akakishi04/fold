# C272 operational preflight recovery — stale validate_result cardinality

## Status

C272 remains ACTIVE / NOT YET JUDGED. The user invocation at HEAD
5c9ff64d9adfc154edc188b25a3699063e25ab4a stopped in Mode Validate.
Own24 reported one ERROR;scientific execution did not start and no scientific log publication was
attempted. This is operational authoring recovery,not a C272 scientific result.

## Root cause

C272 protected-input accounting was corrected before activation from820 to826:
parent C271 protected812 + parent summary1 + parent artifacts7 + C272 OWN6 =826.

The final manifest,precheck,runner,preregistration and handoff used826, but
`validate_result()` still contained the older hard-coded tuple `(478,820)`.
Own test17 creates an otherwise-valid synthetic payload with the registered826 protected inputs and
calls `validate_result`;the stale literal rejected that valid fixture and surfaced as the single
authoring-test ERROR.

The manifest itself was already correctly sealed as:
89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
This recovery does not change `manifest()`,so that seal remains valid.

## Repair

- `precheck` now derives expected source/input counts from the sealed manifest.
- `validate_result` now derives the same expected counts from the sealed manifest.
- the duplicate executable numeric tuple is removed.
- own test21 explicitly verifies manifest counts are478/826,that stale `(478,820)` does not appear
  in `validate_result`,and that both precheck/validator read `registration["protected_inputs"]`.
- docs/experiment-authoring-runtime-gate.md now requires registration cardinalities to have one
  executable source of truth: `manifest()`.

Scientific hypothesis,model code,boundary-pair formula,data,seeds,optimizer,800-update budget,
thresholds,artifacts and workload are unchanged. C272 remains the same experiment.

## Stop

Retry SAME C272 through the standard Validate->Execute path. If Validate fails again,do not force
Execute. C273 remains unregistered until C272 has a valid judged result.
