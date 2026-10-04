# C302 independent post-authoring review

post_authoring_review = PASS
Scope:separate committed-byte/static review plus executed local behavioral tests;not authoritative FOLD science.
Review target:60df5639637db92a7e9bc7f5649634bc01d437e6.
Acceptance base:400dd5337c6e30fe901b91d4587d16d7c12f9c0b.

## Remote-byte match

After the authoring commit,all six OWN files were fetched from that immutable target. Source and
test were read in consecutive ranges covering all379/464 lines;the other four files were read
in full. Returned whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c302_frozen_gain_cross.py:1eb77daeb4fd53141ad31a6ad3c60ceba9ce3ad2;26148 bytes.
- tests_lm/test_v05_c302_frozen_gain_cross.py:77633adba76e3509ba639e5a1236ff2cb4153a51;30216 bytes.
- tools/run_c302.ps1:efcc850bf0333a9fd8dd6be9b487dc4af5edfb3c;4640 bytes.
- tools/invoke_c302.ps1:74c5526f36f8f7f4a1827c6885db7140a7e6ea17;6205 bytes.
- docs/experiment-ledger-addendum-c302-preregistration.md:22544625108f8b04e793390911eb2b23c1de96a7;9050 bytes.
- docs/v5b-frozen-gain-cross-v0.1.md:45883ed46c7ff4357be6a08e823939b6cd329483;1117 bytes.

The remote acceptance-to-authoring comparison contains exactly these six additions. No accepted
source,test,preregistration,log or dispatcher was edited. Activation must retain these six blobs.

## Checks actually executed after all six matches

python -m unittest tests_lm.test_v05_c302_frozen_gain_cross -v
Normal default:Ran32 tests in3.385s;OK.
Entire same32-test suite with io.text_encoding default emulated as CP932:Ran32 in3.633s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. These are post-match runs,not pre-commit results.
All6 files decode as UTF-8 and contain no NUL. Both Python files and all3 embedded runner blocks
compile. Symbol-table traversal finds0 unresolved global references after accounting for imports,
module bindings,builtins and standard module globals. The manifest self-hash matches:
283f4ac996eda2ac866a192408fff2368782b8592d350c11af33723f874f2960.

Tests cover unit-gain identity and independent numerical expectations for nonunit gains;frozen/
no-grad enforcement;invalid coefficients;repeated calls;existing hooks;sum mismatch and exception
cleanup;unchanged parameter values;and prevention of optimizer/state reload inside intervention.
The actual infer_state function executes3*81 model forwards on a controlled small model,checking
all per-pass81/7776/324 counts,original output restoration and strict checkpoint/gain rejection.
The real runtime_preflight function is exercised for both fixed and learned wrapper fixtures.

Integration test31 executes the actual accepted C278 MeanFinalDualReadout and C301 ResidualGain
class ASTs,with substitute backbone/reader components. Both original gain conditions exactly
match the C302 inner-model intervention,including nonunit gain,and all original state/hook
registries remain unchanged. The local support files are fetched CLASS SLICES,not full clones of
those parent modules,and are not committed. On the user's checkout the test extracts the classes
from their full accepted sources. This validates the actual class/hook protocol,not the actual
FOLD backbone or the user's learned checkpoint outcomes.

Other tests exercise30 results/180 partitions/120 comparisons,exact rescue/regression accounting,
wrong-to-wrong changes,parent-record gain reconciliation,all28 hash failures before dispatch,
658/1217 protection and missing-helper rejection. Production run-path tests call the actual child
run and parent-bundle interface,with one bundle load and ten inference dispatches,then serialize/
reconstruct results. Byte tampering and semantic tampering with updated descriptors both fail.
No model checkpoint is written;only evaluation tensors are serialized. All swapped capability
gates may fail while diagnostic integrity passes. Synthetic regression IDs test4670->4669 plus
duplicate rejection,not source-string count assertions. Explicit UTF-8 inventory reads pass under
CP932-default emulation;this is not a full Windows emulation.

## Scientific path and parent contract audit

C301's writer stores wrapper states in fold-c301-gain-models-v1 and final prediction records in
fold-c301-gain-eval-v1. Its run/load_bundle/verify_artifacts implementation was reread at the exact
review ref. Its two arms have distinct state schemas:model.* only versus model.* plus gain_logit.
C302 uses the actual C301.make_models and load_bundle and strict-loads the correct wrapper for
each ordered seed/arm. It verifies the full wrapper fingerprint and its original gain before
inference. No parent parameter is inserted,replaced or changed to implement the coefficient swap.

Main scoring deliberately calls wrapper.model,not wrapper.forward. The child-owned temporary
hook applies the requested gain exactly once after verifying the actual C278 pre-normalization
sum r+a. The original C301 gain_logit is kept untouched in the stored wrapper. This avoids a
double-gain path and permits both fixed and learned states to use either registered coefficient.
The operational smoke compares each original wrapper's actual output against the instrumented
inner model for both parent arms. Baseline passes must reproduce every saved normal and masked
logit within1e-9 and exact argmax,not only aggregate accuracies. Hook registries and full weights
are checked after every pass. All upstream core/reader computation still executes.

C302 verifies28 ordered summary hashes before exact C301.verify_artifacts with27 ancestors and
C301's accepted execution HEAD. The exact C301 summary seals all8 output descriptors;the parent
verifier reconstructs all prior scoring,schedules,gain traces and replay attestations. The child
adapter checks seed/arm identities,parameter count,final fingerprint,checkpoint metadata and exact
agreement between fit.final_gain and summary.seed_results.final_gain. The coefficient donor is the
same seed's learned_gain state,never a different seed or an evaluation-derived value. All ten
parents stay,including TRAIN failures. The original negative counts2/3 seen and2/1 quad are pinned.

Sole direct repository import C301. All652 parent source pins and1202 inputs remain checked,
including C278's exact readout blob and actual repository-local context/core helpers. Add OWN6
and9 C301 summary/artifacts for658/1217. No accepted helper mutation or dependency waiver.
Inherited C284 evaluates the actual inner C278 with unchanged data/masks;its replay_error checks
all three tasks,every profile and view. C287 partition normalization accepts child mode metadata.

## Workload,interpretation and execution boundary

10 saved states*3 passes*81 forwards=2430;233280 row presentations;9720 core calls. Ten strict
state loads,one existing bundle read,no training,new model checkpoint or network call. Operational
smoke8 forwards,regression fixtures and recursive parent reconstruction are separate from science.
Four logical weight/gain conditions per seed are counted once;original_after is only restoration.
Both within-weight unit->trained and across-weight fixed->learned comparisons cover25920 normal
rows each. No extra seeds or independent observations are inferred from the repeated evaluations.
Raw output payload477757440 bytes excludes archive overhead and is not peak-memory accounting.

The within-weight intervention tests the immediate coefficient effect. Across weights at one
coefficient describes the whole prior training-policy difference;it does not isolate training
mechanisms or assign additive causal shares. No gain sweep,per-question best-of,model selection,
training extension,threshold change,production adoption or Gate F promotion is authorized.

Runner contains3 compiled Python blocks;28 paths;postcheck paths=sys.argv[2:30],head=sys.argv[30],
argc31. The launcher contains28 fixed ordered paths and returns before science/publication on
Validate failure. Own32/modules187/loaded4670/focused4669;sole inherited exact C204 exclusion unchanged.
The unchanged invoke_active_v2 dispatcher/selected-launcher/runner ParseFile chain remains required.

Not executed here:PowerShell ParseFile on Windows,the user's28 real parent archives and Windows
protected bytes,the actual4669 inherited regression suite,or inference on the ten actual C301
checkpoints. Parent/scorer/Git/suite inputs are substituted in local fixtures where unavailable.
All remain mandatory local Validate/Execute gates. This review authorizes only the guarded
launcher. Any integrity or restoration failure repairs SAME C302. C303 waits for formal judgment.
