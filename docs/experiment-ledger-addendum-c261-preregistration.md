# C261 preregistration — frozen repeated-value transfer

Experiment:C261-v5b-frozen-repeated-value-transfer.
Stage:V5-B-FROZEN-REPEATED-VALUE-TRANSFER.
C260 ACCEPTED VALID NEGATIVE;C259/C257 negatives,C258 diagnostic PASS,C256 bounded PASS remain.
Gate E PASSED;Gate F NOT PASSED. C262 NOT REGISTERED.

## One question

Do all ten frozen final C260 states answer repeated-value assignments correctly without further
training? This tests the previous task's distinct-value restriction rather than selecting a winning
architecture or adding seeds until a previous gate passes. Preserve BOTH arms and ALL five seeds.
The joint criterion is explicitly new:both arms must each pass5/5 on this NEW task. Report each arm's
pass count independently. No existing C260 capability gate is changed or rescued.

## Accepted parent and exact interfaces

Acceptance/base commit:a2061c1cf321771241e262def1474cb8f59dcd79.
Acceptance:docs/experiment-ledger-addendum-c260-c261.md.
C260 execution:5788a63a692983094a9c6311c58d1440005b7fca.
Published log:e841aa5c312d46bfe11172af45262433cf5ec33d.
Publisher log SHA256:604163ff5f8ad3628e8b3facd49f7e97cafde04822123838b344efc893d2fd15.
Summary SHA256:df6780749afa707fa0c6809e76710f39cdbeac6c1b69665a064248808b1f9ab6.
Summary:runs/c260-v5b-core-free-697d8bdc3ca3411ba81f703b2f16fb96/summary.json.

Required artifact SHA256:
-core-plan.json:ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56.
-evaluations.pt:b109243f5b5d24ffe343586a50b97990524c7b572ec238b5e267863dbd542276.
-measurements.json:5839838218761bd608b5b79137a300649b3a5df11eb909474520a45608f3a8fa.
-trained-models.pt:727ffd1320266a239d21ce172279dc2cec3be6383db74cd4a1b09addbe36976c.
-validation-summary.json:250d099db6ec58b21db06d858e9c0e0ddf8349f66b0d1936001e3874875e26a2.

check_parent requires actual C260.validate_result,execution identity,status FAIL and pass counts
with_core4/without_core3. The negative status is scientific evidence,not an integrity failure.
load_reference calls actual C260.verify_artifacts(parent_dir,PARENT_EXECUTION),then reads the actual
fold-c260-core-eval-v1 records and uses C260.analyze to match accepted measurements/summary again.
The records contain final_sha256 and raw.original/raw.extra per TRAIN/HOLDOUT and all3 views;these
are final800-update logits,not predictions guessed from summary averages. Parent raw shapes are
144x256 for original and288x256 for extra. dataset.json has original/extra keys. Use those rows in
that exact order. Reference evaluation archive loads:two per load_reference pass,one within parent
verification and one to obtain records. The run and saved postcheck use two passes,four such loads.

Strictly load actual C260.load_bundle (fold-c260-core-models-v1) once. C260.make_pair supplies matching
actual Full and CoreFreeReadout architectures. Seeds260001..260005,with_core/without_core order;
parameters14256/10928. Verify each loaded final fingerprint,then eval/requires_grad=False.
Constructing fresh wrappers before strict loading is not fresh training or checkpoint selection.
No accepted source,test,weight,optimizer or default production architecture is modified.

## New data and fixed factors

All64 ordered assignments from values0..3 contain24 distinct assignments and40 nondistinct ones.
Use all40 new assignments:36 with exactly one equal pair and4 with all3 equal.
For each use both identifier spellings EN:a,b,c and JA:甲,乙,丙,all6 fact orders,all3 queried entities.
Exactly1440 new rows:1296 pair_equal and144 all_equal. No new assignment occurred in C260 TRAIN or
HOLDOUT. Existing names,values,delimiter syntax,query-at-end,48-slot BOS/bytes/EOS/PAD encoding and
final model states stay fixed. The model receives only visible bytes and zero task IDs.
The six permutations are lexical itertools.permutations order;do not sort prompts back before scoring.
New dataset SHA256:1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339.

Example:a=0;b=0;c=2;c= has target2,while a=0;b=0;c=2;a= has target0.
The offline singleton flag identifies the one entity whose value occurs once;it never enters the
model. Repeated values cannot be reverse-mapped to a unique entity;do not reuse C258's attribution
logic. New rows are not mislabeled TRAIN/HOLDOUT:those labels apply only to original anchor data.
Score normal,evidence_blind(all fact digits replaced with ?),query_blind(queried name replaced with ?).

## Measurement sequence and integrity

For each frozen model:
1. Actual C259.evaluate on C260 original+extra data,all splits/views:12 forwards/2592 rows.
2. Before any new prompt,compare every raw logit to its saved C260 reference within1e-9 and require
   identical argmax. Old capability misses are allowed if faithfully reproduced;do not require a
   previously failed model to become correct to pass this replay barrier.
3. Score new data in fixed144-row chunks:10 chunks/view x3 views=30 forwards/4320 rows.
4. Repeat original evaluation:12 forwards/2592 rows. Require raw-logit/argmax agreement with both
   the same-run anchor and accepted C260 reference,plus unchanged complete weight fingerprint.

Per model54 forwards/9504 rows. Total540 forwards/95040 row presentations.
Full core calls216/model x5=1080;core-free core calls0. Separate wrapper/core hooks enforce counts.
CPU float64,threads2,deterministic algorithms,finite outputs only. No optimizer or gradient updates.
New training0,new learned checkpoints0,accepted model bundle loads1,strict state loads10.

## New-task metrics and fixed gate

Report24 separate cells/model:2 languages x2 strata x6 orders. Also four stratum/language six-order
consistency scores. Never pool the easy all_equal rows into pair_equal capability.

pair_equal,per language/order:
108 answers across36 assignments.36 singleton-target questions and72 repeated-target questions.
Require total accuracy>=.90,singleton accuracy>=.90,repeated-target accuracy>=.90,
all-three-query correctness>=.80,and normal-minus-evidence-blind accuracy>=.35.
Integer minima:98/108 total,33/36 singleton,65/72 repeated,and29/36 complete query triplets.
Six-order consistency groups identical assignment/query across all orders:108 groups/language,
require>=.80,at least87/108 completely correct groups.

all_equal,per language/order:
12 answers from4 assignments. Require accuracy>=.90 (11/12) and evidence_drop>=.35.
Query-triplet correctness is reported but not a gate. Singleton accuracy is null,not zero or PASS.
Six-order consistency:12 groups/language,require>=.80 (10/12).

Query-blind accuracy/drop are DESCRIPTIVE ONLY in BOTH strata. A query-blind model selecting the
repeated value can score2/3 in pair_equal,so even perfect normal behavior can have only1/3 drop.
In all_equal the query is redundant and a correct query-blind model scores1,with zero drop.
Applying the old.35 query-drop gate would reject correct behavior for mathematical reasons.
Instead,pair_equal singleton/repeated scores and complete-query triplets test query-specific binding.
The all_equal stratum is only an evidence-reading check,not evidence of query understanding.
This explicit new metric contract does not relax or amend any C260 criterion.

Per-state PASS requires every new cell and six-order group score to satisfy these thresholds.
C261 overall PASS iff all ten states pass,i.e.each arm5/5. Report both arm counts without using one
to rescue the other. C260 anchor performance is preserved but is not a new-task capability gate.
A complete valid miss is ACCEPTED VALID NEGATIVE. No tuning,seed filtering or additional training.

## Persistence and costs

Five ignored artifacts plus summary.json:repeat-plan.json,repeat-dataset.json,eval-outputs.pt,
measurements.json,validation-summary.json. Eval schema fold-c261-repeat-eval-v1 stores ten records
with final fingerprints,counts,anchor/new/restored tensors and replay errors. It contains no new
learned weights. Raw logit payload totals194641920 bytes (about195 MB decimal),plus metadata/files;
no claim of reduced disk use. Parent-file hashing,recomputed parent metrics and regression fixtures
are additional computational work,not new scientific samples or included in wrapper-forward counts.
Saved postcheck reloads reference/output archives,verifies hashes and reconstructs all replay tests,
new scores and gates without any new model forward,model construction or learned-bundle load.

## Protection and authoring

Inherit C260406 pins/672 inputs. Add parent summary+SIX parent artifacts and OWN6:
412 source pins/685 inputs. Direct deciding dependency union37 comprises five C231 LM source files,
C230..C260 helpers and C261. All actual lazy scientific imports remain pinned.
OWN6:benchmark,own tests,runner,launcher,this preregistration,and design:
-fold_lm/v05_benchmarks/model_c261_repeated_value_transfer.py
-tests_lm/test_v05_c261_repeated_value_transfer.py
-tools/run_c261.ps1
-tools/invoke_c261.ps1
-docs/experiment-ledger-addendum-c261-preregistration.md
-docs/v5b-repeated-value-transfer-v0.1.md

Own24;modules146;loaded3430/focused3429. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301.
Re-fetch all six committed files and match executable bytes to locally executed files before review
PASS. Execute exact own24,compile/import,global-name checks,hashes,count semantics,CLI/parser order,
parent schema/loader and source coverage audits. Tests use an explicitly synthetic byte-parser oracle,
not trained FOLD models. Test20 executes actual run/probe/analyze/persisted-postcheck with synthetic
parent adapters. Test21's dummy3430-ID suite checks filtering only,not3429 historical regressions.
Record actual checks and pending Windows/full-parent/full-regression checks in the handoff.

## Scope and stop

New assignments are unseen but belong to an authored symbolic task family already repeatedly
inspected. This is a specific distribution-shift probe,not a new independent general benchmark,
natural-language proficiency,core superiority,production readiness or Gate F passage.
Do not select architectures based only on these five pairs. C260 remains negative regardless of C261.
Integrity faults retry SAME C261;valid failure is accepted without retraining or threshold changes.
Operational skips precede logging;repair log-only publication without re-evaluation.
No paid API,external corpus,model expansion,accepted-file cleanup,history rewrite or CI changes.
Judge C261 before C262.
