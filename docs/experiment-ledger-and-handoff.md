# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C258 ACCEPTED PASS (diagnostic integrity only). C259 ACTIVE / NOT YET JUDGED. C260 NOT REGISTERED.**
C259 is the unique ACTIVE experiment:V5-B paired two-order versus six-order training.
C257 remains ACCEPTED VALID NEGATIVE; C256 remains ACCEPTED PASS in its original bounded scope.
C258's diagnostic PASS is not restored order-transfer capability or a confirmed causal mechanism.
No general-language,core-superiority,production-adoption or Gate F promotion.
All earlier accepted verdicts and invalid-attempt recovery records remain preserved.

## Latest accepted evidence — C258

Scientific execution HEAD:e31d4c28a00bc11fb5db3c2ba1b093e4eae15538.
Published log commit:62aac236dc90643dc57b3ed51855f79aeb22f1cd.
Publisher log SHA256:5a7ad7fff7846a76e43eec75542b8327de3a4ca42094e2c68d3e0d143dd32c64.
Log bytes:676199.
Summary SHA256:f6ccc7dc1b8c60c1f1e6bc7587bd9853eeb6bea6e1f7a010fd99de068bbd0ecc.
Local summary:runs/c258-v5b-middle-slot-93386fd77e3749bab4122685ff57720d/summary.json.
Acceptance record:docs/experiment-ledger-addendum-c258-c259.md.
Acceptance/base commit:db8fe078766353e3a3d8217eb6b595c22f10cfcd.

Own20 PASS in0.967s;focused3357 PASS in216.615s.
394 source pins/647 protected inputs verified. All8640 normal answers were attributed:
2880 known-order+5760 novel-order answers,720 order/query cells,120 pooled query cells,40 signatures.
Scientific model forwards0;state loads0;learned bundle loads0;training0;new learned checkpoints0.
One saved-evaluation archive load per analysis pass;scientific analysis and persisted postcheck are
two passes. Historical test computations and parent-file hashing are additional work.
Parent saved-output replay,integer accounting,zero denominators,protected-input checks and persisted
reattribution PASS. Tracked tree clean;scientific HEAD preserved;run_execution_valid=True.
scientific_status=PASS;capability_pass_claim=False;causal_mechanism_claim=False.

Acceptance uses immutable published log ranges,publication metadata and recorded local postchecks.
The reviewer did not independently rerun the user-local learned artifacts or rehash the entire
676199-byte log. Publisher-reported SHA256 is not an independent complete-byte rehash.

Deciding descriptive results:
-candidate novel HOLDOUT1187/1440 correct;253 errors=251 other displayed entity values+2 absent values;
-no out-of-task-byte errors;
-query b/乙 errors141/480(29.375%),pooled a/c errors112/960(11.6667%);
-among141 b errors:middle distractor64,other displayed distractor75,absent value2;
-middle share64/141=45.3901%,not a universal majority signature.

Candidate HOLDOUT error counts,not correct counts:

|Seed|b EN /48|b JA /48|a/c EN /96|a/c JA /96|b middle EN+JA|b other EN+JA|b absent|
|---:|---:|---:|---:|---:|---:|---:|---:|
|256001|0|0|0|0|0|0|0|
|256002|26|23|1|1|19|29|1|
|256003|32|31|30|13|32|31|0|
|256004|1|0|0|0|0|1|0|
|256005|6|22|36|31|13|14|1|

All candidate b known-order cells were24/24 correct. New b errors therefore match
known-both-correct -> novel-wrong cases. Seed256005 EN reverses the pooled pattern:
b errors12.5% versus a/c37.5%. Do not claim every failed seed has a b-only or middle-only failure.
Candidate novel TRAIN1177/1440 correct;263 other-entity errors,no absent/other-byte errors.
TRAIN b errors143/480 versus a/c120/960;middle b errors76 versus other displayed b errors67.
EOS novel HOLDOUT326/1440 correct,968 other-entity errors146 absent0 other bytes;
novel TRAIN805/1440 correct,551 other-entity84 absent0 other bytes. Keep controls separate.

This saved decomposition is exploratory and correlated with C257,not an independent confirmation.
A simple universal middle-value explanation does not account for all states/spellings. No unique
internal mechanism follows. C258 concludes the single saved-answer decomposition;C259 is a new
controlled training-policy experiment,not another internal-intervention chain or C257 rescue.

Accepted C258 artifacts:
-audit-plan.json:a4f2cad192bd56dd73d867caf8453084cdd85e8e0f10f9d2496bfaa4a6c08aef;2281 bytes.
-query-position-cells.json:d4bb64ac620e235b389447b52b4dea88b69466e4f77a3db8e363a0dfa330dea5;181209 bytes.
-row-attribution.json:b94b0224805512c049d3a6dfcee23c682dc700c33df705a750a4f71ea8475e85;2799697 bytes.
-signature-summary.json:e40bfcd11890866e1f02e77b662151a2d414df35b6c7d12c357afd9fa93b1644;20628 bytes.
-validation-summary.json:17d130b1b26545457a9419727548507d480aead01b02c8b6100d251969d95620;1595 bytes.

## Preserved earlier evidence and recovery

C257 ACCEPTED VALID NEGATIVE:only2/5 candidate seeds pass all unseen-order criteria.
Execution016785f35605a3eef5f94d42f0b86cb2fc4d9dfe;log4a322950685b80d7748aa525608555149c2c2ffd.
Summary SHA256:596df75ccc89c5a12c964c2e6be1fc689e5773f4c0a857f90fdcedd4df9b8816.
Summary:runs/c257-v5b-unseen-order-705d486739b44a56bbed34fae66ace89/summary.json.
Acceptance:docs/experiment-ledger-addendum-c257-c258.md.
Passed seeds256001/256004;256002/256003/256005 NEW_ORDER_MISS.
Novel HOLDOUT1187/1440;pooled accuracy cannot replace per-order gates. EOS original criteria were
already unmet;do not count those as five new independent failures caused solely by unseen orders.

C256 bounded ACCEPTED PASS:aligned reader5/5;TRAIN720/720;HOLDOUT718/720;EOS0/5,HOLDOUT248/720.
Executiondb9f3cb90d9268066c34fc91300193058301f06c;log5695706c6306156fa079ce092581270ca781af71.
Summary SHA256:56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184.
Summary:runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.
Acceptance:docs/experiment-ledger-addendum-c256-c257.md.
Its original precheck failure remains INVALID in docs/experiment-ledger-addendum-c256-execution-recovery.md:
failed execution1029158a60d40df24f599fb719411dbde2ffec06;invalid log2dc541041c772d5b9a449bd247862ad906a9b5c8.
The manifest-fingerprint and whitespace-sensitive test repairs did not change scientific conditions.

C255 diagnostic PASS:145/160 self versus140/160 value-swap HOLDOUT.
Execution6b577da1edc7339dbfd68b3127870074de218e48;log48856dd7dabb84f1f8a71158d03a5ee9db2fd255.
Acceptance:docs/experiment-ledger-addendum-c255-c256.md. Both earlier invalid attempts remain in
its execution-recovery addendum. C254 query96/160,order141/160,self145/160;diagnostic only.
C253 pre-residual107/160,reader-only117/160,self145/160;diagnostic only.
C252 aligned reader4/5,not5/5:ACCEPTED VALID NEGATIVE. C2512/5;C250 Full2/5,GRU4/5,EOS0/5.
C249 diagnostic;C248 bounded transfer but failed its all-seed gate.
C247/C246/C244/C242/C241/C239 remain accepted negatives;C245/C243/C240/C237/C235 diagnostics;
C238 seen-prompt fit only. C232/C233 are not general-language or core-superiority claims.
Preserve all accepted source/tests/logs and recovery records;do not edit tools/run_c167.ps1.

## Active C259 — paired order-coverage training

Experiment:C259-v5b-paired-order-coverage-training.
Stage:V5-B-PAIRED-ORDER-COVERAGE-TRAINING.
One question:at fixed architecture,initial state and800-update budget,does six-order training yield
reliable held-assignment performance across all six orders relative to a paired two-order reader?

Fresh seeds259001..259005. Both arms use actual C252.AlignedPrecoreReadout through C256.make_model
and the protected C231 factory. Both14256 parameters,including768 reader parameters,width16,48 slots.
No EOS-adapter arm:two_order and six_order use the SAME aligned-reader architecture.
Create one fresh complete wrapper per seed;deep-copy identical state into the pair.
Require full/backbone initial fingerprint equality,logical-batch digest equality,and changed
full/backbone/head final fingerprints. Fit RNG resets to seed+259000 per arm.
No accepted checkpoint,activation,optimizer-state or failed-seed selection initializes training.

Changed:the specified visible fact-order training policy only.
Held fixed:architecture,paired initial state,assignment/language/query/target exposure per step,
original assignment split,entity names,delimiter/byte contract,query placement,optimizer and budget.
Generate exact C256 data144 rows/split and C257 additional orders288 rows/split.
Original dataset SHA256:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
Additional dataset SHA256:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Twelve value assignments per split;HOLDOUT assignments never enter optimization.

Orders:012,210,021,102,120,201. Pairs:(012,210),(021,102),(120,201).
For zero-based step s,epoch=s//3,block=s%3. Draw randperm144 from seed+256000+epoch,take its48-row block.
Both arms use identical logical rows. Control uses pair0;treatment uses pair(epoch%3).
The original row order bit selects ORDERS[2*pair+bit]. Render it directly;no canonicalizing before
model input and no target/permutation/entity metadata outside visible bytes.
Every complete9 steps gives treatment all6 orders once per72 base questions.
Stop at800 including the registered incomplete tail:pair updates control[800,0,0],treatment[267,267,266].
TRAIN-only tables3x144x48 plus144 targets;control indexes table0 only.

Training:800 updates/model,batch48;AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1.
CPU float64,threads2,deterministic algorithms. No early stop,checkpoint selection,extra steps,
seed replacement or result-driven gate change.
Final evaluation:original6 forwards/864 rows plus extra6/1728=12/2592 per model.
Strict-checkpoint replay repeats12/2592. Train+final812/40992;with replay824/43584 per model.
Total10 models,8000 updates,384000 training presentations,8240 model forwards,435840 total rows.
Evaluation/replay forwards240;one newly trained10-state bundle write/load;ten strict state loads.
No network calls. Historical tests and file validation are separate work.

Fixed primary gate:ALL FIVE six_order seeds pass both languages and both assignment splits.
Original C256 cell criteria stay:accuracy>=.90,order_pair>=.80,query_triplet>=.80,evidence/query drops>=.35.
EACH additional order:accuracy>=.90,query_triplet>=.80,evidence/query drops>=.35.
All-six consistency>=.80. Additional cells36 rows/12 triplets:minima33/36 and10/12;
six-order groups36/language/split:minimum29/36 complete groups.
Control status is separate and cannot rescue/fail treatment. Report all cells and ten paired HOLDOUT
language comparisons of all-order accuracy(/216) and six-order consistency(/36).
A treatment PASS alone does not establish comparative benefit:both arms may pass.

Important boundary:all6 orders are TRAIN-SEEN for treatment. Its PASS would establish held-assignment
performance under covered orders,NOT unseen-order transfer. Fresh seeds do not erase prior inspection
of this authored task family. Coverage and the specified cycling policy are the tested intervention;
no unique internal causal mechanism,core superiority,general language,production or Gate F claim.
C257's negative result and C258's diagnostic-only verdict remain unchanged.

Six ignored artifacts plus summary.json:coverage-plan.json,dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json.
Model schema:fold-c259-order-coverage-models-v1;ten final states in seed/arm order.
Evaluation schema:fold-c259-order-coverage-eval-v1;final original/extra logits with identity,
fit/schedule counters and replay results. Strict reload:fingerprint preserved,exact argmax,
all-view raw-logit error<=1e-9. Postcheck reconstructs all metrics/gates/comparisons from saved logits,
with no additional model evaluation or learned-bundle load. Saved JSON equality and hashes mandatory.

Protection:400 source pins/659 protected inputs;direct dependency union35;OWN6.
Own24;modules144;loaded3382/focused3381. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb.
Registration:docs/experiment-ledger-addendum-c259-preregistration.md.
Design:docs/v5b-order-coverage-training-v0.1.md.
C258 acceptance and C259 preregistration are separate commits.

## C259 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 9ff995ce678b0ff74216c53a1f2f0f76801134a3
Scope:committed-byte C259 authoring validation,not formal scientific execution.

All six committed OWN files were re-fetched and read. Complete locally tested bytes were independently
Git-blob hashed and matched to remotely returned identities before the final exact test run:
-benchmark:aba15a677a0ea25813ec8406d26d028d6a1bb284;24180 bytes.
-tests:6485a0f6d83c92e64e9eaf892a34dc24e89a6cd7;25031 bytes.
-runner:830ff6373a27618a13612f728936663443b82a88;5165 bytes.
-launcher:e01cee731b0efc1e9e780134887dbae0f0b1e21f;2639 bytes.
-preregistration:ca56868a114d4871d210189a7ddcaa115136e0a3;10221 bytes.
-design:fec66f39e18d670b328b653427164e4449444765;4566 bytes.

First exact own run:24/24 PASS in2.948s.
After all remote readback/blob matching:24/24 PASS in2.737s.
No post-first-run authoring correction was needed. UTF-8/NUL checks,Python compile/import,
recursive global-binding audit(zero unresolved names),fixed manifest hash and both dataset hashes PASS.
Exact own tests validate paired800-step schedules,9-step order coverage,unchanged underlying targets,
no HOLDOUT optimization,treatment/control gate separation,per-order/all-six gates,wrong identities,
nonfinite outputs,strict checkpoint replay,artifact corruption and persisted recomputation.
Three embedded Python blocks compile;CLI indices precheck1,regression none,postcheck1/2/3.
AST call-order tests check the actual run/precheck functions. Semantic own-test count is24.
Launcher operational and parser checks precede logging/publication;parent run path calls load_parent.
Source/data/workload/counts/thresholds and parent loader/writer contracts were reviewed against the
retrieved C258/C257/C256 sources and actual C231 factory/C252 readout interfaces.

Own tests explicitly use synthetic Tiny,Base,Orders,Audit and artificial-logit fixtures.
Test09 executes actual C259 train_one's800-step loop and strict replay on Tiny,NOT on actual C252.
Test07 tests real optimizer/gradient flow on Tiny with a reduced test-only3-step budget.
Test20 executes actual run/persisted-postcheck orchestration with substituted synthetic training
records;it is not ten-model production training. Parent loader tests use temporary synthetic artifacts.
Test21's3382 dummy IDs validate filtering only,NOT execution of3381 historical tests.
These tests are authoring evidence,not learned capability evidence or the complete parent import graph.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No complete historical checkout or
user-local accepted artifacts were available;GitHub DNS failed in the container. PowerShell absent:
Windows System.Management.Automation.Language.Parser.ParseFile was NOT executed here.
The standard command parses dispatcher;dispatcher parses selected launcher;launcher parses runner.
All parser checks remain mandatory on the user's environment.
The compared changes since C258 execution comprise its published logs,C258 acceptance and six new
C259 files only. No accepted source/test/script was modified. Only this activation handoff follows.

Pending authoritative checks:Windows parser chain,actual400/659 source/artifact precheck,
exact own24 in user runtime,full3381 regression,actual10-model paired training,real checkpoint replay,
persisted postcheck and log publication. None is claimed complete by this authoring review.
Use the FINAL activation branch HEAD,not review_target_HEAD,parent execution or log-publication HEAD.
Re-read the final ref before issuing ExpectedHead.

## Execution and stop

Use tools/invoke_active.ps1. Formal state contains exactly one ACTIVE token resolving to C259.
Launcher fixes runs/c258-v5b-middle-slot-93386fd77e3749bab4122685ff57720d/summary.json as parent.
Order:dispatcher/launcher/runner ParseFile -> Python compile+parent/task precheck -> own24 ->
focused3381 -> ten-model paired training -> strict checkpoint replay -> persisted postcheck -> log publication.
Progress:model1/10..10/10;step200/400/600/800 for each. Completed valid FAIL is a scientific negative,
not INVALID;do not retrain or change criteria to rescue it.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE:operational SKIPPED before logging;
no scientific execution or log publication. Source/artifact/schema/nonfinite/identity/count/replay/test
faults stop and retry SAME C259 only after minimal repair. No C260 registration before judgment.
Log-only publication failure:repair transport without repeating completed training.
The user normally sends only 'finished';fetch docs/experiment-run-logs/c259/latest.json/latest.log.
Do not advance this branch with unrelated documentation during the user's run/log publication.

Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite or CI changes. Preserve all accepted evidence and recovery history.
Judge C259 before C260.
