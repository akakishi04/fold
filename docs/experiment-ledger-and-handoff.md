# FOLD Experiment Ledger and Handoff

> Current authoritative state. Historical evidence, code and preregistrations are immutable.

## Environment and protocol

Repository **akakishi04/fold** (standalone); branch feat/sft-target-loss; local M:\asobiba\fold.
Paths start fold_lm/,docs/,tests_lm/,tools/; never add obsolete monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; .venv-py31315\Scripts\python.exe.
RTX4070TiSUPER installed; current necessity probes run CPUfloat32/two threads.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
docs/experiment-ledger-addendum-c178-c179.md and unchanged C178 preregistration.
Order:verdict -> validity -> metrics -> interpretation -> confounds -> ledger -> next design.
Valid negatives stay results; never retune thresholds,checkpoints,seeds or cases to pass.

## Formal state

Gate A/B PASSED;C/D PASSED within measured scope;**Gate E NOT PASSED**.
**C178 ACCEPTED VALID NEGATIVE. C179 NOT REGISTERED.**
C174/C175/C177 retain scoped PASS;C176 remains ACCEPTED VALID NEGATIVE.
C170-C173 remain PASS;C160/C168/C169 remain VALID NEGATIVE. No adoption of conditional
loss or bound-input candidate follows from the older diagnostic PASS results.
Latest execution HEAD e9ee578a80b63e72a33414b62ba17a0111329ddb.
C178 requires no rerun for documentation. No active new training experiment at this boundary.

## Accepted chain and scope

Newest:docs/experiment-ledger-addendum-c178-c179.md. Earlier chain continues through
c177-c178.md,c176-c177.md,c175-c176.md,c174-c175.md and older addenda.
Previous full handoff preserved at e9ee578a80b63e72a33414b62ba17a0111329ddb.
C151 per layout WITHIN_FACTOR20727/20736 and GLOBAL_CONCEPT20736/20736;9known errors,
ranker tuning closed. C152-C167 retain their acquisition/recovery/authority/warm scopes.
C16082944live cycles/0ANSWERED negative. C1684/8input-collision lower bound is not model
accuracy. C1693gaps/3boundaries is negative readiness evidence. C17072fields/532transfers/
40guards is transport,not learned reading. C171600proofs/158verified/442rejected is a
handwritten checker. C172197actions/27reservations/147internal units is runtime reservation.
C173122scenarios/98provider/95file reads/24publications/12answers uses scripted actions and
proofs,local-file OBSERVE/ASK_USER;not real human/Vision/durable production memory.

## Necessity evidence retained

Original diagnostic MLP72->128->128->2,26114parameters,NOT FOLD shared core.
TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
C174953tests,6models;full syntax beats learned blind control and missing-rule reference.
C175973tests,311040saved predictions,81TRAIN-only keys;full syntax beats frequency table
primary0.6927057896 in all3. Both PASS,not reliable autonomous control.
C1761001tests,6models,seeds176001/2/3;conditional loss improves targeted recalls but
original groupmacro falls in all3 and one aggregate NEEDS recall falls below0.5:VALID NEGATIVE.
C1771025tests;frozen within-count AUC increases by0.000383594/0.000318475/0.004379284:
scoped PASS,not adoption. Same-visible AUC worsens in two seeds;new errors exceed rescues.
No calibration,threshold repair or checkpoint selection authorized by these results.

## Latest accepted C178

1057/1057tests in24.268s;precheck/postcheckPASS;60historical source pins,90input paths,
10output artifacts.6newmodels,seeds178001/2/3,2000updates/model,batch256,ordinary CE.
Same MLP,initial weights and row schedules paired;only visible-field binding changes.
51840prepared rows,207360lookups,414720copies.12000updates,3072000sampled rows,
56376pilot+254664TRAIN predictions,312inference batches.6new checkpoint loads,old0.
No acquisition/proof/evidence/network/production modification. run_execution_valid=True.

Primary indirect->bound:
1780010.5317227973->0.5256245661;
1780020.5627444203->0.5502559834;
1780030.5414014270->0.5461145738.
Original groupmacro0.7078306724->0.6994697476,0.7094398681->0.7014964222,
0.7178143225->0.7267296602.
Count1NEEDS10/768->0/768,132/768->150/768,107/768->146/768;
count3SUFFICIENT16/312->18/312,74/312->43/312,4/312->15/312.
Gate vectors[false,false,false,true,true],[false,false,true,false,true],[true,true,true,true,true].
Only third pair passes;ALL3required. No averaging/exclusion:ACCEPTED VALID NEGATIVE.
Within-count and matched-visible AUC decline in all3 on BOTH splits.
PILOTrescues/regressions103/106,148/176,168/214;TRAIN352/457,629/688,777/760.
Count0/4perfect with absent-class BA/AUC null. Full numerical tables are in acceptance.
Binding-only was insufficient here;do not infer architecture impossibility or learned
Boolean reasoning. Same reused4groups,not independent holdout. Do not select the third seed.

## Artifacts and evidence levels

C178 runs/c178-v5e-leaf-binding-e16d745f5b3242728e9c561023938719/summary.json;
SHA25619bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8.
Log387180bytes,98bfddf9d6ed487492f9b4f77898c06f43cb523b867c0082ab409b0552f6c2ef.
Reviewer reconstructed196186-byte summary/hash,312confusion tables,72ordering tables,
12exact AUC means,12stratum sums,36exchange tables and three gates with fit integrity.
Underlying10artifact bytes/data/logits/checkpoints/input-binding audit and1057tests/6fits
NOT independently reread or rerun. Hash-bound runner evidence differs from independent replay.
C177 runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json;
SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.
C176 runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json;
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json;
SHA256d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json;
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Older identities and review scopes remain in chained addenda;retain every output.

## Next-design boundary

Existing C178 secondary tables make another unchanged-score audit unnecessary. A concrete
next hypothesis is composition along supplied syntax links versus a sequential shared
update control,with the SAME new cell,weights,inputs and per-node dense workload in both
arms. Both would be NEW diagnostic models,not an in-place change to FOLD core or a
continuation of C178 weights. This is a design direction only;C179 is not registered.
Do not claim that the topology hypothesis is proved by C178. Do not start new training
until comparison,scope,accounting and gate are fixed in a separate preregistration.

## Migration and research limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139 runner-only fix enabled C174. Old direct C174CLI retains monorepo assumptions;
new guards use standalone paths and explicit Gitblobpins. No reset/rebase/history rewrite;
never edit historical artifact commit_sha. Nine-family Gate E contract unchanged;final
evaluation blocked pending full candidate,baselines,splits,numerical registration.
Necessity is not fact/tool choice,learned proof generation or safe live control.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate. No general language,Vision,long-context,
durable memory,production,latency or VRAM claims.
