# C287 committed-byte post-authoring review

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Review target:496cc0a6cc6b26eb4629495b8254f39591b80d61.
Acceptance base:6ce09f66e8ea61a9fbfffd1e2de38a9ba8cdef61.
Initial authoring commit:b325a61090f731c4ee472d00e7b8542c101ab328.
Authoritative Windows runtime gate:PENDING.

## Identity and mutation boundary

Compare acceptance to review target:exactly6 added OWN files;no accepted file changed.
All6 OWN files were fetched after initial commit;complete source and tests were read in ranges.
Review found four default-encoding read_text calls in tests. The review-target commit changes only
those calls to explicit UTF-8 (three changed lines). Modified remote ranges were re-fetched;
compare confirms the other5 files are unchanged. All6 final Git blob identities match local bytes.

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c287_saved_fit_partition_audit.py|05ab28c666203eaf69506c024a2805f31986a3ff|20530|
|tests_lm/test_v05_c287_saved_fit_partition_audit.py|4d04a8e2279113ed7d8ade25440d7966271541a9|17343|
|tools/run_c287.ps1|ef954cac17519c26523245a1c6230a9d5084e900|4982|
|tools/invoke_c287.ps1|b0e21ea77d84707c82d9efdde2457ccb42d632cd|4746|
|docs/experiment-ledger-addendum-c287-preregistration.md|4ae212bda8a59e5e769ddb36efd4788b38263702|6109|
|docs/v5b-saved-fit-partition-audit-v0.1.md|7415a64e5e25ac123941463725bf6021558fef8e|1531|

## Executed checks

Linux/Python3.13.5/PyTorch2.10.0+cpu. Final post-match own32 run:32 tests in0.955s;OK.
Initial and UTF-8-corrected runs also passed. Both Python files and all3 embedded Python blocks
compile. Bytecode global-binding audit with normal module __file__ binding:unresolved globals0.
No NULs. Computed manifest SHA256 matches98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430.
Seal tests actually execute valid,malformed and mismatched cases;no global sentinel replacement.

Behavioral fixtures cover complete3240 grids,missing/duplicate/unordered keys,nonfinite and boolean
metrics,NLL/count consistency,TRAIN versus HOLDOUT versus quad partition distinction,mask-only
separation,two-order direct failures,weighted final NLL versus last-minibatch CE,all180 trace bins
and90 pair deltas,window/length/profile boundaries,prefix mismatch,all13 hashes and parent dispatch,
forbidden neural/state/write operations,result scope,run/persistence/no-overwrite,hash and semantic
tampering,actual suite assembly with exact inherited exclusion,CLI order and immutable inventory.
Parent archives and Git are mocked in relevant fixtures. The test grids/loss traces are synthetic;
no actual C287 parent-data diagnostic or full historical regression was executed here.

## Writer semantics,dependency coverage and call ordering

Read live C286 fit/analyze source:loss_history is pre-update minibatch CE;step400_sha256 is captured
after update400. C286 verifies full LR/exposure/common-prefix histories before child consumption.
Read live C267.score:answer_nll is mean final normal CE by answer cell. C270 uses the same field
and C283 preserves it through profile adaptation. Therefore row-weighted split NLL is a final-model
metric,not a substitute for the chronological trace. Length4 TRAIN is never labeled fitted data.

Direct child import is C286 only. Its context provides the pinned audit/factory helpers. All
repository-local calls remain in inherited protection maps;the dependency pattern extends through
C286 plus OWN source. Source568=562+6;protected1016=1001+9+6;dependency-union63.
No old analyze function is dispatched on C287 output. C286.verify_artifacts is the parent verifier;
C287.analyze owns new partition semantics. All10 identities and exact original flags are retained.

Runner Validate performs parent/protection/manifest checks and a real schema dry-run before own32
and focused4117. Scientific logging starts only after Validate succeeds. Postcheck indices are
out=argv1,thirteen paths=argv[2:15],HEAD=argv15. Launcher has thirteen independent parent paths,
ACTIVE287/branch/clean-tree/ExpectedHead checks and runner ParseFile before logging/publication.
User command parses the protected dispatcher;dispatcher parses the selected launcher.
C287 result PASS means integrity only. Module calls/state loads/checkpoint writes are blocked.

## Remaining runtime gates

Actual user-local parent artifacts/pins,real full4117 regression,PowerShell ParseFile and complete
saved reconstruction remain pending. They must pass on the authoritative Windows environment.
Reviewed OWN6 must remain unchanged at activation. C288 NOT REGISTERED. Gate F NOT PASSED.
