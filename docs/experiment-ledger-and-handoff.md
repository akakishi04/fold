# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C291 ACCEPTED VALID NEGATIVE. C292 ACTIVE / NOT YET JUDGED. C293 NOT REGISTERED.**
C290 remains ACCEPTED PASS (diagnostic integrity only). C292 is the unique ACTIVE saved-output audit.
Latest accepted scientific execution:8d33edabbc7a91654a3da6056091cec2d84d9a24.
Latest accepted published log:49f30351a7687884bf0b9a6f2ddd304de8c26d1e.
The earlier CP932 failure was recovered. Do not rerun C291 or change its gates.

## Latest accepted evidence — C291

Acceptance:docs/experiment-ledger-addendum-c291-c292.md.
Acceptance commit:842e32a59bb5e3ef3f475554fb238c693139377e.
Summary:runs/c291-v5b-answer-margin-7f15f2dbf9ca4a16a2ba0ce2271a3421/summary.json.
Summary SHA256:271cc816f49fd7d53714508fee284bbf9f93783b3e74ac2728fc2a5286d740fa.
Own40/focused4285 PASS;source592/protected1066;run_execution_valid=True.
Manifest99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.
Quad CE4/5,pair_sum2/5,answer_margin4/5. Two/three4/5/4;TRAIN direct5/5/5;HOLDOUT direct4/5/4.
CE and candidate fail seen-length HOLDOUT on291003 despite normal TRAIN fitting;pair_sum passes
seen-length gates on that seed but fails quad. No superiority to CE or production adoption.
Candidate291003 normal TRAIN is576/576 at lengths2/3;HOLDOUT225/288,216/288,211/288 at lengths2/3/4.
CE on the same seed has HOLDOUT165/288,165/288,157/288. Improvement in counts does not clear the gates.
No claim that the new objective solved reliable transfer or proved the cause of remaining errors.

## Active C292 — saved answer-role audit

Experiment:C292-v5b-saved-answer-role-audit. Stage:V5-B-SAVED-ANSWER-ROLE-AUDIT.
Registration:docs/experiment-ledger-addendum-c292-preregistration.md.
Design:docs/v5b-saved-answer-roles-v0.1.md.
Review:docs/c292-post-authoring-review.md.
Acceptance base:842e32a59bb5e3ef3f475554fb238c693139377e.
Authoring/review target:6e6bf264beaecb33cdfaa9c7ed7c2591b53d4a02.

One question:which saved C291 errors output the other fact's value,an absent known value,or a
non-value byte,and how does that pattern vary across value splits and objectives?
Keep all15 models,seeds291001..291005,ce_only/pair_sum/answer_margin,all2/3/4 tasks,three profiles,
English/Japanese and both value splits. No model,weight,training,threshold or cohort changes.

Read final normal logits only after the exact C291 verifier reconstructs every old masked/full
gate and validates the entire8-artifact parent inventory. Verify18 ordered summary hashes first.
C291 writer schema:fold-c291-answer-margin-eval-v1;records.raw[task][split][profile][view].
C267 logical rows use distinct values0..3;target=48+value for the queried entity. Names may vary,
but the old renderers preserve source identities and value bindings. No new prediction is made.

Each full256-class argmax is labeled target/other_fact/absent_known_value/non_value_byte.
The last role is every output class outside ASCII0..3. No output filtering or correction.
Persist38880 exact row observations;reconstruct540 original profile/language normal totals,
including collapse. Produce90 model/task/split partitions and540 ordered-value-pair aggregates,
with denominators and target/prediction confusion tables. Preserve540 profile/language groups
in the full local report. Compare candidate versus both controls on25920 matched rows in60
aggregates,including exact argmax changes,rescues/regressions and full4x4 role-transition counts.
Equal role labels are not necessarily equal predictions. No hidden-mechanism causal claim.

Scientific model forwards,training,row presentations,core calls,model-state loads,new checkpoint
writes and network calls are0. Numerical work on old tensors is allowed. Neural Module calls,
load_state_dict and torch.save are blocked. Operational tests are separate from this workload.
PASS means saved-data diagnostic integrity only;capability_gate_applicable=False.
No old verdict,masked threshold,arbitrary-length claim or Gate F promotion changes with this audit.

Outputs:audit-plan.json,answer-role-report.json,validation-summary.json,plus full summary.json.
Compact receipt and aggregate rows in the console;full row records and protected maps stay local.
Source598/protected1081:all592 parent sources+OWN6;all1066 inputs+9 parent inputs+OWN6.
Direct import C291;require its pinned blob and every repository-local context/core module in
that inherited map. Do not substitute a guessed dependency count for actual module coverage.
Own32/modules177/loaded4318/focused4317. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
All6 OWN files re-fetched at6e6bf264beaecb33cdfaa9c7ed7c2591b53d4a02 and matched to local bytes6/6.
After matching,normal own32 PASS in2.763s;whole-suite CP932-emulated own32 PASS in2.796s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;both Python files and3 embedded blocks compile;custom globals0.
Full38880-row fixture analysis,all256-role coverage,matching/protection/parent hash guards,
no-neural enforcement,persistence/tampering,and explicit UTF-8 reads are tested.
The tests use synthetic parent/scorer/Git/suite data where required. They do NOT establish actual
C292 findings or execution of the real4317-test suite. Real Windows data/pins,all18 parent hashes,
full real-data dry-run,PowerShell parsing,own32 and focused4317 remain mandatory runtime gates.
Activation must not modify reviewed OWN6 or any accepted code/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C292 -> Validate(parent hashes/reconstruction,
598/1081 source/input protection,real full classification dry-run,own32,focused4317) ->
authoring_runtime_preflight=PASS -> Execute(saved role audit,zero new neural calls) ->
persisted reconstruction -> log publication.
Validate failure skips science/publication. Any scientific integrity issue retries SAME C292.
C293 is unregistered until C292 formal judgment. C291 remains a valid negative;Gate F NOT PASSED.
Separate scientific execution HEAD from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c291-pre-acceptance.md.
Its Git blob is96a00899912c1564f4bb9575445ecce08372a819. Earlier handoffs remain unchanged.
Only this Formal state is authoritative;historical ACTIVE commands must not be executed.
Accepted sources/tests/logs/preregistrations and protected dispatchers are immutable.
