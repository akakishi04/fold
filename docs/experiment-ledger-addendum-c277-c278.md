# C277 acceptance and C278 mean-plus-final query boundary

## Formal verdict

C277 ACCEPTED PASS for diagnostic integrity only. This is NOT a capability PASS and does not promote
Gate F. The saved C276 learning-rate failure-profile audit completed exactly as preregistered with
zero neural Module calls,zero training and zero checkpoint writes.

Scientific execution HEAD:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
Published log commit:7a46048503459aa7e03982b22c8dc8cf5ad2f976.
Publisher log SHA256:642c82bcaaf4b6b9b2b7a4b28f0ee9026b77b2bfb3f117082a9efd48ebff1e27.
Publisher log bytes:772797.
Git normalized log blob:f9227cc8749b271585dca237249bc7a136b15198.
Summary:runs/c277-v5b-saved-lr-audit-7e9cad9663144ae9bdbacda802c21306/summary.json.
Summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.

## Execution validity

The pre-science runtime gate passed:parent/source/artifact precheck508/892,sealed manifest
50796e76783611eb04649fd47c450f3fe47d05a34fc0c787168fa38e612d8de9,own24 PASS and focused3813 PASS.
C277 reconstructed accepted C276/C275/C274 evidence with neural Module calls blocked.
model_forward_calls=0;row_presentations=0;core_forward_calls=0;train_steps=0;
new_checkpoint_writes=0;model_state_loads=0.
Persisted audit-plan/failure-profile/validation-summary reconstructed exactly.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False.

## Primary learning-rate attribution

Across all C276 triple fixed records,candidate-minus-control failure-count deltas are:
-accuracy:-37;
-query_pair_accuracy:-37;
-two_order_accuracy:-18;
-evidence_drop:+3;
-query_drop:+1.

Thus lr0.0025 substantially reduces answer/query-pair/two-order failures overall,but slightly
increases mask-drop failures overall.

The overall improvement is highly concentrated in seed276003:
-seed276003 accuracy:-38,query_pair:-38,evidence_drop:-9,query_drop:-14,two_order:-21.

Across the other four stable/control-good seeds276001/276002/276004/276005,the candidate changes are:
-accuracy:+1;
-query_pair:+1;
-evidence_drop:+12;
-query_drop:+15;
-two_order:+3.

Therefore lower lr is not a general reliability improvement across already-stable seeds. It mainly
rescues one broad failure while degrading several fixed criteria in the rest of the cohort.

## Shared-suffix attribution

For shared_suffix2 HOLDOUT,candidate-minus-control failure-count deltas:
-accuracy:-7;
-query_pair_accuracy:-7;
-two_order_accuracy:-5;
-evidence_drop:+4;
-query_drop:+5.

For shared_suffix2 TRAIN:
-accuracy:-4;
-query_pair_accuracy:-4;
-two_order_accuracy:+1;
-evidence_drop:+4;
-query_drop:+6.

So lower lr improves direct answer/query discrimination on shared-suffix prompts but weakens the
registered evidence/query ablation sensitivity. This explains why better pooled answer totals do
not become complete task PASS.

Per-seed triple deltas are heterogeneous:
-276001 worsens every reported criterion class;
-276002 worsens every reported criterion class;
-276003 improves every criterion class strongly;
-276004 improves all present criterion classes;
-276005 improves answer/query-pair but worsens evidence/query-drop and slightly two-order.

## Scientific interpretation

C277 weakens the hypothesis that simply lowering the optimizer step size is the next general
solution. The C276 candidate's apparent aggregate improvement is dominated by recovery of one broad
bad seed. The remaining shared-suffix problem shows a representation/decision tradeoff:direct
answer discrimination can improve while dependence on the registered evidence/query channels
becomes weaker.

The next intervention should therefore return to query representation rather than continue an LR
sweep. C269 mean-span pooling was the strongest bounded two-character result and retained useful
three-character suffix behavior;C274 final-boundary was broadly stronger than first-boundary.
The untested combination is to keep the MEAN span signal and FINAL causal boundary signal separate
through attention,then combine retrieved memories. This is distinct from C273's first+final dual
attention and from C272's pre-attention boundary averaging.

## Non-claims

Do not claim lr0.0025 is better overall. Do not infer that seed276003 should be discarded or that
mask sensitivity alone is the problem. Do not try another LR from C277. C277 is a saved diagnostic,
not a capability ranking.

## Accepted artifacts

-audit-plan.json:50796e76783611eb04649fd47c450f3fe47d05a34fc0c787168fa38e612d8de9;2250 bytes.
-failure-profile.json:f1a0f3e087f3ecc3afafaa56d600168018572e7450c0f79204ed5a6d6d972acc;132564 bytes.
-validation-summary.json:b8ac20e2a2ac7ea2c6306f71d6f121580cb2d0c635b92605263e2e759c76a9db;668 bytes.

## Next question, not activation

With identical fresh paired CE training,does keeping the C269 mean query-span signal and the final
visible query-boundary signal separate through their attention softmaxes,then averaging the two
retrieved memories,improve reliable two/three-character binding relative to mean-span attention alone?

C278 should compare:
-mean_span:actual C269 SpanQueryReadout;
-mean_final_dual:same14256 parameters/state keys/matched initialization;one query from the mean
 visible query-span pre-core state and one from the final visible query-byte pre-core state;shared
 read.query/read.key/read.output;separate masked softmaxes;average retrieved memories before the
 single read.output/post-core residual boundary.

Fresh seeds278001..278005. Use the exact paired two-character CE training policy,800 updates and the
same C267/C270 evaluation gates. No extra parameters,loss term,training steps or learning-rate
change. Primary candidate PASS requires all five mean_final_dual states to pass both complete tasks.
The mean_span arm is matched control only.

A valid miss must be accepted without another fusion tweak inside C278. C278 requires separate
preregistration,implementation,final manifest sealing,committed-byte review and runtime Validate.
C279 NOT REGISTERED.
