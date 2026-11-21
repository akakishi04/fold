# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format (v2) in
`docs/experiment-conversation-handoff-protocol.md`.
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.
Entry:explicit PowerShell7, dispatcher ParseFile, tools/invoke_active_v2.ps1.
Accepted sources/tests/contracts/logs/protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C328 ACCEPTED VALID NEGATIVE. C329 ACTIVE / NOT YET JUDGED. C330 NOT REGISTERED.**
C327 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C326 remains VALID NEGATIVE.
All earlier verdicts are unchanged. Do not rerun C328 or earlier accepted experiments.
C329 authoring approval is not a scientific verdict or native full-regression PASS.
No production adoption is authorized.

## Latest accepted evidence -- C328

Acceptance commit:cc8881705867b748699dc9ce25a27a0a72d76d16.
Report:docs/experiment-ledger-addendum-c328-c329.md.
Scientific execution HEAD:3507021e46d47f6543316d46dc4481d3ead04855.
Publication commit:edf05c01e7fcd91b95c425fca5e7c416150689aa; its sole parent equals execution.
Published metadata/log:docs/experiment-run-logs/c328/latest.json and latest.log.
Log Git blob:72c877b8a03c7cb063612ca47f79ec12275bc15a.
Publisher-reported original Windows bytes:155434; SHA256:
826544d4cd7d9c3127723153c0de286b4c3c709e0f674533b0a92382d53fbbc9.

Full5722 tests/217 modules PASS; failures/errors/skips0;961.811seconds.
Ordered suite-ID SHA256:
28d0bab050e4101f2e6a757cd34d096ed6026325c294fbebaacb06b629aa7c37.
Native locks, parent saved semantics and all five native schedules passed.
All10 fits,5 identical800-update boundaries,10 checkpoint replays,1561 final uncached
rereads and fresh826-source/1561-input envelope verification passed. All exits zero;
run_execution_valid=true; scientific_status=FAIL; paired success0/5.
Interior complete gate0/5 in both arms; original2..6 retention0/5 in both arms.
Interior HOLDOUT normal answers1350->1261/1440 and both-query pairs639->576/720;
late_tenth worsened BOTH counts in every seed. Interior rescued/regressed answers40/129
and pairs19/82. Original pooled gains-53 answers/-49 pairs across all five seeds.
These are descriptive repeated-task totals, not independent sample counts. No pooled
result overrides a local/masked/order gate. The registered late-rate reduction is
not adopted; this does not show that all decay policies fail or that longer training
will succeed, nor does it establish a capacity limit or general LLM capability.

The reviewer read native execution records, all fits/prefix matches/replays, complete
seed flags and all five paired count records, then independently summed those counts.
No independent whole-Windows-log rehash or local model/logit recomputation is claimed.
Old C323/C324 attachments are not C328 evidence.

## C329 registration and completed post-authoring review

Experiment:C329-v5b-fixed-budget-extension. Stage:V5-B-FIXED-BUDGET-EXTENSION.
Contract:docs/experiment-ledger-addendum-c329-preregistration.md.
Review:docs/c329-post-authoring-review.md.
Source/preregistration review target:296b3c8e775f74284086dbb823a7fd29fd515b4a.
post_authoring_review = PASS.
Use the subsequent final activation HEAD supplied in the user command, not the
source-only target, acceptance commit or old C328 execution/publication HEAD.

All six committed own files were reread completely; returned Git blobs matched
independently hashed local tested bytes. After reread:normal48/48 PASS in9.526s and
CP932-default-text-open emulation48/48 PASS in14.455s; failures/errors/skips0.
UTF8/no-NUL/compile/import checks passed; recursive undefined globals0.
Author environment:Linux Python3.13.5/Torch2.10.0+cpu/NumPy2.3.5;two threads.
Real Torch2400-step toy, explicit reference arithmetic, Git/files/subprocess and
safe archive fixtures were executed. Parent/lease/science callbacks and inherited
suite inventory in the author fixtures were explicitly synthetic. These are NOT
native Windows, actual-parent FOLD training or full5770-regression results.
No author-side PowerShell AST execution is claimed; mandatory user-side AST checks
remain. The accepted C319 hook implementation was read to check snapshot state keys.

## C329 one question and fixed intervention

Does one extra fixed1200-update cycle at unchanged constant rates improve interior
binding while retaining original2..6, relative to the1200 state on the same trajectory?
This is a bounded training-budget test, not a claim inferred causally from C328.

Fresh initialization seeds329001..329005;order seeds329101..329105.
Arms:prefix1200(control),extended2400(candidate).
Train FIVE fresh models for2400 uninterrupted updates each, preserving deep-cloned
state_dict snapshots immediately after updates1200 and2400. These are TEN paired
checkpoints, not ten independently trained models. No accepted checkpoint initializes
training. The actual first1200 trajectory is shared by construction, not rerun.

At snapshot creation hash live model/optimizer before and after copying; require
unchanged values and nonaliased nonempty tensor storage. Before update1201 the same
live model/optimizer hashes must match the1200 receipt. Preserve optimizer identity,
moments and step counters. Recheck the stored1200 state after2400. No optimizer
reset/recreation, reseed, rate change, gradient detach or accepted-global patch.

Use unchanged C326 batch4 allocation on the1200-event schedule produced by the new
order seed, then execute exactly the same indices0..1199 once more. Do not modify
accepted fixed-length helper globals. Each update has24 intact query pairs/48 rows;
length4 updates have11..13 original pairs, not exact12/12. Per-row exposures in
original2/original3/original4/interior4 are100/100/50/50 at1200 and200/200/100/100 at2400.
Logical rows, targets, family proportions and ordering repeat; compute/exposure
intentionally double. It is NOT an equal-budget or new-shuffle comparison.

Native mean_last;14256 parameters including3328 core;64slots;192TRAIN/96HOLDOUT;
CPUfloat64,two threads,deterministic. C308 core_slow AdamW factory once per trajectory;
noncoreLR.005/coreLR.0005,betas(.9,.999),eps1e-8,weight_decay0,ordinary meanCE/globalclip1.
FIT_RNG612000 once per trajectory. All2400 rate/CE/gradient/event traces and snapshot
receipts are saved. There is NO intermediate evaluation or outcome-based stopping.
Finish ALL five trajectories before saving/reloading the10-state bundle and scoring.

ALL FIVE extended2400 states must pass full interior AND every original2..6 gate.
Per seed interior HOLDOUT answer AND both-query-pair gains must be strictly positive
versus prefix1200; pooled original2..6 gains in both counts must be nonnegative.
Unchanged local/masked/order thresholds.90/.80/.35/.35/.80;length1 descriptive only.
Perfect control saturation cannot pass strict superiority by a tie; report it,
never relax the criterion afterward. Retain complete cells and rescues/regressions.
No mean override, seed selection, extra budget search or threshold change.

Scientific work:5 trajectories,10 saved states,10 evaluation model instances,
12000 optimizer updates,576000 training-row presentations,15420 model forwards,
904320 total rows,61680 core forwards,20 checkpoint state loads,one bundle reload
and one new bundle write;network0. Both initial evaluation and replay use the saved
states. Each evaluation171forwards/16416rows/684core;each trajectory2400/115200/9600.
Preflight separately validates allfive schedules and one discarded native probe:
6forwards/2backward/12rows/0updates. Tests/verification/hash overhead are separate.
Raw saved-logit payload336199680bytes is not total serialized size or peak RAM.

Manifest SHA256:
9968ab6d8d2abdd3751b6ac1d1b1116a088d1c8abbdebdae50b580005d6fb7d8.
Seen templates/reused logical splits and paired checkpoints do not establish unseen
transfer, independent tasks, optimal budgets, capacity limits, general LLM capability,
Gate F passage or production adoption. A negative2400-budget result would not prove
that no larger budget could ever help.

## C329 parent semantics and complete protection

Immediate parent folder:runs/c328-late-rate-206451e9574c4b578b5cff4201af284b/.
Primary science/summary.json SHA256:
10bf430e74311a883cbcc7a7b70b589490a98d0f6db4458bcfe8be748fbccb53.
Mandatory companion execution-envelope.json SHA256:
d675bf546fb9d46eecf86b9a53847c5c054f4de618f311e0426a195c49f7cc32.

Parent schema:fold-c328-science-v1,statusFAIL,diagnostic_execution_valid=true,
candidate_gate=false. Parent envelope:fold-c328-execution-envelope-v1,scientific_statusFAIL.
Validate exact hashes,manifest/work,full5722receipt,completed saved semantics and
all1561 final rereads. Both records must have identical complete826/1561 unions.
C328's8 outputs plus primary/envelope add TEN immediate-parent files.
Read its canonical dataset/original/interior prompts, check hashes and prompt
semantics, and invoke unchanged C328.semantic_recheck(out,data,old,new,cx,read)
under no_neural. No parent forward or recursive ancestor semantic bodies, but all
older protected bytes remain checked. Do not use the C327 diagnostic loader schema.

Protection:832 sources=826+6 own;1577 inputs=1561+10 parent files+6 own.
All direct/lazy dependencies, accepted C308 optimizer/C319 hooks, C326 allocator,
C325 tables/C324 evaluator and recovery helpers/tests remain source pinned.
Native unchanged R4 Windows leases span worker phases; independent initial reference
hashes and ALL1577 final uncached rereads. No unlocked or cross-run cache fallback,
old-source modifications, artifact deletion or environment reinstall.

## Execution, outputs and stopping

Route:invoke_active_v2 -> invoke_c329 -> run_c329 -> c329_execution controller/worker
-> accepted_C328_composite_snapshot and saved semantics -> native_TRAIN_and_repeated_schedule_preflight
-> full_regression_unmodified_separate_process -> scientific_training_5_trajectories_10_snapshots
-> saved bundle reload and10 evaluations/10 replays -> saved_trajectory_reconstruction
-> final_uncached_input_recheck -> summary/envelope -> fresh byte verifier -> console push.

Full5770 tests/218 modules:5722 inherited+48 own;5771 before the sole inherited exact
C204 mutable-ACTIVE exclusion. No new exclusions/skips or cached test success.
Actual IDs/counts are checked;ordered digest printed. Regression runs in a separate
ordinary interpreter without scientific wrappers. Only all5770 success permits fitting.

Eight local science outputs:experiment-plan.json,dataset.json,original-prompts.json,
interior-prompts.json,trained-models.pt,evaluations.pt,measurements.json,validation-summary.json.
fold-c329-models-v1 stores10 ordered states;fold-c329-evaluations-v1 stores5 trajectories
and10 evaluation records. Saved reconstruction binds state hashes/receipts/traces and
metrics;it does not rerun all2400 historical optimizer steps. Hash/size-bind all eight
outputs before/after saved reconstruction and before summary/envelope writing.
Fresh verification checks all source/input/output bytes, complete maps, manifest,
parent identity, full test receipt and gate/count bindings without refitting.
Primary/envelope schemas:fold-c329-science-v1/fold-c329-execution-envelope-v1.

Local output:runs/c329-budget-<id>/science with enclosing execution-envelope.json,
regression-result.json and science/regression/verify logs. Publish console only to
 docs/experiment-run-logs/c329/latest.log and latest.json. Never publish tensors/data.
10second heartbeats;200update CE/rates;5 prefix_snapshot_preserved=PASS messages;
10 checkpoint_replay=PASS messages;complete seed/pair records;compact domain metrics.
Final:persisted_trajectory_evaluation=PASS -> execution_envelope_verified -> run_execution_valid=true.
Scientific PASS/FAIL is a separate question from execution validity.

Stale host/branch/HEAD,dirty tracked tree,nonunique ACTIVE,missing dependency or AST
failure SKIPS before scientific logging/publication. Source/input/test/schedule/
nonfinite/continuation/snapshot/replay/semantic/envelope failures stop SAME C329;
preserve evidence and do not retry automatically. Finite scientific FAIL with valid
execution is negative evidence. Publication-only failure is repaired without refitting.
No C330,CI,paid services,package installation,cache deletion or old-result edits.

The user may report only finished. Fetch remote latest metadata/log and separate
scientific execution HEAD from publication commit. Do not request old attachments.
For valid C329 complete acceptance AND next-C design/implementation/preregistration/
committed-byte review/activation/launcher in the SAME response. INVALID repairs SAME C329.
Do not advance the experiment branch for unrelated work during the user's ACTIVE run.

## History and inherited compatibility seal

Pre-acceptance handoff:docs/handoff-history/c328-pre-acceptance.md.
C328 acceptance and C329 implementation/registration are separate commits.
All older accepted/invalid records remain unchanged in existing documents/commits.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
