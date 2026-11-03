# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md Current response format (v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Assistant authors/tests/registers; user executes locally. No Codex handoff.
Native Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5; PowerShell7 / ParseFile / active_v2.
Accepted sources/tests/contracts/logs/dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C343 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).**
C342 remains ACCEPTED VALID NEGATIVE, candidate_gate=false / eligible_seed_count=2.
**C344 ACTIVE / NOT YET JUDGED.**
No production adoption. Do not rerun accepted C343. Do not prepare C345 before C344 judgment.

## Latest accepted evidence

Report: docs/experiment-ledger-addendum-c343-c344.md.
Execution: 1effc2138967715e9e9319e1da19c3653e4fd9ac.
Log publication: 74eda8f681f7a68f1d8c4ae91203c2b151855ce6, sole parent execution.
Acceptance: ec33919f2763a629e8c2d1b00f82d0f682e3979a; wording clarification/base:
345830ca6cd256abfb33d2d220db06e8f83e2859.
6442 tests / 237 modules PASS; failures/errors/skips0; 2956.442 seconds.
All 240 subprocess exits0; 923 sources / 7693 protected inputs; all7693 final
uncached rereads and fresh verifier complete; run_execution_valid=true.
C343 child scientific forwards/updates0. Diagnostic integrity is not model capability.

All144 strata /30 criterion summaries /261 failed local /141 failed order rows,
120 normal support /60 paired summaries independently reconcile. All parent C342
HOLDOUT support, answer/pair rescues/regressions and failure counts remain identical.
Full scope:4320 local/2160 order cells,51840 normal observations,25920 paired answers,
12960 query-pair transitions. These are distinct and sometimes overlapping units.

Candidate interior4 has131 actual TRAIN errors,all wrong_observed:342001=99,
342005=32. Of1440 TRAIN query pairs,1312 both correct,125 one correct,3 neither.
Thus125 pairs collapse to one displayed value;3 swap the two values. One wrong
TRAIN answer lies in a passing cell. Unknown value combinations alone are not
the explanation. TRAIN2677->2749 includes132 rescues/60 new regressions;
HOLDOUT1295->1366 includes101 rescues/30 new regressions.
Original6 remaining errors are all new:TRAIN6 wrong_observed,HOLDOUT6 absent_digit,
zero persistent wrong answers. Names of length6 were never fitted. No mask-only
failure in either arm. No pooling,gradient,capacity,parity or shortcut cause is proven.

## C344 registration and independent review

Source/preregistration HEAD: d97d1286f47ee06745083aa5e146c2d9349db3dc.
Source tree: eabee60fc0ebc56f767d7a93c1544b6d4e10b1e7.
Seven additions only, separate from acceptance. All seven remain unchanged in activation.
Preregistration: docs/experiment-ledger-addendum-c344-preregistration.md.
Review: docs/c344-post-authoring-review.md.
post_authoring_review = PASS
Review target HEAD: d97d1286f47ee06745083aa5e146c2d9349db3dc.
Use the later documentation-only activation HEAD as ExpectedHead, not source-only HEAD.

Experiment C344-v5b-pair-max-training / stage V5-B-PAIR-MAX-TRAINING.
Manifest SHA256:
a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8.
Author combined72 tests PASS normally91.885s and CP932-default-text-open92.115s;
failure/error/skip/expected-failure/unexpected-success all0. Exact tested bytes
match the reviewed source. Author runtime Python3.12.14/Torch2.10.0+cpu/NumPy2.3.5.
Actual loaders:6515 before sole inherited exclusion,6514 selected/239 modules,
48 science+24 infra. Parent6442/237 ordered prefix unchanged.
Full ordered-ID SHA256:
c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3.
Excluded inherited exact ID only:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusion,skip or accepted-test modification.

## One question, intervention and fixed gate

Can pair-max full256 CE improve actual fitted and held-value interior4 binding,
while preserving every domain, against ordinary mean CE on identical mixed45 inputs?
Fresh seeds344001..344005/orders344101..344105. Arms mean_ce and pair_max.
Control mean((a+b)/2); candidate mean(torch.maximum(a,b)) over24 complete query
pairs/48 rows. Candidate equals meanCE+.5*mean(abs(a-b)); exact ties split gradients
symmetrically. Both arms compute/log both losses and selected loss. Pair metadata
is checked before optimizer creation and every forward. No auxiliary coefficient.

Hold architecture14256 parameters/core3328/slots64,CPUfloat64/threads2,native_before,
all256 argmax,192TRAIN/96HOLDOUT,paired initial weights and identical actual token/
target/event/family/length streams. Both use C342 mixed45:actual exposure per logical
TRAIN row original2/3=200each,original4/5=50each,interior4=100,original6=0.
All HOLDOUT/masked views stay outside fitting. Same2400 updates,48 rows/update,
3168000 nonpadding tokens/model. One continuous core_slow AdamW,LR.005/.0005,
clip1,1200cycle repeated twice,FIT_RNG612000. All ten fits before any evaluation.

PASS requires ALL:
1. All5 candidates pass full original2..6 AND interior4 native gates.
2. EACH seed/EACH6domain/EACH split TRAIN/HOLDOUT has nonnegative normal answer
   AND query-pair gain:60 complete matched contrasts/120 inequalities.
3. Aggregate interior TRAIN answers,TRAIN query pairs,HOLDOUT answers,HOLDOUT
   query pairs EACH improve strictly:4 independent endpoints.

Thresholds remain accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/order.80.
Ties,perfect-control ceilings and any failed endpoint remain valid negatives.
Do not tune seeds,rates,steps,cohort,loss coefficient or gate after observing results.
Historical C268/C288 paired auxiliaries were valid negatives; this reduction is
distinct. It changes within-pair gradient weights/clipping effects and can neglect
an easier query. The harder-loss query need not be wrong. No causal diagnosis,
general language understanding,arbitrary-length transfer or Gate F completion follows.

## Parent contract, execution and evidence budget

Parent folder:runs/c343-mixed-length-localization-f1a8f5665ebb48c98b273cb549e721fd/.
Primary883c1c0142173f038bec25f65589643af9ba40ef2442e7c376b845a61f1477ce.
Envelope275ac041de4a858ca5a7f50aabb16898e85befebb2ee3ba6159a06198a7c993a.
Parent manifest7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6.
Parent executor8ec24e0b5c10ee653a445209f7caf9961d5c872c;
benchmarke9b8ee752422c93a29fefbb4b8ef0f48b5b776be.
Validate diagnostic PASS and nested C342 candidatefalse/eligible2.

Call C343 benchmark.semantic_recheck(out343,out342,data_out,cx,read),five arguments,
under no_neural. Its executor.parent_semantics alone would only verify C342.
C344 previous()->C332,reference()->C342;canonical data via C330 parent-folder/C329.
Child preflight5/training6/recheck4/report2 arguments. Validate actual writer schemas.
Protect930 sources/8183 inputs = inherited7693 + ALL483C343outputs +7OWN.
The483 include477 regression proofs:3 records +237 JSON/log pairs.
Finite leases max_files8183;all8183 final uncached rereads. No default4096 capacity,
eviction,unlocked fallback,missing direct/lazy pin or ancestor scientific rerun.

Route:invoke_active_v2 ->invoke_c344 ->run_c344 ->c344_execution. Branch/clean tracked
tree/ExpectedHead/unique ACTIVE/dependency/AST checks precede logging. User block
parses dispatcher;dispatcher parses selected launcher;launcher parses itself/runner.
Stale invocation skips without scientific execution or log publication.
Use existing .venv-py31315. Run prefix:runs/c344-pair-max-training-<id>/.

Sequence:native locks/snapshot ->immediate C343 semantics ->discarded native
preflight ->6514 isolated tests/239 processes ->10 fits ->native evaluation/replay
->saved reconstruction ->8183 rereads ->fresh verifier ->console log publication.
Preflight16forwards/64rows/8backwards/0updates is separate from science.
Science24000updates/1152000training rows/27420model forwards/1480320total rows,
109680core forwards/54840query projections/20state loads/10final states.
114views/state,raw replay<=1e-9 AND exact argmax. No intermediate selection.

Six science artifacts:experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json;plus primary and envelope.
Future successor retains489 outputs including481 regression proofs.
Primary fold-c344-trained-v1;envelope fold-c344-execution-envelope-v1.
Console includes all10seed results/120normal summaries/5paired results/60contrasts/
strict interior sums,with TRAIN/HOLDOUT support,collapse and rescue/regression counts.
A mandatory extra diagnosis should not be needed merely to discover TRAIN fitting.
Fresh verifier reconstructs saved arithmetic/streams;it does not replay all updates.

## Next response and stop

On user completion,fetch remote docs/experiment-run-logs/c344/latest.json and
latest.log. Distinguish scientific metadata.execution_head from log publication.
Check all6514 tests/no skips,239 matching module begin/end/proofs,all process exits,
native leases/930sources/8183inputs/final rereads,replay,reconstruction,fresh verifier
and run_execution_valid=true. Derive scientific verdict from preregistered gate.
If valid,record separate acceptance commit,then design/test/register next C in
the same response per protocol. If INVALID,repair/retry same C344 only.
Publication-only failure repairs transport without retraining.
Freeze this branch while the user runs. Do not alter reviewed seven files.

## History and inherited compatibility seal

C344 pre-activation:docs/handoff-history/c344-pre-activation.md.
C343 pre-acceptance:docs/handoff-history/c343-pre-acceptance.md.
C343 review:docs/c343-post-authoring-review.md.
C342 report:docs/experiment-ledger-addendum-c342-c343.md.
C272manifest seal89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
