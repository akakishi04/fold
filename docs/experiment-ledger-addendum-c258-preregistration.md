# C258 preregistration — saved middle-slot attribution

Experiment:C258-v5b-saved-middle-slot-audit.
Stage:V5-B-SAVED-MIDDLE-SLOT-AUDIT.
C257 ACCEPTED VALID NEGATIVE; C256 ACCEPTED PASS in its original bounded scope.
Gate E PASSED; Gate F NOT PASSED. C259 NOT REGISTERED.

## One question and evidence status

Do saved novel-order errors concentrate on query b/乙 and select the middle-position distractor?
This is a descriptive diagnostic of already evaluated data. Aggregate C257 outcomes were inspected
before this plan; query-level output attributions have not been inspected. It is exploratory,
not independent confirmatory evidence. No hypothesis-support threshold or capability gate is set.
A diagnostic PASS means valid accounting/recomputation, not that a positional mechanism is proved.

C256 exposed b/乙 only as the middle fact; all four novel C257 permutations move it to first or
last. Three different assigned values let a scorer identify which displayed entity owns a wrong
digit. This attribution does not prove how the model internally represented or chose the answer.

## Accepted parent identity

Acceptance/base commit:ff34341a10e12b00091649e29c05b088e29a09db.
Acceptance:docs/experiment-ledger-addendum-c257-c258.md.
C257 execution:016785f35605a3eef5f94d42f0b86cb2fc4d9dfe.
Published log:4a322950685b80d7748aa525608555149c2c2ffd.
Publisher log SHA256:6932e3f178cfadb3434a34368a3ba674489b96b6dc509b2a69da18f6a36a66a5.
Summary SHA256:596df75ccc89c5a12c964c2e6be1fc689e5773f4c0a857f90fdcedd4df9b8816.
Path:runs/c257-v5b-unseen-order-705d486739b44a56bbed34fae66ace89/summary.json.
C256 summary:runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.

Required C257 artifacts:
-eval-outputs.pt:6911df9af7a10790cee9b18ff15a6b3479ca7e20046d5f6a16f95d69d068b92a.
-measurements.json:c37f98bbc13526f408b9b00adac16e90e23dc764d59ef4af1ef5e990b235eb22.
-order-dataset.json:9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
-order-plan.json:18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36.
-validation-summary.json:1d0d66a7550d47e34d01b5242c8ad0ef527ed7c36df66a440e31005609975d99.

The loader accepts the actual valid-negative C257 summary: status FAIL, candidate2/control0.
It must not require a capability PASS. It verifies all five artifact hashes and sizes, obtains the
C256 dataset/records through actual C257.load_inputs, and loads C257 eval-outputs.pt once per pass.
Archive schema fold-c257-order-eval-v1; records are ten final-state evaluations in seed/arm order.
C257.analyze(parts,novel,records,refs,C256) recomputes all original/novel/restored views, original
predictions/metrics, and restoration checks, then must match both accepted JSON files and summary.
C257 order-plan.json must equal actual C257.manifest(). No learned checkpoint is loaded.

## Changed and held constant

Only offline grouping/attribution changes. No input, weight, model inference, decision or target
is changed. All five seeds256001..256005, both arms, both languages and both original assignment
splits remain. Original two orders and novel four orders retain their accepted row identities.
TRAIN/HOLDOUT label original C256 assignments; neither is optimized or selected in this diagnostic.
Ground-truth assignments are used only by the offline scorer, never as model input.

Normal-view answers are attributed. Evidence/query-blind and restored logits are replayed by the
parent validator, not counted again as independent answers. Total normal answers8640:
known2880 + novel5760. Ten models x two splits x (144 known +288 novel).
Every seed/arm/split/language/permutation/query cell has12 assignments:720 cells.
Pooled query cells120:24 known and48 novel rows each. Middle-slot signatures40:one per
seed/arm/split/language. Both successful and failed seeds and both arms are retained.

## Exact attribution and contrasts

An answer is exactly one of:correct queried entity; other displayed entity; absent value in0..3;
other byte. The first two also identify the entity and its visible position. Repeated values are
rejected. A correct answer at the middle position is NOT a middle-position error.

For each query report known/novel counts and errors, including middle-position wrong answers.
For novel rows match the same assignment/language/query to BOTH known-order answers. Count
known-both-correct -> novel-wrong and known-not-both-correct -> novel-correct separately.

For b/乙 specifically report:
-known correct /24 and novel correct /48;
-b error rate minus pooled a/c error rate (a/c denominator96);
-middle distractor errors, other displayed distractor errors, absent-value and other-byte errors;
-middle hits / all b errors, and middle hits / in-assignment b errors;
-middle-minus-other displayed distractor count; known-both-correct -> novel-wrong count.
Zero denominators produce JSON null, never zero, an artificial success, or an exception.
Because b is never middle in the novel orders, the middle value is always a distractor for its
query. No causal conclusion or statistical independence is inferred from a positive contrast.
No result-driven cell selection, threshold adjustment, seed replacement or score rescue.

## Workload, outputs and fixed diagnostic gate

Model forwards0; model/state construction and strict loads0; learned bundle loads0; training0;
new learned checkpoint writes0. torch.nn.Module._call_impl is blocked during saved replay/analysis,
including reused parent helpers. The real path performs no factory/model-construction call.
One evaluation archive load per analysis pass:one scientific pass and one persisted postcheck,
therefore two across the formal diagnostic+postcheck. Parent-file hashing, regression fixtures,
serialization and all-view metric recomputation are additional work, not new scientific samples.

Five ignored outputs plus summary.json:
-audit-plan.json;
-row-attribution.json;
-query-position-cells.json (order/query cells and pooled query cells);
-signature-summary.json;
-validation-summary.json.

PASS iff parent identity/replay, full coverage, source/input preservation, no-model-call guard,
partition accounting and persisted re-attribution all pass. The direction or absence of the
middle-slot signature cannot fail or rescue this integrity gate. capability_pass_claim=False;
causal_mechanism_claim=False; production_adoption=False; gate_f_candidate=False.
A source/artifact/schema/nonfinite/identity/count/replay/test fault is INVALID / RETRY SAME C258.

## Protection and authoring quality

Inherit388 source pins/635 protected inputs; add accepted parent summary+five artifacts and OWN6:
394 source pins/647 protected inputs. Direct deciding dependency union34:five C231 LM sources,
C230..C257 benchmark/helper modules, plus this benchmark. Required count and subset checks remain.

OWN6:benchmark,own tests,runner,launcher,this preregistration,and design document.
-fold_lm/v05_benchmarks/model_c258_saved_middle_slot_audit.py
-tests_lm/test_v05_c258_saved_middle_slot_audit.py
-tools/run_c258.ps1
-tools/invoke_c258.ps1
-docs/experiment-ledger-addendum-c258-preregistration.md
-docs/v5b-saved-middle-slot-audit-v0.1.md

Own20;modules143;loaded3358/focused3357. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:a4f2cad192bd56dd73d867caf8453084cdd85e8e0f10f9d2496bfaa4a6c08aef.

Before activation, re-fetch committed bytes and match complete locally tested files to remote blob
identities. Run exact own20, compile/import and global binding audit; review actual parent writer/
loader signatures and archive semantics, integer denominators, manifest, source coverage, suite
counts and launcher argument order. Own tests use synthetic saved logits and explicit parent/audit
adapters, not learned models or the full historical import graph. Record checks and limitations in
the authoritative handoff. Windows ParseFile chain and full3357 remain required in user execution.

## Stop boundary

No accepted source/test/log changes, no new shared infrastructure, no model expansion, no paid API,
external corpus, cleanup, history rewrite or CI changes. No Gate F or production promotion.
C257 is not rerun or converted to PASS. This diagnostic ends after reporting all attributions;
any later training-distribution change must be a separately judged/preregistered experiment.
Use the active dispatcher. Repair log-only publication without redoing completed science.
Judge C258 before C259.
