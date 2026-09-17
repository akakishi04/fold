# C177 preregistration — frozen score ordering after a negative loss intervention

V5-E. Registered after C176 acceptance commit5c8a1bee6571ba3511ca4989408c7bde8d58135e.
Repository akakishi04/fold; branch feat/sft-target-loss. Use final registration HEAD.
**C177 ACTIVE / NOT YET JUDGED. C176 ACCEPTED VALID NEGATIVE. C178 NOT REGISTERED.**
**Gate E NOT PASSED.** C174/C175 remain PASS; all older negatives and results unchanged.

## One question

Did CONDITIONAL_CE improve the ordering of NEEDS versus SUFFICIENT cases WITHIN the same
missing-count stratum, even though its raw decisions failed the original C176 joint gate?

C176 improved its mixed-count BA and both targeted minority recalls in all three seeds,
but degraded original group-macro BA in all three and failed aggregate NEEDS recall>0.5
in176003. Do not change weights,thresholds,capacity,updates or checkpoints to repair it.
Summary confusion matrices cannot tell whether score discrimination improved or whether
prediction offsets moved. C177 uses already saved logits to investigate this distinction.

Changed analytical endpoint: continuous score ordering rather than fixed-argmax accuracy.
Candidate weights,data,split,labels,raw logits and original decisions are all FROZEN.
This is a new post-C176 DEVELOPMENT DIAGNOSTIC,not a new candidate or independent holdout.
It cannot revoke C176's negative or replace C176's original decision rule.

## Frozen source and exact workload

C176 execution HEAD6155242c6564858293d355c51ae2a3dbc7f25bdb.
Parent: runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json.
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
Original C174: runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json.
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Canonical data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.

Reuse ALL six models' stored predictions:seeds176001/176002/176003;
UNIFORM_CE and CONDITIONAL_CE. No winning seed or case subset selected.
TRAIN36groups/524templates/42444rows;PILOT_EVAL4groups/116templates/9396rows.
Use the original NPZ and metadata,not regenerated data.

|Work|Registered count|
|---|---:|
|Stored model decisions replayed|311040=6x51840|
|Pilot rows with two saved logits|56376=6x9396|
|Aligned uniform/conditional prediction-row pairs|155520=3x51840|
|New training/model forward/checkpoint deserialization/fresh seed|0/0/0/0|
|Threshold fitting/calibration/inference correction|0/0/0|
|Actual acquisition/evidence writes/network|0/0/0|

Regression's historical toy training is outside the diagnostic benchmark counts.
C174 eleven and C176 ten artifacts are verified by exact names,hashes and byte sizes;
the twelve checkpoint files are HASHED ONLY,never deserialized. Recheck all saved model
and row identities,raw pilot argmax versus logits,and all C176 train/pilot score tables.
A mismatch is INVALID,not a new behavioral negative. No teacher or rule repairs a decision.

## Score and primary endpoint

Positive class1=NEEDS_OBSERVATION;class0=SUFFICIENT.
Score=float64(saved logit1)-float64(saved logit0). The saved values come from float32
inference; subtraction is explicitly float64. No rescaling,prior correction,probability
calibration,temperature,epsilon-based tie merge or chosen operating threshold.

For each model and missing countm=1,2,3,compare all opposite-label pairs in that stratum:
- win:the NEEDS row has strictly larger score than the SUFFICIENT row;
- tie:scores are exactly equal,credit one half;
- loss:the ordering is reversed.
AUC=(2*wins+ties)/(2*n0*n1).
Compute pair totals by sorted tied-score counts without materializing a Cartesian product.
Primary=equal arithmetic mean of the three stratum AUCs. Use exact rational arithmetic
for strict comparison and save numerator/denominator as well as floating display.
Both classes are required in all three primary strata;do not silently drop one.
For pure count0/4,record pair count0 and AUC=null,not a fabricated0.5 or1.

A constant score offset shared by every case of one stratum cannot change that stratum's
ordering. Thus an improvement cannot be explained SOLELY by such a constant shift.
It still does not identify a unique learned mechanism,prove reasoning,or establish safe
classification. Arbitrary score-order changes may occur without useful practical gains.
Do not interpret negative as proof that the difference was ONLY a constant offset.

## Exact decision and limits

**PASS**: valid complete analysis AND EACH of the three conditional models strictly
exceeds its paired uniform model on the primary within-count AUC mean. Equal score in
any seed fails. No averaging away a failed seed;no significance claim.
**VALID NEGATIVE**: valid complete analysis but any pair fails the strict comparison.
**INVALID / RETRY SAME C177**: source/hash/schema/data or row identity drift,raw argmax
mismatch,metric replay mismatch,incomplete workload,nonfinite scores,protection failure
or unexpected execution exception. Restore validity,not scientific settings.
Finite scientific FAIL writes the full result and exits0 for normal postchecks.

This narrow gate does NOT require all former classification guards to pass:they have
already failed and remain failed in the accepted C176 result. C177 is an ordering test,
NOT an alternative route to promoting CONDITIONAL_CE. Even a PASS leaves C176 negative,
Gate E not passed,and actual inference unchanged. No candidate is selected by this audit.
Both experiments use the same four reused development groups,not new generalization evidence.

## Batched secondary analysis

Keep all group and count profiles rather than requesting separate runs:
1. AUC for all four pilot groups and overall pilot AUC. These mix missing-count strata;
   their interpretation differs from the primary and they do not replace its gate.
2. Pair ordering among rows with the EXACT SAME blind key(raw fields0..3 and46..71,
   as defined by C175). Aggregate wins,ties,losses and denominators across keys. This
   more restricted comparison retains correlations;it is not a one-edit causal test.
3. Paired raw-decision error exchanges separately on TRAIN and PILOT,overall,by semantic
   group and by missing count0..4:both correct,both wrong,uniform-only correct(regressed),
   conditional-only correct(rescued),and direction of prediction flips.

Do not count pairwise combinations as independent trials. The same rows are reused in
several summaries;do not add these overlapping denominators into a new sample count.
TRAIN logits were NOT saved by C176,so TRAIN AUC is unavailable. Only its stored decisions
are replayed. Do not secretly run the model to fill that gap. No additional success gates
are attached to secondary tables and no threshold is selected from any table.

## Protection and outputs

56 historical files=52 parent source pins+four C176-owned files pinned at6155242c.
Four C177-owned files checked against its execution HEAD. Standalone paths only.
83 unique input paths=60source+21artifacts+two parent summaries. C37 and composition
fixture remain additional outer runner protections. No old code or preregistration changed.
Fresh UUID output directory:score-order-plan.json BEFORE reading scores for analysis,
score-order-details.json with full ordering and error tables,complete summary.json.
All source/artifact hashes and byte sizes preserved;tracked tree and HEAD rechecked.
Scientific manifest SHA256942735a9f843485eaf7b2b3b5f15cab774e749f7e52d37adcb64dcd8dcb5572e.

## Verification and execution

24/24 new helper tests passed using the actual new NumPy module. They test pair-order
counts against brute force,half ties,permutation and constant-shift invariance,pure/empty
null results,nonfinite rejection,raw-argmax preservation,paired error accounting,strict
per-seed gate,equal-stratum weighting and additive regression-list parsing.
Tests use synthetic arrays,not the registered pilot. Python compiled and all three
embedded runner Python scripts parsed. Uploaded source/test/runner Git blobs match the
locally tested bytes. No registered score-order endpoint has been computed by reviewer.
Complete prior-module/source-artifact integration,1025focused tests,WindowsPowerShell
and full artifact-backed analysis have NOT been executed by reviewer.

**1025 focused tests expected=1001+24,61modules**,one regression then one CPU audit.
Run tools/run_c177.ps1 -C176Summary ... -C174Summary ... -ExpectedHead ... .
Progress:precheck,regression,plan,1/3replay,three paired AUC lines,2/3tables,3/3protection,
RESULT/POSTCHECK. Preserve full log even if scientific_status=FAIL with valid execution.
Judge C177 -> ledger/handoff -> next design. **No C178 before formal judgment.**
