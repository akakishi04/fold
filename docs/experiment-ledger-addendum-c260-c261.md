# C260 acceptance and C261 repeated-value transfer boundary

## Formal verdict

C260 ACCEPTED VALID NEGATIVE. The preregistered without_core primary arm passed3/5,not5/5.
The with_core reference passed4/5. Neither pooled accuracy nor the other arm rescues the primary gate.
C259/C257 remain accepted valid negatives;C258 remains diagnostic PASS;C256 bounded PASS remains.
Gate E PASSED;Gate F NOT PASSED. No production architecture change or core-superiority claim.

Scientific execution HEAD:5788a63a692983094a9c6311c58d1440005b7fca.
Published log commit:e841aa5c312d46bfe11172af45262433cf5ec33d.
Publisher log SHA256:604163ff5f8ad3628e8b3facd49f7e97cafde04822123838b344efc893d2fd15.
Log bytes:749925.
Summary SHA256:df6780749afa707fa0c6809e76710f39cdbeac6c1b69665a064248808b1f9ab6.
Summary:runs/c260-v5b-core-free-697d8bdc3ca3411ba81f703b2f16fb96/summary.json.
The publication commit changes only c260/latest.log and latest.json. The registered HEAD,metadata
and printed summary execution identity agree. Acceptance uses immutable published log ranges and
recorded local postchecks,not independent learned-model reruns or a complete-log byte rehash.

## Execution validity

Own24 PASS in14.466s;focused3405 PASS in147.380s.
406 source pins/672 protected inputs passed. Ten models completed800 updates each:
8000 updates,384000 training presentations,8240 wrapper forwards,435840 row presentations.
Full core calls16480;core-free core calls0. One10-state bundle write/load;ten strict state loads.
All common-parameter/batch matching,weight-change,checkpoint-logit/argmax replay,persisted metric
recomputation,protected-input,clean tracked-tree and scientific-HEAD checks passed.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.

## Deciding evidence

HOLDOUT all6 orders,216 answers and36 all-six-correct groups per language:

|Seed|Full EN /216|Full JA /216|Free EN /216|Free JA /216|Full six EN,JA /36|Free six EN,JA /36|Full gate|Free gate|
|---:|---:|---:|---:|---:|---|---|---|---|
|260001|216|216|216|216|36,36|36,36|PASS|PASS|
|260002|216|216|115|120|36,36|13,13|PASS|ORIGINAL_CRITERIA_MISS|
|260003|216|216|216|216|36,36|36,36|PASS|PASS|
|260004|216|216|134|139|36,36|19,20|PASS|ORIGINAL_CRITERIA_MISS|
|260005|108|116|216|216|18,19|36,36|ORIGINAL_CRITERIA_MISS|PASS|

Pooled Full1952/2160(90.3704%);core-free1804/2160(83.5185%). This pooling is descriptive only.
Without_core minus with_core:four seed/language accuracy comparisons lower,four tied,two higher.
The direction reverses for seed260005;do not claim that one pathway dominates every initialization.
Full14256 parameters versus core-free10928;the pair was not parameter-,FLOP-,or wall-clock-matched.
Removing the core also changes residual base,optimizer state and the globally clipped gradient.

## Interpretation and non-claims

Removing the core did not make this bounded task reliable across all five states. Some states solve
the task without it;other paired states improve with it. This does not prove general necessity,
sufficiency,architectural superiority,or the cause of C259's miss. Retain both experimental paths;
no removal from the FOLD design and no automatic adoption of either arm.

All training/evaluation assignments used three DISTINCT values chosen from0..3. Success within
that restriction does not establish correct behavior when two entities share a value. Do not keep
adding seeds until an all-seed gate passes;test this unexamined task assumption next.

## Accepted artifacts

-core-plan.json:ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae;2746 bytes.
-dataset.json:3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56;126501 bytes.
-evaluations.pt:b109243f5b5d24ffe343586a50b97990524c7b572ec238b5e267863dbd542276;53123591 bytes.
-measurements.json:5839838218761bd608b5b79137a300649b3a5df11eb909474520a45608f3a8fa;62614 bytes.
-trained-models.pt:727ffd1320266a239d21ce172279dc2cec3be6383db74cd4a1b09addbe36976c;1075036 bytes.
-validation-summary.json:250d099db6ec58b21db06d858e9c0e0ddf8349f66b0d1936001e3874875e26a2;3298 bytes.

## Next question, not activation

With all ten C260 final states frozen,do the models answer correctly when values repeat across
entities,without further training? Keep names,queries,all6 orders,byte encoding and weights. Include
both architectures and every seed,not only successful states. Replay all accepted distinct-value
outputs before and after new inputs. New data comprises the40 nondistinct assignments from0..3:
36 with exactly one equal pair,and4 with all values equal. Score those strata separately.
The all-equal stratum cannot demonstrate query sensitivity. For pair-equal rows,the singleton-value
queries must be reported separately so always answering the repeated value cannot look successful.
C261 registration must address these changed metric semantics explicitly;do not blindly reuse
C260's distinct-target triplet assumption or query-mask-drop gate. No C260 score is revised.
Separate preregistration and committed-byte review control activation. C262 NOT REGISTERED.
