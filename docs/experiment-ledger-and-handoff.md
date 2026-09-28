# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative scientific runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
For current C270 execution use the versioned PowerShell7 entry described below,not the historical generic dispatcher.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C269 ACCEPTED PASS (bounded query-span capability). C270 ACTIVE / NOT YET JUDGED. C271 NOT REGISTERED.**
C269 span_query passed5/5 against the fixed gate;matched eos_query control passed4/5.
C270-v5b-frozen-triple-identifiers is now the sole ACTIVE experiment. It freezes all ten C269 final
states and tests transfer to unseen three-character familiar-byte identifier strings.
C268 remains ACCEPTED VALID NEGATIVE;all earlier verdicts/recovery records are preserved.
No Gate F promotion,production adoption,arbitrary-name claim or C271 registration.

## Latest accepted science — C269

Acceptance:docs/experiment-ledger-addendum-c269-c270.md.
Execution:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Published log:1c34b373ad9610dddcab2e7e54294fd5d4fe7cef.
Summary:runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json.
Summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.
run_execution_valid=True;scientific_status=PASS;candidate_gate=True.
Seed pass counts:eos_query4/5;span_query5/5. Pooled HOLDOUT:control1276/1440 correct with34/720
collapse;candidate1440/1440 with0/720 collapse. C270 is not yet registered.

## Latest accepted science — C268

Acceptance:docs/experiment-ledger-addendum-c268-c269.md.
Execution:aa45ea5df68dcba70c99a009c46b7bf8468304a1.
Published log:1c93db5f8d48e47074ef20e2ce72ba506fe3c660.
Summary:runs/c268-v5b-query-loss-9f62513c65d34a7aa7b1452c9540a5a6/summary.json.
Summary SHA256:9e9ea4dd0d20b0ae0b8d315549a1cf1aa13c79853b3dd129c0f01e395a2bf67c.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:ce_only3/5;ce_pair_margin3/5. Pooled HOLDOUT correct1100/1440 versus1115/1440;
same-answer collapse114/720 versus107/720. These pooled changes do not override the seed gate.
C269 is registered and ACTIVE; its one question is query representation,not another margin retune.

## Historical invalid attempt and recovery

Scientific execution HEAD:8c464589b7f9e339b1a8d195b2d73d35c1279e39.
Invalid log publication:ddcb69e11a812cc3d59ebcf66c223cfd5c347249.
Immutable evidence:docs/experiment-run-logs/c268/latest.log and latest.json at that commit.
Publisher log SHA256:60464755e769f80de86a04d474abf5a6d23b71ad2d72b33f15665150b2683abf;1619 bytes.
The log ends with run_execution_valid=False and ValueError:postcheck input in
C268.precheck -> C268.load_parent -> C267.verify_artifacts -> input_sha256 verification.
No C268 own/regression/training phase started. There is no capability score to judge or rescue.

The user previously reported a separate utf8NoBOM encoding failure while publishing from an
incompatible host. The complete now-published traceback proves the current stop is a protected
input mismatch,not Python quote parsing. The log is now published;do not ask the user to publish
it again or infer successful science merely from successful publication.

Root cause:the assistant's earlier duplicate-launch fix fece51c05c2b38ffa2e96ea601fc4b8a127305b8
edited tools/invoke_active.ps1 in place. The accepted C267 summary actually includes that file in
both source_blobs and input_sha256. Calling it control-plane code did not remove those contracts.
Required historical Git blob:86b5606a5b212b12f416abedac0923da634f88e3.
Required Windows CRLF raw SHA256:57a0f1ffa3a9370b5261ec5bf1e9eb3d778dc84f19f35c51e21174f61735a95b.
The incompatible edit produced blob ea2e3d59cc72f0fa799f61d632f864c366099a89.
The parent verifier correctly rejected it. A clean current Git tree is not proof of ancestor-byte
compatibility. The in-place patch and missed inherited-pin audit were assistant errors,not user error.
The earlier duplicate C267 command was also an assistant completion-handling error. Do not repeat it.
The published error does not enumerate all local mismatches;remaining checks are still mandatory.

Recovery record:docs/experiment-ledger-addendum-c268-execution-recovery.md.
The invalid log remains in history;neither its content nor metadata is changed by this repair.

## Minimal repair and versioned invocation override

Recovery code commit:4cd4a6ab62ea8bd8c573135e4a17a82130bf72bc.
The historical tools/invoke_active.ps1 is restored by reusing its exact accepted Git blob.
No parent summary/hash/mapping is rewritten;no input is exempted;no verifier is patched or bypassed.
Do not edit that historical file again. Its actual Windows working bytes must also match the CRLF
SHA256 above;the new entry checks this before scientific logging and reports expected/actual values.
If checkout line endings differ,stop and identify the mismatch rather than changing all Git settings.

New user entry:tools/invoke_active_v2.ps1.
Invoke it with the installed C:\Program Files\PowerShell\7\pwsh.exe -NoProfile -File.
This versioned entry remains the current user execution path for C270 because the historical tools/invoke_active.ps1 is an accepted pinned dependency.
The new entry preserves the duplicate-result notice without mutating the historical dependency.
It requires PowerShell Core>=7.3 before logging and sets PSNativeCommandArgumentPassing=Standard.
It verifies its parser,branch,tracked-tree,unique formal ACTIVE,ExpectedHead,the historical Git blob
and raw bytes,and the selected launcher parser. The launcher retains the runner parser and gains
the same PowerShell version/argument guard before its logging/publish try/finally.
The standard user block should also parse the new dispatcher before calling the explicit pwsh path.

RESULT_ALREADY_PUBLISHED requires matching experiment/execution metadata AND matching log hash/size.
It means evidence is available,not a valid or accepted result. Other stale HEADs remain SKIPPED.
Never substitute current HEAD into an old ExpectedHead command to force execution. Never edit an
expected hash to match an accidental change. Later operational revisions use new versioned paths.
The publisher itself is unchanged;use the supported host instead of modifying another parent input.

Only C268's unaccepted test24 is changed. It verifies the historical blob/CRLF checksum and fixes
the new versioned entry's normalized UTF-8 SHA256:
68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10.
Thus the operational file is content-pinned through the C268-owned test before training. It is not
a new scientific Python module or permission to weaken inherited pins. Tests01..23 and setUpClass
are unchanged. Scientific benchmark,runner,manifest,preregistration,model/data/loss/gates unchanged.
Existing OWN6 still protects the modified C268 test and launcher. Source/input counts remain454/774;
own24,focused3597,loaded3598,modules153. No additional historical exclusion or waiver.

## Latest accepted science — C267

Acceptance:docs/experiment-ledger-addendum-c267-c268.md.
Execution:3418e545bc261cf1bb920f2ae8f819deec69150c.
Published log:92b57170c6b2c3c3dc451f9d6de402114cbd6f12.
Summary:runs/c267-v5b-name-coverage-f8a591aae4aa4b7aa373aba2e520181c/summary.json.
Summary SHA256:f5f550d362428feaee12d7eee96db4cc324cea311b9b4e91ec50e4f150ec6ef8.
C267 mixed_names passed1/5 (267005);doubled_only0/5. Its valid execution is not rerun.
HOLDOUT totals across all seeds/languages:control744/1440 versus mixed771/1440 correct;
collapsed pairs284/720 versus199/720. Shared-suffix collapse163/240 ->76/240,but mixed suffix
accuracy257/480 and doubled accuracy worsened. This is not uniform improvement or a solved recipe.
Own24/focused3573 passed;448 source pins/761 protected inputs;all_pairs_matched/all_replays true.
The acceptance addendum retains complete artifact hashes and interpretation. This recovery neither
changes C267's scientific result nor rewrites its protected-input manifest.

## Active C270 — frozen triple identifiers

Experiment:C270-v5b-frozen-triple-identifiers.
Stage:V5-B-FROZEN-TRIPLE-IDENTIFIERS.
Registration:docs/experiment-ledger-addendum-c270-preregistration.md.
Design:docs/v5b-frozen-triple-identifiers-v0.1.md.
Acceptance base:f0f10ee158a0f4740fea390f4d96d93ed0e1851b.
Parent C269 execution:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Parent summary:runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json.
Parent summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.

One question:do the same frozen C269 states transfer from TRAIN-seen two-character identifiers to
unseen THREE-character identifiers composed solely from familiar identifier characters?

Profiles are fixed before evaluation for every source character pair u,v:
-tripled:uuu/vvv;
-shared_prefix2:uuu/uuv;
-shared_suffix2:uuu/vuu.
For a/b these are aaa/bbb,aaa/aab,aaa/baa. Japanese applies the same three-character construction.
No three-character identifier string occurred in C269 training. All new prompt bytes are required
to be a subset of bytes present in C269's existing rendered task. Normal prompts are globally unique
across all splits/profiles and fit the existing46-byte payload.

Retain the exact C267 logical TRAIN192/HOLDOUT96 value split,all three entity subsets,EN/JA,both
visible fact orders,both queries and distinct values0..3. Every new identifier string is unseen.
TRAIN-value rows therefore probe name/length shift with previously optimized value pairs;HOLDOUT
rows combine the name shift with the existing held-value dimension. Both splits decide the gate.
No C270 optimization or model mutation occurs.

Strict-load C269's accepted ten-state bundle once,seeds269001..269005,arms eos_query/span_query in
accepted order. Recreate each exact architecture through C269.make_arm_model,verify final_sha256,
set eval/requires_grad=False,and run:
1.accepted two-character evaluation27 forwards/2592 rows;
2.raw-logit replay<=1e-9 and exact argmax against C269 saved final outputs;
3.new three-character evaluation27/2592;
4.accepted two-character restoration27/2592;
5.replay against both anchor/reference and unchanged full fingerprint.
Per state81 forwards/7776 rows/324 core calls. Total810 forwards/77760 rows/3240 core calls.
Bundle loads1;strict state loads10;new training0;new learned checkpoints0.

C270 uses unchanged C267 score semantics with new profile keys. Per split/profile/language/subset/
visible-order answer cell require accuracy>=.90,query-pair>=.80,evidence_drop>=.35,query_drop>=.35.
Per language/subset require two-order>=.80. HOLDOUT answer cells8 rows require8/8. Primary PASS iff
ALL FIVE frozen span_query states pass every criterion on both splits and all three new profiles.
eos_query is a matched reference and cannot rescue/fail candidate. Report60 split/profile/language
paired contrasts in correct answers and same-answer collapse. Pooled means never replace seed gate.

Artifacts:transfer-plan.json,triple-dataset.json,eval-outputs.pt,measurements.json,
validation-summary.json plus summary.json. eval schema fold-c270-triple-eval-v1. Saved postcheck
rebuilds parent references,new prompt identity,replays,scores,contrasts and gates with neural Module
calls blocked. Raw anchor/new/restored payload contract159252480 bytes before serialization metadata.

Protection:466 source pins/800 protected inputs;46 deciding-path dependencies. OWN6 benchmark/test/
runner/launcher/preregistration/design. Own24;modules155;loaded3646/focused3645. Sole inherited exact
exclusion remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016.
Triple prompt dataset SHA256:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

## C270 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 93e3372760ddb70d78879315a8fc3e7de697c0f0
Scope:committed remote-byte/source-contract review,not formal C270 execution.

Compared C269 acceptance f0f10ee158a0f4740fea390f4d96d93ed0e1851b to review target:only C270
OWN6 paths differ. Re-fetched committed OWN files:
-benchmark blob6844e45466ed2bba1b40e565df9cc7853edbaf97;24279 UTF-8 characters.
-test blobdfab06b422f7d34fc677c2935a91d6090f9c4679;16987 characters.
-runner blobaba1006214b41050942675b53fabc48f38eaceb3;4700 characters.
-launcher blob21bcc56f2039595d157ec6a07bd11fbf5176c9a5;2842 characters.
-preregistration blobd1583074598137102e6b356e26f9c67bddfe35c3;5789 characters.
-design blob0ea1495824784cc935cc65bd2dca3d7e28accedf;2498 characters.
No OWN file contains NUL. Test file defines exactly24 distinct numbered methods. Runner has exactly
three embedded Python blocks with sys.argv sets {1},{},{1,2,3};launcher branch/tree/ExpectedHead/
ACTIVE-C270 and runner ParseFile guards precede logging.

Manifest/data hashes were independently reconstructed from the fixed specification. Review confirms
parent schema fold-c269-query-span-eval-v1,child schema fold-c270-triple-eval-v1,global864 unique
normal new prompts,familiar-byte subset enforcement,zero optimizer/backward/train path in C270,
parent loader provenance and81/7776/324 per-state resource accounting. Tests cover unseen identifier
strings,prompt/mask semantics,score gates,replay/freeze,count guards,parent dispatch,actual toy probe,
synthetic orchestration,persisted postcheck,dependency counts and historical dispatcher pins.

The review environment could not resolve GitHub for a complete checkout,so py_compile,actual own24,
full3645 regression,PowerShell ParseFile,parent local-artifact replay and ten real frozen-state
evaluations are NOT claimed complete here. Those remain mandatory gates in the user's Windows run.
Synthetic fixtures are implementation evidence only,not learned capability evidence.

## C270 execution and stopping

Use tools/invoke_active_v2.ps1 through explicit C:\Program Files\PowerShell\7\pwsh.exe -NoProfile.
Historical tools/invoke_active.ps1 remains immutable. Expect legacy_dispatcher_pin=PASS,
active_experiment=C270,parent/task precheck466/800,own24,focused3645,then model1/10..10/10 frozen
evaluations(no800-step training loop),strict restoration,persisted postcheck and log publication.

If branch/tree/HEAD/ACTIVE/parser/legacy-byte preflight skips,do not force execution or alter an
expected hash. Parent/source/artifact/replay/regression validity failure retries SAME C270 only.
If scientific_status=FAIL with run_execution_valid=True,accept a valid negative without training,
profile alteration,seed selection or threshold change. Publication-only failure is repaired without
repeating completed evaluation. Judge C270 before C271. Gate F NOT PASSED. No paid API,external
corpus,production adoption,cleanup,history rewrite or CI change. Preserve tools/run_c167.ps1.
