# C297 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review and local behavioral fixtures,not authoritative FOLD science.
Review target:cd513a561ed52cca9571a959bb58c789787d9430.
Acceptance base:8e76dbbaa2a58658b80f60e2d90ee9acbe23f8b8.

## Post-commit byte verification

All six OWN files were fetched at the immutable authoring commit after creation. Python files
were reread in consecutive ranges covering their complete contents;the other files were fetched
in full. The returned whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c297_init_order_grid.py:49497d433c6302cd2a65635564f254edbf169104;24320 bytes.
- tests_lm/test_v05_c297_init_order_grid.py:dd84c59f660558753c881c3fdecfb8d078f32813;24613 bytes.
- tools/run_c297.ps1:d056d8668873436dc1ffff7e8a65cccd62d93c5d;4626 bytes.
- tools/invoke_c297.ps1:1e2b6ca0695163e5362d6a3664a68073494260c5;5721 bytes.
- docs/experiment-ledger-addendum-c297-preregistration.md:bd3081552c502fe91095ebe9bc3dce1eb7140984;8488 bytes.
- docs/v5b-init-order-grid-v0.1.md:5ad58eb5769fda94c2ccca85f1656f552a03762e;1296 bytes.

The acceptance-to-authoring comparison contains exactly these six additions. No accepted code,
test,preregistration,log or dispatcher changed. Activation must preserve all six reviewed blobs.
Acceptance of C296 and C297 authoring are separate commits.

## Checks actually rerun after matching

python -m unittest tests_lm.test_v05_c297_init_order_grid -v
Normal local default:Ran32 tests in4.758s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in4.775s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. This is not Windows or the full4493-test inherited suite.
The pre-commit32-test result is not substituted for these post-match runs.
All six files are UTF-8/no-NUL;both Python files and all three embedded runner Python blocks compile.
The symbol-table/global-binding audit found0 unresolved names after accounting for builtins and
standard module globals. Manifest recomputation matches:
6fc874b494cdc0b9dea5c55b57e482ef8eca50cc9790abc62840cf29e52bb903.

The actual fit function is executed for800 AdamW updates on a small synthetic classifier. A repeat
with a different external RNG state reproduces the same CE history and final weights. A different
registered order is also fitted;an optimizer spy confirms one optimizer with step800. The separate
train_cell fixture adds81 frozen evaluation calls and checks881/46176/3524 accounting.
Toy inputs encode synthetic target identity for control/numerical verification;these runs do NOT
establish FOLD binding or transfer performance.

Actual schedules for all three order streams verify identical rendered-example multisets and
100 exposures/row/length while changing order hashes. Their private generators preserve the global
Torch RNG. Factory fixtures verify three equal initial states with independent parameter storage.
Grid fixtures reject missing cells,mismatched row initial hashes and column order hashes.
Constant,additive and pure-interaction numerical examples validate the exact finite-grid sum of
squares identity. Nine descriptive capability failures still yield diagnostic integrity PASS only;
this explicit test prevents conflating model success with diagnostic execution validity.
Other tests cover23 hash failures before parent dispatch,628/1146 protection and missing-helper
rejection,semantic suite IDs,bundle ordering,actual run-phase ordering,nine replay calls,roundtrip,
no-overwrite,byte/semantic tampering,UTF-8 inventory reads,CLI and runtime-preflight dispatch.

Parent archives,Git,old model/scorers and inherited suite members are mocked where unavailable.
These fixtures are not actual parent-archive validation or actual4493-test execution.

## Scientific-path and parent semantic review

The sole direct repository import is C296. Its context supplies C294 numerical guard,C287 normalizer,
C284 evaluator/replayer,C283 quad scorer,C282 training tables and the inherited core bundle.
C296 pairs_from_rows/render_batch were read directly:they preserve complete two-query pairs and
return only token inputs and separate loss labels. C297 creates its own deterministic blocked
schedule with independent order IDs;no accepted function is monkeypatched during science.

C296 writer records final frozen logits and actual schedule tensors under fold-c296-render-eval-v1.
Its exact verifier rebuilds old gates,plans and matching under the inherited no-neural guard.
C297 verifies23 ordered summary hashes first,then dispatches C296.verify_artifacts with22 ancestor
paths and the accepted scientific execution HEAD. The summary seals the full eight-file inventory.
Require parent FAIL,quad blocked2/balanced3,all_pairs_matched/all_replays True and candidate_gate False.
Only recursively verified C296 dataset/triple/quad JSONs are used;canonical hashes are checked again.
No old checkpoint initializes a new cell.

C287 normalize_task and partition were re-fetched for the review. The seed/arm arguments are
metadata only;partition returns rows,correct,final_normal_nll,direct_pass,full_pass and failure
counts without introducing conflicting task/split fields. C297 labels order streams explicitly
and does not call C287's old cohort-level analyze function.
C284 replay_one was re-fetched:it needs final_sha256 and raw,strict-loads state,evaluates frozen
models and checks every original view/argmax at tolerance1e-9. It does not require the old seed/arm
record identifiers. C297 own records therefore safely use initial_seed/order_seed.

All622 inherited source pins and1131 inputs are retained and checked,with additional actual module
coverage for repository-local parent/context/core helpers. Adding OWN6 plus9 parent files yields
source628/protected1146. Missing helper coverage is not waived. Parent byte maps are checked on
Windows with the real artifacts rather than inferred from the execution HEAD alone.

## Factor controls,counts and interpretation

Three initial seeds by three order seeds form the complete fixed3x3 grid. Within rows,initial
fingerprints match;within columns,actual schedule hashes match. Require three distinct levels in
each factor. The remaining fit-time RNG is fixed597000 in every cell. Model construction receives
initial seed only;shuffle receives order seed only. No selected winners or losses control retries.
OrdinaryCE,blocked batching,800 updates,LR.005,14256 parameters and all original task gates stay fixed.

Diagnostic PASS is independent of individual model capability and has capability_gate_applicable=False.
All three full-task pass matrices,54 final partitions and12 numeric grids are reported. Additive
SS quantities describe only these nine finite observations,not population variance,p values or
proof of a unique cause. C296's unmet all-five gate is not replaced or retroactively passed.

9*(800+81+81)=8658 forwards;345600 training rows plus139968 evaluation/replay rows=485568 total;
34632 core calls. One9-state checkpoint bundle write/load and9 strict model-state loads.
Own32/modules182/loaded4494/focused4493;only the inherited exact C204 exclusion remains.
The suite-ID test is semantic but uses synthetic test cases;the real suite is still a runtime gate.
All3 embedded blocks compile;postcheck paths=sys.argv[2:25],head=sys.argv[25],argc26.
The launcher has23 fixed ordered parent paths and returns before publishing on Validate failure.
The existing dispatcher remains unchanged;the user block parses it,it parses the selected launcher,
and the launcher parses its runner. No historical test/control-plane pin is weakened.

## Mandatory runtime boundary

Not executed here:PowerShell ParseFile on Windows,the real23 parent archives and protected byte
maps,the full4493 inherited suite,and actual FOLD nine-cell training/scoring/strict replay.
All remain mandatory Validate/Execute gates. This review authorizes only the guarded launcher.
Any integrity failure retries SAME C297. C298 stays unregistered until C297 formal judgment.
No production selection or Gate F promotion is implied by either this review or a diagnostic PASS.
