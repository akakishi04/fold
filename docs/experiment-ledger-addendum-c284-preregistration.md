# C284 preregistration — maximum-training-length-matched comparison

Experiment:C284-v5b-max-length-matched-training.
Stage:V5-B-MAX-LENGTH-MATCHED-TRAINING.
Acceptance base:255ad0ed293b5e6b29266f761c5e6b862a9fca37.
C283 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C285 NOT REGISTERED.

## One question

At matched maximum training length3,architecture and800-update budget,does mixed two/three-character
training improve completely unseen four-character transfer over THREE-character-only training?
This removes the maximum-training-length difference present in C283. It does not isolate diversity
from changed repetition per length or curriculum timing;those are part of this coverage intervention.

## Immutable provenance

C283 scientific execution:24c4acd44905e1d3c4d2a019214eb588d72f9a93.
Published log:aedfa69557782b7484ee71128b08213a27d8798d.
Summary:runs/c283-v5b-frozen-four-bacee738e5a04007ae0f0f3093b0f5a7/summary.json.
Summary SHA256:609718db24ca6e3eda4f8916f04f56b24bff3621ddca4ebe136209617fad4949.
Parent source blob:2c204bbb5e8b53db5c2c1cd5202a0fcc5d4aa4a0.
Require parent FAIL,quad gatefalse,mixed_length3/5,two_char_only0/5,all_replays and all_weights_preserved.

Ten independent ordered summary hashes:C283,C282,C281,C280,C279,C278,C277,C276,C275,C274.
Their exact SHA256 values are the sealed SUMMARY_SHAS;all5 C283 artifact hashes/byte sizes are the
sealed PARENT_ARTIFACTS. The acceptance addendum records the same5 artifacts explicitly.
Use C283.verify_artifacts(parent_dir,nine ancestor paths,accepted execution_HEAD),with neural
Module calls,load_state_dict and torch.save blocked. Parent results are provenance,not training data.
C284 uses entirely fresh initialization,not C282/C283 checkpoint fine-tuning.

## Architecture and TRAIN exposure

Fresh seeds284001..284005;arms three_char_only,mixed_length.
Both use actual C278 all-token MeanFinalDualReadout with14256 parameters and48-token context.
Create the control once and deep-copy its complete initial state into independent candidate storage.
Use unchanged C282.training_tables:only normal TRAIN renderings of lengths2/3,shape[2,3,192,48].
No four-character data,ablated input or HOLDOUT values enters optimization. Model.forward sees only
rendered token tensors and zero task IDs;no length/profile/target metadata.

Same192 logical TRAIN rows,96 complete same-facts/different-query pairs and targets in both arms.
200 epochs x4 batches x48 rows;randperm96(seed+284000+epoch);profile=epoch%3.
Control:length1 every update (three characters). Candidate:length=epoch%2 (two then three).
Per-length/profile updates (rows2/3;columns0/1/2):
-control:[[0,0,0],[268,268,264]].
-candidate:[[136,132,132],[132,136,132]].
Every logical TRAIN row200 exposures total;control0/200 and candidate100/100 per length.
Both maximum training lengths3. No early stopping,best checkpoint,seed replacement or extra steps.
AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global gradient clip1;mean CE only.
Fit RNGseed+285000 reset per arm. CPU float64,2 threads,deterministic algorithms.

Logical dataset SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Triple prompt SHA256:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
Quad prompt SHA256:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
Renderers/scorers/support/model capacity remain unchanged;C283 supplies the quad dataset and scorer.

## Evaluation and primary gate

Only after update800,freeze the model and evaluate all two/three/four-character tasks.
Use unchanged C267/C270/C283 scorers,all value splits,profiles,languages,fact orders and mask views.
Then save/load final states strictly and replay all3 tasks at raw/argmax tolerance1e-9.
Evaluation must not change weights or expose quad/HOLDOUT examples to gradients.

Primary absolute gate is the same four-character criterion as C283:all FIVE mixed_length states
pass every four-character criterion. accuracy>=.90,query_pair>=.80,evidence_drop>=.35,
query_drop>=.35,two_order>=.80. Control cannot rescue or fail the candidate gate.
C284 seed_results.passed means quad_pass,not all_tasks_pass. Two/three/all-task gates are descriptive,
reported completely but do not change the four-character verdict. Never substitute a favorable
pooled metric for a failed cellwise gate. No Gate F promotion or revision of C282/C283 verdicts.

Comparative evidence is separate:report all5 paired seed quad pass states and all60 quad normal
correct/collapse contrasts (also120 descriptive two/three contrasts). Aggregate only with explicit
rows/pairs/seed denominators. A candidate absolute PASS can tie or lose to control;it alone does
not prove diversity superiority. Five seeds do not establish arbitrary-length/large-model behavior.

## Workload and persistence

10 fresh models;8000 updates;384000 training rows.
Per model:800 training+81 final evaluation+81 strict replay=962 forwards.
Totals9620 forwards,539520 row presentations,38480 core calls.
One10-state checkpoint bundle write/load;10 strict state loads;new_checkpoint_writes1.
Raw final-evaluation logits payload159252480 bytes before archive overhead. No network calls.
Training schedule and exact per-length/profile exposures are stored and reconstructed per state.

Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json.
Schemas:fold-c284-max-length-models-v1 and fold-c284-max-length-eval-v1.
New raw record stores task-keyed raw={two_char,triple,quad}. Only C284.analyze accepts this schema;
never dispatch C282/C283.analyze onto C284 records. Saved postcheck blocks new neural evaluation.

## Authoring/protection/runtime

OWN6:source,test,runner,launcher,preregistration,design. Accepted parent files stay immutable.
Source550=544+6;protected976=964+6 new parent inputs+6 OWN;dependency-union60.
The child's only direct repository import is C283;reachable C282/C278/C270/C267 and others remain
covered by inherited source/protection maps. Parent source identity is explicitly checked.
Own32;modules169;loaded4014;focused4013. Sole exact inherited C204 exclusion unchanged.
Build actual loader/suite and unique test-ID counts at runtime;do not assert numeric source strings.
Manifest SHA256:c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080.

Commit OWN6,fetch committed bytes and independently review before activation. Runtime Validate
checks parent artifacts,real training tables/maximum lengths/paired initial models,own32,focused4013
and required PowerShell syntax preflights before science/log publication. Authoring work is separate
from the scientific workload. Operational skip does not publish a scientific latest log.
Scientific integrity failure retries SAME C284;valid quad gate miss is ACCEPTED VALID NEGATIVE.
No gate/seed/schedule/optimizer change after result. C285 NOT REGISTERED until C284 is judged.
