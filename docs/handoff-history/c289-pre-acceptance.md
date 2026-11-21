# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C288 ACCEPTED VALID NEGATIVE. C289 ACTIVE / NOT YET JUDGED. C290 NOT REGISTERED.**
C288 scientific execution:f43618b6bb6fcc1ad4a4a4b928992adce29f4e41.
C288 published log:eb9f27224460ad614e80b5feb23a5411d8ea42d6.
C287 remains ACCEPTED PASS (diagnostic integrity only). Do not rerun C288 or filter its seeds.
C289 is the unique ACTIVE early auxiliary withdrawal comparison with two concurrent anchors.

## Latest accepted science — C288

Acceptance:docs/experiment-ledger-addendum-c288-c289.md.
Acceptance commit:4acd3873a4f524ceb3080aab10653cd13caaa1c4.
Summary:runs/c288-v5b-pair-assignment-f6a7427e94c44fc7b818f8cd18626562/summary.json.
Summary SHA256:2a15fbf6c5e697d5e226bdae5a5b2f243f43625b29255839100d2f05ce24fbc0.
Manifest SHA256:44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False. Own40/focused4157 PASS.
Source574/protected1026. Work:10 models,8000 updates,384000 training rows,9620 forwards,
539520 row presentations,38480 core calls. Strict replay and persisted reconstruction PASS.

Quad primary ce_only3/5,ce_pair_assignment1/5;two3/3;triple3/3;all tasks3/1.
Trained-length TRAIN direct3/5 versus5/5;seen-length HOLDOUT direct3/5 versus3/5.
Candidate fits all normal TRAIN examples at both lengths2/3 exactly with no collapse,but288002/
288003 still fail seen-length HOLDOUT. Candidate loses quad gates288001/288004;only288005 passes.
Pooled quad correct3902->4011 of4320;collapse175->90 of2160. Pooled improvement does not undo
strict reliable-gate regression. Do not claim universal transfer degradation or an adopted solution.

## Active C289 — early pair-loss withdrawal

Experiment:C289-v5b-early-pair-withdrawal. Stage:V5-B-EARLY-PAIR-WITHDRAWAL.
Registration:docs/experiment-ledger-addendum-c289-preregistration.md.
Design:docs/v5b-early-pair-withdrawal-v0.1.md.
Review:docs/c289-post-authoring-review.md.
Acceptance base:4acd3873a4f524ceb3080aab10653cd13caaa1c4.
Authoring/review target:2058969f7f37ef63e117f17939dbd75c729776d7.

One question:can first400-update pair auxiliary retain fitting gains without always-on transfer
regressions at the same800-update budget? Fresh seeds289001..289005;three arms per seed:
-ce_only:CE all800;
-pair_always:CE+0.25*Lpair all800;
-pair_early(candidate):CE+0.25*Lpair updates1..400,exact CE updates401..800.
Lpair=mean softplus(1-(correct_assignment-swapped_assignment)) over24 existing query pairs.
Same margin1 and enabled weight.25 as C288. Labels/pair metadata never enter model.forward.

Actual C278 MeanFinalDualReadout in all3 arms,14256 parameters,48-token context,float64.
Construct independent identical initial states. Normal mixed2/3 TRAIN only;no HOLDOUT,quad or
ablated optimization.192 logical rows,96 intact query pairs,200 epochs x4 batches x48rows.
randperm96(seed+289000+epoch);profile=epoch%3;length=epoch%2;fit RNGseed+290000 reset per arm.
Per-row length exposure100/100;length/profile updates[[136,132,132],[132,136,132]].
AdamWLR.005 constant,betas.9/.999,eps1e-8,weight_decay0,clip1;CPU2threads,deterministic.
One continuous optimizer per model;no reset or LR change at401. No intermediate checkpoint.

Record800 actual auxiliary weights,LRs,CE,pair,total traces and a step400 state fingerprint.
Require pair_always/pair_early exact first400 CE,pair,total histories and step400 state identity.
Require all3 initial states,data schedules and LR histories match. Prefix mismatch is INVALID.
Freeze final states,evaluate unchanged2/3/4 tasks,strict-load and replay all3. Primary absolute
PASS iff all5 pair_early states pass every FOUR-character fixed criterion. Thresholds unchanged:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Seen/all-task and direct
TRAIN/HOLDOUT counts are descriptive. Include90 final partitions and360 named comparator contrasts.

CE-only remains a concurrent anchor so an improvement over always-on alone cannot conceal a loss
relative to ordinary CE. This increases total work50% but not per-model budget. Withdrawal also
changes integrated auxiliary gradient weighting;late-pressure causation is not established.
Auxiliary saturation may make the switch ineffective. Do not retune switch/weight after results.
Absolute candidate PASS is not superiority,arbitrary-length competence or automatic Gate F.

Workload:15 models,12000 updates,576000 training rows,14430 forwards,809280 row presentations,
57720 core calls,one15-state checkpoint bundle write/load,15 strict state loads,network0.
Registration:source580;protected1041;dependency-union65;own48;modules174;loaded4206;focused4205.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own48).
Review target:2058969f7f37ef63e117f17939dbd75c729776d7. All6 committed OWN files fetched back;
whole-file Git blobs match tested local bytes6/6. Post-match own48 PASS in8.483s onLinux/
Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;unresolved globals0.
Tests execute800 real AdamW updates per arm on a small query-conditioned toy model;instrumented
optimizer steps verify continuity across400/401 and exact always/early prefix. Other paths mock
parent archives,Git,inherited models/scorers. This is NOT actual FOLD scientific execution.
Actual parent data,real3-way initial models/tables/objective-equivalence preflight,full4205,
PowerShell parsing and15-model science remain mandatory authoritative Windows runtime gates.
Activation must not change reviewed OWN6 or any accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C289 -> Validate(parent/source/input
580/1041,real tables/pairs/3-way models/objective equivalence,own48,focused4205) ->
authoring_runtime_preflight=PASS -> Execute(15 models,common400-prefix checks,frozen3-task scoring,
strict replay,90 final partitions,persisted reconstruction) -> log publication.

Validate failure skips science/publish. Scientific integrity failure retries SAME C289.
Valid all-five miss is ACCEPTED VALID NEGATIVE. Do not change switch,loss coefficient,LR,seed,
budget or thresholds after results. C290 is unregistered until C289 formal judgment.
Keep scientific execution HEAD distinct from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoffs remain under docs/handoff-history/c280-pre-acceptance.md through
c288-pre-acceptance.md. The latest preserves Git blob2b3efa437e7fb91d35dc59894329904a00055646.
Only this Formal state is authoritative. Accepted source/tests,preregistrations,logs and protected
dispatchers remain unchanged. Earlier C287 chat claims are superseded by its acceptance addendum.
