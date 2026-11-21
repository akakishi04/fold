# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C312 ACCEPTED VALID NEGATIVE. C313 ACTIVE / NOT YET JUDGED. C314 NOT REGISTERED.**
C313 is the unique ACTIVE frozen six-character capability probe;no C313 scientific result yet.
C311 remains diagnostic PASS;C308 bounded PASS and C309 valid negative remain unchanged.
Latest accepted scientific execution:f481ae2b547bccc5cd5f43ae2654f89e8fa3140f.
Latest accepted published log:16e55cffe274ac24a456cb28b650fca3140d8789.
Do not rerun C312 or reinterpret its comparator as its registered candidate.

## Latest accepted evidence — C312

Acceptance:docs/experiment-ledger-addendum-c312-c313.md.
Acceptance commit:0c4dfe291010f90d7b444c36fd49d3accf64158c.
Summary:runs/c312-v5b-value-batches-c23759c73f5c4bfbb03a7c3d9c8e8198/summary.json.
SHA256:2bb0efc9a9f128a0aeda9585dabab4ee0c672ba2e9b31f4b148cc6ba959a5ed6.
Own32/focused4997 PASS;source718/protected1343;run_execution_valid=True.
Manifest5c543202a3c252e69f3f099b369ef9905e39662a37947c8904756b17700fab2c.
All10 training runs and strict replays completed;all_pairs_matched=True.
Both arms pass5/5 at trained lengths2,3,4. At unseen5,random5/5,balanced4/5.
Only balanced312002 fails;normal five TRAIN575/576,HOLDOUT286/288.
All other normal partitions perfect. Paired five:4both,1control_only,0candidate_only,0both_fail.
Five TRAIN-value full gate still passes despite one normal error;HOLDOUT fails local accuracy,
query-pair,query-drop and two-order criteria. Do not replace local gates with pooled accuracy.
No balancing superiority or universal harm established;no Gate F promotion or old verdict change.

## Active C313 — frozen transfer to six characters

Experiment:C313-v5b-frozen-six-transfer. Stage:V5-B-FROZEN-SIX-TRANSFER.
Registration:docs/experiment-ledger-addendum-c313-preregistration.md.
Design:docs/v5b-frozen-six-transfer-v0.1.md.
Review:docs/c313-post-authoring-review.md.
Acceptance base:0c4dfe291010f90d7b444c36fd49d3accf64158c.
Authoring/review target:f6ca577c8c4280032fc31462c42a89342c7d3cd8.

One question:do all5 retained random_pairs baseline checkpoints transfer from training2/3/4
to previously untested6 without retraining? Keep all10 original C312 states and both arms,
including balanced312002. No new seeds,training,checkpoint splicing or per-query model choice.
The prospective primary is all5 random_pairs states passing SIX local/masked gates. Balanced
results remain fully reported but cannot rescue primary failure. Random is the unchanged baseline,
not C312's candidate;C312 remains a valid negative. No six outcome has been observed yet.

Retain actual C312 model factory/checkpoint loader,C304 LengthReadout,14,256 parameters and64slots.
All states previously trained2/3/4 TRAIN only,coreLR.0005/noncore.005,1200updates. Freeze all weights.
No optimizer,new coefficient,decoder restriction,new model capacity or input-frame expansion.
Core/reader computations and full256-class argmax remain unchanged.

Child renderer extends permitted name length to6 with the original three profiles and bilingual
semantics. Same logical facts,values,question,fact order,TRAIN/HOLDOUT value split and all three
normal/evidence-blind/query-blind views. Exhaustively match old2..5 stored prompts and accepted
C304.render byte-for-byte. Six normal inputs864 distinct/disjoint from old normal inputs;new
byte vocabulary is a subset of old. Japanese maximum61UTF8bytes+2markers=63tokens fits64slots.
Check every token byte,BOS/EOS,padding and no truncation. Neither Japanese nor longest rows omitted.
TRAIN-value six evaluation is not six-character training. Five also remains untrained.

Each checkpoint runs old2..5 before -> six -> old2..5 after. Every old task/profile/split/view
must reproduce its own C312 archive<=1e-9 absolute logit drift and exact argmax. Old per-state
full-gate flags stay equal. Full weight fingerprint and inherited temporary hook registries
remain unchanged after each pass. Child installs no new model hooks. Any preservation or replay
failure is INVALID / RETRY SAME C313,not a capability failure.

New six gates use unchanged accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
C304.score_length adapts profiles to the old logical scorer without a name-length argument.
Do not use the old four-length cohort analyzer for six. Report10states,20six partitions,
20five-to-six correctness transitions,10old-reproduction receipts and separate arm pass counts.
Transitions distinguish new errors,recoveries,both wrong and same wrong on aligned logical rows.
Successful5/5 is a bounded six capability PASS,not diagnostic-only PASS or arbitrary-length proof.
Same checkpoint cohort and templates mean no independent fresh-seed generalization claim.

## Parent contract,protection and workload

Verify39 ordered summary hashes BEFORE exact C312.verify_artifacts(parentdir,38ancestors,
accepted execution HEAD). The fixed parent summary seals all7 artifacts. Require parentFAIL,
complete10flags,all_pairs_matched/all_replays and original data/prompt identities.
Read verified C312 dataset.json,length-datasets.json and final-logit evaluations.pt. Checkpoint
schemafold-c312-value-batches-models-v1 is handled by actual C312.load_bundle;eval schema is
fold-c312-value-batches-eval-v1. No newly generated answers are taken from parent teacher outputs.

Sole direct import C312;its inspected context provides C310 no-neural,C308policy,C304model/prefix/
eval/scorer/replay,C287normalizer and backend. All718 parent source pins and1343 protected inputs
remain checked,including C312.PINNED,C304.PINNED and actual repository-local/factory-language
helper coverage. Add OWN6 and8 parent files:source724/protected1357. No dependency waiver,
accepted file modification or new regression exclusion.

Science:10saved models,training0,2430forwards,233280row presentations,9720core calls,10strict state
loads,one parent model-bundle read,new checkpoints0,network0. Before/after controls included in
these counts. Six discarded operational smoke forwards,software tests and recursive parent
verification are separate. This is new inference,not a saved-output-only diagnostic.
Raw float64 logit payload477757440bytes before overhead,not a peak-RAM estimate.
Five outputs:evaluation-plan.json,six-dataset.json,evaluations.pt,measurements.json,
validation-summary.json plus summary.json. Child archivefold-c313-six-transfer-eval-v1 retains
allbefore/six/after logits,original weight fingerprints and replay attestations. No trained-model
file written. Full tensors stay local/ignored;compact receipt and allaggregate outputs in log.
Hash/size checks and fresh no-neural numerical reconstruction of every score/transition required.
Own32/modules198/loaded5030/focused5029;sole inherited exact C204 exclusion unchanged.
Manifest:f6e02599e4704457781f1ac49272a0a8d50d9c40524d66d4bcfb173e1cf86cca.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus executed local software tests).
All6 OWN re-fetched atf6ca577c8c4280032fc31462c42a89342c7d3cd8,independently blob-matched6/6.
Post-match normal32/32 PASS4.970s;whole-suite CP932-default-emulated32/32 PASS5.032s.
Both uninterrupted full unittest runs. Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5.
BothPython+3embedded blocks compile;undefinedglobals0;UTF8/noNUL;manifestselfhash matches.
39orderedpaths/postcheckindices verified;no accepted source/test/log/dispatcher changes.
Actual child infer_one executes243 calls on a controlled model,validates load/freeze/replay/
preservation and rejects weight mutation. Canonical data and oldprompt hashes,novel6bounds,
39hash guards,724/1357protection,primary/secondary separation,production loader dispatch,
no optimizer,new checkpoint prevention,semantic suite IDs and persisted tampering tests pass.
Test30/31 execute accepted C304 renderer/prefix/scorer-adapter function ASTs with controlled
interfaces. Local parent support is exact fetched function slices,not a full clone,and NOT committed.
Synthetic logits/models and substituted Git/parent/scorer/suite interfaces are software controls,
not evidence of actual FOLD capability or actual5029 inherited regression success.
Mandatory Windows39parentarchives/pins,PowerShellParseFile,real frozen bilingual two-arm probe,
own32/full5029 regression and ten actual C312-model inference runs remain user Validate/Execute gates.
Activation must preserve all6 reviewed OWN blobs and every accepted file.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C313 -> Validate(39parents,724/1357,
old/new render bounds,real frozen bilingual probe,own32,focused5029) ->
authoring_runtime_preflight=PASS -> Execute(all10frozen states,oldbefore/six/oldafter,
weight/output preservation,six gates and transitions,saved reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failures repair SAME C313 with fixed
scientific conditions. A valid primary failure is ACCEPTED VALID NEGATIVE. No post-result
retuning of length,weights,cohort,primary or thresholds. C314 waits for formal C313 judgment.
C312 negative,C308 bounded PASS,C309 negative and Gate F NOT PASSED remain distinct.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical lifecycle tests.

## Historical state

Pre-activation handoff:docs/handoff-history/c313-pre-activation.md.
Git blob:e8ee39b0add9ccfc2ead2b9068536be23e614db0.
Earlier handoff:docs/handoff-history/c312-pre-acceptance.md.
Git blob:f48f0bc02fd7cd00948b9fa48d38db5d8ef1fa3d.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
