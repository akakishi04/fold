# C295 preregistration — fixed CE training-budget extension

Experiment:C295-v5b-ce-training-budget. Stage:V5-B-CE-TRAINING-BUDGET.
Acceptance base:1ef1dd45252819d5925d78eaaea3d40b156aeda2.
C294 ACCEPTED PASS (diagnostic integrity only). C293 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C296 NOT REGISTERED.

## One question and changed variable

Does continuing ordinary CE from800 to1600 updates improve reliable untrained four-character
transfer when initial weights and all of the first800 updates are shared exactly?
No new loss or decoder intervention. This directly tests the fixed budget extension policy,
not a diagnosis that undertraining caused C294's errors. Per-state training work doubles;
there is no equal-compute superiority claim. More optimization can also degrade HOLDOUT.

Fresh seeds295001..295005. Each produces one uninterrupted1600-update trajectory with one AdamW.
Clone all tensor states immediately AFTER optimizer updates800 and1600;these are the two
preregistered arms ce800(control) and ce1600(candidate). No snapshot evaluation occurs between
updates,or until all five trajectories finish. Snapshot cloning/fingerprinting does not consume
RNG or reset optimizer state. Final comparisons use those exact saved states,never a selected best
intermediate model. Both checkpoints are kept even if either fails. No successful-seed filtering.
An independent800-update toy fixture verifies the long trajectory's prefix loss and weights exactly.

## Held constant and compute boundary

Actual C278 all-token MeanFinalDualReadout,14256 parameters,48-token context,CPUfloat64,
2threads,deterministic algorithms. Ordinary mean CE only;no auxiliary terms,hard support mask,
conditional decoder,coefficient search,LR decay or output filtering.
AdamW lr.005,betas(.9,.999),eps1e-8,weight_decay0,clip1,error_if_nonfinite=True.
One optimizer per trajectory;no restart/reinitialization at800.

Use original normal C267 TRAIN rows only,rendered at lengths2/3 via C282.training_tables.
192 logical rows/96 intact query pairs;24 pairs per batch;four batches per epoch.
400epochs*4=1600updates. randperm96(seed+295000+epoch);profile=epoch%3;length=epoch%2.
Reset fit RNG once to seed+296000. CE800 receives100 exposures/row at each length;CE1600 gets200.
The second half repeats the existing data with the predefined shuffle schedule;no HOLDOUT,quad
or masked input is optimized. TRAIN-value quad evaluation is still an unseen length.

Actual training work is5*1600=8000 updates,not the12000 obtained by summing overlapping800/1600
prefix lengths. Five trained models yield ten evaluated states;the two states of a seed are not
independent replicates. Training rows384000. Each state receives81 original evaluation forwards
and81 strict-replay forwards:total9620 forwards,539520 row presentations,38480 core calls.
One ten-state checkpoint bundle write/load;20 model-state loads (ten in-memory snapshot evaluations
plus ten archive replays). New model initialization has no model forwards. Evaluation archives
are not model-checkpoint writes. Report real operation counts,not fictional independent controls.
Operational tests/preflight and old-parent numerical reconstruction are separate from these counts.

## Parent writer/schema and dependency audit contract

Accepted C294 execution:dead7ca153a8aadb6f30135f47a59981e4b4dfcf.
Published log:de959a8147df888a6d51234fad7971f4593d25a2.
Summary:runs/c294-v5b-support-choice-79d31882e59f46fe933bb7e863bad8e2/summary.json.
Summary SHA256:abdf1b71f56e3f452d3955277a659722ca38f95a47be1dc6ca5330e688e37e10.
Parent source:fold_lm/v05_benchmarks/model_c294_saved_support_choice_audit.py.
Parent blob:c645e0b62eba41c6f48fa140fa26f8cc3a26e3b9. All3 names/hash/size descriptors fixed in source.
Verify21 ordered summary hashes BEFORE exact C294.verify_artifacts dispatch:
C294,C293,C292,C291,C290,C289,C288..C274. The remaining hashes are immutable ancestor constants.
The C294 verifier accepts20 ancestor paths and its accepted execution HEAD;it reconstructs the
complete parent report and every original masked/full gate without neural execution. C294 is a
diagnostic,not a checkpoint. Require diagnostic PASS and capability_gate_applicable=False.

Read verified C293 data/triple/quad JSONs,then recheck canonical hashes:
-data1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
-triple432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;
-quad86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
All new weights start fresh. No parent model is continued. C294.context yields C293 and the core
bundle;C293.context yields the immutable C287 normalizer,C284 evaluator/replayer,C283 quad scorer,
C282 table builder and core bundle. C284.evaluate requires frozen eval mode;replay_one strict-loads
and compares original full logits<=1e-9 and exact argmax. C295 uses it for each saved state.
The only direct repository import is C294. Retain all610 source pins/1106 protected inputs,check
its exact blob and used repository-local context/core modules. Add OWN6 plus4 C294 files:
source616/protected1116. No accepted code/test/preregistration/log/dispatcher is changed.

## Gates and descriptive metrics

Primary PASS iff all5 ce1600 snapshots pass every original FOUR-character fixed criterion:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. No gate change.
Report CE800/CE1600 seen-length/all-task and direct TRAIN/HOLDOUT counts,60 final partitions,
180 paired count contrasts,output roles and oracle conditional counts. The latter use C294's
measure/aggregate helpers strictly as diagnostics and never decide a capability gate. This reuse
adds only arithmetic on already scored logits,not training or forwards. Reconcile original counts.
Absolute candidate PASS is not automatic superiority overCE800,arbitrary-length generalization,
production adoption or Gate F completion. Do not infer that extra training is always beneficial.

## Persistence and validation

Save architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json.
Model bundle schema:fold-c295-budget-states-v1;identities ordered seed,ce800/ce1600;10 states.
Evaluation schema:fold-c295-budget-eval-v1;10 frozen result records plus5 full1600-step trajectories.
Each trajectory keeps initial/snapshot fingerprints,CE history,prefix-history hash,optimizer count,
training-row count and exact schedule hashes/exposures. Checkpoints are after optimizer steps;
CE histories are per-training-minibatch BEFORE that step,not final corpus losses.

Independent strict archive replay compares every normal/evidence-blind/query-blind output against
the evaluation of in-memory snapshots. Postcheck validates every artifact hash/size and reconstructs
results from saved logits and trajectories under the parent's no_neural guard. All prospective
scientific conditions are fixed;no invalid-run condition relaxation. Compact console receipt and
aggregates;full maps/logits/weights remain local/ignored.

OWN6 source/test/runner/launcher/preregistration/design. Own32/modules180/loaded4422/focused4421.
Only inherited exact C204 exclusion. Explicit UTF-8 text reads;CP932-default emulation test.
Manifest SHA256:b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.
Commit,re-fetch all6 OWN and independently review before activation and user command release.
Mandatory Windows Validate:21 hashes/full parents,616/1116 pins,real training tables,all5 exact
800/1600 schedule prefixes,actual initial model,own32 and full4421 suite. Preserve dispatcher,
launcher and runner ParseFile chain. Validate failure skips science/publish. Scientific integrity
failure retries SAME C295;valid gate miss is ACCEPTED VALID NEGATIVE. C296 stays unregistered.
