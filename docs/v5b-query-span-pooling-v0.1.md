# V5-B query-span pooling v0.1 — C269

C268 validly failed its preregistered five-seed gate: both ordinary CE and the paired-query margin
candidate passed3/5 fresh states. The candidate improved pooled HOLDOUT answers only from1100/1440
to1115/1440 and collapse from114/720 to107/720,with no seed-pass improvement. The auxiliary margin
was already zero at the final TRAIN step in every arm,so another post-hoc margin/weight sweep would
be rescue tuning rather than a clean next question.

C269 changes one structural choice in the existing C252 aligned reader. The control uses the actual
pre-core EOS local state as the reader query. The candidate uses the arithmetic mean of pre-core
local states belonging to the visible query identifier itself. The query span is found only from
input bytes already present in the structured example: positions strictly after the final ';'
(byte59) and before the final '=' (byte61). The final '=' must immediately precede EOS. The span
must be non-empty and contain no delimiter. This includes every UTF-8 byte of Japanese identifiers;
there is no two-character, ASCII-only, target-value or entity-index shortcut.

Everything else remains the actual C252 Full aligned reader: masked pre-core causal states are the
attention memory, the same learned query/key/output maps are used, attention scale stays4.0, PAD is
masked, the actual core runs unchanged, and the residual base remains the post-core EOS state.
The candidate adds no parameter. Control and candidate have identical state_dict keys and14256
parameters. For each fresh seed, the candidate is strict-loaded from the control's complete initial
state into a separate object with no shared parameter storage.

Both arms use ordinary mean cross-entropy only. Both receive the same paired48-row batches, the same
C267192-row TRAIN split, all three TRAIN-seen naming profiles, the same800 updates, AdamW settings
and gradient clip. The paired sampler remains the C268-style96 same-facts/different-query groups,
but uses fresh seeds269001..269005 and seed+269000 shuffle streams. Thus within C269 the changed
factor is query representation, not loss, data coverage, batch composition, update budget or model
capacity.

The primary gate is unchanged: all five span_query models must satisfy every C267 answer-cell,
query-pair, masking and two-order criterion on TRAIN and HOLDOUT across every profile and language.
The eos_query arm is a matched control and cannot rescue or fail the candidate. Report30 paired
HOLDOUT profile/language contrasts in correct answers and same-answer collapse.

This remains a bounded structured-input test. The delimiter rule is hand-specified structure; a
positive result would show that exposing the visible query span to this reader helps this task under
this training policy. It would not prove a general parser, arbitrary-name understanding, a universal
architecture improvement or Gate F completion. A valid miss is accepted; do not retune pooling,
thresholds, seed set or budget after results.
