# C317 preregistration — frozen query-endpoint intervention

Experiment:C317-v5b-frozen-query-endpoint. Stage:V5-B-FROZEN-QUERY-ENDPOINT.
Acceptance base:590edfc7b00fadf894cc5ce629294259843de5de. C316 ACCEPTED VALID NEGATIVE.
C318 NOT REGISTERED. Gate F NOT PASSED. No C317 result observed before registration.

## One question

At every frozen C316 checkpoint,what changes when the readout uses the first query-byte local
representation instead of the last query-byte representation? The mean-query branch is unchanged.
This is a targeted endpoint-sensitivity diagnostic,not another seed or learning-rate search.
Keep all ten C316 states:seeds316001..316005 and both two_to_four/one_to_four training cohorts.
No new learning,checkpoint selection,per-question endpoint choice or modification of old verdicts.

## Exact intervention on the actual accepted model

C304 LengthReadout's real forward calls the shared read.query twice:first on the masked span
mean,and then on local[rows,last_query_byte]. These two resulting attentions are averaged equally.
Temporary child-owned hooks capture input tokens and the masked encoder output. Verify the first
query input exactly equals that native mean and the second exactly equals the native last-byte
local state. In first_byte mode,replace only that second input with local[rows,first_query_byte].
The same trained query projection,keys,value representations,softmaxes,.5 averaging,core/residual,
normalizer,classifier and full256-class output remain. No new attention head or weight is added.
The original C304 function executes normally;no accepted source,method or global is monkeypatched.

Use existing visible-query span boundaries,not targets,language labels or expected answers.
FIRST BYTE is deliberately literal:Japanese characters use multiple UTF8bytes. It is NOT a
whole-character embedding or guaranteed to distinguish all Japanese names. All retained inputs
are the exact C3161..6 prompts;frame64 and14,256 stored parameters remain unchanged.

For each state:original_before -> first_byte -> original_after. All three passes use the same
observer/provenance hooks;original modes return the native query input unchanged. Every pass is
no-grad/eval with all parameters frozen. Query calls must be exactly2 per forward;the local encoder
runs once. Count every forward and validate intermediate shape/float64/CPU/finiteness. Restore
all forward/pre-hook registries including kwargs/always-called metadata on success AND exception.
Strict-load each original state once,then never reload or mutate its weights between passes.
Fingerprint and hook registries remain unchanged after each pass.

Original before AND after reproduce all parent1..6/profile/split/view logits<=1e-9 and exact
argmax;all2..6 full-gate flags remain identical. Query-blind spans contain only one '?' byte,
so every query-blind output must be exactly identical across endpoints. English length1 normal
and evidence-blind queries also have one byte,so their outputs must be exactly unchanged.
Japanese length1 is three bytes and is not used as a degenerate one-byte control.

## Reporting and non-claims

Score the original-before and changed passes using the same accepted C304 scorer for2..6:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Restored pass confirms the
original gates but is NOT an extra scored model or independent observation. Length1 remains a
single canonical profile with descriptive normal/masked counts and NLL,not a new capability gate.
Report20 state/mode results,200 length/split partitions,40 length1 records,10 reproduction receipts.
Paired normal-answer comparisons:640 seed/arm/length/split/profile/language groups,46080 rows.
Report both rescued and regressed answers,wrong-to-wrong flips and both original/candidate counts.
Do not select the correct endpoint per answer or pool successes into a new production decoder.

PASS means diagnostic fidelity/restoration/persistence only,irrespective of changed-mode quality.
A successful intervention could motivate a future TRAINED comparison,but does not prove it would
learn better. Failure may reflect an out-of-training-distribution intervention,not that first-byte
information is useless. No causal attribution to mean dilution,language,attention or training
instability is justified by this single replacement. C316's negative and Gate F remain unchanged.

## Parent writer and dependency contract

C316 execution:233b2aeefb540fd71ca2e8ab81d57f2088a063b1.
Publication:959ccd70646bf917d3e3de8ce20ff0730f4552a4.
Summary:runs/c316-v5b-single-replication-633dc1183add481189698a356817d951/summary.json.
SHA256:875d6dedbaf6e5de8ca998f6a94dfb2f39dbcf5b92a6c5527334d906dc149814.
Source blob:3d15bda5b0c4f3f487548cd6b92d3b1281febb76.
C304 model blob:cacb5852a29171aa8079e634d929fdd54e7f4f58.

Verify43 ordered summary hashes BEFORE exact C316.verify_artifacts(parentdir,42ancestors,
accepted execution HEAD). Parent summary seals all7 artifacts and original ten result flags.
Require FAIL,4/4 six counts with their exact per-state flags,and matched pairs/strict replay.
Read canonical C316 dataset.json,length-datasets.json and fold-c316-single-replication-eval-v1
FINAL logits,not a diagnostic report or a different checkpoint. Load model bundle through actual
C316.load_bundle (fold-c316-single-replication-models-v1),use its make_models with original seeds,
strict-load each matching state,and confirm the full fingerprint against its evaluation record.

Sole direct repository import C316. Its context supplies already accepted C315 evaluator/replayer,
C304 span/model/scorer,C287 normalization,C310 no-neural guard and backend. Retain742 inherited
source pins/1393 inputs,C315.PINNED,C304.PINNED and all actual local helper/factory-language coverage.
Add OWN6 plus8 C316 parent files:748sources/1407inputs. No accepted source/tests/logs/dispatchers
changed;no new regression exclusion or missing-source waiver.

## Work and execution gates

Science10saved states*3passes*144=4320forwards,414720row presentations,17280core calls.
Each pass:13824rows,288read.query calls,8928rows with different first/last byte positions.
Ten strict state loads,one parent checkpoint bundle read,training0,new checkpoint writes0,network0.
The intervention does not reduce upstream compute. Instrumentation overhead is not a speed claim.
Raw logits849346560bytes before serialization overhead;not a peak-memory estimate.
Operational probe:two parent arms*4forwards on discarded bilingual1/6 inputs;separate from science.
Parent recursive verification and software tests also have costs outside scientific forward counts.

Four child artifacts:audit-plan.json,evaluations.pt,measurements.json,validation-summary.json plus
summary.json. fold-c317-endpoint-eval-v1 stores all three raw passes,original fingerprints,hook
receipts and replay errors. No trained-model checkpoint written. All tensors remain local/ignored.
No-neural postcheck reconstructs every baseline/candidate score,one-byte identity and paired count,
and verifies all hashes/sizes. No run-directory overwrite.
Own32/modules202/loaded5150/focused5149;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:10f2e095d09f6ffeb424b2d91c0215aabf8739caace720c4f6662cb4f73a1d10.
Commit/refetch/review all6 OWN before activation. Require actual accepted model-forward integration
on controlled representations,independent first-anchor numerical oracle,query-provenance rejection,
exception cleanup,actual child inference/loader/persistence path,UTF8/CP932 and all43 CLI paths.
Windows Validate retains43real parents/pins,actual two-arm bilingual smoke,own32/full5149regression,
and dispatcher/selected-launcher/runner ParseFile. Any integrity issue repairs SAME C317.
C318 waits for formal judgment. No post-result adjustment of endpoint,cohort,gates or old verdicts.
