# C286 acceptance and C287 saved fit/generalization partition audit

## Formal verdict

C286 ACCEPTED VALID NEGATIVE. The preregistered cosine_tail four-character gate passed3/5,
not the required5/5. constant_lr passed2/5. This is a valid scientific miss,not an execution
failure. Gate F remains NOT PASSED. No C286 rerun,seed replacement or retrospective gate change.

Scientific execution HEAD:7fe7c72ff88e252b3087c9715674510dbba96651.
Published log commit:672b7cc1bf0f75f55c058e73e30ea69e249b2108.
Publisher log SHA256:dee4ea1485ddd71b91dd4934bbbf6521f93be65017feff8e719a97c6b564b0f2;914737 bytes.
Summary:runs/c286-v5b-cosine-tail-1664d75f4cf649fb8c5ca98f4be8308b/summary.json.
Summary SHA256:14bfe8920b80c86cc8e297864402c38c53a26c87085b8963cae363cb6fd98a9a.
Manifest SHA256:3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e.

## Execution validity

Remote latest.json identifies the registered execution HEAD;the log commit is its direct child.
Runtime Validate passed own40/focused4085 (356.766s) and source562/protected1001.
The planned10-model,8000-update experiment completed. Workload9620 forwards,539520 row
presentations,38480 core calls,384000 training rows;one final10-state bundle write/load and10
strict state loads. The verifier requires matching initial states,batches,actual applied LR
histories,step400 fingerprints and first400 losses;all_prefixes_matched=True.
Persisted scoring PASS;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;candidate_gate=False. Known errors are scientific outputs,not integrity errors.

## Deciding metrics

|task gate|constant_lr|cosine_tail|
|---|---:|---:|
|quad primary|2/5|3/5|
|two_char descriptive|3/5|3/5|
|triple descriptive|3/5|3/5|
|all_tasks descriptive|2/5|3/5|

Both arms pass all tasks at286001 and286004.
Both arms fail all tasks at286002 and286003.
At286005,constant_lr passes two/three but fails four;cosine_tail passes all three tasks.
There is one candidate-only quad pass and no control-only quad pass in this five-pair cohort.
This does not establish a population-level stability or superiority claim.

## Interpretation and non-claims

The late LR intervention rescued one final quad gate without losing a previously passing gate
in these five pairs. It did not remove the two broad failing states at either learning policy.
A whole seen-length task includes HOLDOUT values and mask criteria. Its failure is NOT sufficient
evidence of failure to fit the actual optimized normal TRAIN examples. Likewise,last minibatch
CE is not a final full-dataset evaluation,especially under alternating lengths/profiles.

Do not diagnose an optimizer root cause,underfit or overfit from gate counts alone. Do not tune
another LR endpoint,extend training or discard286002/286003 before locating the residual error.
C283/C284 conclusions about length coverage remain separate;C286 is not their direct replication.
All prior verdicts and Gate F remain unchanged.

## Accepted artifacts

|file|SHA256|bytes|
|---|---|---:|
|architecture-plan.json|3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e|3676|
|dataset.json|1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1|36024|
|triple-dataset.json|432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73|158236|
|quad-dataset.json|86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b|172066|
|trained-models.pt|f55a6fed1abb6a0c93053504a3f8a42c4110ded8328cde5e1a2c5d0e37b0d2ce|1238007|
|evaluations.pt|408551ec07aa4ac5d5bd6978cd042657b96634a33cb34e3f3239bdc53cff9279|159563727|
|measurements.json|40bfb616890304229ce1b581cc58d64d22b5bf8456a15d7d773db3672f5a1186|790540|
|validation-summary.json|9ac20a5fe67a69bf3e6ebcadd3b948561d00cc98857c5f0bfb2cb68003b7d803|38210|

## Next question;not activation

C287 should ask where the residual C286 error first appears across actually optimized normal
TRAIN renderings,held-out value assignments at trained lengths,and untrained length4,with the
saved length/profile-stratified training loss history as descriptive evidence.
Use all10 persisted states and unchanged criteria. Reconstruct final TRAIN/HOLDOUT accuracy,
query-pair,two-order,mask failures and row-weighted final NLL separately. Stratify the800 saved
pre-update minibatch losses by registered length/profile and fixed windows;never substitute
last-minibatch loss for final TRAIN performance or tune a checkpoint using the trace.
No training,model forward,state loading,new checkpoint or new data is needed.
C287 requires separate implementation/preregistration/review. C288 NOT REGISTERED.
