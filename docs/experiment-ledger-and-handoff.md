# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, sources and scientific preregistrations stay immutable.

## Environment / response protocol

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Standalone root paths fold_lm/,docs/,tests_lm/,tools/; no monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; `.venv-py31315\Scripts\python.exe`.
Diagnostic probes CPUfloat32/two threads; RTX4070TiSUPER installed.
Protected C37 runs/chatgpt-last-result.json SHA256:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected runs/fixtures/v05-c-composition-20260921.pt SHA256:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md, docs/experiment-conversation-handoff-protocol.md, this file,
docs/experiment-ledger-addendum-c186-c187.md and
**docs/experiment-ledger-addendum-c187-preregistration.md**.
Order: verdict, validity, metrics, interpretation, confounds, ledger, next design,
implementation/preregistration, reproducible PowerShell, progress, log collection, stop.

User clarification: do NOT split result acceptance and preparation of the next single
experiment into separate responses requiring another "continue" request. After judging
and saving the current experiment, complete the next design, implementation, available
validation, preregistration and runnable command IN THE SAME RESPONSE. A separate
acceptance commit is appropriate; a separate user turn is not required. Do not skip
judgment, execute an unregistered experiment or advance past the next unresolved C.
If blocked, state the concrete incomplete operation; never claim unperformed work.
The existing conversation protocol remains in force. Simple questions need no full template.
Never alter checkpoints, seeds, cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C186 ACCEPTED PASS. C187 ACTIVE / NOT YET JUDGED. C188 NOT REGISTERED.**
C186 acceptance986c4fc6497986fc025360cf15b2a20a8c01b1bd precedes C187 registration.
C185/C184/C183/C181 PASS; C182 VALID NEGATIVE. C180/C179/C178/C176 VALID NEGATIVE;
C174/C175/C177 scoped PASS; C170-C173 PASS; C160/C168/C169 VALID NEGATIVE.
All previous judgments and checkpoints remain unchanged. No C186 rerun or adoption.
C186 successful execution HEAD6e59bcbcdf84a37c4bece228b8163042cc6ac06a.
Earlier a4127d8a6bef0bf7eafd6e5d76fbb2061ab74eba attempt stays INVALID EXECUTION,
not a scientific negative or second success. Recovery changed input loading only.

## Latest accepted C186

1341/1341tests62.788s;NPZschema/source/artifactprecheckPASS;80blocks/296960episodes.
Each of3INTERNAL_SEMANTICS candidates:37120episodes,7680attempts,3072admissions,
4608nonadmissions,29440skips;zero initial/missed/unnecessary/post/contract errors.
Total111360candidate episodes,23040attempts,9216admissions,13824correct NEEDS after
nonadmission,88320skips. Three injected failures each4608candidate attempts,allcorrect.
All6C181checkpoints/source seeds181001/2/3;no training/freshseed/teacher/auxhead.
56376static replays/all6logitdelta0;32successful C185live blocks/alllogitdelta0.
222720live initial+42240post neural rows;321336total/360batches/2520cellcalls.
Allpolicies79360realreads,31744publications,47616nonadmissions,17459200readbytes.
Decisioncharges376320/internal614400. Allcontracterrors0.
Allpolicyfailed65436 entirely controls;false sufficiency after nonadmission236 belongs
ONLY to FINAL_ONLY (110/0/126 byseed), not candidate errors.
FINAL_ONLYfailed9310/9440/9566;MISSING_RULE29440;NEVER_QUERY7680.
92historicalpins/203protectedpaths/13artifacts;postcheckpreserved/clean/validTrue.
Reported284.694513s is not production latency;peakRAM/VRAM unmeasured.

Scope:fixed learned necessity -> handwritten unique target -> C172/C173actual read
and admission/rejection -> actual current evidence/resources -> raw reclassification.
Live first11/4/step8,post7/3/step12;unknown stays unknown after nonadmission,not0.
PROVIDER_FAILURE and successful admission both encode outcome0;facts differ.
No truth/threshold/proof override. ONEattempt/TWOdecisions is driver enforced,NOT
learned stopping/retry. No answers/proofs/network/coreEvidenceState/durable DB.
Faults injected AFTER read,not real OS-open failure/timeout simulation. Same4development
groups,not independent generalization. C187 tests the remaining initial authority boundary.

## Evidence / reviewer scope

C186 runs/c186-v5e-nonadmission-0d274f54409144cf83899758d020e82b/summary.json
SHA256e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82.
Uploaded log502259bytes SHA256bad2b41b59cc378d569b2368466b1554693780025250ac161ac66bf96d08816e.
Reconstructedsummary264136bytes/exacthash;80blocks,320grouptables/4480countervalues,
14totals,6static/32livereplays,strictgate and IO/resource arithmetic checked.
32successful blocks also compared with uploaded C185summary. Separate13artifacts,
fullNPZ/traces/checkpoints/data and1341tests NOT independently rerun by reviewer.
C186 NPZ4235987bytes SHA256dcd74467abd090a817998009318762e3ed613b84934f49100786177ea3ebd0cf.
Do NOT route through C175's generic32MiBloader. It is not materialized by C187.
C186's c186_c185_npz_input reader is ONLY for accepted C185 NPZ, not generic.

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

## Active C187 — semantic necessity despite execution restrictions

C187-v5e-restricted-acquisition-necessity / V5-E-RESTRICTED-ACQUISITION-NECESSITY.
Question:does NEEDS remain correct when acquisition cannot execute, and does unchanged
runtime block IO independently? Same C185driver/canonical-binding bridge, C170/C184/
C178/C179/C172/C173 paths and all6C181checkpoints/seeds181001/181002/181003.
No teacher/auxhead/training/newseed/threshold/answer/proof/retry or production changes.

Five conditions:ALLOWED_ZERO,ALLOWED_ONE,PERMISSION_DENIED,PROVIDER_UNAVAILABLE,
ACQUISITION_BUDGET_ZERO. Denials change exactly ONE initial numeric field67,64,63,
respectively. No expression/evidence/binding/clock change. Valid endpoints remain
configured in all conditions; runtime must prevent dispatch. No provider fault shim.
Initial resource11internal/step8 with actual changed field. Normal post7/3/step12;
denied post9internal/step10,acquisition4(or0),outcomes2/0/3. Denials reserve/read/publish0;
unknowns/references unchanged. No reset to training constants or fake observed0.
Raw NEEDS triggers handwritten sole-target proposal even if impossible to authorize:
semantic necessity is NOT an executable-permission decision. MaxONEproposal/TWOdecisions
and unresolved termination enforced by driver,not learned retry/alternative policy.

ALL3712one-missing development rows768NEEDS/2944SUFFICIENT x2layouts x5conditions
x8policies=296960episodes/80blocks. Candidate111360episodes;rule74240episodes.
Expected correct candidates23040proposals,9216normal reads/admissions,13824denied
proposals,88320skips. Counts are expectations,not forced action scripts.
All3candidates/all37120episodes each must havezero initial/post/contract failures.
Allpolicies preserve contracts. MISSING_RULE3712proposals/block,2944unnecessary;
restrictedpost2944errors. NEVER_QUERY0proposals/768misses/block. FINAL_ONLY descriptive.

56376static replayrows.32normal liveblocks replay C185 via accepted schema-bound
loader;exact inputs/argmax,logitsabsdiff<=1e-6,rtol0. EVERY first packet differs from
C185 at only its registered runtime coordinate. Restricted output changes are measured,
not replay failures. Neural initial222720,post0..222720actual,totalupperbound501816.
C186NPZ hash/size checked without allocation.99historicalpins/221protectedpaths plus
outerC37/fixture.13outputs:plan,replay,results,gziptraces,NPZ,8sameC185sourcefiles.
Per-block actual reads and post states measured;group errors and input-context decision
flips saved in the same batch. Future NPZ readers must inspect expanded shape sizes.
ManifestSHA256e6b3c94a9c36bdf9e15333320a95f81f295baf1b6cda956e11c549e1ec89262e.
Finite failures -> VALID NEGATIVE;source/schema/nonfinite/unchanged-replay/protection/
incomplete errors -> SAMEC187 execution recovery. Preserve all earlier results.

36/36new helper tests PASS on complete new module with SYNTHETICdataclasses/packets/
NumPyarrays. Not C185/C172/C173 integration or official checkpoint evaluation. Source
review checks denial reasons/debits and coordinates. No complete local checkout;
git DNS unavailable. Two Python files compile/three embedded Python blocks parse,
not WindowsPS execution. Full1377tests/221inputchain/official296960episodes UNEXECUTED.
**1377expected=1341+36;72modules.** Run tools/run_c187.ps1 with twelve summaries
C186/C185/C184/C183/C182/C181/C180/C179/C178/C177/C176/C174 and exactExpectedHead.
Progress:sourceprecheck,1377tests,56376staticreplays,blocks1/80..80/80,RESULT,POSTCHECK.
JudgeC187 ->ledger/handoff->next prepared single experiment IN SAME RESPONSE.
**C188 NOT REGISTERED; no C188 before C187 judgment.**

## Accepted chain / limits / separate tracks

Latest acceptance c186-c187;then c185-c186,c184-c185,c183-c184,c182-c183,c181-c182 and
older addenda. Previous handoff986c4fc6497986fc025360cf15b2a20a8c01b1bd preserves
acceptance-only state. C186execution-recovery records32MiBloader failure/shape-bound fix.
C151perlayout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9knownerrorsretained.
C152-C167 original authority/acquisition/recovery scopes retained. C17072fields;
C171handwritten proofchecker;C172reservation;C173scripted actual acquisition.
TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows,development only.
C174syntax/C175frequencyreference scopedPASS;C176negative/C177smallAUC notadoption;
C178binding/C179tree/C180bypass negative. C181proper-node TRAINsupervision0errors on
9396pilot+42444TRAIN per3candidates;additional information,not unique mechanism proof.
C182oneerror/648324renamedpredictions;C183localTREE_ONLY_SUFFICIENT attribution;
C184reversible local-ID normalization engineering contract,not learned invariance.
C185all44544candidate successful-acquisition episodescorrect;C186extends to nonadmission.
No natural-language,larger/repeated-variable,multitarget,learnedtool/answer/proof claim.
GateE fullcandidate/baselines/splits/numerical contract still required.
Multi-Axis/MA-1 and PC-ALM/FHLC remain SEPARATE tracks. No scope creep to later gates.
MonorepoC1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
No reset/rebase/historyrewrite/historical artifact commit_sha edit.
