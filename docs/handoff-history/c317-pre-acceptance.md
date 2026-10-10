# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C316 ACCEPTED VALID NEGATIVE. C317 ACTIVE / NOT YET JUDGED. C318 NOT REGISTERED.**
C317 is the unique ACTIVE frozen query-endpoint diagnostic;no C317 scientific outcome yet.
C315 negative,C314 diagnostic PASS,C313/C312 negatives,C308 bounded PASS and C309 negative unchanged.
Latest accepted scientific execution:233b2aeefb540fd71ca2e8ab81d57f2088a063b1.
Latest accepted publication:959ccd70646bf917d3e3de8ce20ff0730f4552a4. Do not rerun C316.

## Latest accepted evidence — C316

Acceptance:docs/experiment-ledger-addendum-c316-c317.md.
Acceptance commit:590edfc7b00fadf894cc5ce629294259843de5de.
Summary:runs/c316-v5b-single-replication-633dc1183add481189698a356817d951/summary.json.
SHA256:875d6dedbaf6e5de8ca998f6a94dfb2f39dbcf5b92a6c5527334d906dc149814.
Own32/focused5117 PASS;742sources/1393inputs;run_execution_valid=True;all_pairs_matched=True.
Both arms5/5 at2..5;unseen6 control4/5,candidate4/5. Paired3both,1candidate_only,1control_only,0both_fail.
Candidate rescues316002 (573/576,287/288 ->576/576,288/288) but loses316003
(576/576,288/288 ->576/576,287/288). Other three states have perfect six normal answers.
Total normal six errors4->1. No uniform improvement or replicated pass-count advantage.
Single-character candidate normal answers all perfect;control316002 gets189/192 TRAIN,94/96 HOLDOUT.
No more seed-only search. C315's earlier3/4 result and all prior verdicts remain separate.

## Active C317 — frozen query endpoint

Experiment:C317-v5b-frozen-query-endpoint. Stage:V5-B-FROZEN-QUERY-ENDPOINT.
Registration:docs/experiment-ledger-addendum-c317-preregistration.md.
Design:docs/v5b-query-endpoint-probe-v0.1.md.
Review:docs/c317-post-authoring-review.md.
Acceptance base:590edfc7b00fadf894cc5ce629294259843de5de.
Authoring/review target:207696e82df54d35ac53cd75fed7496685c687dd.

One question:with all C316 weights fixed,how does replacing only the last query-byte readout
anchor by the first query-byte anchor affect predictions? Preserve the mean-query branch.
Retain all10 original C316 models/seeds316001..316005/both two_to_four and one_to_four cohorts.
No new learning,seed search,model selection,frame expansion,new parameter or answer repair.
The model stays the actual accepted C304 LengthReadout,14256parameters,64slots,full256-class output.

C304's native read.query is called first with the masked query-span mean,and second with the
local state at the final query byte. Child temporary hooks capture tokens and masked encoder
output,verify both native query-input identities exactly,and replace only that second input
in first_byte mode. Same shared query weights,keys,value representations,softmax,.5 averaging,
core/residual/norm/classifier computation remain. Actual parent forward executes normally;
no accepted method/global/source/weight is changed. No labels or expected answers enter forward.
FIRST BYTE is literal,not a whole Unicode character or guaranteed distinguishing character.
Japanese length1 uses three bytes;English length1 uses one byte.

Fixed mode order:original_before -> first_byte -> original_after. Every mode uses identical
observer/provenance hooks,which leave native inputs unmodified in the original modes.
Strict-load each original state once;all parameters frozen/eval/no-grad. Full fingerprint and
forward/pre-hook registries including kwargs/always-call flags remain unchanged after every pass.
Enforce one encoder capture and exactly two query projections per forward;intermediate
CPUfloat64/shape/finiteness checks. Complete hook cleanup is required on success AND exception.

All1..6 lengths/profiles/splits/normal/evidence-blind/query-blind views are evaluated in allmodes.
Original before AND after reproduce each parent logit<=1e-9 and exact argmax;original2..6 gates
must remain unchanged. Every query-blind output is bit-identical between endpoints because
its query is a one-byte '?'. All English length1 views also bit-identical. Japanese length1
is not a degenerate endpoint control. No restored pass is counted as a new independent model.

Score original_before and first_byte with unchanged local/masked2..6 gatesaccuracy.90,
query_pair.80,evidence_drop.35,query_drop.35,two_order.80. One-character single-profile metrics
remain descriptive counts/NLL,not a new gate. Report20 state/mode results,200 length/split
partitions,40 single-character records,10 reproduction receipts,640 paired local groups and
46080 paired normal rows. Group by seed/arm/length/split/profile/language;record both rescued
and regressed answers and wrong-to-wrong flips. Never choose an endpoint per correct answer.

C317 PASS means diagnostic integrity/restoration/persistence only,not an improved capability.
The intervention is outside the original training configuration;failure does not prove first
information useless,and success does not prove a first-anchor model can learn better. No claim
of a unique training/attention/language mechanism. C316 negative and Gate F remain unchanged.

## Parent evidence,dependencies and workload

Verify43 ordered summary hashes BEFORE exact C316.verify_artifacts(parentdir,42ancestors,
accepted execution HEAD). Exact C316 summary seals7 artifact descriptors. Require acceptedFAIL,
ten original result flags,4/4 six counts and matched/replayed metadata. Read canonical C316
inputs and final logits from fold-c316-single-replication-eval-v1. Actual C316.load_bundle handles
fold-c316-single-replication-models-v1;actual make_models takes original seeds and its own context.
Match ordered identities and strict full-state fingerprints. No diagnostic schema guessing.

Sole direct import C316. Its context provides protected C315 evaluate/validate_raw/replay_error,
C304 span/scorer,C287 normalizer,C310 no-neural and backend. Preserve742sources/1393inputs,
C315.PINNED/C304.PINNED and actual repository-local/factory-language helper coverage. Add OWN6
plus8 parent files:748sources/1407inputs. No accepted edits,new exclusions or protection waiver.

Science10saved states*3passes*144=4320model forwards,414720row presentations,17280core calls.
Per pass13824rows,288query-projection calls,8928rows with distinct first/last endpoints.
Ten strict model-state loads,one parent bundle read,training0,new model checkpoints0,network0.
Eight discarded bilingual length1/6 operational forwards,parent recursive verification and
software regressions are separate. Instrumentation overhead is not a speed benefit.
Raw logit payload849346560bytes before serialization overhead,not peak-RAM accounting.
Four outputs:audit-plan.json,evaluations.pt,measurements.json,validation-summary.json plus summary.
Archivefold-c317-endpoint-eval-v1 retains all three raw modes,original hashes,hook receipts and
replay errors. No trained-model archive written. Full arrays local/ignored;aggregates in log.
No-neural postcheck reconstructs every score,one-byte control and paired count;hash/size checks
and no-overwrite apply. Own32/modules202/loaded5150/focused5149;sole exact C204 exclusion unchanged.
Manifest:10f2e095d09f6ffeb424b2d91c0215aabf8739caace720c4f6662cb4f73a1d10.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static plus actual local software tests).
All6 OWN refetched at207696e82df54d35ac53cd75fed7496685c687dd,whole-file Git blobs match6/6.
After matching:normal32/32 PASS10.727s;whole-suite CP932-default-emulated32/32 PASS9.874s.
Both uninterrupted,zero failures/errors,exit0. Rehashed all6 after testing. Linux/Python3.13.5/
PyTorch2.10.0+cpu/NumPy2.3.5. UTF8/noNUL,Python+3embedded blocks compile,unresolvedglobals0,
manifest seal matches,43orderedpaths/CLI indices checked. PowerShell is unavailable locally.

Actual accepted C304 forward/span and C315 evaluation functions are extracted by AST in tests
and executed with controlled encoder/core/reader/scorer components. Independent first-anchor
formula,original identity,query-byte degeneracy,wrong provenance,exception cleanup,real child
432-forward inference pipeline,loader-once/persistence/tamper and43hash/protection tests pass.
Local parent support files are exact fetched function slices,not full modules/repository,and
NOT committed. Synthetic logits and substitute Git/parent/scorer/suite interfaces are software
controls,not actual FOLD capability or actual5149 inherited regression evidence.

Mandatory local Windows43parentarchives/pins,PowerShellParseFile,real frozen bilingual probe,
own32/full5149regression and actual10checkpoint inference/reconstruction remain pending.
Unchanged invoke_active_v2 was reread:unique Formal state resolution,legacy pin and all parser
guards remain. Activation must preserve all6 reviewed OWN and all accepted sources/tests/logs.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C317 -> Validate(43parents,748/1407,
real query-endpoint/bilingual frozen probe,own32,focused5149) -> authoring_runtime_preflight=PASS ->
Execute(all10frozen states,original/first-byte/original,full-view replay,one-byte identity,
paired improvements/regressions,saved reconstruction) -> log publication.
Validate failure skips science/publication. Integrity/restoration failure repairs SAME C317
with fixed science. No outcome-dependent endpoint/cohort/gate change or capability promotion.
C318 waits for formal C317 judgment. All earlier verdicts and Gate F NOT PASSED remain separate.
Separate scientific execution HEAD from later log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-activation handoff:docs/handoff-history/c317-pre-activation.md.
Git blob:1c46ebb9ba88fe66babd7e49da8bd231dc1f1ecb.
Earlier handoff:docs/handoff-history/c316-pre-acceptance.md.
Git blob:e7226bac5dcdcf8ba6d68b4120ad8a03ec38ccc3.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
