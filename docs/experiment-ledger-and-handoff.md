# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C313 ACCEPTED VALID NEGATIVE. C314 ACTIVE / NOT YET JUDGED. C315 NOT REGISTERED.**
C314 is the unique ACTIVE saved-boundary diagnostic;no C314 scientific result yet.
C312 remains valid negative;C311 diagnostic PASS;C308 bounded PASS and C309 negative unchanged.
Latest accepted scientific execution:bc6a226b8605b6ae04e64d46a387487533c0bdc0.
Latest accepted publication:aef7187d19ed49b3ba0f29b5621fc675c4365b2d. Do not rerun C313.

## Latest accepted evidence — C313

Acceptance:docs/experiment-ledger-addendum-c313-c314.md.
Acceptance commit:9221bfbe539d3f91fa3a74caa355e4059c9453fe.
Summary:runs/c313-v5b-frozen-six-8ef41237b7f84f148a0dcdce4b9aed21/summary.json.
SHA256:adfeb06f6db5b77feb172b8ede1f3bf7032c8ca35b299d7ecc692baeca097c97.
Own32/focused5029 PASS;source724/protected1357;run_execution_valid=True.
Manifest:f6e02599e4704457781f1ac49272a0a8d50d9c40524d66d4bcfb173e1cf86cca.
All10 old-before/after replays match with max error0.0;weights preserved.
Six primary random_pairs2/5,comparison value_balanced1/5;five had5/5 and4/5.
Random passes312004/312005;balanced passes312004. Random31 new normal errors;
balanced61 normal errors (58new,3persistent,0recovered). No new training.
Per seed312001..5,six normal TRAIN/HOLDOUT correct counts out576/288:
random:(561,278),(573,286),(576,287),(576,288),(576,288).
balanced:(570,281),(559,274),(569,282),(576,288),(574,286).
Pooled correctness cannot override local gates. These are bounded task results,not
arbitrary-length proof or a change to old verdicts. Language/profile causes remain unknown.

## Active C314 — saved five-to-six boundary profile

Experiment:C314-v5b-saved-six-boundary-profile. Stage:V5-B-SAVED-SIX-BOUNDARY-PROFILE.
Registration:docs/experiment-ledger-addendum-c314-preregistration.md.
Design:docs/v5b-six-boundary-profile-v0.1.md.
Review:docs/c314-post-authoring-review.md.
Acceptance base:9221bfbe539d3f91fa3a74caa355e4059c9453fe.
Authoring/review target:cd993bd1a7fd792a728eba59240eda313f4a6045.

One question:where does saved five-to-six deterioration occur by language and name profile,
at the same weights and logical rows? Retain all10 states,seeds312001..312005,both original
arms,allthree profiles,English/Japanese and the original TRAIN/HOLDOUT. No new model calls,
training,checkpoint,seed search,decoder repair,frame change or threshold adjustment.
Use only C313 raw.before['5'] and raw.six NORMAL logits. Restored after outputs are not new
independent observations. Original masked/full scores and old controls remain parent-verified.

Pair8640 original normal questions,17280 saved answers. Group by seed/arm/split/profile/language:
120 groups. Preserve all source IDs,predictions and tie flags. Full256 first-index argmax,
correct-answer margin=target logit minus max of all255 non-target scores. Ties can have zero
margin while correctness differs. Record raw score gap,not calibrated probability/confidence.
Per group:correctness transitions,both wrong/same wrong,answer roles,margin mean/min/max and
paired changes. No tuned cutoff,selective subgroup,significance or cross-model margin inference.

Answer roles:correct,other_fact,unmentioned_digit (absent ASCII0..3),other_output (remaining252
classes,including ASCII4..9). Read actual verified prompt strings for byte counts plus BOS/EOS:
English24->27tokens,Japanese54->63,64-slot frame unchanged. Language,byte length and EOS position
co-vary;concentration cannot establish a particular language/context/attention cause.

## Parent contract,protection and work

Verify40 ordered summary hashes BEFORE exact C313.verify_artifacts(parentdir,39ancestors,
accepted execution HEAD). Require parentFAIL,random primary,exact ten flags,six2/1 and allreplays.
Parent summary seals5 artifacts. It reconstructs all original/six masked gates and old controls.
Read dataset.json/length-datasets.json from C312 at paths[1];six-dataset.json/evaluations.pt
from C313 at paths[0]. Recheck three canonical hashes and every source_id/target binding.
Archive:fold-c313-six-transfer-eval-v1. No trained-model checkpoint is loaded or rewritten.

C313 metrics return six_score.totals. Use exact C304-to-C270 profile mapping and reconcile120
split/profile/language normal row/correct totals. Reconcile20 original five_to_six transitions,
including same_wrong. No parent capability verdict is inferred from this diagnostic's PASS.
Sole direct import C313;inspect its context/nested C312,C304,backend,factory-language helpers
for source coverage. Retain724 source pins/1357 inputs;add OWN6 plus6 parent files:730/1369.
No accepted file edits or added regression exclusions. Missing deciding-path pins are INVALID.

Science:train_steps/model_forward_calls/model_state_loads/new_checkpoint_writes/row_presentations/
core_forward_calls/network_calls all0. Tensor/JSON reads and numerical work remain;recursive
verification and operational tests are separate costs. Inherited no-neural guard prohibits
model calls,state loads and torch.save. The child writes JSON only.
Outputs:audit-plan.json,boundary-report.json,validation-summary.json plus summary.json.
Detailed8640 paired rows and120 groups stay local/ignored;console mirrors summary and120groups.
Fresh no-neural reconstruction plus all artifact hashes/sizes required;no run-directory overwrite.
Own24/modules199/loaded5054/focused5053;sole inherited exact C204 exclusion unchanged.
Manifest:e249986e20378fd3833dfb26183f94a74b93af3702149ce38bf2c03ba07c5a91.
C314 PASS means diagnostic integrity only;C313 six primary remains2/5 and Gate F NOT PASSED.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static plus executed local software tests).
All6 OWN fetched atcd993bd1a7fd792a728eba59240eda313f4a6045 and independently Git-blob-matched6/6.
Post-match normal24/24 PASS1.411s;whole-suite CP932-default-emulated24/24 PASS1.402s.
Both uninterrupted. Linux/Python3.13.5/PyTorch2.10.0+cpu;PowerShell not available locally.
UTF8/noNUL,Python sources+3embedded blocks compile,recursive unbound globals0,manifest matches.
Independent scalar margin/argmax/tie checks,numeric finiteness,role classes,canonical inputs,
120local/20transition reconciliation,40hash guards,730/1369protection,actual child loader/run/
persistence order,semantic suite IDs and tamper rejection pass. No new neural execution used.
Test24 executes the accepted C313 transition function AST;local support is a fetched function
slice,not a full module/repository,and is NOT committed. Parent/Git/scorer interfaces and logits
are synthetic/substituted for local tests;these do not demonstrate real FOLD capability.
Actual40 parent archives and Windows protected bytes,PowerShell ParseFile,real C313 diagnostic
and full5053 inherited regression remain mandatory local Validate/Execute gates.
Activation must preserve all6 reviewed OWN files and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C314 -> Validate(40parents,730/1369,
real paired-profile/margin dry-run,own24,focused5053) -> authoring_runtime_preflight=PASS ->
Execute(saved-profile audit,0model calls,JSON reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failure repairs SAME C314 with fixed
conditions. C315 waits for formal C314 judgment. Never promote this diagnostic PASS to a
capability pass or alter C313/C312/C309 negatives,C308 bounded PASS or Gate F NOT PASSED.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and historical lifecycle tests.

## Historical state

Pre-activation handoff:docs/handoff-history/c314-pre-activation.md.
Git blob:60cb63bdce77ef6d50903e4a333404cb06df82df.
Earlier handoff:docs/handoff-history/c313-pre-acceptance.md.
Git blob:40208e5c68d53172330511161664f64d805af98a.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
