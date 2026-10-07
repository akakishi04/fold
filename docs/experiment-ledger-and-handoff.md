# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted code/tests/preregistrations/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C309 ACCEPTED VALID NEGATIVE. C310 ACTIVE / NOT YET JUDGED. C311 NOT REGISTERED.**
C308 remains ACCEPTED PASS in its original bounded scope. C310 is the unique ACTIVE diagnostic.
Latest accepted scientific execution:a38c6ff864ab40efa74397017cfeec9f5628ca11.
Latest accepted published log:c3935db64960b7e90325672aa880318a6eed77e2. Do not rerun C309.
C310 has no scientific result yet; software review PASS is not a scientific verdict.

## Latest accepted evidence — C309

Acceptance:docs/experiment-ledger-addendum-c309-c310.md.
Acceptance commit:2cffcea33045a75582a94fadd963fa9f2b7d601d.
Summary:runs/c309-v5b-core-lr-replication-e24b3b724e47415eae204d3084a68185/summary.json.
SHA256:c8a1a2bd3d6ad4e4d6f714b38af3ce8424d314d1f5771b5fca578d49df37066c.
Own32/focused4909 PASS;source700/protected1309;run_execution_valid=True.
Manifest9350f7a5ec4e91a3292f6ecce041bc3ec09f1fa1a8372a4178b58d0ceb4df74d.
Full/frozen/slow passes lengths2/3:4/4/4;lengths4/5:3/4/4. Fitted TRAIN direct all15 pass.
309005 is rescued by frozen/slow;309002 fails five in all arms,with HOLDOUT277/239/269 out288.
Slow309002 also misses12/12/13 HOLDOUT answers at trained lengths2/3/4. No new all-five result.
Do not replace C308's bounded PASS with C309 negative,or pool old successes into the new gate.
User's C309 execution and log publication are complete; no further log submission or retry needed.

## Active C310 — saved value-renaming consistency

Experiment:C310-v5b-saved-value-renaming. Stage:V5-B-SAVED-VALUE-RENAMING.
Registration:docs/experiment-ledger-addendum-c310-preregistration.md.
Design:docs/v5b-value-renaming-v0.1.md.
Review:docs/c310-post-authoring-review.md.
Acceptance base:2cffcea33045a75582a94fadd963fa9f2b7d601d.
Authoring/review target:0739750338ec413390e34aa5f5fcaa2c9d2b0116.

One question:with names/query/fact order/language/length fixed,do saved answers transform with
bijective value renaming? Keep all15 C309 models,seeds309001..309005,three original arms,all2/3/4/5
lengths,three profiles,English/Japanese and original TRAIN/HOLDOUT. No new training or inference.
The union of original splits contains every distinct ordered pair of values0..3 for each context.
Locate counterpart rows by full logical identity;do not create new model inputs or change splits.

Use full256-class argmax with the original first-index tie rule. Map ASCII48..51 according to
all24 value permutations and fix the other252 output classes. Record tied-max indices/counts.
Each row has22 changed-input permutations and2 that leave the displayed facts unchanged:
identity and swapping the two absent values. Keep all three categories separate. Each changed
counterpart appears twice under distinct absent-value mappings;keep this intentional multiplicity.
Comparisons are directed and dependent,not extra independent trials or a population sample size.

Report equivariance and correctness separately,including equivariant-but-wrong outputs. Always
choosing the other fact or a constant non-value byte may be consistent and wrong. No restricted
argmax,answer repair,best-of selection or hidden-mechanism claim. Original masks/full gates remain
under the exact C309 verifier. C310 PASS means diagnostic integrity,not a new capability pass.

Inventory:51840 original normal answers;1140480 changed comparisons in240 model/length/split-pair
groups;51840 absent swaps in120groups;51840 identity controls in60groups. Reconstruct720 original
split/profile/language totals including correct count,pairs and collapse. Preserve60 prediction
blocks,288 source IDs,24 permutation destination maps and tied-max indices in the full report.
Those arrays reproduce every comparison without writing redundant million-row records.

## Parent protection and workload

Verify36 ordered summary hashes BEFORE exact C309.verify_artifacts(parent_dir,35ancestors,
acceptedHEAD). Tail:C309.parent_hashes(C308). Require acceptedFAIL,exact15 flags,all_replays and
all_groups_matched. Exact summary hash seals7 parent artifacts. Writer stores FINAL frozen logits
in fold-c309-core-lr-replication-eval-v1,not selected actions. Read verified dataset/evaluation data
only. C267 canonical dataset hash and values/targets are rechecked. C304 profile adaptation to
C270 tripled/shared_prefix2/shared_suffix2 is preserved when checking parent length_scores totals.

Sole direct import C309. Retain700 source pins/1309 inputs;verify actual repository-local context,
wide,core,factory-language helpers and C304.PINNED. Add OWN6 and8 parent files:source706/protected1323.
No accepted code,test,log,preregistration or dispatcher modification;no new exclusion.
Scientific model_forward_calls/train_steps/model_state_loads/new_checkpoint_writes/row_presentations/
core_forward_calls/network_calls all0. Under no_grad,block Module calls,load_state_dict and torch.save.
Saved tensor reads and numeric work are allowed;CPU numeric threads2. Tests/recursive checks are
separate operational costs. Do not equate zero new model calls with no computation.

Outputs:audit-plan.json,value-renaming-report.json,validation-summary.json plus summary.json.
JSON only. Hash/size checks and fresh reconstruction from the same verified saved evidence are
mandatory. Full predictions/maps stay local/ignored;compact receipt and420 aggregate groups in log.
Own32/modules195/loaded4942/focused4941;sole inherited exact C204 exclusion unchanged.
Manifest0b4304400ddb57789a52aefb0bfe84690df7bb3fee9ef4c63e842fecfd595596.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus executed local software tests).
OWN6 refetched at0739750338ec413390e34aa5f5fcaa2c9d2b0116 and independently hash-matched6/6.
After all six matches:normal32/32 PASS5.579s;CP932-default-emulated32/32 PASS5.170s.
Complete uninterrupted unittest runs;no omitted tests. Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5.
Both Python files and3embedded blocks compile;unresolved globals0;UTF8/noNUL;manifest matches.
Independent scalar reference,bijections/inverses/split counts,ties,consistent-wrong cases,parent
totals,36hash guards,706/1323 protection,actual child run/load/persistence and altered-output
rejections pass. Test31 executes accepted C270 score with controlled synthetic logits/data.

Local support contains a fetched score-function slice,not a full parent clone. Git,archives and
some parent interfaces are substitutes;the actual4941 inherited suite and C309 model outputs were
not executed here. CP932 emulates default decoding,not all Windows behavior. PowerShell unavailable
locally. Real36parents/pins,ParseFile,full real-data audit dry-run,own32 and4941 regression remain
mandatory Windows gates. Activation preserves all6 reviewed blobs and every accepted file.
The prior interrupted authoring stage did not produce a registered experiment or a scientific run.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C310 -> Validate(36parents,706/1323,
full real-data correspondence/original totals,own32,focused4941) -> authoring_runtime_preflight=PASS
-> Execute(saved-value audit,no new model calls,JSON persistence/reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failures repair SAME C310. No coefficient,
cohort,split,output-map or threshold changes after results. C311 waits for C310 formal judgment.
Keep C309 negative,C308 bounded PASS and Gate F NOT PASSED distinct.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Pre-activation handoff:docs/handoff-history/c310-pre-activation.md.
Git blob:a09a67d3389cc797e361f143affad67063baab55.
Prior full handoff:docs/handoff-history/c309-pre-acceptance.md.
Git blob:14e4ded5fe6d3f5fbd26b451f1bef1016d77aebe.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
