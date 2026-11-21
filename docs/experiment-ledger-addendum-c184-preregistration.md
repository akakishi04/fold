# C184 preregistration — canonical LOCAL fact-index adapter

V5-E; akakishi04/fold; feat/sft-target-loss.
Registered AFTER C183 acceptance45a7f6b0df2cf5715f69aafe6cf1a706ee0a2e76.
C184 ACTIVE / NOT YET JUDGED. C185 NOT REGISTERED. Gate E NOT PASSED.
C183 remains ACCEPTED PASS; C182 VALID NEGATIVE and C181 PASS remain unchanged.

## One question / why this is an interface contract

Can an explicit, reversible first-occurrence normalization of LOCAL numeric fact IDs
remove arbitrary numbering from the frozen C181 input, while preserving original
predictions and every numeric reference-to-record association?

C183 localized its complete one-case failure to the frozen tree route. The direct
fact-table route partly opposed that error. Do not repeat bypass removal,retune one
checkpoint,or train the failed row. Address meaningless local index conventions at
the input boundary instead. This is an added HAND-WRITTEN adapter,not new learned
naming invariance or an independent scientific demonstration of broader reasoning.
No conditional special case for seed181003,row41788,permutation17 or any label.
The adapter is applied uniformly to all inputs and all six frozen source models.

## Changed variable / fixed substrate

C182 fed coherently renamed raw numeric fields directly into existing C178 preparation.
C184 inserts canonicalize(raw) BEFORE that same preparation and original frozen
C179TREE_LINKS inference. It returns a new numeric matrix and a zero-based map from
canonical fact slot to input fact slot. It never receives reference answers,source
canonical rows,labels,checkpoints or model predictions.

Traverse supplied postorder syntax,retaining its node order and connectivity. Rename
the first FACT encountered local1,the next local2,etc,and move the complete four-field
numeric fact record(active,status,present,value) together. Preserve operators,negation,
child indices,headers and runtime fields EXACTLY. Do not evaluate NOT,AND,OR,simplify
an expression,fill missing values,sort by observed values or merge distinct facts.
The inverse map reconstructs all original numeric references and records exactly.

Domain:four DISTINCT facts each referenced ONCE,seven connected postorder nodes,
FACT/AND/OR with leaf-only negation,OBSERVED/UNOBSERVED facts. Known0 is not unknown.
Reject unsupported repeated facts,statuses,hidden payloads and malformed syntax.
Do not generalize this bounded helper to correlated repeats or larger expressions.
Its resource/header fields are transported,not a replacement for full C170 validation.

LOCAL numeric IDs are arbitrary addresses,not semantic entity names. External evidence
IDs,scope,provenance and future acquisition targets must never silently be renamed.
This experiment operates on canonical72numeric fields only; it DOES NOT integrate a
complete C170PolicyInput binding sidecar or an action-result inverse-mapping runtime.
The returned map is saved to make that later integration explicit. No retrieval or
observation state is changed. No production runtime or old module is modified.

## Predictable invariance,not an unknown generalization result

Every original C174 row uses first-occurrence IDs1,2,3,4. For any consistent permutation
p,normalization N obeys N(rename_p(x))=x for such a source row. More generally,
N(rename_p(x))=N(x). The inverse map preserves information discarded from the MODEL's
address convention. Idempotence N(N(x))=N(x) is also required.

Therefore,IF adapter equality and frozen execution hold,predictions MUST match the
original known predictions. Zero errors here would be an engineering-contract result
for adapter+model,not the network independently learning a new invariance. We explicitly
expect preservation by construction;do not present an unsurprising PASS as new reasoning.
Original source references used by the TEST to check equality are NOT adapter inputs.
C182's unnormalized one-error result is not changed or overwritten.

## Data / frozen source / workload

Reuse all6C181checkpoints,source seeds181001/2/3,both FINAL_ONLY/INTERNAL_SEMANTICS.
Validate full25921parameter fingerprints,then use C182.restore_bare to construct only
original25726parameter base;no auxiliary head,teacher,training or new checkpoints.
Hash all earlier protected inputs and accepted C183summary/all6outputs.
No checkpoint selection,ensembling,threshold calibration or per-row fallback.

First check normalization on ALL51840original rows,including42444TRAIN rows and9396
PILOT rows. Replay all311040C181saved original main predictions. Require exact raw
argmax and logit absolute error<=1e-6(relative0),unchanged C182 replay tolerance. Replay
or source disagreement is INVALID,not an adapter performance failure.

For EACH23nonidentity fact renamings,normalize ALL9396pilotrows. Measure equality to
original numeric fields,inverse roundtrip,idempotence and preservation of source input.
Run all6models on every normalized batch,not just the historical failed case. Keep
batch1024 and same row order. ALL138model/permutation cells must finish,even on finite
contract failures. Save each raw logit,prediction and canonical-to-input map.
The source C182 raw-renaming outcomes remain archived;no need to reproduce all of them
again to establish this new deterministic input contract.

|Quantity|Registered|
|---|---:|
|Primary normalization checks,original+renamed rows|267948=51840+216108|
|Normalizer row calls including idempotence|535896|
|Inverse reconstruction row calls|267948|
|Original source replay predictions|311040|
|Normalized predictions,all six models|1296648|
|Normalized candidate predictions,three internal models|648324|
|Total main inference predictions|1607688|
|Inference batches/shared-cell calls|1692/11844|
|Source checkpoint loads/fresh seeds|6/0|
|Training/teacher/auxiliary/proof/acquisition/evidence/network|all0|

CPUfloat32,2threads,deterministic algorithms,original7cell applications per input.
Adapter integer work,validation,source hashing and serialization also cost time;
no speed,VRAM or equal-total-work claim. Normalized duplicate inputs are actually
forwarded;not counted as model evaluations after caching only one answer.
Same repeatedly reused4semantic development groups,not independent semantic holdout.
TRAIN identity replay is resubstitution,not new evaluation.

## Fixed deciding gate

ALL24normalization check groups must have zero canonical/roundtrip/idempotence/input
mutation mismatches. All138model/permutation cells must preserve original decisions
and have maximum absolute logit difference<=1e-6(relative0). All69INTERNAL_SEMANTICS
cells additionally require zero semantic errors. FINAL_ONLY retains its original errors;
those errors are not a condition to be perfect but no output changes are allowed.

Any finite miss of these measured contracts=>VALID NEGATIVE,preserve all outputs.
Do not relax tolerance/drop rows/choose a model/modify the normalization rule to force
PASS under C184. Malformed/nonfinite/source/hash/replay/incomplete/protection exceptions
=>INVALID EXECUTION,restore SAME C184 validity without changing scientific conditions.
PASS supports this bounded explicit normalization wrapper,NOT learned index invariance,
stronger semantics,more variables,repeat-variable reasoning or final Gate E.
No output correction based on labels and no counterfactual activation splicing.

## Sources / outputs / implementation validation

Inherit C183.precheck;add C183summary and6artifacts,then its4source files and4ownfiles.
84historicalsourcepins,172protectedinputpaths,plus outerC37/compositionfixture guards.
Parent summary ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24;
parent executionHEAD53bfa13bc74e74334a610605fc4fb63a4cc84702.
Manifest SHA256de54874ad495253c0111c006b9f40f6c85291fc67a8ad243ceb232c1b13e24ed.
Outputs:canonical-index-plan.json,canonicalization-audit.json,frozen-replay.json,
normalized-results.json,normalized-predictions.npz,summary.json. Fiveartifacts excluding
summary. NPZ order model6 xpermutation23 xrow9396,plus all inverse-slot maps.
Save pergroup/percount metrics and decision flips in details;no independent sample
claim from semantically overlapping permutations or repeated source models.

32/32new tests PASS on actual complete new module,without substituted old model code.
Tests target the self-contained numeric adapter and fixed gate,NOT complete run().
Independent enumeration checks9720synthetic renamed rows(5shapes x81visible assignments
x24permutations);also inverse/idempotence,whole records,unknown/0 distinction,invalid
inputs,label-free interface,batch maps,finite mismatch accounting,strict gate/manifest.
No official checkpoint or deciding normalization/model result was executed locally.
Full1249regression,WindowsPowerShell,172input artifactchain and formal1607688predictions
remain UNEXECUTED. Git clone failed DNS;no complete checkout available to reviewer.
New Pythonfiles compile;three embedded PowerShell Python blocks parse;not PSexecution.

1249expected=1217+32;68modules. One regression then one frozen adapter batch.
Run tools/run_c184.ps1 withC183/C182/C181/C180/C179/C178/C177/C176/C174summaries/ExpectedHead.
Judge C184 ->ledger/handoff->next design;C185 NOT REGISTERED until judgment.
After this contract,do not add more unchanged-score diagnostics merely to revisit the
same saturated naming cases. Further ability/real action integration needs a new question.
