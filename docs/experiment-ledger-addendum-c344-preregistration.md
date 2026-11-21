# C344 preregistration: pair-max full-class training loss

Date: 2026-11-04 Japan time. Branch: feat/sft-target-loss.
Stage: V5-B-PAIR-MAX-TRAINING. Experiment: C344-v5b-pair-max-training.
Gate F remains NOT PASSED. No production adoption.
Acceptance base: 345830ca6cd256abfb33d2d220db06e8f83e2859, following C343 acceptance
ec33919f2763a629e8c2d1b00f82d0f682e3979a and its factual wording clarification.
Assistant authors/tests/registers; user executes locally. No Codex handoff.
This source registration is not a scientific result or an ACTIVE instruction.
A separate documentation-only activation follows independent committed-byte review.

## One scientific question and motivation

At the same architecture, mixed45 token stream and 2400-update budget, does replacing
ordinary mean per-query cross-entropy by the mean of each query pair's larger
full-256-class cross-entropy improve fitted and held-value interior4 binding while
retaining every other scored domain?

C343 ACCEPTED PASS (DIAGNOSTIC INTEGRITY) leaves C342 ACCEPTED VALID NEGATIVE,
candidate_gate=false and eligible_seed_count=2. Candidate interior4 has 131 actual
TRAIN errors: 99 for seed342001 and 32 for seed342005, all wrong_observed. Across
1440 TRAIN query pairs, 1312 are both correct, 125 have one correct answer, and
three have neither correct. Since every error is the other displayed value, those
125 pairs answer the same value to both queries; the three remaining pairs swap
the values. Unknown value combinations alone cannot explain these fitted failures.

The mixed45 candidate improves aggregate interior answers, but introduces 60 TRAIN
and 30 HOLDOUT individual-answer regressions. Every remaining original6 wrong
answer is also a new individual regression: six in TRAIN value combinations and
six in HOLDOUT, while length6 names were never fitted. Aggregate gains and failed
cell transitions cannot establish that all previously correct answers survived.
These observations motivate a complete-pair objective comparison, not selected
language/profile/entity/seed training or a causal claim about the old objective.

Historical paired objectives were already tried. C268's pair-margin auxiliary was
a valid negative. C288's assignment auxiliary raised trained direct-gate success
3/5 to 5/5 but lowered four-character full-gate success 3/5 to 1/5. Assignment
scores may compensate one query with its partner. C344 instead changes the
reduction of full-class per-query CE. It is not a claim that pair-aware training
was previously untested or that this objective guarantees better generalization.

## The single changed variable

Arms: mean_ce (control) and pair_max (candidate). Every update contains the same
48 TRAIN rows arranged as 24 complete query pairs. For per-query full-class CE
values a and b, control uses mean((a+b)/2); candidate uses mean(max(a,b)).
Equivalently candidate loss is ordinary mean CE + 0.5*mean(abs(a-b)). There is no
auxiliary coefficient, margin, temperature, support loss or parameter sweep.

Use torch.maximum: exact ties divide the pair's derivative equally between both
queries; otherwise the higher-loss query receives the pair's direct loss gradient.
Both arms compute and record ordinary CE, pair-max and the selected objective on
every pre-update batch; only the selected objective is differentiated. This keeps
loss-measurement overhead symmetric and adds no neural forward or backward call.

Validate actual adjacent row identities before creating an optimizer and again
before each scientific forward: shared language, entities, values, fact order,
two distinct queries and correct counterpart targets. The same canonical pair
receives the same family/length selection for both queries. Label metadata enters
only pairing validation and training loss; neither targets nor supplied values
restrict model inference or all-256-class argmax.

This intervention changes adaptive within-pair gradient weights and their effect
under global clipping. It does not equalize gradient magnitude by an extra rate
change. The larger-loss query need not be the incorrectly predicted query; switching
is non-smooth, and the easier partner receives zero direct gradient on a non-tie
update. Gains would support this fixed objective comparison, not prove that mean
CE, pooling, parity, capacity or a particular shortcut caused the previous errors.

## Fixed data, exposure, schedule and optimizer

Fresh seeds344001..344005 and order seeds344101..344105. Construct both models in
each pair before fitting either; require equal full/core initial weights and
independent parameter storage. Never reuse an accepted fitted state, drop a seed,
restart a failed scientific fit or select an intermediate checkpoint.

Canonical data: 192 TRAIN / 96 HOLDOUT rows, SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Distinct values0..3 use byte classes48..51. HOLDOUT value pairs remain (0,2),
(1,3), (2,0), (3,1). Both languages and all canonical profiles remain mandatory.
HOLDOUT denotes value-combination withholding, not wholly unseen prompt families.

Both arms use the exact C342 mixed45 token policy and immutable canonical banks.
The first1200-event cycle uses the fixed balanced allocator on original-family
slot4 events. Per pair/profile, available repeat/shared_prefix/shared_suffix
occurrences are16/17/17; canonical4 quotas are8/8/9, canonical5 gets8/9/8.
Cycle2 exactly complements each corresponding event/pair choice. The existing
family mask remains identical, with11..13 original pairs per slot4 update and
5..8 of each actual original length. No allocator fallback or schedule search.

|Actual TRAIN domain|Exposures per logical row in either arm|Per cycle|
|---|---:|---:|
|original2|200|100|
|original3|200|100|
|original4|50|25|
|original5|50|25|
|original6|0|0|
|interior4|100|50|

These are whole-fit counts across all profiles, not repetitions of one literal
prompt. All HOLDOUT rows, masks and original6 names remain outside fitting.
Each logical TRAIN row receives600 presentations in total. Allocation and token
accounting are checked on all five actual schedules before fitting.

Use batch4/two_to_four,1200 events repeated twice,48 rows/update,FIT_RNG=612000.
One continuous core_slow AdamW optimizer per model: noncore LR.005/core LR.0005,
betas.9/.999,eps1e-8,weight_decay0,global gradient clip1. Verify the post1200 and
pre1201 weight/optimizer hashes agree. No intermediate evaluation or optimizer
restart. All ten fits finish before any scientific evaluation or replay.

Architecture remains14256 parameters including3328 core parameters,64 slots and
padded input positions,CPU float64,two Torch threads,native_before readout. Final
states are detached deep copies. No new layer, output repair, teacher input,
inference-time constraint, original6 training or additional data is introduced.

C344.previous() returns C332; C344.reference() returns C342. Reuse pure banks,
allocation, input-selection and scoring helpers without changing their globals.
C344 owns its new seed identities, model creation, schedule and loss logic. Do not
send344xxx seeds into older experiment functions that enforce their own cohort.

## Actual input and work accounting

Both arms must have identical canonical-bank, logical-event, target, family-mask,
length-mask and actual-input fingerprints. The fitting loop counts nonpadding
tokens including BOS/EOS and hashes each update's actual tokens then targets as
little-endian int64 bytes, prefixed by the C344 stream identity. Saved reconstruction
independently rebuilds that stream; equality of bank recipes alone is insufficient.
Literal pair metadata is separately validated and bound.

|Arm|Updates/model|Rows/model|Nonpadding tokens/model|
|---|---:|---:|---:|
|mean_ce|2400|115200|3168000|
|pair_max|2400|115200|3168000|

Scientific work: ten training and ten evaluation model instances,ten final states,
ten optimizer creations,24000 train steps/gradient calls/optimizer steps,1152000
training rows. Evaluation/replay adds3420 model forwards. Total27420 model forwards,
1480320 row presentations,109680 core forwards,54840 query projections,20 model-state
loads,one checkpoint-bundle load,one new bundle write,zero network calls.
Raw-logit payload672399360 bytes is neither total serialized size nor peak RAM.
Tests, discarded preflight and immediate-parent reconstruction are separate.

Native preflight validates all five schedules, complete pairs, allocations and
identical input streams before using a discarded native model. Probe both arms,
both cycles and original/interior inputs with complete English and Japanese pairs:
16 forwards,64 rows,8 backwards,zero updates. Nonzero output weights,finite
gradients and a nonzero query-weight gradient are required. Probe weights remain unchanged and are never used
as a scientific state. Preflight failure prevents regression and scientific fitting.

## Evaluation, complete normal statistics and fixed gate

Each final model is loaded,evaluated,reloaded and replayed with native_before and
unrestricted256-class argmax. Retain all114 views/state: original1..6 and interior4,
both logical splits,all profiles/languages,normal and masked controls. Require raw
replay drift<=1e-9 and exact argmax,immutable state/data/prompt fingerprints and
matching receipts. Original1 remains descriptive.

Unchanged original/interior scorers use accuracy.90,query_pair.80,evidence_drop.35,
query_drop.35,both_order.80. Derive normal counts from raw saved logits. Publish
all120 state/domain/split summaries,including normal support partitions,correct
answers,zero/one/both-correct pairs and collapse; publish all60 paired seed/domain/
split comparisons with individual-answer and query-pair rescues/regressions.
Each TRAIN state/domain has576 answers/288 pairs; each HOLDOUT has288/144.
Full256 support categories correct/wrong_observed/absent_digit/outside_catalog are
descriptive; no support-only objective or additional support-error gate is added.

C344 PASS requires ALL of the following:

1. All five candidate states pass every complete original2..6 AND interior4 gate.
2. For EACH paired seed,EACH of the six domains and EACH split TRAIN/HOLDOUT,
   normal correct-answer gain AND both-query-correct gain are nonnegative.
   All60 matched contrasts are mandatory; pooling cannot conceal a loss.
3. Across all five pairs,interior4 TRAIN answer gain,TRAIN query-pair gain,HOLDOUT
   answer gain and HOLDOUT query-pair gain are EACH strictly positive. Four
   endpoints must pass independently.

Any strict-endpoint tie,perfect-control saturation,seed failure or domain/split
regression is ACCEPTED VALID NEGATIVE when execution is valid. No seed selection,
extra update,rate compensation,relaxed threshold or gate revision is allowed.
PASS supports this five-pair cohort and this bounded objective policy only.
Gate F completion,production adoption,general language understanding,arbitrary
length generalization and a causal failure mechanism remain unclaimed.

## Exact immediate C343 parent and complete protection

Execution HEAD1effc2138967715e9e9319e1da19c3653e4fd9ac.
Log publication74eda8f681f7a68f1d8c4ae91203c2b151855ce6.
Folder runs/c343-mixed-length-localization-f1a8f5665ebb48c98b273cb549e721fd/.
Primary883c1c0142173f038bec25f65589643af9ba40ef2442e7c376b845a61f1477ce.
Envelope275ac041de4a858ca5a7f50aabb16898e85befebb2ee3ba6159a06198a7c993a.
Manifest7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6.
Pin executor blob8ec24e0b5c10ee653a445209f7caf9961d5c872c and benchmark blob
e9b8ee752422c93a29fefbb4b8ef0f48b5b776be before import; retain helper-dictionary ABI.

Require fold-c343-diagnostic-v1/PASS,diagnostic_execution_valid=true and
capability_gate_applicable=false. Validate C342 negative at
validation_summary.parent_validation_summary:candidate_gate=false/eligible=2.
Require6442-test/237-module completion,923 sources/7693 inputs,all7693 final
uncached rereads and the accepted manifest/work declaration.

Rebuild inherited maps through unchanged C343.snapshot. Retain ALL483 parent
outputs: four science files,primary,envelope and477 regression proofs (three
records plus237 module receipt/log pairs). Recheck byte hashes,ordered test IDs
and actual PID/log completion evidence. Add seven OWN files: benchmark,executor,
two test modules,runner,launcher,this preregistration. Source930=923+7;
protected input8183=7693+483+7. No duplicate path or unpinned deciding dependency.
Audit direct and lazy repository dependencies,including C343,C342,C340,C338,C337,
C332,C326 and canonical helper chains. Reconstructability at HEAD is not a pin.

Immediate parent reconstruction calls C343 benchmark directly:
semantic_recheck(out343,out342,data_out,cx,read),five arguments,under no_neural.
The C343 executor's parent_semantics validates only C342 and is not a substitute.
C342 source directory is
runs/c342-mixed-length45-cceefd2e5093444483eb61f6f883e058/science/.
Canonical C329 data is root/h['c330'].PARENT_FOLDER/science. Do not rerun ancestor
neural computation. C344 native_preflight hasfive arguments;run_training six;
saved semantic_recheck four. Validate actual writer schemas and summary fields.

Native R4 leases span the full worker interval with explicit finite max_files=8183,
independent initial hashes and ALL8183 final uncached rereads. No default4096
capacity,eviction,unlocked fallback or omitted regression proof. Accepted sources,
tests,contracts,logs and dispatchers stay immutable.

## Regression, artifacts, execution and stop

Preserve6442 ordered parent IDs,237 modules and ID SHA256
0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5.
Append48 actual science tests and24 execution tests: own72,total6514 selected
tests/239 modules;6515 before the sole inherited exact mutable-ACTIVE exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No additional exclusion,skip,cached success or historical test edit. Actual loaders
and ordered IDs define inventory; numeric source-string assertions do not.
Full ordered-ID SHA256: c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3.

Run all239 modules in fresh sequential processes with accepted C330R1.2 direct/
immediate-child PID checks and matching begin/end markers. Bind execution HEAD
and regression-plan hash. Schemas: fold-c344-regression-plan-v1 and
fold-c344-regression-v1. All6514 tests must pass before scientific fitting.

Six science outputs: experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Bundle schemas:
fold-c344-trained-models-v1 and fold-c344-evaluations-v1. Primary schema:
fold-c344-trained-v1;envelope:fold-c344-execution-envelope-v1. Bind HEAD,sources,
inputs,artifact sizes/hashes,manifest,work and completion. Preserve outputs around
saved reconstruction and before final records. Fresh verification checks proofs,
persistence,loss trace invariants,metrics and actual stream fingerprints; it does
not independently replay every optimizer update. A successor retains489 outputs:
six science,primary,envelope and481 proofs (three records plus239 JSON/log pairs).

Route: invoke_active_v2 -> invoke_c344 -> run_c344 -> c344_execution -> native locks/
snapshot -> immediate C343 semantics -> discarded native preflight ->6514 isolated
tests ->ten fresh fits ->native evaluation/replay ->guarded saved reconstruction
->all8183 rereads ->fresh verifier ->console-only latest.log/latest.json publication.
Run prefix:runs/c344-pair-max-training-<id>/.
Native Windows runtime: Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5,PowerShell7.
Use existing .venv-py31315. Branch,tracked-tree,ExpectedHead,unique ACTIVE,dependency
and AST checks precede logging. Stale invocation skips without science/publication.
User block parses active_v2;dispatcher parses invoke_c344;launcher parses itself
and run_c344. Parser failure cannot start the scientific run.

Progress includes every phase/regression module,seed/arm,every200 updates,the ten
state results,five paired summaries,120 normal support rows,60 normal paired rows
and verification heartbeats. Completion requires full regression,fitting,replay,
reconstruction,all rereads,fresh verification,run_execution_valid=true and log
publication. Scientific FAIL with intact execution is valid negative. Source/input/
regression/PID/nonfinite/gradient/pairing/schema/replay/reconstruction failure is
INVALID/RETRY SAME C344. Publication-only failure repairs transport without fitting.
C345 waits for formal C344 judgment. No CI,paid service,accepted-model retraining,
artifact deletion or branch updates while the user runs.

## Mandatory independent committed-byte review

After all seven files are published,an independent reviewer retrieves every exact
remote file through EOF and matches Git blobs with tested local bytes. Run all72
own tests normally and with CP932-default-text-open emulation,keeping explicit
UTF8 and binary modes unchanged. Audit compile/import/UTF8/noNUL,pyflakes and
recursive code-object free-global bindings; require zero unbound names.

Construct actual6514-ID/239-module plan,retain exact6442-ID prefix,and cross-check
manifest,work,thresholds,counts,parentfive-argument/childfour-argument dispatch,
six-argument training,writer schemas,complete source/input coverage and call order.
Inspect actual pair-max gradients (including ties/non-compensation),real pairing,
allfive schedules/allocations/stream equality,one continuous optimizer and complete
60-contrast/four-endpoint gate. Test source strings against their exact function
targets; do not mistake comments/docstrings or other callers for the target code.

Use actual PowerShell Parser.ParseFile on the dispatcher,launcher,runner and final
standard block; verify CLI positions and prelogging skip conditions. A source
correction requires renewed remote-byte review. Record exact review HEAD and
post_authoring_review=PASS in a separate review record/handoff before activation.

Author tests may use canonical tables,renderers,allocators,native preflight and
scorers,plus explicitly synthetic saved logits,small Torch optimizer-continuity
fixtures and OS/parent collaborators. This is not the native6514-test regression,
8183 Windows leases or ten-model scientific run. Native parent artifacts are not
transferred to the author checkout. Native completion remains user-side work.

Manifest SHA256: a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8.
