# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository: akakishi04/fold. Branch: feat/sft-target-loss. Local: M:\asobiba\fold.
Authoritative runtime: Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C261 ACCEPTED VALID NEGATIVE. C262 ACTIVE / NOT YET JUDGED. C263 NOT REGISTERED.**
C262 is the unique ACTIVE experiment: V5-B paired minibatch chronology.
C261 required both arms to pass all five states on the new repeated-value task; it obtained
with_core4/5 and without_core3/5. This is a scientific miss, not an execution fault.
Preserve all earlier verdicts and recovery records. No production adoption, architecture selection,
core-superiority claim, general-language claim or Gate F promotion.

## Latest accepted evidence — C261

Scientific execution HEAD: 5de24467fd439378505a2357e898fc618de31d45.
Published log commit: d441c7e5a699bbb55558261a910483057b70e0f3.
Publisher log SHA256: 1341aa09aaaab7f78a3aabadaaf4263cd6bdaa2c71fcdc695d1dbda0459d8bb6.
Log bytes: 786878.
Summary SHA256: 555ea1f2a1ae6970283d9b7784b0e382f6f58be202d493c0157c706c1255f9bf.
Summary: runs/c261-v5b-repeat-value-66e5eb87a146491e833bbd2f32ce6989/summary.json.
Acceptance: docs/experiment-ledger-addendum-c261-c262.md.
Acceptance/base commit: d83c37ad2febed01d1f5c94d6f60fa87f42dafda.

Own24 PASS in10.060s; focused3429 PASS in153.846s.
412 source pins/685 protected inputs passed. All ten final frozen states completed:
540 model forwards,95040 row presentations,1080 Full core calls,one learned bundle load,ten strict
state loads. Training0;new learned checkpoints0. Accepted-output anchor replay,restoration,finite
outputs,weight preservation,persisted score reconstruction andprotected-input checks passed.
Tracked tree clean;scientific execution HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;joint_gate=False;all_replays=True;all_weights_preserved=True.

Acceptance is based on immutable published log ranges,metadata andrecorded local postchecks.
The reviewer did not independently run the learned states orrehash the entire786878-byte log.
Publisher SHA256 is an identity reported by the publisher,not a newly computed reviewer byte hash.
Metadata,registered execution HEAD andprinted summary agree. Publication changes only C261 latest.*.

Per-state repeated-value gates:

|Seed|with_core|without_core|
|---:|---|---|
|260001|PASS|PASS|
|260002|PASS|FAIL|
|260003|PASS|PASS|
|260004|PASS|FAIL|
|260005|FAIL|PASS|

This is exactly the same pass/fail membership as C260's distinct-value task,although assignments and
metric contracts differ. The seven previously passing states also pass the new repeated-value gate;
the other three remain below its criteria. This is descriptive correspondence,not an independent
replication or a universal predictor of future behavior.

Failing new-task totals:without_core260002=999/1440;without_core260004=972/1440;
with_core260005=836/1440. Pooled totals do not replace per-language/order/stratum criteria.
Example:without_core260002 EN pair_equal order012 gives79/108 answers,30/36 singleton questions,
49/72 repeated-target questions and11/36 complete query triplets;EN all_equal order012 gives8/12.
Successful with_core260001 andwithout_core260001 each score1440/1440. Do not invent unreported
perfect scores for the other passing states solely from their PASS flags.
Query-mask drop was correctly descriptive only in C261;the remaining misses are not caused by
blindly reusing the old distinct-target query-drop threshold.

Interpretation:repeated values did not introduce another failed state among the seven C260 successes.
The failure pattern spans both tested variants;it does not establish a unique internal cause.
An earlier explanation in terms of initial weights alone was too specific:the training seed also
controlled minibatch generation. C260.make_pair uses the seed for initialization,while its batch_plan
uses seed+256000+epoch. C261 freezes both outcomes andcannot isolate these training factors.
C262 therefore holds the complete starting state andthe example exposure totals fixed while changing
only the chronological order of the same minibatches.

Accepted C261 artifacts:
-eval-outputs.pt:ad2b19919cae9a258aef91e6c50596ab3624ab4df6b86f1b251c9a5b75c81fd2;194720583 bytes.
-measurements.json:1f0b7d3e23f14ea744683cd90c504e82e95d307b6668cfaa3047e6310d25934b;93956 bytes.
-repeat-dataset.json:1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339;245666 bytes.
-repeat-plan.json:bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301;2708 bytes.
-validation-summary.json:fc1926548185238f6464bdf30900597d4147eb58be767be14aed901d6b6fa962;826 bytes.

## Preserved earlier evidence and recovery

C260 ACCEPTED VALID NEGATIVE:Full4/5,core-free3/5;pooled HOLDOUT1952/2160 versus1804/2160.
Execution5788a63a692983094a9c6311c58d1440005b7fca;log e841aa5c312d46bfe11172af45262433cf5ec33d.
Acceptance:docs/experiment-ledger-addendum-c260-c261.md. Comparison direction reverses for260005;
no general winner or core removal was authorized. Parameters14256 versus10928 were not matched.
C259 ACCEPTED VALID NEGATIVE:six-order4/5 versus two-order2/5;HOLDOUT1984/2160 versus1704/2160.
Execution78f0811c390d11256e748b1f955f505ad803de49;log9f7abcc2ea2d88b78a2348e693b2850874f56cb6.
Acceptance:docs/experiment-ledger-addendum-c259-c260.md. No failed-seed rescue or extra steps.
C258 diagnostic PASS only:8640 saved answers;no new model inference/training.
Acceptance:docs/experiment-ledger-addendum-c258-c259.md. A universal middle-value shortcut did not
explain all states/spellings. Its saved-answer decomposition was exploratory,not a capability repair.
C257 valid negative:unseen-order2/5,novel HOLDOUT1187/1440.
Acceptance:docs/experiment-ledger-addendum-c257-c258.md. EOS original criteria were already unmet.
C256 bounded PASS:reader5/5,TRAIN720/720,HOLDOUT718/720;EOS0/5,HOLDOUT248/720.
Acceptance:docs/experiment-ledger-addendum-c256-c257.md. Its first precheck INVALID remains in
experiment-ledger-addendum-c256-execution-recovery.md;no scientific conditions were relaxed.
C255/C254/C253 diagnostic PASS;C255's two earlier invalid attempts remain in its recovery addendum.
C2524/5 remains valid negative. C2512/5;C250Full2/5,GRU4/5,EOS0/5. C249 diagnostic;C248 missed its
all-seed gate. C247/C246/C244/C242/C241/C239 negatives;C245/C243/C240/C237/C235 diagnostics;
C238 seen-prompt fit only. C232/C233 are not general-language orcore-superiority claims.
Detailed identities remain in all acceptance/recovery addenda andthe previous handoff at
 d441c7e5a699bbb55558261a910483057b70e0f3. Preserve accepted sources/tests/logs andtools/run_c167.ps1.

## Active C262 — paired minibatch chronology

Experiment:C262-v5b-paired-minibatch-order.
Stage:V5-B-PAIRED-MINIBATCH-ORDER.
Question:at identical Full aligned-reader initialization,exactly the same minibatches and800 updates,
does reversing their chronological order within an epoch alter held-assignment performance?
This changes minibatch processing order,NOT the visible fact order inside a given prompt.

Fresh seeds262001..262005. Both forward_blocks andreverse_blocks use actual C252 Full aligned readers,
through C256.make_model andthe protected C231 factory. Both14256 parameters. One fresh complete
wrapper is copied into both arms;equal initial fingerprints,unmodified template andno tensor aliasing.
No accepted learned checkpoint,activation,optimizer-state orfailed-seed selection initializes training.
Use the unchanged Full reference;neither previous architecture path is deleted oradopted globally.

Fixed task:C256 distinct-value assignment split andC257's all-six-order presentations,not C261's
repeated-value data. Twelve TRAIN andtwelve HOLDOUT assignments;all3 queries,EN/JA identifiers,
query-at-end,delimiters and48-slot byte contract. HOLDOUT never enters optimization.
Original dataset SHA256:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
Extra dataset SHA256:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Original144+extra288 rows/split;216/language. Actual C259.training_tables builds TRAIN-only3x144x48
input tokens and144 target IDs. No target/oracle metadata outside the visible input bytes.

Step s:epoch=s//3,offset=s%3. Generate randperm144 with seed+256000+epoch andsplit into48-row blocks.
Both arms use the same blocks andwithin-block row order. Fact-order pair=epoch%3 in both arms,
using pairs012/210,021/102,120/201 andthe original logical row's order bit.
Complete epoch:forward blocks0,1,2;reverse blocks2,1,0.
Final epoch266 has only steps798 and799:forward0,1;reverse1,0. Both omit block2.
Do not reverse into2,1 in the tail,which would silently change the examples taught.
No extra step is added. Pair-update counts267/267/266;total800 updates per model.
At a particular update the minibatches intentionally differ;consumed per-epoch batch multisets and
final exact prompt exposure totals are equal. Gradients/optimizer trajectories may diverge as effects.

Save chronology SHA256,exposure SHA256 andall432 exposure counts keyed by table_pair*144+logical_row.
fit directly indexes the registered800x48 row matrix and800 pair vector. Regenerate the schedule
from seed/arm during result verification. Pairwise initial state andexposures must match,while
chronology hashes must differ. Same prompt bytes andsame number of presentations across the pair.

Training:AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global clip1,batch48,800 updates.
CPU float64,threads2,deterministic algorithms. Reset fit RNG to seed+259000 per arm.
No early stop,extra training,checkpoint selection,seed replacement orpost-result threshold change.

## C262 fixed gate,comparisons andworkload

Primary joint PASS:BOTH batch-order arms pass all five fresh seeds under unchanged C260 distinct-task
criteria,on both languages andboth original assignment splits. Report arm counts independently.
Original cells:accuracy>=.90,order-pair>=.80,query-triplet>=.80,evidence/query drops>=.35.
Each additional fact order separately:accuracy>=.90,query-triplet>=.80,evidence/query drops>=.35.
All-six-order consistency>=.80. Additional cells36 answers/12 triplets need33/36 and10/12;
all-six consistency needs29/36 completely correct groups. Use actual C260.score/C256/C257 scorers.
One arm cannot rescue the other. A complete valid miss is ACCEPTED VALID NEGATIVE.

Report ten paired HOLDOUT language comparisons:reverse-minus-forward accuracy,each six-order score,
answer disagreements,correct-to-wrong,wrong-to-correct andboth-wrong-but-different answers.
Denominator216 each. Reconcile disagreement classes andcorrect-count changes. Equal aggregate scores
can hide different answers;raw-logit drift alone is not a correctness change.
Different paired outcomes can show sensitivity to this particular chronological intervention with
initialization/exposures fixed. They do not explain every earlier failure,prove initial weights are
irrelevant,oridentify a universal optimal curriculum. Equal outcomes do not prove every order safe.
No statistical significance,population guarantee,independent benchmark orinternal-cause claim.

Ten models x800 updates=8000 updates/384000 training rows.
Per model training+final812 forwards/40992 rows;strict replay12/2592.
Total8240 wrapper forwards/435840 rows;240 final/replay evaluation forwards.
Both branches use the Full core,four calls per wrapper:32960 core calls total.
Separate hooks enforce3248 train/final+48 replay per model. One new10-state bundle write/load;
ten strict state loads. Historical tests,parent hashing,schedule regeneration andserialization are
additional computational work,not independent science samples orpart of wrapper-forward counts.

Six ignored artifacts plus summary.json:batch-plan.json,dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json. Model schema fold-c262-batch-models-v1;ten final states in
seed/arm order. Eval schema fold-c262-batch-eval-v1 stores final original/extra logits,initial/final
fingerprints,fit schedule/exposure records,counters andstrict replay results. No initial/intermediate
outputs are presented as final. Approx53 MB raw final-logit payload plusweights/metadata;no speed claim.
Actual C259.replay_one strict-loads,checks final fingerprint,exact argmax andraw error<=1e-9;
C262 additionally checks core calls. Saved postcheck reconstructs schedules,scores,flips andgates
without new model construction,forward orlearned-bundle load. Stored JSON must match exactly.

Parent contract:load_parent requires C261.validate_result,accepted execution,status FAIL andcounts
with_core4/without_core3;checks all five artifact hashes/sizes,saved validation summary andC261.manifest.
No incorrect call to C261's multi-parent verify_artifacts signature. Parent artifacts are provenance,
not training examples orinitial weights. No parent learned-weight load orclaimed new parent-tensor replay.
precheck calls this loader andinherits all source/input protections.

Protection:418 source pins/697 inputs=parent412/685 +OWN6 +parent summary/FIVE artifacts.
Direct dependency union38:five C231 LM files,C230..C261 helpers,andC262. Lazy dependencies included.
Own24;modules147;loaded3454/focused3453. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c.
Registration:docs/experiment-ledger-addendum-c262-preregistration.md.
Design:docs/v5b-minibatch-order-v0.1.md. C261 acceptance andC262 preregistration are separate commits.
All six fact orders are training-visible andthe authored family has been inspected. No general
language,core superiority,production adoption orGate F claim. No C261 criterion is amended.

## C262 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 12f8bbbcce5a6f2eb4d38a761e5169e21e458a07
Scope:committed-byte C262 authoring verification,NOT a formal scientific run.

All six OWN files were re-fetched andread after writing was complete. The complete four local
executable files were independently Git-blob hashed andmatched to returned remote identities:
-benchmark:a0509533d917b9b54d3d67e47a0680e32b21a7bb;22674 bytes.
-tests:075ef224368235b28e3d0d2ab1fea0bfef39084a;25524 bytes.
-runner:a358b56b3c824907eb65c767dc4f8869e90cf188;5435 bytes.
-launcher:09b0ee81131387a3ab03ca8cbf2b274b5f5a3397;2640 bytes.
Read/text-reviewed documentation identities:
-preregistration:dacef4355d5752d65a42dee30cfba66a905c829e;
-design:1ec5c56ffb1e2df03d7ce6c9a4bbe17f4fdb3ac0.
The two docs were text-reviewed,not independently locally rehashed.

First exact own suite:24/24 PASS in3.706s.
After remote readback andfour executable blob matches:24/24 PASS in3.810s.
No code/test correction was needed after the first passing run.
Executed UTF-8/NUL checks,Python compile/import,recursive bytecode global binding audit(zero unresolved
LOAD_GLOBAL names),manifest hash,both dataset hashes,andsemantic24-test identity count.
Exhaustively checked both schedules for all267 epochs andall five seeds:reverse batch correspondence,
identical432-prompt exposure counts,different chronology hashes,correct267/267/266 fact-order pair
counts,andthe final two-block tail. Dependency regex scope/cardinality andsource/input arithmetic
were checked using expected synthetic filenames,not represented as the full historical source audit.
Three embedded Python blocks compile;CLI indices precheck1,regression none,postcheck1/2/3.
Actual-function AST/source tests verify run sequencing andprecheck loader dispatch. Launcher branch,
tracked-tree,HEAD/ACTIVE guards andrunner parser precede execution/logging/publication.

The exact tests use synthetic Tiny/Core,Base/Orders/Trainer/Scorer/Audit fixtures. The surrogate
Full model does NOT implement real FOLD/GRU computations. Test09 executes the actual C262800-update
train loop andstrict replay on Tiny;test08 has a test-only3-step budget. Test21 exercises actual
run/persisted-postcheck orchestration with substituted synthetic training records. Test20 exercises
actual load_parent with temporary artifacts andno learned-bundle load. Test22 constructs3454 dummy
IDs to test exclusion,NOT to claim3453 historical tests executed. These tests are authoring evidence,
not learned-model capability evidence orfull parent import-graph validation.

Actual C260 core_counter/score andseed-dependent batch_plan/make_pair were inspected;actual C259
replay_one argument order andrecord fields were checked. C261 result keys/counts andparent artifact
semantics were checked against published evidence andsource. The run uses parent result validators
rather than guessed summary field names. Full user-local source/artifact verification remains required.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No full historical checkout oruser-local
learned artifacts were available;container GitHub DNS failed. PowerShell absent:Windows ParseFile
was NOT executed here. The standard command parses dispatcher;dispatcher parses launcher;launcher
parses runner before use. All parser checks remain mandatory in the user's environment.
Compared C261 log commit to review target:seven additions only(C261 acceptance+six C262 files).
No accepted source,test,log,runner,shared dispatcher orCI file was modified. Only this handoff follows.

Pending authoritative checks:Windows parser chain,actual418/697 parent/source/input precheck,own24
in user runtime,complete3453 regression,ten actual Full-model training runs,real strict checkpoint
replay,persisted postcheck andlog publication. None is claimed complete by authoring review.
Use FINAL activation branch HEAD,not review_target_HEAD,parent scientific HEAD orlog commit.
Re-read final branch ref before issuing ExpectedHead. C263 waits for C262 judgment.

## Execution and stop

Use tools/invoke_active.ps1. Formal state contains exactly one ACTIVE token resolving to C262.
Parent path:runs/c261-v5b-repeat-value-66e5eb87a146491e833bbd2f32ce6989/summary.json.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent/task precheck ->own24 ->focused3453
->ten-model paired training ->strict checkpoint replay ->persisted postcheck ->log publication.
Progress:model1/10..10/10;each model step200/400/600/800. Valid FAIL is scientific negative,not INVALID.
Do not add updates,reselect seeds,change exposures orrelax gates to rescue it.

Wrong branch,dirty tracked tree,stale ExpectedHead orstale ACTIVE are operational SKIPPED before
logging;no scientific execution orlog publication. Source/artifact/schema/nonfinite/identity/count/
replay/test faults stop andrequire minimal SAME C262 repair. C263 is not registered on an invalid run.
Log-only publication failures are repaired without retraining. The user normally sends only
'finished';fetch docs/experiment-run-logs/c262/latest.json/latest.log for judgment.
Do not advance this branch with unrelated work while the user's formal run/log publication is active.

Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite orCI changes. Preserve all accepted evidence,recovery records andtools/run_c167.ps1.
Judge C262 before C263.
