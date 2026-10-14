# C324 preregistration — interior-order TRAIN coverage

Experiment: C324-v5b-interior-coverage-training.
Stage: V5-B-INTERIOR-COVERAGE-TRAINING. Branch: feat/sft-target-loss.
Acceptance base: 88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.
C323 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C321 remains ACCEPTED VALID
NEGATIVE. Gate F remains NOT PASSED. C325 is not registered.
Execution is authorized only by the authoritative handoff after the independent
post-authoring review; this specification does not itself activate the experiment.

## One question and intervention

Can explicit coverage of C321 interior-order names improve held-out binding at the
same training budget, while retaining the original name-task performance?
Use the original and interior4 arms. Both use native mean_last, never last_only.
Only the three length-four TRAIN template tables change. The original
repeat/shared_prefix/shared_suffix slots map respectively to C321
u_dominant/balanced/v_dominant. Length-two/three strings stay identical.
The helper consumes TRAIN-only projections; targets, source IDs, row order, fact
permutations, languages and logical value split stay fixed. No candidate-restricted
decoder, new vocabulary, oracle name matching, extra loss, extra steps or seed search.

## Fixed population and optimization

Fresh initialization seeds 324001,324002,324003,324004,324005.
Paired schedule seeds 324101,324102,324103,324104,324105.
Two independent model copies per initialization: 10 models, 14256 parameters each,
3328 core parameters, 64 slots, width16, four core calls per forward.
C304.LengthReadout and the C319 native mean_last arithmetic are unchanged.
C315.plan_for_order(order,'two_to_four',TRAIN,p312,pairs) defines the schedule.
1200 optimizer steps/model, 48 rows/step, 57600 row presentations/model.
Each of 192 TRAIN rows appears 100 times at each of lengths2,3,4; length1 exposure0.
Training stochastic seed612000; ordinary mean 256-way CE; C308 core_slow AdamW;
other lr.005/core lr.0005, betas.9/.999, eps1e-8, weight_decay0, global gradient clip1.
CPU float64, two threads, deterministic algorithms. No accepted checkpoint is used
as an initialization. Recursive ancestor verification is not new scientific fitting.

## Evaluation and fixed gate

Evaluate all original lengths1..6 plus the three C321 interior profiles, using
TRAIN192/HOLDOUT96, English/Japanese, every fact ordering and all three views:
normal, evidence_blind, query_blind. Original length1 is descriptive only.
Reuse C304.score_length / C321.score_new and their existing C270 local criteria:
normal accuracy>=.90, both-query correctness>=.80, evidence drop>=.35,
query drop>=.35, and both-fact-order correctness>=.80. Do not change a scorer.

For EVERY one of the five seed pairs, success requires:
1. interior4 passes every existing interior local/masked/both-order criterion;
2. interior4 passes every original length2..6 local/masked/both-order criterion;
3. interior4 has strictly more correct HOLDOUT normal answers than original;
4. interior4 has strictly more both-query-correct HOLDOUT pairs than original.
HOLDOUT contrasts aggregate all three profiles and both languages within each seed:
288 answers and144 query pairs per arm/seed. Report rescues AND new errors, including
pair rescues/regressions, with exact conservation. Do not replace all-five by a mean.
Control success/failure and candidate learning/retention are reported separately.

A finite completed run failing this gate is a valid scientific negative, not an
execution failure. Execution-validity, replay and source protection failures instead
require repair of the SAME C324 without changing this scientific specification.

## Exact scientific workload

Per model:1200 training calls/57600 rows +171 evaluation calls/16416 rows;
171 checkpoint-replay calls/16416 rows;4 core calls per model forward.
Total:12000 training steps,576000 training rows,15420 model forwards,
904320 row presentations,61680 core forwards,10 model state loads,
1 child checkpoint bundle load for replay,1 new checkpoint bundle write,0 network calls.
Saved raw-logit payload336199680 bytes, excluding tensor-container overhead and fit traces.
Artifact verification, preflight probes and regression tests are separately scoped
software/verification work; they must never be reported as performance improvement.
Record artifact sizes, elapsed science-process time and process peak RSS including
ancestor verification. VRAM is not measured (null); all model tensors remain on CPU.

## Parent contracts and protection

Require 50 ordered summary hashes, C323..C274, BEFORE parent dispatch.
Parent C323 summary SHA256:
fcc87597395300e45eacabaa94b87b6910093669532279f9ed6c67ec3f84af1f.
Parent scientific execution:1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4.
Parent source blob:9d9dc794ce95d14755e0916b21ebebe2ae2ac176.
Call C323.verify_artifacts(C323dir,49 ancestors,parent execution), then validate its
actual diagnostic fields. Read C319 dataset.json/length-datasets.json from ordered
parent index4 only after recursive verification. Enforce the existing DATA_SHA and
PROMPTS_SHA and C321.check_prompts; JSON diagnostics are not model checkpoints.
Preserve all784 accepted source pins and1478 protected inputs. Add eight OWN files
and the five C323 output files:792 source pins,1491 protected inputs. The template
helper and both test modules are included. Audit all direct helper modules and all
repository-local model classes; no waived path or retroactive protection.

## Persistence and regression

Eight outputs plus summary.json: experiment-plan.json, dataset.json,
original-prompts.json, interior-prompts.json, trained-models.pt, evaluations.pt,
measurements.json, validation-summary.json. Never overwrite an existing output dir.
The checkpoint schema is fold-c324-interior-coverage-models-v1, with exact ordered
identities, native mean_last policy and10 states. Replay checks exact tensor schema,
tensor digest, full model fingerprint, <=1e-9 logits and exact 256-way argmax.
The evaluation schema is fold-c324-interior-coverage-evaluations-v1. Reconstruct all
JSON measurements and gates from saved logits under no_neural. Recheck all file
hashes/sizes, state digests and protected inputs. A status FAIL is still preserved.

Own64 tests = unchanged template-component20 + benchmark44.
Regression:208 parent modules +2 new modules=210;5358 loaded tests;5357 selected.
The ONLY exclusion remains the exact inherited C204 mutable-state test ID in code.
No accepted test changes and no new exclusions. Construct the actual suite and
check unique ordered IDs/counts before running it as one process; do not parallelize
fixtures, skip old tests or replace full regression by the own64 authoring tests.

## Execution and stop

Use tools/invoke_active_v2.ps1 after explicit PowerShell7/ff-only pull/ParseFile.
Dispatcher parses the selected launcher; launcher parses the runner. Wrong branch,
dirty tracked tree, stale ExpectedHead or non-ACTIVE C324 stops before publication.
Validate:50 real ancestors,792/1491 guards,TRAIN substitution/native gradient probes,
own64 and full5357. Execute:10 fits, original/interior evaluation, checkpoint replay,
no-neural saved reconstruction, clean-tree/HEAD postcheck, standard log publication.
No retry loop. No C325 before the formal C324 verdict. A log transport failure does
not justify retraining. Parent code/tests/logs and protected dispatchers are immutable.

## Interpretation boundary

This is explicit-template learnability and held-out VALUE-combination evaluation,
not frozen unseen-name generalization. A positive result supports this coverage
intervention under the fixed budget, not universal identity matching. A negative
result does not prove structural impossibility: training allocation and optimization
remain possible limitations. C321/C322/C323 historical conclusions remain distinct.
