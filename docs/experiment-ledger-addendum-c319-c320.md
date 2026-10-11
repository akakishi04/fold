# C319 formal acceptance — trained last-only valid negative

C319 ACCEPTED VALID NEGATIVE. Candidate last_only six4/5;mean_last control5/5.
C320 NOT REGISTERED in this acceptance. Gate F NOT PASSED;all earlier verdicts unchanged.

## Evidence

Scientific execution:529c54ef63b1015b25632b8123a9a552eebcd263.
Published log:3abe218dc9191d26963e5b5022d4d1983300084d.
Publication changes only docs/experiment-run-logs/c319/latest.json and latest.log.
Metadata log SHA256:1ebba1cdea333cb3be95d54d1cd321e424ff31c3da4053440b6cc88c31766022.
Summary:runs/c319-v5b-trained-last-0f94e96bbbba43b395fcf8eab1e38246/summary.json.
Summary SHA256:48815ca382d0da078da12ec2d54f2c42261e94498b682f679d8f46d746ec0580.
Own24/focused5197 PASS;focused tests completed in754.953s.
Source760/protected1429;all10 fits/evaluations/same-policy replays completed.
all_pairs_matched=True;persisted_trained_last=PASS;run_execution_valid=True;
tracked tree clean;scientific execution HEAD preserved. Do not rerun C319.

## Deciding results and limitations

Both arms5/5 at lengths2,3,4,5. Six mean_last5/5,last_only4/5.
Paired six:4both_pass,1control_only,0candidate_only,0both_fail.
Only last_only319005 fails six:TRAIN-value567/576,HOLDOUT-value283/288.
Its paired mean_last gives575/576 and288/288 and passes the original full gates.
Thus a gate PASS need not mean perfect pooled normal accuracy. Do not alter local thresholds.
Candidate failure is not a model load/policy failure. Last-only learned many tasks but this
cohort does not support replacing native mean-plus-last for stronger six reliability.
The comparison is bounded;it does not prove two branches universally necessary or uniquely causal.

## Next scientific boundary before registration

Keep native mean-plus-last as the default rather than continue small seed/readout searches.
Propose frozen unequal-name-length transfer:two names within one question have lengths2 and4,
then4 and2,while all names remain inside the trained length range. Original training used equal
lengths for both names. This tests that unexamined within-question equality constraint,not a
longer frame or new vocabulary. Keep all10 C319 models and their respective trained readout
policies;original1..6 before/after must reproduce. No training,checkpoint filtering or repairing
C319. Prospective primary would be all5 retained mean_last baselines passing both new layouts;
last_only remains a full comparator. Register and review separately before any execution.
