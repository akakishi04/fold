# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C295 ACCEPTED VALID NEGATIVE. C296 ACTIVE / NOT YET JUDGED. C297 NOT REGISTERED.**
C294 remains diagnostic ACCEPTED PASS. C296 is the unique ACTIVE rendering-batch comparison.
Latest accepted scientific execution:c5ba373c0ed7e4699adc06cd2aac44624b4330e8.
Latest accepted published log:e213d8b56093f9ef37b1d9aeafc1d0fcd4f209d0.
Do not rerun C295,extend it further or select alternative checkpoints.

## Latest accepted evidence — C295

Acceptance:docs/experiment-ledger-addendum-c295-c296.md.
Acceptance commit:ae3705004c346edd7c29d1ee5708233d5b77b61d.
Summary:runs/c295-v5b-ce-budget-2361f7495977449a9c95d5dfff51d6ad/summary.json.
Summary SHA256:ea6e10cc0d0371b3dbf11316f37a794b97a7dbd1889053ce771644e9e96f10a5.
Own32/focused4421 PASS;616/1116 protection;run_execution_valid=True.
Manifest:b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.
Quad ce8001/5,ce16002/5. Seen tasks/TRAIN/HOLDOUT direct3/5 at both times.
295004's one quad HOLDOUT error disappears;295002/295003 remain failed even on TRAIN.
295002 HOLDOUT correct counts decline;295003 HOLDOUT NLL increases. No universal benefit.
Five uninterrupted trajectories,ten paired timepoint states;not ten independent models.
No Gate F promotion,model adoption or causal attribution to limited training budget.

## Active C296 — rendering-balanced minibatches

Experiment:C296-v5b-render-balanced-minibatches. Stage:V5-B-RENDER-BALANCED-MINIBATCHES.
Registration:docs/experiment-ledger-addendum-c296-preregistration.md.
Design:docs/v5b-render-balanced-minibatches-v0.1.md.
Review:docs/c296-post-authoring-review.md.
Acceptance base:ae3705004c346edd7c29d1ee5708233d5b77b61d.
Authoring/review target:128824681fd3cef51246153a817a6060f833a7ba.

One question:at the same800-update budget,does mixing existing length/profile renderings inside
minibatches improve reliable quad transfer versus the homogeneous-rendering batching policy?
Fresh seeds296001..296005;blocked(control) and balanced(candidate). Ten independent model instances,
paired by seed with identical initial weights. No parent checkpoint continuation or success selection.

Blocked schedule:canonical192 normal TRAIN rows grouped into96 intact query pairs;200epochs*4
minibatches of24pairs. randperm96(seed+296000+epoch);length=epoch%2;profile=epoch%3.
First792 updates are33 complete24-update blocks,each containing all six renderings.
Balanced schedule:within each block,keep six stable rendering queues of96 pairs each;each update
concatenates four consecutive pairs from each queue in sorted(length,profile) order. Every mixed
batch has48 rows (eight per rendering). Verify exact event multiset equality per block and globally.
All final8 updates have identical event plans in both arms. Every logical row has100 exposures
at each trained length,with unchanged per-profile multiplicities. No new data,label or budget.
Actual int64[800,24,4] events are persisted per fit and independently reconstructed at postcheck.
Ordering and within-batch composition change jointly;do not infer a uniquely causal mechanism.

Actual C278 all-token MeanFinalDualReadout,14256 parameters,48tokens,CPUfloat64,2threads,deterministic.
Ordinary mean CE only,AdamWlr.005 constant,betas.9/.999,eps1e-8,weight_decay0,clip1.
One optimizer800updates/model;fit RNGseed+297000 reset per arm. No LR decay or auxiliary losses.
Models receive prefix tokens and existing zero task IDs only,not rendering metadata or targets.
No four-character,HOLDOUT or ablated examples are optimized. No adaptive stop/checkpoint selection.
This is a fresh matched800-update experiment,not an altered C295 or a historical1600-vs800 claim.

Verify22 ordered parent hashes before exact C295.verify_artifacts with21 ancestor paths and its
accepted execution HEAD. The exact summary commits all eight parent descriptors and the verifier
reconstructs its ten timepoint records/five trajectories,all gates and replay metadata.
Require FAIL,exact parent results,common_trajectory and all_replays. Read verified C295 input JSONs
and check canonical hashes again. Sole direct import C295;retain/check all616 inherited pins and
1116 input hashes plus coverage of repository-local context/core helpers. Add OWN6 and nine
parent summary/artifact files:source622/protected1131. No accepted dependency repair or waiver.

Freeze each final model,evaluate original two/three/quad tasks with normal/evidence-blind/query-blind
views,strict-load archive states and replay all logits<=1e-9 with exact argmax. Primary PASS iff ALL5
balanced states pass EVERY original quad criterion:accuracy.90,query_pair.80,evidence_drop.35,
query_drop.35,two_order.80. No pooled-accuracy substitution or gate relaxation. Save seen/all-task/
direct TRAIN/HOLDOUT counts,60 partitions and180 paired contrasts. C294 output-role/conditional
counts remain numerical diagnostics,not a decoder or capability gate.

Work:10models,8000updates,384000training rows,9620forwards,539520row presentations,38480core calls,
one10-state checkpoint write/load,10strict state loads,network0. Operational tests are separate.
Eight artifacts plus summary:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Model schema
fold-c296-render-models-v1;evaluation schema fold-c296-render-eval-v1. Retain all800 CE values and
actual schedule events. Full tensors/maps remain local/ignored;console compact receipt+aggregates.
Own40/modules181/loaded4462/focused4461;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local behavioral fixtures).
All6 OWN files re-fetched at128824681fd3cef51246153a817a6060f833a7ba;whole-file blobs matched6/6.
After matching,normal own40 PASS in16.582s;entire CP932-emulated own40 PASS in17.273s.
Linux/Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;unresolved
custom globals0;UTF-8/no-NUL;manifest self-hash matches. Actual schedules for all5 seeds verify
exact multisets/tail/exposures;toy800-step fits check ordinaryCE,optimizer continuity and reproducibility.
Additional fixtures cover parent hashes,protection,roles,counts,gates,run ordering and persistence.
The toy inputs encode targets for control tests;these are NOT FOLD binding/generalization results.
Parent archives,Git,old models/scorers and synthetic suite members are substituted where needed.
Real Windows22-parent reconstruction,pins,PowerShell parsing,actual4461 suite,and ten FOLD
training/evaluation/replay runs remain mandatory local Validate/Execute checks.
Activation must preserve reviewed OWN6 and accepted code/tests/logs/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C296 -> Validate(22parent hashes,
622/1131 protection,real gathered batches/all5 multiset-tail schedules/initial models,own40,
focused4461) -> authoring_runtime_preflight=PASS -> Execute(10models*800updates,
frozen evaluation,strict replay,schedule/result reconstruction) -> log publication.
Validate failure skips science/publication. Any scientific integrity issue retries SAME C296.
Valid all-five miss is ACCEPTED VALID NEGATIVE. Do not change seeds,batch policy,tail,budget,LR,
thresholds or select successful models after results. C297 is unregistered until C296 judgment.
Gate F remains NOT PASSED. Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep the accepted legacy seal. Historical tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c295-pre-acceptance.md.
Git blob57f79ee235747822a3360a2c31abf777ad57056e. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
