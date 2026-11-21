# C269 preregistration — paired query-span pooling

## One scientific question

With the same paired CE-only training, does replacing the actual C252 pre-core EOS query vector with
a visible query-span pooled pre-core vector improve reliable held-value binding across five fresh
initializations?

C268 is ACCEPTED VALID NEGATIVE at execution
aa45ea5df68dcba70c99a009c46b7bf8468304a1. Its paired-margin treatment and CE control each passed
3/5 seeds. C269 does not tune that loss. It returns both arms to ordinary CE and changes only the
reader query source.

## Arms

Fresh seeds:269001..269005. Arms: eos_query and span_query.

eos_query is the unchanged actual C252 AlignedPrecoreReadout created through the existing C256/base
factory path. Its query is read.query(pre_core_EOS_local_state).

span_query has the identical14256-parameter state layout and exact same initial tensor values.
Its query source is the mean of pre-core local states at positions strictly after the final visible
';' byte59 and before the final visible '=' byte61. The final '=' must be EOS-1. The span must be
non-empty and delimiter-free. UTF-8 multibyte identifiers contribute all their bytes. No entity ID,
target, split, profile, query-pair index or supervision metadata enters model.forward.

Both retain the same masked pre-core memory, read.query/read.key/read.output weights, score divisor4,
PAD masking, actual Full core path, post-core EOS residual, readout_norm and decoder. No parameter
or state is added. Candidate initial state is strict-loaded from the matched control and parameter
storage must be disjoint.

## Fixed data and training

Use the exact C267 dataset SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1:
TRAIN192/HOLDOUT96 logical rows, three two-entity subsets, both languages, both visible fact orders,
both queries, distinct values0..3 and all three naming profiles doubled/shared_prefix/shared_suffix.
The four held value pairs remain completely absent from optimization. Names/profiles are TRAIN-seen;
this is not unseen-name transfer.

Partition TRAIN into96 groups keyed by language/entities/values/permutation, each containing the two
different queries. For each fresh seed and epoch, randperm96 uses seed+269000+epoch. Four consecutive
24-pair blocks create48-row batches. Profile=epoch%3.800 updates=200 full epochs, so each TRAIN row
appears200 times per arm and profile updates are268/268/264. Both arms use identical logical batches.

Both optimize mean cross-entropy only. AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0;global
norm clip1. Reset fit RNG seed+270000 per arm. CPU float64,threads2,deterministic algorithms. No early
stop,extra updates,seed replacement,checkpoint selection,loss sweep or HOLDOUT optimization.

## Fixed gate

Use the unchanged C267 scorer. For every split/profile/language/entity-subset/visible-order answer
cell require accuracy>=.90,query_pair_accuracy>=.80,evidence_drop>=.35,query_drop>=.35. Require
two-order consistency>=.80. TRAIN cells16 answers/8 pairs imply15/16 and7/8 minima; HOLDOUT cells8
answers/4 pairs imply8/8 and4/4. Two-order minima are13/16 TRAIN and7/8 HOLDOUT.

Primary PASS iff all FIVE span_query seeds pass every fixed criterion. eos_query is reported
separately and cannot rescue or fail the candidate. Report30 paired HOLDOUT profile/language
contrasts, each48 answers/24 query pairs. Pooled accuracy or collapse changes are descriptive only.

## Accepted parent and provenance

Parent C268 summary:
runs/c268-v5b-query-loss-9f62513c65d34a7aa7b1452c9540a5a6/summary.json
SHA256:9e9ea4dd0d20b0ae0b8d315549a1cf1aa13c79853b3dd129c0f01e395a2bf67c.
Parent execution:aa45ea5df68dcba70c99a009c46b7bf8468304a1.
Require status FAIL,candidate_gate=False,seed_pass_counts ce_only3/ce_pair_margin3 and10 records.
Verify the six exact parent artifacts:
loss-plan cf16b504aa03e1e5f61c000c161b44c3a551fe7c103096c9119274947fb4e07b;
dataset 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
trained-models c4f7bfa9a38bffe871efda54dc9c06d0f82b8acf2b84b42344d6417455daba47;
evaluations 59a17ceb9d228ff4472394b2e9ef11bcf30d5e6d0c448163ac325dc7b10cc6d6;
measurements b95667f0de648574afacab38ef21fa1d24d0ba9945ff504eba04f5c4e4f8a00e;
validation-summary 2b20b57ccd87057405dd11600854d538b5ff933907665ee3c787243a4d96e209.
Parent verification is provenance only; no C268 learned checkpoint initializes C269.

## Workload and persistence

Ten models;8000 optimizer updates;384000 training row presentations. Per model:800 train forwards,
27 final-evaluation forwards and27 strict-replay forwards. Total8540 model forwards,435840 row
presentations and34160 actual core calls. One10-state bundle write/load and10 strict state loads.
Final/replay evaluation forwards total540. File hashing, parent verification and full regression are
additional work.

Artifacts:query-plan.json,dataset.json,trained-models.pt,evaluations.pt,measurements.json,
validation-summary.json plus summary.json. Bundle schema fold-c269-query-span-models-v1; evaluation
schema fold-c269-query-span-eval-v1. Persisted postcheck recomputes schedules,scoring,contrasts and
gate from saved tensors with learned Module calls blocked.

## Protection and regression

Inherit C268's454 source pins/774 protected inputs. Add the accepted C268 summary plus six artifacts
and C269 OWN6. Expected:460 source pins,787 protected inputs,45 deciding-path dependencies.
OWN6:
-fold_lm/v05_benchmarks/model_c269_query_span_pooling.py
-tests_lm/test_v05_c269_query_span_pooling.py
-tools/run_c269.ps1
-tools/invoke_c269.ps1
-docs/experiment-ledger-addendum-c269-preregistration.md
-docs/v5b-query-span-pooling-v0.1.md

Own24;modules154;loaded3622/focused3621. Sole inherited exact exclusion remains
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa.
Preserve tools/run_c167.ps1 and historical invoke_active.ps1 bytes. User execution continues through
the versioned PowerShell7 dispatcher invoke_active_v2.ps1 because the historical dispatcher is an
accepted pinned dependency.

## Interpretation boundary and stop

A candidate PASS supports only that explicit visible query-span pooling is sufficient to improve
reliability in this bounded structured family under the fixed policy. It does not identify a general
language parser or prove the EOS representation is universally harmful. A candidate miss is an
ACCEPTED VALID NEGATIVE if execution validity passes. Do not rescue by changing pooling rule,
learning rate,loss,steps,seeds or threshold after results. No Gate F promotion,production adoption,
paid API,external corpus,cleanup,history rewrite or CI change follows automatically. C270 NOT REGISTERED.
