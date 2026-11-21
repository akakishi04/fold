# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C304 ACCEPTED VALID NEGATIVE. C305 ACTIVE / NOT YET JUDGED. C306 NOT REGISTERED.**
C303 remains ACCEPTED VALID NEGATIVE. C302 remains diagnostic PASS.
C305 is the unique ACTIVE saved-output length-error-overlap diagnostic.
Latest accepted scientific execution:f309fde3e2aa8df33156ce55c703c9c37c6e106b.
Latest accepted published log:e54f443acbbc5e55d3dcab18d08c418d56867d1e. Do not rerun C304.

## Latest accepted evidence — C304

Acceptance:docs/experiment-ledger-addendum-c304-c305.md.
Acceptance commit:75b6545c1dc1d570286e76bb0b53473673247d33.
Summary:runs/c304-v5b-length-breadth-5090e7ce18a8444e9095afe14ad41266/summary.json.
SHA256:c4b0babc2f7b9ea544c96385ed386a721630ce81bfb26fcb5e1e028450670717.
Own40/focused4749 PASS;source670/protected1243;all_groups_matched=True;run_execution_valid=True.
Manifest:af8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0.
Operational48/64 compatibility:54rows,max_logit_error0.0,max_gradient_error2.220446049250313e-16.
All15 models completed1200updates and frozen/reloaded evaluation at lengths2/3/4/5.
Length2/3/4/5 pass counts in four_only/three_four/two_three_four order:
0/1/2;2/2/2;3/2/2;3/2/2. All-length simultaneous passes0/1/2.
Fitted TRAIN direct3/2/3;trained-length HOLDOUT direct3/2/2.
Five passes:four_only304002/304003/304005;both mixed arms304003/304005.
Same individual4/5 full-gate flags in all15 models,not proof of identical predictions/errors.

Candidate304001 passes trained-length TRAIN direct with576/575/575 correct out of576 at2/3/4,
but HOLDOUT is120/123/120 out of288. TRAIN-direct PASS is not perfect memorization.
Candidate304002 and304004 fail fitted TRAIN direct. Candidate304002 HOLDOUT2/3/4/5 is
152/151/149/144 out of288;four_only on that seed has288/288 at3/4/5.
Broader coverage did not improve five-character reliability at the registered common64-slot,
1200-update budget. It improves full-range coverage for some models,not a reliable adopted policy.
Exposure allocation and temporal spacing remain coupled. No universal harm-from-diversity,
length-independent-rule or unique-mechanism claim. Historical48-slot cohorts are not controls.

## Active C305 — saved cross-length error overlap

Experiment:C305-v5b-saved-length-error-overlap. Stage:V5-B-SAVED-LENGTH-ERROR-OVERLAP.
Registration:docs/experiment-ledger-addendum-c305-preregistration.md.
Design:docs/v5b-saved-length-overlap-v0.1.md.
Review:docs/c305-post-authoring-review.md.
Acceptance base:75b6545c1dc1d570286e76bb0b53473673247d33.
Authoring/review target:0d48409fac678d7ad53b1bcd6b3d23e57bf2d143.

One question:which five-character errors persist on the exact same logical question at4,and
which newly appear or disappear with the length change? Four is the primary reference;two and
three are descriptive references. Keep all15 C304 states and all5 seeds/all3 training arms.
Do not train,execute a model,filter a cohort,correct predictions or search another training policy.

Read final frozen C304 raw[str(length)][split][profile][view] logits. Align the same model,split,
profile,source_id,query and target;check every prompt's source_id/target against its canonical
logical row. Do not align by rendered string equality or independently sort prediction arrays.
All predictions are unchanged full256-class argmax,including original first-index tie behavior.
Parent nested length_scores use triple-profile names. Explicitly map repeat/shared_prefix/
shared_suffix to tripled/shared_prefix2/shared_suffix2. Reconcile720 original normal totals
(rows,correct,pairs,collapsed pairs) and120 model/length/split partitions before reporting.
All masked/full gates remain the exact original parent verifier's gates,not conditional scores.

Persist12960 aligned logical-question rows,each with four predictions at2/3/4/5:51840 saved normal
predictions. Include seed,arm,split,profile,language,source_id,query,target and four-bit correctness
signature. Report all16 signatures,including zero-count ones,in30 model/split groups.
For2/3/4 versus5,report both_correct,reference_only(new5error),five_only(recovered5),both_wrong.
Split persistent errors into same and different predicted wrong bytes. Report exact argmax flips,
counts and denominators,checking net correctness conservation. Produce90 model/split/reference
aggregates and540 profile/language subgroups. No per-question best-of output is produced.
Persistent fraction of5errors and5error rate among reference-correct rows use null for zero
denominators. These are descriptive conditional rates,not new capability gates or independent
trials. Error overlap cannot by itself identify memorization,attention failure or a general rule.

## Parent contract,protection and workload

Verify31 ordered summary hashes BEFORE exact C304.verify_artifacts(parent_dir,30 ancestors,
accepted scientific HEAD). Tail hashes are C304.parent_hashes(C303). Exact parent summary seals
all7 artifact descriptors. Require valid-negative FAIL,all_groups_matched/all_replays and exact
original15 length-pass records. Read only already-verified dataset.json,length-datasets.json and
fold-c304-length-eval-v1 evaluations.pt. No trained checkpoint is loaded into a model.
The parent writer/verifier was inspected;final outputs are not intermediate training predictions.

Sole repository import C304. Retain/check all670 inherited source pins and1243 protected inputs,
including actual repository-local parent/context/core helpers. Add OWN6 and8 parent files:
source676/protected1257. No accepted source/test/preregistration/log/dispatcher edit or new exclusion.
Scientific train_steps/model_forward_calls/row_presentations/core_forward_calls/model_state_loads/
new_checkpoint_writes/network_calls are all0. Computing argmax on saved tensors is allowed.
Module calls,load_state_dict and torch.save are blocked under no_grad through parent numerical
verification and child reconstruction. Operational regression fixtures are separate.

Outputs:audit-plan.json,aligned-answers.json,validation-summary.json plus summary.json.
No copied dataset or trained-model bundle. Every output is deterministic UTF-8 JSON with hash/size
checks and full reconstruction from sealed parent bytes. Full aligned rows/detailed subgroups
stay local/ignored;console mirrors90 transition groups and30 signature groups plus compact receipt.
PASS means diagnostic completion/integrity only. C304 remains negative and Gate F NOT PASSED.
Own32/modules190/loaded4782/focused4781;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static review plus executed local software tests).
All6 OWN files re-fetched at0d48409fac678d7ad53b1bcd6b3d23e57bf2d143;whole-file Git blobs match6/6.
Post-match normal own32 PASS0.873s;CP932-emulated whole-suite32 PASS1.032s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;both Python files/3embeddedblocks compile;unresolved globals0;
UTF8/noNUL;manifest matches. Independent transition/signature/conservation checks and full12960-row
synthetic alignment pass. Tests reject misaligned IDs,parent total/partition mismatch,bad logits,
missing helpers and byte/semantic tampering. Actual child load/reconstruct/run path and no-neural
scope are exercised with fixture parents;JSON roundtrip/no overwrite and31hash guards pass.
Local files are OWN only,not a complete repository clone. Parent archives/verifiers,Git,scorer
totals and inherited suite entries are substituted where unavailable. No actual C305 finding or
actual4781-suite execution is claimed. Mandatory Windows31-parent/pin checks,PowerShell parsing,
full real-data alignment dry-run,own32 and inherited4781 remain pending.
Activation must preserve all6 reviewed OWN files and every accepted file/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C305 -> Validate(31parents,676/1257
protection,complete real-data alignment/reconciliation,own32,focused4781) ->
authoring_runtime_preflight=PASS -> Execute(saved overlap/signatures,no new neural execution,
full output reconstruction) -> log publication. Full regression still runs despite zero scientific
training. Validate failure skips scientific execution/publication. Any integrity issue repairs
SAME C305 without changing the cohort,reference lengths,alignment or counting rules.
C306 remains unregistered until C305 formal judgment. No best-model selection or Gate F promotion.
Separate scientific execution HEAD from the later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Complete previous handoff:docs/handoff-history/c304-pre-acceptance.md.
Git blob:f421097c4157e95d0eb43e706d31fd4a4b54a4fe.
Only this Formal state is authoritative;historical ACTIVE commands must not be executed.
