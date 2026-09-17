# FOLD Experiment Ledger and Handoff

> Current authoritative state. Historical evidence, code and preregistrations stay immutable.

## Environment / protocol

Repository **akakishi04/fold** (standalone), branch `feat/sft-target-loss`, local
`M:\asobiba\fold`. Paths start fold_lm/,docs/,tests_lm/,tools/; never add monorepo fold/.
Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5, `.venv-py31315\Scripts\python.exe`.
RTX4070 Ti SUPER is installed; C174/C175 are CPU experiments.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
**docs/experiment-ledger-addendum-c175-c176.md**,and C175/C174 preregistrations.
Judge -> validity -> metrics -> interpretation -> confounds -> ledger -> next design.
Valid negatives stay results; never alter thresholds/checkpoints/cases to turn one PASS.

## Formal state

Gate A/B PASSED;C/D PASSED within measured scope;**Gate E NOT PASSED**.
**C175 ACCEPTED PASS. C174 ACCEPTED PASS. C176 NOT REGISTERED.**
No active deciding experiment at this acceptance-only boundary.
C175 execution HEAD d54a4921a4e90ea58d72cd66988f946e67c1031d.
C170-C173 remain ACCEPTED PASS;C160/C168/C169 remain ACCEPTED VALID NEGATIVE.
No C174 retraining or C175 rerun for documentation.

## Accepted chain

C175 detailed verdict:experiment-ledger-addendum-c175-c176.md. Prior history:
experiment-ledger-addendum-c174-c175.md,experiment-ledger-addendum-c173-c174.md and earlier
addenda. Full earlier handoff remains at C175 execution HEAD in Git.
C151 WITHIN_FACTOR20727/20736 and GLOBAL_CONCEPT20736/20736 per layout;9 known errors;
ranker tuning closed. C152-C167 retrieval/recovery/authority/warm evidence retains scope.
C16082944 live cycles/0ANSWERED negative. C168 input collision4/8 lower bound is not learned
accuracy. C1693 gaps/3 boundaries remains a negative on its frozen interface.
C170809 tests/532 transfers/40 guards/72 fields is input transport,not a learned reader.
C171845 tests/600 proofs/158verified/442rejected is handwritten bounded proof checking.
C172885 tests/197 action calls/27reservations/147internal units is reservation/runtime.
C173921 tests/122 scenarios/98provider/95file reads/24publications/12derived answers;
scripted proposals/proofs,local-file OBSERVE/ASK_USER,not human/Vision/production memory.

## C174 learned pilot retained

Execution d011b13952abc10093d8d8d2b418ecc3d39f5fc3.953 tests,6 models,3 paired seeds
174001/174002/174003;MLP72->128->128->2,26114 parameters;2000 updates each,12000 total,
3072000 sampled rows. TRAIN36 groups/524templates/42444rows;PILOT4groups/116templates/
9396rows.56376pilot+254664resubstitution predictions. CPUfloat32/2threads,paired initial
weights and minibatches;all final checkpoints saved before pilot scoring. No live action.
Full primary0.7217363934/0.7267349717/0.7383088136;blind0.6914442907/0.6969538563/
0.7277355168;missing-rule0.6566257816. Correct preregistered PASS,not safe practical quality.
Full misses1101/1099/927 of2652 needs rows. Group3 loses to ablation in all seeds.
C174 data SHA256 eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Scientific manifest6b06991409954a6a97340a2fd93dcf22bd4622e9b90e9968a670f337c830f1a4.

## Latest accepted C175

973/973 tests,18.873s.311040 saved decisions reaggregated;81 TRAIN-only frequency keys;
51840reference classifications.0newtraining/model forwards/checkpoint loads/seeds/
acquisitions/evidencewrites/network. Source/artifact precheck and final protections PASS.
64input paths,48historical pins. C174 outputs and all historical code remain unchanged.

Primary reference0.6927057895807895. Full improvements are2.9030603848/3.4029182141/
4.5603024001 percentage points;each full model's two aggregate recalls>0.5. PASS.
Reference is TRAIN row-majority,not an optimum for pilot macro BA or uniformly stronger
than learned blind controls. Group3 still loses to reference in all3 seeds.
Same four pilot groups,reused analysis;not independent confirmation or an improved model.

Important secondary findings on PILOT_EVAL:
- With1missing,needs recall73/768,24/768,230/768 (9.505%,3.125%,29.948%).
- With3missing,sufficient recall11/312,7/312,11/312 (3.526%,2.244%,3.526%).
- With2missing,BA58.890%,60.110%,59.390%.
- With0/4missing,all correct but each stratum has only one label;BA null.
- Matched-visible opposite-label both-correct25585/23176/35258 of165552 correlated pairs;
  full rates15.454%,13.999%,21.297%;blind all0,an expected fixed-input limitation.
Similar count1/count3 weaknesses exist in TRAIN,not only held-out transfer.
TRAIN counts [sufficient,needs] by missing count:
0:[8384,0],1:[12416,4352],2:[6048,6528],3:[968,3224],4:[0,524].
These patterns motivate a TRAIN-loss incentive intervention;they do not prove the internal
mechanism or justify arbitrary capacity/step/threshold search.

## Artifacts and review scope

C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json.
SHA256 d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
Uploaded log235289bytes,34830743bf4da903f7a02e5816d08e21ecc68ee43dd65433b92158166f82209c.
audit-details.json218224bytes,e3b0590fec5e46ad8463a897ca06775514df3ee7c3967dc304b8af0411e12ef9.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json.
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
C173 parent identity and earlier artifacts remain in chained acceptance addenda.
Reviewer recomputed full C175 summary hash,96confusion metric tables,group arithmetic,
12pair rates and three gate differences. Underlying detailed81-key table,C174data/
predictions/checkpoints and user973test run were not independently read/replayed.
Keep every previous output. Do not overwrite historical report commit_sha.

## Migration

Old monorepo C1745e05168e maps to standalone19603c7267;C173 source2cc2b1f4 maps to
61c78906. d011b139 runner-only guard adaptation enabled accepted C174 execution.
Original C174 direct CLI still retains monorepo source assumptions;its accepted runner
handles them explicitly. New guards use standalone paths and preserved blob identities.
No reset/rebase/history rewrite is needed.

## Next-design boundary / independent tracks

C176 not yet registered here. Prefer testing TRAIN loss balancing within missing-count
strata,with unchanged model,rows,split,steps and paired batches,before capacity increases.
A design must declare reused pilot data,TRAIN-only weights,no inference label access,
raw predictions,exact endpoints and fixed workload. No result is implied by this proposal.
Nine-family Gate E contract unchanged;final evaluation blocked pending full candidate,
splits,baselines and numerical preregistration. Fact/tool choice,learned proof generation
and reliable live decisions remain separate. Multi-Axis/MA-1 and PC-ALM/FHLC independent.
No language,Vision,long-context,durable memory or production performance claims.
