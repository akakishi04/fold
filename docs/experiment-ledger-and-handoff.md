# FOLD Experiment Ledger and Handoff

> Authoritative state. Historical evidence, source and preregistrations remain immutable.

## Environment / protocol

Repository akakishi04/fold (standalone); branch feat/sft-target-loss; local M:\asobiba\fold.
Root-relative fold_lm/,docs/,tests_lm/,tools/; no monorepo fold/ prefix.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; .venv-py31315\Scripts\python.exe.
Current diagnostic probes CPUfloat32/two threads; RTX4070TiSUPER installed.
Protected C37 runs/chatgpt-last-result.json:
FD4A8DA897BDAEA9D103A252E30212C7FF842D23300D7C837333E146DEE51931.
Protected fixture runs/fixtures/v05-c-composition-20260921.pt:
A52F8209703149407580F7E2965B61B78653030EE992AF6D759865736741CA9E.
Read AGENTS.md,docs/experiment-conversation-handoff-protocol.md,this file,
docs/experiment-ledger-addendum-c184-c185.md and
**docs/experiment-ledger-addendum-c185-preregistration.md**.
Order:verdict,validity,metrics,interpretation,confounds,ledger,next design.
Preserve valid negatives;never change checkpoints,seeds,cases or thresholds to obtain PASS.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;**Gate E NOT PASSED**.
**C184 ACCEPTED PASS. C185 ACTIVE / NOT YET JUDGED. C186 NOT REGISTERED.**
C184 acceptance08ac8ef47b917a34d54dd1d84ac1ede41b2f88d6 PRECEDES C185 registration.
C183 ACCEPTED PASS;C182 ACCEPTED VALID NEGATIVE;C181 ACCEPTED PASS.
C180/C179/C178/C176 remain VALID NEGATIVE;C174/C175/C177 retain scoped PASS.
C170-C173 PASS;C160/C168/C169 VALID NEGATIVE. All earlier judgments unchanged.
C184 executionHEAD4d07e9e5190487fdcc9cb68f7204381e5ea5ab67.
No C184 rerun,no checkpoint change or production adoption. Use final C185 registration HEAD.

## Accepted chain / scope

Latest accepted detail:docs/experiment-ledger-addendum-c184-c185.md,then c183-c184.md,
c182-c183.md,c181-c182.md and earlier chained addenda.
Previous handoff at08ac8ef47b917a34d54dd1d84ac1ede41b2f88d6 retains C184 acceptance state.
C151 per layout WITHIN_FACTOR20727/20736,GLOBAL_CONCEPT20736/20736;9known errors unchanged.
C152-C167 retain original acquisition/authority/recovery/warm scopes.
C170transports72fields;C171handwritten bounded proof checker;C172reserves typed actions;
C173scripted local acquisition/admission/proofs,not autonomous target selection/durable memory.
Data TRAIN36groups/524templates/42444rows;PILOT4groups/116templates/9396rows.
Repeatedly inspected pilot is DEVELOPMENT,not independent confirmation.
C174syntax MLP beats blind control;C175beats TRAIN-frequency reference.
C176loss weighting fails;C177small AUC gains do not adopt it.
C178binding/C179tree/C180bypass removal fail their joint comparisons.
C181proper-node auxiliary supervision:all3internalmodels correct on9396pilot+42444TRAIN
rows each;no teacher/head at inference. Real extra TRAIN information,not unique mechanism proof.
C182renaming fails strict invariance:one candidate error/648324predictions,seed181003,perm17.
C183localizes that error to TREE_ONLY_SUFFICIENT;direct fact path partly counteracts it.
Original F1 AND(F2 AND(NOT F3 AND NOT F4)),facts1,1,unknown,0;source_row41788.
Margins ORIGINAL5.9391820431,RENAMED-.0096115172,TREE_ONLY-.1055186987,DIRECT_ONLY6.0350892544.
The hybrids are internal counterfactuals,not legal full tasks or a corrected policy.

## Latest accepted C184

1249/1249tests58.614s;source/artifactprecheckPASS;postcheckpreserved/clean/validTrue.
24normalizationgroups:51840original+23*9396renamed=267948rows.
All96canonical/roundtrip/idempotence/input-mutation counters0.
535896normalizerrowcalls including idempotence;267948inverse reconstructions.
All6frozen C181checkpoints;no freshseeds/training/teacher/auxhead.
311040identityreplaypredictions;all12replays decisions identical and logitdelta0.
1296648normalizedpredictions/all138model-permutationcells;allflips0/logitdelta0.
INTERNAL_SEMANTICS:216108/216108correct each;total648324/648324,errors0.
FINAL_ONLY retains2459/2429/2411errors perpermutation;56557/55867/55453total,not repaired.
Total1607688inference rows/1692batches/11844cells;checkpointloads6.
84historicalpins,172protectedpaths,5outputartifacts. Acquisition/proof/evidence/network0.
ProductionmodifiedFalse;GateEcandidateFalse. Reported69.212859s not a latency claim.

Interpretation:handwritten first-occurrence normalization of LOCAL arbitrary slot IDs,
whole numeric records preserved with inverse map. No logical evaluation/hidden values.
Identical canonical inputs imply known outputs by construction. Engineering contract,
NOT new learned invariance/semantic generalization. C182negative stays unchanged.
Scope4distinct facts/7nodes/read-once/observed-unobserved. External identities not renamed.
Full PolicyInput binding-sidecar/action remapping and learned acquisition loop untested by C184.
Stop repeated unchanged-score/naming diagnostics;C185 addresses the live integration boundary.

## Evidence / independent verification

C184 runs/c184-v5e-canonical-indices-5e2a159b64164b3a919762ebdbdc4f90/summary.json
SHA2567817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04.
Uploadedlog284056bytes,SHA256990ed33e89fc66cdc539b09e3397392b22020514fc9cccba00cdaf2bd3931729.
Reconstructedsummary72652bytes;24checks/96counters,138records,12replays,workload/gate verified.
Repeated uploaded copies are the SAME execution,not independent successes.
Separate5artifact/checkpoint/data bytes and1249tests NOT independently replayed.
No confusion tables in summary;do NOT claim normalized-results detail was reaggregated.
C183 runs/c183-v5e-path-attribution-b806a83c1a4044538713b844fe640198/summary.json
SHA256ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24.
C182 runs/c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4/summary.json
SHA25606c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73.
C181 runs/c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad/summary.json
SHA256bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98.
C180/C179/C178/C177/C176/C174 paths and hashes remain in prior addenda and runners.
DataSHA256eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
Retain all past artifacts/checkpoints;summary arithmetic is not model replay.

## Active C185 — learned trigger / real acquisition / live reclassification

C185-v5e-learned-single-missing-acquisition / V5-E-LEARNED-SINGLE-MISSING-ACQUISITION.
One question:do frozen necessity decisions correctly control bounded real acquisition
and subsequent reclassification,without resetting actual resource/evidence inputs?
All6C181checkpoints,seeds181001/2/3,baseonly25726parameters,full25921fingerprint checked.
No training/freshseed/teacher/auxiliary head/answer/proof/network/coreEvidenceState writer.
Two handwritten controls:MISSING_RULE and NEVER_QUERY. No checkpoint selection.

C170encode + C184numeric normalizer + matching opaque Binding relocation/inverse check.
External fact IDs/references remain original;source-view digest prevents stale map use.
Model sees numeric input only. Handwritten target=sole unknown;tool=RETRIEVE only.
C172reserves,C173actuallyreads/publishes,then SAME frozen model sees new current state.
Output SUFFICIENT_CLASSIFICATION is not an answer/verified conclusion/ANSWERED terminal.
At most two classification decisions,one acquisition attempt per independent owner;
remaining NEEDS ends UNRESOLVED,not another attempt. Wrong outputs never corrected.

Cohort ALL3712PILOTrows with one unknown,768NEEDS/2944SUFFICIENT;selection by visibility,
not labels/margins. Identity+reverse layouts;both completions0/1,identical initial data.
8policies x2layouts x2completions x3712 =118784episodes/32blocks;
89088model episodes,44544candidate episodes,29696rule episodes.
Original9396PILOT replay for all6 =56376predictions;exactargmax,logitabsdiff<=1e-6,rtol0.
Live initial neural rows89088;post rows0..89088depend on RAW decisions;totalmax234552.
Actual matrices/batches/seven-cell calls/readbytes/reservations/publications are metered.
Expected correct candidates:9216acquisitions and35328no-acquisitions,not forced counts.
MISSING_RULE14848reads/11776unnecessary;NEVER_QUERY0reads/3072missed. Baseline costs explicit.
Eight registered tiny files,one target record each;runtime only,not hidden inputs.
Setup/hashing IO is additional to provider read meters;no zero-total-IO claim.

Resources start from actualC17412internal/4acquisition/step7. Each decision is charged1
BEFORE encoding through trusted owner.refresh. First model input11/4/step8;normal
post input7/3/step12 after reservation1+dispatch2+seconddecision1. Budget changes remain
visible;this is a new runtime context,not source replay. Do not clamp to TRAIN constants.

Gate:all3INTERNAL_SEMANTICS candidates,all14848episodes each,zero initial/missed/unneeded/
post/contract failures. Controls retain errors but all must preserve contracts;two rule
patterns fixed. Finite failure VALID NEGATIVE;source/schema/replay/nonfinite/unfinished/
protection issue INVALID,restore SAME C185 validity. Keep complete outputs,never tune.
Development groups repeatedly reused,not independent semantics/language/general Gate E.

88historicalpins,182protectedpaths plusouterC37/fixture;13artifacts excluding summary:
plan,replay,episode-results,JSONLgziptraces,NPZinputs/logits/decisions plus8snapshotfiles.
NPZ missing decisions-1;logit_present distinguishes absent/rule logits from real scores.
Manifest61563a16d40883db8f2f651e440ae4704d5ef8f36115aca28f9bade64d3d6385.
36helpertestsPASS on actual new module +4Git-blob-identical typed runtime modules;
localC184support has fetched adapter definitions,notfullcheckout;policies SYNTHETIC.
Actual tiny-file IO/admission,24bindingmaps,livecounter/noreset,denial and no-retry covered.
Full1285regression/WindowsPS/182inputchain/officialcheckpoints/118784episodes UNEXECUTED.
TwoPythonfilescompile,threeembeddedPythonblocksparse;no PowerShell execution.
**1285expected=1249+36;69modules.** Run tools/run_c185.ps1 withC184/C183/C182/C181/C180/
C179/C178/C177/C176/C174summaries andExpectedHead. Progress56376replay,blocks1/32..32/32,
RESULT/POSTCHECK. Judge C185 ->ledger/handoff->next design;C186 NOT REGISTERED.

## Migration / project limits

Monorepo C1745e05168e maps to standalone19603c7267;C173source2cc2b1f4 maps to61c78906.
d011b139runner-only migration fix enabled C174. New guards use standalone paths/Gitblob pins.
No reset,rebase,history rewrite or historical artifact commit_sha modification.
Gate E nine-family contract unchanged;final assessment requires full candidate,baselines,
splits,numerical preregistration. Multi-Axis/MA-1 and PC-ALM/FHLC remain SEPARATE tracks.
No language,Vision,long-context,durable-memory,latency/VRAM claim. No C186 registration yet.
