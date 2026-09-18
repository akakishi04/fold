# C183 preregistration — frozen renaming path attribution

V5-E; akakishi04/fold; branch feat/sft-target-loss.
Registered AFTER C182 acceptance cdf424217f14bb6272e3a5d37ac8aa638dd1136f.
C183 ACTIVE / NOT YET JUDGED. C184 NOT REGISTERED. Gate E NOT PASSED.
C182 remains ACCEPTED VALID NEGATIVE; C181 ACCEPTED PASS; all earlier judgments fixed.

## One scientific question

For the complete observed C182 candidate failure set, does exactly ONE of the two
changed input routes reproduce the decision flip when its final-readout activation
is interchanged in the frozen model, while the other route alone does not?

This is local, outcome-conditioned failure localization, not a repair experiment,
new accuracy claim or another scoring rule to pass C182. Both direct-only and tree-only
outcomes can support single-route sufficiency; neither is assumed in advance.

C182 has exactly one candidate error: seed181003, permutation17 old_to_new(2,3,1,0),
semantic group3,missing-count1,true NEEDS1 -> SUFFICIENT0. The precise source row is
identified from all saved candidate predictions, not chosen manually. Naming affects
both the leaf-ID scalar entering the shared tree cell and the positional fact table
entering the final readout. C180's retrained bypass ablation did not isolate these
routes in a frozen C181 model.

## Frozen source and cohort

Keep all six C181 final checkpoints,seeds181001/181002/181003,both FINAL_ONLY and
INTERNAL_SEMANTICS. No new seed,training,optimizer,checkpoint selection or saved replacement
weights. Use C182.restore_bare: verify full C18125921parameter state including unused
auxiliary tensors, then construct original25726parameter C179TREE_LINKS base only,
with gradients disabled and RNG restored. No teacher or auxiliary-head forward.

Hash the accepted C182 summary and all five outputs,then audit ALL1296648 saved raw
predictions against logits,record identities and the138detailed group/count tables.
Identify the complete candidate failure set automatically;require exactly the accepted
one-case/one-permutation profile. No failure can be dropped or renamed as a control.

Inference cohort:all9396source PILOT rows at identity and permutation17,all six models.
The other22permutations are audited from saved predictions but NOT run through models
again. This cohort contains the actual failure and matched controls; it is selected
AFTER observing C182 and is not an independent test or semantic generalization claim.

## Four readout conditions

Run the original graph.predict with batch1024 on identity and coherently renamed inputs.
A temporary readout pre-hook COPIES its actual94dimensional input and returns None;
it never replaces data or changes forward outputs. Require exact saved argmax and
absolute logit difference<=1e-6,relative0,for all112752coherent replay predictions.
Replay/schema/source/nonfinite mismatches are INVALID,not new scientific errors.
Keep the original9396row ordering/batch boundaries rather than replaying one row alone.

Original readout input is [root64,header4,facts16,runtime10]. Under coherent renaming,
header4 and runtime10 must be exactly identical. Let R0,F0 be original root/facts,
and R1,F1 the renamed root/facts. Evaluate:

|Condition|Root|Direct fact table|Meaning|
|---|---|---|---|
|ORIGINAL|R0|F0|Recorded correct candidate decision|
|RENAMED|R1|F1|Recorded naming-change decision,including failure|
|TREE_ONLY|R1|F0|Only the tree-route effect reaches readout|
|DIRECT_ONLY|R0|F1|Only the direct-fact-route effect reaches readout|

Hybrid states reuse the actual captured activations and ORIGINAL frozen Linear94->2.
Only first64 or positions68:84 are exchanged. Both hybrid head calls use batch1024.
No extra shared-cell evaluation,truth-table solver,label-dependent intervention,
new teacher target,threshold fit or output correction is used. Label is used solely
for scoring and selecting the already-observed failure cohort,not model inference.

IMPORTANT: TREE_ONLY/DIRECT_ONLY are deliberately mixed INTERNAL activations, not legal
complete TaskView/PolicyInput objects. Their accuracy-like agreement tables are descriptive
counterfactual diagnostics,not performance of an admissible policy. Do not deploy them,
replace the original failed output,or claim observation binding remains coherent.
Original and coherently renamed full inputs remain the legitimate replay conditions.

## Deciding gate and scientific interpretation

For every actual candidate failure,original must replay correct and renamed must replay
wrong. The unchanged binary argmax then yields four possibilities:
- TREE_ONLY wrong,DIRECT_ONLY correct: TREE_ONLY_SUFFICIENT.
- TREE_ONLY correct,DIRECT_ONLY wrong: DIRECT_ONLY_SUFFICIENT.
- BOTH isolated conditions wrong: EITHER_ALONE.
- BOTH isolated conditions correct: JOINT_REQUIRED.

PASS requires exactly one isolated route to reproduce the wrong decision for the complete
observed candidate failure set (here one case). Either of the first two modes qualifies.
This supports local isolated-route sufficiency under the specified intervention,not a
unique universal mechanism or proof that other paths have no score contribution.
VALID NEGATIVE for EITHER_ALONE or JOINT_REQUIRED:the single-route explanation is not
supported. Preserve all diagnostics; do not change the primary question after seeing them.
Controls and other cohort rows are fully reported but not required to become perfect.
Source/replay/schema/nonfinite/incomplete/protection issues=>restore SAME C183 validity.
Finite scientific FAIL exits0;invalid execution retains invalid.json. No retuning.

Record original/coherent/hybrid logits and signed NEEDS margins on the counterexample;
record the additive margin residual as a numerical diagnostic,not a replacement gate.
Near-zero margins must be discussed as numerically sensitive rather than silently
rounded or treated as evidence of broad causal robustness. Exact logit equality across
hybrid routes is not assumed. No claim that a FLOAT32 numerical decision is an exact
symbolic proof. Neither outcome rewrites C182 or passes Gate E.

## Fixed workload

|Quantity|Registered total|
|---|---:|
|Saved C182 predictions reaggregated|1296648|
|Frozen source checkpoint loads / fresh seeds|6 / 0|
|Legitimate model replay rows,identity+permutation17|112752|
|Original model forward batches / shared-cell calls|120 / 840|
|Additional counterfactual readout rows|112752|
|Additional readout batches|120|
|All four conditions' output decisions|225504|
|Training / teacher / auxiliary forward calls|0 / 0 / 0|
|Acquisition / proof / evidence / network calls|0 / 0 / 0 / 0|

CPUfloat32,2threads,deterministic algorithms,batch1024,unchanged base parameters.
Work is not comparable to original training or a new production speed benchmark.
The additional head-only interventions pay their real compute; no speed/VRAM claim.
No parameters,source data or historical artifacts are modified.

## Outputs and integrity

Outputs:path-attribution-plan.json,source-audit.json,replay.json,path-results.json,
counterexamples.json,path-predictions.npz,summary.json. Six artifacts excluding summary.
Save all6models x4conditions x9396rows logits/decisions. Save group confusion for all
conditions and exact counterexample expression,visible facts,source-row identity,
label and all four predictions/margins. Rendering displays syntax without evaluating it.

Reuse C182.precheck through C181/C180/C179/C178/C177/C176/C174,then add accepted C182
summary and five artifacts.80historical pins+4current own files;161protected paths,
plus outer C37/composition-fixture guards. Old source blobs/preregistrations unchanged.
Parent summary06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73;
source execution HEAD8ee4942d7b4ec73ac65de8d6f17f59c297c6ee99.
Manifest SHA256e4152fd486ccbe0c03c48c6bcf3dcc154ca41b03b079c24dee14d78f070a49f3.

## Review and execution limits

32/32 new tests passed on the actual new module. Tests use synthetic94dimensional
activations,a toy Linear94->2 model/predictor,and hand-built raw rows; they do NOT
simulate completion of the full checkpoint/artifact integration. No official checkpoint
or deciding C183 outcome has been executed by the reviewer. No claim that a toy
predictor is the complete original C179 inference implementation.
Tests cover isolated coordinate ranges,context invariants,immutability,hook cleanup,
unchanged forward on the synthetic model,batch handling,raw argmax,four outcome modes,
strict gate,syntax-only rendering,no label interface and frozen manifest.
New module/tests compile;three embedded PowerShell Python blocks parse.
Full1217tests,WindowsPowerShell itself,the complete161input source/artifact chain,and
formal112752base+112752head counterfactual predictions remain UNEXECUTED.
Local git clone failed DNS resolution;no complete local checkout was available.

**1217expected=1185+32;67modules**. One regression then one frozen diagnostic batch.
Run tools/run_c183.ps1 with C182/C181/C180/C179/C178/C177/C176/C174 summaries and ExpectedHead.
Progress:source audit,model1/6..6/6,counterexample path_mode/margins,RESULT/POSTCHECK.
Judge C183 ->ledger/handoff->next design. C184 must not be registered before judgment.
