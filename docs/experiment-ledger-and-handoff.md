# FOLD experiment ledger and handoff

Updated: 2026-11-26 Japan time.
Conversation protocol:docs/experiment-conversation-handoff-protocol.md,Current response format v2.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C346 ACCEPTED VALID NEGATIVE.** Valid C346-R0 execution,candidate_gate=false/eligible_seed_count=0.
C346 attempt01 remains INVALID;documentation recovery1 preserved the original scientific conditions.
C345 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY);C344 remains ACCEPTED VALID NEGATIVE.
No production adoption or broader capability improvement.
C347 NOT REGISTERED. C348 NOT REGISTERED. Do not rerun accepted C344/C345/C346.

## Latest accepted evidence

Report:docs/experiment-ledger-addendum-c346-c347.md.
Scientific execution:622e623faa0c3c698a18033eb8b4bca554088918.
Publication:426c52f9f33f2465e8b1cd1879182558b443f660;soleparent execution,onlylatest.log/json.
Original Windows620183bytes/SHA256ede8f82041571f5481eeaa1dfbbc22c395ad71df0d67b73cd2decf118a2ee338.
Git LF615757bytes/4426LF reconstructs original exactly.
Manifest:8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64.
All7OWN blobs remain identical to sourcebe76c4c53c36105638e59e059af241078758b628.

Full6652tests/243modules PASS3340.151s;failures/errors/skips0;all246process exits0.
Actual full ID plan and all243module begin/complete/count/topology records match.
FullID SHA39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Parent6578IDs exactorderedprefix/SHA2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Sixcleanupchecks PASS with C344-R1implementation receipt bound tothisC346HEAD.
Native locks,parentsemantics,objectivepreflight,944sources/9177inputs passed.
All15fits reached2400updates beforeevaluation;all15saved states evaluated/replayed.
Scientific WORK36000updates/backwards,1728000trainingrows,41130forwards,
2220480totalrows,164520corecalls,82260querycalls,15optimizers,30stateloads,
1checkpointbundleload/1newbundlewrite/network0.
All9177finaluncachedrereads and separatefreshverifier complete;run_execution_valid=true.

Public validation-summary reconstructed and checked with pinnedC346check_summary.
Canonical reconstructedSHA16768a9a7994d8f9e6c4f7202a886c1bbf77422364e0a05f8c0a00b52d488325.
Integrityflags/rawsemanticreplay/individualsuccessfulIDproofs are nativeverifier attestations.
Reviewers did not fetch user-native tensors,fullprimary/envelope,source/inputmaps or moduleJSONs.
Do not claim independent reconstruction of unpublished primary/envelope bytes.

## Scientific result and interpretation

Full original+interior gates:meanCE2/5,defaultpairmax1/5,half-ratepairmax0/5.
Half-ratecandidate interior0/5 andoriginal6gate0/5;eligible0/5.
Nonnegativeanswer/pair inequalities68/120vdefaultpairmax,64/120vmeanCE;bothfail.
Fourstrictinterior gainsvdefault:TRAINanswers-217/pairs-209,HOLDOUTanswers-170/pairs-120.
Positiveprimaryheadroom:TRAIN409answers/404pairs,HOLDOUT252answers/204pairs;notaceilingfailure.

InteriorTRAINanswers:2824/2880meanCE,2471defaultpairmax,2254halfrate.
InteriorHOLDOUTanswers:1395/1440meanCE,1188defaultpairmax,1018halfrate.
InteriorTRAINbothquerypairs:1384/1440,1036,827;HOLDOUT683/720,516,396.
Half-rate answersworsein4/5seedseachsplit vdefault;346002improvespartlyfromseveredeterioration.
Default346002HOLDOUT all6domains108/288answers and0/144bothquerypairs.
Half-rateinterioranswersbelowmeanCEfor all5seedseachsplit.
Original6pooledanswersimprovevdefault butfailthefixedretentiongate andremainbelowmeanCE.

InteriorHOLDOUT meanCE loss .993879073->.786599756 andpairmax1.774960732->1.224536909
(defaultpairmax->halfrate),despite170feweranswers/120fewerbothquerypairs.
346001interiorHOLDOUTalsohaslowerbothlossesbut47feweranswers/36fewerpairs.
TRAINinteriorbothlossesincreaseinaggregate. Lossandexactcorrectnessarenotinterchangeable.
Lossmeansarewithin-domain/split,notwholemixtureexposureweightedtrainingobjectives.
No provenconvergence,undertraining,clippingcause,gradientstarvation,capacitylimit oroptimalrate.
Nohalf-rateCEarm,so noobjective-by-ratefactorialclaim. DonotpoolC344/C346aspairedcohorts.

## Preserve accepted C346 artifacts

Folder:runs/c346-pair-max-rate-68993e9eaa4e410886dbe0d24a3def3c/.
Primaryscience/summary.json:d06fa2a06287696424ac58e3d56e7262282caca81b028f61709f609ab728e816.
Envelope:b8b57583363d61aca10d947c891de0d8b3d8b2319e659652cacf101a334e3c3d.
Trainedprimaryschema:fold-c346-trained-v1;executionenvelope:fold-c346-execution-envelope-v1.
Keep497outputs:6science+primary+envelope+489proofs(3+243JSON/logpairs).
Do not substitute C345diagnostic schema or C346attempt01 identity.

## Next one question, before registration

C347proposal(stageV5-B):whichmatchedcorrectnessgroupsaccountforlowerterminalloss
coexistingwithworseexactanswers/querypairsunderthefixedhalf-ratepolicy?
Saved-onlyloss/correctness-transitiondecomposition,all15C346states,all5seeds,
6domains,2splits,bothcontrols. Canonicalmetadataquerypairs/full256savedlogits.
Allgroupsretained,includingexplicitemptygroups;no modelorcase selection.
Cross-armterminalcorrectnesscomparison isnot atemporallearningtrajectory.
Diagnosticintegrityonly;C346false/eligible0andallsubgatesremainfixed.
No newtraining,forward,gradient,optimizerupdate,model-stateload orcheckpointwrite.
Source/tests/executor/launchers/preregistration andindependentcommittedremotereview
mustcompletebefore C347activation orusercommand. Thisacceptanceisnotregistration.

## Inherited regression compatibility seals

Append-only historical provenance,not current ACTIVE state. Retain this section whenever
the handoff is rewritten while the inherited pinned tests remain in the regression.
The accepted C273 preflight recovery and docs/experiment-authoring-runtime-gate.md
(Mutable handoff lifecycle rule) require this specific legacy marker permanently.
C273..C278 also assert it. Do not delete it during later acceptance or activation edits.
C272manifest seal:89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.


## Historical context and stop

docs/handoff-history/c346-pre-acceptance.md retains theexactC346recoveryhandoff.
docs/c346-recovery-r1.md and docs/c346-r1-post-authoring-review.md retain recovery1.
docs/experiment-run-logs/c346/attempt-01/latest.log and latest.json retain INVALID attempt01.
docs/experiment-ledger-addendum-c345-c346.md retains acceptedC345diagnostic.
docs/cross-experiment-evidence-synthesis-2026-11-22.md and itsJSONindex remain
unchangedhistoricalC344-bounded snapshots;theC345/C346acceptancereports provideupdates.

Before anynewactivation,run actualinheritedC272..C282handoffconsumers againstfinaldocumentbytes,
checkuniqueACTIVEseparately,andpreservethepermanentC272compatibilityseal.
If a futureexecutionisINVALID,repairSAMEC only;donotadvancetheCnumber.
Logtransportfailuredoesnotjustifyretraining. Preserveusernativeartifacts.
