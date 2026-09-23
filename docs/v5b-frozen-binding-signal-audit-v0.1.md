# V5-B frozen binding signal audit v0.1 — C237

## One question

For the six frozen C236 final models, do changes to the queried object or factual assignment
remain numerically distinguishable along the input-to-output path despite the failed final answers?
This is descriptive localization before another training or architecture intervention.

C236 was a valid negative: all12 seed/family/language cells scored4/8 on the16 seen TRAIN prompts,
with0/4 fact/query pairs and zero evidence/query-mask accuracy drop. A score that does not change
is not proof that hidden vectors or output logits do not change. See
`docs/experiment-ledger-addendum-c236-c237.md` for accepted evidence and limitations.

## Fixed path, passive measurement

Use all six C236 step400 states in the accepted order. Freeze their weights; keep the same16 rows,
normal/evidence-blind/query-blind renderings, CPU float64, two threads and deterministic algorithms.
No training, optimization, new checkpoint, checkpoint selection or production model modification.

For each frozen model, run the actual C234 evaluator once without internal capture (three views),
then once with passive hooks (three views). Hooks only clone values; they do not return replacement
outputs. Record the real GRU sequence output at each row's EOS position, readout-normalization
input, normalization output, decoder input and final logits. The captured normalized vector must
be exactly what the decoder receives. A functional linear reconstruction must reproduce its logits.

The authoritative EOS is the last non-PAD token, with a checked BOS/contiguous-prefix/EOS layout.
Do not use the GRU's final recurrent state after processing PAD slots. The Full model's normalization
input is the iterative core's pooled EOS state; GRU-only's is the local encoder's EOS state. Their
origin differs, and the report must not pretend both are the same component.

Passive and plain predictions must agree exactly. Raw logits and metrics must agree within1e-9.
The captured pass must reproduce C236's stored final_probe and all three saved prediction arrays.
Fingerprint checks must match C236 final_sha256 and remain unchanged across all forwards.

## Matched contrasts

Report separately, in each language and model:

1. Query change: facts/order unchanged; queried object and correct target change.
2. Assignment swap: objects/order/query unchanged; the0/1 value assignments and target change.
3. Fact-order reversal: assignment/query unchanged; order changes but correct target stays the same.

Each kind has4 pairs per language. The same row is also contrasted between normal and each of
the two inherited masked views. Masks may change byte length and EOS position as well as content;
these are observations of the inherited rendering, not clean causal interventions on semantics.

Per contrast, save token-position mismatch count; exact tensor equality and linf/l2/relative_l2
at GRU EOS, pooled readout input, normalized readout and256-class logits; both unrestricted argmax
answers; target correctness; signed logit(1)-logit(0); top-two output gap; and softmax mass on0/1.
The answer is NOT restricted to the supplied values. All other byte classes remain eligible.

Relative l2 uses max(norm(left),norm(right)) as denominator, and0 when both norms are0. There is
no epsilon cutoff that turns small nonzero responses into equality. Exact equality is a finite-
precision observation. Magnitudes across different layers have different scales and cannot by
themselves establish where a causal bottleneck lies. A common shift in all logits can have large
raw drift without changing any probability; the digit-logit contrast and argmax are kept separate.

## Workload and integrity gate

Six models x three views x two passes =36 model forwards and576 row presentations.
18 separate functional decoder reconstructions are algebra checks, not additional full-model
forwards. Postcheck reconstruction of persisted contrast metrics also runs no model forwards.

Matched pairs:6 models x2 languages x3 kinds x4 pairs =144.
Masked-row contrasts:6 models x16 rows x2 masks =192. Total336 contrast records,56/model.
Twelve seed/family/language diagnostic cells. New training/optimizer steps/checkpoint writes0.

C237 PASS means diagnostic integrity only: accepted checkpoint/input identity, parent replay,
passive-capture equivalence, unchanged weights, correct trace shapes, complete fixed workload and
persisted-trace/contrast replay. The measured sensitivity and accuracy cannot turn a valid
measurement into FAIL. A missing source pin, bad input/artifact/schema, nonfinite tensor, weight
mutation, replay mismatch or missing work is INVALID / RETRY SAME C237.

## Interpretation boundary

If inputs differ and encoder vectors differ, this rules out exact collapse at that sampled encoder
state, not a more subtle failure to encode useful relations. If intermediate values differ but the
winning answer stays fixed, it does not establish a learned binding or identify the decoder as
the sole cause. If vectors coincide, that describes these states and this precision, not all FOLD
architectures or all possible training. A future causal test would require a separately registered
intervention. C237 does not perform such an intervention.

C236 remains a valid negative regardless of C237 results. No threshold rescue, useful language,
generalization, Full/GRU ranking, Gate F promotion or extra training. Numeric-memory tuning stays
paused. Judge C237 before registering C238.
