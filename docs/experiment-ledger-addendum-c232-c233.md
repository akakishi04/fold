# C232 acceptance and C233 core-ablation boundary

## Formal verdict

**C232 ACCEPTED PASS. Gate F remains NOT PASSED.**

Scientific execution HEAD: `5fced21f02448e5b1047ef661186ce9b5c6bdb02`.
Published log commit: `3f67a03bdd5e5bc07e9324d8a7ea830ea798b7b7`.
Log SHA256: `0c328cdc40d62bfee0523e685981e35327846f3124f7fee876839649eedaecf1`.
Summary SHA256: `df75e3956a6bfaa37aaebdb12f3d189a10010576f0d9fa8709e5e399e1da75d2`.
Local summary: `runs/c232-v5b-bilingual-learning-67b366b0db07449185a18bd0bbe7b996/summary.json`.

Own32 tests passed in1.390s; focused2721/2721 passed in60.495s. Source/artifact prechecks and final
postchecks passed; protected inputs preserved; tracked tree clean; run_execution_valid True.
Publication changed only latest.log/latest.json. Acceptance uses published evidence and recorded
local postchecks, not a reviewer rerun of user-local checkpoints.

## Deciding results

All three13488-parameter instruments completed400 training steps (1200 total,38400 sampled TRAIN
byte presentations). Each seed reduced aggregate TRAIN BPB, and final EVAL BPB beat both its own
initialization and the TRAIN-only unigram separately in English and Japanese.

| Seed | Initial EN EVAL BPB | Final EN | Initial JA EVAL BPB | Final JA | Final aggregate TRAIN |
|---:|---:|---:|---:|---:|---:|
| 232001 | 8.139344152 | 0.541316849 | 8.656696136 | 0.524732128 | 0.522918493 |
| 232002 | 8.127756147 | 0.426583413 | 8.573135698 | 0.551531750 | 0.479480007 |
| 232003 | 8.243823111 | 0.479749709 | 7.797179309 | 0.448818815 | 0.463904134 |

TRAIN-only unigram EVAL BPB: English4.579441272; Japanese4.642439365.
All weights changed, all checkpoint fingerprints round-tripped, EVAL reload error0 and all48
four-byte generation replays matched. Training times12.1571/10.9846/9.2021 seconds are descriptive.

Artifacts:
- dataset.json: `1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200`
- learning-plan.json: `09f2a463981d49680ca66940698baf363731adda9fda8718c5b59fdc281b80c4`
- measurements.json: `ca14020688c9993edde9d176d596c7ffc1704ddbf78ab55520abbc48f5351c04`
- trained-models.pt: `c26e7bb71a9e9a882561165ef91e94b9c2ff257a0d39aa8166654c995e042a7b`
- validation-summary.json: `d7084ad67ee1072aa1c985c5d62ae958ce7771994db18bd29530442486e04ded`

## Interpretation and confounds

The fixed-route uncompressed V5-B model learns byte-pattern regularities that lower loss on the
registered held-out noun/color combinations. This is actual training, unlike the untrained C231
evaluator audit. It is not evidence of useful conversation or general reasoning.

The corpus contains only64 authored template sentences,48 TRAIN/16 EVAL. EVAL consists of four
underlying pairs with language/template realizations, not16 independent semantic tests. Vocabulary
and grammar are seen in TRAIN. Teacher-forced byte loss is dominated by many predictable spelling
and formatting positions; low BPB does not prove noun/color understanding. Generated four-byte
fragments were replay checks, not semantic answer tests. The unigram is a weak reference.

The GRU front-end itself is learned. Beating a unigram does not establish that the FOLD core is
necessary or more useful than the ordinary recurrent front-end alone. Do not infer a FOLD-specific
advantage from the loss reduction.

## Next single question

C233 will remove only the fixed-routing iterative core, retain the same initial embedding/GRU/
normalization/decoder weights, and train this GRU-only ablation from the beginning on the same
TRAIN rows with the same seed-indexed sampling and400-step budget. Compare it against the frozen
accepted C232 checkpoints after verifying their replay.

This is a backbone-matched ablation, not a parameter-matched architecture contest: removing the
core reduces total parameters from13488 to10160. An advantage for the full model cannot separate
extra capacity from the iterative architecture; a competitive smaller ablation would weaken the
claim that the core is needed for this pilot. The already observed EVAL split is reused for this
registered diagnostic, not newly independent confirmation. No tuning or seed replacement.

C233 is NOT REGISTERED by this acceptance document. See the handoff/preregistration for permission.
The numeric-memory track stays paused; no Gate F waiver, model-scale increase or external data.
