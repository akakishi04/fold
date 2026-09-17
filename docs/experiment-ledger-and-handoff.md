# FOLD Experiment Ledger and Handoff

> Current authoritative state. Historical results, source and preregistrations remain immutable.

## Environment / protocol

Repository **akakishi04/fold** (standalone), branch `feat/sft-target-loss`;
local `M:\asobiba\fold`. Repository-relative source paths begin `fold_lm/`, `docs/`,
`tests_lm/`, `tools/`: do not add the obsolete monorepo `fold/` prefix.
Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Hardware RTX4070 Ti SUPER; C174 itself ran CPU float32 / 2 threads.
Protected C37 `runs/chatgpt-last-result.json`:
`FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931`.
Protected fixture `runs/fixtures/v05-c-composition-20260921.pt`:
`A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E`.
Read AGENTS.md, docs/experiment-conversation-handoff-protocol.md, this handoff,
**docs/experiment-ledger-addendum-c174-c175.md**, C174 preregistration and
learned-necessity-probe-v0.1.md; Gate E evaluation contract is unchanged.
Judge -> execution validity -> metrics -> interpretation -> confounds -> ledger -> next C.
Valid negatives stay results. Do not retrain to improve a judged score or change thresholds.

## Formal state

Gate A/B PASSED; C/D PASSED within measured scope; **Gate E NOT PASSED**.
**C174 ACCEPTED PASS. C175 NOT REGISTERED. No active deciding experiment at this boundary.**
C174 execution HEAD `d011b13952abc10093d8d8d2b418ecc3d39f5fc3`.
No C174 rerun for documentation or later opt-in analyses.
C170-C173 remain ACCEPTED PASS; C160/C168/C169 remain ACCEPTED VALID NEGATIVE.

## Accepted history / interpretation boundaries

Earlier chain: docs/experiment-ledger-addendum-c173-c174.md and previous addenda;
full earlier handoff is retained in Git history at C174 execution HEAD.
C151: WITHIN_FACTOR20727/20736 and GLOBAL_CONCEPT20736/20736 per layout; nine known
errors, ranker tuning closed. C152-C167 recovery/authority/warm claims retain their scope.
C160:82944 live cycles but0 ANSWERED, accepted negative. C168:input collision lower bound
4/8, not measured model accuracy. C169:3 gaps/3 boundaries, accepted negative readiness.
C170:809 tests,532 input transfers,40 guards,72 integer fields+binding; no learned reader.
C171:845 tests,600 proof checks,158 verified/442 rejected, handwritten bounded verifier.
C172:885 tests,197 calls,27 reservations,147 internal units; reservation is not real fetch.
C173:921 tests,122 scenarios,0 failures;236 action calls/143 dispatch/122 reservations/
417 internal units/98 provider calls/95 file reads/26434 bytes/24 publications/12 derived
answers/18 verifier calls/36 rules. Single-owner local-file bridge, no learned policy,
real human messaging,Vision,durable ownership or core EvidenceState publication.

## Latest accepted C174

953/953 regression;6 models (3 paired seeds174001/174002/174003),MLP72->128->128->2,
26114 parameters.2000 updates/model,12000 total,3072000 sampled training examples.
TASK_VISIBLE versus SYNTAX_ABLATED; paired initial/batch hashes identical.
All6 final checkpoints saved before pilot scoring;raw uncorrected two-class decisions.
TRAIN36 groups/524 templates/42444 rows;pilot4 groups/116 templates/9396 rows.
56376 pilot +254664 resubstitution predictions;312 inference batches.
No actual acquisition/proof calls/evidence writes/network/production integration.

Primary macro-group BA visible:0.7217363934/0.7267349717/0.7383088136.
Paired blind:0.6914442907/0.6969538563/0.7277355168.
Missing-fact rule:0.6566257816. All3 comparisons and both recalls>0.5 pass as registered.
This is a directional development-pilot PASS, not practical necessity accuracy or Gate E.
Visible misses1101/1099/927 of2652 needs-observation rows (34.95-41.52%).
Group3 loses to blindness in all3 seeds; group38 loses in174003. Preserve heterogeneity.
Training primary BA0.7407335661/0.7410268471/0.7628742080 is also imperfect.
Mean paired gain2.35488 percentage points is descriptive,not a significance estimate.

## Artifacts / review limits

C174 `runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json`.
SHA256 `3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36`.
Log210379 bytes,SHA256 `d6dbc289260415305e2f2b4857c72d5304ef8370db5628e3a8ad1fae88a8d86c`.
Scientific manifest `6b06991409954a6a97340a2fd93dcf22bd4622e9b90e9968a670f337c830f1a4`.
Data `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.
11 artifact hashes/sizes,49 input paths,42 historical pins recorded in full summary.
Complete summary hash/metrics/gate independently recomputed;11 underlying artifacts,
953 regression and6 fits not independently rerun by reviewer. Postchecks passed per log.
C173 parent `runs/c173-v5e-acquisition-lifecycle-4507b2745ec8499982006b960a469bd3/summary.json`,
SHA256 `3c4759bbc14b4ab9849d482d2f330cbf1038c1473e2deab2aaf40f9637e635aa`.
All inherited36 blobs and42 shared source hashes agree across uploaded C173/C174 summaries.
Keep every earlier result/weight/trace; do not change historical artifact commit_sha.

## Migration / reproduction

Monorepo C1745e05168e maps to standalone registration19603c7267; C173 source snapshot
2cc2b1f4 maps to standalone61c78906. See acceptance addendum for full SHA identities.
Obsolete ExpectedHead then obsolete :fold/ source paths caused pre-training stops.
Runner-only fixd011b139 adapts source guards; science,model,data andgate unchanged.
Use tools/run_c174.ps1 for exact accepted reproduction; direct old module CLI retains
monorepo source assumptions. Future guards use standalone paths and explicit blob pins.
No reset,rebase,history rewrite or C173 rerun is needed because of migration.

## Gate / independent tracks

Nine-family Gate E contract unchanged. Final evaluation remains blocked pending candidate,
baselines,splits and numerical registration. Learned necessity is not fact/tool selection,
proof generation,live learned control or safe answers under all evidence conditions.
Multi-Axis/MA-1 and PC-ALM/FHLC remain independent research tracks;diagnostic MLP does not
replace FOLD shared-core/compression architecture. No language,Vision,long-context,
durable memory,production rollout or inferred peak-memory/latency claims.
