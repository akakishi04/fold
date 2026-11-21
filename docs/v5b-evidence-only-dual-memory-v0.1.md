# V5-B evidence-only dual memory support v0.1 — C280

C279 shows that C278's mean/final dual-query intervention improves every registered three-character
criterion overall,but shared_suffix2 is asymmetric: direct answer/query-pair,query-drop and two-order
failures improve while evidence-drop failures increase.

C280 tests one mechanism only. C278 forms query vectors from the mean visible query span and the final
visible query byte,but both attention softmaxes can retrieve key/value states from every valid token,
including the visible query tail itself. This permits query-local memory retrieval.

The C280 candidate keeps the C278 query vectors,parameters,weights,softmax count,memory averaging and
post-core residual boundary unchanged. It changes only the key-value support mask: both attention
softmaxes may attend to valid positions strictly before the first visible query byte. Because the
query begins immediately after the final semicolon,the evidence support includes that separator and
all preceding fact states,while excluding query bytes,the final equals,EOS and padding.

This is deliberately not a first-boundary retry. C274 showed first-boundary query vectors were weak.
C280 still uses the C278 mean/final query vectors; only the memory source is evidence-only.

The hypothesis is that preventing query/self-token retrieval will increase causal dependence on fact
values,especially on shared_suffix2 where the final query byte is non-discriminating,without losing
C278's shared_prefix2 improvements.

A negative result is informative. If evidence-only support does not improve the fixed all-five gate,
the residual cannot be attributed to all-token memory support alone. No profile-specific routing,
extra head,auxiliary loss,LR change,training extension or threshold change is allowed inside C280.
