# C248 acceptance and C249 frozen read-path ablation boundary

## Formal verdict

**C248 ACCEPTED VALID NEGATIVE.** The preregistered primary token_read/Full gate is False.
This verdict preserves the successful individual cells:8/12 reader seed/family/language cells
pass all original TRAIN and HOLDOUT criteria;4/12 miss HOLDOUT. The equal-parameter EOS adapter
passes TRAIN in all12 cells but misses HOLDOUT in all12. Gate E PASSED;Gate F NOT PASSED.
No production architecture adoption or relaxed all-seed gate.

Scientific execution HEAD:23bcc949638ea3e927ec0bb3d846b9f42b552a56.
Published log commit:5a3e7e7ae371b5f5f384d1283d68dd434201e6ec.
Publisher log SHA256:7a1984dd55d93253ea3498503873c0cb41fa3667dfa4f467b7ca0994e3dea99c.
Log bytes:609500.
Summary SHA256:99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6.
Local summary:runs/c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22/summary.json.
Publication is one commit after execution,changing only c248/latest.log and latest.json.
Acceptance is based on retrieved immutable log ranges and recorded user-local postchecks,not
an independent full-byte log rehash or a reviewer rerun of the accepted scientific checkpoints.

## Execution integrity

24 own tests PASS in26.019s;3121 focused tests PASS in135.539s.
334 source pins/526 protected inputs. Twelve fresh models x400 updates=4800 training steps,
153600 training presentations,4980 full-model forwards and162816 total row presentations.
All initial metric replays,head/whole-model weight changes,checkpoint/prediction replays and
persisted paired/discrete checks passed. Protected inputs,tracked tree and execution HEAD were
preserved;run_execution_valid=True. scientific_status=FAIL,production_adoption=False.

## Deciding metrics

HOLDOUT normal correct counts,each language cell out of16:

| Seed | Full reader EN/JA | Full EOS control EN/JA | GRU reader EN/JA | GRU EOS control EN/JA |
|---:|---:|---:|---:|---:|
|234001|16,16|9,9|16,16|6,7|
|234002|5,4|4,4|12,12|8,7|
|234003|16,16|7,8|16,16|6,7|

Every token_read TRAIN cell scores32/32 and passes all criteria. Its eight BOTH_PASS cells
(seed234001 and234003 in both families/languages) score16/16 HOLDOUT,all three paired criteria1.0,
and both mask drops>=0.35. All four remaining reader cells are RECOMBINATION_MISS.
The eos_adapter TRAIN cells all pass;GRU234003 English is31/32,the other11 are32/32.
All12 eos_adapter cells are RECOMBINATION_MISS.

Within-family pooled descriptive HOLDOUT:reader Full73/96 versus EOS41/96;reader GRU88/96 versus
EOS41/96. Combined161/192 versus82/192. Reader exceeds control in11 cells,ties1,worsens0.
These are correlated small-fixture cells,not12 independent training replicates. There are only
three paired seeds. Do not imply population reliability or significance from these aggregates.

## Interpretation and limits

The residual token-reader intervention has substantially better measured transfer than the
registered equal-parameter EOS adapter on this fixed task,including eight fully qualifying cells.
This is stronger evidence than seen-TRAIN fitting alone. However,the all-seed gate remains unmet,
with failures concentrated in seed234002. Initial backbone/head randomness is linked in this
experiment;the cause of that variation is not isolated.

Both arms add768 parameters,so extra parameter count alone does not distinguish them. They differ
in token access,nonlinearity,compute and optimization geometry. The result does not uniquely prove
correct entity binding,learned attention as the mechanism,or superiority of the FOLD core over GRU.
The EOS query summarizes the entire prompt;there are no explicit fact slots or parsed entity keys.
An adaptive two-entity/four-value internal benchmark does not establish broad language ability.
Do not replace failing seeds,extend C248 training or automatically adopt the reader in production.

## Accepted artifacts

- measurements.json:d2c7f99d79e6ac2ddc47e5d5d900ccaea4479b2325c0d0b35e7a9f05f587e382 (38317 bytes)
- readout-plan.json:bfaafd5c699690553aa072ba74b9707853a2e627b22a6d3d488b646f27047593 (3050 bytes)
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346 (15904 bytes)
- trained-models.pt:35e39b16f5a30f9a55d7718427294d4bba6255772ad7fdf183ea0275e310cdc3 (1288213 bytes)
- validation-summary.json:7130fbc17973ea9189313c60df880ea5b9593c1e1e0871f5ddeb08898c0e0dff (1757 bytes)

## Next question, not registration

On all12 frozen C248 final checkpoints,does original normal-input performance depend on the
added residual branch and,on reader models,on its learned nonuniform token weighting?
Compare intact inference with residual_off for both arms,and uniform nonPAD averaging for readers.
Reuse the exact inputs and final weights;do not train or choose only successful seeds. Restore
intact execution afterward and require original predictions/logits/metrics to return unchanged.

This is a diagnostic of the computation used by these trained networks,not another training
recipe,seed-robustness trial or independent test set. Disabling a co-trained branch shifts internal
representations and is not equivalent to training a model without it. A uniform-weight comparison
is not a model trained with uniform attention. A performance loss does not identify the cause of
learning or prove a unique semantic binding mechanism. No C248 rescue or Gate F promotion.
Separate C249 preregistration and committed-byte review must control activation.
