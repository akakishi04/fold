# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C290 ACCEPTED PASS (diagnostic integrity only). C291 ACTIVE / NOT YET JUDGED. C292 NOT REGISTERED.**
C289 remains ACCEPTED VALID NEGATIVE. Do not rerun C289/C290 or alter their gates.
Latest accepted scientific execution:327e0a2e45270a4eb60f43daf8cca5c21242987c.
Latest accepted published log:76706cdc46914e67957abb37fcb75c46d1af0eaa.
C291 is the unique ACTIVE answer-wise hardest-rival objective comparison.

## Latest accepted evidence — C290

Acceptance:docs/experiment-ledger-addendum-c290-c291.md.
Acceptance commit:8f3158ea7f61c87bf674794755c8c36ccb0b27fe.
Summary:runs/c290-v5b-pair-margin-dd335cb112744775980aa441008b9a7f/summary.json.
Summary SHA256:1f4a3c16130b4c4517ddc7b5c09d7404ed83652fd0d6ce8b9a2438195a9cb11e.
Own40/focused4245 PASS;source586/protected1056;run_execution_valid=True.
Manifest SHA256:123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.
19440 saved query pairs,90 partitions,60 comparisons/12960 matched pairs;scientific neural calls0.
Original C289 masked/full gates reconstructed without changes. C290 PASS is diagnostic integrity only.
Quad HOLDOUT auxiliary arms meet144/144 margins but still miss1 answer on289002/289003 and4 on289005.
Aligned always/early NORMAL predictions match exactly for289002..289005;289001 differs.
A met pair-sum margin is not a guarantee of individual256-class answer correctness.
Do not infer a uniquely causal representation/optimizer failure or retune old conditions.
C289 quad gates remain ce_only3/5,pair_always0/5,pair_early0/5. Gate F remains NOT PASSED.

## Active C291 — answer-wise hardest-rival margin

Experiment:C291-v5b-answer-wise-hardest-rival-margin. Stage:V5-B-ANSWER-WISE-HARDEST-RIVAL-MARGIN.
Registration:docs/experiment-ledger-addendum-c291-preregistration.md.
Design:docs/v5b-answer-margin-v0.1.md.
Review:docs/c291-post-authoring-review.md.
Acceptance base:8f3158ea7f61c87bf674794755c8c36ccb0b27fe.
Authoring/review target:cc76905645ab60a650389e15456057088def6006.

One question:does answer-wise hardest-rival supervision improve reliable unseen four-character
transfer at the same800-update/model budget? Fresh seeds291001..291005;three concurrent arms:
-ce_only:CE;
-pair_sum:CE+.25*mean_pair softplus(1-[(z0[y0]+z1[y1])-(z0[y1]+z1[y0])]);
-answer_margin(candidate):CE+.25*mean_row softplus(1+max_{k!=y}z[k]-z[y]).
All penalties use the same forward per batch. Only the registered total loss is differentiated.
Correct labels are excluded from the255 alternatives only inside the supervised objective;
no labels,pair metadata or selected rival IDs enter model.forward. Ordinary CE stays in all arms.

Actual C278 all-token MeanFinalDualReadout,14256 parameters,48-token context,CPUfloat64,2threads,
deterministic. Independent identical initial states,fingerprints,first-input losses and schedules.
Normal TRAIN only at lengths2/3;192logical rows/96complete pairs;200epochs x4 batches x48rows.
randperm96(seed+291000+epoch);profile=epoch%3;length=epoch%2;fit RNGseed+292000 reset per arm.
Per-row length exposure100/100;length/profile updates[[136,132,132],[132,136,132]].
AdamWLR.005 constant,betas.9/.999,eps1e-8,weight_decay0,clip1;one optimizer800updates.
No new architecture,inference filter,training length,seed filtering,early stop or coefficient sweep.

Exact17 parent summaries:C290,C289,C288..C274. C290 is diagnostic,not a training checkpoint.
Its exact summary SHA and3 output descriptors are checked before its own verifier dispatch.
C290 recursively reconstructs C289 and its saved diagnostic. Read already-verified C289 input
JSONs and recheck canonical hashes. All C291 weights start from scratch,not saved parent weights.

Freeze final states;evaluate unchanged two/three/quad normal/evidence-blind/query-blind tasks;
strict-load and replay all three tasks. Primary PASS iff all5 answer_margin models pass every
original FOUR-character criterion. Thresholds:accuracy.90,query_pair.80,evidence_drop.35,
query_drop.35,two_order.80. Seen/all-task/direct TRAIN/HOLDOUT counts are descriptive.
Save90 final partitions and360 candidate-versus-each-anchor count contrasts. No pooled-gate substitute.

The objective's aggregation and negative set change jointly;equal coefficient.25 does NOT mean
matched gradient scale. C290 co-occurrence is not causal proof. Absolute PASS is not automatically
superiority,arbitrary-length capability,production adoption,or Gate F completion.

Work:15models,12000updates,576000training rows,14430forwards,809280row presentations,57720core calls,
one15-state checkpoint bundle write/load,15strict state loads,network0. Operational tests excluded.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json. Compact receipt and
aggregates in console;full protected maps,datasets and weights remain local/ignored.
Source592;protected1066;dependency-union67;own40;modules176;loaded4286;focused4285.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Review target:cc76905645ab60a650389e15456057088def6006. All6 OWN files re-fetched after commit;
whole-file Git blobs match tested local bytes6/6. Post-match own40 PASS in11.563s onLinux/
Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compile;unresolved globals0.
Fixtures execute800 real AdamW steps/arm on small toy models,loss gradients and equivalence,
matching/loader/protection/gate/persistence checks. Parent data,Git and inherited scorers/models
are mocked where needed;this is NOT actual FOLD scientific execution or the full4285 suite.
Actual Windows parent artifacts/pins,real tables/models,full4285,PowerShell parsing,and15-model
science/strict replay remain mandatory. Activation must not change reviewed OWN6 or accepted files.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C291 -> Validate(17summary hashes,
592/1066 source/input protection,real tables/all5schedules/three initial models,CE+pair-sum
loss/gradient equality to C289,own40,focused4285) -> authoring_runtime_preflight=PASS ->
Execute(15models x800updates,frozen3task scores,strict replay,persisted reconstruction) -> log publish.
Validate failure skips science/publish. Scientific integrity failure retries SAME C291.
A valid all-five miss is ACCEPTED VALID NEGATIVE;do not alter seeds,coefficient,margin,LR,budget
or thresholds after results. C292 is unregistered until C291 formal judgment.
Scientific execution HEAD must remain distinct from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

The complete pre-acceptance C290 handoff is docs/handoff-history/c290-pre-acceptance.md,
Git blob722d41d5b2f7076827c5a7d0bdb2ecbbdc92b5da. Older handoffs remain unchanged.
Only this Formal state is authoritative. Accepted source/tests/preregistrations/logs and protected
dispatchers remain immutable;historical ACTIVE instructions are not executable.
