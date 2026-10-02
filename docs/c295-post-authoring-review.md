# C295 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review plus local behavioral fixtures;not authoritative FOLD science.
Review target:0bcfc7de56bef1d0b9b0f949b038224ef6eaa992.
Acceptance base:1ef1dd45252819d5925d78eaaea3d40b156aeda2.

## Committed-byte match and unchanged parents

All six OWN files were fetched at the immutable authoring commit after creation. Source and test
were reread in consecutive ranges covering the entire files;the other four were fetched in full.
Whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c295_ce_budget.py:ae88e50e3aa77fb81b8dc800aee98cdb89276dab;24857 bytes.
- tests_lm/test_v05_c295_ce_budget.py:5ce113b5a70deef2833bd29c4393d14836829e34;24541 bytes.
- tools/run_c295.ps1:1b75c4c6816d0d9fe7e3046736874e12eda7e8b7;4630 bytes.
- tools/invoke_c295.ps1:0e781373c136e0a0917e91711de33511c88ac16a;5528 bytes.
- docs/experiment-ledger-addendum-c295-preregistration.md:fc99c3c773da864f700933a2870c24fc96686a43;7827 bytes.
- docs/v5b-ce-training-budget-v0.1.md:8da25347d63052290e2d77c27b02e9bce5fe443c;1502 bytes.

The remote acceptance-to-authoring comparison shows exactly these six additions. No accepted
source,test,preregistration,log or protected dispatcher was modified. Activation must preserve
all six reviewed blobs. C294 acceptance and next-C authoring are separate commits.

## Checks actually run AFTER matching remote bytes

python -m unittest tests_lm.test_v05_c295_ce_budget -v
Normal local default:Ran32 tests in6.805s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in6.590s;OK.
Local environment:Linux/Python3.13.5/PyTorch2.10.0+cpu. This is not Windows or full4421 regression.
All6 files decode as UTF-8 with no NUL. Both Python files and all3 runner-embedded Python blocks
compile. Post-match symbol-table audit found zero unresolved globals,allowing standard module
__file__/__name__/__annotations__. Manifest recomputation matches:
b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.

The suite runs the actual C295 fit_trajectory loop on a small synthetic classifier for1600 updates
and independently800 updates. It compares every first800 CE loss and every saved800 tensor exactly.
A separate1600-update optimizer-spy run confirms one optimizer and step1600 for its state entries,
then reproduces the full trajectory. The800 snapshot shares no tensor storage with the1600 state
or live model. These are control/numerical tests:the toy inputs encode synthetic target identity
and do NOT establish FOLD binding,transfer or scientific performance.

A scoring fixture strict-loads the real toy snapshot,freezes it,and makes81 calls/7776 rows. Other
fixtures cover all five actual schedule prefixes,100/200 exposures per length,paired label mapping,
loss/fingerprint/replay rejection,10-result/60-partition/180-contrast analysis,one-candidate-miss
negativity,21 hash failures before parent dispatch,616/1116 protection and missing-helper rejection,
semantic suite-ID filtering,model bundle ordering,CLI indices,run phase order,roundtrip,no overwrite,
byte/semantic tampering,UTF-8 inventory reads and global guards. The production run fixture verifies
that all five training calls precede any of ten snapshot evaluations and ten replays.
Parent archives,Git,legacy scorers/models and inherited test-suite members are mocked where needed.
No real local parent archives or the full inherited4421 suite have been executed in this runtime.

## Parent writer,loader and direct dependency checks

The only direct repository import is C294. Its context yields C293;C293.context was inspected and
yields C292/C291 plus C287 normalizer,C284 evaluator/replayer,C283 quad scorer,C282 training table
builder and the core bundle. C295 pins the exact C294 source blob and retains every inherited
source/input. Repository-local used context/core modules must be present in that inherited map.
Source616=610+OWN6;protected1116=1106+4 C294 summary/artifacts+OWN6. No helper pin is waived.

C294 is a diagnostic,not a model checkpoint. The21 summary hashes are verified BEFORE its exact
verify_artifacts dispatch with20 ancestor paths and accepted execution HEAD. Its three artifact
name/hash/size descriptors are fixed from the published receipt. The recursive verifier validates
all old masked/full gates. The already-verified C293 data/triple/quad JSONs are rechecked against
canonical digests. No parent checkpoint initializes new scientific trajectories.

C284.evaluate and replay_one were reread at the authoring commit. Evaluation requires eval mode
and requires_grad=False;each replay strict-loads state,checks final_sha256,compares every old task,
profile and normal/evidence-blind/query-blind view with drift<=1e-9 and exact argmax,and accounts
81 forwards/7776 rows/324 core calls. C295 supplies these exact record fields without invoking
C284's old identity/budget-specific analyze or training functions.

## Scientific comparison and resource accounting

Exactly one1600-update CE trajectory is trained per fresh seed295001..295005. Clone AFTER updates
800 and1600. No evaluation occurs during training or until all five trajectories finish. No AdamW
reset,extra labels,new lengths,auxiliary loss,output filter,adaptive stop or checkpoint selection.
Snapshots and histories have independent meanings:weights are after an update;each CE value is
from its training batch before that update. Full histories and exact snapshot fingerprints persist.
The two timepoints are paired dependent states,not independent models. The candidate has twice
its control's per-state training cost;this is NOT an equal-compute superiority experiment.

Actual optimizer updates5*1600=8000. Shared prefixes are not counted twice as12000. Training rows
384000. Ten states receive81 evaluation plus81 strict replay forwards each:9620 total forwards,
539520 row presentations,38480 core calls. The two stages strict-load10 in-memory snapshots and
10 archive states:20 state loads,one10-state archive write/load. Snapshot clones are in-memory,
not extra checkpoint files. Operational testing and old-parent numerical checks are separate.

The all-five ce1600 FOUR-character gate and all original masked thresholds remain fixed. All
seeds and both timepoints remain,including failures. Oracle conditional counts from C294 remain
descriptive;they cannot change any primary gate or original prediction. No automatic Gate F,
production or arbitrary-length claim. Budget extension is not a proof of earlier undertraining.

## Runner and authoritative runtime boundary

Own32/modules180/loaded4422/focused4421. Only the inherited exact C204 exclusion remains. The
suite-ID fixture verifies the actual loader/filter logic on synthetic members;real construction
and execution of the inherited suite is still required. No mutable ACTIVE assertion is added to
historical tests. Explicit UTF-8 reading is exercised under CP932 emulation without user settings.
Runner has3 embedded Python blocks;21 summary arguments;postcheck paths[2:23],head[23],argc24.
Launcher contains21 fixed ordered paths,checks unique C295 ACTIVE,and returns before scientific
publication on Validate failure. Existing invoke_active_v2.ps1 is unchanged. The user block must
ParseFile the dispatcher;the dispatcher parses its selected launcher,and the launcher its runner.

Not executed here:actual Windows PowerShell ParseFile,real21 parent summaries/artifacts and byte
pins,the full4421 inherited tests,real FOLD training and strict scientific replay. All remain
mandatory local Validate/Execute gates. This review authorizes only that guarded execution path.
An integrity failure retries SAME C295 without changing conditions. C296 remains unregistered
until C295 is formally judged. Gate F remains NOT PASSED.
