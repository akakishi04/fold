# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
All accepted code/tests/preregistrations/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C310 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C311 ACTIVE / NOT YET JUDGED. C312 NOT REGISTERED.**
C311 is the unique ACTIVE saved-error-context diagnostic. C310 is not a new capability pass.
C309 remains ACCEPTED VALID NEGATIVE;C308 remains ACCEPTED PASS in its original bounded task.
Latest accepted scientific execution:bdbf7c4c410ceb9d621ae5d3ecf86e764061550b.
Latest accepted published log:45da9b7b1f63375bf0af251a7f65cc0c83b76765. Do not rerun C310.

## Latest accepted evidence — C310

Acceptance:docs/experiment-ledger-addendum-c310-c311.md.
Acceptance commit:0738f8e1c0be9aeecacea450abab806c9f5403a2.
Summary:runs/c310-v5b-value-renaming-580abae854514a7fb49fe1f702f4b50d/summary.json.
SHA256:eec24c37d318d0634623185193b50a4a7e4fb82abd6abe350a4712f807d59961.
Own32/focused4941 PASS;source706/protected1323;run_execution_valid=True.
Manifest0b4304400ddb57789a52aefb0bfe84690df7bb3fee9ef4c63e842fecfd595596.
720 original normal totals independently reconciled;51840 saved predictions and1140480
dependent directed changed-input value-renaming comparisons. Equivariant totals by arm:
full378610/380160;frozen374320/380160;slow377774/380160.
Total1130704/1140480,9776 violations. Identity51840/51840,absent-swap51643/51840.
Failed309002 five length:full18502/19008,frozen16912/19008,slow18178/19008.
Correctness and equivariance differ:equivariant wrong answers remain wrong.
No new training/model forwards/checkpoints/state loads. Gate F remains NOT PASSED.

## Active C311 — saved-error context and length persistence

Experiment:C311-v5b-saved-error-context. Stage:V5-B-SAVED-ERROR-CONTEXT.
Preregistration:docs/experiment-ledger-addendum-c311-preregistration.md.
Design:docs/v5b-saved-error-context-v0.1.md.
Review:docs/c311-post-authoring-review.md.
Acceptance base:0738f8e1c0be9aeecacea450abab806c9f5403a2.
Authoring/review target:2524d9a6a2192b9104a1e18ce0a6e82ae645b2ae.

Scientific question:which ordered held-out value pairs explain C309's original wrong
answers,especially309002,and were those same logical questions already wrong at trained
lengths2/3/4 before unseen length5? This is strictly descriptive,not causal attribution.
Keep exactly15 original C309 states,seeds309001..309005 and arms full_train/core_frozen/core_slow;
all2/3/4/5 lengths,three name profiles,English/Japanese,original TRAIN/HOLDOUT and288 rows.
Only the accepted and verified C310 value-renaming-report.json hard predictions enter analysis.
No training,model forward,new input/seed/checkpoint,optimizer,LR change,mask change or threshold
change. Preserve C310 comparisons and C309 normal/masked gates unchanged.

Classify full256-class saved argmax by original question:
correct;other_fact;unmentioned_digit;non_digit. Group12 ordered distinct value pairs,
24 questions per pair per(seed,arm,length,profile),4 HOLDOUT pairs,8 TRAIN pairs.
Produce2160 pair groups,720 split/profile/language groups,90 four-bit-signature groups
(seed,arm,profile,split) with all16 correctness signatures and four-to-five transitions.
All group totals must reconcile51840 original predictions and720 C310 original count receipts.
Report all arms/seeds,preserve309002 HOLDOUT focus without selecting a winning policy.
All observations are dependent saved-model rows,not new validation tasks or new trials.
Primary C311 PASS means exact diagnostic reconstruction/integrity only,not model competence.

## Parent chain,source protection,work and authoring review

Verify37 ordered summary SHA256 values BEFORE exact C310.verify_artifacts
(C310dir,36ancestors,accepted execution HEAD). It returns(payload,report). The C310
summary seals3 artifacts;the parent verifier recursively proves C309 archive integrity,
original dataset,source ID alignment,value permutations,ties and720 score totals.
Recheck original C309 dataset and value targets. Sole direct child import is C310; C310
provides C309/context/source protection and original scorer/backend. Retain706 parent
source pins and1323 protected inputs;add OWN6 plus4 C310 summary/artifacts:
source712,protected1333. Every newly required deciding module is pinned.
No historical regression exclusion changes.

Scientific costs:model_forward_calls=0,train_steps=0,model_state_loads=0,
new_checkpoint_writes=0,row_presentations=0,core_forward_calls=0,network_calls=0.
Reading and analyzing JSON is permitted. Three outputs:
audit-plan.json,error-context-report.json,validation-summary.json plus summary.json;
fresh JSON reconstruction/sha/byte checks mandatory. No source/test/accepted artifacts
are modified. Manifest SHA:b9e5f42cf681031892d77f2f134bc307d56233f22e039cac13009b3cd90b34fd.
Own24/modules196/loaded4966/focused4965;only exact inherited C204 exclusion.
post_authoring_review=PASS at2524d9a6a2192b9104a1e18ce0a6e82ae645b2ae.
All6 committed OWN bytes matched local SHA,post-match own24/24 normal and CP932 emulated PASS.
Python source+3embedded blocks compile,0 unresolved globals;37parent paths and C311 ACTIVE
guard verified. Code,runner,launcher and preregistration are source and byte sealed.
Local synthetic fixtures are NOT evidence of actual real FOLD accuracy or inherited suite PASS.
Windows Validate must still check37 original parents,712/1333 protection,real C310 report,
own24 plus focused4965 actual regression tests and PowerShell ParseFile. Validate failure skips
new science/publication. Any integrity failure repairs SAME C311,no scientific retuning.

## Execution and stop

Use tools/invoke_active_v2.ps1 by explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C311 -> Validate(37parents,712/1333,
real saved correspondence,own24,focused4965) -> authoring_runtime_preflight=PASS ->
Execute(saved original error/context audit,0model calls,reconstruction)->log publication.
C311 capability_gate_applicable=False. C312 NOT REGISTERED until formal C311 judgment.
Keep C308 bounded PASS,C309 negative,C310 diagnostic PASS and Gate F NOT PASSED separate.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve immutable accepted seals,commit identities and historical lifecycle tests.

## Historical state

Pre-activation C311 handoff:docs/handoff-history/c311-pre-activation.md.
Git blob:6f61f8de54acd33b9056af99f33bedb14e121003.
Earlier acceptance handoff:docs/handoff-history/c310-pre-acceptance.md.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
