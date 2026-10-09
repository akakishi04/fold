# C317 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review and executed local software tests,NOT actual FOLD science.
Review target:207696e82df54d35ac53cd75fed7496685c687dd.
Acceptance base:590edfc7b00fadf894cc5ce629294259843de5de.

## Committed bytes and change scope

All six OWN files were fetched after commit from the immutable review target and reread.
Source351lines and tests406lines were covered by complete consecutive ranges;the other four
files were fetched in full. Returned whole-file Git blob IDs match independently hashed local
bytes6/6. After the post-match test runs,all six hashes were independently checked again:

- fold_lm/v05_benchmarks/model_c317_query_endpoint_probe.py:7ef1736df78b5dd883a331c434f5f82f1eb8ab92;24700bytes.
- tests_lm/test_v05_c317_query_endpoint_probe.py:da8c0af48329652ec9357aa0bc50d81c33e52651;28772bytes.
- tools/run_c317.ps1:f2d184866b82a74c1311a611e7372de94f8349d0;4526bytes.
- tools/invoke_c317.ps1:be2aa8673428c0c825c8b7f305d2b9ca4f2b4037;7700bytes.
- docs/experiment-ledger-addendum-c317-preregistration.md:58873cbc66d780460388d0c8d5a1fe609adeaaf1;7842bytes.
- docs/v5b-query-endpoint-probe-v0.1.md:a880790bf7661cc769ed11cbf0ba81aa033fb9bd;1160bytes.

Acceptance-to-authoring remote comparison contains exactly these six additions. No accepted
source,test,log,preregistration or dispatcher was changed. Activation must preserve OWN6.

## Executed checks after all six remote/local matches

Normal:python -u -m unittest tests_lm.test_v05_c317_query_endpoint_probe -v
Ran32 tests in10.727s;OK,zero failures/errors,process exit0.

Complete same module under io.text_encoding default-CP932 emulation:
Ran32 tests in9.874s;OK,zero failures/errors,process exit0. Patch covers module import,setup,
all tests and teardown,with only omitted encoding mapped to cp932. Both were uninterrupted
full-suite executions. Earlier12.581s pre-commit run is NOT the post-authoring review evidence.
Terminal cleanup TERM-not-set messages after OK did not change successful process/test results.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No PowerShell installed locally.
Default-encoding emulation is not full Windows or console emulation.

All six files decode as UTF8 and have no NUL. Both new Python files and all three embedded
runner Python blocks compile. Recursive symtable/import-binding audit reports0 unresolved
globals after allowing module bindings,builtins and standard module globals. Manifest seal:
10f2e095d09f6ffeb424b2d91c0215aabf8739caace720c4f6662cb4f73a1d10.
43 launcher paths are ordered C316..C274. Postcheck paths=sys.argv[2:45],head[45],argc46.
Own32/modules202/loaded5150/focused5149;sole inherited exact C204 exclusion unchanged.

## Actual scientific path and behavioral coverage

Scientific code uses the actual C304 LengthReadout forward,not a reimplemented model forward.
Its source was inspected at the accepted blob:read.query is called first on the query-span
mean,then on the final query-byte local representation. Shared query weights transform both;
the two attention readouts are averaged equally before the original residual/norm/classifier.
C317 installs child-owned hooks without changing any parent method,global or parameter.

Every model call records tokens/span and the masked pre-core local encoder representation.
The first query input must exactly equal the native span mean;the second must exactly equal
local[rows,last]. Only the second call in first_byte mode receives local[rows,first] instead.
The other computation and trained weights remain unchanged. CPUfloat64/shape/finiteness,
one encoder capture,two query calls and per-pass counts are enforced. Original modes use the
same observers but return native query inputs unchanged. No targets or expected answers enter
these hooks. First byte is literal,not a whole Unicode character or unique character ID.

Tests execute the exact accepted C304 forward/span ASTs on controlled encoder/core/reader
components. An independently calculated first-anchor attention formula matches intervention
outputs while differing from native outputs. Pass-through observer output is bit-identical.
English one-byte and masked one-byte inputs are unchanged;Japanese one-character queries have
three bytes and are not incorrectly treated as degenerate. Wrong query-input provenance and
forward exceptions are rejected with complete hook cleanup. Existing hooks,repeated calls,
frozen/no-grad enforcement,no optimizer and no parameter mutation are tested.

Actual child infer_one plus the extracted accepted C315 evaluator executes three full144-call
passes on a controlled model,checking13824rows/576core calls per pass and8928rows with distinct
endpoints. It verifies strict checkpoint hashes,original output replay,one-byte controls and
registry restoration. The actual runtime_preflight path is tested for both parent arms on
bilingual length1/6 examples. This is not an evaluation of the user's trained FOLD checkpoints.

The synthetic cohort checks20 scored results,200 partitions,40 single-length diagnostics,
640 local paired groups and46080 normal paired rows. Independent examples distinguish rescues,
regressions and wrong-to-wrong flips. Even if every changed-mode capability gate fails,the
child may only pass diagnostic integrity;no quality promotion is inferred. Original gate flags
and replay/probe receipts are protected. Incomplete cohorts and changed receipts are rejected.

Each of43 individual parent hash failures occurs before verifier dispatch. Actual precheck
exercises748/1407 temporary source/input fixtures and rejects a missing helper. Production run
fixtures verify one parent-bundle load,ten inference dispatches and only an evaluation tensor
archive write,no model checkpoint. Numerical reconstruction rejects byte tampering and semantic
tampering even after descriptors are resealed. Wrong HEAD and run-directory overwrite fail.
Semantic regression tests construct5150 TestCase IDs,retain the exact5149 IDs and reject duplicate
IDs;they do NOT execute the real inherited regression suite.

Local C304 and C315 support files contain fetched exact function slices,not full modules or a
repository clone,and are NOT committed. Tests extract the same functions from full accepted
sources on the user's checkout. Synthetic logits and substitute Git/parent/scorer interfaces
are software controls,not actual FOLD capabilities or evidence from the real43 parent archives.

## Parent writer/loader and dependency contract

C316 run/load_bundle/verify_artifacts were reread at the immutable review ref. Model schema:
fold-c316-single-replication-models-v1;final output schema:fold-c316-single-replication-eval-v1.
The model bundle stores ten ordered states. Final raw1..6 logits are from the learned state,
with strict replay already checked. C317 does not interpret a diagnostic report as a model.
It verifies43 ordered hashes before C316.verify_artifacts with42 ancestors and the exact
accepted execution HEAD. Exact parent summary seals all7 descriptors. Require validFAIL,
ten original per-state flags,4/4 six counts and matched/replayed metadata. Read canonical
C316 dataset/prompts and its final-logit archive. Actual C316.make_models/load_bundle are used,
strict-load each corresponding state once and confirm its full fingerprint against the record.

Sole direct repository import:C316. Through its context the child calls already protected
C315 evaluator/raw validator/replayer,C304 span/scorer,C287 normalizer and original backend.
Retain742 inherited source pins/1393 inputs plus C315.PINNED/C304.PINNED and actual repository-local
helper/factory-language coverage. OWN6+8parentfiles yields748sources/1407inputs. No accepted
source edits,new exclusions or source-protection waiver. Actual runtime pin checks remain mandatory.

## Work,interpretation and runtime boundary

All ten states retained;three fixed passes original_before/first_byte/original_after. Scientific
4320forwards,414720rows,17280core calls;10strict state loads,one parent bundle read,training0,
new model checkpoint0,network0. Eight discarded operational probe forwards,parent reconstruction
and software tests are separate costs. Raw logits849346560bytes exclude serialization overhead
and are not peak-memory accounting. All arrays stay local/ignored;console carries aggregates.

Original before/after must reproduce all parent views<=1e-9 and exact argmax. Query-blind outputs
and all English-length1 views must be bit-identical between endpoints. Every final output is
retained;there is no best-of selection. This is an untrained inference intervention and tests
sensitivity,not whether a first-anchor architecture learns better. It neither proves a training
mechanism nor promotes Gate F. C316's negative and all prior verdicts remain unchanged.

The unchanged invoke_active_v2.ps1 was reread:it parses itself,extracts the unique ACTIVE from
Formal state,pins the legacy dispatcher and parses the selected launcher. That launcher parses
the runner and returns before science/publication on Validate failure. No dispatcher edit.

Not executed here:Windows PowerShell ParseFile,the user's43 real parent archives/protected bytes,
the actual5149 inherited regressions,or inference on the ten real C316 checkpoints. All remain
mandatory local Validate/Execute gates. This review authorizes only the guarded launcher.
Any integrity or restoration failure repairs SAME C317 with the scientific conditions fixed.
C318 remains unregistered until C317 formal judgment.
