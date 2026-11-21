# C327 post-authoring review

Review date: 2026-10-17 Japan time.
post_authoring_review = PASS
Source/preregistration review target HEAD:
461835dcf162f0de7d4828a6a4f6043e708bfdb7.
Acceptance base: c3aff2fe3a6067860d19e76903b8f50677984467.
This is authoring approval, not a scientific C327 result, a native Windows run or
a full historical-regression PASS. Use the subsequent final activation HEAD in the
user command, not this source-only review target.

## Independent committed-byte review

After publishing the complete source/tests/runner/launcher/preregistration commit,
all six own files were fetched again at the exact commit and read completely.
The three long Python files were read through consecutive complete line ranges.
Their Git blob IDs were compared with independently hashed local raw files used
for the post-review tests. All six match:

| File | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c327_gradient_alignment.py | 889cfce9a4a8108557ec5868a7626b431719359c |
| tools/c327_execution.py | d329092835a15f6d89b77640da9cb8b842050ae2 |
| tests_lm/test_v05_c327_gradient_alignment.py | 7bf872819a784a84080c63ba9ba05a3921093b18 |
| tools/run_c327.ps1 | f01ce679ee1ba4490e013ebe868471b0789626fb |
| tools/invoke_c327.ps1 | 8105732af980938c145b75e6c9b3cd635997a756 |
| docs/experiment-ledger-addendum-c327-preregistration.md | 9860abe5a62d462616035383efff31cecd04d444 |

The remote comparison against the acceptance base contains exactly these six added
files, with no edits or deletions to accepted sources/tests/logs/contracts. This
review and the activation handoff are subsequent documentation-only changes.
C326 acceptance is a separate prior commit; no result is rewritten by this review.

## Tests rerun after the remote reread

- Normal own suite: 48/48 PASS, zero failures/errors/skips; 2.198 seconds.
- CP932-default-text-open emulation: 48/48 PASS, zero failures/errors/skips;
  1.969 seconds. This is explicit default-open emulation, not native Windows.
- All three Python files compile/import; all six files are UTF-8 with no NUL.
- Recursive function/nested-code LOAD_GLOBAL and import-binding audit: zero
  undefined globals in the benchmark, execution helper and test module.
- Actual own unittest loader contains 48 tests. Additive-suite test uses the actual
  own loader plus an explicit synthetic 5610-case historical inventory; it checks
  total5658, unique IDs and duplicate rejection. It is not a real full5658 run.
- Manifest self-hash matches
  36fca7e0b0baea3b51adcaad167caa551033e0f802ab3f883d4f4f846cbc22ee.

Author environment: Linux Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5, two threads.
No PowerShell executable was available. No author-side native AST execution is
claimed; the mandatory dispatcher -> selected launcher -> runner ParseFile chain
is retained and source-reviewed for the user-side native execution.

The tests exercise actual Torch CE/autograd and a centered finite-difference check,
unused-tensor connectivity, unchanged parameters and nonaccumulating gradients.
Parallel, opposed, orthogonal, zero-norm and negative-dot-with-joint-descent cases
are covered. Reverse-order measurement, drift rejection, native tensor save/load,
complete60-record saved-geometry reconstruction, count/partition conservation and
saved-record tampering are checked with explicit fixtures.

Real temporary Git repositories, JSON/hash/source-LF-CRLF checks and failing
subprocess logs are exercised. Production stage ordering and the actual diagnostic
worker control function are tested with explicitly synthetic parent/lease/model
callbacks. Failed regression cannot reach cohort measurement. Controller runs
science then fresh verify once; there is no automatic retry. Those fixtures are
not native Windows, real-parent checkpoint measurements or historical regression.

## Scientific scope and measurement audit

C327 reuses ALL ten C326 final states: seeds326001..326005, epoch4 and batch4.
There is no checkpoint selection, new fitting, optimizer step or checkpoint write.
Each model has six matched original4/interior4 objectives: three fixed profile
slots and two languages. Each objective uses all96 TRAIN rows of one language in
unchanged order; HOLDOUT is not used to form gradients or select rows.

The actual C319 trained_readout hook implementation was reread. Native mean_last
keeps the autograd graph, counts grad-enabled forwards and restores hooks. C327
loads the exact parent state into an ephemeral native model, checks its fingerprint,
uses eval mode with autograd enabled, and checks unchanged weights/hooks/no .grad
accumulation. No accepted global or forward function is patched.

Every objective forward checks logits against its corresponding protected C326
TRAIN logits at maxabs1e-9 and identical argmax. Every gradient pair is computed in
old/interior order and then interior/old order, requiring repeated loss/gradient
agreement and identical connectivity. All240 forwards/gradient evaluations and
23040 row presentations are explicitly metered, including reverse repeats.
The fixed native preflight separately performs4forwards/4gradients/384rows on the
first registered model/profile/language before full regression; no optimizer exists.

Unused parameter tensors are retained as zero vector segments with connectivity
bits. Connected zero and unused tensors are not conflated. Parameter order, shapes,
unique names, total14256 and core3328 are validated. The disjoint core/read.*/other
partition reconciles with the all vector. Reader is specifically read.*, not every
output-head parameter. Dot products, norms, cosine and Euclidean negative-mean
first-order derivatives are reported; zero-norm cosine is null without an epsilon
or silent clamp. A negative dot alone is not called a harmful mean update.

PASS means complete diagnostic integrity, not a particular sign, conflict frequency
or model capability. The diagnostic observes terminal local geometry, not the full
training path, causal mechanism, finite-step improvement or actual AdamW motion.
It does not directly measure original-length-six gradients or explain every failed
gate. C326 remains VALID NEGATIVE and Gate F remains NOT PASSED.

## Parent writer, saved artifacts and dependency protection

The actual C326 checkpoint/evaluation writers, load_bundle and semantic_recheck were
reread, together with its primary-summary/envelope construction. C327 consumes their
actual schema/keys, exact accepted execution identity and pinned hashes. Both the
primary summary AND execution envelope are mandatory; they must agree on the full
814-source/1533-input union, original manifest/work and full5610-test completion.
All inherited source Git blobs and raw input bytes are checked, including the
C324 supplemental recovery helpers/tests. No omitted direct dependency is excused.

Ten immediate-parent files (summary, eight outputs, envelope) and six own files
extend protection to820sources/1549inputs. The own benchmark/executor/tests/launcher/
runner/contract and all direct/lazy inherited dependencies are covered. C326's
immutable executor loads its immutable C325/R4/R6 helpers without global patching.

Unchanged C326.semantic_recheck reconstructs the immediate parent's complete saved
plan/metrics/summary from checkpoints/evaluations under no_neural. This parent
verification does not refit, perform a model forward or recursively rerun older
semantic validators. Accepted older identities and every inherited byte remain
checked. The subsequent diagnostic's240forward calls are new, explicitly metered work.

Native Windows R4 read leases stay held through all worker phases; first hash reads
are independently checked, and all1549 inputs receive final uncached rereads.
The full5658-test suite runs in a separate ordinary interpreter without science
wrappers. Only full success permits cohort measurement. The saved gradients are
reread with weights_only=True; geometry, complete identities, conservation and CE
from protected parent logits are reconstructed. This saved pass is not falsely
called a second independent autograd run.

All four child output hashes/sizes are bound immediately before and after semantic
reconstruction and checked again before summary/envelope creation. A fresh process
verifies exact parent/child source/input unions, every source/input/output byte,
manifest, cohort, zero-update work and complete regression receipt. Both child
primary and envelope carry the complete820/1549 union. The fresh byte verifier
is not an extra gradient measurement or model replay.

## Launcher and stopping boundaries

Host/branch/ExpectedHead/tracked-tree/unique ACTIVE/dependency/AST checks precede
scientific logging and publication. The unchanged active_v2 dispatcher parses the
selected launcher; that launcher parses itself and run_c327.ps1. Named Python CLI
options, existing .venv-py31315 interpreter, unique local run folders and publication
paths match the contract. Python independently guards branch/HEAD/current C327.

Source/input/test/nonfinite/logit/gradient/state/semantic/envelope failure stops
SAME C327, preserving the attempt. Positive, negative or zero measured alignment is
not an execution failure and never authorizes refitting. Publication-only failure
is repaired without repeating diagnostics. No CI, package reinstall, paid service,
artifact deletion, old-source mutation or C328 activation is introduced.
Native Windows locking, authoritative runtime, real parent data, full5658 historical
regression and actual FOLD gradient measurements remain unperformed by the author;
they must pass the registered user execution and are not assumed successful here.
