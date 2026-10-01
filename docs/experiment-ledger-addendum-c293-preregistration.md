# C293 preregistration — fact-support component reweighting

Experiment:C293-v5b-fact-support-loss. Stage:V5-B-FACT-SUPPORT-LOSS.
Acceptance base:b6e90c80768c48a999f253cfa5b3cced29b465aa.
C292 ACCEPTED PASS (diagnostic integrity only). C291 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C294 NOT REGISTERED.

## One question

Does selectively upweighting the component of CE that assigns probability to either stated fact
value improve reliable unseen four-character transfer,relative to ordinary CE and uniformly scaled
CE,at the same training budget? This is one loss-reweighting comparison,not a restricted decoder.

C292 identified predominantly absent-known-value answers on the failing candidate291003 HOLDOUT.
This is an empirical motivation,not proof of memorization,a causal attention fault,or expected
success. C293 uses new seeds293001..293005 and all three concurrent arms;no old model is continued.

## Objectives and exact supervision boundary

For each existing TRAIN query pair,the two labels y0,y1 are distinct values of the two same facts.
Use S={y0,y1} as an UNORDERED support set for BOTH rows. For each row's256 logits z:
Lsupport=logsumexp(z)-logsumexp(z[S]);
Lchoice=logsumexp(z[S])-z[y];
CE=Lsupport+Lchoice (up to registered float64 tolerance1e-10).
Average per row over48 rows. The set has exactly two classes,no repeated target. Check the logical
pair and label/value correspondence before optimization;do not combine unrelated examples.

Three arms:
- ce_only:CE;
- scaled_ce:1.25*CE;
- support_weighted(candidate):CE+.25*Lsupport =1.25*Lsupport+Lchoice.
All three arms compute the same CE/support/choice scalar diagnostics from one forward;only their
registered total is differentiated. Record800 histories of all components,total and applied LR.
No extra input,query,label or pair is added. The two labels already exist in the original intact
query-pair minibatch. They are used only inside the supervised loss,never in model.forward.
No target/support set,negative label,metadata or fact parser is passed to the model or decoder.

The scaled_ce control tests ordinary uniform loss amplification. It does NOT exactly match the
candidate gradient,AdamW dynamics,epsilon or clipping. Thus success is evidence about this entire
reweighting policy,not a fully isolated causal mechanism. Lsupport can be tiny when the WRONG
in-context fact wins. Keeping CE/Lchoice and the old full gates is essential. No claim of new
supervision information or a universal support-based solution;the loss is a reweighting of CE.
No coefficient search,temperature,output masking or candidate filtering.

## Fixed model,data and schedule

Actual C278 all-token MeanFinalDualReadout,14256 parameters,48-token context,CPUfloat64,2threads,
deterministic. Three independent copies per seed with identical initial state/fingerprint/storage
checks,initial loss components,batches,rendering order and LR. No parent weights initialize C293.
Train only normal length2/3 C267 TRAIN examples.192 logical rows,96 intact pairs,24 pairs/batch.
200 epochs x4 =800updates/model. randperm96(seed+293000+epoch);profile=epoch%3;length=epoch%2.
Reset fit RNG to seed+294000 per arm. Each row gets100 exposures at each length;length/profile
updates[[136,132,132],[132,136,132]]. Four-character and HOLDOUT examples are never optimized.
AdamW lr.005,betas(.9,.999),eps1e-8,weight_decay0,clip1,error_if_nonfinite=True. One optimizer/model.
No early stopping,checkpoint selection,training extension or resampling of failed seeds.

## Exact parent/schema/dependency boundary

C292 accepted execution:4e7d4468a103fa70dcfaee719fcf6daa75af5b7e.
Published log:513f820c494e067e67d1c3757af09cf7642b0b90.
Summary:runs/c292-v5b-answer-roles-ba65b6ac20ac46e5b08fe96a5e5a8e74/summary.json.
Summary SHA256:44aa5ddbe5856ffdd7a62f63ac7574367527fab17c447c02ca68f7071e9ae513.
Parent source:fold_lm/v05_benchmarks/model_c292_saved_answer_roles.py.
Parent Git blob:715ef24d73bc023ac8ed6fd7363b32bc0321b708.
All3 C292 artifact names/hash/size descriptors are pinned from its published receipt in source.
C292 is a DIAGNOSTIC,not a model checkpoint. Verify19 ordered summary hashes first:C292,C291,C290,
C289,C288..C274,using exact constants from immutable parent modules. Then invoke the exact C292
verify_artifacts(parent_dir,18 ancestor paths,accepted_execution_HEAD) under its no_neural guard.
The parent recursively reconstructs its own report and the full old masked gates and artifacts.
Read already-verified C291 dataset/triple/quad JSONs,then check canonical digests again:
- data 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
- triple 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;
- quad 86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.

The only direct repository import is C292. It yields C291 and its context:immutable C287 diagnostic,
C284 evaluator/strict replayer,C283 quad scorer,C282 TRAIN table builder and the core bundle.
All598 inherited source pins and1081 protected inputs are retained and checked. Require C292's
exact blob and every repository-local module exposed by the used contexts to be source-pinned.
Add OWN6 plus4 C292 summary/artifact files:source604;protected1091. No guessed direct-C count.

## Fixed gate,scientific workload and saved evidence

Freeze the final800-update state. Evaluate old length2/3/4 normal/evidence-blind/query-blind inputs.
Strict-load final checkpoints and repeat all evaluations;max drift<=1e-9 and identical argmax.
Primary PASS iff all5 support_weighted states pass EVERY original four-character criterion:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. No pooled substitution.
Report full seen-length/all-task gates,TRAIN/HOLDOUT direct gates,90 final partitions and360
candidate-versus-each-control contrasts. Add original full256-class output-role counts to all90
partitions using immutable C292 helpers;reconcile correct counts with the old scorer. No filtering.
Success is not automatically superiority,arbitrary-length competence,production adoption or Gate F.

15models,12000updates,576000training rows. Per model800 training+81 final+81 replay forwards.
Totals14430 forwards,809280 row presentations,57720 core calls. One15-state bundle write/load;
15 strict state loads,network0. Numerical loss/role work does not add model forwards. No latency
or memory advantage is claimed. Operational tests/preflight are separate from scientific counts.

Save architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json and full summary.json. Schemas:
fold-c293-support-models-v1 / fold-c293-support-eval-v1. Records contain frozen final raw logits
and all800 loss components/LRs,not only the final minibatch. Reconstruct results and histories
from saved data under no_neural guards;verify all output hashes and byte sizes. Console compact
receipt plus result aggregates;full maps/tensors stay local/ignored. No historical logger changes.

## Authoring and execution gate

OWN6:source,test,runner,launcher,preregistration,design. Own40/modules178/loaded4358/focused4357.
Only inherited exact C204 exclusion;accepted tests remain immutable. All text reads explicit UTF-8.
Manifest SHA256:0aadd3137b216f6e0fbc37feffe8b0ad947e48eeb22da881f38e58ee38a424f7.
Commit and re-fetch all6 OWN;independent post-authoring review before activation/command release.
Mandatory Windows Validate:19 parent hashes/full reconstruction,604/1091 protection,real tables,
all5 actual schedules,three identical initial models,support decomposition values/gradients,
own40 and focused4357. Dispatcher/selected launcher/runner ParseFile chain remains mandatory.
Validate failure skips science/publication. Integrity failure retries SAME C293 without science
changes. Valid primary miss is ACCEPTED VALID NEGATIVE. C294 unregistered until C293 judgment.
