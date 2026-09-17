# FOLD Experiment Ledger and Handoff

> Current authoritative state. Historical evidence,code and preregistrations are immutable.

## Environment and protocol

Repository **akakishi04/fold** (standalone),branch feat/sft-target-loss,local M:\asobiba\fold.
Repository-relative paths start fold_lm/,docs/,tests_lm/,tools/. Never add old fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5;.venv-py31315\Scripts\python.exe.
RTX4070 Ti SUPER installed;current necessity probes run CPUfloat32/2threads.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
docs/experiment-ledger-addendum-c176-c177.md and
**docs/experiment-ledger-addendum-c177-preregistration.md**.
Order:formal verdict -> validity -> metrics -> interpretation -> confounds -> ledger -> next C.
Valid negative results stay results;do not retune checkpoints,thresholds or cases to pass.

## Formal state

Gate A/B PASSED;C/D PASSED within measured scope;**Gate E NOT PASSED**.
**C176 ACCEPTED VALID NEGATIVE. C177 ACTIVE / NOT YET JUDGED. C178 NOT REGISTERED.**
C174/C175 remain ACCEPTED PASS;C170-C173 remain ACCEPTED PASS;
C160/C168/C169 remain ACCEPTED VALID NEGATIVE.
C176 execution HEAD6155242c6564858293d355c51ae2a3dbc7f25bdb.
C176 acceptance5c8a1bee6571ba3511ca4989408c7bde8d58135e precedes C177 registration.
Use final C177 registration HEAD for execution. No rerun of C176 for documentation.

## Accepted chain and boundaries

Newest detail:experiment-ledger-addendum-c176-c177.md;history continues through
experiment-ledger-addendum-c175-c176.md,c174-c175.md,c173-c174.md and earlier addenda.
Prior full handoff is preserved at6155242c6564858293d355c51ae2a3dbc7f25bdb.
C151 WITHIN_FACTOR20727/20736 and GLOBAL_CONCEPT20736/20736 per layout;9known errors,
ranker tuning closed. C152-C167 recovery/authority/warm claims retain original scope.
C16082944live cycles/0ANSWERED negative. C168 input-collision4/8 is a classifier lower
bound,not actual model accuracy. C1693gaps/3boundaries is a negative readiness result.
C170809tests/532transfers/40guards/72fields is input transport,not learned reading.
C171845tests/600proofs/158verified/442rejected is handwritten bounded proof checking.
C172885tests/197actions/27reservations/147internal units is reservation/runtime.
C173921tests/122scenarios/98provider/95file reads/24publications/12derived answers;
scripted actions/proofs,local-file OBSERVE/ASK_USER,not real human/Vision/production memory.

## C174/C175 retained

C174953tests;diagnostic MLP72->128->128->2,26114parameters,not FOLD shared core.
TRAIN36groups/524templates/42444rows;pilot4groups/116templates/9396rows.
6models,seeds174001/2/3,2000updates/model;paired full/blind initial weights and batches.
Original pilot macro-group BA full0.7217363934/0.7267349717/0.7383088136;
blind0.6914442907/0.6969538563/0.7277355168;missing-rule0.6566257816.
C175973tests;311040 stored predictions;81TRAIN-only keys;51840 table classifications;
0training/forwards/checkpoint loads. Reference primary0.6927057896;full gains
2.90306/3.40292/4.56030points. Both correctly registered PASS,not usable safe policy.
Count1 NEEDS and count3 SUFFICIENT recognition weak,including on training rows.
Matched-visible pairs correlated,not independent tests;4pilot groups reused.

## Latest accepted C176 — loss-only intervention

1001/1001tests in17.597s;precheck/postcheckPASS;71input paths,52historical pins,
10output artifacts. CPUfloat32/2threads;6new models(seeds176001/2/3),same full syntax,
initial/batches paired. Uniform versus fixed TRAIN conditional loss weights only.
For mixed count1..3,w(m,y)=N_m/(2*N_m_y);pure0/4weight1;batch-length reduction.
Counts[0,1]:[8384,0],[12416,4352],[6048,6528],[968,3224],[0,524].
12000updates,3072000samples,56376pilot+254664train predictions,312inference batches.
Six new checkpoint roundtrips,historical loads0;no actual acquisition/proof/evidence/network.
All6 final checkpoints saved before scores. No capacity/steps/threshold/seed retuning.

Mixed-count BA uniform->conditional:
1760010.5625558301->0.5687604269;
1760020.5380938275->0.5731907963;
1760030.5387065201->0.5652427614.
Original group-macro BA0.7491107571->0.6855456349;
0.7005135297->0.6809826251;0.6892424825->0.6223572642.
ALL3 fail nondegradation. Both targeted recalls improve in ALL3,but conditional176003
aggregate NEEDS recall0.4713423831 also fails>0.5 guard. Uniform176003 also below0.5;
retain it,not invalid. Do not report primary-only improvement as PASS.
Aggregate missed-needed835->827,1223->885,1350->1402 (denominator2652);
false-needs1627->2318,1133->2202,918->1451 (denominator6744).
Training mixed-count BA improves while original training group score drops in all3.
Result is a loss/quality trade-off,not proof that reweighting or FOLD is impossible.
Frozen logits may separate ordering changes from decision-offset changes;summary alone
cannot establish that mechanism. No threshold fitting or inference correction authorized.

## Artifacts and evidence levels

C176 runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json.
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
Uploaded log345072bytes,caa9bfd2496ea416d8c780d8244e32d6db315463aa299524199acf1d0003207b.
Reviewer independently reconstructed162846-byte summary hash and312 metric tables,
group/stratum arithmetic,pair/workload integrity,weights and exact gate. Underlying10
output artifacts/originalNPZ,1001regression and6fits NOT independently read or rerun.

C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json;
SHA256d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json;
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Earlier manifests/hashes and detailed review limits are in chained addenda. Keep outputs.

## Active C177 — frozen score-order audit

C177-v5e-frozen-score-order-audit;V5-E-FROZEN-SCORE-ORDER-AUDIT.
One question:did conditional loss improve score ordering within the same missing count,
not only alter raw decision bias? Same six C176 models and four reused pilot groups.
No retraining,new forward,checkpoint deserialization,new seed,threshold fitting,
calibration,inference correction,actual acquisition or evidence write.
311040 saved decisions replayed;56376 pilot score rows;155520 aligned decision-row pairs.
TRAIN logits unavailable,so TRAIN AUC is not computed and not filled by new inference.
Score=float64(logit1)-float64(logit0),NEEDS positive,ties exact half.
Primary=equal mean pair-order AUC of counts1/2/3;exact fractions for strict comparison.
PASS only if conditional>uniform in EACH seed. Ties/failed seed=>VALID NEGATIVE.
This is a NARROW NEW DIAGNOSTIC ENDPOINT,not an alternate C176 adoption criterion.
C176 remains negative even if C177 passes;no practical accuracy,calibration or Gate E claim.
Positive ordering excludes only a pure per-stratum constant-offset account of these scores.
Negative does not prove offset-only behavior or architecture incapacity.

Batch secondary:all4 pilot-group AUCs,overall AUC,same-blind-key pair ranking,and paired
rescues/regressions/flip directions on TRAIN and PILOT separately by group/count.
Correlated pair counts are not independent samples. No selected threshold or model.
C174 eleven+C176 ten artifacts hash/size checked;twelve checkpoints hashed only.
56historical+4own source files;83input paths;C37/fixture outer protection.
Outputs:score-order-plan.json,score-order-details.json,complete summary.json.
Manifest942735a9f843485eaf7b2b3b5f15cab774e749f7e52d37adcb64dcd8dcb5572e.
24/24 actual new-module synthetic helper tests passed;Python and three embedded scripts
parsed. Full old-module/artifact integration,1025tests,WindowsPowerShell and registered
analysis NOT executed by reviewer. **1025expected=1001+24,61modules**,one regression.
Run tools/run_c177.ps1 -C176Summary ... -C174Summary ... -ExpectedHead ... .
Progress1/3replay,three paired AUC lines,2/3tables,3/3protection,RESULT/POSTCHECK.
**Judge C177 -> ledger/handoff -> next design. No C178 before judgment.**

## Migration and research scope

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139 runner-only migration fix enabled C174. Old direct C174CLI retains monorepo
assumptions;new sourceguards use standalone paths and explicit Gitblobpins. No reset,
rebase or history rewrite;do not edit historical artifact commit_sha.
Nine-family Gate E contract unchanged;final evaluation blocked pending full candidate,
baselines,splits and numerical preregistration. Necessity is not fact/tool selection,
learned proof generation or safe live control. Multi-Axis/MA-1 and PC-ALM/FHLC separate.
No language,Vision,long-context,durable memory,production or latency/VRAM claims.
