# C249 acceptance and C250 fresh-seed replication boundary

## Formal verdict and identity

**C249 ACCEPTED PASS — diagnostic integrity only.**
C248 remains ACCEPTED VALID NEGATIVE. Gate E PASSED; Gate F NOT PASSED.
No production architecture adoption or new capability verdict follows from this diagnostic.

Scientific execution HEAD:9d28b7420e69efe57555b7db2ccbb0eec6f3d302.
Published log commit:cac4102c0798800f3925c02cb1b38b20cd7ef8a4.
Publisher-recorded log SHA256:607db37473a7f8ed17b0692d798df582e3433f79f03be5514f2c5cb0928c5ca0.
Log bytes:618591.
Summary SHA256:3b95e6ca6b7ba645e13367a483f55fd75a9e112f3f928b2e1cdaf69913be0500.
Local summary:runs/c249-v5b-frozen-read-ablation-9da92553f325421d8acd94d8cccc3b98/summary.json.
Publication is one commit after execution and changes only c249/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges and recorded local postchecks, not an independent
full-log byte rehash or a reviewer execution of the actual trained checkpoints.

## Validity

24 own tests PASS in6.295s;3145 focused tests PASS in142.198s.
340 source pins/538 inputs preserved. All12 final models audited;180 model forwards/8640 rows;
5184 retained logit rows/72 normal contrast cells;zero new training or checkpoint writes.
All original prediction/metric replays, restoration replays and unchanged-weight checks PASS.
Persisted ablation-logit/contrast recomputation PASS. Tracked tree and execution HEAD preserved;
run_execution_valid=True. Diagnostic status PASS;capability_pass_claim=False.

## Deciding observations

The table pools three seeds and two languages within each family. Each entry is correct normal
HOLDOUT answers out of96, not96 independent experimental replications.

| Family / arm | Intact | Residual off | Uniform token read |
|---|---:|---:|---:|
|Full / token_read|73/96|22/96|24/96|
|GRU-only / token_read|88/96|25/96|27/96|
|Full / eos_adapter|41/96|38/96|not applicable|
|GRU-only / eos_adapter|41/96|41/96|not applicable|

Reader totals:161/192 intact,47/192 residual-off,51/192 uniform.
All8 previously successful reader seed/family/language cells fall from16/16 to3/16 or4/16
under residual-off and to2/16 or4/16 under uniform replacement. The four unsuccessful reader
cells are retained, not excluded:in seed234002 Full,HOLDOUT is5/16 and4/16 intact,3/16 and4/16 off,
4/16 and4/16 uniform;GRU-only12/16 and12/16 intact,5/16 and5/16 off,6/16 and7/16 uniform.

Some equal-parameter EOS controls also lose TRAIN accuracy when their branch is removed.
Unchanged pooled accuracy can hide answer flips and opposing gains/losses. The result does not
establish that every residual branch is irrelevant except the reader, or that NLL and accuracy
always move together. All original outputs return after removing the intervention.

## Interpretation and limits

The observed performance of these frozen trained readers depends substantially on their added
branch and on learned nonuniform token weighting, compared with the specified interventions.
This strengthens the rationale for testing the same reader recipe across fresh initializations.

Ablation changes a jointly trained computation and its internal distribution. It is not the same
as separately training a backbone-only or uniform-read model. It does not prove a unique semantic
binding mechanism, identify the training cause, or guarantee reliability on new seeds/tasks.
C248 had only three paired seed blocks, with failure concentrated in234002;do not replace that seed
or reinterpret its all-seed negative as a PASS. No model modification is adopted here.

## Accepted artifact identities

- ablation-plan.json:9fd82672124ff0227174d7a9df894c67ca9f1958a36fad6cbc575e1179dfa414 (2428 bytes)
- contrasts.json:c7bf603849b29a55a0fa7b7e4843b909df4fab7a41ab1081c4f77125b0438e22 (34773 bytes)
- diagnostics.json:2e849c3d6fda7bae1b9b89325f7515f51e18886e679914a32a470234fa9d6310 (5200 bytes)
- logits.json:c28e79ac452bfbc49a4904582abdc233db211ec703f1b8340f0756f389f792d0 (25652812 bytes)
- validation-summary.json:7613f8266a32e67e683a3b0c86aac47437b18a4b677e808a4d5a0ef5442a7aed (309 bytes)

## Next question, not registration

Does the unchanged C248 reader-versus-equal-parameter-EOS recipe reproduce its bounded result in
five new paired initialization blocks250001,250002,250003,250004,250005?
Use both families and both arms in every block,20 models total,400 updates each. Keep architecture,
head initialization rule seed+248000,training rows/order,optimizer,budget per model and original
TRAIN/HOLDOUT criteria fixed. Never choose or discard seeds after scores appear.

The new seed set is prospective;the repeatedly used task/HOLDOUT is not a pristine external test.
New backbone initial references must be measured and paired within each block;old fingerprints
cannot be required for different seeds. Count this extra reference evaluation explicitly.
Report full per-seed results and seed-level success counts, not language cells as independent
replications. A primary all-new-seed PASS would concern this new batch only and would not erase
C248's failed seed or establish universal reliability/general language/Gate F.
Separate preregistration and committed-byte authoring review control C250 activation.
