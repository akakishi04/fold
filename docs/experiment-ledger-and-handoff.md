# FOLD Experiment Ledger and Handoff

> Authoritative state; historical evidence, source and preregistrations remain immutable.

## Environment / protocol

Repository akakishi04/fold (standalone); branch feat/sft-target-loss; local M:\asobiba\fold.
Root-relative fold_lm/,docs/,tests_lm/,tools/; no old monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; .venv-py31315\Scripts\python.exe.
RTX4070TiSUPER installed; current probes CPUfloat32/two threads.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
**docs/experiment-ledger-addendum-c181-c182.md** and
**docs/experiment-ledger-addendum-c182-preregistration.md**.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Preserve valid negatives;never alter checkpoints,seeds,cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C181 ACCEPTED PASS. C182 ACTIVE / NOT YET JUDGED. C183 NOT REGISTERED.**
C180/C179/C178/C176 remain VALID NEGATIVE;C174/C175/C177 retain scoped PASS.
C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier judgments unchanged.
C181 execution HEAD3ec4cd8f2afc664799f1e6bfecfce457dd255ad4.
C181 acceptancebd3117087e2a1aefd99c3e07e54269015c0099fa PRECEDES C182 registration.
Use final C182 registration HEAD. No C181 rerun or production adoption.

## Accepted chain / scientific scope

Latest detail:experiment-ledger-addendum-c181-c182.md,then c180-c181.md,c179-c180.md,
c178-c179.md,c177-c178.md,c176-c177.md,c175-c176.md,c174-c175.md and earlier addenda.
Previous full handoff at3ec4cd8f2afc664799f1e6bfecfce457dd255ad4 retains prior detail.
C151 per layout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9known errors unchanged.
C152-C167 retain original acquisition/authority/recovery/warm scopes.
C170transports72fields;C171handwritten bounded proof checker;C172reserves actions;
C173scripted local acquisition/admission/proofs,not autonomous selection or durable memory.
Original necessity data:TRAIN36groups/524templates/42444rows;
PILOT4groups/116templates/9396rows. Reused pilot groups are DEVELOPMENT.
C174syntax MLP beats blind control;C175beats TRAIN-frequency reference.
C176loss weighting fails;C177small AUC gains do not adopt it.
C178binding,C179tree routing,C180direct-readout removal fail their joint comparisons.
C181proper-node auxiliary supervision passes on the unchanged common tree/bound-input
substrate with direct fact readout. Negative prior comparisons remain unchanged.

## Latest accepted C181

1153/1153tests14.986s;precheck/postcheckPASS;72historical pins,135input paths,11outputs.
Six models,seeds181001/2/3;25921stored parameters,25726inference parameters;
seven tree-cell applications/row. Only auxiliary loss alpha0 FINAL_ONLY vs alpha1
INTERNAL_SEMANTICS differs. TRAIN two proper internal nodes,three classes:
KNOWN_ZERO/KNOWN_ONE/UNRESOLVED. No root/leaf/pilot auxiliary targets,no hidden values,
no teacher-forced states;inference uses original base only,no teacher/head calls.
42444teacherrows/84888targets/254664nonroot evaluations;
12000updates/84000batchcells/3072000mainsamples;
12000auxforwards/6144000targetuses(3072000activealpha).
56376pilot+254664TRAIN predictions,312inferencebatches/2184cells;
newcheckpointloads6,oldloads0;acquisition/proof/evidence/network0;productionmodifiedFalse.
Primary final-only->internal:.5445409706->1;.5666106133->1;.5551288778->1.
Original groupmacro:.7138799019->1;.7567305611->1;.6991769650->1.
Count1NEEDS198/264/264->768each of768;count3SUFFICIENT21/3/18->312each of312.
Every internal model:9396/9396pilot and42444/42444TRAIN main correct;both recalls1;
bothsplit mixed-count and matched-visible AUC1. Allfiveconditions/allseedsPASS.
Pilotrescued2459/2429/2411,regressed0;TRAINrescued9591/9604/9605,regressed0.
28188candidatepilotpredictions are three repeats of9396inputs,not independent problems.
No threshold repair. Freeze all six checkpoints;do not train further on saturated pilot.

Interpretation:strong local support for added proper-node supervision,not a unique
credit-assignment mechanism. Measured base can express correct decisions on this
finite family;does not prove capacity sufficient for larger tasks or impossibility of
final-only learning under another budget. Handwritten training teacher/common routing
are explicit. No independent final holdout,arbitrary/repeated-variable reasoning,
language,Vision,autonomous fact/tool selection or Gate E claim.

## Artifacts / independent verification

C181 runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json;
SHA256bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98.
Uploadedlog406464bytes,SHA256bb41d932f432d30f501fb0982fa1934f4966b9d82db5b308f687777e07e7a2ff.
Reconstructedsummary201752bytes;reviewer checked312confusiontables,72ranktables,
12exactAUCmeans,36exchanges,threegates,pairhashes,workload;allconsistent.
Reviewer inspected main/teacher code boundary. Separate11artifact bytes and full1153
regression/sixfits NOT independently rerun. Do not claim checkpoint replay yet.
C180 runs/c180-v5e-fact-bypass-669cce9093064995bf26b1bf176dd609/summary.json;
SHA2569ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2.
C179 runs/c179-v5e-shared-graph-49f8f07577d74b8dace13a677691fe99/summary.json;
SHA256ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b.
C178 runs/c178-v5e-leaf-binding-e16d745f5b3242728e9c561023938719/summary.json;
SHA25619bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8.
C177 runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json;
SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.
C176 runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json;
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json;
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
C175/earlier identities remain in chained addenda. Retain all artifacts/checkpoints.

## Active C182 — frozen fact-index renaming

C182-v5e-frozen-fact-renaming / V5-E-FROZEN-FACT-RENAMING.
One question:frozen necessity decisions invariant to consistent fact-index renaming?
Same six C181checkpoints,source seeds181001/2/3,no fresh seed/training/update/selection.
Verify entire25921parameter C181state,then construct ONLY original25726parameter
C179TREE_LINKSbase;auxiliary head not constructed/called. Original predict,batch1024,
CPUfloat32/two threads,seven cells. No teacher generation,hidden values or output repair.

First replay all311040original TRAIN/PILOTpredictions:exactargmax,absolute logit
error<=1e-6,relative0;reaggregate saved predictions and metrics. Replay discrepancy
is INVALID,not silently repaired. Hashes and source guards precede inference.
Then9396pilotrows x23lexicographic nonidentity permutations =216108new numeric inputs.
Permutation maps OLDfactindex -> NEWfactindex;move the complete fact record and change
all matching references together. Keep ASTtopology/operators/negation/runtime unchanged;
bound leaf presence/value must match original. No labels in transform. All original
leaforders1,2,3,4;nonidentityleaforders prove numeric novelty but NOT new semantic tasks.

New-condition predictions1296648(all6models),648324(3internalcandidates).
Totalinference1607688rows/1692batches/11844cells;checkpointloads6;
training/freshseeds/teacher/auxiliary/proof/acquisition/evidence/network0.
Gate:ALL3INTERNAL_SEMANTICSmodels,ALL23permutations,EVERYrow must remain correct
and decision-invariant;one finite error=>VALID NEGATIVE. All138model/permutation cells
complete;FINAL_ONLYcontrols scored,not required perfect. No logit invariance demand.
PASS is naming-robustness evidence ONLY;C181status and GateE unchanged either way.

Save plan,transform-audit,frozen-replay,renaming-results,renamed-predictionsNPZ,summary.
Fiveartifacts excluding summary;rawlogits/decisions preserved;bygroup/bycount/exchanges
in same batch. Data and checkpoints stay fixed;no re-scoring with adjusted thresholds.
76historicalsourcepins+4ownfiles;151protectedinputpaths plusC37/fixture outerguards.
Manifest4aa37d094447417e466048f92d2b4949296078ab77d00f5d7d4b24ec46ff55d5.
32helpertestsPASS using actualnewcode+transcribedfetchedparentdefinitions,notfullcheckout;
9720syntheticrenamingschecked by independentcompletionenumeration;noofficialscores.
TwoPythonfilescompile;threeembeddedPythonblocksparse. Full1185regression,WindowsPS,
fullsource/artifactchain and1607688predictionbatch UNEXECUTED.
**1185expected=1153+32;66modules**,one regression plusonefrozenbatch.
Run tools/run_c182.ps1 withC181/C180/C179/C178/C177/C176/C174summaries/expectedHEAD.
Progressidentityreplay,permutation1/23..23/23,candidateerrors,RESULT/POSTCHECK.
Judge C182 ->ledger/handoff->next;**no C183 until judgment**.

## Migration / project limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. New guards use standalone paths/Gitblob
pins. No reset,rebase,history rewrite or historical artifact commit_sha modification.
Gate E nine-family contract unchanged;final assessment requires full candidate,
baselines,splits,numerical preregistration. Multi-Axis/MA-1 and PC-ALM/FHLC remain
SEPARATE research tracks. No language,Vision,long-context,durable-memory,latency/VRAM claim.
