# C302 preregistration — frozen weight/gain cross

Experiment:C302-v5b-frozen-gain-weight-cross. Stage:V5-B-FROZEN-GAIN-WEIGHT-CROSS.
Acceptance base:400dd5337c6e30fe901b91d4587d16d7c12f9c0b.
C301 ACCEPTED VALID NEGATIVE;C300 diagnostic PASS;Gate F NOT PASSED;C303 NOT REGISTERED.

## One question

At fixed saved C301 common weights,does switching between gain1 and the same seed's TRAIN-learned
gain rescue or regress predictions? Evaluate both trained weight sets at both coefficient values.
C301 changed the coefficient and the whole optimization trajectory together;do not attribute its
quad2/5 versus1/5 to the final coefficient alone. No further gain range,initialization or loss sweep.

For each of all5 original seeds301001..301005:
- fixed_gain-trained weights at unit gain1 (original) and candidate's saved TRAIN gain;
- learned_gain-trained weights at that saved TRAIN gain (original) and unit gain1.
The gain donor is ALWAYS the same seed's learned_gain model,never a better-performing seed.
The exact gain comes from fit.final_gain and must match summary.seed_results.final_gain and the
strict-loaded original wrapper. No fresh training,no evaluation-based coefficient fitting or
candidate selection,no model-specific threshold,per-question routing,or best-of accuracy.

## What the comparison can and cannot establish

Within one fixed weight set,the changed inference coefficient is the sole intervention. Across
weight sets at one common coefficient,the entire prior training-policy outcome differs,including
all original weights and effects of the scalar's gradient on clipping/optimization. This does
not isolate an individual training mechanism or yield additive causal shares of total accuracy.
The learned coefficient need not be equally calibrated to the fixed-arm weights. An off-diagonal
is a deliberately untrained pairing,not a production recommendation. Models can rescale their
internal representations,so coefficient magnitude is not a universal importance measure.
This is a follow-up on5 dependent paired runs,not independent replication or new seeds.

## Exact inference and preservation

Use C301.make_models and C301.load_bundle for the10 original wrapper states;strict-load each into
its correct fixed_gain or learned_gain wrapper. Full state includes model.* keys and optional
gain_logit. Verify original full fingerprint and original gain. Do NOT add a gain parameter to
a fixed-arm checkpoint,mutate a learned gain_logit,copy common weights between arms,or reload
states between passes. Existing parameter counts remain14256/14257;no new learned parameter.

Inference executes wrapper.model,the actual accepted C278 MeanFinalDualReadout,with child-owned
temporary hooks. The C301 outer wrapper is not called for main scoring,avoiding double gain.
Its weights and scalar remain stored untouched;both common weights and gain are frozen.
Capture post-core residual r before C278's dynamic normalizer hook,and read.output contribution a.
Install a late normalizer hook during local_encoder,after the original hook exists. Require exact
actual original normalizer input r+a on EVERY call,batch-by16 CPUfloat64 finite tensors and one
complete capture. Supply alpha*r+a,using the exact saved float64 alpha;unit gain returns None and
leaves the original input unmodified. All upstream core/reader computation remains;no speed claim.
Existing C278 provenance assertions remain active. Exception cleanup restores all forward/pre-hook
registries,including with-kwargs and always-call registries. No optimizer or backward pass is used.

Each of10 states uses fixed pass order original_before,swapped,original_after. Original labels:
fixed weights unit/trained/unit;learned weights trained/unit/trained. Every mode evaluates all
2/3/4 tasks,all profiles,TRAIN/HOLDOUT and normal/evidence-blind/query-blind views.
Both original passes reproduce C301 raw logits with maximum drift<=1e-9 and exact argmax;also
compare before/after. Full wrapper fingerprint,stored gain and hook registries stay unchanged.
C302 smoke directly compares original C301 wrapper outputs against the inner-model intervention
for BOTH parent arms,not only unit gain. Any baseline/restoration mismatch invalidates C302.

## Parent writer,adapter and dependencies

C301 scientific HEAD:d67c900c588ff0e4c8974cd8f80721da381a8770.
Publication:871d5c55a0cb8139a1ff95fbfce95b7472bf16fa.
Summary:runs/c301-v5b-residual-gain-8e72f4cf3e744128b905da20770c9f5b/summary.json.
Summary SHA256:19d5a94c3ce5d2bef94683b05983c44b1e76f452490e184f8ffde7b934d559c1.
C301 source blob:a1c2baa1762b57be32eff4b4b9828bd7e5da340f.
C278 readout blob:0aa8d65874f4a021e21d04948ffd0a1d5615248b.

Verify28 ordered summary hashes BEFORE C301.verify_artifacts with27 ancestors and accepted HEAD.
Tail hashes are C301.parent_hashes(C300). Require parent statusFAIL(valid negative),matched pairs,
strict replay,and original task counts fixed/learned two2/3,triple2/3,quad2/1. The exact summary
seals all8 artifact names/hashes/sizes;the exact verifier reconstructs all earlier contracts.
Read dataset/triple/quad from verified C301 files. Load fold-c301-gain-eval-v1 for final raw
prediction anchors. Its fit contains the FINAL trained gain,not a last-batch surrogate or a
coefficient picked from evaluation. adapt_anchors verifies identities,state metadata and gain
agreement with summary records. Model states use fold-c301-gain-models-v1 through its actual loader.

Sole direct import C301. Its context exposes C294 no-neural,C287 normalization,C284 evaluation/
replay_error,C283 quad,C282 tables and the original model/core bundle. All652 inherited source
pins/1202 protected inputs remain checked. Actual repository-local context/core helper files must
be pinned. Add OWN6 and9 C301 summary/artifacts:source658/protected1217. Accepted sources,tests,
logs,preregistrations and dispatchers are immutable;no parent monkeypatch or new exclusion.

## Reporting and unchanged gates

Keep30 state/pass results,180 final task/split partitions,10 reproduction receipts and5 exact gains.
Within-weight comparisons:unit->trained for each10 states,3 tasks,2 splits=60 aggregates.
Across-weight comparisons:fixed-trained weights->gain-trained weights at each2 coefficient labels,
5 seeds,3 tasks,2 splits=60 aggregates. Each family has25920 matched normal-row presentations;
combined51840. Both report exact flips,rescues,regressions and left/right correct counts.
Wrong-to-wrong changes are not rescues. Count four logical weight/gain conditions only ONCE;
original_after is a restoration control,not an additional model or independent observation.

All original thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Original-before/after task flags must exactly reproduce the respective parent,not merely aggregate
pass counts. Swapped-condition gates are descriptive. PASS means completed intervention,unchanged
states/hook restoration and saved reconstruction,NOT capability promotion. The original C301 all-five
negative and Gate F remain unchanged even if an off-diagonal passes every test.

## Workload,artifacts and execution gate

Training0.10 saved models*3passes*81forwards=2430 model forwards;233280 row presentations;
9720 core calls;10 strict model-state loads,one existing checkpoint bundle read,new checkpoints0.
Operational smoke uses2 original wrapper forwards plus6 inner intervention forwards outside science.
Old-artifact verification and regression fixtures are separate. No claim of zero inference.
Raw float64 output payload477757440 bytes plus metadata/serialization overhead;not peak-memory estimate.
Outputs:gain-plan.json,gain-evaluations.pt,measurements.json,validation-summary.json plus summary.json.
Child writes NO dataset copies or trained-model checkpoint. Archive fold-c302-gain-cross-eval-v1
stores all30 raw passes,original fingerprints,gain provenance,hook attestations and reproduction errors.
Full tensors/maps stay local/ignored. Compact console receipt and all aggregates are mirrored.
Numerical postcheck re-derives all gates,comparisons and baseline agreements under no-neural scope.

Own32/modules187/loaded4670/focused4669;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:283f4ac996eda2ac866a192408fff2368782b8592d350c11af33723f874f2960.
Commit/re-fetch/review all6 OWN before activation/command release. Require explicit UTF-8/CP932,
module/global binding audit,CLI indices,real production call ordering and loader/count tests.
Execute actual accepted C278 AND C301 class ASTs with controlled backbone/reader in an integration
fixture to verify both original gains and restoration;this is not actual FOLD capability testing.
Windows Validate requires all28 real parent archives/pins,both actual wrapper/inner smoke checks,
own32 and full4669 tests. Preserve dispatcher/launcher/runner ParseFile chain.
Validate failure skips science/publication. Integrity failure repairs SAME C302 with fixed conditions.
C303 remains unregistered until C302 formal judgment. No best coefficient or model selection.
