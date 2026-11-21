# C311 formal acceptance — saved error-context diagnostic

C311 ACCEPTED PASS (diagnostic integrity only). C312 NOT REGISTERED at this acceptance.
C309 remains ACCEPTED VALID NEGATIVE; C308 remains bounded ACCEPTED PASS; Gate F NOT PASSED.

## Evidence and execution validity

Execution HEAD: a777fc793b2affe287d055733b012ea919504446.
Publication commit: d894b4b26ffb821bcd89db17b70d4f9798d3e1ee.
Console log: docs/experiment-run-logs/c311/latest.log.
Metadata SHA256: 8eee2426b01cf8986bda330be74b289c5b97b8266fdaee800cc3105558a28581; 755416 bytes.
Summary: runs/c311-v5b-error-context-2e3d082f8a9a4045b09dbe38a62ca6a8/summary.json.
Summary SHA256: 9bfdad83b33d24a986c3f76ef0e40d0ad323698b28826f80f659ff5fa6e0cdec.
Manifest: b9e5f42cf681031892d77f2f134bc307d56233f22e039cac13009b3cd90b34fd.
Own24/focused4965 passed; full regression701.240s. Source712/protected1333.
All51840 saved answers classified;2160 value-pair groups,720 language groups,90 signature groups.
Published postcheck: diagnostic_complete=True; persisted_error_context=PASS;
model_forward_calls=0; tracked_tree clean; execution_HEAD preserved; run_execution_valid=True.
Publication changed only latest.json/latest.log. No C311 rerun is needed.
Evidence reviewed is the immutable published receipt, not access to the user's local result JSONs.

## Deciding focus: seed309002, five-character HOLDOUT

All arms retained. Each arm has288 normal answers; profiles each96; ordered value pairs each72
across profiles. Counts in full_train/core_frozen/core_slow order:
errors11/49/19; other_fact1/11/2; unmentioned_digit10/38/17; non_digit0/0/0.
Four-to-five matching: both_wrong3/33/13; newly_wrong_at_five8/16/6;
four_wrong_but_five_correct0/1/0. Thus slow has13 of19 five-errors already wrong at four,
including11 questions wrong at all four lengths. No claim that length adds zero errors.

Slow errors by profile:repeat5,shared_prefix8,shared_suffix6.
Slow errors by ordered pair:(0,2)=7,(1,3)=3,(2,0)=1,(3,1)=8,denominator72 each.
Frozen errors by ordered pair:3/17/11/18. Full:1/4/4/2.
No single held-out ordered pair contains all failures. Slow outputs largely unmentioned digits;
that does not prove memorization,attention failure,or minibatch imbalance as a cause.
All findings are descriptive of the fixed C309 saved cohort,not new independent observations.

## Next boundary

A separately preregistered C312 will test TRAIN value-balanced minibatches, holding core_slow,
1200 updates,2/3/4 training lengths,64 slots,logical examples and exposure counts fixed.
Compare the original random24-pair minibatch with one containing3 query pairs from each of the
8 original ordered TRAIN value-pair strata. Complete every96-pair epoch without replacement;
retain both questions of each fact pair and the same per-epoch length/profile.
Only minibatch composition/order changes. Do not expose original HOLDOUT pairs as augmentation.
Use fresh paired seeds,not failed309002 alone. This is not proof that imbalance caused C311.
C312 requires committed source/tests/preregistration and post-authoring review before activation.
