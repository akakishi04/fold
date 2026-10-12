# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C320 ACCEPTED PASS. C321 ACTIVE / NOT YET JUDGED. C322 NOT REGISTERED.**
C321 is the unique ACTIVE frozen interior-name-order probe. No C321 scientific result yet.
C320 is bounded unequal-length capability PASS,not merely diagnostic integrity.
C319 remains valid negative;all previous verdicts unchanged. Do not rerun C320.
Latest accepted execution:0e4687acfa72355cbddc47c3ceb98700354fe34d.
Latest publication:7a693b5d7747ab67146a8c2fa2f996cb10b5054d.

## Latest accepted evidence — C320

Acceptance:docs/experiment-ledger-addendum-c320-c321.md.
Acceptance commit:8785a88b70a14a4b8d632ff520a03977eb73f129.
Summary:runs/c320-v5b-unequal-names-d1599525908a404998a52011a5567b81/summary.json.
SHA256:9e41e82228f26cf525ee54e4097abd493a339641d6b3d3f5b2a6d10ba8868431.
Log SHA256:34570e813588d80f63f2ac3e49fa9eeb909aab7c1c9475bb7de90c503e851093;965523bytes.
Own24/full5221 PASS,failures0/errors0,exit0,source766/input1443. All10 states/replays complete,
all replay errors0.0,weights/hooks preserved,persisted_unequal_names PASS,run_execution_valid=True.
Mean_last5/5 for(2,4),5/5 for(4,2),5/5 both. Last_only4/5 short_long,5/5 long_short,4/5 both.
Only last_only319002 short_long HOLDOUT287/288 fails;its TRAIN576/576. All other normal partitions
perfect;mean_last8640/8640. Local/masked gates remain deciding,not pooled accuracy.
No C319 outcome relabelled. Publication changes latest.json/latest.log only.

## Recovery boundary

Earlier full-suite preflight interruption did not recur. The unchanged ordered5221test suite
completed in735.042s,failures0/errors0,exit0/0x00000000. The original cause remains UNCONFIRMED.
Do not claim a C174 bug,thread/OOM/native root cause or environment repair. Preserve previous
local logs and operational diagnostic logging;no full rerun of accepted C320 is needed.

## Active C321 — frozen interior name order

Experiment:C321-v5b-frozen-interior-name-order. Stage:V5-B-FROZEN-INTERIOR-NAME-ORDER.
Registration:docs/experiment-ledger-addendum-c321-preregistration.md.
Design:docs/v5b-interior-name-order-v0.1.md.
Review:docs/c321-post-authoring-review.md.
Authoring/review target:672a96440ec779d7f440685bb0c856da0e7e41c5.

One question:can frozen C319 models bind four-character names whose first/last characters and
character multisets agree,but internal order differs? Three fixed families:
u_dominant:uuvu/uvuu;balanced:uuvv/uvuv;v_dominant:vuvv/vvuv.
Examples:aaba/abaa,aabb/abab,babb/bbab. No longer names,new vocabulary or training.
Use all10C319states,seeds319001..319005,both mean_last/last_only,including every previously failed
state. Keep own trained policy throughout;14,256parameters/64slots/full256-class output unchanged.
No checkpoint selection,per-query model choice,new coefficients,optimizer or backward.

Retain canonical two facts/values/queries/both fact orders,three entity pairs,English/Japanese,
TRAIN/HOLDOUT value splits and normal/evidence-blind/query-blind views. Input length4 already
trained,but new name-order patterns not trained.864new normal prompts,distinct/disjoint from
original1..6normalinputs,old byte vocabulary subset. Japanese43bodybytes+2markers=45tokens.
Verify every exact byte,BOS/EOS,padding and actual query span. No truncation or language removal.
Original data/prompt hashes retained. Equal input character counts need not yield equal learned
hidden means;do not assume the local encoder is a bag-of-characters model.

Primary:ALL5mean_last states pass all3families under original local/masked criteria:
accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/two_order.80. Last_only full comparator
cannot rescue primary failure. New family names map bijectively to opaque old scorer slots
repeat/shared_prefix/shared_suffix;the actual input names and rows/tensors are not changed by
this adapter. Reuse C304.score_length->C270 logical gates. PASS is bounded capability here;
valid primary failure ACCEPTED VALID NEGATIVE. Neither cancels C320 nor promotes Gate F.
Same previously evaluated checkpoints/value split mean not independent fresh-seed replication.

## Parent contract,protection and work

Verify47ordered hashes BEFORE actual C320.verify_artifacts with46ancestors and accepted C320
execution HEAD. ParentPASS and exact10layout flags required. C320's5outputs are evaluation
artifacts,not model/data bundles. Actual C320.load_parent(paths[1:]) yields validated C319 data,
oldprompts and final same-policy anchors. Actual C319.load_bundle reads paths[1].parent/model
bundle;never seek weights in the C320 directory(paths[0]). Factory/strict-state loading retain
all original identities. No generated answers used as model weights or new teacher data.

Sole direct science import C320;C319/C315/C304/C287/C310/backend inherited. Verify all766source
pins/1443inputs and actual repository-local context/lazy/factory-language dependency coverage.
Add OWN6 and6C320parentfiles ->772sources/1455inputs. No accepted-file modification or pin waiver.
Own24/modules206/loaded5246/focused5245;sole inherited exact C204 exclusion unchanged.
Manifest:813f7283535086c9b7ebd416da1fb1d50b5240ece9d58e364173b4cb4d433fea.

Each state:old1..6before -> newinterior -> old1..6after. Both old outputs reproduce C319<=1e-9
and exactargmax,original2..6flags unchanged. C320unequal archive recursively verified,not new
inference. State/hook registries and actual trained-policy receipts checked after each pass.
10states*(144+27+144)=3150forwards,302400rows,12600core calls,10strictstate loads,oneC319bundle
read,training0,newcheckpoints0,network0.6discarded smoke forwards,recursive checks/tests separate.
Rawlogits619315200bytes before overhead,not peakmemory. All tensors local/ignored.
Five outputs plus summary:evaluation-plan.json,interior-prompts.json,evaluations.pt,
measurements.json,validation-summary.json. Schemafold-c321-interior-eval-v1 retains allthreepasses,
policies,fingerprints,receipts/reproduction errors. Numerical no-neural saved reconstruction of
all scores/prompts/JSON required,hash/size checks and no-overwrite enforced. Report10stateflags,
20splitpartitions,10reproductions,separate armcounts. No pooled pass substitutes for local gates.

## Post-authoring review and runtime boundary

post_authoring_review=PASS for committed bytes/static and local software tests. All6OWN refetched
at672a96440ec779d7f440685bb0c856da0e7e41c5 and independently Git-blob-matched6/6,rehashed after tests.
Post-match full24/24 normal PASS11.511s;full24/24 defaultCP932emulation PASS10.902s,both exit0 and
no omitted IDs. Patch includes import/setup/tests/teardown,not fullWindows emulation.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No native PowerShell executable.
UTF8/noNUL,Python+3embeddedblocks compile,unresolvedglobals0,manifest selfhash matches.
47paths C320..C274,postcheckpaths[2:49]/head49/argc50 verified. Remote diff exactly6newOWNfiles.

Tests execute actual C304forward/span/scoreradapter,C315evaluate/replay and C319policy functions
on controlled models. Independent parser/names/inputbytes,315forward child path perpolicy,
47hashguards,772/1455fileprotection,correctC319bundlepath,primaryseparation,persistence/tampering,
semantic suite IDs and no-optimizer boundaries verified. Exact parent function slices support
local testing,NOT fullmodules/repository and NOT committed. Synthetic scorers/models/archives/Git
are software evidence,not actualFOLDcapability or real5245regression. Mandatory user validation:
47actualarchives/Windows pins,dispatcher/launcher/runnerParseFile,realbilingual probes,
own24/full5245ordered regression and all10actualcheckpoint evaluation. Activation preserves OWN6.

## Execution and stop

Use tools/invoke_active_v2.ps1 with explicitPowerShell7 and dispatcherParseFile after gitpull.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C321 -> Validate(47parents,772/1455,
new input invariant/span checks,real bothpolicy probes,own24,focused5245) ->
authoring_runtime_preflight=PASS -> Execute(all10frozenstates,old/interior/old,preservation,
new gates and savedreconstruction) -> logpublication.

Keep recovered one-process ordered-suite observation,unique directUTF8/fataltrace logs,fixture
boundary markers,exact childexitdecimal/hex and previouspreflight preservation. No test splits,
automatic retry,extra exclusion or environment changes. Validatefailure skips science/publication.
Any source/artifact/replay/policy/integrity failure repairs SAME C321 with fixed scientific
conditions. Valid primaryfailure stays negative;no family/seed/gate change after outcomes.
C322 waits for formal C321judgment. C320boundedPASS/C319negative/GateFNOTPASSED remain distinct.
Scientific execution HEAD differs from subsequent publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-activation:docs/handoff-history/c321-pre-activation.md.
Git blob:557cb93817929ff2f517c1365c1f678fad88c281.
Pre-acceptance:docs/handoff-history/c320-pre-acceptance.md.
Git blob:2ea5b6b86fd6c8d6a3f0a62a10618c27866de943.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
