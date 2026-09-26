# C264 preregistration — frozen two-fact deletion

Experiment:C264-v5b-frozen-two-fact-deletion. Stage:V5-B-FROZEN-TWO-FACT-DELETION.
C263 ACCEPTED PASS within its bounded capability scope; no learning-rate benefit established.
C262 and all earlier negatives remain. Gate E PASSED;Gate F NOT PASSED. C265 NOT REGISTERED.

## One question

Do all twenty frozen C263 final states keep answering correctly when one unqueried fact is deleted?
This tests transfer from three visible facts to two,using the same known names and values.
It is not more training,another seed search,an optimizer intervention or architecture adoption.
Example:a=0;b=1;c=2;b= -> a=0;b=1;b=;both targets are1. Never delete the queried fact.

## Accepted parent and actual interfaces

Acceptance/base:5f6bd9ca1c3c318451f30b4d4c9858285b3d272b.
Acceptance:docs/experiment-ledger-addendum-c263-c264.md.
Execution:abca8d7eb25146fca6f7404790071d1e6f0999d0.
Published log:1b47b5e3dc8ee3c6c2edd6972e7521b16e4f1b67.
Publisher log SHA256:d089e8f808170a58bfb292547387642a4d0d6312ec61764564462ba26cc2441b.
Summary SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
Summary:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.

Required parent artifact SHA256:
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;
-evaluations.pt:1681c71811844655081ca5597b6dfbe1ab80fbdc5b5046b1f947b1bf51aefd89;
-measurements.json:9b8bab48074a91e1dd5f3c5d389598739b651bcadeed6ec49fbf7ec0c92631ee;
-rate-plan.json:ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305;
-trained-models.pt:a63519b761bc876b8088fe14432018cd01024bfdecbcf1fca38a0515021dede9;
-validation-summary.json:e42f668ec6c2a01f573be92bbcd938f1d991e48cf02d242315d02d740d29066f.

check_parent calls actual C263.validate_result and requires its execution identity,PASS,all four
arm counts5 and both rate_joint_pass values true. precheck verifies all parent hashes/sizes plus
inherited source/input protection before own tests. Before model evaluation,load_reference calls
actual C263.verify_artifacts(parent_dir,PARENT_EXECUTION),then loads the saved evaluation archive.
That verifier reconstructs parent metrics/contrasts/schedules without model inference. Guard module
calls during parent verification. It returns20 measurement records. The separate archive read obtains
fold-c263-rate-eval-v1 records with final_sha256 and raw.original/raw.extra;they are final800-update
outputs,not initial or selected intermediate states. Original logits144x256 and extra288x256 per
TRAIN/HOLDOUT/view are paired with dataset.json in its exact saved row order.
There are two reference archive loads per load_reference pass:parent verification and record read.
The formal evaluation and persisted postcheck invoke it once each,four reference loads total.

C263.load_bundle strictly validates fold-c263-rate-models-v1,twenty states in seed/arm order.
Construct the actual C252 Full aligned reader via C256.make_model/C231 factory,then strict-load the
corresponding final state. Seeds263001..263005,all four arms standard_forward,standard_reverse,
lower_forward,lower_reverse;all14256 parameters. Verify final fingerprint and freeze eval/gradients.
Keep every model;no filtering by either rate. New wrappers receive saved states before any inference.
One learned-bundle load,twenty strict state loads,no new learned checkpoint or optimizer.

## Dataset and deletion provenance

Use all three known entity subsets:a,b; a,c; b,c (and corresponding Japanese identifiers).
Each subset receives all12 ordered distinct value pairs from0..3,both fact orders,both languages
and both queried entities. Exactly288 unique normal prompts. Same syntax,values,query-at-end and
48-slot BOS/bytes/EOS/PAD encoding;only two facts are visible. No deleted value,source label,target,
entity index or permutation metadata enters the model. Do not sort prompts before inference.
Dataset SHA256:8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1.

Delete each of the two unqueried facts from all864 original C263 normal rows (both saved stages
and both original assignment splits). This produces1728 provenance edges. Each reduced prompt has
six parents:two possible deleted values and three possible insertion positions of the removed fact.
Score each reduced prompt ONCE. Store sorted source stage/split/row-ID and deleted entity for all
six parents. Reconstruct provenance during saved postcheck and require unchanged target semantics.
Never treat those six presentations as independent new questions. Projection can cross the old
TRAIN/HOLDOUT split,so reduced prompts have NO such split label. The old splits remain replay anchors.
The new prompts were not in C263 training,but their retained pairwise associations were present;
this is fact-count/deletion transfer,not new-value or new-name learning.

## Fixed scoring gate

Per state report12 cells:two languages x three entity subsets x two visible orders.
Each cell has24 answers and12 groups containing both queries for the same assignment/order.
Require accuracy>=.90 (22/24),both-query correctness>=.80 (10/12),evidence-mask accuracy drop>=.35
and query-mask accuracy drop>=.35. Both values are distinct;query-blind guessing one displayed
value scores1/2,so the query-drop threshold remains compatible with perfect normal accuracy.
No pooling across subsets or languages to rescue a weak cell.

Also report six language/subset two-order-consistency cells. Each has24 assignment/query groups,
requiring both presentations correct for a group to count. Require>=.80,at least20/24 groups.
C264 primary PASS requires every cell for all20 states to pass. Report all four arm counts separately.
This is a new frozen-transfer gate,not retrospective amendment of C263's lower-rate capability gate.
A valid criterion miss is ACCEPTED VALID NEGATIVE,not an execution failure or grounds to retrain.

## Sequence,workload and persistence

For each frozen state:
1. Actual C259.evaluate on all C263 original/extra splits/views:12 forwards,2592 rows.
2. Before new inputs,match accepted final raw logits within1e-9 and exact argmax;verify unchanged state.
3. Two-fact dataset:two144-row batches per view,three views;6 forwards,864 rows.
4. Original evaluation again:12 forwards,2592 rows;match both same-run anchor and accepted outputs.
5. Verify unchanged full state and exact wrapper/core counters;remove hooks even after exceptions.

Per state30 model forwards/6048 row presentations/120 Full core calls. Total600 forwards/120960 rows/
2400 core calls. Twenty states,training0,new learned checkpoints0,bundle loads1,strict loads20.
CPU float64,threads2,deterministic algorithms;nonfinite output is an integrity fault.
Final saved logits total247726080 raw payload bytes (about248 MB decimal),plus metadata and JSON.
This is not a storage or performance optimization. Historical tests,parent metric reconstruction,
file hashing and provenance reconstruction are additional work,not extra scientific samples.

Six ignored artifacts plus summary.json:deletion-plan.json,two-fact-dataset.json,provenance.json,
eval-outputs.pt,measurements.json,validation-summary.json. Eval schema fold-c264-deletion-eval-v1
stores20 records with final fingerprints,anchor/reduced/restored tensors,counters and replay errors.
Saved postcheck rebuilds parent references,all replay checks,provenance,scores and gates from files.
No model construction,model forward or learned-bundle load is permitted in saved postcheck;module
calls are blocked. All persisted JSON and artifact hashes/sizes must match. Only console logs publish.

## Protection and review

Inherit424 source pins/710 inputs. Add OWN6 and parent summary+SIX artifacts:430 pins/723 inputs.
Direct deciding dependency union40=five C231 LM sources,C230..C263 helpers,andC264. Lazy imports count.
OWN6:benchmark,own tests,runner,launcher,this preregistration,and design:
-fold_lm/v05_benchmarks/model_c264_two_fact_deletion.py;
-tests_lm/test_v05_c264_two_fact_deletion.py;
-tools/run_c264.ps1;
-tools/invoke_c264.ps1;
-docs/experiment-ledger-addendum-c264-preregistration.md;
-docs/v5b-two-fact-deletion-v0.1.md.
Own24;modules149;loaded3502/focused3501. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1.

Before activation re-fetch all committed files;match executable blob identities to complete tested
files,run exact own24,compile/import,global binding/fixed hash/count/CLI/parent-interface checks.
Own tests explicitly use a string-parser oracle with placeholder parameters and Identity core,not
a trained FOLD model. They exercise actual new run/probe/scoring/provenance/persistence and synthetic
parent dispatch. The3502-ID test fixture checks filtering only,not3501 historical tests. Record all
limitations in the handoff. Full parent graph/artifacts,Windows ParseFile and real frozen-state
execution remain mandatory on the user runtime. Never issue a launcher before review PASS.

## Interpretation and stop

Deletion changes visible fact count,effective sequence length and positions together;do not claim
a uniquely localized internal cause or arbitrary-length reasoning. Names/values are familiar and
the authored family has been repeatedly inspected;no independent-general-benchmark claim.
No learning-rate advantage,default optimizer change,architecture adoption,production or Gate F.
C263 PASS and earlier negatives are unchanged regardless of C264. No result-driven tuning or training.
Integrity faults retry SAME C264;operational skips precede logging;log-only faults are repaired
without repeating completed evaluation. No paid API,external corpus,model expansion,cleanup,
history rewrite or CI changes. Judge C264 before C265.
