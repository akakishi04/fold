# C334 preregistration -- frozen training/inference policy crossover

Date:2026-10-20 Japan time. Stage:V5-B-FROZEN-POLICY-CROSSOVER.
Experiment:C334-v5b-frozen-policy-crossover.
Acceptance base:0b63bcc7f7efe1045f2bfb6644e6b4426e20b19b.
C333 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY),C332 VALID NEGATIVE.
Gate F NOT PASSED;no first_mean adoption or C335 registration. Separate committed-byte
review and authoritative ACTIVE registration must precede an execution command.

## One question

At all ten fixed C332 checkpoints,how does the effect of the inference readout
interact with the readout used to train those weights? C333 localized rescued and
newly failed conditions,but cannot separate an immediate inference change from
adaptation of weights to the training policy. This is a full2x2 crossover,not a
selected-seed retry,a new coefficient search,or another trained capability claim.

For each of seeds332001..332005 retain BOTH native-trained and first_mean-trained
states. Freeze weights and run own_before,cross,own_after in that order:
- native-trained: native ->first_mean ->native;
- first_mean-trained: first_mean ->native ->first_mean.
All four training-policy by inference-policy cells are retained. No best-policy
selection per example,language,template or seed. No retraining/fine-tuning or updates.
C331 used older native C329 states;it did not run this complete C332 crossover.

## Exact changed variable and controls

Reuse the accepted C332 factory/load_states/policy_mode and C331 readout/measure,
without modifying any accepted source/global/function. Native mean/last versus
.5*(mean+first-query-byte-local)/last. The last-byte branch,projection weights,two
attention calls,core,residual path,coefficient.5,input parser and targets remain fixed.
The first position is a UTF8 BYTE,not the end of a complete Japanese character.
Each saved state is loaded once into an independent native C332 model. All three
modes use eval/no_grad and must preserve the full state hash after every evaluation.

Load the actual C332 fold-c332-trained-models-v1 bundle and fold-c332-evaluations-v1
archive,not C329's trajectory schema. The latter has schema/records and each record
has seed,arm,state_sha256,readout_mode,raw(evaluation/replay),receipts. Validate all
identities,policies,hashes and exact actual171forward/16416row/342query/0grad receipts.

Own_before must reproduce BOTH C332 evaluation and replay. Own_after must reproduce
own_before. Every one of114raw view tensors must be CPUfloat64,finite,shape-identical,
within1e-9maximum absolute logit drift AND exact argmax. Do not replace the argmax
control by tolerance alone. All38query-blind tensors and English original1 views
must also remain invariant under the same-weight swap. This is NOT a requirement
that differently trained models have identical query-blind predictions. Japanese
original1 is not mislabeled a one-byte invariant. No post-hoc tolerance adjustment.

All original1..6/interior4,TRAIN/HOLDOUT,en/ja,profiles,entity sets,fact orders and
views are evaluated. Original1 is descriptive/control-only as before. Score own and
cross with unchanged accepted scorers. Keep .90/.80/.35/.35/.80 local/mask/order
thresholds. Original5/6 name families were not in C332 fitting even on logical TRAIN.
The native-matching diagonal must reproduce every C332 gate/failure map and complete
paired HOLDOUT contrast,including individual-answer and question-pair rescues and
regressions. A aggregate gate-cell transition is not an individual-answer transition.

## Factorial accounting and meaning of results

For each seed/domain preserve four answer counts and four both-query-correct counts:
NN=native-trained/native inference;NF=native-trained/first_mean inference;
FN=first_mean-trained/native inference;FF=first_mean-trained/first_mean inference.
Inference effect on native weights=NF-NN;on first_mean weights=FF-FN;
interaction=(FF-FN)-(NF-NN). The same formula applies to query-pair counts.
Do not confuse the first_mean-trained own->cross comparison(FN-FF) with FF-FN.
The diagonal NN/FF is bound to the already accepted C332 contrasts. Save all30
seed/domain factorial rows and all10state-specific swap contrasts with signs intact.
Complete local scorer records stay in measurements.json;all three raw modes are saved.

Within a frozen state,this is a controlled inference intervention. Across training
arms,interpretation is restricted to the paired C332 training protocol and these
states. It is not an identification of internal causal mechanisms or a mediation
decomposition. Benefits,ties,harms and interaction signs are all admissible outcomes.
PASS means complete valid replay,unchanged weights/inputs and reproducible analysis,
not that either off-diagonal policy is better. No capability gate is tuned to the
observed results. C332 candidate_gate=false remains false. No Gate F or adoption.
No per-example selector,trained hybrid,independent-sample or efficiency claim.

## Work and native preflight

10frozen models,10model-state loads,1checkpoint-bundle load. Thirty full evaluations:
5130model forwards,492480row presentations,20520core forwards,10260query projections.
20scored state/policy records. Scientific training/gradient/optimizer steps,new
checkpoint writes and network calls0. Raw-logit payload1008599040bytes is not total
serialization size or peak RAM. Parent reconstruction,tests and fresh saved analysis
are separately scoped work,not free computation or another model cohort.

Native preflight uses one discarded C332-factory model with a deterministic nonzero
read.output weight. Four English original1/6 normal/query-blind prompts each receive
one unhooked baseline and both three-mode sequences:28forwards/28rows/0updates.
It checks native parity,single-byte controls,own-policy restoration,finite logits,
query receipts and weight preservation. No preflight state enters the cohort.
Native work follows the registered Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5 runtime,
CPUfloat64,2threads,14256parameters/core3328,64slots. No environment installation.

## Immediate C333 parent and full inherited protection

Execution4545da60d8e54bb3a46f090259644c44eacdab1b.
Publication98bff288caed1a0ffe8aff9198c4fa85000d5987.
Folder:runs/c333-paired-localization-9035c7fd110c4509b60caa635a0957d4/.
Primary science/summary.json SHA256:
abfda3d87ecc44c66cf4509382ced20ffe8fdc8452e36298a777e6b891f1c19b.
Mandatory execution-envelope.json SHA256:
7b3cef93cba77cba008a48bc4466e5f7c1fc3523f0a57ef6de3867550ce7d479.
Require fold-c333-diagnostic-v1/fold-c333-execution-envelope-v1,PASS,diagnostic valid,
capability not applicable,exact manifests/work,identical859source/2969input maps,
5978test success and all2969final uncached rereads. Retain the negative C332 summary.

Use unchanged C333 snapshot to reconstruct older source/input/proof maps. Add ALL455
parent output files:4science+primary+envelope+3regression records+223module JSON/log
pairs. The449test-proof files are mandatory;reconstruct exact5978IDs and validate
all success/exit/PID/log-marker semantics with accepted helpers. No receipt-only
or smaller-map shortcut. Source865=859+6;inputs3430=2969+455+6.

Pin C333 executor efd6a3d82ba1495242558a98cbe688437065ae10 before importing its helper
chain. C333.helpers returns(C332,(C331,(R1.2,C330,runtime,legacy,locks))). The child
maps this nesting to named fields rather than reusing an obsolete tuple index.
Immediate scientific reconstruction calls C333.semantic_recheck(C333science,
C332science,read) under no_neural. Do not call an old five-argument C331 loader.
Older scientific semantic bodies are not rerun;older bytes/proofs stay protected.
Validate canonical C329 prompts/data and ensure every C332 tensor/data dependency
used by the crossover already belongs to the inherited protected input map.
Native R4 leases span the worker;independent initial hashes and ALL3430final uncached
rereads remain required. No accepted source mutation or unlocked fallback.

## Regression, files and execution route

Preserve all5978ordered test IDs,base digest:
3f785186b97135ede6fec9be56c4ac24e439a19e44f6137a82a4c0d29345675b.
Append32own tests:6010selected/224modules,6011before the sole inherited exact C204
mutable-ACTIVE exclusion. No new exclusions/skips/cached success or auto retry.
Sequential fresh interpreter per module;retain both tests_lm and exact registered
tests_tools modules. C334 owns its guard/plan/CLI;unchanged R1.2 executes tests and
validates generic fold-c330-r1-module-v2 records bound to NEW C334HEAD/plan/index.
Keep direct/immediate-child PID topology and canonical begin/complete log markers.
C334 plan/evidence schemas:fold-c334-regression-plan-v1/fold-c334-regression-v1.

Own six files:benchmark,executor,32-test module,run_c334,invoke_c334,this contract.
Four outputs:diagnostic-plan.json,evaluations.pt,measurements.json,validation-summary.json.
Archivefold-c334-crossover-v1 holds all10states and own_before/cross/own_after modes.
Primary/envelopefold-c334-diagnostic-v1/fold-c334-execution-envelope-v1 bind complete
865/3430maps and the complete new regression evidence. Byte/size-bind all outputs
around saved reconstruction and before writing summary/envelope. A fresh verifier
reconstructs parent/test proofs and child tensor/JSON metrics without new model
forwards or replaying historical optimizer steps. Successors must preserve451new
test proofs(3+224*2) plus6science/primary/envelope files=457parent output files.

Route:active_v2 ->invoke_c334 ->run_c334 ->c334_execution controller/worker ->locked
parent proofs/JSON ->native crossover preflight ->6010isolated tests ->30frozen
evaluations ->saved reconstruction ->3430final rereads ->fresh verifier ->console push.
Local:runs/c334-policy-crossover-<id>/science plus enclosing regression-plan/evidence/
result.json,224module JSON/log pairs,execution envelope and worker logs. Publish only
console to docs/experiment-run-logs/c334/latest.log/latest.json. Ten state-completion
markers then all10crossovers and30factorial rows print. No training-step progress.
Complete requires persisted_policy_crossover=PASS,execution_envelope_verified and
run_execution_valid=true. Harm alone is not an execution error or permission to retry.

## Author review and stops

After source/tests/runner/launcher/contract commit,reread every file through EOF and
compare Git blob identities with independently hashed tested local bytes. Rerun32
own tests,CP932-default-open emulation,UTF8/NUL/compile/import and recursive global
binding audit. Tests use real Torch tensors/state loading/archives,JSON/Git/subprocess
and child production orchestration with explicitly synthetic legacy scorers,parent
checkpoints,proofs/runtime/lease callbacks where replaced. They are not actual FOLD
checkpoint inference,native Windows6010tests or a separate native fresh verifier.
Retain mandatory user-side dispatcher/selected-launcher/runner PowerShell AST checks.
Do not claim native PowerShell execution when the author host lacks PowerShell.

Any source/input/test/PID/identity/nonfinite/control/weight/replay/schema/reconstruction
failure remains INVALID SAME C334;no C335. Preserve each attempt;no automatic retry.
Publication-only failures repair publication without model reruns. Wrong/stale/dirty/
ambiguousACTIVE/dependency/AST conditions skip before science/log publication. Never
bypass RESULT_ALREADY_PUBLISHED with a publication HEAD substituted as execution.
No CI,paid services,package installation,artifact deletion,threshold change or refit.

Manifest SHA256:7cfbcfdd88bcfbe55bc7e7f9e84b839984f4f7cac01510330027622e71cc69ce.
