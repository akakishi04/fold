# C341 acceptance and C342 mixed-length retention trial

Date: 2026-11-02 Japan time.
C341 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
C340 remains ACCEPTED VALID NEGATIVE, candidate_gate=false / eligible_seed_count=2.
Gate F NOT PASSED. No production adoption. This acceptance does not activate C342.

## Execution identity and validity

Scientific execution a6a052912d52f786dd8c809ed6e8e96996c74edd.
Log publication 69ac5ae2e6fb4e268b3ef0453a83c3ad9cd1ecdb; sole parent is execution.
Only docs/experiment-run-logs/c341/latest.log and latest.json were added.
All seven source/test/launcher/preregistration blobs are unchanged from reviewed
source ba0ce613198c79131797da9e20ac9b561079769d through execution/publication.

Published metadata:425560 Windows bytes, SHA256
5fd76fc01880f02b3d3f48e09b4f2e5282b3d9bbc1291c6898187222e0f066c2.
Git LF:422456 bytes / 3104 lines, SHA256
5de4f0f134a509a9e5356f3ec14eef8776eb6e3db36ef0808fcffe0e762467ae.
Reconstructing CRLF matches both metadata byte count and hash exactly.

6314 tests / 233 modules PASS, zero failures/errors/skips, 2343.503 seconds.
All module begin/end records agree; indices0..232; all236 module/regression/science/
verify process exits are zero. Ordered test-ID SHA:
3ee31f196c842e57f786d5efe1c22df5460d41ddc92b86cf40d8c9f56209ac76.
Native lock probe PASS; explicit capacity6723; all6723 final uncached rereads.
Fresh verifier checked909sources/6723inputs/6314tests/233modules.
Parent C340 reconstruction completed with zero forwards/ancestor semantic reruns.
Saved diagnostic reconstruction complete; run_execution_valid=true.

Folder runs/c341-length-gate-localization-eff5826958774979923f8d9aa67a1abf/.
Primary ec30706ed3761c7b36c4ef215a85c53ccc79cbd1ffb271a5b387fe2049b406eb.
Envelope6cc5988f3126f0b51a2d5543755cf58471e8839354e3dcf6bc86b7ce1f30ac8e.
Manifest453b701fcf597a7ea8d38eb7b9457ee97693575f1349fa4903beebe5a1f6a647.
Successor retains909sources/6723inputs and ALL475C341outputs:four science files,
primary,envelope,469regression proofs(three records plus233module JSON/log pairs).

## Complete diagnostic inventory

144published strata cover4320local cells and2160both-order cells. All30criterion
transitions and all85failed local/31failed order rows are published. Independent
audit reconstructed all144stratum failure/pattern/criterion/failed-seed counts and
all30transitions from complete failure-coordinate sets. Coordinates,values,
denominators,fixed thresholds,deficits and arm-specific exposure agree. Parent
normal HOLDOUT answer/pair counts were independently reaggregated and also agree.

|Domain|Control local|Candidate local|Control order|Candidate order|
|---|---:|---:|---:|---:|
|original2|2|0|0|0|
|original3|0|0|0|0|
|original4|1|4|0|2|
|original5|8|0|2|0|
|original6|29|1|10|0|
|interior4|35|5|15|2|
|Total|75|10|27|4|

Counts include both splits and all seed/profile/language/entity/order coordinates;
they are not normal HOLDOUT answer counts. Candidate full-gate states remain
340001/340005 only(2/5);control0/5. Candidate failures are5normal_binding_only+
5mixed versus control38+37. ZERO mask_only failures occur in either arm:every
failed local cell also fails accuracy AND query-pair accuracy. Mixed failure does
not establish an independent shortcut cause.

## Candidate failure localization

All10candidate failed local cells use entities[1,2]. This observation does not
authorize selecting that pair,language,profile orseed for a new favorable cohort.

### 340002:interior4, five local and two order failures

Four local cells are balanced/Japanese/entities[1,2],both splits and fact orders:

|Split|Fact order|Accuracy|Query-pair accuracy|Evidence drop|Query drop|
|---|---|---:|---:|---:|---:|
|TRAIN|[1,2]|9/16=.5625|1/8=.125|.3125|.3125|
|TRAIN|[2,1]|10/16=.625|2/8=.25|.375|.375|
|HOLDOUT|[1,2]|6/8=.75|2/4=.50|.50|.50|
|HOLDOUT|[2,1]|5/8=.625|1/4=.25|.375|.375|

Both-order accuracy is.50TRAIN/.625HOLDOUT. The fifth local failure is
HOLDOUT/v_dominant/English/order[2,1]:accuracy7/8=.875,pairs3/4=.75,
evidence/query drops.625/.375pass. All5local and2order failures persist from control.
Interior4 was trained in both arms;the TRAIN normal prompts above were fitted.
Unseen-domain transfer cannot explain all of this failure. Internal optimization
mechanisms remain unproven.

### 340003:original4, four local and two order regressions

All are shared_suffix/Japanese/entities[1,2],both splits/orders. TRAIN accuracy is
.50/.5625 andpairs.00/.125;HOLDOUT accuracy.625/.50 andpairs.25/.00. Both-order
accuracy is.50in both splits. All4local failures are mixed:query-drop fails in all4
and evidence-drop in3. These criteria newly regressed;one unrelated original4
control accuracy cell was rescued. Original4 was absent from candidate fitting;
TRAIN denotes known values,not fitted original4 prompts. Prior HOLDOUT loss remains
seven answers/seven pairs.

### 340004:original6, one NEW regressed local cell

Exact coordinate:HOLDOUT/shared_suffix/English/entities[1,2]/order[2,1].
Accuracy7/8=.875fails.90;query-pair3/4=.75fails.80. Both masked drops are.625pass,
and no both-order cell fails. This is not a persistent control failure:ALL29control
original6 accuracy/query-pair failures were rescued;one different cell regressed.
All10control original6order failures were rescued. High pooled accuracy does not
justify changing the gate.

## Deciding transitions and unchanged parent metrics

|Domain/criterion|Rescued|Regressed|Persistent failures|
|---|---:|---:|---:|
|original4 accuracy/query-pair(each)|1|4|0|
|original4 evidence drop|0|3|0|
|original4 query drop|0|4|0|
|original4 both-order|0|2|0|
|original6 accuracy/query-pair(each)|29|1|0|
|original6 both-order|10|0|0|
|interior4 accuracy/query-pair(each)|30|0|5|
|interior4 both-order|13|0|2|

Individual answer/pair changes remain C340's result. Normal HOLDOUT original6 is
1396->1439/1440answers,681->719/720pairs;original4 1439->1433and719->713;interior4
1374->1434and662->714. C341 changed no model/prediction. Criterion rescues above
are not individual-answer rescues.

## Interpretation and audit boundary

Length5 exposure improved the fixed C340 cohort broadly but exchanged some failure
locations and removed original4 training coverage. Remaining problems include an
untrained original4 domain,a trained interior4 domain,and an unseen original6
HOLDOUT cell. Neither unseen length alone nor masked-control behavior alone is
supported as an explanation of all residual errors.

C341 establishes complete saved-result localization/integrity,not model improvement,
a causal mechanism,optimal curriculum,production readiness orGate F completion.
Five paired seeds,reused canonical templates/value split andC340nonpadding exposure
differences remain boundaries. Root and independent reviewer audited the complete
published evidence;local-only tensor/JSON artifacts were not fetched and rerun here.
Native reconstruction/fresh-verifier claims rely on the reviewed immutable executor
and its complete published completion evidence,independently cross-checked against
every published failure coordinate and pooled metric.

## Next bounded question

C342 will test whether restoring original4 exposure within a fixed original4/5
mixture improves original4 retention relative to original5-only fitting while
retaining original6 and every other domain. Use five fresh pairs,2400updates,
ordinaryCE/native readout and the whole canonical TRAIN population. Change only
actual token lengths at original-family slot4 presentations;original2/3,interior4,
logical events,query pairing,targets,family masks,rates/capacity remain fixed.
No profile/entity/seed targeting,threshold change or extra training budget.

Use accepted deterministic integral allocation on first-cycle original-family edges,
fixed4length per-pair/profile quotas8/8/9(repeat/prefix/suffix),then complement the
same choices in cycle2. Registered original-family quotas are16/17/17percycle.
Every row gets25length4+25length5percycle,50/50over the complete fit. Both actual
lengths occur within each slot4update while interior assignments stay unchanged.
Validate all five schedules before fitting;no output-dependent alternative allocator.
Measure actual nonpadding tokens and preserve paired input/logical fingerprints.

The contrast is original5 versus mixed45,not a fresh re-estimate of C340's original4
versus5 effect. Original5 exposure decreases when original4 is restored. Require
all5candidate full gates,EACHseed/EACHdomain nonnegative answerANDpair gains,and
strict aggregate original4 answerANDpair improvement. Saturated control ties are
valid negatives. This new C342 estimand never changes C340's judgment retrospectively.

Mixed exposure may not repair trained interior4 failure;its full gate stays mandatory.
Finish source/tests/preregistration,independent committed-byte review and separate
ACTIVE registration before a command. C343 waits for C342 judgment.
