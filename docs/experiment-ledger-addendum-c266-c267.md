# C266 acceptance and C267 name-coverage training boundary

## Formal verdict

C266 ACCEPTED PASS (saved-output diagnostic integrity only).
C265 remains ACCEPTED VALID NEGATIVE; C264/C263 retain their bounded PASS scopes.
Gate E PASSED; Gate F NOT PASSED. No model, optimizer default, architecture or production change.
The diagnostic concludes the single saved-name decomposition promised in C266.

Scientific execution HEAD: b377042dcdb903a308da131feb135b0f5362d9de.
Published log commit: a18f2e82e9edb9e96d5b25937041be089288e6ec.
Publisher log SHA256: a50a971d382a66e0f4af10f7376bc48027c91f99620cd53280c44d5df3ae20e2.
Log bytes: 787239; lines: 3828.
Summary SHA256: 5d9c79306aae5fb2fd39a82fae645a1447029cae3aedfb2bf92e953bb2435247.
Summary: runs/c266-v5b-query-pairs-b652a5a2d2ea4dac9b913b64df6d78e0/summary.json.
The publication immediately follows the registered execution and adds only C266 latest.log/latest.json.
Acceptance uses immutable published log ranges, metadata and recorded user-local postchecks.
The reviewer did not independently rerun user-local artifacts or hash the entire log. The log hash
above is publisher-reported, not a new independent complete-byte reviewer measurement.

## Execution validity

Own24 PASS in7.338s; focused3549 PASS in379.386s.442 source pins/748 protected inputs verified.
17280 normal answers attributed into8640 query pairs,720 detailed cells,120 profile summaries and80
matched contrasts. All integer partitions and parent correct/query-pair scores reconciled.
Model forwards0; state loads0; learned-bundle loads0; training0; new learned checkpoints0.
Six saved-evaluation archive reads per analysis pass; analysis and persisted postcheck are two passes.
Source/protected-input checks and persisted reattribution passed; tracked tree clean;
scientific execution HEAD preserved; run_execution_valid=True; scientific_status=PASS.
capability_pass_claim=False; causal_parser_claim=False.

## Deciding descriptive results

Each profile contains2880 query pairs, aggregated over all20 states and both languages.

|Profile|Both correct|Same displayed value|Same outside value|Swapped values|Other unequal answers|
|---|---:|---:|---:|---:|---:|
|doubled|2835|19|0|0|26|
|shared_prefix|2509|298|5|0|68|
|shared_suffix|664|2142|7|39|28|

Same-answer collapse includes both displayed-value and outside-value collapse. It occurs in19/2880
pairs for doubled,303/2880 for shared_prefix,and2149/2880(74.6181%) for shared_suffix.
Among the2216 shared_suffix pairs that are not both correct,2149(96.9765%) collapse to one answer.
These are PAIR counts,not individual-error percentages or independent model-training replications.
Suffix collapse selects logical entity0 in1595 pairs and entity1 in547;7 select an outside value.
Logical entity0 is the first entity within the source subset,not always the first displayed fact.
The complete output retains per-state/language and first/last displayed-position counts.

The main observed failure is therefore same-answer collapse,not an exchange of the two values.
This describes outputs; it does not prove absent query representation or a last-character-only
internal parser. Equal argmax need not imply equal logits. For example,printed263001 lower_forward
shared_suffix EN has44 collapsed pairs and zero exactly-equal-logit pairs among72 queries.
Do not infer a population-wide mechanistic conclusion from this one diagnostic or aggregate table.
No scores or verdicts from C265 are revised.

## Accepted artifacts

-audit-plan.json:85be4d973b9f8ce8a59e1ffa9028faceb1de3fcc8d8b3035264c2af72ed88b3e;2269 bytes.
-pair-attribution.json:038dd3a9aecc86aadcd2f99a8269103a579a3aa7787ac0bc8983e37dba082e90;3463178 bytes.
-cells.json:2c593908456838ff582c51632106f1a21af5082d081b1647fa6a6d6efbf85357;365733 bytes.
-profile-summary.json:6a33a496099a60aeb2d7715338d7c2f5caecb9cec51c0f3cff92f696f3d581d4;58160 bytes.
-matched-contrasts.json:a685b34f814b16295dae958d87dd0b23b405b8d4065e512af8262dc66d7d7bf2;18024 bytes.
-validation-summary.json:17f9a7895fc2d208d1bdb2a463c3455a78aa7aeb53698ab91952c4d7d963f12f;788 bytes.

## Next question, not activation

Does explicitly covering compound-name collisions during training reduce collapse on held-out value
pairs,relative to equal-length doubled-name-only training at the same model and update budget?
Use fresh paired Full models,not continued C263 states. Keep model,initial state,base questions,
values,targets,optimizer and800 updates matched within each pair; change naming coverage only.
Do not add another frozen-name diagnostic chain or treat the remaining cause as already established.
C267 must define its new two-fact TRAIN/HOLDOUT split explicitly:it cannot reuse C264's projected
rows as though the original three-fact split remained disjoint. Its capability gate must be fixed
before training. Treatment names will be training-seen,so success will not be unseen-name transfer.
C267 implementation,preregistration and committed-byte review precede activation. C268 NOT REGISTERED.
