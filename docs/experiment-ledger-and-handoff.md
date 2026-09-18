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
**docs/experiment-ledger-addendum-c182-c183.md** and original C182 preregistration.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Preserve valid negatives;never alter checkpoints,seeds,cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C182 ACCEPTED VALID NEGATIVE. C181 ACCEPTED PASS. C183 NOT REGISTERED.**
No active experiment until separate registration. No C182 rerun or production adoption.
C180/C179/C178/C176 remain VALID NEGATIVE;C174/C175/C177 retain scoped PASS.
C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier judgments unchanged.
C182 execution HEAD8ee4942d7b4ec73ac65de8d6f17f59c297c6ee99.

## Accepted chain / scientific scope

Latest detail:experiment-ledger-addendum-c182-c183.md,then c181-c182.md,c180-c181.md,
c179-c180.md,c178-c179.md,c177-c178.md,c176-c177.md,c175-c176.md,c174-c175.md and earlier.
Full previous handoff at8ee4942d7b4ec73ac65de8d6f17f59c297c6ee99 retains all prior detail.
C151 per layout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9known errors unchanged.
C152-C167 original acquisition/authority/recovery/warm scopes retained.
C170transports72fields;C171handwritten proof checker;C172reserves actions;
C173scripted local acquisition/admission/proofs,not autonomous selection/durable memory.
Data:TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Reused pilot groups are DEVELOPMENT,not independent confirmation.
C174syntax MLP beats blind control;C175beats TRAIN-frequency reference.
C176loss weighting fails;C177small AUC gains do not adopt it.
C178binding,C179tree routing,C180direct-readout removal fail their joint comparisons.
C181proper-node auxiliary supervision passes on common tree/bound input/direct readout:
three INTERNAL_SEMANTICS models correct on all9396pilot+42444TRAIN rows each;
no teacher/head at inference. Its finite-task success does not prove a unique causal
credit-assignment mechanism,larger-task capacity or independent generalization.

## Latest accepted C182

1185/1185tests43.599s;precheck/postcheckPASS;76historicalpins,151inputpaths,5outputs.
Six frozen C181checkpoints,seeds181001/2/3;no freshseed/training/selection.
311040original decisions replayed;ALL12replays max_abs_logit_difference0.
9396pilotrows x23nonidentity renamings=216108new numeric inputs,notnewsemanticproblems.
All138model/permutation cells complete;1296648new predictions,648324candidate predictions.
Total1607688rows/1692batches/11844cells;checkpointloads6;teacher/head/proof/acquisition/
evidence/network0. Original base only. ProductionmodifiedFalse;GateEcandidateFalse.
Candidate errors/flips per seed:0/0,0/0,1/1. Sole failure:181003,permutation17,
old_to_new(2,3,1,0),group3,missing1,label1NEEDS->prediction0SUFFICIENT.
Candidate total648323/648324correct does NOT pass strict zero-error gate.
Control errors54828/55768/54330;flips8115/169/6667,descriptive only.
Do not invent exact row/formula/margin:these require saved NPZ/data,not console summary.
The transform changes leaf-ID numeric channel and final fact-table layout together;
which route caused the error remains unmeasured. Do not call it numeric noise without
replay/margins. C180retraining-ablation differs from frozen path attribution.

## Artifacts / verification

C182 runs/c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4/summary.json;
SHA25606c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73.
Log287823bytes,SHA256ec89e4ea2ba4ebfc68c658897c8aa03a7af410ce53741b5977d3cba8240e93ee.
Reconstructedsummary83982bytes;60metric tables,6exchanges,138records,12replays checked.
Separate5artifacts/data/checkpointbytes NOT independently replayed by reviewer;
full1185tests NOT rerun. Local git clone failed DNS;not a checkout.
C181 runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json;
SHA256bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98.
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
DataSHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Retain all artifacts/checkpoints. Further analysis must not rewrite prior outcomes.

## Migration / project limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. New guards use standalone paths/Gitblob
pins. No reset,rebase,history rewrite or historical artifact commit_sha modification.
Gate E nine-family contract unchanged;final assessment requires full candidate,
baselines,splits,numerical preregistration. Multi-Axis/MA-1 and PC-ALM/FHLC remain
SEPARATE research tracks. No language,Vision,long-context,durable-memory,latency/VRAM claim.
