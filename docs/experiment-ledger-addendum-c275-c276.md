# C275 acceptance and C276 optimization-reliability boundary

## Formal verdict

C275 ACCEPTED PASS for diagnostic integrity only. This is NOT a capability PASS and does not promote
Gate F. The saved C274 gate-failure attribution completed exactly as preregistered with zero neural
Module calls,zero training and zero checkpoint writes.

Scientific execution HEAD:3cd34c37a4329f8b8a030f320f1eeefa303706e4.
Published log commit:9308dc7fac2a6e298f2e2dbb1b02b9caf2d96649.
Publisher log SHA256:7e4a6a5d7d92b92a186a4ac260dc49bd5f3acfa3765c12b1e346eedfadf12ba6.
Publisher log bytes:759306.
Git normalized log blob:750ec589ad7d51f35786b6befd547380c4a443cb.
Summary:runs/c275-v5b-gate-failure-audit-fb5be8dc32064545aa7a993b70e50706/summary.json.
Summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb.

## Execution validity

The pre-science runtime gate passed:parent/source/artifact precheck496/868,sealed manifest
18af6d20c41fbb2e0bff672ac4e82e9e06eb324bc9c56ef53f409621ac95e102,own24 PASS and
focused3765 PASS. C275 then verified and reconstructed accepted C274 artifacts with neural Module
calls blocked. model_forward_calls=0;row_presentations=0;core_forward_calls=0;train_steps=0;
new_checkpoint_writes=0;model_state_loads=0. Persisted audit-plan/failure-audit/validation-summary
reconstructed exactly. run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False.

## Primary final-boundary triple attribution

C274 final_boundary triple produced100 failing fixed records across all five seeds.
Criterion counts across those100 records:
-accuracy:69;
-query_pair_accuracy:69;
-evidence_drop:43;
-query_drop:33;
-two_order_accuracy:31.

Negative-margin ranges:
-accuracy:-0.65 to -0.025;
-query_pair_accuracy:-0.80 to -0.05;
-evidence_drop:-0.35 to -0.0375;
-query_drop:-0.35 to -0.0375;
-two_order_accuracy:-0.55 to -0.05.

Failure-record split:
-near-passing seeds274001/274002/274004/274005:23 records;
-broad seed274003:77 records.

Per-seed criterion counts:
-274001:accuracy4,query_pair4,evidence_drop3,query_drop3,two_order2;
-274002:accuracy4,query_pair4,two_order1;
-274003:accuracy52,query_pair52,evidence_drop40,query_drop28,two_order25;
-274004:accuracy6,query_pair6,query_drop2,two_order3;
-274005:accuracy3,query_pair3.

The near-passing cohort therefore does NOT fail primarily because of mask-drop criteria.
Every near-passing seed has answer-accuracy and query-pair failures. Mask-drop failures are absent
for274005 and evidence/query-drop failures are absent for274002. The broad seed274003 fails every
criterion class heavily.

Profile-level counts also show the problem is not confined to a single name profile. HOLDOUT
shared_suffix2 has the most answer/query-pair failures, but tripled and shared_prefix2 also contain
failures. TRAIN shared_suffix2 remains a major contributor.

## Scientific interpretation

C275 narrows the unresolved issue substantially. For the four near-passing final-boundary states,
the common failure signature is answer discrimination plus paired-query discrimination,not merely
insufficient evidence/query masking effects. Therefore an intervention that only changes mask-drop
behavior would not address the shared failure mode.

At the same time,C273 seed273001 and C274 seed274005 demonstrate that the current small architecture
can reach very strong or locally complete answer behavior. The large variation across fresh seeds,
together with seed274003's broad failure and the nonzero near-seed answer/query-pair failures,
suggests optimization reliability is now a first-class hypothesis rather than adding more query
fusion machinery immediately.

This is still not proof that optimization alone is the cause. A controlled training-policy
comparison is required.

## Non-claims

Do not declare final_boundary a winner from C275. Do not relax the fixed gates,discard seed274003,
select a passing seed,or increase training after seeing results. Do not conclude that mask-drop
criteria are irrelevant;they still fail in several seeds and profiles. C275 only establishes that
answer/query-pair failures are common to all four near-passing final-boundary seeds.

## Accepted artifacts

-audit-plan.json:18af6d20c41fbb2e0bff672ac4e82e9e06eb324bc9c56ef53f409621ac95e102;2126 bytes.
-failure-audit.json:b28b93768e979295e9b2294d150c6c6c29ec9943ef9f42b5496de023cfa83c0f;364517 bytes.
-validation-summary.json:d6d4992f9ba626609d580664e4ec064b4f14003430cd74dc988a6c51cb627cab;506 bytes.

## Next question, not activation

Does a more conservative fixed optimizer step size improve fresh-seed reliability of the
final_boundary architecture without changing architecture,data,loss,steps or evaluation gates?

C276 should compare fresh matched final_boundary models under two fixed learning rates:
-control lr0.005:the accepted C274 policy;
-candidate lr0.0025:exactly half the step size.

Use fresh seeds276001..276005,identical initialization and identical paired batch order per seed.
Keep AdamW betas/eps/weight_decay,global clip1,800 updates,CE-only loss,the C267 two-character data
and C270 three-character evaluation unchanged. Do not add training steps or select checkpoints.

Primary capability candidate PASS requires all five lr0.0025 states to pass both the original
two-character and complete three-character fixed gates. lr0.005 is the matched control and cannot
rescue the candidate.

This tests the optimization-reliability hypothesis directly. A valid miss must be accepted without
trying additional learning rates inside C276. C276 requires separate preregistration,implementation,
final manifest sealing,committed-byte review and runtime Validate. C277 NOT REGISTERED.
