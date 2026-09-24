# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C251 ACCEPTED VALID NEGATIVE. C252 ACTIVE / NOT YET JUDGED. C253 NOT REGISTERED.**
C252 is the unique ACTIVE experiment:Full pre-core K/V + pre-core query with post-core residual.
Post-authoring review PASS;authoritative Windows prechecks/full regression/scientific training pending.
C250/C248 remain ACCEPTED VALID NEGATIVE;C249 remains diagnostic-integrity PASS.
No production architecture adoption.

## Latest accepted evidence — C251

Scientific execution HEAD:9fb7e7cfec2521815258cf2f0c3b433bcea6419d.
Published log commit:36555face557650c73521ef0709063ba4ae7f8c7.
Publisher log SHA256:0cf296dca8d7633cd3b4d8547a5b2be408d21675a961355743006ee01a25e694.
Log bytes:620744.
Summary SHA256:55038562223ac2bf87db09d2f102d9bd0ca6aacaeaf1381186a836330e26578c.
Local summary:runs/c251-v5b-precore-read-dcc6ca85fe504ea7a71db741ab1558b1/summary.json.

24 own tests PASS in27.509s;3193 focused tests PASS in194.369s.
352 source pins/563 protected inputs. Five models x400=2000 updates/64000 training presentations;
2075 full-model forwards/67840 rows. All initial/checkpoint/prediction replays,weight updates,
protected inputs,tracked tree and execution HEAD checks passed;run_execution_valid=True.
Scientific status FAIL;candidate_gate=False.

All10 candidate TRAIN language cells pass the fixed criteria.
HOLDOUT normal correct counts,each cell /16,with immutable C250 Full/token_read comparator:

| Seed | C251 EN | C251 JA | C250 EN | C250 JA |
|---:|---:|---:|---:|---:|
|250001|16|16|3|8|
|250002|10|9|6|8|
|250003|10|10|16|16|
|250004|6|5|2|2|
|250005|16|16|16|16|

C251 outcomes:BOTH_PASS4 language cells,RECOMBINATION_MISS6.
Whole-seed both-language passes:C2512/5 (250001,250005);C250 comparator2/5
(250003,250005). Descriptive pooled HOLDOUT:C251114/160 versusC25093/160.
Ten paired language cells:6 improve,2 tie,2 worsen.
These are correlated cells from the same five reused initializations/task;no significance or
population reliability claim.

Changing only Full reader K/V memory from post-core states to pre-core local-encoder states did
not improve the preregistered all-seed reliability. It materially changed which solution was
learned:250001 changed from miss to perfect,while250003 changed from perfect to10/16 in both
languages. Memory source therefore affects this learned solution,but a simple pre-core switch is
not a stable remedy.

Do not conclude that the FOLD core destroys information,that pre-core memory is generally superior,
or that C250/C251 are statistically equivalent. The changed path also changes training gradients.
The repeatedly inspected HOLDOUT is an adaptive internal fixture,not external confirmation.
C250 and all earlier verdicts remain unchanged;no production/Gate F promotion.

Acceptance/artifacts:docs/experiment-ledger-addendum-c251-c252.md.
Acceptance/base commit:c217a7562c1c396d1a390e8e250083521ef027a5.
Accepted artifact SHA256:
-measurements.json:c98c5e6bbe313eac35895290d06f002756816918d7341de946941ab70ed0c398
-precore-plan.json:2f72dec74e0fe27e9a9aba129dd1064b34a467363b5a8dc9f5a7a3a2c636fc87
-split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
-trained-models.pt:0fce9c6e666360cf28a3723f870565a7aa1308bfa2a9a524c9a804080dc1e5c1
-validation-summary.json:f4b5128aeb4d730a4227a2c820cdc21874ae269c3ea3c3f669d0202390227da2.
Publication is one commit after scientific execution and changes only c251/latest.log/latest.json.
Acceptance uses retrieved immutable log evidence and recorded user-local postchecks,not a reviewer
rerun of the accepted learned checkpoints. No C251 rerun,seed replacement or threshold rescue.

## Preserved earlier boundaries

C250 fresh-seed replication:Full reader2/5 whole seeds,GRU reader4/5,both EOS controls0/5;
reader effect reproduces but initialization robustness is not established.
C249 diagnostic PASS:accepted C248 readers depend on their residual and learned nonuniform read.
C248 reader has8/12 joint-pass cells versus EOS0/12 but misses its all-seed gate.
C247/C246/C244/C242/C241/C239 remain accepted negatives under their registered questions.
C245/C243/C240/C237/C235 remain diagnostics;C238 is seen-prompt fitting only.
C232 established bounded byte-level learning;C233 showed the smaller GRU-only backbone competitive
on that tiny template-byte task. Preserve all accepted evidence and recovery records.

## Active C252 — align query space with pre-core memory

Experiment:C252-v5b-precore-query-alignment.
Stage:V5-B-PRECORE-QUERY-ALIGNMENT.
One question:with C251's pre-core K/V memory fixed,does changing only the attention query from
post-core EOS to the corresponding pre-core local-encoder EOS improve the same five-seed Full result?

C251:
-memory K/V=masked local causal encoder states;
-query q=Wq*h_postcoreEOS;
-residual base=h_postcoreEOS.

C252:
-memory K/V=the SAME masked local causal encoder states;
-query q=Wq*h_precoreEOS;
-residual base=the SAME h_postcoreEOS.

The FOLD core still executes both original routes for every internal step and remains jointly
trainable. The candidate does not bypass/freeze the core. AlignedPrecoreReadout uses the unchanged
C248 ResidualHead modules and original seed+248000 initialization:
q=Wq*h_pre;k_i=Wk*H_pre_i;alpha=softmax(k_i dot q/4);
z=h_post+Wo*sum(alpha_i H_pre_i),PAD excluded.
No new parameters,parser,gold location,loss,gating layer or output restriction.
Full remains14256=13488+768 parameters. Query-source change also changes gradient flow,so a
performance difference is not a unique inference-time causal proof.

Use all seeds250001..250005. Five fresh Full candidates only. Accepted C251 endpoints are immutable
comparators and are not rerun. Require exact C251 bare-backbone and complete wrapper/head initial
fingerprints. The trainable state and initial values are identical to C251;zero output projection
makes initial observable predictions identical. No accepted trained state initializes C252.

Exact reused TRAIN64/HOLDOUT32 rows/order/targets/provenance and normal/evidence_blind/query_blind
views. Actual unchanged C248.train_one/fit and C244.replay_one.
400 updates/model,batch32,normal old32/added32 alternating;AdamW lr0.005,betas0.9/0.999,
eps1e-8,weight_decay0,clip1,CPU float64,threads2,deterministic algorithms.
HOLDOUT is first scored after the fixed endpoint;no early stop,seed selection or extra budget.

PRIMARY:all five candidates pass BOTH languages and BOTH TRAIN/HOLDOUT:
accuracy>=0.90;fact/query/order pair>=0.80;evidence/query drops>=0.35.
TRAIN minima29/32 and13/16 pairs;HOLDOUT15/16 and7/8.
Report all10 language cells,whole-seed pass count,cell outcomes and paired HOLDOUT deltas versus
C251. Any valid performance miss is ACCEPTED VALID NEGATIVE;integrity faults retry same C252.
A pass remains bounded to this adaptive internal task;no external validation,production adoption,
core-superiority or Gate F claim.

Workload:5x400=2000 updates/64000 training presentations.
Each model415 forwards/13568 rows including reload;totals2075/67840,75 evaluation forwards.
Zero new reference/comparator forwards;one five-state bundle;zero scientific network calls.

Protection:358 source pins/575 protected inputs;direct dependency union28;OWN6.
Own tests24;modules137;loaded3218/focused3217. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
Five ignored outputs:alignment-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Bundle schema fold-c252-precore-query-v1.
Manifest:f662c4d9c5588bbc0662ae9f578dd59068354a76951bf7192f18f8e53166fd9b.
Design:docs/v5b-precore-query-alignment-v0.1.md.
Registration:docs/experiment-ledger-addendum-c252-preregistration.md.
Preregistration/review HEAD:b7dd76c63f99d0e085f4da285104be9317396873.
Use tools/invoke_active.ps1 with the final activation HEAD,not the preregistration/C251 HEAD.

## C252 post-authoring review

`post_authoring_review = PASS`
Review HEAD:b7dd76c63f99d0e085f4da285104be9317396873.
Scope:committed-byte/source review plus isolated synthetic/equivalent authoring checks;not C252 science.

All six OWN files were re-fetched after authoring. Reviewed blob identities:
-benchmark:00cb6f8307876c9aa86f97bf9ed6915467e14001
-tests:49a2b18003aa9254d7222b06c9ec160aba6fbb38
-runner:e61ec2b403038fca8631f21bf1b9bc3c2cd65839
-launcher:af72f8cc0f2a5b62d386d5f55c76641c5165d20d
-design:5e7e5216bb33031807eba153126709d586a69521
-preregistration:7a54673e0d01e1780e0c2d59ac130f1d09fe8b39.
Acceptance-base to review comparison contains exactly six added files,no accepted edits.

Remote-byte/source review verified24 unique test definitions,no bare unbound c### aliases,no detach
or checkpoint initialization in the candidate wrapper,manifest/count constants,parent C251 path,
three embedded runner Python blocks,focused3217 contract,ACTIVE C252 check and parser-before-log
publication. Query/memory/residual provenance matches preregistration.

Reviewer environment independently exercised a24-case semantic harness over a causal toy encoder/
core representation of the committed computation:24/24 PASS. It covered exact reconstructed
partition hash,identical initial C251/C252 state and zero-head outputs,pre-core query and K/V versus
post-core residual provenance,manual reader equation,nonzero query/key/encoder/core gradients,
PAD exclusion,hook cleanup,core-context rejection,task/EOS contracts,state nonmutation,gate/mask
criteria,initial/count/nonfinite guards,five-seed retention,two-step weight update,workload/accounting
and no-detach/no-checkpoint path. An earlier reviewer-scaffold attempt exposed scaffold-only
omissions;the corrected equivalent harness passed all24. This equivalent harness is not represented
as the authoritative committed-module unittest execution.

The reviewer container cannot resolve github.com for a full clone and has no PowerShell. Therefore
NOT executed in review:the exact committed own unittest module inside a complete repository import
graph,the full3217 historical regression,Windows ParseFile,user-local accepted-parent artifact
precheck,or actual five-model FOLD training. The authoritative runner must execute the exact24 own
tests first and stops before science if any fail. None of these pending checks is reported PASS.

Only this handoff changes after review HEAD. Re-read final branch HEAD before returning ExpectedHead.
Do not advance the branch during the user's formal C252 run.

## Stop and scope

Gate F NOT PASSED;numeric-memory/erasure-mixture tuning paused. Preserve accepted source/tests/logs
and tools/run_c167.ps1. No paid API,external corpus,model expansion,production adoption,cleanup or
history rewrite. Exact24 own tests ->3217 focused regression ->C252 five-model training ->postcheck
->log publication. Integrity faults stop same C252;valid misses do not trigger retries.
Repair log-only transport without retraining. Judge C252 before registering C253.
