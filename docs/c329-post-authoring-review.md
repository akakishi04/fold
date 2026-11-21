# C329 post-authoring review

Review date: 2026-10-17 Japan time.
post_authoring_review = PASS
Committed source/preregistration review target:
296b3c8e775f74284086dbb823a7fd29fd515b4a.
Acceptance base: cc8881705867b748699dc9ce25a27a0a72d76d16.
This is authoring approval, NOT a scientific C329 verdict, native Windows execution
or full historical-regression PASS. Use the subsequent final activation HEAD in the
user command, not the source-only review target.

## Complete committed-byte reread

After publishing the source/tests/runner/launcher/preregistration commit, all six own
files were fetched again at that exact commit and read through EOF. Long Python and
preregistration files were read in consecutive ranges; no truncated range was used
as a claim of complete coverage. Returned Git blobs match the independently calculated
Git blob hashes of the local raw bytes tested below:

| File | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c329_fixed_budget_extension.py | e817c877d765661ae3baa82d0d4558b3945d88df |
| tools/c329_execution.py | 1dc02b935837037fc4c8f0c30429dca9311229e3 |
| tests_lm/test_v05_c329_fixed_budget_extension.py | 62eb5c3512abcb959adbbdd1beb29c3f41563772 |
| tools/run_c329.ps1 | 42d44a83eafae6957a129fc2163e77ddf24201f6 |
| tools/invoke_c329.ps1 | b8f20601257a23855573e4de9f439b19e589f6b4 |
| docs/experiment-ledger-addendum-c329-preregistration.md | d324d7ba0ba85bf71b7833913a6be999c0ba1dbe |

Remote compare against the acceptance commit confirms exactly these six additions;
no accepted source/test/contract/log/dispatcher was edited or deleted. C328 acceptance
is a separate commit. This review and ACTIVE handoff are later documentation-only
changes, not modifications of the six protected experimental files.

## Checks rerun after the remote reread

Normal own suite:48/48 PASS, failures/errors/skips0;9.526seconds.
CP932-default-text-open emulation:48/48 PASS, failures/errors/skips0;14.455seconds.
The emulation wraps both builtins.open and io.open, supplying CP932 only when a text
encoding is unspecified; explicit encodings and binary opens remain unchanged.
This is not native Windows or a claim about the user's actual system locale.

All six files decode as UTF-8 and contain no NUL. All three Python files compile and
import. Recursive function/method/nested-code LOAD_GLOBAL checks found zero undefined
global names. The manifest self-hash matches:
9968ab6d8d2abdd3751b6ac1d1b1116a088d1c8abbdebdae50b580005d6fb7d8.

Environment:Linux Python3.13.5 / PyTorch2.10.0+cpu / NumPy2.3.5;two Torch threads.
No PowerShell executable was available. Author-side native PowerShell AST execution
is NOT claimed; the mandatory user-side dispatcher/launcher/runner ParseFile chain
was retained and source-reviewed. Native authoritative runtime remains unchanged.

## Numeric path and actual trajectory prefix

The production optimize loop creates one native C308 core_slow AdamW optimizer,
sets FIT_RNG once, uses constant noncore.005/core.0005 rates, and executes the exact
base1200 event indices twice. It keeps ordinary mean CE, backward, global norm1
clipping and optimizer.step. There is no rate decay, reset, second seed call,
intermediate evaluation or accepted-global patch in this scientific path.

The real2400-update Torch toy fixture runs this production loop with an explicitly
small model and synthetic token selector. It verifies one optimizer creation, the
exact0..1199 repeated event order, constant rates,1200/2400 snapshot hashes, preserved
prefix storage, unchanged optimizer/model state across the continuation boundary,
and distinct final snapshots. A separate four-update reference gives exact prefix
and final state parity with explicit CE/backward/clip/AdamW arithmetic. These are
software arithmetic checks, not scientific FOLD training or performance results.

Snapshot tensors are cloned and detached without changing the live model/optimizer.
Nonempty tensors must not alias the live state; zero-size pointers are not falsely
interpreted as shared payload. Hashes before/after snapshot creation must match;
the live model/optimizer hashes immediately before update1201 must equal the1200
receipt. The stored1200 snapshot is rechecked after all2400 updates. Corrupted
continuation receipts and nonfinite outputs fail closed before subsequent work.

The accepted C319 trained_readout implementation was reread: it installs removable
forward hooks and uses closure-local temporary representations, not registered
parameters/buffers. Thus snapshotting during its context does not intentionally
add readout state keys or replace trainable weights. It clears per-forward state and
restores hook inventories. Native gradient/readout parity is still checked during
the real preflight; source review does not replace that native execution.

## Parent writer, loader and dependency audit

C328 writes fold-c328-science-v1, not the earlier diagnostic schema. Its scientific
FAIL is paired with diagnostic_execution_valid=true and candidate_gate=false. The
child explicitly accepts this exact valid-negative evidence rather than requiring
capability PASS or accidentally accepting an incomplete execution.

The exact C328 primary/envelope hashes, execution HEAD, manifest/work, full5722
receipt, saved semantic completion and1561 final rereads are bound. Both parent
records must carry identical complete826-source/1561-input maps. C328 has8 science
outputs plus primary/envelope, so the immediate-parent addition is10 files.

The child reads C328 dataset/original/interior prompts, validates canonical data and
prompt semantics and calls unchanged C328.semantic_recheck(out,data,old,new,cx,read)
under no_neural. It validates all older protected bytes but does not recursively
rerun ancestor semantic bodies or invoke a parent model forward.

Direct/lazy dependencies remain in the inherited maps: C328 executor/benchmark,
C326 allocator and token selection, C325 training tables, C324 evaluator/scorers,
C319 readout hooks, C308 optimizer, native recovery helpers and inherited tests.
The new executor verifies its direct bootstrap blobs before executing their loader.
Helper tuple ordering is e328,e327,e326,legacy,r4,r6; the child passes the expected
arguments into the unchanged C328 suite. Native runtime is obtained from e326.
No smaller protection map or post-hoc pin replacement is allowed.

Protection arithmetic:832 sources=826+6;1577 inputs=1561+10+6. A real temporary-file
fixture exercises complete union construction and detects changed inherited bytes.
Its parent records and lease callbacks are explicitly synthetic, not the user's
actual protected files or native Windows locks. Real execution retains unchanged
R4 read leases through all phases and independently rereads all1577 files at end.

## Work accounting, saved outputs and gate semantics

Five fresh2400-update trajectories provide ten checkpoints, not ten independent
fits. Total training is12000 updates/576000 rows. Each of ten evaluation model
instances loads a saved checkpoint, evaluates it, reloads it and repeats evaluation:
20 state loads,20*171 evaluation/replay forwards. Total15420 forwards/904320 rows/
61680 core forwards. Scientific bundle write/read counts are1/1. Preflight/tests/
parent and saved verification have separate work scopes.

The production run_science orchestration was exercised with synthetic scientific
callbacks and real safe Torch/file writes:all five fits precede all20 evaluations,
all ten ordered seed/arm records exist, and all eight registered outputs are written.
This checks control flow and writer shape, not native FOLD quality. Saved semantics
uses the new fold-c329-evaluations-v1 trajectory/record schema and the actual bundle
loader; altered saved validation content is rejected. State hashes bind each record
to its1200/2400 receipt and saved tensor state. Full cells use unchanged scorers.

The gate retains strict interior answer AND pair improvement, nonnegative pooled
original2..6 answer AND pair gains, and complete local interior/original gates in
ALL5 seeds. Masked/order thresholds are unchanged. Every requirement, count
conservation, missing/duplicate/reordered seed and boolean-as-integer error is tested.
A valid negative summary is preserved as FAIL; it is not converted into an execution
error. Control saturation is explicitly discussed in the preregistration rather than
silently permitting ties. Paired checkpoints and unequal budgets are explicit.

Saved reconstruction validates stored traces, snapshot hashes and checkpoints; it
does not independently replay all2400 historical optimizer updates. Fresh verification
rechecks every protected source/input/output byte and size, complete maps, parent
identity, full regression receipt, work and gate bindings without refitting.

## Regression, failure control and launcher

The real own unittest loader contains48 tests. Additive suite logic combines it
with an explicitly synthetic5722-ID inherited inventory, verifies total5770 and
uniqueness, and rejects duplicates. Module inventory expects218. This is NOT an
execution of all5770 historical tests. There is only the inherited exact C204
mutable-ACTIVE exclusion; no new exclusions, skips or cached regression successes.
The actual full suite will run unmodified in a separate ordinary interpreter.

Actual scientific_worker control flow was tested with synthetic parent/model/lock
callbacks:preflight -> tests -> fitting -> saved reconstruction -> final reread ->
lease release -> summary/envelope. Valid negative output is preserved; regression
failure never calls fitting. Preflight failure prevents regression, saved mismatch
prevents finalization, and modified artifacts fail before an integrity claim.

Real temporary Git guard, UTF8 JSON, LF/CRLF byte verification, exclusive file writes,
subprocess invalid-CLI rejection and production no-auto-retry controller were tested.
Source assertions were checked against their exact functions; the AST inspection of
optimize counts its own optimizer creation and manual_seed calls, not those of a
caller/callee. Count contracts use real loaders/IDs, not source-number literals.

The unchanged invoke_active_v2 dispatcher derives C329 only from the unique Formal
state entry and parses the chosen launcher. The user command parses the dispatcher;
the C329 launcher parses itself and run_c329 before creating a log. Branch, ExpectedHead,
tracked tree, ACTIVE and dependency failures return SKIPPED before publication.
run_c329 uses .venv-py31315, explicit UTF8 output and the correct executor/arguments.
Local output runs/c329-budget-<id> and console publication c329/latest.* agree.
Scientific FAIL with valid execution is negative evidence; only technical failures
require same-C329 recovery. Publication failure alone never authorizes refitting.

## Approval boundary

No native Windows, real-parent FOLD trajectory or full5770 historical-regression
success is claimed by this author-side review. Those are mandatory in the user's
registered execution. The next activation is documentation-only and does not alter
any of the six reviewed protected files. Gate F remains NOT PASSED; no production
adoption, unseen-template transfer, capacity limit or optimal-budget conclusion.
C330 remains NOT REGISTERED.
