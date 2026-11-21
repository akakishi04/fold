# C247 acceptance and C248 readout-pilot boundary

## Formal verdict

**C247 ACCEPTED VALID NEGATIVE — primary normal-budget TRAIN sufficiency not established across all cells.**
Gate E PASSED; Gate F NOT PASSED. C246/C244 remain valid negatives. No earlier verdict is changed.

Scientific execution HEAD:6705aa76bf70ec2685100c47e1abe9cec3625523.
Published log commit:539bdb7860f1a9a5d59046c43d006c9989b636d9.
Publisher-recorded log SHA256:65402c6ffeb4147e71b3ca1228b4a761e391676d550aef2c7e0cf3908e06150c.
Log bytes:598978.
Summary SHA256:2f77f23ee7b77016ad44e1900b7396bbe07855e13429adc32cded0d0276ce404.
Local summary:runs/c247-v5b-normal-exposure-a3cec4a219a14360bac90cf8d7303da5/summary.json.

The publication is one commit after execution and changes only c247/latest.log/latest.json.
Review uses immutable retrieved log ranges and recorded user-local postchecks, not an independent
full-log rehash or rerun of the six real checkpoints. The publisher digest is explicitly attributed.

## Execution validity

24 own tests PASS in3.588s;3097 focused tests PASS in110.436s.328 source pins/514 inputs protected.
6x200=1200 updates/38400 normal presentations;1290 total forwards/43008 row presentations.
All checkpoint/prediction replays and changed-weight checks PASS. Persisted comparator/discrete
replay PASS;protected inputs,tracked tree and execution HEAD preserved;run_execution_valid=True.
Scientific status FAIL;both primary TRAIN family gates and both secondary joint gates False.

## Deciding measurements

Normal correct counts;each language has32 TRAIN rows and16 HOLDOUT rows:

| Seed | Full TRAIN EN/JA | GRU TRAIN EN/JA | Full HOLDOUT EN/JA | GRU HOLDOUT EN/JA |
|---:|---:|---:|---:|---:|
|234001|27/32,28/32|31/32,32/32|9/16,8/16|7/16,7/16|
|234002|32/32,32/32|18/32,17/32|3/16,5/16|4/16,5/16|
|234003|16/32,15/32|17/32,23/32|4/16,5/16|4/16,4/16|

Full seed234002 EN/JA passes the complete TRAIN criteria, unlike C246 with the same normal
exposure. GRU-only seed234001 EN/JA passes in both C247 and C246. The other8 cells pass neither.
Exact comparison_counts:BOTH_TRAIN_PASS2,CONTROL_TRAIN_PASS_ONLY2,NEITHER_TRAIN_PASS8.
Thus4/12 TRAIN cells pass,8/12 miss;all12 HOLDOUT cells miss the full criteria.
This primary verdict is TRAIN-only;HOLDOUT misses are reported separately,not its deciding cause.

## Interpretation and limits

The answer is mixed, not a universal attribution. In the matched Full234002 cells, reduced
normal-example count alone cannot explain C246's TRAIN failure:the same normal exposure without
masked updates passes. For8 cells that fail both, normal-budget insufficiency remains compatible
with the observation,without excluding mixed-training effects. C244's400-normal-update fitting
success remains a relevant saved comparator,not an independently rerun baseline.

Removing masked updates changes total optimizer steps and moments;this does not isolate gradient
conflict, an encoder defect or a particular internal algorithm. The pattern is seed-dependent.
Both model families still have holdout problems,so it is unjustified to blame the FOLD core alone.
Earlier suggestions of a binding/readout bias are hypotheses,not established diagnoses.

Stop iterating the erasure recipe for now. Preserve all accepted sources/tests/logs and the
uncompressed reference model. The discussion of architecture candidates was not adoption of a
new production design and does not authorize editing shared accepted runtime modules.

## Accepted artifacts

- control-plan.json:f9558bfead121a605f8cc2dd776eed5db6db981c1c20b675d44d49d4b95a502c (2559 bytes)
- measurements.json:14d37a60a23db8475a0161c70cc7bc3c92e034b7f1329012746ebbd9349c62a1 (30358 bytes)
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346 (15904 bytes)
- trained-models.pt:809d248f31f56f7c07c2e53637277a3fd0c62edbaa409d6c47e565421cf7d79f (601940 bytes)
- validation-summary.json:2301115ce19ca0422858054bd29de9b92f2ca2335e7e8e7d586006bb860a61b2 (2260 bytes)

## Next question, not registration

As a bounded experimental candidate, can a small residual readout that revisits per-token states
meet the original normal-input recombination criteria, compared with an equal-parameter residual
adapter that sees only the final EOS state? This is a minimal part of candidate A, not fact slots,
structured memory, supervised entity extraction or adoption of a new FOLD architecture.

Keep the C244 partition,400-normal-update recipe and common initial backbone;add768 parameters
per arm in both Full and GRU-only. The reader uses a learned query from EOS,learned token keys,
and a zero-initialized output projection. The control uses a16->24->16 EOS-only residual MLP,
with the same768 additional parameters and zero output projection. Both start with the same
original logits. No correct value/location/entity metadata is fed into the model.

The Full core and GRU frontend remain unchanged;the pilot lives entirely in new experiment files.
Use two trained arms,not an unparameter-matched headline comparison to C244. No speed/causal/core
superiority claim;new capacity and compute are disclosed. Separate preregistration,authoring tests
and committed-byte review control readiness. Gate F and production design remain unchanged.
