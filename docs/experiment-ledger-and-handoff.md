# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C241 ACCEPTED VALID NEGATIVE. C242 ACTIVE / NOT YET JUDGED. C243 NOT REGISTERED.**
C242 is the unique ACTIVE experiment. Post-authoring review PASS; full authoritative execution pending.
C240 remains diagnostic-integrity PASS; C239 remains a valid order-transfer negative;
C238 remains PASS only for fitting the seen16 prompts.

## Latest accepted evidence — C241

Scientific execution HEAD:b7b33718da1edd94cc1ed113baa6e56cc27dc3e4.
Published log commit:a53a96e6e2ec716d33ab3f7f8ae9cb2d49d110a0.
Publisher log SHA256:5067ca2deefdc14b03e72500918bc2eae134f8a01b1751e1be450a93275f50f8.
Summary SHA256:b228992dfd5d85e59d7c45d1dd899145588978a19ade0817a547d740e8c67e26.
Local summary:runs/c241-v5b-assignment-holdout-445ca70720c948e7966236416922e580/summary.json.

24 own tests PASS in3.739s;2953 focused tests PASS in92.184s.
292 source pins/442 protected inputs. Six models x400 updates;2400 steps/76800 training
presentations/2490 full-model forwards/77520 total rows. All checkpoint/prediction replays and
weight-update checks PASS;partition/initial-ID postcheck PASS;tracked tree clean;execution HEAD
preserved;run_execution_valid=True. Acceptance is based on published logs/postcheck,not a reviewer
checkpoint rerun or independent full-log byte rehash. Publication changed only latest.log/latest.json.

All12 seed/family/language cells:
TRAIN accuracy4/4,query/order pairs2/2,evidence drop0,query drop0.50.
HOLDOUT accuracy0/4,query/order pairs0/2,evidence drop0,query drop-0.50.
Both family gates False. cell_outcomes TRAIN_FIT_MISS:12 means the full TRAIN criteria missed
because evidence_drop=0,NOT that the normal TRAIN answers were wrong. Do not rename those cells.
TRAIN NLL0.000558-0.000726,HOLDOUT8.126891-8.705085 at logged precision.

C241 kept box=0/book=1 fixed in TRAIN. Query identity alone therefore predicted targets. The
outcome is consistent with fixed entity-value behavior but aggregate scores do not identify exact
wrong bytes or a unique internal algorithm. Our experimental design removed the position shortcut
while leaving a value shortcut; this is not grounds to blame only the architecture.

Acceptance/artifact identities:docs/experiment-ledger-addendum-c241-c242.md.
Acceptance/base commit:0caa412ce1ce6452d721adac19d2d37f6e3d0128.
Do not rerun/rescue C241 or relax its gates. Gate F is unchanged.

## Active C242 — balanced value recombination

Experiment:C242-v5b-balanced-value-recombination.
Stage:V5-B-BALANCED-VALUE-RECOMBINATION.
One question:can fresh models trained with variable entity values and positions solve held-out
value-pair recombinations under the fixed400-update,32-row complete-cohort recipe?

Use existing C234 dataset.json,objects[0,1],digits0/1/2/3;preserve original row bytes/order.
TRAIN32:ordered assignments(0,1),(1,0),(2,3),(3,2),both orders,queries,languages.
HOLDOUT64:remaining8 ordered distinct pairs,also both orders,queries,languages.
Prompt/ID/assignment-group sets are disjoint. Each individual entity/value pairing appears in TRAIN;
only pair combinations are held out. Original split labels are provenance,not C242 optimizer membership.
No claim of a pristine external benchmark or unseen vocabulary.

Precheck exact joint balance and finite-dataset ambiguity ceilings. Query-only and identical
value-masked-input lookup cannot exceed25%;identical query-masked inputs50%;the fixed-query-position
rule50%. These controls prevent C241's evidence-redundant TRAIN design;they are not learned accuracy.

Fixed:Full13488/GRU-only10160,width16/48 slots,fresh seeds234001/234002/234003,C241 initial fingerprints,
common-weight baseline copy before either fit,unrestricted256-byte output,C234 renderer/evaluator,
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 updates,CPU float64,threads2,
deterministic algorithms. Fit AST equals C241 except progress label. Index helper changes8x4 to32x1.
Training diversity/digit coverage/repetitions change together;not a one-variable causal comparison.
Never initialize from a trained parent checkpoint. HOLDOUT first reaches a model after step400.

Require BOTH TRAIN/HOLDOUT to meet accuracy>=0.90,fact/query/order pair>=0.80,both mask drops>=0.35
in every Full seed/language cell. GRU-only independent. TRAIN has16 rows and8 pairs per language;
HOLDOUT32 rows/16 pairs. Minimum correct counts15/16 and7/8;HOLDOUT29/32 and13/16.
Use actual C234 fact/query metrics plus new order-pair score. C241's fixed4-row metric validator
is used only by its own parent summarizer,not on C242 results.
Report TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS beside actual accuracy/mask numbers.
A valid Full miss is ACCEPTED VALID NEGATIVE;integrity fault is INVALID / RETRY SAME C242.
A pass supports this bounded recombination task only,not general language,core advantage or Gate F.

Workload:6x400=2400 updates/76800 training presentations;90 evaluation forwards/4032 scoring rows;
2490 total full-model forwards/80832 rows;one six-state checkpoint bundle;zero scientific network calls.
Before reload409 calls/13184 rows per model;reload6/288;final415/13472.
Protection:298 source pins/454 inputs;direct dependency union18;OWN6.
Own tests24;modules127;loaded2978/focused2977;only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:recombination-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Schema fold-c242-recombination-v1;six ordered states. Summary counters are
train_steps,answer_presentations,model_forward_calls,row_presentations,not older total_* names.

Dataset SHA256:72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85.
Split SHA256:9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0.
Manifest SHA256:8088155ef7ba95eb47a8a7ae3790247ff20d61804ac08c7fc1b1ed2f0c645760.
Design:docs/v5b-balanced-recombination-v0.1.md.
Registration:docs/experiment-ledger-addendum-c242-preregistration.md.
Preregistration/review HEAD:704563a6d2ffc7b5ed4f79ebfcaf91f96ed7c336.
Use tools/invoke_active.ps1 with the final activation HEAD,not the earlier review or C241 HEAD.

## C242 post-authoring review

`post_authoring_review = PASS`
Review HEAD:704563a6d2ffc7b5ed4f79ebfcaf91f96ed7c336.
Scope:committed-byte authoring and synthetic-path validation;not the actual scientific run.

All6 OWN files re-fetched after completion. Reviewed Git blobs:
-benchmark:623ddbed9e922717979855863edb0c68313df0d9
-tests:5c12f74ebf299263d9bacb5ce2f16678ae2679b5
-runner:febfaaf7a915e3795a4db7f99433a1032b78d032
-launcher:74312b131603e1881dafc9b9b372a6a473b0fb23
-design:3d52e2ae6f72a18a8417849ec7a6bb21dcaa6cfc
-preregistration:feb4511e3a00a335749d331d80bf59ad02da9884.
Four code/script full-file Git blob hashes were mechanically matched against local tested bytes.
Compare from acceptance/base to review HEAD changes exactly6 OWN additions,no accepted file edits.
A one-character publication transcription error in result validation was caught and corrected
before readiness;the final source is byte-identical to the compiled/tested local source.

Actually executed on the matched source after remote readback:
-Python compile/import,UTF-8/NUL checks;symbol-table global/import audit:0 unresolved names in both files;
-all24 own tests PASS in2.713s (first authoring run2.737s);actual unittest loader constructs24 unique tests;
-full C234 dataset independently reconstructed with exact canonical hash;new split/manifest hashes pass;
-both masked-input ceilings,joint factor balance,disjoint prompts/groups/IDs and actual batch membership;
-fit AST/constant agreement with a transcription of the retrieved immutable C241.fit excerpt;
-initial-state rejection before fit,held-out evaluation after fit,actual forward/row counters;
-actual new six-model run/save/reload/postcheck exercised with synthetic models and substituted
 parent/protection/context adapters,including tampered artifact/wrong-HEAD rejection;
-three embedded Python blocks compile;precheck argv1/2 and postcheck argv1/2/3/4 match launcher/runner;
-source ordering checks:own loader/common copy before fit,save before reload,no parent trained initialization.

Source review also checked C241 context/writer/summary semantics and actual C234 dataset/render/
paired-metric/evaluator contracts. C234 evaluator supports the selected complete pairs;new order
pairs have equal targets. All direct helper paths remain protected,including lazy context imports.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,isolated workspace with complete
new files and a reviewer-only C241.fit excerpt,not a complete checkout. github.com DNS lookup failed;
connector reads supplied authoritative source. The C234 evaluator was source-reviewed;own tests
use a synthetic Binding double,not the actual model factory or accepted user-local artifacts.
NOT executed here:full2977-test historical suite,Windows PowerShell AST,accepted local input
precheck,or the scientific6-model FOLD/GRU run. None is reported PASS. Those remain mandatory.
Historical count arithmetic is accepted2954 loaded+24=2978,minus the same exact1 exclusion=2977;
the authoritative loader enforces it. No extra exclusions or mutable-control-state assertions.

Only this unpinned handoff changes after review HEAD. Re-read it and verify branch HEAD before
issuing ExpectedHead. Do not advance this branch while the user's formal run is active.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve all accepted sources/tests/logs and
 tools/run_c167.ps1. No larger model,paid API,external corpus,history rewrite,cleanup or production change.
24 own tests ->2977 focused tests ->C242 probe ->postcheck ->remote log publication.
Stop same C242 on integrity failures;repair log-only transport without retraining. Judge C242 before C243.
