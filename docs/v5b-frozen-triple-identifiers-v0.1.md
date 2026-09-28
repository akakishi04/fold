# V5-B frozen triple identifiers v0.1 — C270

C269 passed the fixed five-seed query-span gate: span_query5/5 versus eos_query4/5. The positive
result is still limited to name structures that were present during C269 training. C270 therefore
does not train again. It freezes all ten C269 final states and asks whether the same query-source
choice transfers to longer, previously unseen identifier strings built only from familiar bytes.

For each original character pair u,v use exactly three new equal-length naming profiles:
- tripled: uuu / vvv
- shared_prefix2: uuu / uuv
- shared_suffix2: uuu / vuu

For a/b this gives aaa/bbb, aaa/aab and aaa/baa. For 甲/乙 it gives 甲甲甲/乙乙乙,
甲甲甲/甲甲乙 and 甲甲甲/乙甲甲. No three-character identifier string appears in C269 optimization.
All underlying characters, values, delimiters and task structure are familiar. Normal prompt length
remains <=34 bytes, within the existing46-byte payload/48-slot interface.

Keep the exact C267 logical value split. TRAIN rows contain the eight value pairs seen during C269
optimization; HOLDOUT rows contain the four held pairs. Every new identifier string is unseen in both
splits. Reporting both matters: TRAIN-value rows are a cleaner name/length transfer probe, while
HOLDOUT-value rows combine new-name transfer with the already tested held-value dimension.

No new training, optimizer, gradients, learned weights or checkpoint selection occur. For each frozen
state, first replay all accepted C269 two-character outputs exactly, then evaluate all three new name
profiles and all three views, then replay the accepted outputs again. Require unchanged full-state
fingerprints, raw-logit error <=1e-9 and identical argmax before and after the new inputs.

The new task keeps the C267 gates unchanged per split/profile/language/subset/order: answer accuracy,
paired-query correctness, evidence/query mask drops and two-order consistency. The C270 candidate
PASS requires all five frozen span_query states to meet every criterion on both value splits and all
three unseen name profiles. The eos_query states are a matched reference and cannot rescue or fail
the candidate.

A PASS would establish only transfer from trained two-character names to these three-character
familiar-byte constructions. It is not arbitrary-name understanding, natural-language parsing,
unbounded length generalization or Gate F. A FAIL is accepted without retraining or changing the
new profiles, value split, thresholds or previously learned states.
