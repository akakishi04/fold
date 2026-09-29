# C285 acceptance and next fixed-budget optimization question

## Formal verdict

C285 ACCEPTED PASS (diagnostic integrity only). Capability_gate_applicable=False.
Gate F remains NOT PASSED. C284 remains ACCEPTED VALID NEGATIVE; its quad gates are
three_char_only2/5 and mixed_length3/5. No seed selection,rerun or retrospective gate change.

Scientific execution HEAD:f2bd32785895c30defa16be7d1eca6279ba4ed23.
Published log commit:d8a24df7b94a1b8c3d339b868c6db4fc2ed7e3b6.
Publisher log SHA256:b11036503e521d94a6ff64a4abd51721334c2100428100a3b868f6db1ad3e700.
Publisher log bytes:881390.
Summary:runs/c285-v5b-saved-length-audit-94786461780e4110a04f18ca3c92c427/summary.json.
Summary SHA256:702092926265bb893babce1e5b93dd234791527344193ea876d33210e8bfdba1.
Manifest SHA256:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c.

## Execution validity

Published own32/focused4045 PASS. Source556/protected991 and sealed manifest checks passed.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True.
All3240 fixed records and accepted parent seed/task flags reconstructed. Parent loader is actual
C284.verify_artifacts with neural Module calls,state loading and torch.save blocked.
Scientific model_forward_calls,row_presentations,core_forward_calls,train_steps,model_state_loads,
new_checkpoint_writes and network_calls all0. Persisted output reconstruction passed and tracked
tree/execution HEAD were preserved. This is a saved-output audit,not independent replication.

## Deciding metrics

Quad between-arm fixed-criterion failures (left=three_char_only,right=mixed_length):

|criterion|left_fail|right_fail|rescued|introduced|
|---|---:|---:|---:|---:|
|accuracy|50|43|14|7|
|query_pair_accuracy|48|43|12|7|
|evidence_drop|27|27|5|5|
|query_drop|30|38|6|14|
|two_order_accuracy|21|20|3|2|

The first4 criteria have360 matched cells each;two_order has180. Criteria overlap.
Pooled normal correct4139/4320->4149/4320;collapse97/2160->80/2160.
Evidence-blind correct1080/4320 in both arms;query-blind1881/4320->1983/4320.
Quad mask-only failing answer cells0 in both arms. Equal pooled counts do not imply identical outputs.

Within-state triple-to-quad accuracy:
-three_char_only:39 already-failing matched cells persist;11 new failures;0 rescues;quad total50.
-mixed_length:37 already-failing matched cells persist;6 new failures;0 rescues;quad total43.
Mixed query-pair:37 persistent+6 new=43. Mixed two-order:18 persistent+2 new=20.
Mixed evidence-drop:25 persistent+2 new=27. Mixed query-drop:32 persistent+6 new-3 rescued=38.

Seed284002 accounts for42/43 mixed quad accuracy failures,all27 evidence-drop failures,
all38 query-drop failures,all20 two-order failures and all80 mixed quad collapsed pairs.
Its mixed triple/quad normal correct counts are710/864 and694/864. Mixed seed284001 has one
quad answer error (863/864),one failed accuracy cell and one failed query-pair cell;its original
triple task was perfect and it has no quad collapse. Mixed284003/284004/284005 pass all quad gates.

## Interpretation and non-claims

Most mixed quad failing accuracy cells already fail at the trained three-character length.
This is not only an unseen-length boundary problem. However,a task includes TRAIN and HOLDOUT;
co-failure does not by itself establish training-set underfitting,late optimizer oscillation,
a particular shortcut or causal inheritance of the same erroneous rows. Do not diagnose an
optimization cause solely from these scalar/paired-cell results.

The previous mixed-training advantage is modest and heterogeneous once maximum trained length is
matched. Direct answer failures remain;mask-only failing answer cells are absent. Query-drop is
worse overall for mixed_length,localized to the shared problematic seed,not a uniform intervention
benefit. No independent population-superiority claim is warranted.

Before another architecture/support/coverage change,a bounded learning-policy intervention is a
reasonable falsifiable next question:at the same mixed2/3 data,initialization and800-update budget,
does reducing only late learning rates improve final seen-length reliability and unseen quad
performance? This is a hypothesis test,not a claim that C285 proves constant LR caused failures.
A prior lower-constant-LR result does not answer a time-dependent late-decay question.

## Accepted artifacts

-audit-plan.json:cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c;3246 bytes.
-cell-attribution.json:2d733c0d92bf57678ff610153aab95d48ab2b1c17ec67d8bc447cedd2c2f8b15;1687080 bytes.
-validation-summary.json:a814abd30a8a5432722ed35ae0ee19d87706aa4db5a876a58887e4de4e6ebf3b;29907 bytes.

## Next question,not activation

Propose fresh paired constant_lr versus cosine_tail mixed2/3 training. Both use actual C278
all-token MeanFinalDualReadout,14256 parameters,48-token context,800 updates and unchanged scorers.
The first400 updates use lr.005 in both. For updates401..800 the candidate follows the fixed cosine
curve from.005 toward.0005,while control stays.005. No warmup,extra steps,seed selection,quad training,
loss/architecture change or checkpoint selection. Record and verify actual LR histories and require
paired step400 fingerprints to match before interpreting the intervention.
Primary remains all-five candidate quad PASS;two/three/all-task gates and paired results are
reported separately. No automatic Gate F promotion. C286 requires separate preregistration,source,
tests,runner,manifest sealing and committed-byte review before activation. C287 NOT REGISTERED.
