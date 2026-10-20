# C335 acceptance and C336 authoring boundary

Date: 2026-10-20 Japan time.
C335 ACCEPTED VALID NEGATIVE. C334 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
Gate F NOT PASSED. No alternating/first_mean/production adoption.
C336 is not activated by this acceptance; separate preregistration and review required.

## Evidence and review scope

Execution:3b185a97ef86ab911d425620b4e6645fbd0c9f9e.
Publication:2587c5905e137728f22de06321c3e41943038945; sole parent equals execution.
Publisher reports222576original Windows bytes and log SHA256
 d5fdf5ef00c311898f729eeb4a1fb3a8cc04d91130edc4910f2978275853adb5.
Log Git blob:bb9210d41e5cfc833e3962d6b979b9371812e0b2.
Metadata blob:76cd7593a96ec8ee55c66a656b77981115e9528c.
Startup,registered manifest,full regression,all five paired comparisons,per-state
gates,saved reconstruction and terminal fresh verification were inspected at the
publication ref. Aggregate arithmetic was independently calculated from the printed
per-seed counts. This is a published-receipt review,not independent whole-Windows-log
rehashing,all local receipt-file inspection,raw-tensor recomputation or model replay.
Old C323/C324 attachments are unrelated to the current execution.

6058tests/225modules PASS;failures/errors/skips0;1465.259seconds including orchestration.
Ordered test-ID SHA0e87a5c604e102e837f606fcb5a731c80f1abee1381e63d20076f2e849f0c3be.
Native locks,parent semantics,871source/3893input registration,10paired trainings,
24000updates,27420forwards,native saved evaluation/replay,all3893final uncached
rereads and fresh verification completed. Science/verify exits0;run_execution_valid=true.
scientific_status=FAIL;candidate_gate=false;eligible_seed_count=1.

Local folder:runs/c335-alternating-training-7dd29eebabd64360b31b40985bd6fd40/.
PrimarySHA6624fc176f349f7688af45da55ac5855951e7094c824201b16fe127b92aa25c4.
EnvelopeSHA70f5102a454db4370533f8da2f765d2e4eac6ab29d0bb93f5f4cbe976b9b5ab0.
Manifest946639b00b62504f89faf0c5a8a0b14fba375da031f1b17b11436a61b1ec48b0.
Successor must inherit871sources/3893inputs and461parent outputs:
6science+summary+envelope+453regression proofs(3records+225JSON/log pairs).

## Deciding HOLDOUT arithmetic

Each domain1440answers/720query pairs across all five preregistered seeds.
These reuse logical tasks;they are not independent novel samples.

|Domain|Native answers|Alternating answers|Gain|Native pairs|Alternating pairs|Gain|
|---|---:|---:|---:|---:|---:|---:|
|original2|1313|1278|-35|608|583|-25|
|original3|1308|1280|-28|605|587|-18|
|original4|1301|1279|-22|601|587|-14|
|original5|1299|1273|-26|597|581|-16|
|original6|1279|1281|+2|580|589|+9|
|interior4|1257|1232|-25|567|559|-8|

Original6 per-seed answer gains:-2,-15,+1,+18,0;pair gains:-2,-8,+1,+18,0.
Strict aggregate6improvement passes,but per-pair preservation and all5candidate-full
requirements fail. Both arms have one full-pass model,seed335005. Eligibility1/5.
Do not reinterpret integral scientific FAIL as INVALID or authorize retraining.

Seed335002 is broadly unsuccessful in BOTH arms:original2answers161->126/288;
original6=148->133/288;interior=121->97/288 and pairs7->0/144. Its underlying cause is
unknown. Short-name regressions2/3/4are concentrated in that seed;do not discard it.
Seed335004 improves6by18answers/pairs but loses7answers/pairs on5 and1oninterior.
Seed335001 interior totals tie272/288 yet8answers are rescued and8regressed;
aggregate ties do not establish identical predictions. All these effects are retained.

## Interpretation and next bounded question

Equal-budget alternating TRAIN exposure with native-only evaluation is not supported
as a robust improvement by this cohort. Different old/new seeds prevent attributing
cross-experiment score shifts solely to policy. The weak native comparator in335002
is evidence of initialization/order sensitivity or other unresolved failure,not proof
of any particular optimization or representation mechanism.

Next investigate saved four-response patterns for every seed/arm/domain/language/
split/profile:two queried entities under both fact orders. Distinguish query-correct,
query-swapped,first-fact tracking,last-fact tracking,fixed observed value,other output
class and mixed responses. Preserve raw argmax outcomes and reconcile all C335 paired
HOLDOUT counts including rescued/regressed answers and pairs. No fitting,policy
selection,cohort exclusion or new model inference. This diagnoses behavior,not internal
causality. Source/tests/contract/review/activation must precede a C336 command.
