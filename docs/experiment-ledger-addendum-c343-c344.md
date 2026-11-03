# C343 acceptance and C344 pair-max training boundary

Date: 2026-11-04 Japan time.
**C343 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).**
C342 remains ACCEPTED VALID NEGATIVE, candidate_gate=false / eligible_seed_count=2.
Gate F remains NOT PASSED. No production adoption. This acceptance does not activate C344.

## Execution identity and validity

Scientific execution: `1effc2138967715e9e9319e1da19c3653e4fd9ac`.
Log publication: `74eda8f681f7a68f1d8c4ae91203c2b151855ce6`, sole parent execution.
Publication changes only docs/experiment-run-logs/c343/latest.json and latest.log.
All seven files reviewed at source `10a4cc6e69e52bfd657cd119b4c85f46cd14e761`
remain unchanged through activation and publication.

Published Windows log: 890204 bytes, SHA256
`bd3f00df72c1995e1880bb0f9b9faaa99b346e46b9e46434321b02cafa2ced3d`.
Git LF: 886413 bytes / 3791 lines, SHA256
`c7ce7b9fd72af23c7ced69c0130582b712a1fd8dad6e0153ea4fd5d1a32bac2e`.
LF-to-CRLF reconstruction exactly matches metadata. Remote content and Git blob
`45d91f9b54c1375bcbdcff57dc19c100fccbbc94` agree.

6442 tests / 237 modules PASS in 2956.442 seconds; failures/errors/skips all zero.
All 237 module begin/end records and individual test footers agree; all 240
module/regression/science/verify exits are zero. Ordered test-ID SHA256:
`0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5`.
Native lock probe PASS; 923 sources / 7693 protected inputs; all 7693 final
uncached rereads and separate fresh verification complete. run_execution_valid=true.
Child scientific forwards/updates are zero. Parent semantics and regression proofs
were reconstructed without rerunning ancestor scientific computations.

Folder: `runs/c343-mixed-length-localization-f1a8f5665ebb48c98b273cb549e721fd/`.
Primary: `883c1c0142173f038bec25f65589643af9ba40ef2442e7c376b845a61f1477ce`.
Envelope: `275ac041de4a858ca5a7f50aabb16898e85befebb2ee3ba6159a06198a7c993a`.
Manifest: `7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6`.
Successor retains all 483 C343 outputs: four science files, primary, envelope and
477 regression proofs (three records plus 237 module JSON/log pairs).

## Complete accounting and independent reconciliation

All 144 strata represent 4320 local and 2160 both-order cells. The complete 261
failed-local and 141 failed-order rows reproduce every stratum's criteria/patterns
and all 30 criterion-transition summaries. These two types of cells can overlap;
they are not independent wrong answers.

All 120 normal support and 60 paired normal summaries reconcile 51840 observations,
25920 paired-answer transitions and 12960 query-pair transitions. Independent review
checked full 4x4 kind-matrix margins, correctness conservation, answer/pair gains,
prediction-change bounds, denominators and exposure fields. Every corresponding
C342 published HOLDOUT support/contrast and failure count agrees. Parent negative
status is preserved, not replaced by the child diagnostic PASS.

Individual transition records remain local-only in transitions.json. The author
reviewed exact remote logs, complete published aggregates, immutable writer/verifier
code and native completion evidence; it did not transfer/reexecute all native
checkpoints or 7693 inputs in the author environment.

## Deciding findings

Candidate normal results across five seeds:

|Domain|Actual TRAIN exposures per logical row, all profiles|TRAIN correct /2880|HOLDOUT correct /1440|Failed local TRAIN/HOLDOUT|
|---|---:|---:|---:|---:|
|original2|200|2880|1440|0 / 0|
|original3|200|2880|1440|0 / 0|
|original4|50|2880|1440|0 / 0|
|original5|50|2880|1440|0 / 0|
|original6|0|2874|1434|2 / 3|
|interior4|100|2749|1366|16 / 17|

Exposure counts are per canonical logical TRAIN row across all profiles, not
repetitions of one literal prompt. HOLDOUT rows and all masked views were never
fitted. In original6, TRAIN means familiar value combinations, not fitted names.

### Interior4: fitting failures as well as held-out failures

Candidate interior TRAIN has 131 wrong answers, all wrong_observed. Seed342001
has 99 errors (477/576 correct); seed342005 has 32 (544/576). Both domains were
actually included in fitting. Candidate HOLDOUT has 74 errors: 58 wrong_observed
and 16 absent_digit. No outside_catalog errors occur.

Across the 1440 TRAIN query pairs, 1312 are both correct, 125 have exactly one
correct answer and three have neither correct. Because all 131 errors are the
other displayed value, the 125 single-error pairs give the same value to both
queries; the three double-error pairs swap the two values. This is derived from
the complete support/pair counts, not only failed-cell rows. One TRAIN error is
in a passing cell; failed-cell error totals alone would miss it.

|Interior4 split|Control -> candidate correct|Rescued answers|New regressions|Wrong in both arms|
|---|---:|---:|---:|---:|
|TRAIN|2677 -> 2749 /2880|132|60|71|
|HOLDOUT|1295 -> 1366 /1440|101|30|44|

All 33 candidate failed local interior cells are mixed binding/masked failures;
mask-only failures are zero in both arms. Accuracy/query-pair gate failures have
33 persistent, zero new failed cells and 36 rescues; both-order has 17 persistent,
zero new failed cells and 17 rescues. These cell transitions do not negate the
60 TRAIN / 30 HOLDOUT individual-answer regressions. Mask criteria themselves
also regress in some cells (evidence three, query one).

342005's eight failed local cells are Japanese v_dominant, entity sets [0,2] and
[1,2], both orders and splits, each with half the answers correct and no both-query
correct pairs. 342001 additionally fails Japanese u_dominant/balanced [1,2] and
some English v_dominant conditions. This is descriptive localization, not a basis
for choosing only those groups in the next trial.

### Original6: all remaining wrong answers are new individual regressions

|Original6 split|Control -> candidate correct|Rescued answers|New regressions|Wrong in both arms|
|---|---:|---:|---:|---:|
|TRAIN|2878 -> 2874 /2880|2|6|0|
|HOLDOUT|1385 -> 1434 /1440|55|6|0|

342003 newly loses six TRAIN answers (wrong_observed) and five HOLDOUT answers
(absent_digit), all English shared_suffix / entities[1,2], across both fact orders.
342001 newly loses one HOLDOUT answer (absent_digit), Japanese shared_suffix /
entities[0,2] / order[0,2]. Every remaining six-character error is new relative to
its paired control. A persistent failed criterion cell does not mean the same
answer remained wrong. All five candidate original6 local failures have only
normal-binding failures; their masked drops pass. Both-order failures number two.

## Interpretation and boundaries

The candidate has fitted normal binding failures in interior4 and transfer failures
in untrained original6. Unknown value combinations alone cannot explain the former.
The result is consistent with limitations in learning query-conditioned binding,
but does not identify pooling, gradients, capacity, parity, or another specific
internal cause. A masked criterion failing alongside normal binding is not an
independent causal shortcut diagnosis. C342 full-gate 2/5 remains unchanged.

Historical objective experiments matter: C268's pair-margin auxiliary was a valid
negative; C288's assignment auxiliary improved trained direct-gate count 3/5->5/5
but reduced four-character full-gate count 3/5->1/5. Adding an assignment term again
would not be a new mechanism. See accepted reports c268-c269 and c288-c289.

## Next one question: C344 pair-max reduction

At the same architecture, mixed45 token stream and 2400 updates, does replacing
ordinary mean per-query CE by the mean of each query pair's larger full256 CE
improve fitted and held-out interior4 binding while retaining every domain?

Fresh seeds344001..344005 / orders344101..344105; paired arms mean_ce and pair_max.
Use the same 48 rows / 24 complete pairs each update. If per-query losses are a,b,
control uses mean((a+b)/2), candidate mean(max(a,b)). Equivalently candidate is
ordinary mean CE + 0.5*mean(abs(a-b)); no margin, coefficient or temperature sweep.
Use symmetric torch.maximum tie gradients. Existing labels enter loss only; full
256 argmax/native_before inference and all masked evaluation remain unchanged.

This changes within-pair gradient weighting, including its effect under clipping.
It does not change family weighting or prove that the old objective caused failure.
The larger-loss query is not necessarily the currently wrong query. Non-smooth
switching and zero direct gradient to an easier partner can hurt other behavior.
No extra data, forward, parameters, updates or training of original6/HOLDOUT/masks.

Require all five candidates to pass all original2..6/interior4 gates. For EACH seed,
EACH domain and EACH split TRAIN/HOLDOUT, both normal answer and query-pair gains
must be nonnegative. Aggregate interior TRAIN/HOLDOUT answer/pair gains must all
be strictly positive (four endpoints). Ties and perfect-control saturation are
valid negatives; do not alter the cohort or gate. Publish all final TRAIN/HOLDOUT
support/collapse/counts and paired rescues/regressions, not just aggregate gains.

Finish source/tests/preregistration, independent committed-byte review, then a
separate documentation-only ACTIVE commit. C344 is not activated by this report.
