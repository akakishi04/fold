# V5-B training-only distractor erasure v0.1 — C246

## One question

Can replacing half of C244's scheduled training presentations with the same prompt minus only
the nonqueried value improve performance on the original, fully observed held-out pairs?
This is a training-input intervention, not a production masking fix or another masked-score gate.

C245's frozen-model diagnostic improved pooled HOLDOUT accuracy from80/192 to141/192 when the
other value was hidden, but those modified input strings coincide with masked TRAIN forms.
They also identify the answer-bearing field by leaving only its value visible. These are important
reasons not to claim general binding or novel-pair generalization from that score.

The new hypothesis is that occasional explicitly simplified training inputs could help the model
learn a useful representation that survives when both values are present. It might instead learn
a separate easy copying task, or lose normal-task accuracy because normal exposures are halved.
The ordinary unmasked endpoint distinguishes those outcomes. No predicted success is assumed.

## Fixed data and training views

Preserve the exact C244 TRAIN64/HOLDOUT32 partition, row order, names, values, labels and provenance.
Do not promote any HOLDOUT row into TRAIN. Construct only TRAIN's additional other_value_blind
view using the accepted C245.masked_prompt and tensors functions. A single factual ASCII digit
is changed to '?' using the visible query, not the target label. Preserve all other bytes and EOS.
The selected location is an explicit relevance/copying cue during training, not learned selection.

Keep C244's row schedule:old block32 then added block32, alternating for400 updates.
Use a four-update view cycle:
1. old block, other value hidden;
2. added block, other value hidden;
3. old block, ordinary full evidence;
4. added block, ordinary full evidence.

Repeat100 times. Final update400 is normal-added. Every TRAIN row is presented200 times:
100 ordinary and100 other-hidden. Each block/view cell receives100 updates. Batch32 is unchanged.
The actual input of every training forward is checked independently against the row/view schedule.
No block index, step number, row ID, target or mask flag is passed as a separate model input.

The original normal HOLDOUT strings are disjoint from both forms of TRAIN input. Selectively
masked HOLDOUT would overlap and is therefore not a capability endpoint and is not evaluated by
C246. Original evidence_blind/query_blind remain diagnostic controls, as in C244.

## Fixed model and optimization

Create six fresh models using seeds234001/234002/234003. Match C244.initial_sha256, not its trained
final fingerprint. Construct the common-weight GRU-only copy before either paired model trains.
Full13488/GRU-only10160 parameters,width16,48 slots,256-way unconstrained byte output.
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,400 updates.
CPU float64,threads2,deterministic algorithms. No continued parent training or parent-model inference.

The fit AST matches C244 except the progress label and the model input expression selecting one
of the two views. Row indices, targets, loss and optimizer are unchanged. The unused seed+1000
sampler remains inert. There is no additional loss, teacher inference or extra forward per update.

Total training presentations are fixed. Normal presentations fall from76800 to38400; the other
38400 use the simplified view. Any result is attributable only to this specified training recipe,
not uniquely to removal of interference, copying cues, regularization or internal architecture.

## Evaluation and comparator

Use C242.evaluate through the same C244 context:normal, both-values-hidden and query-hidden views.
Initial scoring is TRAIN only. Final TRAIN/HOLDOUT scoring occurs after step400 and after saved
checkpoint reload. No held-out metric controls optimization, seed selection, stopping or another run.

Require all Full seed/language cells to pass BOTH TRAIN and HOLDOUT using unchanged C244 criteria:
normal accuracy>=0.90, fact/query/order pair both-correct>=0.80, both mask drops>=0.35.
TRAIN:32 rows/language,16 pairs per kind; integer minima29/32 answers and13/16 pairs.
HOLDOUT:16 rows/language,8 pairs per kind; minima15/16 answers and7/8 pairs.
GRU-only is independent. Report TRAIN_CRITERIA_MISS,RECOMBINATION_MISS,BOTH_PASS with actual metrics.
A valid miss is ACCEPTED VALID NEGATIVE; an integrity fault is INVALID / RETRY SAME C246.

Store C244's final metrics on exactly these same rows as c244_comparator. They are accepted saved
evidence, not a freshly repeated baseline or independent replication. Report per-seed/language
normal accuracy and differences, never substitute C245's selective score for this comparator.
A pass is bounded normal-input recombination only. Gate F remains NOT PASSED.

## Workload and integrity

6x400=2400 updates/76800 training presentations; normal38400/masked38400.
Identical C244 scoring workload:90 scoring forwards/4608 scoring rows;
2490 total forwards/81408 total rows. Before reload409 calls/13280 rows per model; after415/13568.
One new six-state bundle, no trained parent bundle load. No scientific network call.

Require fresh fingerprints, updated weights, non-mutating evaluation, exact schedule counts,
strict checkpoint schema/order/final identity, exact prediction replay and logit/metric error<=1e-9.
Reuse accepted C244.replay_one and summarize with the actual C242 fitting module; do not guess
parent helper signatures. Postcheck verifies source/input/artifact hashes, plan, partition,
initial/comparator identities and every child discrete metric from saved answers.

No output correction, selective inference masking, expanded model, larger training budget, paid
API, external data, cleanup/history rewrite or production runtime change. Numeric-memory tuning
remains paused. Judge C246 before registering C247.
