# C174 acceptance — learned necessity syntax ablation

## Formal verdict

2026-09-17 JST: **C174 ACCEPTED PASS** under its original directional pilot rule.
Gate E remains **NOT PASSED**. C175 is not registered by this acceptance commit.
C160/C168/C169 remain ACCEPTED VALID NEGATIVE. No historical result is rewritten.
Read the C174 preregistration, learned-necessity-probe-v0.1.md and conversation protocol.

## Execution / identities

Repository: `akakishi04/fold`, branch `feat/sft-target-loss`.
Execution HEAD: `d011b13952abc10093d8d8d2b418ecc3d39f5fc3`.
953/953 focused tests PASS in 15.929 seconds; source precheck PASS;
protected inputs, tracked tree and execution HEAD preserved; run_execution_valid=True.
The existing passing C145 warning is not an execution failure.

Report: `runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json`.
SHA256: `3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36`.
Uploaded log: `貼り付けられたテキスト（1 点）(20260917-081415).txt`, 210379 bytes.
Log SHA256: `d6dbc289260415305e2f2b4857c72d5304ef8370db5628e3a8ad1fae88a8d86c`.
C173 parent SHA256: `3c4759bbc14b4ab9849d482d2f330cbf1038c1473e2deab2aaf40f9637e635aa`.
Scientific manifest SHA256: `6b06991409954a6a97340a2fd93dcf22bd4622e9b90e9968a670f337c830f1a4`.
Canonical dataset SHA256: `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.
Written necessity-plan.json includes source pins and therefore has a different SHA256:
`c05e3cec9c57209e9f5ccc720589cf70a248bf2cc1151b3d4c40d1757841d8f8`.
Pilot predictions SHA256: `f718d6a1aa90ade2d9f8e2454fba3744e074ee4d82c0ce95c3505615880aaaa7`.
Training predictions SHA256: `0bc10c35744ca5e97c3270cca1823ee8e6dc70e30acf37a7a3946cf48ed67dba`.
All 11 artifact names, hashes and sizes and all 6 checkpoint fingerprints remain in the report.

## Repository migration incidents (not scientific negatives)

The original monorepo registration HEAD was `5e05168efa1680e075e5dffde990535c713b539b`;
its standalone registration HEAD is `19603c7267ad2808ad953fe70af2caa4b646833c`.
An obsolete ExpectedHead first blocked execution before regression/training.
The next attempt reached an old `BASE:fold/...` source guard and stopped before regression/training.
That source-precheck incident is INVALID EXECUTION / RETRY SAME C174, not a quality result.
The runner-only fix d011b139 maps the historical C173 source lookup to standalone commit
`61c78906c28df07a12c9eacd5c8d1b09bc1ca534` and uses `HEAD:<relative path>`.
It substitutes only protect_sources in its precheck, benchmark and postcheck processes.
The C174 Python benchmark, learned model, split, seeds, steps and decision rule were not changed.
The C173 artifact keeps its actual historical monorepo execution SHA
`2cc2b1f40e9c7638e4bc0f72c07feb85d95a9c26`; do not edit that artifact to match migrated Git history.
The module's original direct CLI still assumes monorepo paths; C174 reproduction uses the
accepted tools/run_c174.ps1 entrypoint. Do not claim that every old direct CLI was migrated.

## Deciding measurements

Each arm/seed trained 2000 updates, 512000 sampled examples, 26114 parameters.
Seeds 174001/174002/174003; paired initial weights and minibatch hashes match in all 3 pairs.
6 final models, 12000 training forwards/updates, 3072000 sampled examples.
56376 pilot predictions, 254664 training-resubstitution predictions, 312 postfit batches.
CPU float32, 2 threads, PyTorch 2.10.0+cu130, NumPy 2.3.5.
No actual acquisition, proof checker, evidence write, network or production wiring.

Primary endpoint: equal-weight mean of balanced accuracy across the 4 pilot function groups.
Missing-fact rule primary score: 0.6566257816257817.

| Seed | TASK_VISIBLE primary | SYNTAX_ABLATED primary | Difference (percentage points) | Sufficient recall | Needs recall |
|---|---:|---:|---:|---:|---:|
|174001|0.7217363934291018|0.6914442906630407|3.0292102766|0.8167259786476868|0.5848416289592760|
|174002|0.7267349717219510|0.6969538563288562|2.9781115393|0.8198398576512456|0.5855957767722474|
|174003|0.7383088135822511|0.7277355167980168|1.0573296784|0.7743179122182681|0.6504524886877828|

All three seeds strictly exceed their matched ablation and the missing-fact rule;
all six required class recalls exceed 0.5. No seed averaging is used to decide PASS.
Descriptive mean paired primary difference: 2.3548838314 percentage points.
TASK_VISIBLE ordinary pilot accuracy is 75.1277%, 75.3725%, 73.9357%; this is not the primary metric.

## Scientific interpretation

Structured task/facts -> small trained MLP -> uncorrected SUFFICIENT/NEEDS_OBSERVATION argmax.
The original criterion supports an aggregate benefit from exposing syntax for this fixed,
read-once four-variable pilot. It does not establish reliable necessity reasoning, a FOLD
shared-core advantage, learned tool selection, learned proof generation or live policy safety.

Of 2652 truly needs-observation rows per seed, 1101 / 1099 / 927 are incorrectly called
sufficient (41.5158% / 41.4404% / 34.9548%). Of 6744 sufficient rows, 1236 / 1215 / 1522
are incorrectly called needs-observation. These are classifier errors, not observed
hallucinated answers or actual unnecessary acquisitions: no live answer/action was run.
Do not deploy the raw pilot classifier as a trusted no-acquisition gate.

## Confound / heterogeneity audit

Syntax gain is not uniform. TASK_VISIBLE minus ablation per-group BA, percentage points:

| Seed | group 3 | group 22 | group 30 | group 38 |
|---|---:|---:|---:|---:|
|174001|-0.9672|10.1405|1.0531|1.8904|
|174002|-1.3258|7.0115|3.8347|2.3920|
|174003|-3.6061|10.7442|0.3320|-3.2407|

Group 3 worsens in every seed; group 38 worsens in seed 174003. Preserve these outcomes;
the preregistration requires group-macro improvement, not improvement in each group.
The blind model also scores well above 0.5, showing that a syntax-free comparator is
nontrivial on this distribution. That fact alone does not establish leakage.
Visible training-resubstitution primary BA: 0.7407335661 / 0.7410268471 / 0.7628742080.
Fitting is imperfect even on training rows. This is not proof that more steps or larger
width will solve it, nor a reason to retune C174. Last minibatch losses are not epoch losses.

TRAIN 36 groups / 524 templates / 42444 rows; pilot 4 groups / 116 templates / 9396 rows.
The 9396 rows and 3 initializations are not independent semantic/task samples. No p-value,
statistical significance, universal generalization or practical-quality claim is made.
Teacher labels and truth-table grouping are evaluator/training work, not inference input.

Wall time 33.61050479998812 seconds covers this benchmark's data/training/evaluation/IO,
not regression and not production inference latency. Checkpoint sizes 107949/108037 bytes;
all 6 total 647958 bytes. No peak RAM/VRAM was reported; do not infer it from these sizes.

## Independent reviewer coverage

The complete console summary was parsed and canonically reserialized; its reported SHA256
matches independently. Confusion-derived recalls/accuracy/BA and per-group aggregation,
all fit counts, paired hashes, the exact PASS rule and log/postcheck were recomputed.
C173 summary from the earlier uploaded log also reconstructs its pinned hash; all 36
inherited source blobs and 42 overlapping file hashes agree with C174.
11 underlying C174 artifacts (including row predictions and weights) were not uploaded;
the reviewer has not independently reread them or rerun the 953 tests / six fits.
Runner source checks and artifact postchecks are reported evidence, not an independent rerun.

## Disposition

Accept C174 without rerun or retuning. Update standalone repository identity in the live
handoff, not in immutable historical reports. Preserve every checkpoint/prediction/group.
Next design must follow this acceptance. C175 remains unregistered in this commit.
