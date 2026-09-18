# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, source and preregistrations remain immutable.

## Environment / protocol

Repository akakishi04/fold (standalone); branch feat/sft-target-loss; local M:\asobiba\fold.
Root-relative fold_lm/,docs/,tests_lm/,tools/; no monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; .venv-py31315\Scripts\python.exe.
Current diagnostic probes CPUfloat32/two threads; RTX4070TiSUPER installed.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
**docs/experiment-ledger-addendum-c183-c184.md** and
**docs/experiment-ledger-addendum-c184-preregistration.md**.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Preserve valid negatives;do not change checkpoints,seeds,cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C183 ACCEPTED PASS. C184 ACTIVE / NOT YET JUDGED. C185 NOT REGISTERED.**
C182 ACCEPTED VALID NEGATIVE;C181 ACCEPTED PASS. No rerun or production adoption.
C180/C179/C178/C176 remain VALID NEGATIVE;C174/C175/C177 retain scoped PASS.
C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier judgments unchanged.
C183 executionHEAD53bfa13bc74e74334a610605fc4fb63a4cc84702.
C183acceptance45a7f6b0df2cf5715f69aafe6cf1a706ee0a2e76 PRECEDES C184registration.
Use final C184registrationHEAD for execution. No historical source/checkpoint edits.

## Accepted chain / scope

Latest detail:experiment-ledger-addendum-c183-c184.md,then c182-c183.md,c181-c182.md,
c180-c181.md and earlier chained addenda. Full prior handoff at53bfa13bc74e74334a610605fc4fb63a4cc84702.
C151 per layout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9known errors unchanged.
C152-C167 original acquisition/authority/recovery/warm scopes retained.
C170transports72fields;C171handwritten proof checker;C172reserves actions;
C173scripted local acquisition/admission/proofs,not autonomous selection/durable memory.
Data TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Repeatedly inspected pilot is DEVELOPMENT,not independent confirmation.
C174syntax MLP beats blind control;C175beats TRAIN-frequency reference.
C176loss weighting fails;C177small AUC gains do not adopt it.
C178binding/C179tree/C180bypass removal fail their joint comparisons.
C181proper-node auxiliary supervision:all3internal models correct on9396pilot+42444TRAIN
rows each;no teacher/head at inference. Additional TRAIN supervision is real.
C182frozen renaming:648324candidate predictions,one error(seed181003,permutation17);
C181 preserved;zero-error naming-invariance claim failed. No seed dropping or repair.

## Latest accepted C183

1217/1217tests55.625s;precheck/postcheckPASS;80historicalpins,161protectedpaths,6outputs.
Six frozen C181checkpoints,seeds181001/2/3;no new seed/training/teacher/auxiliary calls.
1296648savedC182predictions audited.112752coherent replay rows/120batches/840cells;
112752hybridheadrows/120batches;225504outputs.12coherent replays exact,logitdelta0.
Failure identified automatically:source_row41788,pilot_row7687,template515,group3,
missing1,seed181003,permutation17(2,3,1,0),label1NEEDS.
Original F1 AND(F2 AND(NOT F3 AND NOT F4));facts1,1,unknown,0;depends on NOT F3.
Renamed F3 AND(F4 AND(NOT F2 AND NOT F1));facts0,unknown,1,1;same meaning.
ORIGINAL/RENAMED/TREE_ONLY/DIRECT_ONLY decisions1/0/0/1;
NEEDS margins5.9391820430755615/-.009611517190933228/-.10551869869232178/6.0350892543792725.
Mode TREE_ONLY_SUFFICIENT:local isolated tree-route sufficiency,not universal mechanism.
Tree margin shift-6.044700741767883;direct+.09590721130371094 helps correct class.
Additive residual-2.9802322387695312e-08. Readout is linear;no nonlinear final-head claim.
Small final margin disclosed,not dismissed as numerical noise. No float64 test performed.
All candidate cohort hybrid errors0except181003RENAMED/TREE_ONLY1each.
Hybrids are not valid full inputs or corrected policy. C182negative remains unchanged.
No acquisition/proof/evidence/network/productionchange. No GateE candidate.

## Evidence / independent verification

C183 runs/c183-v5e-path-attribution-b806a83c1a4044538713b844fe640198/summary.json
SHA256ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24.
Log304544bytes,SHA256b69446b4444c9725b5ad23ecc30858a366321f9ffd237ab5d1464b673a03c3cd.
Reconstructedsummary97680bytes. Reviewer independently checked120confusiontables,
24groupaggregates,24counterexampleargmaxes,12replays,margins,residual,gate/workload.
Separate6artifact/checkpoint/data bytes and1217tests NOT independently replayed.
C182 runs/c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4/summary.json;
SHA25606c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73.
C181 runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json;
SHA256bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98.
C180/C179/C178/C177/C176/C174paths and hashes remain in prior handoff/addenda and runners.
DataSHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Retain ALL past artifacts/checkpoints. Do not turn summary arithmetic into model replay.

## Active C184 — explicit LOCAL index normalization contract

C184-v5e-canonical-fact-index-adapter / V5-E-CANONICAL-FACT-INDEX-ADAPTER.
Changed variable:handwritten first-occurrence numeric fact-ID normalization before
unchanged C178preparation/C179TREE_LINKS frozen C181base. All6models/seeds181001/2/3.
No training,freshseed,selection,threshold adjustment,teacher or auxiliary inference.
Traverse existing syntax;rename first encountered fact1,second2,etc;move all4numeric
fact-record fields together. Keep syntax operators,links,negation,headers/runtime.
Do NOT evaluate logic. Preserve canonical-to-input inverse slot map. Unknown stays unknown.
Scope4distinct facts/7nodes/read-once,observed/unobserved only;reject unsupported inputs.
LOCAL slot IDs are NOT meaningful entity names or external provenance identifiers.
Complete C170PolicyInput binding-sidecar/action remapping integration is NOT implemented.
Diagnostic module only;no production modification or observed-state writes.

For source canonical x and consistent renaming p,N(rename_p(x))=x. Thus identical
normalized input implies identical frozen behavior by construction. This is an adapter
contract,NOT new learned invariance or new semantic generalization. Do not oversell PASS.
No per-case oracle/golden-row argument to canonicalize;references only in TEST equality.
C182rawnegative/C183diagnosis remain unchanged and all historical outputs remain archived.

267948primary normalization rows=51840original+216108renamed;535896normalizer rowcalls
including idempotence;267948inverse reconstructions. Original311040prediction replay:
exactargmax/logitatol1e-6,rtol0;source/replay disagreementINVALID.
Then23renamings x9396rows x6models=1296648normalized predictions;648324candidateoutputs.
All138model/permutation cells;total1607688inference rows/1692batches/11844cells.
Checkpointloads6;no new checkpoints. CPUfloat32/2threads/deterministic/batch1024.
Actual duplicate normalized inputs are still forwarded;no hidden cache counting.
Gate:all canonical/roundtrip/idempotence/input checks0mismatches;all models preserve
original decisions/logitswithin1e-6;all3internalmodels0errors;controloriginalerrorsretained.
Finite failure=>VALID NEGATIVE;source/schema/nonfinite/replay/incomplete/protection=>
SAME C184 validity recovery. No retuning. Same4developmentgroups;Gate E NOT PASSED.

Inherit C183precheck+summary/all6artifacts;84historicalpins+4ownfiles,172protectedpaths,
plusouterC37/fixture. Manifestde54874ad495253c0111c006b9f40f6c85291fc67a8ad243ceb232c1b13e24ed.
5artifacts excluding summary:plan,canonicalization-audit,replay,normalized-results,
normalized-predictionsNPZ including inverse maps. Save all raw predictions,not repair oldones.
32/32newtestsPASS on actual newmodule/self-contained adapter+gate,not full run().
9720synthetic renamings independently evaluated;no official checkpoints or scores used.
Pythoncompilation/3embeddedPythonblocksPASS. No complete checkout(DNSfailure).
Full1249/WindowsPS/172artifactchain/formal1607688predictions UNEXECUTED.
1249expected=1217+32;68modules;one regression then frozenbatch.
Run tools/run_c184.ps1 withC183/C182/C181/C180/C179/C178/C177/C176/C174summaries/ExpectedHead.
Progresssource-replay,permutation1/23..23/23,canonical_mismatches/candidate_errors,RESULT/POSTCHECK.
Judge C184 ->ledger/handoff->next;C185 NOT REGISTERED. After this contract,do not add
unchanged-score audits merely to revisit saturated naming cases;use a new ability question.

## Migration / project limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. New guards use standalone paths/Gitblob
pins. No reset,rebase,history rewrite or historical artifact commit_sha modification.
Gate E nine-family contract unchanged;final assessment requires full candidate,
baselines,splits,numerical preregistration. Multi-Axis/MA-1 and PC-ALM/FHLC remain
SEPARATE research tracks. No language,Vision,long-context,durable-memory,latency/VRAM claim.
