# C300 independent post-authoring review

post_authoring_review = PASS
Scope:separate committed-byte/static review and executed local behavioral fixtures,not authoritative FOLD science.
Review target:49227f1eb5b795553723d5e4188084d16b39dce3.
Acceptance base:c726cc8d1c587328943229276d6588fb59386a06.

## Remote-byte match and actual post-match tests

All six OWN files were fetched after commit at the immutable target. Source and test were read
in consecutive ranges covering their full contents;other files were read in full. Returned whole-file
Git blob identities were checked against independently hashed local file bytes6/6:

- fold_lm/v05_benchmarks/model_c300_frozen_readout_terms.py:7299772d37af3a6b693a922ca63d2418565f2d69;24457 bytes.
- tests_lm/test_v05_c300_frozen_readout_terms.py:60cdb6339661038f99e2c3ef3669b8424956db6b;28407 bytes.
- tools/run_c300.ps1:5e843cacbccbc83a37a8e6846199170b7666bc8a;4799 bytes.
- tools/invoke_c300.ps1:ebe6403787eedf31ab08a60d3363c6cdae02e72d;6016 bytes.
- docs/experiment-ledger-addendum-c300-preregistration.md:2bbc57c413db768ac1586ac773d4a1ddf27ddda8;8722 bytes.
- docs/v5b-frozen-readout-terms-v0.1.md:cb43e6450a81fda59a7b12a3b60782f95b1c16fa;1259 bytes.

Remote compare from acceptance to authoring contains exactly these six additions. No accepted
source,test,preregistration,log or dispatcher was modified. Activation must retain these6 blobs.

After all six remote matches,the COMPLETE new test module was rerun:
python -m unittest tests_lm.test_v05_c300_frozen_readout_terms -v
Normal default:Ran40 in3.704s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran40 in3.812s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. Pre-commit results are not substituted for these runs.
All6 files UTF-8/no-NUL;both Python files and all3 embedded runner Python blocks compile.
Symbol-table/import-binding traversal found0 unresolved global references,allowing builtins and
standard module globals. Manifest recomputation matches:
31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30.

## Hook integration and tests actually exercised

The exact accepted C278 MeanFinalDualReadout class body was fetched and executed via its AST with
controlled substitute backbone/reader modules. The local support file contains that class slice,
not a full clone of the accepted repository module. It is not one of OWN6 and is not committed.
On the user's checkout,test40 extracts the same class from the full accepted source. This checks
C278's real dynamic hook registration/provenance assertions,not an independently rewritten forward,
but does NOT establish behavior of the actual FOLD backbone or trained checkpoints here.

A second small dynamic-hook fixture provides independent exact residual-only and reader-only
expected outputs through its normalizer/classifier. Tests exercise identity before/after,all4 modes,
multiple batch sizes,existing hooks,weight equality,wrong sum/dtype detection,and exception cleanup.
A deliberate extra term in the sum is rejected. Empty contexts and non-frozen/grad-enabled calls
are rejected. Scoped hooks neither construct an optimizer nor reload model state.

The actual infer_cell path performs4*81 fixture forwards,including all3 tasks/splits/views and4 core
calls per forward. It verifies per-mode81/7776/324 counts and actual hook-formula attestations,
strict state loading,full-before/after output agreement and unchanged fingerprints/registries.
Synthetic full-cohort analysis covers36 model/mode results,216 partitions,108 paired comparisons,
46656 matched normal rows and9 reproduction records. Wrong-to-wrong argmax changes are not rescues.
Even all ablations failing their capability gates still permits diagnostic integrity PASS only.

Additional tests cover26 summary hash failures before parent dispatch,exact C278/C299 pins,646/1191
protection-map accounting and missing helpers,actual run-path order and9 inference calls,checkpoint
loader dispatch,numerical archive roundtrip,no overwrite,byte and semantic tampering,old baseline
gate preservation,CLI indices,and explicit UTF-8 reads under CP932 emulation. A serialization spy
confirms run writes intervention-evaluations.pt,not a new trained-model checkpoint. Suite-ID tests
use a synthetic4598-member inventory and verify the exact inherited exclusion/4597 retained IDs.
These are not execution of the full real4597 inherited tests.

## Deciding-path semantics and dependencies

Accepted C278 combines post-core next-route EOS residual r and added-reader output a before
readout_norm. Its constructor/forward was read;C284 evaluate/replay_error/replay_one and C267
scorer/evaluator/counted contracts were also read. The original normalization and classifier remain.
The additional reader uses pre-core local evidence/query states;it is not the vocabulary classifier.
r is not a core-only tensor. Suppressing r is not equivalent to removing the core from computation.

A persistent capture hook precedes C278's dynamically installed norm hook. The local-encoder hook
registers the replacement hook after C278's norm hook. read.output supplies the captured a.
Before any intervention,the late hook requires exact observed input==r+a and finite CPUfloat64
batch-by16 tensors. Full modes return None,leaving the original input untouched. A root always_call
hook removes per-call hooks even on exceptions;the context finally removes its persistent hooks
and checks registry restoration. C278's own assertions and cleanup continue to execute.

Sole direct repository import:C299. Its context supplies C294 no-neural,C287 partition,C284 original
scoring/replay,C283 quad,C282 training-table smoke and the actual core/model modules. Verify26 ordered
summary hashes before C299.verify_artifacts with25 ancestors and the accepted execution HEAD.
The exact C299 summary seals every parent artifact descriptor. The loader requires the complete9
cohort and exact original diagnostic/gate matrices,then reads final raw-output anchors from
fold-c299-core-eval-v1. It uses C299.load_bundle for fold-c299-core-models-v1 in the actual run path.
Compatible model instances are constructed,then strictly loaded from all9 learned states once;
no learning or successful-cell filtering occurs. Parent losses are not substituted for predictions.

All640 inherited source pins and1176 protected inputs remain enforced;actual repository-local
context/core helpers must be covered. C278's exact readout source blob is required explicitly.
Add OWN6 and9 parent files:source646/protected1191. No missing dependency waiver or accepted edit.

## Workload,runner and interpretation limits

9 models*4 passes*81 forwards=2916;279936 total row presentations;11664 core calls. Every upstream
core and reader computation still runs in every mode. Training0;9 strict state loads;one existing
checkpoint-bundle read;new checkpoints0. The new tensor archive is an evaluation artifact,not weights.
Raw float64 logits have573308928 payload bytes plus serialization overhead. No speed/memory claim.
The real runtime smoke performs5 forward calls outside scientific counts. Operational tests and
recursive parent verification likewise have separate scope. Numerical postcheck uses no-neural.

Runner3 Python blocks;26 paths;postcheck argv[2:28],head argv[28],argc29. Launcher lists26 fixed parent
paths and returns before science/publication when Validate fails. Preserve dispatcher/selected
launcher/runner ParseFile chain. Own40/modules185/loaded4598/focused4597;sole inherited C204 exclusion.

Ablation effects can include distribution/scale changes in jointly trained states. They are not
additive logit attribution,training-cause proof,core necessity or an automatically deployable policy.
No per-query better-branch selection or old capability threshold change. All9 successes/failures remain.

Not executed here:Windows PowerShell ParseFile,real26 ancestor archives and their byte pins,the full
real4597 regression suite,or actual frozen C299 model inference. Mandatory Windows Validate includes
those parent checks and an actual trained-checkpoint intervention smoke before science. All9
scientific states must reproduce the original full outputs before/after and retain weights/hooks.
Any integrity issue repairs SAME C300;C301 remains unregistered until formal C300 judgment.
