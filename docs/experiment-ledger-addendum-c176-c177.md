# C176 acceptance — conditional loss yields a trade-off, not joint improvement

Judged 2026-09-18 JST. Repository akakishi04/fold; branch feat/sft-target-loss.
Read the unchanged C176 preregistration and conversation handoff protocol.

## Formal verdict

**C176 ACCEPTED VALID NEGATIVE. C174/C175 remain ACCEPTED PASS. Gate E NOT PASSED.**
C177 is NOT REGISTERED at this acceptance-only boundary. Historical C160/C168/C169
negatives and all earlier accepted results retain their original scope.
No rerun, threshold relaxation, checkpoint selection, longer training, new seed search,
loss-weight tuning or replacement of the original endpoint is authorized by this result.

## Execution validity and identity

Execution HEAD: 6155242c6564858293d355c51ae2a3dbc7f25bdb.
Source/artifact precheck PASS; 1001/1001 focused tests in 17.597 seconds.
Six completed models; paired initial weights and sampled row-index schedule hashes agree
for all seeds176001/176002/176003. Both arms see the same syntax and all original fields.
CPU float32, two threads, torch2.10.0+cu130, NumPy2.3.5.
2000 updates and512000 sampled examples per model;12000 updates/3072000 samples total.
56376 pilot and254664 TRAIN resubstitution predictions;312 inference batches.
Six new checkpoint roundtrip loads; historical checkpoint loads0.
Actual acquisitions, proof checker calls, evidence writes and network calls0;
production_runtime_modified=false;gate_e_candidate=false.
71 protected input paths,52 historical source pins,10 output artifacts recorded.
Runner postchecks: inputs preserved,tracked tree clean,execution HEAD preserved,
run_execution_valid=True. Existing C145 warning occurs in passing regression,not invalidity.
Wall clock36.05408079997869 seconds includes registered benchmark work,not serving latency.

Report:
runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json
Report SHA256:b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b
Uploaded log345072bytes:
caa9bfd2496ea416d8c780d8244e32d6db315463aa299524199acf1d0003207b
Canonical reconstructed summary162846bytes,identical to reported SHA256.
Scientific manifest09ce8d00f2f6d09fda96f93e51aed6c34fd5b4e74eba77d51848c8e1f8dbafa8.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Parent C175 SHA256d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
Parent C174 SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.

## Deciding metrics

Percentages below; differences are percentage points. Uniform and conditional share each
seed's initial state and batches. This comparison is NOT against an old C174 checkpoint.

|Seed|Mixed-count BA uniform|Conditional|Delta|Original group-macro BA uniform|Conditional|Delta|
|---|---:|---:|---:|---:|---:|---:|
|176001|56.255583|56.876043|+0.620460|74.911076|68.554563|-6.356512|
|176002|53.809383|57.319080|+3.509697|70.051353|68.098263|-1.953090|
|176003|53.870652|56.524276|+2.653624|68.924248|62.235726|-6.688522|

|Seed|Count1 NEEDS recall uniform -> conditional|Count3 SUFFICIENT recall uniform -> conditional|Aggregate conditional NEEDS recall|
|---|---|---|---:|
|176001|33.854167% ->56.510417%|1.282051% ->30.448718%|68.815988%|
|176002|13.671875% ->59.244792%|6.410256% ->36.217949%|66.628959%|
|176003|2.734375% ->43.619792%|17.948718% ->66.666667%|47.134238%|

Preregistered conditions1,3,4 pass in every pair. Condition2(original group-macro BA
must not decrease) fails in ALL THREE pairs. Condition5(both conditional aggregate
recalls>0.5) also fails for176003. Uniform176003 also has NEEDS recall49.095023%,but
that is neither an execution invalidity nor a reason to omit the seed.
No averaging or isolated primary improvement converts this experiment into PASS.

Aggregate error counts,denominators NEEDS2652 and SUFFICIENT6744 per model:
176001 missed-needed835->827;false-needs1627->2318.
176002 missed-needed1223->885;false-needs1133->2202.
176003 missed-needed1350->1402;false-needs918->1451.
These are classification errors,not measured hallucinations or tool executions.

## Scientific interpretation and confound audit

TRAIN-only weighting moved both targeted recalls in the intended direction, but did not
satisfy the joint requirement of preserving original quality. It changes which cases
are sacrificed: for176003,count3 NEEDS recall fell87.987013%->42.694805% while count3
SUFFICIENT recall improved. Count0/4 remain perfect,with BA null for absent classes.
This is a real finite trade-off under the specified model,budget,objective and pilot.
It does not prove that all loss balancing fails or that model architecture is incapable.

All three conditional TRAIN mixed-count scores also improve,while original TRAIN
macro-group BA decreases:0.7708522234->0.7370005433;
0.7294832791->0.7242989161;0.7147724629->0.6842278548.
Therefore the disagreement is not confined to unseen semantic groups. Do not infer that
extra steps/width necessarily solve it. Different objective_loss values across arms
are not directly comparable training-quality measurements;their loss weights differ.

Same reused four pilot groups,not independent confirmation. New seeds do not create a
new semantic holdout. No teacher,truth-table repair or loss weights enter inference.
No proof of internal reasoning,calibration,safe live control or FOLD shared-core quality.
The summary cannot distinguish changed score ordering from shifted decision offsets.
That unresolved distinction must not be answered by silently tuning a threshold.

## Review scope

Reviewer independently recomputed the complete summary hash,all312 supplied confusion
matrix tables,their group/stratum sums and means,all three five-condition verdicts,
paired initial/batch hashes,workload totals,and five TRAIN weight rows/mass preservation.
All agree. The10 output artifacts(including full saved logits/checkpoints) and original
NPZ inputs were NOT independently read here;1001 tests and six full fits were NOT rerun.
Hash-bound runner evidence and independent summary arithmetic are distinct evidence levels.

## Disposition

Preserve every model,log,plan,prediction and prior result. Do not adopt CONDITIONAL_CE as
an accepted replacement and do not amend C176 settings to obtain PASS. The next design
may examine frozen score ordering and error exchanges without training or changing raw
predictions;it requires separate preregistration after this verdict. C177 unregistered
here. C176 needs no rerun merely for documentation.
