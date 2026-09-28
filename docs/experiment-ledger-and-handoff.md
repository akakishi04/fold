# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative scientific runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
For current C269 execution use the versioned PowerShell7 entry described below,not the historical generic dispatcher.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C268 ACCEPTED VALID NEGATIVE. C269 ACTIVE / NOT YET JUDGED. C270 NOT REGISTERED.**
C268 recovered execution aa45ea5df68dcba70c99a009c46b7bf8468304a1 is the authoritative
accepted valid negative:ce_pair_margin3/5 and ce_only3/5 against the fixed5/5 candidate gate.
C269-v5b-paired-query-span-pooling is now the sole ACTIVE experiment. It uses five fresh seeds,
matched CE-only control/candidate arms and changes only the reader query source.
No Gate F promotion,production adoption,post-hoc loss retuning or C270 registration.

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

## Active C269 science — registered and reviewed

Experiment:C269-v5b-paired-query-span-pooling.
Stage:V5-B-PAIRED-QUERY-SPAN-POOLING.
Registration:docs/experiment-ledger-addendum-c269-preregistration.md.
Design:docs/v5b-query-span-pooling-v0.1.md.
Acceptance base:edba206232f341059ecd8ab4b572896e0ddb7143.
C268 parent execution:aa45ea5df68dcba70c99a009c46b7bf8468304a1.
C268 parent summary SHA256:9e9ea4dd0d20b0ae0b8d315549a1cf1aa13c79853b3dd129c0f01e395a2bf67c.

One question:with the same paired CE-only training,does replacing the actual C252 pre-core EOS
query vector with a visible query-span pooled pre-core vector improve reliable held-value binding
across five fresh initializations?

Fresh seeds269001..269005;arms eos_query and span_query. Control is the actual unchanged C252
AlignedPrecoreReadout. Candidate has the same14256 parameters,state_dict keys and initial tensor
values;it changes only the source passed to read.query. Candidate query=mean of masked pre-core local
states strictly after the final visible ';' byte59 and before the final visible '=' byte61.
The final '=' must be EOS-1;span is nonempty/delimiter-free. All visible UTF-8 bytes are pooled.
No entity ID,target,split,profile,pair index or supervision metadata enters model.forward.
Masked pre-core memory,read.query/key/output,score divisor4,PAD mask,actual Full core,post-core EOS
residual,readout_norm and decoder remain unchanged. Candidate/control parameter storage is disjoint.

Use exact C267 dataset SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
TRAIN192/HOLDOUT96;three entity subsets;EN/JA;both visible orders and queries;all three naming
profiles. Four held value pairs remain absent from optimization. Names/profiles are TRAIN-seen.
Both arms use ordinary mean CE only and identical paired batches. Shuffle96 query pairs using
seed+269000+epoch;24 pairs/batch;four batches/epoch;profile=epoch%3.800 updates=200 epochs;
each TRAIN row200 exposures;profile updates268/268/264. AdamW lr.005,betas.9/.999,eps1e-8,
weight_decay0,global clip1;fit RNG seed+270000 per arm;CPU float64,threads2,deterministic.

Primary PASS iff all FIVE span_query states meet the unchanged C267 criteria on every split/profile/
language/entity-subset/order:answer accuracy>=.90,query-pair>=.80,evidence_drop>=.35,
query_drop>=.35 and two-order>=.80. HOLDOUT answer cells8 rows imply8/8 and paired groups4/4.
eos_query is a matched control and cannot rescue/fail the candidate. Report30 paired HOLDOUT
profile/language correct/collapse contrasts. Pooled metrics do not replace the five-seed gate.

Workload:10 models;8000 optimizer updates;384000 training rows;8540 model forwards;435840 row
presentations;34160 core calls;540 final/replay evaluation forwards;one10-state bundle write/load;
10 strict state loads. Persist query-plan,dataset,weights,raw evaluation records,measurements and
validation summary;postcheck reconstructs schedules/scoring/contrasts with learned Module calls
blocked. Parent verification is provenance only;no accepted C268 learned state initializes C269.

Protection contract:460 source pins;787 protected inputs;45 deciding-path direct dependencies.
OWN6:benchmark,own test,runner,launcher,preregistration,design. Own24;modules154;
loaded3622/focused3621. Sole inherited exact exclusion remains:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa.
Preserve tools/run_c167.ps1 and historical tools/invoke_active.ps1.

## C269 post-authoring review

post_authoring_review = PASS
review_target_HEAD = f03df747c89d7d7c93c80f892fb860a6468a264e
Scope:committed remote-byte/source-contract review;not scientific execution.

Compared C268 acceptance edba206232f341059ecd8ab4b572896e0ddb7143 to the immutable review target:
only C269 OWN6 paths differ. No accepted benchmark,test,runner,artifact,legacy dispatcher or C268 log
was modified. Re-fetched complete C269 OWN6 identities at the review target:
-benchmark blob eb8e441e442530e377c5aad1db0c05552288c5d7;23933 UTF-8 characters.
-test blob adc42ee9181d5c77b53d0ebaf31ed4d399f33f11;18166 UTF-8 characters.
-runner blob31306abaee3761865a184089250ec2366cc158f4;4758 characters.
-launcher blob5cc45a0e5f11c500a58c33a74fcf344cfb16e877;2842 characters.
-preregistration blob4b80da1347f12dbfacf26b50d2251374e3bbe9c4;6800 characters.
-design blobaff1653a6aeea1118574a21f4086c1b76ef83199;3023 characters.
No NUL was found in any OWN file. Manifest was independently reconstructed from committed constants
and hashes to cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa.
The committed test defines exactly24 distinct numbered test methods. The runner has exactly three
embedded Python blocks with sys.argv index sets {1},{},{1,2,3};launcher branch/tree/ExpectedHead/
ACTIVE-C269 and runner-ParseFile guards precede the logging failure boundary.

Review confirmed query_span_mask accepts only token IDs and derives the span from final semicolon/
equals/EOS delimiters;fit passes only token batches and zero task IDs to model.forward and uses target
bytes only in CE. The own tests cover ASCII,all UTF-8 bytes,query_blind '?',malformed boundaries,
all actual TRAIN/HOLDOUT renderings across all profiles/views,matched complete initial state,
query-source formula,post-core residual provenance,gradient flow,schedule/gate/replay/protection and
historical dispatcher pins. Source call-order assertions cover precheck before training tables,
model construction before train,training before bundle load,and replay before scoring.

No authoritative Windows repository/runtime is available to this reviewer. Therefore no claim is
made that PowerShell ParseFile,py_compile,all own24,full3621 regression,C268 local-artifact replay or
real ten-model learning has already run. Those remain mandatory gates in the user's Windows runtime.
Synthetic/toy authoring tests are implementation evidence only,not scientific capability evidence.

## C269 execution and stopping

User entry:tools/invoke_active_v2.ps1 through explicit
C:\Program Files\PowerShell\7\pwsh.exe -NoProfile -File. The historical invoke_active.ps1 must
remain unchanged. The user block parses the versioned dispatcher;it parses itself and selected
launcher;invoke_c269 parses run_c269 before logging. Expect legacy_dispatcher_pin=PASS,
active_experiment=C269,then parent/task precheck460/787,own24,focused3621,ten models with
200/400/600/800 progress,strict replay,persisted postcheck and log publication.

If branch/tree/HEAD/ACTIVE/parser/legacy-byte preflight skips,do not force execution or alter an
expected hash. If parent/source/artifact/replay/regression validity fails,repair SAME C269 only.
If scientific_status=FAIL with run_execution_valid=True,accept the valid negative without tuning
pooling,loss,steps,seeds or thresholds. If log transport alone fails,repair publication without
retraining. On user 'finished',fetch C269 latest.json/latest.log from remote and judge C269 before
registering C270. Do not move the experiment branch during execution/publication. Gate F NOT PASSED.
No paid API,external corpus,production adoption,cleanup,history rewrite or CI change.
