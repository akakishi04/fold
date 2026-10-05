# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs and historical dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C305 ACCEPTED PASS (diagnostic integrity only). C306 ACTIVE / NOT YET JUDGED. C307 NOT REGISTERED.**
C304 remains ACCEPTED VALID NEGATIVE. C306 is the unique ACTIVE broad-length/core-freeze comparison.
Latest accepted scientific execution:9c8beb3c66548c1e68def4ea2ced93acc0067e6e.
Latest accepted published log:f89d33f9dd0dd84a54f045541117ca48a4f0a342. Do not rerun C305.

## Latest accepted evidence — C305

Acceptance:docs/experiment-ledger-addendum-c305-c306.md.
Acceptance commit:73282101c89ac14cf5aa55d6d91c4bedc87b176d.
Summary:runs/c305-v5b-length-overlap-4d5851c168fc401cbc5926f1d1ca841c/summary.json.
SHA256:dd8580fe7f544b2e94688c4236cb862cfc77bb57984b04e5116a2c2cd8cc4734.
Own32/focused4781 PASS;source676/protected1257;run_execution_valid=True.
Manifest844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd.
Candidate five-HOLDOUT errors430,of which418 also wrong at4 (97.2093%),new12,recovered4.
By failing seed304001/304002/304004:persistent/five-errors168/168,136/144,114/118.
The two other candidate seeds have zero errors4/5. Same wrong byte counts166/133/112;
persistent errors can change wrong answer without becoming correct. These are known dependent
paired observations,not independent trials or a new capability gate. TRAIN-value examples have
70 five-errors,57persistent,13new,2recovered:some length-specific errors remain.
C305 scientific training/forwards/state loads/new checkpoints0;all15 parent models retained.
Overlap is not a mechanism diagnosis or proof length is solved. C304 five gates remain3/2/2.

## Active C306 — core freezing with2/3/4 training and unseen5

Experiment:C306-v5b-broad-length-core-freeze. Stage:V5-B-BROAD-LENGTH-CORE-FREEZE.
Registration:docs/experiment-ledger-addendum-c306-preregistration.md.
Design:docs/v5b-broad-length-core-freeze-v0.1.md.
Review:docs/c306-post-authoring-review.md.
Acceptance base:73282101c89ac14cf5aa55d6d91c4bedc87b176d.
Authoring/review target:eb84648751125f11289abd257aedd20787f39088.

One question:at identical broad-length training,does fixing the initially random core improve
unseen5 reliability versus full training? C303 core_frozen4/5 quad is a motivation,not an adopted
policy or concurrent control. C305 did not establish a core mechanism. Keep the user's2/3/4->5
axis rather than extending further before learning stability improves.
Fresh paired seeds306001..306005 and order seeds306101..306105;full_train versus core_frozen.
Do not reuse learned parent states or pick successful initial cores. Every pair starts with
identical full state dictionaries and independent storage. Actual accepted C304 LengthReadout,
64slots,14256stored parameters remain. Full arm trains14256;candidate10928;core3328 frozen at
its seed's random initial value. Record actual gradient receiving counts/names separately.

Only core requires_grad flags and optimizer membership change. No detach,gradient-stop wrapper,
new forward hooks,coefficient,extra loss,core removal or output filter. Core still computes and
passes backward signal to its inputs;encoder/reader/output parameters remain trainable. On
operational discarded first-TRAIN-batch copies,require initial logits and noncore preclip gradient
agreement,absent frozen core gradients and nonzero encoder gradients. No probe update is used.
Freezing changes trainable capacity,global clipping and backward work;do not claim equal FLOPs,
speed or unique causal attribution. This is a complete training-policy comparison.

Normal TRAIN only,192logical rows/96pairs.2/3/4 lengths,300epochs*4updates,24pairs/48rows per update.
Private shuffle randperm96(order+306000+epoch);length=2+epoch%3;
profile=(epoch//3+epoch%3)%3;every row100 exposures per length and400updates per profile.
Same complete events/initial weights/first CE within each pair. Global fitRNG612000 reset per model.
Ordinary meanCE,one AdamW1200updates,lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1.
No5/HOLDOUT/masked training,no early stop,sweep or checkpoint selection. All old language/profile
renderers and nontruncating64-slot tokenization are reused without changes.

Freeze final models;evaluate2/3/4/5 normal,evidence-blind,query-blind views. Save all10states,
strict-load and replay every view;max logit drift1e-9,exact argmax,unchanged final state.
Candidate core hashes must equal initial;full-train core hashes must change. Both arms save
initial/final core fingerprints,all1200losses/events,actual gradient-receiving union/counts and
final logits. Primary PASS iff ALL5 candidate models pass every original-style five-character
local/masked criterion. Thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,
two_order.80. Report10 seed records,80partitions,40paired correct-count contrasts and10gradient
summaries. Show control and candidate separately;TRAIN fitting does not replace HOLDOUT transfer.
Absolute5/5 is not automatically superiority to a5/5 control,arbitrary-length competence or Gate F.

## Parent contract,protection and workload

Verify32 ordered summary hashes BEFORE exact C305.verify_artifacts with31 ancestors and its
accepted execution HEAD. The C305 verifier returns ONE payload dict,not tuple. Its exact summary
seals3artifact descriptors;require diagnostic scope,original flags and720/120 reconciliation.
C305 has no dataset/checkpoint. Read the recursively verified C304 dataset from the SECOND summary
directory. C304 prompt_dataset/validate_prompts recheck canonical hashes/render identities.
Never use the aligned predicted answers as learning targets. New weights start from scratch.

Sole direct import C305. Its context exposes C304,c;C304 context yields C301 pair-helper access,
C287 normalizer,C283 renderer/scorer and original model/core bundle. Child owns initialization,
schedule/training/analysis because accepted C304 cohort functions require oldseeds/full-corechange.
Reuse only compatible C304 LengthReadout,training_tables,schedule_stats,score_length,evaluate and
replay_one. Original all-masked/local scoring is not reimplemented or weakened.
Keep all676 inherited sources and1257 protected inputs. Require exact C305/C304 blobs and all
C304.PINNED backend/core/reader/scorer sources;actual pair/context/core/factory language helpers
must be source-covered. Add OWN6+4 parent inputs:source682/protected1267. No accepted file edits
or new historical test exclusion.

Work:10models,12000updates,576000training rows,14160model forwards,783360total row presentations,
56640core calls,10strict state loads,one model bundle write/read,network0. Operational probes,
regression fixtures and recursive saved-data verification are separate from scientific counts.
Seven artifacts:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. Schemas:
fold-c306-broad-core-models-v1 and fold-c306-broad-core-eval-v1. Full datasets/checkpoints/tensors
stay local/ignored;console mirrors compact receipt and aggregate results. Numerical postcheck
rebuilds all outcomes from saved logits without executing a model.
Own32/modules191/loaded4814/focused4813;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static plus executed local software tests).
All6 OWN fetched at eb84648751125f11289abd257aedd20787f39088 and local Git hashes match6/6.
After all matches:normal own32 PASS14.770s;whole-suite CP932-emulated own32 PASS20.192s.
Linux/Python3.13.5/PyTorch2.10.0+cpu;Python files/3embedded blocks compile;globals0;
UTF8/noNUL;manifest matches. Actual child1200-step loops,core freeze/optimizer/determinism,
first-batch gradient routing,source factory state/pointers and accepted C304 evaluate/replay
helpers are tested using substitute backend components. Production run tests use10fits before
10replays,actual bundle serialization/loading and semantic reconstruction/tamper detection.

Local parent support is selected fetched C304 definitions,not a full byte-identical parent module
or repository clone. Only OWN6 are asserted byte-identical. Parent archives/verifiers,Git,legacy
scorers and full suite members are substituted where unavailable. No actual FOLD training or
4813-suite completion is claimed here. Windows32-parent/pin verification,actual model gradients,
PowerShell ParseFile and full4813 regression remain mandatory local gates before science.
The exact unchanged active_v2 dispatcher was fetched;its blob is e3923b6224959b442afefa02fafa967e2e6d462e.
Activation must retain all6 reviewed files and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C306 -> Validate(32parents,682/1267
protection,real2/3/4 schedules,initial logits/noncore gradients and frozen-core policy,own32,
focused4813) -> authoring_runtime_preflight=PASS -> Execute(10models*1200updates,all2/3/4/5
views,core-state invariants,strict replay,saved reconstruction) -> log publication.
Validate failure skips science/publication. Any integrity issue repairs SAME C306 with unchanged
scientific conditions. Valid all-five miss is ACCEPTED VALID NEGATIVE. Do not select models,
change budgets,freeze conditions or thresholds after results. C307 waits for formal judgment.
Gate F remains NOT PASSED. Separate scientific execution HEAD from log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c305-pre-acceptance.md.
Git blob26b48f27c3610c8455347742fdd6774c01f4bd35.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
