# C238 preregistration — complete-cohort sampler intervention

Experiment: C238-v5b-complete-cohort-sampler.
Stage: V5-B-COMPLETE-COHORT-SAMPLER.
C237 ACCEPTED PASS for diagnostic integrity only; C236 remains ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED. C239 NOT REGISTERED.
C238 is registered by this document. The authoritative handoff controls activation/readiness only
after the committed source has passed independent post-authoring review.

## One scientific question

Does presenting every one of the fixed16 TRAIN rows twice per update, instead of sampling32 with
replacement, permit minimal TRAIN fitting under otherwise unchanged C236 conditions?
The sampler is a hypothesis, not a cause established by C237's observed numerical sensitivity.

## Accepted evidence and parent contracts

Acceptance record: docs/experiment-ledger-addendum-c237-c238.md.
Acceptance commit: 4794376d53aba9e01c780b8569f1db75f64ca952.
Acceptance/handoff base: 6c3d4150f42cd43592b5c5a1ef1c18dab9396270.

C237 scientific execution HEAD: 2dec1314181d62fbdf0a7d4c52007a9360921fd2.
Published log commit: f59b0012e488978f5733c4e8669eabc74ae47ad6.
Log SHA256: f4f6328ca74d96f21ee498da3d1d06f2e754d2abb70a51f0a15a0eccc22361db.
Summary SHA256: 056fcbe4ebd2f888c0d5d5aa2761a18cd4229ed4af428e8e298d7af3abf55b32.
Local summary: runs/c237-v5b-frozen-signal-audit-8dbdc04fdad84f49b41a78388ad0b7fb/summary.json.
C237.validate_result must accept that exact summary and its execution identity must match.

Required C237 artifact SHA256 identities:
- contrasts.json: 3449be022b490fb8c67bf47f688e68d9d7b277e235399e671acc2f61aebcb85f
- diagnostic-plan.json: 1e5ab23f80a3cf2b510ce82bdd9f343b53716a6dc9641eb9b09ae6dd165c06ce
- diagnostics.json: 87c37f0b645b0740cd2202c6d85a56a4d1164c5580c6eaa04036501f83627b70
- traces.json: eee07984fb62d83d1114ffa9476ab410257646dcb61a9c8096c21eb15a0063e0
- validation-summary.json: 066206986d83833a759d1e36d8d1efd5aab4b95c0693b32c3935b1d9baf06d9f

The accepted C236 comparator is already included in inherited source/input protection:
Execution HEAD: 0bc91722ca27803f065d2458505b502a2d01e50f.
Summary SHA256: 0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec.
Local summary: runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json.
C236.validate_result must accept this exact negative summary. It is not required to be PASS.

Load C236 probe-dataset.json and measurements.json, not C237 trace vectors as new model inputs.
The C237 parent-record adapter validates C236 final_probe/final_sha256/predictions/replays;
C236.summarize must reproduce the accepted validation summary. A C238-specific adapter additionally
validates initial_sha256 and initial_probe and all12 recorded C23650%/zero-pair/zero-drop cells.
The initial fields are BEFORE C236 training, as verified from its writer; final fields are after.
C238 initializes fresh, matches the initial fields and compares against the unchanged final metrics.
It never loads a trained parent checkpoint as the starting model. Historical artifacts remain intact.

## Fixed cohort, intervention and constants

Cohort SHA256: bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c.
Same16 C236 TRAIN rows in the same order. Two assignments x two fact orders x two queries x
English/Japanese. Eight rows per language. Same target bytes, renderer and three existing views.

Single intervention: replace C236's per-step `torch.randint(..., generator=sampler)` ids assignment
with `balanced_indices(len(train_targets))`, returning0..15 repeated twice. Every row appears twice
per batch and800 times/model over400 steps. Each batch has16 of each target byte and balanced joint
factor combinations. It is a complete-cohort policy, not an isolated manipulation of label balance.

An executable AST audit permits only this assignment and the progress tag to differ from C236.fit.
Constants STEPS/BATCH/LR/CLIP/TOL must match. The unused CPU sampler-generator construction is retained
for exact comparison and has no sampling effect. No loss reweighting or average-loss change.

Seeds234001,234002,234003, ordered seed/full then seed/gru_only. New Full13488/GRU-only10160 models;
width16,48 slots, same byte vocabulary and unrestricted256-way answer argmax. Full's common-weight
GRU-only copy is made before either paired model trains. Match C236 initial fingerprints exactly and
initial metrics within1e-9. Use AdamW lr0.005, betas(0.9,0.999), eps1e-8, weight_decay0, clip norm1.0,
batch32 and400 steps per model. CPU float64, threads2, deterministic algorithms.

No continued learning from final checkpoints, early stop, step extension, favorable seed replacement,
new data, architecture expansion, changed optimizer, external model or production runtime change.

## Fixed workload, gate and interpretation

Six fresh models x400 steps =2400 new training steps /76800 answer presentations.
Each model has3 initial +3 final +3 checkpoint-replay forwards over16 rows:54 evaluation forwards,
864 evaluated rows. Total2454 full-model forwards /77664 row presentations.
One new checkpoint bundle with six states. No comparator retraining/forward, no held-out evaluation,
and zero scientific network calls. Synthetic test work is separate from these scientific totals.

Primary gate: every Full seed/language cell must satisfy the unchanged C236 conditions:
exact accuracy>=0.90, fact-pair both-correct>=0.80, query-pair both-correct>=0.80,
normal-minus-evidence-blind accuracy>=0.35, normal-minus-query-blind accuracy>=0.35.
With8 rows and4 pairs per language, the exact and paired thresholds require8/8 and4/4.
Reuse C236 metric/gate functions. GRU-only gate is independent and cannot substitute for Full.
Record the candidate metrics, frozen C236 final metrics and descriptive accuracy difference.

A valid Full miss is status FAIL / ACCEPTED VALID NEGATIVE, not a reason to rerun or loosen gates.
A valid Full pass is bounded to fitting16 seen TRAIN prompts; memorization is not ruled out.
Either outcome leaves C236/C237 verdicts and Gate F unchanged. The experiment does not establish
held-out generalization, useful language, full/GRU superiority or the unique cause of past failure.
Complete-cohort sampling jointly changes coverage, balance and stochastic-gradient variability.

Execution requires exact initial fingerprints, initial metric replay, weight changes in every model,
non-mutating evaluation, actual call/row counters, strict six-state save/reload, exact final prediction
replay and raw-logit/metric error<=1e-9. Test, schema, nonfinite, source, artifact, replay, initialization
or workload failure is INVALID / RETRY SAME C238.

## Source protection and tests

Inherit C237268 source pins /394 protected inputs. Add C237 summary plus its five artifacts (6)
and OWN6 source files (6):274 source pins /406 protected inputs. C236 summary/artifacts are already
protected and must not be counted again. Every actual deciding-path direct dependency is pinned.
Direct union14: five C231 LM_SOURCES plus C230/C231/C232/C233/C234/C235/C236/C237/C238 entry points.

OWN6:
- fold_lm/v05_benchmarks/model_c238_complete_cohort_sampler.py
- tests_lm/test_v05_c238_complete_cohort_sampler.py
- tools/run_c238.ps1
- tools/invoke_c238.ps1
- this preregistration
- docs/v5b-complete-cohort-sampler-v0.1.md

Own tests24; modules123; loaded2882/focused2881. Only inherited exact historical exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Actual unittest loaders and unique IDs enforce counts. No accepted parent file/test/log is changed.

## Artifacts and postcheck

Five generated local-only artifacts under ignored runs/: sampler-plan.json, probe-dataset.json,
trained-models.pt, measurements.json, validation-summary.json. Checkpoint schema
fold-c238-complete-cohort-v1, identities in registered order, six state dicts.
Measurements retain initial_probe/final_probe, initial/final fingerprints, fit, predictions,
replays, workload and comparator_final. Summary contains source/input IDs and artifact hashes/sizes.

Postcheck verifies source/input/output identity, plan/cohort, recomputed summary, unchanged recorded
C236 comparator_final, and initial fingerprint/metric agreement. It runs no new model forwards.
Only console log and receipt are mirrored to docs/experiment-run-logs/c238/latest.log/latest.json.

Manifest SHA256: ae9d0b7e92ee7024b57210f1779aebbfc0757fa995acbdf6f9359b2f23664232.

## Review and execution boundary

After all OWN files are committed, re-fetch them at a fixed review HEAD and verify their Git blobs
against locally checked bytes. Run24 own tests; compile/import; check manifest and cohort digests;
validate parent writer semantics, actual loader dispatch, fresh/common-copy ordering, sampler-only
AST delta, declared counts, free-name bindings, embedded Python and PowerShell argument ordering.
Synthetic six-model run plus persisted postcheck are authoring checks, not scientific capability.
Record actual checks and limitations in the authoritative handoff before activating C238.

Order: dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile -> Python compile ->
source/artifact/sampler precheck ->24 own tests ->2881 focused tests ->C238 probe ->postcheck ->log push.
Branch/tree/HEAD/ACTIVE mismatch skips before execution/publication. Do not represent Windows AST,
full historical regression or local parent artifact checks as passed until actually executed.

## Stop

Gate F NOT PASSED; numeric-memory tuning paused. No cleanup/history rewrite, paid API, external
corpus, larger model, C236 rescue or unregistered next run. Preserve tools/run_c167.ps1 and all
accepted evidence. Stop same C238 on an integrity fault; fix transport-only failure without retraining.
Judge C238 before C239 registration.
