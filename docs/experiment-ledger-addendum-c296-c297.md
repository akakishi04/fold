# C296 formal acceptance and next diagnostic boundary

C296 ACCEPTED VALID NEGATIVE. Scientific execution is valid;balanced quad gate3/5 misses the preregistered5/5.
C295 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C297 NOT REGISTERED in this acceptance commit.

## Evidence identity

Scientific execution HEAD:3d52da4b565d05727b604560bbf60710dd9536e2.
Published log commit:16d3800de33edda84b88904b805029912de4ddc0.
Metadata log SHA256:c527d43d81902f20c5f5b7c7f136ba67832a3f17454be42fb638c22e47d4fe8a;757918 bytes.
The publication changes only docs/experiment-run-logs/c296/latest.json and latest.log.
Summary:runs/c296-v5b-render-batches-653d5ee53ab747f69da1611a8fc69630/summary.json.
Summary SHA256:d48c4c6725cecdf9e15034448186fe39b7e8b86b45f7a6418c839e2536f1093b.
Source Git blob:ae4fd7a45ec9306b1b81a82f8707269f1d88277b.
Manifest SHA256:b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9.

## Validity

Own40 and focused4461 PASS;the focused suite completed in506.947s. Preflight PASS.
Source622/protected1131;all10 models complete800 updates. Exact per-block rendering multisets,
common final8 updates and independent identical initial states were checked by the C296 path.
all_pairs_matched=True;persisted_render_batch_scores=PASS;tracked_tree clean;execution_HEAD preserved;
run_execution_valid=True. Scientific status FAIL and candidate_gate False reflect capability,not integrity.
No rerun of C296 is needed. Original full/masked criteria and all seeds remain unchanged.

## Deciding metrics

Counts blocked/balanced:quad2/3;two_char4/4;triple4/4;all_tasks2/3;fitted TRAIN direct5/4;
seen-length HOLDOUT direct4/4. Quad paired results:
296001 FAIL/PASS;296002 PASS/FAIL;296003 FAIL/PASS;296004 PASS/PASS;296005 FAIL/FAIL.
Two rescues and one regression are not a robust uniform benefit. Ordinary-TRAIN fitting also loses a seed.

Seed296005 balanced TRAIN correct two557/576,triple559/576;blocked triple573/576.
HOLDOUT triple blocked153/288 versus balanced80/288;quad155/288 versus85/288.
Balanced quad HOLDOUT errors:154 absent-known-value,49 other-fact,0 non-value outputs.
Thus the net increase in fully passing seeds hides substantial regressions on a failed seed.
No claim of universal benefit,forgetting,gradient conflict or model incapacity is supported.

## Next question

Previous paired comparisons used one seed to select both parameter initialization and example shuffle.
A separately preregistered crossed diagnostic can hold these independently:three fresh initial states
by three fresh training-order streams,ordinary CE/blocked800 throughout. Evaluate all nine cells,
not selected winners. This diagnoses finite-grid sensitivity,not a new capability candidate,not
an estimate of population variance components and not a relaxation of C296's5/5 gate.
No Gate F promotion or deployment selection is authorized by such a diagnostic.

## Parent output receipt sealed by the exact summary

architecture-plan.json:2674 bytes;b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9.
dataset.json:36024 bytes;1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
triple-dataset.json:158236 bytes;432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
quad-dataset.json:172066 bytes;86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
trained-models.pt:1238007 bytes;d3444d3484cce4f8c4228139c460e9f2734406eb186f279bca6344b0ceeec522.
evaluations.pt:165661923 bytes;1fe48f5db5b8e5813e363fbf0318d4f2ae0782c5703b2b1b1173eae515f5df4f.
measurements.json:787690 bytes;d1dd50c63ecc614f8a43b620a035162cef12b0b4e7e6fe2713b7fb90c4cac086.
validation-summary.json:66447 bytes;1aaba3dc4e3ffb1e9f552515f9a23c4cd4d6fc5b3fad661ceb60d16d0d885516.
