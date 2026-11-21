# C181 formal verdict — ACCEPTED PASS

V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
This acceptance precedes any C182 registration. C182 NOT REGISTERED at acceptance.
Gate E NOT PASSED. Historical negatives and all earlier judgments remain unchanged.

## 1. Formal verdict

C181-v5e-proper-subexpression-supervision / V5-E-PROPER-SUBEXPRESSION-SUPERVISION:
**ACCEPTED PASS** against the unchanged C181 preregistration.
Each of three paired seeds satisfies all five joint conditions. The three
INTERNAL_SEMANTICS models have zero main classification errors on every registered
TRAIN and reused PILOT row. No rerun, checkpoint/seed selection or retuning is needed.

## 2. Execution validity and evidence identity

Execution HEAD: 3ec4cd8f2afc664799f1e6bfecfce457dd255ad4.
1153/1153 focused tests passed in 14.986s. Source/artifact precheck PASS; postcheck
protected_inputs preserved, tracked_tree clean, execution_HEAD preserved;
run_execution_valid=True. Existing C145 requires_grad scalar warning did not fail tests.

Summary: runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json
Summary SHA256: bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98
Reconstructed canonical summary: 201752 bytes; exact hash match to runner output.
Uploaded log: 406464 bytes; SHA256
bb41d932f432d30f501fb0982fa1934f4966b9d82db5b308f687777e07e7a2ff.
The upload is the complete C181 log, not a new C180 run or a clipboard test result.

Seeds181001/181002/181003, six models; all paired initial fingerprints and batch
schedule hashes match. 2000 updates/model, batch256, 12000 updates, 3072000 main
samples, 84000 batch-cell calls. Both models store25921parameters; inference uses
25726base parameters. Teacher42444TRAINrows/84888proper-node labels,254664nonroot
node evaluations;12000auxiliary forwards,6144000target uses including zero-alpha
control,3072000nonzero-alpha target uses. Pilot/root/leaf auxiliary targets0.
56376PILOT+254664TRAIN main predictions;312inference batches/2184cells;
inference auxiliary calls0; newcheckpoint loads6, historicalcheckpoint loads0.
72historical source pins,135input paths,11artifacts excluding summary.
Actual acquisition/proof/evidence/network calls0; productionmodified=False;
gate_e_candidate=False. End-to-end reported benchmark178.8699673s is not a speed claim.

Reviewer independently reconstructed the summary and recalculated312confusion-based
metric tables,72ordering tables,12exact AUCmeans,36error-exchange tables, all three
gate vectors, group/count sums, pair hashes and workload totals. No discrepancies.
Source inspection confirms predict delegates to original graph.predict(model.base,x),
without the auxiliary head or teacher. Teacher targets are generated from TRAIN only;
no teacher-forced state is supplied to forward; root is excluded from the teacher.

Limit: the11separate output artifacts, source data NPZ and trained checkpoints were
NOT supplied as bytes to this reviewer. Their hashes/preservation are reported by the
user-side runner; the reviewer did not independently replay model predictions, fits
or the1153tests. A failed local git network-resolution attempt was not a repository
checkout. Do not convert summary arithmetic verification into artifact-byte replay.

## 3. Deciding metrics

|Seed|Mixed-count BA final-only -> internal|4group macro BA final-only -> internal|Count1 NEEDS correct/768|Count3 SUFFICIENT correct/312|
|---|---|---|---|---|
|181001|0.5445409706419136 -> 1|0.713879901926777 -> 1|198 -> 768|21 -> 312|
|181002|0.5666106133257668 -> 1|0.756730561105561 -> 1|264 -> 768|3 -> 312|
|181003|0.5551288778091048 -> 1|0.6991769650102984 -> 1|264 -> 768|18 -> 312|

Both aggregate recalls=1 for each internal model. All five gate conditions=True in
all three pairs. Each internal PILOT confusion=[[6744,0],[0,2652]], n9396;
each TRAIN confusion=[[27816,0],[0,14628]], n42444. All per-group/count main errors0.
Mixed-count and matched-visible AUC=1 on both splits; pure-class count0/4 AUC/BA=null.
PILOT rescued2459/2429/2411 and regressed0/0/0. TRAIN rescued9591/9604/9605,
regressed0/0/0. 28188correct candidate PILOT predictions are three models on the
SAME9396inputs, not28188independent problems; TRAIN127332candidate predictions are
resubstitution. All six models account for the56376/254664prediction workload.

Last logged sampled-batch mainCE final-only -> internal:
181001 .4539886415 -> .0013648259;
181002 .3980440199 -> .0022174548;
181003 .4130636454 -> .0012293224.
These are not full-dataset losses or a formal learning-curve convergence proof.
Control auxiliary head has zero-weight training; its high auxiliary loss is not a
fair trained semantic-decoder baseline.

## 4. Scientific interpretation

TRAIN proper-node semantic labels -> auxiliary loss -> learned shared-cell weights
-> original teacher-free base inference -> main necessity judgment.

The fixed auxiliary-supervision package removes all measured main errors, including
both previously weak minority conditions, without changing inference architecture,
input data or update count within each pair. This is a substantial local result, not
merely a threshold-driven exchange of one class error for another.

The measured base capacity is sufficient to express successful decisions over THIS
registered finite task set: simply lacking representational capacity is not a
necessary explanation for the previous plateau. It does NOT establish sufficiency
for larger problems, nor prove final-only training could never learn with other
budgets/optimizers. It supports intermediate-supervision usefulness, not a unique
causal proof of credit assignment versus representation/optimization/regularization.

## 5. Confound audit and limits

Teacher is hand-coded partial Boolean semantics for a read-once four-variable family.
Additional training information is real and its cost is counted. The main forward
uses learned states; teacher outputs are neither runtime facts nor hidden answers.
Tree routing and bound leaves remain handwritten common scaffolding. C178/C179
negatives are not retrospectively overturned by their use in this common substrate.
C180direct-fact mask is not carried forward and its negative remains unchanged.

The four pilot semantic groups were repeatedly inspected during development. Even
zero errors do not constitute an untouched final holdout, arbitrary logical reasoning,
natural-language understanding, repeated-variable reasoning, larger/deeper expression
reasoning, autonomous target/tool selection or the full Gate E candidate.
Current tests do not establish robustness to different naming/index conventions.
Freeze all six checkpoints; next research should challenge frozen behavior rather
than retune this saturated development set. Design/preregistration is a later step.

## 6. Handoff

C181 ACCEPTED PASS; no active next experiment until a separate C182 preregistration.
Retain the full log, summary and all11artifacts. Keep authoritative environment,
protected C37/composition fixture, history chain and separate research tracks.
Multi-Axis/MA-1 and PC-ALM/FHLC stay outside the C series.
