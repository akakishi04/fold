# FOLD experiment ledger and handoff

Updated: 2026-11-26 Japan time.
Conversation protocol:docs/experiment-conversation-handoff-protocol.md,Current response format v2.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C346 ACCEPTED VALID NEGATIVE.** Valid C346-R0 execution,candidate_gate=false/eligible_seed_count=0.
C346 attempt01 remains INVALID;documentation recovery1 preserved the original scientific conditions.
C345 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY);C344 remains ACCEPTED VALID NEGATIVE.
No production adoption or broader capability improvement.
**C347 ACTIVE / NOT YET JUDGED.** Saved-only loss/correctness-transition diagnostic.
C348 NOT REGISTERED. Do not rerun accepted C344/C345/C346.

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

## C347 registration and independent review

Experiment:C347-v5b-saved-loss-transition.
Stage:V5-B-SAVED-LOSS-TRANSITION.
Acceptance commit:c0597bbc24ca3db2761763b65cfe8521af7d1b2e.
Reviewed source commit:3f34750492c065ca9185517bd2e9e8f8b8865464.
post_authoring_review = PASS
post_authoring_review_target = 3f34750492c065ca9185517bd2e9e8f8b8865464
Review status:committed-byte/static review PASS; runtime gate pending.
Review:docs/c347-post-authoring-review.md.
Preregistration:docs/experiment-ledger-addendum-c347-preregistration.md.
Manifest:8e85821c7d4e69c49cd0695ccb5126a7dbb8b5cc0f5b9ca77f5fb0cd98a0aee3.

Use the documentation-only activation HEAD that contains this handoff as the
ExpectedHead on feat/sft-target-loss. Do not use the source-only registration,
C346 execution/publication/acceptance or main merge HEAD. The short user block
must parse tools/invoke_active_v2.ps1 before invoking it; the dispatcher parses
the selected C347 launcher. All seven OWN blobs remain identical to reviewed source.

Author tests:72/72 normal PASS43.184146s and72/72 CP932-default-text-open simulation
PASS43.333929s; failure/error/skip/expected-failure/unexpected-success all0.
Actual loader:6725 raw candidates,6724 selected IDs/245modules; OWN40science+32execution.
Full ordered ID SHA:28b5c7fc80732b94cdb32f94f241cc142dff3e9da0dc68fdba26ded270ffef58.
Parent6652IDs/243groups are the exact ordered prefix, SHA
39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Sole exclusion remains the inherited C204 test33; no new exclusion or parent edits.
Four Python files compile/import/pyflakes PASS;324code objects/2271global loads,
undefined globals0. Actual PowerShell7.5.4 parsed dispatcher/invoke/runner,errors0;
an executed fixture proves native Validate failure calls neither runner nor publisher.
These are software checks. Native Windows full regression and C347 diagnostic
remain pending; do not treat author fixtures as a formal C347 result.

## C347 one question and fixed scientific boundary

Which matched correctness groups account for lower terminal loss coexisting with
worse exact answers or both-query-correct pairs under C346's half-rate policy?
Use all15saved states, all5seeds346001..346005,3arms,6domains,2splits,3profiles and
both languages. Compare pair_max_half_rate with both pair_max and mean_ce across
all120 coordinates. Full256 first-index argmax and canonical metadata pairs remain fixed.

Retain77760 normal answers/38880pairs and51840matched answers/25920matched pairs.
For each comparison decompose answer correctness(CC/CW/WC/WW),both-query correctness
and same-answer-collapse transitions. Each partition has480explicit groups in total.
Pair W includes one-correct pairs; distinct predictions do not imply correct answers.
Groups retain signed loss sums/means/extrema and contributions using the full
comparison denominator. Empty groups have zero sums/contributions and null means/extrema.
Each partition separately reproduces parent losses and exact rescue/regression counts.
Never add the three overlapping partition families or call them independent samples.

Trace final-state hashes bind the saved logits; there is no trajectory/norm audit.
Cross-arm terminal changes are not temporal learned/forgotten events. No new fitting,
forward,backward,optimizer update,model-state load,new checkpoint or network call.
Archive deserialization is measured separately:1evaluation bundle/1trace JSON per
child computation or reconstruction pass. Parent validation and separate reconstruction
passes are additional reads; historical regression fixtures may perform their own work.

PASS means complete diagnostic integrity only, with all180parent terminal records
and120contrasts bound. C346 candidate_gate=false/eligible0 and all subgates remain
unchanged. No desired-sign gate, rate selection, causal optimizer/convergence/
undertraining/calibration claim or capability promotion. Gate F remains NOT PASSED.

## C347 native Validate, Execute and retention

Reuse .venv-py31315:Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5,CPUfloat64/threads2.
No environment upgrade. Run prefix:runs/c347-saved-loss-transition-<id>/.
Execution revision:C347-R0;accepted timeout cleanup implementation:C344-R1.
The parent is trained C346 with FAIL/valid execution, not diagnostic C345 or INVALID attempt01.

Validate is operational and precedes formal logging/publication. It performs owned
compile/import,native runtime,six cleanup cases,locked parent/source reconstruction,
all6724tests/245isolated modules,complete proof verification and9681uncached input rereads.
It closes validation.log before writing validation-receipt.json. The receipt binds
canonical run folder,HEAD,manifest,source/input maps,runtime,parent,cleanup,compile/import,
full regression and closed transcript bytes. Failed Validate prints
AUTHORING_RUNTIME_PREFLIGHT_FAILED/experiment_executed=False/publish_attempted=False;
it does not replace latest.log/json. Branch/tree/HEAD/ACTIVE guards are checked again.

Execute copies the successful validation text into the formal log, verifies the
bound validation/proof set under leases, performs the diagnostic and saved reconstruction,
and completes final rereads. The complete regression runs once in Validate,zero times
in Execute. The separate fresh verifier repeats all proof/byte/semantic bindings.
Formal output reports the reused receipt/log/closure hashes. No automatic retry.

Protection:951sources=944+7;9681inputs=9177+497parent outputs+7.
Preserve all497C346 outputs. C347 has493regression proof files(3+245JSON/log pairs),
plus validation-receipt.json/validation.log:495separately leased validation outputs.
The successor-retained contract is501files:495validation/proofs+4science+primary+envelope.
Auxiliary process transcripts and the outer console log are outside that required count.
Four science outputs:audit-plan.json,normal-pair-observations.json,
loss-transition-decomposition.json,validation-summary.json.
Primary:fold-c347-diagnostic-v1;envelope:fold-c347-execution-envelope-v1.

## Inherited regression compatibility seals

Append-only historical provenance,not current ACTIVE state. Retain this section whenever
the handoff is rewritten while the inherited pinned tests remain in the regression.
The accepted C273 preflight recovery and docs/experiment-authoring-runtime-gate.md
(Mutable handoff lifecycle rule) require this specific legacy marker permanently.
C273..C278 also assert it. Do not delete it during later acceptance or activation edits.
C272manifest seal:89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.


## Historical context and stop

docs/handoff-history/c347-pre-activation.md preserves the exact accepted-C346,
unregistered-C347 handoff. Earlier attempt01/recovery archives remain unchanged.
docs/cross-experiment-evidence-synthesis-2026-11-22.md and its JSON index remain
historical C344-bounded snapshots; C345/C346 acceptance addenda provide subsequent evidence.

Before delivering the launcher, verify the final activation's eleven C272..C282
handoff consumers and the actual C347 guard; retain the permanent legacy seal.
Freeze feat/sft-target-loss while the user runs C347. On completion fetch remote
docs/experiment-run-logs/c347/latest.json and latest.log; distinguish scientific
execution HEAD from log publication. On a preflight SKIPPED repair C347 only.
On execution integrity failure preserve the attempt and retry SAME C347 only.
Transport failure does not justify a scientific rerun. C348 is not registered.
