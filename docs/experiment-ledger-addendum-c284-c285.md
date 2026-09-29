# C284 acceptance and C285 saved length-transfer attribution

## Formal verdict

C284 ACCEPTED VALID NEGATIVE. The registered absolute four-character candidate gate requires
5/5 mixed_length states; observed3/5. The matched three_char_only control passed2/5.
Gate F NOT PASSED. C282/C283 verdicts remain unchanged. No C284 rerun or seed selection.

Scientific execution HEAD:3d34f6ba19017fd7d0422f070624ea7b1b494555.
Published log commit:4fe9b2f0d55b98c15855c2f9580572c8e9a9158e.
Publisher metadata log SHA256:d1399269d700cc2e3c7adfff1a2a3e006f4b45066fc08d4fea045adf555a955c.
Publisher metadata log bytes:899220.
Summary:runs/c284-v5b-max-length-450fab44535d4dd09c14931b8de1a283/summary.json.
Summary SHA256:83df761b835fa529d72ba1cee5fe618ddaff6936d9db56defc02957b90788c83.
Manifest SHA256:c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080.

## Execution validity

Published log reports authoring_runtime_preflight=PASS,own32/focused4013 PASS,source550/protected976,
run_execution_valid=True,scientific_status=FAIL,candidate_gate=False,persisted_max_length_scores=PASS,
tracked tree clean and execution HEAD preserved. The registered10-model workload completed:
8000 updates,384000 training rows,9620 forwards,539520 row presentations,38480 core calls;
one10-state bundle write/load and10 strict state loads. Parent reconstruction and saved scoring
completed through the source-pinned C284 path. Reviewer did not independently rerun local archives.

## Deciding metrics

|gate|three_char_only|mixed_length|
|---|---:|---:|
|four-character primary|2/5|3/5|
|two-character descriptive|3/5|4/5|
|three-character descriptive|4/5|4/5|
|all tasks descriptive|1/5|3/5|

Per-seed task flags (two/three/four):
-284001:control T/T/T;candidate T/T/F.
-284002:control F/F/F;candidate F/F/F.
-284003:control F/T/T;candidate T/T/T.
-284004:control T/T/F;candidate T/T/T.
-284005:control T/T/F;candidate T/T/T.

Paired four-character gates:2 candidate-only passes,1 control-only pass,1 both pass,1 both fail.
This is a net one-seed advantage,not uniformly better transfer and not5/5 reliability.

## Interpretation and non-claims

Matching maximum trained length3 removes the maximum-length confound of C283. The observed
five-seed comparison favors mixed_length by one complete quad gate,but the opposite direction
at284001 prevents a blanket claim that mixed training always improves transfer. Repetition per
length,curriculum timing and rendered diversity remain coupled. Five paired seeds do not establish
a robust population advantage,an arbitrary-length algorithm or a production-ready model.
C283's0/5 versus3/5 used a different control and seed group;do not compare those rates causally
with C284 as if only one factor changed between experiments.

C284 already separates two failure patterns:both arms at284002 miss even their three-character
training-length gate;candidate284001 passes two/three but misses four. Before another optimizer
or architecture change,inspect which specific fixed criteria are already failing at length3 and
which fail only at length4. Aggregate pass flags cannot identify those criteria or causes.

## Accepted artifacts (SHA256;bytes)

-architecture-plan.json:c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080;4082.
-dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024.
-triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236.
-quad-dataset.json:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b;172066.
-trained-models.pt:4f4e23be2c803b1b15a3d5ead607fa16de30650031c49bf96e15857b0610c117;1238007.
-evaluations.pt:d5469f156adbe1f03e5f255ce424062bbad3a021130f89b02abcd22c990a0e3f;159421903.
-measurements.json:c7cc3f82a98d352ecef22b788c928c19704d8ca47335b8e3e7ed18011679636d;788207.
-validation-summary.json:0e3e0914ba8bdd9d710a57fe7d99e7fdb2456df14e88d1752dd8fda5be220e28;38125.

## Next question, not activation

C285 should audit saved C284 outputs only:which four-character fixed-criterion failures are newly
introduced relative to the same model's matched three-character cells,and how does this attribution
differ between three_char_only and mixed_length? Preserve all10 states and all three tasks;
report arm-paired quad rescues/regressions and within-state triple-to-quad transitions. Do not
interpret matched-cell co-failure as proof that identical individual rows or causal mechanisms fail.
No training,neural forwards,model-state loads,checkpoint writes or new seeds are required.
Diagnostic PASS means integrity only;no favorable delta required. Gate F stays NOT PASSED.
C285 requires separate implementation,preregistration and committed-byte review. C286 NOT REGISTERED.
