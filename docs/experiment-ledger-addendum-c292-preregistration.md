# C292 preregistration — saved answer-role audit

Experiment:C292-v5b-saved-answer-role-audit. Stage:V5-B-SAVED-ANSWER-ROLE-AUDIT.
Acceptance base:842e32a59bb5e3ef3f475554fb238c693139377e.
C291 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C293 NOT REGISTERED.

## One scientific question

Which C291 residual errors output the other fact's value,an absent known value,or a non-value byte,
and how does this vary across original value splits and objectives? These are observable output
roles,not claims of a hidden retrieval/attention mechanism. No further loss or optimizer sweep.

## Exact parent and data semantics

C291 execution:8d33edabbc7a91654a3da6056091cec2d84d9a24.
Published log:49f30351a7687884bf0b9a6f2ddd304de8c26d1e.
Summary:runs/c291-v5b-answer-margin-7f15f2dbf9ca4a16a2ba0ce2271a3421/summary.json.
Summary SHA256:271cc816f49fd7d53714508fee284bbf9f93783b3e74ac2728fc2a5286d740fa.
Parent source:fold_lm/v05_benchmarks/model_c291_answer_margin.py.
Parent Git blob:4257586769ffd9e810fd41d5bc0debea86dd087f.

Verify18 ordered summary hashes BEFORE dispatch:C291,C290,C289,C288..C274. Ancestor hashes come
from the immutable source-pinned C291/C290/C289 constants,not a mutable latest pointer. Invoke
C291.verify_artifacts(parent_dir,17 ancestors,accepted_execution_HEAD). It validates every one of
its eight artifact names/hash/size descriptors and reconstructs all original normal/masked gates,
loss traces,matching and replay metadata. The exact parent summary hash commits all descriptors.
Require FAIL,exact15 seed_results,all_replays/all_groups_matched True. Quad CE4/pair2/answer4;
seen tasks4/5/4;TRAIN direct5/5/5. No filtered model cohort.

Read the verified dataset.json and fold-c291-answer-margin-eval-v1 archive. Records contain frozen
final raw[task][split][profile][view] logits. They are not per-step losses or intermediate states.
C267.dataset assigns target=48+values[entities.index(query)];its renderer prints the two fact
values as decimal0..3. C270 triple and C283 quad rendering change only identifiers,not value
bindings;their prompt identities and targets were already checked by C291's parent chain.
C292 revalidates the canonical C267 data and target/value mapping before labeling output roles.
It never tries to decode arbitrary predicted byte values as UTF-8 text.

## Fixed observations and comparisons

Keep all15 models:seeds291001..291005;ce_only,pair_sum,answer_margin. All2/3/4 tasks,all3 profiles,
English/Japanese,and both original value splits. TRAIN/HOLDOUT are inherited value-combination
splits;quad TRAIN means TRAIN-valued examples at an UNTRAINED length,not optimized quad examples.
Analyze only original normal logits. Original evidence/query-blind gates remain under the exact
parent verifier;do not reinterpret or replace them using this diagnostic.

Classify each256-class argmax exactly once:
- target:the requested fact's value;
- other_fact:the other stated fact's value;
- absent_known_value:one of0..3 not present among these two facts;
- non_value_byte:any of the other252 output classes.
Facts have distinct values. These four classes are mutually exclusive and exhaustive. No model
output filtering,restricted argmax,temperature,threshold adjustment or post-hoc accuracy rescue.

Persist38880 row records=15models*3tasks*3profiles*(192+96). Each keeps source ID,query,entity/value
binding,fact order,language,profile,target,distractor,prediction and role. Reconstruct all540 original
profile/language normal totals,including collapse,against parent metrics before accepting the audit.
Report90 model/task/split aggregates and540 ordered-value-pair groups;include role counts and
explicit target/prediction confusion counts with denominators. Retain a540-group profile/language
view in the full local report. This is not a new capability gate.
Compare identical source/profile/task/split rows for answer_margin versus each of CE and pair_sum:
60 comparisons/25920 matched rows. Count exact argmax changes,correct-answer rescues/regressions
and the complete4x4 role-transition table. Equal role classes do not imply equal predictions.
Rows share models/data and are not independent statistical replicates or additional seeds.

## Workload,protection and verification

Scientific training,model forwards,model-state loads,new checkpoints,row presentations,core calls
and network calls are0. Existing tensor-file reads and numerical argmax/classification are allowed.
Module calls,load_state_dict and torch.save are blocked under no_grad. No checkpoint is loaded into
a model. Operational regression fixtures are separate from this zero-neural diagnostic workload.

Outputs:audit-plan.json,answer-role-report.json,validation-summary.json,plus full summary.json.
Every output is hash/size-verified and independently rebuilt from the accepted saved logits.
The console emits a compact receipt and aggregate tables;full row records and protected maps stay
local/ignored. No accepted logger or old log is changed. No new external dataset or paid API.

Retain every592 parent source pin and1066 protected input;add OWN6 and9 parent artifacts/summary:
source598/protected1081. Direct repository import is C291 only. Verify the exact parent blob and
that every repository-local module yielded by its context/core bundle is in the inherited map.
All reachable older modules remain protected by the parent's full immutable map and verifier.
Do not substitute a guessed C-number dependency count for direct source protection.
Own32;modules177;loaded4318;focused4317. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.

## Review,execution and stop

Commit,re-fetch and review source/test/runner/launcher/preregistration/design before activation.
Explicit UTF-8 reads are required;test the actual document inventory under a CP932-default
emulation without changing user settings. Check test IDs,embedded Python,CLI indices and globals.
Mandatory Windows Validate:all18 hashes,parent reconstruction,pins,full real-data classification
dry-run,own32 and focused4317. The dispatcher/launcher/runner ParseFile chain remains required.
Validate failure skips science/publication. Integrity failure retries SAME C292. PASS means only
saved-data integrity;capability_gate_applicable=False. C291 verdict and Gate F remain unchanged.
C293 is not registered before C292 formal judgment. No claim of causal memorization or attention
failure follows merely from the observed class distribution.
