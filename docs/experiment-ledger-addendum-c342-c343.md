# C342 acceptance and C343 complete saved-cohort diagnosis

Date: 2026-11-02 Japan time.
**C342 ACCEPTED VALID NEGATIVE.** Execution is valid; the fixed mixed45 candidate
gate did not pass. Gate F remains NOT PASSED. No production adoption. This
acceptance commit does not activate C343.

## Execution identity and validity

Scientific execution: e379de3ff300dd01381eeb90055c017c87ead670.
Published log commit: 1f8a890f5a08fe2e43fdfe847b06f936b9cb6472, sole parent execution.
Only c342/latest.log and latest.json were added. All seven reviewed source/test/
launcher/preregistration files are unchanged from source HEAD
eb9ddb8388df4e2321b6b2e88769a827dd6cd09b through publication.

Published metadata: 280032 Windows bytes, SHA256
b28a1f7ff3a97d9c496cfcd1708ef66cd2a2781e0112bab7492243c4c4b795a5.
Git LF: 276634 bytes / 3398 lines, SHA256
e62d875b42fc3315b948ed1b9818ba580c612fcd9ebcc1c63790e0392f7a5c10.
CRLF reconstruction matches both published byte count and hash exactly.

6378 tests / 235 modules PASS in 3131.060 seconds, failures/errors/skips all zero.
All 235 module begin/end records match, indices0..234, and sum to6378 tests.
All238 module/regression/science/verify process exits are zero. Ordered test-ID SHA:
76dfa4fd2952bdffd80250e57880d58cda72e7f7c16402c1817fed39ff294460.
Native lock probe PASS, max_files7205. Registration/fresh verification agree on
916sources/7205inputs. All7205 final uncached rereads completed. Immediate parent
semantics, native preflight, evaluation replay and saved training reconstruction
completed. run_execution_valid=true.

Independent result review re-fetched exact remote metadata/log bytes and verified
their Git blobs, every module test footer, all ten fit/evaluation completion records,
all five paired comparisons, ten state summaries and fixed-gate arithmetic. Local
user checkpoints and all7205 input files were not transferred to this authoring
environment; native artifact integrity relies on the immutable executor and the
published fresh-verifier completion evidence, not a claimed second native rerun.

Folder: runs/c342-mixed-length45-cceefd2e5093444483eb61f6f883e058/.
Primary47862c134f7f3be25784a88694e0bc1e29041772c025006c256673dc83695775.
Envelope6d8e1ac497fd28f0c6e58fa2770526619fc0bbc47de158ab3803bcbc7559481a.
Manifest538150bd2b43ff286e4d5b0e0c1d665ea1e1c4d43cf8148cba1c5d1a4192734c.
Successor retains all481 outputs: six science files, primary, envelope, and473
regression proofs (three records plus235 module JSON/log pairs).

## Fixed gate and deciding metrics

Candidate full-gate/eligible seeds:342002 and342004, **2/5**.
Control full-gate seeds:342003 and342004, also2/5.
The gate required all five candidates to pass every original2..6/interior4 gate,
nonnegative HOLDOUT answer AND query-pair gains for EACH seed/EACH domain, and
strictly positive aggregate original4 gains for BOTH measures. Strict original4
gains pass; the first two requirements fail. candidate_gate=false.

Each domain below has1440 normal HOLDOUT answers and720 two-query pairs across
five seeds. A pair counts only when both queries are correct. Aggregate totals
cannot replace the per-seed/per-domain gate.

|Domain|Control correct|Mixed45 correct|Answer gain|Control both correct|Mixed45 both correct|Pair gain|
|---|---:|---:|---:|---:|---:|---:|
|original2|1393|1440|+47|676|720|+44|
|original3|1396|1440|+44|678|720|+42|
|original4|1390|1440|+50|672|720|+48|
|original5|1387|1440|+53|670|720|+50|
|original6|1385|1434|+49|668|715|+47|
|interior4|1295|1366|+71|591|654|+63|

|Seed|Control full gate|Mixed45 full gate|Deciding observation|
|---|---|---|---|
|342001|FAIL|FAIL|original4 +50 answers/+48 pairs; original6 and interior4 still fail|
|342002|FAIL|PASS|interior4 +1 answer/+1 pair; original domains tie at perfection|
|342003|PASS|FAIL|original6 -5 answers/-4 pairs violates per-domain retention|
|342004|PASS|PASS|All normal HOLDOUT domains tie at perfection|
|342005|FAIL|FAIL|interior4 +1 answer/0 pairs; its full gate still fails|

## Scientific interpretation

All original4 improvement comes from342001. Its original2/3/5/6 answer gains are
also+47/+44/+53/+54. The other four original4 controls/candidates are perfect on
normal HOLDOUT. The intervention improves this paired cohort, but does not isolate
an original4-specific mechanism or show uniform benefit across initializations.
Initialization and schedule vary together across seeds; their causal effects have
not been separated.

Candidate original6 has six wrong normal HOLDOUT answers, all absent_digit:
one in342001 and five in342003. The former is a new individual-answer regression
despite positive net six gain. Across seeds, original6 rescues55/regresses6 answers
and rescues52/regresses5 query pairs.

Candidate interior4 has74 wrong answers:58wrong_observed+16absent_digit.
Seed342001 has58errors(42+16);342005 has16wrong_observed errors.
Interior rescues101/regresses30 answers(26regressions in342001,four in342005),
for net+71. Query pairs rescue63/regress0. These are different units; do not
interchange individual-answer, query-pair, gate-cell or both-order transitions.

Gate-cell totals include both splits and every fixed coordinate:

|Domain|Control local|Mixed45 local|Control both-order|Mixed45 both-order|
|---|---:|---:|---:|---:|
|original2|32|0|18|0|
|original3|31|0|18|0|
|original4|31|0|18|0|
|original5|30|0|17|0|
|original6|30|5|17|2|
|interior4|69|33|34|17|
|Total|223|38|122|19|

Mixed45 achieves perfect original2..5 normal HOLDOUT accuracy and complete gates
in all five candidates. Interior4 still fails in two seeds and original6 in two,
with342001 shared. Current summaries do not identify each failed coordinate or
whether residual interior errors include normal TRAIN prompts actually fitted.
Do not infer C342 localization from C341's different weights/seeds.

## Confounds and nonclaims

The results are compatible with sensitivity to training trajectories and coverage;
they do not prove a representation, parity shortcut, attention collision, capacity
limit or optimizer mechanism. Original5 and mixed45 both use2400updates/48rows,
but nonpadding tokens/model are3225600 versus3168000. Equal updates/rows are not
equal tokens or measured FLOPs. Restoring length4 reduces length5 exposure; the
fixed allocation/timing is part of the intervention. No optimal-ratio, general
language, or Gate F claim follows. C340 and C342 are different fresh cohorts and
are not paired estimates of the same contrast.

## Next one-question boundary: C343

Diagnose the complete saved C342 cohort: where do improvements, regressions and
remaining gate failures occur relative to actual TRAIN exposure, held-out value
combinations, name domains, binding/masked dependence and both-order conditions?

Use every saved seed/arm/domain/split/profile/language/entity/fact-order coordinate.
Reconcile unchanged parent gates, normal answer/pair totals and raw prediction
transitions. Correct exposure is original5 sees2/3/5/interior4; mixed45 sees
2/3/4/5/interior4. Original6/HOLDOUT logical rows/masked prompts are never fitted.
Record exposure counts with their unit; canonical-row counts across profiles are
not literal-prompt repetitions. Analyze successes and failures without selecting
a favorable cohort.

No new fit, forward, optimizer, model-state load, prompt intervention, output
filter, checkpoint selection or gate change. Diagnostic integrity PASS establishes
complete consistent accounting, not capability improvement; C342 stays negative.
Complete source/tests/preregistration and independent committed-remote-byte review
before a separate documentation-only C343 activation and launcher.
