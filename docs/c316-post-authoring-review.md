# C316 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review and executed local software tests,NOT actual FOLD science.
Review target:81b37e65a138c19edf22a90ebd1f9871ca02f56a.
Acceptance base:0d83544dfeb835a5c74f9690008598872f3e0f2d.

## Committed bytes and change scope

All six OWN files were fetched after commit from the immutable target and reread. Source356lines
and test399lines were covered by complete consecutive ranges;the other four files were read in
full. Returned whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c316_single_mix_replication.py:3d15bda5b0c4f3f487548cd6b92d3b1281febb76;25339bytes.
- tests_lm/test_v05_c316_single_mix_replication.py:ad36f60f64c69def2a925bc29f4be2d6d09d4dc6;28466bytes.
- tools/run_c316.ps1:49d801d9c5928d9e5ef9a4a3d41102d6ecda469b;4646bytes.
- tools/invoke_c316.ps1:46ed200c8464f45a328d71255641f05c723155ac;7596bytes.
- docs/experiment-ledger-addendum-c316-preregistration.md:ff3d98caf8dbc1fda1a23566f1b47da465ba6a9a;7641bytes.
- docs/v5b-single-mix-replication-v0.1.md:c44304ce54f244a424a9de8901f9d340ae478ca5;1007bytes.

The remote acceptance-to-authoring comparison contains exactly these six additions. No accepted
source,test,log,preregistration or dispatcher was changed. Activation must retain these six blobs.

## Executed checks after remote/local matching

An initial post-match whole-suite call reached the local45second execution limit before completion;
it is NOT counted as a completed PASS. The unchanged test module was then run in two explicit
nonoverlapping partitions,methods01..16 and17..32,under each default-encoding mode:

- Normal:16/16 PASS18.515s plus16/16 PASS12.764s.
- CP932-default emulation:16/16 PASS20.008s plus16/16 PASS13.385s.

All32 distinct test IDs appear exactly once across the two completed partitions in each mode.
All four completed runs have zero failures/errors and successful exit codes. The CP932 patch
covers module import,setup,test methods and teardown in each partition. No test was omitted or
modified to avoid the timeout. Pre-commit results are not substituted for these post-match runs.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No PowerShell executable is installed.
CP932 default emulation is not full Windows or console emulation. Terminal cleanup messages
following the unittest results do not change the recorded successful process/test outcomes.

All six hashes were rechecked after testing. UTF8/noNUL;both Python files and all3 embedded runner
blocks compile. Recursive symtable/import-binding audit found0 unresolved globals after allowing
module bindings,builtins and standard module globals. Manifest self-hash matches:
e77e05efffb480bce89fb9b16071babfff15dd533d0ac6677798478fd2103718.
42 launcher paths are ordered C315..C274. Postcheck paths=sys.argv[2:44],head[44],argc45.
Own32/modules201/loaded5118/focused5117. Sole inherited exact C204 exclusion unchanged.

## Behavioral checks and limitations

Canonical synthetic construction matches C315 DATA and full1..6 PROMPTS SHA256. Every new seed's
plans preserve complete epochs,intact query pairs,per-length exposures and the identical logical
order across arms. The control matches the old C312 random schedule. Independent candidate
schedule examples and unchanged global RNG checks pass. One-character evaluation remains one
profile,not three duplicates;the real inherited evaluator produces144forwards/13824rows.

Test10 extracts the exact accepted C315 fit/scheduler functions and executes both full1200step
arms on controlled models. Child optimize and parent fit match every loss,optimizer-rate trace,
gradient receiver trace,schedule and final weight fingerprint. This exercises actual optimization,
not only source-string equality. Test12 executes actual child train_one and parent final evaluation/
strict replay on a toy model,checking1344+144 forwards and exact restoration. Changed states fail.
The synthetic toy's first token deliberately encodes a target for software-loop testing;it is
not a dataset or performance claim for FOLD. Padded toy parameter counts are not an efficiency claim.

Actual runtime_preflight executes with controlled bilingual inputs and model factories. Source/
input protection uses742/1393 temporary-file fixtures;missing local helper coverage is rejected.
All42 summary hash positions are tested for rejection BEFORE parent verifier dispatch. Parent
identity/outcome/schema mismatches fail. The production child run invokes its actual loader once,
after all10 train dispatches and before all10 strict replay dispatches. JSON/tensor roundtrip,
no-overwrite,wrong-HEAD and tampering even after resealing a descriptor are tested. New-only six
primary failure remains FAIL and cannot be rescued by old parent successes or length1 diagnostics.
Semantic suite tests construct5118 synthetic IDs,retain the exact5117 and reject duplicates;
they do NOT run the actual inherited5117 tests.

Local C315 support is a fetched exact function slice,not a complete parent module or repository,
and is NOT committed. Tests extract its AST into isolated namespaces with original constants.
The user's checkout extracts these functions from the full accepted C315 file. The scientific
runtime uses ordinary imports of full accepted modules,not AST execution or parent monkeypatches.
Parent archives,Git,scorers and model interfaces are substituted locally where unavailable.

## Scientific path and parent writer contract

C315 saves final prediction records in fold-c315-single-mix-eval-v1 and the ordered learned states
in fold-c315-single-mix-models-v1. It also writes the canonical dataset and all1..6 prompt JSONs.
C316 checks42 ordered summary hashes before C315.verify_artifacts with41 ancestors and the exact
accepted scientific HEAD. The fixed summary seals all7 artifacts;the original3/4 six outcomes,
ordered ten flags,matched pairs and replays remain explicit. The actual parent verifier reconstructs
its learning traces,final scores and prior protection chain. Only verified dataset/prompts feed
new training. No prior learned state or predicted answer initializes or teaches the new models.

Reuse the actual seed-agnostic C315 plan_for_order,schedule_stats,training_tables,validate_prompts,
validate_raw,evaluate and replay. C315's fixed-seed fit/schedule/factory/analyzer are NOT called
with new seeds or globally patched. Child optimize owns an explicit schedule and otherwise retains
C315's operation order,loss,clipping,optimizer and fixed fitRNG. Actual C308 optimizer grouping
and verification remain in use. New factories verify full/core identity,parameter counts and
independent storage. Each discarded common-input probe compares initial logits,preclip gradients
and first update;the real first rendered batches and losses may legitimately differ by arm.

Sole direct repository import:C315. Its context exposes C314/C313/C312,C310 no-neural guard,
C304 model/scorer,C308 optimizer,C296 pairs,C287 normalizer and backend. Existing736 source pins/
1379 inputs and C315.PINNED/C304.PINNED plus actual local helper/factory-language coverage remain.
OWN6 plus8 parent files gives742/1393. No source-protection waiver or new exclusion is authorized.
The child model/evaluation schemas use new identities. C315.replay accepts these record fields
without a fixed old-seed requirement;C316's own loader validates the new ordered checkpoint schema.

## Work and execution boundary

10new models,12000updates,576000training rows,14880forwards,852480row presentations,59520core calls,
10strict state loads,one new10state bundle write/read,network0. Final evaluation and strict replay
are included. Operational probes,local tests and recursive parent reconstruction are separate work.
Candidate replaces part of2..4 exposures with length1,so dilution/profile-timing confounds remain.
New seeds are new initial/order conditions,not new tasks. No six result has been observed locally.

Not executed here:Windows PowerShell ParseFile,the user's42 actual parent archives/protected bytes,
the actual5117 inherited regression suite,or the ten scientific FOLD training/evaluation/replay runs.
All remain mandatory Validate/Execute gates. Preserve the unchanged dispatcher/selected-launcher/
runner ParseFile chain. This review authorizes the guarded launcher only. Valid primary failure
is a valid negative;integrity failures repair SAME C316. C317 waits for formal C316 judgment.
