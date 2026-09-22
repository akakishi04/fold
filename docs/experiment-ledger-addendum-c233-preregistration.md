# C233 preregistration — backbone-matched core ablation

**C232 ACCEPTED PASS. C233 ACTIVE / NOT YET JUDGED. C234 NOT REGISTERED.**
Stage V5-B-BACKBONE-MATCHED-CORE-ABLATION. Gate E PASSED; Gate F NOT PASSED.
No Gate G promotion or numeric-memory optimization is implied.

## One scientific question

With the same common initialization, TRAIN minibatches and400-step budget, does the full C232
model outperform a freshly trained version with the iterative fixed-routing core removed?

Changed: remove the core from the comparison model and train the remaining backbone from matching
initial weights. Fixed: C232 data/split, byte adapter, common initial embedding/GRU/norm/decoder,
seed-indexed sample order, optimizer recipe, training steps and precision. No trained common
weights are copied to the baseline. The full model is restored for replay only, not retrained.

## Accepted parent

C232 execution HEAD: `5fced21f02448e5b1047ef661186ce9b5c6bdb02`.
Published log commit: `3f67a03bdd5e5bc07e9324d8a7ea830ea798b7b7`.
Summary SHA: `df75e3956a6bfaa37aaebdb12f3d189a10010576f0d9fa8709e5e399e1da75d2`.
Validation SHA: `d7084ad67ee1072aa1c985c5d62ae958ce7771994db18bd29530442486e04ded`.
Measurements SHA: `ca14020688c9993edde9d176d596c7ffc1704ddbf78ab55520abbc48f5351c04`.
Checkpoint SHA: `c26e7bb71a9e9a882561165ef91e94b9c2ff257a0d39aa8166654c995e042a7b`.
Dataset SHA: `1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200`.
Local summary:
`runs/c232-v5b-bilingual-learning-67b366b0db07449185a18bd0bbe7b996/summary.json`.

Parent record adapter checks seeds, parameter/workload identities, accepted learning criteria,
fingerprints, byte counts and NLL/BPB meaning. Checkpoint loader requires
fold-c232-trained-byte-models-v1, ordered seeds and three states. Full EVAL metric drift must be
<=1e-9 and generation records identical before the baseline is judged.

## Fixed data, model and training

Same64 authored EN/JA sentences; TRAIN48/948 bytes and EVAL16/316 bytes. Pair grouping and all
language/template realizations remain fixed. These are four held-out semantic pairs on an already
observed split, not independent confirmatory data. No EVAL inputs enter training.

Full13488 versus GRU-only10160 parameters; width16,48 slots. Baseline retains only embedding, GRU,
readout norm and decoder. This is not matched capacity or compute. Common weights are copied from
the exact initial full model before accepted trained full weights are loaded. Copy storage is
independent; no dormant core weight is counted as active baseline capacity.

Seeds232001/232002/232003, paired with C232. CPU float64, threads2, deterministic algorithms.
AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0, gradient L2 clipping1.0.
400 steps/seed, batch32, uniform TRAIN-byte sampling with replacement using CPU seed+1000.
Total new steps1200, new byte presentations38400; full retraining0. No early stop, tuning, seed
replacement or EVAL-based checkpoint selection. Compare final step400 only.

## Fixed gate and interpretation

First require baseline qualification for every seed: aggregate TRAIN BPB decreases; each language's
EVAL BPB beats that baseline's own initialization and the TRAIN-only smoothed unigram.
An unqualified baseline is INCONCLUSIVE for superiority and must never be counted as a full win.

Then require full BPB strictly lower in every one of the six seed/language cells. Report full-minus-
baseline BPB deltas, full wins, baseline wins and ties separately. Exact ties fail the full-advantage
gate. Qualification, all checkpoint/final-generation replays and fixed workload are required.

Full wins do not separate extra capacity from recurrence. Competitive ablation results weaken
necessity only on this small task. Same hyperparameters are a budget-controlled diagnostic, not
independent tuning of both architectures. No general language, speed or Gate F superiority claim.

Complete finite qualified gate misses are scientific valid negatives. Baseline qualification
failure is a completed but inconclusive comparison. Source/artifact/schema/nonfinite/replay defects
are INVALID / RETRY SAME C233. Do not change thresholds after observing outcomes.

## Authoring and protection

OWN6:
- fold_lm/v05_benchmarks/model_c233_core_ablation.py
- tests_lm/test_v05_c233_core_ablation.py
- tools/run_c233.ps1
- tools/invoke_c233.ps1
- this preregistration
- docs/v5b-backbone-matched-core-ablation-v0.1.md

Parent sources238 + OWN6 =244. Parent protected inputs334 + parent summary/artifacts6 + OWN6 =346.
Nine deciding source dependencies: five C231 language/import sources; C231 evaluator/factory;
C232 data/scoring helpers; C230 audit entry; C233 benchmark. Transitive parent dependencies remain
protected. No accepted source/test/log was changed and the existing draft benchmark is unchanged.

New tests32, regression modules118, loaded2754, focused2753. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Five artifacts: comparison-plan.json, baseline-models.pt, comparisons.json, replay-audit.json,
validation-summary.json. Outputs and weights stay ignored under runs/. Console/receipt publishing
is through the existing tools/publish_experiment_log.ps1 only.

Manifest SHA: `01459cd555cc15193b1289767cd824d159999faff130d537d16c5895f3f83d39`.

## Authoring interruption and review

The previous test-file creation was blocked and no C233 execution was authorized. After the user's
renewed request, the standard GitHub create_file operation succeeded for that path; no alternate
write route was used. This is resumed authoring, not same-C scientific execution recovery.
Acceptance of C232 remains unchanged and no new experiment number is consumed.

`post_authoring_review = PENDING`

Initial targeted authoring run:30/30 tests passed in1.010s on Python3.13.5 / PyTorch2.10.0+cpu.
Tests use synthetic parent fixtures with real embedding/GRU/norm/decoder layers and real short
optimizer steps. Full-run adapter testing simulates training/evaluation and preserves a valid
negative; it is not accepted-checkpoint science or a400-step baseline-quality result.

Pending in this environment: actual parent TRAIN-only smoke test31; historical suite test32 and
all2753 regression tests; Windows PowerShell AST; local-only accepted checkpoint/artifact replay;
formal1200-step baseline run. Container DNS cannot resolve raw.githubusercontent.com, and pwsh is
not installed. Connector source reads succeed. Do not claim these pending checks are already PASS.

After all OWN files are committed, re-fetch remote code/test/runner/launcher and compare Git blobs
with tested copies. Rerun targeted tests and compile embedded Python. Review fixed manifest/data,
parent generation/loader semantics, copy-before-trained-load ordering, sampler identity, complete
launcher guard ordering, source dependency coverage and all counts. Record review HEAD and scope.
Only then issue the standard invoke_active.ps1 command.

## Stop

C232 does not need rerunning. Run32 own tests,2753 focused tests, then C233 only after review PASS.
Judge C233 before C234. Gate F remains NOT PASSED. No larger model, external data, paid API,
cleanup, history rewrite, new CI or Actions-storage change is part of this experiment.
