# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C263 ACCEPTED PASS (bounded capability only). C264 ACTIVE / NOT YET JUDGED. C265 NOT REGISTERED.**
C264 is the unique ACTIVE experiment:V5-B frozen two-fact deletion.
C263's lower-rate capability gate passed,as did both standard-rate arms. Final accuracy and
chronology-disagreement comparisons are at ceiling;no learning-rate benefit is established.
Keep optimizer defaults unchanged. Preserve all earlier negatives and recovery records.
No production adoption,architecture selection,general-language or Gate F promotion.

## Latest accepted evidence — C263

Scientific execution HEAD:abca8d7eb25146fca6f7404790071d1e6f0999d0.
Published log commit:1b47b5e3dc8ee3c6c2edd6972e7521b16e4f1b67.
Publisher log SHA256:d089e8f808170a58bfb292547387642a4d0d6312ec61764564462ba26cc2441b.
Log bytes:875870;lines4160.
Summary SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
Summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
Acceptance:docs/experiment-ledger-addendum-c263-c264.md.
Acceptance/base commit:5f6bd9ca1c3c318451f30b4d4c9858285b3d272b.

Own24 PASS in12.872s;focused3477 PASS in292.013s. Source pins424/protected inputs710.
Twenty models each completed800 updates:16000 updates,768000 training rows,16480 forwards,
871680 row presentations,65920 core calls. One20-state bundle write/load;20 strict state loads.
Four-way initial-state/exposure matching,rate/order metadata,weight changes,strict checkpoint
fingerprint/raw-logit/argmax replay,persisted metrics/contrasts and protected-input checks passed.
Tracked tree clean;scientific execution HEAD preserved;run_execution_valid=True.
scientific_status=PASS;candidate_gate=True;all_pairs_matched=True;all_replays=True.

Acceptance uses immutable published log ranges,metadata and recorded local postchecks.
The reviewer did not independently run the learned models or rehash the complete875870-byte log.
Publisher-reported SHA256 is not a new reviewer byte hash. The log-publication commit immediately
follows the registered execution HEAD and changes only c263/latest.json and latest.log.

Deciding capability evidence:

|Arm|Learning rate|Whole-seed passes|HOLDOUT correct|All-six groups correct|
|---|---:|---:|---:|---:|
|standard_forward|0.005|5/5|2160/2160|360/360|
|standard_reverse|0.005|5/5|2160/2160|360/360|
|lower_forward|0.001|5/5|2160/2160|360/360|
|lower_reverse|0.001|5/5|2160/2160|360/360|

Per seed/language216 answers and36 all-six groups. All20 models together HOLDOUT8640/8640.
The registered per-order,masked-input and TRAIN criteria also pass;the pooled total does not replace
those gates. Both rate_joint_pass values are true. No seed or less favorable chronology was removed.
All20 rate contrasts and20 order contrasts have zero final accuracy delta,answer disagreements and
correctness flips. All10 disagreement interactions are zero,with both rates' worst chronology
accuracy1.0 in every seed/language cell. Equal argmax does not imply equal raw logits,NLL,weights
or learning curves. Do not invent equality of those quantities from equal final correct answers.

Interpretation:C263 establishes bounded capability of these20 final states at the fixed budget.
It does NOT show that lowering the rate helped,because the standard-rate comparison also reaches
the ceiling. The effect on final accuracy/disagreement is unresolved here;do not change defaults
or claim that training-order sensitivity has been universally removed. C262 used a different cohort
and retains its valid chronology-sensitivity evidence. The authored task has been repeatedly
inspected;fresh seeds are not an independent general benchmark or an initialization-population
guarantee. No general language,core superiority,production readiness or Gate F passage follows.

Accepted C263 artifacts:
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:1681c71811844655081ca5597b6dfbe1ab80fbdc5b5046b1f947b1bf51aefd89;106263991 bytes.
-measurements.json:9b8bab48074a91e1dd5f3c5d389598739b651bcadeed6ec49fbf7ec0c92631ee;118267 bytes.
-rate-plan.json:ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305;2779 bytes.
-trained-models.pt:a63519b761bc876b8088fe14432018cd01024bfdecbcf1fca38a0515021dede9;2475525 bytes.
-validation-summary.json:e42f668ec6c2a01f573be92bbcd938f1d991e48cf02d242315d02d740d29066f;15183 bytes.

## Preserved earlier evidence and recovery

C262 ACCEPTED VALID NEGATIVE:forward_blocks0/5,reverse_blocks2/5. HOLDOUT1543/2160 versus1709/2160.
Execution28030ad02e69a9ae7236fca7f7e84a61f3c89c46;log4dc8fec24578efa5f7d8abfea17c56be2dc23673.
Summary SHA256:9cda47219d6e376516044d5807e546a8c13110f584f139bda2a3da8800b2d93d.
Acceptance:docs/experiment-ledger-addendum-c262-c263.md. Its639 paired disagreements comprised201
correct-to-wrong,367 wrong-to-correct and71 different wrong answers. Initial state and exact
exposures were held constant,so this is evidence of the specified chronology effect,not an
initial-weight-only explanation. Reverse was not universally better. C263 does not revoke this.

C261 ACCEPTED VALID NEGATIVE:repeated-value with_core4/5,without_core3/5. Same membership as C260,
but not independent retraining. Acceptance:docs/experiment-ledger-addendum-c261-c262.md.
C260 ACCEPTED VALID NEGATIVE:Full4/5,core-free3/5;direction reverses at260005. No global winner.
Acceptance:docs/experiment-ledger-addendum-c260-c261.md.
C259 ACCEPTED VALID NEGATIVE:six-order4/5,two-order2/5. C258 diagnostic PASS only.
C257 unseen-order2/5 remains negative. C256 bounded three-entity task-shift PASS5/5 remains.
C256's precheck INVALID and C255's invalid attempts remain in their execution-recovery addenda.
C255/C254/C253 diagnostic passes do not rescue C252's4/5 accepted negative. C251/C250 and earlier
scopes/verdicts remain. Complete historical identities and review details are retained in all
acceptance/recovery addenda and the prior handoff at abca8d7eb25146fca6f7404790071d1e6f0999d0.
Preserve accepted code,tests,logs,checkpoints,recovery records and tools/run_c167.ps1.

## Active C264 — frozen two-fact deletion

Experiment:C264-v5b-frozen-two-fact-deletion. Stage:V5-B-FROZEN-TWO-FACT-DELETION.
One question:do all twenty frozen C263 final states retain correct answers after one unqueried
fact is deleted,leaving only two facts? No new training,seed search or optimizer intervention.
Example:a=0;b=1;c=2;b= -> a=0;b=1;b=;target1 is unchanged. Never remove the queried fact.

Retain seeds263001..263005 and all four C263 rate/order arms in their accepted identity order.
Every model is the actual unchanged C252 Full aligned reader,14256 parameters,created via the
C256.make_model/C231 factory then strict-loaded with its C263 final state. Use actual C263.load_bundle
once for its20-state fold-c263-rate-models-v1 archive. Verify final fingerprint and freeze eval mode
and requires_grad. Fresh wrapper construction is not new training or a fresh learned checkpoint.
Do not choose a learning rate or a subset of models based on the new results.

Changed:visible fact count3->2 through deletion of an unqueried fact. Effective input length and
positions change together. Held fixed:weights,architecture,known names,values0..3,distinct retained
values,query,target,delimiter syntax and48-slot BOS/bytes/EOS/PAD encoding. Only visible bytes and
zero task IDs enter the model;no deletion index,source partition,oracle label or hidden target.
No canonicalization back to three facts or sorting into a preferred order before inference.

Dataset:all three entity subsets(0,1),(0,2),(1,2),all12 ordered distinct value pairs,both identifier
languages,both visible orders,and both queries. Exactly288 unique prompts. Dataset SHA256:
8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1.
Project all864 accepted C263 normal rows by each of their two unqueried deletions:1728 provenance
edges,six full parents per reduced prompt(two deleted values x three insertion positions).
Score each reduced prompt once. Preserve all parent stage/split/source IDs and removed entities.
Deletion must preserve target semantics. Reconstruct the same sorted provenance in saved postcheck.
Reduced prompts may cross the original TRAIN/HOLDOUT projection,so they carry NO new split label.
Old partition labels apply only to replay anchors. Retained pairwise associations are familiar;
this tests fact-count/deletion transfer,not new-value or new-name learning.

## C264 fixed gate and inference sequence

Each state reports12 language/subset/order cells,each24 answers and12 paired-query groups.
Require accuracy>=.90(22/24),both-query correctness>=.80(10/12),evidence-mask drop>=.35 and
query-mask drop>=.35. The two target values differ,so a query-blind displayed-value guess can score
one half;unlike all-equal cases,this query-drop criterion is compatible with perfect normal answers.
Also require two-order consistency>=.80 for every language/subset:20/24 groups where the same
assignment/query must be correct in both presentations. Do not pool away a weak subset or language.
C264 primary PASS iff ALL20 states meet every criterion. Report all four arm pass counts separately.
This is a new frozen-task gate,not an amendment of C263's lower-rate gate. A valid miss is accepted
negative and does not authorize learning on the reduced prompts or tuning the thresholds.

Per model sequence:
1.Actual C259.evaluate on all accepted original/extra splits/views:12 forwards/2592 rows.
2.Match raw logits to C263 saved final outputs within1e-9 and exact argmax BEFORE new inputs.
3.Two-fact prompts in two144-row batches per view,three views:6 forwards/864 rows.
4.Repeat original evaluation:12 forwards/2592 rows;match both anchor and accepted reference.
5.Verify full state unchanged,30 wrapper forwards/6048 rows/120 Full core calls;remove hooks on errors.

Totals:20 models,600 wrapper forwards,120960 row presentations,2400 core calls,training0,new learned
checkpoints0,accepted bundle loads1,strict final-state loads20. CPU float64,threads2,deterministic;
nonfinite outputs,identity/count mismatch or replay failure is an integrity fault. Expected raw
output tensor payload247726080 bytes(about248 MB decimal),plus metadata/JSON. No storage/speed claim.
Parent metric reconstruction,file hashing and historical test fixtures are additional work,not
new scientific samples or extra formal model forwards.

## C264 parent interfaces,artifacts and protection

check_parent calls actual C263.validate_result and requires execution identity,PASS,all four arm
counts5,both rate_joint_pass values true and all six parent artifact hashes above. precheck verifies
parent hashes/sizes and inherited source/input identity. load_reference calls actual
C263.verify_artifacts(parent_dir,PARENT_EXECUTION) before model evaluation. Its saved-tensor metrics,
contrasts and schedules must reproduce the parent summary. Model calls are blocked during that
verification. The explicit second archive read obtains final_sha256 and raw.original/raw.extra
from fold-c263-rate-eval-v1,not guessed summary outputs. Original144x256/extra288x256 raw tensors per
split/view follow dataset.json's exact saved row order. Twenty reference identities are required.
Two reference archive loads per load_reference pass(parent verification+record read);one pass during
evaluation and one during saved postcheck,four reference loads total. No parent model rerun here.

Six ignored artifacts plus summary.json:deletion-plan.json,two-fact-dataset.json,provenance.json,
eval-outputs.pt,measurements.json,validation-summary.json. Evaluation schema fold-c264-deletion-eval-v1
stores20 records with final fingerprints,counters,replay errors and anchor/reduced/restored logits.
Persisted postcheck reconstructs parent references,every raw/argmax replay,provenance,metrics and gates.
No model construction,model forward or learned-bundle load is performed in saved postcheck;module
calls are blocked. Hashes/sizes and JSON equality must pass. Only console text logs publish to Git.

Protection:430 pins/723 inputs=parent424/710 plus OWN6 and parent summary+SIX artifacts.
Direct deciding dependency union40=five C231 LM sources+C230..C263 helpers+C264;lazy imports included.
Own24;modules149;loaded3502/focused3501. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1.
Registration:docs/experiment-ledger-addendum-c264-preregistration.md.
Design:docs/v5b-two-fact-deletion-v0.1.md. C263 acceptance and C264 registration are separate commits.
Deletion changes fact count,length and positions jointly;no unique internal-cause or arbitrary-length
reasoning claim. The finite symbolic family has been inspected and uses familiar names/values.
No independent general benchmark,ordinary language,learning-rate benefit,default optimizer change,
architecture adoption,production readiness or Gate F claim. All prior verdicts remain unchanged.

## C264 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 28f5f03b4dd57821a542bf8be946aa97d9836dbf
Scope:committed-byte C264 authoring validation using explicit synthetic fixtures,NOT formal execution.

All SIX committed OWN files were re-fetched and read completely. Each complete local file was
independently Git-blob hashed and matched to the returned remote identity before the final own run:
-benchmark:8714a23b1996e4d136b362dadc137e3c7e1981ef;23043 bytes.
-tests:54c24d509f5930f8172bc230d27a4a0b49f589f5;19632 bytes.
-runner:31a18699a69c080b1a4f21f47b76987bd7587e39;4657 bytes.
-launcher:53ef1e8680a47a4da34fc91b3891fb9962227717;2638 bytes.
-preregistration:a46cc266ebc299a9596990911d34648cd3954cc0;9882 bytes.
-design:c532dd70f9824e101d6256ef266d2ab0df9bafbb;3162 bytes.

First exact own suite:24/24 PASS in8.487s.
After complete committed-file readback and six blob matches:24/24 PASS in7.568s.
No code/test correction was needed after the first passing suite. UTF-8/NUL checks,Python compile/
import,manifest and dataset fixed hashes,semantic24-test identity count and three embedded Python
blocks passed. Recursive global-name audit inspected68 locally defined functions/methods and112
code objects,including nested code,with zero unresolved LOAD_GLOBAL names. Provenance reconstructs
288 unique reduced rows and1728 source edges. CLI indices:precheck1,regression none,postcheck1/2/3.
Dependency regex/count arithmetic and247726080-byte tensor payload were checked by actual own tests.
The dummy historical suite checks filtering only;it is not execution of3501 tests.

The tests use a clearly labeled string-parser Oracle with14256 placeholder parameters and Identity
core counters,plus self-contained Base/Factory/Trainer/CoreCounter/Audit adapters. This is NOT
actual FOLD computation or learned-capability evidence. Test16 runs the actual new probe and checks
30/6048/120 counters. Test20 executes actual twenty-model run/probe/scoring/provenance/persistence/
saved-postcheck code with those adapters;it does not substitute the new probe or scoring functions.
Test19 executes the actual reference-loader function with a mocked parent validator and temporary
archive,checking the two-argument parent dispatch. Other tests cover masks,target preservation,
projection deduplication/split crossing,per-cell gates,exact argmax,mutation/mode guards,hook cleanup,
wrong saved HEAD,artifact corruption and prohibition/restoration of model calls in saved verification.
No complete historical parent modules or learned user artifacts were locally available.

Actual C263 writer/run/verify/load semantics and parent context were source-reviewed;the saved
schema is final-state raw.original/raw.extra,not initial or intermediate outputs. Actual C256
original-row generator and C257 novel-row renderer/generator were re-read to verify the provenance
fields,order semantics,identifiers,targets and144/288 row shapes. The existing active dispatcher was
re-read:it resolves one formal ACTIVE token and parses the selected launcher before invocation.
Launcher operational guards and its runner parser precede scientific logging/publication.
Compared C263 log commit to review HEAD:seven additions only(C263 acceptance plus six C264 files).
No accepted source,test,log,runner,shared dispatcher or CI file was edited. Only this activation
handoff follows review.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Container GitHub DNS resolution failed;
no complete checkout or user-local learned artifacts were available. PowerShell/pwsh absent;
Windows System.Management.Automation.Language.Parser.ParseFile was NOT run here. Standard command
parses dispatcher;dispatcher parses launcher;launcher parses runner. All are mandatory on Windows.
Pending authoritative checks:Windows parser chain,real430/723 source/artifact precheck,own24 through
full repository dependencies,complete3501 regression,twenty actual frozen-state evaluations,
strict checkpoint/anchor replay,persisted postcheck and log publication. None is claimed complete
by this authoring review. Use FINAL activation branch HEAD,not review_target_HEAD or parent HEAD.
Re-read the final branch ref before issuing ExpectedHead. C265 waits for C264 judgment.

## Execution and stop

Use tools/invoke_active.ps1. Formal state has exactly one ACTIVE token resolving to C264.
Fixed parent:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent/task precheck ->own24 ->focused3501
->twenty frozen-model evaluations ->persisted postcheck ->log publication.
Progress:model1/20..20/20;no800-step training loop. A complete valid FAIL is scientific negative,
not INVALID. Do not retrain,select states,change data or relax gates after results.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE:operational SKIPPED before logging;
no scientific execution or log publication. Source/artifact/schema/nonfinite/identity/count/replay/
test faults stop and require minimal SAME C264 repair. No C265 registration on an invalid run.
Log-only publication failure is repaired without repeating completed evaluation. The user normally
sends only 'finished';fetch docs/experiment-run-logs/c264/latest.json/latest.log for judgment.
Do not advance this branch with unrelated work during the user's formal run/log publication.
Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite or CI changes. Preserve all accepted evidence,recovery records and run_c167.ps1.
Judge C264 before C265.
