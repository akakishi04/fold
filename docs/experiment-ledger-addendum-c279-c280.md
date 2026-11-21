# C279 acceptance and C280 evidence-only memory support

## Formal verdict

C279 ACCEPTED PASS for diagnostic integrity only. This is NOT a capability PASS and does not promote
Gate F. The saved C278 failure-profile audit completed exactly as preregistered with zero neural
Module calls,zero training and zero checkpoint writes.

Scientific execution HEAD:b07425eddfab2d4f3f6bacd8dff02295b44f3063.
Published log commit:ad5eed44f8ba66d29cda9627d54245b56fb8ff13.
Publisher log SHA256:9ca0ebbc237727c92b2d321b0b4feffd742b39e57d6e5ee6e9750a8ae5f0825e.
Publisher log bytes:785160.
Summary:runs/c279-v5b-saved-dual-audit-e6d76ea781994de085b16ea8e7a6b972/summary.json.
Summary SHA256:a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb.

## Execution validity

The pre-science runtime gate passed:parent/source/artifact precheck520/916,sealed manifest
daeea4cfcf5083ec9a5237ea092f0c11ac7ab3cf38b76e9cdf62f60c4fea1af7,own24 PASS and focused3861 PASS.
C279 reconstructed accepted C278/C277/C276/C275/C274 evidence with neural Module calls blocked.
model_forward_calls=0;row_presentations=0;core_forward_calls=0;train_steps=0;
new_checkpoint_writes=0;model_state_loads=0.
Persisted audit-plan/failure-profile/validation-summary reconstructed exactly.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False.

## Deciding metrics

All triple candidate-minus-control failure-count deltas:
-accuracy:-78;
-query_pair_accuracy:-78;
-two_order_accuracy:-39;
-query_drop:-49;
-evidence_drop:-10.

The candidate therefore improves every registered criterion overall.

shared_prefix2 HOLDOUT candidate-minus-control:
-accuracy:-29;
-query_pair_accuracy:-29;
-two_order_accuracy:-14;
-query_drop:-17;
-evidence_drop:-10.

shared_suffix2 TRAIN:
-accuracy:-12;
-query_pair_accuracy:-12;
-two_order_accuracy:-4;
-query_drop:-3;
-evidence_drop:+4.

shared_suffix2 HOLDOUT:
-accuracy:-9;
-query_pair_accuracy:-9;
-two_order_accuracy:-8;
-query_drop:-7;
-evidence_drop:+5.

Exact candidate triple failure counts remain:
-accuracy34;
-query_pair_accuracy34;
-two_order_accuracy12;
-query_drop15;
-evidence_drop12.

For shared_prefix2 HOLDOUT the candidate has only3 accuracy,3 query-pair,1 query-drop and1 two-order
failures,with zero evidence-drop failures. For shared_suffix2 the candidate retains both direct
discrimination failures and a distinctive evidence-drop regression.

Per-seed triple evidence-drop candidate-control:
-278001:0 versus0;
-278002:0 versus3;
-278003:4 versus3;
-278004:8 versus6;
-278005:0 versus10.

Thus the evidence-drop regression is localized to seeds278003/278004 rather than universal.

## Scientific interpretation

C279 rejects a simple claim that mean_final_dual merely trades one broad criterion for another:
overall it improves every fixed criterion substantially. The remaining failure is narrower.

The key asymmetric result is shared_suffix2. Its final query byte is shared by both competing
three-character identifiers,while shared_prefix2 retains a discriminating final byte. C278 uses the
final query state as one of two query vectors and allows both attentions to read every valid token,
including the query itself. A plausible remaining mechanism is therefore query/self-token retrieval:
the final-boundary branch can retrieve query-local representations that are predictive enough to
answer but insufficiently dependent on fact values,which appears as evidence_drop failure.

The next intervention should test this mechanism directly without changing the query vectors.
Restrict both mean/final attention key-value support to the evidence segment before the visible query
bytes,while keeping the same14256 parameters,dual queries,shared read weights,post-retrieval averaging,
training policy and fixed gates.

## Non-claims

Do not claim evidence self-attention is proven causal from C279 alone. Do not add a new loss,
profile-specific routing,query metadata,extra parameters,another LR or longer training. Do not infer
that shared_suffix2 evidence_drop is the only residual issue;direct accuracy/query-pair failures also
remain. Gate F remains NOT PASSED.

## Accepted artifacts

-audit-plan.json:daeea4cfcf5083ec9a5237ea092f0c11ac7ab3cf38b76e9cdf62f60c4fea1af7;2457 bytes.
-failure-profile.json:b35020a8e440925599ea2c1ddf8b1b07a1f2c18a9ca53a11195f9a0f7085e7c4;104844 bytes.
-validation-summary.json:0514f2a64c1726e8765f86420bd8b2741c800df000da93f3a69ccaa1364de732;978 bytes.

## Next question, not activation

With identical fresh paired CE training,does keeping C278's mean/final query vectors but restricting
both attention softmaxes to evidence positions before the visible query bytes improve reliable
two/three-character binding relative to C278's all-valid-token memory support?

C280 should compare:
-all_token_dual:actual C278 MeanFinalDualReadout;
-evidence_only_dual:same14256 parameters/state keys/matched initialization and identical mean/final
 query vectors;same read.query/read.key/read.output;the only change is attention support. Candidate
 keys/values may attend only positions before the first visible query byte,including the final
 evidence/query separator semicolon and excluding visible query bytes,final equals,EOS and padding.
Both masked softmaxes remain separate and retrieved memories are averaged before one read.output.

Fresh seeds280001..280005. Use the exact paired two-character CE training policy,800 updates and the
same C267/C270 evaluation gates. No extra parameters,loss term,training steps or learning-rate change.
Primary candidate PASS requires all five evidence_only_dual states to pass both complete tasks.
The all_token_dual arm is matched control only.

A valid miss must be accepted without changing the support boundary inside C280. C280 requires
separate preregistration,implementation,final manifest sealing,committed-byte review and runtime
Validate. C281 NOT REGISTERED.
