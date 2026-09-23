# C237 preregistration — frozen C236 binding signal audit

Experiment: C237-v5b-frozen-binding-signal-audit.
Stage: V5-B-FROZEN-BINDING-SIGNAL-AUDIT.
C236 ACCEPTED VALID NEGATIVE; C235 diagnostic-integrity PASS only; C234 ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED. C238 is NOT REGISTERED.
C237 is registered by this document. The authoritative handoff controls unique ACTIVE state and
readiness only after independent post-authoring review.

## One scientific question

With all six accepted C236 final models frozen, are factual/query changes numerically
 distinguishable at the input, encoder EOS state, pooled/normalized readout and output logits,
even where the final selected answer fails to change correctly?
No causal attribution, additional learning or capability threshold is part of this diagnostic.

## Accepted parent and identity

Acceptance record: docs/experiment-ledger-addendum-c236-c237.md.
Acceptance record commit: `7b626b9a3886117145d3c469dc41549119d9a9ab`.
Acceptance/handoff base: `eb2d5ed3cf6504b98152246f9583239427ea0fbc`.

C236 scientific execution HEAD: `0bc91722ca27803f065d2458505b502a2d01e50f`.
Published log commit: `46e453a7e3900085002479791c6544b8669b9cf0`.
Log SHA256: `784bba560a4b9a9d168def96314ef9da36df4d9594d913ed526b1e0f297a92e8`.
Summary SHA256: `0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec`.
Local summary: `runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json`.
The parent must be execution-valid with status FAIL and full_probe_gate/gru_probe_gate False.
Do not require a scientific parent PASS for this diagnostic.

Required byte-identical C236 artifacts:
- measurements.json: 19d24911d53e08898324514fedaafc32f27168f1526f9958b1572481cf957971
- probe-dataset.json: bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c
- probe-plan.json: 86f534a54964a31d0139d5a3ceb3ef4b5e3c2ab46667adb002390a5b5d347957
- trained-models.pt: 90c711f1609b77d426395446e9e7757b2a897c6e2372322fabe3c16cf5f6fc45
- validation-summary.json: a1e46ad4b0373daf6c1a920edc1ec8b7be5f9ab7f6c56490a9baa89062232042

Load the C236 bundle only through C236.load_bundle: schema fold-c236-minimal-binding-v1, ordered
identities and six state dicts. Identity order is234001/full,234001/gru_only,234002/full,
234002/gru_only,234003/full,234003/gru_only.

C236 measurements are adapted with required final_probe, predictions, final_sha256,
checkpoint_roundtrip, prediction_replayed, weights_changed, reload_max_error and replay_metric_error.
C236.validate_metrics checks final_probe; C236.summarize must reproduce the accepted summary.
The writer source establishes final_sha256 as the trained final state, not initial_sha256.
C237 uses that final state and does not use C234 before-training fingerprints as checkpoints.

## Changed and held constant

Change only measurement instrumentation and derived descriptive contrasts.
Keep the exact16 C236 TRAIN rows and order, both languages, both assignments, fact orders, queries,
normal/evidence-blind/query-blind rendering, target bytes and unconstrained256-byte output scoring.
All six accepted trained checkpoints, Full/GRU-only architectures, CPU float64, threads2 and
deterministic algorithms remain fixed. No model expansion, new train data, optimizer, backward
pass, gradient update, checkpoint write, seed replacement, checkpoint choice or production change.
Fresh model objects are only containers for strict loading of every accepted state dict key.

## Capture and passive replay contract

Use C234.evaluate once plainly and once with passive capture hooks, each scoring all three views.
Root model hooks count actual calls and row presentations. Internal capture hooks must not return
replacement outputs and must be removed even when an evaluator raises.

Capture local_encoder output at the actual EOS, readout_norm input (pooled), readout_norm output,
and decoder input. Norm output must equal the real decoder input. Persist tokens, GRU EOS,
pooled, normalized readout and logits. GRU EOS/pooled/readout shapes are16x16; logits16x256;
tokens16x48. All floating captures must be finite CPU float64.

Validate BOS257, EOS258 and PAD256 with a contiguous prefix; EOS must be the final non-PAD slot.
Do not use the GRU final hidden state after PAD processing. Full pooled vectors originate after
its iterative core; GRU-only pooled vectors originate directly from its causal encoder.

Require exact parent/plain/captured argmax predictions for all three views. Require parent final
metric replay and plain/captured raw-logit and metric agreement within1e-9. Independently compute
F.linear(captured_readout, decoder.weight, decoder.bias) and require output agreement within1e-9.
Require accepted final fingerprints before capture and unchanged fingerprints afterward, eval mode,
requires_grad=False and no parameter gradients. Capture adds no training or model modification.

## Fixed comparisons and descriptive measurements

For each model and language, form4 pairs of each kind:
- query: same facts/order, changed queried object and target;
- facts: same objects/order/query, swapped0/1 assignments and target;
- order: same assignment/query/target, reversed fact order.

Also compare every row's normal trace with each of the two masked traces. Masks can change
prompt length and EOS position. Their changes are not isolated semantic interventions.

Each contrast records token mismatch count; exact equality, linf, l2 and relative_l2 for GRU EOS,
pooled, normalized readout and logits; both unrestricted argmax predictions and correctness;
signed logit(1)-logit(0); top-two logit gap; probability mass on the two supplied values.
Relative_l2 denominator is max(norm(left),norm(right)), with0 when both norms are0.
Use exact equality, not an arbitrary small-distance cutoff. Replay tolerance1e-9 is an integrity
bound, not a sensitivity or ability threshold. Report raw logits separately from digit-logit
contrast and argmax, since a common logit shift can leave all probabilities unchanged.

## Workload and diagnostic gate

Six models x3 views x2 passes =36 full model forwards /576 presented rows.
18 separate functional linear reconstructions. These are algebra checks, not extra model forwards.
144 paired contrasts (6x2x3x4) and192 masked-row contrasts (6x16x2):336 total,56/model.
12 seed/family/language diagnostic cells. Training steps0, optimizer steps0, checkpoint writes0,
scientific network calls0. Authoring synthetic-test work is outside these scientific totals.

C237 status PASS means diagnostic integrity only: accepted parent identity, all replays,
passive instrumentation, unchanged weights, full fixed workload, all diagnostic cells,
protected sources/artifacts and replay of persisted traces/contrasts.
Observed accuracy or sensitivity does not determine PASS. Any source/artifact/schema/nonfinite/
mutation/replay/workload defect is INVALID / RETRY SAME C237. No C238 registration until judgment.
No C236 verdict change or Gate F promotion even when C237 passes.

## Protection and regression

Inherit C236262 source pins /382 protected inputs. Add parent summary and five artifacts (6),
then OWN6 source files:268 source pins /394 protected inputs. Parent summaries/artifacts already
in inherited protection are not double-counted. Every deciding-path direct dependency is pinned.
Direct union13: five C231 LM_SOURCES plus C230/C231/C232/C233/C234/C235/C236/C237 entry points.

OWN6:
- fold_lm/v05_benchmarks/model_c237_frozen_signal_audit.py
- tests_lm/test_v05_c237_frozen_signal_audit.py
- tools/run_c237.ps1
- tools/invoke_c237.ps1
- this preregistration
- docs/v5b-frozen-binding-signal-audit-v0.1.md

Own tests24; modules122; loaded2858/focused2857. The one inherited exact exclusion remains:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Use actual unittest loader/suite counts and unique test IDs. No parent test/file is altered or
new historical test excluded. Preserve all accepted logs/sources and tools/run_c167.ps1.

## Output and postcheck

Five local-only artifacts under ignored runs/: diagnostic-plan.json, traces.json, contrasts.json,
diagnostics.json, validation-summary.json. No model/checkpoint is written by C237. Summary.json
contains source/input identities, artifact hashes/sizes and integrity summary. Traces retain all
three views and all captured layer values; diagnostics include metrics, fingerprints and12 cells.

Postcheck verifies every hash/size, parent/source identity, summary and plan; reconstructs tensors
from persisted traces using explicit dtypes; verifies tokens against the actual parent renderer;
recomputes all contrasts/cell summaries and predictions; and compares them with saved records.
This postcheck has no additional model forward. Console diagnostics and publisher receipt alone
are mirrored to docs/experiment-run-logs/c237/latest.log and latest.json.

Manifest SHA256: `1e5ab23f80a3cf2b510ce82bdd9f343b53716a6dc9641eb9b09ae6dd165c06ce`.

## Authoring and execution review

After all six files are committed, re-fetch their bytes, verify code/script blob identities against
locally tested bytes, rerun own tests, compile/import, check free-name bindings and manifest/count/
parent schema contracts. Review the actual call ordering, frozen-model flags, passive hook return
behavior, EOS indexing and decoder reconstruction. Test synthetic successful capture, failure
cleanup, hidden postprocessing rejection and the six-model run plus persisted-artifact postcheck.
Synthetic artifact readers must use explicit UTF-8, including on Windows.

These authoring tests are not the formal run on accepted checkpoints. Record actual checks and
remaining limitations with post_authoring_review and review HEAD in authoritative handoff.
Windows PowerShell AST and the full2857 historical regression are not reported PASS without execution.

Execution order: outer dispatcher ParseFile -> selected launcher ParseFile -> runner ParseFile ->
Python compile and source/artifact precheck ->24 own tests ->2857 focused tests -> frozen audit ->
artifact/trace postcheck -> remote log publication. Branch/tree/HEAD/ACTIVE mismatches skip before
scientific execution/log publication. Repair transport-only failure without rerunning a completed
scientific diagnostic. Do not bypass any preflight to obtain a result.

## Non-claims and stop

Signal sensitivity is neither learned binding nor causal attribution. Exact equality at one
sampled layer does not prove architecture-wide impossibility. Cross-layer vector norms are not
causal effect sizes. Constant accuracy does not prove identical predictions or identical logits.
No useful-language, unseen-generalization or Full/GRU superiority claim. Gate F remains NOT PASSED.

No extra training, larger model, external corpus, paid API, cleanup/history rewrite, numeric-memory
retuning, threshold rescue or automatic next experiment. Judge C237 before C238 registration.
