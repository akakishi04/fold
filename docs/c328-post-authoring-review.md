# C328 post-authoring review

Review date: 2026-10-17 Japan time.
post_authoring_review = PASS
Source/preregistration review target HEAD:
6296eae8209f674da2ae9cff4516857e010c1d59.
Acceptance base: d96e7ff66f76463e6fe39ca159e687f7d26d2011.
This is authoring approval, NOT a scientific C328 verdict, native Windows execution
or full historical-regression PASS. Use the subsequent final activation HEAD in
the user command, not the source-only review target.

## Committed-byte reread and scope

After the complete source/tests/runner/launcher/preregistration commit was published,
all six own files were fetched again at the exact target and read completely.
The three long Python files were retrieved in consecutive complete line ranges
through EOF. Returned Git blobs were compared with independently calculated Git
blob hashes of the local raw files used for the checks below. All six match:

| File | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c328_late_rate_decay.py | a7248af8da12bf84d18e8e270917847f7e3aa1d5 |
| tools/c328_execution.py | aecc0e191632f909c64917c1be135314819b5591 |
| tests_lm/test_v05_c328_late_rate_decay.py | 14dfb675330c2137bafd23978dc4f1c3dd4d8a18 |
| tools/run_c328.ps1 | fa86a18a0e978f24add60e88c3d7fb1cc33a2b9c |
| tools/invoke_c328.ps1 | c0edd68d883c79c1d28e44dd29a316215cf03aa9 |
| docs/experiment-ledger-addendum-c328-preregistration.md | b6910dc8638c1be47d05d99e5c96c6056dba1a96 |

Remote compare against acceptance showed exactly these six additions, no edits or
deletions of accepted sources/tests/logs/contracts. C327 acceptance was committed
separately. This review and ACTIVE handoff are subsequent documentation-only changes.
No protected dispatcher or earlier result is rewritten to authorize this child.

## Checks rerun after the complete remote reread

- Normal own suite: 64/64 PASS, failures/errors/skips 0; 3.711 seconds.
- CP932-default-text-open emulation: 64/64 PASS, failures/errors/skips 0;
  3.642 seconds. Both builtins.open and io.open supplied CP932 only when the
  text-file encoding was unspecified. Explicit encodings and binary opens were
  preserved. This is not native Windows or a claim about the system locale.
- All six files decode as UTF-8 and contain no NUL. All three Python files compile
  and import. Recursive function/method/nested-code LOAD_GLOBAL and import-binding
  checks found zero undefined global names.
- Actual own unittest loader contains exactly64 tests. Additive-suite validation
  combines the real own loader with an explicitly synthetic5658-case historical
  inventory, checks total5722 and uniqueness, and rejects duplicate historical IDs.
  This is NOT execution of the actual full5722 historical suite.
- Manifest self-hash matches
  75f3de53837dcc64127b72f541ded650436b3a6ac46686bd9d8ff2aa8b89a226.

Author environment: Linux Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5, two Torch
threads. No PowerShell executable was available; native author-side AST execution
is not claimed. The mandatory dispatcher -> launcher -> runner ParseFile chain is
retained and source-reviewed for user-side execution.

## Numerical and optimization-policy audit

The accepted C308 parameter_groups/optimizer_for/verify_optimizer implementations
were read, including noncore-first/core-second group ordering, active-parameter
membership, AdamW settings and the distinction between LR and gradient scaling.
C328 calls the unchanged optimizer factory once per model and validates its initial
native contract. No accepted module global, optimizer factory or verifier is patched.

The child captures optimizer identity, parameter identities/order, all non-LR group
settings and optimizer defaults. It validates them at every update alongside the
registered rates. Only group['lr'] changes at zero-based step800, BEFORE update801.
The constant arm retains.005/.0005; late_tenth changes to their products with.1.
Updates1..800 are identical-policy training in both arms; the total stays1200.
Optimizer moments and step counters are byte-fingerprinted before and after the LR
assignment and must match. No optimizer recreation, state clearing/scaling or
restart is allowed. Gradients are not rescaled or detached before global clipping.

The production numeric loop was exercised for1200 updates in each arm using the
explicit small Torch model. The800-update model/optimizer boundary hashes and all
first800 CE values matched exactly; optimizer creation occurred once per model;
moments survived the switch; final states differed after the rate intervention.
A separate four-update constant-rate reference exactly matched explicit mean CE,
backward, global clipping and AdamW arithmetic. With matched populated moments and
matched gradients, the late-rate toy step had one-tenth the reference delta within
the declared floating tolerance. Nonfinite logits stop before an optimizer step.
These are software arithmetic fixtures, NOT scientific FOLD outcomes.

Boundary metadata is not portrayed as a saved replay of every intermediate state:
the actual run records full state/optimizer hashes at the800-update boundary plus
all first800 losses, then requires pairwise equality. Saved reconstruction checks
these traces, hashes, switch receipts, final checkpoints and evaluation results;
it does not rerun the complete optimization history.

## Scientific isolation, evaluator and gates

C328 uses fresh328001..328005 initializations and328101..328105 order seeds.
Both arms use the unchanged C326 batch4 mask algorithm and the same logical row
order, profile schedule, intact query pairs, targets, family exposure and models.
Each TRAIN row sees original2/original3 each100 times and original4/interior4 each50.
The actual five schedules must pass native preflight. No accepted checkpoint is
used to initialize fitting; C327 saved gradients are never training inputs.

The C326/C325/C324 training/evaluator/scorer/checkpoint interfaces and writer-side
schemas were inspected. C328 keeps native mean_last,14256 parameters/core3328,
64 slots,CPUfloat64,2threads,1200 updates of48 rows,fit RNG612000 and the original
mean CE/clipping/AdamW settings. First800 equality is an execution-integrity condition,
not an outcome-dependent selection. No ratio, switch-time, seed or budget search.

All original local/masked/order thresholds remain.90/.80/.35/.35/.80. Every candidate
seed must pass interior AND all original2..6 gates, increase both interior HOLDOUT
answer/pair counts strictly, and not decrease either pooled original2..6 count.
Length1 remains descriptive. All rescues/regressions and local cells are retained;
pooled accuracy cannot hide a failing seed. C327 local-gradient geometry is motivation
for a prospective LR test, not proof that this policy will work or of a prior cause.

## Diagnostic-parent writer/loader and protection audit

The immediate parent is C327's diagnostic primary summary AND execution envelope,
not C326's training schema. Both exact hashes and execution identity are fixed to
the accepted C327 run. The original diagnostic PASS/capability-false flags, manifest,
work, full5658 receipt, saved semantic completion and final1549 rereads are checked.
Both parent records must carry the same complete820-source/1549-input maps.

C327 wrote FOUR outputs:diagnostic-plan.json,gradients.pt,measurements.json and
validation-summary.json. With primary summary and envelope this adds SIX files,
not ten. New protection is826 sources=820+6own,1561 inputs=1549+6parent+6own.
The actual parent writer and semantic_recheck signature were reread. Canonical data
and saved logits come from the immutable C327 executor's fixed C326 ancestor path;
the required files must already be protected inherited inputs and have exact hashes.
C327.semantic_recheck(C327_out,C326_out,data,read_json) reconstructs its60 gradient
pairs and metrics under no_neural. No older recursive semantic verifier bodies or
parent model forwards are invoked. All inherited bytes remain checked.

Every new deciding-path file is protected:benchmark,executor,test,runner,launcher,
contract. Direct/lazy ancestor code includes C327/C326/C325/C324 and C308 optimizer,
all supplemental recovery helpers/tests and the immutable source/input maps. No
smaller inherited pin inventory or HEAD-reconstruction excuse is accepted.

Native unchanged R4 Windows read leases remain held through all worker phases,
with first-read reference hash checks and final uncached rereads ofALL1561 inputs.
Full5722 regression runs in a separate ordinary interpreter, not a scientific-wrapper
process. Only native preflight and complete regression success permit fitting.
All ten new models are evaluated and checkpoint-replayed. Eight child output files
are hash/size-bound before/after saved reconstruction and checked again before
summary/envelope creation. A fresh process checks every source/input/output byte,
exact unions, manifest, cohort, complete test receipt and fixed-gate bindings.
It is a byte verifier, not another model replay or optimization-history replay.

## Control-flow, launcher and remaining native scope

Production stages and the actual scientific_worker control function were exercised
with explicit synthetic parent/lease/model dependencies. The valid fixture follows
snapshot -> parent semantics -> native preflight -> regression -> fit -> saved
verification -> final rereads -> lease release. Regression failure never reaches
fitting. Saved mismatch prevents finalization; byte mutation is detected. The
controller invokes science then fresh verify once and preserves subprocess failures.

The unchanged active_v2 dispatcher selects the new launcher. Host/branch/HEAD/dirty
tracked tree/unique current ACTIVE/dependency/AST checks precede scientific logging
and publication. Named CLI options match the runner; the existing .venv-py31315
interpreter and unique local run folder are used. Standard log publication records
scientific execution HEAD separately from the descendant log-publication commit.
No CI, paid service, package installation, cache deletion or automatic retry is added.

Native Windows locks, authoritativePython3.13.15/Torch+cu130, real parent files,
full5722 historical regression and scientific ten-model FOLD training were NOT run
on the author host. They are enforced by the registered user execution, not assumed
passed by this review. Operational mismatches are SKIPPED; integrity failures stop
SAME C328. Finite scientific FAIL remains valid negative evidence. Publication-only
failure is repaired without refitting. Gate F remains NOT PASSED;C329 unregistered.
