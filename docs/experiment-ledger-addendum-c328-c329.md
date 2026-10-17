# C328 acceptance and C329 handoff

Review date: 2026-10-17 Japan time.
Formal verdict: C328 ACCEPTED VALID NEGATIVE. Scientific status FAIL; execution valid.
C327 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY), C326 remains VALID NEGATIVE.
Gate F NOT PASSED. No production adoption. C329 is not registered by this acceptance.

## Evidence identity and review boundary

Scientific execution HEAD: 3507021e46d47f6543316d46dc4481d3ead04855.
Published log commit: edf05c01e7fcd91b95c425fca5e7c416150689aa.
The publication commit's sole parent is the scientific execution HEAD.
Metadata: docs/experiment-run-logs/c328/latest.json; experiment_id=C328.
Published log Git blob: 72c877b8a03c7cb063612ca47f79ec12275bc15a.
Publisher-reported original Windows bytes: 155434.
Publisher-reported log SHA256:
826544d4cd7d9c3127723153c0de286b4c3c709e0f674533b0a92382d53fbbc9.

Reviewed the exact-ref metadata, native startup/registration, regression completion,
all ten fits, five common-prefix confirmations, ten checkpoint replays, all ten seed
flags, all five complete paired count records, final input rereads and terminal
fresh-process verification. Independently summed the published deciding counts.
The reviewer did not independently rehash the whole Windows log or recompute the
local checkpoints/logits. One compact metric record was inspected for context;
no claim of independently inspecting every local metric cell is made.
Older attached C323/C324 logs are NOT evidence for this C328 judgment.

## Execution validity

5722 tests / 217 modules PASS; failures=errors=skipped=0; 961.811 seconds.
Ordered suite-ID SHA256:
28d0bab050e4101f2e6a757cd34d096ed6026325c294fbebaacb06b629aa7c37.
Native read leases and parent semantic reconstruction passed. All five actual
schedules passed native preflight. Protection: 826 sources / 1561 inputs.
Ten fits completed all 1200 updates each. All five paired first-800 model/optimizer
states matched exactly. Each late_tenth arm used original rates through update800
and the registered tenth rates afterward. Ten checkpoint replays passed.
Saved reconstruction, all1561 final uncached rereads and fresh envelope verification
completed. Regression/science/verify exit codes were zero; run_execution_valid=true.
Scientific work: 10 models,12000 updates,576000 training-row presentations,
15420 model forwards,904320 total rows,61680 core forwards,10 checkpoint state loads,
one replay-bundle read and one new bundle write. Preflight/tests are separate work.

Local folder: runs/c328-late-rate-206451e9574c4b578b5cff4201af284b/.
Primary science/summary.json SHA256:
10bf430e74311a883cbcc7a7b70b589490a98d0f6db4458bcfe8be748fbccb53.
Companion execution-envelope.json SHA256:
d675bf546fb9d46eecf86b9a53847c5c054f4de618f311e0426a195c49f7cc32.
Eight science outputs plus primary/envelope make TEN immediate-parent files.
C328 manifest SHA256:
75f3de53837dcc64127b72f541ded650436b3a6ac46686bd9d8ff2aa8b89a226.

## Deciding paired HOLDOUT counts

Counts per seed: interior288 answers /144 query pairs; original pooled2..6 is
1440 answers /720 pairs. Gains are late_tenth minus constant.

| Seed | Interior correct constant -> late | Interior both-correct constant -> late | Original answer gain | Original pair gain |
|---|---|---|---|---|
|328001|259 ->235|120 ->100|-29|-29|
|328002|266 ->218|124 ->97|+14|+14|
|328003|276 ->273|132 ->129|+3|+4|
|328004|271 ->265|129 ->123|-45|-44|
|328005|278 ->270|134 ->127|+4|+6|

Interior answer sum1350 ->1261 of1440 (93.75% ->87.569444%); gain-89.
Interior both-query sum639 ->576 of720 (88.75% ->80%); gain-63.
Interior rescued/regressed answers40/129; rescued/regressed pairs19/82.
Original pooled gains across all five seeds: answers-53, pairs-49.
These pooled denominators reuse the same logical tasks across seeds/profiles and
are descriptive totals, not independent sample counts for significance claims.

Composite paired success:0/5. Interior complete gate:0/5 in BOTH arms.
Original2..6 retention gate:0/5 in BOTH arms.
Original length gates passed, constant/late_tenth:
2:5/5,3:5/5,4:3/3,5:1/0,6:0/0 (each numerator out of five seeds).
High pooled normal accuracy does not override failed local, masked, pair or order
conditions. No threshold, seed, comparator or exposure was changed after the run.

## Interpretation and non-claims

At the registered fixed1200-update budget, scaling both learning rates by0.1 after
800 updates did not improve the objective; interior answer and pair counts worsened
in every paired seed. This is stronger than merely failing a stringent composite
criterion, but does not establish that ALL learning-rate decay policies are harmful.
C327 terminal Euclidean gradients did not predict finite AdamW improvement here.
The experiment does not identify full-trajectory causes, prove a capacity limit,
establish that longer training works, or show unseen-template/general LLM ability.
Terminal minibatch CE is not a full TRAIN-set loss or an early-stopping criterion.

## Next question, not yet execution authorization

A bounded next test should compare the same constant-rate trajectory at1200 and2400
updates, with a repeated identical1200-event batch4 schedule and preserved optimizer
state. This tests a fixed extra-training budget, not a new decay ratio or a search.
Use fresh preregistered seeds, preserve both checkpoints without evaluating midway,
and keep all original/interior gates and paired comparison semantics explicit.
Separate implementation/preregistration, committed-byte review and activation are
required before a C329 command. Do not rerun C328 or reuse its weights for fitting.
