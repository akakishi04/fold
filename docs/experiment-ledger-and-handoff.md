# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical dispatchers and accepted sources/tests/logs remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C303 ACCEPTED VALID NEGATIVE. C304 ACTIVE / NOT YET JUDGED. C305 NOT REGISTERED.**
C302 remains diagnostic PASS. C304 is the unique ACTIVE length-breadth comparison.
Latest accepted scientific execution:8e01ac5bb1dae57f129615731b7013eed43b5719.
Latest accepted published log:726d43f4236f5128d88c3e38dfe77de4988c73b7. Do not rerun C303.

## Latest accepted evidence — C303

Acceptance:docs/experiment-ledger-addendum-c303-c304.md.
Acceptance commit:c8ccecbbfbb74cffb520ed4da507c9f7b8c0623b.
Summary:runs/c303-v5b-gradient-route-ef832a6117c44389aa035cd16c76be70/summary.json.
SHA256:33d3370d383d8f220cea46056cb0fefdae27498794110fb7672bca726bc45d01.
Own40/focused4709 PASS;source664/protected1228;all_groups_matched=True;run_execution_valid=True.
Quad full_train3/5,core_frozen4/5,residual_stop0/5. Seen full gates4/5/4;TRAIN direct4/5/5.
Gradient-receiving union14256/10928/10928;frozen cores unchanged. Do not adopt residual_stop.
Core_frozen's4/5 is not universal proof or a reason to silently change the next baseline.
303001 full_train two TRAIN526/576,HOLDOUT222/288;core_frozen576/576,288/288.
303004 candidate seen HOLDOUT285/288 at both2/3;quad287/288. Zero quad passes is not zero correct answers.

## Active C304 — training length breadth to unseen five

Experiment:C304-v5b-length-breadth-to-five. Stage:V5-B-LENGTH-BREADTH-TO-FIVE.
Registration:docs/experiment-ledger-addendum-c304-preregistration.md.
Design:docs/v5b-length-breadth-v0.1.md.
Review:docs/c304-post-authoring-review.md.
Acceptance base:c8ccecbbfbb74cffb520ed4da507c9f7b8c0623b.
Authoring/review target:a4064f0a341d1a3628de3fd667f3178a5be4f5a0.

User requested training2/3/4 then testing5. One question:does broader training-length coverage
improve unseen5 reliability at common maximum4 and1200updates? Fresh seeds304001..304005,paired
order seeds304101..304105. Arms:four_only=(4),three_four=(3,4),two_three_four(candidate)=(2,3,4).
Use ordinary FULL CE in every arm;no core freezing,residual stop,gain,auxiliary loss or prior weights.
All15 models retain identical initial states within each seed and independent parameter storage.

300epochs*4updates,48rows/24intact pairs per update. Shared logical pair order and profile eachstep.
Length=allowed[epoch%len(allowed)];profile=(epoch//3+epoch%3)%3. This avoids3length/3profile aliasing.
Private randperm96 with order_seed+304000+epoch;fitRNG608000 resets each model. Each row's exposures
at lengths2/3/4:four_only0/0/300;three_four0/150/150;candidate100/100/100. All arms400updates/profile.
Candidate length/profile update matrix[[136,132,132],[132,136,132],[132,132,136]].
One AdamW1200updates,lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1;no adaptive budget or selection.

The64-slot context is common to all arms. Japanese5 prompts require52UTF8bytes plus BOS/EOS=54,
which cannot fit the old48. No truncation,language omission or tokenization change. Accepted
backbone has no slot-indexed weights. Clone actual old48 C278 weights,replace copied backbone
max_tokens and core.slots configs with64,and use child LengthReadout with generalized shape/span.
Keep14256parameters(core3328),state keys/order,pre-core memory,mean/final dual attention and
post-core residual unchanged. No accepted source edit or global monkeypatch. The expanded frame
adds slot-level computation;do not equate forward counts or historical runtime across48/64.

Mandatory operational parity:old48 versus new64 on54 TRAIN-based views covering both languages,
lengths2/3/4,allprofiles/views. Ephemeral matched nonzero-reader perturbation avoids a vacuous
zero-head comparison. Logits/gradients<=1e-9 and exact argmax;dummy labels are software probes only.
Discard probe copies. Actual training models start from the original unperturbed initialization.
A separate untrained5-length smoke checks shape only,never performs optimizer updates.

Canonical C267 logical data remains192TRAIN/96HOLDOUT with the exact old value split and hashes.
New render2/3/4 must match actual C267/C270/C283 bytes. Render5 by the same repeat/shared-prefix/
shared-suffix construction;all3456 normal prompts across2..5 unique;maximum52bytes;alphabet unchanged.
Only TRAIN values at each arm's allowed lengths enter training;never5,HOLDOUT or masked inputs.
Freeze all final models and evaluate every2/3/4/5 length,profile,language,split and normal/evidence-
blind/query-blind view. Five's TRAIN label is TRAIN-valued UNTRAINED length,not learned5 examples.

The original C270 scorer is reused through an explicit profile-family adapter;it depends on
logical row grouping and predictions,not actual identifier length. C287 normalization consumes
that canonical triple-shaped schema;outer records explicitly identify length and whether trained.
Primary PASS iff all5 two_three_four models pass ALL FIVE-character local/masked criteria.
Thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Report all15 results,per-length gates,120 final partitions,80 candidate/control count contrasts.
Shorter-length results are descriptive. No old C303/gate verdict is retroactively changed.
Coverage,exposure allocation and timing differ together. Success is bounded structured-name
transfer,not proof of a length-independent rule or arbitrary identifiers;failure identifies no
unique representation defect. Do not causally compare older different-seed/48-slot cohorts.

## Parent contract,protection and workload

Verify30 ordered summary hashes BEFORE exact C303.verify_artifacts with29 ancestors and its
accepted execution HEAD. Its exact summary seals all8 artifact descriptors. Require valid-negative
original counts,matched groups and replay;read canonical verified dataset.json only,not model states.
Sole direct import C303;context exposes C301/audit/C287/C283 and inherited core/model helpers.
C301.pair_source supplies pair grouping. All deciding helper sources remain pinned;the exact
language/core/C278/C269/C270/C267 blobs receive additional assertions. Factory language_module,
context and lazy pair helper coverage is checked. Retain664sources/1228inputs;addOWN6+9C303inputs:
source670/protected1243. No accepted source,test,log,preregistration or dispatcher is modified.

Work:15models,18000updates,864000training rows,21240forwards,1175040total rows,84960core calls,
15strict state loads,one15-state bundle write/read,network0. Per model1200training+108evaluation+
108replay. Four evaluated lengths add10368rows/pass. Expanded64slots applies to all arms.
Operational tests/probes and recursive parent checks are separate. No equal-FLOP or speed claim.
Seven artifacts plus summary:architecture-plan.json,dataset.json,length-datasets.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c304-length-models-v1(includes slots64),fold-c304-length-eval-v1. Keep1200losses,schedules,
allrawoutputs,hashes and strict replay<=1e-9/exactargmax. Full tensors/maps remain local/ignored.
Own40/modules189/loaded4750/focused4749;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:af8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static review and executed local software tests).
All6 OWN files re-fetched ata4064f0a341d1a3628de3fd667f3178a5be4f5a0 and matched by full Git blob6/6.
Post-match normal own40 PASS17.649s;CP932-emulated whole-suite40 PASS17.788s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;source/test and3embeddedblocks compile;unresolvedglobals0;
UTF8/noNUL;manifest recomputes. Actual new fit loops run1200updates/arm on small synthetic models,
with deterministic-repeat/optimizer instrumentation,full train/eval/replay accounting and persistence.
Integration tests on the user checkout extract accepted backend/core/reader/scorer definitions.
Local parent support files are reconstructed excerpts from fetched definitions,NOT byte-identical
accepted clones. Only OWN6 are asserted byte-identical;local integration verifies bounded numerical
behavior,not the complete repository graph or15-model capability. Synthetic inputs intentionally
encode targets for software tests. Parent archives,Git/normalization and suite members are mocked
where unavailable. No reconstructed parent support file is committed.
Mandatory actual Windows30parent/pin checks,actual old48/new64 compatibility,allrealrenderings,
PowerShell parsing,own40,full4749regression and15actualC304fits/replays remain pending.
Activation must preserve OWN6 and all accepted sources/tests/logs/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C304 -> Validate(30parents,670/1243pins,
no-truncation2..5renderings,all15schedules,actual48/64compatibility,5-length smoke,own40,focused4749)
-> authoring_runtime_preflight=PASS -> Execute(15models*1200updates,all2..5frozen scoring,
strict state replay,saved reconstruction) -> log publication.
Validate failure skips science/publication. Any integrity issue repairs SAME C304 without changing
scientific conditions. Valid all-five miss is ACCEPTED VALID NEGATIVE. No factor/cohort/budget/
threshold changes after outcomes. C305 remains unregistered until formal judgment. Gate F NOT PASSED.
Separate scientific execution HEAD from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Complete previous handoff:docs/handoff-history/c303-pre-acceptance.md.
Git blob:fd02f3cbd2f7974be082d4cf7fa1f99fb701df46. Historical ACTIVE commands are not executable.
