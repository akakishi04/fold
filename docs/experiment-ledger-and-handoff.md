# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative scientific runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
For this recovery use the versioned entry described below,not the historical generic dispatcher.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C268 ACCEPTED VALID NEGATIVE. C269 NOT REGISTERED.**
Recovered C268 execution aa45ea5df68dcba70c99a009c46b7bf8468304a1 is the authoritative
scientific result. Candidate ce_pair_margin passed3/5, not the fixed5/5 gate; ce_only also passed3/5.
The earlier C268 attempt at8c464589b7f9e339b1a8d195b2d73d35c1279e39 remains INVALID history.
C267 remains ACCEPTED VALID NEGATIVE;C266 diagnostic PASS;C265 negative;C263/C264 bounded PASS.
No Gate F promotion, production adoption or post-hoc loss retuning.

## Latest accepted science — C268

Acceptance:docs/experiment-ledger-addendum-c268-c269.md.
Execution:aa45ea5df68dcba70c99a009c46b7bf8468304a1.
Published log:1c93db5f8d48e47074ef20e2ce72ba506fe3c660.
Summary:runs/c268-v5b-query-loss-9f62513c65d34a7aa7b1452c9540a5a6/summary.json.
Summary SHA256:9e9ea4dd0d20b0ae0b8d315549a1cf1aa13c79853b3dd129c0f01e395a2bf67c.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:ce_only3/5;ce_pair_margin3/5. Pooled HOLDOUT correct1100/1440 versus1115/1440;
same-answer collapse114/720 versus107/720. These pooled changes do not override the seed gate.
C269 is not yet registered; next question is query representation,not another margin retune.

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
This explicitly supersedes older generic instructions to invoke tools/invoke_active.ps1 for C268.
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

## Active C268 science — unchanged registration

Experiment:C268-v5b-paired-query-discrimination-loss.
Stage:V5-B-PAIRED-QUERY-DISCRIMINATION-LOSS.
One question:with identical mixed-name coverage,initial weights,paired batches and800 updates,does
CE+paired-query discrimination improve held-value binding compared with CE alone?
Registration:docs/experiment-ledger-addendum-c268-preregistration.md.
Design:docs/v5b-paired-query-loss-v0.1.md.
These scientific documents remain authoritative;only their historical dispatcher instructions are
superseded by the explicit recovery entry above.

Five fresh seeds268001..268005;arms ce_only and ce_pair_margin;actual unchanged Full aligned reader,
14256 parameters. Copy each complete initial state into both arms. No accepted learned-state reuse.
A batch has24 same-facts/different-query pairs,48 rows,identical between arms. Targets never enter
model.forward. For target bytes t0,t1 and logits z0,z1:
 d=(z0[t0]-z0[t1])-(z1[t0]-z1[t1]);P=mean(relu(2-d)).
Control loss=CE;candidate loss=CE+0.1*P. Keep margin2 and coefficient0.1,not a result-driven sweep.
Low auxiliary loss does not guarantee correct answers;retain CE and the real task gates.

Use exact C267 data:192 TRAIN/96 HOLDOUT logical rows,three naming profiles,all source subsets,
EN/JA,both fact orders and queries. HOLDOUT value pairs(0,2),(1,3),(2,0),(3,1) stay excluded in every
training rendering. Dataset SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Shuffle96 pairs each epoch using seed+268000+epoch;four24-pair batches.200 epochs/800 updates;
each base row200 exposures,profile updates268/268/264. Both arms use the same paired sampler.
AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1,fit RNG seed+269000 per arm.
CPU float64,threads2,deterministic algorithms. No early stop,extra updates or seed selection.

Primary PASS requires all five ce_pair_margin states to pass existing C267 criteria on both splits
and all profiles. Accuracy>=.90,query-pair correctness>=.80,evidence/query mask drops>=.35,
two-order consistency>=.80. HOLDOUT answer cells8 rows require8/8. Report controls and30 paired
HOLDOUT profile/language correct/collapse contrasts independently. No gate rescue by pooled means,
reduced collapse or low auxiliary loss. All name profiles are trained;no unseen-name claim.

Workload:10 models,8000 updates,384000 training rows,8540 model forwards,435840 row presentations,
34160 core calls. Final evaluation27 forwards/2592 rows per model;strict replay repeats that work.
One new10-state bundle write/load;10 strict loads. Save final raw logits and checkpoints;recompute
metrics/schedules/contrasts from saved tensors without new neural inference in postcheck.
The exact parent verifier still checks all761 inherited input hashes including the restored legacy
entry. No missing/corrupt artifact is substituted or ignored. The restored file removes the known
operational conflict;the real precheck must verify all remaining user-local files.

## Recovery post-authoring review

post_authoring_review = PASS
review_target_HEAD = 4cd4a6ab62ea8bd8c573135e4a17a82130bf72bc
Scope:limited recovery source/changed-test review,not full own24 or scientific execution.

Committed restored/new dispatcher,launcher,changed test section and recovery record were re-fetched
at the immutable review commit. Complete local executable-file Git hashes matched returned blobs:
-tools/invoke_active.ps1:86b5606a5b212b12f416abedac0923da634f88e3;3354 LF bytes.
-tools/invoke_active_v2.ps1:e3923b6224959b442afefa02fafa967e2e6d462e;7048 bytes.
-tools/invoke_c268.ps1:aefd100e35b99e6e4b1ec797b1e56a2fe782c9ec;2838 bytes.
-tests_lm/test_v05_c268_paired_query_loss.py:01489b55b78a0411451f391881a9f227eab65451;21351 bytes.
Recovery record read back as blob1c90522d8f882fc644deb97bce54903a69d689c3.
Independent conversion of the accepted LF blob to Windows CRLF reproduces the recorded57a0...SHA256.
That is not a direct measurement of the user's checkout bytes;the new entry performs that check.

Executed the actual changed test24 body in an AST-extracted isolated unittest,without the unrelated
neural setUpClass:1/1 PASS. Repeated after committed-byte/hash readback:1/1 PASS. The other23 test
bodies and setUpClass were AST-compared to the original C268 test file and are unchanged.
Whole test file compiles;UTF-8/NUL checks and semantic24-test-definition count pass. These facts do
not claim all24 tests ran. The test checks both historical hashes,new-entry fixed hash,version guard,
Standard argument setting,legacy pin guards,branch/tree/ACTIVE/stale checks,parser-before-launch,
metadata matching and no ExpectedHead substitution. It is static PowerShell source verification.
No PowerShell executable was present in the review container. No ParseFile execution,full repository
import graph,full own24,full3597 regression or real parent-artifact replay was available locally.
The review environment is not the authoritative Windows environment. All those checks remain
mandatory on the user's runtime before training. Do not repeat prior overbroad review claims.

Compared invalid-log commit to recovery code commit:five changed paths only,as listed in this
recovery;no scientific benchmark,runner,dataset,manifest,parent test/verifier or old log changed.
Only this handoff commit follows that code review. Use the FINAL recovery branch HEAD,not the code
review HEAD,the old8c464...execution HEAD or ddcb69...log HEAD. Re-read branch ref before the command.

## Execution and stopping

The retry entry is tools/invoke_active_v2.ps1 through the explicit PowerShell7 executable.
Parse the dispatcher in the user block;the entry parses itself and the selected launcher;the
launcher parses run_c268.ps1. Version guards precede logging. Expect legacy_dispatcher_pin=PASS,
powershell_host with Standard arguments,and active_experiment=C268. Then unchanged parent precheck,
own24,focused3597,ten-model training,strict replay,persisted postcheck and log publication follow.

If a preflight skips,report the reason and do not force a run. LEGACY_DISPATCHER_BYTES_MISMATCH
requires checking the reported raw-byte discrepancy,not changing the recorded expected hash.
Further parent-input failures require identifying the actual file and restoring its provenance.
If science completes with FAIL but execution-validity passes,judge that as a valid negative,not a
reason to retune. If only publication fails,repair transport without repeating completed training.
On 'finished',read C268's new latest metadata/log (use blob API for >1MB) before replying. Never
recycle a C267/C266 answer or command. No C269 until C268 has a valid judged result.
Do not move the experiment branch with unrelated changes during the user's execution/publication.
No paid API,external corpus,model expansion,production adoption,cleanup,history rewrite or CI changes.
Historical details are preserved in all acceptance/recovery addenda and in the prior handoff at
8c464589b7f9e339b1a8d195b2d73d35c1279e39. Gate F NOT PASSED. Preserve tools/run_c167.ps1.
