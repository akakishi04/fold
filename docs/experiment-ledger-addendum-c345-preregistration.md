# C345 preregistration: saved objective and trajectory audit

Date: 2026-11-22 Japan time.
Experiment: C345-v5b-saved-objective-audit.
Stage: V5-B-SAVED-OBJECTIVE-AUDIT.
Acceptance base: a7174ae51f71f001901793603ab9f7ddb26ed923.
Manifest SHA256:
5e69553fd6661ef46459883500fd719b474fd7cacbd17d002c957eb3fb2f1a9f.

This is a retrospective diagnostic of accepted C344 artifacts. The question and
complete accounting rules are fixed before computing the new loss-level results.
It is not a new trained candidate or a confirmatory replication on fresh seeds.
Authoring and independent remote review must finish before activation; the later
authoritative handoff records review PASS and its target source commit.

## One scientific question

On the same fitted prompts, does pair-max's worse exact-answer binding accompany
a higher terminal pair-max loss, or a lower surrogate loss despite worse answers?
Use all saved C344 states, domains and logical splits, and complete recorded
preupdate loss/norm trajectories to constrain this interpretation.

The measured terminal losses are equal-weight means within each domain/split.
They are not the exposure-weighted objective over the entire training mixture.
No global optimum, convergence guarantee or particular internal cause follows.

## Changed and held constant

Changed: add arithmetic and descriptive reporting over immutable saved logits,
canonical query-pair metadata and recorded training traces.

Held: all ten C344 checkpoints, seeds344001..344005, arms mean_ce/pair_max,
canonical192TRAIN/96HOLDOUT rows, original2..6/interior4 domains, three profiles,
both languages and fact orders, full256 output classes, native_before predictions,
training schedule, actual token/target streams, rates, parameters and parent gate.
No new model forward/backward, optimizer creation/update, state load into a model,
checkpoint write, fitting data, external data, inference filtering or network call.
No seed exclusion, coefficient sweep, selected checkpoint or hand-picked time window.

The parent remains C344 ACCEPTED VALID NEGATIVE, candidate_gate=false and
eligible_seed_count=2, regardless of any loss difference discovered here.
Gate F remains NOT PASSED; no production adoption or capability gate is applicable.

## Exact accepted parent and writer contract

Scientific execution:8d1e1170cd614503deab1e09474fe82de4bba561.
Log publication:9d163289775373aaf62028a7b8aeacbfb41593a6.
Folder:runs/c344-pair-max-training-76ae8eb6e3bf4d08ac577c5fde9e0caa/.
Primary SHA256:610398ced893ff1d1885faf9bd02ffef57779ca2bd96bfa995b6929e6d8f20d7.
Envelope SHA256:c77f0fcf5fcbbf59d3961894713dbf8dcb30ae89841df0325b980a07d8913562.
Parent manifest:a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8.
Executor tools/c344_execution.py blob76c8663caafc97ece440df71e250e546198d425b.
Benchmark model_c344_pair_max_training.py blob6261a0c267df027835093c7ce53958f8f0034186.

The primary schema is fold-c344-trained-v1; its status is FAIL but
scientific_execution_valid=true and capability_gate_applicable=true. Its direct
validation_summary carries the negative result. Do not read a C343 nested summary
or treat a C344 FAIL status as an invalid execution. Require the C344-R1 revision,
exact six-case native timeout receipt, all6514 regression IDs/239 module proofs,
930source pins/8183inputs, final rereads and saved reconstruction flags.

The accepted evaluations.pt writer uses fold-c344-evaluations-v1 with ten records
in seed/arm order. Each has seed,arm,state_sha256,evaluation_policy,raw,receipts.
raw has evaluation/replay; each contains original string length keys and interior,
then split/profile/view. Read only each normal view for new terminal objectives;
validate all saved views/replay through the immutable parent validators. Match
state_sha256 to the trace final_sha256 and require native_before receipts.

training-traces.json contains ten ordered traces. Each of2400 loss_history entries
has exactly mean_ce,pair_max,selected; the norm is preclip_norm_history at the same
step. The recorded loss precedes that update. The first losses match across paired
arms because initial weights and inputs match. The final step's logged minibatch
loss is not the final checkpoint's full-cohort objective.

The immediate-parent call is exactly
model_c344_pair_max_training.semantic_recheck(out344,data_out,cx,read),four arguments,
under no_neural. C345's loader calls C332.load_data on the canonical C329 output
located through the inherited C330 parent folder, then C344.prepared. The C345
run_diagnostic and semantic_recheck signatures are
(out,parent_out,data_out,cx,read),five arguments. No ancestor training or neural
evaluation is rerun. All deciding direct/lazy repository dependencies must be pinned;
an omitted dependency is INVALID rather than recoverable evidence after the fact.

## Terminal objective measurements

For every saved state, domain, split and profile, reconstruct canonical query pairs
from language/entities/values/fact order and distinct counterpart queries/targets.
Require complete unique coverage of every row; do not assume arbitrary adjacency.
Verify the same targets used by the parent writer. Compute per-answer CE from the
saved finite CPUfloat64 logits over all256 classes, with no probability floor,
class filtering or replacement for overflow/nonfinite values.

For each true pair with losses a,b, retain both per-query losses, targets,
predictions and metadata; report mean_ce=(a+b)/2 and pair_max=max(a,b). Preserve
full256 first-index argmax semantics, including ties. Bind exact correct-answer and
both-query-correct counts to every parent's normal summary and paired contrast.

Inventory:10states x6domains x2splits =120 terminal summaries; all51840 normal
answers and25920 query pairs. There are60 paired seed/domain/split contrasts.
The terminal mean_ce statistic is over pair means (equivalent to the balanced
answer mean); its minimum/maximum are pair-mean extremes, not individual-answer
extremes. The pair_max statistic is over pair maxima. Report count/mean/min/max.

For both losses, delta is candidate minus control: positive is a larger loss.
Publish both deltas next to the unchanged parent answer/pair gains. No desired
sign is a diagnostic PASS condition. A lower loss with worse answers is compatible
with surrogate/answer tradeoff on those fixed prompts; a higher loss with worse
answers identifies an endpoint optimization shortfall relative to this comparator,
not a proof of its cause or a claim that training cannot eventually improve.
Original6 TRAIN contains familiar value combinations but was never fitted.

## Complete training trajectories

Validate every original trace with the accepted C344 checker, including schedule,
pair metadata, input-stream fingerprints, actual exposure, initial/final states,
continuous optimizer and fixed rates. Reconstruct every canonical event, family
mask and length mask. Retain all24000 preupdate rows and12000 same-step paired
differences without changing the recorded values.

Each step contains24 complete query pairs. Canonical slot2 is original2; slot3 is
original3; **slot4 mixes original4,original5 and interior4**. Reconstruct the exact
domain-pair counts at each step; the logged batch loss cannot be split into pure
constituent-family losses. Original6 has zero fitting pairs.

Use all12 consecutive fixed200-step blocks per state:120 block summaries.
Also use all2cycles x3slots x3profiles per state:180 group summaries. Report60 paired
block and90 paired cycle/slot/profile comparisons. Both partitions cover all24000
rows and preserve total exposure and norm-threshold counts.

For mean_ce,pair_max,selected,pair_max_minus_mean and preclip_norm, report finite
count/mean/minimum/maximum with math.fsum-based means. selected must exactly equal
that arm's registered objective. The gap is a descriptive within-pair imbalance.
For the common metrics excluding selected, report paired same-step differences
and negative/zero/positive counts. Both arms have different later weights; same
event does not turn later loss deltas into same-state causal interventions.

norm_gt1 counts stored preclip norms strictly greater than1. It is a conservative
threshold-exceedance description, not a literal count of all clipping calls or the
exact implementation's rescaling factors. No gradient starvation, causal clipping,
learned-then-forgotten exact answers or independent-observation inference follows
from these preupdate minibatch traces.

## Work, outputs and integrity gate

Per child computation/reconstruction pass:checkpoint_records10,
normal_answers51840,query_pairs25920,terminal_summaries120,terminal_contrast_count60,
training_trace_rows24000,paired_trace_rows12000,trace_blocks120,trace_groups180,
evaluation_bundle_loads1,training_trace_loads1. All neural/training/optimizer/model
state-load/checkpoint-write/network counters are0. Parent semantic checks, scientific
computation, saved reconstruction and fresh-process reconstruction are separate
passes; the per-pass count must not be represented as one global file read.
Historical regression tests can execute their own fixtures; zero forwards describes
the C345 scientific diagnostic, not all processes including regression.

Four science outputs, all local-only:

1. audit-plan.json: exact sealed manifest.
2. terminal-objectives.json: all25920 pair observations and metadata.
3. training-trajectory.json: all24000 rows and12000 paired row deltas.
4. validation-summary.json: parent scientific result unchanged,120terminal,
   60contrasts,120blocks,180groups,60paired blocks,90paired groups and work counts.

The primary is fold-c345-diagnostic-v1, with diagnostic_execution_valid=true,
capability_gate_applicable=false,gate_f_candidate=false,production_adoption=false.
The envelope is fold-c345-execution-envelope-v1. A diagnostic PASS requires every
schema/count/pairing/parent-result/arithmetic/protection/reconstruction invariant;
there is no capability-improvement or desired-sign gate. Any invalid/nonfinite/
missing/mutated input, skipped or failed test, broken replay/proof or absent protected
dependency stops the run: INVALID EXECUTION / RETRY SAME C345. No automatic retry.

## Protection and regression contracts

Retain all489 C344 output files:6science+primary+envelope+481regression proofs.
The481 proofs are3records plus239module JSON/log pairs. New counts:
937sources=930+7OWN;8679inputs=8183+489+7. Native read leases have explicit capacity
8679, with no eviction/unlocked fallback. Final uncached rereads must cover all8679.
All accepted historical sources/tests/launchers/preregistrations remain immutable.

New own tests:40science+24execution=64. Full6578tests/241isolated modules.
Full ordered test-ID SHA256:
2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Actual loader candidates6579 before the sole inherited C204 exclusion; the parent's
6514 IDs/239groups remain an identical ordered prefix with SHA256
c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3.
Excluded exact ID only:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusion,skip or accepted-test edit. Future successor retains491C345 outputs:
4science+primary+envelope+3records+241module JSON/log pairs.

## Native execution and timeout boundary

Reuse existing .venv-py31315:Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5,
CPUfloat64/threads2. No environment upgrade is part of this registration.
Route:invoke_active_v2 ->invoke_c345 ->run_c345 ->c345_execution.
Branch:feat/sft-target-loss. Run prefix:runs/c345-saved-objective-audit-<id>/.
The standard user block parses dispatcher AST; dispatcher parses selected launcher;
launcher parses itself/runner before logging. Wrong branch,dirty tracked tree,stale
ExpectedHead or nonunique/wrong ACTIVE experiment skips before scientific execution
and does not publish a log. Use the later reviewed activation HEAD, not the parent
execution,publication,acceptance or main merge HEAD.

C345 execution_revision=C345-R0. timeout_cleanup_implementation=C344-R1 explicitly
identifies the inherited accepted implementation. The six-case preflight delegates
to that pinned parent implementation; its receipt deliberately retains schema
fold-c344-r1-timeout-cleanup-preflight-v1/execution_revision C344-R1 but binds the
current C345 execution HEAD. The parent checker verifies it exactly. This does not
mislabel the child experiment. The full module runner uses the same scoped R4/R5
monitor barrier. Accepted historical tests and the C344 executor are not edited.

Sequence:six native timeout checks ->native locks and protected snapshot ->immediate
C344 saved semantics ->6578tests/241processes ->saved objective/trajectory diagnostic
->saved reconstruction ->8679uncached rereads ->separate fresh verifier ->log publish.
Parent R1 receipt is separately checked against its original execution HEAD.
All six early cases must pass without retry; they supplement the full test inventory.

## Stop and next response

After completion fetch remote docs/experiment-run-logs/c345/latest.json and latest.log.
Distinguish scientific execution HEAD from the log publication commit. Verify every
integrity condition and the complete diagnostic output, then report objective/answer
relations and complete trajectory summaries without inventing a causal conclusion.
If valid,accept diagnostic integrity and design the next one question under the
conversation protocol. If invalid,repair/retry C345 only. Never rerun accepted C344
to repair log transport or to replace an unfavorable loss-level observation.
