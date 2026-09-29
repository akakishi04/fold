# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C283 ACCEPTED VALID NEGATIVE. C284 ACTIVE / NOT YET JUDGED. C285 NOT REGISTERED.**
C283 scientific execution HEAD:24c4acd44905e1d3c4d2a019214eb588d72f9a93.
C283 published log commit:aedfa69557782b7484ee71128b08213a27d8798d.
Four-character whole gates:mixed_length3/5;two_char_only0/5. No rerun or seed selection.
C282 remains ACCEPTED VALID NEGATIVE. No Gate F promotion or retrospective threshold change.
C284 is the unique ACTIVE maximum-training-length-matched comparison.

## Latest accepted science — C283

Acceptance:docs/experiment-ledger-addendum-c283-c284.md.
Acceptance commit:255ad0ed293b5e6b29266f761c5e6b862a9fca37.
Summary:runs/c283-v5b-frozen-four-bacee738e5a04007ae0f0f3093b0f5a7/summary.json.
Summary SHA256:609718db24ca6e3eda4f8916f04f56b24bff3621ddca4ebe136209617fad4949.
Manifest SHA256:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False;
all_replays=True;all_weights_preserved=True. Own32/focused3981 and persisted reconstruction PASS.
Scientific workload1350 forwards,129600 rows,5400 core calls,zero training/new checkpoint writes.

Mixed states282002/282003/282004 pass;282001/282005 fail. All control states fail.
All-value-split four-character correct3805/4320->4266/4320;collapse347->5.
HOLDOUT correct1239/1440->1391/1440;shared_suffix3 HOLDOUT325/480->469/480.
Every seed improves pooled normal accuracy/collapse,but not every profile improves.
All four-character examples were untrained. Transfer benefit does not isolate diversity from larger
maximum training length. The published contrast rows and exact per-seed totals are in the acceptance.

## Active C284 — maximum-training-length-matched comparison

Experiment:C284-v5b-max-length-matched-training.
Stage:V5-B-MAX-LENGTH-MATCHED-TRAINING.
Registration:docs/experiment-ledger-addendum-c284-preregistration.md.
Design:docs/v5b-max-length-matched-training-v0.1.md.
Review:docs/c284-post-authoring-review.md.
Acceptance base:255ad0ed293b5e6b29266f761c5e6b862a9fca37.
Authoring/review target:19a678c1852977d22ae25a653b71bccd880d1aaa.

One question:at matched maximum training length3,architecture and800-update budget,does mixed2/3
training improve unseen four-character transfer over THREE-character-only training?
Fresh paired seeds284001..284005;arms three_char_only,mixed_length. Actual C278 all-token
MeanFinalDualReadout in both,14256 parameters,48-token context,identical initial state/independent storage.
No evidence-only mask,extra head,auxiliary loss,LR change,seed selection or training extension.

Same192 logical TRAIN rows,96 query pairs,200 epochs x4 batches x48 rows.
Paired logical batches/profiles:randperm96(seed+284000+epoch),profile=epoch%3.
Control three-character only:length1. Candidate alternates2/3:length=epoch%2.
Per-length row exposures:control0/200;candidate100/100. Both total200 and maximum length3.
Length/profile matrices:[[0,0,0],[268,268,264]] and [[136,132,132],[132,136,132]].
AdamW lr.005,CE only,CPU float64,2 threads,deterministic;fit RNGseed+285000 reset per arm.
C282 TRAIN-table helper excludes HOLDOUT/ablated/four-character optimization.

Freeze after800 updates,evaluate unchanged two/three/four tasks,then strict checkpoint replay.
Primary PASS requires all5 mixed_length states pass all FOUR-character fixed criteria.
Two/three/all-task pass counts remain descriptive;passed=quad_pass,not all_tasks_pass.
Thresholds unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Compare paired seed/normal/collapse results separately:an absolute candidate PASS alone is not
superiority. Exposure allocation/curriculum remain part of the intervention. No arbitrary-length
claim or automatic Gate F closure;C282/C283 verdicts stay unchanged.

Workload:10 models,8000 updates,384000 training rows,9620 total forwards,539520 row presentations,
38480 core calls,one10-state checkpoint bundle write/load,10 strict state loads;network calls0.
Registration:source550;protected976;dependency-union60;own32;modules169;loaded4014;focused4013.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Review target:19a678c1852977d22ae25a653b71bccd880d1aaa. All6 committed OWN files fetched and matched
locally tested Git blob identities6/6. Linux/Python3.13.5/PyTorch2.10.0+cpu:own32 PASS after matching,
final run3.757s;both Python files/3 embedded blocks compile;unresolved global names0.
Relevant fixtures mock parent archives,Git,inherited models/scorers;actual fit uses a tiny toy model.
This is NOT actual C284 scientific training. Real parent validation,PowerShell parsing,real models,
full focused4013 and10-model science remain authoritative Windows runtime gates.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after ParseFile on dispatcher.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C284 -> Validate(source/artifact550/976,
real TRAIN tables/maximum lengths/paired models,own32,focused4013) -> authoring_runtime_preflight=PASS
-> Execute(10 models,frozen two/three/four evaluation,strict replay,persisted postcheck) -> log publication.

Validate failure skips science/publish. Scientific integrity failure retries SAME C284.
Valid quad gate miss is ACCEPTED VALID NEGATIVE. No seed/threshold/schedule change or C285
registration before formal judgment. Prior verdicts and Gate F remain unchanged.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads mutable handoff. Preserve this seal.
Later lifecycle-aware tests use immutable acceptance addenda after acceptance.

## Historical state and recovery

Full prior handoffs are preserved under docs/handoff-history/:
c280-pre-acceptance.md,c281-pre-acceptance.md,c282-pre-acceptance.md,c283-pre-acceptance.md.
The last preserves Git blob902e902bfb175f8b127b676c8141ee65ab8dba82 byte-for-byte.
Only this file's Formal state is authoritative;older ACTIVE instructions are historical.
All accepted source/tests,preregistrations,logs and protected dispatchers remain unchanged.
