# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C314 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C315 ACTIVE / NOT YET JUDGED. C316 NOT REGISTERED.**
C315 is the unique ACTIVE single-character training-mix experiment;no C315 scientific result yet.
C313/C312 remain valid negatives;C308 bounded PASS and C309 negative remain unchanged.
Latest accepted scientific execution:41d132a50b246de5357a3878606a1ac7776c830d.
Latest accepted publication:ec39b319d333527d4786ac6299ded6faa6a1601b. Do not rerun C314.

## Latest accepted evidence — C314

Acceptance:docs/experiment-ledger-addendum-c314-c315.md.
Acceptance commit:c9443536d956944c3f04d9825d01742a7851bbee.
Summary:runs/c314-v5b-six-boundary-31c4ca923fa8459cbe9afde6fade9c83/summary.json.
SHA256:daa6403d0eb00399cecb73e83693db41dbbb42151b979080d904428da5484e51.
Own24/focused5053 PASS;730sources/1369inputs;run_execution_valid=True.
8640 paired rows/17280 answers;five correct8637,six correct8548.
Both correct8548,new errors89,both wrong3,same wrong3,recovered0.
120 local totals and20 transition totals match;zero neural work.
Representative examples,NOT all-group aggregates:random312001 shared-suffix errorsEnglish6/144,
Japanese19/144;random312002 shared-prefix errorsEnglish5/144,Japanese0/144. The former Japanese
HOLDOUT mean target-vs-best-wrong gap8.378211460508153->3.554789852911447,all48 gaps decreased.
English six inputs use27tokens,Japanese63 under64slots. English failures rule out a purely
Japanese-near64 explanation for every error;language,position,content still are not separated.
Diagnostic PASS does not change C313 six capability negative or Gate F.

## Active C315 — single-character training at fixed budget

Experiment:C315-v5b-single-character-mix. Stage:V5-B-SINGLE-CHARACTER-MIX.
Registration:docs/experiment-ledger-addendum-c315-preregistration.md.
Design:docs/v5b-single-character-mix-v0.1.md.
Review:docs/c315-post-authoring-review.md.
Acceptance base:c9443536d956944c3f04d9825d01742a7851bbee.
Authoring/review target:1d15baedb214a9af0109056e8dd2dd7f302c788b.

One question:at fixed1200updates and trained maximum4,does adding canonical length1 improve
unseen6 reliability? This tests the user's short-example proposal,not a proven C314 mechanism.
Fresh initial seeds315001..315005,paired order seeds315101..315105. Two arms:two_to_four control
and one_to_four candidate. All ten models train anew;no prior successful or failed state is reused.

Control sees each original TRAIN row100times at2/3/4. Candidate sees75times at1/2/3/4. Both
300epochs*4batches/1200updates,57600row presentations/model. Candidate short examples replace some
long exposure;this is not pure diversity with long exposure held constant. No extra candidate
training budget. No length5/6,HOLDOUT or masked views enter optimization.

Every epoch shares the same private randperm96(order+306000+epoch),consecutive24intact query-pairs
per batch. Each logical TRAIN row appears once/epoch and both questions stay together. No value
balancing/new rows. Control cycle2/3/4 profile=(epoch//3+length-2)%3 exactly matches old C312 random
schedule after length-index translation. Candidate cycle1/2/3/4 profile=(epoch//4+length-2)%3 except
length1 profile0. Candidate longer profiles each25 exposures/row;length1 only75total,not225.
Logical pair order is identical across arms;length/profile timing and global frequency differ.

Length1 repeat/shared-prefix/shared-suffix all collapse to the same string. Store/train/evaluate
one canonical repeat profile. Do not count identical profile labels as independent tasks.
Length1 normal/masked/NLL diagnostics have192TRAIN/96HOLDOUT rows per state,not576/288.
Old2..6 prompts remain byte-exact. All4608normal inputs across1..6 are distinct;max61UTF8bytes
plusBOS/EOS=63tokens fits64slots. Verify exact bytes,markers,padding and English1byte/Japanese3byte
single-character query spans. Query-blind span is one question-mark byte in both languages.

Model unchanged:actual C278 with C304 LengthReadout,14256parameters,3328core,64slots,all trainable.
Actual C308 core_slow configure/optimizer/verification:coreLR.0005/noncore.005,ordinary meanCE,
AdamW betas.9/.999,eps1e-8,weight_decay0,clip1 before step,FIT_RNG612000,CPUfloat64,threads2,
deterministic. No new gain,auxiliary loss,freeze,teacher,stop-gradient,early-stop or decoder limit.
First actual losses need not match because the first inputs differ. Discarded common bilingual
length1/2 input probes require identical initial logits,preclip gradients and one optimizer step.
Both arms start at identical full/core weights with independent storage.

Primary:all5 new one_to_four states pass all original local/masked SIX criteria. Thresholds
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80 remain. Report all2..6 gates,
100 state/length/split partitions,20 length1 diagnostic records and paired-six outcomes.
Length1 has no newly invented full gate and cannot rescue the six primary. Success is not
superiority over the control,arbitrary names/lengths or general model competence. No old verdict
or Gate F promotion is automatic. Negative results cannot be repaired by changing seed/exposure.

## Parent contract,protection and work

Verify41 ordered summary hashes BEFORE C314.verify_artifacts(parentdir,40ancestors,acceptedHEAD).
Require parent diagnosticPASS with8640pairs/17280answers/89new/3persistent/8548six correct. Its
three JSON artifact descriptors are sealed by the exact summary. It does not provide checkpoints
or new training labels. Read verified C312 dataset/old prompts from paths[2] and C313six prompts
from paths[1]. Check canonical hashes and source IDs/targets. C314 report is not training data.
Sole direct repository import C314;its C313/C312 contexts provide C308optimizer,C304model/prefix/
span/scorer,C296pairs,C287normalizer,C310no-neural and backend. Explicit pins and C304.PINNED plus
actual local context/factory-language coverage remain. Retain730sources/1369inputs;OWN6+4parent
files gives736/1379. No accepted sources/tests/preregistrations/logs/dispatchers or exclusions change.

Science:10models,12000updates,576000training rows,14880forwards,852480row presentations,59520core
calls,10strict state loads,one model bundle write/read,network0. Final evaluation16unique profile
blocks=144forwards/13824rows per model,then144strict replay. One-character evaluations are not
tripled. Operational probes,software regressions and recursive artifact checks are separate work.
Seven artifacts plus summary:architecture-plan.json,dataset.json,length-datasets.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c315-single-mix-models-v1 and fold-c315-single-mix-eval-v1. Save every loss/LR/gradient trace,
actual schedule,exposure counts,whole/core initial/final fingerprints and all final views.
Strict replay requires<=1e-9 logit difference and exact argmax for all1..6;no overwrite. Rebuild
all scores,schedules,primary and JSON hashes/sizes under no-neural postcheck. Full tensors/maps
remain local/ignored;compact receipt and all reported aggregates are mirrored to the console log.
Own32/modules200/loaded5086/focused5085;sole inherited exact C204 exclusion unchanged.
Manifest:eb47e7656de2e83666bb780ea6bbbed34e9c56cfd00d4611ad8cca75b5e50c6d.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus actually executed local software tests).
All6 OWN fetched at1d15baedb214a9af0109056e8dd2dd7f302c788b;independent Git-blob matches6/6.
Post-match normal32/32 PASS16.153s;whole-suite CP932-default-emulated32/32 PASS16.735s.
Both uninterrupted full unittest runs. Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;
PowerShell unavailable locally. UTF8/noNUL,Python+3embedded blocks compile,unbound globals0,
manifestselfhash matches.41orderedpaths and postcheckindices[2:43]/head[43]/argc44 verified.
Canonical data/prompts,single-profile degeneracy/spans,allseedexposures,independent schedule and
1200step optimization loop,actual train/evaluate/replay accounting,loader/persistence/tampering,
41hash guards,736/1379protection and synthetic suiteID5086->5085 checks pass.
Tests09/29/30 execute accepted C312batch/C304span/C308optimizer function ASTs. Local parent support
is fetched function slices,not full modules/repository,and NOT committed. Synthetic label-encoded
toy inputs/padded models and substituted parent/Git/scorers are software controls,not real FOLD
capability or actual inherited5085 regression evidence. See review for exact scope and exclusions.
Mandatory real41parentarchives/Windowspins,PowerShellParseFile,actual FOLD one-character bilingual
probe,own32/full5085 regression and ten real fits/replays remain user Validate/Execute gates.
Activation must retain all6 reviewed OWN files and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C315 -> Validate(41parents,736/1379,
canonical single inputs/old prompt identity,allnew schedule budgets,real common-input probe,
own32,focused5085) -> authoring_runtime_preflight=PASS -> Execute(10models*1200updates,
all1..6evaluation,strict replay,paired gates/diagnostics,saved reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failures repair SAME C315. Valid failure
of candidate six5/5 is ACCEPTED VALID NEGATIVE. No post-result retuning of data/seed/exposure/primary.
C316 waits for formal C315 judgment. C314diagnosticPASS,C313/C312negatives,C308boundedPASS,C309negative
and Gate F NOT PASSED remain separate. Separate scientific HEAD from later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals and immutable historical lifecycle tests.

## Historical state

Pre-activation handoff:docs/handoff-history/c315-pre-activation.md.
Git blob:8427121d5bbd15aed63c6a1de7cec00d12270b74.
Earlier handoff:docs/handoff-history/c314-pre-acceptance.md.
Git blob:bac2b81fbaec1a30776ae75063d38808231d13f0.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
