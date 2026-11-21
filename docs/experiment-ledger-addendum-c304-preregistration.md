# C304 preregistration — length breadth to unseen five

Experiment:C304-v5b-length-breadth-to-five. Stage:V5-B-LENGTH-BREADTH-TO-FIVE.
Acceptance base:c8ccecbbfbb74cffb520ed4da507c9f7b8c0623b. C303 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C305 NOT REGISTERED.

## One question and explicit controls

Does training at lengths2/3/4 improve unseen five-character identifier reliability over training
at4 alone or3/4,with common maximum training length4 and1200 updates? This implements the user's
requested length-breadth axis. Use ordinary FULL learning in every arm,not the core-frozen policy
that performed better in C303. No residual stop,gain,auxiliary loss or learned parent checkpoint.

Fresh seeds304001..304005 with private order seeds304101..304105. Matched triples:
-four_only:train4 only;
-three_four:train3 and4;
-two_three_four(candidate):train2,3,4.
Each gets1200 updates,48 rows/update,one optimizer and identical logical row and profile order.
Candidate gives each logical TRAIN row100 presentations at EACH of2/3/4,matching the earlier100
per trained length. Controls get300 at4 or150 at each3/4. Total exposure is equal within this C,
not equal per-length across its arms. Coverage,exposure allocation and temporal spacing remain
coupled. A positive result supports this coverage policy on this bounded family,not proof of a
length-independent rule. A negative result does not identify a unique representation defect.

## Common context expansion is necessary,not hidden

The original48 slots include BOS and EOS. Japanese five-character normal prompts are52 UTF-8
bytes,so require54 slots. Use64 for ALL arms in training and evaluation;never truncate,drop
Japanese,change byte tokenization or feed gold answers. Maximum logical name length5 remains
separate from prompt byte length. Same alphabet and value vocabulary as the accepted task.

The accepted ShortByteLanguageModel has no slot-indexed learned weights. Its frozen dataclass
max_tokens and its recurrent core's slots control shapes only. Clone actual untrained C278
backbone/read parameters and replace those two copied configs with64. New child LengthReadout
reproduces C278's operations and provenance checks with the runtime frame size instead of48;
child span_mask generalizes only that shape contract. State names/order and14256 parameters
remain identical,core3328. No accepted file is edited or globally monkeypatched.

Operational TRAIN-only compatibility probe compares old48 C278 versus new64 on lengths2/3/4,
all three profiles and all views,using the first English and Japanese logical TRAIN rows.
A deterministic nonzero reader-output perturbation is applied identically to ephemeral copies,
so attention parity is not hidden by its zero output initialization. Require logits and all
parameter gradients within1e-9 and exact argmax. Probe labels cycle ASCII0..3 solely to exercise
software gradients;they are NOT capability ground truth or additional training. Copies are discarded.
Actual make_models creates independent identical unperturbed64-slot triples. The unit test reads
accepted backend/core/reader definitions and exercises the same contracts. Compatibility checks
are bounded numerical checks,not proof that longer training trajectories equal old48 trajectories.
The larger frame increases slot-level computation. Forward call count alone is not matched FLOPs
to any prior48-slot experiment. Do not causally compare historical pass counts from different seeds.

## Data,order and five-character scoring

Use the exact accepted C267 dataset SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
TRAIN192,HOLDOUT96;same value-pair split,entities,language,permutations,queries and targets.
Render two facts and a query with repeated names,shared prefixes or shared suffixes. The2/3/4
renderings must match the accepted C267/C270/C283 functions byte for byte under all views.
Five uses the same construction at length5. Persist all3456 unique normal prompts across2..5,
plus evidence/query-blind views;verify existing-byte alphabet,max52bytes,and BOS/EOS boundaries.
Five-character prompts are never optimizer inputs. HOLDOUT values are never optimizer inputs.
Operational untrained5-length smoke and software tests are not scientific training or selection.

300 epochs*4 batches. In epoch e,length=allowed[e modulo number_of_lengths];
profile=(e//3+e%3)%3. This is IMPORTANT:profile=e%3 would lock each length to one profile in the
three-length arm. Current schedule covers all nine length/profile pairs;candidate update matrix
[[136,132,132],[132,136,132],[132,132,136]]. Every arm has400 updates per profile.
Private randperm96 with order_seed+304000+e;24 intact query pairs per batch. Same pair order and
profile at every step in all arms. Global fit RNG608000 resets before every fit.
Ordinary mean CE;AdamW lr.005,betas(.9,.999),eps1e-8,weight_decay0,clip1;all parameters train;
no early stop,checkpoint choice,coefficient search or extension after observing results.

Evaluate final frozen models at all2/3/4/5 lengths,both languages,all profiles,TRAIN/HOLDOUT value
splits,and normal/evidence-blind/query-blind views. Five's TRAIN label means TRAIN values at an
UNTRAINED length,not training on five. Two is also unseen by some controls;report that explicitly.
The existing C270 scorer groups the same logical rows,values,permutations and query pairs;it
never inspects the length of a name. Map family labels into its three profiles without modifying
its criteria. Preserve the canonical scorer profile names in nested measurements and place
identifier_length separately. C287 normalization uses its triple-shaped score schema,not a
claim that the prompt length is three. All local accuracy/query-pair/two-order/mask checks remain.

Primary PASS iff all5 two_three_four models pass every FIVE-character criterion. Thresholds:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Descriptive old-length
results do not rescue primary failure or change C303's old verdict. Absolute PASS is not superiority
unless concurrent controls justify it. No arbitrary identifiers,length-independent-rule proof,
production adoption or Gate F promotion. Retain all15 models and both control comparisons.

## Parent contract and protection

C303 execution:8e01ac5bb1dae57f129615731b7013eed43b5719.
Publication:726d43f4236f5128d88c3e38dfe77de4988c73b7.
Summary:runs/c303-v5b-gradient-route-ef832a6117c44389aa035cd16c76be70/summary.json.
Summary SHA256:33d3370d383d8f220cea46056cb0fefdae27498794110fb7672bca726bc45d01.
Parent source:fold_lm/v05_benchmarks/model_c303_residual_gradient.py;blob0a59fd58ad89e460976f64218460c6de17ef8228.
Verify30 ordered hashes before C303.verify_artifacts(parent_dir,29 ancestors,accepted HEAD).
The exact summary commits all8 artifact names/hashes/sizes. Require FAIL,original three-arm task
counts,matched groups/replays. Read verified dataset.json;never initialize from its trained states.
Only direct import C303. Its context provides C301,audit,C287,C283 and the shared helper bundle;
C301.pair_source yields accepted pair construction. All called language/core/span/scorer helpers
are inherited pins;their exact deciding blobs are additionally checked in PINNED. Retain all664
source pins and1228 protected inputs. Add OWN6 and9 C303 input files:source670/protected1243.
No accepted sources/tests/logs/dispatchers are modified and no new exclusion is introduced.

## Workload,persistence,review and stop

15 models*1200=18000 updates;864000 training-row presentations. Each state gets108 final and108
reload evaluation forwards,10368 rows each. Total21240 forwards,1175040 rows,84960 core calls.
Per train/eval record1308/67968/5232;per replay108/10368/432.15 strict state loads,one15-state
checkpoint bundle write/read,network0. Training/workload increase is explicit. Operational
preflight/probes/tests and old-artifact reconstruction are separate. Every model uses64 slots.

Seven outputs:architecture-plan.json,dataset.json,length-datasets.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json plus summary.json. New model bundle
fold-c304-length-models-v1 records slots64 and ordered identities;eval archive
fold-c304-length-eval-v1 records all raw length/view outputs,1200 losses and complete schedules.
Save120 final partitions,80 candidate/control contrasts and per-length/model gates. Strict-load
all states and replay every view,drift<=1e-9 and exact argmax. Saved verifier reconstructs all data,
schedules,scores and gates without neural execution. Full tensors/maps remain local/ignored.

Own40/modules189/loaded4750/focused4749;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:af8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0.
Commit/re-fetch/post-authoring review of OWN6 required before activation/command release.
Check UTF8/CP932,actual integration,free globals,runner indices,source coverage and parent dispatch.
Mandatory Windows Validate:all30 parents/pins,real data/render/shape parity,all15 schedules,
old48/new64 forward+gradient check,untrained5-shape smoke,own40 and focused4749. Preserve the
active_v2 dispatcher/selected-launcher/runner ParseFile chain. Validate failure skips science
and publication. Any integrity issue repairs SAME C304. A valid primary miss is VALID NEGATIVE.
C305 is unregistered until C304 formal judgment. No post-hoc factor,seed,budget or gate changes.
