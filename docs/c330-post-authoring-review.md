# C330 post-authoring review

Review date:2026-10-17 Japan time.
post_authoring_review = PASS
Committed source/preregistration review target:
a1d447e6b9f0d1a05f1dfa56a40223ea4c5c3c4c.
Acceptance base:a7a36bb212656f08bd8d1c5402512ce28acb1e00.
This is authoring approval,not a native Windows/full5818 regression result or a
scientific C330 verdict. Use the subsequent activation HEAD in the user command.

## Complete remote reread and local-byte identity

After the six-file source/test/runner/launcher/preregistration commit was published,
all six files were retrieved again at the exact target and read through EOF. Long
files were read in consecutive complete ranges. Returned Git blob identities match
independently calculated hashes of the local raw bytes used for the checks below:

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c330_saved_gate_localization.py|73c30cba137b4d11a9ac39c8f3702bdd0b2e6baf|
|tools/c330_execution.py|1fb5fb47e1e9998cd8ec3a38b25afeb7ec44b31a|
|tests_lm/test_v05_c330_saved_gate_localization.py|9329faf739a7d2f033e44c943b2ec2551ccf7d51|
|tools/run_c330.ps1|e15dd6ea2ff46d11761f915d61559d6d12e37bf8|
|tools/invoke_c330.ps1|8c188f783bae1325aeea06301490005fa378c473|
|docs/experiment-ledger-addendum-c330-preregistration.md|8e2cea381e1de3f6bae0a2e6f9568bb3dc9bd8c0|

Remote comparison against the acceptance commit shows exactly these six additions,
with no edited/deleted accepted source,test,contract,log or dispatcher. C329
acceptance is separate. This review and activation are subsequent documentation only.

## Checks after the committed-file reread

Normal own suite:48/48 PASS;failures/errors/skips0;5.202seconds.
CP932-default-text-open emulation:48/48 PASS;failures/errors/skips0;4.955seconds.
Both builtins.open and io.open supplied CP932 only for unspecified text encoding;
explicit encoding and binary modes were preserved. This is not a native locale test.
All six files are valid UTF-8 without NUL;all three Python files compile/import.
Recursive LOAD_GLOBAL checks of189 function/method/nested code objects found zero
undefined global names. The actual own loader contains48tests. Manifest self-hash:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
Author environment:Linux Python3.13.5. The own tests use Python metric/file/control
fixtures,not FOLD fitting. No native Windows,real-parent-files or full5818historical
suite success is claimed. No PowerShell executable was available;author-side native
AST execution is not claimed. The mandatory user-side AST chain is retained.

## Scientific scope and scorer writer audit

C329's actual analyze/run_science/semantic_recheck and the execution helper's tuple,
suite and parent adapter were reread. The parent evaluation schema contains five
trajectories and ten checkpoint records,not ten independent fits. The child uses
unchanged C329.semantic_recheck(out,data,old,new,cx,read) under no_neural,then reads
measurements.json and validation-summary.json through its own called loader.
It does not load model state into a neural module or run inference in the diagnostic.
Parent semantic verification still reads saved tensors and reconstructs the existing
raw-logit metrics;this is explicit separately scoped work,not free computation.

C270.score's full local/order writer was read,including grouping by split,language,
entity subset,fact order and value/query identities. The child checks exactly those
fields and denominators,integer normal/pair/masked counts,finite NLL,feasible joint
counts and collapsed pairs. It recomputes each unchanged criterion and all local,
order,profile-total,domain and seed flags,then reconciles per-seed/domain HOLDOUT
counts,gains and the original composite verdict with the accepted parent summary.
It does not pretend that aggregate cells reconstruct individual rescued ANSWERS.
The parent raw-logit semantic validator establishes those existing contrasts first.

C304.score_length and C321.score_new mappings were read with C267 entity subsets.
The scorer slots tripled/shared_prefix2/shared_suffix2 are opaque labels;the real
input profiles are repeat/shared_prefix/shared_suffix for original2..6 and
u_dominant/balanced/v_dominant for interior4. Both names are preserved in output.
Original5/6 name families remain marked unseen in fitting even on logical TRAIN rows.
No profile label is silently treated as a literal name length or renamed to make
an evaluation appear trained. Original1 remains excluded only because it was not
part of the parent gate,not because a measured result was inconvenient.

The four local thresholds remain.90/.80/.35/.35 and the both-order threshold.80.
All4320local/2160order cells across every seed/checkpoint/domain are retained,
including successes. Exclusive pass/normal_binding_only/mask_only/mixed categories
coexist with overlapping individual failed criteria. Both-order failures remain a
separate correlated assessment,not extra independent examples. Exact coordinate
matching yields2160local/1080order transitions with conserved rescue,regression,
persistent-fail and stable-pass counts. No cell sorting,seed selection,mean override
or threshold softening changes a parent verdict. A diagnostic PASS is integrity,
not a capability PASS or evidence of a causal mechanism.

## Tests and limits of fixtures

Full-inventory synthetic score fixtures exercise every domain,profile,split,language,
entity set and fact order. Tests cover all four patterns,exact threshold boundaries,
unknown/missing/duplicate coordinates,false pass flags,normal/pair/order feasibility,
masked-count recovery,overlapping criteria and exact matched transitions. They
reconcile parent flags/counts and reject attempted post-hoc gate/count changes.

The actual diagnostic run/loader/writer and saved reconstruction execute against
complete synthetic parent JSON on disk;all four outputs roundtrip and tampering is
rejected. Real Git temporary repositories,strict UTF8 JSON,LF/CRLF byte identity,
exclusive writes,subprocess CLI errors and no-auto-retry paths are exercised.
The actual scientific_worker control flow is exercised with explicitly synthetic
parent,lease,runtime and diagnostic callbacks. Regression failure never reaches
diagnosis;successful diagnosis writes PASS with capability_gate_applicable=false
while retaining its synthetic parent's negative result. This is not a native lock
or actual checkpoint experiment. Existing48tests pass without new exclusions.
The suite fixture uses the real48-test loader plus an explicitly synthetic5770-ID
inventory to test5818unique cases;it is not execution of the historical5770tests.
Source assertions inspect their exact target functions,not comments in a caller.

## Complete dependency, execution and saved-result coverage

Immediate parent is the exact accepted C329 science summary plus mandatory envelope:
execution f8582ca34bd7e10c7403713e935debe94720dfde;
summary89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a;
envelope6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Validate negative status,valid execution,paired success1/5,manifest/work,full5770
receipt,saved semantics and1577final rereads. Both parent records must carry the
same complete832source/1577input maps. Eight outputs plus primary/envelope addTEN
files;with six own files protection becomes838sources/1593inputs. Every own file
and direct/lazy inherited deciding dependency remains pinned;no smaller fallback.

Helper ordering is e329/e328/e327/e326/legacy/r4/r6. The C329 suite is called with
its actual seven-argument signature;native runtime comes from e326. Bootstrap bytes
are verified before import. C329/C328/C326/C325/C324/C321/C304/C270/C267 and native
recovery dependencies inherit protection. No accepted module global is patched.
Parent semantic verification is immediate-only;older semantic bodies are not
recursively rerun but every inherited byte is still checked.

Unchanged R4 native read leases span the worker. Initial independent reference hashes
and all1593final uncached rereads remain mandatory. Full5818regression runs unchanged
in a separate ordinary interpreter before diagnosis under no_neural. No neural
preflight is added merely to this saved-only experiment. Four child output files
are hash/size-bound before/after saved reconstruction and checked before writing
primary/envelope. A fresh process verifies complete maps and every source/input/
output byte,parent identity,manifest,regression and conservation,and reconstructs
the child from parent JSON again. This is not a new model or optimizer replay.

## Launcher and approval boundary

User command parses invoke_active_v2;the unchanged dispatcher parses its selected
invoke_c330;the launcher parses itself and run_c330. Host,branch,ExpectedHead,
tracked tree,unique Formal ACTIVE and dependency checks precede logging/publication.
Runner points to .venv-py31315 and tools/c330_execution.py with correct named CLI
arguments. Local c330-localization directory and c330/latest.* publication agree.
Scientific model-criterion failures are diagnostic data,not a reason to refit.
Schema/count/parent/source/input/test/semantic/envelope failures stop SAME C330;
no automatic retry,no C331. Publication-only failure is repaired without rerunning
science. Native full5818and true-parent validation remain required in the user's
registered execution. No CI,paid service,reinstall,artifact deletion or Gate F claim.
