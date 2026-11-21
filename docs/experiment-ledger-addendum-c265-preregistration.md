# C265 preregistration — frozen compound identifiers

Experiment:C265-v5b-frozen-compound-identifiers. Stage:V5-B-FROZEN-COMPOUND-IDENTIFIERS.
C264 ACCEPTED PASS for bounded two-fact transfer. Earlier verdicts/recoveries remain unchanged.
Gate E PASSED;Gate F NOT PASSED. C266 NOT REGISTERED.
Acceptance/base:d0af4709b7362f145ca55c2bfee5038b107e2961.
Acceptance:docs/experiment-ledger-addendum-c264-c265.md.

## One question

Can all twenty frozen states bind compound identifiers made from familiar characters,including
names sharing their first or last character? Three profiles are fixed before evaluation,not selected
after seeing answers. No training,seed selection,new vocabulary bytes or architecture change.

For each C264 entity subset,let u,v be its two names in ascending original entity-index order.
Use exactly these bijective maps from the two original entities to visible names:
-doubled: u->uu,v->vv;
-shared_prefix: u->uu,v->uv;
-shared_suffix: u->uu,v->vu.
For a/b this gives aa/bb,aa/ab,aa/ba. For 甲/乙 it gives 甲甲/乙乙,甲甲/甲乙,甲甲/乙甲.
Replace both fact names and the queried name consistently. aa=0;ab=1;ab= has target1.
The doubled profile has equal length to both collision profiles and distinct first/last characters.
It is a reference condition,not proof that character composition or position confounds are absent.

## Fixed inputs and paired scoring

Keep all C264 two-fact rows,all three source subsets,both visible orders,both languages,all12 distinct
value pairs and both queried entities.288 rows per profile,864 unique new normal prompts per model.
All three profiles preserve the same row order,source_id,target and grouping as C264.
The model receives only renamed visible bytes and zero task IDs. Never translate compound names
back to single-character names before inference. Original entity indices are OFFLINE scoring keys.
Original rows go to the existing C264 scorer solely to supply unchanged targets and group identities.
No target,rename map or source metadata is passed through a second model channel.

Store every profile's normal,evidence_blind and query_blind prompt strings. Evidence-blind replaces
both values with ?;query-blind replaces the whole queried identifier with ?. Normal ASCII prompts
are13 bytes and Japanese prompts25 bytes;all fit the existing46-byte payload/48-slot BOS-EOS-PAD
contract. The three profile lengths match for every paired normal row. All new normal bytes were
already present in the familiar names,values and delimiters. No new random byte embedding is needed.
Each profile is evaluated separately;no new TRAIN/HOLDOUT split is assigned to these frozen probes.
Dataset SHA256:4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb.

## Parent evidence and checkpoint sources

C264 execution:6da6c182f328cccddbdfbd94e232141b0c68c0ea.
Published log:5e62210d4b2a5b5d0cf7dbbc0fe6cf7be05d47e1.
Publisher log SHA256:f228c6ede8e95546c6e534a4afcde97255e69fe38d0692b2293e71f35c2ad445.
C264 summary SHA256:1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503.
C264 summary:runs/c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935/summary.json.
C263 model-source summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
C263 summary SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
The model-source summary is already inherited/protected;reject a source path not in that mapping.

C264 artifact SHA256:
-deletion-plan.json:a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1;
-eval-outputs.pt:3123aa3b0c2e74b1a069edeb56da5a52046fc5731f681656abf51d4200db55b3;
-measurements.json:34c43a5eea6aa235a7bcf8451f3742393a53255a63299c43874c5bf948b87f99;
-provenance.json:35f96556b849adeac41cc04cc77d91c94ba4e560783d0f58c67e3898ea479577;
-two-fact-dataset.json:8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1;
-validation-summary.json:171731535a0f725e5cfb5912828e8c082c5950507a9dade64cf43463fe304a14.

check_parent calls C264.validate_result and checks execution,PASS,all four arm counts5 and all six
artifact identities. precheck checks actual bytes/sizes,inherited source pins and protected inputs.
load_reference calls the actual THREE-argument interface:
C264.verify_artifacts(c264_directory,c263_summary,C264_EXECUTION).
That verifies saved C263/C264 evidence without new model inference. The explicit second C264 archive
read uses fold-c264-deletion-eval-v1 records. Extract seed,arm,final_sha256 and reduced outputs.
The reduced field is the actual frozen model's two-fact logits,not its three-fact anchor/restored
fields. Its three tensors each have288x256 CPU float64 values. Recompute actual C264.score for these
outputs and match all20 accepted measurement records before any new evaluation.

Model weights still come from C263,not C264 (C264 wrote no learned checkpoints). Load actual
C263.load_bundle(c263_directory/trained-models.pt) once. Construct C252 Full aligned readers through
the same C256.make_model/C231 factory,then strict-load all20 states in the accepted identity order.
Seeds263001..263005;arms standard_forward,standard_reverse,lower_forward,lower_reverse;14256 parameters.
Check final fingerprints against C264 references and freeze eval/requires_grad. No selected seed,
new initialization outcome,optimizer or mutable training state enters the experiment.

## Gate and scientific interpretation

Use actual unchanged C264.score per naming profile. Each profile has12 language/subset/order cells,
each24 answers and12 paired-query groups. Require accuracy>=.90(22/24),query-pair correctness>=.80
(10/12),evidence-mask drop>=.35 and query-mask drop>=.35. Also require each of six language/subset
two-order scores>=.80(20/24 groups). Distinct target values make the query-drop criterion applicable.
Each model passes iff ALL THREE profiles pass;C265 passes iff ALL20 models pass. Report each profile
by each original arm as well as whole-model counts. No profile,language or arm may rescue another.

A first-character-only parser must fail the shared-prefix condition;a last-character-only parser
must fail the shared-suffix condition. These are explicit authoring negative controls,NOT hypotheses
confirmed about the learned model. Failure of a learned state does not identify its internal parser.
Name length,composition and positions differ from the original inputs. The three new profiles match
lengths but not all character distributions. No causal localization or arbitrary-name generality.
A pass covers these finite maps only,not arbitrary strings,ordinary language or an independent
benchmark. All four rate/order cohorts remain;no learning-rate benefit or optimizer adoption claim.

## Sequence and resource contract

For each frozen model:
1.C264.evaluate_new on the288 original two-fact rows,three views:6 forwards/864 rows.
2.Replay raw logits within1e-9 and exact argmax against accepted C264 reduced tensors before new names.
3.Three naming profiles,two144-row chunks/view:18 forwards/2592 rows.
4.Original two-fact rows again:6 forwards/864 rows;match both same-run anchor and accepted reference.
5.Verify unchanged full fingerprint and hook counts:30 forwards/4320 rows/120 Full core calls.

Total600 forwards/86400 row presentations/2400 core calls.20 strict state loads;one C263 model-bundle
load;training0;new learned checkpoints0. CPU float64,threads2,deterministic algorithms. Replay of
previously incorrect answers is integrity evidence,not a demand for new perfection.
Reference loading invokes two C264 evaluation-archive loads and two C263 evaluation-archive loads
per pass. Evaluation and saved postcheck each call it once,four loads of each reference archive
in total. These are saved-output reads,not model inference or learned-bundle loads.
Historical tests,file hashing,parent metric reconstruction and serialization are additional work.

Five ignored artifacts plus summary.json:identifier-plan.json,identifier-dataset.json,eval-outputs.pt,
measurements.json,validation-summary.json. Eval schema fold-c265-identifiers-eval-v1 stores20 records
with anchor,three renamed profiles,restored outputs,identity/counts/replay results. Raw tensor payload
176947200 bytes(about177 MB decimal),plus metadata;do not confuse it with peak RAM or file size.
Saved postcheck blocks module calls and rebuilds references,dataset,replays,profile scores and gates.
No model construction,new inference or learned-bundle load is performed in this saved verification.

## Protection and review

Inherit430 source pins/723 inputs;add parent summary+SIX artifacts and OWN6:436 pins/736 inputs.
The C263 source path was already protected and must not be counted again. Direct deciding dependency
union41=five C231 LM sources,C230..C264 helpers and C265. All accepted source/tests remain immutable.
OWN6:benchmark,own tests,runner,launcher,this preregistration,and design:
-fold_lm/v05_benchmarks/model_c265_compound_identifiers.py;
-tests_lm/test_v05_c265_compound_identifiers.py;
-tools/run_c265.ps1;
-tools/invoke_c265.ps1;
-docs/experiment-ledger-addendum-c265-preregistration.md;
-docs/v5b-compound-identifiers-v0.1.md.
Own24;modules150;loaded3526/focused3525. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3.

Authoring tests use the actual C264 dataset/scorer/evaluator and an explicit parser Oracle with
placeholder weights and Identity core counters. They do not establish learned capability. They test
actual new run/probe/replay/load dispatch/persistence,known-byte and length controls,and deliberate
first/last-character shortcut failures. The full historical parent graph and user-local artifacts
remain authoritative-run checks. A dummy3526-ID suite tests exclusion only,not execution of3525 tests.
After all files are committed,re-fetch and match the tested file blobs;run exact own24 and compile/
import/global binding/manifest/data/count/CLI/source-order checks. Record real limits in the handoff.
No user launcher until post-authoring review PASS. Windows ParseFile remains mandatory.

## Stop

Integrity fault:INVALID / RETRY SAME C265;no C266. Valid capability miss:accept negative without
training,profile selection,threshold change or seed replacement. Operational skips precede logging.
Log-only publication failure is repaired without repeating completed evaluation. Gate F NOT PASSED.
No paid API,external corpus,model expansion,cleanup,history rewrite or CI change. Judge C265 before C266.
