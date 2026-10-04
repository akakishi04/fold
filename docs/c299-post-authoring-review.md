# C299 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review and local behavioral fixtures,NOT authoritative FOLD science.
Review target:be4f0c6ce22632924a217eddeeb49a7125de310a.
Acceptance base:315e24172119cd85f040def1ca01a7e4c6a0dfed.

## Remote-byte verification

After committing,all six OWN files were fetched from the immutable review target. Source/test
were reread in consecutive ranges covering their complete contents;the four other files were
read in full. Returned whole-file Git blob hashes match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c299_core_initialization.py:b97749c29217b0ad9c57a4bf61d668684e391880;26040 bytes.
- tests_lm/test_v05_c299_core_initialization.py:35e9bc5dc435d55e8690d7db0f54f4a12ca25963;28078 bytes.
- tools/run_c299.ps1:1911363e9097ee21751deca92ae0ebb341871cd2;4665 bytes.
- tools/invoke_c299.ps1:76d60d564cbb7c417236fb035fcb9438d1c72a91;5913 bytes.
- docs/experiment-ledger-addendum-c299-preregistration.md:2879c97f9414600e67545763e9bb46f5fe4cf265;7423 bytes.
- docs/v5b-core-initialization-v0.1.md:3435308e9b72019524208452bc361df1d235af35;1169 bytes.

Acceptance-to-authoring comparison contains exactly these six additions. No accepted source,
test,preregistration,log or dispatcher was modified. Activation must preserve all six blobs.

## Checks actually rerun after all six matches

python -m unittest tests_lm.test_v05_c299_core_initialization -v
Normal local default:Ran32 tests in5.127s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in5.151s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. This is not Windows or the actual4557-test suite.
The pre-commit test result is not substituted for these post-match runs.

All6 files are UTF-8/no-NUL. Both Python sources and all3 runner-embedded Python blocks compile.
Symbol-table/import-binding audit:0 unresolved global names after allowing builtins/module globals.
Manifest recomputation matches796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846.
Tests read actual OWN files with explicit UTF-8 under CP932-default emulation. AST checks reject
implicit read_text calls in the new source/test. User locale/settings need not change.

The actual C299 fit loop executes800 AdamW steps on a small synthetic model. A separately written
reference loop reproduces all800 losses and final weights. An additional fit with altered external
RNG reproduces those losses;optimizer instrumentation verifies one optimizer with step800.
A train_cell fixture adds81 frozen evaluation calls and checks881/46176/3524 accounting.
Toy inputs encode synthetic target identity for software-control testing,not actual FOLD performance.

Correctly sized substitute components test the complete nine-cell factory,component provenance,
fixed reader,independent storage and identical same-source diagonal initialization. The remainder
fingerprint ignores core.* changes but detects changes elsewhere. Grid checks reject missing cells,
wrong row/column fingerprints,reader mismatch and wrong schedules. Diagonal tests reject altered
initial/final states,losses,events,anchor-reader identities and raw outputs.
Full synthetic analysis validates54 partitions,12 decompositions and the integrity/capability
separation. All capability failures remain compatible with diagnostic integrity PASS only.

Other fixtures reject each of25 summary hashes before verifier dispatch,wrong parent schema/cohort,
missing protected helpers,changed replay/workload counts,bundle reordering,byte tampering and
semantic tampering even after recomputing a descriptor. Production run-path tests verify all9
training calls precede all9 archive replays,persisted roundtrip and no overwriting of run folders.
The real runtime_preflight function is tested with a missing actual core-class module pin,then
with that pin restored,and with a changed diagonal initialization. Synthetic test-suite ID sets
exercise4558 loaded to4557 retained and duplicate rejection;the real inherited suite is pending.

## Parent and scientific-path contract review

The source imports only C298. Its context supplies C297,C296,C294 no-neural,C287 normalizer,
C284 evaluation/replay,C283 quad,C282 training tables and the core bundle. C299 reuses helper-level
contracts,not C298's old cohort-level analyze with incompatible identity fields.
C298 writes final outputs in fold-c298-components-eval-v1 using backbone_seed/reader_seed.
C299 verifies25 ordered summary hashes before C298.verify_artifacts with24 ancestor paths and
C298's accepted execution HEAD. That exact summary seals all eight artifact descriptors and the
parent verifier reconstructs original scores,component provenance and prior diagonal controls.
Only verified data JSONs feed learning. Parent evaluation records are anchors,not learned initializers.

Crucial anchor mapping:C299's three same-source core/remainder diagonals reproduce C298's FIRST
reader column(reader297001),not C298's previous same-backbone/reader diagonals. All3 levels stay,
including backbone297002 with2 normal quad errors. Do not compare it with the18-error cell that
used reader297002. Require exact initial/final fingerprints,all800 losses,events,plus all-view
logit tolerance1e-9 and exact argmax via the existing C284 replay_error. No relaxed reproduction.

C278's unchanged model has backbone plus read;C260's unchanged full/core-free source identifies
3328 removed core parameters. The C299 runtime checks the actual13488 backbone partition:
3328 core +10160 other parameters,plus768 added-reader parameters=14256. It does not remove
or freeze any module. Independent UNTRAINED component copies are recombined,then all parameters
train. Complete state order and parameter storage are checked. The remainder includes input and
output components,not only the encoder. The fixed reader is fixed at initialization only.
Actual component construction and all3 diagonal initial hashes remain mandatory Windows preflight.

All634 inherited source pins and1161 protected inputs remain enforced. Add OWN6 and9 parent files
for640/1176. Repository-local context/core helpers must be pinned;runtime also checks the actual
core class implementation module. No missing dependency or accepted-source mutation is waived.

## Workload,runner and interpretation boundaries

9*800=7200 updates;345600 training rows;9*(800+81+81)=8658 model forwards;485568 total rows;
34632 core calls. One9-state bundle write/load,9 strict state loads,network0. Diagonal numerical
comparison adds no forward. Old-artifact reconstruction and operational fixtures are separate.
The only changed conditions are initialized core and remaining-backbone factor assignments.
Reader297001,order297101,fitRNG597000,ordinaryCE,lr.005,800 steps and all original gates remain fixed.
One known three-level grid at one reader/order is not independent replication,population variance,
core necessity,or architectural superiority. No winning cell is deployed;Gate F remains NOT PASSED.

Runner has3 compiled Python blocks;25 summary paths;postcheck paths=sys.argv[2:27],head=sys.argv[27],
argc28. Launcher has25 fixed ordered run paths. Validate failure returns before scientific logging/
publication. Preserve existing active_v2 dispatcher and dispatcher/selected-launcher/runner ParseFile.
Own32/modules184/loaded4558/focused4557;sole inherited exact C204 exclusion remains unchanged.

Not executed here:Windows PowerShell ParseFile,the real25 parent archives and Windows byte pins,
the actual4557 inherited regression tests,or nine actual FOLD training/evaluation/replay cells.
These remain mandatory Validate/Execute gates. This review authorizes only the guarded launcher,
not a scientific verdict. Any integrity or reproduction failure repairs SAME C299 with fixed
conditions. C300 stays unregistered until formal C299 judgment.
