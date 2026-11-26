# C347 preregistration: saved loss and correctness-transition decomposition

Date: 2026-11-26 Japan time.
Experiment: C347-v5b-saved-loss-transition.
Stage: V5-B-SAVED-LOSS-TRANSITION.
Acceptance base: c0597bbc24ca3db2761763b65cfe8521af7d1b2e.
Manifest SHA256: 8e85821c7d4e69c49cd0695ccb5126a7dbb8b5cc0f5b9ca77f5fb0cd98a0aee3.

This is a retrospective arithmetic diagnostic of the accepted C346 cohort.
The motivating aggregate losses and answer counts are already observed. The full
decomposition, coverage rules and diagnostic gate are fixed before computing the
new loss-transition results. This is not a fresh-seed confirmatory experiment.
All seven OWN files must finish authoring and independent committed remote review
before activation. The later authoritative handoff records review PASS and the
exact reviewed source commit; this source-only registration does not activate C347.

## One scientific question

Which matched correctness groups account for lower terminal loss coexisting with
worse exact answers or both-query-correct pairs under the fixed half-rate policy?

C346 interior HOLDOUT illustrates the question: default pair-max to half-rate
pair-max reduced mean CE from 0.9938790728483501 to 0.7865997559833081 and mean
pair-max loss from 1.7749607318430114 to 1.2245369085052082, while correct answers
fell from 1188 to 1018 of 1440 and both-correct pairs from 516 to 396 of 720.
The same qualitative relation exists within seed346001 interior HOLDOUT. These
observations motivate the diagnostic; they do not select which strata to retain.

Analyze all five seeds346001..346005, all three arms mean_ce/pair_max/
pair_max_half_rate, all six domains original2..6/interior4, both TRAIN/HOLDOUT
splits, all three canonical profiles and both languages. The candidate is always
pair_max_half_rate; controls are pair_max then mean_ce in the accepted parent order.
All120 seed/control/domain/split comparisons are mandatory, including relations
with higher loss, fewer errors, zero transitions or results contrary to the motive.

## Changed and held constant

Changed: group the existing terminal predictions and losses by matched answer
correctness, both-query correctness and same-answer collapse status, and compute
an exact additive decomposition of each full-comparison loss difference.

Held: C346's15 saved states, all seeds, prompts, input rows, targets, profile order,
fact order, checkpoints, rates, budgets, fitted data, evaluation policy, full256
output classes and parent capability gate. Canonical data has192 TRAIN/96 HOLDOUT
rows. No new fitting, gradient, optimizer update, model forward, model state load,
checkpoint write, seed exclusion, filtering, prediction repair, rate selection or
external data/network call is part of this diagnostic. Production code is unchanged.

"Transition" means a matched comparison of two arms' final predictions. It is not
a temporal learned/forgotten event. The trace JSON is read only to bind each saved
record to its final state identity; there is no loss/norm trajectory audit here.

## Exact accepted parent and writer/reader contract

Scientific execution:622e623faa0c3c698a18033eb8b4bca554088918.
Log publication:426c52f9f33f2465e8b1cd1879182558b443f660.
Folder:runs/c346-pair-max-rate-68993e9eaa4e410886dbe0d24a3def3c/.
Primary science/summary.json SHA256:
d06fa2a06287696424ac58e3d56e7262282caca81b028f61709f609ab728e816.
Envelope SHA256:
b8b57583363d61aca10d947c891de0d8b3d8b2319e659652cacf101a334e3c3d.
Parent manifest:
8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64.
Executor tools/c346_execution.py blob:
7950248a3d9acd9e8eb8c7da48b1b707ea478d85.
Benchmark model_c346_pair_max_rate.py blob:
684970a7a1d073f22422cb46f7f1514802af832e.

The immediate parent is trained C346, not diagnostic C345. Require primary schema
fold-c346-trained-v1 and envelope fold-c346-execution-envelope-v1, C346-R0 revision,
status/scientific_status FAIL, scientific_execution_valid=true and
capability_gate_applicable=true. Require candidate_gate=false, eligible_seed_count=0,
all_candidates_full_pass=false, candidate_full_pass_count=0, nonnegative_vs_mean_ce=
false, nonnegative_vs_pair_max=false and strict_interior_vs_pair_max=false.
The nonnegative inequalities remain64/120 versus mean_ce and68/120 versus pair_max.
Gate F remains NOT PASSED; neither gate_f_candidate nor production_adoption is true.

The accepted fold-c346-evaluations-v1 archive has15 ordered records, each with
seed,arm,state_sha256,evaluation_policy,raw,receipts. Require the complete seed/arm
product and native_before policy; raw and receipts each contain evaluation/replay.
Bind state_sha256 to the same ordered trace's final_sha256. Each evaluation/replay
receipt is calls171/query_calls342/rows16416/grad_calls0. The saved normal predictions
are the original full-class terminal argmax decisions, without a later repair or
action-selection stage. Validate all raw views and saved replay with the immutable
parent validators; new arithmetic uses only each normal view.

Call C346.semantic_recheck(parent_out,data_out,cx,read), exactly four arguments,
under no_neural. Require exact equality to the accepted primary validation_summary.
C347.run_diagnostic and C347.semantic_recheck each take
(out,parent_out,data_out,cx,read), exactly five arguments, and use their real loader.
Canonical data/prompt hashes and the inherited pairing contract must pass again.
Parent check_summary validates the complete parent scientific result, not just
selected fields. Bind all180 terminal records,120 terminal contrasts and exact
normal rescue/regression/collapse counts back to this accepted result.

C346.helpers() returns parent,prior,cleanup,recovery,c330,runtime,legacy,locks.
The cleanup implementation is that helper mapping's cleanup=C344-R1; its parent
is C345 and must not be mistaken for a cleanup implementation. Preserve the exact
eight-key bridge. Do not invoke the parent's current-ACTIVE guard during immutable
parent reconstruction. Every deciding direct or lazy repository dependency must
be inherited source-pinned/protected; a missing pin is an integrity failure.

## Observations and arithmetic

Compute per-answer cross entropy from saved finite CPU float64 logits over all256
classes. Preserve first-index full-class argmax, including ties. No probability
floor, target-only filtering, favorable class subset or nonfinite repair is allowed.
Use the accepted C345 terminal_view helper through C346's pinned parent module.

Canonical pairs match language,entities,values,permutation/fact order and distinct
counterpart queries/targets. Require complete unique row coverage, never arbitrary
adjacency. Across arms also match seed,domain,split,profile,row IDs and targets.
Retain all38880 saved normal pairs/77760 answers and their metadata. The matched
candidate-versus-control inventory is25920 pairs/51840 answers; repeating the
candidate against two controls does not create independent new observations.

For query losses a,b, pair mean CE is (a+b)/2 and pair-max is max(a,b). Every delta
is candidate minus control. Pair-max delta is max(candidate query CEs) minus
max(control query CEs), not the maximum of the two per-query deltas. The maximizing
query may change across arms. Multiclass answer correctness does not constrain
the sign of a CE delta: a C-to-W change can lower CE and a W-to-C change can raise CE.

For every one of120 comparisons retain each of three complete partitions:

| Partition | Four groups | Losses decomposed |
|---|---|---|
| Per-answer correctness | CC, CW, WC, WW | Per-answer CE |
| Both-query pair correctness | CC, CW, WC, WW | Pair mean CE and pair-max |
| Same-answer collapse | distinct_to_distinct, distinct_to_same, same_to_distinct, same_to_same | Pair mean CE and pair-max |

In correctness labels the first letter is the control and the second the candidate.
C means a correct answer, or BOTH correct answers for a pair. Pair W means not
both correct, including a pair with one correct answer. "Same" means the two query
argmax predictions coincide; "distinct" does not imply either answer is correct.
Collapse is a secondary descriptive partition of the same paired observations.
Do not add counts or contributions across these three overlapping partition families.

Each group records exact count, control/candidate loss sums and means, delta sum,
mean, minimum and maximum, and signed contribution to the FULL comparison mean:
delta_sum divided by that comparison's entire answer count or pair count.
The group mean uses group count instead. Empty groups have count0, sums0,
contribution0 and null means/extrema; no group is silently dropped or assigned a
zero observed mean. Use math.fsum for reductions. Numerical conservation uses
1e-12 times max(1, compared magnitudes, underlying control/candidate sums or means),
including cancellation between large sums. Identities, counts, group labels,
coordinates and parent terminal/contrast bytes remain exact, without such tolerance.

Each partition separately covers its full comparison. Counts reproduce parent
correct/rescued/regressed/both-correct/pair-rescued/pair-regressed/collapse totals.
Loss sums recover parent means and the four signed contributions recover each
parent loss delta. All raw matched observations remain available, including every
query delta and pair-max delta. Equal answer/pair weighting within domain/split
is not exposure weighting over the training mixture. Original6 TRAIN includes
familiar combinations but was never itself fitted.

## Work, outputs and diagnostic gate

Per child computation or reconstruction pass:

| Counter | Fixed count |
|---|---:|
| checkpoint_records | 15 |
| normal_answers / query_pairs | 77760 / 38880 |
| terminal_summaries / terminal_contrast_count | 180 / 120 |
| matched_answers / matched_pairs | 51840 / 25920 |
| comparison_groups | 120 |
| answer_transition_groups | 480 |
| pair_transition_groups | 480 |
| collapse_transition_groups | 480 |
| evaluation_bundle_loads / training_trace_loads | 1 / 1 |
| train_steps / model_forward_calls / gradient_calls / optimizer_steps | 0 / 0 / 0 / 0 |
| model_state_loads / new_checkpoint_writes / network_calls | 0 / 0 / 0 |

Model-state loads mean loading parameters into a model, not tensor archive
deserialization. The saved evaluations archive is necessarily deserialized once
per diagnostic pass. Parent semantic checks, science, saved reconstruction and
fresh-process reconstruction are separate passes; do not call the per-pass work
one global read. Historical regression fixtures can perform their own model work;
zero neural work describes the diagnostic, not every process in the full suite.

Four science outputs, all local-only:

1. audit-plan.json: exact sealed manifest.
2. normal-pair-observations.json: all38880 saved pairs with losses and metadata.
3. loss-transition-decomposition.json: all25920 matched pairs and120 comparisons,
   with all three four-group partitions.
4. validation-summary.json: complete unchanged parent validation summary,
   180terminal/120contrast/120comparison records, provenance fingerprints and WORK.

The primary is fold-c347-diagnostic-v1 with diagnostic_execution_valid=true,
capability_gate_applicable=false,gate_f_candidate=false,production_adoption=false.
The envelope is fold-c347-execution-envelope-v1. Diagnostic PASS requires complete
coverage, schemas, provenance, arithmetic, protection and saved reconstruction.
There is no desired-sign or capability-improvement condition. Parent negative/zero
eligible and every parent subgate remain unchanged whatever the decomposition.

This can identify which error/correctness groups account arithmetically for a loss
change. It cannot identify a causal optimizer mechanism, prove convergence or
undertraining, establish calibration, choose an optimal rate or raise the capability
gate. No extra half-rate mean-CE arm exists, so no objective-by-rate factorial claim.

## Protection and regression contracts

Retain all497 C346 output files:6science+primary+envelope+489regression proofs.
The489 proofs are3records plus243module JSON/log pairs. New protection:
951sources=944+7OWN;9681inputs=9177+497+7. Native read leases have explicit capacity
9681 with no eviction/unlocked fallback. Every final uncached input pass covers
all9681 identities. The sealed manifest is the executable source for child
source_count/input_count; descriptive docs and constants must agree with it.

New own tests:40science+32execution=72.
Full6724 tests/245 isolated modules, including the complete own
suite once. Ordered full test-ID SHA256: 28b5c7fc80732b94cdb32f94f241cc142dff3e9da0dc68fdba26ded270ffef58.
The parent's6652 IDs/243 groups remain an exact ordered prefix with SHA256:
39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Actual loader candidates are6725 before the sole inherited C204
exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusion, skip or accepted-test edit. Keep the permanent C272 compatibility
seal in the authoritative handoff and run all eleven C272..C282 document consumers
on final activation bytes. Child own tests check this immutable requirement;
current ACTIVE guards use synthetic fixtures plus the actual final activation review.

Retained C347 completion inventory:501 files. These are4science+primary+envelope,
493regression proofs (3records+245module JSON/log pairs), validation-receipt.json
and validation.log. The495 validation/proof files form a separately hashed and
leased output set; they are not added to the9681 inherited-plus-OWN input count.
Other transport logs are useful local records but are not part of this required
501-file successor retention contract.

## Native Validate and Execute boundary

Reuse .venv-py31315:Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5,
CPUfloat64/threads2. No runtime upgrade is registered. Branch:feat/sft-target-loss.
Route:invoke_active_v2 ->invoke_c347 ->run_c347 ->c347_execution.
Run prefix:runs/c347-saved-loss-transition-<id>/.
The short user block parses dispatcher AST; dispatcher parses the selected launcher;
launcher parses itself/runner. Wrong branch, dirty tracked tree, stale ExpectedHead,
missing dependency or wrong/nonunique ACTIVE state skips without formal execution
or publication. Use the later reviewed activation HEAD, not the parent execution,
log publication, acceptance, source-only registration or main merge HEAD.

The C270+ authoring runtime gate remains in force. C347 restores its explicit
Validate-before-formal-logging boundary; historical C345/C346 execution records and
scientific verdicts are unchanged. Validate performs source compile/import, native
runtime, six accepted cleanup checks, protected parent/source/artifact validation
and the complete preregistered regression before a diagnostic is allowed. A failed
Validate reports AUTHORING_RUNTIME_PREFLIGHT_FAILED,experiment_executed=False and
execution_log_publish_attempted=False. It does not replace published latest.log/json.

The launcher invokes native --mode validate before entering its formal log or
publication try/finally. Validate creates a unique run folder and UTF-8
validation.log, compiles/imports the four owned Python sources/two own test
modules, then performs native runtime/cleanup/lock checks, the full protected
snapshot, immediate-parent saved semantics, all6724tests in245isolated modules,
complete test-proof verification and9681uncached final input rereads.

Only after the validation transcript closes and guards pass does Validate write
validation-receipt.json, schema fold-c347-runtime-validation-v1. It binds the
canonical unique run folder, execution HEAD, manifest, exact source/input maps,
compile/import inventory, native runtime, parent identities, cleanup receipt,
complete regression evidence, final input rereads and the closed log's SHA/size.
There is no self-hash cycle and no receipt on validation failure. A copied receipt
from another folder, stale HEAD, incomplete suite or altered transcript is refused.

The launcher checks successful completion and required files, rechecks branch/
tracked-tree/HEAD/ACTIVE, and only then opens the formal execution log. It copies
the complete successful validation text into that log. Execute reopens and leases
the9681 protected inputs plus a separate495-file validation/proof set. It verifies
the full receipt, source/input identity, cleanup and all per-module proof semantics
before creating science outputs. It reports the reused validation/proof binding,
performs the saved-only diagnostic and exact saved reconstruction, and completes
uncached rechecks of both sets. The envelope binds the validation receipt/log/
proof-set fingerprint, records one regression execution in Validate and zero in
Execute, and fixes the501-output retention contract. The expensive suite is not
executed a second time.

A separate fresh process revalidates the native runtime, accepted parent, complete
validation/proof set, both protection maps, diagnostic output bytes and reconstructed
summary, then rechecks all9681inputs and495validation/proof files. Only an invocation
that passed Validate enters formal log publication scope. An integrity failure after
successful Validate preserves and publishes that attempted execution as INVALID; it never
turns an invalid prerequisite into a scientific negative or triggers an automatic retry.

C347 execution_revision=C347-R0; timeout_cleanup_implementation=C344-R1. The six
native cleanup checks delegate to the accepted cleanup implementation. Its receipt
keeps schema fold-c344-r1-timeout-cleanup-preflight-v1 and revision C344-R1 while
binding this C347 execution HEAD. The parent's receipt separately remains bound
to its own C346 execution HEAD. Full isolated modules retain the same scoped R4/R5
monitor barrier; accepted historical tests and executor sources remain immutable.

## Stop and next response

After a complete execution fetch remote docs/experiment-run-logs/c347/latest.json
and latest.log. Distinguish scientific execution HEAD from the log commit. Check
the bound preflight, regression, diagnostic, source/input protection, final rereads
and fresh verifier before accepting diagnostic integrity. Report the full loss
decomposition with the unchanged C346 capability result and explicit claim limits.
On preflight SKIPPED repair the same C347 operational gate; do not advance the C
number. On an execution integrity failure use INVALID EXECUTION / RETRY SAME C347.
Preserve the attempt; no automatic retry. Transport failure does not justify a
scientific rerun, and no outcome here authorizes rerunning accepted C346.
