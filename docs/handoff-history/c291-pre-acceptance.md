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
The first C291 invocation stopped in operational own-test preflight;no scientific run or publication.
Retry SAME C291 with the reviewed UTF-8 test recovery and the new branch HEAD.

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
Current recovery review:docs/c291-cp932-preflight-recovery.md.
Original review:docs/c291-post-authoring-review.md (historical test-blob approval superseded).
Acceptance base:8f3158ea7f61c87bf674794755c8c36ccb0b27fe.
Original authoring/review target:cc76905645ab60a650389e15456057088def6006.
Current recovery code/review target:02ba39b039d6d85b04c5a536f1fc44b6058351c9.

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

## Original post-authoring review (test approval superseded by recovery below)

Original review target:cc76905645ab60a650389e15456057088def6006. All6 OWN files were re-fetched;
whole-file Git blobs matched tested local bytes6/6. Original own40 PASS in11.563s onLinux/
Python3.13.5/PyTorch2.10.0+cpu. Both Python files and3 embedded blocks compiled;unresolved globals0.
Fixtures executed800 real AdamW steps/arm on small toy models,loss gradients and equivalence,
matching/loader/protection/gate/persistence checks. Parent data,Git and inherited scorers/models
were mocked where needed. That review did not cover the CP932 default and missed implicit test reads.
The unchanged scientific source remains the original reviewed source;the old test blob is not current.

## C291 operational preflight recovery and current review

Failed invocation HEAD:57ef469ed23950f37eb17f788f582bf1a35eb3f1.
User reported40 own tests,one UnicodeDecodeError in test39 preregistration.read_text():
CP932 could not decode UTF-8 byte0x94 at offset25. invocation_skipped=AUTHORING_RUNTIME_PREFLIGHT_FAILED;
experiment_executed=False;execution_log_publish_attempted=False. No new scientific result exists.
Operational log path:runs/c291-preflight-last.log. No failed scientific log publication is required.

Recovery code:02ba39b039d6d85b04c5a536f1fc44b6058351c9.
Current test blob:f9d14c3228bb0ab55c95f4998b7b9c293909be93.
Only C291 tests39/40 changed:four text reads explicitly specify UTF-8;test39 exercises its actual
inventory reads with an emulated CP932 default;test40 rejects implicit reads in the C291 source/test.
All40 test IDs remain;tests01..38 are AST-identical. No scientific source,runner,launcher,prereg,
manifest,loss,seed,data,threshold or workload change. No accepted parent files or logs were modified.

Recovery review:docs/c291-cp932-preflight-recovery.md.
post_authoring_review=PASS (committed-byte/static and local40-test module,normal and CP932-emulated).
Remote repaired test fetched and matched to local Git blob after commit;diff confirms only one
code file changed. All6 local OWN blobs match the current/unchanged repository blobs.
Post-match normal40 PASS in6.705s;post-match CP932-emulated40 PASS in6.461s.
Original actual test39 reproduces the same error under the same emulation;repaired tests pass.
Python/embedded blocks compile;unresolved-global audit0;manifest digest unchanged.
This is Linux/Python3.13.5/PyTorch2.10.0+cpu with the existing small-model/mocked-parent fixtures,
NOT real Windows,FOLD15-model science or the full4285 regression suite. CP932 emulation covers
Path text-decoding defaults only. No user locale/environment change is required.
Mandatory Windows Validate and the real experiment remain pending. Do not weaken or bypass them.

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
