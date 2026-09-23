# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C240 ACCEPTED PASS (diagnostic integrity only). C241 ACTIVE / NOT YET JUDGED. C242 NOT REGISTERED.**
C241 is the unique ACTIVE experiment: fresh balanced-position assignment holdout, not a Gate F run.
C239 remains ACCEPTED VALID NEGATIVE; C238 remains minimal seen-TRAIN fitting PASS.
Post-authoring review is PASS; authoritative runtime prechecks/tests/regression remain mandatory.

## Latest accepted evidence — C240

Scientific execution HEAD:7bf66561cfb151a6ba2562791a1645b760ad6f1f.
Published log commit:24141d62cdb58be0d11ae3b57e35b5f0593c7e50.
Log SHA256:48066d34eee74c201dae7660fd32dd8b04bebedefd73547e745cfa51f8b24315.
Summary SHA256:3551a5da3346381fdeb81b80a7cd297822ee51f64e80f9d966158ecf4c36b8b0.
Local summary:runs/c240-v5b-saved-position-audit-4b604be67f5b47f0b18cabdb2513d12d/summary.json.

24 own tests PASS in0.104s;2929 focused tests PASS in112.356s.
286 source pins/430 protected inputs. No new training/model forward/checkpoint load/write.
288 saved predictions,96 normal rows,576 rule comparisons,48 order pairs,24 diagnostic cells.
All discrete parent replays and persisted audit recomputation PASS;protected inputs/tracked tree/
execution HEAD preserved;run_execution_valid=True. capability_pass_claim=False;causal_claim=False.

TRAIN normal rows:48/48 correct and48/48 query_fixed_position.
HOLDOUT normal rows:4/48 correct,44/48 other_entity,44/48 query_fixed_position,0 outside-supplied.
Matched order pairs:4/48 same answer,4/48 both correct,44/48 both fixed-position.
This is strong behavioral consistency with the preregistered positional shortcut,not proof of an
internal algorithm. On TRAIN entity=fixed-position;on this binary HOLDOUT fixed-position=other entity.

Acceptance/artifacts:docs/experiment-ledger-addendum-c240-c241.md.
Acceptance record commit:dc75a8defc0d21d70d1c7ec06914914468e0bd77.
Acceptance/handoff base:e74ec1f66b1b475f3d91b54183818c8168c2ab3b.
No C239 verdict reversal,answer inversion,NLL reconstruction,core ranking or Gate F promotion.

## Preserved earlier evidence

C239:all12 TRAIN cells pass;all12 reversed-order HOLDOUT cells miss.
C238:all12 seen-TRAIN cells pass after complete-cohort sampling.
C237:diagnostic PASS with internal sensitivity but no correct answer switching.
C236:valid negative under random replacement sampling.
C235 diagnostic PASS;C234/C233 valid negatives;C232 bounded template-byte learning only.

## Active C241 — balanced-position assignment holdout

Experiment:C241-v5b-assignment-holdout-balanced-order.
Stage:V5-B-ASSIGNMENT-HOLDOUT-BALANCED-ORDER.

One question:after exposing each queried entity in both rendered positions during TRAIN,can the
unchanged fresh model/optimizer transfer from assignment[0,1] to held-out assignment[1,0]?

Start from the exact C23916-row source mapping and preserve row bytes/provenance.
TRAIN8:values[0,1],both orders,queries,languages.
HOLDOUT8:values[1,0],both orders,queries,languages.
Exact prompt/ID sets are disjoint. Each language/split has4 rows,2 orders,2 queries,balanced0/1 targets.
Split SHA256:1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a.

The C239 query_fixed_position shortcut is predeclared to score50% on C241 TRAIN because each queried
entity occupies both positions. A fixed entity-value lookup can score100% TRAIN but0% HOLDOUT.
A HOLDOUT pass would therefore rule out these two simple behavioral shortcuts on this bounded
fixture;it would not identify a unique internal mechanism or prove general language.

Fresh models must match C239 initial_sha256. Never load C239/C238 trained states. Make the
common-weight GRU-only copy before either paired model trains. Keep Full13488/GRU-only10160,
width16/48 slots,byte renderer,unrestricted256-way output,seeds234001-234003,AdamW lr0.005,
betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 steps,CPU float64,threads2,
deterministic algorithms. Every update uses TRAIN8 repeated4. C241.fit is source-normalized equal
to C239.fit except the progress label;balanced_indices is equal after experiment-label normalization.

Only TRAIN is evaluated before fitting. HOLDOUT is first evaluated after step400 and cannot control
updates/early stop/selection. No inherited fact_pair score is fabricated:each split contains one
assignment only. Instead score exact accuracy,query-pair and order-pair both-correct,plus evidence/
query mask drops and NLL.

Primary gate on BOTH TRAIN/HOLDOUT in every Full seed/language cell:
accuracy>=0.90,query_pair>=0.80,order_pair>=0.80,evidence_drop>=0.35,query_drop>=0.35.
At4 rows/2 pairs this requires4/4 answers,2/2 query pairs,2/2 order pairs. GRU-only independent.
Classify TRAIN_FIT_MISS,ASSIGNMENT_HOLDOUT_MISS or BOTH_PASS using full criteria.
A valid miss is ACCEPTED VALID NEGATIVE;integrity failure is INVALID / RETRY SAME C241.

Fixed workload:6 models x400=2400 training steps/76800 answer presentations.
Per model initial TRAIN3+final TRAIN3/HOLDOUT3+reload TRAIN3/HOLDOUT3=15 evaluation forwards.
Totals2490 model forwards/77520 rows;one ordered six-state checkpoint bundle;no scientific network call.

Protection:292 source pins/442 inputs;direct dependency union17;OWN6.
Own tests24;modules126;loaded2954/focused2953. Only inherited exact historical exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:assignment-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Manifest:
1552239e7701744af508ba41ac4b620898d219380b377be1c5671b816dbac1f8.

Design:docs/v5b-assignment-holdout-v0.1.md.
Registration:docs/experiment-ledger-addendum-c241-preregistration.md.
Preregistration/review HEAD:240aff9ebcd8cb920b088fd7c2e14057fcdd07f9.
Use tools/invoke_active.ps1 with the final activation HEAD returned to the user.

## C241 post-authoring review

`post_authoring_review = PASS`
Review HEAD:240aff9ebcd8cb920b088fd7c2e14057fcdd07f9.
Scope:committed remote-byte/static authoring review;not formal C241 execution.

All6 OWN files were re-fetched after authoring. Reviewed Git blobs:
-benchmark:90b1b2aa4d629e6320950e5edef16e224232bd6d
-tests:ec45abaaf6c91334dd2b6b850ab28c8d1ffcceb5
-runner:3c8eb4f7acada6449b62464cc1ec73dbfbadb42e
-launcher:5575019b6c15d7de06f62570692fb193054b4f42
-preregistration:0efdee586f23733a153b098746796c8774c757f2
-design:4effb369ab71d70f04206fd4a47bc317496288cf.
Comparison from acceptance basee74ec1f6 to review HEAD changes exactly those6 additions.
No accepted source/test/log/shared launcher is modified.

Remote-readback checks actually completed:
-24 test methods counted from the committed test module;
-no NUL or placeholder/C242 residue in new Python source/test;
-C241 fit body normalizes exactly to immutable C239 fit after C239->C241 progress-label replacement;
-balanced_indices normalizes exactly to C239's8x4 helper after experiment-label normalization;
-runner contains exactly3 embedded Python blocks and declares focused2953;
-launcher resolves only ACTIVE C241,parses the runner before the execution/publication block,
and pins the exact C240/C239 local summary paths;
-manifest/split identities,workload/protection/count arithmetic,parent field contracts and direct
dependency union were re-read against committed source/preregistration;
-source/test/runner/launcher/doc blobs above are from the committed review HEAD.

Reviewer environment could not clone github.com because DNS resolution failed. Therefore Python
py_compile/import,the24 own tests,full2953 historical regression,Windows PowerShell AST,user-local
parent artifact reads and the six scientific models were NOT executed in the reviewer container.
They are not represented as already passed. The authoritative Windows runner executes syntax,
precheck,24 own tests and2953 regression before C241 training;any failure stops before a valid result.
The committed source was manually/static-reviewed for free-name/import bindings,custom metric
schema,holdout timing,save/load/replay order and parent loader dispatch.

Only this unpinned activation/review handoff changes after review HEAD. Verify final branch HEAD
before giving ExpectedHead;do not advance the experiment branch while the user runs.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted evidence and tools/run_c167.ps1.
No cleanup/history rewrite,paid API,external corpus,larger model or production runtime change.
24 own tests ->2953 focused tests ->C241 assignment holdout ->artifact postcheck ->remote log publication.
Stop same C241 on integrity faults;repair transport-only failure without retraining.
Judge C241 before registering C242.
