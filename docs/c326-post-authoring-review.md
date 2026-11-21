# C326 post-authoring review

Review date: 2026-10-16 (Japan time).
post_authoring_review = PASS
Source/preregistration review target HEAD:
895a6e29416a88a70cdd5cfb4cd6ab9444227467.
Acceptance base: 1a8d15e46aa0b661d5570bed662e67aa1760fc77.
This is authoring approval, NOT a C326 scientific verdict or native full-regression
PASS. Use the subsequent activation HEAD in the user command.

## Independent committed-byte review

After the complete source/tests/runner/launcher/preregistration commit was published,
all six own files were fetched again at the exact commit and read in full. The three
long Python files were read in consecutive complete ranges through their EOFs.
Returned Git blob IDs were compared with independently computed Git blob hashes of
the local raw files used for the tests below. Every file matched:

| File | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c326_mixing_granularity.py | 1090c13372720abf9ec2a14941bbce34f436df98 |
| tools/c326_execution.py | e4808721464a20e87f08e16b4f47a7c88ca40ad0 |
| tests_lm/test_v05_c326_mixing_granularity.py | ef26626ddce409222644d43a861efbac049718cd |
| tools/run_c326.ps1 | c36ace107f75a857a9224a10adc9bd504159b398 |
| tools/invoke_c326.ps1 | 11f146c320a3ab2d70bbbfd65c5442784e2bd5dd |
| docs/experiment-ledger-addendum-c326-preregistration.md | e3b50104bc82bd9d73dfd3f96eeca634a1ef7d4c |

The remote comparison against the acceptance base showed exactly these six added
files, with zero deletions or edits to accepted source/tests/logs/contracts.
This review and activation are subsequent documentation-only changes. The existing
active dispatcher and C325 acceptance are not rewritten to change a result.

## Checks rerun after committed-byte comparison

- Own suite: 64/64 PASS, zero failures/errors/skips; 5.396 seconds.
- CP932-default-file-open emulation: 64/64 PASS, zero failures/errors/skips;
  4.221 seconds. builtins.open and io.open supplied CP932 only for otherwise
  unspecified text encodings. This is not a native Windows run or locale claim.
- All three new Python files compiled and imported; all six files are UTF-8 and
  contain no NUL. Recursive function/nested-code LOAD_GLOBAL and import-binding
  audit found zero undefined global names in benchmark, execution helper and tests.
- Actual own unittest loader contains 64 tests. The additive-suite test builds an
  explicit synthetic 5546-case historical inventory plus the real own loader and
  checks total5610, distinct IDs and rejection of duplicate historical IDs.
- Manifest self-hash matches
  2be1555cf0296e55f5adf2e11302d6112b9b49836781199fcb3fc126d384871e.

Environment: Linux Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5, two Torch threads.
Tests exercise real temporary Git repositories, files/JSON/hashes, subprocess error
preservation, actual Torch CE/AdamW/clipping arithmetic, deterministic integral flow,
actual production stage ordering, and the actual scientific_worker control function
with explicitly synthetic parent/lease/model dependencies. Those fixtures are NOT
native Windows, the full5610 historical suite or ten-model scientific fitting.
No PowerShell executable was available, so native author-side AST execution is not
claimed. The mandatory dispatcher -> launcher -> runner AST chain remains intact.

## Scientific-variable audit

The control is exactly the C325 mixed4 whole-epoch rule, applied to fresh326001..326005
initial states and326101..326105 order seeds. The candidate changes only temporal
family assignment within length-four updates. Both arms use the same logical row
order, targets, intact query pairs, length/profile schedule, total row presentations,
per-pair/per-profile old/interior exposure, native mean_last, model, optimizer and
precision. No accepted model/global/forward or optimizer policy is patched.

Allocation uses only schedule identities, never text/labels/losses/HOLDOUT. Per-profile
old quotas are inherited exactly from the control. Deterministic Dinic max flow uses
chronological updates and sorted pair edges, and the resulting mask is recounted.
Each pair/profile has identical family exposure between arms. Every row sees old4
50 times and interior4 50 times; length2/3 remain original100 each. All five registered
order-seed software schedules pass. Each of400 length-four updates has11,12 or13 old
pairs; counts48,304,48 respectively. This is not falsely described as12/12 every batch.
The actual runtime preflight separately checks all five real plans, actual inherited
C325 control-mask parity and native TRAIN/readout/gradient checks before fitting.

The pure-original one-update toy path is bit-exact to an explicit CE/AdamW/clipping
reference. A mixed mask changes updates; both members of a pair receive one family;
nonfinite logits stop. Allocation failure has no alternative schedule or fallback.
The allocator does not consume training RNG, mutate logical events or inspect model
outputs. It is data scheduling, not a new neural architecture or an output oracle.

Existing C324 evaluators, raw-logit contracts, query-pair contrasts, scorers and
checkpoint fingerprints are reused through the immutable C325/C324 modules. C326
owns fresh cohort, fit masks/traces, bundle schemas, analysis and gate. Per-seed
candidate interior and original2..6 gates are required, with positive interior answer
AND pair gains and nonnegative pooled original answer AND pair gains. The threshold
set remains .90/.80/.35/.35/.80 at every local/masked/order condition. No pooled mean
can override a failed seed. No ratio, seed, learning-rate or threshold search.

## Parent writer/loader and source coverage

The actual C325 writer, saved model/evaluation schemas and semantic_recheck were
reread, as was its primary-summary/execution-envelope construction. C326's adapter
uses their actual keys and semantics, not similar-sounding schema assumptions.
Parent is the accepted C325 primary summary AND envelope at the exact recorded
SHA256 values and execution HEAD f95895313da81634976d0ff2761efdd793888c2b.

Before fitting, both parent records must agree on the complete808-source/1517-input
union. Their identity, scientific FAIL, manifest/work, full5546 regression receipt,
immediate semantic completion and final1517 rereads are checked. All inherited source
Git blobs and input bytes are checked. The eight parent outputs, parent summary and
envelope add ten files, and six own files extend protection to814sources/1533inputs.
Bootstrap and lazy deciding-path dependencies include the immutable C325 execution
helper, C325/C324 benchmarks, R4 lock helper, R6 helper and inherited supplemental tests.
No omission is excused merely because a prior commit could reconstruct it.

The unchanged C325.semantic_recheck loads its fixed checkpoints/evaluations and
reconstructs full saved measurements/plan/summary under no_neural. This does NOT
refit or run parent model forwards. Older semantic validators are not recursively
reexecuted: their accepted evidence and every inherited byte remain checked. This
scope is explicit, not described as fresh ancestor semantic execution.

Inputs retain unchanged R4 native Windows read leases through the worker; no unlocked
fallback or cross-run cache. Full regression runs in an ordinary separate process
with no scientific wrappers. Only complete5610 success permits fitting. Actual ten
new-model checkpoint replays precede saved child semantic reconstruction. All eight
child output files are hash/size-bound before and after reconstruction and checked
again before result/envelope creation. All1533 inputs receive final uncached rereads.
A fresh process checks exact parent/child source/input unions, every source/input byte,
all output hashes/sizes, manifest, cohort, fixed-gate bindings and full test receipt.
This fresh byte verifier is not falsely described as another independent model replay.

## Failure paths and launcher

The actual production worker fixture checks snapshot -> parent semantics -> native
preflight -> separate regression -> fit -> saved semantic verification -> final
rereads -> lease release. Its failed-regression variant never reaches fitting.
Controller calls science then fresh verify once, retaining nonzero process exits.
Saved-result mismatch stops before finalization, and output tampering is rejected.

PowerShell launcher verifies host, branch, tracked tree, ExpectedHead and unique
current C326 before scientific logging/publication. The unchanged active_v2 entry
parses the selected launcher; launcher parses itself and run_c326.ps1. Named Python
CLI options match the runner; existing .venv-py31315 runtime and unique local runs
folders are used. Python guard independently checks the same branch/HEAD/ACTIVE.

Scientific finite FAIL remains valid negative evidence, not an automatic retry.
Source/input/flow/test/schema/nonfinite/replay/semantic/envelope failure stops SAME
C326. Publication-only failure is repaired without refitting. No CI, paid service,
package installation, cache deletion, old result mutation or C327 activation.
Author native Windows/full5610/real-parent-files/FOLD-fitting execution remains
unperformed; these are enforced by the registered user run, not assumed passed.
