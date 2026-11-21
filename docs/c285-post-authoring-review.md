# C285 committed-byte post-authoring review

Review target:8b2b1030fea7166bdd86537290f5b874f6c66266.
Acceptance base:8b16da05d3669e86ee6b9d323c6cb9eeec4766bf.
post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Authoritative Windows parent-artifact/full-regression/runtime gate:PENDING.

## Remote bytes and executed tests

The compare from acceptance to review target contains exactly six new OWN files. No accepted
source,test,preregistration,existing log or protected dispatcher was changed. All six committed
files were fetched again after commit; source/test were read in contiguous ranges. Each returned
Git blob SHA matches SHA1(blob-header + locally tested bytes),6/6.

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c285_saved_length_transfer_audit.py|383b4156351c601a26b1f58c2ccdea59206f8538|19210|
|tests_lm/test_v05_c285_saved_length_transfer_audit.py|0e399d2dd89d7a30c042fe270674a95900f9ad3d|16199|
|tools/run_c285.ps1|2328c1f89c07ebae1b1e1a486170d9209080d7ef|4778|
|tools/invoke_c285.ps1|63a034a11fefe523aaebdfaaca279c49cfae6fa7|4545|
|docs/experiment-ledger-addendum-c285-preregistration.md|54e0639617adaa91a8980f84fd2ed63cc6f48cbd|5712|
|docs/v5b-saved-length-transfer-audit-v0.1.md|95f50db56002a6f65b047f211e2abda7843a9adc|1846|

Reviewer environment:Linux/Python3.13.5/PyTorch2.10.0+cpu.
After all remote identity comparisons:Ran32 tests in1.645s;OK.
Both Python files and all three embedded runner Python blocks compile. Recursive symbol-table
inspection reports zero unresolved global names. All OWN bytes are UTF-8 without NUL.
The manifest was computed from manifest();only its assignment was sealed. The actual valid,
malformed and mismatched seal checks were exercised,not merely source-string asserted.
Manifest SHA256:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c.

Fixtures replace parent archives and Git context. They cover complete3240-record reconstruction,
missing/duplicate/unknown cells,nonfinite and boolean metrics,integer denominators,correct counts,
query-pair/collapse consistency,task flags,deterministic cell-order normalization,arm rescue/new
failure counts,longitudinal triple-to-quad co-failure and introduced failures,net-zero turnover,
seed additivity,mask-only classification,all eleven independent parent hashes,correct loader
arguments,blocked Module/state-load/checkpoint-write operations,missing source pins,zero-workload
flags,actual run call order,JSON persistence/no overwrite and hash plus semantic tamper detection.
The suite test constructs a synthetic4046-test suite and checks exactly4045 retained IDs; it does
NOT claim the real inherited4045-test suite ran in the reviewer environment.

## Parent contract and scientific path

The live C284 source was read at acceptance ref and matches cc560842a4f2b4e9b0ba6ae9481c42e2f3bb1df1.
C284.analyze emits metrics={seed,arm,two_char,triple,quad}; there is no required top-level passed
in a metric. Its separate seed_results.passed is quad_pass,not all_tasks_pass. C285 models this
actual distinction and checks all ten published parent task-flag tuples.
C284.verify_artifacts(output_dir,ten ancestor summary paths,execution_HEAD) owns reconstruction of
fold-c284-max-length-eval-v1 and dispatch to C267/C270/C283 scorers. C285 passes those arguments
exactly and consumes returned scalar metric records. It does not dispatch an older analysis helper
onto the C284 schema and never loads a model/checkpoint state.

C285 uses all three task grids,72 answer cells+36 two-order cells per state/task. Profile index
mapping joins tripled/quadrupled,prefix2/prefix3,suffix2/suffix3 without changing model/scorer inputs.
Each pair also matches kind,split,language,entity pair and fact order. The registered full views
contain540 matched records:360 answer and180 two-order. All10 states remain present.
Exact criteria and their denominators remain those of the parent; margin signs reproduce PASS.
Ablated correct counts are normal accuracy minus drop,checked as discrete ratios.
Matched-cell co-failure is explicitly NOT treated as identical-row failure or causal inheritance.

Only the pinned C284 repository module is directly imported. Its context and verifier reuse inherited
source-pinned helpers; no new repository dependency is bypassed. Dependency union extends through
C284 plus OWN source. Expected source550+6=556;protected976+9 new parent inputs+6 OWN=991;
inherited dependency union61. Real path/hash/cardinality checks remain the local runtime gate.

## Launcher, lifecycle and boundaries

Eleven ordered summaries:C284,C283,C282,C281,C280,C279,C278,C277,C276,C275,C274.
Postcheck argv is output[1],summaries[2:13],HEAD[13],total14. Embedded Python blocks were compiled
and their CLI order tested. Launcher verifies branch,tracked tree,ExpectedHead and unique C285 ACTIVE
before science/logging. It parses the runner; active dispatcher and selected launcher parsing are
required by the standard entry path. No PowerShell executable is installed here,so native ParseFile
is NOT claimed executed. User-local PowerShell parsing remains mandatory before science.

Validate failure skips scientific execution and log publication. Execute failure publishes diagnostic
evidence and retries SAME C285. Diagnostic PASS requires complete exact reconstruction,not favorable
results. No training,neural model forward,state load,new checkpoint or network call in C285 science.
Authoring/regression work is separate. No mutable ACTIVE assertion is added to historical tests.

Activation changes only this review and the authoritative handoff. All six reviewed OWN blobs stay
unchanged. Actual parent archives,source/input pins,full4045 regression,PowerShell parsing and real
saved-result reconstruction are still pending authoritative Windows execution. No scientific C285
result,Gate F promotion or C286 registration is asserted by this review.
