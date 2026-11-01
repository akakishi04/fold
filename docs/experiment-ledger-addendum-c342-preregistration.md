# C342 preregistration: mixed length-four/five TRAIN exposure

Date: 2026-11-02 Japan time. Branch: feat/sft-target-loss.
Stage: V5-B-MIXED-LENGTH45-TRAINING. Gate F remains NOT PASSED.
Acceptance base: d8ab608b482d877a3927ef48b0f03a4212451aa1, a separate C341 result commit.
Assistant authors/tests/registers; the user executes locally. No Codex handoff.
This registration is not a scientific result or permission to skip independent
committed-byte review. A separate documentation-only activation follows review PASS.

## One scientific question and motivation

At the same 2400-update budget, does restoring half of the original-family slot4
TRAIN exposure to canonical length4 improve original4 retention against fresh
original5-only training while preserving original6 and every other scored domain?

C341 ACCEPTED PASS (DIAGNOSTIC INTEGRITY) localized the accepted C340 negative.
The original5 candidate has 10 local / 4 order failures versus control 75 / 27.
Four candidate original4 local failures and two order failures are newly regressed;
all are shared_suffix / Japanese / entities[1,2]. Five interior4 local failures and
two order failures persist, including normal TRAIN prompts actually fitted by that
arm. The remaining original6 local failure is new, not persistent: all 29 control
original6 accuracy/query-pair failing cells were rescued and a different cell failed.
No mask-only local failure exists. C340 remains candidate_gate=false, eligible=2/5.

These observations motivate an exposure-retention comparison. They neither prove
a length shortcut nor predict that restoring original4 will fix the interior4
failure. Do not target the observed language, entity set, profile, cell or seed.
All canonical TRAIN rows/profiles/languages and all five fresh pairs are mandatory.

## Intervention, allocator and controls

Control arm: original5. Candidate arm: mixed45. Both use ordinary mean CE over all
256 classes and native_before readout during fitting, evaluation and replay.
The single intervention is the actual token-length policy on original-family slot4
TRAIN events. The unchanged schedule still labels these events with index4.
Prepare both canonical original4 and original5 banks using immutable C340.prepared.
Keep original2, original3 and interior4 tokens, logical events, paired query rows,
targets and the family mask identical. No support loss, filtering, label change,
capacity change, optimizer change or output repair is introduced.

Candidate allocation is fixed before the scientific run:

1. Use immutable C326.balanced_allocation on the first 1200-event cycle. Restrict
   its edges to the original-family slot4 query pairs, separately for each profile.
   Available occurrences per pair/profile are 16 / 17 / 17 for repeat /
   shared_prefix / shared_suffix. Choose canonical4 quotas 8 / 8 / 9; canonical5
   receives the complementary 8 / 9 / 8 occurrences.
2. In cycle2, complement the choice for each corresponding event/query pair exactly.
   Canonical4 then has 8 / 9 / 8 and canonical5 has 8 / 8 / 9 occurrences.
3. Both query rows of each pair always receive the same length. Every slot4 update
   retains its existing 11..13 original-family pairs and its interior-family pairs;
   each original actual length contributes 5..8 pairs in a mixed update.
4. Allocation must be feasible and satisfy every exact quota for all five schedules.
   There is no fallback, result-dependent assignment or alternative schedule search.

|Actual TRAIN domain|original5 exposures/row|mixed45 exposures/row|
|---|---:|---:|
|original2|200|200|
|original3|200|200|
|original4|0|50|
|original5|100|50|
|original6|0|0|
|interior4|100|100|

These are whole-fit totals, 600 presentations per logical TRAIN row. Each candidate
cycle has exactly 100 / 100 / 25 / 25 / 0 / 50 presentations per row in the table's
order. Both cycle exposure and pair/profile quotas are checked from actual masks.
All HOLDOUT logical rows, all masked prompts and original6 remain outside fitting.
The selector receives no target labels and can change only the registered token rows.

The intervention combines restored original4 exposure, reduced original5 exposure
and one fixed temporal assignment. It is not an isolated extra-data effect or a
search for the optimal mixture. Both arms see normal TRAIN templates from their
respective fitted domains; HOLDOUT still means held-out value combinations. Do not
describe all evaluation domains as equally unseen or as arbitrary-length transfer.

## Paired cohort, data and learning

Seeds 342001..342005; order seeds 342101..342105. Fresh five pairs / ten models;
construct both models in each pair before fitting either. Require equal full/core
initial weights and independent parameter storage. Never reuse an accepted model,
drop a seed or select an intermediate/favorable checkpoint.

Canonical data: 192 TRAIN / 96 HOLDOUT rows, SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Values are distinct members of 0..3, byte classes 48..51. HOLDOUT value pairs remain
(0,2), (1,3), (2,0), (3,1). Keep both languages and all canonical profiles.
Unchanged C332/C329/C326/C324 helpers supply data, prompt writers, schedules, family
masks, native architecture and scoring. C342.previous() returns C332;
C342.reference() returns C340. Do not substitute the immediate diagnostic parent
for the trained-data helper bridge.

Use batch4 / two_to_four, 1200 events repeated twice, 48 rows/update, FIT_RNG=612000.
One core_slow AdamW optimizer per model continues across both cycles: noncore LR
.005 / core LR .0005, betas .9/.999, eps 1e-8, weight_decay 0, global gradient clip1.
Verify post1200 = pre1201 weight/optimizer hashes. No intermediate evaluation or
optimizer restart. All ten fitting runs finish before any scientific evaluation.
Final checkpoints are detached deep copies, not references to mutable model storage.

Architecture: 14256 parameters including 3328 core parameters, 64 slots / padded
input positions, CPU float64, two Torch threads. Initial weights, targets, event
indices, family masks, rates and logical training fingerprints match within pairs.
Actual input-stream and length-mask fingerprints must differ between the arms.

## Token and work accounting

The actual fitting loop counts nonpadding tokens including BOS/EOS and hashes each
update's actual tokens followed by targets as little-endian int64 bytes. Saved
reconstruction independently rebuilds that stream from canonical banks, events and
fixed masks. Also bind complete bank recipes, targets, logical events, family masks,
length masks and exact per-cycle exposure; a bank-only fingerprint is insufficient.

|Arm|Updates/model|Rows/model|Nonpadding tokens/model|
|---|---:|---:|---:|
|original5|2400|115200|3225600|
|mixed45|2400|115200|3168000|

Candidate uses 57600 fewer nonpadding tokens/model, 288000 fewer across five models.
Equal updates, rows and padded64 frames are not FLOP or nonpadding-exposure equality.
Report these counts in each seed result; do not infer a wall-clock saving from them.

Scientific work: ten training and ten evaluation model instances, ten final states,
ten optimizer creations, 24000 train steps / gradient calls / optimizer steps,
1152000 training rows. Evaluation/replay adds 3420 model forwards. Totals are 27420
model forwards, 1480320 row presentations, 109680 core forwards, 54840 query
projections, 20 model-state loads, one checkpoint-bundle load, one new checkpoint
bundle write, zero network calls. Raw-logit payload 672399360 bytes is neither
serialized total nor peak RAM. Tests, parent reconstruction and preflight are separate.

Preflight checks all five actual schedules, allocations, exposures and token streams
before creating a discarded native model. Probe both arms, both cycles, original and
interior inputs, English and Japanese: 16 forwards / 32 rows / 8 backwards / zero
updates. Nonzero output weights and finite gradients are required; probe weights
stay unchanged and are never reused as a scientific model. Changed inputs need not
produce equal logits. Failure prevents the full regression or scientific fitting.

## Evaluation and fixed gate

Each final model is loaded, evaluated, reloaded and replayed using native_before and
all256-class argmax. Retain all 114 views: original1..6 and interior4, both logical
splits, all profiles/languages, normal and masked controls. Require raw replay drift
<=1e-9 AND exact argmax, immutable state/data/prompt fingerprints and matching receipts.
Original1 is descriptive. Neither target labels nor the supplied pair restrict inference.

Unchanged original/interior scorers use accuracy .90, query_pair .80, evidence_drop
.35, query_drop .35 and both_order .80. Report per-domain normal HOLDOUT correct-answer
and both-query-correct counts, gains and individual rescued/regressed answers/pairs.
C338.support_report / C337.audit_logits supply descriptive correct / wrong_observed /
absent_digit / outside_catalog partitions, 288 normal HOLDOUT answers/domain/state.
These partitions introduce neither a support objective nor a support-error gate.

C342 PASS requires ALL of the following:

1. All five candidate states pass the complete original2..6 AND interior4 gates.
2. For EACH paired seed and EACH of those six domains, normal HOLDOUT correct-answer
   gain AND both-query-correct gain are nonnegative. Pooling cannot hide a loss in
   one domain. Pooled short-domain statistics are descriptive only.
3. Summed over all five pairs, original4 correct-answer gain AND both-query-correct
   gain are strictly positive. Neither endpoint can compensate for the other.

This is a new original4 retention estimand against freshly trained original5-only,
not a retrospective change to the C340 original6 transfer gate. There is no fresh
original4-only arm, so C342 cannot re-estimate the six-character gain against that
baseline. Perfect-control original4 performance, ties, saturation or any failed
criterion produce ACCEPTED VALID NEGATIVE when execution is valid. They do not
authorize new seeds, extra updates, a new mixture, relaxed thresholds or retries.
PASS supports this fixed cohort and policy only. Gate F completion, production
adoption, general language understanding, an optimal curriculum and a general
length mechanism remain unclaimed. Interior4 remains mandatory even if unchanged
exposure makes its residual failure persist.

## Immediate C341 parent and complete evidence protection

Execution HEAD a6a052912d52f786dd8c809ed6e8e96996c74edd.
Publication commit 69ac5ae2e6fb4e268b3ef0453a83c3ad9cd1ecdb.
Folder runs/c341-length-gate-localization-eff5826958774979923f8d9aa67a1abf/.
Primary ec30706ed3761c7b36c4ef215a85c53ccc79cbd1ffb271a5b387fe2049b406eb.
Envelope 6cc5988f3126f0b51a2d5543755cf58471e8839354e3dcf6bc86b7ce1f30ac8e.
Manifest 453b701fcf597a7ea8d38eb7b9457ee97693575f1349fa4903beebe5a1f6a647.
Pin C341 executor blob 5d846635ee34a0138bcf2c4f02eb7a146734d97b and benchmark blob
1af9dadce1b3b2dd6c329397654c8e970f3f5afd before import; retain the helper-dictionary ABI.

Require fold-c341-diagnostic-v1 / PASS, diagnostic_execution_valid=true and
capability_gate_applicable=false. Validate C340's negative within
validation_summary.parent_validation_summary: candidate_gate=false / eligible=2.
Require complete 6314-test / 233-module receipts, 909 sources / 6723 inputs,
all 6723 uncached rereads and the accepted manifest/work declarations.

Rebuild inherited maps through unchanged C341.snapshot. Add ALL 475 parent outputs:
four science files + primary + envelope + 469 regression proofs (three records and
233 receipt/log pairs). Check ordered test IDs, actual process/PID/log evidence and
all byte hashes. Add seven OWN files: benchmark, executor, two test modules, runner,
launcher and this preregistration. Source count is 916=909+7. Protected input count
is 7205=6723+475+7. No duplicate path, missing proof or unpinned deciding dependency.
Audit direct/lazy imports including C340, C338, C337, C332, C326 and their immutable
canonical helpers. Reconstructability from execution HEAD is not a pin substitute.

Parent reconstruction is exactly C341.semantic_recheck(out341,out340,read), three
arguments, under no_neural. The C340 source directory is
runs/c340-length5-training-0c8af407e2564082b7221f1c95ddb709/science/.
Read canonical C329 data through the established C330 parent-folder bridge. Do not
call a stale trained-parent signature or rerun ancestor neural semantics. All older
bytes remain protected. C342 native_preflight(data_out,cx,root,pins,read) has five
arguments; run_training(out,data_out,cx,root,pins,read) has six; child saved
semantic_recheck(out,data_out,cx,read) has four.

Native R4 leases protect the full execution interval with explicit finite
max_files=7205, independent initial hashes and ALL 7205 final uncached rereads.
No default4096 capacity, eviction, unlocked fallback, omitted proofs or edits to
accepted sources/tests/contracts/logs/dispatchers are permitted.

## Regression, artifacts, execution and stop

Preserve all 6314 ordered parent IDs, SHA256
3ee31f196c842e57f786d5efe1c22df5460d41ddc92b86cf40d8c9f56209ac76.
Append the actual 40 science and 24 execution tests: 6378 selected / 235 modules;
6379 before the sole inherited exact mutable-ACTIVE exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusion, skip, cached success or accepted-test change. Real loaders and
ordered test IDs define the inventory, never numeric source-string assertions.
Full ordered-ID SHA256 is
76dfa4fd2952bdffd80250e57880d58cda72e7f7c16402c1817fed39ff294460.
All 235 modules run in fresh sequential processes with accepted C330R1.2
direct/immediate-child PID checks and matching begin/end markers. The generic
module ABI binds the new execution HEAD and regression plan. Schemas are
fold-c342-regression-plan-v1 and fold-c342-regression-v1. All 6378 tests must pass
before scientific fitting; a module-level OK alone is insufficient.

Six science outputs: experiment-plan.json, training-traces.json, trained-models.pt,
evaluations.pt, measurements.json and validation-summary.json. Bundle schemas are
fold-c342-trained-models-v1 and fold-c342-evaluations-v1. Primary fold-c342-trained-v1
and envelope fold-c342-execution-envelope-v1 bind HEAD, sources and protected inputs.
Hash/size-bind all six outputs around saved reconstruction and before final records.
The fresh verifier checks proofs, persistence, saved metrics and actual input
fingerprints. It does not independently replay all 24000 optimizer updates.
A successor must preserve 481 outputs: six science + primary + envelope + 473
regression proofs (three records and 235 receipt/log pairs).

Route: invoke_active_v2 -> invoke_c342 -> run_c342 -> c342_execution -> native locks /
parent snapshot -> immediate C341 semantics -> discarded native preflight -> 6378
isolated tests -> ten fresh fits -> native evaluation/replay -> guarded saved
reconstruction -> all 7205 rereads -> independent fresh verifier -> console-only
c342/latest.log + latest.json publication. Run prefix: runs/c342-mixed-length45-<id>/.
Native runtime: Windows Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5, PowerShell7.
Use the existing .venv-py31315; no runtime reinstall. Branch, tracked tree,
ExpectedHead, unique ACTIVE, dependency and AST guards precede logging. Stale
invocations skip without scientific execution or log publication. The user block
parses active_v2; the dispatcher parses invoke_c342; launcher parses itself/runner.

Progress includes each phase, regression module, seed/arm, every 200 fitting updates,
all ten state results, five paired contrasts and verification heartbeats. Completion
requires full regression, fitting/replay/reconstruction, all rereads, fresh verifier,
run_execution_valid=true and log publication. A scientific FAIL with these integrity
checks passing is valid negative. Source/input/regression/PID/nonfinite/gradient/
pairing/schema/replay/reconstruction failure is INVALID / RETRY SAME C342.
Publication-only failure repairs publication without retraining. C343 waits for
formal judgment. No CI, paid service, accepted-model retraining or artifact deletion.

## Mandatory independent committed-byte review

After publishing all seven files, reread each remote file through EOF and compare
its Git blob with the tested local bytes. Run all 64 own tests normally and under
CP932-default-text-open emulation. Audit UTF8/noNUL/compile/import and recursive
free-global bindings; verify zero unbound module aliases. Construct the actual
6378-ID / 235-module plan, and compare manifest, work, counts, thresholds, parent
three-argument and child four-argument dispatch, complete protection and call order.
Check the restricted allocator and exact cycle complement on all five real
schedules, token/target streams, unchanged family masks and ordinary CE/native path.
Use real PowerShell Parser.ParseFile, verify CLI positions and prelogging skip guards.
Review source-string assertions against their actual target function/file; do not
mistake docstrings/comments for code or count contracts.

An independent reviewer other than the source authors must PASS on committed remote
bytes before a separate documentation-only ACTIVE commit. Record exact reviewed
HEAD and post_authoring_review=PASS in the review record/handoff. Any source fix
requires renewed remote-byte review before approval.

Author tests use real canonical tables/renderers/schedules/allocators/native
preflight/scorers and saved-archive reconstruction. The 2400-update continuity test
uses a small Torch model; worker/fresh-verifier/proof-map tests use explicitly
synthetic parent/OS/scientific collaborators. Neither 64 author tests nor constructing
the full inventory equals the native 6378-test suite, Windows leases or ten-model
scientific run. These remain user-side execution work.

Manifest SHA256: 538150bd2b43ff286e4d5b0e0c1d665ea1e1c4d43cf8148cba1c5d1a4192734c.
