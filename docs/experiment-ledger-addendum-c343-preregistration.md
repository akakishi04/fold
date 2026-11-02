# C343 preregistration: complete saved mixed-length localization

Date: 2026-11-02 Japan time.
Stage: **V5-B-SAVED-MIXED-LENGTH-LOCALIZATION**.
Experiment ID: `C343-v5b-saved-mixed-length-localization`.
Branch: `feat/sft-target-loss`. Native repository: `M:\asobiba\fold`.
Acceptance base: `50c277fff5242244dd82a87d392e543dc8c3594f`.
This source/preregistration commit is not ACTIVE. A separate documentation-only
activation follows independent review of all seven committed remote files.
The full activation HEAD is the user launcher's ExpectedHead.

## 1. One scientific question

Where do C342 mixed45 improvements, regressions and remaining binding, masked
dependence and both-order gate failures occur relative to actual arm-specific
training exposure? Diagnose every saved coordinate, including successful conditions,
and distinguish fitted TRAIN prompts from held-out value combinations and untrained
name domains. Track changes in individual answers as well as changes in gate cells.

C342 is ACCEPTED VALID NEGATIVE, not an invalid execution. Its candidate full gate
passed2/5, equal to the control count but with different passing seeds. Original4
gained50normal HOLDOUT answers/48pairs, entirely in342001; that seed improved
other domains broadly. Candidate342003 lost5six answers/4pairs. Pooled six gains
hide6individual regressions and pooled interior gains hide30. These facts motivate
complete paired accounting; they do not identify a neural mechanism or license a
selected-seed/profile follow-up. The acceptance report is
`docs/experiment-ledger-addendum-c342-c343.md`.

## 2. Fixed inputs and comparison

Use the exact ten saved C342 states, represented by their saved evaluation records;
do not select or load weights into a model. Seeds342001..342005, arms in fixed order
`original5`, `mixed45`. No fresh seed, checkpoint, training, inference or prompt
intervention. Analyze original2,original3,original4,original5,original6,interior4,
both TRAIN/HOLDOUT partitions, all profiles, languages, entity sets, value pairs,
fact orders and queries. Full cohort order is `product(SEEDS, ARMS)`.

Parent scientific execution: `e379de3ff300dd01381eeb90055c017c87ead670`.
Parent log publication: `1f8a890f5a08fe2e43fdfe847b06f936b9cb6472`.
Parent folder:
`runs/c342-mixed-length45-cceefd2e5093444483eb61f6f883e058/`.
Parent primary SHA256:
`47862c134f7f3be25784a88694e0bc1e29041772c025006c256673dc83695775`.
Parent envelope SHA256:
`6d8e1ac497fd28f0c6e58fa2770526619fc0bbc47de158ab3803bcbc7559481a`.
Parent manifest:
`538150bd2b43ff286e4d5b0e0c1d665ea1e1c4d43cf8148cba1c5d1a4192734c`.

C342 executor blob `780274ffd0236d0a24147cfb7a9b7015ee4eb0a5` and benchmark blob
`7a3d1c3d2aca1cb3b632a2ef490fff5c76028289` are checked before import. Canonical data
comes from `h['c330'].PARENT_FOLDER/science`, specifically the accepted C329 folder
`runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/science`.
Keep exact canonical192TRAIN/96HOLDOUT logical rows and original/interior prompt
banks. Canonical data hash:
`1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1`.
Labels classify saved outputs; they are never supplied as new inference inputs.

## 3. Actual parent writer/loader contract

The primary schema is `fold-c342-trained-v1`, the envelope is
`fold-c342-execution-envelope-v1`, and scientific execution must be valid even
though status is FAIL. Require capability_gate_applicable=true, candidate_gate=false,
eligible_seed_count=2 and the exact full C342 summary/work/manifest contracts.

`measurements.json` records have exactly seed/arm/score. Score has original/interior;
original has string keys2..6. Seed-result rows have exactly eight fields:
seed,arm,original_pass,interior_pass,retention_pass,failures,support,
training_nonpadding_tokens. A child projection validates these extras before
selecting the six gate fields; complete parent_validation_summary is retained.

Paired comparisons have exactly13fields:seed,control_full_pass,candidate_full_pass,
four_answer_gain,four_pair_gain,six_answer_gain,six_pair_gain,short_answer_gain,
short_pair_gain,interior_answer_gain,interior_pair_gain,original_by_length,interior.
No guessed old field names or silent removal of support/token information.

`evaluations.pt` has exactly schema/records and schema `fold-c342-evaluations-v1`.
Each record has seed,arm,state_sha256,evaluation_policy,raw,receipts. Policy is
native_before; raw/receipts each have evaluation/replay. Validate all114saved views
per state, dtype, shape, finite values, detachment and both mode receipts:
171model calls,342query projections,16416rows,0grad calls. Reconstruct scalar scores
with the immutable scorer and require exact canonical JSON equality to measurements.
Saved replay must satisfy1e-9 and exact argmax conditions inherited from C342.

The immediate parent call is exactly:
`C342.semantic_recheck(out342, data_out, cx, read)` (four arguments).
It reconstructs saved weights/trace/token semantics without model forward. Do not
copy the different three-argument C341 diagnostic ABI.

Child APIs are:

```python
run_diagnostic(out, parent_out, data_out, cx, read)
semantic_recheck(out, parent_out, data_out, cx, read)
check_summary(value)
report_failures(out, read, emit)
```

Both child paths invoke the actual load_inputs/reconstructed/analyze chain. Each
reads one saved evaluation bundle; no model object is built or receives a state.
Parent reconstruction also reads saved checkpoint data; this is not a model-state
load and is separately scoped from child diagnostic work. Older ancestor science
is not recursively rerun; its accepted bytes and regression proofs remain protected.

## 4. Exposure semantics and units

Record four booleans separately:name_family_seen_in_training,
value_combination_seen_in_training,normal_prompt_seen_in_training,
masked_views_seen_in_training. A TRAIN value combination alone does not imply that
an original6 prompt was trained. A trained name family alone does not imply that
a HOLDOUT value pair was trained. Masked views were never fitted.

Two integer fields are attached to every applicable output:

- `domain_presentations_per_logical_train_row`: all-profile total presentations of
  one canonical TRAIN logical row in that domain across the complete2400update fit.
- `domain_presentations_per_logical_row`: the same count for TRAIN; zero for a
  HOLDOUT logical row.

These are NOT counts of repetitions of one literal rendered prompt. Profiles vary
across fitting. The accepted schedule/exposure reconstruction establishes coverage.

|Domain|original5 control|mixed45 candidate|
|---|---:|---:|
|original2|200|200|
|original3|200|200|
|original4|0|50|
|original5|100|50|
|original6|0|0|
|interior4|100|100|

The diagnostic replaces only obsolete exposure annotations copied by the immutable
numeric localization helper. It does not change any parent score or threshold.

## 5. Complete fixed accounting

|Object|Count|
|---|---:|
|Saved seed/arm records|10|
|State/domain records|60|
|Local gate cells|4320|
|Both-order cells|2160|
|Paired local gate transitions|2160|
|Paired both-order transitions|1080|
|Pooled arm/domain/split/profile/language strata|144|
|Domain/criterion transition summaries|30|
|Saved normal answer observations across both arms|51840|
|Paired normal answer transitions|25920|
|Paired two-query transitions|12960|
|Seed/arm/domain/split support summaries|120|
|Seed/domain/split normal transition summaries|60|

Per state/domain, normal TRAIN has576answers/288query pairs and normal HOLDOUT has
288answers/144pairs. The answer inventory is10*6*(192+96)*3=51840. A two-query pair
keeps language, entities, values and fact order fixed and asks both entity queries.
It is distinct from the both-order gate, which matches across reversed fact order.

All4320local cells retain coordinates and original metrics. The fixed thresholds
are accuracy>=.90,query_pair_accuracy>=.80,evidence_drop>=.35,query_drop>=.35.
All2160both-order cells retain accuracy>=.80. Deficit is max(0,threshold-value),
descriptive only. Gate transitions report rescued/regressed/persistent/stable_pass
for each criterion; different criteria can fail together and are not disjoint errors.

Normal answers use immutable C337.audit_logits with first-index all256-class
argmax. Classify as correct,wrong_observed,absent_digit,outside_catalog. Store the
original prediction, target and other displayed value, never a repaired prediction.
Every paired answer retains row ID,language,entities,values,fact order,query,profile,
both predictions/kinds and arm exposures. Every paired query record retains both
row IDs, both predictions/kinds and both-correct flags.

Correctness transitions are rescued,regressed,persistent_failure,stable_correct.
Store full4x4control-to-candidate kind matrices, including wrong-to-different-wrong
changes. Verify matrix margins,correctness totals,prediction-change bounds and
query-pair feasibility. Net answer gain must equal rescues minus regressions; net
pair gain must obey the separate pair identity. Reconcile all30parent HOLDOUT
contrasts including individual rescued/regressed counts, not just net differences.
Reconcile all120normal summaries to local-cell counts and parent HOLDOUT support.

## 6. Fixed decision rule and interpretation boundary

This is a diagnostic integrity experiment. PASS requires complete unique ordered
coverage, exact parent scalar/gate/count reconstruction, all normal/pair transition
identities, full saved-output reconstruction, every software/protection check and
fresh verification. Any mismatch is INVALID / RETRY SAME C343, not a scientific
reason to exclude a row, seed, profile, language or failing domain.

A valid diagnostic PASS does not improve a model. Preserve C342 candidatefalse/
eligible2 and its accepted negative. capability_gate_applicable=false,
gate_f_candidate=false,production_adoption=false. No post-hoc favorable gate,
threshold tolerance, selected checkpoint, candidate filtering or new fit.

Localization may show errors already occur on fitted prompts, or occur only on
held-out conditions. This is evidence about error location, not proof of a causal
representation, attention collision, parity rule or optimization mechanism. The
structured value split remains unchanged. TRAIN/HOLDOUT differences alone do not
prove a shortcut. Seed initialization and schedule are not causally separated.
No claims about optimal mixture, unseen arbitrary lengths or general language.

## 7. Scientific work and resources

Child scientific training steps, model forwards, gradients, optimizer steps,
model-state loads, checkpoint writes and network calls are all zero. Counting,
tensor argmax/scalar reductions, JSON serialization, saved-logit reads and hashing
are real CPU/I/O work; zero neural forwards does not mean zero cost or instant run.
Parent validation and software regression are separately required and may exercise
synthetic models. They are not new C343 scientific fitting or inference.

All sources and input files remain read-only during science. New outputs use
exclusive-create writes under `runs/c343-mixed-length-localization-<id>/science`.
Four scientific files:diagnostic-plan.json,localization.json,transitions.json,
validation-summary.json. Primary summary and execution envelope wrap these with
source/input/artifact identities and execution proofs. All raw arrays/checkpoints
and new diagnostic artifacts remain local-only, not tracked in Git.

Print every failed local and both-order cell from both arms, all144strata and
30criterion summaries, all120normal support and60normal transition summaries.
Individual answer/pair records remain complete in transitions.json; console
summaries are not permission to omit them. Reporter validates failure publication
against the saved inventory. Parent negative is printed separately.

## 8. Software inventory and historical immutability

Own64tests=40science+24infrastructure. Full6442tests/237modules. Before the sole
inherited exact mutable-ACTIVE exclusion,6443tests. Keep the ordered parent6378
prefix byte-for-byte; no additional exclusions, skips or accepted-test changes.

Excluded exact inherited ID:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Parent ordered-ID SHA:
`76dfa4fd2952bdffd80250e57880d58cda72e7f7c16402c1817fed39ff294460`.
Full ordered-ID SHA:
`0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5`.
Counts and IDs come from actual unittest loaders/build_plan, not source literals.
Regression uses one fresh process per module, reports progress and saves each
module JSON/log plus plan, aggregate result and receipt. Require all counters zero
and all process exits zero. Do not run the formal native regression during authoring.

Before registration run all64own tests normally and under CP932-default-text emulation;
use actual PowerShell ParseFile for dispatcher/launcher/runner. Audit UTF8/noNUL,
compile/import, pyflakes, recursive Python global binding, exact source assertions,
actual test inventory, CLI positions, parent schemas, production ordering and all
deciding-path direct/lazy source dependencies. These author checks are separate
from the user's native full suite and protected-artifact run.

## 9. Source and artifact protection

Seven OWN additions:benchmark,executor,science tests,execution tests,run_c343.ps1,
invoke_c343.ps1,and this preregistration. Source923=parent916+7.
Protected inputs7693=parent7205+all481parent outputs+7OWN. Retain all473parent
regression proof files, not just summary/envelope. Explicit finite native lease
max_files7693; hash every input and perform all7693final uncached rereads.

Bootstrapping checks exact immediate parent executor and benchmark bytes before
import. Dependency coverage includes C330 localizer, C342 parent, C332 helpers,
C329/C324 canonical raw/context/query-pair paths, C331 scalar scorer and the
C340/C338/C337 support-classification chain, including lazy imports. C341 scientific
code is an immutable authoring reference, not a child production import. Retain
all inherited source pins and protected artifacts; no dependency may be justified
solely by reconstructability from a commit after execution.

Future successor must retain all483C343 outputs:four science,primary,envelope and
477proofs (three records plus237module JSON/log pairs).

## 10. Native sequence, launcher and stop rules

Native environment remains Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5,
CPUfloat64 with twoTorchthreads; do not substitute a globally installed runtime.
Entry is `tools/invoke_active_v2.ps1`, then invoke_c343.ps1,run_c343.ps1,
tools/c343_execution.py. The immutable legacy dispatcher stays pinned.

Before any logging/publication, check branch,clean tracked tree,ExpectedHead,
unique authoritative ACTIVE token,required dependencies and PowerShell syntax.
The standard user block parses the active_v2 dispatcher; dispatcher parses selected
launcher; launcher parses itself and runner. Stale/wrong/dirty invocation prints
SKIPPED,does not start science and does not publish a log.

Execution order: native read-lock probe -> finite lease/snapshot -> exact parent
semantics -> full isolated regression -> no_neural diagnostic -> no_neural saved
reconstruction -> all7693uncached rereads -> summary/envelope/report -> separate
fresh verifier -> run_execution_valid=true -> dedicated text-log publication.
The actual production ordering is tested with positive and fail-fast paths.
Use only exact parent C342 semantics; do not launch another training run.

Expected phases include saved_mixed_length_localization and
saved_diagnostic_reconstruction, module begin/end records and worker/hash heartbeats.
Terminal scientific marker identifies10states,4320local,2160order,
25920answer transitions,12960query-pair transitions,0forwards/0updates.
Publisher mirrors only docs/experiment-run-logs/c343/latest.log and latest.json.

After user completion fetch the exact remote log/metadata, distinguish execution
HEAD from publication commit and judge integrity before diagnostic status.
If INVALID, minimally repair this same C343 without changing the design. If only
log publication fails, repair transport without rerunning science. After a valid
result, accept it and prepare C344 under protocol v2 in the same response.
Freeze this branch while the user runs. Do not register C344 before C343 judgment.

## 11. Manifest seal and review activation

C343 manifest SHA256:
`7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6`.
Serialization is sorted-key compact UTF8 JSON,ensure_ascii=false,allow_nan=false,
with one terminal LF. The manifest records the full fixed work and exposure table.

Independent post-authoring review must fetch all seven committed remote files
through EOF and match tree/local blobs. Any source fix requires review of the new
committed bytes. Review PASS and its exact source HEAD are recorded in
docs/c343-post-authoring-review.md and authoritative handoff in a separate
documentation-only activation. Do not issue a user launcher before that PASS.
