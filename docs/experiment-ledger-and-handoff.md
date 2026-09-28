# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative scientific runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
For current C269 execution use the versioned PowerShell7 entry described below,not the historical generic dispatcher.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C269 ACCEPTED PASS (bounded query-span capability). C270 NOT REGISTERED.**
C269 span_query passed5/5 against the fixed gate;matched eos_query control passed4/5.
Candidate HOLDOUT normal answers1440/1440 with zero collapse across720 query pairs.
This is positive evidence for the registered structured query-source intervention only.
C268 remains ACCEPTED VALID NEGATIVE;all earlier verdicts/recovery records are preserved.
No Gate F promotion,production adoption,general parser claim or C271 registration.

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
This versioned entry remains the current user execution path for C269 because the historical tools/invoke_active.ps1 is an accepted pinned dependency.
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

## C269 accepted scope and next boundary

The complete C269 registration/review remains in its preregistration/design documents and the prior
handoff at7c44987b4a70f6ed821657f518b81f78bf0a376d. Its execution has now been judged PASS only in
that bounded scope. C270 is not yet registered;next question is frozen transfer to unseen
three-character familiar-byte identifiers. Preserve tools/run_c167.ps1,historical
tools/invoke_active.ps1,and the versioned PowerShell7 operational entry. Gate F NOT PASSED.
