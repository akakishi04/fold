# C336 post-authoring review

Date:2026-10-20 Japan time.
post_authoring_review = PASS
Committed source/preregistration review target:
a059a5228c7bc2b8f0a20f56469ccfdd831ea66e.
Acceptance base:8984740dcc538cf785ca2fdc96db735b9ff8a4a1.
This is authoring approval,not native Windows/full6090 regression or a C336 outcome.
Use the subsequent documentation-only activation HEAD in the user command.

## Committed-byte reread and identity

All six files were fetched at the exact source commit and read through EOF.
Benchmark1..150,151..260;executor1..140,141..280,281..408;
tests1..120,121..240,241..350,351..419;complete21-line runner and58-line launcher;
contract1..95,96..169. Returned Git blobs match independently calculated hashes of
the local raw bytes used for the post-reread checks below.

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c336_saved_query_order_patterns.py|78e33df0faed7cddcc888d4c068f8026327d99e8|
|tools/c336_execution.py|7c79c0d66afe3d1e31ebd61f58999cb9f7cdfa0c|
|tests_lm/test_v05_c336_saved_query_order_patterns.py|02bb7e8fe883c940f525369308a09b608ee4490d|
|tools/run_c336.ps1|ccaf326724f7d29b14f53e0b0a68034d54f00b0e|
|tools/invoke_c336.ps1|da097874586a3369494f3a81460c1752ab48ac46|
|docs/experiment-ledger-addendum-c336-preregistration.md|eb909f082dfd5f71dc0ed6294a1a32398a12d4d4|

Remote compare confirms exactly these six additions relative to the acceptance base.
No accepted source,test,contract,log or dispatcher was edited. No post-publication
source amendment was necessary. Acceptance,source and review/activation are separate.

## Actual post-reread checks and limits

Normal32/32 PASS,0failures/errors/skips,5.70032420199982seconds.
CP932-default-text-open emulation32/32 PASS,0failures/errors/skips,5.896776153000019seconds.
Each condition ran in a separate author Python invocation. The emulation wraps both
builtins.open and io.open,substituting CP932 only for text encoding None/locale;
explicit UTF8 and binary modes remain unchanged. This is not native Windows testing.
All six files decode UTF8,contain no NUL and have no trailing whitespace. All three
Python files compile/import. Recursive LOAD_GLOBAL audit of185nested code objects
(excluding the three module roots) finds0undefined globals. Actual32unique test IDs
have ordered digest96ce8e07f180137d2035601083aade23244cac87e83f23dfae3eff23940a2b73.
Manifest self-hash validates:
e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.

Mutation control:an in-memory classify wrapper changes first_fact to last_fact.
Both test07(exhaustive independent classification) and test08(order orientation)
fail their assertions:2tests,2expected failures,0errors/skips,0.591380701999924seconds.
The original function is restored,manifest validates,and all six file SHA256values
remain unchanged. These intentional mutant failures are not normal-suite failures.

Author environment:LinuxPython3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,2Torch threads for
tests. Targeted authored-file tree,not a complete repository checkout. No package
installation,paidservice or CI. No pwsh executable was found;native PowerShell AST
execution was not performed. Mandatory user-side dispatcher/launcher/runner AST
checks remain. These tests do NOT establish Windows6090historical success,actual
C335tensor/model outcomes,or independent reconstruction of the user's local artifacts.

## Scientific-path audit

The unchanged C335 writer and semantic_recheck signatures are the parent contract.
C335evaluations contain ordered10records with native evaluation/replay,actual state
fingerprints and forward receipts. Child parent validation requires scientificFAIL
with executionvalid/capabilityapplicable,not the older diagnosticPASS schema.
Immediate parent reconstruction verifies saved traces,checkpoint state fingerprints,
full raw evaluator views,scorers and the negative capability verdict. It does not
replay24000updates. Child analysis never constructs or runs a neural model.

Dataset semantics were checked against the existing source row contracts:two distinct
entities,opposing binary values,two queries and both fact orders. The child groups
by explicit logical identities and retains positions into saved raw tensors;it does
not assume query rows are adjacent in the real dataset. Rows must cover each of the
four query/order slots exactly once. Source targets are validated before offline
scoring. Ground truth never replaces a model prediction. The first/last categories
follow actual fact permutation,not target rank or output-dependent selection.

All256logits participate in argmax. A third output class remains a third class;it is
not projected to0/1. The seven categories are exclusive,including query-swapped and
fixed observed-value behaviors. Other-class takes precedence over a constant invalid
class. A stable query response need not be correct. The taxonomy is behavioral,not
a causal statement about network internals,optimizer failure or memorization.

All10states,18normal domain/profile combinations,bothsplits/languages and all logical
value/order/query combinations are retained. Original1/masked views remain in full
parent/replay checks but are outside the new taxonomy. The analysis reconciles all
fields of all30parent HOLDOUT contrasts,including rescued/regressed answer and pair
counts. Equal gains or equal aggregate accuracies alone cannot satisfy this check.
The complete parent validation_summary is preserved;C335 remains VALID NEGATIVE.
TRAIN is a logical-split label,not evidence every evaluated name variant was fitted.

## Actual software coverage and synthetic boundaries

The real classify function is checked against an independent property-based reference
for all16binary four-response patterns in both target orientations. Tests distinguish
first/last tracking,query reversal,value lock,other-class and mixed behavior. Explicit
controls retain rescues/regressions under a tied total and require both answers for
pair success. Invalid prediction types,targets,language,duplicate/missing slots,
nonfinite/incorrectly shaped logits and incomplete cohorts are rejected.

The full12960-quad/6480-transition/720-stratum production analysis runs over synthetic
Torch logits and logical rows. Its parent contrast expectations are calculated by a
separate direct per-answer/per-pair routine. Legacy raw-validator/replay/parent-summary
collaborators are explicitly synthetic,not actual accepted FOLD scorer execution.
The real safe Torch loader,exclusive four-JSON writer and semantic reconstruction
run against temporary files;changed saved transitions and changed parent rescue
counts are rejected. No scientific capability outcome is inferred from this fixture.

A real453-temporary-proof-file inventory verifies mandatory parent regression files.
The strengthened snapshot test uses871real temporary source files,explicit synthetic
inherited maps and actual parent/child files to exercise the production union code:
877sources/4360inputs,without mutating inherited maps. Ancestor snapshot/legacy helpers
are collaborators,not a claim of reconstructing the actual full repository provenance.
Exact immediate-parent four-argument loader dispatch and protected-file membership
are tested. A missing deciding evaluations.pt input fails closed.

Own actual32-test loader is appended to an explicitly synthetic6058base inventory.
The collector/fresh verifier execute against226synthetic module receipts and a labeled
accepted-validator double,checking452delegated validations,changed log bytes and
missing/duplicate/reordered IDs. Real accepted R1.2 PID/marker semantics are reused
unchanged by production and remain covered in the user's inherited suite. No actual
6090historical tests or226real module subprocesses were run by this author check.

Production scientific_worker and verify_outputs function paths run with explicit
synthetic locks/runtime/source maps and diagnosis callbacks. They verify regression
before diagnosis,final rereads before lease release,diagnostic-only flags,and rejection
of a forged capability claim. Other tests use real temporary Git,strict JSON,UTF8,
exclusive writes,LF/CRLF source hashes,a real nonzero subprocess and actual CLI parsing.
Failure tests prohibit diagnosis after regression failure and prohibit automatic retry.

## Dependency, evidence and execution review

C335executor49e2a9c8103851ccfffaa283d4fd8943170fbaf3 is checked before import. Its
helper tuple(C334executor,C334helperdict) is explicitly adapted;no wrong numeric helper
index is guessed. Inherited c330 identifies canonical C329data. Parent semantic call
is C335.semantic_recheck(C335science,C329data,cx,read),not C334's six-argument crossover.
All deciding repository imports are inherited C335/C332/C334/evaluator/data/recovery
chains or the six owned files. The inspected C323 source is not a new runtime dependency.

Parent871source/3893input maps are reconstructed unchanged. Add all461parent files:
6science+summary+envelope+453testproofs. Verify exact6058test identities/success/PID/log
semantics through unchanged accepted helpers. Then add six child sources. No smaller
map fallback,unprotected lazy helper or omission of supplemental evidence is allowed.
Native R4 leases,independent initial hashes and all4360final uncached rereads remain.
Four output hashes/sizes are bound around reconstruction and before result/envelope
writing. A fresh process reconstructs parent and child semantics without model inference.

New regression preserves exact6058IDs and appends32,for6090tests/226modules. The sole
inherited exactC204mutable-ACTIVE exclusion is unchanged;no new skip/exclusion/retry.
Generic module ABI stays fold-c330-r1-module-v2 with NEW C336HEAD/plan/index/module.
C336 owns guards and CLI,while unchanged R1.2 validates direct/immediate-child process
relationships and exact log markers. No equal-PID assumption or parent CLI misuse.

Both PowerShell scripts were fully read:branch/HEAD/dirty/ACTIVE/dependency/ParseFile
checks precede creation of the scientific log. Publication is C336 and output prefix
c336-query-order. The unchanged active_v2 selects the launcher;the supplied command
parses the dispatcher. Native PowerShell execution remains user-side,not author-proven.

The final review/ACTIVE commit changes documentation only. Native6090tests,actual
C335source reconstruction,all classifications/reconciliations,4360rereads and fresh
verification remain required. Technical failure stays SAME C336. DiagnosticPASS does
not change C335negative or pass Gate F. No C337,production adoption,CI,paidservice,
installation,artifact deletion,old-science mutation or post-hoc selection authorized.
