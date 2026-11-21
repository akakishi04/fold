# C183 formal verdict — ACCEPTED PASS

V5-E; akakishi04/fold; feat/sft-target-loss.
Acceptance precedes any C184 registration. C184 NOT REGISTERED at this commit.
Gate E NOT PASSED. C182 remains ACCEPTED VALID NEGATIVE; C181 remains ACCEPTED PASS.
All historical source, checkpoints, preregistrations and judgments are unchanged.

## 1. Formal verdict

C183-v5e-frozen-renaming-path-attribution / V5-E-FROZEN-RENAMING-PATH-ATTRIBUTION:
ACCEPTED PASS. The complete one-case C182 failure set is TREE_ONLY_SUFFICIENT under
the registered frozen activation interchange. No rerun or repair of C182 is implied.

## 2. Execution validity / evidence

Execution HEAD53bfa13bc74e74334a610605fc4fb63a4cc84702.
1217/1217 focused tests passed in55.625s. Source/artifact precheck PASS; protected
inputs preserved, tracked tree clean, execution HEAD preserved; run_execution_valid=True.
Existing C145 warning occurred inside a passing test and did not invalidate execution.
Summary:runs/c183-v5e-path-attribution-b806a83c1a4044538713b844fe640198/summary.json
SHA256:ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24.
Canonical summary97680bytes reconstructed exactly from uploaded complete log.
Uploaded log304544bytes; SHA256
b69446b4444c9725b5ad23ecc30858a366321f9ffd237ab5d1464b673a03c3cd.

All1296648 saved C182 decisions audited by runner. Six frozen C181checkpoints;
112752 coherent identity/permutation17 replay rows,120batches/840shared-cell calls;
112752 additional hybrid readout rows,120headbatches;225504total decisions.
All12coherent replay sections have exact decisions and max_abs_logit_difference0.
80historicalsourcepins,161protectedinputpaths,6outputartifacts excluding summary.
Training/freshseeds/teacher/auxiliary/proof/acquisition/evidence/network0.
Productionmodified=False; gate_e_candidate=False. Reported benchmark35.40309080001316s
includes diagnostic work and is not production latency or performance evidence.

Reviewer independently verified summary hash,120confusion-derived metric tables,
24four-group aggregates and their sums,24model/condition counterexample argmaxes,
12replay summaries,workload totals and fixed gate. Recalculated all four counterexample
margins and additive residual. No discrepancy. Source inspection checked capture hook,
coordinate selection and frozen-head intervention.
Limits: separate6outputartifacts,source NPZ and checkpoint bytes were NOT supplied;
no independent model replay or1217regression here. Local git clone failed DNS and
must not be described as a full checkout or complete dependency integration.

## 3. Exact counterexample / deciding measurements

Seed181003,INTERNAL_SEMANTICS,permutation17,old_to_new(2,3,1,0).
Zero-based source_row41788,pilot_row7687,template_index515,semantic_group3,missing1.
Original:(F1 AND (F2 AND (NOT F3 AND NOT F4))).
Visible facts:F1=1,F2=1,F3=UNOBSERVED,F4=0. Thus the expression depends on NOT F3;
both completions remain possible and NEEDS_OBSERVATION(label1) is correct.
Renamed:(F3 AND (F4 AND (NOT F2 AND NOT F1))).
Visible facts:F1=0,F2=UNOBSERVED,F3=1,F4=1. Meaning unchanged.

|Condition|SUFFICIENT logit|NEEDS logit|NEEDS margin|Decision|
|---|---:|---:|---:|---|
|ORIGINAL|-2.504523277282715|3.4346587657928467|5.9391820430755615|NEEDS(correct)|
|RENAMED|0.40941694378852844|0.3998054265975952|-0.009611517190933228|SUFFICIENT(wrong)|
|TREE_ONLY|0.5437130928039551|0.4381943941116333|-0.10551869869232178|SUFFICIENT(wrong)|
|DIRECT_ONLY|-2.638819456100464|3.3962697982788086|6.0350892543792725|NEEDS(correct)|

Tree-route margin change=-6.044700741767883.
Direct-route margin change=+0.09590721130371094,partially offsetting the adverse tree change.
Additive residual(renamed-tree-direct+original)=-2.9802322387695312e-08.
Final readout is linear; additive score decomposition is expected up to arithmetic.
Do not call threshold crossing a nonlinear interaction in this final head.

On the full matched9396row cohort,INTERNAL_SEMANTICS181001/181002 have0errors in all
four conditions;181003 has0/1/1/0errors in ORIGINAL/RENAMED/TREE_ONLY/DIRECT_ONLY.
These hybrid counts are counterfactual diagnostics,not admissible policy performance.

## 4. Interpretation / confounds

For THIS frozen model and counterexample,the renamed tree/root route alone suffices
to reproduce the wrong decision. The direct-fact route alone does not;its score effect
actually favors the correct class here. This is stronger local evidence than a
retrained bypass comparison,but not a universal causal explanation of model errors.
C182 changes the leaf fact-ID scalar along this tree route while topology,operators,
negation and bound visible bits remain fixed. Learned root state retains harmful
sensitivity to an arbitrary reference-index convention on this case.

The coherent margin is small and sensitivity must be disclosed. However,all original
replays are exact and the tree-route score movement is about6.045,not the2.98e-8
additive residual. The log does not establish that the error is mere rounding noise,
that float64 would repair it,or robustness across alternative numerical environments.
Margins are uncalibrated logits,not confidence probabilities or proof certificates.

C181's strong finite-family learning result remains. C182's one real renamed error
remains. Do not discard seed181003,modify thresholds,train the counterexample,or deploy
hybrid activations. This localization is complete; no additional unchanged-score audit
is required. Any proposed repair must have its own explicit scope and registration.
Canonicalizing nuisance LOCAL indices is a possible interface intervention,not learned
invariance;never conflate local IDs with meaningful entity names or external evidence IDs.

## 5. Handoff

C183 ACCEPTED PASS. C184 NOT REGISTERED at acceptance. Gate E NOT PASSED.
Retain summary/log/all6artifacts and the complete prior chain. Next design is a later
commit and cannot rewrite this diagnosis. Multi-Axis/MA-1 and PC-ALM/FHLC remain separate.
