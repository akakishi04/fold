# C339 post-authoring review

Date: 2026-10-26 Japan time.
post_authoring_review = PASS
Committed source/preregistration target: e9a806236bcb6376ca9eb7632c8c24fb7344111e.
Acceptance base: 928bc539f83a22584e71e99adac7f5031bd480d0.
This is authoring approval, not native Windows/full6202 regression/scientific PASS.
Use the subsequent documentation-only activation HEAD for the user launch.

## Complete committed-byte reread

All six files were fetched again at the exact source commit and read through EOF:
benchmark1..105,106..210,211..330(actual307lines); executor1..110,111..210,
211..310,311..430(actual406); tests1..110,111..220,221..325,326..446;
full21-line runner/full58-line launcher; contract1..95,96..200(actual168).
Returned Git blobs match independently hashed local raw files used below:

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c339_saved_support_transfer.py|edde2009f4b8135199eea993d2a85aa987e87d4b|
|tools/c339_execution.py|27c83c8b5a3af364475a73ffd1563607255607ad|
|tests_lm/test_v05_c339_saved_support_transfer.py|e5ee1cb249ce5256471f24db761538e48082467e|
|tools/run_c339.ps1|dc44c3e79327102eabae223fee83e782b3738943|
|tools/invoke_c339.ps1|657c3bf63077f6f6b808e87770f9179c5efc8707|
|docs/experiment-ledger-addendum-c339-preregistration.md|a525cf3966f851ef17bd4265f0af17628abf4d5d|

Remote comparison confirms exactly these six additions. No accepted source, test,
contract, log, lock implementation or dispatcher changed. No correction to these
committed files was needed during this independent post-authoring review.

## Checks performed after the complete reread

Normal own unittest:32/32 PASS,0failures/errors/skips,13.227seconds.
CP932-default-text-open emulation:32/32 PASS,0failures/errors/skips,14.075seconds.
Both builtins.open and io.open use CP932 only when text encoding is unspecified;
explicit encoding/binary modes remain unchanged. This is not native Windows testing.
All6files UTF8/noNUL; all3Python files compile/import. Recursive LOAD_GLOBAL audit
of208function/method/nested code objects found0undefined global bindings.
Actual32method ordered-ID SHA256:
4e617dae39b4d8a61731f8e96cf5fb06a246d33c15448e5e733e39d08fd05e36.
Manifest self-hash:
3f3380eac1a0e5d0c076825081c10edfa86bed75e02b2c1b5ee23ebf21dc42f1.

After normal/encoding tests, two in-memory negative controls were exercised:
- Set every supportNLL to0: test04 exact tie and test05 independent decomposition
  each produce the expected assertion failure (2failures,not source-test failures).
- Reverse native/candidate transition orientation: test09 catches the changed
  wrong_observed->outside_catalog transition (1expected assertion failure).
Original functions were restored and those tests then passed normally. All six
source SHA256 values stayed unchanged. No intentional mutant was written to Git.

Environment LinuxPython3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5; own class uses2Torchthreads.
This is a targeted source tree, not a full repository checkout. Local-only verbatim
C267dataset and C337audit_logits/aggregate extracts were used; never committed.
Parent summaries/scorers, historical test inventories/module proofs and OS leases
in integration tests are explicit synthetic collaborators. Actual child control
paths and numeric analysis run; actual C338logits/checkpoints, full6202historical
suite and Windows native locks do not run in this author environment.
PowerShell was not available; native AST execution is not claimed. The mandatory
standard user block/dispatcher/launcher/runner AST chain remains before logging.

## Scientific-variable and numerical audit

All ten C338states retained, seeds338001..338005 and native/support_loss; no selection,
new fitting/model forward, output filtering, changed prompt or altered prior verdict.
Scope includes original2..6/interior4, both splits/languages and all profiles.
Original1 is not silently promoted to a new diagnostic domain; parent semantics
still validates its raw views along with all114saved views.

Accepted C337.audit_logits supplies unchanged256class first-index argmax, four
answer kinds, exact pair/support-margin signs. outside_catalog is not synonymous
with nondigit. Both outside254classes and both supplied values are retained.
New supportNLL and withinNLL use stable logaddexp(0,gap), preserving the exact softplus
identity rather than default functional-softplus threshold approximation. Their
mathematical sum is the ordinary target cross-entropy; no floor/epsilon/clipping.
Source logits, derived gaps/components and paired differences must be finite.

Tests compare against independent log_softmax and two-class cross_entropy arithmetic,
including values around the usual softplus approximation threshold, exact ties,
all256argmax, nonbinary canonical values, scalar shifts, immutability and overflow.
Inputs to this offline measurement include labels; they do not enter model inference.
No label-assisted corrected accuracy is computed or claimed.

Paired comparisons bind row_id, target and other supplied value. A4x4 kind matrix
and two3x3sign matrices preserve raw rescue/regression and their direction. Means
use math.fsum with candidate-minus-native deltas. Sign/partition/marginal checks
prevent counts moving unnoticed between groups. Positive NLL delta means worse,
not improvement. A positive margin delta is descriptive, not guaranteed accuracy.

## Real analysis/writer paths and parent semantic contract

Production analyze executes across51840synthetic normal answers,720strata and360
paired strata (25920paired answers). Synthetic logits deliberately contain all four
error kinds, ties, rescues and regressions. Canonical data fixture is compared with
C267.dataset and fixed SHA, including all12ordered0..3value pairs; no binary-only test.
Independent parent fixtures compute60supportpartitions and30query-pair contrasts.
Production grouping uses language/entities/values/permutation and entity query,
not assumed arbitrary row adjacency. Accepted C324query-pair source was inspected.

Every parent correct/pair/rescue/regression/gain/outside_gain field must reconcile.
All normal source replay logits and argmax are checked. Complete source114-view,
checkpoint fingerprint and training-trace reconstruction remains in mandatory
immediate C338.semantic_recheck before child diagnosis. Synthetic source fixtures
cover only normal child-selected views and do not claim to replace that parent work.

Real temporary torch archive/JSON loader, writer and semantic recheck round-trip all
four outputs, then reject changed paired output. Cohort/order/schema/data/state/
receipt/replay and parent count changes are rejected. Summary tests cover joint
marginals, sign marginals, finite means, parent negative and rescue conservation.

Immediate parent has fold-c338-trained-v1 with statusFAIL, scientific_execution_valid
true and capability_gate_applicable true. Child has diagnosticPASS/nonapplicable;
these contracts are explicitly separated. Parent candidatefalse/eligible0 is retained.
Exact four-argument C338.semantic_recheck(source_out,data_out,cx,read) is called under
no_neural. Test22 asserts that dispatch and rejects missing protected inputs.
No old six-argument diagnostic-loader guess or recursive ancestor semantic rerun.

## Evidence protection and execution audit

Require exact C338primary/envelope and889source/5296input maps, full6170receipt and
all5296final rereads. Parent executor and benchmark blobs are verified before import;
dictionary helper bridge remains. Rebuild inherited maps through C338.snapshot.
Add ALL467parent outputs, including459module proofs(3+228JSON/logpairs), then6own:
895sources/5769inputs. Test21 builds a real5769-file temporary union with synthetic
ancestor contracts; test20 independently rejects a changed module proof file hash.
Accepted direct/lazy C338/C332/C329/C324/C337 dependencies remain inherited pins.
No unpinned helper or accepted source rewrite was introduced.

Native R4read leases span evidence checks/regression/diagnosis/reconstruction, with
EXPLICIT finite max_files=INPUT_COUNT=5769. Test27 rejects omission or wrong capacity.
No default4096, eviction, omitted evidence or unlocked fallback. All5769inputs receive
final uncached rereads; all four outputs are hash/size-bound around reconstruction
and again before summary/envelope writing. Fresh verification reconstructs parent,
proof maps and child metrics without new model inference or replaying optimizer steps.

Full6202tests/229modules=unchanged6170IDs+actual32own loader. Sole inherited exact
C204mutable-ACTIVE exclusion retained; no new exclusions/skips/cached test success.
C339owns guard/CLI/plan and delegates ordinary unittest execution and module evidence
to accepted C330R1.2helpers. Direct/immediate-child PID and canonicalmarkers remain.
Synthetic229module receipts exercise collector/verifier458validator calls and reject
changed logs; these are not6202native historical tests run on the author host.

Actual worker/fresh-verifier paths run with explicitly synthetic parent/runtime/lock
callbacks and real child output/summary/envelope writes. Failed regression never
reaches audit. Diagnostic applicability tampering is rejected. Real temporary Git,
JSON/CRLF handling and a nonzero subprocess retain failure evidence without retry.

## Launcher and approval boundary

Runner/launcher paths, ExpectedHead/Folder arguments, role, output prefix and c339
publisher all agree. Standard user block parses active_v2; unchanged dispatcher
parses selected invoke_c339; launcher parses itself and run_c339 before logging.
Stale/dirty/wrong branch/ambiguousACTIVE/missing dependency invocations skip first.
Source-only commit is not an execution authorization; final review/ACTIVE commit
changes documentation only. Native full6202tests, real saved-logit diagnosis,
5769final rereads and independent verification must still pass in the user run.
INVALID stays SAMEC339, never C340. C338negative and Gate F NOT PASSED remain.
