# C180 formal verdict — ACCEPTED VALID NEGATIVE

V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
Execution HEAD 074419e41b38ad756b2c29a50ea070d5ca60f2d3.
C180-v5e-direct-fact-readout-ablation / V5-E-DIRECT-FACT-READOUT-ABLATION.
Judged against the immutable C180 preregistration and gate, not a replacement metric.
**C180 ACCEPTED VALID NEGATIVE. Gate E NOT PASSED. C181 NOT REGISTERED in this acceptance commit.**
C179/C178/C176 remain VALID NEGATIVE; scoped C174/C175/C177 PASS and all prior judgments remain unchanged.

## Execution validity

Source/artifact precheck PASS; focused regression 1117/1117 in 15.165s; postcheck preserved
protected inputs, clean tracked tree and execution HEAD; run_execution_valid=True.
Existing C145 scalar-conversion warning occurred inside a passing regression, not an invalid execution.
68 historical Git-blob pins, 120 protected input paths, ten output artifacts excluding summary.
Six models, seeds 180001/180002/180003; both original C179 TREE_LINKS, same C178 bound input,
25726 nominal parameters each, 177596 dense forward MACs and 94 mask multiplies/row each.
Only final readout columns 68:84 differ (raw-facts16 bypass); visible leaf information retained.
Paired initial weight fingerprints and row schedules agree in all three pairs.
2000 updates/model, batch256, unweighted CE, Adam .001, CPUfloat32/two threads.
12000 training forwards/updates, 84000 batch-cell calls, 3072000 sampled rows;
56376 pilot + 254664 TRAIN predictions, 312 inference batches, 2184 inference cell calls,
12312 total readout-mask calls. Preparation:51840rows,207360leaf lookups,414720field copies.
Six new checkpoint roundtrips; historical checkpoint deserializations0.
Acquisition/proof/evidence/network calls0; production_runtime_modified=False; gate_e_candidate=False.
Reported benchmark wall clock226.01843590001226s, not comparable to a different environment's timing.

## Deciding metrics (DIRECT_FACTS -> NO_DIRECT_FACTS)

|Seed|Mixed-count1/2/3 BA|Four-group macro BA|Count1 NEEDS correct /768|Count3 SUFFICIENT correct /312|
|---|---|---|---|---|
|180001|0.5612275160 -> 0.5629750876|0.7177524742 -> 0.7214223537|264 -> 264|28 -> 31|
|180002|0.5538738272 -> 0.5354616036|0.6851235806 -> 0.6810320756|113 -> 75|70 -> 34|
|180003|0.5666788151 -> 0.5743076451|0.7208480929 -> 0.7407231754|264 -> 259|51 -> 44|

Gate vectors in the preregistered order (primary,group nondecline,count1 NEEDS,count3 SUFFICIENT,
aggregate recalls>0.5):[T,T,F,T,T],[F,F,F,F,F],[T,T,F,F,T]. No pair satisfies the complete gate.
In seed180002 aggregate NEEDS recall is0.4932126697 -> 0.4852941176; no-direct fails the >0.5 condition.
No seed average, alternate threshold, checkpoint selection or AUC rescues this verdict.

## Secondary evidence and interpretation

Mixed-count AUC:0.5868101049 -> 0.5895868940;0.5910799768 -> 0.5908188398;
0.5917805956 -> 0.5932081039. Small/nonuniform changes, not a strong ordering improvement.
Pilot predictions unchanged:9356/9396 (99.5743%),9225/9396 (98.1801%),9145/9396 (97.3287%).
Rescued/regressed:23/17,91/80,141/110. Ordinary accuracy improves slightly in all three,
but this does not imply the preregistered minority/group tradeoff is solved.
In seed180001 ALL count1 decisions are unchanged (also on TRAIN); this is not merely the
same aggregate confusion with potentially different decisions.
TRAIN mixed-count BA:0.6162036577 -> 0.6176402415;0.6132532223 -> 0.5966249856;
0.6322409913 -> 0.6195045798. TRAIN mixed-count AUC decreases slightly in all three.

Claim:removing this redundant direct readout route alone does not deliver consistent joint
improvement under the fixed diagnostic configuration. It is not adopted as a solution.
The simple hypothesis that this bypass is the single dominant cause is weakened. Remaining
root-state shortcuts, optimization difficulty, semantic representation and supervision remain hypotheses.
Similar predictions from separately trained models do NOT prove the direct branch had zero causal
contribution; alternative paths can compensate during learning. The mask also silences32readout
weight coordinates, so nominal count parity is not effective expressivity parity.
No causal proof that auxiliary supervision will fix the model follows from this negative.

## Correction / limits on preceding discussion

Seven shared-cell calls per input do NOT imply seven sequential ancestors on each tree gradient
path. More cell applications than an old flat MLP do not rule out state-width or training-budget
limitations. No controlled width/budget sweep has established either sufficiency or insufficiency.
Intermediate semantic supervision is a candidate intervention, not a diagnosed necessity.
Repeatedly inspected four pilot groups are DEVELOPMENT, not independent holdout evidence.
This is a diagnostic probe, not a test of FOLD's complete core, language, vision or live acquisition.

## Artifact identity and independent review scope

runs/c180-v5e-fact-bypass-669cce9093064995bf26b1bf176dd609/summary.json
SHA256 9ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2
Reconstructed canonical summary:205427bytes; matches the runner's declared SHA256.
Uploaded UTF-8 log:404324bytes;SHA25605e3c95345cc710d1c359b7154e9d82c422991eec732fb1698cd44c95ff51fde.
Plan ec4b8070887cfe29d2f5aa813dc4a5ed4a397ffb6d229d513d6e48c56b15da94 (8661bytes).
Readout audit562eb22166ab122b593a25f2c55f423410807f5c1bb961707bfcf30b11880682 (1735bytes).
Pilot predictions e6cdb95bc24ac456bc50a5f523c77ccce5aea1cb9ff029cb36a9cc854e923372 (5349289bytes).
TRAIN predictions d6f362ffcca2e3035af22fe1c6cbabb57937da00dff610297de7b5faa47cd5a8 (1953443bytes).
Six checkpoint hashes/sizes are retained in the full summary; no weights are committed to Git.
Reviewer independently recalculated312confusion tables,72ordering tables,12exact rational
AUCmeans,36error-exchange tables,group/count sums,three gate vectors,pair fingerprints and
workload totals from the uploaded complete summary. Separate ten artifact bytes/raw logits/
checkpoints and full1117tests/six formal fits were NOT independently rerun.

## Next boundary

No C180 rerun or retuning. Save this acceptance before registering the next question.
A possible next comparison is TRAIN-only semantic supervision of proper internal subexpressions,
with unchanged inference and a paired final-label-only control. Do not equate a Boolean
necessity bit with sufficient intermediate semantics:known0 and known1 behave differently at
parent AND/OR. Exclude root-target duplication and teacher injection at inference. Exact design
and execution are not authorized by this note alone; a separate preregistration is required.
