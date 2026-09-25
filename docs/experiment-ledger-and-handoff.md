# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C257 ACCEPTED VALID NEGATIVE. C258 ACTIVE / NOT YET JUDGED. C259 NOT REGISTERED.**
C258 is the unique ACTIVE experiment:V5-B exploratory saved middle-slot attribution.
C256 remains ACCEPTED PASS within its original three-entity value-assignment scope.
C257 completed validly but only2/5 candidate seeds passed its all-five-seed unseen-order gate.
C258 is diagnostic integrity only; no new capability, causal mechanism, production or Gate F claim.
All earlier accepted verdicts and invalid-attempt recovery records remain preserved.

## Latest accepted evidence — C257

Scientific execution HEAD:016785f35605a3eef5f94d42f0b86cb2fc4d9dfe.
Published log commit:4a322950685b80d7748aa525608555149c2c2ffd.
Publisher log SHA256:6932e3f178cfadb3434a34368a3ba674489b96b6dc509b2a69da18f6a36a66a5.
Log bytes:680841.
Summary SHA256:596df75ccc89c5a12c964c2e6be1fc689e5773f4c0a857f90fdcedd4df9b8816.
Local summary:runs/c257-v5b-unseen-order-705d486739b44a56bbed34fae66ace89/summary.json.
Acceptance record:docs/experiment-ledger-addendum-c257-c258.md.
Acceptance/base commit:ff34341a10e12b00091649e29c05b088e29a09db.

Own24 PASS in4.897s;focused3337 PASS in224.138s.
388 source pins/635 protected inputs verified. Ten frozen C256 final models completed180 model
forwards/34560 row presentations. Training0;accepted checkpoint bundle loads1;strict state loads10;
new learned checkpoint writes0. Original metric/prediction replay, anchor restoration, saved
logit/metric recomputation and weight/protected-input preservation passed.
Tracked tree clean;scientific HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;candidate_gate=False;all_replays=True;all_weights_preserved=True.

Acceptance uses immutable published log ranges, publication metadata and recorded local postchecks.
The reviewer did not independently run the learned models or rehash the entire680841-byte log.
The log publisher reports its SHA256; do not present that as an independent complete-byte rehash.

Candidate metrics on novel orders of the original HOLDOUT assignment partition:

| Seed | New EN /144 | New JA /144 | Six-order EN /36 | Six-order JA /36 | Whole-seed result |
|---:|---:|---:|---:|---:|---|
|256001|144|144|36|36|PASS|
|256002|117|120|23|23|NEW_ORDER_MISS|
|256003|82|100|2|13|NEW_ORDER_MISS|
|256004|143|144|35|36|PASS|
|256005|102|91|19|12|NEW_ORDER_MISS|

Candidate pooled novel-order HOLDOUT1187/1440=82.4306%;joint seed passes2/5,not5/5.
This pooled accuracy does not replace the preregistered per-order/per-language/per-split gate.
Seed256002 EN bac answers33/36 but query triplets9/12, below0.80.
The three failing seeds also miss some novel-order TRAIN-assignment cells.
EOS outcomes are ORIGINAL_CRITERIA_MISS5, inherited from their C256 performance; do not present
that as five newly independent failures attributable only to C257's input-order change.
No threshold, seed, comparator, data or replay tolerance was changed to rescue the result.

Accepted C257 artifacts:
-eval-outputs.pt:6911df9af7a10790cee9b18ff15a6b3479ca7e20046d5f6a16f95d69d068b92a;70832057 bytes.
-measurements.json:c37f98bbc13526f408b9b00adac16e90e23dc764d59ef4af1ef5e990b235eb22;61378 bytes.
-order-dataset.json:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052;92184 bytes.
-order-plan.json:18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36;2248 bytes.
-validation-summary.json:1d0d66a7550d47e34d01b5242c8ad0ef527ed7c36df66a440e31005609975d99;1268 bytes.

Interpretation:value-assignment transfer on the original two orders does not guarantee all-order
transfer. Two accepted trained states do transfer, while three do not meet this fixed gate.
No unique internal cause or universal architectural impossibility follows. This authored,
repeatedly inspected, correlated task family is not a general-language/external benchmark.

## Preserved earlier evidence and recovery

C256 ACCEPTED PASS:aligned candidate5/5,TRAIN720/720,HOLDOUT718/720;EOS0/5,HOLDOUT248/720.
Execution:db9f3cb90d9268066c34fc91300193058301f06c;log:5695706c6306156fa079ce092581270ca781af71.
Summary SHA256:56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184.
Summary:runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.
Acceptance:docs/experiment-ledger-addendum-c256-c257.md;base:ee4c282687c71bed407ecb687659edd7103c740d.
C256's first precheck attempt remains INVALID in docs/experiment-ledger-addendum-c256-execution-recovery.md.
Failed execution1029158a60d40df24f599fb719411dbde2ffec06;invalid log2dc541041c772d5b9a449bd247862ad906a9b5c8.
Its manifest fingerprint and a whitespace-sensitive test were repaired without changing science.

C257's pre-activation test17 correction1487f6033e151f767b3ed3ebd29aabbe9648c94b was an authoring
repair,not an invalid scientific run. Prior review record is preserved in this handoff at
016785f35605a3eef5f94d42f0b86cb2fc4d9dfe. No formal C257 integrity failure occurred in this run.

C255 diagnostic PASS:self HOLDOUT145/160,value residual swap140/160.
Execution6b577da1edc7339dbfd68b3127870074de218e48;log48856dd7dabb84f1f8a71158d03a5ee9db2fd255.
Acceptance:docs/experiment-ledger-addendum-c255-c256.md;earlier invalid attempts remain in its
execution-recovery addendum. C254 diagnostic:self145/160,order141/160,query96/160.
C253 diagnostic:self145/160,pre-residual107/160,reader-only117/160.
C252 ACCEPTED VALID NEGATIVE:aligned reader4/5,not5/5. C2512/5;C250 Full reader2/5,GRU reader4/5.
C249 frozen diagnostic. C248 bounded transfer but failed its all-seed gate.
C247/C246/C244/C242/C241/C239 remain accepted negatives;C245/C243/C240/C237/C235 diagnostics;
C238 seen-prompt fit only. C232 bounded byte learning and C233 competitive GRU-only result do
not establish ordinary language, general reasoning or FOLD-core superiority.
Preserve all accepted source/tests/logs and tools/run_c167.ps1.

## Active C258 — saved middle-slot attribution

Experiment:C258-v5b-saved-middle-slot-audit.
Stage:V5-B-SAVED-MIDDLE-SLOT-AUDIT.
Question:do saved novel-order errors concentrate on query b/乙 and choose the middle-position
distractor? This diagnostic was designed after seeing C257 aggregate outcomes, but before
query-level attribution. It is exploratory,not independent confirmation or a causal intervention.

Changed:only offline answer grouping/attribution.
Held constant:all ten saved C257 final-model evaluations,all five seeds,both arms,both languages,
both original assignment partitions,known/novel permutations,queries,targets and all input bytes.
No training,new model evaluation,model construction,learned state loading or output correction.
All successful and unsuccessful seeds and controls are retained.

Known orders012/210;novel021/102/120/201. b/乙 was always middle in C256 and is never middle in
the new orders. The task's three distinct assigned digits let the scorer attribute a wrong answer
to the middle distractor,other displayed distractor,absent0..3 value,or an unrelated byte.
Correct middle-position answers are NOT classified as shortcut errors.

Normal answers8640=known2880+novel5760. Masked/restored views are replayed for parent validation,
not counted again as independent answers. Order/query cells720,each12 assignments.
Pooled query cells120,each24 known+48 novel answers. Signature cells40,one perseed/arm/split/language.
Report known-both-correct to novel-wrong transitions matched on assignment/language/query.
For b report known/novel accuracy,error-rate difference versus pooled a/c,middle and other
incorrect displayed-entity counts,absent-value/other-byte counts,and middle-error shares with
both all-error and in-assignment-error denominators. Zero denominator is JSON null.
Do not cherry-pick cells or turn a descriptive contrast into causal proof.

The loader requires the actual C257 status FAIL/candidate2/control0 and verifies parent artifact
hashes/sizes. It calls actual C257.load_inputs for C256 data/records,then loads only C257's saved
evaluation archive,schema fold-c257-order-eval-v1. Actual C257.analyze replays all original,
novel and restored views and must reproduce accepted measurements/summary and plan.
No nonexistent saved C256 raw logits are assumed. The original saved C257 anchor is used.
The scorer uses normal-view argmax bytes; no target or entity index is passed to any model.

Workload:model forwards0,training0,learned bundles/state loads0,new learned checkpoints0.
Module._call_impl is blocked during saved replay/analysis. One evaluation-archive load per pass;
formal diagnostic and persisted postcheck total two passes. Source/artifact hashing,all-view
metric recomputation,serialization and historical test work are separate cost,not new samples.

Fixed gate:diagnostic integrity only. Parent replay,complete attribution/counts,source preservation,
no-model-call guard and exact persisted re-attribution must pass. Any direction or absence of
middle-slot bias is reportable. capability_pass_claim=False;causal_mechanism_claim=False;
production_adoption=False;gate_f_candidate=False. A diagnostic PASS does not reverse C257.

Protection394 source pins/647 inputs;direct dependency union34;OWN6.
Own20;modules143;loaded3358/focused3357. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:a4f2cad192bd56dd73d867caf8453084cdd85e8e0f10f9d2496bfaa4a6c08aef.
Registration:docs/experiment-ledger-addendum-c258-preregistration.md.
Design:docs/v5b-saved-middle-slot-audit-v0.1.md.

Five ignored output artifacts plus summary.json:audit-plan.json,row-attribution.json,
query-position-cells.json,signature-summary.json,validation-summary.json.
Only console text and publication metadata are mirrored to Git.

## C258 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 740ddb19ad948a9ca8816204b5dbd6abc924676f
Scope:committed-byte authoring review,not formal C258 execution or learned-output evidence.

All six committed OWN files were re-fetched and read. Complete locally tested file bytes were
independently Git-blob hashed and matched to returned remote identities:
-benchmark:aae238ee0fbb4afe8c7f93dbf3448eee9397ae51.
-tests:5c4ca2a555b87db6f6a2e29b453b9e60340c19e9.
-runner:1f2caf97fbae93bc100ba372fc2d4b824ed87935.
-launcher:624635fec3ef1506a717fd55394fb5e63fd6eafb.
-preregistration:4c22446d53818e662b60f4bdf155d0807b63796b.
-design:4aae7068227bac73e3d1b4d32c42633ef280ed96.

Executed before publication:20/20 own tests PASS in0.699s.
After complete remote readback and six blob matches:20/20 PASS in0.696s.
Python compile/import,UTF-8/NUL checks,recursive global-binding audit (zero unresolved names),
manifest/original/novel dataset hashes,semantic own-test identity count and inherited-count
arithmetic passed. Three embedded Python blocks compile;CLI indices are precheck1..2,regression
none,postcheck1..4. Launcher parser and operational guards precede execution/log publication.
Exact run/loader/attribution call ordering,wrong-HEAD rejection,artifact corruption,zero denominators,
no-model-call enforcement,all query/position counts,and persisted recomputation were exercised.
No authoring correction was needed after the first complete own-test run.

Tests use synthetic saved logits and explicit parent/audit adapters. Test17 executes actual C258
run and persisted postcheck with those adapters;tests14/15 exercise its actual archive loader and
parent-interface dispatch. They do NOT execute the full historical import graph or validate the
user-local learned artifact bytes. Test18's constructed3358 IDs check filtering only,not3357 tests.
Actual C257 writer/loader/analyze interfaces and output semantics were inspected from protected
source;complete parent-source/artifact precheck remains required on the user's machine.

Reviewer:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. GitHub DNS failed in the container;no complete
historical checkout or user-local learned outputs were available. PowerShell is absent,so Windows
System.Management.Automation.Language.Parser.ParseFile was NOT executed here. The standard
command parses dispatcher;dispatcher parses selected launcher;launcher parses runner before use.
The final code comparison contains only the C257 published logs,C257 acceptance,and six new C258
files;no accepted source/test was modified. Only this activation handoff follows the review.

Pending authoritative checks:Windows parser chain,real394/647 source/artifact precheck,own20 in
user runtime,complete3357 regression,saved real-output attribution,persisted postcheck and log
publication. None is claimed complete by authoring review. Use the FINAL activation branch HEAD,
not review_target_HEAD or either parent's scientific/log HEAD. Read final branch HEAD before
issuing ExpectedHead.

## Execution and stop

Use tools/invoke_active.ps1. Formal state contains exactly one ACTIVE token resolving to C258.
The launcher fixes the accepted C257 and C256 summary paths above.
Order:dispatcher/launcher/runner ParseFile -> Python compile+parent precheck -> own20 ->
focused3357 -> saved-output replay/attribution -> persisted postcheck -> log publication.

Wrong branch,dirty tracked tree,stale ExpectedHead or stale ACTIVE are operational SKIPPED
before experiment logging;they publish no scientific execution log and are not scientific INVALID.
Source/artifact/schema/nonfinite/identity/count/replay/test faults stop and retry C258 only after
minimal repair. No result-driven data,seed,threshold or hypothesis-selection changes.
A log-only publication fault is repaired without redoing completed diagnostic work.
The user normally sends only 'finished';fetch docs/experiment-run-logs/c258/latest.json/latest.log.
Do not move this branch with unrelated documentation while the formal run/log push is active.

Gate F NOT PASSED. No paid API,external corpus,model expansion,production adoption,cleanup,
history rewrite or CI changes. This saved diagnostic ends after one full decomposition;any
order-coverage training intervention needs a separate controlled preregistration after judgment.
Judge C258 before C259.
