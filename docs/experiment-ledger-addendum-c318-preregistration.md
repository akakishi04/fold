# C318 preregistration — frozen native readout branch isolation

Experiment:C318-v5b-frozen-readout-branches. Stage:V5-B-FROZEN-READOUT-BRANCHES.
Acceptance base:300dcb6ed45411cec6e646f732cb95ed664cf683. C317 diagnostic PASS only.
C319 NOT REGISTERED. C316/C315 negatives and Gate F NOT PASSED unchanged.

## One question

At the same frozen C316 weights,what behavior is retained by the native mean-query attention
alone versus the native last-query-byte attention alone? C317 first-byte replacement damaged
all scored gates;that does not separate damage from the novel query input and the importance
of the existing two jointly trained branches. No first-byte candidate or new training here.
Keep all10 C316 states,all5 original seeds and both training mixtures;no checkpoint filtering.

## Exact intervention and scale

Native C304 forward projects the span-mean query first and the last-byte local state second,
then averages their two attention-weighted memory vectors with coefficient .5. In mean_only,
replace only the second projection input by the same native span mean. In last_only,replace
only the first projection input by the same native last-byte local state. Same learned shared
query projection,keys,softmax,value states,core/residual,normalizer and classifier. Both calls
still execute;there is no new learned weight,method replacement or accepted source mutation.

Duplicating one native branch gives .5*(memory+memory):the total coefficient remains1,not.5.
This prevents confounding branch removal with simply halving the whole memory contribution.
It does NOT match the actual vector norm/covariance to the original mixed output. Any effect
is an inference-time intervention on a jointly trained function,not independent causal shares,
a proof of universal branch necessity,or a comparison of separately trained architectures.
Last BYTE is literal;no substitution of a whole Unicode character or target-aware location.

Temporary hooks validate every native query input BEFORE replacement:call1 equals the true
query-span mean and call2 equals the true last-query-byte local state. One encoder capture,
exactly2 projections/forward,CPUfloat64 finite batch-by64-by16 local states. The model's actual
accepted C304 forward executes. No target label,expected answer or per-row endpoint choice.
No optimizer/backward,frame extension,coefficient search or adaptation of frozen parameters.

Order per state:original_before -> mean_only -> last_only -> original_after. Both originals
use the same observer hooks but do not change inputs. Strict-load each C316 state once;no
parameter reloads between modes. Every pass preserves the full weight fingerprint and all
forward/pre-hook registries,including kwargs/always-call metadata. Cleanup on exceptions too.
Original before/after reproduce every C3161..6/profile/split/view logit<=1e-9 and exact argmax;
original2..6 gates unchanged. All query-blind and all English length1 outputs must be identical
in both interventions (single-byte span). Japanese length1 is not a single-byte control.

## Inputs,scoring and reporting

Same14256parameters,64slots,canonical C316 input1..6,all original TRAIN/HOLDOUT values and English/
Japanese. Length1 one canonical profile;2..6 three. All normal/evidence-blind/query-blind views.
Same full256-class argmax and C304/C270 gates:accuracy.90,query_pair.80,evidence_drop.35,
query_drop.35,two_order.80. No new capability gate. Score original-before and the two isolated
branches;the final original is restoration,not a fourth independently scored model.
Report30state/mode results,300length/split partitions,60single diagnostics,10reproductions,
1280paired local groups/92160paired normal rows. Both rescues and regressions retained;wrong-to-
wrong changes not called rescues. The same baseline appears in both comparisons,not independent
trials. PASS means diagnostic fidelity/restoration/persistence ONLY even if all changed gates fail.

## Parent writer and protection

C317 execution:3ecd3a638726f86b294f0fe94d53a2fc5d082e01.
Publication:a948757c3f2a0e524bdef50521cf4034b900fc2a.
Summary:runs/c317-v5b-query-endpoint-88ae97edc7d44cd3bcd9732e66c8b14e/summary.json.
SHA256:09632cda7689c9b23229ec993d19c108ac23a7bb142285cd58b11bcc713d8cb5.
C317 blob:7ef1736df78b5dd883a331c434f5f82f1eb8ab92.
C304 blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify44 ordered summary hashes BEFORE actual C317.verify_artifacts with43 ancestors and its
accepted execution HEAD. Its four artifacts are diagnostics,NOT a model/data bundle. Require
PASS(diagnostic),original botharms5/5 at2..5,4/5 at6;first-byte0/5 at2..6. Use actual C317.load_parent
on paths[1:] to validate/load C316 data/prompts/final prediction anchors. Actual C316.load_bundle
reads trained-models.pt at paths[1].parent,NOT the C317 directory at paths[0]. C316.make_models
uses its original seeds/context;strict checkpoint fingerprints match the original final records.
No C317 changed predictions supply a model checkpoint or new training signal.

Sole direct repository import C317. Reuse its context/guard/parent-hash/paired-count/one-byte helpers,
C316 factory/loader,C315 evaluator/replayer,C304 span/scorer,C287 normalizer,C310 no-neural/backend.
All748 inherited sources and1407 inputs checked;actual local helper/factory-module coverage
mandatory. Add OWN6 and5 C317 parent files:source754/protected1418. No accepted source/test/log/
preregistration/dispatcher edits or new regression exclusions. Source coverage failures stop.

## Work,artifacts and execution

10states*4modes*144=5760forwards;552960row presentations;23040core calls. One mode:13824rows,
288query calls,4896rows with a one-byte span.10strict state loads,one C316 bundle read,training0,
new checkpoints0,network0. Both query calls are retained;no compute saving claim. Ten discarded
operational forwards(two arms*native+fourmodes) and recursive checks/tests are separate work.
Raw logit payload1132462080bytes before overhead;not a peak-RAM estimate.

Four artifacts:audit-plan.json,evaluations.pt,measurements.json,validation-summary.json plus
summary.json. Schemafold-c318-branches-eval-v1 stores all4raw passes,original fingerprints,
per-mode hook receipts and replay errors. No trained-model archive. All tensors local/ignored.
No-neural postcheck reconstructs every score,control,paired count and JSON;hash/size verification
and no-overwrite enforced. Integrity failure repairs SAME C318;no science retuning after results.

Own24/modules203/loaded5174/focused5173;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:757879ae36418ab5b3973a18ea80902aef081c3e41b4a463f03cc841c2c3e4ad.
Commit/refetch/review all6 OWN before activation. Tests must execute actual accepted C304 forward
and C315 evaluator on controlled models,independent single-branch numerical oracles,provenance/
cleanup/strict-state checks,44hash guards,correct C316 loader path,paired statistics,persistence,
UTF8/CP932,semantic suite IDs and CLI index contracts. Local synthetic controls are not actual
FOLD scientific evidence. User Windows Validate still requires44real parents/pins,real bilingual
frozen probes,own24/full5173 regression and dispatcher/launcher/runner ParseFile.
Validate failure skips science/publication. C319 waits for formal judgment. Gate F stays unmet.
