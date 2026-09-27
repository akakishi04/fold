# V5-B frozen compound identifiers v0.1 — C265

C264 passed the two-fact deletion gate for all20 states. This does not show that models can bind
unfamiliar identifiers rather than rely on the fixed a/b/c or 甲/乙/丙 labels. Test that restriction
without changing the model or teaching the new names.

For every accepted pair of original names u,v,replace them consistently in facts and query:
-uu/vv is the doubled-name reference;
-uu/uv shares the first character;
-uu/vu shares the last character.
For example aa=0;ab=1;ab= asks for1. Returning the value for aa because it also starts with a is
wrong. Conversely aa=0;ba=1;ba= must distinguish names that end in the same character.

These are not three new model variants. Each of the same20 frozen states receives all three naming
profiles. Values,answers,two-fact count,subsets,languages and fact orders stay matched. All normal
input bytes were already present in the familiar symbolic task;only their composition into longer
identifiers is new. All profiles have the same paired input length,13 ASCII or25 Japanese bytes,
within the original48-slot interface. No automatic translation back to old names is allowed.

There are288 questions per profile,864 new questions per model. The actual C264 scoring function
uses unchanged original target/group metadata only OFFLINE. It never supplies original names to
the model. Require each profile's per-cell answer,paired-query,mask-drop and two-order criteria;
all20 states must pass all three profiles. Report each profile/arm separately. The doubled profile
cannot hide collision failures,and a bad profile cannot be dropped after evaluation.

First-character-only and last-character-only synthetic parsers provide negative authoring controls.
They are deliberately NOT learned-model evidence. A real failure can reflect unfamiliar name
composition,length/position effects or other mechanisms;the test does not prove an internal parser.
Even a full pass establishes only this finite set of compound naming transformations.

The actual weights remain in C263's accepted checkpoint bundle. C264 supplies the accepted two-fact
output references. Use the correct three-argument C264 verifier with its C263 source summary;do not
mistake C264's evaluation archive for learned weights or its three-fact anchor for reduced outputs.
Per state,check old two-fact outputs,run all naming profiles,then check old outputs and weights again.

Formal cost:600 model forwards,86400 input rows,2400 Full core calls,zero learning updates. One
accepted weight-bundle load and20 strict state loads. Raw saved logits about177 MB plus metadata;
this is not a peak-memory measurement. The postcheck reconstructs all metrics without model calls.
Own24 and full3525 regression plus the Windows parser chain precede the real evaluation.

C264's PASS and all earlier results remain unchanged. No optimizer/architecture adoption,arbitrary
name handling,general-language capability,independent benchmark or Gate F passage is implied.
No additional training is authorized by a valid failure. Judge C265 before registering C266.
