# C291 formal acceptance and next diagnostic boundary

## Verdict and evidence identity

C291 ACCEPTED VALID NEGATIVE. Candidate answer_margin passes4/5 quad gates,not the registered5/5.
CE also passes4/5 and pair_sum2/5. No superiority over CE is established. Gate F NOT PASSED.
Scientific execution HEAD:8d33edabbc7a91654a3da6056091cec2d84d9a24.
Published log commit:49f30351a7687884bf0b9a6f2ddd304de8c26d1e.
Log SHA256:ee7e6ea370ccdd6e07223f652458c6137753f835237f5c64ac286bdfccc5309e;801296 bytes.
Summary:runs/c291-v5b-answer-margin-7f15f2dbf9ca4a16a2ba0ce2271a3421/summary.json.
Summary SHA256:271cc816f49fd7d53714508fee284bbf9f93783b3e74ac2728fc2a5286d740fa.
Manifest SHA256:99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.
The previous CP932 failure was operational;judge only this completed recovered invocation.

## Execution validity

Own40 and focused4285 PASS. The log reports4285 tests in327.693s and preflight PASS.
Source592/protected1066. All15 models finished800 updates:12000 updates,576000 training rows,
14430 model forwards,809280 total row presentations,57720 core calls. Final strict replay and
persisted reconstruction PASS;all_groups_matched=True;tracked tree clean;execution HEAD preserved;
run_execution_valid=True. scientific_status=FAIL;candidate_gate=False. No rerun is required.
The completed run preserves the accepted parent source map and exact parent reconstruction.

## Deciding metrics

Counts in CE/pair_sum/answer_margin order:
- quad primary4/2/4;
- two-character4/5/4;
- three-character4/5/4;
- all-task4/2/4;
- trained-length TRAIN direct5/5/5;
- seen-length HOLDOUT direct4/5/4.
CE and answer_margin pass every task for291001,291002,291004,291005;both fail all-task on291003.
Pair_sum passes seen-length tasks for all5,but quad only for291002/291005.
Do not equate identical seed gates with identical answers or logits.

Seed291003 normal answers:
- CE TRAIN two576/576,triple576/576;HOLDOUT two165/288,triple165/288,quad157/288.
- answer_margin TRAIN two576/576,triple576/576;HOLDOUT two225/288,triple216/288,quad211/288.
- pair_sum TRAIN two576/576,triple576/576;HOLDOUT two288/288,triple288/288,quad280/288.
Answer_margin improves this seed's answer counts relative to CE but does not clear its fixed gates.
The residual is not only a new-length problem:seen-length HOLDOUT fails despite fitting TRAIN.

## Interpretation and non-claims

The answer-wise objective recovers two quad passes relative to pair_sum in this sample but does
not improve the number of reliable seeds relative to ordinary CE. It is not adopted or called a
solution. Equal coefficients did not match gradient scale;negative set and aggregation changed
jointly. No causal explanation,arbitrary-length claim,or Gate F promotion follows.
Before another loss/schedule change,distinguish observable error roles:the other fact's value,
an absent value from the trained0..3 vocabulary,or a non-value byte. These are output descriptions,
not proof of wrong attention,memorization,or a particular hidden computational mechanism.

## Output receipt

All8 descriptors are sealed by the exact summary hash:
- architecture-plan.json:3348 bytes;99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.
- dataset.json:36024 bytes;1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
- triple-dataset.json:158236 bytes;432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
- quad-dataset.json:172066 bytes;86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
- trained-models.pt:1856766 bytes;972fe531333b4f0f8129cc91b2f6180189cda62f97794585976e5dc30f366cd7.
- evaluations.pt:239775339 bytes;d3bf127d7282a90021a9c39d740cf14f533e9587725ad0a5fb2f0480b000b9db.
- measurements.json:1183175 bytes;ee1b741478a6701b2f878e24039d6b5f9098e38e883a63f60ee834846d277774.
- validation-summary.json:124909 bytes;002f6ce4de8228275d75b08b6af3ee32041c98eb1c74f27257d9aea4ecb26376.

## Next question,not activation

C292 should audit all C291 final normal predictions by target/other-fact/absent-known-value/non-value
roles across every seed,arm,length,profile,language and original value split. Preserve exact row
identities and compare answer_margin to both controls. Use saved logits only,no model execution.
Reconstruct the original masked/full gates through the exact C291 verifier before classification.
C292 requires separate source/test/runner/launcher/preregistration/design and committed-byte review.
C292 NOT REGISTERED in this acceptance commit. C293 NOT REGISTERED.
