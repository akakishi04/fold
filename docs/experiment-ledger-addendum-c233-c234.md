# C233 acceptance and C234 boundary

## Formal verdict

**C233 ACCEPTED VALID NEGATIVE. Gate F remains NOT PASSED.**

Scientific execution HEAD: `fedf6c3e5c163d449d1ad793a87d4fa6952deb1d`.
Published log commit: `519d71abe912639869130cb4dff3f196e166b92f`.
Log SHA256: `63e5b22242720deac9b33999cf38b2331ad4069604b866c0801ab6cec0a9a651`.
Summary SHA256: `5e9895008ebf02c72c3b5c00a8668f1c8078feef94dd2fc1eff192d41e8709bf`.
Local summary:
`runs/c233-v5b-core-ablation-f73f95f4afa44668a64b953f1bbad723/summary.json`.

## Execution validity

Published receipt identifies the registered execution HEAD. Focused2753/2753 tests passed in53.150s.
The three GRU-only models each completed400 steps. Parent full-model replay, baseline checkpoint
replay, final artifact checks, protected inputs and clean tracked tree passed.
`run_execution_valid = True`, `all_replays = True`, `baseline_qualified = True`.
The publication commit contains only latest.log/latest.json. Acceptance is based on published
console evidence and its recorded local artifact checks, not a reviewer rerun of local checkpoints.

## Deciding metrics

BPB is evaluated on exactly the same observed C232 split. Lower is better.

| Seed | Full EN | GRU-only EN | Full JA | GRU-only JA |
|---:|---:|---:|---:|---:|
| 232001 | 0.5413168493188328 | 0.4910411857956119 | 0.5247321276142884 | 0.43533578966062153 |
| 232002 | 0.4265834128672163 | 0.5028083066473705 | 0.5515317499163915 | 0.5219413264684115 |
| 232003 | 0.4797497091521084 | 0.49971860443620225 | 0.4488188149083432 | 0.46900804397888435 |

Full wins3 / GRU-only wins3 / ties0. The registered full-advantage requirement was6/6 cells.
Therefore `scientific_status = FAIL`, `core_ablation_gate = False` is a valid negative, not an
execution failure or a reason to rerun the same experiment with relaxed thresholds.
All three baselines qualify: they learn beyond their initialization and the TRAIN-only unigram.
New steps1200; sampled byte presentations38400; full-model retraining0.

Artifacts:
- baseline-models.pt: `0bbe764c832d2fb33b3f51e3838c7178ab7121cf6c2f72a25bda43b2cb0722a3`
- comparison-plan.json: `01459cd555cc15193b1289767cd824d159999faff130d537d16c5895f3f83d39`
- comparisons.json: `7ad45aac3d70cc2a5d8054b4dfcaae36ad169f2434981904e8b657eb053b872c`
- replay-audit.json: `f2a8c96fd6201593f5b7c9326844ab58db94f93fde71d8cd0b29398d666bb551`
- validation-summary.json: `c839db0ed26f0369dcedb6227ae5278ca60904d8636da0d00e49da02d75998e4`

## Interpretation and confounds

The smaller ordinary recurrent backbone is competitive on this tiny template-byte task. C232's
successful learning is not evidence that the iterative FOLD core is necessary or uniquely helpful.
The negative does not establish that the core is universally useless or that the models are
statistically equivalent. There are only three paired seeds, four reused held-out noun/color pairs,
one fixed400-step recipe and unequal capacity (13488 full versus10160 baseline parameters).
No architecture-wide performance or statistical significance claim follows.

Retain both paths; do not select favorable seeds, extend steps, or keep changing baselines to obtain
a full-model win. The numeric-memory track remains paused and prepared_capsule stays optional.

## Next single question

C234 will move from spelling/template prediction to an explicit contextual binding task:
can the unchanged full model answer the requested object's current value, and change that answer
when either the facts or the queried object changes? Keep the GRU-only baseline alongside it.

Use newly registered short EN/JA textual bindings, a grouped held-out value-pair split, balanced
query/position roles, exact single-byte answers and paired fact/query interventions. Train both
unchanged architectures from paired fresh initializations under the same fixed budget. Test actual
answer selection rather than low loss on predictable punctuation. No memory integration, larger
model, outside data or extra optimization. This is still a controlled symbolic text task, not a
public language benchmark or Gate F completion.

C234 is NOT REGISTERED by this acceptance document. See the final preregistration/handoff.
