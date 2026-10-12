# C321 preregistration — frozen interior name-order binding

Experiment:C321-v5b-frozen-interior-name-order. Stage:V5-B-FROZEN-INTERIOR-NAME-ORDER.
Acceptance base:8785a88b70a14a4b8d632ff520a03977eb73f129. C320 bounded capability PASS.
C322 NOT REGISTERED. C319 valid negative and all earlier verdicts/Gate F NOT PASSED unchanged.

## One prospective question

Can the existing frozen models bind names when both names have the same four-character length,
first/last character and character multiset,while internal order differs? This removes the
simple cues that could distinguish C320's unequal-length names,without adding vocabulary or
using longer identifiers. Three fixed families,using canonical entity characters u and v:

| New family | First entity | Second entity | Legacy scorer slot only |
| --- | --- | --- | --- |
| u_dominant | uuvu | uvuu | repeat |
| balanced | uuvv | uvuv | shared_prefix |
| v_dominant | vuvv | vvuv | shared_suffix |

Example:aaba=0;abaa=1;aaba= answers0;query abaa instead answers1. The pairs have equal character
counts and equal endpoints,not identical strings. The scorer-slot names are opaque adapter
labels,NOT descriptions of these new names. The adapter preserves all rows/tensors/values and
uses actual C304.score_length -> C270.score without changing logical local/masked gates.
The model never sees profile labels,correct-answer-derived choices or an adapted output mask.

## Fixed models,inputs and gates

Use all ten C319 states,seeds319001..319005,both mean_last/last_only. Retain failed last_only319005
and C320's failed last_only319002. No cherry-picking,retraining,seed search or ensemble.
Actual C319.make_models/load_bundle/trained_readout;strict state fingerprint/readout-policy match.
Preserve each state's OWN trained policy throughout all passes;never replay last_only as mean_last.
All14256parameters/64slots/full256-class argmax unchanged. No optimizer/backward/new model weights.

Names are length4 in both entities,a length already used in training. New order patterns only.
Keep original two facts,values,questions,both fact permutations,canonical entity pairs,English/
Japanese,TRAIN/HOLDOUT value split and normal/evidence-blind/query-blind views. No changes to
source logical row IDs or targets.864 distinct new normal prompts,disjoint from all old1..6
normal inputs,new byte vocabulary subset. Japanese body43bytes+2markers=45 of64slots. Verify
all exact UTF8 bytes,BOS/EOS,padding and actual accepted query span;no truncation or omissions.
Validate original canonical dataset/prompt hashes before constructing new inputs.

Primary:ALL5 mean_last states pass ALL THREE new profiles with all existing local/masked gates:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Last_only is retained as a
separate comparison and cannot rescue primary failure. PASS is bounded new name-order capability;
valid primary failure is ACCEPTED VALID NEGATIVE. No aggregate accuracy replaces a failed local
gate. Primary fixed before the new outputs are observed;same previously used checkpoint cohort
means no independent fresh-seed confirmation. No outcome rewrites C319/C320 or promotes Gate F.

## Parent writer and complete protection

C320 scientific execution:0e4687acfa72355cbddc47c3ceb98700354fe34d.
Publication:7a693b5d7747ab67146a8c2fa2f996cb10b5054d.
Summary:runs/c320-v5b-unequal-names-d1599525908a404998a52011a5567b81/summary.json.
SHA256:9e41e82228f26cf525ee54e4097abd493a339641d6b3d3f5b2a6d10ba8868431.
C320 source5e183c330c883d8c44d9cd66ac2b89365517f9cc.
C319 model/policy source8222ddc165464b8acb84380f47d397504308a9df.

Verify47 ordered summary hashes BEFORE actual C320.verify_artifacts(C320dir,46ancestors,
C320executionHEAD). Require parentPASS and exact ten layout flags:mean_last5/5 both;
last_only only319002 short_long fails. C320's five artifacts are new prompts/evaluation outputs,
NOT a trained-model/data bundle. After verification,call actual C320.load_parent on paths[1:]
to obtain verified C319 dataset,original1..6 prompts and final same-policy prediction anchors.
C319 model bundle is at paths[1].parent,not C320 paths[0].parent. Use actual C319.load_bundle
and strict-load each correct ordered state exactly once. No reusing generated answers as weights.

Sole direct science import C320;its C319 owner and existing context provide original C315 eval/
replay,C304 span/scorer,C287 normalizer,C310 no-neural/backend and other inherited helpers.
Retain and verify all766 source pins/1443 protected inputs,including actual local lazy/context/
factory-language module coverage. Add OWN6 and6C320parentfiles ->772sources/1455inputs.
No accepted sources/tests/logs/preregistrations/dispatchers changed. No new exclusion or pin waiver.

## Order,reproduction,accounting and persistence

For each state:original1..6 before -> new interior names -> original1..6 after. All original
views/profile/split logits reproduce C319 within1e-9 and exact argmax. Preserve original per-state
2..6 full gate flags. The C320 unequal archive is recursively verified,not freshly inferred here.
Full state/hook registries unchanged after each pass. Both old and new evaluations stay inside
actual owner.trained_readout;verify per-mode calls/query-calls/rows/grad_calls=0.

Per state144+27+144=315forwards,30240rows,1260core calls. Tenstates:3150forwards,302400rows,
12600core calls,10strict state loads,one C319 bundle read,training0,new checkpoint0,network0.
Six discarded operational smoke forwards(two arms*old/new/old),recursive artifact checks and
software tests are separate costs. Raw float64 logit payload619315200bytes plus overhead,
not peak-memory accounting. Full tensor archives local/ignored;no trained-model archive written.

Five artifacts:evaluation-plan.json,interior-prompts.json,evaluations.pt,measurements.json,
validation-summary.json plus summary.json. Schemafold-c321-interior-eval-v1 retains all three
passes,original fingerprints/policies,receipts and reproduction errors. Report ten scored states,
20split partitions,10reproductions and separate arm pass counts. Numerical no-neural reconstruction
of scores,controls,prompts and JSON is mandatory,with hash/size checks and no-overwrite policy.

## Review/runtime/stop boundary

Own24/modules206/loaded5246/focused5245;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:813f7283535086c9b7ebd416da1fb1d50b5240ece9d58e364173b4cb4d433fea.
Commit/refetch/review all6OWN before activation. Tests cover independent prompt parsing,native
query spans,both actual readout policies and accepted forward/eval functions on controlled
components,paired source/target identities,all47hash guards,source coverage,correct C319 loader,
primary separation,semantic suite IDs,persistence/tampering,UTF8/CP932 and CLI indices.
Local substitute components are software evidence,not real FOLD capability or full5245 success.

Retain C320 recovery's one-process observed full-suite run,unique direct UTF8/fatal-trace logs,
fixture-boundary markers,exact child exit decimal/hex,and previous preflight-log preservation.
No per-module splitting,no test skipping,no automatic retry. C320's old interruption cause
remains unknown despite its successful retry. Native Windows ParseFile,47real parent archives,
actual probes,own24/full5245 remain mandatory user-side Validate gates.

Validate failure skips science/publication. Any source/artifact/replay/policy/integrity failure
repairs SAME C321. Valid primary failure is not repaired by changing family/seed/thresholds.
Success would show discrimination on these finite new families,not arbitrary name matching;
the change introduces new character-order patterns as well as removing simple identifying cues.
C322 waits for formal C321 judgment. Gate F remains NOT PASSED.
