# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C319 ACCEPTED VALID NEGATIVE. C320 ACTIVE / NOT YET JUDGED. C321 NOT REGISTERED.**
C320 is the unique ACTIVE frozen unequal-name-length capability probe;no C320 scientific result.
C318/C317 diagnostic PASS,C316/C315 negatives,C308 bounded PASS and old verdicts unchanged.
Latest accepted execution:529c54ef63b1015b25632b8123a9a552eebcd263.
Latest accepted publication:3abe218dc9191d26963e5b5022d4d1983300084d. Do not rerun C319.

## Latest accepted evidence — C319

Acceptance:docs/experiment-ledger-addendum-c319-c320.md.
Acceptance commit:1c60afa5997ca9f61a6f5b44e73a31e2b15cd609.
Summary:runs/c319-v5b-trained-last-0f94e96bbbba43b395fcf8eab1e38246/summary.json.
SHA256:48815ca382d0da078da12ec2d54f2c42261e94498b682f679d8f46d746ec0580.
Own24/focused5197 PASS;760sources/1429inputs;run_execution_valid=True;all_pairs_matched=True.
Both arms5/5 at2..5;six mean_last5/5,last_only4/5. Paired4both,1control_only,0candidate_only,0both_fail.
last_only319005 six TRAIN567/576,HOLDOUT283/288;paired mean_last575/576,288/288.
The latter passes full gates despite one normal error;do not substitute pooled perfection.
No support for adopting trained last-only as a reliability improvement in this cohort.

## Active C320 — frozen unequal-name-length transfer

Experiment:C320-v5b-frozen-unequal-name-lengths. Stage:V5-B-FROZEN-UNEQUAL-NAME-LENGTHS.
Registration:docs/experiment-ledger-addendum-c320-preregistration.md.
Design:docs/v5b-unequal-name-lengths-v0.1.md.
Review:docs/c320-post-authoring-review.md.
Authoring/review target:b975f7d2c8cfbf3c9ae71c4b9f147ab1be10ebd1.

One question:can equal-name-length-trained models handle two-character and four-character names
in the same question? Test(2,4) and(4,2) assigned to canonical entity IDs,not fact order. Both fact
orders,both questions,three original name families,English/Japanese and TRAIN/HOLDOUT values remain.
All individual lengths are in the original trained range2..4;only their within-question combination
is new. No new vocabulary,frame extension,learning or readout modification.

Freeze ALL10 C319 states,seeds319001..319005,both mean_last and last_only. Preserve each record's
own trained policy via actual C319.trained_readout throughout every old/new pass. Actual factory/
loader/strict-load,full14,256parameters/64slots retained. No model filtering or old-state training.
Primary:all5 retained mean_last models pass BOTH new layouts under all original local/masked gates.
last_only fully reported but cannot rescue a primary failure. Primary fixed before new outcomes,
not before old C319 results;not independent model selection. No C319 verdict rewrite.

Renderer:repeat u*n/v*m;shared_prefix u*n/u*(m-1)+v;shared_suffix u*n/v+u*(m-1). Distinct names;
all facts/values/questions/orders unchanged. For(n,n),match every original1..6 prompt byte-for-byte.
Canonical data/prompts hashes retained. New normal prompts1728distinct/disjoint from old normals;
byte vocabulary subset. Every token,BOS/EOS/padding and actual C304 query span checked. Maximum
Japanese new body37bytes/39encoded tokens fits64,shorter than some old training inputs. No
truncation/language exclusion. Different lengths create identifying cues as well as position/
separation changes;success alone does not prove full name-content matching or arbitrary reasoning.

Every state:old1..6 BEFORE -> unequal layouts -> old1..6 AFTER. Old logits match the same C319
archive<=1e-9 and exact argmax;original2..6 gates unchanged. Full weights/hooks preserved perpass.
All views retained,full256-class output. Reuse C304 logical scorer/profile adapter per layout,
not its old fixed-length cohort analyzer. Thresholdsaccuracy.90/query_pair.80/evidence_drop.35/
query_drop.35/two_order.80. No averaging away a failed layout. Report20model/layout scores,
40split partitions,10reproductions,per-layout and combined counts for both cohorts.
PASS is bounded unequal-length capability;valid primary failure is ACCEPTED VALID NEGATIVE.
Neither outcome proves fresh-seed reliability or promotes Gate F.

## Parent contract,protection and work

46ordered summary hashes checked BEFORE actual C319.verify_artifacts with45ancestors and its
accepted scientific HEAD. RequireFAIL,exact ten old flags,all_pairs_matched/all_replays and seven
artifact descriptors. Read C319's own dataset/prompts/final same-policy logits,not diagnostic
ancestor artifacts. Schemasfold-c319-trained-readout-models-v1 and fold-c319-trained-readout-eval-v1.
Full state fingerprints/readout_policy/ordered identities matched. No target labels enter forward.

Sole direct import C319;all inherited C318/C317/C316/C315/C304/C287/C310/backend and actual local
context/lazy/factory helpers remain protected.760sources/1429inputs plus OWN6 and8C319parentfiles
->766sources/1443inputs. No accepted files changed or new regression exclusion. Missing dependency
coverage stops the run. Same single exact C204 exclusion;own24/modules205/loaded5222/focused5221.
Manifest:34ac7cbac03191c2e64ae05887f7d04cbc90c3cf0a73e18427708c1bbeed307d.

Science10models*(144+54+144)=3420forwards,328320rows,13680core calls. Training0,10strict state loads,
one existing bundle read,new checkpoints0,network0. Six discarded smoke forwards,recursive parent
verification and software regression separate. Raw logit payload672399360bytes plus overhead,not
peak-RAM accounting. Five artifacts plus summary:evaluation-plan.json,unequal-prompts.json,
evaluations.pt,measurements.json,validation-summary.json. Child schemafold-c320-unequal-eval-v1
retains before/new/after logits,policy receipts,hashes/replay errors. No-neural saved reconstruction
and all tensor/JSON hash/size checks mandatory;no overwrite. Full arrays remain local/ignored.

## Review and execution boundary

post_authoring_review=PASS;all6 OWN refetched atb975f7d2c8cfbf3c9ae71c4b9f147ab1be10ebd1,
independently Git-blob-matched6/6 and rechecked after tests. Post-match uninterrupted full runs:
normal24/24 PASS12.710s,CP932-default-emulated24/24 PASS12.890s;zero failures/errors,exit0.
24distinct test IDs verified per mode. CP932 patch covers import/setup/tests/teardown,not complete
Windows emulation. UTF8/noNUL,Python+3embedded blocks compile,unresolved globals0,manifest matches.
46paths/CLI[2:48]/head48/argc49 confirmed. No accepted sources/tests/logs/dispatchers changed.

Tests execute actual accepted C304 forward/span/scorer-adapter,C315 evaluator/replayer and C319
policy/hook functions on controlled models. Independent prompt parsing,canonical hashes,all new
bounds,real child342forward per-policy inference,46hash guards,766/1443file checks,loader/run/
persistence ordering,semantic suite IDs,primary separation and tamper rejection pass. Parent
support is exact function slices,NOT full repository/modules and NOT committed. Synthetic models/
scorers and substituted archives/Git are software evidence,not actual FOLD capability/full5221
regression. No PowerShell locally. Real user checkpoints/46archives/Windows pins/ParseFile,
frozen bilingual probes,own24/full5221regression and scientific evaluation remain mandatory.

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C320 -> Validate(46parents,766/1443,
old/new render and native-span checks,both-policy probes,own24,focused5221) ->
authoring_runtime_preflight=PASS -> Execute(10frozen models,old/unequal/old,reproductions,layout
scores,saved reconstruction) -> publication. Validate failure skips science/publication.
Integrity failure repairs SAME C320 without changing layouts/policies/models/thresholds. C321
waits for formal judgment. Scientific execution HEAD differs from the subsequent log commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-activation:docs/handoff-history/c320-pre-activation.md.
Git blob:3ea0fa8b0d1c10c2e4f0a80b8f4fb7827cfff1a8.
Previous:docs/handoff-history/c319-pre-acceptance.md.
Git blob:8f9b42fffeb109f5ce31ff4bae80468cce6da386.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
