# C246 acceptance and C247 normal-exposure control boundary

## Formal verdict

**C246 ACCEPTED VALID NEGATIVE.** Gate E PASSED; Gate F NOT PASSED.
C245 remains diagnostic-integrity PASS; C244 remains a valid recombination negative.
The registered training-only erasure recipe did not meet the normal-input capability criteria.

Scientific execution HEAD: c17195b7c0f80ae7dd60050e25dca6a3effc21fb.
Published log commit: 30142c60dedf52537c9cef26b35ca2909446b5ee.
Publisher log SHA256: ceaec8ba66f2609acf18663c76b7925fb8053a91f8d199075b50d697ae566362.
Log bytes: 589070.
Summary SHA256: 9a462485dffc948674b7752012893a8175cdb5de251f179763ae03e26659623a.
Local summary: runs/c246-v5b-training-erasure-471de735eb204a129692672d2849c270/summary.json.

Publication is one commit after execution and changes only c246/latest.log/latest.json.
Acceptance uses immutable log ranges, metadata and recorded local postchecks, not an independent
complete-log rehash or a reviewer rerun of the actual learned models.

## Execution validity

24 own tests PASS in3.973s;3073 focused tests PASS in71.197s.
322 source pins/502 protected inputs. Six models completed400 updates each:
2400 training updates/76800 training presentations,38400 normal and38400 masked.
All block_view_updates matrices are [[100,100],[100,100]].
2490 total model forwards/81408 total row presentations. All replays/weight changes PASS;
persisted normal endpoint/comparator/discrete replay PASS. Protected inputs, clean tracked tree
and execution HEAD were preserved;run_execution_valid=True.
Scientific status FAIL;full_augmentation_gate=False;gru_augmentation_gate=False.

## Deciding metrics

The table gives exact normal-answer counts, in EN/JA order. Each TRAIN language cell has32 rows;
each HOLDOUT language cell16 rows.

| Seed | Full TRAIN | GRU-only TRAIN | Full HOLDOUT | GRU-only HOLDOUT |
|---:|---:|---:|---:|---:|
|234001|18/32,18/32|31/32,32/32|5/16,4/16|6/16,9/16|
|234002|16/32,16/32|18/32,16/32|6/16,6/16|7/16,8/16|
|234003|17/32,17/32|16/32,22/32|8/16,8/16|6/16,6/16|

All six Full cells and four GRU-only cells fail TRAIN criteria. Only GRU-only seed234001 in both
languages passes the full TRAIN criteria; those two still fail HOLDOUT. Thus the exact outcomes
are TRAIN_CRITERIA_MISS:10 and RECOMBINATION_MISS:2.
Full TRAIN pooled102/192;GRU-only135/192,versus192/192 each in C244.
Full HOLDOUT37/96 versus C24439/96;GRU-only42/96 versus41/96.
Combined descriptive HOLDOUT79/192 versus80/192:5 improving cells,2 ties,5 worsening cells.
These are correlated small-fixture summaries, not independent replicates or significance tests.
An early conversational tally of78 was corrected to79 after exact integer aggregation.

## Interpretation and non-claims

The input augmentation did not demonstrate useful normal-input transfer and often lost even the
previously achieved TRAIN fit. Better accuracy when erasing an input at inference in C245 did not
translate into a successful mixed-view training recipe in C246.

C246 replaced half the ordinary presentations rather than adding budget. Reduced normal exposure,
masked-task learning, switching dynamics and optimizer state are not separately identified.
Do not conclude that erasure is universally harmful, the architecture is impossible, or one module
is the cause. The actual masked-training-task accuracy was not measured by C246; do not claim
that the model mastered the simplified task. Keep C246's negative and all previous results intact.

## Accepted artifacts

- measurements.json:81b6aaa5ae69be11e49bb0e64dff0763d8f12437393df18ff4c7ca346d8d908b (24449 bytes)
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346 (15904 bytes)
- trained-models.pt:8282b378bea2c6ff166fb18ed9345bfee71ab5ac2080204a43251229f8b6fd34 (601940 bytes)
- training-plan.json:761b00863243d9118cd85058f585b7e3592404c677b8d8f548be45ed2fd05db8 (2725 bytes)
- validation-summary.json:68ccff53230dc8ab8fcf24d542547ade89f63335c4fd508db401ff0e68b80cf3 (438 bytes)

## Next question, not registration

Is C246's ordinary-example exposure alone sufficient to fit the original TRAIN task when no
masked updates are interleaved? Use fresh identical initial states, exact C244/C246 partition,
normal row order and optimizer settings, but only200 normal updates per model:100 presentations
per TRAIN row, matching C246's NORMAL portion. No masked forward, zero-loss placeholder update,
idle optimizer step or continued training from accepted checkpoints.

This is a missing normal-exposure control, not a retry or rescue. Compare its original TRAIN
criteria with C246 at equal normal exposure and with C244's400-normal-update record. HOLDOUT is
reported on the same unchanged rows, but the primary question/gate concerns normal TRAIN fitting.
A primary PASS is budget-sufficient TRAIN fitting, not new generalization or Gate F completion.

If the control fits while C246 does not, fewer normal presentations alone cannot explain those
specific misses. If it does not fit, the reduced normal budget is compatible with the failure,
but that does not exclude an additional effect of mixed training. Optimizer step count and state
naturally differ when the200 masked updates are removed; no unique internal mechanism is isolated.
Separate preregistration and committed-byte authoring review control C247 readiness.
