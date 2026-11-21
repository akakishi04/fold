# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C292 ACCEPTED PASS (diagnostic integrity only). C293 ACTIVE / NOT YET JUDGED. C294 NOT REGISTERED.**
Latest accepted scientific execution:4e7d4468a103fa70dcfaee719fcf6daa75af5b7e.
Latest accepted published log:513f820c494e067e67d1c3757af09cf7642b0b90.
C291 remains ACCEPTED VALID NEGATIVE. No rerun or Gate F promotion.
C293 is the unique ACTIVE fact-support loss reweighting experiment.

## Latest accepted evidence — C292

Acceptance:docs/experiment-ledger-addendum-c292-c293.md.
Acceptance commit:b6e90c80768c48a999f253cfa5b3cced29b465aa.
Summary:runs/c292-v5b-answer-roles-ba65b6ac20ac46e5b08fe96a5e5a8e74/summary.json.
Summary SHA256:44aa5ddbe5856ffdd7a62f63ac7574367527fab17c447c02ca68f7071e9ae513.
Manifest:f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.
Own32/focused4317 PASS;source598/protected1081;run_execution_valid=True.
38880 saved normal answers classified;scientific neural calls/training0.
Candidate291003 HOLDOUT errors at lengths2/3/4:63/72/77;absent known values62/71/72;
other-fact values1/1/5;non-value bytes0/0/0. Of212 errors across these partitions,205 are absent.
CE291003 absent/other errors:two112/11,triple110/13,quad113/18.
Both CE and candidate fit all original two/three TRAIN normal answers on that seed.
This does not prove memorization or a hidden retrieval failure;partitions are dependent observations.
Parent quad gates stay CE4/pair2/answer4. No capability or Gate F promotion from diagnostic PASS.

## Active C293 — fact-support component reweighting

Experiment:C293-v5b-fact-support-loss. Stage:V5-B-FACT-SUPPORT-LOSS.
Registration:docs/experiment-ledger-addendum-c293-preregistration.md.
Design:docs/v5b-fact-support-loss-v0.1.md.
Review:docs/c293-post-authoring-review.md.
Acceptance base:b6e90c80768c48a999f253cfa5b3cced29b465aa.
Authoring/review target:40b12de5ba46e9d5f3b89efaed006d293f764daa.

One question:does selectively upweighting CE's fact-support component improve reliable unseen
four-character transfer versus ordinary CE and uniform CE scaling,at the same training budget?
Fresh seeds293001..293005;three concurrent arms per seed:
-ce_only:CE;
-scaled_ce:1.25*CE;
-support_weighted(candidate):CE+.25*Lsupport.
For the existing intact query pair,S={y0,y1} is the unordered set of the two stated fact values.
Lsupport=mean_row(logsumexp_all256-logsumexp_supported2).
Lchoice=mean_row(logsumexp_supported2-target_logit). CE=Lsupport+Lchoice.
Candidate weights support1.25 and conditional choice1. The scaled arm weights both1.25.
Both labels already occur in the original TRAIN minibatch. They are used only in the supervised
loss;no labels,pair metadata,support masks or parser output enter model.forward or its decoder.
All three arms still predict all256 classes without filtering or correction.

Actual C278 all-token MeanFinalDualReadout,14256 parameters,48tokens,CPUfloat64,2threads,deterministic.
Three independent identical initial states,shared batch/rendering/LR schedules and first-input
loss components are checked. Normal length2/3 TRAIN only;no HOLDOUT,quad or ablated optimization.
192 logical rows/96 intact pairs;24pairs per batch;200epochs*4=800updates/model.
randperm96(seed+293000+epoch);profile=epoch%3;length=epoch%2;fit RNGseed+294000 reset per arm.
Each row sees100 repetitions at each length;length/profile updates[[136,132,132],[132,136,132]].
AdamWlr.005,betas.9/.999,eps1e-8,weight_decay0,clip1;one optimizer800uninterrupted updates.
No coefficient sweep,architecture change,extra data,early stopping or checkpoint selection.

The parent is C292's diagnostic,not a model checkpoint. Verify19 ordered summary hashes before
calling C292.verify_artifacts with18 ancestor paths and its accepted execution HEAD. Three C292
output descriptors are fixed from its publication. Recursive verification reconstructs all older
gates. Read already-verified C291 data/triple/quad JSONs and recheck canonical hashes. All new
models start from scratch. Only direct repository import:C292;its used context modules must be
in the inherited source map. No accepted helper,source,test or log is patched.

Freeze final states,evaluate unchanged2/3/4 normal/evidence-blind/query-blind tasks,strict-load
and replay all views with max drift1e-9 and exact argmax. Primary PASS iff all5 support_weighted
models pass every original FOUR-character fixed criterion. Thresholds:accuracy.90,query_pair.80,
evidence_drop.35,query_drop.35,two_order.80. No pooled or role-count substitution for the gate.
Save all seen/all-task/direct TRAIN/HOLDOUT flags,90 partitions with original output-role counts,
and360 candidate-versus-each-control contrasts. Role and scorer correct counts must agree.

This is selective CE reweighting,not new supervision information or a hard support constraint.
Lsupport can be small while the other fact wins. The scaled control exposes uniform amplification
but is not an exact gradient/AdamW/clipping match. Findings do not establish a hidden cause or
automatic superiority,arbitrary-length competence,production adoption,or Gate F completion.

Work:15models,12000updates,576000training rows,14430forwards,809280row presentations,57720core calls,
one15-state checkpoint bundle write/load,15strict state loads,network0. Operational tests excluded.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus full summary.json. Keep all800
CE/support/choice/total/LR histories and frozen raw logits. Compact console receipt+aggregates;
full protected maps and tensor artifacts remain local/ignored. No historical logger changes.
Source604/protected1091:all598 parent sources+OWN6;all1081 inputs+4 parent inputs+OWN6.
Own40/modules178/loaded4358/focused4357. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:0aadd3137b216f6e0fbc37feffe8b0ad947e48eeb22da881f38e58ee38a424f7.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local behavioral fixtures).
All6 OWN files re-fetched at40b12de5ba46e9d5f3b89efaed006d293f764daa and whole-file blobs matched6/6.
After matching:normal own40 PASS in6.819s;entire CP932-emulated own40 PASS in6.799s.
Linux/Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;unresolved
globals0;UTF-8/no-NUL;manifest digest matches. Fixtures exercise real800-update loops on small
synthetic classifiers,objective decomposition/gradients,matching,roles,parent hashes,protection,
run order,persistence/tampering and semantic suite filtering. Toy inputs encode synthetic label
identity;this is control/numerical verification,not evidence of FOLD binding/generalization.
Parent archives,Git,inherited models/scorers and suite members are mocked where needed.
Not executed here:real Windows artifacts/pins,PowerShell parsing,full4357 regression,real-model
preflight and actual15-model experiment. These remain mandatory guarded Validate/Execute gates.
Activation must not modify reviewed OWN6 or any accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C293 -> Validate(19parent hashes,
604/1091 protection,real tables/all5schedules/three initial models,loss decomposition/gradient
check,own40,focused4357) -> authoring_runtime_preflight=PASS -> Execute(15models*800updates,
frozen3task scores,strict replay,roles and persisted reconstruction) -> log publication.
Validate failure skips science/publication. Scientific integrity failure retries SAME C293.
Valid all-five miss is ACCEPTED VALID NEGATIVE. Do not retune weights,seeds,budget,LR or thresholds
after results. C294 is unregistered until C293 formal judgment. Gate F remains NOT PASSED.
Scientific execution HEAD must remain distinct from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c292-pre-acceptance.md.
Its Git blob is43e27532c735595d9a2c1c8b5f189093f4a595ba. Older handoffs remain unchanged.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.
