# C346 preregistration: pair-max learning-rate comparison

Date: 2026-11-22 Japan time.
Experiment: C346-v5b-pair-max-rate.
Stage: V5-B-PAIR-MAX-RATE.
Acceptance base: f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2.
Manifest SHA256: 8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64.

This file is part of seven new OWN files. Registration source and an independent
review of the committed remote bytes must precede activation. The later reviewed
documentation-only activation HEAD is the user ExpectedHead. Do not execute an
unreviewed source commit or a main merge.

## One scientific question

Does halving both AdamW learning-rate groups from initialization make pair-max
training improve interior answer/query-pair correctness while retaining every
registered domain relative to default-rate pair-max and ordinary mean CE?

C345 found higher terminal interior mean CE and pair-max in all ten seed/split
comparisons,with worse answers in the major failing seeds. It did not prove that
the learning rate,clipping or a particular optimizer mechanism caused the failure.
The factor0.5 is one prospectively fixed intervention,not an optimum derived from
C345 and not a coefficient search. C286/C328 late-rate results remain valid negatives
under their different objective/timing;no past verdict is replaced.

## Changed and held constant

Three arms at every fresh seed:

|Arm|Selected objective|Noncore LR|Core LR|Role|
|---|---|---:|---:|---|
|mean_ce|Mean full256 CE across48answers|0.005|0.0005|Strong ordinary-CE reference|
|pair_max|Mean of24within-query-pair maximum full256 CE|0.005|0.0005|Matched default-rate pair-max control|
|pair_max_half_rate|Same pair-max reduction|0.0025|0.00025|Candidate|

The isolated intervention is the fixed learning-rate scale within the pair-max
comparison. Same-state pair-max losses and gradients must agree between those two
arms before applying the rate policy. No loss scaling,auxiliary penalty,change in
clipping,rate warmup/decay,optimizer restart or post-result coefficient change.
Actual later update vectors need not be exactly half: later gradients/moments/states
differ. The declaration concerns optimizer group rates.

The ordinary-CE reference prevents interpreting improvement over a weak pair-max
control alone as retention of the existing baseline. There is no mean-CE half-rate
arm,so no objective-by-rate interaction,universal half-rate benefit or optimal-rate
claim. A15-model policy comparison is not a complete factorial design.

Fresh initialization seeds346001..346005;paired order seeds346101..346105.
All three arms share exact common initial states,canonical event order,actual input
tokens/targets and exposures. No accepted C344 learned state initializes a fit.
The authored logical task family is reused;fresh seeds do not create an untouched
external benchmark or independent language examples.

Architecture: native mean+last dual reader,14256parameters/core3328,64slots,
full256byte-class outputs,CPUfloat64,threads2. Optimizer AdamW betas(.9,.999),
eps1e-8,weight_decay0,global gradient clip1,one continuous optimizer/model.
Same2400updates: a fixed1200event cycle repeated twice;48rows/24completequery pairs
per update. All15fits finish before normal/masked/order evaluation and replay.

## Data and actual exposure

Canonical192TRAIN/96HOLDOUT logical rows,three profiles,both languages and fact orders.
Use the immutable mixed45 allocation and canonical banks from the accepted lineage.
Validate literal pair metadata and complete distinct counterpart queries/targets,
not merely even batch size or arbitrary row adjacency.

|Domain|Presentations per logical TRAIN row over2400updates|
|---|---:|
|original2|200|
|original3|200|
|original4|50|
|original5|50|
|original6|0|
|interior4|100|

These are per-model rates across the registered profiles,not sums across seeds.
HOLDOUT and masked examples are never fitted. TRAIN labels refer to value-combination
partitions;original6TRAIN names/prompts have zero fitting exposure. Original1 remains
descriptive and cannot rescue the registered original2..6/interior4 gate.
Each model uses115200training rows and3168000nonpadding tokens including BOS/EOS.
Equal updates/rows/tokens do not establish equal measured wall-clock or FLOPs.

## Fixed gate and complete reporting

Retain the inherited local accuracy>=.90,query-pair>=.80,evidence-mask drop>=.35,
query-mask drop>=.35 and both-order>=.80 criteria with their exact scorer semantics.
Candidate gate is the conjunction of four separately reported components:

1. All five candidate states pass every original2..6 and interior4 complete gate.
2. Candidate minus defaultpair-max normal answer AND both-query-correct counts are
   nonnegative for EACH5seeds x6domains x2splits:120inequalities.
3. The same120inequalities hold against ordinary mean CE.
4. Aggregate interior gains against defaultpair-max are strictly positive for all
   four endpoints:TRAIN answers,TRAIN query pairs,HOLDOUT answers,HOLDOUT query pairs.

Total retention inequalities240;two controls yield120seed/domain/split contrasts.
Keep all five seeds and all strata. Report candidate eligible count,each control's
full-pass set,each comparator's nonregression failures,and all four strict gains.
If default-rate pair-max is already perfect at a strict endpoint,there is no accuracy headroom;
the superiority conjunction remains a valid negative. Do not replace seeds,extend
training,relax a threshold or rerun to manufacture headroom.

Record answer/pair rescues,regressions and support partitions for both splits and
both controls. A composite FAIL does not imply the intervention had no useful
effect;describe which subgate failed and which paired outcomes improved.

Compute terminal mean CE and pair-max from all saved normal full256logits at every
state/domain/split:180summaries,77760answers/38880query pairs. Use exact metadata
pairing and full-class first-index argmax. Report both same-metric loss deltas for
all120candidate/control contrasts. These losses are diagnostic,not desired-sign
gate conditions;capability PASS does not itself imply lower loss or convergence.
Domain/split means are not the exposure-weighted whole-training objective.

Persist each preupdate mean CE,pair-max,selected objective,preclip norm and optimizer
rates. The two pair-max arms select exactly the same reduction. A norm>1 threshold
is not an exact clipping-call count or an actual update-magnitude measure. Slot4
mixesoriginal4/original5/interior4;its batch loss is not an interior-only measure.

## Scientific work and outputs

15training/evaluation states;15optimizers;36000updates/gradient calls/optimizer steps;
1728000training rows;41130model forwards;2220480total row presentations;
164520core forwards;82260query-projection calls;30strict state loads;
one checkpoint-bundle load and one new bundle write;network0.
Raw saved logit payload1008599040bytes. Preflight,parent verification and regression
fixtures are separately accounted;do not hide them inside the scientific counters.

Expected six local-only science outputs:
experiment-plan.json,training-traces.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json. Primaryscience/summary.json and the
execution envelope bind these exact files and their hashes. No datasets,tensors,
checkpoints or generated run outputs enter Git;only dedicated console logs/receipt
are mirrored under docs/experiment-run-logs/c346/.

## Immediate parent and protection

Parent is the accepted C345 diagnostic,not a C344 training-schema substitute.
Executionc81ffe102c3a9280f28a68e572403549ce77fa1d;
publication25ff2f93ce63c9668f3111672caf75db095d2f45.
Folder:runs/c345-saved-objective-audit-749db4a6ede44b608c06ee1461b6e393/.
Primarycfc3fe5b8f4ec927d875e2a016a940b5d34aac9ef14d93644eeb26567c0e1f30.
Envelopee883c26d1df24d940cd51b551f06e46e7ac69da216ea6024dc299ee24d2cceab.
Require fold-c345-diagnostic-v1/fold-c345-execution-envelope-v1,PASS,valid,
capability_gate_applicable=false,and preserved nested C344negative/eligible2.

C345 semantic_recheck(out345,out344,data_out,cx,read) takes5arguments underno_neural.
The new C346 training ABI is native_preflight(data_out,cx,root,pins,read)5arguments,
run_training(out,data_out,cx,root,pins,read)6,and
semantic_recheck(out,data_out,cx,read)4. Training runs outside no_neural;parent and
saved arithmetic checks run inside it. The actual deciding model dependency path
must remain pinned,including lazy helper imports.

Protect all491C345outputs:4science+primary+envelope+485proofs(3+241JSON/logpairs).
New total944sources=937+7OWN;9177inputs=8679+491+7. Retain complete inherited maps,
native lease capacity9177,all9177finaluncached rereads;no eviction/unlocked fallback.
Accepted sources/tests/launchers/preregistrations remain unchanged.

## Regression and native execution

OWN74tests=48science+26execution. Full6652tests/243isolated modules;
the parent6578IDs/241groups must remain an exact ordered prefix. Actual loader
counts and ordered IDs must be audited before activation,not source-literal guessed.
Actual loader6653candidates minus the sole inherited exclusion gives6652selectedIDs.
Full ID SHA256: 39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Inherited parent IDs:2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Sole inherited exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusion,skip or accepted-test change. Successor retains497outputs under
the six-science/243module inventory:6+primary+envelope+3+486proof files.

Existing .venv-py31315:Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5;
CPUfloat64,threads2. No environment upgrade.
Route:invoke_active_v2->invoke_c346->run_c346->c346_execution.
Branch feat/sft-target-loss;run prefix runs/c346-pair-max-rate-<id>/.
Wrongbranch/dirtytrackedtree/staleExpectedHead/nonunique-or-wrongACTIVE/AST failure
skips before experiment logging or publication. Parse dispatcher in the standard
user block and selected launcher/runner before execution.

C346-R0 reuses C344-R1timeout-cleanup implementation through the explicit C345
parent-helper bridge. Receipt keeps the implementation schema but binds C346HEAD;
the C345parent receipt remains bound to its own original execution.
Six native cleanup checks precede lease/snapshot/parent checks. Native schedule,
pair/stream/model/backward preflight must complete before full regression/fitting.
This separate preflight checks all five schedules and uses one discarded native
model with three zero-step optimizer configurations:24forwards,96row presentations,
12backwards and zero optimizer updates. It covers all three arms,both cycles,both
families and English/Japanese query pairs. These calls are outside scientific WORK.
Then6652tests/243processes,all15fits,evaluation/replay,saved reconstruction,
9177finalrereads,separate fresh verifier and dedicated log publication.

## Stop and next response

Fetch remote latest.json/latest.log;distinguish execution HEAD and publicationcommit.
Any missing source/protected input,wrong schema,nonfinite,failed/skipped test,
broken replay/receipt or absent final fresh verification is INVALID/RETRY SAME C346.
No automatic retry or ancestor retraining. Valid scientific FAIL is accepted negative
under the unchanged gate. Do not claim Gate F or production adoption even onPASS.
After valid judgment prepare the next one-question experiment under the conversation
protocol;C347 is not registered here. Review PASS is required before issuing a command.
