# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C264 ACCEPTED PASS (bounded two-fact transfer). C265 ACTIVE / NOT YET JUDGED. C266 NOT REGISTERED.**
C265 is the unique ACTIVE experiment:V5-B frozen compound identifiers.
All twenty C264 states passed its thresholds,but this does not mean all answers were correct.
C263 bounded PASS and all earlier verdicts/recoveries remain unchanged. No optimizer default change,
architecture selection,production adoption,general-language claim or Gate F promotion.

## Latest accepted evidence — C264

Scientific execution HEAD:6da6c182f328cccddbdfbd94e232141b0c68c0ea.
Published log commit:5e62210d4b2a5b5d0cf7dbbc0fe6cf7be05d47e1.
Publisher log SHA256:f228c6ede8e95546c6e534a4afcde97255e69fe38d0692b2293e71f35c2ad445.
Log bytes:779217;lines3980.
Summary SHA256:1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503.
Summary:runs/c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935/summary.json.
Acceptance:docs/experiment-ledger-addendum-c264-c265.md.
Acceptance/base commit:d0af4709b7362f145ca55c2bfee5038b107e2961.

Own24 PASS in13.519s;focused3501 PASS in316.942s.430 source pins/723 protected inputs verified.
All20 frozen C263 final states evaluated:600 wrapper forwards,120960 row presentations,2400 core
calls. One accepted weight-bundle load,20 strict state loads;training0,new learned checkpoints0.
Accepted-output replay,two-fact scoring,restoration,weight preservation,provenance reconstruction,
saved metric reconstruction and protected-input checks passed. Tracked tree clean;execution HEAD
preserved;run_execution_valid=True;scientific_status=PASS;joint_gate=True.

Acceptance is based on immutable published log ranges,metadata and recorded local postchecks.
The reviewer did not independently run the learned states or rehash the entire779217-byte console
log. Publisher-reported SHA256 is not an independently computed reviewer hash. The publication
commit immediately follows the registered execution HEAD and adds only C264 latest.json/latest.log.

|Arm|Whole-seed passes|
|---|---:|
|standard_forward|5/5|
|standard_reverse|5/5|
|lower_forward|5/5|
|lower_reverse|5/5|

Each state has288 unique reduced prompts,12 language/subset/order cells and six two-order cells.
All satisfy the fixed thresholds. Do not invent perfect per-state totals from PASS flags.
Confirmed examples:standard_forward263001=288/288;lower_reverse263005=286/288.
For the latter,EN a/c order01 and10 each score23/24 with paired-query11/12;the associated two-order
score is23/24. This is a valid threshold PASS,not an execution failure. No grand exact-accuracy
sum or uninspected per-state perfect scores are asserted by this acceptance.

Interpretation:these frozen states can transfer from three visible facts to two familiar named
entities after deleting an unqueried fact. Fact count,length and positions changed jointly.
Retained pairwise associations,names and values are familiar. Reduced projections can cross the old
TRAIN/HOLDOUT partition,so they do not form a new disjoint split. No arbitrary-name/length,ordinary
language,learning-rate advantage or unique internal mechanism follows. Keep all cohorts unchanged.

Accepted C264 artifacts:
-deletion-plan.json:a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1;2398 bytes.
-eval-outputs.pt:3123aa3b0c2e74b1a069edeb56da5a52046fc5731f681656abf51d4200db55b3;247882609 bytes.
-measurements.json:34c43a5eea6aa235a7bcf8451f3742393a53255a63299c43874c5bf948b87f99;63095 bytes.
-provenance.json:35f96556b849adeac41cc04cc77d91c94ba4e560783d0f58c67e3898ea479577;114338 bytes.
-two-fact-dataset.json:8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1;39746 bytes.
-validation-summary.json:171731535a0f725e5cfb5912828e8c082c5950507a9dade64cf43463fe304a14;1445 bytes.

## Preserved earlier evidence and recovery

C263 ACCEPTED PASS:all four rate/order arms5/5,held-assignment normal answers8640/8640.
Both standard0.005 and lower0.001 reach the final accuracy ceiling;no learning-rate benefit or
universal training robustness is established. Do not change optimizer defaults on that result.
Execution:abca8d7eb25146fca6f7404790071d1e6f0999d0.
Published log:1b47b5e3dc8ee3c6c2edd6972e7521b16e4f1b67.
Summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
Summary SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
Acceptance:docs/experiment-ledger-addendum-c263-c264.md. This is the learned-weight source for C265.

C262 ACCEPTED VALID NEGATIVE:forward0/5,reverse2/5;639 paired answer differences under identical
initial state and exact exposures. It retains evidence for its specified chronology intervention.
Acceptance:docs/experiment-ledger-addendum-c262-c263.md. C263 uses a different cohort and does not
revoke C262. Earlier variability was not isolated to initial weights alone.
C261 repeated-value4/5 with_core and3/5 without_core remains valid negative,not independent retraining.
C260 core ablation4/5 versus3/5 remains valid negative;no globally superior architecture selected.
C259 six-order4/5 versus two-order2/5 remains negative. C258 diagnostic PASS only;C257 unseen-order2/5
remains negative;C256 bounded three-entity5/5 PASS remains. C256 precheck INVALID and C255 invalid
attempts remain in execution-recovery addenda. C255/C254/C253 diagnostic passes do not rescue C252.
Complete historical identities,metrics and reviews remain in acceptance/recovery addenda and the
prior handoff at6da6c182f328cccddbdfbd94e232141b0c68c0ea. Preserve all accepted code/tests/logs,
checkpoints,recovery records and tools/run_c167.ps1. No cleanup or history rewrite.

## Active C265 — frozen compound identifiers

Experiment:C265-v5b-frozen-compound-identifiers. Stage:V5-B-FROZEN-COMPOUND-IDENTIFIERS.
One question:can all twenty frozen states bind two-symbol names made from familiar characters,
including identifiers sharing their first or last character? No training or seed/model selection.

For every C264 source subset,take original names u,v in ascending original entity-index order:
-doubled: u->uu,v->vv (aa/bb);
-shared_prefix: u->uu,v->uv (aa/ab);
-shared_suffix: u->uu,v->vu (aa/ba).
Apply the same bijection in facts and query,including Japanese names. aa=0;ab=1;ab= has target1.
All20 models receive all3 profiles;these are input conditions,not separately trained architectures.
No translation back to the original one-symbol identifiers before inference.

Keep two facts,distinct values0..3,all three source subsets,EN/JA identifiers,both fact orders,both
queries and source-row ordering.288 questions/profile,864 unique new normal prompts/state.
Original targets/entity-group metadata are used only OFFLINE by the actual unchanged C264 scorer.
Only renamed visible bytes and zero task IDs reach the model. Do not pass source indices/answers
through a hidden channel. Each profile preserves source_id and target for every row.
All normal bytes already occur in the familiar task. Normal lengths are13 ASCII/25 Japanese bytes,
equal across the three profiles for each source row and within the46-byte payload/48-slot contract.
The same two values are masked for evidence_blind;the whole query name becomes ? for query_blind.
New dataset SHA256:4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb.
No new TRAIN/HOLDOUT split is assigned to the frozen probes.

All states are C263 final Full aligned readers,14256 parameters,seeds263001..263005,arms
standard_forward,standard_reverse,lower_forward,lower_reverse. Construct through C256.make_model/
C231 factory,then strict-load the corresponding C263 state;check C264 final fingerprints and freeze
all modules/gradients. C264 wrote no learned checkpoint. Do not load its eval archive as weights.

## C265 gate and interpretation boundary

Score each profile with actual unchanged C264.score.12 cells/profile (2languages x3subsets x2orders),
24 answers/12 paired-query groups per cell. Require accuracy>=.90(22/24),paired-query>=.80(10/12),
evidence_drop>=.35 and query_drop>=.35. Each of six language/subset two-order groups must also
pass>=.80(20/24 groups correct in both presentations). Distinct targets make query-drop applicable.
Whole-state PASS requires ALL3 profiles;overall C265 PASS requires ALL20 states. Report profile-by-arm
counts and whole-model counts. A good doubled profile cannot rescue a shared-character failure.
Valid misses are accepted negatives,not permission to retrain,select profiles or loosen thresholds.

The doubled profile is an equal-length reference for shared-prefix/suffix profiles,not a full causal
control for every composition effect. Compared with original inputs,name length,composition and
positions change. Profiles also differ in character distributions. First-/last-character parser
failures are synthetic authoring controls,not confirmed mechanisms of a learned model. Neither a
pass nor a failure uniquely identifies an internal parser. No arbitrary-name,ordinary-language,
independent-general-benchmark,learning-rate advantage,optimizer adoption or Gate F claim.

## C265 parent interfaces and provenance

C264 summary:runs/c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935/summary.json.
C263 weight-source summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
Their exact hashes are listed above. C263 summary must already exist in the inherited protection
mapping;reject an unprotected substitute path and do not count this source twice.

check_parent calls actual C264.validate_result,requires its execution/PASS/four5-of5 counts and exact
six artifact identities. precheck verifies all hashes/sizes,inherited pins and protected files.
load_reference calls actual C264.verify_artifacts(c264_dir,c263_summary,C264_EXECUTION),THREE arguments.
Parent saved evidence verification is guarded against neural model calls. A second C264 eval archive
read extracts seed,arm,final_sha256 and reduced from fold-c264-deletion-eval-v1. The reduced field is
C264's actual two-fact output,not its original three-fact anchor/restored output. Require288x256
CPU float64 tensors for each view. Recompute C264.score and match all20 accepted metrics.
Weights come through actual C263.load_bundle(c263_dir/trained-models.pt) once;20 strict state loads.
C264 verification also validates its C263 source evidence,without rerunning old neural inference.

## C265 workload,artifacts and protection

Per frozen state:old two-fact6 forwards/864 rows -> accepted raw-logit/argmax replay barrier ->
three new naming profiles18/2592 -> old two-fact restoration6/864. Compare restored outputs with
both same-run anchor and accepted reduced tensors. Require full weights unchanged and remove hooks
on exceptions.30 wrapper forwards/4320 rows/120 Full core calls per state.
Totals600 forwards/86400 row presentations/2400 core calls;new training0,new checkpoints0;
one accepted weight-bundle load/20 strict state loads. CPU float64,threads2,deterministic algorithms.
Raw replay tolerance1e-9 and exact argmax. Reproducing an old wrong answer is valid integrity replay,
not a demand for a previously imperfect state to become perfect.
Reference loads per pass:two C264 and two C263 evaluation archives. Run and saved postcheck each
use one pass,four reads of each reference archive total. Parent metric reconstruction,source hashing,
serialization and historical tests are additional work,not extra formal model-forward samples.

Five ignored artifacts plus summary.json:identifier-plan.json,identifier-dataset.json,eval-outputs.pt,
measurements.json,validation-summary.json. Eval schema fold-c265-identifiers-eval-v1 stores anchor,
renamed profile tensors,restored tensors,identity,counters and replay results. Raw output payload
176947200 bytes(about177 MB decimal),not a peak-RAM or serialized-file-size measurement.
Saved postcheck blocks neural model calls and rebuilds references,dataset,replays,metrics and gates.
No additional model construction,inference or learned-bundle load is performed during saved postcheck.

Protection436 source pins/736 inputs=430/723 plus OWN6 and parent summary+SIX artifacts.
Direct deciding dependency union41=five C231 LM sources,C230..C264 helpers and C265;lazy imports count.
Own24;modules150;loaded3526/focused3525. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3.
Registration:docs/experiment-ledger-addendum-c265-preregistration.md.
Design:docs/v5b-compound-identifiers-v0.1.md. C264 acceptance and C265 registration are separate commits.

## C265 post-authoring review

post_authoring_review = PASS
review_target_HEAD = f3ad13aee3c3f373497e227bc35bec4f519342cb
Scope:committed-byte C265 authoring validation with exact C264 helper code and synthetic model fixtures,
NOT a formal learned-model run or complete historical checkout verification.

All SIX committed OWN files were re-fetched/read completely after authoring. Complete local files
were independently Git-blob hashed and matched to returned remote identities before the final test:
-benchmark:b7536b3bb3e0c505a9a0c6a1052d2d895202362c;20969 bytes.
-tests:3fa8d3082f2191cdf6674ddb820329dbb24c68f6;18700 bytes.
-runner:7740a1782f251f6f6921517e456ad84525b66228;4883 bytes.
-launcher:153ae723b08eb723038b77944a1d26895b2c8c17;2745 bytes.
-preregistration:e30c730d0d08d2ffd3d01f5c37142347e82d3a0e;10609 bytes.
-design:1f71c75d640bffd761f79bea245124809422c8f7;3105 bytes.
The complete accepted C264 benchmark module was also locally reconstructed from all fetched ranges
and byte-matched:8714a23b1996e4d136b362dadc137e3c7e1981ef;23043 bytes. It was not modified/published.
Unlike a surrogate scorer,the tests use its actual dataset,render,evaluate_new,score and call guard.
The C263-and-earlier historical import graph remains unavailable locally and is not claimed tested.

First exact own suite:24/24 PASS in5.986s.
After committed readback and all six blob matches:24/24 PASS in4.633s.
No code/test correction was needed after the first passing suite. UTF-8/NUL,compile/import,manifest
and dataset hashes passed. Recursive LOAD_GLOBAL audit covered92 new-file code objects including
nested functions,with zero unresolved globals. Profile lengths mechanically checked at13/25 bytes.
Three embedded Python blocks compile;CLI indices precheck1/2,regression none,postcheck1/2/3/4.
Semantic own24 count,source/input arithmetic,dependency regex scope and176947200-byte payload pass.

The model is a clearly labeled string-parser Oracle with14256 placeholder parameters and Identity
core counters,NOT learned FOLD computation. First-character-only and last-character-only variants
fail their respective shared-prefix/shared-suffix cases at144/288. The exact parser passes,so the
scorer can distinguish these specific wrong algorithms from correct binding in synthetic controls.
Test13 executes the actual new probe30/4320/120. Test17 executes the actual reference loader with a
mocked three-argument parent verifier,temporary archive and actual C264 scorer. Test18 checks the
actual C264 verifier signature and reduced-field semantics. Test19 executes actual20-state new
run/probe/analyze/persistence/saved-postcheck with synthetic checkpoint/runtime adapters;new profile
evaluation and scoring are not replaced. Test22's3526 dummy IDs verify exclusion only,NOT execution
of3525 historical tests. No synthetic result is learned-capability evidence.

Actual parent writer/reference fields and verifier signatures were read from the complete C264
source. The existing active dispatcher was re-read:one formal ACTIVE token,selected-launcher parser
before invocation. Launcher branch/tree/HEAD/ACTIVE and runner parser checks precede experiment logs.
Compare C264 log commit to review target:seven additions only(C264 acceptance plus six C265 files).
No accepted source,test,log,runner,dispatcher or CI file changed. Only this activation handoff follows.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu. GitHub DNS failed in the container;no full checkout
or user-local learned artifacts were available. PowerShell/pwsh absent;Windows ParseFile was NOT run.
The standard command parses dispatcher;dispatcher parses selected launcher;launcher parses runner.
Pending authoritative checks:Windows parser chain,actual436/736 source/artifact precheck,own24 through
full repository dependencies,complete3525 regression,twenty real frozen-model evaluations,real
checkpoint/reference replay,persisted postcheck and log publication. None is claimed completed by
this authoring review. Use FINAL activation HEAD,not review_target_HEAD or parent execution/log HEAD.
Re-read final branch ref before issuing ExpectedHead. C266 waits for C265 judgment.

## Execution and stop

Use tools/invoke_active.ps1. Formal state has exactly one ACTIVE token resolving to C265.
Fixed parent/output and weight-source paths are listed above and in tools/invoke_c265.ps1.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent/task precheck ->own24 ->focused3525
->twenty frozen-model evaluations ->persisted postcheck ->log publication.
Progress:model1/20..20/20;no800-update training loop. A complete valid FAIL is a scientific negative,
not INVALID. Do not retrain,select profiles/states,change thresholds or rewrite earlier verdicts.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE:operational SKIPPED before logging;
no scientific execution or log publication. Source/artifact/schema/nonfinite/identity/count/replay/
test faults require minimal SAME C265 repair. No C266 registration on an invalid attempt.
Log-only publication failure is repaired without repeating completed evaluation. The user normally
sends only 'finished';fetch docs/experiment-run-logs/c265/latest.json/latest.log for judgment.
Do not move this branch with unrelated work during the user's formal run/log publication.
Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite or CI change. Preserve all accepted evidence,recoveries and tools/run_c167.ps1.
Judge C265 before C266.
