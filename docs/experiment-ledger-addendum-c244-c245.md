# C244 acceptance and C245 selective-evidence boundary

## Formal verdict

**C244 ACCEPTED VALID NEGATIVE.** C243 remains diagnostic-integrity PASS; C242 remains a valid negative.
Gate E PASSED; Gate F NOT PASSED. No retraining, threshold rescue or replacement seed is authorized for C244.

Scientific execution HEAD: d89007bc5a04c4f6b99bff966093b0e14174e04b.
Published log commit: d1e2933492cf4f4d0cbfb535c80b800c58bcadf7.
Publisher-recorded log SHA256: fad665eeb8a89322079f21425b89ae28336567574a47043b10a479303780b158.
Log bytes: 578100.
Summary SHA256: a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297.
Local summary: runs/c244-v5b-two-partner-recombination-63a64987412a494291853ed0afb9c639/summary.json.

The publication commit follows execution by one commit and changes only c244/latest.log/latest.json.
Acceptance uses immutable retrieved log ranges, publication metadata and recorded local postchecks,
not an independent full-log byte rehash or reviewer rerun of the user's checkpoints.

## Execution validity

24 own tests PASS in6.544s;3025 focused tests PASS in134.647s.
310 source pins/478 protected inputs. All6 models completed400 updates, with block_updates=[200,200].
2400 training steps/76800 training presentations/2490 model forwards/81408 total row presentations.
Checkpoint/prediction replays, weight updates, protected inputs and common-HOLDOUT comparator passed.
Tracked tree clean; execution HEAD preserved; run_execution_valid=True.
Scientific status FAIL; full_two_partner_gate=False; gru_two_partner_gate=False.
cell_outcomes={RECOMBINATION_MISS:12}. All twelve full TRAIN criteria passed.

## Deciding measurements

All TRAIN cells:32/32 normal answers and16/16 fact/query/order pairs. Evidence drop0.75;
query drop0.50-0.59375. TRAIN answer NLL0.001237-0.003094 at printed precision.
HOLDOUT correct answers, out of16 per language (C242 same rows -> C244):

| Seed | Full EN | Full JA | GRU-only EN | GRU-only JA |
|---:|---:|---:|---:|---:|
|234001|2 -> 7|3 -> 8|7 -> 7|7 -> 8|
|234002|6 -> 2|6 -> 5|7 -> 6|7 -> 7|
|234003|6 -> 8|6 -> 9|3 -> 6|5 -> 7|

HOLDOUT accuracy12.5%-56.25%, below90% in every cell. All paired gates also miss overall.
Query-pair both-correct counts Full EN/JA:0/0,0/1,3/2 out of8 per cell;
GRU-only EN/JA:2/4,0/0,0/1 out of8. HOLDOUT NLL2.980051-7.039740.

Identical-row comparator:7 cells improve,2 tie,3 worsen. Pooled correct answers65/192 ->80/192
(33.8542% ->41.6667%). This pooled descriptive count does not treat rows as independent training
replicates and is not a significance test, universal improvement or a Full/GRU ranking.
Do not compare the current32-row HOLDOUT against the old64-row average.

## Interpretation and limits

The expanded two-partner TRAIN set is fitted, but generalization to the remaining pairs still
fails. The intervention did not establish robust binding under the fixed recipe. Improvements
are not uniform across seeds/languages. Coverage, repetition and alternating-block dynamics
changed together; the results do not uniquely identify partner multiplicity as the cause.

Perfect TRAIN fitting and sensitivity to hiding BOTH values do not reveal how much the model
uses the queried entity's value versus the other entity's value. C243 audited the older C242
answers, not these C244 checkpoints. Do not transfer that older error mechanism as an established
fact about C244. Exact current error categories require fresh analysis of its outputs.

## Accepted artifacts

- measurements.json: cd0fba1897aea554a74b984622f97fa93399baadda4fff5a757e1bfdbd24239d (20836 bytes)
- split-dataset.json: e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346 (15904 bytes)
- trained-models.pt: 90c367dc4026e757ed561af75a25d529d37dd9fea404d4d6370f1bac5211b519 (601940 bytes)
- two-partner-plan.json: e89a41c15ef3d702c7009a9b4fc22f4e28809dea3892c5d63cf02120a1e10b0b (2670 bytes)
- validation-summary.json: b80fea969f5329fc401c0be3470233ae50dd55319b3a83c0e0047a5fe4c0808f (354 bytes)

## Next question, not registration

Freeze all six C244 final checkpoints. How do their answers and scores change when only the
queried entity's value is hidden, compared with hiding only the other entity's value?
Keep exact TRAIN64/HOLDOUT32 and replay the three original views first. For the two new views,
replace exactly one factual ASCII digit with '?', preserving names, order, query and byte length.
No new training, model expansion, answer correction or checkpoint selection.

This measures behavior under controlled input erasure, not a unique internal mechanism. The
single-value masks were not part of training; distribution shift and redundant information must
be disclosed. In particular, the held-out pairs have a one-to-one partner relation, so the correct
value can be inferred from the other value by an oracle that knows that distribution. Do not
interpret masked-input accuracy as proof of direct reading or as a capability gate.
Separate C245 preregistration and committed-byte review control activation. C246 is not registered.
