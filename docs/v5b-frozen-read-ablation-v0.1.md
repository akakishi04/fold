# V5-B frozen read-path ablation v0.1 — C249

## One question

On the accepted C248 final checkpoints,does original-input performance depend on the added
residual branch and,on reader models,on learned nonuniform token weighting?

C248's reader passed all TRAIN/HOLDOUT criteria in8/12 seed/family/language cells,but missed4/12.
The equal-parameter EOS adapter missed all12 HOLDOUT cells. Keep that formal negative and the
successful cell-level evidence. Before changing the architecture again,measure the computation
used by all twelve trained models,including unsuccessful readers and EOS controls.

## Frozen interventions

Inputs,targets,row order,checkpoint state and original model code remain fixed. Instantiate the
actual C248 ReadoutPilot and load the accepted final state strictly. All parameters have
requires_grad=False,all gradients are absent,and the complete model is in evaluation mode.

1. Intact:run each original normal/evidence_blind/query_blind input on TRAIN64 and HOLDOUT32.
   Reproduce C248's saved final metrics and all prediction arrays before any intervention.
2. residual_off,both arms:the head output delivered to the existing readout normalization is h,
   the original pooled EOS state,instead of h plus the trained residual. The rest of the trained
   backbone/normalization/decoder remains unchanged.
3. uniform_read,reader only:replace learned softmax weights with a uniform distribution over the
   same nonPAD slots. Deliver h+Wo*mean(H_nonPAD),retaining trained token states and trained Wo.
   BOS/EOS and question bytes remain eligible,exactly as in C248. Never include PAD states.
4. Restored:remove the temporary intervention and rerun all three original views on both splits.
   Predictions must return exactly;raw logits must match the first intact pass within1e-9.

Interventions2/3 are scored only on normal input. Do not fabricate mask-drop measurements for
those interventions. Both raw normal logits and normal accuracy/NLL/fact/query/order metrics
are retained. Report answer flips,lost/gained correct answers,accuracy drop,NLL change and raw
logit drift separately for every model,split and language.

The scientific implementation uses scoped head forward hooks to replace the returned residual
representation. Original head computation still executes before replacement;uniform mode also
performs an output projection. This is not a speed-optimized ablation and makes no timing/FLOP
advantage claim. Hooks do not modify parameters;removing them restores the original forward.
No context or cache is shared across models. Only CPU/NEXT-only task inputs are supported.

## Interpretation

A loss after residual_off shows dependence on the added branch in that already-trained network.
It does not say an independently trained backbone-only model would have the same loss:the backbone
and branch were jointly trained. Uniform-read loss shows sensitivity to the learned read weighting
rather than unweighted pooling in that frozen network. It does not identify the correct semantic
entity/value relation or prove that a model trained with uniform pooling could not succeed.

Residual removal and uniform replacement change internal representations outside their trained
computation. Co-adaptation,scaling and normalization can contribute to an effect. Equal scores do
not imply identical logits or absence of a training-time benefit. This is not a seed-reliability
experiment or a fresh held-out dataset. Do not select only successful C248 seeds or claim broad
language ability,unique learning causes,core superiority or production readiness.

## Fixed accounting and gate

Each of6 token readers:6 intact forwards +2 off +2 uniform +6 restored =16 forwards/768 rows.
Each of6 EOS controls:6 intact +2 off +6 restored =14 forwards/672 rows.
Totals180 full-model forwards/8640 row presentations. One accepted bundle is deserialized into
12 states;no new checkpoint or optimizer is written. Additional training steps0.

Store5184 rows of raw logits:intact and intervened outputs only. Restored outputs are checked
online;their replay-error/identity results are stored rather than duplicating the restored arrays.
There are72 normal contrast cells:6 reader models x2 modes x2 splits x2 languages plus6 controls
x1 mode x2 splits x2 languages. Postcheck recomputes all retained metrics/contrasts from stored
logits without additional model forwards. File/JSON and historical regression costs are separate.

C249 PASS means diagnostic integrity only,regardless of ablation effects. Require accepted
state/input/source identities,original prediction/metric replay,unchanged weights/tokens,hook
cleanup,restoration replay,fixed workload and persisted-output recomputation. An integrity fault
is INVALID / RETRY SAME C249. C248 remains a valid negative and Gate F remains NOT PASSED.

Five ignored artifacts:ablation-plan.json,logits.json,diagnostics.json,contrasts.json,
validation-summary.json. No accepted source/test/log is changed. No training,seed replacement,
threshold relaxation,production adoption,external data,paid API,cleanup or history rewrite.
Judge C249 before registering C250. Numeric-memory and erasure-mixture tuning remain paused.
