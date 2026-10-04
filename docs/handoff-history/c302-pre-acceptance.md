# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C301 ACCEPTED VALID NEGATIVE. C302 ACTIVE / NOT YET JUDGED. C303 NOT REGISTERED.**
C300 remains diagnostic PASS. C302 is the unique ACTIVE frozen weight/gain cross diagnostic.
Latest accepted scientific execution:d67c900c588ff0e4c8974cd8f80721da381a8770.
Latest accepted published log:871d5c55a0cb8139a1ff95fbfce95b7472bf16fa. Do not rerun C301.

## Latest accepted evidence — C301

Acceptance:docs/experiment-ledger-addendum-c301-c302.md.
Acceptance commit:400dd5337c6e30fe901b91d4587d16d7c12f9c0b.
Summary:runs/c301-v5b-residual-gain-8e72f4cf3e744128b905da20770c9f5b/summary.json.
Summary SHA256:19d5a94c3ce5d2bef94683b05983c44b1e76f452490e184f8ffde7b934d559c1.
Own40/focused4637 PASS;source652/protected1202;all_pairs_matched=True;run_execution_valid=True.
Manifest:c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9.
Fixed/learned quad2/1,seen tasks2/3,all-tasks2/1,TRAIN direct3/3,HOLDOUT direct2/3.
301002 passes all tasks in both arms;301003 loses quad in learned_gain;301005 gains seen-length
passes but still misses quad;301001/301004 still fail TRAIN in both arms. No superiority or adoption.
Learned final alpha by seed301001..5:
[0.8684034644345564,0.7330682658799806,0.7781612711147479,0.8356705336201741,0.7789613854784259].
All are below1,but the common weights/learning trajectories also changed. Magnitude is not an
isolated causal contribution or proof of universal benefit from attenuating the residual.
301005 two HOLDOUT278->288,triple273->288,quad262->283.301003 quad HOLDOUT288->287.
301001 HOLDOUT two141->119,triple135->119,quad132->122. Keep improvements and regressions visible.

## Active C302 — frozen weight/gain cross

Experiment:C302-v5b-frozen-gain-weight-cross. Stage:V5-B-FROZEN-GAIN-WEIGHT-CROSS.
Registration:docs/experiment-ledger-addendum-c302-preregistration.md.
Design:docs/v5b-frozen-gain-cross-v0.1.md.
Review:docs/c302-post-authoring-review.md.
Acceptance base:400dd5337c6e30fe901b91d4587d16d7c12f9c0b.
Authoring/review target:60df5639637db92a7e9bc7f5649634bc01d437e6.

One question:at fixed saved common weights,does changing the inference coefficient between1 and
the same seed's TRAIN-learned alpha rescue or regress predictions? Keep all5 C301 seeds and both
trained states. For each seed,compare fixed_gain-trained and learned_gain-trained weights at both
unit and trained coefficients. No new training,cohort filtering,gain search or new parameters.
The donor is always the same seed's learned_gain final_gain,checked against its summary and state.
This separates an immediate coefficient intervention at fixed weights from the whole prior
training-policy outcome in the common weights. It does not isolate a unique training mechanism.

Strict-load each original C301 wrapper once via its actual make_models/load_bundle. Preserve its
full fingerprint,optional gain_logit and common model.* state. Do not mutate the scalar,add it to
a fixed checkpoint,or splice common parameters between arms. Freeze all weights. Original stored
parameter counts14256/14257 remain unchanged. The implementation evaluates wrapper.model,the
actual C278 inner model,not the outer C301 forward;there is no double application of gain.

Temporary child-owned hooks capture r before C278's dynamic norm hook and a at read.output.
A late norm hook is installed during local_encoder. Require actual normalizer input exactly r+a
on every call,CPUfloat64/batch-by16/finite tensors,one complete capture. Supply alpha*r+a;unit
coefficient returns None to preserve the original sum. C278 assertions stay active. All upstream
core/reader computation executes. No labels or coefficient-selection rules based on answers enter
forward. Cleanup restores forward/pre-hook registries including kwargs/always-call metadata.

Each of10 states executes original_before,swapped,original_after. Fixed-arm gain order1/trained/1;
learned-arm ordertrained/1/trained. Every pass evaluates all old tasks,profiles,TRAIN/HOLDOUT and
normal/evidence-blind/query-blind views. Both originals must reproduce C301 logits<=1e-9 with exact
argmax;also compare before to after. Full wrapper weights,original stored gain and hooks remain
unchanged after every pass. Operational smoke compares actual wrapper versus inner outputs for
BOTH original coefficient conditions. Any mismatch is INVALID / RETRY SAME C302.

Report30 pass results,180 final partitions,10 reproduction receipts and5 exact gains. Within-weight
comparisonsunit->trained cover60 aggregates/25920 matched normal rows. Across-weight comparisons
fixed-trained->gain-trained at the same gain label cover60 aggregates/25920 rows. Report flips,
rescues,regressions,left/right correct counts. Wrong-to-wrong changes are not rescues. Count four
logical weight/gain conditions once;restored originals are controls,not additional independent runs.
All original gates remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Original per-state task flags must match their parent. Swapped gates are descriptive. PASS means
intervention fidelity,restoration and saved-data reconstruction only. C301's all-five negative
and Gate F remain unchanged even if a swapped condition succeeds. No deployment/best-of selection.

## Parent contract,protection and workload

Verify28 ordered hashes BEFORE exact C301.verify_artifacts(parent_dir,27 ancestors,accepted HEAD).
The exact C301 summary seals all8 artifact descriptors. Require statusFAIL,matched pairs,replay,
original counts and ordered seed/arm records. Read verified C301 data JSONs and final prediction
archivefold-c301-gain-eval-v1. adapt_anchors checks state/gain metadata and summary agreement.
The model archivefold-c301-gain-models-v1 is loaded through its actual parent loader;new child
output is NOT a trained-model bundle. The five coefficients are trained-only,not evaluation fits.

Sole direct repository import C301. Its context supplies inherited C294 no-neural,C287 normalization,
C284 evaluate/replay_error,C283 quad,C282 tables and model/core bundle. Retain all652 parent sources
and1202 inputs;check real repository-local helper coverage and exact C278 readout blob
0aa8d65874f4a021e21d04948ffd0a1d5615248b. Add OWN6+9 parent files:source658/protected1217.
No accepted source/test/preregistration/log/dispatcher is changed;no additional regression exclusion.

Science:10saved models,training0,2430forwards,233280row presentations,9720core calls,10strict state
loads,one existing bundle read,new checkpoints0,network0. Operational smoke8forwards,tests and
recursive parent reconstruction are separate. This is not a zero-inference log-only audit.
Outputs:gain-plan.json,gain-evaluations.pt,measurements.json,validation-summary.json plus summary.json.
Archivefold-c302-gain-cross-eval-v1 retains all30 passes,coefficients,original fingerprints and
restoration attestations. Raw logit payload477757440 bytes before overhead,not peak RAM estimate.
Full tensors/maps remain local/ignored;compact receipt and aggregate rows are mirrored in the log.
Numerical postcheck reconstructs all scores and parent agreements under no-neural scope.
Own32/modules187/loaded4670/focused4669;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:283f4ac996eda2ac866a192408fff2368782b8592d350c11af33723f874f2960.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static review plus actual local behavioral tests).
All6 OWN files re-fetched at60df5639637db92a7e9bc7f5649634bc01d437e6;whole-file Git blobs match6/6.
After all matches:normal own32 PASS in3.385s;entire CP932-emulated own32 PASS in3.633s.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;both Python files and3 embedded blocks compile;
free globals0,UTF8/noNUL,manifest self-hash matches. Actual accepted C278/C301 class AST integration
with substitute backbone/reader verifies unit/nonunit original function and hook restoration.
Local parent support files are fetched class slices,not whole parent clones,and are not committed.
The user checkout test extracts those classes from full accepted modules. Actualinfer_state fixture
executes3*81 model calls and checks counts/strict-state restoration. Other tests cover28hash guards,
658/1217 protection,all cohort/mode mapping,actual child run/bundle dispatch,persistence/tampering,
diagnostic/capability separation and explicitUTF8. Parent archives,Git,legacy scorers/suite entries
are substituted where unavailable. These are not tests of real FOLD capability or actual4669 suite.
Mandatory Windows28-parent checks,protected bytes,PowerShell ParseFile,actual two-arm wrapper
smoke,full4669 regression and ten saved-model inference runs remain pending.
Activation must retain all6 reviewed OWN blobs and every accepted file/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C302 -> Validate(28parents,658/1217
protection,both actual wrapper/inner coefficient smoke,own32,focused4669) ->
authoring_runtime_preflight=PASS -> Execute(all10frozen states,original/swapped/original,
no training,original logits/weights/hooks preserved,paired comparisons,saved reconstruction) ->
log publication. Validate failure skips science/publication. Any integrity issue repairs SAME C302.
Do not change cohort,coefficient donor,mode order,thresholds or select better branches/models.
C303 remains unregistered until C302 formal judgment. Gate F remains NOT PASSED.
Separate scientific execution HEAD from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c301-pre-acceptance.md.
Git blob:c5d7e6c0f8d62a9d49be03fb13b742c63246f195. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
