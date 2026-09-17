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
docs/experiment-ledger-addendum-c180-c181.md and
**docs/experiment-ledger-addendum-c181-preregistration.md**.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Preserve valid negatives;never alter checkpoints,seeds,cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C180 ACCEPTED VALID NEGATIVE. C181 ACTIVE / NOT YET JUDGED. C182 NOT REGISTERED.**
C179/C178/C176 remain VALID NEGATIVE;C174/C175/C177 retain scoped PASS.
C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier judgments unchanged.
C180 execution HEAD074419e41b38ad756b2c29a50ea070d5ca60f2d3.
C180 acceptance01253f5fd548c69f3db3e1b1c4fbc56b4017160a PRECEDES C181 registration.
Use final C181 registration HEAD. No C180 rerun, production modification or adoption.

## Accepted chain / scientific scope

Latest detail:experiment-ledger-addendum-c180-c181.md,then c179-c180.md,c178-c179.md,
c177-c178.md,c176-c177.md,c175-c176.md,c174-c175.md and earlier addenda.
Prior full handoff at074419e41b38ad756b2c29a50ea070d5ca60f2d3 preserves historical detail.
C151 per layout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9known errors unchanged.
C152-C167 retain original acquisition/authority/recovery/warm scopes.
C170 transports72fields,not learned reading;C171handwritten bounded proof checker;
C172reserves actions;C173joins scripted local acquisition/admission/proofs,not autonomous
fact/tool selection,human/Vision integration or durable production memory.
Original necessity data:TRAIN36groups/524templates/42444rows;
PILOT4groups/116templates/9396rows. Reused pilot groups are DEVELOPMENT.
C174full-syntax MLP beats blind control;C175beats TRAIN-frequency reference.
C176weighted loss fails joint classification;C177small AUC gains do not adopt it.
C178leaf binding and C179tree versus sequence fail joint improvement.
C180masking final raw-fact bypass also fails;do not infer one causal mechanism from negatives.

## Latest accepted C180

1117/1117tests15.165s;precheck/postcheckPASS;68historical pins,120input paths,10outputs.
Six paired models,seeds180001/2/3;25726parameters,177596dense MACs+94mask multiplies/row;
seven tree-cell calls. Only final raw-facts16bypass masked in NO_DIRECT_FACTS;leaf facts retained.
12000updates/84000batch cells/3072000samples;
56376pilot+254664TRAIN predictions/312inference batches/2184cells/12312mask calls.
51840prepared rows,207360lookups,414720copies;six new checkpoint roundtrips,old loads0.
No acquisition/proof/evidence/network/production modification;run_execution_valid=True.
Primary direct->no-direct:0.5612275160->0.5629750876;0.5538738272->0.5354616036;
0.5666788151->0.5743076451. Original groupmacro0.7177524742->0.7214223537;
0.6851235806->0.6810320756;0.7208480929->0.7407231754.
Count1NEEDS264/768->264/768,113/768->75/768,264/768->259/768;
count3SUFFICIENT28/312->31/312,70/312->34/312,51/312->44/312.
Gate vectors[T,T,F,T,T],[F,F,F,F,F],[T,T,F,F,T];no pair passes.
Unchanged pilot decisions99.5743%,98.1801%,97.3287%. Removing this edge is not a sufficient
fix. Similar re-trained outputs do not prove no causal use;other paths can compensate.
Bothsplit confusion/AUC/error-exchange/logits already stored;no duplicate unchanged-score audit.

## Artifacts / independent verification

C180 runs/c180-v5e-fact-bypass-669cce9093064995bf26b1bf176dd609/summary.json;
SHA2569ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2.
Log404324bytes,SHA25605e3c95345cc710d1c359b7154e9d82c422991eec732fb1698cd44c95ff51fde.
Reconstructed summary205427bytes. Reviewer checked312confusion tables,72ordering tables,
12exact AUCmeans,36exchange tables,three gates,pair hashes,sums/workload meters.
Separate10artifact bytes and full1117regression/six fits NOT rerun here.
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
C175 and earlier identities remain in chained addenda. Retain all artifacts/checkpoints.

## Active C181 — TRAIN proper-subexpression supervision

C181-v5e-proper-subexpression-supervision;V5-E-PROPER-SUBEXPRESSION-SUPERVISION.
Question:does TRAIN-only intermediate semantic supervision improve main necessity?
Both use original C179 TREE_LINKS/DIRECT readout,C178bound72;negative variants are common
substrates,not adopted improvements. No C180mask. Changed variable:auxiliary loss alpha0
FINAL_ONLY vs alpha1 INTERNAL_SEMANTICS. Same added Linear64->3 head in both.
Temporary hook captures seven actual cell outputs;read exactly two proper internal nodes.
Main forward unchanged;no teacher-forced states. Inference uses only original base.forward;
no teacher or auxiliary-head calls and no prediction repair.

Teacher classes KNOWN_ZERO/KNOWN_ONE/UNRESOLVED (0/1/2),from TRAIN visible facts only.
Read-once validation;do not generalize three-valued propagation to correlated repeats.
Generate42444TRAIN rows/84888labels once. Evaluate six nonroot nodes per row,254664total;
root not evaluated/supervised;leaves not supervised;pilot teacher labels0. Node indices
checked against neural syntax. Freeze labels before fitting;no hidden payloads.
Root-label duplication is excluded. A single necessity bit is not full intermediate
semantics:known0 and known1 differ under parent AND/OR.

Seeds181001/2/3;six fresh models;2000updates/model,batch256,Adam.001,ordinary mean mainCE
+alpha*mean two-nodeCE;no class reweighting. CPUfloat32/2threads,paired full initial weights
and row schedules(seed+1000000). All six final checkpoints saved/restored before scoring.
25921stored parameters each (25726base+195head);inference evaluates25726base parameters.
Dense forwardMACs177980training/177596inference each;seven cell calls each. Zero-alpha head
has zero gradients;nominal/forward-budget parity is not effective-gradient parity.
12000main updates/84000batch cells/3072000main samples;12000aux forwards;
6144000aux target uses both arms,3072000with nonzero coefficient.
56376pilot+254664TRAIN main predictions;312inference batches/2184cells;inferenceaux0.
Historicalcheckpoint loads0,new6;acquisition/proof/evidence/network0;productionmodifiedFalse.

Same per-seed joint gate:internal improves mixed-count1/2/3BA,count1NEEDS,count3SUFFICIENT;
original4groupmacro cannot decline;both aggregate recalls>0.5. ALL conditions/ALL seeds.
PASS supports added-supervision package,not a unique cause;finite miss=>VALID NEGATIVE.
Invalid source/schema/nonfinite/protection/unpaired/incomplete=>restore SAME C181 validity.
No retuning. Same four reused DEVELOPMENTgroups;Gate E NOT PASSED.
Bothsplit MAIN logits/confusion/AUC/exchanges saved in same batch;no auxiliary-score rescue.

72historical pins+4own files;135protectedinputpaths;53prior artifacts hashed,not loaded.
C37/fixture extra outerguards. Outputs11excluding summary:plan,teacher-audit,teacher-targets,
6checkpoints,pilot-predictions,training-predictions. Preserve all results.
Manifest1f1baf3f40018ab84eb69d1812cf0c04d9fae624ee50e705d3bc780e35d6d3f4.
36/36new helper tests pass on actual new code+transcribed fetched C179definitions;
NOT complete Gitblob parent/checkout. Synthetic teacher enumeration648rows;fits2rows/2updates.
Historical regression-list helper mocks predecessor;formalrunner resolvesREALlist.
PyTorch2.10CPU/NumPy2.3.5;two Pythonfiles compiled;3embeddedrunner Pythonblocks parsed.
Full1153/WindowsPowerShell/completeartifactchain/formal6fits UNEXECUTED.
**1153expected=1117+36,65modules**,one regression then paired batch.
Run tools/run_c181.ps1 -C180Summary ... -C179Summary ... -C178Summary ... -C177Summary ...
-C176Summary ... -C174Summary ... -ExpectedHead ... . Progress main_loss/aux_loss every500,
three pairedBA lines,RESULT/POSTCHECK. **Judge C181 ->ledger/handoff->next;no C182 yet.**

## Migration / project limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. Old CLI retains monorepo assumptions;
new guards use standalone paths/Gitblob pins. No reset,rebase,history rewrite or alteration
of historical artifact commit_sha. Gate E nine-family contract remains unchanged;final
assessment requires full candidate,baselines,splits,numerical preregistration.
Multi-Axis/MA-1 and PC-ALM/FHLC remain SEPARATE research tracks.
No language,Vision,long-context,durable-memory,latency or VRAM claim.
