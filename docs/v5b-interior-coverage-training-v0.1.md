# V5-B interior-coverage training v0.1

## Motivation

C323's integrity-valid diagnosis found all-four same-answer lock in814/1080
mean_last and809/1080 last_only interior groups, much more often than consistent
first- or last-fact following. It did not establish an internal causal mechanism.
The next intervention therefore changes TRAIN coverage, not another readout branch.
The precise scientific question, workload and fixed gate are registered in
experiment-ledger-addendum-c324-preregistration.md and the sealed code manifest.

## Data flow and leakage boundary

50 accepted summary hashes -> C323 recursive artifact verification -> canonical
C319 dataset and original length prompts -> exact C321 interior renderer ->
TRAIN-only projections -> c324_training_templates.build_training_views -> token
arrays and separate teacher labels -> fixed paired schedule -> two native mean_last
models -> original/interior 256-way logits -> unchanged local/masked scorers.

The helper is only a template selector. It must not be mistaken for a canonical
artifact validator. The caller checks both accepted hashes and renderer semantics
before giving TRAIN projections to it. HOLDOUT records never enter fit/model input
construction for training. Known fact values in input are task evidence; targets
remain separate teacher values. Inference gets only tokens and task IDs.

Original:the same nine length/profile tables used by the C319-style control.
Interior4:the three length-four tables alone are replaced with uuvu/uvuu,
uuvv/uvuv and vuvv/vvuv patterns, respectively. These names have equal length,
endpoints and character counts but differ in internal order. The two short lengths
retain their original bytes; both arms retain identical logical schedules/targets.

## Model and optimization boundary

Fresh seed pairs324001..324005; independent storage, exact initial state equality.
No last_only condition, no accepted state reuse, no extra capacity, no prompt-side
matching solver, no logit correction. Native mean_last is checked by the C319
trained_readout context in training, evaluation and checkpoint replay.
C308 core_slow parameter groups and the C319 CE/update arithmetic are retained.
The software preflight uses discarded nonzero-output probes and TRAIN rows only;
it performs no optimizer step and does not select a checkpoint or hyperparameter.

## Decision and failure handling

Candidate learning and original2..6 retention are separate per-seed facts.
Paired HOLDOUT answer and both-query-correct gains are computed from the original
all256 argmax, not a two-value restriction. Rescue/new-error accounting is exact.
All five pairs must meet both absolute criteria and both strict positive gains.
Finite gate failures remain serialized valid negatives; broken source, artifact,
nonfinite, replay or call-count checks prevent execution validity.

## Artifact writer / reader semantics

run writes the complete cohort, including failures, once. It calls the child
load_bundle before all10 checkpoint replays. Each replay checks shape/dtype,
state digest/full fingerprint and exact argmax with1e-9 numerical tolerance.
verify_artifacts checks hashes/sizes before tensor loading; under no_neural it
revalidates the parents, reaggregates saved outputs and verifies checkpoint tensor
digests and every saved JSON file. Neither verifier retrains a model.

## Protection / authoring boundary

Eight OWN paths extend784 pins to792. Five C323 parent-output files plus the eight
new source files extend1478 inputs to1491. The helper is pinned explicitly, and
all deciding-path repository modules/model classes are checked before use.
Parent C323 diagnostics have four JSON output artifacts; C319 model bundles have
a different schema and are NOT treated as C323 outputs or initialization weights.
The50 parent paths use C323 at index0 and C319 at index4. Postcheck CLI order is
output_dir, expected_head, then50 summaries:argv length53, paths=argv[3:].

The own64 tests include explicit synthetic parent/model fixtures and real PyTorch
update arithmetic on a tiny software-only network. They are not a scientific C324
run and not proof that the user's archives or the full5357 regression have passed.
The full suite and actual FOLD native-gradient/parent preflight remain mandatory in
the user execution. Authoring review must reread committed remote bytes; an honest
review report distinguishes these scopes and does not fabricate Windows execution.
