# V5-B grouped bilingual learning pilot v0.1

## Question

With the exact C231 model and prefix-evaluation convention, does a fixed small training budget
reduce held-out noun/color-combination byte loss below the same initialization and a TRAIN-only
smoothed unigram reference, separately for English and Japanese?

C231 verified the instrument, not language skill. C232 now changes the weights through training.
This is still a bounded authored-template pilot, not a useful conversational model or general
benchmark. The numeric-memory optimization track remains paused. Gate F remains NOT PASSED.

## Dataset and split unit

Four nouns: box/book/ball/umbrella and corresponding 箱/本/玉/傘.
Four colors: red/blue/white/black and corresponding 赤い/青い/白い/黒い.
Two templates per language:

```text
The {noun} is {color}.\n
A {color} {noun} is here.\n
{noun}は{color}。\n
{color}{noun}がある。\n
```

There are64 sentences. A pair is EVAL iff (noun_id+color_id)%4==0. All four realizations of a
noun/color pair, across language and template, stay on the same side of the split. Do not split
individual prefix rows randomly: that would expose other portions/realizations of the same pair.

TRAIN:12 pairs,48 sentences,948 UTF-8 bytes (492 English/456 Japanese).
EVAL:4 pairs,16 sentences,316 bytes (164 English/152 Japanese).
All vocabulary and templates are already represented in TRAIN. Only selected combinations are
held out. No claim of unseen vocabulary, unseen syntax or public-corpus generalization follows.

Dataset SHA256: `1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200`.
The generator and metadata are source-controlled; generated dataset.json is local-only under runs/.

## Model and objective

Reuse C231.new_model(seed), with the same uncompressed V5-B ShortByteLanguageModel:
13488 total parameters, width16,48 slots,2 modules,2 internal steps, fixed TASK_NEXT=0.
Do not substitute the legacy FoldLanguageModel, a compressed/shared-basis path or the memory stack.
The fixed-route reference computes both branches but selects NEXT; this is not learned routing.

Use C231.document_rows(): BOS + observed prefix + prefix-boundary EOS + PAD. The scorer/trainer
has the next real byte separately. EOS is an adapter boundary, not a predicted future ending.
Japanese prefixes may end in the middle of a UTF-8 sequence and remain bytes. No special-token loss.
The longest sentence is26 bytes, below the fixed-slot limit. No truncation or variable-length
runtime is introduced.

TRAIN tensors alone enter fit(). It receives no EVAL tensors, per-language labels or EVAL scores.
Uniform sampling over TRAIN byte positions, with replacement, uses a CPU generator seeded seed+1000.

## Fixed training budget

Seeds232001/232002/232003. Fresh initializations of the same architecture, not continuation from
C231's untrained artifacts. CPU float64, threads2, deterministic algorithms.
AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0; gradient clipping L2 norm1.0.
400 steps per seed; batch32. Total1200 steps and38400 target-byte presentations.

No early stopping, EVAL-based checkpoint selection, seed replacement, learning-rate search or
budget increase. Evaluate the final400-step weights even when loss or generation is disappointing.
Nonfinite training loss/gradients stop as an invalid execution; a complete finite learning failure
is a valid negative. Do not change the gate to turn that negative into PASS.

## Comparisons and metrics

Record before/after train and EVAL NLL sums and bits per byte (BPB), weighted by byte counts rather
than per-document means. Report overall, English and Japanese separately.

References:
1. The exact same seed's untrained initialization.
2. Per-language byte frequencies estimated from TRAIN only, with add-one smoothing over256 values.

The unigram is a weak calibration baseline with language identity supplied by metadata. It is not
parameter-matched or compute-matched, and beating it does not establish a benefit from the FOLD core
versus an ordinary GRU/Transformer. Such neural comparisons require separate registration.

For each trained checkpoint, record four greedy bytes from each EVAL sentence's first8 observed
bytes through the existing C231 generation method. These short hex continuations are descriptive,
not a fluency or semantic-answer gate. Restore the serialized checkpoint, compare EVAL logits
within1e-9 and reproduce every continuation exactly.

## PASS and non-claims

For every seed:
- aggregate TRAIN BPB must decrease;
- English EVAL BPB must be strictly below both its initial BPB and English unigram BPB;
- Japanese EVAL BPB must be strictly below both its initial BPB and Japanese unigram BPB;
- weights must change, checkpoint fingerprints must round-trip, reload error <=1e-9 and generation
  replay must match.

A tie is not PASS. There is no100% byte-accuracy requirement: some continuations are intrinsically
ambiguous from their prefixes. General language competence, semantic compositional reasoning,
conversation quality, many-factor memory, compression, useful speed and Gate F/G are not established.
Even held-out BPB gains may come from learning common spelling and formatting rather than
understanding noun/color relationships. Preserve this limitation when interpreting results.

## Runtime, artifacts and safety

Use the normal active launcher and user-local authoritative environment.32 new tests precede2721
focused regression tests, then the fixed-budget experiment. Progress prints every100 training steps.
All generated data/checkpoints remain ignored in runs/. Five artifacts: learning-plan.json,
dataset.json, trained-models.pt, measurements.json, validation-summary.json, plus summary.json.
Store initial/final fingerprints, training workload/time, per-language metrics and replay evidence.
No external calls, paid services, new dependencies, CI changes or destructive cleanup.
