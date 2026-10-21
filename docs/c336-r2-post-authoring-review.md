# C336 R2 post-authoring review

Date:2026-10-21 Japan time.
post_authoring_review = PASS
Committed source/recovery review target:2072b613055093e600fdafe4807de3fa77f5c2ad.
Invalid publication base:3ab32fc78d924914b07141d4a009de3c8e39fcbe.
This approves the authoring repair,not Windows/full6090 success or a C336 result.
Use the subsequent documentation-only final recovery HEAD supplied to the user.

## Committed-byte review and scope

After source publication,the complete modified benchmark was retrieved at the exact
commit in ranges1..145 and146..261;the complete test file in ranges1..185,186..350,
351..516. The full180-line amended preregistration and110-line recovery record were
reread. Returned Git blobs match independently hashed local tested bytes:

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c336_saved_query_order_patterns.py|d1862be34e673ee6da433be711bcf2b8b70645e7|
|tests_lm/test_v05_c336_saved_query_order_patterns.py|317e71eca0964dce81b49e147b82cc5511f07af2|
|docs/experiment-ledger-addendum-c336-preregistration.md|bb43353d522bbd659fecd42e9f63049f0e5b9b1b|

Unchanged R1 executor blob2d35c49a0adf570458c7232cf44e373e7e2e54c4 remains byte-identical,
including max_files=s.INPUT_COUNT. Launcher da097874586a3369494f3a81460c1752ab48ac46
is unchanged. The source compare shows only the benchmark's two guard corrections,
own test strengthening,explicit preregistration correction,recovery/handoff docs and
exact attempt/history copies. No accepted historical source,test,contract,runner,
launcher or dispatcher changed. AST comparison finds only logical_groups and classify
changed among benchmark functions;the manifest,scorers,analysis/writers are unchanged.

## Executed post-reread validation

Normal own suite32/32PASS,failures/errors/skips0,6.349seconds.
CP932-default-text-open emulation32/32PASS,failures/errors/skips0,6.860seconds.
Each ran in a separate Python invocation after remote-source reread. CP932 emulation
wraps builtins.open and io.open only for unspecified/locale TEXT encodings;explicit
UTF8 and binary opens remain unchanged. It is not a native Windows locale execution.
All three C336 Python modules compile/import. Modified protected files decodeUTF8,
contain no NUL/trailing whitespace. Recursive LOAD_GLOBAL audit:199function/method/
nested code objects;undefined globals0. Actual own loader32IDs match the original
method names/order;digest96ce8e07f180137d2035601083aade23244cac87e83f23dfae3eff23940a2b73.
Scientific manifest self-hash unchanged and valid:
e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
Canonical dataset reconstruction hash verified:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

Environment:LinuxPython3.13.5/PyTorch2.10.0+cpu,targeted reconstructed source tree,
not a complete repository checkout. Two historical dependencies use verbatim source
EXTRACTS with required constants/helpers:C267 dataset/validate_data/render and C324
LockedHashes. These author-only extracts are NOT full historical modules,NOT native
Windows locks,and are never committed. User-side tests import the full accepted
modules;both already belong to the inherited protected dependency set.
No actual C335 trained predictions/checkpoints,full6090historical test run,native
Windows sharing semantics or PowerShell AST execution is claimed. No environment
installation or CI. Existing mandatory user-side AST preflight remains unchanged.

## Schema/writer audit and coverage

Actual accepted C267 writer source5a167f078ab5b3aa8052e7995d004a25ca25fc0f was read:
three integer entity subsets,all12ordered distinct value pairs from0..3,both languages,
both fact orders and both queries. HOLDOUT uses(0,2),(1,3),(2,0),(3,1),TRAIN the other8.
Targets are48+queried value. This same canonical DATA_SHA is retained by C304/C329.
The diagnosis must therefore accept two observed target bytes from48..51,not only48/49.

The fix retains distinctness,integer-not-bool,range,target/query binding,all four
query/order slots,language coverage and row positions. It does not rewrite source
rows or choose predictions. Full256-way argmax remains. Any predicted value not in
this particular observed pair remains other_class,even another digit from0..3.
The existing two-observed-value taxonomy and all parent-count reconciliation remain.
The initial unaccepted textual binary assumption is explicitly corrected,with its
original archived. No accepted result is retroactively reinterpreted.

The test fixture now independently reproduces ALL canonical rows,IDs and order and
must equal the frozen SHA;test02 also compares actual writer output/validator. It
cannot silently substitute the previous invented binary-only entity/value fixture.
All production analysis,loader,writer and saved-reconstruction tests now consume
these exact logical rows. Synthetic logits and ancestor/scorer callbacks are still
explicitly synthetic;this is not the user's scientific outcome. The complete fixture
covers12960quads,6480matched changes,720strata and30parent contrast reconciliations.

Retain old0/1 tests and extend to all12ordered target pairs*16within-pair response
patterns with an independent property-based category reference. Also test third-digit
other_class,observed-value lock,row-order invariance,duplicate/out-of-range/bool/float
values and targets. Prior all256-class argmax,nonfinite,missing-state,policy/replay,
reconciliation,tamper,lock-capacity and worker/fresh-verifier tests are retained.

Independent in-memory negative controls restored EACH old guard separately,then
called actual run_diagnostic on a canonical dataset file and synthetic tensor archive.
Old logical_groups fails with logical row semantics;old classify fails with two
distinct target values. Both fail before any diagnostic output is written. These
expected exceptions are negative-control successes,not ordinary test failures.
Functions were restored;all file Git blobs and manifest were checked afterward.

## Failure identity, invariants and approval

Attempt02 execution5029fbbad2209f462af8939c0e77f56a5a63be5e;
publication3ab32fc78d924914b07141d4a009de3c8e39fcbe,sole parent matching execution.
Native parent/capacity and6090tests/226modules passed;diagnosis then failed before
completion/final rereads/fresh verification. run_execution_valid=false. Its existing
6090receipt cannot be reused under the repaired source. The later stale C335 command
executed nothing and is not a third invalid attempt. Exact attempt02 logs are archived.

Same32own IDs/6090full tests/226modules/877sources/4360inputs;no new exclusions or skips.
All10C335states,all profiles/languages/splits,12960quads/6480pairedquads/51840answers,
720strata and all30parent contrasts remain fixed. No new inference/training/update.
R1 capacity4360,all native held leases,initial independent hashes,4360final uncached
rereads,full parent proofs,output binding and independent fresh verifier remain.
C335 stays ACCEPTED VALID NEGATIVE;Gate F NOT PASSED;C337 NOT REGISTERED.

The final commit changes only review and handoff documentation. Registered native
execution must still pass all6090tests,real diagnostic data and final verification.
Any technical failure stays SAME C336,no automatic retry or threshold relaxation.
No C335 retraining,publication-HEAD bypass,package installation,paidservice,CI,
accepted-source mutation or artifact deletion.
