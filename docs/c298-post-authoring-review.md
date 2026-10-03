# C298 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static and local behavioral fixtures,NOT authoritative FOLD science.
Review target:0705f8022c060d30bc04a52d18531f33d60e1d6c.
Acceptance base:fe56cfdd4d393ae5d6a3d268eaa66f19a0b5a578.

## Remote-byte verification

All six OWN files were fetched after the authoring commit at its immutable SHA. The complete
Python source and test were reread in consecutive ranges;the other four files were fetched in
full. Their returned whole-file Git blobs match independently hashed local tested bytes6/6:

- fold_lm/v05_benchmarks/model_c298_component_initialization.py:a1f64f270dcba45e25168841d76113a1b195aebc;25856 bytes.
- tests_lm/test_v05_c298_component_initialization.py:a1ca6926d9cbf7e7d35d65c723024b5bee90372e;28012 bytes.
- tools/run_c298.ps1:9441ae3566f1c51c7cf9d464830da6f8238a2bc7;4719 bytes.
- tools/invoke_c298.ps1:2460236a71e8b10ebe1a8566e8625d529b392a34;5817 bytes.
- docs/experiment-ledger-addendum-c298-preregistration.md:c74fde811ecfe4017136bc6d3add38a2c0fa6689;8759 bytes.
- docs/v5b-component-initialization-v0.1.md:a75bebc57bdb211a51923a0e840a277e8a5d83c3;1330 bytes.

Acceptance-to-authoring comparison contains exactly these six additions. No accepted sources,
tests,preregistrations,logs or dispatchers changed. Activation must preserve these six blobs.

## Checks actually executed after matching

python -m unittest tests_lm.test_v05_c298_component_initialization -v
Normal default:Ran32 tests in7.268s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in8.095s;OK.
Linux/Python3.13.5/PyTorch2.10.0+cpu. This is NOT Windows or the full4525 inherited suite.
The earlier pre-commit result is not substituted for these post-match tests.

All six files are UTF-8/no-NUL. Both Python files and all three embedded runner Python blocks
compile. Symbol-table audit finds zero unresolved global references after accounting for module
bindings,builtins and standard module globals. Manifest recomputation matches:
e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62.

The actual C298 fit loop runs800 AdamW updates on a small synthetic model. A separately written
reference loop reproduces its800 CE values and final weights exactly. A second fixed-RNG fit
with optimizer instrumentation confirms one optimizer and step800. A train_cell fixture executes
800 training plus81 frozen evaluation calls,checking881 forwards/46176 rows. The toy input encodes
synthetic targets for control/numerical tests;these are not FOLD binding or generalization results.

Factory fixtures use correctly sized substitute modules to verify all nine independent component
combinations,exact diagonal initial state,distinct factor levels and storage isolation. Changing
one cell does not mutate another. Grid checks reject missing cells,wrong component provenance,
wrong common schedules,and changed diagonal initial/final hashes,loss histories or raw outputs.
Complete synthetic grids test54 partitions/12 decompositions and diagnostic-versus-capability scope.
Parent hash guards reject each of24 hashes before verifier dispatch. Additional tests exercise
634/1161 protection,missing-helper rejection,semantic suite-ID filtering,bundle ordering,actual
run call ordering,strict replay dispatch,roundtrip,no overwrite,byte/semantic tampering,real local
UTF-8 document reads under CP932 emulation,CLI indices and runtime anchor checks.

Some parent archives,Git,legacy scorers,models and inherited test-suite members are substituted.
The real24 parent archives,full4525 regression and nine actual FOLD training cells were NOT run
here. CP932 emulation checks default text decoding,not an entire Windows environment.

## Scientific path and writer/loader contracts

C278 constructor/forward was read:the complete registered parameter boundary is backbone and read.
Read is the additional query/key/output residual reader,not the final vocabulary classifier.
C298 uses the same actual class and only reassigns an independently copied UNTRAINED read module.
Module/state-key boundaries,13488+768 parameter counts,component fingerprints,full state order,
precision and storage checks fail closed. All parameters train;no trained checkpoint is spliced.

C297 schedule/fit/check_fit/train_cell source was read. C298 keeps its first original order297101,
fit RNG597000,ordinary CE,AdamW and800-step numerical operation order. Construction may consume
randomness before fitting,but every cell resets the global fit RNG and the shuffle uses its own
generator. Component donors include all3 original levels,not only the known failed initial state.
Same-component diagonals must reproduce initial/final fingerprints,800 CE values and schedule
exactly. C284.replay_error compares all task/view logits<=1e-9 with exact argmax;this uses already
computed outputs and adds no model forward. Runtime preflight verifies real diagonal initial
fingerprints/events before science;the full training reproduction remains an Execute gate.

C297's writer saves fold-c297-grid-eval-v1 final raw outputs and fit records. C298 first verifies24
ordered summary hashes,then calls the exact parent verifier with23 ancestor paths and accepted
execution HEAD. It validates diagnostic PASS,all9 parent identities and original task matrices;
only verified canonical input JSONs and three original-order records become reproduction anchors.
Parent trained weights are not training inputs. All eight artifact descriptors are sealed by the
exact summary hash. C297.check_fit is reused;C297.analyze is not because factor identities changed.

The only direct repository import is C297. Its inspected context exposes C296 pair/render helpers,
C294 no-neural guard,C287 label-tolerant normalization,C284 evaluation/replay,C283 quad scoring,
C282 training tables and the core namespace. Retain/check all628 source pins and1146 inputs plus
actual repository-local context/core coverage;add OWN6 and9 parent files to obtain634/1161.
No accepted protection failure or dependency omission is waived.

## Counts,runner and mandatory runtime gates

Nine cells*800=7200 updates,345600 training rows,8658 forwards,485568 row presentations,34632 core
calls. One9-state bundle write/load and9 strict state loads. Initial template copies are not
neural forwards;operational tests and inherited saved-data reconstruction are separate costs.
Own32/modules183/loaded4526/focused4525. Sole inherited exact C204 exclusion unchanged. The local
suite-ID fixture is synthetic;actual inherited module loading remains a Windows Validate gate.

Runner has three compiled Python blocks;24 summaries;postcheck paths[2:26],head[26],argc27.
Launcher has24 fixed ordered parent paths and validates branch/tree/head/unique ACTIVE before
logging. Its runner is parsed before Validate. A Validate failure returns before scientific
Execute/publication. The existing dispatcher remains unchanged and its user ParseFile plus selected
launcher ParseFile chain is retained. No claim that PowerShell parsing ran in this Linux review.

One fixed order and previously observed factor levels make this a targeted diagnostic,not an
independent replication or population variance study. A better off-diagonal cell does not authorize
winner selection,adoption,Gate F promotion or changing old all-five gates. All results stay reported.
Any integrity failure retries SAME C298 with fixed scientific conditions. C299 remains unregistered.
