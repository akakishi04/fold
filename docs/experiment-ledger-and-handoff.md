# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence,sources and scientific preregistrations stay immutable.

## Environment / protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Standalone root paths fold_lm/,docs/,tests_lm/,tools/; no monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Diagnostic probes CPUfloat32/two threads; RTX4070TiSUPER installed.
Protected C37 runs/chatgpt-last-result.json SHA256:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected runs/fixtures/v05-c-composition-20260921.pt SHA256:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
**docs/experiment-ledger-addendum-c186-c187.md** and C186 preregistration/recovery addendum.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Never alter checkpoints,seeds,cases or thresholds to obtain PASS.

## Formal state

GateA/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C186 ACCEPTED PASS. No active experiment. C187 NOT REGISTERED.**
C185/C184/C183/C181 PASS;C182 VALID NEGATIVE. C180/C179/C178/C176 VALID NEGATIVE;
C174/C175/C177 scoped PASS;C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier
judgments remain. No C186 rerun,checkpoint replacement or production adoption.
C186 successful execution HEAD6e59bcbcdf84a37c4bece228b8163042cc6ac06a.
Earlier a4127d8a6bef0bf7eafd6e5d76fbb2061ab74eba attempt stays INVALID EXECUTION,
not a scientific negative or second success. Recovery changed input loading only.

## Latest accepted C186

1341/1341tests62.788s;NPZschema/source/artifactprecheckPASS;80blocks/296960episodes.
Each3INTERNAL_SEMANTICS candidates:37120episodes,7680attempts,3072admissions,
4608nonadmissions,29440skips;zero initial/missed/unnecessary/post/contract errors.
Totals111360candidate episodes,23040attempts,9216admissions,13824correct NEEDS after
nonadmission,88320skips. Three injected failures each4608candidate attempts,allcorrect.
All6C181checkpoints/source seeds181001/2/3;no training/freshseed/teacher/auxhead.
56376static replays/all6logitdelta0;32successful C185live blocks/alllogitdelta0.
222720live initial+42240post neural rows;321336total/360batches/2520cellcalls.
Allpolicies79360realreads,31744publications,47616nonadmissions,17459200readbytes.
Decisioncharges376320/internal614400. Allcontracterrors0.
Allpolicyfailed65436 entirely controls;false sufficiency after nonadmission236 belongs
ONLY to FINAL_ONLY (110/0/126 byseed). Do not label those236 candidate errors.
FINAL_ONLYfailed9310/9440/9566;MISSING_RULE29440;NEVER_QUERY7680.
92historicalpins/203protectedpaths/13artifacts;postcheckpreserved/clean/validTrue.
Reported284.694513s is not a production latency measurement;peakRAM/VRAM unmeasured.

Scope:fixed learned necessity -> handwritten unique target -> C172/C173actual read
and admission/rejection -> actual current evidence/resources -> raw reclassification.
Live first11/4/step8,post7/3/step12;unknown stays unknown after nonadmission,not0.
PROVIDER_FAILURE and successful admission both encode outcome0;facts differ.
No truth/threshold/proof override. At mostONEattempt/TWOdecisions is driver enforced,
NOT learned stopping/retry. No answers/proofs/network/coreEvidenceState/durable DB.
Faults injected AFTER read,not real OS-open failure/timeout simulation. Same4development
groups,not independent generalization. Permission denial/unavailable/zero acquisition
budget with these learned models remains unmeasured;this is the next proposed boundary.

## Evidence / reviewer scope

C186 runs/c186-v5e-nonadmission-0d274f54409144cf83899758d020e82b/summary.json
SHA256e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82.
Uploaded log502259bytes SHA256bad2b41b59cc378d569b2368466b1554693780025250ac161ac66bf96d08816e.
Reconstructedsummary264136bytes/exacthash;80blocks,320grouptables/4480countervalues,
14totals,6static/32livereplays,strictgate and IO/resource arithmetic independently checked.
32successful blocks also compared with uploaded C185summary. Separate13artifacts,
fullNPZ/traces/checkpoints/data and1341tests NOT independently rerun by reviewer.
C186 NPZ4235987bytes SHA256dcd74467abd090a817998009318762e3ed613b84934f49100786177ea3ebd0cf.
It is larger when expanded:do NOT route through C175's generic32MiBloader unexamined.
C186's specific c186_c185_npz_input reader is ONLY for accepted C185 NPZ,not generic.

C185 runs/c185-v5e-single-missing-acquisition-72d30a1a4e114de5b981352de26055e6/summary.json
SHA256843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949.
C185 NPZ1716066bytes SHA256e597baf0dfa76b34a32dcb2a0445640aaeb21bb99a22af25c26c854ef3eabcf8.
C184 runs/c184-v5e-canonical-indices-5e2a159b64164b3a919762ebdbdc4f90/summary.json
SHA2567817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04.
C183 runs/c183-v5e-path-attribution-b806a83c1a4044538713b844fe640198/summary.json
SHA256ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24.
C182 runs/c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4/summary.json
SHA25606c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73.
C181 runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json
SHA256bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98.
C180/C179/C178/C177/C176/C174paths/hashes remain in previous addenda/runners.
DatasetSHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.

## Accepted chain / limits

Latest detail c186-c187;then c185-c186,c184-c185,c183-c184,c182-c183,c181-c182 and earlier.
C186execution-recovery addendum records32MiBloader failure and schema-bound repair.
Full previous handoff at6e59bcbcdf84a37c4bece228b8163042cc6ac06a preserves original retry.
C151perlayout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9knownerrorsunchanged.
C152-C167 original authority/acquisition/recovery scopes retained.
C17072fields;C171handwritten proofchecker;C172reservation;C173scripted actual acquisition.
TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Repeatedly inspected PILOT is DEVELOPMENT,not independent final confirmation.
C174syntax helps/C175beats frequency;C176weighting negative/C177smallAUC not adoption;
C178binding/C179tree/C180bypass negative. C181proper-node TRAINsupervision gives0errors
on9396pilot+42444TRAIN per3candidates;extra training information,not unique mechanism proof.
C182oneerror/648324renamedpredictions;C183localTREE_ONLY_SUFFICIENT attribution;
C184reversible local-ID normalization engineering contract,not learned invariance.
C185all44544candidate live episodescorrect,but all attempted deliveries succeeded.
C186adds frozen-model nonadmission evidence,without rewriting C185or historical negatives.
No natural-language,larger/repeated-variable,multitarget,learnedtool/answer/proof claim.

## Next design / separate tracks

Proposed next question:does semantic NEEDS stay correct when acquisition cannot be
executed due to permission,availability or acquisition-budget restrictions,and does
unchanged runtime independently prevent IO? Not registered;no next run command yet.
Freeze models/cases/thresholds. Do not silently clamp resource context to training values.
NoC187execution until separate preregistration. GateEfullcandidate/baselines/splits/
numerical contract required. Multi-Axis/MA-1 and PC-ALM/FHLC stay SEPARATE research tracks.
MonorepoC1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
No reset/rebase/historyrewrite/historical artifact commit_sha edit.
