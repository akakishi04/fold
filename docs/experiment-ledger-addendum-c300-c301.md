# C300 formal acceptance — frozen readout-term intervention

C300 ACCEPTED PASS (diagnostic integrity only). C299 remains diagnostic ACCEPTED PASS.
Gate F NOT PASSED. C301 NOT REGISTERED in this acceptance commit.

## Evidence and validity

Scientific execution HEAD:b1d24f9ca330711802eb450f86fc3b4c64d88666.
Published log commit:14e8a6972c0364a30ddb755c5d45d678d5673bea.
Log SHA256:eac88132581c7d0a02f6b5d063160917f554e2afd3f8e49a6780b2b2d835d978;819407 bytes.
Publication changes only docs/experiment-run-logs/c300/latest.json and latest.log.
Summary:runs/c300-v5b-readout-terms-ba7889d232f342d591bb8b75f48cb853/summary.json.
Summary SHA256:440d5dcd9b8293f3925f394fa9ea1fc08d9754dfd67fc411340c5d6d1548fed3.
Manifest:31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30.
Own40/focused4597 PASS (focused suite641.078s). Source646/protected1191.
All9 learned C299 models evaluated in all4 modes;scientific training0,2916 forwards,
279936 row presentations,11664 core calls,9 model-state loads,new checkpoints0.
All nine before/after/restoration maximum logit errors are0.0. Weights and hooks preserved.
Persisted reconstruction PASS;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
No C300 rerun required. Diagnostic PASS does not assert any improvement or capability gate.

## Deciding metrics

Full before/after task passes:two_char7/9,triple7/9,quad3/9.
Residual_only:0/9 for every task. Reader_only:two_char6/9,triple6/9,quad4/9.
Full matrices reproduce C299 unchanged. Reader_only quad matrix:
[[True,False,False],[False,True,False],[True,False,True]].
Reader_only seen-task matrices:
[[True,False,False],[True,True,False],[True,True,True]].

At remaining297002/core297002,reader_only rescues exactly2 quad HOLDOUT answers,
286/288 ->288/288,without losing another answer there;this cell clears the full quad gate.
At remaining297002/core297003,reader_only loses1 correct HOLDOUT answer at each seen length,
288/288 ->287/288;quad HOLDOUT also regresses281/288 ->277/288 (4 losses,0 rescues).
At remaining297001/core297003,quad TRAIN falls553/576 ->357/576 (14 rescues,210 losses),
and quad HOLDOUT159/288 ->121/288 (12 rescues,50 losses). Retain these adverse effects.
No unconditional reader-only policy is supported by the added one quad pass.

## Interpretation boundary and next question

On these jointly trained fixed models,removing a summand changes inference behavior. It does not
identify the cause of their training failures or prove the recurrent core is dispensable.
All upstream computation still executed. Normalization makes this non-additive in logit space.
Ablated distributions differ from training. Do not choose the better mode per input or deploy a
selected successful cell. Earlier judgments and thresholds remain unchanged.

A separately preregistered next comparison will test learning a single global residual gain from
TRAIN,starting at exactly the original r+a behavior,against a fixed-gain concurrent control.
It must use fresh paired seeds,ordinary CE,unchanged budget and old full gates;holdout cannot tune
the gain. This is a new learning hypothesis,not a conclusion already established by C300.
C301 requires source/test/runner/launcher/preregistration/design and committed-byte review.

## Parent artifact receipt

intervention-plan.json:2242 bytes;31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30.
intervention-evaluations.pt:573885309 bytes;3c2f4509d7425c32d424572481d44a0310d96bc9591b616fc02d627ae6f3d153.
measurements.json:2839469 bytes;fa0f35eb7b5e9412f6c82755d7505103253803cc52919ff07b9c41623fa353a7.
validation-summary.json:109401 bytes;e3541531a9f62a00db264a09c140923ed38555cacda6c713a348a3bf4e2ad27a.
