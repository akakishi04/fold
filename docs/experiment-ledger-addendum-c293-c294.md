# C293 acceptance and saved support/choice diagnostic boundary

## Formal verdict

C293 ACCEPTED VALID NEGATIVE. support_weighted passes2/5 quad gates,not the preregistered5/5.
ce_only also passes2/5;scaled_ce passes1/5. No reliable superiority or production adoption.
C292 remains ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED.
C294 NOT REGISTERED in this acceptance commit.

Scientific execution HEAD:318d9fd76f4253b30d68645ee34c124457be78a3.
Published log commit:3d35190c718b8b3c52e5c68120358ba96811466e.
Publication changes only docs/experiment-run-logs/c293/latest.json and latest.log.
Log SHA256:68336f6be02f5b1cbc1f8a2ebb3976519540d99621e262e3d328cf8dccc33315;820524 bytes.
Summary:runs/c293-v5b-fact-support-834c844c03c84023bc4ef1c6d32e3067/summary.json.
Summary SHA256:61a92e5d5775381cc1b7ef0fa19a9fa393197afd05a7642b74b0486ab6d338e6.
Manifest:0aadd3137b216f6e0fbc37feffe8b0ad947e48eeb22da881f38e58ee38a424f7.

## Execution validity

Own40/focused4357 PASS;4357 tests in448.396s. Runtime preflight and source604/protected1091 PASS.
15 fresh models completed800 updates each:12000updates,576000 training rows,14430 forwards,
809280 total row presentations,57720 core calls. Strict replay and persisted reconstruction PASS.
POSTCHECK:tracked tree clean,execution HEAD preserved,run_execution_valid=True.
scientific_status=FAIL;candidate_gate=False. No C293 rerun is needed.

## Deciding metrics

Counts in ce_only/scaled_ce/support_weighted order:
quad2/1/2;two_char4/4/4;triple4/4/4;all_tasks2/1/2;fitted TRAIN direct4/4/4;
seen-length HOLDOUT direct4/4/4. All three arms fail seen-length gates on293004.
Quad CE passes293002/293005;scaled CE passes293003;candidate passes293002/293003.
Relative to CE,candidate rescues293003 but loses293005. Equal totals do not imply equal outputs.

Seed293004 normal HOLDOUT (CE -> candidate):
-two_char correct226->259 of288;absent-known-value errors49->29;other-fact errors13->0.
-triple correct216->253 of288;absent-known-value errors59->33;other-fact errors13->2.
-quad correct200->239 of288;absent-known-value errors71->40;other-fact errors17->9.
Candidate helps that seed's counts but does not clear its fixed gate. Its two-character TRAIN
is575/576 and passes its direct subgate;triple TRAIN567/576 still fails. Do not call this a pure
unseen-length failure or assume the new weighting has no effect.

Seed293005 quad CE is864/864 correct;candidate857/864. Candidate TRAIN has4 other-fact errors;
HOLDOUT has3 absent-known-value errors. It is not a universal reduction in unsupported answers.
Do not tune coefficient,seeds,thresholds,training duration or the split after seeing the result.

## Interpretation and next question

The intended error counts can improve without improving the number of reliable models. Before
another loss sweep,measure the distinction the support/choice decomposition suggests:when the
full256-class winner is outside the two fact values,is the target nevertheless ranked above the
other fact value,or is the within-fact ranking also wrong?
C294 may audit saved C293 normal logits,all15 models and all2/3/4 tasks/value splits. Its additional
conditional ranking must use the unordered fact-value set from the verified input data,not the
answer key to choose the winner. Score correctness only after this ranking. Treat this as an
oracle-support diagnostic with privileged task structure,not an implemented decoder or a new
capability gate. Keep original predictions and all original masked/full gates unchanged.
Include exact ties and stable CE=support+choice loss decomposition;do not infer causal mechanisms
from descriptive categories. All results still derive from the same dependent evaluation cohort.
C294 requires separate implementation/preregistration/committed-byte review before activation.

## Accepted output receipt

The exact summary SHA commits all8 output names,hashes and sizes:
- architecture-plan.json:3112 bytes;0aadd3137b216f6e0fbc37feffe8b0ad947e48eeb22da881f38e58ee38a424f7.
- dataset.json:36024 bytes;1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
- triple-dataset.json:158236 bytes;432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
- quad-dataset.json:172066 bytes;86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
- trained-models.pt:1856766 bytes;7988e4f5b84f48058c4d7592e8a904e80cbfd75c0673dc4159ab171e95702073.
- evaluations.pt:239667179 bytes;1ecafb4ab7704dd206edf2cdb904b84b41c778d3dc1e5b717ed1e89bb794d860.
- measurements.json:1183339 bytes;958a0e276cf4238ea3b8a400785606d849f32b2369ad0a2a3cb8363da4963ed6.
- validation-summary.json:134735 bytes;ae3d24ff45c6ccffc3d74cba4a5a2457abf703cc8a9c3a0c1eaa70fdcc6a36b4.
