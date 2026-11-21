# C330 acceptance / C331 authoring boundary

Date: 2026-10-18 Japan time.
C330 ACCEPTED PASS (DIAGNOSTIC INTEGRITY), execution revision C330-R1.2.
Attempts 01/02/03 remain INVALID EXECUTION. C329 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. No production adoption. C331 not registered by this acceptance.

## Evidence identity and review boundary

Scientific execution: a92b0096949c4176f793dc2b57e910149222efb0.
Publication: 50e931bc13b9af8a6b25acae104a12f27d4eeaff; sole parent equals execution.
Publisher reports 289867 original Windows bytes; log SHA256:
ee852498382aad79a3892082a3b11a0368dc519debd5fef97279e16fa204a7ff.
Git log blob: b577bf4d2bf9a626f44d7f45d897690fc63162cc.
Metadata blob: 4c14913549cd1109c5502108e4b6dc83779c6a68.
The reviewer inspected exact-ref startup, full-regression completion, final rereads,
preserved seed gates, deciding residual strata and criterion transitions, and final
fresh verification. Counts below were reconciled from those published aggregates.
No independent whole-Windows-log rehash, all 220 local receipt-file read, raw-logit
recalculation or model replay is claimed by this remote review. The native executor
and fresh verifier report those integrity checks. Old C323/C324 attachments are not
current evidence. Publication alone was not used as proof of success.

## Valid native execution

5850 tests / 220 modules, failures=errors=skipped=0, successful=true.
Module-isolated regression elapsed 1189.327 seconds (including process orchestration).
Ordered full-test-ID digest:
f7c7f355197393a53f0d9d8f3f4c8a044e4b365719a4894090017e206e709dc6.
Native locks, accepted C329 saved semantics,841-source/1596-input registration,
all module success/PID evidence, saved diagnostic reconstruction,1596 final uncached
rereads and fresh verification passed. Regression/science/verify exit0;
run_execution_valid=true. The earlier C311 fault was not reproduced in this successful
isolated run; its original internal cause is NOT established or declared repaired.

Local folder: runs/c330-localization-688c9a321f204989b6a694820eaab9bd/.
Primary science/summary.json SHA256:
f7c1a6567f2ab9929528722bfc699b8228275e8cb185c31f1de87e5260278691.
Mandatory execution-envelope.json SHA256:
ad30fc8f64775ebe93f9c2650bc74dc809583c877397a94889745b3e388381ad.
Scientific manifest:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
Accepted recovery manifest:
cb09791f16e446ad2e1116981700c5be26997865d2da2eef89e76acdad1df8b9.
Both result/envelope carry full841/1596 protection and exact R1.2 manifest.
The parent execution also binds regression-plan-r1.json,regression-isolation-r1.json,
regression-result.json and220 module JSON/log pairs. A successor that relies on the
full regression receipt must validate and protect these443 evidence files as well
as the4 diagnostic outputs,primary and envelope. Do not fall back to838/1593 or
pretend the accepted supplemental executor/tests/receipts are optional.

## Deciding localization (extended2400, all five seeds and both logical splits)

Each domain has360 local cells /180 both-order cells.

|Domain|Failed local cells|Failed both-order cells|Mask-only local cells|
|---|---:|---:|---:|
|original2|0|0|0|
|original3|0|0|0|
|original4|0|0|0|
|original5|5|2|0|
|original6|32|12|0|
|interior4|9|3|0|

Total46/2160 failed local cells and17/1080 failed order cells. These are overlapping
assessments of reused tasks, not independent samples or summable error events.
All46 local failures include a normal-accuracy/query-pair failure; none is mask-only.
Original5: all5 failures are shared_suffix in English (2TRAIN,3HOLDOUT).
Original6:31/32 failures are shared_suffix across both languages/splits;one additional
shared_prefix English HOLDOUT cell fails. Interior:all9 failures are v_dominant,
all in seed329002 (4English TRAIN,4English HOLDOUT,1Japanese HOLDOUT).
Opaque scorer slot shared_suffix2 is NOT the same input-template meaning as v_dominant.

Original6 normal-accuracy failed conditions fall71->32 with43rescued/4regressed/28
persistent. Its evidence-drop failures17->14 and query-drop39->18; both-order29->12.
Interior normal failures97->9 with88rescued/0regressed; both-order48->3 with45rescued.
Original5 normal failures25->5 with21rescued/1regressed. Keep regressions visible.
C329's preserved full gates remain interior0/5->4/5, original2..6 retention1/5->1/5,
paired joint success1/5. C330 PASS does not revise any of those capability verdicts.

## Interpretation and bounded next question

Residual failure is not merely an overly strict mask-only criterion: genuine normal
binding errors remain, concentrated on long names that share their trailing bytes.
This is localization,not proof that query pooling caused them. It does not justify
changing thresholds,selecting the successful seed or claiming general language ability.

Before another fit, a bounded frozen-readout intervention can test whether supplying
some first-query-byte local representation to the mean-query branch changes these
errors while retaining the separate last-byte branch. Keep all ten C329 checkpoints
and all original/interior evaluation conditions,compare native before/after replay,
and distinguish this from C317 (which replaced the last branch by the first).
This note is not execution authorization. Separate implementation, preregistration,
committed-byte review and activation are required before a C331 user command.
