# C327 acceptance / C328 boundary

Reviewed 2026-10-17 Japan time.
C327 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
C326 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED; earlier verdicts unchanged.
C328 NOT REGISTERED at acceptance. No ACTIVE until separate implementation/review.

## Identity and review scope

Scientific execution:847c924f50303d93ed4df7acec74b77209b7d261.
Publication:926113e7602f1ee36445cde9bbf90eab1539ace1; its parent equals execution.
Published console:docs/experiment-run-logs/c327/latest.log and latest.json.
Metadata:35743 Windows bytes;log SHA256
cbff015cbec04a51270a9b3410ede85391879e2bdbc2dc4ea34db2b203595cb5.
Git log blob:54c0f9301e34cb12e87c89e7551e0c83394a0298.
Reviewer read native preflight, regression completion, all40 alignment aggregates,
all10 model completion lines, final reread and fresh-envelope verification. Aggregate
counts were independently summed. No independent whole-log rehash, local gradient
recomputation or checkpoint replay is claimed. Old uploads are not C327 evidence.

Folder:runs/c327-gradient-1cf048a0cd9449b6af6485a4802c46ca/.
Primary science/summary.json SHA256:
c4a061e158a1bd617fb7638bb034b7aa3ef78da06b15062474ff986d1f347719.
Mandatory execution-envelope.json SHA256:
fb44749ce38e0b0909238c51c13bbb1eb95e1898369313fb34d95483a543e535.
Immediate outputs:diagnostic-plan.json,gradients.pt,measurements.json,
validation-summary.json. Four outputs plus summary+envelope are SIX parent files,
not the eight-output training schema inherited by earlier experiments.

## Execution validity

Native lock, immediate C326 semantic reconstruction and native gradient preflight PASS.
820sources/1549inputs;manifest
36fca7e0b0baea3b51adcaad167caa551033e0f802ab3f883d4f4f846cbc22ee.
Full5658tests/216modules PASS;0failures/errors/skips;864.515 seconds.
Ordered test-ID digest:
47c7f39d55ebfe22be9a4e65d33bb1b1b56bba1087700e2ba0953330d53cb7b1.
All10 fixed models completed6gradient pairs each;reverse repeats PASS;weights unchanged.
Cohort240forwards/gradients,23040rows,960coreforwards;0updates/optimizer steps.
Saved gradient geometry reconstructed;all1549final uncached rereads completed.
Fresh envelope verified820sources/1549inputs/5658tests;all process exits0;
diagnostic_status=PASS;run_execution_valid=true. Existing warnings remain in the log.

## Observations

Every group has6defined cosines per seed/arm. Denominator30per arm,60pooled.

| Parameter group | Negative dot epoch4 | Negative dot batch4 | Joint strict descent epoch4 | Joint strict descent batch4 |
|---|---:|---:|---:|---:|
|all|7/30|11/30|25/30|25/30|
|core|11/30|14/30|21/30|19/30|
|reader (read.* only)|10/30|9/30|22/30|27/30|
|other|6/30|10/30|26/30|26/30|

Pooled negative dots:18/25/19/16 of60 for all/core/reader/other.
Pooled joint strict descent:50/40/49/52 of60. The all group overlaps its partitions;
these are not240 independent objectives. PASS does not require any particular sign.

At these terminal checkpoints, negative alignment occurs, but the Euclidean negative
mean is still a strict first-order descent direction for both losses in50/60 whole-
parameter conditions. This does not establish an actual finite AdamW update, optimizer
moment history, full-trajectory causality, or the original-length6 gradient geometry.
No capability gain, structural impossibility, generalization or Gate F claim.

## Next prospective question (not executable registration)

With the fixed C326 batch4 curriculum and1200updates, compare constant learning rates
against both rates scaled0.1 after800completed updates. Use fresh paired seeds,
identical first800weights/moments, unchanged optimizer state at the switch and all
existing task gates. The result above motivates testing optimization sensitivity;
it does not prove that late constant rates caused prior failures.
Register/test/commit/reread/review the complete child before activation. No seed,
ratio or budget search; no accepted source edits, CI or environment repair.
