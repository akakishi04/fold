# C262 acceptance and C263 learning-rate interaction boundary

## Formal verdict

C262 ACCEPTED VALID NEGATIVE. Forward blocks passed0/5 and reverse blocks2/5; the
registered joint all-ten-state robustness gate was not met. This does not erase the
positive evidence that minibatch chronology changes answers with initialization and
exposure counts held fixed. Capability robustness and sensitivity are different claims.
Gate E PASSED; Gate F NOT PASSED. All earlier verdicts remain unchanged.

Scientific execution HEAD:28030ad02e69a9ae7236fca7f7e84a61f3c89c46.
Published log commit:4dc8fec24578efa5f7d8abfea17c56be2dc23673.
Publisher log SHA256:9dc5f6850866548f8f1e3a6681e2aab58069c36526d3355321ae814c05d502f7.
Log bytes:768728; lines3833. Publication is one commit after execution and changes
only docs/experiment-run-logs/c262/latest.json and latest.log.
Summary SHA256:9cda47219d6e376516044d5807e546a8c13110f584f139bda2a3da8800b2d93d.
Summary:runs/c262-v5b-batch-order-b955446fc91846aa9fea770cd36b9276/summary.json.
Acceptance uses immutable log ranges,metadata and recorded user-local postchecks.
The reviewer did not independently rerun learned checkpoints or rehash the full log.

## Execution validity

Own24 PASS in5.976s; focused3453 PASS in314.228s. Source pins418/protected inputs697.
Ten800-update runs completed:8000 updates,384000 training rows,8240 wrapper forwards,
435840 total row presentations and32960 core calls. One ten-state bundle write/load;
ten strict state loads. Initial-state and exact-exposure matching,changed chronology,
checkpoint fingerprint/logit/argmax replay,score/flip reconciliation,persisted
recomputation and protected-input checks passed. Tracked tree clean; execution HEAD
preserved; run_execution_valid=True. scientific_status=FAIL; joint_gate=False.

## Deciding HOLDOUT evidence

All-six-order answer counts have denominator216 per language:

|Seed|Forward EN|Forward JA|Reverse EN|Reverse JA|Forward gate|Reverse gate|
|---:|---:|---:|---:|---:|---|---|
|262001|202|197|216|216|ORIGINAL_CRITERIA_MISS|PASS|
|262002|156|161|132|129|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|262003|146|136|144|139|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|262004|123|124|150|152|ORIGINAL_CRITERIA_MISS|ORIGINAL_CRITERIA_MISS|
|262005|146|152|216|215|ORIGINAL_CRITERIA_MISS|PASS|

Pooled forward1543/2160=71.4352%;reverse1709/2160=79.1204%. Seven paired language
accuracies improve and three decline; no tie. Pooling does not replace the fixed gate.
Across2160 matched HOLDOUT questions,639 answers differ:201 forward-correct/reverse-wrong,
367 forward-wrong/reverse-correct,and71 different wrong answers. Net correct-count
change367-201=166 equals1709-1543. These are correlated answers,not2160 independent runs.
Seed262002 is worse under reversal; reversal is not a universally better curriculum.
The two reverse passes do not authorize selecting only that schedule or those seeds.

## Interpretation and limits

The specified minibatch chronology intervention changes task performance even with
complete initial state and exact prompt exposure held fixed. Earlier seed variability
cannot be explained by initial weights alone. This experiment does not identify which
optimizer mechanism mediates that sensitivity or explain every historical failure.
All six fact orders were training-visible; the authored task has been repeatedly
inspected. No general-language,independent-benchmark,core-superiority or production claim.

## Accepted artifacts

-batch-plan.json:2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c;2869 bytes.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:f360dccf8b5523b27755e87734b0ae1c1b4ab8628b4e9c3fb32ada20f102db2f;53132231 bytes.
-measurements.json:13ffc5ce99372df17914f5a8cc07e03ba63e74cd091a24e650db62c6273e5e8d;62906 bytes.
-trained-models.pt:84ce31fe704c193a9a5f17a0e9023b9f6d4dc84fd25badafd118a95738595713;1238007 bytes.
-validation-summary.json:d2843f6443c759795f50f81e68fc35cf742c28f3657716812207b756aab4c864;4308 bytes.

## Next question, not activation

Does lowering AdamW learning rate from0.005 to0.001 reduce sensitivity to the same
forward/reverse block intervention while retaining the fixed task criteria at800 updates?
Use five fresh seeds and a paired2x2 design:two rates by two chronologies. Within a
seed all four models start with identical Full aligned-reader weights; same-order
rate contrasts see identical batches at each update. Do not reuse learned C262 states.
No schedule is discarded because it looked worse. No rate sweep,extra updates or
post-result selection. Low-rate underfitting is a valid negative,not grounds to extend.
Reduced disagreement alone is not useful robustness if both models answer incorrectly.
Separate capability gates,order-disagreement contrasts and rate effects. A capability
PASS does not alone prove that learning-rate reduction helps. C263 requires separate
preregistration and committed-byte review; C264 is not registered.
