# C296 preregistration — rendering-balanced minibatches

Experiment:C296-v5b-render-balanced-minibatches. Stage:V5-B-RENDER-BALANCED-MINIBATCHES.
Acceptance base:ae3705004c346edd7c29d1ee5708233d5b77b61d.
C295 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C297 NOT REGISTERED.

## One question

At an equal800-update budget,does mixing all six trained length/profile combinations inside
minibatches improve reliable unseen four-character transfer relative to rendering-homogeneous
batches,when each24-update block contains exactly the same rendered query pairs?
Fresh seeds296001..296005;blocked(control) versus balanced(candidate). Ordinary CE in both.
This is a new paired800-update experiment,not a revision of C295 or continuation of its weights.
C295 did not establish that rendering order caused its failures. Returning to the standard800
budget limits cost;both concurrent arms have identical budget and no claim compares new seed
counts directly with historical C295's1600 states.

## Exact intervention

Build the blocked plan from the original canonical192 logical TRAIN rows grouped into96 intact
same-facts/different-query pairs. For each of200 epochs,shuffle96 pairs using seed+296000+epoch;
use four batches of24 pairs. All rows in an epoch use length_index=epoch%2,profile_index=epoch%3.
The first792 updates comprise33 complete24-update blocks (six epochs each);eight updates remain.

Within each complete block,the candidate collects the96 pair events for each of the six rendering
combinations in their original order. For candidate update t=0..23,concatenate events4t:4t+4 from
each queue in sorted(length,profile) order. Thus every candidate minibatch has4 intact pairs per
combination (8 rows*6=48). No pair is split or relabeled. Each complete block has the identical
multiset of (length,profile,row0,row1) events in both arms. This is checked exactly,not inferred
from total counts. All final8 updates are byte-for-byte identical event plans in both arms.
This common tail avoids a different final-rendering exposure;it is fixed before any results.

Each logical row appears100 times at each trained length in both arms,with exactly the same
per-profile multiplicities as the blocked schedule. There are no new unique examples,labels,
lengths,values,epochs or optimizer updates. Only minibatch composition and ordering change.
These changes jointly affect gradient noise and correlations;this is not an isolated mechanism
experiment or a claim of catastrophic forgetting. Partial-block mixing is not attempted.

An int64[800,24,4] event tensor (length,profile,query-row0,query-row1) is saved per model with hashes,
33 exact block-multiset hashes,common-tail hash and exposure counts. Persisted validation rebuilds
all plans from canonical data and seed and checks tensor equality plus cross-arm matching.
Model inputs are gathered prefix tokens plus existing zero task IDs. No labels,rendering metadata,
pair IDs,support sets or oracle answers are passed into forward. Targets are loss-only.

## Held constant and gate

Actual C278 all-token MeanFinalDualReadout;14256 parameters;48-token context;CPUfloat64;
2threads;deterministic algorithms. Separate identical initial models per seed;strict fingerprints
and storage independence. Fit RNG seed+297000 reset separately per arm. First-input losses need
not match because the intended first minibatches differ. No false prefix-equivalence claim.
AdamW lr.005 constant,betas(.9,.999),eps1e-8,weight_decay0,clip1,error_if_nonfinite=True.
One optimizer800 updates/model. No auxiliary loss,LR decay,adaptive stop or checkpoint selection.
Train only normal two/three-character C267 TRAIN renderings supplied by C282.training_tables.
HOLDOUT,quad and ablated examples remain evaluation-only. Quad TRAIN means trained values at
an untrained length,not four-character learning.

Primary PASS iff all5 balanced models pass every original FOUR-character criterion:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. No threshold changes.
Report both arms' seen/all-task/direct TRAIN/HOLDOUT counts,60 final partitions,180 paired count
contrasts,original output roles and oracle conditional counts. The last are diagnostic only and
never replace predictions or gates. An absolute PASS is not automatic superiority or Gate F.
All5 seed pairs remain even when failed. No claim from dependent rows as additional trials.

## Parent writer,loader and protection

C295 accepted execution:c5ba373c0ed7e4699adc06cd2aac44624b4330e8.
Published log:e213d8b56093f9ef37b1d9aeafc1d0fcd4f209d0.
Summary:runs/c295-v5b-ce-budget-2361f7495977449a9c95d5dfff51d6ad/summary.json.
Summary SHA256:ea6e10cc0d0371b3dbf11316f37a794b97a7dbd1889053ce771644e9e96f10a5.
Parent source:fold_lm/v05_benchmarks/model_c295_ce_budget.py.
Parent Git blob:ae88e50e3aa77fb81b8dc800aee98cdb89276dab.
Verify22 ordered summary hashes BEFORE calling the exact C295.verify_artifacts with21 ancestor
paths and its accepted execution HEAD:C295,C294,C293,C292,C291,C290,C289,C288..C274.
The parent verifier checks its eight descriptors sealed by the exact summary hash,its ten
snapshots/five trajectories,all masked/full gates,replay metadata and schedules. Require FAIL,
exact parent seed results,common_trajectory and all_replays. Do not treat C295 as a three-arm run.
Read the verified C295 dataset/triple/quad JSONs and recheck canonical hashes. No parent weight is
loaded for training. The sole direct import is C295;its context exposes C294 numerical helpers,
C287 diagnostic normalizer,C284 evaluator/replayer,C283 quad scorer,C282 tables and the core bundle.
C284.evaluate receives a frozen eval model;replay_one strict-loads final states and checks all
views with tolerance1e-9,exact argmax and unchanged fingerprints. C294 measure/aggregate add only
arithmetic on frozen logits;their oracle counts remain non-capability diagnostics.

Retain/check all616 inherited source pins and1116 protected inputs. Used repository-local modules
exposed by the parent context/core must be pinned. Add OWN6 and9 C295 summary/artifact inputs:
source622/protected1131. Accepted sources/tests/dispatchers/logs remain immutable.
Own40/modules181/loaded4462/focused4461;sole inherited exact C204 exclusion unchanged.

## Workload,persistence and execution

Ten separately trained models*800=8000 updates;384000 training-row presentations.
Per model800 training+81 final evaluation+81 strict replay=962 forwards. Totals9620 forwards,
539520 row presentations,38480 core calls. One10-state checkpoint bundle write/load;10 strict
model-state loads;network0. Operational tests/preflight and inherited verification are separate.
No speed/memory claim:per-row rendering gathers differ from the old homogeneous indexing and
complete scientific costs must include all artifacts and temporary tensors.

Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus full summary.json.
Model schema:fold-c296-render-models-v1;eval schema:fold-c296-render-eval-v1 with10 frozen records.
Each fit stores all800 pre-update CE values and actual schedule_events. Final weights are saved
once and independently strict-replayed. Postcheck rebuilds every result from the saved logits,
canonical data and registered schedules under no-neural guards. Compact receipt and aggregates
are published;all tensors/weights/full protected maps remain local/ignored.

Manifest SHA256:b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9.
Commit/re-fetch all6 OWN and review before activation/command. Explicit UTF-8 reads;test CP932
emulation. Mandatory Windows Validate:22 parents,622/1131 protection,real gathered batches,all5
multiset/tail checks,initial models,own40 and actual4461 suite. Preserve ParseFile chain.
Validate failure skips science/publication. Integrity failure retries SAME C296. Valid gate miss
is ACCEPTED VALID NEGATIVE. C297 remains unregistered until C296 judgment. No Gate F promotion.
