# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C281 ACCEPTED PASS (diagnostic integrity only). C282 ACTIVE / NOT YET JUDGED. C283 NOT REGISTERED.**
C281 scientific execution HEAD:96d02062bf98cf32cfc5173c36db28bb00960f0d.
C281 published log commit:e3b5bd2e67da32ccfdff4f7503a99d364f4b76ec.
C280 remains ACCEPTED VALID NEGATIVE. No rerun,seed exclusion,support retuning or Gate F promotion.
C282 is the unique ACTIVE training-distribution experiment,not an unseen-length capability closure.

## Latest accepted science — C281

Acceptance:docs/experiment-ledger-addendum-c281-c282.md.
Acceptance commit:d54a8d5a775949ccb54dae6ebc9e934c7579c8f5.
Summary:runs/c281-v5b-saved-support-audit-674eda46d9634e258004cabe55550065/summary.json.
Summary SHA256:f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7.
Manifest SHA256:ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False. Own32/focused3917 and persisted reconstruction PASS.
Scientific model forwards,training,state loads and checkpoint writes0.

All triple criterion failures control->candidate:
accuracy92->85 (23 rescue,16 introduced);query_pair92->85;evidence_drop45->29;
query_drop58->43;two_order34->33. Criteria overlap.
Mask-only failing answer cells0 in both arms on both tasks. Direct answer discrimination remains.
Evidence-drop net improvement-16 is dominated by280004 (-18),while other seeds worsen+2.
Triple normal answers3960/4320->3973/4320;both arms evidence_blind1080/4320.
Do not infer identical ablated predictions or a unique causal mechanism from pooled counts.

## Active C282 — fixed-budget length coverage

Experiment:C282-v5b-mixed-length-training.
Stage:V5-B-MIXED-LENGTH-TRAINING.
Registration:docs/experiment-ledger-addendum-c282-preregistration.md.
Design:docs/v5b-mixed-length-training-v0.1.md.
Review:docs/c282-post-authoring-review.md.
Acceptance base:d54a8d5a775949ccb54dae6ebc9e934c7579c8f5.
Initial OWN6 commit:3cbb0f3ba3874f4ab1bb4ebbe396c441f83cbefa.
Final review target:7f6432bb2d40bc7ec19561b561c1b9f0fd9db5f2.

One question:at identical architecture and800 updates/model,does alternating two-character and
three-character TRAIN renderings improve both-task reliability over two-character-only training?

Fresh seeds282001..282005;arms two_char_only,mixed_length;actual C278 all-token MeanFinalDualReadout
in both arms.14256 parameters;identical initial state keys/values;independent storage.
No evidence-only support mask,extra head,loss,LR,training-step or gate change.

Use same192 logical TRAIN rows and96 paired groups.200 epochs x4 batches x48 rows.
Logical batches identical within seed;randperm96(seed+282000+epoch);profile=epoch%3.
Control:length0 only. Candidate:length=epoch%2;0=two-character,1=three-character.
Logical row exposure200 in both;control200/0 and candidate100/100 by length.
Length/profile matrices:[[268,268,264],[0,0,0]] and [[136,132,132],[132,136,132]].
AdamW lr.005,CE only,CPU float64,2 threads,deterministic;fit RNGseed+283000.

C267/C270 scorers,thresholds and HOLDOUT value assignments unchanged.
Candidate PASS requires all5 mixed_length states pass both complete tasks. Control separate.
Critical boundary:candidate sees three-character TRAIN names;PASS is seen-length/held-out-value-
combination learning,NOT the original unseen-length transfer claim. Gate F remains NOT PASSED.

Workload:10 models,8000 updates,384000 training rows,9080 total forwards,487680 row presentations,
36320 core calls,one10-state checkpoint bundle write/load,10 strict state loads.
Registration:source538;protected950;dependency-union58;own32;modules167;loaded3950;focused3949.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Review target:7f6432bb2d40bc7ec19561b561c1b9f0fd9db5f2;OWN6 identities match tested bytes6/6.
Local Linux/Python3.13.5/PyTorch2.10.0+cpu:own32 PASS,final run3.802s;embedded Python compiles;
unresolved global names0. Parent archives/scorers/model calls are mocked in relevant fixtures;
fit selection smoke uses a tiny toy model. This is NOT real C282 scientific training.
Actual parent verification,real training-table/model construction,full focused3949,PowerShell
ParseFile and actual10-model train/evaluate/replay remain authoritative runtime gates.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after ParseFile on dispatcher.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C282 -> Validate(parent532-derived
source/artifact538/950,real TRAIN tables/initial models,own32,focused3949) ->
authoring_runtime_preflight=PASS -> Execute(10 models,both tasks,strict replay,persisted postcheck)
-> log publication.

Validate failure skips science and scientific log publication. Execute integrity failure retries
SAME C282. A valid gate miss is ACCEPTED VALID NEGATIVE. No seed replacement,extra steps,revised
length schedule or C283 registration before formal judgment. Never relabel seen-length PASS as
unseen-length transfer or automatic Gate F completion.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Historical state and recovery

Previous complete handoffs are preserved at docs/handoff-history/c280-pre-acceptance.md and
 docs/handoff-history/c281-pre-acceptance.md. Their ACTIVE instructions are historical only.
C279 remains ACCEPTED PASS (diagnostic integrity only);C278/C280 remain ACCEPTED VALID NEGATIVE.
Accepted source/tests,preregistrations,logs and protected dispatchers are unchanged.
