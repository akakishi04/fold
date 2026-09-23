# C237 acceptance and C238 fixed-cohort sampler boundary

## Formal verdict

**C237 ACCEPTED PASS — diagnostic integrity only.**
C236 and C234 remain ACCEPTED VALID NEGATIVE. C235 remains diagnostic-integrity PASS only.
Gate E PASSED; Gate F NOT PASSED. No binding capability or causal explanation is accepted here.

Scientific execution HEAD: `2dec1314181d62fbdf0a7d4c52007a9360921fd2`.
Published log commit: `f59b0012e488978f5733c4e8669eabc74ae47ad6`.
Published log SHA256: `f4f6328ca74d96f21ee498da3d1d06f2e754d2abb70a51f0a15a0eccc22361db`.
Log bytes: 547866.
Summary SHA256: `056fcbe4ebd2f888c0d5d5aa2761a18cd4229ed4af428e8e298d7af3abf55b32`.
Local summary: `runs/c237-v5b-frozen-signal-audit-8dbdc04fdad84f49b41a78388ad0b7fb/summary.json`.

The log commit is exactly one commit after the execution HEAD and changes only
`docs/experiment-run-logs/c237/latest.json` and `latest.log`.
Acceptance uses published execution/postcheck evidence, not an independent rerun of user-local
checkpoints. The digest above is the publisher's recorded digest; selected log ranges were read,
not independently rehashed as a complete byte stream.

## Execution validity

24 own tests PASS in 1.565s; 2857 focused tests PASS in 62.308s.
Python syntax and source/artifact precheck PASS; 268 source pins / 394 protected inputs.
All six frozen C236 final models completed plain/captured evaluation: 36 full-model forwards,
576 row presentations, 144 paired contrasts, 192 masked-row contrasts and 12 diagnostic cells.
New training steps zero. All parent replays, passive replays and unchanged fingerprints PASS.
Persisted trace/contrast replay PASS; protected inputs preserved; tracked tree clean and execution
HEAD preserved. `diagnostic_status = PASS`; `run_execution_valid = True`.
`capability_pass_claim = False`; `causal_claim = False`.

## Deciding measurements

Aggregate counts below sum the printed per-model/per-language counts, not percentages averaged
across differently sized groups. Query/facts/order have 6 models x2 languages x4 pairs =48 each.
Each mask has 6 models x2 languages x8 rows =96 contrasts.

| Contrast | Encoder EOS different | Same selected answer | Both correct |
|---|---:|---:|---:|
| Query change |48/48|48/48|0/48|
| Assignment swap |48/48|48/48|0/48|
| Fact-order reversal |48/48|48/48|24/48|
| Normal versus evidence-blind |96/96|96/96|48/96|
| Normal versus query-blind |96/96|96/96|48/96|

All printed token_equal and gru_exact_equal counts are zero. Readout and logit linf_max are
nonzero in each printed cell; this establishes a nonzero response within every cell, not by
itself that every individual downstream pair has nonzero difference. Those individual values
remain in the local trace/contrast artifacts.

Example, Full seed234001 English query-change cell (4 pairs): GRU EOS linf is0.162092467677 to
0.178331134894; maximum logit linf0.00908251965231; maximum change in logit(1)-logit(0)
0.00126862026933. All4 answers stay the same and0/4 pairs are both correct.
These are the printed precision and vector-coordinate differences, not causal effect sizes.

## Scientific interpretation and non-claims

The sampled encoder states are not exactly collapsed across these input changes. Numerical
responses also reach readout/logits, but do not yield correct answer switching. This rules out
'no numerical response at all' on the measured path; it does not establish learned binding,
useful representation, query understanding, or the decoder as the unique cause of failure.

Cross-layer scales differ; a raw-logit change can include common shifts. A larger response in one
family is not a capability ranking. Masking can change byte length/EOS. C236's50% result and its
failed paired criteria remain unchanged. More training, another optimizer or architecture-wide
impossibility has not been tested by this frozen diagnostic.

## Accepted artifacts

- contrasts.json: `3449be022b490fb8c67bf47f688e68d9d7b277e235399e671acc2f61aebcb85f` (315236 bytes)
- diagnostic-plan.json: `1e5ab23f80a3cf2b510ce82bdd9f343b53716a6dc9641eb9b09ae6dd165c06ce` (2260 bytes)
- diagnostics.json: `87c37f0b645b0740cd2202c6d85a56a4d1164c5580c6eaa04036501f83627b70` (35560 bytes)
- traces.json: `eee07984fb62d83d1114ffa9476ab410257646dcb61a9c8096c21eb15a0063e0` (1728261 bytes)
- validation-summary.json: `066206986d83833a759d1e36d8d1efd5aab4b95c0693b32c3935b1d9baf06d9f` (295 bytes)

## Next question — fixed complete-cohort sampling

A controlled training intervention is now proposed rather than interpreting sensitivity as ability:
with C236's16 rows, architectures, fresh initial states, optimizer, batch32 and400-step budget
unchanged, does presenting every row exactly twice in every batch permit minimal TRAIN fitting?
C236 sampled32 rows with replacement at every step. The candidate uses indices0..15 repeated twice.
The accepted C236 measurements are the comparator; do not rerun or overwrite C236.

This is a sampler hypothesis, NOT an explanation established by C237. Complete-cohort sampling
changes joint coverage, per-batch label balance and stochastic-gradient variability together; it
does not isolate label imbalance alone. The loss, learning rate, model size and update count must
not change with it. Success would still be fitting16 seen prompts, possibly memorization, not
held-out language/generalization or Gate F. A valid miss remains a valid negative.

This acceptance record does not register C238. Separate preregistration and independent
post-authoring review must precede activation. Numeric-memory tuning stays paused.
