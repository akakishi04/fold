# C301 formal acceptance — valid negative

C301 ACCEPTED VALID NEGATIVE. Candidate learned_gain passes1/5 quad gates,not the registered5/5.
Fixed_gain passes2/5. C300 remains diagnostic ACCEPTED PASS. Gate F NOT PASSED.
C302 NOT REGISTERED in this acceptance commit;no experiment is ACTIVE until its separate review.

## Evidence and validity

Scientific execution HEAD:d67c900c588ff0e4c8974cd8f80721da381a8770.
Published log commit:871d5c55a0cb8139a1ff95fbfce95b7472bf16fa.
Publication changes only docs/experiment-run-logs/c301/latest.json and latest.log.
Metadata log SHA256:374f10a81899dd7bed318c9b7dc79b5f6bf03694187629d929089effb8d823f9;737603 bytes.
Summary:runs/c301-v5b-residual-gain-8e72f4cf3e744128b905da20770c9f5b/summary.json.
Summary SHA256:19d5a94c3ce5d2bef94683b05983c44b1e76f452490e184f8ffde7b934d559c1.
Manifest:c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9.
Own40/focused4637 PASS;focused suite551.652s. Source652/protected1202.
All10 fits,evaluations and strict replay completed. all_pairs_matched=True;
persisted_residual_gain=PASS;tracked_tree clean;execution_HEAD preserved;run_execution_valid=True.
Scientific status FAIL is a valid capability negative,not execution failure. Do not rerun C301.

## Deciding measurements

Fixed/learned counts:two_char2/3;triple2/3;quad2/1;all_tasks2/1.
Fitted-TRAIN direct3/3;seen-length HOLDOUT direct2/3.
301002 passes every task in both arms. 301003 passes all tasks in fixed_gain but fails quad in
learned_gain. 301005 gains seen-length task passes but still fails quad. 301001 and301004 fail
seen-length TRAIN in both arms. No universal rescue or superiority is established.

Learned final gains by seed:
301001:0.8684034644345564
301002:0.7330682658799806
301003:0.7781612711147479
301004:0.8356705336201741
301005:0.7789613854784259
All are below1,not evidence that reducing the residual is universally better or that the gain
alone caused any change. The jointly learned common weights can compensate/rescale.

301005 normal correct counts(fixed->learned):two TRAIN574->576,HOLDOUT278->288;
triple TRAIN573->576,HOLDOUT273->288;quad TRAIN557->572,HOLDOUT262->283.
301003 learned quad HOLDOUT287/288 versus fixed288/288;it loses the quad gate.
301004 HOLDOUT two161->212,triple151->203,quad149->191,but fixed gates remain unmet.
301001 HOLDOUT two141->119,triple135->119,quad132->122:some held-out outcomes deteriorate.

## Interpretation boundary and next question

C301 changed both the eventual coefficient and the optimization trajectory of every common
parameter;the scalar also participated in global clipping. Do not attribute the whole outcome
to the final coefficient or claim that a smaller gain is the measured optimal inference setting.
A separately registered frozen cross-evaluation can hold each learned state fixed and compare
alpha1 with the candidate's TRAIN-learned alpha from the same seed. Evaluate both weight sets
at both gains,with original-before/after reproduction. No new training,gain sweep,seed removal,
per-question choice or best-cell adoption. Such a test isolates an immediate inference intervention
at fixed weights but does not uniquely identify the mechanism of training failure.
