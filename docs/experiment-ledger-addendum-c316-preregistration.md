# C316 preregistration — one fresh-seed short-mixture replication

Experiment:C316-v5b-single-mix-replication. Stage:V5-B-SINGLE-MIX-REPLICATION.
Acceptance base:0d83544dfeb835a5c74f9690008598872f3e0f2d. C315 ACCEPTED VALID NEGATIVE.
C317 NOT REGISTERED. Gate F NOT PASSED. No C316 scientific outcome observed before registration.

## One question and stopping boundary

Does the fixed C315 one-character allocation reproduce its unseen-six reliability in one new
paired cohort? New initial seeds316001..316005 and paired-order seeds316101..316105 only.
Both two_to_four control and one_to_four candidate remain. No old checkpoint or good seed reuse.
This is one preregistered replication,not an authorization to keep replacing cohorts until5/5.

C315 gave3/5 control and4/5 candidate at six,with a single rescued seed and one shared failure.
That bounded improvement is not enough to change the mixture,train longer or declare superiority.
C316 retains every policy and evaluation condition. Primary:ALL5 NEW candidate states pass SIX
local/masked criteria. C315 successes cannot compensate for a new C316 failed seed. A valid
primary failure is ACCEPTED VALID NEGATIVE;C315's earlier negative is never rewritten.

## Fixed science

Training maximum4. Control per logical TRAIN row:0/100/100/100 exposures at lengths1/2/3/4.
Candidate:75/75/75/75. Both300epochs*4=1200updates,57600row presentations/model. Single-character
inputs are one canonical repeat profile,not three degenerate duplicates. Values/splits/English/
Japanese/name profiles unchanged;five and six,HOLDOUT and masked views never enter training.
Original C315 length1..6 prompt bytes/hash retained,including64slots and max63 encoded tokens.

Use ACTUAL C315.plan_for_order with the new order and the same original C312 pair inventory.
Private randperm96(order+306000+epoch),24 intact two-query pairs/batch. The two arms share identical
logical row order per epoch,not identical rendered batches. Check each complete epoch and all
per-length row exposures. The control is also checked against C312's exact random schedule.
Candidate length1 reduces longer-length exposures and changes profile timing;these confounds
remain. This is not a test with long-length exposure fixed or a proof of rule abstraction.

Actual C304 LengthReadout,14256parameters/core3328,64slots,all trainable. Actual C308 core_slow
optimizer/coreLR.0005/other.005;ordinary mean CE,AdamW betas.9/.999,eps1e-8,weight_decay0,
globalclip1 before step,FIT_RNG612000,CPUfloat64,threads2,deterministic,1200steps. No gain,auxiliary
loss,teacher,extra capacity,freeze,stop-gradient,early stopping,decoder restriction or LR search.
New model factory copies the same initial state independently to both arms,with exact whole/core
fingerprints. Discarded common bilingual length1/2 input probes require initial output,preclip
parameter gradients and first optimizer-step equality. Actual first losses may differ,as in C315.

## Reuse and numerical equivalence

Sole direct repository import:C315. Reuse its real plan_for_order,schedule_stats,training_tables,
validate_prompts,validate_raw,evaluate and strict replay. These helpers are seed-agnostic at the
interfaces used. C315.fit/schedule/make_models/analyze have fixed old-seed contracts;do not call
them with new seeds or monkeypatch their globals. The child owns a new seed-aware factory and
analyzer and an explicit-schedule optimize loop matching C315.fit operation for operation.

A software integration test extracts the exact accepted C315 fit and scheduler function ASTs.
For BOTH arms,at the same original schedule on a controlled model,the child optimize function
must match all1200 losses,optimizer rates,gradient-receiver records and final weights. This is
numerical software equivalence,not evidence from actual FOLD training. Runtime uses normal
imports of full accepted modules;AST execution is confined to authoring tests.

Evaluate1..6 in every final frozen model with C315.evaluate:one length1 profile plus15 profiles
for2..6. Strict saved-checkpoint replay uses C315.replay and matches every view<=1e-9 with exact
argmax. Report100 state/length/split partitions,20 length1 diagnostic entries and five paired-six
outcomes. Length1 has only descriptive normal/masked correct counts and NLL,no new capability gate.
Thresholds stay accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. C304 scorer
and C287 normalizer remain unchanged. Full256-class argmax;both successes and regressions retained.

## Parent evidence semantics and protection

C315 execution:5708562420e530749a8f63b1f4baf3c7e0f28029.
Publication:0b4ce1c953d2ccf0eea04747b1194c6dd70729ee.
Summary:runs/c315-v5b-single-mix-dbdffe0b88094f729d1dbfbcdba520f0/summary.json.
Summary SHA256:aceda00cebf61b49e5f923bf7c426e2f4522dcac68444fc2e07b27a17b63dd66.
C315 source blob:8bf47583b3c8dd3e4e35a8612912d170a2a8b77c.
C315 manifest:eb47e7656de2e83666bb780ea6bbbed34e9c56cfd00d4611ad8cca75b5e50c6d.

Verify42 ordered summary hashes BEFORE exact C315.verify_artifacts(parentdir,41ancestors,
accepted execution HEAD). The fixed summary seals all7 artifacts and original ten outcome flags.
Require FAIL,exact3/4 six results,all_pairs_matched/all_replays. Then read canonical dataset.json
and length-datasets.json from C315 itself,not C314's diagnostic schema. Recheck DATA/PROMPTS hashes
and inherited renderer validation. No parent learned weights or predictions are used for learning.
The C315 verifier reconstructs its final predictions,learning traces and prior protection chain.

Retain736 source pins/1379 inputs;add OWN6 and8 parent files:742/1393. Explicit C315 blob plus
C315.PINNED,C304.PINNED and real repository-local parent/context/pair/factory-language helpers must
be protected. No accepted source/test/log/preregistration/dispatcher edit or new test exclusion.
No repair may waive missing deciding-path source coverage.

## Work,storage and execution boundaries

Science10new models,12000updates,576000training rows,14880model forwards,852480row presentations,
59520core calls,10strict state loads,one new10-state checkpoint bundle write/read,network0.
Evaluation/replay each144forwards and13824rows per model,unchanged from C315. Software tests,
common-input discarded probes and recursive parent verification are separate costs.

Seven artifacts plus summary:architecture-plan.json,dataset.json,length-datasets.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Child schemas:
fold-c316-single-replication-models-v1 and fold-c316-single-replication-eval-v1. Strict new loader
checks ordered new identities. Save all1200 losses,LRS,gradient counts/unions,exact events/exposures,
initial/final full/core hashes and every final view. Actual run uses its own loader once before
all10 strict parent replays. No overwrite. Numerical no-neural reconstruction checks every score,
schedule and saved JSON;all tensor/JSON artifact hashes/sizes remain sealed. Full arrays local only.

Own32/modules201/loaded5118/focused5117. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e77e05efffb480bce89fb9b16071babfff15dd533d0ac6677798478fd2103718.
Commit/refetch/review all6 OWN before activation. Require UTF8/CP932,zero unresolved globals,
42path/CLI agreement,real suite-ID sets,production train/loader/replay ordering and tamper checks.
Windows Validate requires42 actual parents/pins,new initial/common-input checks,own32/full5117
regression and dispatcher/launcher/runner ParseFile. Validate failure skips science/publication.
Integrity failure repairs SAME C316 with unchanged science. C317 waits for formal C316 judgment.
