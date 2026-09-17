# FOLD Experiment Ledger and Handoff

> Authoritative state; historical evidence,source and preregistrations stay immutable.

## Environment / protocol

Repository akakishi04/fold (standalone),branch feat/sft-target-loss,local M:\asobiba\fold.
Use root-relative fold_lm/,docs/,tests_lm/,tools/;no old monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; .venv-py31315\Scripts\python.exe.
RTX4070TiSUPER installed;current probes run CPUfloat32/two threads.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file and
**docs/experiment-ledger-addendum-c179-c180.md**.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Preserve valid negatives;never change thresholds/checkpoints/seeds/cases to obtain PASS.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C179 ACCEPTED VALID NEGATIVE. C180 NOT REGISTERED.**
C178/C176 remain VALID NEGATIVE;C174/C175/C177 retain scoped PASS.
C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier judgments unchanged.
C179 execution HEAD ec1db352749e4931d59aa7a21f1766347cbf918e.
No C179 rerun required for these documents;no model adopted or runtime modified.

## Accepted evidence / historical chain

Detailed newest record:experiment-ledger-addendum-c179-c180.md. Chain continues through
c178-c179.md,c177-c178.md,c176-c177.md,c175-c176.md,c174-c175.md and earlier addenda.
Full prior handoff at ec1db352749e4931d59aa7a21f1766347cbf918e preserves historical detail.
C151 per layout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9known errors unchanged.
C152-C167 retain original acquisition/authority/recovery/warm scopes.
C170 transports72fields,not learned reading. C171 is a handwritten bounded proof checker.
C172 reserves actions;C173 joins scripted local acquisition/admission/proofs,not autonomous
fact/tool selection,human/Vision integration or durable production memory.

Original necessity dataset:TRAIN36groups/524templates/42444rows;
PILOT4groups/116templates/9396rows. The four repeatedly inspected groups are DEVELOPMENT.
C174full-syntax MLP beats its blind control;C175beats a TRAIN-frequency reference.
C176conditional loss fails joint classification;C177small score-order gains do not adopt it.
C178visible-leaf binding fails two of three pairs;do not select its winning seed.

## Latest accepted C179

1089/1089tests in18.163s;precheck/postcheckPASS;64historical pins,105input paths,10outputs.
Six models,seeds179001/2/3,paired initialization and batches;25726parameters EACH;
177596dense forward MACs/row EACH,seven shared-cell calls. Same bound inputs and ordinary CE.
12000updates/84000batch-cell calls/3072000samples;
56376pilot+254664TRAIN predictions/312inference batches/2184cell calls.
51840prepared rows,207360lookups,414720copies. Six new checkpoint roundtrips,old loads0.
No acquisition/proof/evidence/network/production modification;run_execution_valid=True.
Primary sequence->tree:0.5599713695->0.5594518798;
0.5619536843->0.5583708105;0.5557618224->0.5499314416.
Original groupmacro0.7239095289->0.7308322310;
0.7482630048->0.7366005137;0.7386266791->0.7223088240.
Count1NEEDS243/768->264/768,264/768->264/768,183/768->132/768;
count3SUFFICIENT31/312->21/312,3/312->24/312,18/312->43/312.
Gate vectors[F,T,T,F,T],[F,F,F,T,T],[F,F,F,T,T];all fail primary.
TRAIN mixed-count BA improves in all3 but remains about0.61-0.62;not a solved training set.
Pilot AUC/order and error-exchange tables are already included;no duplicate audit needed.
A negative for this topology comparison is not an impossibility claim for FOLD.

## Artifacts / verification scope

C179 runs/c179-v5e-shared-graph-49f8f07577d74b8dace13a677691fe99/summary.json;
SHA256ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b.
Log397367bytes,72067532bc30ae65a74bad6969f68cdec9315871b1c7f7fbca8a37bad27ab0f3.
Reconstructed summary202097bytes. Reviewer checked312confusion tables,72ordering tables,
12exact AUCmeans,36exchange tables,all sums,three gates,pair hashes and workload meters.
Separate10artifact bytes/rawdata/logits/checkpoints and full1089tests/6fits not rerun here.
C178 runs/c178-v5e-leaf-binding-e16d745f5b3242728e9c561023938719/summary.json;
SHA25619bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8.
C177 runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json;
SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.
C176 runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json;
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json;
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
C175 and earlier identities remain in chained addenda. Retain all outputs.

## Next design boundary

Source exposes raw facts16 directly to the final linear head,besides the composed root64.
A possible next comparison masks only that redundant bypass while leaving the same facts
visible at leaves,both models on TREE_LINKS,and the same dense computation/training budget.
Its causal role is a hypothesis,not established by C179;no experiment registered here.
Do not silently adopt TREE as superior after its negative. No loss/threshold/width tuning.

## Migration / project limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. Old direct CLI retains monorepo assumptions;
new guards use standalone paths and Gitblobpins. No reset/rebase/history rewrite or edits
to historical artifact commit_sha. Gate E nine-family contract unchanged;final evaluation
requires a full candidate,baselines,splits,numerical preregistration. Multi-Axis/MA-1 and
PC-ALM/FHLC are separate. No language,Vision,long-context,durable-memory or speed/VRAM claim.
