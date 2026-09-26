# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C262 ACCEPTED VALID NEGATIVE. C263 ACTIVE / NOT YET JUDGED. C264 NOT REGISTERED.**
C263 is the unique ACTIVE experiment:V5-B learning rate by minibatch chronology.
C262's joint robustness gate missed:forward_blocks0/5,reverse_blocks2/5. The valid
comparison nevertheless demonstrates sensitivity to its specified chronology change.
Do not confuse a capability-gate miss with absence of a scientifically useful effect.
All earlier verdicts and recovery records remain. No production adoption,architecture
selection,core-superiority,general-language or Gate F promotion.

## Latest accepted evidence — C262

Scientific execution HEAD:28030ad02e69a9ae7236fca7f7e84a61f3c89c46.
Published log commit:4dc8fec24578efa5f7d8abfea17c56be2dc23673.
Publisher log SHA256:9dc5f6850866548f8f1e3a6681e2aab58069c36526d3355321ae814c05d502f7.
Log bytes:768728; lines3833.
Summary SHA256:9cda47219d6e376516044d5807e546a8c13110f584f139bda2a3da8800b2d93d.
Summary:runs/c262-v5b-batch-order-b955446fc91846aa9fea770cd36b9276/summary.json.
Acceptance:docs/experiment-ledger-addendum-c262-c263.md.
Acceptance/base commit:9edbef91d9a5bc81427b93003bae9127032643be.

Own24 PASS in5.976s; focused3453 PASS in314.228s. Source pins418/protected inputs697.
Ten models completed800 updates each:8000 updates,384000 training rows,8240 wrapper
forwards,435840 row presentations,32960 core calls. One ten-state bundle write/load;
ten strict state loads. Complete initial state and exact exposure counts matched;
chronology hashes differed. Weight-change,strict checkpoint/logit/argmax replay,
score/flip reconciliation,persisted reconstruction and protected-input checks passed.
Tracked tree clean;scientific execution HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;joint_gate=False;all_pairs_matched=True;all_replays=True.

Acceptance uses immutable published log ranges,metadata and recorded local postchecks.
The reviewer did not independently execute the learned checkpoints or rehash the full
768728-byte console log. Publisher-reported SHA256 is not a new reviewer byte hash.
Execution/metadata/summary identities agree. Publication is one commit after execution
and changes only docs/experiment-run-logs/c262/latest.json and latest.log.

Deciding HOLDOUT all-six-order correct counts,denominator216 per language:

|Seed|Forward EN|Forward JA|Reverse EN|Reverse JA|Forward gate|Reverse gate|
|---:|---:|---:|---:|---:|---|---|
|262001|202|197|216|216|ORIGINAL_CRITERIA_MISS|PASS|
|262002|156|161|132|129|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|262003|146|136|144|139|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|262004|123|124|150|152|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|262005|146|152|216|215|ORIGINAL_CRITERIA_MISS|PASS|

Pooled forward1543/2160=71.4352%;reverse1709/2160=79.1204%. Seven paired language
accuracies increase and three decrease;no ties. Pooling cannot replace the fixed gate.
Across2160 matched HOLDOUT answers:639 disagreements partition into201 forward-correct/
reverse-wrong,367 forward-wrong/reverse-correct and71 different wrong answers.
Net correct-count change367-201=166 equals1709-1543. These are correlated questions,
not2160 independent training runs. Reverse worsens seed262002;do not adopt it universally.
The new cohort differs from C259/C260;their seed counts are not paired regression controls.

Interpretation:with complete initial state and exact prompt exposures held constant,
this minibatch chronology intervention changes answers and held-assignment scores.
Initial weights alone cannot explain every observed training variation. No unique
optimizer mechanism or explanation of all historical failures is identified. All fact
orders were training-visible,and the authored task has been repeatedly inspected.
No general-language,independent-benchmark,core-superiority or deployment claim.

Accepted C262 artifacts:
-batch-plan.json:2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c;2869 bytes.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:f360dccf8b5523b27755e87734b0ae1c1b4ab8628b4e9c3fb32ada20f102db2f;53132231 bytes.
-measurements.json:13ffc5ce99372df17914f5a8cc07e03ba63e74cd091a24e650db62c6273e5e8d;62906 bytes.
-trained-models.pt:84ce31fe704c193a9a5f17a0e9023b9f6d4dc84fd25badafd118a95738595713;1238007 bytes.
-validation-summary.json:d2843f6443c759795f50f81e68fc35cf742c28f3657716812207b756aab4c864;4308 bytes.

## Preserved earlier evidence and recovery

C261 ACCEPTED VALID NEGATIVE:repeated-value with_core4/5,without_core3/5. The successful
and unsuccessful state membership matches C260 descriptively;not independent training.
Execution5de24467fd439378505a2357e898fc618de31d45;log d441c7e5a699bbb55558261a910483057b70e0f3.
Summary SHA256:555ea1f2a1ae6970283d9b7784b0e382f6f58be202d493c0157c706c1255f9bf.
Acceptance:docs/experiment-ledger-addendum-c261-c262.md. Its query-mask drops are correctly
descriptive on duplicate-target strata;no older metric contract was retrospectively changed.
C260 ACCEPTED VALID NEGATIVE:Full4/5,core-free3/5;comparison reverses at260005.
Acceptance:docs/experiment-ledger-addendum-c260-c261.md. No global architecture winner.
C259 ACCEPTED VALID NEGATIVE:six-order4/5,two-order2/5. C258 diagnostic PASS only;
C257 unseen-order2/5 remains negative. C256 bounded three-entity task-shift PASS5/5.
C256's precheck INVALID and C255's invalid attempts remain in their recovery addenda.
C255/C254/C253 diagnostic passes do not rescue C252's4/5 accepted negative.
C251/C250 and earlier scopes/verdicts remain unchanged. Complete historical identities
and review details are retained in acceptance/recovery addenda and the prior handoff at
28030ad02e69a9ae7236fca7f7e84a61f3c89c46. Preserve accepted code/tests/logs and run_c167.ps1.

## Active C263 — learning rate by minibatch chronology

Experiment:C263-v5b-learning-rate-order. Stage:V5-B-LEARNING-RATE-ORDER.
One question:does lowering AdamW learning rate0.005 to0.001 reduce sensitivity to the
same forward/reverse minibatch intervention while retaining fixed criteria at800 updates?
This is one predefined2x2 comparison,not a rate sweep or a retry of failed learned states.

Fresh seeds263001..263005. Four arms per seed,in exact order:
standard_forward,standard_reverse,lower_forward,lower_reverse.
Standard arms lr0.005;lower arms lr0.001. All actual C252 Full aligned readers,14256
parameters,through protected C256.make_model/C231 factory. Each four-model group clones
one complete fresh initial state;no shared tensor storage or accepted checkpoint reuse.
Same-order rate pairs receive exactly the same minibatch at each update. All four arms
have identical final prompt exposure counts. Full initial fingerprints are checked.

Keep batch48,800 updates,AdamW betas0.9/0.999,eps1e-8,weight_decay0,global clip1.
Fit RNG resets to seed+259000 per arm. CPU float64,threads2,deterministic algorithms.
Only learning rate changes within each chronology. Later gradient/optimizer trajectory
changes are allowed consequences,not additional independent interventions. No early
stop,extra steps,rate schedule,checkpoint selection,seed replacement or rescue rate.
Smaller rate may underfit at800 updates;accept that result rather than extending it.

Same distinct-value C256 assignment partition and C257 all-six-order rendering,not C261
repeated cases. Original SHA256:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
Extra SHA256:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Twelve TRAIN/twelve HOLDOUT assignments,EN/JA identifiers,three distinct values0..3,
three queries,48-slot byte input. Original144+extra288=432 rows/split,216 per language.
Actual C259.training_tables builds TRAIN-only3x144x48 tokens+144 targets. No HOLDOUT
optimization or oracle metadata input. All fact orders are taught in both chronologies.

C262 schedule for fresh seeds:epoch=step//3,offset=step%3;randperm144 seed+256000+epoch;
48-row blocks;fact-order pair=epoch%3. Complete epochs forward0,1,2 versusreverse2,1,0.
Final steps798/799 forward0,1 versusreverse1,0;block2 omitted in BOTH. No extra update.
Within-batch row order is preserved;only minibatch chronology changes. Fact-order pair
updates267/267/266. Save and regenerate full432-prompt exposure counts,their SHA256,and
chronology SHA256. Exposures match all four;chronology matches rates at the same order
and differs between orders. The fit function indexes the saved schedule directly.

## C263 capability gate and comparisons

Use actual C260.score and protected C256/C257 scoring helpers unchanged. Every state is
scored on both languages,both TRAIN/HOLDOUT splits,all original and extra orders/views.
Original accuracy>=.90,order_pair>=.80,query_triplet>=.80,evidence/query drops>=.35.
Each extra order separately accuracy>=.90,query_triplet>=.80,evidence/query drops>=.35.
All-six-order consistency>=.80. Extra cells require33/36 answers and10/12 triplets;
six-order groups require29/36. No previously accepted threshold is changed.

Primary C263 PASS iff all TEN lower-rate states pass,both chronologies and all five seeds.
Standard-rate joint gates and each four-arm pass count are reported separately. This is
a new treatment gate,not retrospective relaxation of C262's joint all-ten criterion.
Standard outcomes cannot rescue or fail the lower-rate gate. Valid lower-rate criterion
misses are accepted negatives,including insufficient learning within the fixed budget.

Report20 rate contrasts(lower minus standard at same order/seed/language),20 order
contrasts(reverse minus forward at same rate/seed/language),and10 interaction records.
Each uses216 matched HOLDOUT answers. Actual C262.compare_answers reports disagreements,
correct-to-wrong,wrong-to-correct and different wrong answers;reconcile score differences.
Interaction disagreement_delta=lower-rate disagreements minus standard disagreements.
Report each rate's worse chronology accuracy alongside it. Identical wrong answers can
produce zero disagreement;that is not useful robustness. Primary capability PASS alone
also does not establish an LR advantage,as both rates might pass. Comparisons are
descriptive;no population guarantee,statistical significance or unique mechanism claim.
learning_rate_benefit_claim=False prevents automatic benefit claims from a PASS flag.

## C263 workload,artifacts and protection

Twenty models,not ten. Each800 updates:16000 updates/768000 training rows.
Per model train+final812 forwards/40992 rows;strict replay12/2592. Total16480 wrappers,
871680 rows,65920 Full core calls,480 evaluation/replay forwards. Twice C262's model work.
One new20-state bundle write/load;20 strict state loads;network calls0. Approximate final
raw-logit payload106 MB plus weights/records/JSON. Historical tests,parent saved-output
recomputation,schedule rebuilding and file hashing are separate computational work.

Six ignored artifacts plus summary.json:rate-plan.json,dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Bundle schema fold-c263-rate-models-v1
contains20 final states in seed/arm order. Eval schema fold-c263-rate-eval-v1 contains
final original/extra logits,initial/final fingerprints,fit/rate/schedule records and counters.
Actual C262.replay_one ->C259.replay_one strictly loads states,preserves final fingerprint,
requires exact argmax and all-view logit error<=1e-9,counts12/2592 and48 core calls.
Persisted postcheck rebuilds metrics,schedules,flips and interactions from saved tensors,
without another model construction,forward or learned-bundle load. JSON/hash checks remain.

load_parent checks the accepted C262 summary SHA,then calls actual
C262.verify_artifacts(parent_directory,PARENT_EXECUTION). Require its status FAIL,
forward_blocks0/reverse_blocks2,ten measurement records and all six artifact identities.
This validates saved parent scores/schedules rather than rerunning old model inference;
no parent checkpoint initializes the new models. precheck invokes load_parent.

Protection:424 source pins/710 protected inputs=418/697 plus OWN6 and parent summary+SIX artifacts.
Direct deciding dependency union39=five C231 LM sources+C230..C262 helpers+C263.
Own24;modules148;loaded3478/focused3477. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305.
Registration:docs/experiment-ledger-addendum-c263-preregistration.md.
Design:docs/v5b-learning-rate-order-v0.1.md. C262 acceptance and C263 preregistration are separate commits.

## C263 post-authoring review

post_authoring_review = PASS
review_target_HEAD = abaf759facbd784f7ae67f7ba84f7af79bcc1fc1
Scope:committed-byte new-file authoring validation with limited parent-fixture dependencies,
NOT a formal C263 scientific run or complete historical checkout verification.

All SIX committed OWN files were re-fetched/read and their complete locally held UTF-8
bytes independently Git-blob hashed to match the returned remote identities:
-benchmark:72a8e0431b4df3aa6bf31ca9992755dd6a644c49;22626 bytes.
-tests:3d4e9322484e6ede46573a56760a01543ff7dca7;17092 bytes.
-runner:5619d62f75e2d2eb0bd87b86013577df4f5ebe9f;5480 bytes.
-launcher:01b82b20dd253b4108ad78d8c4dda1149a43d92c;2639 bytes.
-preregistration:71fe1abf89c9889f250272d25f1ddf1c1e2999df;10126 bytes.
-design:52d1619a5af97a735b64cdca07cedea57f58b5e9;3410 bytes.

First exact new own suite:24/24 PASS in8.061s.
After six-file committed readback and blob matching:24/24 PASS in8.504s.
No source/test correction was needed after the first passing suite. UTF-8/NUL checks,
Python compile/import,recursive bytecode global binding audit(zero unresolved names),
fixed manifest/dataset hashes and semantic24-test count passed. Embedded Python blocks3,
CLI indices precheck1,regression none,postcheck1/2/3. Tests inspect actual run/precheck call
order and launcher parser/operational guards before execution/logging/publication.

Exact tests cover optimizer dispatch to both fixed rates,all four arm identities,all
five seeds' complete epoch/tail reversal and equal exposures,clone isolation,wrong
metadata/identities/nonfinite values,per-order and six-order gates,twenty-state
orchestration,persisted recomputation,directional flips and rate/order interactions.
An explicit negative fixture makes both lower-rate models equally wrong and confirms
that zero disagreement does not pass capability. Test07 executes the actual new800-update
loop and parent replay wrapper on synthetic Tiny;test06 uses a test-only3-step budget.
Test20 substitutes training records while exercising actual20-state orchestration,
replay and persistence. Test19 mocks parent validation to check the real two-argument
loader dispatch. Test22's3478 dummy IDs validate filtering,not3477 historical tests.

Important dependency limitation:the complete NEW C263 files above are exact committed
bytes. The reviewer lacked a full checkout;review-only local C262 dependency modules
were reconstructed from retrieved code excerpts:its exercised require/compare_answers/
replay_one bodies and its synthetic Tiny/Factory/Base/Orders/Trainer/Scorer/Audit class
definitions. They are NOT the complete parent modules and were NOT published. The
committed new test imports those named fixtures from the actual accepted C262 test module,
not its TestCase. Therefore the exact24 new methods passed with limited reconstructed
parent-fixture dependencies,not the entire real repository import graph. No synthetic
result is FOLD learned capability evidence. User-side own tests must run with full parents.
Actual C262 writer/validator/replay fields and parent call signatures were source-reviewed;
real parent artifact/source protection and full historical dependency checks remain pending.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Container raw.githubusercontent.com
DNS failed;no complete checkout or user-local learned artifacts were available. PowerShell
and pwsh were absent,so Windows System.Management.Automation.Language.Parser.ParseFile
was NOT run here. The standard command parses dispatcher;dispatcher parses selected
launcher;launcher parses runner before use. The Windows checks remain mandatory.
Compare C262 log commit to review target:seven additions only(C262 acceptance+six C263 files).
No accepted source,test,log,runner,shared dispatcher or CI file changed. Only this
activation handoff follows review. Review status does not imply actual20-model execution.

Pending authoritative checks:Windows parser chain,real424/710 source/artifact precheck,
exact own24 through complete user-repository dependencies,full3477 regression,twenty
real Full-model training runs,strict learned-checkpoint replay,persisted postcheck and
log publication. Use FINAL activation branch HEAD,not review_target_HEAD or a parent
execution/log commit. Re-read final branch ref before issuing ExpectedHead.

## Execution and stop

Use tools/invoke_active.ps1. Formal state contains exactly one ACTIVE token resolving to C263.
Fixed parent:runs/c262-v5b-batch-order-b955446fc91846aa9fea770cd36b9276/summary.json.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent/task precheck ->own24
->focused3477 ->twenty-model paired training ->strict replay ->persisted postcheck ->log publication.
Progress:model1/20..20/20;each model step200/400/600/800. Valid FAIL is a scientific negative,
not INVALID. Do not increase steps,replace rates,seeds or schedules,or relax criteria.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE are operational SKIPPED
before logging;no scientific execution or log publication. Source/artifact/schema/nonfinite/
identity/count/replay/test faults stop and require minimal SAME C263 repair. C264 is not
registered before judgment. Log-only publication failures are repaired without retraining.
The user normally sends only 'finished';fetch docs/experiment-run-logs/c263/latest.json/latest.log.
Do not move this branch with unrelated work during the user's formal run/log publication.

Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,
cleanup,history rewrite or CI work. Preserve all accepted evidence,recovery records
and tools/run_c167.ps1. Judge C263 before C264.
