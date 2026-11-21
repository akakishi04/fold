# C341 preregistration -- saved length-gate localization

Date: 2026-10-29 Japan time.
Experiment C341-v5b-saved-length-gate-localization; stage V5-B-SAVED-LENGTH-GATE-LOCALIZATION.
Accepted scientific base 20478759b35b930170ac0e723f71da8788349e73.
C340 remains ACCEPTED VALID NEGATIVE; C339 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
Gate F NOT PASSED. No production adoption. Source publication is not activation.
An independent committed-byte review must PASS before a separate documentation-only
ACTIVE registration and user execution command. C342 NOT REGISTERED.

## One scientific question

Which unchanged local binding, masked-dependence and both-order criteria improve,
regress or remain failed after C340 replaces original4 TRAIN tokens with original5?

C340 completed its registered execution but did not pass its capability conjunction.
Normal HOLDOUT original6 correctness improved 1396->1439/1440 and both-query-correct
pairs improved 681->719/720. Only 2/5 candidate states passed the full gate. Candidate
340002 failed interior4, 340003 failed original4 with pooled short-domain losses of
7 answers/7 pairs, and 340004 still failed original6. The console gives their failure
counts, not the exact split/profile/language/criterion. Do not infer a masked-control
failure, shortcut mechanism or local causal explanation from pooled accuracy alone.

This diagnostic reads the complete saved measurements and the raw-verified parent
summary. It neither fits a model nor performs model inference. An immediate repeated
training intervention would leave the missing gate-localization evidence unresolved.

## Changed analysis and fixed scientific conditions

Add only a saved-measurement localization layer. Keep all five paired seeds
340001..340005, both original4/control and original5/candidate arms, all original2..6
and interior4 domains, TRAIN/HOLDOUT value partitions, languages, profiles, entity
sets and fact orders. Include every success and failure; no seed or cell selection.
Keep the original C340 models, predictions, states, prompts, thresholds and fixed
negative judgment. No new prompt, checkpoint choice, inference filter, loss term,
coefficient sweep, model-state load, optimizer update or production-code change.

Use immutable C330 numeric adapters/counts/criterion-transition helpers. Match exact
seed/domain/split/scorer-profile/language/entity-set/fact-order coordinates. Scorer
profile slots are not literal input names: original profiles are repeat/shared_prefix/
shared_suffix; interior profiles are u_dominant/balanced/v_dominant in that order.
Retain the actual input_profile as well as the scorer slot in every report.

Thresholds are unchanged: accuracy .90, query-pair accuracy .80, evidence drop .35,
query drop .35, and both-order accuracy .80. Each cell reports its original values,
failed criteria and max(0, threshold-value) deficits. Deficits are descriptive;
they add no tolerance, altered cutoff, ranking rule or causal interpretation.

## Training-exposure semantics

The old numeric helper carries C329-era static exposure annotations. C341 replaces
only those annotations on its own copied output records, without modifying the
accepted helper, scores, flags or thresholds.

|Arm|Named domains actually used for normal TRAIN fitting|Named domains not fitted|
|---|---|---|
|original4 control|original2/3/4 and interior4|original5/6|
|original5 candidate|original2/3/5 and interior4|original4/6|

Keep four distinct booleans: name_family_seen_in_training,
value_combination_seen_in_training, normal_prompt_seen_in_training and
masked_views_seen_in_training. TRAIN marks the logical value partition, including
in an unseen name domain; it does not establish that that prompt was fitted.
Normal prompts were fitted only when both the named domain and TRAIN partition were
seen. Masked views were never fitted in either arm. Original6 remains untrained in
both arms; candidate original5 TRAIN is fitted, while its HOLDOUT values are not.
Carry these fields into local cells, order cells, pooled strata and both sides of
matched transitions. No global monkeypatch of inherited constants is permitted.

## Complete localization and reconciliation

C340 measurements are ten ordered records with exactly seed/arm/score; score holds
original keyed by strings 2..6 and interior. Its saved seed_results records have
eight keys: seed, arm, original_pass, interior_pass, retention_pass, failures, support,
training_nonpadding_tokens. Validate the actual C340 parent summary before applying
an explicit six-field gate projection. Retain the complete original summary,
including support partitions, token counts and paired answer transitions.

For each of the 60 state/domain records, adapt 72 local cells and 36 order cells.
Reconcile every original/interior/retention flag and every local/order failure count
to the saved C340 writer output. For all 30 paired seed/domain contrasts, reproduce
normal HOLDOUT correct-answer and both-query-correct totals and gains, with exactly
288 answers/144 query pairs per state/domain. A query pair asks both entities under
one fact order; both-order correctness is a different gate.

|Diagnostic inventory|Fixed count|
|---|---:|
|Saved trained-state records|10|
|State/domain records|60|
|Local gate cells|4320|
|Both-order cells|2160|
|Matched local transitions|2160|
|Matched both-order transitions|1080|
|Pooled arm/domain/split/profile/language strata|144|
|Domain/criterion transition summaries|30|

For each criterion classify every matched pair as rescued, regressed, persistent
failure or stable pass; require conservation and exact agreement with arm-specific
stratum failure counts. Aggregate over all seeds and report failed seed identities.
Gate-cell/criterion rescues are not individual-answer rescues. The latter stay in
the inherited C340 summary, already checked against saved raw logits by its semantic
validator; aggregate cell counts cannot reconstruct individual answer identities.

Scientific diagnostic work is exactly 0 training steps, model forwards, gradient
calls, optimizer steps, model-state loads, new checkpoint writes and network calls.
Parent evidence reconstruction, full software regression, JSON processing and
publication are separate work. Tests themselves may exercise model code; this is
not a claim that the full launcher performs no computation or no test-time forwards.

## Immediate parent and complete evidence protection

C340 execution 15f88d08071ac0b36551fb2f61b3e10dbd0c6445.
Publication 586c03adad82d0ff53d0815f55c88ee44fc67239.
Folder runs/c340-length5-training-0c8af407e2564082b7221f1c95ddb709/.
Primary 263902957881a2a6a9bff426f540b7e05e8b43be46c1ce6e546e235cf0db7b7e.
Envelope a4b32eebbff72a6e6637bed1ef23e881dee77e9747b467d80349095909613c9a.
Require fold-c340-trained-v1 and fold-c340-execution-envelope-v1, scientific status
FAIL, scientific_execution_valid=true, capability_gate_applicable=true,
candidate_gate=false, eligible_seed_count=2, complete 6258-test evidence and all
6243 final uncached rereads. A valid failed capability gate is not an invalid parent.

Pin tools/c340_execution.py to 84c92a7225eaac526963dbe3b07439d25bf8dc48 and
fold_lm/v05_benchmarks/model_c340_length5_training.py to
4837a70777445d8964aa3aa1274aa09356bec20d before import. Keep the inherited helper
dictionary ABI. Reconstruct unchanged parent maps through C340.snapshot, then add
ALL 473 C340 outputs: six scientific files, primary summary, execution envelope and
465 regression proof files (three records plus 231 module JSON/log pairs). Validate
every proof byte, ordered successful test ID, PID relation and log marker.

Add seven OWN files: benchmark, executor, two test modules, runner, launcher and
this preregistration. Protection is 909 sources=902+7 and 6723 inputs=6243+473+7.
Reject collisions, changed inherited sources, missing artifacts or missing deciding
dependencies. Audit actual direct/lazy C340/C338/C337/C332/C330 and lower canonical
helpers against inherited source pins, not merely the existence of an execution HEAD.

Immediate parent reconstruction uses the actual four-argument trained contract:
C340.semantic_recheck(out340, data329, cx, read), under no_neural. Reconstruct its
saved logits, traces and token/accounting fingerprints, not optimizer updates.
Canonical data/prompt checks remain active. Do not dispatch the older diagnostic
parent's five-argument API or recursively rerun ancestor scientific bodies. All
ancestor bytes and module proofs remain protected.

Native R4 read leases span parent checks, regression, diagnostic and reconstruction
with explicit finite max_files=6723. Keep initial hashes and ALL 6723 final uncached
rereads. No default4096 capacity, eviction, omitted module proofs, unlocked fallback
or edits to accepted sources/tests/contracts/logs/dispatchers.

## Regression, outputs and execution ordering

Preserve all 6258 ordered parent test IDs, SHA
807b1fd8cbefff30b4d73e3f62b5a24170b014064e4e4a0a487800f8827ccd17.
Append actual 32 science tests then 24 infrastructure tests: 6314 selected tests /
233 modules, 6315 before the sole inherited exact mutable-ACTIVE C204 exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new skip or exclusion, cached success, accepted-test edit or automatic retry.
Use actual loaders and ordered test IDs, not numeric source-string assertions.
Each module runs in a fresh sequential process; preserve accepted C330 R1.2 PID
validation and begin/end markers. Bind generic module receipts to the NEW execution
HEAD and plan. Own plan/evidence schemas are fold-c341-regression-plan-v1 and
fold-c341-regression-v1. All 6314 tests must pass before diagnosis.

Four scientific outputs: diagnostic-plan.json, localization.json, transitions.json,
validation-summary.json. The child run_diagnostic(out, parent_out, read) and
semantic_recheck(out, parent_out, read) are both three-argument calls under no_neural.
Recompute every saved JSON result and compare exact canonical bytes. Hash/size-bind
all four outputs around reconstruction and final reporting. Primary schema is
fold-c341-diagnostic-v1; envelope is fold-c341-execution-envelope-v1.
A successor must preserve 475 C341 outputs: four science files, primary, envelope,
469 regression proofs (three records plus 233 module receipt/log pairs).

Route: invoke_active_v2 -> invoke_c341 -> run_c341 -> c341_execution -> native locks /
parent snapshot -> immediate C340 semantics -> 6314 isolated tests -> saved diagnosis
-> saved reconstruction -> 6723 final uncached rereads -> independent fresh verifier
-> console-only c341/latest.log + latest.json publication. No discarded neural
preflight is needed for this saved-only diagnostic. Local output prefix is
runs/c341-length-gate-localization-<id>/.

Native runtime remains Windows Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5 and
PowerShell7, CPU float64, two Torch threads; no environment reinstall. Branch,
tracked-tree, ExpectedHead, unique ACTIVE, dependency and AST guards precede logging.
Stale requests skip without execution or log publication. The standard user block
parses active_v2; dispatcher parses invoke_c341; launcher parses itself and runner.

Progress includes regression modules, hash/worker heartbeats, 144 pooled strata,
30 transition summaries, preserved parent gate and EVERY failed local/both-order
cell from BOTH arms. Print full seed/arm/domain/split/input_profile/language/entity/
permutation or fact-order coordinates, criteria, values, thresholds, deficits and
exposure metadata. Validate full failure inventory before emitting cells; no
hand-picked examples substitute for coverage. Do not print all 4320 successes.

## Fixed diagnostic gate and interpretation boundary

PASS means complete, consistent reconstruction of the entire saved cohort, all
parent counts/gains/flags, transition conservation and unchanged protected evidence.
Require run_execution_valid=true, full regression, all rereads, fresh verification
and successful log publication. Keep capability_gate_applicable=false,
gate_f_candidate=false and production_adoption=false. Parent candidate_gate remains
false and eligible_seed_count remains 2 regardless of which criteria are localized.

Any protection, schema, count, source, regression, PID, nonfinite or reconstruction
failure is INVALID / RETRY SAME C341. Publication-only failure repairs transport
without repeating diagnosis. Diagnostic PASS cannot promote C340, establish a
shortcut cause, prove an optimal curriculum or complete Gate F. C342 remains
unregistered until C341 is formally judged. No CI, paid service, retraining of
accepted models or artifact deletion is authorized by this diagnostic.

## Mandatory independent committed-byte review

After all seven files are committed, fetch remote bytes through EOF, compare Git
blobs with tested files, and have a reviewer distinct from both authors inspect
the completed change. Rerun all 56 own tests normally and under CP932 default-text-
open emulation. Audit UTF8/noNUL, compile/import/free names, real 6314-test inventory,
manifest/counts, direct/lazy dependencies, actual C340 writer fields, parent four-
argument and child three-argument dispatch, arm-specific exposure, all-cell coverage,
criterion versus answer transitions, failure publication, CLI and PowerShell AST.
Any fix requires renewed review of committed remote bytes before approval.

Science tests use real canonical data/renderers/scorers on explicitly synthetic
logits and a coherent full C340-shaped fixture, including negative/positive gate
transitions. Diagnostic saved-file reconstruction executes with neural calls and
torch.load forbidden. Infrastructure tests exercise real worker/fresh-verifier and
proof-map control paths using explicit synthetic parent, OS and diagnostic
collaborators; accepted PID/log validators remain real. These are author checks,
not native Windows leases, the 6314-test formal run or actual C340 saved diagnosis.
Record those limits, reviewed HEAD and post_authoring_review=PASS before a separate
documentation-only ACTIVE commit. Do not give the user a command before that gate.

Manifest SHA256:453b701fcf597a7ea8d38eb7b9457ee97693575f1349fa4903beebe5a1f6a647.
