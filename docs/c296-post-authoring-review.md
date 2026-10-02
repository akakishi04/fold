# C296 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review and local behavioral fixtures,not authoritative FOLD science.
Review target:128824681fd3cef51246153a817a6060f833a7ba.
Acceptance base:ae3705004c346edd7c29d1ee5708233d5b77b61d.

## Committed-byte verification

All six OWN files were fetched after the authoring commit at the immutable review SHA. The Python
source and tests were reread in consecutive ranges spanning the complete files;the four remaining
files were fetched in full. Whole-file Git blobs match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c296_render_balanced_batches.py:ae4fd7a45ec9306b1b81a82f8707269f1d88277b;27353 bytes.
- tests_lm/test_v05_c296_render_balanced_batches.py:9701ede1f60e382fc320cdf4282321a2078145ee;27060 bytes.
- tools/run_c296.ps1:5eaf7a0c487c144a10ab1b20f250bbf4431c72d2;4676 bytes.
- tools/invoke_c296.ps1:219d0f09af6df93eab568ed6ac6868b8c075dcc0;5623 bytes.
- docs/experiment-ledger-addendum-c296-preregistration.md:e3abdcccfdae8787373bc24411dec41d552663e2;8018 bytes.
- docs/v5b-render-balanced-minibatches-v0.1.md:2cb123531205ebeb4d7f2793a3c14bb7ae2981bb;1362 bytes.

Remote acceptance-to-authoring comparison shows exactly these six additions. No accepted source,
test,preregistration,log or dispatcher was modified. Activation must preserve the reviewed blobs.
Acceptance of C295 and authoring of C296 are separate commits.

## Tests actually executed after all six matches

python -m unittest tests_lm.test_v05_c296_render_balanced_batches -v
Normal local default:Ran40 in16.582s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran40 in17.273s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. Not Windows or the full4461-test inherited suite.
The earlier pre-commit40-test run is not substituted for these post-match executions.

All six files decode as UTF-8 and contain no NUL. Both Python files and three embedded runner
Python blocks compile. Symbol-table/import-binding audit finds zero unresolved custom globals,
allowing standard module globals. Manifest recomputation matches:
b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9.

The actual schedule builder is exercised for all five seeds. Tests verify every complete24-step
block's event multiset,all792 balanced batches' six rendering counts,identical final8 batches,
complete intact query pairs,per-length exposure100 for every row,and deterministic schedules.
Separate rendered-token/target checks compare complete block multisets,not just event counts.
Missing/duplicated events,out-of-range indices,wrong target bindings,changed tails and altered
persisted plans are rejected. Each fit stores its actual tensor plan and reconstructible hashes.

The actual fit loop performs800 AdamW steps on each of two small synthetic classifiers. A repeated
balanced run with an optimizer spy confirms one optimizer,step800 and identical losses/weights.
A separate train_one fixture executes800 training calls plus81 frozen evaluation calls and checks
881 forwards/46176 rows. The toy inputs encode synthetic target identity:these tests verify control
flow and arithmetic,NOT binding or transfer ability of the actual FOLD model.

Other fixtures check independent initial storage,ordinary CE calculation,loss/replay corruption,
10-result/60-partition/180-contrast analysis,one-candidate-miss negativity,role reconciliation,
22 summary hash failures before parent dispatch,and622/1131 protection with missing-helper failure.
Production run-path tests exercise loader order,ten train calls,ten replays,persisted roundtrip,
no-overwrite and both hash/semantic tampering. Parent archives,Git,legacy models/scorers and suite
members are mocked where unavailable. Semantic ID-filter tests build synthetic suites;they do not
mean the real inherited4461 tests have been loaded or run here.

## Scientific-path and parent contract review

The sole direct repository import is C295. Its context returns C294 numerical helpers,C293,
C287 diagnostic normalizer,C284 evaluator/replayer,C283 quad scorer,C282 TRAIN tables and the core
bundle. C296 uses the corresponding returned modules without altering any accepted helper.
The parent C295 writer saves ten800/1600 timepoint records and five trajectories,not a three-arm
cohort. C296 verifies22 ordered summary hashes before calling exact C295.verify_artifacts with21
ancestors and its accepted execution HEAD. That verifier reconstructs all original masked/full
gates,trajectories and eight artifacts under no-neural guards. The exact parent summary hash
commits every artifact hash/size descriptor. Canonical dataset/triple/quad hashes are checked again.
Fresh C296 weights never initialize from a parent checkpoint or selected successful seed.

C296 precheck retains and checks every616 parent source and1116 protected input. Modules exposed
by the used parent context/core bundle must be present in the inherited map,including C295's
exact ae88e50e3aa77fb81b8dc800aee98cdb89276dab blob. Adding OWN6 and nine parent summary/artifact
files yields622 source pins and1131 protected inputs. No missing pin is waived after execution.
The inherited C284 frozen evaluate/replay contract remains81 calls/7776 rows/324 core calls per
state pass,strict state load,fingerprint preservation,all-view drift<=1e-9 and exact argmax.
C294's oracle conditional counts are numerical diagnostics only and never decide the gate.

C278 mean/final readout and C269 visible query-span source were re-read:query boundaries and masks
are computed per row. C296 gathering keeps each complete padded48-token prefix and does not pass
length/profile metadata,labels,query-pair identifiers or support masks into model.forward. Actual
mixed-rendering FOLD execution still must pass the user's scientific runtime;it is not claimed
executed by the synthetic fixtures.

## Conditions,counts and operational review

Both arms are fresh800-update ordinary-CE runs. Only batching/order differs;the original rendered
example multiset is identical within each complete24-update block and globally. Last8 updates
are shared. Independent same-seed models have identical initial weights but intentionally different
first minibatches;no false first-loss or common-trajectory claim is asserted. This is not a direct
comparison to old C295's1600 checkpoints or a proof of gradient conflict/forgetting.
All candidate5/5 four-character thresholds remain original;seen tasks and oracle views are separate.
Per model800 train+81 evaluation+81 replay gives962 forwards;totals9620/539520/38480 for ten models.
One model archive write/load and10 strict state loads;not C295's20 timepoint-related loads.

Own40/modules181/loaded4462/focused4461;sole inherited exact C204 exclusion retained. No accepted
mutable-ACTIVE test is changed. New tests do not hardcode future handoff state. All read_text calls
in the new source/tests explicitly use UTF-8 and actual document reads are tested under CP932 emulation.
Runner has three Python blocks and22 inputs:postcheck paths=sys.argv[2:24],head=sys.argv[24],argc25.
Launcher contains22 fixed ordered paths,checks ACTIVE C296,branches/HEAD/clean tree and runner syntax,
and returns before scientific publication on Validate failure. Existing invoke_active_v2 was
re-fetched at the review target;blob e3923b6224959b442afefa02fafa967e2e6d462e. Its self/selected-launcher
parsing and RESULT_ALREADY_PUBLISHED protection remain unchanged. The user block parses it too.

## Mandatory authoritative runtime boundary

Not performed here:Windows PowerShell ParseFile,real local parent artifacts/Windows byte hashes,
the actual4461 inherited regression suite,and ten real FOLD training/evaluation/replay runs.
These remain mandatory Validate/Execute gates. Review PASS authorizes only that guarded path,
not a scientific outcome. Validate failures skip science/publication;integrity failures retry
SAME C296 without changed scientific conditions. C297 remains unregistered;Gate F NOT PASSED.
