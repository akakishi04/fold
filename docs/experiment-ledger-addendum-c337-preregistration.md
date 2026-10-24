# C337 preregistration -- saved value-support and within-pair ranking

Date: 2026-10-24 Japan time.
Experiment: C337-v5b-saved-value-support. Stage: V5-B-SAVED-VALUE-SUPPORT.
Acceptance base: 5f7e434ca76132057036155c7467a15caee91b6c.
C336 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C335 remains VALID NEGATIVE.
Gate F NOT PASSED. No policy adoption. Source publication is not activation:
committed-byte post-authoring review must PASS before the registered user command.

## One question

When a saved answer is wrong, does its score rank a value outside the supplied pair
above both supplied values, or also fail to distinguish the two supplied values?
C336 found substantial outside-pair responses in both arms of seed335002. Its
other_class category intentionally does not distinguish an absent catalog value
from a byte outside the catalog, or describe the ranking below the raw winner.
C337 measures these distinctions before another training intervention. It does not
claim that this decomposition identifies the internal cause or a deployable repair.

## Fixed data and outputs

Retain every one of the ten C335 saved states:335001..335005, native/alternating,
all original2..6/interior4, TRAIN/HOLDOUT, en/ja and three domain-specific profiles.
No failed-seed removal, favorable-profile selection, weight update, new inference,
checkpoint selection, threshold change, policy selector or ensemble.
The canonical dataset has192TRAIN/96HOLDOUT rows. Its frozen SHA256 is
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
It uses two distinct values from0..3. HOLDOUT pairs are(0,2),(1,3),(2,0),(3,1).
Targets are48+queried value; entity identities, order, IDs and saved tensor row
positions remain unchanged. Do not repeat C336's initial binary-only assumption.

Read unchanged fold-c335-evaluations-v1 with ordered10records, native_before policy,
all evaluation/replay outputs and receipts. Mandatory immediate C336 semantic
reconstruction validates the complete114-view parent tree and replay through its
accepted R2 implementation before the child audit. The new audit uses only the
18normal domain/profile sets, not masked views or original1. Those excluded-from-
taxonomy views remain part of parent validation; they are not silently unprotected.

## Per-answer decomposition, without repairing predictions

Keep ordinary first-index torch.argmax over ALL256classes as the actual prediction.
For each answer, use the source target and the other supplied value only for offline
scoring. Four mutually exclusive classes:
- correct: raw prediction equals the queried value.
- wrong_observed: equals the other value present in the same problem.
- absent_digit: a catalog digit0..3 that is absent from this problem's pair.
- outside_catalog: any other byte. This includes digits4..9 as well as nondigits;
  it must NOT be presented as synonymous with a nondigit or malformed text.

Measure two float64 logit differences without changing the original tensor:
1. pair_margin = target_logit - other_supplied_logit.
2. support_margin = max(two supplied logits) - max(254 outside logits).

Record positive/zero/negative signs explicitly. Exact ties remain ties; there is no
chosen epsilon, tie-breaking repair, softmax cutoff or posthoc decision threshold.
The support calculation excludes two entries in a CLONE for measurement only; raw
argmax is computed from the original256-class tensor and stays unchanged. Reject
nonfinite source logits or derived margins rather than silently clipping them.
Each stratum includes the4x3 error-class/within-pair-rank joint counts, three support
rank counts, and means of both margins. Means are descriptive, not capability gates.

An outside winner with positive pair_margin means only that the correct supplied
value outranks its supplied alternative below that winner. It is NOT a corrected
model answer or a demonstrated gain. The label-assisted comparison is an offline
diagnostic, not a candidate filter implemented in the model or an end-to-end metric.
No answer is replaced. Ground-truth identities never enter inference because no
new model is run. No claim of causal mechanism, generalization or Gate F passage.

## Exact parent reconciliation

Reconstruct each of the12960 C336 four-response records from the same raw logits,
including source row IDs, canonical query/order orientation, targets, predictions,
all seven categories and every answer/pair/order count. Require exact canonical JSON
equality against query-order-quads.json. Reconstruct all720parent strata, not only
correct totals. Require correct=parent correct and absent_digit+outside_catalog=
parent other_answers in every stratum. No denominator changes or aggregate-only
substitute for per-quad binding. Immediate parent semantics also preserve all30C335
HOLDOUT contrasts, including rescued/regressed answers/pairs, and the negative gate.

Diagnostic output:51840per-answer records,12960source-quad reconciliations and720
strata. TRAIN strata have96answers each, HOLDOUT48. These are repeated controlled
variants, not51840independent tasks. TRAIN is the logical split, not an exact
exposure audit. Keep C335candidate_gate=false and eligible_seed_count=1.
Scientific train/forward/gradient/optimizer/state-load/checkpoint/network work0.
Tensor archive reads and software tests are separate work, not new model inference.

## Parent contract and all protected inputs

Accepted C336execution:274048a72eea1cbb53ece4ec57708e7de2603e6f.
Publication:9eb7f834b8470c89cef7cb65618864ca7fa8d23d.
Folder:runs/c336-query-order-79c949c728c44366a8f62a6e5b2304a2/.
Primary31ed3d3e9d45f079bbf4bc200e3a7b5aa82b197cc3f0ded176c01db2b6046b98.
Envelope39f2afcdf7107d7e070977e7b4e834694ee77bb68d00cf30a46be15c5c519dcb.
Require fold-c336-diagnostic-v1/fold-c336-execution-envelope-v1, diagnostic PASS,
capability not applicable, preserved negative C335, exact manifest/work, both877/
4360maps,6090full tests, all4360final uncached rereads and all completion flags.
Pin C336executor2d35c49a0adf570458c7232cf44e373e7e2e54c4 AND R2benchmark
d1862be34e673ee6da433be711bcf2b8b70645e7 before importing the helper chain.
Its helpers return a dict with parent/prior/recovery/c330/runtime/legacy/locks.
The new parent bridge preserves that dictionary, not the older C335 tuple assumption.

Reconstruct the complete inherited map with unchanged C336.snapshot. Add ALL461
parent outputs:4scientific outputs+primary+envelope+455regression proofs(3+226*2).
Validate hashes, exact6090ordered IDs, all module test success/PID/log evidence with
the unchanged accepted module validator. No optional proof or stale-receipt shortcut.
Child protection:883sources=877+6;4827inputs=4360+461+6. Exact finite native capacity
max_files=INPUT_COUNT=4827; no eviction, unlocked fallback or inherited4096default.
Hold read leases through parent/child work; keep independent initial hashes and ALL
4827final uncached rereads. No source omission, accepted-file edit or data deletion.

Immediate semantic dispatch is C336.semantic_recheck(C336science,C335science,C329data,
C336validation_summary.parent_validation_summary,cx,read), not C335's four-argument
loader. Use the unchanged C332/C329/C324 context and canonical data/prompt validators
under no_neural. No older recursive semantic-body calls or historical optimizer replay.
All directly/lazily used repository modules already belong to inherited pins; new
scientific dependencies are only the six child files. Source/input bytes are checked
again by an independent fresh verifier. The C335archive and C329data remain inherited
protected files; C336quad outputs are mandatory newly added protected inputs.

## Full regression and execution

Preserve all6090ordered parent IDs, SHA
469a8865f79307ef97c8dba2eac3d87d522f75f80fb7c16e34c64510a9ee5132.
Append32own IDs:6122selected tests/227modules,6123before the sole inherited exact
C204mutable-ACTIVE exclusion. No other omission, skip, cached success or automatic retry.
Child owns its guard/plan/CLI. Delegate module execution and proof validation to
unchanged C330R1.2 helpers; retain direct/immediate-child PID relationships and exact
begin/endmarkers. Generic module ABI fold-c330-r1-module-v2 binds the NEW C337HEAD/
plan/index/module. New aggregate schemas fold-c337-regression-plan-v1 and
fold-c337-regression-v1. Full6122success precedes science.

Six own files:benchmark,executor,32tests,runner,launcher,this contract.
Four scientific JSON outputs:audit-plan.json,answer-support.json,
source-reconciliation.json,validation-summary.json. Summary/envelope schemas
fold-c337-diagnostic-v1/fold-c337-execution-envelope-v1 carry full883/4827maps,
fixed manifest and workload, protected parent identity and full regression proof.
All4outputs are byte/size-bound around reconstruction and before summary/envelope.
Fresh verifier repeats parent/proof/child reconstruction without a model run.

Route:active_v2 ->invoke_c337 ->run_c337 ->c337_execution controller/science
->native locks/complete parent snapshot ->C336semantic reconstruction ->6122isolated
module tests ->saved_value_support ->saved_diagnostic_reconstruction ->4827final
uncached rereads ->independent fresh verifier ->console publication.
Local:runs/c337-value-support-<id>/science plus227moduleJSON/logpairs and regression
plan/evidence/result. Only console is published to c337/latest.log+latest.json.
Print720strata and preserved parent gate. Future successor must retain457new
regression proofs plus6science/summary/envelope=463parent outputs.

## Author review and stopping boundary

Reread all six committed files through EOF and compare Git blobs to locally tested
bytes. Run own32tests normally and under CP932-default-text-open emulation, check
compile/import/UTF8/NUL/free globals/manifest/counts and negative controls that
reintroduce output filtering or mislabel absent values. Test actual production
analysis/writer/snapshot/worker/fresh-verifier paths, keeping synthetic collaborators
explicit. The author tree contains verbatim EXTRACTS of accepted C336 pure helpers
and C267canonical dataset writer, not complete historical modules or Windows evidence;
these local-only extracts are never committed. Native tests import actual accepted
full modules. Do not claim full6122historical/native execution or real C335raw-logit
results from author fixtures. Mandatory PowerShell AST checks remain in dispatcher/
selected launcher/runner; no author pwsh execution unless actually available.

PASS is diagnostic integrity only, irrespective of unfavorable distributions.
No C338or training intervention is authorized by this registration. Technical source/
input/PID/test/nonfinite/row/quad/stratum/JSON mismatches remain INVALID SAMEC337.
Do not retry a valid unfavorable result or bypass publicationHEAD safeguards.
Publication-only failure repairs publication alone. No CI, paidservice, reinstall,
accepted-model retraining, source mutation or artifact deletion.

Manifest SHA256:4233762c9dd30360f0173e22e1db6ec697c1d7cafd479fc3ce6c3bad0ca81d26.
