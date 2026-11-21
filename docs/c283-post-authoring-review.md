# C283 committed-byte post-authoring review

Review target:cc4d71ee7edc4ae917d3535f1cd31c809da066ee.
Acceptance base:b597180933fcc464395ad62cc0e915e01c796871.
post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Authoritative Windows parent-artifact/full-regression/scientific execution remains PENDING.

## Identity and executed checks

GitHub compare shows exactly six added OWN files relative to C282 acceptance;no accepted parent
source,test,preregistration,log or protected dispatcher was changed. All six committed files were
fetched after commit. Their Git blob identities match the locally tested UTF-8 bytes6/6:

|path|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c283_frozen_four_character_transfer.py|2c204bbb5e8b53db5c2c1cd5202a0fcc5d4aa4a0|21648|
|tests_lm/test_v05_c283_frozen_four_character_transfer.py|0c87e6dde5059e137f6b21246b693b6c0bc94a3f|19168|
|tools/run_c283.ps1|3192d104549de5f6bb3e1fdf6eb37f53eb57bb60|5911|
|tools/invoke_c283.ps1|5206547da4b22ede9f6bc03ab8def64f077feeda|4346|
|docs/experiment-ledger-addendum-c283-preregistration.md|3da7bec68a46988daef99880843c6c8bb6b58848|6820|
|docs/v5b-frozen-four-character-transfer-v0.1.md|b86d6f8f6bae8fab873eb014a0969e6e979da5c7|1726|

Reviewer environment:Linux,Python3.13.5,PyTorch2.10.0+cpu.
After remote identity comparison,the exact source/tests passed all32 own tests;final run1.089s,OK.
Parent artifacts,scorers,Git context and full-model probe are mocked in relevant unit fixtures.
An elementary neural fixture exercises the actual quad evaluation loop and27 forwards/2592 rows.
This is NOT a real C283 result and NOT authoritative Windows execution.

Both Python files compile;all three embedded runner Python blocks compile. Recursive symbol-table
checks find zero unresolved global-name bindings. UTF-8 files contain no NUL bytes. The manifest
seal is computed from manifest(),not guessed. Tests execute valid/malformed/mismatched seals.
No global string replacement of a sentinel guard was used.
Manifest SHA256:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4.
Quad dataset SHA256:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.

Tests cover four-character names,exact prefix/suffix patterns,mask views,the canonical logical-data
hash,no old-prompt overlap,Japanese43-byte bound,no truncation,profile adapter tensor identity and
nonmutation,all-seed inclusion,known-error anchor replay,freeze/state/workload checks,control/candidate
gate separation,nine independent parent hashes,parent dispatch/neural blocking,missing parent pin,
actual run-function checkpoint dispatch and output roundtrip,no overwrite,artifact tampering,
CLI argument order and synthetic3982-test/exact3981-filter construction.
The new test inventory does not inspect mutable ACTIVE state;its seal reference is immutable prereg.

## Parent and scorer contracts

C282.verify_artifacts signature is outdir,eight-summary-list,execution_HEAD. C283 passes exactly
those and pins C282 source fdf35a6c0c18e0c0da4b1f592cef73be156de481. Parent result is an accepted
FAIL with mixed4/control0 whole-state passes,not a guessed PASS prerequisite. The actual C282 writer
stores raw_two,raw_triple,final_sha256,seed and arm in fold-c282-mixed-length-eval-v1. The model
bundle is loaded through C282.load_bundle,not a similarly named older loader.

C282.make_models returns the actual C278 all-token model for both arms;C283 strictly loads each
saved state,sets eval/requires_grad(False),checks its fingerprint and preserves all10 states.
Anchor replay reuses C270.replay_old and C280.replay_triple on their schema-independent raw-output
contracts. No C282 schedule/analyze function is incorrectly dispatched on C283 records.

The inspected C270.score implementation uses raw logits and canonical logical rows;it does not
render identifiers. A reversible three-profile adapter changes labels only and relabels cells,
two_order and totals. Runtime Validate uses the actual scorer with perfect synthetic logits to
check72 answer cells,36 order cells and864 correct normal rows. Local unit fixtures do not claim
this actual inherited scorer was executed in the review environment.

The child directly imports C282 and obtains its already-pinned context helpers. Expected inherited
dependency-union59 includes C283;source pins538+6=544;protected inputs950+8+6=964.
All source/input guards remain;no accepted file is changed to evade protection.

## Workload, launcher and remaining gates

Per model:54 original-task anchor+27 new-task+54 original-task restore=135 forwards,
12960 row presentations and540 core calls. Ten models:1350/129600/5400.
One existing checkpoint bundle load,10 model-state loads,zero optimizer steps/updated checkpoints.
The saved evaluation tensor archive is not a checkpoint;raw payload265420800 bytes is registered.
Every four-character normal prompt is new to both arms;TRAIN/HOLDOUT denotes inherited value splits.

Precheck gets9 paths,C282 through C274. Postcheck gets output_dir,9 paths,ExpectedHead:
sys.argv[1],sys.argv[2:11],sys.argv[11]. Embedded blocks/CLI phase order were tested.
Launcher checks host/branch/tracked tree/ExpectedHead/unique C283 ACTIVE before science/publish.
Dispatcher remains tools/invoke_active_v2.ps1. ParseFile on dispatcher is required in user command;
dispatcher parses selected launcher and launcher parses runner before invocation.
No PowerShell executable is available in the review environment;native ParseFile was NOT run here.

Actual parent artifact verification,real tokenizer/scorer/model construction,full focused3981,
native PowerShell parsing and all10 frozen scientific probes remain user-local runtime gates.
Validate failures skip scientific logging/publication. Scientific integrity failures retry SAME C283.
A four-character candidate PASS does not repair C282 or promote Gate F. Diversity versus maximum
training length remains a stated confound. C284 is not registered.
