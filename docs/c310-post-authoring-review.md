# C310 post-authoring review

post_authoring_review = PASS
Scope: committed-byte/static review and executed local software tests; not actual C310 scientific evidence.
Review target: 0739750338ec413390e34aa5f5fcaa2c9d2b0116.
Acceptance base: 2cffcea33045a75582a94fadd963fa9f2b7d601d.

## Committed-byte verification

All six OWN files were fetched after the authoring commit and reread. Source388lines and test428lines
were read in consecutive ranges covering their full contents. The other four files were read in full.
Returned whole-file Git blob identities match independently computed hashes of local tested bytes6/6:

- fold_lm/v05_benchmarks/model_c310_value_renaming_audit.py: 2f581ca13bdcc5dc0cd7a87f15eea6782af367a9;24660bytes.
- tests_lm/test_v05_c310_value_renaming_audit.py: 82886fea3b992a176375341075a2acbea2d38498;27928bytes.
- tools/run_c310.ps1: 76690e7a475f9836ff2904fc0a1aad52e86b93c6;4635bytes.
- tools/invoke_c310.ps1: c20b024b14cd20d5f058ddfe2105635e08a0a697;7007bytes.
- docs/experiment-ledger-addendum-c310-preregistration.md: ebb26d34717ef05ba235ebaa27fe2a0b9831b322;8103bytes.
- docs/v5b-value-renaming-v0.1.md: f7560bc6602aff7a2f1ec17f0c159df814a3e4e9;1148bytes.

The remote acceptance-to-authoring comparison contains exactly those six additions. No accepted
source, test, preregistration, log or dispatcher was modified. Activation must preserve all six blobs.
The previous uncommitted draft was not treated as registered or as having completed post-commit tests.

## Tests actually run after all six matches

Normal: python -m unittest tests_lm.test_v05_c310_value_renaming_audit -v
Ran32 tests in5.579s; OK, zero failures/errors.

CP932 default emulation: the complete same unittest module was loaded and run under an
io.text_encoding patch returning cp932 only when no explicit encoding was supplied. The patch
covered import, class setup, all32 tests and teardown. Ran32 in5.170s; OK, zero failures/errors.
Both were complete uninterrupted TextTestRunner executions. Earlier pre-commit results are not
substituted for these post-match runs.
Runtime: Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5.

All6 files are UTF-8/no-NUL. Both Python files and all3 embedded Python blocks compile.
Recursive symtable/import-binding audit finds0 unresolved globals in the new source and tests,
allowing builtins and standard module globals. No py_compile-only claim of free-name validation.
Manifest self-hash matches0b4304400ddb57789a52aefb0bfe84690df7bb3fee9ef4c63e842fecfd595596.
All36 launcher paths are ordered C309 through C274. Postcheck uses sys.argv[2:38], head[38], argc39.

## Behavioral and scientific-path checks

The independently constructed logical fixture matches the exact accepted dataset SHA. A separate
scalar Python reference implements value lookup, class renaming and comparison counting without
using the vectorized counter. It agrees on changed and unchanged inputs and split-filtered cases.
All24 mappings preserve names' logical context and target bindings, are bijections, have exact
inverses and exactly two mappings per displayed destination. Every source has22 changed-input
permutations and two no-change permutations. Split denominators are explicitly checked.

Perfect predictions, always-the-other-fact predictions, constant non-value predictions and
TRAIN-correct/HOLDOUT-wrong predictions exercise the separation of consistency and correctness.
The last case stays consistent within each split while failing cross-split consistency, without
being promoted to capability PASS. A tied-output fixture preserves the first-class argmax rule
and reports every tied maximum. Invalid values, IDs, splits, queries, data shapes, logits, views,
cohorts and original totals are rejected. All60 prediction blocks/720 totals and all420 aggregate
groups are checked, with1140480 changed comparisons and separate51840+51840 controls.

Integration test31 executes the actual accepted C270 score function extracted by AST and checks
its original total fields against the child fixture totals. The local support file contains only
that fetched function, not a full parent module or repository clone; it is NOT committed. On the
user's checkout the test extracts score from the full accepted C270 file. This validates the
actual scorer's totals schema and grouping, not performance of a trained FOLD model.

All36 parent-hash rejections occur before parent verifier dispatch. Wrong parent status/schema,
flags and source identities are rejected. The actual precheck runs against a controlled706/1323
file fixture, rejects an unprotected repository helper and detects changed protected input bytes.
No-neural guards reject Module calls, model-state loads and tensor saves, then restore normal
operations. Actual runtime_preflight and run/verify_artifacts paths execute with substituted
parent/Git interfaces, preserving loader order, output inventory, no-overwrite and HEAD guards.
Byte alteration is rejected; semantic alteration is also rejected after updating its descriptor.
The suite-ID fixture constructs4942 test objects and verifies4941 exact retained IDs, plus duplicate
rejection. This is NOT execution of the actual4941 inherited tests. New source/tests explicitly
read files as UTF-8; CP932 emulates default decoding, not all Windows behavior.

## Parent semantics and dependency coverage

The exact accepted C309 verifier accepts35 ancestor summaries and its own execution HEAD and
returns(payload,metrics). Its writer stores final raw[str(length)][split][profile][view] logits in
fold-c309-core-lr-replication-eval-v1, plus original length_scores[*].totals. C310 verifies36 hashes
first, then invokes that exact verifier with35 ancestors; the summary hash seals all7 descriptors.
It requires the accepted negative cohort and rechecks the dataset hash. No model checkpoint is
loaded into a model, no predictions become training targets and no new evaluation inputs are run.

C304's scorer adapter maps repeat/shared_prefix/shared_suffix to the actual C270 profile names.
C310 repeats that mapping and validates original rows/correct/pairs/collapsed_pairs for every
split/profile/language. Hard predictions are compared on exactly corresponding logical rows.
Full256 argmax is preserved; only ASCII48..51 transform. Non-value classes stay fixed, so their
trivial consistency is counted as wrong. Ties are recorded, not silently resolved in favor of truth.

Sole direct repository import C309. All700 inherited sources and1309 inputs are retained and
verified, including C304.PINNED and repository-local context/core/factory-language helper coverage.
The test's C270 scorer source is already in this inherited set. Add OWN6+8 parent files for706/1323.
No accepted file or exclusion changes. No missing direct dependency is justified after the fact.
The full report's source IDs, permutation destinations and original predictions allow every pair
to be reconstructed without materializing redundant per-pair records. Repeated/directed comparisons
are not independent observations. No mechanism, significance or general-language claim is made.

## Runtime and release boundary

Scientific training/model calls/model-state loads/new checkpoints/row presentations/core calls/
network calls are0. Existing tensor reads and numeric work are allowed. JSON-only child output;
no tensor checkpoint write. Numerical work is fixed at2 CPU threads. Operational tests and
recursive parent verification are separate costs. Diagnostic PASS is not capability improvement.
C309's negative, C308's bounded PASS and Gate F NOT PASSED remain unchanged.

The selected launcher parses the runner; the unchanged active_v2 dispatcher must be parsed by
the user command and must parse the selected launcher. Validate precedes Execute and failure
returns before scientific publication. Own32/modules195/loaded4942/focused4941; sole inherited
exact C204 exclusion unchanged. ExpectedHead and unique ACTIVE checks remain mandatory.

Not run here: Windows PowerShell ParseFile, the user's36 real parent archives and protected bytes,
the real4941 inherited suite or the actual C310 saved-prediction findings. The container could not
clone the repository; local data/scorer support and parent/Git interfaces are controlled fixtures.
These limitations are not waived. All real-data checks remain mandatory in local Validate/Execute.
The review authorizes the guarded C310 launcher only. Integrity failures repair SAME C310;
C311 remains unregistered until formal C310 judgment. No old experiment is rerun for this release.
