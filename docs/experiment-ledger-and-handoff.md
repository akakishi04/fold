# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C294 ACCEPTED PASS (diagnostic integrity only). C295 ACTIVE / NOT YET JUDGED. C296 NOT REGISTERED.**
C293 remains ACCEPTED VALID NEGATIVE. C295 is the unique ACTIVE CE training-budget comparison.
Latest accepted scientific execution:dead7ca153a8aadb6f30135f47a59981e4b4dfcf.
Latest accepted published log:de959a8147df888a6d51234fad7971f4593d25a2.
Do not rerun C294. RESULT_ALREADY_PUBLISHED correctly blocked a duplicate old command.

## Latest accepted evidence — C294

Acceptance:docs/experiment-ledger-addendum-c294-c295.md.
Acceptance commit:1ef1dd45252819d5925d78eaaea3d40b156aeda2.
Summary:runs/c294-v5b-support-choice-79d31882e59f46fe933bb7e863bad8e2/summary.json.
Summary SHA256:abdf1b71f56e3f452d3955277a659722ca38f95a47be1dc6ca5330e688e37e10.
Own32/focused4389 PASS;610/1106 protection;run_execution_valid=True.
Manifest:e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.
Candidate293004 HOLDOUT full/conditional correct:two259/276,triple253/269,quad239/255 out of288.
Quad candidate has16 outside-but-correct-choice,24 outside-and-wrong-choice,9 other-fact errors.
Even oracle support leaves33 errors. Candidate quad TRAIN-value has26 other-fact errors and no
outside errors. The two-choice oracle is diagnostic only;no decoder/gate changes or causal proof.
C293 gates remain CE2/scaled1/support2. Gate F NOT PASSED regardless of conditional accuracy.

## Active C295 — fixed CE800/CE1600 snapshots

Experiment:C295-v5b-ce-training-budget. Stage:V5-B-CE-TRAINING-BUDGET.
Registration:docs/experiment-ledger-addendum-c295-preregistration.md.
Design:docs/v5b-ce-training-budget-v0.1.md.
Review:docs/c295-post-authoring-review.md.
Acceptance base:1ef1dd45252819d5925d78eaaea3d40b156aeda2.
Authoring/review target:0bcfc7de56bef1d0b9b0f949b038224ef6eaa992.

One question:does continuing ordinary CE from800 to1600 updates improve reliable untrained
four-character transfer with exactly the same first800 updates? New seeds295001..295005.
Five uninterrupted1600-update trajectories,one AdamW each. Copy weights immediately after
updates800(control ce800) and1600(candidate ce1600). No evaluation before all five trajectories
finish. No optimizer reset,adaptive stopping,best-checkpoint selection or failed-seed filtering.
These are ten dependent timepoint states of five trained models,not ten independent models.
The candidate gets double per-state training;no equal-compute superiority is claimed.

Actual C278 all-token MeanFinalDualReadout,14256 parameters,48-token context,CPUfloat64,
2threads,deterministic. Mean CE only;no auxiliary loss,LR decay or restricted decoder.
AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1,error_if_nonfinite=True.
Normal two/three-character TRAIN only;192 logical rows,96 intact query pairs,48 rows/batch.
400epochs*4=1600updates;randperm96(seed+295000+epoch);profile=epoch%3;length=epoch%2.
Reset fit RNG once to seed+296000. CE800 has100 exposures/row at each length;CE1600 has200.
No new data,HOLDOUT,quad or ablated input enters optimization. Quad remains an unseen length.

Verify21 ordered parent hashes before exact C294.verify_artifacts with20 ancestor paths and
accepted execution HEAD. The C294 diagnostic summary and3 output descriptors are pinned;
read only recursively verified C293 data/triple/quad JSONs and recheck their canonical digests.
Do not use a diagnostic as a checkpoint loader or continue old C293 model weights.
The direct import is C294;retain all610 inherited pins and1106 inputs and verify used context/core
module coverage. Add OWN6 plus4 C294 summary/artifacts:source616/protected1116.

All original normal/evidence-blind/query-blind two/three/quad criteria remain. Primary PASS iff
ALL5 ce1600 states pass EVERY original FOUR-character criterion. Thresholds:accuracy.90,
query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Seen/all-task/direct TRAIN/HOLDOUT
counts are descriptive. Report60 final partitions and180 paired count contrasts. Output-role
and oracle conditional counts remain diagnostics,not new gates or altered predictions.
Freeze in-memory snapshots and evaluate;strict-load independent archive copies and replay
all tasks/views with drift<=1e-9,exact argmax and unchanged fingerprints. Save both states.

Actual workload:5trajectories,10evaluated states,8000updates,384000training rows,9620forwards,
539520row presentations,38480core calls,one10-state archive write/load,20state loads,network0.
Do not double-count common training prefixes as12000 updates. Operational tests are separate.
Persist8 artifacts plus summary:architecture-plan.json,dataset.json,triple-dataset.json,
quad-dataset.json,trained-models.pt,evaluations.pt,measurements.json,validation-summary.json.
Bundle schema:fold-c295-budget-states-v1. Evaluation schema:fold-c295-budget-eval-v1 with10records
plus5full1600-update trajectories and exact snapshot/prefix fingerprints. Per-step CE is not
final corpus loss. Console compact receipt+aggregates;full maps/logits/weights stay local/ignored.

Own32/modules180/loaded4422/focused4421. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.
No prior verdict,production runtime or Gate F promotion changes automatically with C295.
An improvement is evidence about the fixed extension policy,not proof of an earlier hidden cause.

## Post-authoring review and authoritative runtime boundary

post_authoring_review=PASS (committed-byte/static plus local behavioral fixtures).
All6 OWN files re-fetched at0bcfc7de56bef1d0b9b0f949b038224ef6eaa992;whole-file blobs matched6/6.
After matching:normal own32 PASS in6.805s;entire CP932-emulated own32 PASS in6.590s.
Linux/Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;custom
globals0;UTF-8/no-NUL;manifest matches. Actual toy1600 and standalone800 fits have identical
prefix losses and800state tensors;optimizer spy confirms one uninterrupted1600-step optimizer.
Fixtures verify snapshots,scoring calls,parent hashes,protection,counts,gates and persistence.
Synthetic target-encoded toy input verifies control/numerics,not FOLD binding/generalization.
Parent archives,Git,old scorers/models and inherited suite members are mocked where needed.
Real Windows21-parent verification,pins,PowerShell parsing,real model/table preflight,full4421
suite,and real FOLD training/replay remain mandatory local Validate/Execute gates.
Activation must preserve all six reviewed OWN blobs and all accepted files/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C295 -> Validate(21parent hashes,
616/1116 source/input protection,real tables/all5 schedule prefixes/initial model,own32,
focused4421) -> authoring_runtime_preflight=PASS -> Execute(5trajectories*1600updates,
10frozen snapshots,strict archive replay,persisted reconstruction) -> log publication.
Validate failure skips science/publication. Any scientific integrity failure retries SAME C295.
Valid all-five miss is ACCEPTED VALID NEGATIVE;do not retune budgets,seeds,LR,thresholds or
select other checkpoints after seeing results. C296 is unregistered until C295 formal judgment.
Keep scientific execution HEAD separate from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep the accepted legacy seal. Historical tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c294-pre-acceptance.md.
Git blob79a5c1cc8d471e47ef143c7dd8d46c93361bc491. Accepted sources/tests/logs remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
