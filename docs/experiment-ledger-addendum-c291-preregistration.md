# C291 preregistration — answer-wise hardest-rival margin

Experiment:C291-v5b-answer-wise-hardest-rival-margin. Stage:V5-B-ANSWER-WISE-HARDEST-RIVAL-MARGIN.
Acceptance base:8f3158ea7f61c87bf674794755c8c36ccb0b27fe.
C290 ACCEPTED PASS (diagnostic integrity only). C289 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C292 NOT REGISTERED.

## One question and fixed comparison

At an unchanged800-update/model budget,does replacing the pair-sum auxiliary with an answer-wise
hardest-rival auxiliary improve reliable unseen four-character transfer? Use concurrent CE and
pair-sum controls,not historical seed counts. Fresh seeds291001..291005;three arms per seed:
- ce_only:CE only;
- pair_sum:CE+.25*mean over24 pairs softplus(1-[(z0[y0]+z1[y1])-(z0[y1]+z1[y0])]);
- answer_margin(candidate):CE+.25*mean over48 rows softplus(1+max_{k!=y} z[k]-z[y]).

Every batch is the same24 intact logical query pairs in all arms. Both penalties are recorded in
all arms using the SAME forward outputs;only the specified total loss is backpropagated. The target
is excluded from the255-class maximum. No candidate filtering,temperature,additional head,loss sweep,
selective retry or early stopping. Ties use torch.max's first class index;finite differences are
checked away from ties and a separate finite tie-gradient test is included. Raw logits must be finite.
Target masking inside the supervised loss is not an input/evaluation evidence-mask intervention.

C290 showed satisfied summed margins with wrong individual answers. This motivates the intervention
but does not prove the cause. Aggregation,negative set and resulting gradient magnitudes change together.
The coefficient .25 and margin1 remain numerically unchanged,NOT gradient-scale matched. This tests
one complete objective replacement,not which of its subproperties caused any improvement.

## Exact parent/schema boundary

C290 execution:327e0a2e45270a4eb60f43daf8cca5c21242987c.
Published log:76706cdc46914e67957abb37fcb75c46d1af0eaa.
Summary:runs/c290-v5b-pair-margin-dd335cb112744775980aa441008b9a7f/summary.json.
Summary SHA256:1f4a3c16130b4c4517ddc7b5c09d7404ed83652fd0d6ce8b9a2438195a9cb11e.
Parent source:fold_lm/v05_benchmarks/model_c290_saved_pair_margin_audit.py.
Parent Git blob:43cbbd346f8d6f8b1b57bf9bc026a995ed52786d.
The code pins all three C290 output names/hash/size triples from its published compact receipt.
Verify17 ordered summary hashes before dispatch:C290,C289,C288..C274. C289 hash is obtained from
immutable C290.PARENT_SHA;the other15 are immutable C289.SUMMARY_SHAS. No mutable latest selection.

C290 is a diagnostic,not a model checkpoint. Call C290.verify_artifacts with16 ancestor summaries
and C290's accepted execution HEAD. This recursively reconstructs the C289 evidence and the C290
pair report under no-neural guards. Require diagnostic PASS,capability_gate_applicable=False and
exact parent_results. Then read the already-verified C289 dataset/triple/quad JSONs;verify their
canonical SHA256 identities again. No old checkpoint initializes C291 models.

The only direct repository import is C290. Its context yields C289;C289 yields the immutable
C287 diagnostic,C284 evaluator/replayer,C283 quad renderer/scorer,C282 training-table builder
and the inherited core bundle. Source-level call contracts were checked before authoring.
C284.evaluate requires eval mode and frozen parameters;replay_one strict-loads each final state,
checks fingerprint,full-view logit drift<=1e-9 and exact argmax. No inference from loss to accuracy.
C282.training_tables uses only normal TRAIN rendering at lengths2/3 and provides targets separately.

## Held constant

Actual C278 all-token MeanFinalDualReadout,14256 independent parameters,48-token context,CPU float64.
Three independent copies of each initial state;compare fingerprints,storage,first-input losses.
No labels,pair metadata or selected rival identities enter model.forward;only prefix tokens and
existing zero IDs do. TRAIN rows192;96 complete pairs;HOLDOUT never optimized. Four-character
prompts are evaluation only,including its inherited TRAIN-value split (not length4 training).

200 epochs x4 batches x48 rows =800updates;profile=epoch%3;length=epoch%2.
randperm96(generator seed+291000+epoch). Reset fit RNG to seed+292000 independently for each arm.
Each logical row receives100 exposures at each trained length. Length/profile update matrix:
[[136,132,132],[132,136,132]]. All3 arms have identical batch/rendering schedules and LR histories.
AdamWLR .005 constant,betas(.9,.999),eps1e-8,weight_decay0,clip norm1,error_if_nonfinite=True.
One optimizer per model,800 uninterrupted updates,no intermediate checkpoint selection.

## Fixed gate and reporting boundary

Unchanged C267/C270/C283 full normal/evidence-blind/query-blind scoring at lengths2/3/4.
Thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Primary candidate PASS iff ALL5 answer_margin models pass EVERY original four-character criterion.
Report each arm's two/three/quad/all-task pass counts,trained-length TRAIN and HOLDOUT direct counts,
90 final model/task/split partitions and360 named candidate-versus-each-anchor count contrasts.
All seeds are retained;no pooled-accuracy substitution for the all-five gate.
An absolute PASS is not automatic superiority over controls,arbitrary-length competence or Gate F.
Existing parent verdicts and thresholds remain unchanged. Later adoption requires separate evidence.

## Workload,artifacts and protection

15 newly trained models,12000 updates,576000 training-row presentations.
Per model:800 training forwards+81 final scoring forwards+81 reload-scoring forwards=962.
Total14430 model forwards,809280 total row presentations,57720 core calls.
One15-state checkpoint bundle write/load,15 strict state loads,network0. Evaluation-tensor archive
serialization is not a model-checkpoint write. Operational tests/preflight are excluded from these
scientific counts. All learning/output/state costs remain in local artifacts;no speed/memory claim.

Artifacts:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json;plus full summary.json.
The archive records frozen final logits for all3 tasks/all views and all800 per-model CE,pair,answer,
total,LR and coefficient histories. Persisted reconstruction checks every file hash/size and
recomputes gates from saved logits without neural calls. Compact console receipt plus aggregates;
full protected maps and tensor artifacts remain local/ignored,not committed into the repository.

OWN6:source,test,runner,launcher,preregistration,design. Source592=586+6.
Protected1066=1056+4 C290 inputs+6 OWN. Dependency-union67. Own40;modules176;
loaded4286;focused4285. Sole inherited exact C204 exclusion unchanged;no accepted test modification.
Manifest SHA256:99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.

## Review/execution/stop

Commit/re-fetch all OWN6;independent post-authoring review PASS before activation and command release.
Mandatory authoritative Windows Validate:17 parent hashes/full reconstruction,source/input protection,
real tables/all5 schedules/three identical initial models,CE and pair-sum loss+gradient equality to
C289 objectives,own40 and focused4285. Dispatcher,selected launcher and runner require ParseFile.
Only after Validate PASS may15-model scientific execution and log publication begin.
Invalid integrity retries SAME C291 without changing scientific conditions. Valid primary miss is
ACCEPTED VALID NEGATIVE. C292 remains unregistered until C291 formal judgment.
