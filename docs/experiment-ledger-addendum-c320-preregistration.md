# C320 preregistration — frozen unequal-name-length transfer

Experiment:C320-v5b-frozen-unequal-name-lengths. Stage:V5-B-FROZEN-UNEQUAL-NAME-LENGTHS.
Acceptance base:1c60afa5997ca9f61a6f5b44e73a31e2b15cd609. C319 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED;C321 NOT REGISTERED. No new-layout predictions observed before registration.

## One question and prospective primary

Can models trained with equally long names in each question handle a two-character name and a
four-character name together? Test lengths(2,4) and(4,2),assigned to the canonical two entity IDs,
not to fact presentation order. Both fact orders and both queried entities remain represented.
Every name length is individually within the TRAIN range2..4. The new variable is their unequal
combination within a question,not a longer input frame,novel byte vocabulary or new readout.

Use ALL10 C319 saved models/seeds319001..319005,mean_last and last_only. Retain each model's own
trained readout policy for every old and new input. No learning,new parameters,checkpoint selection
or changed inference policy. Prospective primary:all5 retained mean_last baseline models pass BOTH
new layouts under all original local/masked criteria. Last_only remains fully reported but cannot
rescue baseline failure. This is a new task probe,not a way to relabel C319's candidate4/5 as PASS.
Baseline selection occurs after old results but before new results;not independent model selection.

## Rendering and unchanged inputs

For entities i,j and lengths n,m:repeat uses u*n,v*m;shared_prefix uses u*n,u*(m-1)+v;
shared_suffix uses u*n,v+u*(m-1). u/v are the same English or Japanese entity symbols as before.
Names remain distinct. Same logical facts,values,query,fact order,original TRAIN/HOLDOUT values,
normal/evidence-blind/query-blind views. Querying short and long names is balanced by intact
original question pairs. No hidden target controls rendering or model inputs. Never restrict
the256 output classes to digits or the two values in a question.

The new renderer must reproduce every archived equal-length1..6 input byte-for-byte when given
(n,n). Length1 uses one canonical profile;new layouts use all three profiles. Canonical DATA and
original PROMPTS hashes unchanged. New normal prompts1728 distinct and disjoint from old normal
prompts. New bytes are a subset of the old vocabulary. Every actual prefix token,BOS/EOS/padding
and actual C304 query-span mask is verified. Maximum new Japanese body37UTF8bytes+2markers=39
encoded tokens,within64slots and shorter than some training inputs. No truncation or language
exclusion. Unequal positions/separations and name-template geometry change together;this cannot
separate those mechanisms or establish arbitrary-name reasoning.

## Frozen lifecycle and counters

Actual C319.make_models and C319.load_bundle;strict-load every final state once and freeze it.
All14256parameters,64slots and original core/readout calculations remain. C319.trained_readout
wraps each pass with that record's own mean_last/last_only policy. Do not use the native mixed
forward for a model trained last_only. Policy provenance remains validated by accepted hooks.

Per checkpoint:original1..6 BEFORE -> two unequal layouts -> original1..6 AFTER. All views and
profiles evaluated. Both old passes match their own C319 final archive<=1e-9 absolute logit drift
and exact argmax;original per-state2..6 full-gate flags unchanged. Full weight fingerprint and all
hook registries preserved after every pass. Same records reused only as controls,not new models.

Per checkpoint144+54+144=342forwards,32832rows,1368core calls. Full10:3420forwards,328320rows,
13680core calls.10strict state loads,one existing C319 model-bundle read,training0,new model
checkpoints0,network0. Each forward has2query projections,zero grad-enabled calls. Six discarded
operational forwards(two arms*old/new/old) and recursive ancestor checks/regression are separate.
Raw float64 logit payload672399360bytes before serialization overhead;not a peak-RAM estimate.

## Parent writer and dependency contract

C319 execution:529c54ef63b1015b25632b8123a9a552eebcd263.
Publication:3abe218dc9191d26963e5b5022d4d1983300084d.
Summary:runs/c319-v5b-trained-last-0f94e96bbbba43b395fcf8eab1e38246/summary.json.
Summary SHA256:48815ca382d0da078da12ec2d54f2c42261e94498b682f679d8f46d746ec0580.
C319 blob:8222ddc165464b8acb84380f47d397504308a9df.
C304 blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify46 ordered hashes BEFORE exact C319.verify_artifacts(parentdir,45ancestors,acceptedHEAD).
Require acceptedFAIL,seven artifact descriptors,exact original10 seed flags,all_pairs_matched and
all_replays. C319 writes final same-policy outputs after training and strict replay;these are not
outputs of a frozen policy switch. Read its own dataset.json,length-datasets.json and
fold-c319-trained-readout-eval-v1 records. Model schemafold-c319-trained-readout-models-v1 is
handled by actual C319.load_bundle. Use matching ordered identities,policy tags and full hashes.

Sole direct repository import C319. Its context supplies protected C318/C317/C316/C315 helpers,
C304 model/span/scorer,C287 normalizer,C310 no-neural,backend. All760source pins/1429inputs remain
checked including actual repository-local lazy/context/factory-language modules. Add OWN6 plus
8C319parent files:766sources/1443inputs. No accepted source/test/log/dispatcher/preregistration
edits or new regression exclusions. Missing dependency coverage invalidates rather than waives.

## Scoring,persistence and interpretation

Reuse actual C304.score_length:it adapts profile names into the inherited C270 logical scorer,
which does not receive a name-length argument. Score each unequal layout separately. Unchanged
accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/two_order.80. Do not average a failed layout
with the other to pass. Report20model/layout scores,40split partitions,10old-output reproductions,
per-layout counts and both-layout counts for both arms. A valid primary failure is ACCEPTED VALID
NEGATIVE. PASS is bounded unequal-length task capability,not superiority,arbitrary composition
or Gate F. C319 and every earlier verdict remain unchanged.

Five artifacts plus summary:evaluation-plan.json,unequal-prompts.json,evaluations.pt,
measurements.json,validation-summary.json. Schemafold-c320-unequal-eval-v1 retains oldbefore/new/
oldafter logits,policy receipts,full hashes,replay errors. No checkpoint write. Arrays stay local.
No-neural reconstruction verifies parent evidence,all scores/controls,generated prompts and JSON;
hash/size checks cover all arrays. Existing run directories are never overwritten.

Own24/modules205/loaded5222/focused5221;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:34ac7cbac03191c2e64ae05887f7d04cbc90c3cf0a73e18427708c1bbeed307d.
Commit/refetch/review all6 OWN before activation. Test actual accepted C304 forward/span/scorer
adapter,C315 evaluator/replayer and C319 trained policy on controlled components. Independent
prompt parsing verifies names,values,query and fact order. Require both policies,exact call
counts,46hash guards,766/1443protection,correct C319 loader path,persistence/tamper and UTF8/CP932.
These software controls are not real checkpoint capability or complete inherited regression.

User Windows Validate still requires46actual parents/pins,real two-arm bilingual old/new probes,
own24/full5221regression and dispatcher/launcher/runner ParseFile. No scientific output is used
to retune the layouts or select a cohort. Validate failures skip science/publication. Integrity
failures repair SAME C320 with fixed conditions. C321 waits for formal C320 judgment.
