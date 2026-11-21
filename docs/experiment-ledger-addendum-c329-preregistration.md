# C329 preregistration -- fixed uninterrupted training-budget extension

Date: 2026-10-17 Japan time.
Experiment: C329-v5b-fixed-budget-extension; stage: V5-B-FIXED-BUDGET-EXTENSION.
Acceptance base: cc8881705867b748699dc9ce25a27a0a72d76d16.
C328 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C330 NOT REGISTERED.
This protected contract does not authorize execution before separate committed-byte
review and ACTIVE registration. No existing accepted code/test/log/contract changes.

## One scientific question

Does one extra fixed1200-update cycle, with constant native C308 core_slow rates,
improve interior binding while retaining original2..6 on the same trajectory,
relative to the1200-update checkpoint? The endpoint is fixed at2400 before fitting.
C328's late-tenth policy worsened interior answer and pair counts in every seed.
That motivates rejecting this particular decay policy, not claiming longer training
will work. This is a single bounded budget test, not a budget/schedule/seed search.

## Paired checkpoints, not ten independent fits

Fresh initialization seeds329001..329005 and order seeds329101..329105. Construct
five fresh native models and train each for2400 updates. Preserve two detached,
deep-cloned state_dict snapshots per trajectory after optimizer updates1200 and2400:
`prefix1200` (control) and `extended2400` (candidate). No accepted checkpoint is used
as an initial model. No C328 logits/gradients choose TRAIN examples or stopping.

The comparison shares the actual first1200 updates by construction. At1200 snapshot,
hash full model and optimizer state before and after copying; require equality.
Before update1201, rehash and require equality with the1200 receipt. Keep the same
optimizer identity and all moments/step counters. No optimizer reset/recreation,
LR change, reseed, gradient detach, accepted-global patch or intermediate evaluation.
Verify that the stored prefix snapshot remains unchanged after completing2400.
Zero-sized tensors carry no payload and do not imply aliasing merely because their
storage pointer is0. Every nonempty snapshot tensor must have independent storage.

Do not call the1200 state an independently trained control. Do not count it as a
second1200 fit. The actual total is5*2400=12000 updates, not18000 or24000. Five fresh
training instances and ten separate evaluation instances are accounted separately.
Checkpoint-copy/optimizer-hash overhead is real. No wall-clock speedup is claimed.

## Exactly held conditions and intentional extra work

Native mean_last;14256 parameters including3328 shared-core parameters;64slots;
CPU float64,2 Torch threads, deterministic runtime. Same logical192TRAIN/96HOLDOUT
rows and canonical original/interior prompt tables inherited from C328.
Native C308 optimizer factory, exactly once per trajectory: AdamW noncoreLR.005,
coreLR.0005, betas(.9,.999),eps1e-8,weight_decay0,mean cross entropy,global gradient
norm clipping1 in original parameter order before each optimizer.step.
FIT_RNG612000 is set once per trajectory, not again at the cycle boundary.

For each fresh order seed, call the unchanged plan_for_order(...,'two_to_four',...)
and C326 validate_schedule/family_mask(events,'batch4') on the1200-event schedule.
Each event has24 intact query pairs/48 rows. The original/interior allocation of
length4 updates is11..13 original pairs of24, not an exact12/12 assertion.
Execute indices0..1199 twice, in exactly the same order and with the same masks.
Do NOT extend the old helper's fixed-length contract by changing its globals.

Per TRAIN row exposure (original2,original3,original4,interior4):
- prefix1200:100,100,50,50;
- extended2400:200,200,100,100.
Length/profile/query-pair identities, labels and proportions are identical; total
exposure and compute intentionally differ. This is not an equal-budget comparison,
a new independent dataset, a shuffle-policy study or a pure capacity intervention.
Persist base schedule/mask, exact executed event indices, per-cycle exposure map,
all2400 CE/rate/gradient traces, initial hashes, two checkpoint receipts and the
continuation hashes. Saved checks reconstruct these contracts; they do not rerun
the optimization history or prove every historical intermediate weight tensor.

## Evaluation, unchanged gates and strict paired outcome

Finish ALL five2400 fits and save/reload the ten-state bundle before ANY scientific
evaluation. Evaluate every checkpoint with the unchanged original1..6/interior
normal, evidence-blind and query-blind evaluator, then load the same checkpoint again
and replay it. Each of20 evaluations uses171 model forwards/16416 rows/684 core
forwards and native mean_last receipt(calls171,query_calls342,rows16416,grad_calls0).
Compare raw saved/replayed logits with the inherited1e-9 bound and preserve weights
and hooks. Both initial evaluation and replay are from actually saved bundle states.

Retain all local TRAIN/HOLDOUT profile/language/masked/order gates unchanged:
accuracy>=.90, both-query>=.80, evidence-blind drop>=.35, query-blind drop>=.35,
two-order>=.80. Original length1 remains descriptive only.
ALL FIVE paired seeds must satisfy the SAME composite comparison form as C328:
1. extended2400 passes the full interior gate and every original2..6 gate;
2. interior HOLDOUT correct answers AND both-query-correct pairs strictly increase
   versus its own prefix1200 control;
3. pooled original2..6 HOLDOUT answer AND pair counts do not decrease.
A control already at a perfect interior count cannot satisfy strict superiority by
a tie. This is intentionally a reliable-improvement gate; report saturation rather
than relax it afterward. No seed selection, average override or threshold change.
Save all cells, per-length contrasts and rescued/regressed counts, including negative
outcomes. Gate failure with valid execution is VALID NEGATIVE, not automatic retry.

## Fixed workload

5 training trajectories,10 saved states,10 evaluation model instances;
12000 optimizer updates,576000 training-row presentations;
15420 model forwards =12000 training +10*171 evaluation +10*171 replay;
904320 total row presentations;61680 core forwards;
20 checkpoint state loads;1 scientific bundle reload;1 new model bundle write;
0 network calls. Raw persisted-logit payload336199680 bytes, not peak RAM or all
serialized bytes. Saved semantic verification loads are outside these cohort counters.

Separate native preflight:validate all five real schedules/masks; one discarded
probe with original/interior English/Japanese inputs,6forwards/2backward evaluations,
12row presentations,0 optimizer updates. Temporary nonzero output weights test
useful gradient connectivity; this model never initializes a scientific trajectory.
Allocation, tests, parent/saved verification and hashing are separately scoped.

## Immediate accepted parent and writer-side schema

C328 scientific execution:3507021e46d47f6543316d46dc4481d3ead04855.
Publication:edf05c01e7fcd91b95c425fca5e7c416150689aa.
Parent folder:runs/c328-late-rate-206451e9574c4b578b5cff4201af284b/.
Primary science/summary.json SHA256:
10bf430e74311a883cbcc7a7b70b589490a98d0f6db4458bcfe8be748fbccb53.
Companion execution-envelope.json SHA256:
d675bf546fb9d46eecf86b9a53847c5c054f4de618f311e0426a195c49f7cc32.

The parent is fold-c328-science-v1 with statusFAIL and diagnostic_execution_valid=true,
NOT the earlier C327 diagnostic schema. Its candidate_gate isfalse. The envelope is
fold-c328-execution-envelope-v1, scientific_statusFAIL. Validate these semantics,
manifest/work, full5722 regression, final1561 rereads and completed saved verification.
Full result/envelope source/input maps must match, with826sources/1561inputs.
The parent writer's eight outputs plus summary and envelope add TEN files.

Read C328's saved dataset/original-prompts/interior-prompts, validate canonical data
hashes and prompt semantics, then invoke unchanged
C328.semantic_recheck(C328_out,data,old,new,cx,read) under no_neural. This recomputes
the parent metrics and validates saved traces/checkpoints with no model forward.
Do not recursively execute older semantic bodies; still verify all inherited bytes.
C328 readout/output logits are model scores, not repaired or oracle-picked actions.

## Complete protection and ordinary regression

832 sources =826 inherited+6 own.
1577 inputs =1561 inherited+10 immediate-parent files+6 own.
All own benchmark/executor/test/runner/launcher/contract bytes and direct/lazy shared
C328/C326/C325/C324/C308/recovery dependencies remain pinned. Both primary/envelope
contain the complete unions. No smaller-map fallback or retroactive dependency pin.
Unchanged R4 native Windows read leases span all phases, independent first-read
reference hashes andALL1577 final uncached rereads. No unlocked/cross-run cache,
artifact deletion, source mutation or environment reinstall.

48 own tests;5722 inherited+48=5770 selected;218modules;5771 before the sole inherited
C204 mutable-ACTIVE exact-ID exclusion. No new exclusions/skips or cached regression
success. Build actual suites, validate unique IDs/counts and print ordered ID digest.
The historical regression runs unchanged in a separate ordinary Python process.
Native preflight and all5770 tests must pass before scientific fitting.

## Outputs and execution order

PowerShell7 -> invoke_active_v2 -> invoke_c329 -> run_c329 -> c329_execution controller
-> worker -> C328 locked snapshot and saved semantics -> native preflight -> separate
full regression -> five uninterrupted trajectories and ten snapshots -> saved bundle
reload -> ten evaluations and ten replays -> saved semantic reconstruction -> final
1577 rereads -> summary/envelope -> fresh byte verifier -> console log publication.

Eight local science outputs:experiment-plan.json,dataset.json,original-prompts.json,
interior-prompts.json,trained-models.pt,evaluations.pt,measurements.json,
validation-summary.json. New model schema fold-c329-models-v1 stores ordered ten states.
New evaluation schema fold-c329-evaluations-v1 stores five trajectories and ten scored
checkpoint records. Its saved loader is explicitly used by semantic_recheck.
The summary schema is fold-c329-science-v1; envelope fold-c329-execution-envelope-v1.
Hash/size-bind outputs before/after saved reconstruction and before final records.
Fresh verification checks all source/input/output bytes, maps, manifests, cohort,
counts, original parent evidence and fixed-gate bindings, without refitting.

Local location:runs/c329-budget-<id>/science plus enclosing execution-envelope.json,
regression-result.json and science/regression/verify logs. Publish console ONLY to
 docs/experiment-run-logs/c329/latest.log and latest.json. Never commit tensors/data.
10-second heartbeats,200-update CE/rate progress, five prefix-preservation messages,
ten checkpoint-replay messages, seed/pair deciding records and compact domain metrics.

## Authoring gate, interpretation and stopping

Manifest SHA256:
9968ab6d8d2abdd3751b6ac1d1b1116a088d1c8abbdebdae50b580005d6fb7d8.
Reread all6 committed remote files and compare their Git blobs to the tested local
bytes. Rerun48 own tests, CP932-default-text-open emulation, UTF8/NUL/compile/import
and recursive free-global audits after the remote reread. Counts must be semantic,
not source-literal guesses. Native PowerShell AST execution is not assumed on Linux;
retain the actual user-side dispatcher -> selected launcher -> runner ParseFile chain.
The full2400-update real Torch toy run is a SOFTWARE fixture, not FOLD performance.
Synthetic parent/locks/suite/science callbacks must be labeled as synthetic. No
native Windows, true-parent training or full5770 success is claimed by author tests.

This test cannot prove abstract rules, architectural capacity limits, optimal budgets,
general LLM performance, unseen-template transfer, production adoption or Gate F.
One negative fixed-budget test does not show no larger budget could ever help.
Source/input/test/schedule/nonfinite/continuation/snapshot/replay/semantic/envelope
failures are INVALID; preserve evidence and repair SAME C329, no automatic rerun.
Stale branch/HEAD/ACTIVE/trackedtree/dependency/AST failures SKIP before logging/push.
Scientific FAIL with complete integrity is negative evidence, not an execution fault.
Publication-only failure is repaired without refitting. C330 remains NOT REGISTERED.
Authoritative runtime remainsPython3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
No CI, paid service, package installation or accepted-result edits.
