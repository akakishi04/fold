# FOLD Experiment Ledger and Handoff

> Current authoritative state. Historical evidence, code and preregistrations stay immutable.

## Environment / protocol

Repository **akakishi04/fold** (standalone),branch feat/sft-target-loss,local M:\asobiba\fold.
Paths start fold_lm/,docs/,tests_lm/,tools/;never add the obsolete monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5;.venv-py31315\Scripts\python.exe.
RTX4070 Ti SUPER installed;current necessity experiments run CPUfloat32/2threads.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this handoff,
**docs/experiment-ledger-addendum-c175-c176.md** and
**docs/experiment-ledger-addendum-c176-preregistration.md**.
Judge -> validity -> metrics -> interpretation -> confounds -> ledger -> next design.
Valid negatives stay results;never retune thresholds/checkpoints/cases to obtain a PASS.

## Formal state

Gate A/B PASSED;C/D PASSED within measured scope;**Gate E NOT PASSED**.
**C175 ACCEPTED PASS. C176 ACTIVE / NOT YET JUDGED. C177 NOT REGISTERED.**
C175 execution HEAD d54a4921a4e90ea58d72cd66988f946e67c1031d.
C175 acceptance847472a9f38f664b276675543935254326d45af7 precedes C176 registration.
Use final C176 registration HEAD as ExpectedHead. C174/C175 need no rerun for new files.
C170-C174 remain ACCEPTED PASS;C160/C168/C169 remain ACCEPTED VALID NEGATIVE.

## Accepted chain and scope

Latest detail:experiment-ledger-addendum-c175-c176.md. Prior chain continues through
experiment-ledger-addendum-c174-c175.md,experiment-ledger-addendum-c173-c174.md and earlier
addenda;full older handoff retained at C175 execution and acceptance-only HEADs.
C151 WITHIN_FACTOR20727/20736 and GLOBAL_CONCEPT20736/20736 per layout;9known errors,
ranker tuning closed. C152-C167 recovery/authority/warm evidence retains scope.
C16082944live cycles/0ANSWERED negative. C168 input-collision4/8 lower bound is not model
accuracy. C1693gaps/3boundaries remains accepted negative on its frozen interface.
C170809tests/532transfers/40guards/72fields is input transport,not learned reading.
C171845tests/600proofs/158verified/442rejected is handwritten bounded proof checking.
C172885tests/197calls/27reservations/147internal units is reservation/runtime.
C173921tests/122scenarios/98provider/95file reads/24publications/12derived answers;
scripted decisions/proofs,local-file OBSERVE/ASK_USER,not human/Vision/production memory.

## C174/C175 evidence retained

C174 execution d011b13952abc10093d8d8d2b418ecc3d39f5fc3.953tests,6models,3paired seeds
174001/174002/174003;MLP72->128->128->2,26114parameters;2000updates/model,12000total,
3072000sampled rows. TRAIN36groups/524templates/42444rows;pilot4groups/116templates/
9396rows.56376pilot+254664resubstitution predictions. Paired initial weights/batches;
all final checkpoints saved before pilot scoring. No runtime acquisition or proof repair.
Full original primary0.7217363934/0.7267349717/0.7383088136;blind0.6914442907/
0.6969538563/0.7277355168;missing-rule0.6566257816. Correct C174PASS,not safe necessity policy.

C175973/973tests,311040stored decisions replayed,81TRAIN-only frequency keys,
51840reference classifications;0training/forwards/checkpoint loads/seeds/acquisition.
64input paths,48historical source pins;source/artifact/final guardPASS per log.
Reference primary0.6927057895807895. Full gains2.90306/3.40292/4.56030percentage points;
each full model has both aggregate recalls>0.5. Registered C175PASS. Group3 still loses
in all3seeds. Reference optimizes TRAIN row-majority,not held-out macroBA;it is not
uniformly stronger than all learned blind controls. Same4pilot groups,not independent evidence.

Secondary PILOT_EVAL pattern,full seeds in order:
count1 needs recall73/768,24/768,230/768 (9.505%,3.125%,29.948%);
count3 sufficient recall11/312,7/312,11/312 (3.526%,2.244%,3.526%);
count2BA58.890%,60.110%,59.390%. Count0/4all correct but one class only;BA null.
Matched-visible both-correct25585/23176/35258 of165552 correlated pairs;15.454%,13.999%,
21.297%;blind0 is expected when input is identical. Not independent samples or logical mastery.
Similar count1/count3weakness on TRAIN means not exclusively held-out generalization.
TRAIN counts[sufficient,needs] by missing count:
0:[8384,0],1:[12416,4352],2:[6048,6528],3:[968,3224],4:[0,524].
Frequency-biased incentives are a hypothesis,not a proved internal mechanism.

## Artifacts and review scope

C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json.
SHA256d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
Uploaded log235289bytes,34830743bf4da903f7a02e5816d08e21ecc68ee43dd65433b92158166f82209c.
audit-details.json218224bytes,e3b0590fec5e46ad8463a897ca06775514df3ee7c3967dc304b8af0411e12ef9.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json.
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
C174 data eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65;
manifest6b06991409954a6a97340a2fd93dcf22bd4622e9b90e9968a670f337c830f1a4.
Earlier parent/checkpoint/trace identities remain in chained addenda;keep all outputs.
Reviewer recomputed complete C175summary hash,96confusion tables,group arithmetic,
12matched-pair rates and three gate differences. Detailed81-key table,C174NPZ/predictions/
checkpoints and user973regression were NOT independently read/replayed by reviewer.

## Active C176 — paired conditional loss intervention

C176-v5e-missing-count-conditional-loss;V5-E-MISSING-COUNT-CONDITIONAL-LOSS.
Changed variable ONLY fixed TRAIN loss weighting conditional on missing count and label.
Both arms see full C174syntax. Same original model class,scaling,rows,split,optimizer,
capacity,updates,batch size and exact paired sampled row sequence. New seeds176001/2/3;
UNIFORM_CE versus CONDITIONAL_CE;6newmodels,no C174checkpoint continuation.

For mixed strata1..3,w(m,y)=N_m/(2*N_m_y);pure strata0/4weight1. Counts derive TRAIN only.
Each mixed class gets equal loss mass;each stratum and full TRAIN retain original total
mass. Uniform row sampling unchanged. mean(weight*unreducedCE) divides by batch length,
not batch weight sum. No clipping/threshold tuning/evaluation-based weights or inference repair.
Same common loop for both arms;ordinary CE mathematically,not promised bitwise C174replay.
2000updates/model,batch256,Adam.001,CPUfloat32/2threads,deterministic.12000updates,
3072000samples,56376pilot+254664train predictions,312inference batches. Save/reload all6
final checkpoints before any scores. Final only,no selection/early stopping. No live actions.

Primary NEW intervention score=equal mean BA of missing-count1/2/3 on reused pilot.
For EACH seed:conditional primary strictly improves over uniform;original4groupmacroBA
must not drop;count1needs recall AND count3sufficient recall strictly improve;both
aggregate recalls>0.5. No seed averaging. Finite miss=>VALID NEGATIVE. Source/nonfinite/
incomplete/paired-schedule/protection error=>INVALID,sameC176retry unchanged specification.
All per-group/count0..4 metrics retained;pure-stratum BA null,accuracy still reported.
Post-C175development design reuses4groups;new seeds do not make an independent holdout.
No final Gate E threshold,statistical-significance or practical reliability claim.

Parent C175and C174summaries plus all13artifacts protected.52historical+4new source files,
71input paths;standalone C175guard reused,no old monkey-patch. C37/fixture outer guards.
Fresh UUID directory:plan,weighttable,6checkpoints,pilotpredictions,trainingpredictions,
summary. Manifest09ce8d00f2f6d09fda96f93e51aed6c34fd5b4e74eba77d51848c8e1f8dbafa8.
28/28actual-code helper tests passed with small synthetic counts/8-row linear toy fits;
not registered pilot training or complete dependency integration. Python compiled and3
embedded scripts parsed. Full1001/WindowsPowerShell/artifact-backed6model batch unexecuted.
**1001 focused tests expected=973+28,60modules**,one regression then one training batch.
Run tools/run_c176.ps1 -C175Summary ... -C174Summary ... -ExpectedHead ... .
Progress precheck,regression,plan,seed/arm every500updates,3comparisons,RESULT/POSTCHECK.
**Judge C176 -> ledger/handoff -> next design. C177 stays unregistered until then.**

## Migration / Gate limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only adaptation enabled accepted C174. Its original direct CLI retains
monorepo assumptions;new sourceguards use standalone paths and preserved Gitblobpins.
No reset/rebase/history rewrite. Do not edit historical artifact commit_sha.
Nine-family Gate E contract unchanged;final evaluation blocked pending full candidate,
splits,baselines and numerical preregistration. Fact/tool choice,learned proof generation
and safe live control remain separate. Multi-Axis/MA-1 and PC-ALM/FHLC independent.
No language,Vision,long-context,durable memory,production rollout or memory/latency claims.
