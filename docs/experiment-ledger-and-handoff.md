# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C293 ACCEPTED VALID NEGATIVE. C294 ACTIVE / NOT YET JUDGED. C295 NOT REGISTERED.**
C292 remains diagnostic ACCEPTED PASS. C294 is the unique ACTIVE saved support/choice audit.
Latest accepted scientific execution:318d9fd76f4253b30d68645ee34c124457be78a3.
Latest accepted published log:3d35190c718b8b3c52e5c68120358ba96811466e.
Do not rerun C293,change its thresholds/seeds,or promote Gate F.

## Latest accepted evidence — C293

Acceptance:docs/experiment-ledger-addendum-c293-c294.md.
Acceptance commit:8bdfdeae1daeab051af6407e5101578e66c1d06f.
Summary:runs/c293-v5b-fact-support-834c844c03c84023bc4ef1c6d32e3067/summary.json.
Summary SHA256:61a92e5d5775381cc1b7ef0fa19a9fa393197afd05a7642b74b0486ab6d338e6.
Manifest0aadd3137b216f6e0fbc37feffe8b0ad947e48eeb22da881f38e58ee38a424f7.
Own40/focused4357 PASS;source604/protected1091;run_execution_valid=True.
Quad CE2/scaled1/support2;seen-length full4/4/4;TRAIN direct4/4/4;HOLDOUT direct4/4/4.
Candidate rescues293003 but loses293005 relative to CE. All arms fail seen-length gates on293004.
Candidate293004 HOLDOUT normal counts improve226->259,216->253,200->239 across2/3/4 versus CE;
absent errors49->29,59->33,71->40. These improvements do not clear the full gates.
Candidate293005 quad is857/864 versus CE864/864,so the change is not uniformly beneficial.
No robust superiority,adoption,arbitrary-length claim or Gate F promotion.

## Active C294 — saved support versus conditional choice

Experiment:C294-v5b-saved-support-choice-audit. Stage:V5-B-SAVED-SUPPORT-CHOICE-AUDIT.
Registration:docs/experiment-ledger-addendum-c294-preregistration.md.
Design:docs/v5b-saved-support-choice-audit-v0.1.md.
Review:docs/c294-post-authoring-review.md.
Acceptance base:8bdfdeae1daeab051af6407e5101578e66c1d06f.
Authoring/review target:11366c4e8d90ff51e048aeb1d7b74123a5be124a.

One question:when a C293 full256-class winner is outside the stated fact values,is the target
still ranked above the other fact value,or is within-fact choice also wrong?
Use all15 saved models,seeds293001..293005,ce_only/scaled_ce/support_weighted,all2/3/4 tasks,
three profiles,English/Japanese and original TRAIN/HOLDOUT value splits. No new training policy.
Quad TRAIN means trained value combinations at an untrained length,not optimized length4 data.

Verify20 ordered summary hashes before exact C293.verify_artifacts with19 ancestor paths and
accepted execution HEAD. Its summary SHA commits all8 parent artifact descriptors. Reconstruct
all original masked/full gates,loss histories and matching before reading final normal logits
from fold-c293-support-eval-v1 records.raw[task][split][profile][view]. No checkpoint-to-model load.
The parent final_partitions provide original rows,correct,output_role_counts and final_normal_nll
for independent reconciliation. Do not infer capability from a surrogate or from publication.

Support is the unordered pair of values in each verified logical input,sorted by numeric class.
It is not selected by the answer key or the model prediction. Keep full argmax and separately
record conditional support argmax. Exact ties choose the lowest numeric class in both;never
put the target first. Record choice and support/outside ties and raw logit gaps explicitly.
Categories:full_correct,outside_correct_choice,outside_wrong_choice,other_fact.
Stable log-softmax CE=support_NLL+choice_NLL is checked at1e-10 and against original final NLL.
A support mass above1/2 is not a guarantee that the full argmax lies inside support.

Persist38880 observations,90 model/task/split partitions,540 profile/language groups. Reconstruct
all540 original normal totals/collapse and all90 original partitions. Compare support_weighted
against CE and scaled CE on25920 aligned rows in60 comparisons,including original/conditional
argmax changes and complete4x4 category transitions. No success filtering or extra independent seeds.
The conditional result is an ORACLE-SUPPORT diagnostic using known input structure,not a deployed
decoder,achieved capability,causal proof or replacement gate. Original predictions stay unchanged.

Scientific model forwards,training,model-state loads,new checkpoints,row presentations,core calls
and network calls are0. Saved tensor reads and numerical scoring are permitted;Module calls,
load_state_dict and torch.save are blocked under no_grad. Operational regression work is separate.
PASS means exact diagnostic integrity only;capability_gate_applicable=False. C293 remains a valid
negative and Gate F remains NOT PASSED regardless of the conditional accuracy.
Outputs:audit-plan.json,support-choice-report.json,validation-summary.json plus full summary.json.
Compact receipt and90 partitions/60 comparisons in console;full row reports/maps stay local/ignored.
Source610/protected1106:all604 parent sources+OWN6;all1091 inputs+9 parent files+OWN6.
Direct import C293;require its exact blob and used context/core modules in the inherited map.
Own32/modules179/loaded4390/focused4389;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local numerical/control fixtures).
All6 OWN files re-fetched at11366c4e8d90ff51e048aeb1d7b74123a5be124a and whole-file blobs matched6/6.
After matching:normal own32 PASS in10.569s;entire CP932-emulated own32 PASS in9.977s.
Linux/Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;unresolved
globals0;UTF-8/no-NUL;manifest digest matches. Fixtures cover complete38880-row analysis,tie
handling,stable decomposition,original-score reconciliation,parent hashes,protection,run order,
no-neural enforcement,persistence/tampering and semantic suite-ID filtering.
Parent archives,Git and inherited suite members are mocked where needed. This is NOT real FOLD
science or actual Windows execution. Real20 ancestor artifacts/pins,PowerShell parsing,full4389
regression and actual saved-output diagnosis remain mandatory local Validate/Execute gates.
Activation must preserve reviewed OWN6 and all accepted code/tests/logs/dispatchers.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C294 -> Validate(20parent hashes,
610/1106 protection,real saved-logit numerical dry-run,own32,focused4389) ->
authoring_runtime_preflight=PASS -> Execute(saved support/choice diagnostic,zero model calls) ->
persisted reconstruction -> log publication.
Validate failure skips science/publication. Scientific integrity failure retries SAME C294.
Do not change original gates or promote conditional results to capability PASS. C295 stays
unregistered until C294 formal judgment. Gate F remains NOT PASSED.
Keep scientific execution HEAD distinct from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep the accepted legacy seal. Historical tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c293-pre-acceptance.md.
Git blob041497debafe241c2ac1897def0f827f75ceff15. Earlier history remains unchanged.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
Accepted source/test/log/preregistration and protected dispatcher files remain immutable.
