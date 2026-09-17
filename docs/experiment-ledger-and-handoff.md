# FOLD Experiment Ledger and Handoff

> Current authoritative state. Historical evidence, code and preregistrations are immutable.

## Environment and protocol

Repository **akakishi04/fold** (standalone), branch feat/sft-target-loss, local M:\asobiba\fold.
Repository-relative paths start fold_lm/, docs/, tests_lm/, tools/. Never add old fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; .venv-py31315\Scripts\python.exe.
RTX4070 Ti SUPER installed; necessity probes use CPU float32 / two threads.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md, docs/experiment-conversation-handoff-protocol.md, this file,
docs/experiment-ledger-addendum-c177-c178.md and
**docs/experiment-ledger-addendum-c178-preregistration.md**.
Order: verdict -> validity -> metrics -> interpretation -> confounds -> ledger -> next design.
Valid negatives stay results; do not retune checkpoints, thresholds or cases to obtain PASS.

## Formal state

Gate A/B PASSED; C/D PASSED within measured scope; **Gate E NOT PASSED**.
**C177 ACCEPTED PASS. C178 ACTIVE / NOT YET JUDGED. C179 NOT REGISTERED.**
**C176 remains ACCEPTED VALID NEGATIVE.** C174/C175 and C170-C173 remain ACCEPTED PASS;
C160/C168/C169 remain VALID NEGATIVE. Latest execution HEAD691b6df851525469889fe3640e638411ea284b58.
C177 acceptance ca8e3cf35e310372bf293327f28314d6f2d1f9fc precedes C178 registration.
Use the final C178 registration HEAD as ExpectedHead. No rerun of C176/C177 for new files.

## Accepted chain and scope

Newest detail: experiment-ledger-addendum-c177-c178.md. History continues through
experiment-ledger-addendum-c176-c177.md, c175-c176.md, c174-c175.md and earlier addenda.
Full prior handoff is preserved at691b6df851525469889fe3640e638411ea284b58 and C177 acceptance.
C151 WITHIN_FACTOR20727/20736 and GLOBAL_CONCEPT20736/20736 per layout; nine known
errors, ranker tuning closed. C152-C167 recovery/authority/warm claims retain scope.
C16082944live cycles/0ANSWERED negative. C168 collision4/8 is an input-bound lower
bound, not actual model accuracy. C1693gaps/3boundaries is negative readiness evidence.
C170809tests/532transfers/40guards/72fields is input transport, not learned reading.
C171845tests/600proofs/158verified/442rejected is handwritten bounded proof checking.
C172885tests/197actions/27reservations/147internal units is reservation/runtime.
C173921tests/122scenarios/98provider/95file reads/24publications/12derived answers;
scripted actions/proofs, local-file OBSERVE/ASK_USER, not human/Vision/production memory.

## Necessity experiments C174-C176 retained

Diagnostic MLP72->128->128->2,26114parameters, NOT FOLD shared core.
TRAIN36groups/524templates/42444rows; pilot4groups/116templates/9396rows.
C174953tests; six models,seeds174001/2/3,2000updates/model. Full syntax beats its learned
blind control and missing-rule reference under the original gate. C175973tests;
311040stored predictions,81TRAIN-only keys,51840reference decisions; full syntax beats
TRAIN-frequency reference primary0.6927057896 in all3. Both PASS,not a reliable live policy.
Count1 NEEDS/count3 SUFFICIENT weak on both TRAIN and PILOT; four groups repeatedly reused.

C1761001tests; six new paired models,seeds176001/2/3,ordinary CE vs fixed TRAIN-only
class loss balancing within missing counts. Initial weights and sampled batches paired;
12000updates/3072000samples;56376pilot+254664training predictions;312inference batches.
Mixed-count BA increases in all pairs, but original group-macro BA decreases
0.7491107571->0.6855456349,0.7005135297->0.6809826251,0.6892424825->0.6223572642.
Conditional176003 NEEDS recall0.4713423831 also fails>0.5. ACCEPTED VALID NEGATIVE.
All models/results/thresholds retained. Do not adopt or retune CONDITIONAL_CE under C176.

## Latest C177 accepted evidence

1025/1025tests in14.958s; all phases and pre/postchecks PASS.311040stored decisions,
56376pilot score rows,155520aligned decision-row pairs. Training/forwards/checkpoint
loads/seeds/threshold search/correction/acquisition/evidence writes/network all0.
83input paths,56historical pins,two outputs. Primary within-count1/2/3 mean AUC:
1760010.5910100661914962->0.5913936600412220 (+0.038359385 AUC points);
1760020.5960457082542381->0.5963641829385455 (+0.031847468 points);
1760030.5932198463519958->0.5975991306747999 (+0.437928432 points).
All exact fractions strictly improve: ACCEPTED PASS under narrow preregistered gate.
Small effects, not statistical significance, practical reliability or C176 adoption.
Same-visible-key AUC falls in first2seeds; count2/3 ordering also falls in first2.
Overall AUC falls in all3. Pilot rescues/new errors376/1059,567/1298,556/1141;
TRAIN2017/3958,2910/4762,2878/4434. Changed count1 decisions all move toward NEEDS;
changed count3 decisions all move toward SUFFICIENT. This is not proof of exact offset-only
behavior. Ordering change excludes only a pure per-count constant-shift account.
Same four reused groups; pair combinations correlated; TRAIN AUC unavailable in C177.

## Artifacts and evidence levels

C177 runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json.
SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.
Uploaded log226030bytes,aa63e74325b541ed7689fd02ce34c0bf919ca3be36375fa44af645f6cda1873e.
score-order-details.json58158bytes,4ba428f8370e9549dbe85abf76627ce60f4bd005ac5ec86182f7b8daa779b12d.
Reviewer recomputed47274-byte summary hash,66ordering tables,6exact fractions,3verdicts
and36exchange tables against uploaded C176 confusion counts. Underlying data/logit/weight
files, detailed per-group exchanges and1025regression NOT independently read/reexecuted.

C176 runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json;
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json;
SHA256d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json;
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Earlier manifests and review limits remain in chained addenda. Keep all outputs.

## Active C178 — visible-leaf binding input comparison

C178-v5e-visible-leaf-binding;V5-E-VISIBLE-LEAF-BINDING. One question:does explicit
visible-fact binding help under the same MLP and workload? This is a source-based
bottleneck hypothesis, not a diagnosis already proved by C177.
INDIRECT_FACTS=unchanged C174 full-syntax preparation. BOUND_VISIBLE_FACTS copies each
FACT leaf's referenced presence/raw observed bit into its two zero child placeholders,
as0/1 AFTER scaling. Internal child pointers and all other fields stay exact; zeroing
only those leaf coordinates recovers original input. No NOT/AND/OR evaluation, hidden
values, teacher dependency, label/group input, changed C170 PolicyInput or inference repair.
Four-fact/seven-node read-once family only. Checkpoint carries explicit representation
version. Handwritten binding is acknowledged; same parameter count does not prove equal
conditioning/effective expressivity. It is diagnostic,not production schema or FOLD core.

Changed input only; BOTH arms ordinary unweighted CE using unchanged C174 api.fit/model.
Same capacity26114, width72/128/128/2, TRAIN/pilot rows and split, optimizer and row order.
New paired seeds178001/2/3; six models;2000updates/model,batch256,Adam.001,CPUfloat32/2threads.
Paired initial and private sampled-row schedule hashes; all6final checkpoints saved and
reloaded before scores; no early stopping/selection/threshold fit. C176 weights not used.
12000updates,3072000samples,56376pilot+254664TRAIN predictions,312inference batches.
Prepare51840rows once;207360leaf lookups/414720copied fields;count preprocessing explicitly.
Historical checkpoint loads0;new roundtrip loads6;actual acquisition/proof/evidence/network0.

Primary equal mean BA for missing1/2/3. For EACH seed require bound>indirect primary;
original groupmacro>=indirect;count1NEEDS and count3SUFFICIENT recalls each strictly improve;
both bound aggregate recalls>0.5. Same joint gate form as C176,not retroactive rescoring.
Finite gate miss=>VALID NEGATIVE;no settings changed to pass. Source/schema/hash/nonfinite/
incomplete/unpaired/protection error=>INVALID,sameC178retry with restored validity.
Secondary in same batch:TRAIN/PILOTgroup/count metrics,within-count and matched-visible
AUC,paired error exchanges. TRAIN logits now saved too. Pure0/4 BA/AUC null,accuracy retained.
Same4reusedgroups,not independent holdout or final Gate E. No additional secondary gates.

C177+C176+C174summaries and23prior artifacts protected. Historical60+new4source files;
90input paths;C37/fixture extra outer guards. No old source changed. Fresh UUID output:
leaf-binding-plan.json,input-binding-audit.json,6checkpoints,pilot-predictions.json,
training-predictions.npz(with logits,seed/arm identities),complete summary.10listed artifacts.
Manifest4393da528c6193cd2d8762cfea081e102e02537148299578806b0f3dcb9facc0.
32/32actual new tests passed with Gitblob-identical C170input/C174probe dependencies;
only2synthetic rows/2updates in toy fitting. Two Python files compiled;3embedded scripts parsed.
Uploaded code/test/runner/preregistration Gitblobs match reviewed local bytes. Full historical
integration,1057regressions,WindowsPowerShell and formal6model batch NOT executed by reviewer.
**1057expected=1025+32,62modules**;one regression then one CPU learning batch.
Run tools/run_c178.ps1 -C177Summary ... -C176Summary ... -C174Summary ... -ExpectedHead ... .
Progress:precheck,regression,plan,seed/arm every500steps,3pairedBA comparisons,RESULT/POSTCHECK.
**Judge C178 -> ledger/handoff -> next design. C179 stays unregistered until then.**

## Migration and research scope

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139 runner-only migration fix enabled C174. Old direct C174CLI retains monorepo
assumptions; new guards use standalone paths and explicit Gitblobpins. No reset/rebase/
history rewrite; never edit historical artifact commit_sha. Nine-family Gate E contract
unchanged;final evaluation blocked pending full candidate,baselines,splits,numerical gate.
Necessity is not fact/tool choice,learned proof generation or safe live control.
Multi-Axis/MA-1 and PC-ALM/FHLC remain separate. No general language,Vision,long-context,
durable memory,production,latency or VRAM claims.
