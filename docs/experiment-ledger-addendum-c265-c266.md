# C265 acceptance and C266 saved-query diagnostic boundary

## Formal verdict

C265 ACCEPTED VALID NEGATIVE. All twenty states miss the joint three-profile gate.
The shared-suffix profile passes 0/20, while doubled passes16/20 and shared-prefix6/20.
C264/C263 bounded PASS and all earlier verdicts/recoveries remain. Gate E PASSED;
Gate F NOT PASSED. No default optimizer,architecture or production change.

Scientific execution HEAD:e0809d90c552471dee8723ce1b10528488f23be0.
Published log commit:4a51a286efcbe20336dba61699736e02ed51b5fa.
Publisher log SHA256:fb1c50a21c8829aef5a98dccbe189205006c127590fbe7eb9c418e59818fc025.
Log bytes:999513;lines4764.
Summary SHA256:f8c00bbcb311eeaf686ee43ef36d0597180e57c2bd70598d0fc23357c4da7998.
Summary:runs/c265-v5b-identifiers-755ab6d49ab84080ac18ff8f0699953f/summary.json.
The publication is one commit after execution and changes only c265/latest.json/latest.log.
Acceptance uses immutable published log ranges,metadata and recorded local postchecks.
The reviewer did not independently rerun learned states or rehash the complete console log.
Publisher-reported SHA256 is not an independent reviewer whole-log hash.

## Execution validity

Own24 PASS in10.021s;focused3525 PASS in323.929s.436 source pins/736 protected inputs verified.
Twenty frozen states completed600 wrapper forwards,86400 row presentations and2400 Full core calls.
One accepted weight-bundle load,twenty strict state loads;new training0,new learned checkpoints0.
Accepted two-fact anchor replay,renamed-input evaluation,restoration,unchanged weights and saved
metric reconstruction passed. Tracked tree clean;scientific HEAD preserved;run_execution_valid=True.
scientific_status=FAIL;joint_gate=False;all_replays=True;all_weights_preserved=True.

## Deciding profile gates

|Original training arm|Doubled uu/vv|Shared prefix uu/uv|Shared suffix uu/vu|All profiles|
|---|---:|---:|---:|---:|
|standard_forward|5/5|3/5|0/5|0/5|
|standard_reverse|5/5|2/5|0/5|0/5|
|lower_forward|3/5|0/5|0/5|0/5|
|lower_reverse|3/5|1/5|0/5|0/5|
|All states|16/20|6/20|0/20|0/20|

Counts are whole-profile gate passes,not per-answer accuracies. A failed profile can contain many
correct answers. The normal lengths are matched among profiles,and all characters were familiar.
Confirmed example:263001/standard_forward/doubled287/288 (PASS). Do not infer perfect totals from
other PASS flags or fabricate a grand accuracy total from the above counts.

## Interpretation and non-claims

Transfer from single-character names is not reliable for these compound names;common suffixes are
particularly limiting in the registered test. Prior success with two familiar names is preserved.
No new-byte embedding problem is introduced,but length,composition,positions and character
frequencies remain confounds. A last-character-only strategy is compatible with some aggregate
patterns,not established as the learned internal mechanism. Profile failure alone cannot distinguish
same-answer collapse from swapped values or other failures. No arbitrary-name capability claim.
The standard-rate states have more profile passes here;this does not establish a universal optimum
or authorize changing defaults after inspecting this same finite task family.

## Accepted artifacts

-eval-outputs.pt:546f5eb5dd62aa205c046fc5f2c7065837dc9ce578c79725c72ac451f87ae782;177035681 bytes.
-identifier-dataset.json:4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb;133970 bytes.
-identifier-plan.json:1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3;2439 bytes.
-measurements.json:208943819e92e4f5cdd4f299668c86b14cba338180e1686ddd40d776b8315656;200144 bytes.
-validation-summary.json:fd2e2028c442b651b740b7e0e82ea9e326750c0052b22a9d7b072486a2988bbd;3289 bytes.

## Next question, not activation

In the saved C265 answers,when only the queried identifier changes,do the two questions collapse
to the same predicted value,swap the two values,or fail in another way? Include every state,profile,
language,subset and fact order. Use a complete mutually exclusive partition and retain the equal-
length doubled condition as a matched descriptive reference. Distinguish same argmax from equal
logits. No new inference,weight loading,training or internal intervention is required.
C266 is one saved-output diagnostic,not capability promotion or causal parser identification.
A diagnostic PASS means exact attribution/reconstruction,even if the collapse hypothesis is unsupported.
Conclude this single decomposition rather than starting an open-ended chain of frozen-name probes.
Any subsequent training or architectural intervention needs its own scientific question and registration.
C266 needs separate implementation/preregistration/review before activation. C267 NOT REGISTERED.
