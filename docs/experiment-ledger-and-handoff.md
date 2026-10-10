# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C317 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C318 ACTIVE / NOT YET JUDGED. C319 NOT REGISTERED.**
C318 is the unique ACTIVE native readout branch-isolation diagnostic;no C318 result yet.
C316/C315 negatives,C314 diagnostic PASS,C313/C312 negatives,C308 bounded PASS unchanged.
Latest accepted execution:3ecd3a638726f86b294f0fe94d53a2fc5d082e01.
Latest publication:a948757c3f2a0e524bdef50521cf4034b900fc2a. Do not rerun C317.

## Latest accepted evidence — C317

Acceptance:docs/experiment-ledger-addendum-c317-c318.md.
Acceptance commit:300dcb6ed45411cec6e646f732cb95ed664cf683.
Summary:runs/c317-v5b-query-endpoint-88ae97edc7d44cd3bcd9732e66c8b14e/summary.json.
SHA256:09632cda7689c9b23229ec993d19c108ac23a7bb142285cd58b11bcc713d8cb5.
Own32/focused5149 PASS;sources748/inputs1407;run_execution_valid=True.
Both replay errors0.0 at all10 states;one-byte controls and weights/hooks preserved.
Original both arms5/5 at2..5,4/5 at6. first_byte both arms0/5 at every scored2..6.
This is diagnostic PASS,not capability PASS. Original C316 negatives remain accepted.
Example only:one_to_four316005 six HOLDOUT shared_prefix English48->24/48,Japanese48->23/48;
shared_suffix English48->48/48,Japanese48->43/48. Do not call0/5 zero answer accuracy.

## Active C318 — frozen native branch isolation

Experiment:C318-v5b-frozen-readout-branches. Stage:V5-B-FROZEN-READOUT-BRANCHES.
Registration:docs/experiment-ledger-addendum-c318-preregistration.md.
Design:docs/v5b-readout-branch-isolation-v0.1.md.
Review:docs/c318-post-authoring-review.md.
Authoring/review target:06375ef01097beef25cfe7438310b9f9676f52ac.

One question:with the same C316 weights,what behavior is retained by the native mean-query
attention alone versus the native last-query-byte attention alone? No new first-byte candidate.
Retain all10 C316 checkpoints,seeds316001..316005,both two_to_four/one_to_four cohorts,and all
canonical1..6 English/Japanese inputs/splits/profiles/views. No training,seed or checkpoint search.

Actual C304 forward has two shared query projections:span mean and last-byte local state. In
mean_only duplicate the native mean into the second call;in last_only duplicate the native last
into the first call. Validate each native input before replacement. Same query weights,keys,
softmax,value states,.5memory averaging,core/residual/normalizer/classifier/full256-class output.
No new parameters or model-method replacement.14,256parameters/64slots unchanged.
Duplicating one branch keeps total coefficient1 instead of halving memory strength. The actual
activation norm/covariance need not match. Results do not establish universal necessity or how
separately trained branches would perform. No labels or answers enter the intervention.

Mode order:original_before -> mean_only -> last_only -> original_after. All modes use the same
observer/provenance hooks,returning native inputs unchanged for originals. Strict-load once per
state,freeze/eval/no-grad,check complete weight fingerprint and hook registries after each mode.
One encoder capture/two query projections per forward,CPUfloat64/intermediate finite checks.
Exception cleanup mandatory. Original before/after reproduce all C3161..6 logits<=1e-9 and exact
argmax,plus original2..6 gates. All query-blind and English length1 outputs identical across both
interventions. Japanese length1 is multiple bytes,not a single-byte control.

Score original-before and both isolation modes;restoration is not a fourth independently scored
model. Reuse original C304/C270 local/masked gatesaccuracy.90/query_pair.80/evidence_drop.35/
query_drop.35/two_order.80. Report30state/mode flags,300length/split partitions,60single diagnostics,
10reproductions,1280paired groups/92160paired normal rows. Keep rescues/regressions/wrong-to-wrong
flips distinct. Shared baselines and repeated rows are not independent learned trials.
C318 PASS means diagnostic integrity only,even if both isolated modes fail every capability gate.
No outcome promotes Gate F,changes the old C316 negatives,or authorizes per-question model choice.

## Parent contract,protection and workload

Verify44 ordered hashes BEFORE actual C317.verify_artifacts with43 ancestors and its accepted
execution HEAD. C317 has4diagnostic artifacts,not a dataset/model bundle. Its status is diagnostic
PASS,old2..5 counts5/5 and6counts4/5 in botharms,first_byte0/5 everywhere. Then C317.load_parent
on paths[1:] returns verified C316 data/prompts/final-output anchors. Load C316 trained-models.pt
at summaries[1].parent through actual C316.load_bundle;never seek a model in C317 directory.
C316.make_models uses original seeds/context. All10 strict fingerprints match original records.

Sole direct import C317;C316/C315/C304/C287/C310/backend helpers inherited and source-protected.
All748 source pins/1407 inputs retained and checked,including actual local context/factory-module
coverage. OWN6+5C317parentfiles gives754/1418. No accepted source/test/log/dispatcher changes or
new regression exclusions. The single inherited exact C204 exclusion remains unchanged.

Science:10saved states*4modes*144=5760forwards,552960rows,23040core calls,10strict state loads,
one C316 bundle read,training0,new model checkpoint0,network0. Each mode has288query projections
and4896single-byte-span rows. Ten discarded operational forwards and recursive verification/
regression costs separate. Raw logits1132462080bytes plus overhead,not peak-RAM accounting.
Both projections execute;there is no compute-saving claim. All tensors remain local/ignored.
Four artifacts plus summary:audit-plan.json,evaluations.pt,measurements.json,validation-summary.json.
Schemafold-c318-branches-eval-v1 stores4raw modes,original fingerprints,receipts,reproduction errors.
No-neural postcheck reconstructs all scores/controls/paired counts and verifies JSON/tensor hashes
and sizes. No run-directory overwrite. Own24/modules203/loaded5174/focused5173.
Manifest:757879ae36418ab5b3973a18ea80902aef081c3e41b4a463f03cc841c2c3e4ad.

## Post-authoring review and runtime boundary

post_authoring_review=PASS. All6 OWN refetched at06375ef01097beef25cfe7438310b9f9676f52ac,
independently Git-blob-matched6/6;rehashed after tests. Post-match24unique tests each encoding mode:
normal01..12 PASS13.126s and13..24 PASS10.245s;CP93201..12 PASS19.953s and13..24 PASS24.274s.
All completed partitions zero failures/errors/exit0,no omissions. Encoding patch spans imports,
setup,tests,teardown. Linux/Python3.13.5/PyTorch2.10.0+cpu. No native PowerShell available.
UTF8/noNUL,Python+3embedded blocks compile,unresolvedglobal0,manifest seal matches.44fixed paths
and CLI[2:46]/head46/argc47 checked. No accepted source/test/preregistration/log/dispatcher edit.

Tests execute actual C304 forward/span and C315 evaluator function ASTs with controlled components;
independent mean-only/last-only numerical references match,original outputs restore,one-byte
controls hold,exception/provenance/strict-state violations fail. Actual child576forward inference
path,754/1418file protection,44hash guards,C316loader path/run order,persistence/tamper,semantic
suite IDs and diagnostic-only scope tested. Local parent support is exact helper/function slices,
NOT full modules/repository and NOT committed. Synthetic models/scorers,parent/Git substitutes
are software-control evidence,not actual FOLD competence or real5173 inherited-regression evidence.
Mandatory local gates still pending:44actual archives/Windows pins,PowerShellParseFile,real frozen
bilingual probes,own24/full5173regression,all10checkpoint inference. Activation preserves OWN6.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C318 -> Validate(44parents,754/1418,
real mean/last probes,own24,focused5173) -> authoring_runtime_preflight=PASS -> Execute(all10
frozen states,original/mean-only/last-only/original,reproduction/one-byte controls,paired results,
saved reconstruction) -> log publication. Validate failure skips science/publication.
Integrity failure repairs SAME C318 with fixed science. No retuning,per-row endpoint choice,
capability promotion or seed filtering. C319 waits for formal C318 judgment;old verdicts and
Gate F NOT PASSED remain. Separate scientific execution HEAD from later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical tests.

## Historical state

Pre-activation:docs/handoff-history/c318-pre-activation.md.
Git blob:36e8178dd1a89dc355af57e815e83e7ed8515517.
Previous:docs/handoff-history/c317-pre-acceptance.md.
Git blob:40175d12ac9fce1f9922cdc8b3c717e1e023e740.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
