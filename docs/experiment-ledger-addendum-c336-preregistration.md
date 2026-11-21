# C336 preregistration -- saved query/fact-order response patterns

Date:2026-10-20 Japan time. Stage:V5-B-SAVED-QUERY-ORDER-PATTERNS.
Experiment:C336-v5b-saved-query-order-patterns.
Acceptance base:8984740dcc538cf785ca2fdc96db735b9ff8a4a1.
C335 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. No policy/production adoption.
Source publication is not activation:committed-byte review PASS must precede the
separate authoritative ACTIVE registration and user execution command.

## R2 schema correction -- 2026-10-21 Japan time

The initial unaccepted contract incorrectly described the inherited values as binary.
C267.dataset(), retained by C329/C335, uses two distinct integers from0..3, with
HOLDOUT pairs(0,2),(1,3),(2,0),(3,1); the other eight ordered pairs are TRAIN.
This amendment corrects that schema interpretation only. No saved data, predictions,
row inclusion, targets, categories, thresholds, workload or accepted result changes.
The original text is archived at docs/handoff-history/c336-pre-r2-preregistration.md.
See docs/c336-execution-recovery-r2.md. The scientific manifest describes two observed
values, not a0/1-only catalog; its serialized contents and SHA remain unchanged.

## One question and motivation

Which query/fact-order behavioral patterns account for C335's errors and paired
changes,including broad failure in BOTH arms of seed335002?
C335 original6 aggregate HOLDOUT gained2answers/9pairs,but short/interior preservation
failed and only1of5candidate models passed all gates. Seed335002's native comparator
also failed broadly. These observations do not establish a particular cause.
Before changing weights,training budget or readout again,inspect saved predictions
under two query identities and both fact orders. This is a behavior diagnosis,not a
causal account of optimizer failure,an internal circuit attribution or a new fit.

## Complete fixed cohort and unchanged observations

Use all10C335 final saved-output records,seeds335001..335005,arms native/alternating.
Both were evaluated with native_before. Keep original2..6 and interior4,all TRAIN/
HOLDOUT,en/ja,all3domain-specific profiles and all entity/value/order combinations.
Original profiles are repeat/shared_prefix/shared_suffix. Interior profiles retain
u_dominant/balanced/v_dominant;they are not renamed to opaque original scorer slots.
Original1 and all masked views remain in mandatory full parent semantic/replay
validation;the NEW response taxonomy concerns the18normal domain/profile sets only.
No state,seed,language or unsuccessful condition is excluded. No model inference,
optimization,new checkpoint,policy selector,ensemble or coefficient adjustment.

Input is the exact protected C335 evaluations.pt writer schema
fold-c335-evaluations-v1:ordered10records with seed,arm,state_sha256,evaluation_policy,
raw(evaluation/replay),and per-mode receipts. Require native_before,full114view
validation and unchanged accepted same_tree replay checks. The immediate C335
semantic reconstruction also verifies saved training traces,checkpoint fingerprints,
original scorers and fixed negative capability gate. Do not infer correctness merely
from a tensor shape or substitute a summary for the deciding saved predictions.

## Four-response unit and exclusive taxonomy

Group dataset rows by logical split,language,ordered entity pair and value assignment.
Validate each source target as48+the queried entity's value. Values are distinct
integers from0..3. Every group must contain exactly two queries under both fact permutations.
Keep row IDs and positions into saved tensors. Canonical response order is:
queryA/queryB under factsAB,then queryA/queryB under factsBA. No output-dependent order.

Compute ordinary argmax across ALL256saved logits;do not restrict output to the two targets,
repair a wrong class,choose an endpoint by target or use probability thresholds.
Let targets be(a,b),two distinct bytes from48..51. Exclusive categories are:
- query_correct:(a,b,a,b).
- query_swapped:(b,a,b,a).
- first_fact:(a,a,b,b),following the first fact's value after swapping fact order.
- last_fact:(b,b,a,a),following the last fact's value after swapping fact order.
- value_lock:all four responses equal ONE of the two observed values.
- other_class:any response lies outside those two values,including a constant third class.
- mixed:remaining patterns containing only the two observed values.

These categories partition groups,not individual answers. Also retain answer counts,
both-query-correct pairs,four-correct groups,collapsed query pairs,stable query answers
across fact orders,and out-of-value answers. Stability alone is not correctness.
A swapped but order-stable query pattern differs from a single-value lock. A perfect
four-response group differs from one correct pair. The seven labels describe observable
patterns;they do not establish where in the network the behavior originated.

## Paired changes and mandatory reconciliation

Align native/alternating quads by seed,domain,split,profile,language,entities and values.
Save before/after categories,per-answer correctness changes and per-order pair changes.
Retain rescues and regressions separately even where aggregate correct counts tie.
Reconstruct EVERY field of all30C335 HOLDOUT domain contrasts:denominators,correct/
both-correct counts,rescued/regressed answers and pairs,and both net gains. Exact
canonical JSON equality is required;gains alone or equal totals are insufficient.
Preserve the complete C335 validation_summary,including failed gate and eligible1/5.
No category count or localization changes an accepted capability verdict.

Report720strata:10states*6domains*2splits*3profiles*2languages. Each TRAIN stratum
contains24quads/96answers/48pairs;each HOLDOUT stratum12quads/48answers/24pairs.
Total12960quads/51840normal answers/25920query pairs;6480paired quad comparisons.
These are repeated logical tasks under controlled variants,not independent samples.
TRAIN labels refer to the original logical split;not every evaluated name variant
was necessarily presented by the training schedule. Do not call a TRAIN diagnostic
an exact training-exposure audit or infer memorization/generalization from that label alone.

## Work and success boundary

Scientific new train steps,model forwards,gradient calls,optimizer steps,model-state
loads,new checkpoint writes and network calls are all0. Parent validation loads saved
checkpoint tensors to verify fingerprints;it does not instantiate/load a model or
replay optimizer updates. Software fixture tensors and tests are separate work.
The saved diagnostic itself reads existing logits;no neural preflight is needed.

PASS means complete inventory,valid classification,exact parent-count reconciliation,
source/input protection and saved reconstruction. Every behavioral distribution is
an admissible outcome. capability_gate_applicable=false,gate_f_candidate=false,
production_adoption=false. C335 stays VALID NEGATIVE and no favorable seed selection.
Four JSON science outputs:audit-plan.json,query-order-quads.json,transitions.json,
validation-summary.json. All detailed classifications and transitions stay local and
hash-bound;the720stratum summaries and preserved parent gate are printed to console.
Fresh reconstruction recomputes all four outputs from the same protected raw logits.

## Immediate parent and full protection

C335execution:3b185a97ef86ab911d425620b4e6645fbd0c9f9e.
Publication:2587c5905e137728f22de06321c3e41943038945.
Folder:runs/c335-alternating-training-7dd29eebabd64360b31b40985bd6fd40/.
PrimarySHA6624fc176f349f7688af45da55ac5855951e7094c824201b16fe127b92aa25c4.
MandatoryenvelopeSHA70f5102a454db4370533f8da2f765d2e4eac6ab29d0bb93f5f4cbe976b9b5ab0.
Require fold-c335-trained-v1/fold-c335-execution-envelope-v1,scientificFAIL with
executionvalid and capabilityapplicable,exact manifest/work,negative candidate gate,
identical871source/3893input maps,6058full tests and3893final uncached rereads.
A valid negative parent is not a failed technical prerequisite.

Pin C335executor49e2a9c8103851ccfffaa283d4fd8943170fbaf3 before import. Its helpers
return(C334executor,C334helperdict). Reuse unchanged C335snapshot for ancestor maps,
then add ALL461parent outputs:6science+primary+envelope+453regression proofs
(3records+225moduleJSON/log pairs). Reconstruct parent6058IDs and every successful
ID/PID/log marker with the unchanged accepted helpers. No optional receipt shortcut.
Child protection877sources=871+6;4360inputs=3893+461+6. Preserve all accepted source,
tests,contracts,dispatchers and logs. All direct/lazy deciding modules are inherited
pins:C335/C332/C334/old evaluator/data/scorer/recovery chains. No new unpinned helper.

The C335helper bridge's c330 points to the C329data folder. Immediate reconstruction
calls C335.semantic_recheck(C335science,C329data,cx,read) under no_neural. This dispatch
is intentionally different from the C334crossover six-argument loader. Validate
canonical original/interior prompts and require all diagnostic source files in the
protected map. No recursive older semantic bodies,model inference or training.
Native unchangedR4leases cover parent,full regression,diagnosis and saved recheck.
Keep independent initial hashes and ALL4360final uncached rereads. Byte/size-bind
all4outputs before/after reconstruction and before primary/envelope writing.

## Regression, execution and stops

Preserve exact6058ordered IDs;baseSHA
0e87a5c604e102e837f606fcb5a731c80f1abee1381e63d20076f2e849f0c3be.
Append32own tests:6090selected/226modules,6091before the sole inherited exactC204
mutable-ACTIVE exclusion. No new exclusions,skips,cached success or retries.
C336owns guards/plan/CLI. Delegate ordinary module execution and evidence validation
to unchangedR1.2helpers. Keep direct/immediate-child PID relationships,canonical
begin/endmarkers,all successful IDs and fresh validation. Generic module ABI remains
fold-c330-r1-module-v2,bound to NEW C336HEAD/plan/index/module;child aggregate schemas
fold-c336-regression-plan-v1/fold-c336-regression-v1. All6090tests precede diagnosis.

New own six files:benchmark,executor,32tests,runner,launcher,this contract.
Primary/envelope schemas:fold-c336-diagnostic-v1/fold-c336-execution-envelope-v1.
Route:active_v2 ->invoke_c336 ->run_c336 ->controller/science ->locked acceptedC335
->full6090regression ->saved_query_order_patterns ->saved_diagnostic_reconstruction
->4360final rereads ->fresh verifier ->console publication. No training progress.
Local:runs/c336-query-order-<id>/science,regression proofs,worker logs and envelope.
ConsoleONLY published to docs/experiment-run-logs/c336/latest.log+latest.json.
Future successor must retain455new proofs(3+226*2)+6science/summary/envelope=461outputs.
Complete requires persisted_query_order_patternsPASS,execution_envelope_verified and
run_execution_valid=true. Parent candidate_gate=false is expected,not a diagnostic error.

After committing all six files,retrieve them through EOF and match Git blob identities
to local tested bytes. Rerun32tests,CP932-default-text-open emulation,UTF8/NUL/compile/
import/free-global audit and classification mutation controls. Distinguish real Torch/
Git/files/process checks from synthetic historical scorers/proofs/runtime/leases.
The full12960-quad synthetic fixture is NOT actual C335evidence or native6090tests.
Native PowerShell AST remains checked in the user dispatcher/launcher/runner path;
no author PowerShell execution is claimed unless actually performed.

Technical source/input/test/PID/nonfinite/coverage/parent-reconciliation/JSON failures
stay INVALID SAMEC336. Do not advance toC337 or weaken scientific scope. Publication-
only failure repairs publication alone. NoCI,paidservice,installation,artifact deletion,
accepted-source mutation,post-hoc cohort/policy selection or automatic rerun.

ManifestSHA256:e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
