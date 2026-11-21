# C303 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review and executed local behavioral tests, not authoritative FOLD science.
Review target: 2974cc1af29b5a264642cc57d7c74f04e99b1281.
Acceptance base: d628bf0b901ee6a63fc9e6c5f338fac867e8bcfc.

## Committed-byte verification

All six OWN files were fetched after the authoring commit. Source and test were reread in
consecutive ranges covering all399/401 lines; the other four files were read in full. Returned
whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c303_residual_gradient.py: 0a59fd58ad89e460976f64218460c6de17ef8228; 29566 bytes.
- tests_lm/test_v05_c303_residual_gradient.py: 3dee13c0b3767ce21c18dc457d83d3a6083b6914; 30060 bytes.
- tools/run_c303.ps1: fa6ca16982d9c4b2ba478420a70d1ed43373e9ef; 4509 bytes.
- tools/invoke_c303.ps1: 21a4428e2fbb6ab47ebfc366b6e79a9495c5c117; 6301 bytes.
- docs/experiment-ledger-addendum-c303-preregistration.md: e7b72c8d1d173dbc1ad18eac4831f96d4397d35d; 8704 bytes.
- docs/v5b-residual-gradient-v0.1.md: 64a922b2e41f464f7d7f9e881f68dfde8c26af46; 1192 bytes.

The acceptance-to-authoring comparison has exactly these six additions. No accepted source,
test,log,preregistration or dispatcher changed. Activation must preserve all six reviewed blobs.

## Checks actually rerun after all six matches

python -m unittest tests_lm.test_v05_c303_residual_gradient -v
Normal local default: Ran40 tests in9.077s; OK.
Entire same40-test suite with io.text_encoding default emulated as CP932: Ran40 in10.217s; OK.
Runtime: Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. This is not the authoritative Windows runtime.
These are post-match runs; earlier pre-commit tests are not substituted for them.
Both Python sources and all3 runner-embedded Python blocks compile. All six files are UTF-8/no-NUL.
Symbol-table/import-binding audit found0 unresolved global names in source and test.
Manifest recomputation matches265067d9ca156f5181b6275ce4274ffee919751bcf1cd395b470656bce163ad7.
Explicit UTF-8 reads of the actual new files pass under CP932-default emulation. AST checks reject
implicit read_text calls. The emulation covers text-decoding defaults,not the whole Windows OS.

The actual C303 fit loop runs800 AdamW updates for all three arms on controlled toy models.
Tests verify full-training core weights change, frozen-arm core weights do not, and reader
weights do learn. A repeated candidate fit after a changed external RNG reproduces the complete
loss trace; optimizer instrumentation verifies one optimizer with step800.
An independent manually detached reference reproduces the candidate's parameter gradients.
The residual tensor receives gradients in full_train and core_frozen,but not residual_stop.
Initial local-encoder gradients are equal for full_train/core_frozen and differ for residual_stop;
initial outputs and reader gradients are identical. This tests the intended contrast rather than
mistaking requires_grad=False on core weights for a cut in gradients to core inputs.

Toy components are padded to match required stored parameter counts and synthetic tokens encode
targets for software-control tests. Their learning success is NOT actual FOLD capability evidence.
The inventory tests explicitly distinguish stored/trainable scalars from parameters receiving a
gradient and reject frozen-core membership in the active gradient union.
A separate real child train_one/replay fixture executes881/46176/3524 then81/7776/324 calls/rows/core
counts and exact saved-state replay on the toy model. It is not a substitute for production scoring.

The integration fixture executes the actual accepted C278 MeanFinalDualReadout class AST using
controlled backbone/reader modules. It checks the true class's dynamic hook order, original output
identity,reader-gradient identity and cleanup across all three arms. The local support file is a
fetched class slice,not the full parent module,and is not committed. On the user checkout this
class is extracted from the complete accepted source. No actual FOLD backbone was run locally.

Further fixtures exercise all five800-update schedules and row exposures,independent storage,
wrong-sum/dtype/error cleanup,29 summary-hash rejections before dispatch,664/1228 protection and
missing-helper rejection. The real child run/verify path is tested with substituted parents and
scorers:15 training dispatches precede15 bundle replays,then persisted reconstruction succeeds.
Byte tampering and semantic tampering after descriptor replacement both fail. One candidate miss
keeps the all-five gate negative. Synthetic semantic suite IDs verify4710 loaded to4709 retained
and duplicate rejection;they do not claim the actual inherited suite ran here.

## Scientific and parent contract review

C303 wraps the unchanged actual C278 class and leaves its forward assertions intact. Capture the
original post-core residual r before C278's normalization hook;capture a from read.output;append
the replacement hook during local_encoder so it runs after C278's dynamically installed sum hook.
Every call requires exact original input r+a. Controls return None;candidate r.detach()+a must
be numerically identical. The reader term is not detached. Registries are restored even on failure.
During inference stop-gradient changes no value;no evaluation-time gain or branch selection exists.

The two frozen arms have core parameters explicitly requires_grad=False and excluded from AdamW.
core_frozen still differentiates the fixed core operations with respect to their inputs.
residual_stop removes this residual contribution to shared upstream gradients. Other r-only
parameters may then receive no gradient. All arms still execute the forward core and reader.
Store14256 parameters each;requires_grad counts14256/10928/10928. Measure actual non-None gradient
counts and parameter unions instead of claiming all10928 actively learn. Equal forward counts do
not imply equal backward compute;global clipping and optimization differ as part of the policy.

First logits,CE and reader-parameter gradients must match per fresh triple before clipping.
Core/input gradients deliberately need not match. Stop-gradient is a chosen backward rule,not the
full mathematical derivative of the unchanged forward scalar; the detached reference,not a false
full-model finite-difference equivalence claim,is the relevant software test.
The mandatory real runtime probe compares plain C278 and all three wrappers and checks full-core
nonzero gradients and frozen-core None gradients. Actual observed parameter counts remain pending.

Only direct repository import is C302. C302.context exposes C301 and the inherited audit,normalizer,
evaluator,quad scorer,table builder and core bundle. Reuse C301.counted and C296 pair/render helpers
through C301.pair_source(C300); do not pass new identities into old cohort analyzers.
C303 verifies29 hashes BEFORE exact C302.verify_artifacts with28 ancestors and accepted C302 HEAD.
C302 has four diagnostic artifacts and NO dataset/checkpoint of its own. Read recursively verified
C301 data files at the next ancestor path and recheck canonical hashes through the source-pinned
C301->C300->C299 context chain. C300's actual context was reread to confirm this traversal.
All658 inherited sources/1217 inputs remain protected;actual repository-local context/pair helpers
and C278's exact readout blob are required. OWN6 plus5 parent files yield664/1228. No waiver.

New model states use model.* keys with the same numeric layout across arms. requires_grad flags
are reconstructed by the correct arm factory;strict final replay freezes all parameters. Core
initial/final fingerprints verify freeze policy. All800 histories,schedules and raw final outputs
are saved. Numerical reconstruction checks the new schema rather than an incompatible old cohort.

## Workload and execution boundaries

15*800=12000updates;576000training rows;15*(800+81+81)=14430forwards;809280row presentations;
57720core calls. One15-state bundle write/read,15 strict state loads,network0. Operational probe
4forward/backward calls,regression fixtures and recursive parent verification are separate.
Fresh seeds303001..303005 with paired orders303101..303105,fitRNG606000,ordinaryCE,lr.005 and
all original data/masks/thresholds remain fixed. No result-dependent policy or seed selection.
Primary all-five residual_stop quad gate remains distinct from comparisons to both controls.

Runner has3 compiled embedded Python blocks and29 ordered paths. Postcheck indices[2:31],head[31],
argc32. Validate precedes Execute;Validate failure returns before scientific publication.
Own40/modules188/loaded4710/focused4709;the sole inherited exact C204 exclusion is unchanged.
The existing active_v2 dispatcher/selected-launcher/runner ParseFile chain remains mandatory.

Not executed here: Windows PowerShell ParseFile,the29 actual user-local parent archives/byte pins,
the actual4709-test inherited regression suite,or15 actual FOLD model fits/evaluations/replays.
Local parent/Git/scorer/suite inputs are substituted where unavailable. These checks remain
mandatory local Validate/Execute gates. This review authorizes only the guarded launcher,not a
scientific result. Invalid execution repairs SAME C303;valid all-five miss is a valid negative.
C304 is unregistered until C303 formal judgment;Gate F remains NOT PASSED.
