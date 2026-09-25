# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C256 ACCEPTED PASS (bounded three-entity task-shift capability). C257 ACTIVE / NOT YET JUDGED. C258 NOT REGISTERED.**
C257 is the unique ACTIVE experiment: V5-B frozen unseen fact-order transfer.
C256 is a capability PASS within its preregistered authored task, not merely diagnostic integrity.
No production adoption, general-language claim, core-superiority claim or Gate F promotion.
C252 remains ACCEPTED VALID NEGATIVE. C253/C254/C255 remain diagnostic PASS.
All earlier accepted verdicts and invalid-attempt recovery records are preserved.

## Latest accepted evidence — C256

Scientific execution HEAD: db9f3cb90d9268066c34fc91300193058301f06c.
Published log commit: 5695706c6306156fa079ce092581270ca781af71.
Publisher log SHA256: 4f21d18bec9eb3ae937c42be9d8af3091d67a241a53a85820afd3e6694110ce6.
Log bytes: 654496.
Summary SHA256: 56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184.
Local summary: runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.
Acceptance record: docs/experiment-ledger-addendum-c256-c257.md.
Acceptance/base commit: ee4c282687c71bed407ecb687659edd7103c740d.

24 own tests PASS in0.832s; 3313 focused tests PASS in207.503s.
382 source pins/623 protected inputs verified. Ten fresh models each completed800 updates:
8000 training updates,384000 training presentations,8120 model forwards,401280 total row presentations.
Changed total/head weights, strict checkpoint state loading, saved prediction identity, metric and
raw-logit replay passed. Persisted metric/artifact checks and protected-input checks passed.
Tracked tree clean; scientific execution HEAD preserved; run_execution_valid=True.
scientific_status=PASS; candidate_gate=True; all_replays=True; all_weights_changed=True.

This acceptance is based on immutable published log ranges, publication metadata and the recorded
local postchecks. The reviewer did not independently rerun the accepted learned checkpoints or
rehash the entire654496-byte log. Do not confuse publisher-reported hashes with a new byte rehash.

Deciding HOLDOUT correct counts per language, denominator72:

| Seed | aligned EN | aligned JA | EOS control EN | EOS control JA |
|---:|---:|---:|---:|---:|
|256001|72|72|29|25|
|256002|72|72|29|28|
|256003|72|72|26|24|
|256004|72|72|21|24|
|256005|70|72|20|22|

Candidate TRAIN720/720; HOLDOUT718/720 (99.7222%). Control HOLDOUT248/720 (34.4444%).
Whole-seed joint passes: aligned_precore_read5/5; eos_adapter0/5.
Candidate BOTH_PASS language cells10. Control TASK_SHIFT_MISS9; TRAIN_CRITERIA_MISS1.
The control seed256001 JA TRAIN query-triplet score is19/24, below0.80 despite66/72 normal accuracy.
Do not describe every control TRAIN cell as passing or perfectly fitted.

Candidate seed256005 EN HOLDOUT:70/72 answers,34/36 order pairs,22/24 query triplets,
evidence_drop0.722222...,query_drop0.638888...; all original thresholds are satisfied.
Other candidate HOLDOUT cells:72/72 answers,36/36 order pairs,24/24 query triplets.
The registered gate was not relaxed. Every candidate seed passes both languages and both splits.

Accepted artifacts:
-dataset.json:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b (34296 bytes)
-measurements.json:f7d11d7592769e54824d3d7dccc4e481029dc5157b6c35c333831408d7b032c8 (45697 bytes)
-task-plan.json:43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1 (2691 bytes)
-trained-models.pt:72d9ada52e48395290200c1c6918d7eef091aebd44a3d2a6176dc1dd442dae3a (1236574 bytes)
-validation-summary.json:a25fe29ed2deb33ceab64c0f7d7e450e6a143ea5c0bc428eea20b9d45dff8bc2 (2313 bytes)

Interpretation: the aligned reader learned withheld three-way assignments on five new initializations
under this fixed authored task and budget. The equal-parameter EOS control did not reproduce it.
This is not a compute-matched comparison, ordinary English/Japanese proficiency, a general benchmark,
proof of core superiority, or a guarantee over initialization populations. Relative to C252, names,
assignment split, sampling, batch and budget also changed; do not infer that three entities are
inherently easier or that general initialization robustness is solved.

Only abc and cba fact orders were used. The middle entity b/乙 never changed its middle position.
Value-assignment transfer does not establish transfer to the other four permutations.

## Preserved earlier evidence and recovery

C256's earlier precheck attempt remains INVALID, not scientific evidence:
failed execution1029158a60d40df24f599fb719411dbde2ffec06;
invalid log commit2dc541041c772d5b9a449bd247862ad906a9b5c8;
invalid log SHA2565e774f0043a8f4661bbda08fe1ccaa8f728b1e10315947677d7ee6a40f62dce8.
It stopped before own tests/regression/training on the incorrectly recorded manifest fingerprint.
The fingerprint and a separate whitespace-sensitive launcher test were repaired without changing
scientific conditions. Full history: docs/experiment-ledger-addendum-c256-execution-recovery.md.
The successful execution above supersedes the stale ACTIVE recovery state, not the invalid record.

C255 ACCEPTED PASS (diagnostic only): self HOLDOUT145/160 versus value residual swap140/160.
Scientific HEAD6b577da1edc7339dbfd68b3127870074de218e48; log48856dd7dabb84f1f8a71158d03a5ee9db2fd255.
Acceptance: docs/experiment-ledger-addendum-c255-c256.md.
Its two earlier invalid attempts remain in docs/experiment-ledger-addendum-c255-execution-recovery.md.
C254 query/order swaps:145/160 self,141/160 order,96/160 query; diagnostic only.
C253 residual removal:145/160 self,107/160 pre-residual,117/160 reader-only; diagnostic only.
C252 aligned reader4/5 whole-seed passes, not5/5: ACCEPTED VALID NEGATIVE.
C2512/5; C250 Full reader2/5,GRU reader4/5,EOS controls0/5.
C249 frozen reader dependency diagnostic. C248 bounded transfer but failed its all-seed gate.
C247/C246/C244/C242/C241/C239 remain accepted negatives; C245/C243/C240/C237/C235 diagnostics;
C238 seen-prompt fit only. C232 bounded byte learning and C233 competitive GRU-only result are not
general language or core-superiority claims. Do not overwrite accepted source/tests/logs.

## Active C257 — frozen unseen fact-order transfer

Experiment:C257-v5b-unseen-fact-order-transfer.
Stage:V5-B-UNSEEN-FACT-ORDER-TRANSFER.
One question: without further training, do all five accepted aligned-reader models retain their
bounded capability when the same facts appear in the four permutations never used by C256?

Freeze all ten accepted C256 final800-update models: seeds256001..256005, paired aligned_precore_read
and eos_adapter,14256 parameters each. Use actual C256.make_model/load_bundle, C252/C248 classes and
C231 factory. Strict-load final states, verify fingerprints, then eval/requires_grad=False.
No C252 checkpoints or C255 activations initialize the evaluation.

Changed: visible fact permutation only.
Held fixed: final weights, entities, assignments, original assignment splits, languages, queried
entity, target, delimiters,48-slot byte encoding and query-at-end placement.
Known orders:(0,1,2),(2,1,0). Novel:(0,2,1),(1,0,2),(1,2,0),(2,0,1), i.e.acb,bac,bca,cab.
Do not sort inputs back to a known order. No target/oracle/entity index is passed outside visible bytes.
Original rows144/split; novel288/split. TRAIN/HOLDOUT still name the original assignment partitions;
neither is used for optimization in C257. Preserve both arms and all seeds.
New dataset SHA256:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.

Per-model sequence:
-original C256.evaluate:6 forwards/864 rows, exact saved predictions and all metrics within1e-9;
-only after that replay barrier, novel orders:6 forwards/1728 rows;
-original restoration:6 forwards/864 rows, anchor/restored raw logits within1e-9 and exact argmax;
-complete weight fingerprint preserved,18 forwards/3456 rows per model.
C256 did not save endpoint raw logits. Initial replay uses its saved metrics/predictions; restoration
compares the new original anchor logits captured in this C257 run. Do not claim nonexistent replay.

Fixed primary gate: all five candidate seeds, both languages and both original assignment splits:
-original C256 criteria remain satisfied;
-EACH new permutation:accuracy>=0.90,query_triplet>=0.80,evidence_drop>=0.35,query_drop>=0.35;
-all-six-order consistency>=0.80, requiring every presentation in a group to be correct.
Per new order/language/split:36 rows/12 query triplets; minima33/36 answers and10/12 triplets.
All-six-order score:36 groups/language/split; minimum29/36 completely correct groups.
No pooling away a weak permutation. EOS performance is reported separately and cannot rescue or
fail the candidate gate. An already-failed original EOS gate is not a new independent control failure.
Outcomes:ORIGINAL_CRITERIA_MISS,NEW_ORDER_MISS,SIX_ORDER_MISS,PASS.
Valid criterion miss:ACCEPTED VALID NEGATIVE. Integrity failure:INVALID / RETRY SAME C257.

Workload:ten models,180 full-model forwards/34560 row presentations; training0;
accepted checkpoint bundle loads1; strict state loads10; new learned checkpoint writes0.
CPU float64,threads2,deterministic algorithms; finite outputs mandatory.
Artifacts5 plus summary.json:order-plan.json,order-dataset.json,eval-outputs.pt,measurements.json,
validation-summary.json. Evaluation archive schema fold-c257-order-eval-v1 contains original/novel/
restored logits, not newly learned weights. Persisted recomputation uses no additional model forwards.

Protection:388 source pins/635 inputs; direct deciding dependency union33; OWN6.
Own24; modules142; loaded3338/focused3337. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36.
Registration:docs/experiment-ledger-addendum-c257-preregistration.md.
Design:docs/v5b-unseen-fact-order-v0.1.md.
C256 acceptance and C257 preregistration are separate commits. All six C257 files already existed at
1ca89cbdf309976f36311265b617a9c86a59c489 before this activation review; do not duplicate registration.

## C257 post-authoring review

post_authoring_review = PASS
review_target_HEAD = 1487f6033e151f767b3ed3ebd29aabbe9648c94b
Review scope is committed-byte C257 authoring validation, NOT a formal scientific C257 execution.

All six OWN files were read from the committed repository. After the test correction, source/script/
document identities were re-fetched at the review HEAD. Complete local code/test/script copies were
matched against the remotely returned Git blob identities before rerunning the exact own tests:
-benchmark:12f9e114e5c6d0a47eacdf06f8ff1933686d1b1b;
-tests:d5ce8fb9bc08ab2fafcc9a3d8587133b5ae30e4e;
-runner:37bb99aba999d63e17321f444bf8e9d8330cafef;
-launcher:997577b31fa9d45b89b37fb168ad3aa55b954716;
-preregistration:621ad0877eff2d29389f7b6f60677aa755bf039a;
-design:7a24c42afb285a71eda337bb93199893518e5b24.

The initial exact24-test review reproduced23 PASS/1 FAIL in2.656s: test17 incorrectly expected a
ValueError when re-verifying an unchanged valid artifact with the correct HEAD. The test now passes
wrong-head and requires the saved-HEAD rejection. Its separate artifact-corruption rejection remains.
Repair commit1487f6033e151f767b3ed3ebd29aabbe9648c94b changes only this C257 authoring test.
No scientific source, data, manifest, seed, weight, gate, workload, runner or launcher changed.
No user C257 scientific attempt has been executed; this was a pre-activation authoring defect,
not an INVALID scientific result and not grounds to register a new C number.

Executed after correction:24/24 own tests PASS in2.571s. After remote identity readback and fresh
blob matching:24/24 PASS again in2.392s. Python compile/import, UTF-8/NUL checks, recursive global-name
binding audit (zero unresolved names), manifest hash, original/novel dataset hashes and semantic
24-test identity count passed. The exact suite also compiles all three embedded Python blocks,
checks CLI indices, call ordering, replay barriers, frozen-state/resource accounting, persisted-logit
recomputation, malformed records, per-order gates and six-order group construction.

These own tests explicitly use synthetic lookup models and substituted parent/factory/audit adapters.
They exercise the actual C257 run/probe/analyze/persisted-postcheck code, but are NOT learned-model
capability evidence, execution of the full parent import graph, real parent-artifact precheck, or
execution of3337 historical tests. Test21's constructed3338-ID fixture tests filtering only.
The parent writer/loader schema and final-state semantics were checked against actual C256 source;
the source coverage and runner counts were reviewed, but full inherited precheck remains required.

Reviewer environment:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No complete historical checkout or
user-local learned artifacts were available; GitHub DNS failed in the container and PowerShell
was absent. Windows System.Management.Automation.Language.Parser.ParseFile was NOT run here.
The standard command parses dispatcher; dispatcher parses selected launcher; launcher parses runner
before execution/logging. These checks remain mandatory in the user's environment.

Pending authoritative checks:Windows parser chain, actual388/635 parent/source protection precheck,
exact own24 in the user's environment, full3337 regression, ten real frozen checkpoint evaluations,
persisted postcheck and log publication. None is claimed complete by this authoring review.
Only this handoff activation follows the review. Use the final activation branch HEAD as ExpectedHead,
not the review target or C256 execution/log HEAD. Re-read final branch HEAD before issuing the command.

## Execution and stop

Use tools/invoke_active.ps1 with the registered final activation HEAD. The Formal state section has
exactly one ACTIVE token resolving to C257. The launcher fixes the accepted parent summary path:
runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.

Order:dispatcher/launcher/runner ParseFile -> Python compile + parent/order precheck -> own24 ->
focused3337 -> ten-model frozen order evaluation -> persisted postcheck -> log publication.
Operational wrong branch/dirty tracked tree/stale HEAD/stale ACTIVE skips happen before logging and
publish no experiment log. They are not scientific INVALID results.

A source/artifact/schema/identity/nonfinite/replay/test/count fault stops evaluation and retries C257
only after a minimal repair. Do not change seeds, thresholds, data or weights to obtain PASS.
A complete valid FAIL is accepted negative; it does not revoke C256's value-assignment PASS.
A log-only publication failure is repaired without rerunning completed science.
The user normally only sends 'finished'; fetch docs/experiment-run-logs/c257/latest.json and latest.log.
Do not move this branch with unrelated changes while the formal run/log publication is in progress.

Gate F remains NOT PASSED. Preserve all accepted source/tests/logs and tools/run_c167.ps1.
No paid API, external corpus, model expansion, production adoption, cleanup/history rewrite or CI work.
Judge C257 before C258.
