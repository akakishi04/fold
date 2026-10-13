# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C321 ACCEPTED VALID NEGATIVE. C322 ACTIVE / NOT YET JUDGED. C323 NOT REGISTERED.**
C322 is the unique ACTIVE saved-output query-contrast diagnostic;no C322 result yet.
C320 bounded PASS,C319 negative,and every earlier verdict remain unchanged.
Latest accepted execution:a31d5c5389f41cdb137b0bf375b7c7a99d8fb882.
Latest publication:b4e1686971d8d4a6d988a7f0e5e02a80cea6ec41. Do not rerun C321.

## Latest accepted evidence — C321

Acceptance:docs/experiment-ledger-addendum-c321-c322.md.
Acceptance commit:9025d339a67ae4b4b22435b8bda068c204d49d5e.
Summary:runs/c321-v5b-interior-order-ef98962d405b402ba3926a6d1c2625b2/summary.json.
SHA256:0e95c700cbac90025beb7baf1d65413cb1694de72b659540c2eb901f77f52fd9.
Log SHA256:44c54ed61f481a82f5e683d10563750073821a56ffedaad462034d4d49cd4456;960689bytes.
Own24/full5245 PASS;source772/protected1455;run_execution_valid=True.
Full5245 completed927.170s with failures0/errors0/exit0. Scientific exit0;capability statusFAIL.
All10 original/interior/original passes complete and every old replay error0.0.
Both arms0/5 on new interior-order names. Mean_last TRAIN1500/2880,HOLDOUT711/1440,total2211/4320;
last_only TRAIN1546/2880,HOLDOUT746/1440,total2292/4320. Original collapsed query-pair sums1996/2160
and1951/2160 respectively. These count same argmax,not identical logits or hidden states.
No new decoder/scores used to determine C321. Publication changes latest.json/latest.log only.

## Recovery boundary

Earlier execution failed at5bffb4887a1f2729058472d875cf413bc26836e4 and published
caaa42ac45a332c8b946714919eda58c38533384. That evidence remains in immutable history.
Instrumented retry completed all stages;original root cause remains UNCONFIRMED.
Preserve direct science/stderr logging and exact exit capture. Do not claim an environment fix.

## Active C322 — saved paired-query contrast

Experiment:C322-v5b-saved-query-contrast. Stage:V5-B-SAVED-QUERY-CONTRAST.
Registration:docs/experiment-ledger-addendum-c322-preregistration.md.
Design:docs/v5b-saved-query-contrast-v0.1.md.
Review:docs/c322-post-authoring-review.md.
Authoring/review target:6da3aba9af21754e1616148e07cd6b316913f8f5.

One question:when the question changes but the two facts remain identical,are the output vectors
nearly unchanged,or do their scores change without changing the winning answer? Compare saved
C321 interior names with its same-checkpoint ORIGINAL FOUR-character controls. Keep all10states,
seeds319001..319005,mean_last/last_only,all profiles,languages and original value splits. No new
inputs,model calls,training,model-state loading or output-candidate restriction.

Pair by canonical language/entities/values/fact permutation. Require one query per entity,
unique IDs,correct target bindings and full coverage;do not rely on adjacent archive rows.
A=entities[0],B=entities[1],never orient by values or scores. Read NORMAL saved CPUfloat64 logits.
The unchanged full parent verifier still validates every original/masked output and gate.

Per pair:original full256class argmax and correct-count/same-prediction;raw max_abs(zA-zB);
offset-invariant max_abs((zA-zB)-(zA[0]-zB[0]));mA=zA[tA]-zA[tB],mB=zB[tA]-zB[tB],D=mA-mB.
Exact D signs positive/zero/negative and mA>0&mB<0 are descriptive,NOT a two-class decoder.
A third class can remain highest even when relative target preference moves correctly.
Near offset-invariance fixed1e-9 is a diagnostic tolerance,not a capability threshold. All
logits and derived values finite. Equal argmax does not imply equal logits;equal logits do not
identify which hidden layer lost information. Neither measure is a calibrated confidence.
Old/new profile slots are aligned comparison families,not identical input strings.

## Parent contract,protection and work

Verify48ordered hashes BEFORE actual C321.verify_artifacts(C321dir,47ancestors,acceptedexecution).
Require parentFAIL,bothpasscounts0,primaryFalse,source identity and5artifact descriptors.
Use actual C321.load_parent on paths[1:] for verified logical data. Read hash-verified C321
fold-c321-interior-eval-v1 archive:raw.before['4'] and raw.interior. No trained-models.pt read by
the child,no checkpoint instantiated,no parent prediction repurposed as a newly inferred answer.

Actual C270.score's collapsed_pairs equals the two queries' normal argmax equality at fixed
language/entities/factorder/values. C287 partition sums those counts. C322 reconciles rows,
correct,pairs and collapsed_pairs for all40state/condition/split partitions,and the20interior
partitions additionally match stored C321 full_pass. All old local/masked gates stay unchanged.

Sole direct science import C321;C320/C319/context provide inherited scorer/audit/no-neural helpers.
All772source pins/1455inputs checked plus actual local/lazy/factory-language module coverage.
OWN6+6parentfiles ->778sources/1467inputs. No accepted files or exclusions changed. Precheck
returns its already verified loaded data to run,not a cross-process cache. End-of-run input
hashes and repository guard checked again;postcheck reloads/reconstructs all saved JSON.

10states*2conditions*864answers=17280savednormalanswers,8640querypairs,240localgroups,
40reconciliations. New model forwards/training/model-state loads/checkpointwrites/network all0.
Recursive parent verification and software tests still consume CPU/RAM and can load historical
evaluation tensors;do not call these costs free.4JSONartifacts plus summary:audit-plan.json,
query-pairs.json,measurements.json,validation-summary.json. Exact pair/group/overall reconstruction,
hash/size checks and no-overwrite required. No new tensor or model archive written.

Own24/modules207/loaded5270/focused5269;sole inherited exact C204 exclusion unchanged.
Manifest:719cd169028e0c0ead99f4620035b532cefed65145c4bcb4f8af3c781fda01e8.
PASS means diagnostic integrity only regardless of numerical contrast. No capability gate,
winning model,causal attribution,hidden-state claim or promotion of Gate F. C3210/5 stays negative.

## Post-authoring review and runtime boundary

post_authoring_review=PASS for committed-byte/static plus executed local software tests.
All6 OWN refetched at6da3aba9af21754e1616148e07cd6b316913f8f5,independent Git blob match6/6.
After allmatches,normal24/24 PASS5.674s and defaultCP932emulated24/24 PASS4.789s,both full
uninterrupted runs,exit0,zero failures/errors.24distinct IDs per mode verified and hashes
rechecked after tests. CP932 patch covers import/setup/tests/teardown,not full Windows emulation.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No native PowerShell executable.
Python+3embeddedblocks compile,UTF8/noNUL,undefinedglobals0,manifesthashmatches.48paths ordered
C321..C274;postcheckpaths[2:50],head50,argc51. Remote diff exactly6newOWNfiles. Activation preserves6.

Tests exercise independent contrast/offset/tie arithmetic,nonadjacent query binding,fullinventory,
48hashguards,778/1467real temporary files,childrun/no-neural/JSONonly,persistence and tampering,
CLI/suiteID semantics and diagnostic-only scope. Synthetic parent/scorer/Git interfaces replace
unavailable actual archives;they are software controls,not real C322 results or full5269PASS.
C270/C287 score-count definitions were source-audited,not run on actual parent data here.
Mandatory usergates:48real parentarchives/Windowspins,dispatcher/launcher/runnerParseFile,
own24/full5269 originalorder oneprocess regression,and real saved-output analysis.

## Execution and stop

Standard tools/invoke_active_v2.ps1 through explicitPowerShell7 after dispatcherParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C322 -> Validate(48parents,778/1467,
actual saved-query reconciliation,own24,focused5269) -> authoring_runtime_preflight=PASS ->
Execute(savedold4/interiorpairedcontrast,40reconciliations,240groups,persisted reconstruction) ->
logpublication. Direct UTF8 science/regression logs,native stderr,fataltrace where supported,
fixture-boundary progress,immediate decimal/hex exits and previous-preflight preservation remain.
No autoreties,process splitting,test skipping,environment changes or relaxed thresholds.
Validatefailure skips science/publication. Any integrity failure repairs SAME C322.
C323 waits for formal C322 judgment;oldverdicts and GateFNOTPASSED stay distinct.
Scientific execution HEAD differs from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-activation:docs/handoff-history/c322-pre-activation.md.
Git blob:379dcd56d37cda0229a825240626762caf03d8b3.
Pre-acceptance:docs/handoff-history/c321-pre-acceptance.md.
Git blob:d05a8ffdc6eb4da12f5c864c416186be41392f78.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
