# C288 committed-byte post-authoring review

Review target:072c3d66b205d7438254367f0825d53e2f0c5406.
Acceptance base:6acdfd588cca0cba3ede448df8e0e066a391fdef.
post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Authoritative Windows runtime gate:PENDING.

## Mutation boundary and byte identity

GitHub compare from acceptance to review target reports exactly6 added OWN files.
No accepted source,test,preregistration,dispatcher or published log was changed by C288 authoring.
All6 committed files were fetched back. Benchmark/test were read in complete successive ranges;
runner,launcher,preregistration and design were read completely. Returned whole-file Git blob
identities match complete local tested UTF-8 bytes6/6:

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c288_query_pair_assignment_loss.py|f7f9c73565828e23533efd188f25009e5e4b3d50|27396|
|tests_lm/test_v05_c288_query_pair_assignment_loss.py|f28c82400dea27f52c54f1cdd287739061591a5b|27189|
|tools/run_c288.ps1|e71897d12b5e4f2958c0462a6f57efb9ee44ffe5|5337|
|tools/invoke_c288.ps1|f393e5485c27d70074fb869e27c859444b22f88f|4839|
|docs/experiment-ledger-addendum-c288-preregistration.md|11db2e2bdaa25f0cdf6f10c34ddb6c948e21631c|8213|
|docs/v5b-query-pair-assignment-loss-v0.1.md|0ee11efc56105771e3739a9ace9e875b23381f51|1775|

No recovery change was required during this review. All six identities must stay unchanged during
activation. Only the review document and authoritative handoff should change at activation.

## Executed local checks

Environment:Linux/Python3.13.5/PyTorch2.10.0+cpu.
Initial own40 run:40 tests in4.641s;OK.
Post-fetch identity-matched own40 rerun:40 tests in4.577s;OK.
Both Python files and all3 embedded runner Python blocks compile. NUL bytes0.
A symbol-table recursive free-global/import-binding audit found unresolved global names0 in both
new Python files. Manifest digest from manifest() equals
44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5.
Malformed/mismatched seals are behaviorally rejected;there was no global placeholder replacement.

The tests execute real800-update AdamW fits on a small query-conditioned toy model for BOTH arms.
AppliedLR is instrumented at optimizer.step and remains.005 for all800 updates. The tests check
paired batches,per-length exposure,target alignment,finite CE/pair/total traces,and reconstruction
of total=CE+weight*pair. These are authoring tests,not actual FOLD C288 scientific training.

Objective tests verify closed-form zero-logit loss,assignment-swap direction,per-row offset
invariance,query-independent scores giving zero assignment difference,autograd versus numerical
finite differences,exact control CE value/gradient,and expected target/competitor gradient signs.
A counterexample confirms a favorable summed pair margin can coexist with a wrong individual
answer;the auxiliary objective never substitutes for independent CE or fixed evaluation gates.

Other tests exercise invalid shapes/precision/targets/nonfinite values,complete epochs and query
pairs,independent matched initial storage,train/freeze/evaluate ordering,all3 task summaries and60
final partitions,objective-trace tampering,primary/descriptive distinction,all14 parent hashes and
correct dispatch,forbidden neural/state/write operations,temporary-file source/input coverage,
missing dependency rejection,actual synthetic suite construction with exact exclusion and duplicate
ID rejection,production run/save/load/replay order,no overwrite,artifact hash and semantic tampering,
checkpoint schema,CLI argument order,immutable inventory and repository guards.

## Scientific and parent semantic audit

C287 is the direct repository import and a saved-diagnostic parent,not a checkpoint source.
context() resolves C287 -> C286 -> C284 evaluation/replay,C283 transfer,C282 training tables.
Parent verifier receives14 summary paths as parent directory plus13 ancestor paths and the accepted
C287 execution HEAD. All3 C287 artifact hashes/sizes and the direct source blob are fixed.
Parent results are required to reproduce the actual4 fitted_train/0 seen_holdout/1 quad/5 none
partitions. Parent Module calls,load_state_dict and torch.save are blocked.

C284.evaluate/replay_one consume the task-keyed raw={two_char,triple,quad} schema and do not bind new
experiment identities. C288 owns its analyze/schedule/objective validators. C287.normalize_task
and partition are identity-independent normalization helpers and preserve original thresholds,
cell denominators and row-weighted NLL. The old identity-bound C287.analyze is not called on C288.
C288 final output includes TRAIN/HOLDOUT partitions immediately,not a newly selected follow-up grid.

Both arms share model capacity,initial state,logical batches,rendering schedule,constantLR and800
updates. Only the optimized loss differs. TRAIN labels enter objective(),never model.forward or
inference. The candidate adds a fixed.25-weight margin1 correct-versus-swapped assignment loss.
CE is retained;control differentiates exact CE. No extra model forward or example is introduced,
but auxiliary arithmetic/autograd cost is real. NominalLR equality does not equal gradient-scale
matching. All5 fresh seed pairs and every unfavorable outcome are retained.

## Counts,runner and dependency coverage

Source574=568 inherited+6 OWN. Protected1026=1016 inherited+4 new parent inputs+6 OWN.
Dependency union64 includes inherited reachable scientific helpers and the new benchmark. Direct
C287 blob is checked explicitly;temporary-file coverage and missing-pin failure tests pass.
Own40;modules173;loaded4158;focused4157. The sole exact inherited C204 exclusion is unchanged.
The production suite loader counts unique actual test IDs;numeric source-string counts are not used.

Runner CLI uses14 summaries. Postcheck reads sys.argv[2:16],head=sys.argv[16],argc17.
Launcher has14 ordered exact parent paths,C288 ACTIVE guard,ExpectedHead/branch/clean-tree checks,
Validate before Execute,and publication only after scientific logging begins. Validate failure
skips science and publisher. Explicit UTF-8 source/doc reads are used in new tests.
The unchanged invoke_active_v2.ps1 was read:it parses itself and the selected experiment launcher;
C288 launcher parses its runner. The user command must also ParseFile the entry before invocation.

## Limits and activation

Fixture checks mock parent archives,Git and inherited FOLD models/scorers in several paths.
No actual C288 ten-model training,result,full4157 regression or real parent-artifact replay is claimed.
PowerShell is unavailable in the review container,so ParseFile remains an enforced user-local gate,
not an executed reviewer check. Real TRAIN tables,paired initial models,real parent provenance,
full regression and scientific training remain authoritative Windows Validate/Execute gates.

Activate only this reviewed OWN6 set. Any subsequent integrity failure retries SAME C288;no result-
dependent loss coefficient,margin,seed,budget or gate edits. Gate F remains NOT PASSED and C289
is not registered before C288 formal judgment.
