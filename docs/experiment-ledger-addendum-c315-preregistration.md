# C315 preregistration — single-character examples at fixed training budget

Experiment:C315-v5b-single-character-mix. Stage:V5-B-SINGLE-CHARACTER-MIX.
Acceptance base:c9443536d956944c3f04d9825d01742a7851bbee. C314 diagnostic PASS;C313/C312 negatives and Gate F NOT PASSED remain.
C316 NOT REGISTERED. No C315 scientific outcome observed before this registration.

## One question

At fixed1200 updates and trained maximum4,does replacing part of the2/3/4 mixture with canonical
single-character names improve unseen6 reliability? This tests the user's short-example proposal,
not a consequence proven by C314. No promise of abstract-rule learning or a cure for similar names.
Fresh initial seeds315001..315005,paired order seeds315101..315105;two arms,two_to_four and one_to_four.
All10 new models train from scratch. Keep all five pairs,not previously successful cores/checkpoints.

## The changed factor and its confounds

Control lengths2,3,4,100 exposures/logical TRAIN row/length. Candidate1,2,3,4,75 exposures each.
Both300epochs*4=1200updates,57600row presentations/model. Thus adding shorter examples dilutes
longer-length exposure;this is a fixed-budget curriculum allocation,not an isolated diversity effect.
No extra learning budget is given to candidate. No additional5/6 examples enter learning.
Only original TRAIN192 rows/96 intact paired questions are used;original HOLDOUT96 untouched.
Same logical rank/order per epoch for both arms:private randperm96(order+306000+epoch),four
consecutive24-pair batches,all96pairs exactly once. No value-balanced batching or new pair selection.

Control cycle2,3,4 has profile=(epoch//3+length-2)%3,exactly matching the accepted random schedule.
Candidate cycle1,2,3,4 has profile=(epoch//4+length-2)%3 except length1 uses canonical repeat only.
Every candidate longer length receives25 row exposures per profile;length1 receives75 total,not
225. Length/profile timing and global profile frequencies differ as part of this schedule.
The first actual batches differ,so first losses need not match. Compare discarded common-input
initial output/preclip gradients/one-update equality instead,including English/Japanese length1.

For length1 the three legacy name families collapse to the SAME strings. Store a single profile,
train it only in its allotted epochs,and evaluate it once per original logical row/view. Do not
count identical labels as independent tasks or repeat it three times per epoch. Mask views remain
separate interventions. Longer2..6 renderers and source IDs/targets remain byte-exact to accepted
C312/C313 prompts. Original value splits unchanged;no HOLDOUT augmentation via value renaming.

## Unchanged model/optimization and evaluation

Accepted C278 plus C304 LengthReadout,14256parameters (core3328),64slots,all parameters train.
Core learning rate.0005,others.005 via actual C308 configure/parameter_groups/optimizer_for/
verify_optimizer. Ordinary mean CE,AdamW betas.9/.999,eps1e-8,weight_decay0,global clip1 before step;
FIT_RNG612000,1200updates,CPUfloat64,threads2,deterministic. No auxiliary loss,teacher,LR sweep,
freeze,stop-gradient,new attention mechanism,early stopping or answer restriction.

Training uses normal views only of each arm's allowed lengths. Evaluation covers1..6 in both arms,
all original TRAIN/HOLDOUT values,English/Japanese and normal/evidence-blind/query-blind views.
Length1 has one profile;2..6 have three. The longest input remains61UTF8bytes+2 markers=63tokens,
so64slots do not change. Check actual query spans at one character (English1byte/Japanese3bytes),
exact token bytes/BOS/EOS/padding and no truncation. New normal inputs are4608 distinct strings.

Primary:ALL5 one_to_four states pass original local/masked SIX gates. Keep accuracy.90,query_pair.80,
evidence_drop.35,query_drop.35,two_order.80. Use C304.score_length unchanged for2..6;report all
100 state/length/split partitions. Length1 normal/masked counts and normal NLL are descriptive
20 state/split records,not a new local capability gate or an input to the primary decision.
Full256-class argmax kept. Six success does not imply superiority over control,arbitrary-length
reasoning or Gate F. All prior verdicts remain;never substitute old five success for this primary.

## Writer contracts,dependencies and protected evidence

C314 execution:41d132a50b246de5357a3878606a1ac7776c830d;publication:ec39b319d333527d4786ac6299ded6faa6a1601b.
Summary:runs/c314-v5b-six-boundary-31c4ca923fa8459cbe9afde6fade9c83/summary.json.
Summary SHA256:daa6403d0eb00399cecb73e83693db41dbbb42151b979080d904428da5484e51. C314 source blob:c84328a825b3edf1525faae6f140280953cca63c.
Verify41 summary hashes BEFORE exact C314.verify_artifacts with40 ancestors and accepted HEAD.
C314 writes three diagnostic JSONs,NOT a model or dataset. The report is not used as training data.
After recursive verification,read C312 dataset.json/length-datasets.json at paths[2],and C313
six-dataset.json at paths[1]. Check canonical hashes,IDs/targets and reproduce original2..6 text.
C314 summary/parent diagnostics:8640 pairs,17280answers,89new errors,3persistent,8548six correct.
These outcomes do not become a candidate quality requirement or alter the data split.

Sole direct repository import C314. Its C313/C312 context supplies the actual C308 optimizer,
C304 model/prefix/scorer/span,C296 intact-pair helper,C287 normalizer,C310 no-neural guard and backend.
Explicit parent/C313/C312/C308/C304 pins plus inherited C304.PINNED and actual local helper/factory
module coverage remain mandatory. Retain730source pins/1369inputs;add OWN6 and4parentfiles:
source736/protected1379. No accepted source/test/preregistration/log/dispatcher changes or exclusions.

## Work,storage and authoring gates

10models*1200=12000updates;576000training rows. Evaluation16 unique profile blocks=144forwards/
13824rows per model,then identical strict replay. Total14880model forwards,852480row presentations,
59520core calls. Ten strict state loads;one10-state checkpoint bundle write/read;network0.
Operational probes and recursive verification/regression costs are separate from scientific work.

Seven artifacts:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c315-single-mix-models-v1 and fold-c315-single-mix-eval-v1. Save actual1200step schedule,
row/profile exposure counts,all losses/LRs/gradient receivers,full/core initial/final fingerprints,
and every final view's logits. Strict replay<=1e-9 and exact argmax;no overwritten run directory.
New archives have a single length1 profile;do not send them to an old four-length cohort analyzer.
Child no-neural postcheck rebuilds scores,schedules,counts,primary and all JSON/hash/size evidence.

Own32/modules200/loaded5086/focused5085;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:eb47e7656de2e83666bb780ea6bbbed34e9c56cfd00d4611ad8cca75b5e50c6d.
Commit/refetch/review OWN6 before activation. Require UTF8/CP932,unbound globals0,real suite ID
counting,41path CLI correctness,one-character degeneracy/span checks,original random-schedule
compatibility,actual production train/replay/loader dispatch and independent1200step reference.
Windows Validate still needs real41parentarchives/pins,actual FOLD one-character bilingual
common-input probe,own32/full5085 regression and dispatcher/launcher/runner ParseFile.
Validate failure skips science/publication. Integrity failure repairs SAME C315;valid primary
failure is ACCEPTED VALID NEGATIVE. C316 waits for formal C315 judgment;no outcome-driven retuning.
