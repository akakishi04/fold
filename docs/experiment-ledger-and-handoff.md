# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C242 ACCEPTED VALID NEGATIVE. C243 ACTIVE / NOT YET JUDGED. C244 NOT REGISTERED.**
C243 is the unique ACTIVE experiment:offline saved-answer error analysis,not a capability run.
Post-authoring review PASS;authoritative runtime prechecks and full regression remain mandatory.

## Latest accepted evidence — C242

Scientific execution HEAD:372c2c37429acece3f06a9b4521313da4b3d5f8e.
Published log commit:998b34447fc1ac5c4a0f2c42b0a4eb1958b87eb0.
Publisher log SHA256:490be44e71cbaab6169f4965ce7983c0276a543523921ef1c162b7574dcacd9e.
Log bytes:564532. Summary SHA256:d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb.
Local summary:runs/c242-v5b-balanced-recombination-530e801ba23f496aa8e0a588e0d52982/summary.json.

24 own tests PASS in6.420s;2977 focused tests PASS in93.412s.
298 source pins/454 inputs protected. Six models x400=2400 training steps/76800 answer presentations.
2490 model forwards/80832 rows. All checkpoint/prediction replays and weight-update checks PASS.
Persisted split/initial-identity replay PASS;tracked tree clean;execution HEAD preserved;
run_execution_valid=True. Both family recombination gates False;scientific status FAIL.
cell_outcomes RECOMBINATION_MISS:12,not TRAIN_CRITERIA_MISS.

All12 TRAIN cells:16/16 answers,8/8 fact/query/order pairs,evidence drop0.75,query drop0.50.
HOLDOUT exact answers (32 per language):
-seed234001:Full EN7 JA9;GRU-only EN11 JA12.
-seed234002:Full EN13 JA12;GRU-only EN13 JA12.
-seed234003:Full EN12 JA12;GRU-only EN8 JA10.
HOLDOUT accuracy21.875%-40.625%,below90% in every cell. Full query pairs0/16 throughout;
GRU-only1/16 for both languages of234001,0/16 otherwise. TRAIN NLL0.001047-0.003695;
HOLDOUT3.947179-6.914980 at logged precision.

This establishes training-distribution fitting with mask sensitivity but not generalization to
new value-pair combinations. It does not establish a unique binding algorithm or core superiority.
TRAIN co-occurrence remains deterministic:0 pairs with1,2 with3. Inferring the queried value from
the TRAIN partner of the OTHER entity's value also solves TRAIN and can pass masking checks.
This is a remaining ambiguity,not a claim that the actual models follow that rule.

Acceptance/artifacts:docs/experiment-ledger-addendum-c242-c243.md.
Acceptance/base commit:17d5cd5d82c584faaee0b02d52a22776c9ef47a3.
The log publication is one commit after execution and changes only c242/latest.log/latest.json.
Acceptance uses immutable log ranges and recorded local postcheck,not a checkpoint rerun or
independent full-log byte rehash. Do not rerun/rescue C242 or modify its registered thresholds.

## Preserved earlier evidence

C241:valid negative;normal TRAIN100% but evidence drop0 and HOLDOUT0%,full TRAIN criteria missed.
C240:diagnostic PASS;C239 saved errors largely matched fixed query-to-position behavior.
C239:valid order-transfer negative. C238:PASS for16 seen-TRAIN prompts only.
C237 diagnostic PASS;C236 valid negative under random replacement sampling;C235 diagnostic PASS;
C234/C233 valid negatives;C232 bounded template-byte learning only. All evidence is preserved.

## Active C243 — saved recombination error audit

Experiment:C243-v5b-saved-recombination-error-audit.
Stage:V5-B-SAVED-RECOMBINATION-ERROR-AUDIT.
One question:do saved HOLDOUT errors select the wrong supplied value,an absent value consistent
with fixed TRAIN partner associations,or another byte?

Change only offline measurement. Keep all six C242 final models,TRAIN32/HOLDOUT64,raw saved
predictions,three views,targets,source provenance and verdict fixed. No training,inference,
checkpoint deserialization,answer correction or new evidence samples.

Use actual C242.validate_result and summarize for parent integrity. Read final[split][language]
and predictions[split][view] after step400,as confirmed from the parent writer/replay source.
Independently recompute all discrete metrics with exact fact/query/order grouping and mask-drop
semantics. Require agreement<=1e-9. NLL remains finite/hash-protected only;nll_recomputed=False.
The checkpoint artifact is hashed,not loaded as a model. All output bytes0..255 remain valid candidates.

Derive and verify the fixed TRAIN co-occurrence map0->1,1->0,2->3,3->2. Ten registered rules:
entity,other_entity,partner_of_other,query_fixed_position,first,last,constant_0..constant_3.
Classify normal predictions in precedence order:correct,other_supplied,absent_partner_of_other,
absent_partner_of_queried,other_byte. Retain all per-row rule matches and fact/query/order pairs.

Interpretation boundary:entity=partner_of_other on TRAIN. On HOLDOUT the four digit categories
exhaust0..3,so membership in a named category cannot prove a mechanism. Rule agreement is behavioral,
not causal,and reused answers are not independent replication. Do not promote Gate F or change C242.

Primary record counts:1728 saved answers,576 normal rows,5760 rule comparisons,864 pair records,
24 diagnostic cells. Scientific model forwards/training/checkpoint loads/writes/network calls0.
Repeated verification reads and historical regression fixture costs are separate.
C243 PASS means diagnostic integrity only;no minimum agreement with any rule. Faults are INVALID /
RETRY SAME C243. Low or mixed agreement is not an execution failure.

Protection:304 source pins/466 inputs;direct dependency union19;OWN6.
Own tests24;modules128;loaded3002/focused3001. Only inherited exact historical exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:audit-plan.json,row-errors.json,pair-audit.json,diagnostics.json,
validation-summary.json. Postcheck reconstructs every output exactly from original parent files.
Manifest SHA256:02f2420c59bfa7a232686ea42cf2ed47ee6c17ebe2714e81a2fbc169a8e70379.
Design:docs/v5b-saved-recombination-audit-v0.1.md.
Registration:docs/experiment-ledger-addendum-c243-preregistration.md.
Preregistration/review HEAD:bfe77748f5c55aae2662f180ecea146000b6e449.
Use tools/invoke_active.ps1 with the final activation/handoff HEAD,not the review or C242 HEAD.

## C243 post-authoring review

`post_authoring_review = PASS`
Review HEAD:bfe77748f5c55aae2662f180ecea146000b6e449.
Scope:committed-byte authoring and synthetic-data execution,not formal C243 analysis.

All six OWN files were fetched again after authoring completion. Reviewed Git blobs:
-benchmark:77a810274ed8572959ed7198030f2af963b90413
-tests:4a310a1f0d79ef3dd426bf701a2bc4ed21e6548d
-runner:db8055e3f80f08f0250e67951c24505b8b2d3634
-launcher:903feb3ba9a18058cf05e4f1cdea2394df5164dc
-design:04ac0da08aae96a3fa68f1b6cb5c193e64f233d9
-preregistration:52277b0f348f0bb4fdbe6f351ff8d6db59527a01.
Four code/script Git blob hashes were mechanically matched to full locally tested bytes after
remote readback. Comparison from acceptance/base to review HEAD contains exactly six additions;
no accepted source,test,log or shared launcher was modified.

Actually executed:
-Python compile/import and UTF-8/NUL checks on complete new source/test files;
-symbol-table free-global/import audit:zero unresolved names in either Python module;
-all24 own tests PASS in0.228s before publication and0.237s after readback;
-actual own unittest count and unique IDs;synthetic constructed3002-test suite filtering to3001;
-immutable split/manifest hashes,partner-rule degeneracy and disjoint HOLDOUT category controls;
-all ten synthetic rule patterns,unrestricted-byte/schema/nonfinite/replay rejection;
-actual loader on synthetic parent-shaped files with substituted parent summarizer;
-actual run and persisted postcheck with substituted protection/parent adapters,including
 wrong-HEAD and artifact-tamper rejection;all five derived outputs exactly replayed;
-independent relational pair matching agreed on200 synthetic three-view prediction arrays;
-three embedded runner Python blocks compile;precheck argv1/postcheck argv1,2,3 verified;
-source AST confirms actual loader/analyze dispatch and no executable model/training operations.

Parent C242 writer,checkpoint replay,summarizer and validator were read at the immutable log HEAD.
Final predictions are trained outputs,not initial metrics;the parent stores32/64 predictions per
view and includes fact/query/order scores. The current child uses the correct field names and
grouping semantics. Lazy parent/context helpers are included in the19-module protected union.
Launcher inspection confirms branch/tree/ExpectedHead/ACTIVE guards before logging/publication,
runner ParseFile before execution,and the exact C242 local summary directory.

Reviewer environment:Python3.13.5,isolated namespace workspace,not a full repository checkout.
A git ls-remote attempt failed because github.com DNS resolution was unavailable. Connector reads
supplied committed source. Full3001 historical regression,Windows PowerShell AST,accepted local
parent prechecks and C243 analysis of actual C242 predictions were NOT executed here. None is
represented as PASS. The authoritative Windows runner must perform these remaining checks.
The200-array parity check is reviewer-only synthetic validation,not200 additional scientific samples.

Only this unpinned activation/handoff record changes after review HEAD. Re-read it and verify
branch HEAD before issuing ExpectedHead. Do not advance the branch while the formal run is active.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted sources/tests/logs and tools/run_c167.ps1.
No larger model,paid API,external corpus,history rewrite,cleanup or production runtime change.
24 own tests ->3001 focused tests ->C243 saved-error audit ->postcheck ->remote log publication.
Stop same C243 on integrity faults;repair transport-only failure without repeating completed analysis.
Judge C243 before registering C244.
