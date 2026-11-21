# C184 formal verdict — ACCEPTED PASS

V5-E; repository akakishi04/fold; branch feat/sft-target-loss.
Acceptance precedes any C185 registration. C185 NOT REGISTERED at this commit.
Gate E NOT PASSED. All historical judgments, especially C182 VALID NEGATIVE,
C183 local attribution PASS and C181 scoped PASS, remain unchanged.

## 1. Formal verdict

C184-v5e-canonical-fact-index-adapter / V5-E-CANONICAL-FACT-INDEX-ADAPTER:
**ACCEPTED PASS** against the unchanged registration. All normalization, inverse,
idempotence, preservation and frozen prediction conditions passed. No rerun required.
This is an explicit handwritten adapter contract, not new learned naming invariance.

## 2. Execution validity and evidence identity

Execution HEAD 4d07e9e5190487fdcc9cb68f7204381e5ea5ab67.
1249/1249 focused regression tests passed in 58.614s. Source/artifact precheck PASS.
Final protected_inputs preserved; tracked_tree clean; execution_HEAD preserved;
run_execution_valid=True. Existing C145 requires_grad scalar warning did not fail tests.

Summary: runs/c184-v5e-canonical-indices-5e2a159b64164b3a919762ebdbdc4f90/summary.json
Summary SHA256: 7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04
Canonical summary reconstructed from full uploaded log: 72652 bytes, exact SHA match.
Uploaded log: 284056 bytes; SHA256
990ed33e89fc66cdc539b09e3397392b22020514fc9cccba00cdaf2bd3931729.
Parent C183 summary ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24.
Original data eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.

Reviewer checked 24 normalization records / 96 mismatch counters, all138 ordered
model-permutation records, all12 identity replay records, exact workload arithmetic,
84 historical source-pin identities,172 protected-path hash formats, and five artifact
identities. All records agree with the fixed deciding gate; no inconsistencies found.
No confusion tables are present in this summary: per-group/count detail is in the
separate normalized-results.json and was NOT independently reaggregated by reviewer.
The five separate output artifacts, actual model checkpoints and data bytes were NOT
supplied for independent replay; all1249tests and1607688predictions were not rerun here.
Source inspection and summary arithmetic verification are not artifact-byte replay.
Local git network lookup failed DNS; do not describe it as a complete local checkout.

## 3. Metrics

24 normalization groups: identity51840rows plus23*9396renamed rows =267948.
Every canonical_mismatches,roundtrip_mismatches,idempotence_mismatches,
mutated_input_rows counter is zero. Normalizer rowcalls535896 including idempotence;
inverse reconstruction rowcalls267948.

Six frozen C181 checkpoints,source seeds181001/181002/181003,both FINAL_ONLY and
INTERNAL_SEMANTICS. Original replay311040predictions,all12sections decisions identical
and max_abs_logit_difference=0. All138 normalized model/permutation records complete:
1296648predictions; all decision_flips=0 and all max_abs_logit_difference=0.
Each INTERNAL_SEMANTICS model:216108/216108normalized decisions correct.
Candidate total648324/648324correct,errors0. All69candidate model/permutation cells perfect.
FINAL_ONLY retains2459/2429/2411errors per9396rows at EACH permutation; totals56557,
55867,55453 across23renamings. Its mistakes were preserved,not repaired or discarded.

Total model predictions1607688;1692forward batches/11844shared-cell calls;
checkpoint loads6. Fresh seeds,new training,teacher,auxiliary-head,acquisition,proof,
evidence-write,network calls all0. Production runtime modified=False;Gate E candidate=False.
Reported benchmark69.21285899999202s is not a production latency or speedup claim.
Five output artifacts exclude summary; hashes and sizes are retained in the summary.

## 4. Scientific interpretation

Arbitrary LOCAL reference numbering -> reversible first-occurrence normalization
-> unchanged visible-leaf preparation -> frozen learned C181 base -> original decision.

Within four distinct read-once facts/seven nodes, numeric references and complete fact
records can be normalized without information loss. The inverse map reconstructs input
numbering. The prior one-error unnormalized condition is absent from this new wrapped
pipeline, while the original C182 result stays archived as a valid negative.
Because normalized inputs are exactly original known inputs, matching outputs are
expected by construction. This confirms implementation and integration of this bounded
input contract,not independent semantic generalization or stronger network reasoning.

## 5. Confounds / remaining boundary

Canonicalizer is handwritten and uniformly applied,not a per-seed/per-case repair.
It has no answer,label,checkpoint or original-golden-input argument. It does not
execute logical operators,fill unknown values or alter external evidence identities.
The same4development semantic groups are reused; renamed copies/models are not
independent observations. TRAIN replay is resubstitution.

Still unmeasured here: full PolicyInput binding sidecar and external action mapping,
learned acquisition decisions driving the real lifecycle,learned target/tool selection,
answer/proof generation,larger or repeated-variable formulas,language or final Gate E.
Do not spend another C number merely rescoring saturated naming cases. Next work should
connect the learned necessity decision to a bounded real acquisition path,with explicit
handwritten target/transport responsibilities,or pose a genuinely new ability question.
This is a direction for subsequent design,not a registered experiment at acceptance.

## 6. Handoff

C184 ACCEPTED PASS; C185 NOT REGISTERED at this acceptance; Gate E NOT PASSED.
Retain all logs,summaries,checkpoints and artifacts. No historical source or condition
changes,no reset/rebase/history rewrite. Preserve authoritative environment and protected
C37/composition fixture. Multi-Axis/MA-1 and PC-ALM/FHLC remain separate research tracks.
