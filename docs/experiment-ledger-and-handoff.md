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
docs/experiment-ledger-addendum-c177-c178.md and the unchanged C177 preregistration.
Order: verdict -> validity -> metrics -> interpretation -> confounds -> ledger -> next design.
Valid negatives stay results; do not retune checkpoints, thresholds or cases to obtain PASS.

## Formal state

Gate A/B PASSED; C/D PASSED within measured scope; **Gate E NOT PASSED**.
**C177 ACCEPTED PASS. C176 ACCEPTED VALID NEGATIVE. C178 NOT REGISTERED.**
C174/C175 and C170-C173 remain ACCEPTED PASS; C160/C168/C169 remain VALID NEGATIVE.
Latest execution HEAD: 691b6df851525469889fe3640e638411ea284b58.
No rerun of C176 or C177 for documentation. No new experiment is active at this
acceptance-only boundary; a new comparison requires a separate preregistration.

## Accepted chain and scope

Newest detail: experiment-ledger-addendum-c177-c178.md. History continues through
experiment-ledger-addendum-c176-c177.md, c175-c176.md, c174-c175.md and earlier addenda.
Previous full handoff is preserved at 691b6df851525469889fe3640e638411ea284b58.
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

Diagnostic MLP72->128->128->2, 26114parameters, NOT the FOLD shared core.
TRAIN36groups/524templates/42444rows; pilot4groups/116templates/9396rows.
C174953tests; six models, seeds174001/2/3, 2000updates/model. Full syntax beats its
learned blind control and missing-rule reference under the original registered gate.
C175973tests; 311040stored predictions,81TRAIN-only keys,51840reference decisions;
full syntax beats TRAIN-frequency reference primary0.6927057896 in all three seeds.
Both PASS, not a reliable live necessity policy. Count1 NEEDS/count3 SUFFICIENT weak,
including on training resubstitution; repeated four pilot groups, not independent tests.

C1761001tests; six new paired models, seeds176001/2/3, ordinary CE vs fixed TRAIN-only
class loss balancing within missing counts. Same initial weights and sampled batches;
12000updates/3072000samples;56376pilot+254664training predictions;312inference batches.
Primary mixed-count BA increases in all pairs, but original group-macro BA decreases
0.7491107571->0.6855456349,0.7005135297->0.6809826251,0.6892424825->0.6223572642.
Conditional176003 NEEDS recall0.4713423831 also fails >0.5. ACCEPTED VALID NEGATIVE.
All models, results and thresholds retained. No adoption or retuning of CONDITIONAL_CE.

## Latest C177 accepted evidence

1025/1025tests in14.958s; all analysis phases and pre/postchecks PASS.
311040stored decisions,56376pilot scores,155520aligned decision-row pairs.
Training/forwards/checkpoint deserialization/fresh seeds/threshold search/correction/
actual acquisition/evidence writes/network all0.83input paths,56historical pins,two outputs.
Primary mean within-count1/2/3 AUC uniform->conditional:
176001 0.5910100661914962->0.5913936600412220 (+0.038359385 AUC points);
176002 0.5960457082542381->0.5963641829385455 (+0.031847468 points);
176003 0.5932198463519958->0.5975991306747999 (+0.437928432 points).
Exact fractions satisfy each-seed strict improvement: ACCEPTED PASS under narrow gate.
Small effects; no statistical significance or practical reliability claim.
Same-visible-key AUC decreases in first two seeds and improves only in third.
Overall AUC decreases in all3. Count2/3 ordering decreases in first two seeds.
Pilot rescued/new errors:376/1059,567/1298,556/1141. TRAIN:2017/3958,2910/4762,2878/4434.
All changed count1 decisions move toward NEEDS; all changed count3 toward SUFFICIENT.
This does not prove exact offset-only behavior. Narrow ordering gain excludes only a
pure per-count constant-shift explanation, not other mechanisms. C176 stays NEGATIVE.
Same four reused groups; pair combinations are correlated. TRAIN AUC unavailable.

## Artifacts and evidence levels

C177 runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json.
SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.
Uploaded log226030bytes,aa63e74325b541ed7689fd02ce34c0bf919ca3be36375fa44af645f6cda1873e.
Detailed ordering/exchanges:score-order-details.json58158bytes,
4ba428f8370e9549dbe85abf76627ce60f4bd005ac5ec86182f7b8daa779b12d.
Reviewer recomputed complete47274-byte summary hash,66ordering tables,6exact fractions,
3verdicts and36exchange tables against uploadedC176 confusion counts. Underlying data,
logit/checkpoint files, detailed per-group exchanges and1025regression NOT independently
read/reexecuted here. No model or threshold changed during review.

C176 runs/c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7/summary.json;
SHA256b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b.
C175 runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json;
SHA256d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
C174 runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json;
SHA2563e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
Data SHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Earlier manifests and review limits remain in chained addenda. Keep all outputs.

## Next design, not yet registered

Do not extend unchanged-logit auditing merely to find a favorable endpoint. A concrete
candidate bottleneck is input binding: current MLP must match leaf fact indices to the
separate observed-fact table, then learn Boolean composition. This is source-based
hypothesis, not a measured cause. Consider a paired input-only comparison that copies
already-visible presence/value to referencing leaves without solving the expression,
changing labels/loss/width/training budget or supplying hidden facts. It needs a separate
preregistration after this acceptance; no C178 execution is authorized by this paragraph.

## Migration and research scope

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139 runner-only migration fix enabled C174. Old direct C174CLI retains monorepo
assumptions; new sourceguards use standalone paths and explicit Gitblobpins. No reset,
rebase or history rewrite; never edit historical artifact commit_sha.
Nine-family Gate E contract unchanged; final evaluation blocked pending full candidate,
baselines,splits,numerical preregistration. Necessity is not fact/tool choice, learned
proof generation or safe live control. Multi-Axis/MA-1 and PC-ALM/FHLC remain separate.
No general language,Vision,long-context,durable memory,production,latency or VRAM claims.
