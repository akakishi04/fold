# C254 acceptance and C255 fixed-query value-swap boundary

## Formal verdict

**C254 ACCEPTED PASS — diagnostic integrity only.**
C252 remains ACCEPTED VALID NEGATIVE; C253 remains diagnostic PASS. Gate F NOT PASSED.
No learned capability improvement, production adoption, or training-time core necessity is claimed.

Scientific execution HEAD:4e6e5abf5a6a3c97e784868b9fc5e016fc1cf77c.
Published log commit:4fb92919e1da8146fcfe14d779f6b5a91008316a.
Publisher log SHA256:8f13b86ea18c7522170046bf6a70e49f7d334b2d5dca74c8261d007f089901e3.
Log bytes:656074.
Summary SHA256:96f0a3eaafbf0b9fc62e7e9f789344eac45497b2679662525ea54993803535f5.
Local summary:runs/c254-v5b-paired-residual-e324dc81a0364f92820cf8da7f3a0172/summary.json.
The publication is one commit after execution and changes only c254/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges, metadata, and recorded local postchecks, not an
independent whole-log byte rehash or actual checkpoint rerun by the reviewer.

## Validity

24 own tests PASS in3.084s;3265 focused tests PASS in231.431s.
370 source pins/599 inputs protected. All five models,120 head evaluations/5760 head rows.
Full-model/encoder/core/reader forwards0;training0;checkpoint bundle loads1;strict state loads5;
new learned checkpoint writes0. Intact/restored logits and query-blind negative control replay PASS.
Weights preserved;persisted paired-swap output replay PASS;tracked tree clean;execution HEAD
preserved;run_execution_valid=True. The scientific gate is diagnostic integrity,not performance.

## Deciding outcomes

HOLDOUT exact correct counts, EN/JA, denominator16 per language:

| Seed | Self | Order swap | Query swap |
|---:|---:|---:|---:|
|250001|16,16|16,16|16,15|
|250002|9,9|8,7|3,2|
|250003|16,16|16,16|8,8|
|250004|15,16|15,15|11,11|
|250005|16,16|16,16|12,10|

HOLDOUT totals:self145/160,order_swap141/160,query_swap96/160.
TRAIN totals:self320/320,order_swap319/320,query_swap212/320.
Query-swap HOLDOUT:50 correct-to-wrong,1 wrong-to-correct,61 total answer flips.
Order-swap HOLDOUT:7 correct-to-wrong,3 wrong-to-correct,10 total answer flips.
Query-swap donor-target matches21/160,so errors do not generally amount to copying the donor answer.
Query swaps reduce HOLDOUT accuracy in9 language cells and leave250001 EN unchanged;order swaps
reduce3 cells and leave7 accuracy counts unchanged. Query-swap NLL increases in all10 HOLDOUT cells.
The two mode comparisons share five models and the same tiny task;no independent-sample or
significance claim. The early conversational total94 was an arithmetic error, corrected to96
before this acceptance record; the per-cell source values and formal judgment never changed.

## Interpretation and limitations

With recipient reader vectors fixed, changing the donor query has substantially greater effect
than changing only fact order on these frozen states. This supports query-specific dependency in
the residual/read combination, beyond the effects observed for that order control.
It does not prove that the residual contains the correct bound value, distinguish a query-name
signal from a value-assignment signal, or identify a unique semantic algorithm. Feature combinations
are off the training distribution and LayerNorm/co-adaptation remain possible contributors.
Not all wrong answers follow the donor target. C252's original seed failure is not repaired.

## Accepted artifacts

- contrasts.json:562e6fae59bd1cb79dcefd1191445277d53735c2bec1ee1cbfc08726cd5b80b2 (10474 bytes)
- diagnostics.json:2c98ffc583768f43aa3311d7164828163888da19f18594d36ce49840b75990e2 (20366 bytes)
- head-outputs.pt:ad4bfefa0380323fb5c408c1f9de4778d2e04c09637bae44049efb7df5f2d5a1 (11831621 bytes)
- swap-plan.json:cfbf05fc55fe6c87a0b738bfab7f4c676bb75ed503883cb399898f7936641276 (2239 bytes)
- validation-summary.json:f204facbb500f7bc43db578e39231c8c2bc39dd07c7c399dcbef1de3ca3b9d95 (460 bytes)

## Next question, not registration

Keep the query name and fact order fixed, but swap the two entity-value assignments in the donor.
Does replacing only the residual with that donor's saved residual change recipient answers?
This supplies the complementary value-assignment intervention to C254's query intervention.
Reuse all five C252 learned states and C253 saved components. No new learning or full-model forward.
Use self, residual-only fact swap, coherent fact swap of BOTH residual and read, and restored self.
Coherent swaps are a replay control:they must reproduce the original donor logits,not necessarily
the recipient's target. Evidence-blind fact swaps must leave the outputs unchanged because paired
masked inputs coincide. Compare new residual-only effects to the immutable C254 query/order effects.

A coherent control is not a learned ability gain or an answer repair. This remains a bounded
frozen-feature dependency analysis;after these question/value contrasts, avoid extending this
same microtask diagnostic chain without an explicit next decision. Separate C255 preregistration
and committed-byte review are required before activation. Judge C255 before C256.
