# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C236 ACCEPTED VALID NEGATIVE. C237 ACTIVE / NOT YET JUDGED. C238 NOT REGISTERED.**
C237 is the unique ACTIVE experiment: a frozen signal-path diagnostic, not an ability/Gate F run.
C235 remains diagnostic-integrity PASS only; C234 remains ACCEPTED VALID NEGATIVE.
Post-authoring review is PASS. Authoritative execution prechecks and regression remain mandatory.

## Latest accepted evidence — C236

Scientific execution HEAD: `0bc91722ca27803f065d2458505b502a2d01e50f`.
Published log commit: `46e453a7e3900085002479791c6544b8669b9cf0`.
Log SHA256: `784bba560a4b9a9d168def96314ef9da36df4d9594d913ed526b1e0f297a92e8`.
Summary SHA256: `0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec`.
Local summary: `runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json`.

24 own tests PASS in1.675s;2833 focused tests PASS in60.430s.
262 source pins /382 protected inputs; C234 training-AST parity PASS.
Six models x400 steps:2400 total steps /76800 answer presentations.
2454 model forwards /77664 total row presentations. All replays and changed-weight checks PASS.
Tracked tree clean; execution HEAD preserved; run_execution_valid=True.

Every one of12 seed/family/language cells: accuracy50% (4/8), fact-pair0/4, query-pair0/4,
evidence-mask drop0, query-mask drop0. full_probe_gate=False; gru_probe_gate=False.
This recipe did not fit even the selected16 seen TRAIN prompts. It does not prove architecture-wide
impossibility. Unchanged accuracy does not imply unchanged predictions, hidden activations or logits.
The evidence is published run/postcheck evidence, not an independent rerun of user-local models.

Acceptance/artifact identities: `docs/experiment-ledger-addendum-c236-c237.md`.
Acceptance record commit: `7b626b9a3886117145d3c469dc41549119d9a9ab`.
Acceptance/handoff base: `eb2d5ed3cf6504b98152246f9583239427ea0fbc`.
Do not rerun or rescue C236. No ability/generalization/core-superiority claim or Gate F promotion.

## Preserved earlier evidence

C235: diagnostic-integrity ACCEPTED PASS; all12 complete TRAIN cells below90%, accuracy47.9167%-53.125%.
Full evidence: docs/experiment-ledger-addendum-c235-c236.md.
Its initial invalid attempt remains in docs/experiment-ledger-addendum-c235-execution-recovery.md
and immutable log commit1615b5ce54afed8bde44ac9d326cace6c6e674d0.
C234: ACCEPTED VALID NEGATIVE; contextual binding not demonstrated on held-out value pairs.
Full evidence: docs/experiment-ledger-addendum-c234-c235.md.
C233 remains ACCEPTED VALID NEGATIVE; C232 remains bounded template-byte learning only.

## Active C237 — frozen binding signal audit

Experiment: C237-v5b-frozen-binding-signal-audit.
Stage: V5-B-FROZEN-BINDING-SIGNAL-AUDIT.

One question: do factual/query changes remain numerically distinguishable through the frozen
C236 input/encoder/readout/logit path, even where the final selected answer fails to change correctly?

Changed: passive measurement instrumentation and derived descriptive contrasts only.
Held fixed: all six C236 final trained state dicts and fingerprints; original16 rows/order/targets;
both languages; normal/evidence-blind/query-blind renderings; Full/GRU-only architectures;
CPU float64, threads2 and deterministic algorithms. No training or architecture intervention.

Use the exact C234 evaluator plainly and with passive hooks. Capture actual GRU output at EOS,
readout_norm input/output, decoder input and logits. The captured normalized vector must equal the
actual decoder input; functional linear reconstruction must reproduce logits. Do not read a GRU
final state after PAD slots. Full pooled input is post-core; GRU-only pooled input is encoder EOS.

For each model/language separately report4 query-change pairs,4 assignment-swap pairs,4 fact-order
pairs, and8 normal-to-each-mask row contrasts. Query/assignment changes alter targets; order does not.
Measure token mismatches, exact equality and linf/l2/relative_l2 at four captured layers, unrestricted
256-byte argmax, correctness, digit-logit contrast, top-two gap and supplied-value probability mass.
Raw logit changes are not argmax changes; common logit shifts can leave probabilities unchanged.
There is no sensitivity threshold or post-hoc capability gate.

Fixed scientific workload:
-six frozen models x3 views x2 passes =36 full-model forwards /576 row presentations;
-18 separate functional decoder reconstructions (not extra model forwards);
-144 matched pairs +192 masked-row contrasts =336 total;56/model;
-12 seed/family/language diagnostic cells;
-zero training steps, optimizer steps, checkpoint writes or scientific network calls.

C237 PASS means diagnostic integrity only: exact parent prediction replay, parent metric and
plain/captured logit/metric agreement within1e-9, unchanged final fingerprints, decoder reconstruction,
fixed workload, source/artifact protection and persisted-trace/contrast replay. Observed sensitivity
or accuracy never controls this PASS. A fault is INVALID / RETRY SAME C237.
No C236 verdict change, general language, unseen generalization, causal module blame or Gate F claim.
Masks can change byte length/EOS; cross-layer scales differ. These are descriptive, not causal effects.

Protection:268 source pins /394 protected inputs; direct dependency union13; OWN6.
Own tests24; modules122; loaded2858/focused2857 with only the inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored local outputs: diagnostic-plan.json, traces.json, contrasts.json, diagnostics.json,
validation-summary.json. No new model/checkpoint is saved. Postcheck verifies hashes/sizes and
rebuilds contrast summaries and predictions from persisted tensors without extra model forwards.

Manifest SHA256: `1e5ab23f80a3cf2b510ce82bdd9f343b53716a6dc9641eb9b09ae6dd165c06ce`.
Design: `docs/v5b-frozen-binding-signal-audit-v0.1.md`.
Registration: `docs/experiment-ledger-addendum-c237-preregistration.md`.
Preregistration commit: `eac3e5085cb7936ba38a79a8e8c6300ce520d727`.
Use tools/invoke_active.ps1 with the final activation/handoff branch HEAD returned with the command,
not the C236 execution HEAD and not the preregistration HEAD before activation.

## C237 post-authoring review

`post_authoring_review = PASS`

Review HEAD: `eac3e5085cb7936ba38a79a8e8c6300ce520d727`.
Scope: authoring/instrumentation review, not a formal result on the accepted C236 checkpoints.

After all six OWN files were committed, all six were re-fetched from this immutable review HEAD.
Reviewed Git blobs:
-benchmark: `8faa0a98900e004503542b7025e63b7dcbb41fd2`
-tests: `d9898f90849453040b808480ead131aa51efae5a`
-runner: `526d57121fa03d98bffcd4614ac9a42ae5265a04`
-launcher: `c33bc231f04fc37916e07304e45d1c9a0b38b24c`
-preregistration: `2933eeff4d8469313caf1529e40ed71c01bdc09f`
-design: `d2848b6dac1857a1b2c7c5cd9dbb761506a33a3d`.

Comparison from acceptance baseeb2d5ed3 to review HEAD changes exactly the six OWN additions.
No accepted source/test/log or shared launcher is changed. The synthetic reader was changed to
explicit UTF-8 before this review, rather than depending on the Windows locale. All four code/script
remote blob identities were mechanically matched to the reviewer-local bytes used for final tests.

Checks actually executed after remote readback:
-UTF-8/NUL checks and Python compile/import of complete new source/test modules;
-all24 own tests PASS in1.154s, including own unittest loader count/unique IDs;
-manifest digest exactly matches registered SHA; reconstructed16-row fixture matches accepted hash;
-free-global/import binding audit reports zero unresolved names in both new modules;
-passive capture/output equivalence, correct EOS selection, hook cleanup on failure, frozen-mode
 rejection, nonfinite rejection and post-decoder modification rejection on synthetic models;
-exact versus1e-12 nonzero contrasts and independent raw-logit/argmax behavior checks;
-query/fact/order pairing and all144+192 contrast count contracts;
-actual six-model run function and persisted artifact verification exercised with synthetic models
 and substituted parent loader/protection adapters; verifies loader dispatch,36 forwards, outputs,
 trace/contrast recomputation and wrong execution-HEAD rejection;
-three embedded runner Python blocks compile; precheck argv1 and postcheck argv1/2/3 checked;
-source AST checks no fit/backward/step/zero_grad/torch.save/torch.optim execution path.

Parent C236 writer/bundle source, C234 evaluator/renderer, C233 GRU-only readout and the real language
model source were read for schema and timing semantics: final_probe/final_sha256 refer to trained
states; all normal/masked predictions are replayed; EOS is chosen before PAD; captured pooled
vectors are the real normalization inputs. The scientific path calls the C237 loader and the
actual parent evaluator; toy-fixture helpers are only in tests.

Runner and launcher review verifies branch/tree/ExpectedHead/ACTIVE guards before logging,
PowerShell ParseFile before invocation, argument ordering, fixed local parent path and C237-only
log publication. Source protection covers the13-module direct dependency union.
Historical counts are based on accepted C236121 modules/2834 loaded plus the new24-test module:
122 modules/2858 loaded, with the same one exclusion giving2857. Full historical suite construction
and execution were NOT performed in the isolated reviewer environment.

Reviewer environment: Python3.13.5 / PyTorch2.10.0+cpu / NumPy2.3.5, isolated package scaffolding,
not the user's Windows installation or a complete checkout. A clone attempt could not resolve
github.com. NOT executed here: Windows PowerShell AST, full2857-test historical regression,
accepted user-local artifact precheck or the scientific diagnostic on the six accepted C236 models.
None of those pending checks is represented as PASS. They remain mandatory in the unchanged
ordered launcher/runner path before any C237 result may be accepted.

Only this unpinned authoritative handoff changes after review HEAD. Re-read the final handoff and
verify final branch HEAD before returning ExpectedHead to the user.

## Numeric-memory track and stop

C230 route remains optional; numeric-memory tuning stays paused. Gate F is not waived.
Preserve accepted sources/tests/logs and tools/run_c167.ps1. No cleanup/history rewrite, paid API,
external corpus, larger model or production runtime change.
24 own tests ->2857 focused tests ->C237 frozen audit ->artifact/trace postcheck ->remote log publication.
Stop same C237 on execution/integrity faults. Repair log-transport-only failure without rerunning a
completed scientific diagnostic. Judge C237 before C238 registration.
