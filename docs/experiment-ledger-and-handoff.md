# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold. Branch:feat/sft-target-loss. Local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C266 ACCEPTED PASS (diagnostic integrity only). C267 ACTIVE / NOT YET JUDGED. C268 NOT REGISTERED.**
C267 is the unique ACTIVE experiment:V5-B paired name-coverage training.
C265 remains ACCEPTED VALID NEGATIVE. C264/C263 bounded PASS and all earlier verdicts/recoveries remain.
No architecture,optimizer default or production change. C266 did not improve model capability.
Its one saved-output decomposition is complete;C267 is a new paired training-distribution experiment.

## Latest accepted evidence — C266

Scientific execution HEAD:b377042dcdb903a308da131feb135b0f5362d9de.
Published log commit:a18f2e82e9edb9e96d5b25937041be089288e6ec.
Publisher log SHA256:a50a971d382a66e0f4af10f7376bc48027c91f99620cd53280c44d5df3ae20e2.
Log bytes:787239;lines3828.
Summary SHA256:5d9c79306aae5fb2fd39a82fae645a1447029cae3aedfb2bf92e953bb2435247.
Summary:runs/c266-v5b-query-pairs-b652a5a2d2ea4dac9b913b64df6d78e0/summary.json.
Acceptance:docs/experiment-ledger-addendum-c266-c267.md.
Acceptance/base commit:38272da75661b1f2f028719b41aa4406ee6dd26b.
This corrects a cells.json hash transcription in the immediately preceding acceptance draft;
no scientific result or accepted source was changed by that documentation correction.

Own24 PASS in7.338s;focused3549 PASS in379.386s.442 source pins/748 protected inputs verified.
17280 normal answers were attributed to8640 query pairs,720 detailed cells,120 profile summaries
and80 matched contrasts. Integer partitions and parent correct/query-pair scores reconciled.
Model forwards0;state loads0;learned-bundle loads0;training0;new learned checkpoints0.
Six saved-evaluation archive reads per analysis pass;analysis and saved postcheck are two passes.
Protected inputs and persisted reattribution passed;tracked tree clean;execution HEAD preserved;
run_execution_valid=True;scientific_status=PASS. capability_pass_claim=False;causal_parser_claim=False.

Acceptance uses immutable published log ranges,metadata and recorded user-local postchecks.
No independent user-local artifact rerun or complete-log rehash was performed. The SHA above is
publisher-reported,not a new independent reviewer measurement. Publication immediately follows
execution and adds only docs/experiment-run-logs/c266/latest.log/latest.json.

Each profile contains2880 query pairs,aggregated across all20 states and both languages:

|Profile|Both correct|Same displayed value|Same outside value|Swapped|Other unequal|
|---|---:|---:|---:|---:|---:|
|doubled|2835|19|0|0|26|
|shared_prefix|2509|298|5|0|68|
|shared_suffix|664|2142|7|39|28|

Collapse includes the same displayed value OR the same outside answer. Rates:19/2880 for doubled,
303/2880 for shared_prefix,2149/2880(74.6181%) for shared_suffix. Among2216 suffix pairs that are not
both correct,2149(96.9765%) collapse. These are pair counts,not percentages of individual errors or
independent training runs. Shared-suffix displayed collapse selects logical entity0 in1595 pairs
and entity1 in547. Logical first entity is not necessarily the first displayed fact.

The observed main failure is same-answer collapse,not exchanging two values. It does not prove a
last-character-only internal parser or complete absence of query information. Equal argmax need
not imply equal logits. Example:263001 lower_forward shared_suffix EN has44 collapsed pairs and
zero exactly-equal-logit pairs among72 total pairs. Complete per-state/language/position tables
remain in the accepted artifacts. No C265 verdict or score is revised.

Accepted artifact SHA256:
-audit-plan.json:85be4d973b9f8ce8a59e1ffa9028faceb1de3fcc8d8b3035264c2af72ed88b3e;2269 bytes.
-pair-attribution.json:038dd3a9aecc86aadcd2f99a8269103a579a3aa7787ac0bc8983e37dba082e90;3463178 bytes.
-cells.json:2c593908456838ff582c51632106f1a21af5082d081b1647fa6a6d6efbf85357;365733 bytes.
-profile-summary.json:6a33a496099a60aeb2d7715338d7c2f5caecb9cec51c0f3cff92f696f3d581d4;58160 bytes.
-matched-contrasts.json:a685b34f814b16295dae958d87dd0b23b405b8d4065e512af8262dc66d7d7bf2;18024 bytes.
-validation-summary.json:17f9a7895fc2d208d1bdb2a463c3455a78aa7aeb53698ab91952c4d7d963f12f;788 bytes.

## Preserved earlier evidence and recovery

C265 ACCEPTED VALID NEGATIVE:whole-model0/20;doubled16/20,shared_prefix6/20,shared_suffix0/20.
Acceptance:docs/experiment-ledger-addendum-c265-c266.md. These are gate counts,not zero answer accuracy.
C264 bounded two-fact PASS:all20 states;not all predictions perfect. C263 bounded PASS:all four
rate/order arms5/5 and final HOLDOUT8640/8640;standard-rate ceiling prevents an LR-benefit claim.
C262 chronology comparison remains negative overall and retains its evidence of a chronology effect.
C261 repeated-value and C260 core ablation remain negatives;C259 naming-order coverage remains negative.
C258 diagnostic PASS,C257 unseen-order negative,C256 bounded PASS and all older scopes remain.
C256 precheck INVALID and C255 invalid attempts remain in their execution-recovery addenda.
Historical identities,metric tables and reviews are retained in acceptance/recovery addenda and
in the prior handoff at b377042dcdb903a308da131feb135b0f5362d9de. Do not delete or rewrite history,
accepted sources/tests/logs/checkpoints,or tools/run_c167.ps1.

## Active C267 — paired name-coverage training

Experiment:C267-v5b-paired-name-coverage-training. Stage:V5-B-PAIRED-NAME-COVERAGE-TRAINING.
Question:with matched architecture,initial weights,base questions and800 updates,does teaching
compound-name collisions reduce collapse and support held-out value-pair answers,relative to
equal-length doubled-name-only teaching? This tests a training policy,not an assumed internal cause.

Fresh seeds267001..267005. One actual C252 Full AlignedPrecoreReadout per seed is created through
C256.make_model/C231 factory,then deep-copied into doubled_only and mixed_names. Both14256 parameters.
No accepted learned weights,optimizer state or selected failed model is continued. Common initial
full-state fingerprints match;full/backbone/reader changes and nonmutation during evaluation checked.

Both use two facts,known character pools,distinct values0..3,all source subsets,both languages,
both fact orders,both queries and the existing48-slot byte contract. Profiles exactly follow C265:
doubled uu/vv;shared_prefix uu/uv;shared_suffix uu/vu. Rename consistently in facts and query.
Only visible bytes and zero task IDs reach the model. Offline targets and indices do not enter it.
Normal profile lengths match:13 ASCII or25 Japanese bytes. No canonicalization back to old names.
Control always trains doubled;candidate cycles the three profiles. All other settings and the
same base assignment/language/subset/order/query/target at each update match across the pair.
Rendered-string exposures differ by design;logical-question exposures and update counts match.

## C267 new split,schedule and gate

New two-fact split,NOT inherited C264 projections. Hold out(0,2),(1,3),(2,0),(3,1) in every naming
profile/subset/language/order. The other8 ordered distinct value pairs are TRAIN. Both positions'
digit marginals are balanced:each value twice among TRAIN assignments,once among HOLDOUT.
TRAIN192 logical rows;HOLDOUT96. No held row is optimized. The split is deliberately structured:
held values differ by2 modulo4,training values by1 or3. It is small and not a random benchmark.
Prior inspection of the symbolic family remains a limitation despite fresh initialization.
Dataset SHA256:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.

TRAIN token tables3x192x48 and192 targets. Step s uses epoch=s//4,block=s%4,randperm192 seeded
seed+267000+epoch,and the same48-row slice in both arms. Candidate profile=epoch%3;control profile0.
800 steps=200 complete epochs. Every base row appears200 times. Candidate epochs67/67/66 and
updates268/268/264;control800/0/0. Recorded schedules/exposures are reconstructed in the postcheck.
Reset fit RNG seed+268000 per arm. AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1,batch48.
CPU float64,threads2,deterministic algorithms. No extra updates,seed selection or checkpoint selection.

Final evaluation covers both splits and all profiles,including profiles not trained by control.
Per model72 answer cells and36 two-order cells. Require accuracy>=.90,complete-query-pair>=.80,
evidence/query mask drops>=.35,and two-order consistency>=.80. TRAIN cells16 answers/8 pairs imply
15/16 and7/8;HOLDOUT cells8 answers/4 pairs imply8/8 and4/4. Thus HOLDOUT cell accuracy must be100%.
Two-order minima:TRAIN13/16,HOLDOUT7/8. No pooling away a weak profile,subset,order or language.
Primary PASS iff all five mixed_names states satisfy all criteria. Control gates are separate.
This is a new treatment gate,not a change to the C265 frozen gate or an old result rescue.

Report30 paired HOLDOUT contrasts(5 seeds x3 profiles x2 languages),each48 answers/24 query pairs.
Show correct-answer and same-answer-collapse differences,mixed minus control. Collapse includes
identical outside answers. A reduction in collapse alone is not capability;both models can be wrong.
Primary PASS alone is not treatment advantage either;both arms may pass. No significance claim.
Treatment names are training-seen:success means held-VALUE-pair performance under covered names,
NOT unseen-name transfer,arbitrary identifier understanding or proof of an internal parser.

## C267 workload,provenance and artifacts

Ten models:8000 updates/384000 training presentations. Final evaluation uses TRAIN2x96 and HOLDOUT1x96
chunks for each of3 profiles and3 views:27 forwards/2592 rows. Replay repeats27/2592.
Per model train+final827/40992,including replay854/43584. Total8540 forwards/435840 rows/34160 core calls;
540 evaluation/replay forwards. One new10-state bundle write/load;10 strict loads. Final raw logits
53084160 bytes(about53 MB decimal),not a measured peak-memory figure. Tests,hashing and I/O are extra.

Parent summary path and SHA are the accepted C266 identity above. load_parent invokes actual
C266.validate_result,requires diagnostic PASS and capability_pass_claim=False,checks all6 artifact
hashes/sizes,audit-plan equality and validation-summary equality. Parent data are provenance,not
initialization. No parent learned archive is loaded for this direct contract;inherited inputs remain
hash-protected. Actual context chain C266->C265 supplies C260 core,C256 base,C252 reader,C231 factory.
All repository-local deciding dependencies remain pinned,including lazy helpers.

Protection448 pins/761 inputs=442/748 plus OWN6 and parent summary+SIX artifacts. Direct dependency
union43=five C231 LM sources+C230..C266 helpers+C267. Own24;modules152;loaded3574/focused3573.
Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:4f83a11bd6b2c31d7f1bd23b617772d1eab413e5099d5aafe3c4a34eb453f2d7.
Registration:docs/experiment-ledger-addendum-c267-preregistration.md.
Design:docs/v5b-name-coverage-training-v0.1.md. Acceptance and next registration are separate commits.

Six ignored artifacts plus summary.json:coverage-plan.json,dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Bundle schema fold-c267-coverage-models-v1;
evaluation schema fold-c267-coverage-eval-v1. Raw tensors are FINAL per-split/profile/view outputs.
Strict reload verifies final fingerprint,exact argmax,max raw-logit error<=1e-9 and27/2592/108 replay
counts. Saved postcheck reconstructs schedules,metrics,contrasts and gates without another model
construction,model call or learned-bundle load. Fixed SPLITS order avoids JSON key-order dependence.
Only console logs publish;generated data and learned states stay in ignored runs/.

## C267 post-authoring review

post_authoring_review = PASS
review_target_HEAD = bd57da667a6ebed20340ce9dc2d73c91386eacff
Scope:committed-byte C267 authoring verification with synthetic model/parent fixtures,NOT formal science.

All six committed OWN files were re-fetched and fully read at this immutable review HEAD.
The four locally tested executable files were independently Git-blob hashed and matched exactly:
-benchmark:5a167f078ab5b3aa8052e7995d004a25ca25fc0f;26999 bytes.
-tests:199f5f0e031546807a963f9780a56351148884cd;19469 bytes.
-runner:244cd02670f0ba631406d163ad01ac3e89039d7b;4883 bytes.
-launcher:bdfc538a2f0204ac8afe395732225cce52b9a20d;2639 bytes.
Documentation was re-read/text-reviewed,not independently locally rehashed:
-preregistration:31a17c0b63f52f39be890f85e22294af6356d3df;
-design:a4c39b537c6fba195bbdd6b4bed909c14bbef9ce.

The initial prepublication24-test run found two authoring issues:JSON sorted-key serialization
changed iteration order during saved metric reconstruction,and a source-order test compared calls
on the same semicolon-separated line. Explicit SPLITS iteration and separate run statements fixed
these before the executable files were committed. No scientific model result was obtained or used.
After those fixes:24/24 PASS in5.237s. After remote readback and four executable blob matches:
24/24 PASS in5.306s. No postpublication executable correction was needed.
UTF-8/NUL and Python compile/import checks passed. Recursive LOAD_GLOBAL audit covered110 code
objects,using each function's actual globals and unwrapped decorated functions:zero unresolved names.
Fixed manifest/data hashes passed. Semantic own24 count,all five seeds'200 complete-epoch exposure
checks,three embedded Python block compilation and CLI indices1/none/1,2,3 passed.

Tests use a labeled synthetic Tiny with14256 parameters and four surrogate core calls,not FOLD's
real state-update computation. Test09 executes actual new800-step train_one and strict replay on
Tiny;test08 uses a four-update test-only budget. Test20 substitutes training records but executes
actual new ten-state run/evaluate/replay/analyze/persistence/postcheck. Test19 exercises the actual
parent loader against temporary JSON with a mocked parent validator and forbids learned loads.
Test22's3574 dummy IDs test exclusion logic,not3573 historical tests. No synthetic score is capability
evidence. Full repository import graph and user-local accepted files were not executed here.

Actual C265 context tuple and C256 make_model/fingerprint contracts were re-read;C266 diagnostic
writer/validator fields and counts were reviewed against its published results. Direct-dependency
range/count checks are synthetic and real source/input verification remains required. The existing
active dispatcher was re-read and parses the selected launcher. New launcher guards and runner
ParseFile precede experiment logging/publication. Diff from the C266 log commit shows seven new
paths(acceptance+OWN6),with no accepted source/test/log/runner/dispatcher/CI modification. The extra
acceptance commit corrects only the documented cells hash. Only this activation handoff follows.

Reviewer runtime:Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Container GitHub access failed DNS;
no complete checkout or user-local learned artifacts were available. Neither pwsh nor powershell
is installed;Windows System.Management.Automation.Language.Parser.ParseFile was NOT executed here.
The user command parses dispatcher;dispatcher parses launcher;launcher parses runner before use.
Pending authoritative checks:Windows parser chain,real448/761 precheck,own24 with full repository,
complete3573 regression,ten real Full-model training/evaluation runs,strict checkpoints,persisted
postcheck and log publication. None is claimed complete by this authoring review.
Use FINAL activation HEAD,not review_target_HEAD,parent execution or published-log HEAD.
Re-read final ref before issuing ExpectedHead. C268 remains unregistered until C267 is judged.

## Execution and stop

Use tools/invoke_active.ps1. Formal state has one ACTIVE token resolving to C267.
Parent:runs/c266-v5b-query-pairs-b652a5a2d2ea4dac9b913b64df6d78e0/summary.json.
Order:dispatcher/launcher/runner ParseFile ->Python compile+parent/task precheck ->own24 ->focused3573
->ten-model paired training ->strict checkpoint replay ->saved postcheck ->log publication.
Progress:model1/10..10/10;each model steps200/400/600/800. This is training,unlike the C266 diagnostic.
Valid scientific FAIL is not INVALID. Do not extend the budget,change profiles/rate/split,seeds or
gates to rescue a miss. Operational stale branch/tree/HEAD/ACTIVE conditions SKIP before logs.
Source/artifact/schema/nonfinite/count/replay/test faults require SAME C267 recovery;do not advance.
Repair log-only publication without retraining. User normally sends only 'finished';retrieve
C267 latest.json/latest.log for judgment. Do not move this branch during the user's active run.
No paid API,external corpus,model expansion,production adoption,cleanup,history rewrite or CI change.
Preserve all accepted evidence and recoveries. Gate F NOT PASSED. Judge C267 before C268.
