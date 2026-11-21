# C330 preregistration -- saved gate-failure localization

Date:2026-10-17 Japan time.
Experiment:C330-v5b-saved-gate-localization;stage:V5-B-SAVED-GATE-LOCALIZATION.
Acceptance base:a7a36bb212656f08bd8d1c5402512ce28acb1e00.
C329 remains ACCEPTED VALID NEGATIVE;Gate F NOT PASSED;C331 NOT REGISTERED.
This protected contract requires separate committed-byte review and ACTIVE registration.

## One scientific question

Which unchanged local binding,masked-dependence and both-fact-order gates remain
unmet after C329's fixed budget extension, and which exactly matched conditions
improve or regress between prefix1200 and extended2400?

C329 improved interior HOLDOUT answer and both-query counts in allfive trajectories,
with four complete interior passes and one joint success. Its original2..6 retention
was only1/5. Before another fitting intervention, localize what actually failed.
This is a saved-evidence diagnostic, not a claim that any failure category causes
another, and not permission to weaken an existing gate.

## Frozen cohort and complete scope

Use all ten C329 checkpoint records:seeds329001..329005,arms prefix1200/extended2400.
Do not select the successful seed or just the extended checkpoints. Both logical
TRAIN and HOLDOUT splits remain present. Domains:original2,3,4,5,6 and interior4.
Original1 is excluded because it was descriptive only, not part of the parent gate.
Within each domain:three profiles,two languages,three entity subsets and both fact
orders. Every source record is retained,including complete successes.

The immutable C270 scorer stores profiles tripled/shared_prefix2/shared_suffix2 as
OPAQUE SLOTS. They do not literally describe every child's name length. Expose BOTH
scorer-profile and actual input-profile in each localization record:
- original2..6:repeat/shared_prefix/shared_suffix;
- interior4:u_dominant/balanced/v_dominant.
C304.score_length and C321.score_new supply this mapping without altering inputs.
Original5/6 name families were not included in C329 fitting even where the logical
split field is TRAIN. Preserve that distinction with explicit metadata.

## Exact parent metric schema and reconstruction

C329 measurements.json has ten records with seed,arm,original,interior,single_character.
Original maps string lengths2..6 to scores;interior is one score. Each score has
cells,two_order,totals,passed from the actual C270.score writer.
Each local cell has split/profile/language/entities/permutation,rows/correct/accuracy,
query_pair_accuracy,collapsed_pairs,pairs,evidence_drop,query_drop,answer_nll,passed.
Each both-order cell has split/profile/language/entities,groups/both_correct/accuracy,
passed. No similarly named field is substituted. Reject unknown/missing schemas,
duplicate or missing coordinates,boolean counts,nonfinite values and inconsistencies.

For local cells the denominator is16TRAIN or8HOLDOUT,with8/4 query pairs. Derive
integer both-query-correct counts from query_pair_accuracy*pairs and verify exact
normal-accuracy/count agreement and feasible paired/collapse counts. Recover
masked correct counts as(accuracy-drop)*rows and require a valid integer count.
For order cells the denominator is16/8 groups. Validate normal-answer consistency
across the two constituent fact orders. Recompute all saved local,order,profile
aggregate,domain and seed gates;compare them with C329 validation-summary.json.
Reconcile all per-seed/domain HOLDOUT normal and both-query counts and paired gains,
including the original2..6 sum and the unchanged C329 composite gate. This does not
reconstruct individual rescued ANSWERS from aggregate counts;the parent's saved
semantic verification independently checks the raw-logit contrasts first.

## Fixed categories and matched transitions

Keep exactly the existing thresholds:normal accuracy>=.90,query_pair_accuracy>=.80,
evidence_drop>=.35,query_drop>=.35,both-order accuracy>=.80. No threshold search,
tolerance-based softening,rounding-up or pooled-mean override.

Retain each of the four local failed criteria separately and assign one exclusive
local category:
- pass:no failed local criterion;
- normal_binding_only:accuracy and/or query-pair fails,neither masked-drop fails;
- mask_only:both normal criteria pass,but evidence/query drop fails;
- mixed:normal binding and masked-drop criteria both contain a failure.
Both-order failure is a separate record,not hidden in or added as an independent
sample to the local categories. Overlapping criteria counts must not be summed as
if they were unique failed cells. A mask-only category does NOT prove a shortcut.

Match by exact seed/domain/split/scorer-profile/language/entity-set/fact-order key;
order records omit only the fact-order coordinate. Input row order is not the
matching mechanism. For each criterion preserve rescued,regressed,persistent-fail
and stable-pass transitions. Their partition must equal the full paired denominator
and their before/after totals must agree with stratified failed-criterion counts.

## Work and diagnostic acceptance

10checkpoint records*6domains=60score records;
4320local cells and2160both-order cells;
2160matched local transitions and1080matched order transitions.
Stratified summary:144arm/domain/split/profile/language groups,30local/15order cells
each,including allfive seeds. Preserve full coordinates locally. Print all10parent
seed flags,72extended2400 strata and30domain/criterion transition summaries.

New training steps,model forwards,gradient calls,model state loads,optimizer steps,
new checkpoints and network calls areALL0 in the diagnostic. Parent verification
still reads the existing tensor bundles and reconstructs parent metrics;this is
separately scoped work,not a neural-model state load or a new inference run.
Diagnostic construction and saved reconstruction each traverse the full inventory;
this workload is not represented as free or as a single raw-file read.

PASS means complete valid inventory,reconciled original counts/gates,unchanged
inputs and reproducible localization. Any distribution of failure categories,
including no failures,can be a valid diagnostic result. C329 remains its original
VALID NEGATIVE irrespective of C330 PASS. capability_gate_applicable=false.
No capability improvement,causal mechanism,optimal budget,capacity limit,unseen-name
transfer,independent statistical samples,Gate F passage or production adoption.

## Parent evidence and source coverage

Scientific execution:f8582ca34bd7e10c7403713e935debe94720dfde.
Publication:2d181d23c7f84749384e9283c8d8de2df7619bd8.
Folder:runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
Primary science/summary.json SHA256:
89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
Mandatory execution-envelope.json SHA256:
6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Primary schemafold-c329-science-v1,statusFAIL,diagnostic_execution_valid=true,
candidate_gate=false,paired_success_count1. Envelopefold-c329-execution-envelope-v1,
scientific_statusFAIL. Validate both exact hashes,manifest/work,complete5770test
receipt,saved reconstruction and1577final uncached rereads. The complete832-source/
1577-input maps must match in both records. Eight outputs+primary+envelope=10files.

Before diagnosis invoke unchanged C329.semantic_recheck(out,data,old,new,cx,read)
under no_neural. It understands the five trajectories/ten checkpoint writer schema,
not the older ten-independent-fit schema. Reconstruct parent saved traces,checkpoint
hashes,raw-logit metrics and full summary;validate canonical data/prompts. No parent
model forward or recursive older semantic body. All inherited bytes remain checked.
C330 then reads measurements.json and validation-summary.json through its own loader;
its run path actually invokes that loader. No accepted function or global is patched.

Protection838sources=832inherited+6own;
1593inputs=1577inherited+10immediate-parent files+6own.
Own benchmark/executor/test/runner/launcher/contract all protected. Direct/lazy
C329/C328/C326/C325/C324/C321/C304/C270/C267 and recovery dependencies inherit pins.
Native unchanged R4 Windows leases span the entire worker. Independently hash initial
reads and finally reread ALL1593inputs without the cache. No unlocked fallback,
source replacement,smaller-map shortcut,artifact deletion or environment change.

## Regression, writer and verification

48own tests;5770inherited+48=5818selected tests;219modules. There are5819before the
sole inherited exact C204 mutable-ACTIVE exclusion. No new exclusions or skips.
Construct actual suites and unique test-ID sets;print ordered digest. Historical
regression runs unmodified in a separate ordinary interpreter. Full5818success is
required before diagnosis. No neural preflight is added to this saved-only child.

Route:PowerShell7 ->invoke_active_v2 ->invoke_c330 ->run_c330 ->c330_execution controller
->native locked C329 snapshot/parent semantics ->ordinary full regression ->saved
localization under no_neural ->saved JSON reconstruction ->1593final input rereads
->primary/envelope ->fresh verification and pure-JSON reconstruction ->console push.

Four child outputs:diagnostic-plan.json,localization.json,transitions.json,
validation-summary.json. Localization keeps all4320local/2160order records with
original numeric measurements and failed criteria. Transitions keeps2160/1080pairs.
Primary schemafold-c330-diagnostic-v1;envelopefold-c330-execution-envelope-v1.
Both carry full source/input maps. Bind output hashes/sizes before and after saved
reconstruction and again before result/envelope writing. A fresh process checks all
source/input/output bytes,complete unions,parent identity,manifest,full regression,
summary conservation,and reconstructs the child from saved parent JSON again.
It is not a new neural replay or replay of historical optimizer updates.

Local:runs/c330-localization-<id>/science plus enclosing execution-envelope.json,
regression-result.json and science/regression/verify logs. Only console text is
published to docs/experiment-run-logs/c330/latest.log and latest.json;no tensors/data.
Use10second heartbeats and phase markers. No1200/2400training progress is expected.

## Authoring review and stops

Manifest SHA256:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
Reread all6committed files and compare remote Git blobs with tested local bytes.
Rerun48own tests,CP932-default-text-open emulation,UTF8/no-NUL/compile/import and
recursive free-global audit after reread. Verify actual writer/loader signatures,
profile-slot mapping,full-cell inventory and parent composite/count reconstruction.
Source-string assertions must inspect their exact target function. Suite counts use
actual test loaders,not numeric source-literal matching. Synthetic parent/metric/
lease fixtures are explicitly not native FOLD or full5818historical test success.
Retain dispatcher/selected-launcher/runner PowerShell AST checks before invocation.

Stale branch/HEAD/ACTIVE/host/dependency/dirtytree/AST failures SKIP before logging
or publication. Any source/input/schema/count/criterion/parent/saved-reconstruction/
regression/envelope failure is INVALID;repair SAME C330,no automatic retry,no C331.
An observed failed model criterion is valid diagnostic content,not a reason to
refit or change a threshold. Publication-only failures are repaired without redoing
diagnosis. Runtime remainsPython3.13.15/Torch2.10.0+cu130/NumPy2.3.5.
No CI,paid services,package installation,artifact deletion or accepted-result edits.
