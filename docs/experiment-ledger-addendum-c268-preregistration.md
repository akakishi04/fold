# C268 preregistration — paired-query discrimination loss

Experiment:C268-v5b-paired-query-discrimination-loss.
Stage:V5-B-PAIRED-QUERY-DISCRIMINATION-LOSS.
C267 ACCEPTED VALID NEGATIVE;C266 diagnostic PASS;all earlier verdicts remain.
Gate E PASSED;Gate F NOT PASSED. C269 NOT REGISTERED.
Acceptance/base:9465a4bddf1182e1da3044764dec765ae5a7cacc.
Acceptance:docs/experiment-ledger-addendum-c267-c268.md.

## One question

At identical mixed-name coverage,initial weights,paired batches and800 updates,does an additional
paired-query discrimination loss improve held-out value binding relative to cross-entropy alone?
No more frozen-output decomposition or repetition of the completed C267 run. This is a new objective
comparison. Both arms use paired batches,so the experiment does not isolate a benefit of pairing
itself relative to C267. Fresh seeds also prevent direct historical seed-by-seed causal attribution.

## Arms and exact objective

Five fresh seeds268001..268005;arms ce_only and ce_pair_margin. Create one actual C252 Full aligned
reader through C256.make_model/C231 factory per seed,then deep-copy its complete initial state.
Both14256 parameters,identical surviving/full initial weights;no shared storage or accepted learned
checkpoint initialization. Model inputs remain token IDs and zero task IDs. No pair index,target,
profile or split label enters model.forward. Training targets are supervision only.

Each batch contains24 adjacent query pairs,48 rows. A pair has identical visible facts and different
queried entities,ordered by the original entity index. Its target bytes t0 and t1 are distinct.
For logits z0 and z1 before softmax,define:

    d = (z0[t0] - z0[t1]) - (z1[t0] - z1[t1])
    P = mean(max(0, 2.0 - d)) over the24 pairs
    L_control = CE(z,targets)
    L_candidate = CE(z,targets) + 0.1 * P

CE is the mean cross-entropy over48 answers and256 output bytes. Margin2.0 and coefficient0.1 are
fixed engineering choices,not optimized values or claimed theoretical optima. Do not tune them
or add a sweep after reading results. The control computes the penalty for reporting but backpropagates
exactly CE,with the same gradient as ordinary CE. Both arms use the same single model forward per
update. The candidate adds arithmetic and gradient terms,not a second neural evaluation.

This contrast encourages query-dependent relative preference between the two correct targets.
It does NOT guarantee both answers are correct:the first answer can favor t0 more strongly than
the second while both still choose t0. CE and all existing capability gates remain mandatory.
Neither low penalty nor different wrong answers count as task success. Swapping both pair rows
and their targets leaves the contrast unchanged. Synthetic tests check signs and gradients.
The modified gradient also changes its globally clipped direction;that is part of the objective
intervention,not an independently controlled internal mechanism.

## Fixed data,coverage and paired batching

Use actual unchanged C267.dataset/validate_data/training_tables/render/evaluate/score.
Dataset SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
TRAIN192 logical rows,HOLDOUT96. All source entity subsets,both EN/JA symbolic spellings,both visible
fact orders and both queries are retained. Distinct values0..3;HOLDOUT pairs exactly(0,2),(1,3),
(2,0),(3,1) across every profile/subset/language/order. Other8 distinct pairs are TRAIN.
This small modular split is structured,not a random population benchmark. Do not alter it.
Both arms train all3 name profiles:uu/vv,uu/uv,uu/vu,using exactly C267's byte rendering.
No HOLDOUT example or alternate rendering of a held pair enters optimization.

Group TRAIN rows by(language,entities,values,permutation),giving96 pairs. Sort keys deterministically,
then sort each pair by query index. For epoch e,shuffle96 groups using seed+268000+e. Four consecutive
blocks of24 pairs give four48-row batches. Both arms receive identical indices at every update.
Profile=e mod3.800 updates=200 complete epochs;each TRAIN row appears200 times per arm.
Profile updates268/268/264. Store/reconstruct exact batch SHA,row exposures and profile counts.
This paired sampler differs from C267's row-wise sampler,but is the same in both C268 arms.
Thus only the objective differs WITHIN C268;do not call a C267-to-C268 comparison loss-only.

AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0;global norm clip1. Batch48,800 updates/model.
Reset fit RNG to seed+269000 for each arm. CPU float64,threads2,deterministic algorithms.
No early stop,extra updates,seed selection,intermediate checkpoint choice or optimizer default change.

## Capability gate and paired comparisons

Use the unchanged C267 scorer on final outputs for both splits,all3 profiles,all languages/subsets/
orders and normal/evidence_blind/query_blind views.72 answer cells and36 two-order cells per model.
Each answer cell requires accuracy>=.90,paired-query correctness>=.80,evidence_drop>=.35 and
query_drop>=.35. Two-order consistency>=.80. TRAIN cells16 answers/8 pairs require15/16 and7/8;
HOLDOUT cells8 answers/4 pairs require8/8 and4/4. Two-order minima13/16 TRAIN and7/8 HOLDOUT.
The small HOLDOUT cells make the accuracy criterion effectively perfect answers;state this clearly.

Primary PASS iff all FIVE ce_pair_margin models meet every existing criterion. Control results
are independent and neither rescue nor fail treatment. Record30 paired HOLDOUT profile/language
contrasts,each48 answers/24 query pairs,including correct-answer and same-answer-collapse differences.
A treatment PASS is not automatically superiority over CE-only;both may pass. No post-hoc success
criterion based on penalty decrease,average accuracy or selected profiles replaces the fixed gate.
Names are TRAIN-seen in both arms. Success is held-VALUE-pair transfer under these names,not unseen-name
transfer,arbitrary-string understanding,an independent broad benchmark or causal parser identification.

## Accepted parent and source semantics

C267 execution:3418e545bc261cf1bb920f2ae8f819deec69150c.
Published log:92b57170c6b2c3c3dc451f9d6de402114cbd6f12.
Log SHA256:f8ee03f3e30132601b1a6f055388a3411b93638280ff1680a6c1075aa20c852c.
Parent summary:runs/c267-v5b-name-coverage-f8a591aae4aa4b7aa373aba2e520181c/summary.json.
Summary SHA256:f5f550d362428feaee12d7eee96db4cc324cea311b9b4e91ec50e4f150ec6ef8.
The six parent artifact hashes are frozen in PARENT_ARTIFACTS and the acceptance record.
load_parent calls actual C267.verify_artifacts(parent_dir,PARENT_EXECUTION),TWO arguments,with
neural Module calls blocked. It verifies saved final outputs,schedules,metrics,hashes and sizes;
require status FAIL,counts doubled_only0/mixed_names1 and10 measurement records. A scientific negative
parent is valid provenance,not a capability PASS prerequisite. No parent weight initialization occurs.
The parent verifier reads evaluations.pt but does not invoke its learned models. File hashing and
saved metric reconstruction are real work,not new scientific neural forwards.

Parent context returns(core,base,aligned,reader,factory,audit) through the protected C267 chain.
C268 calls its actual counted/evaluate/replay_one/score functions. Saved raw outputs are final-state
split/profile/view tensors,TRAIN192x256 and HOLDOUT96x256. Strict parent replay loads each C268 final
state into the same architecture,checks full fingerprint,exact argmax and max absolute logit error
<=1e-9,and records27 forwards/2592 rows/108 core calls. It does not require C267 seed membership.

## Workload,persistence and protection

Ten models:8000 updates/384000 training rows. Final evaluation27 forwards/2592 rows per model;
strict replay repeats27/2592. Training+final827/40992/3308 core calls;replay27/2592/108 core calls.
Total8540 model forwards,435840 row presentations,34160 core calls,540 final/replay forwards.
One new10-state bundle write/load;10 strict state loads. Extra loss arithmetic is not zero compute.
No network calls. Historical tests,parent/source hashing and schedule reconstruction are additional work.

Six ignored artifacts plus summary.json:loss-plan.json,dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json. Bundle schema fold-c268-query-loss-models-v1;evaluation
schema fold-c268-query-loss-eval-v1. Records contain final logits,initial/final fingerprints,actual
paired schedule,counters,CE/penalty/total loss and checkpoint-replay results. Reconstruct last-loss
arithmetic for each arm. Saved postcheck reconstructs paired schedules,parent scores,contrasts and
gates from saved tensors with Module calls blocked and without a learned-bundle reload.
Raw final tensor payload53084160 bytes,plus weights and JSON;not a peak-memory measurement.

Inherit448 source pins/761 protected inputs. Add OWN6 and parent summary+SIX artifacts:454/774.
Direct deciding dependency union44=five C231 LM sources,C230..C267 helpers andC268;lazy imports count.
No accepted model/source/test is edited. The previously patched dispatcher remains a control-plane
script;do not waive any actual inherited source/input check. Those mappings must pass on user runtime.
OWN6:benchmark,own tests,runner,launcher,this preregistration,and design:
fold_lm/v05_benchmarks/model_c268_paired_query_loss.py;
tests_lm/test_v05_c268_paired_query_loss.py;
tools/run_c268.ps1;tools/invoke_c268.ps1;
docs/experiment-ledger-addendum-c268-preregistration.md;docs/v5b-paired-query-loss-v0.1.md.
Own24;modules153;loaded3598/focused3597. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:cf16b504aa03e1e5f61c000c161b44c3a551fe7c103096c9119274947fb4e07b.

## Review,duplicate-launch correction and stop

Re-fetch all committed OWN files,match complete tested bytes,rerun exact own24 and inspect Python
free names,manifest/data hashes,CLI indices,parent signatures,source order and parser-before-logging.
Authoring fixtures use Tiny,not actual Full computation. The local reviewer may only have retrieved
parent helper excerpts;record that limitation instead of claiming a complete historical checkout.
The800-step Tiny test validates implementation,not learned capability. Ten-state orchestration uses
substituted training records. Dummy3598 test IDs validate filtering,not3597 historical regressions.

The old repeated C267 command was an assistant completion-handling error,not a new failed run.
Preserve dispatcher RESULT_ALREADY_PUBLISHED and the genuine STALE_EXPECTED_HEAD fallback. Never
replace an old expected HEAD with current HEAD to force a rerun. Published means evidence available,
not necessarily accepted or successful. On completion,read the new experiment's logs before replying.
A static dispatcher contract test is included;it is not Windows execution. User ParseFile chain and
full regression remain mandatory. No user launcher until committed-byte post-authoring review PASS.

C267 stays accepted negative whatever C268 finds. Valid capability failure is accepted,not repaired
by extra updates,changing margin/coefficient,seeds or thresholds. Integrity failures retry SAME C268;
no C269 until judgment. Repair log-only publication without retraining. No production adoption,
paid API,external corpus,model expansion,cleanup,history rewrite or CI change. Gate F NOT PASSED.
