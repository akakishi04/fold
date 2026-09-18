# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations remain immutable.

## Environment / protocol

Repository `akakishi04/fold` (standalone); branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Root-relative `fold_lm/`, `docs/`, `tests_lm/`, `tools/`; no monorepo `fold/` prefix.
Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Probes: CPU float32 / two threads; RTX4070TiSUPER installed.
Protected C37 `runs/chatgpt-last-result.json` SHA256:
`FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931`.
Protected `runs/fixtures/v05-c-composition-20260921.pt` SHA256:
`A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E`.
Read AGENTS.md, docs/experiment-conversation-handoff-protocol.md, this file,
docs/experiment-ledger-addendum-c185-c186.md, the unchanged C186 preregistration, and
**docs/experiment-ledger-addendum-c186-execution-recovery.md**.
Order: verdict, validity, metrics, interpretation, confounds, ledger, next design.
Preserve valid negatives. Never alter checkpoints/seeds/cases/thresholds to obtain PASS.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C185 ACCEPTED PASS. C186 ACTIVE / NOT YET JUDGED. C187 NOT REGISTERED.**
Latest C186 attempt at `a4127d8a6bef0bf7eafd6e5d76fbb2061ab74eba`:
**INVALID EXECUTION / RETRY SAME C186**, not a scientific negative.
Use the subsequent execution-recovery commit HEAD, not that failed-attempt HEAD.
C185 acceptance `4ce19a7f08717fef8c963f53282cc4340458700f` precedes C186 registration.
C184/C183/C181 PASS; C182 VALID NEGATIVE; C180/C179/C178/C176 VALID NEGATIVE.
C174/C175/C177 retain scoped PASS; C170-C173 PASS; C160/C168/C169 VALID NEGATIVE.
All earlier results/checkpoints remain unchanged. No C185 rerun or production adoption.

## Latest execution recovery — before any C186 model replay

Full uploaded log: 218511 bytes, SHA256
`2772bdf9cc8f0e28fa769a6f10d6c9c950860e790ddc49ce554555db665ea1a0`.
Source/artifact precheck PASS; **1317/1317 tests PASS in40.601s**.
Then old C175.load_npz rejects C185 episode-predictions.npz: `Oversized expanded NPZ`.
Its 32MiB generic ceiling is smaller than the registered 70810728-byte C185 raw arrays.
Failure occurs BEFORE checkpoint restoration/static replay/providers/episode blocks.
No C186 scientific result; 0 completed blocks. Final protected inputs preserved,
tracked tree clean, execution HEAD preserved, run_execution_valid=False.
Separate invalid.json was not uploaded; retain its existing run directory and log.

Recovery: C186-only accepted-artifact reader, no C175 edit or global monkeypatch.
Exact accepted compressed bytes/hash, eight names/shapes/dtypes, bounded NPY headers,
no object/pickle, no duplicate/unregistered member, full header checks before arrays.
Expanded ceiling70843592bytes is derived from shapes plus header/framing allowance.
C186 precheck exercises headers before tests; its one parent-NPZ load uses this reader.
Scientific manifest and original C186 preregistration unchanged.
**Current execution counts:1341tests=1317+24,71modules,92historicalpins,203protectedpaths.**
OWN additionally protects loader, recovery test module and recovery addendum.
13 output artifacts unchanged. No change in replay tolerance or deciding gate.
56/56 helper tests passed on actual complete patched C186+loader (32old+24new), including
synthetic full70810728-byte arrays and exact value preservation. Three embedded Python
blocks parse; no WindowsPS/fullcheckout/203-input chain/official NPZ or model replay here.
Full1341regression and296960episodes remain for the user-side SAME C186 retry.

## Latest accepted C185 / evidence chain

Detailed acceptance: docs/experiment-ledger-addendum-c185-c186.md; follow c184-c185,
c183-c184,c182-c183,c181-c182 and earlier chained addenda. Previous full handoff at
`a4127d8a6bef0bf7eafd6e5d76fbb2061ab74eba` retains the original C186 registration state.

C185:1285/1285tests64.077s;32blocks;118784episodes. Each INTERNAL_SEMANTICS candidate:
14848episodes,3072necessary reads/publications,11776skips,zero initial/missed/unneeded/
post/contract failures. All3:44544episodes,9216reads,35328skips,0static-to-live flips.
All6C181checkpoints,56376static replays/logitdelta0,89088live initial+16896post neural
rows;162360total rows/180batches/1260cellcalls. Allpolicies31744reads/publications,
6983680bytes;26080failures entirely controls. Decision charges150528/internal245760.
88historicalpins,182protectedpaths,13artifacts. Reported wall-clock is not production latency.

C185 summary: runs/c185-v5e-single-missing-acquisition-72d30a1a4e114de5b981352de26055e6/summary.json
SHA256`843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949`.
Accepted episode-predictions.npz:1716066bytes, SHA256
`e597baf0dfa76b34a32dcb2a0445640aaeb21bb99a22af25c26c854ef3eabcf8`.
C185 uploaded log335006bytes SHA25623376d685553dba67dc0f8c01b20c653138be7da0d4553aaf9faa80168c4a356.
C184 summary runs/c184-v5e-canonical-indices-5e2a159b64164b3a919762ebdbdc4f90/summary.json
SHA256`7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04`.
C183 summary runs/c183-v5e-path-attribution-b806a83c1a4044538713b844fe640198/summary.json
SHA256`ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24`.
C182 summary runs/c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4/summary.json
SHA256`06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73`.
C181 summary runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json
SHA256`bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98`.
C180/C179/C178/C177/C176/C174 paths/hashes remain in previous addenda and runners.
Dataset SHA256`eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.
Summary arithmetic/source review is not independent checkpoint/artifact-byte replay.

## Accepted scope / limitations

C151 per layout: WITHIN_FACTOR20727/20736;GLOBAL_CONCEPT20736/20736;9known errors retained.
C152-C167 original acquisition/authority/recovery scopes remain unchanged.
C170transports72fields;C171handwritten proof checker;C172reserves;C173real tiny-file
acquisition/admission with scripted targets,not learned selection or durable memory.
TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Repeatedly inspected PILOT is DEVELOPMENT,not independent confirmation.
C174syntax helps/C175beats frequency reference;C176weighting fails;C177smallAUC gains
are not adoption. C178binding/C179tree/C180bypass fail joint comparisons.
C181proper-node TRAIN supervision gives0errors on all9396pilot+42444TRAIN per3candidates;
no teacher/head at inference,extra TRAIN information,not unique mechanism proof.
C182oneerror/648324 renaming predictions;C183localTREE_ONLY_SUFFICIENT attribution,
not a repaired policy. C184reversible local-ID normalizer reproduces known inputs,
engineering contract rather than learned invariance. Original C182negative remains.
C185 connects learned necessity to handwritten sole-target mapping/C172/C173real IO
and reclassification with actual budgets11/4/step8 then7/3/step12,without resets.
Classification is not an answer/proof or ANSWERED terminal. All C185 attempts succeeded;
its synthetic fault tests did not establish learned behavior after non-admission.

## Active C186 — unchanged scientific design

C186-v5e-nonadmission-reclassification / V5-E-NONADMISSION-RECLASSIFICATION.
Question:retain correct NEEDS after no admissible information,while becoming SUFFICIENT
after successful observation. Same6C181checkpoints,source seeds181001/181002/181003,
both FINAL_ONLY/INTERNAL_SEMANTICS,plus MISSING_RULE/NEVER_QUERY controls.
No training/freshseed/teacher/auxhead/threshold/ensemble/answer/proof/retry.
Unchanged C185driver/target/inversebinding;C170/C184/C178/C179/C172/C173 paths.
ONLY provider return after a real file read changes:FOUND_ZERO,FOUND_ONE,NO_DELIVERY,
WRONG_VALUE(witness unchanged),PROVIDER_FAILURE. Faults are synthetic return-path
injections,not realistic timeout/OS-read failures or permission-withdrawal experiments.

All3712one-missing developmental rows(768needs/2944sufficient)x2layouts x5scenarios
x8policies=296960episodes/80blocks;111360candidate episodes,74240rule episodes.
56376static replays;222720live initial neural rows;postrows0..222720measured;
totalmax501816. 32successblocks replay C185 arrays/tolerance1e-6,rtol0;fault INITIAL
phases also match C185. Invalid replay/source/nonfinite/incomplete differs from a
finite model error on fault POST,which is scientific negative evidence.
Live budgets first11/4/step8,post7/3/step12;actualoutcomesNONE0/MISSING_DELIVERY4/
INVALID_EVIDENCE6 kept. Unadmitted information stays unknown,None,emptyreference.
No hidden zero/fact/label correction,no discarded cases. At mostONEattempt/TWOdecisions.
Raw NEEDS ends UNRESOLVED,no retry;falseSUFFICIENT remains scored.
Candidate expectations23040attempts/9216publications/13824nonadmissions/88320skips,
not forced behavior. Gate all3candidates zero failures,allpolicycontracts preserved.
MISSING_RULE3712calls/block/2944unnecessary and2944posterrors onfaultblocks;
NEVER_QUERY0calls/768missed perblock. FINAL_ONLYerrors remain descriptive.
13artifacts:plan,replay,results,compressedtraces,NPZplus8snapshots. Actual IO/inference
counts measured. No fullGateE,larger/repeated-variable/language/multitarget/durable claim.
Manifest`0cbe7212e5bafd9fc52f3f315d2d4732afaca6eb11940c6fa16ac58aeb336edc` unchanged.
Run tools/run_c186.ps1 with SAME11summaries and repairedExpectedHead; archive old log.
Use a new GUID output directory. Judge C186 ->ledger/handoff->next. **No C187 yet.**

## Migration / separate tracks

MonorepoC1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. Use standalone paths/Gitblob guards.
No reset/rebase/history rewrite/historical artifact commit_sha edit. GateE nine-family
contract remains unchanged;fullcandidate/baselines/splits/numerical preregistration
are still required. Multi-Axis/MA-1 and PC-ALM/FHLC remain SEPARATE research tracks.
