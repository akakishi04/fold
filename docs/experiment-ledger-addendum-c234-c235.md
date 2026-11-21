# C234 acceptance and C235 frozen-diagnostic boundary

## Formal verdict

**C234 ACCEPTED VALID NEGATIVE. Gate F remains NOT PASSED.**

Scientific execution HEAD: `c225c2d82636085e2d639878738e1b9a7aa37b42`.
Published log commit: `930fa77881d60558b3199b980f139ddef8bcb6ee`.
Log SHA256: `414e2de1fafa2fe86fb84bdc18a9477100086133df938a10b0244ad446e38de8`.
Summary SHA256: `a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`.
Local summary: `runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/summary.json`.

## Execution validity

32 own tests passed in2.037s;2785 focused tests passed in50.439s. Six models completed400 steps each,
2400 total and76800 answer presentations. All checkpoint/prediction replays passed, weights changed,
protected inputs and execution HEAD were preserved, tracked tree was clean, run_execution_valid True.
The publication commit changes only latest.log/latest.json. This verdict uses published evidence
and the recorded local artifact postcheck, not an independent reviewer rerun of local checkpoints.

Scientific status FAIL, full_binding_gate False and gru_binding_gate False are valid ability misses,
not execution defects. Do not rerun C234 or relax its thresholds.

## Deciding results

Each language has96 EVAL rows. Counts below are exact correct answers, not rounded percentages.

| Seed | Full EN | Full JA | GRU-only EN | GRU-only JA |
|---:|---:|---:|---:|---:|
| 234001 | 24/96 | 25/96 | 31/96 | 37/96 |
| 234002 | 24/96 | 24/96 | 39/96 | 36/96 |
| 234003 | 19/96 | 19/96 | 30/96 | 33/96 |

Full accuracy19.79%-26.04%; GRU-only31.25%-40.625%; registered threshold90%.
The always-first/always-last observed-value baselines achieve50%, constant digit25% on this balanced
fixture. These comparisons do not imply a formal significance test or exact statistical chance.

Full query-pair both-correct counts: EN0/48 for every seed, JA2/48 for234001 and0/48 for the rest.
GRU-only query-pair both-correct is0/48 in every seed/language cell. Other registered80% pair and
35-point evidence/query-mask-drop criteria also do not pass. C234 did not establish contextual
object/value binding for either architecture at this fixed budget.

Final sampled TRAIN-batch NLL was about0.66-0.79, but C234 did not record an exhaustive TRAIN
accuracy evaluation. Those last-batch losses must not be treated as proof that training examples
were solved. It remains unresolved whether failure is already present on TRAIN, concentrated on
held-out value-pair contexts, or both.

## Accepted artifact identities

- binding-plan.json: `0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38`
- dataset.json: `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`
- measurements.json: `23f822d0a05faac176efc767b5702a21763946b295a76c503f01abc965c776c3`
- trained-models.pt: `711dd636597d5ec575136bd780ac303eb21ed6198d411f977bb20c67fd20bd26`
- validation-summary.json: `655dc04bd3509246c432eb8817699b5685ca300df612515d55358d78e634b629`

## Interpretation boundary and next question

The positive C232 result was byte-pattern learning in short templates. It did not establish
understanding, and C234 now supplies a negative result on a direct, small binding task.
C233's lack of consistent core advantage remains unchanged. Neither result proves all FOLD designs
impossible, but neither supports useful general language/reasoning or a core-specific advantage.

Next, freeze all six C234 models and evaluate the complete TRAIN and EVAL sets with the same
normal/evidence-blind/query-blind views. Replay the recorded EVAL predictions exactly, then report
TRAIN/EVAL accuracy, paired query correctness, supplied-value selection and unchanged answers to
changed queries. This localizes the observed failure before any architecture or training change.

C235 is a diagnostic audit, with no additional learning, altered split or threshold rescue. It must
not change C234's verdict. It is NOT REGISTERED by this acceptance document; see current handoff
and the separate preregistration. Numeric-memory tuning remains paused.
