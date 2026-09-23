# C241 preregistration — balanced-position assignment holdout

Experiment:C241-v5b-assignment-holdout-balanced-order.
Stage:V5-B-ASSIGNMENT-HOLDOUT-BALANCED-ORDER.
C240 ACCEPTED PASS for diagnostic integrity only; C239 remains ACCEPTED VALID NEGATIVE.
C238 remains minimal seen-TRAIN fitting PASS. Gate E PASSED; Gate F NOT PASSED.
C242 NOT REGISTERED. This document registers C241; authoritative handoff controls activation
after independent post-authoring review.

## One scientific question

After breaking C239's query-to-position correlation inside TRAIN by exposing both fact orders,
can the unchanged fresh model/training recipe transfer from assignment[0,1] to the held-out
swapped assignment[1,0]?

This is bounded assignment transfer on the existing two-entity/two-value fixture, not general
language, unseen vocabulary or a causal-mechanism proof.

## Accepted parent identities

Acceptance record:docs/experiment-ledger-addendum-c240-c241.md.
Acceptance record commit:dc75a8defc0d21d70d1c7ec06914914468e0bd77.
Acceptance/handoff base:e74ec1f66b1b475f3d91b54183818c8168c2ab3b.

C240 scientific execution HEAD:7bf66561cfb151a6ba2562791a1645b760ad6f1f.
Published log commit:24141d62cdb58be0d11ae3b57e35b5f0593c7e50.
Log SHA256:48066d34eee74c201dae7660fd32dd8b04bebedefd73547e745cfa51f8b24315.
Summary SHA256:3551a5da3346381fdeb81b80a7cd297822ee51f64e80f9d966158ecf4c36b8b0.
Local summary:runs/c240-v5b-saved-position-audit-4b604be67f5b47f0b18cabdb2513d12d/summary.json.
Require exact execution-valid PASS, all_discrete_replays=True, capability/causal claims False.

Required C240 artifacts:
- audit-plan.json:31d2b0579d65b354979ef1d98e3012a57a95820e2f12cd729c931c8d8525bc25
- diagnostics.json:3db440f1348746bbdee122abd404fa7894cca9a9cc5a7abd8d688735c575be8e
- paired-orders.json:4e9bb61c419a9f710374261f8b5c95fd5414ce254fb2a7d5b1963ca88bc9fc6f
- row-audit.json:bffbba05c1625ff8375867a7642c9087ba6edcc901fa31214e2b396a87bf2d4e
- validation-summary.json:ba79501874430b2967db3e2c57cf9bd8abe8cae0258e6827ff1b92e7b716a66e

C239 remains an inherited protected input and supplies fresh-initial identities plus the fixed
16-row source mapping:
Execution HEAD:c847609c8d045c9c5db4ec882bf336a9671180ff.
Summary SHA256:500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af.
Local summary:runs/c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5/summary.json.
Require its exact valid negative with cell_outcomes ORDER_HOLDOUT_MISS:12.
Never load C239's trained checkpoint as initialization.

## Fixed partition and behavioral controls

Validate the exact C239 split-dataset artifact first, then repartition its16 unchanged rows:
- TRAIN: values[0,1], both orders,queries,languages —8 rows;
- HOLDOUT: values[1,0], both orders,queries,languages —8 rows.

Canonical C241 partition SHA256:
1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a.

Each split has4 rows/language,2 per order,2 per query and two targets of each byte per language.
Exact IDs/prompts are disjoint; inherited split="TRAIN" provenance is preserved.
The C241 outer partition alone controls optimizer membership.

The registered C239 query_fixed_position rule reaches exactly50% on TRAIN because each queried
entity occurs in both rendered positions. A fixed entity-value lookup matching TRAIN assignment
reaches exactly0% on HOLDOUT. These are predeclared control predictions, not post-result labels.

## Fixed model/training conditions

Seeds234001,234002,234003; ordered seed/full then seed/gru_only.
Fresh Full13488/GRU-only10160 parameters,width16,48 slots. Recreate models from the same seeds,
make the GRU-only common-weight copy before either paired model trains, and require each initial
fingerprint to match the corresponding C239 initial_sha256. Initial/final identities must differ
after valid training.

Same byte renderer, target bytes and unrestricted256-class output. Same normal/evidence-blind/
query-blind views. AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 steps.
CPU float64,threads2,deterministic algorithms.

Each update uses TRAIN indices0..7 repeated four times. The complete C241 fit executable AST must
match accepted C239.fit except the progress tag, and STEPS/BATCH/LR/CLIP/TOL must match exactly.
No random sampling, loss change, curriculum, continued training or checkpoint selection.

Only TRAIN is evaluated before fitting. Fit receives only TRAIN normal tensors/targets.
HOLDOUT tensors first reach the evaluator after the400-step endpoint. No holdout-driven early stop,
hyperparameter choice, seed replacement or extra update is permitted.

## C241-specific metrics and gate

Do NOT call the inherited C234 fact_pair metric on assignment-fixed splits. A fact-swap counterpart
is absent within each split, so fabricating one would violate the dataset contract.

For each split/language compute from the actual three model forwards:
- rows=4;
- exact normal accuracy and answer NLL;
- evidence/query masked accuracies and drops;
- query_pair_accuracy over2 groups: same assignment/order, two queries with different targets;
- order_pair_accuracy over2 groups: same assignment/query, both fact orders with the same target.

Validate finite values, exact key schema, ranges and mask-drop arithmetic.
Require on BOTH TRAIN and HOLDOUT for every Full seed/language:
accuracy>=0.90,query_pair>=0.80,order_pair>=0.80,evidence_drop>=0.35,query_drop>=0.35.
Discrete thresholds mean4/4 normal answers,2/2 query pairs and2/2 order pairs.
GRU-only gate is independent and cannot substitute for Full.

Per seed/family/language classify:
- TRAIN_FIT_MISS if TRAIN full criteria miss;
- ASSIGNMENT_HOLDOUT_MISS if TRAIN passes and HOLDOUT misses;
- BOTH_PASS if both pass.

Scientific status PASS iff all Full cells are BOTH_PASS. A valid miss is ACCEPTED VALID NEGATIVE,
not grounds for threshold/seed/step changes. Any integrity failure is INVALID / RETRY SAME C241.

## Workload and replay

Six models x400 steps=2400 training steps/76800 answer presentations.
Each TRAIN row appears1600 times/model.
Per model:initial TRAIN3,final TRAIN3/HOLDOUT3,reload TRAIN3/HOLDOUT3 =15 evaluation forwards.
Totals:2490 model forwards/77520 presented rows. Before reload409 calls/12872 rows;reload adds6/48.
One six-state checkpoint bundle. No parent model inference or scientific network calls.

Require changed weights, non-mutating evaluation, strict checkpoint schema/order/fingerprint,
exact saved/reloaded argmax arrays, raw-logit/metric replay<=1e-9 and actual hook counts.
Postcheck recomputes summary, validates plan/split hashes, artifacts and fresh initial identities
without extra model forwards.

## Protection, suite and outputs

Inherit C240286 source pins/430 protected inputs. Add C240 summary+5 artifacts and OWN6:
292 source pins/442 protected inputs. C239 summary/artifacts are already inherited; verify its
summary exact hash and do not double-count. Deciding-path dependency union17:five C231 LM_SOURCES
plus C230 through C241 benchmark/helper entry points.

OWN6:
- fold_lm/v05_benchmarks/model_c241_assignment_holdout.py
- tests_lm/test_v05_c241_assignment_holdout.py
- tools/run_c241.ps1
- tools/invoke_c241.ps1
- this preregistration
- docs/v5b-assignment-holdout-v0.1.md

Own tests24;modules126;loaded2954/focused2953. Only inherited exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Use actual loader counts/unique IDs. No accepted historical source/test/log is edited.

Local ignored outputs:assignment-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Checkpoint schema fold-c241-assignment-holdout-v1 with six ordered states.
Only console log and receipt are published to docs/experiment-run-logs/c241/latest.*.

Manifest SHA256:
1552239e7701744af508ba41ac4b620898d219380b377be1c5671b816dbac1f8.

## Review and stop

After all OWN files are committed, re-fetch them at a fixed review HEAD; compare source/script blobs
to tested bytes; compile/import; run24 own tests; verify manifest/split hashes,parent schema/writer
semantics,actual loader dispatch,fit AST,holdout timing,free names,count arithmetic and embedded
Python/PowerShell argument order. Synthetic execution is authoring evidence only.

Execution order:dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile ->
Python syntax/source/artifact/split precheck ->24 own tests ->2953 focused tests ->C241 probe ->
artifact postcheck -> remote log publication. Operational branch/tree/HEAD/ACTIVE mismatches skip
before execution/log publication. Do not report full regression,Windows AST or user-local artifact
checks as PASS until the authoritative runner executes them.

A PASS rules out the two preregistered simple shortcuts on this bounded fixture but does not prove
a unique representation or general language. No larger model,extra steps,paid API,external corpus,
cleanup/history rewrite or production change. Gate F NOT PASSED;numeric-memory tuning paused.
Judge C241 before registering C242.
